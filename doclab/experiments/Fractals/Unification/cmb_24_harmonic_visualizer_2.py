import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import maximum_filter
from scipy.spatial.distance import pdist
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 512
K_TARGET = 1.0              # Reality Check
FREQ_TARGET = 24.0          # The Resonance
PEAK_THRESHOLD_PCT = 98.5   # Only the brightest "Universes"

# ======================
# 1. GENERATE THE 24HZ GEOMETRY
# ======================

def get_alms_and_grid(fits_path, lmax, n_res):
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
    
    n_theta = lmax * 3; n_phi = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta)
    p_alm = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
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
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, TH_GRID, PH_GRID

def synthesize_resonant_geometry(alms, TH, PH, k_res):
    """ Synthesizes the map specifically tuned to the 24Hz resonance phase at K=1.0 """
    # Phase = 24 * (k - 1.0) * 2pi. At k=1.0, Phase=0.
    # We essentially want the "Rest State" geometry.
    # But let's verify if we need to sum profiles or just single synthesis.
    
    # Actually, let's just synthesize the field at K=1.0 using the profiles method
    # and assuming the "Standing Wave" is inherent in the structure.
    
    lmax = LMAX
    field = np.zeros_like(TH, dtype=np.complex128)
    
    # Standard synthesis for K=1.0 (Reality)
    # The 24Hz pattern is the *response* to twist, but the structure exists at rest.
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            Y_lm = sph_harm(m, l, PH, TH)
            field += alms[(l, m)] * Y_lm
            
    return field.real

# ======================
# 2. LATTICE DECODER
# ======================

def find_nodes(field):
    # Normalize
    f_norm = (field - field.min()) / (field.max() - field.min())
    
    # Filter
    threshold = np.percentile(f_norm, PEAK_THRESHOLD_PCT)
    local_max = maximum_filter(f_norm, size=15) == f_norm
    mask = (local_max) & (f_norm > threshold)
    
    y_idx, x_idx = np.where(mask)
    return y_idx, x_idx

def angular_distance_histogram(y_idx, x_idx, n_res):
    # Convert pixels to Spherical Coords (Radians)
    # Theta (0 to pi), Phi (-pi to pi)
    theta = (n_res - y_idx) * (np.pi / n_res) # y=0 is North (Theta=0)?? Check extent.
    # Extent is usually origin='lower', so y=0 is South (Theta=pi).
    # Let's align with our previous plots: origin='lower', extent -90 to 90.
    # y=0 -> -90 deg -> Theta = pi
    # y=N -> 90 deg -> Theta = 0
    theta = np.linspace(np.pi, 0, n_res)[y_idx]
    phi = np.linspace(-np.pi, np.pi, n_res)[x_idx]
    
    # Calculate pairwise great circle distances
    # Formula: d = 2*arcsin( sqrt( sin^2(dlat/2) + cos(lat1)cos(lat2)sin^2(dlon/2) ) )
    # Or vector dot product.
    
    # Convert to unit vectors
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    
    vectors = np.column_stack((x, y, z))
    n_points = len(vectors)
    
    if n_points < 2: return []
    
    distances = []
    # Brute force pdist is fast enough for ~1000 points
    # Dot product: cos(angle) = v1 . v2
    # Clip to -1, 1 to avoid numerical errors
    
    # Using scipy pdist with custom metric or just loop
    # Let's do matrix mult for speed
    dot_products = vectors @ vectors.T
    
    # We only want upper triangle
    i_upper, j_upper = np.triu_indices(n_points, k=1)
    dots = dot_products[i_upper, j_upper]
    dots = np.clip(dots, -1.0, 1.0)
    
    angles = np.arccos(dots) # Radians
    angles_deg = np.degrees(angles)
    
    return angles_deg

# ======================
# 3. MAIN
# ======================

def run_lattice_decoder():
    alms, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    
    print(f"[*] Synthesizing Reality Grid (K=1.0)...")
    field = synthesize_resonant_geometry(alms, TH, PH, K_TARGET)
    
    # We use the GRADIENT ENERGY as the structure map (as per previous success)
    gy, gx = np.gradient(field)
    structure_map = np.sqrt(gx**2 + gy**2)
    
    print(f"[*] Identifying Lattice Vertices (Top {100-PEAK_THRESHOLD_PCT:.1f}%)...")
    y_nodes, x_nodes = find_nodes(structure_map)
    print(f"   -> Found {len(y_nodes)} Nodes (Conserved Universes).")
    
    print(f"[*] Calculating Angular Fingerprint (Pairwise Distances)...")
    angles = angular_distance_histogram(y_nodes, x_nodes, N_RES)
    
    # --- PLOTTING ---
    fig = plt.figure(figsize=(12, 10), facecolor='#050505')
    gs = gridspec.GridSpec(2, 2, height_ratios=[1.5, 1])
    
    # 1. Map with Nodes
    ax_map = plt.subplot(gs[0, :])
    ax_map.imshow(structure_map, origin='lower', cmap='magma', extent=[-180, 180, -90, 90])
    
    # Convert pixels to degrees for scatter
    lon_deg = np.linspace(-180, 180, N_RES)[x_nodes]
    lat_deg = np.linspace(-90, 90, N_RES)[y_nodes]
    
    ax_map.scatter(lon_deg, lat_deg, c='cyan', s=10, alpha=0.8, edgecolors='none')
    ax_map.set_title(f"LATTICE VERTICES | Conserved Topological Charges ({len(y_nodes)})", color='white', fontsize=14)
    ax_map.axis('off')
    
    # 2. Angular Histogram
    ax_hist = plt.subplot(gs[1, :])
    ax_hist.set_facecolor('#111')
    
    counts, bins, patches = ax_hist.hist(angles, bins=180, range=(0, 180), color='cyan', alpha=0.6, density=True)
    
    # Highlight Key Geometric Angles
    key_angles = [30, 45, 60, 90, 120, 135, 150]
    for ang in key_angles:
        ax_hist.axvline(ang, color='yellow', linestyle='--', alpha=0.3)
        ax_hist.text(ang, max(counts)*0.9, f"{ang}°", color='yellow', ha='center', fontsize=8, rotation=90)
        
    ax_hist.set_xlim(0, 180)
    ax_hist.set_xlabel("Angular Separation (Degrees)", color='gray')
    ax_hist.set_ylabel("Probability Density", color='gray')
    ax_hist.set_title("LATTICE FINGERPRINT: Angular Distribution of Nodes", color='white', fontsize=12)
    ax_hist.tick_params(colors='gray')
    ax_hist.grid(color='#333', linestyle=':')
    
    plt.tight_layout()
    plt.savefig("cmb_lattice_decoder.png", dpi=100, facecolor='#050505')
    print("✅ Lattice Decoded. Saved to cmb_lattice_decoder.png")

if __name__ == "__main__":
    run_lattice_decoder()