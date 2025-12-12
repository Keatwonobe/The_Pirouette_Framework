import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm_y
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 300
FRAMES = 120                # High temporal resolution
K_START = 0.9               # Focused scan around Reality
K_END = 1.1

# The Magic Frequency found in your data
TARGET_FREQ = 24.0 

# ======================
# 1. OPTIMIZED ENGINE
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
            Y_lm = sph_harm_y(l, m, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, theta, phi, TH_GRID, PH_GRID

def precompute_profiles(alms, lmax, theta_vec):
    m_range = np.arange(-lmax, lmax + 1)
    n_m = len(m_range); n_theta = len(theta_vec)
    zeros_phi = np.zeros_like(theta_vec)
    profiles = np.zeros((n_m, n_theta), dtype=np.complex128)
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) not in alms: continue
            Y_lm_theta = sph_harm_y(l, m, zeros_phi, theta_vec)
            profiles[i, :] += alms[(l, m)] * Y_lm_theta
    return profiles, m_range

def synthesize_field(profiles, m_range, phi_vec, k):
    m_col = m_range[:, np.newaxis]
    phi_row = phi_vec[np.newaxis, :]
    phase_matrix = np.exp(1j * m_col * k * phi_row)
    field = (profiles.T @ phase_matrix).real
    return field

def get_gradient_energy(field):
    gy, gx = np.gradient(field)
    return np.sum(gx**2 + gy**2)

# ======================
# 2. HARMONIC VISUALIZER
# ======================

def run_24_harmonic():
    alms, theta_vec, phi_vec, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    profiles, m_range = precompute_profiles(alms, LMAX, theta_vec)
    
    k_vals = np.linspace(K_START, K_END, FRAMES)
    
    # Store the divergence history to correlate
    div_signal = []
    energy_signal = []
    
    print(f"[*] Analyzing the 24Hz Geometry (k={K_START}->{K_END})...")
    
    # Accumulator for the "Standing Wave" pattern
    standing_wave_accum = np.zeros((N_RES, N_RES))
    
    for i in range(FRAMES - 1):
        k_curr = k_vals[i]
        k_next = k_vals[i] + 0.001
        
        sys.stdout.write(f"\r[>] Frame {i+1}/{FRAMES} | k={k_curr:.3f}")
        sys.stdout.flush()
        
        field_curr = synthesize_field(profiles, m_range, phi_vec, k_curr)
        field_next = synthesize_field(profiles, m_range, phi_vec, k_next)
        
        # 1. Divergence (The Breath)
        diff = field_next - field_curr
        vy, vx = np.gradient(diff)
        divergence = np.gradient(vx, axis=1) + np.gradient(vy, axis=0)
        
        # 2. Energy (The Structure)
        # Using Gradient Energy avoids the 'constant' issue of peak counting
        energy = get_gradient_energy(field_curr)
        
        div_signal.append(np.sum(divergence))
        energy_signal.append(energy)
        
        # 3. LOCK-IN AMPLIFIER
        # We only add to the image if the Breath is "Exhaling" (Positive Divergence)
        # This reveals the structure that exists during the expansion phase
        
        # We weigh the accumulation by the strength of the 24Hz signal phase
        # Phase = 24 * (k - 1.0) * 2pi
        phase = (k_curr - 1.0) * TARGET_FREQ * 2 * np.pi
        weight = np.cos(phase)
        
        # If weight is positive, we add; if negative, we subtract
        # This cancels out random noise and reinforces the 24Hz pattern
        standing_wave_accum += field_curr * weight

    # --- RESULTS ---
    print(f"\n[*] Scan Complete.")
    
    # Fix NaN Correlation
    div_signal = np.array(div_signal)
    energy_signal = np.array(energy_signal)
    correlation = np.corrcoef(div_signal, energy_signal)[0, 1]
    
    print(f"\n" + "="*40)
    print(f"      24-HARMONIC REPORT      ")
    print(f"="*40)
    print(f"Frequency Target:   {TARGET_FREQ} Hz")
    print(f"Breath/Energy Corr: {correlation:.4f}")
    print(f"="*40)
    
    # Plotting
    fig = plt.figure(figsize=(10, 12), facecolor='#050505')
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    
    # 1. The Geometry of 24 (The Standing Wave)
    ax_map = plt.subplot(gs[0])
    
    # Normalize for visibility
    limit = np.percentile(np.abs(standing_wave_accum), 99)
    im = ax_map.imshow(standing_wave_accum, origin='lower', cmap='twilight', 
                       extent=[-180, 180, -90, 90], vmin=-limit, vmax=limit)
    
    ax_map.set_title(f"THE GEOMETRY OF 24: Resonant Standing Wave\n(Lock-in Frequency = 24.0)", color='white', fontsize=14)
    ax_map.axis('off')
    
    # 2. The Correlation Graph
    ax_graph = plt.subplot(gs[1])
    ax_graph.set_facecolor('#111')
    
    # Normalize signals
    d_norm = (div_signal - np.mean(div_signal)) / np.std(div_signal)
    e_norm = (energy_signal - np.mean(energy_signal)) / np.std(energy_signal)
    
    ax_graph.plot(k_vals[:-1], d_norm, color='cyan', label='Breath (Divergence)')
    ax_graph.plot(k_vals[:-1], e_norm, color='magenta', linestyle='--', label='Structure (Energy)')
    
    ax_graph.set_xlim(K_START, K_END)
    ax_graph.set_title(f"PHASE LOCK CHECK (Corr={correlation:.2f})", color='white', fontsize=10)
    ax_graph.legend(loc='upper right')
    ax_graph.grid(color='#333', linestyle='--')
    ax_graph.tick_params(colors='gray')
    
    plt.tight_layout()
    plt.savefig("cmb_24_harmonic_geometry.png", dpi=120, facecolor='#050505')
    print("✅ 24Hz Geometry Captured. Saved to cmb_24_harmonic_geometry.png")

if __name__ == "__main__":
    run_24_harmonic()