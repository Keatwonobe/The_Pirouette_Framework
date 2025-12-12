import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import maximum_filter
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 512                 # High resolution for precise alignment
K_REALITY = 1.0             # We test this in the "Real" configuration
CHAOS_DAMPING = 5.0         # To isolate the dots
TRAVELER_THRESHOLD = 70     # Percentile of chaos defining a "Pathway"

# ======================
# 1. OPTIMIZED ENGINE (Reused)
# ======================

def get_alms_and_coords(fits_path, lmax, n_res):
    print(f"[*] Loading CMB Data...")
    try:
        data = fits.getdata(fits_path)
        if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else: cmb = data.astype(np.float64)
        cmb[np.isnan(cmb)] = np.nanmean(cmb)
    except FileNotFoundError:
        print("[!] File not found.")
        sys.exit(1)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    n_theta_alm = lmax * 3; n_phi_alm = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta_alm)
    p_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')
    
    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta_vec = np.linspace(0, np.pi, n_res)
    phi_vec = np.linspace(-np.pi, np.pi, n_res)
    return alms, theta_vec, phi_vec

def precompute_profiles(alms, lmax, theta_vec):
    print(f"[*] Separating Spectral Bands (Universes vs Travelers)...")
    m_range = np.arange(-lmax, lmax + 1)
    n_m = len(m_range); n_theta = len(theta_vec)
    zeros_phi = np.zeros_like(theta_vec)
    
    # We need:
    # 1. L=10 and L=20 (The Universes)
    # 2. Substrate (The Traveler Pathways)
    profiles = {
        'L10': np.zeros((n_m, n_theta), dtype=np.complex128),
        'L20': np.zeros((n_m, n_theta), dtype=np.complex128),
        'Substrate': np.zeros((n_m, n_theta), dtype=np.complex128)
    }
    
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) not in alms: continue
            term = alms[(l, m)] * sph_harm(m, l, zeros_phi, theta_vec)
            
            if l == 10: profiles['L10'][i, :] += term
            elif l == 20: profiles['L20'][i, :] += term
            else: profiles['Substrate'][i, :] += term
            
    return profiles, m_range

def synthesize_band(profile_matrix, m_range, phi_vec, k):
    m_col = m_range[:, np.newaxis]
    phi_row = phi_vec[np.newaxis, :]
    phase_matrix = np.exp(1j * m_col * k * phi_row)
    field = (profile_matrix.T @ phase_matrix).real
    return field

def get_gradient_magnitude(field):
    gy, gx = np.gradient(field)
    return np.sqrt(gx**2 + gy**2)

# ======================
# 2. CENSUS LOGIC
# ======================

def find_universes(field, neighborhood_size=20):
    """
    Finds local maxima (The Dots) in the field.
    Returns: binary mask of universe locations.
    """
    # 1. Normalize
    field_norm = (field - field.min()) / (field.max() - field.min())
    
    # 2. Find Peaks
    local_max = maximum_filter(field_norm, size=neighborhood_size) == field_norm
    
    # 3. Filter weak peaks (noise)
    # We only want the "Bright Dots" (Top 10% of peaks)
    peak_values = field_norm[local_max]
    threshold = np.percentile(peak_values, 50) # Take top 50% of the peaks
    
    universe_mask = (local_max) & (field_norm > threshold)
    return universe_mask

# ======================
# 3. MAIN EXECUTION
# ======================

