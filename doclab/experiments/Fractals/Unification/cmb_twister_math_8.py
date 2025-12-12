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
N_RES = 800        # High resolution
GIF_FRAMES = 60
GIF_DURATION = 100 

# The Singularity Probe
K_RANGE = np.linspace(0.99999, 1.00001, GIF_FRAMES) 

# MODE: 'flux' (Lyapunov) or 'interference'
VISUALIZATION_MODE = 'flux' 

# ======================
# 1. THE REFERENCE GENERATOR (Direct Projection)
# ======================
def generate_reference_universe_fast(fits_path, n_res, blur_sigma=4.0):
    print(f"[*] Initializing Reference State (Direct Projection)...")
    
    # 1. Load Data
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        return None, None, None

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    # 2. Healpix Grid Setup
    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # 3. Create Target Grid (Theta, Phi)
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    print(f"    Projecting sky to {n_res}x{n_res} grid...")
    
    # 4. Map Coordinates
    lon_deg = np.rad2deg(PH_GRID)
    lat_deg = np.rad2deg(0.5*np.pi - TH_GRID)
    
    # 5. Interpolate directly (FIXED LINE)
    # We must pass the 'cmb' data array as the third argument
    T_ref = hpix.interpolate_bilinear_lonlat(lon_deg * u.deg, lat_deg * u.deg, cmb)
    
    # 6. Apply smoothing to match LMAX aesthetic
    print(f"    Applying smoothing (sigma={blur_sigma})...")
    T_ref = gaussian_filter(T_ref, sigma=blur_sigma)
        
    return T_ref, TH_GRID, PH_GRID

# ======================
# 2. HELICAL ADVECTION OPERATOR
# ======================
def apply_helical_twist(T_ref, k, n_res):
    """
    Uses Helical Advection: T_twist(phi) = T_ref(k * phi)
    """
    if abs(k - 1.0) < 1e-9:
        return T_ref

    indices_i, indices_j = np.indices(T_ref.shape)
    
    # The Helical Twist scales the Phi index
    center_j = n_res / 2
    indices_j_centered = indices_j - center_j
    indices_j_new = (indices_j_centered * k) + center_j
    
    # Wrap coordinates for periodicity
    indices_j_new_wrapped = indices_j_new % (n_res - 1)
    
    coords = np.array([indices_i, indices_j_new_wrapped])
    
    # Warp the fabric
    T_twisted = map_coordinates(T_ref, coords, order=1, mode='nearest')
    
    return T_twisted

# ======================
# 3. MAIN LOOP
# ======================
def run_helical_simulation():
    start_time = time.time()
    
    T_ref, TH, PH = generate_reference_universe_fast(FITS_PATH, N_RES, blur_sigma=4.0)
    
    if T_ref is None: return
    print(f"[*] Reference Map Generated in {time.time() - start_time:.2f}s")

    frames_buffer = []
    print(f"[*] Simulating {GIF_FRAMES} frames using Helical Advection...")

    for i, k in enumerate(K_RANGE):
        if i % 10 == 0: print(f"  Frame {i}/{GIF_FRAMES} (k={k:.5f})...")

        # B. Apply Operator
        T_twist = apply_helical_twist(T_ref, k, N_RES)
        
        # C. Compute Observable
        if VISUALIZATION_MODE == 'flux':
            # Lyapunov / Flux Probe
            denom = (k - 1.0)
            if abs(denom) < 1e-9: denom = 1e-9
            
            # The Flux is (Strain / Distance from Unity)
            data = np.abs(T_ref - T_twist) / abs(denom)
            norm_power = 0.5
            title = f"Helical Flux (Lyapunov Gradient): k={k:.8f}"
            cmap = 'magma'
            
        else:
            # Interference
            data = np.abs(T_ref - T_twist)
            norm_power = 0.4
            title = f"Interference Magnitude: k={k:.8f}"
            cmap = 'inferno'

        # D. Render
        vis_data = np.power(data, norm_power)
        v_min, v_max = vis_data.min(), vis_data.max()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        im = ax.imshow(vis_data, extent=(-180, 180, -90, 90), cmap=cmap,
                       norm=colors.Normalize(vmin=v_min, vmax=v_max), origin='lower')
        
        ax.set_title(title, fontsize=14, color='white')
        ax.set_axis_off()
        
        # Dark mode styling
        fig.patch.set_facecolor('#050505')
        ax.set_facecolor('#050505')
        
        fname = f"temp_helical_{i:03d}.png"
        plt.savefig(fname, bbox_inches='tight', dpi=100, facecolor=fig.get_facecolor())
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames_buffer.append(img.copy())
        os.remove(fname)

    # E. Save
    out_name = f"cmb_helical_{VISUALIZATION_MODE}_scan.gif"
    frames_buffer[0].save(out_name, save_all=True, append_images=frames_buffer[1:], 
                          duration=GIF_DURATION, loop=0)
    print(f"\n✅ Simulation Complete. Saved to {out_name}")

if __name__ == "__main__":
    run_helical_simulation()