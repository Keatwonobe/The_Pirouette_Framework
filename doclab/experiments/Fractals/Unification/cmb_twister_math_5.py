import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord
from PIL import Image
import os
import time

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60          # Increased back to 60 because optimization makes it fast
N_RES = 400        # Resolution back to 400
GIF_FRAMES = 60
GIF_DURATION = 100 

# Focusing tightly on the singularity
# We avoid exactly 1.0 in the list to prevent division by zero in derivative mode
# unless we handle it specifically, but for interference, 1.0 is fine.
K_RANGE = np.linspace(0.99999999, 1.00000001, GIF_FRAMES) 

# Mode: 'interference' (original) or 'flux' (derivative/Lyapunov-like)
VISUALIZATION_MODE = 'flux' 

# ======================
# GLOBAL CACHE
# ======================
BASE_MAPS_BY_M = {} # The new cache structure
TH_GRID = None
PH_GRID = None
T_REF_CACHE = None

def load_and_precompute_bases(fits_path, lmax, n_res):
    global BASE_MAPS_BY_M, TH_GRID, PH_GRID, T_REF_CACHE
    
    if BASE_MAPS_BY_M: return

    print(f"[*] Loading CMB data...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] File not found: {fits_path}")
        return

    # Handle FITS structure
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    # Healpix setup
    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Generate Grid
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    # Sample CMB to get alms
    # Note: We do a simplified alm extraction on the grid for speed in this demo
    # For high precision, using healpy.map2alm is better, but this matches your logic
    print(f"[*] Extracting a_lm coefficients (LMAX={lmax})...")
    
    # Create extraction grid
    n_theta_alm = lmax * 4
    n_phi_alm = lmax * 8
    th_alm = np.linspace(0, np.pi, n_theta_alm)
    ph_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(th_alm, ph_alm, indexing='ij')
    
    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    dtheta = th_alm[1] - th_alm[0]
    dphi = ph_alm[1] - ph_alm[0]
    weights = np.sin(TH_ALM) * dtheta * dphi
    
    # --- THE OPTIMIZATION STEP ---
    print(f"[*] Pre-computing Base Maps (Grouping by m)...")
    
    # Initialize dictionary for m
    # Range of m is -lmax to lmax
    for m in range(-lmax, lmax + 1):
        BASE_MAPS_BY_M[m] = np.zeros_like(TH_GRID, dtype=np.complex128)

    # Populate Base Maps
    # We loop L first, then M, but we accumulate into the M-bucket
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            # Calculate Y_lm on the visualization grid
            Y_lm = sph_harm(m, l, PH_GRID, TH_GRID)
            
            # Calculate Y_lm on the extraction grid
            Y_lm_ex = sph_harm(m, l, PH_ALM, TH_ALM)
            
            # Get a_lm
            alm = np.sum(T_sample * np.conjugate(Y_lm_ex) * weights)
            
            # Accumulate into the base map for this m
            BASE_MAPS_BY_M[m] += alm * Y_lm

    print(f"[*] Pre-computation complete. Ready for real-time twisting.")

    # Cache T_ref (k=1 means phase shift is 0)
    T_REF_CACHE = np.zeros_like(TH_GRID, dtype=np.complex128)
    for m, base_map in BASE_MAPS_BY_M.items():
        T_REF_CACHE += base_map
    T_REF_CACHE = T_REF_CACHE.real

def synthesize_twisted_optimized(k):
    # This function is now O(L) instead of O(L^2)
    # It sums the pre-computed base maps with the phase shift
    map_out = np.zeros_like(TH_GRID, dtype=np.complex128)
    
    twist_factor = (k - 1)
    
    for m, base_map in BASE_MAPS_BY_M.items():
        if m == 0:
            map_out += base_map # m=0 has no phase shift
        else:
            # The Twist: phase depends only on m and grid phi
            phase = np.exp(1j * m * twist_factor * PH_GRID)
            map_out += base_map * phase
            
    return map_out.real

def run_simulation():
    load_and_precompute_bases(FITS_PATH, LMAX, N_RES)
    if not BASE_MAPS_BY_M: return

    print(f"\n[*] Rendering {GIF_FRAMES} frames in '{VISUALIZATION_MODE}' mode...")
    frames_buffer = []
    
    start_time = time.time()
    
    for i, k_val in enumerate(K_RANGE):
        if i % 10 == 0: print(f"  Frame {i}/{GIF_FRAMES}...")
        
        T_twist = synthesize_twisted_optimized(k_val)
        
        if VISUALIZATION_MODE == 'interference':
            # Original mode: |T_ref - T_twist|
            # Approaches 0 as k->1
            data = np.abs(T_REF_CACHE - T_twist)
            norm_power = 0.4
            title_prefix = "Interference"
            cmap = 'inferno'
            
        elif VISUALIZATION_MODE == 'flux':
            # FLUX MODE: (T_ref - T_twist) / (1 - k)
            # This approximates dT/dk. It will NOT fade to black at k=1.
            # It shows the "potential energy" of the tear.
            
            diff = np.abs(T_REF_CACHE - T_twist)
            epsilon = 1e-9 # Avoid division by zero
            denom = abs(1.0 - k_val)
            if denom < epsilon: denom = epsilon
                
            data = diff / denom
            norm_power = 0.5
            title_prefix = "Topological Flux (dT/dk)"
            cmap = 'magma' # Distinct from inferno for flux
            
        # Visualization
        vis_data = np.power(data, norm_power)
        v_min, v_max = vis_data.min(), vis_data.max()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        im = ax.imshow(vis_data, extent=(-180, 180, -90, 90), cmap=cmap,
                       norm=colors.Normalize(vmin=v_min, vmax=v_max), origin='lower')
        
        ax.set_title(f"{title_prefix}: k = {k_val:.8f}")
        plt.axis('off')
        
        # Save to buffer
        fname = f"temp_{i}.png"
        plt.savefig(fname, bbox_inches='tight', dpi=100)
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames_buffer.append(img.copy())
        os.remove(fname)

    elapsed = time.time() - start_time
    print(f"\n[*] Render time: {elapsed:.2f}s (Avg {elapsed/GIF_FRAMES:.2f}s/frame)")

    out_name = f"cmb_{VISUALIZATION_MODE}_lmax{LMAX}.gif"
    frames_buffer[0].save(out_name, save_all=True, append_images=frames_buffer[1:], 
                          duration=GIF_DURATION, loop=0)
    print(f"[*] Saved: {out_name}")

if __name__ == "__main__":
    run_simulation()