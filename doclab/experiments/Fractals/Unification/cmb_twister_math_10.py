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
N_RES = 1024        # High resolution for fine filaments
GIF_FRAMES = 60
GIF_DURATION = 80 

# SCAN RANGE: Crossing the Singularity at k=1.0
# We scan from 0.9999 to 1.0001 to catch the "Flash"
K_RANGE = np.linspace(0.9999, 1.0001, GIF_FRAMES) 

# VISUALIZATION MODE: 'shield_coherence'
# Implements the Ta metric from your Shield Fractal
VISUALIZATION_MODE = 'shield_coherence'

# SENSITIVITY: How "tight" the phase locking is. 
# Higher = Flash fades faster (more sensitive to twist).
PHASE_SENSITIVITY = 10000.0 

# ======================
# 1. THE REFERENCE GENERATOR
# ======================
def generate_reference_universe_fast(fits_path, n_res, blur_sigma=4.0):
    print(f"[*] Initializing Reference State...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        return None

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    # Normalize CMB to typical range (helps sensitivity tuning)
    # Standard deviation of CMB is approx 0.0001 K
    cmb_mean = np.nanmean(cmb)
    cmb_std = np.nanstd(cmb)
    cmb = (cmb - cmb_mean) / cmb_std
    
    # Healpix Setup
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Grid Projection
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    lon_deg = np.rad2deg(PH_GRID)
    lat_deg = np.rad2deg(0.5*np.pi - TH_GRID)
    
    print(f"    Projecting sky to {n_res}x{n_res}...")
    T_ref = hpix.interpolate_bilinear_lonlat(lon_deg * u.deg, lat_deg * u.deg, cmb)
    
    print(f"    Applying smoothing (sigma={blur_sigma})...")
    T_ref = gaussian_filter(T_ref, sigma=blur_sigma)
        
    return T_ref

# ======================
# 2. HELICAL ADVECTION
# ======================
def apply_helical_twist(T_ref, k, n_res):
    if abs(k - 1.0) < 1e-12:
        return T_ref

    indices_i, indices_j = np.indices(T_ref.shape)
    
    # Twist logic
    center_j = n_res / 2
    indices_j_centered = indices_j - center_j
    indices_j_new = (indices_j_centered * k) + center_j
    indices_j_new_wrapped = indices_j_new % n_res
    
    coords = np.array([indices_i, indices_j_new_wrapped])
    T_twisted = map_coordinates(T_ref, coords, order=1, mode='nearest') # order=1 is faster/sharper
    
    return T_twisted

# ======================
# 3. MAIN LOOP
# ======================
def run_helical_simulation():
    start_time = time.time()
    T_ref = generate_reference_universe_fast(FITS_PATH, N_RES, blur_sigma=3.0)
    if T_ref is None: return
    
    frames_buffer = []
    print(f"[*] Simulating {GIF_FRAMES} frames (Metric: Shield Coherence Ta)...")

    for i, k in enumerate(K_RANGE):
        
        # A. Apply Twist
        T_twist = apply_helical_twist(T_ref, k, N_RES)
        
        # B. Shield Fractal Metric: Ta (Time Adherence / Coherence)
        # We treat T_ref and T_twist as phase angles in a coupled system.
        # Ta = | < e^(i*theta) > |^2
        # For 2 oscillators: Ta = cos^2( (theta1 - theta2) / 2 )
        
        # Scale temperature to phase radians
        theta1 = T_ref * PHASE_SENSITIVITY
        theta2 = T_twist * PHASE_SENSITIVITY
        
        diff = theta1 - theta2
        
        # The Coherence Map
        # 1.0 = Perfect Alignment (White Flash)
        # 0.0 = Orthogonal (Dark)
        Ta = np.cos(diff / 2.0)**2
        
        # C. Visualization
        # We want the "Flash" to be bright White.
        # Ta is already 0..1.
        
        vis_data = Ta
        
        # Dynamic Title
        if abs(k - 1.0) < 1e-5:
            title = "SINGULARITY: PERFECT COHERENCE (Ta=1.0)"
        else:
            title = f"Topological Coherence: k={k:.6f}"

        if i % 10 == 0:
            print(f"  Frame {i}/{GIF_FRAMES} (k={k:.6f}) | Mean Coherence: {vis_data.mean():.4f}")

        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Use a fiery/electric colormap: 'afmhot' or 'inferno'
        # 1.0 (Flash) -> White/Yellow
        # 0.0 (Decoherence) -> Black/Red
        im = ax.imshow(vis_data, extent=(-180, 180, -90, 90), cmap='inferno', 
                       vmin=0.0, vmax=1.0, origin='lower')
        
        ax.set_title(title, fontsize=14, color='white', pad=10)
        ax.axis('off')
        
        # Dark Background
        fig.patch.set_facecolor('#050505')
        ax.set_facecolor('#050505')
        
        fname = f"temp_shield_{i:03d}.png"
        plt.savefig(fname, bbox_inches='tight', dpi=100, facecolor=fig.get_facecolor())
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames_buffer.append(img.copy())
        os.remove(fname)

    out_name = "cmb_shield_coherence_flash.gif"
    frames_buffer[0].save(out_name, save_all=True, append_images=frames_buffer[1:], 
                          duration=GIF_DURATION, loop=0)
    print(f"\n✅ Simulation Complete: {out_name}")

if __name__ == "__main__":
    run_helical_simulation()