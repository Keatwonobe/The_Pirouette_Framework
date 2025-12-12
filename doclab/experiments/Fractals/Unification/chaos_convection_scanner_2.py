import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord
from PIL import Image
import os
import sys
import time

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60                   # Bandwidth
N_RES = 300                 # Grid Resolution (300x300)
FRAMES = 80                 # Animation smoothness
K_START = 0.9
K_END = 1.1
GIF_NAME = "cmb_chaos_convection_fast.gif"

# ======================
# 1. PRE-CALCULATION ENGINE
# ======================

def get_alms_and_coords(fits_path, lmax, n_res):
    print(f"[*] Loading CMB Data from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # High Res Grid for ALM Extraction
    print("[*] Extracting Spherical Harmonics (ALMs)...")
    n_theta_alm = lmax * 3
    n_phi_alm = lmax * 4
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
            
    # Synthesis Coords
    theta_vec = np.linspace(0, np.pi, n_res)
    phi_vec = np.linspace(-np.pi, np.pi, n_res)
    
    return alms, theta_vec, phi_vec

def precompute_m_profiles(alms, lmax, theta_vec):
    """
    OPTIMIZATION CORE:
    Pre-sums the Legendre polynomials for each m.
    Returns a matrix of shape (2*LMAX+1, N_THETA).
    """
    print(f"[*] Pre-computing Latitudinal Profiles (Speed Optimization)...")
    
    # Map m (-L to L) to array index
    m_range = np.arange(-lmax, lmax + 1)
    n_m = len(m_range)
    n_theta = len(theta_vec)
    
    # Complex profile matrix
    profiles = np.zeros((n_m, n_theta), dtype=np.complex128)
    
    # We evaluate Y_lm at phi=0 to get the P_lm(theta) dependence (times normalization)
    # sph_harm(m, l, phi, theta) -> use phi=0
    zeros_phi = np.zeros_like(theta_vec)
    
    for i, m in enumerate(m_range):
        # Sum over all valid l for this m
        # (Skip l=0 for cleaner gradients if desired, but let's keep it generally)
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) in alms:
                # The longitudinal part is just 1.0 at phi=0
                # We are essentially baking the a_lm into the shape function
                Y_lm_theta = sph_harm(m, l, zeros_phi, theta_vec)
                profiles[i, :] += alms[(l, m)] * Y_lm_theta
                
    return profiles, m_range

def fast_synthesize(profiles, m_range, phi_vec, k):
    """
    MATRIX SYNTHESIS:
    Field = Profiles_Matrix @ Phase_Matrix
    """
    # 1. Create Phase Matrix (N_m, N_phi)
    # phase = exp(i * m * k * phi)
    # Note: The 'k' factor replaces the standard '1' in usual synthesis
    m_col = m_range[:, np.newaxis]
    phi_row = phi_vec[np.newaxis, :]
    
    # The Twist: Effective frequency is m*k
    phase_matrix = np.exp(1j * m_col * k * phi_row)
    
    # 2. Matrix Multiply: (N_m, N_theta).T @ (N_m, N_phi) 
    # -> (N_theta, N_m) @ (N_m, N_phi) -> (N_theta, N_phi)
    field = profiles.T @ phase_matrix
    
    return field.real

def calculate_chaos_metric(field, theta_step, phi_step):
    grad_theta, grad_phi = np.gradient(field, theta_step, phi_step)
    sin_theta_map = np.sin(np.linspace(0, np.pi, field.shape[0]))
    sin_theta_map = np.clip(sin_theta_map, 0.01, 1.0)
    sin_theta_grid = sin_theta_map[:, np.newaxis]
    chaos = np.sqrt(grad_theta**2 + (grad_phi / sin_theta_grid)**2)
    return chaos

# ======================
# 2. MAIN LOOP
# ======================

def run_fast_scanner():
    start_time = time.time()
    
    # 1. Load & Precompute
    alms, theta_vec, phi_vec = get_alms_and_coords(FITS_PATH, LMAX, N_RES)
    profiles, m_range = precompute_m_profiles(alms, LMAX, theta_vec)
    
    theta_step = theta_vec[1] - theta_vec[0]
    phi_step = phi_vec[1] - phi_vec[0]
    
    # 2. Setup Animation Buffers
    K_RANGE = np.linspace(K_START, K_END, FRAMES)
    convection_history = np.zeros((FRAMES, N_RES))
    frustration_history = []
    frames = []
    
    print(f"[-] Starting Fast Render (k={K_START}->{K_END})...")
    
    for i, k in enumerate(K_RANGE):
        iter_start = time.time()
        
        # A. Fast Synthesis
        field = fast_synthesize(profiles, m_range, phi_vec, k)
        
        # B. Chaos Calculation
        chaos_map = calculate_chaos_metric(field, theta_step, phi_step)
        
        # C. Metrics
        zonal_chaos = np.mean(chaos_map, axis=1)
        convection_history[i, :] = zonal_chaos
        total_frustration = np.sum(chaos_map)
        frustration_history.append(total_frustration)
        
        # D. Plotting
        fig = plt.figure(figsize=(10, 10), facecolor='#050505')
        gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1.5, 1])
        
        # Map
        ax_map = plt.subplot(gs[0])
        ax_map.imshow(chaos_map, origin='lower', extent=[-180, 180, -90, 90], 
                      cmap='inferno', vmin=0, vmax=np.percentile(chaos_map, 99))
        ax_map.set_title(f"CHAOS FIELD (Gradient) | k={k:.4f}", color='white')
        ax_map.axis('off')
        
        # Convection Flow
        ax_conv = plt.subplot(gs[1])
        display_conv = np.zeros_like(convection_history)
        display_conv[:i+1] = convection_history[:i+1]
        ax_conv.imshow(display_conv.T, origin='lower', extent=[K_START, K_END, -90, 90], 
                       cmap='magma', aspect='auto')
        ax_conv.axvline(x=k, color='cyan', linestyle='--')
        ax_conv.set_title("CONVECTION FLOW (Hovmöller)", color='orange', fontsize=9)
        ax_conv.set_ylabel("Latitude", color='gray')
        ax_conv.tick_params(colors='gray')
        
        # Heartbeat
        ax_graph = plt.subplot(gs[2])
        ax_graph.set_facecolor('#111')
        ax_graph.plot(K_RANGE[:i+1], frustration_history, color='cyan', linewidth=1.5)
        ax_graph.set_xlim(K_START, K_END)
        if len(frustration_history) > 1:
            ax_graph.set_ylim(min(frustration_history)*0.99, max(frustration_history)*1.01)
        ax_graph.set_title("TOTAL CHAOS (Frustration)", color='cyan', fontsize=9)
        ax_graph.tick_params(colors='gray')
        
        plt.tight_layout()
        
        fname = f"_fast_frame_{i:03d}.png"
        plt.savefig(fname, dpi=60, bbox_inches='tight', facecolor='#050505')
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames.append(img.copy())
        os.remove(fname)
        
        iter_dt = time.time() - iter_start
        sys.stdout.write(f"\r[>] Frame {i+1}/{FRAMES} | k={k:.4f} | Render Time: {iter_dt*1000:.1f}ms")
        sys.stdout.flush()

    print(f"\n[*] Saving GIF: {GIF_NAME}")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=50, loop=0)
    
    total_time = time.time() - start_time
    print(f"✅ DONE. Total time: {total_time:.2f}s (Avg {total_time/FRAMES:.2f}s/frame)")

if __name__ == "__main__":
    run_fast_scanner()