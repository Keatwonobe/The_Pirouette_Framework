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

# INCREASED RESOLUTION: Now feasible because projection is instant.
# This helps capture the tiny sub-pixel shifts of the singularity.
N_RES = 2048        
GIF_FRAMES = 60
GIF_DURATION = 80 

# The Singularity Probe
# We scan extremely close to 1.0 to see the "tear" mechanics
K_RANGE = np.linspace(0, 10, GIF_FRAMES) 

# MODE: 'flux' (The derivative dE/dk)
VISUALIZATION_MODE = 'flux' 

# ======================
# 1. THE REFERENCE GENERATOR
# ======================
def generate_reference_universe_fast(fits_path, n_res, blur_sigma=4.0):
    print(f"[*] Initializing Reference State (Direct Projection)...")
    
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        return None, None, None

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    # Clean NaNs
    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Generate Target Grid
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    print(f"    Projecting sky to {n_res}x{n_res} grid...")
    lon_deg = np.rad2deg(PH_GRID)
    lat_deg = np.rad2deg(0.5*np.pi - TH_GRID)
    
    # Interpolate from HEALPix to Cartesian Grid
    # We pass 'cmb' as the values argument
    T_ref = hpix.interpolate_bilinear_lonlat(lon_deg * u.deg, lat_deg * u.deg, cmb)
    
    # Apply smoothing to remove pixel noise and simulate LMAX
    print(f"    Applying smoothing (sigma={blur_sigma})...")
    T_ref = gaussian_filter(T_ref, sigma=blur_sigma)
        
    return T_ref

# ======================
# 2. HELICAL ADVECTION OPERATOR
# ======================
def apply_helical_twist(T_ref, k, n_res):
    if abs(k - 1.0) < 1e-12:
        return T_ref

    indices_i, indices_j = np.indices(T_ref.shape)
    
    # Helical Twist: Scale Phi (axis 1) around the center
    center_j = n_res / 2
    indices_j_centered = indices_j - center_j
    indices_j_new = (indices_j_centered * k) + center_j
    
    # Periodic Wrap: modulo n_res
    indices_j_new_wrapped = indices_j_new % n_res
    
    coords = np.array([indices_i, indices_j_new_wrapped])
    
    # Cubic interpolation (order=3) to catch sub-pixel shifts
    T_twisted = map_coordinates(T_ref, coords, order=3, mode='nearest')
    
    return T_twisted

# ======================
# 3. MAIN LOOP
# ======================
def run_helical_simulation():
    start_time = time.time()
    
    T_ref = generate_reference_universe_fast(FITS_PATH, N_RES, blur_sigma=4.0)
    if T_ref is None: return
    
    print(f"[*] Reference Generated. Max Temp: {T_ref.max():.2f}, Min: {T_ref.min():.2f}")
    
    frames_buffer = []
    print(f"[*] Simulating {GIF_FRAMES} frames...")

    for i, k in enumerate(K_RANGE):
        
        # Apply Twist
        T_twist = apply_helical_twist(T_ref, k, N_RES)
        
        # Compute Flux
        denom = (k - 1.0)
        if abs(denom) < 1e-12: denom = 1e-12
        
        # Flux = Gradient of the Twist
        raw_diff = np.abs(T_ref - T_twist)
        data = raw_diff / abs(denom)
        
        # === AUTO EXPOSURE (The Fix for Black Images) ===
        # We calculate percentile limits to ignore the zeros and outliers
        v_min = np.percentile(data, 1)
        v_max = np.percentile(data, 99.5)
        
        # Safety check for the exact singularity frame (k=1)
        if v_max <= v_min: 
            v_max = v_min + 1.0 
        
        if i % 10 == 0:
            print(f"  Frame {i}/{GIF_FRAMES} (k={k:.6f}) | Flux range: [{data.min():.2e}, {data.max():.2e}]")

        # Render
        # Power law 0.5 helps see faint structures
        vis_data = np.power(data, 0.5) 
        # Re-scale limits for the power law
        v_min_p = np.power(v_min, 0.5)
        v_max_p = np.power(v_max, 0.5)

        fig, ax = plt.subplots(figsize=(10, 10)) # Square for higher res
        im = ax.imshow(vis_data, extent=(-180, 180, -90, 90), cmap='magma',
                       norm=colors.Normalize(vmin=v_min_p, vmax=v_max_p), origin='lower')
        
        ax.set_title(f"Singularity Flux: k={k:.8f}", fontsize=14, color='white')
        ax.axis('off')
        
        # Dark Background
        fig.patch.set_facecolor('#050505')
        ax.set_facecolor('#050505')
        
        fname = f"temp_flux_{i:03d}.png"
        plt.savefig(fname, bbox_inches='tight', dpi=120, facecolor=fig.get_facecolor())
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames_buffer.append(img.copy())
        os.remove(fname)

    out_name = f"cmb_helical_flux_hq.gif"
    frames_buffer[0].save(out_name, save_all=True, append_images=frames_buffer[1:], 
                          duration=GIF_DURATION, loop=0)
    print(f"\n✅ Simulation Complete: {out_name}")

if __name__ == "__main__":
    run_helical_simulation()