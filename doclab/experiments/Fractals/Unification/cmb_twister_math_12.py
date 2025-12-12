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

# SCAN RANGE: Crossing the Singularity (k=1.0)
# Narrow range to catch the "Flash" in slow motion
K_RANGE = np.linspace(0.9998, 1.0002, GIF_FRAMES) 

# METRIC: Shield Coherence (Ta)
# 1.0 = Connected (White), 0.0 = Torn (Black)
VISUALIZATION_MODE = 'shield_coherence'

# SENSITIVITY: 
# Adjusted for the dipole-free map. 
# Lowered slightly to broaden the "Flash" duration so you don't miss it.
PHASE_SENSITIVITY = 5000.0 

# ======================
# 1. THE REFERENCE GENERATOR (Dipole Removed)
# ======================
def generate_reference_universe_fast(fits_path, n_res, blur_sigma=3.0):
    print(f"[*] Initializing Reference State...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        return None

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    # Clean NaNs
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
    T_ref = hpix.interpolate_bilinear_lonlat(lon_deg * u.deg, lat_deg * u.deg, cmb)
    
    # === HIGH-PASS FILTER (Dipole Removal) ===
    print("    Removing Doppler Dipole (High-Pass Filter)...")
    dipole_background = gaussian_filter(T_ref, sigma=50.0) 
    T_detail = T_ref - dipole_background
    
    print(f"    Applying texture smoothing (sigma={blur_sigma})...")
    T_final = gaussian_filter(T_detail, sigma=blur_sigma)
    
    # Normalize to Standard Deviations
    T_std = np.std(T_final)
    T_final = T_final / T_std
        
    return T_final

# ======================
# 2. HELICAL ADVECTION (Centered Seam)
# ======================
def apply_helical_twist(T_ref, k, n_res):
    if abs(k - 1.0) < 1e-12:
        return T_ref

    indices_i, indices_j = np.indices(T_ref.shape)
    
    # Twist logic
    center_j = n_res / 2
    indices_j_centered = indices_j - center_j
    indices_j_new = (indices_j_centered * k) + center_j
    
    # Wrap: This is where the seam is created.
    indices_j_new_wrapped = indices_j_new % n_res
    
    coords = np.array([indices_i, indices_j_new_wrapped])
    T_twisted = map_coordinates(T_ref, coords, order=1, mode='nearest')
    
    return T_twisted

# ======================
# 3. MAIN LOOP
# ======================
def run_helical_simulation():
    start_time = time.time()
    
    T_ref = generate_reference_universe_fast(FITS_PATH, N_RES, blur_sigma=3.0)
    if T_ref is None: return
    
    frames_buffer = []
    print(f"[*] Simulating {GIF_FRAMES} frames (Seam Centered + Auto-Gain)...")

    for i, k in enumerate(K_RANGE):
        
        # A. Twist
        T_twist = apply_helical_twist(T_ref, k, N_RES)
        
        # B. Shield Metric (Ta)
        theta1 = T_ref * PHASE_SENSITIVITY
        theta2 = T_twist * PHASE_SENSITIVITY
        diff = theta1 - theta2
        Ta = np.cos(diff / 2.0)**2
        
        # C. CENTER THE SEAM
        # The topological tear happens at the array edges (indices 0 and N).
        # We roll the array by N/2 to bring that edge to the center of the screen.
        Ta_centered = np.roll(Ta, N_RES // 2, axis=1)

        # D. AUTO-EXPOSURE (The Fix for Blackness)
        # We find the max brightness in THIS frame and scale to it.
        # This ensures we see structure even when the flash fades.
        v_max = np.percentile(Ta_centered, 99.9) 
        if v_max < 0.001: v_max = 0.001 # Prevent div/0 on empty frames
        
        # Visualization Data
        vis_data = Ta_centered
        
        # Title logic
        if abs(k - 1.0) < 1e-5:
            title = "SINGULARITY: ZERO-POINT"
        else:
            title = f"Topological Seam: k={k:.6f}"

        if i % 10 == 0:
            print(f"  Frame {i}/{GIF_FRAMES} (k={k:.6f}) | Max: {v_max:.4f}")

        fig, ax = plt.subplots(figsize=(10, 10))
        
        # 'inferno' creates that hot, electric look.
        # vmin=0 (Black), vmax=v_max (White/Yellow)
        im = ax.imshow(vis_data, extent=(-180, 180, -90, 90), cmap='inferno', 
                       vmin=0.0, vmax=v_max, origin='lower')
        
        ax.set_title(title, fontsize=14, color='white', pad=10)
        ax.axis('off')
        
        # Dark Mode
        fig.patch.set_facecolor('#050505')
        ax.set_facecolor('#050505')
        
        fname = f"temp_seam_{i:03d}.png"
        plt.savefig(fname, bbox_inches='tight', dpi=100, facecolor=fig.get_facecolor())
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames_buffer.append(img.copy())
        os.remove(fname)

    out_name = "cmb_seam_magnified.gif"
    frames_buffer[0].save(out_name, save_all=True, append_images=frames_buffer[1:], 
                          duration=GIF_DURATION, loop=0)
    print(f"\n✅ Simulation Complete: {out_name}")

if __name__ == "__main__":
    run_helical_simulation()