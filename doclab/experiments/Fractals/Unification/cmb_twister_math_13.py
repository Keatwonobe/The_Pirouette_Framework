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
K_RANGE = np.linspace(0.9998, 1.0002, GIF_FRAMES) 

# === THE DIALS (Knotted Topology) ===
# We apply these to the "Backlight" of the Dipole
WINDING_NUMBER = 3.0    # 3-fold symmetry (Henon-Heiles style)
KNOTTEDNESS = 0.05      # Strength of the "Ripple"
ANISOTROPY = 0.2        # Vertical shearing

# VISUALIZATION
VISUALIZATION_MODE = 'shield_coherence'

# LOWER SENSITIVITY: 
# Since we brought back the massive Dipole, we need lower sensitivity 
# so the screen doesn't just turn purely white/noise.
PHASE_SENSITIVITY = 5000.0 

# ======================
# 1. THE REFERENCE GENERATOR (Dipole Restored)
# ======================
def generate_reference_universe_fast(fits_path, n_res, blur_sigma=4.0):
    print(f"[*] Initializing Reference State (Dipole Enabled)...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        return None

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    # Normalize
    cmb_mean = np.nanmean(cmb)
    cmb_std = np.nanstd(cmb)
    cmb = (cmb - cmb_mean) / cmb_std

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
    
    # NO HIGH-PASS FILTER: We keep the Dipole!
    # This ensures one side is "lit up" by the galaxy's motion.
    
    print(f"    Applying smoothing (sigma={blur_sigma})...")
    T_ref = gaussian_filter(T_ref, sigma=blur_sigma)
        
    return T_ref

# ======================
# 2. KNOTTED MANIFOLD OPERATOR
# ======================
def apply_knotted_twist(T_ref, k, n_res):
    if abs(k - 1.0) < 1e-12:
        return T_ref

    indices_i, indices_j = np.indices(T_ref.shape)
    
    # Normalize coordinates for math
    phi_norm = (indices_j / n_res) * 2 * np.pi
    theta_norm = (indices_i / n_res) * np.pi
    
    # Distortion Scaling
    distortion_strength = (k - 1.0) * 100.0 
    
    # 1. KNOTS (Winding)
    knot_offset = KNOTTEDNESS * np.sin(WINDING_NUMBER * phi_norm) * distortion_strength
    
    # 2. ANISOTROPY (Shear)
    anisotropy_offset = ANISOTROPY * np.cos(theta_norm) * distortion_strength
    
    # Apply
    center_j = n_res / 2
    indices_j_centered = indices_j - center_j
    
    indices_j_new = (indices_j_centered * k) + center_j + knot_offset + anisotropy_offset
    indices_j_new_wrapped = indices_j_new % n_res
    
    coords = np.array([indices_i, indices_j_new_wrapped])
    T_twisted = map_coordinates(T_ref, coords, order=1, mode='nearest')
    
    return T_twisted

# ======================
# 3. MAIN LOOP
# ======================
def run_simulation():
    start_time = time.time()
    
    T_ref = generate_reference_universe_fast(FITS_PATH, N_RES, blur_sigma=4.0)
    if T_ref is None: return
    
    frames_buffer = []
    print(f"[*] Simulating {GIF_FRAMES} frames (Dipole Backlight + Knots)...")

    for i, k in enumerate(K_RANGE):
        
        # A. Twist
        T_twist = apply_knotted_twist(T_ref, k, N_RES)
        
        # B. Shield Metric
        theta1 = T_ref * PHASE_SENSITIVITY
        theta2 = T_twist * PHASE_SENSITIVITY
        diff = theta1 - theta2
        Ta = np.cos(diff / 2.0)**2
        
        # Center Seam
        Ta_centered = np.roll(Ta, N_RES // 2, axis=1)

        # C. Auto-Exposure (Still useful, but Dipole provides main signal)
        v_max = np.percentile(Ta_centered, 99.5) 
        if v_max < 0.001: v_max = 0.001 
        
        # Title
        if abs(k - 1.0) < 1e-5:
            title = f"SINGULARITY: ALIGNED"
        else:
            title = f"Knotted Dipole: k={k:.6f}"

        if i % 10 == 0:
            print(f"  Frame {i}/{GIF_FRAMES} (k={k:.6f})")

        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Inferno
        im = ax.imshow(Ta_centered, extent=(-180, 180, -90, 90), cmap='inferno', 
                       vmin=0.0, vmax=v_max, origin='lower')
        
        ax.set_title(title, fontsize=14, color='white', pad=10)
        ax.axis('off')
        fig.patch.set_facecolor('#050505')
        ax.set_facecolor('#050505')
        
        fname = f"temp_backlight_{i:03d}.png"
        plt.savefig(fname, bbox_inches='tight', dpi=100, facecolor=fig.get_facecolor())
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames_buffer.append(img.copy())
        os.remove(fname)

    out_name = f"cmb_backlight_knotted_w{int(WINDING_NUMBER)}.gif"
    frames_buffer[0].save(out_name, save_all=True, append_images=frames_buffer[1:], 
                          duration=GIF_DURATION, loop=0)
    print(f"\n✅ Simulation Complete: {out_name}")

if __name__ == "__main__":
    run_simulation()