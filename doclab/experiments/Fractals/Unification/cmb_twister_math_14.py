import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.ndimage import map_coordinates, gaussian_filter
import astropy.units as u
from PIL import Image
import os
import time

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
N_RES = 1024        
GIF_FRAMES = 60
GIF_DURATION = 100 

# SCAN RANGE: Crossing the Singularity
# We scan from 0.9998 to 1.0002 to capture the flash dynamics
K_RANGE = np.linspace(0.9998, 1.0002, GIF_FRAMES) 

# COMPOSITE WEIGHTS
# Layer 1 (Base): Volume 4 Interference (The "Body" / Light)
GAIN_BASE = 1.0     
# Layer 2 (Overlay): Volume 10 Coherence (The "Spirit" / Flash)
GAIN_OVERLAY = 0.8  
# Sensitivity for the overlay flash
OVERLAY_SENSITIVITY = 10000.0 

# ======================
# 1. THE REFERENCE GENERATOR
# ======================
def generate_reference_layers(fits_path, n_res, blur_sigma=4.0):
    print(f"[*] Initializing Reference Layers...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        return None, None

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    # Clean
    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    # Healpix Setup
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Projection
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    lon_deg = np.rad2deg(PH_GRID)
    lat_deg = np.rad2deg(0.5*np.pi - TH_GRID)
    
    print(f"    Projecting sky to {n_res}x{n_res}...")
    T_raw = hpix.interpolate_bilinear_lonlat(lon_deg * u.deg, lat_deg * u.deg, cmb)
    
    # --- LAYER 1: BASE (With Dipole) ---
    # Used for the "Volume 4" interference view.
    # We smooth slightly to remove pixel noise but KEEP the massive Dipole.
    T_base = gaussian_filter(T_raw, sigma=blur_sigma)
    
    # Normalize Base to 0..1 range roughly for consistent brightness
    base_min, base_max = T_base.min(), T_base.max()
    T_base_norm = (T_base - base_min) / (base_max - base_min)
    
    # --- LAYER 2: OVERLAY (Dipole Removed) ---
    # Used for the "Volume 10" Coherence Flash.
    # We must remove the dipole so the flash is topological, not directional.
    print("    Creating High-Pass Layer (Dipole Removal)...")
    dipole_background = gaussian_filter(T_raw, sigma=50.0)
    T_detail = T_raw - dipole_background
    T_detail = gaussian_filter(T_detail, sigma=blur_sigma)
    
    # Normalize Detail to Std Devs for phase calc
    detail_std = np.std(T_detail)
    T_detail_norm = T_detail / detail_std
        
    return T_base_norm, T_detail_norm

# ======================
# 2. HELICAL ADVECTION OPERATOR
# ======================
def apply_helical_twist(T_ref, k, n_res):
    """
    Implements the Helical Derivative (d_h/dt) as geometric advection.
    T(phi) -> T(k*phi)
    """
    if abs(k - 1.0) < 1e-12:
        return T_ref

    indices_i, indices_j = np.indices(T_ref.shape)
    
    # Twist logic
    center_j = n_res / 2
    indices_j_centered = indices_j - center_j
    indices_j_new = (indices_j_centered * k) + center_j
    
    # Wrap Indices for periodicity
    indices_j_new_wrapped = indices_j_new % n_res
    
    coords = np.array([indices_i, indices_j_new_wrapped])
    
    # Fast Interpolation
    T_twisted = map_coordinates(T_ref, coords, order=1, mode='nearest')
    
    return T_twisted

# ======================
# 3. MAIN LOOP
# ======================
def run_simulation():
    start_time = time.time()
    
    # Load both layers
    T_base, T_detail = generate_reference_layers(FITS_PATH, N_RES, blur_sigma=4.0)
    if T_base is None: return
    
    frames_buffer = []
    print(f"[*] Simulating {GIF_FRAMES} frames (Composite Mode)...")

    for i, k in enumerate(K_RANGE):
        
        # --- A. TWIST BOTH LAYERS ---
        # "Transfer Volume 4 to Helical" -> Applying advection to base
        T_base_twist = apply_helical_twist(T_base, k, N_RES)
        # Applying advection to detail layer for the overlay
        T_detail_twist = apply_helical_twist(T_detail, k, N_RES)
        
        # --- B. COMPUTE LAYERS ---
        
        # Layer 1: Volume 4 Interference (The Body)
        # Metric: |Ref - Twist|
        # This is robust and visible everywhere except k=1
        L1_Interference = np.abs(T_base - T_base_twist)
        
        # Layer 2: Volume 10 Shield Coherence (The Flash)
        # Metric: cos^2(diff/2)
        # This is bright White at k=1, fades to noise elsewhere
        theta1 = T_detail * OVERLAY_SENSITIVITY
        theta2 = T_detail_twist * OVERLAY_SENSITIVITY
        diff = theta1 - theta2
        L2_Coherence = np.cos(diff / 2.0)**2
        
        # --- C. CENTER SEAM (Meeting of Two Masses) ---
        L1_centered = np.roll(L1_Interference, N_RES // 2, axis=1)
        L2_centered = np.roll(L2_Coherence, N_RES // 2, axis=1)
        
        # --- D. COMPOSITE BLEND ---
        # Visual = (Interference * Gain) + (Coherence * Gain)
        # At k=1: Interference is 0, Coherence is 1. Result: Bright Flash.
        # At k!=1: Interference is High, Coherence is Low. Result: Visible Structure.
        
        # Auto-exposure for Base Layer to prevent darkness
        v_base_max = np.percentile(L1_centered, 99.5)
        if v_base_max < 0.001: v_base_max = 0.001
        L1_norm = L1_centered / v_base_max
        
        # Blend
        vis_data = (L1_norm * GAIN_BASE) + (L2_centered * GAIN_OVERLAY)
        
        # Title
        if abs(k - 1.0) < 1e-5:
            title = f"SINGULARITY: COHERENCE OVERLAY"
        else:
            title = f"Composite Manifold: k={k:.6f}"

        if i % 10 == 0:
            print(f"  Frame {i}/{GIF_FRAMES} (k={k:.6f})")

        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Inferno handles the addition of light intensities naturally
        im = ax.imshow(vis_data, extent=(-180, 180, -90, 90), cmap='inferno', 
                       origin='lower') # vmin/vmax auto-scaled by matplotlib for max range
        
        ax.set_title(title, fontsize=14, color='white', pad=10)
        ax.axis('off')
        fig.patch.set_facecolor('#050505')
        ax.set_facecolor('#050505')
        
        fname = f"temp_comp_{i:03d}.png"
        plt.savefig(fname, bbox_inches='tight', dpi=100, facecolor=fig.get_facecolor())
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames_buffer.append(img.copy())
        os.remove(fname)

    out_name = "cmb_composite_helical.gif"
    frames_buffer[0].save(out_name, save_all=True, append_images=frames_buffer[1:], 
                          duration=GIF_DURATION, loop=0)
    print(f"\n✅ Simulation Complete: {out_name}")

if __name__ == "__main__":
    run_simulation()