def run_universality_test():
    # A. Setup
    alms, theta_vec, phi_vec = get_alms_and_coords(FITS_PATH, LMAX, N_RES)
    profiles, m_range = precompute_profiles(alms, LMAX, theta_vec)
    
    print(f"[*] Synthesizing Reality (k={K_REALITY})...")
    
    # B. Generate the Maps
    # 1. The Universes (L10 + L20)
    #    We sum them to get the full "Foam"
    map_10 = synthesize_band(profiles['L10'], m_range, phi_vec, K_REALITY)
    map_20 = synthesize_band(profiles['L20'], m_range, phi_vec, K_REALITY)
    
    # Apply Chaos Filter to isolate dots
    chaos_10 = get_gradient_magnitude(map_10)
    chaos_20 = get_gradient_magnitude(map_20)
    
    clean_10 = map_10 * np.exp(-CHAOS_DAMPING * (chaos_10/np.max(chaos_10)))
    clean_20 = map_20 * np.exp(-CHAOS_DAMPING * (chaos_20/np.max(chaos_20)))
    
    # Find Dots
    print("[*] Conducting Census of Universes...")
    dots_10 = find_universes(clean_10, neighborhood_size=15)
    dots_20 = find_universes(clean_20, neighborhood_size=10) # Smaller bubbles
    
    total_universes = np.sum(dots_10) + np.sum(dots_20)
    
    # 2. The Traveler Pathways (Substrate Chaos)
    map_sub = synthesize_band(profiles['Substrate'], m_range, phi_vec, K_REALITY)
    traveler_chaos = get_gradient_magnitude(map_sub)
    
    # Define Pathways (Top X% of Chaos)
    path_threshold = np.percentile(traveler_chaos, TRAVELER_THRESHOLD)
    traveler_mask = traveler_chaos > path_threshold
    
    # C. The Correlation Test
    print("[*] Testing Universality (Intersection Check)...")
    
    hits_10 = np.sum(dots_10 & traveler_mask)
    hits_20 = np.sum(dots_20 & traveler_mask)
    total_hits = hits_10 + hits_20
    
    hit_rate = (total_hits / total_universes) * 100
    
    # Random Baseline Calculation
    # (Area of Traveler Mask / Total Area) * 100
    baseline_chance = (np.sum(traveler_mask) / traveler_mask.size) * 100
    
    print(f"\n" + "="*40)
    print(f"       TRAVELER UNIVERSALITY TEST       ")
    print(f"="*40)
    print(f"Detected Universes (L10): {np.sum(dots_10)}")
    print(f"Detected Universes (L20): {np.sum(dots_20)}")
    print(f"Total Population:         {total_universes}")
    print(f"-"*40)
    print(f"Traveler Surface Area:    {baseline_chance:.2f}% of Sky")
    print(f"Universes on Pathways:    {hit_rate:.2f}%")
    print(f"Enrichment Factor:        {hit_rate / baseline_chance:.2f}x")
    print(f"="*40)
    
    # D. Plotting
    fig = plt.figure(figsize=(12, 12), facecolor='#050505')
    
    # Overlay Map
    plt.imshow(traveler_chaos, cmap='gray', origin='lower', extent=[-180, 180, -90, 90], alpha=0.6)
    
    # Plot Pathways (The "Lava")
    plt.contour(traveler_mask, levels=[0.5], colors='orange', linewidths=0.5, extent=[-180, 180, -90, 90], origin='lower', alpha=0.5)
    
    # Plot Universes
    y10, x10 = np.where(dots_10)
    y20, x20 = np.where(dots_20)
    
    # Convert pixels to coords for scatter
    def pix_to_deg(y, x):
        lon = (x / N_RES) * 360 - 180
        lat = (y / N_RES) * 180 - 90
        return lon, lat
        
    l10, b10 = pix_to_deg(y10, x10)
    l20, b20 = pix_to_deg(y20, x20)
    
    plt.scatter(l10, b10, c='cyan', s=50, marker='o', label='L10 Universes (Bass)', edgecolors='black', linewidth=0.5)
    plt.scatter(l20, b20, c='magenta', s=20, marker='o', label='L20 Universes (Tenor)', alpha=0.8)
    
    plt.title(f"THE COSMIC LAVA LAMP: Universes Surfing Traveler Pathways\nHit Rate: {hit_rate:.1f}% (Expected: {baseline_chance:.1f}%)", 
              color='white', fontsize=14)
    plt.legend(loc='upper right')
    plt.xlabel("Galactic Longitude", color='gray')
    plt.ylabel("Galactic Latitude", color='gray')
    plt.grid(color='#333', linestyle='--')
    
    plt.savefig("cmb_traveler_universality.png", dpi=100, bbox_inches='tight', facecolor='#050505')
    print("✅ Visual Proof saved to cmb_traveler_universality.png")

if __name__ == "__main__":
    run_universality_test()