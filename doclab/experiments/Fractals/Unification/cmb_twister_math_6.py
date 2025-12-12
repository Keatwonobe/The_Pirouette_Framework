import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import map_coordinates
import astropy.units as u
from astropy.coordinates import SkyCoord
from PIL import Image
import os
import time

# ======================
# HELICAL CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60          # We can afford high resolution now because interpolation is cheap
N_RES = 600        # Higher pixel resolution for the art print quality
GIF_FRAMES = 60
GIF_DURATION = 100 

# The Singularity scan range
K_RANGE = np.linspace(0.99999, 1.00001, GIF_FRAMES) 

# MODE: 'flux' probes the singularity energy (Lyapunov). 
# 'interference' shows the classic fringe patterns.
VISUALIZATION_MODE = 'flux' 

# ======================
# 1. THE REFERENCE GENERATOR (Run Once)
# ======================
def generate_reference_universe(fits_path, lmax, n_res):
    print(f"[*] Initializing Helical Reference State (LMAX={lmax})...")
    
    # 1. Load Data
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        return None, None, None

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    # 2. Healpix Grid
    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # 3. Create Visualization Grid (theta, phi)
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res) # Full circle
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    # 4. Extract ALMs (The "Weaving" Step - done only once)
    print("    Extracting spherical harmonics...")
    # Use a sampling grid for ALM integration
    n_sample = lmax * 3
    th_s = np.linspace(0, np.pi, n_sample)
    ph_s = np.linspace(-np.pi, np.pi, n_sample*2, endpoint=False)
    TH_S, PH_S = np.meshgrid(th_s, ph_s, indexing='ij')
    
    coords = SkyCoord(l=np.rad2deg((PH_S + 2*np.pi) % (2*np.pi))*u.deg, 
                      b=np.rad2deg(0.5*np.pi - TH_S)*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    # Integration weights
    dth = th_s[1] - th_s[0]
    dph = ph_s[1] - ph_s[0]
    weights = np.sin(TH_S) * dth * dph

    # Synthesize T_ref
    T_ref = np.zeros_like(TH_GRID, dtype=np.complex128)
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm_s = sph_harm(m, l, PH_S, TH_S)
            alm = np.sum(T_sample * np.conjugate(Y_lm_s) * weights)
            
            Y_lm_out = sph_harm(m, l, PH_GRID, TH_GRID)
            T_ref += alm * Y_lm_out
            
    return T_ref.real, TH_GRID, PH_GRID

# ======================
# 2. HELICAL ADVECTION OPERATOR
# ======================
def apply_helical_twist(T_ref, k, n_res):
    """
    Uses the geometric implication of the Helical Derivative:
    Twisting is just advecting the coordinates along phi.
    Complexity: O(N_pixels) instead of O(N_pixels * LMAX^2)
    """
    if abs(k - 1.0) < 1e-9:
        return T_ref

    # 1. Create the target coordinate grid
    # We want the value at (theta, phi) to come from (theta, k*phi)
    # Map index j (phi) -> phi -> k*phi -> index j_new
    
    indices_i, indices_j = np.indices(T_ref.shape)
    
    # Phi range is indices 0 to n_res-1 mapping to -pi to pi
    # The map is periodic in axis 1 (phi)
    
    # Center the scaling around phi=0 (index = n_res/2) or just scale?
    # Your math: exp(i*m*(k-1)*phi) -> implies scaling phi directly.
    
    # Convert index to relative coordinate, scale, convert back
    # But strictly, since phi is periodic [-pi, pi], simple scaling works.
    
    # This factor (k) stretches the index space directly
    # We rely on map_coordinates to handle the fractional lookup
    
    # Twist: The value at index j should come from index j*k?
    # Or value at phi comes from k*phi.
    # Yes.
    
    # For the wrap to work correctly with linspace including endpoints,
    # we treat index space as 0..(N-1) covering 2pi roughly.
    
    # The twist shift:
    shift = (k - 1.0) * (indices_j - n_res/2) # Twist around center?
    # Or simply k * indices_j?
    # Let's align with the math: exp(i m (k-1) phi)
    # This is a phase shift proportional to phi. 
    # It effectively scales phi to k*phi.
    
    indices_j_new = indices_j * k 
    
    # Create the query coordinates
    # Axis 0 (Theta) is untouched
    coords = np.array([indices_i, indices_j_new])
    
    # 2. Interpolate (Advect)
    # mode='wrap' handles the phi periodicity automatically!
    # mode='nearest' handles theta boundaries (poles)
    # We can't mix modes easily in one call in older scipy, 
    # but since theta isn't changing, 'wrap' is safe if we don't shift i.
    
    # Note: map_coordinates applies one mode. 
    # Since we only shift phi (axis 1), we want wrap on axis 1.
    # We can enforce wrap manually for J to be safe.
    
    indices_j_new_wrapped = indices_j_new % (n_res - 1)
    coords_wrapped = np.array([indices_i, indices_j_new_wrapped])
    
    T_twisted = map_coordinates(T_ref, coords_wrapped, order=1, mode='nearest')
    
    return T_twisted

# ======================
# 3. MAIN LOOP
# ======================
def run_helical_simulation():
    # A. Pre-compute (The "Memory")
    start_time = time.time()
    T_ref, TH, PH = generate_reference_universe(FITS_PATH, LMAX, N_RES)
    if T_ref is None: return
    print(f"[*] Reference Map Generated in {time.time() - start_time:.2f}s")

    frames_buffer = []
    print(f"[*] Simulating {GIF_FRAMES} frames using Helical Advection...")

    for i, k in enumerate(K_RANGE):
        # B. Apply Operator (The "Perception")
        T_twist = apply_helical_twist(T_ref, k, N_RES)
        
        # C. Compute Observable
        if VISUALIZATION_MODE == 'flux':
            # Lyapunov / Flux Probe
            # Avoid div/0 at k=1.0 by using a small epsilon
            denom = (k - 1.0)
            if abs(denom) < 1e-9: denom = 1e-9
            
            # The Flux is (Difference / Strain)
            # This reveals the layout of the "Tear"
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
        
        # Dark mode for the "Traveler" vibe
        fig.patch.set_facecolor('#050505')
        ax.set_facecolor('#050505')
        
        # Save
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