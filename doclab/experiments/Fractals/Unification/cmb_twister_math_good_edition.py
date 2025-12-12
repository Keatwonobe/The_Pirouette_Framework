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

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 40          # Lower LMAX for faster synthesis (original was 60)
N_RES = 300        # Plot resolution (original was 400)
GIF_FRAMES = 60
GIF_DURATION = 150 # ms per frame

# Twist range for the animation (k=1 is untwisted)
# Narrowing the range slightly to keep k=1 in the middle
K_RANGE = np.linspace(0.99999999, 1.00000001, GIF_FRAMES, endpoint=False) 

# ======================
# GLOBAL CACHE (Y_lm, a_lm, Grids)
# (Helper functions get_alm_and_grid and synthesize_twisted_universe_fast 
# are unchanged from the previous optimized version)
# ======================

YLM_CACHE = None
ALMS_CACHE = None
TH_GRID = None
PH_GRID = None

def get_alm_and_grid(fits_path, lmax, n_res):
    global YLM_CACHE, ALMS_CACHE, TH_GRID, PH_GRID
    if ALMS_CACHE is not None: return
        
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {fits_path}")
        return

    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    n_theta_alm = lmax * 4
    n_phi_alm = lmax * 8
    theta_alm = np.linspace(0, np.pi, n_theta_alm)
    phi_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(theta_alm, phi_alm, indexing='ij')
    
    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    dtheta = theta_alm[1] - theta_alm[0]
    dphi = phi_alm[1] - phi_alm[0]
    weights = np.sin(TH_ALM) * dtheta * dphi
    
    print(f"[*] Computing a_lm (lmax={lmax})...")
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM) 
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    
    ALMS_CACHE = alms
    
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')

    print(f"[*] Caching UNTWISTED Y_lm on {n_res}x{n_res} grid...")
    YLM_CACHE = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            YLM_CACHE[(l, m)] = sph_harm(m, l, PH_GRID, TH_GRID)
            
def synthesize_twisted_universe_fast(k, lmax):
    map_out = np.zeros_like(TH_GRID, dtype=np.complex128)
    delta_phi_multiplier = (k - 1) * PH_GRID
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            alm = ALMS_CACHE[(l, m)]
            Y_lm_untwisted = YLM_CACHE[(l, m)]
            phase_corr = np.exp(1j * m * delta_phi_multiplier)
            map_out += alm * Y_lm_untwisted * phase_corr
            
    return map_out.real


# ======================
# 3. MAIN GIF EXECUTION (MODIFIED FOR INTERFERENCE PLOT)
# ======================
def run_interference_gif_generator():
    
    get_alm_and_grid(FITS_PATH, LMAX, N_RES)
    if ALMS_CACHE is None: return

    print(f"\n[*] Starting Interference GIF generation over k-range {K_RANGE[0]:.4f} to {K_RANGE[-1]:.4f}...")

    frames_buffer = []
    
    # 1. Synthesize T_ref (k=1) ONCE
    print("[*] Generating Reference Map (k=1.0)...")
    T_ref = synthesize_twisted_universe_fast(1.0, LMAX)
    
    print(f"Rendering {GIF_FRAMES} frames...")
    
    for i, k_val in enumerate(K_RANGE):
        if (i + 1) % 5 == 0:
            print(f"  Frame {i+1}/{GIF_FRAMES} (k={k_val:.4f})...")

        # 2. FAST Synthesis for current k
        T_twist = synthesize_twisted_universe_fast(k_val, LMAX)
        
        # 3. Calculate Interference Magnitude
        interference_map = np.abs(T_ref - T_twist)
        
        # 4. Normalization and Enhancement (The "Deeply Rendered" Look)
        # Power scaling compresses the dynamic range to reveal faint fringes.
        # This matches the visualization logic of the pi_scanner code.
        vis_data = np.power(interference_map, 0.4) 
        v_min, v_max = vis_data.min(), vis_data.max()
        
        # 5. Plotting
        fig, ax = plt.subplots(figsize=(10, 6.2))
        extent = (-180, 180, -90, 90)
        
        # Use 'inferno' colormap for the high-energy look
        im = ax.imshow(vis_data, extent=extent, cmap='inferno', 
                       norm=colors.Normalize(vmin=v_min, vmax=v_max), 
                       origin='lower')
                       
        ax.set_title(f"Topological Interference Map $|T_{{ref}} - T_{{twist}}|$: k = {k_val:.8f}", fontsize=14)
        ax.set_xlabel("Galactic Longitude (deg)")
        ax.set_ylabel("Galactic Latitude (deg)")
        
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label("Interference Amplitude (Enhanced)", rotation=270, labelpad=15)
        
        # Save frame to a temporary buffer
        frame_filename = f"temp_interference_frame_{i:03d}.png"
        plt.savefig(frame_filename, bbox_inches='tight', dpi=100)
        plt.close(fig)

        # Fix for PermissionError: Use context manager and copy
        with Image.open(frame_filename) as img:
            frames_buffer.append(img.copy()) 

        os.remove(frame_filename) 

    # 6. Save GIF
    output_filename = f"cmb_topological_interference_animation_lmax{LMAX}.gif"
    if frames_buffer:
        frames_buffer[0].save(
            output_filename,
            save_all=True,
            append_images=frames_buffer[1:],
            duration=GIF_DURATION,
            loop=0
        )
        print(f"\n✅ GIF saved: {output_filename} with {GIF_FRAMES} frames.")
    else:
        print("\n[!] Failed to generate GIF frames.")


if __name__ == "__main__":
    # We call the new interference-specific generator
    run_interference_gif_generator()