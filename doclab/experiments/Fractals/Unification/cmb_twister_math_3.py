import numpy as np
import matplotlib.pyplot as plt
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
GIF_FRAMES = 30
GIF_DURATION = 150 # ms per frame

# Twist range for the animation (k=1 is untwisted)
K_RANGE = np.linspace(0.8, 1.2, GIF_FRAMES, endpoint=False) # A subtle range around k=1

# ======================
# GLOBAL CACHE
# ======================
YLM_CACHE = None
ALMS_CACHE = None
TH_GRID = None
PH_GRID = None

# ======================
# 1. HELPER: Get ALM 
# ======================
def get_alm_and_grid(fits_path, lmax, n_res):
    global YLM_CACHE, ALMS_CACHE, TH_GRID, PH_GRID
    
    if ALMS_CACHE is not None:
        return
        
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {fits_path}")
        return

    # Extract CMB data
    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    # Fill NaNs (if any)
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    
    # HEALPix setup
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Generate Integration Grid (Optimized Resolution for ALM calculation)
    n_theta_alm = lmax * 4
    n_phi_alm = lmax * 8
    theta_alm = np.linspace(0, np.pi, n_theta_alm)
    phi_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(theta_alm, phi_alm, indexing='ij')
    
    # Sample Map
    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    dtheta = theta_alm[1] - theta_alm[0]
    dphi = phi_alm[1] - phi_alm[0]
    weights = np.sin(TH_ALM) * dtheta * dphi
    
    # Compute a_lm
    print(f"[*] Computing a_lm (lmax={lmax})...")
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    
    ALMS_CACHE = alms
    
    # Generate Standard Synthesis Grid (This is the grid for the final image)
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')

    # Pre-compute UNTWISTED Y_lm on the Synthesis Grid and Cache
    print(f"[*] Caching UNTWISTED Y_lm on {n_res}x{n_res} grid...")
    YLM_CACHE = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            YLM_CACHE[(l, m)] = sph_harm(m, l, PH_GRID, TH_GRID)
            
# ======================
# 2. FAST HARMONIC SYNTHESIS
# ======================
def synthesize_twisted_universe_fast(k, lmax):
    """
    Synthesizes the map by reusing cached Y_lm and only applying
    the phase correction factor exp(i * m * (k-1) * phi).
    """
    map_out = np.zeros_like(TH_GRID, dtype=np.complex128)
    
    # This phase correction depends on m, k, and phi
    delta_phi_multiplier = (k - 1) * PH_GRID
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            alm = ALMS_CACHE[(l, m)]
            Y_lm_untwisted = YLM_CACHE[(l, m)]
            
            # Phase correction factor: exp(i * m * (k-1) * phi)
            # The numpy-vectorized way:
            phase_corr = np.exp(1j * m * delta_phi_multiplier)

            # Reconstruct: alm * Y_lm_untwisted * phase_corr
            map_out += alm * Y_lm_untwisted * phase_corr
            
    return map_out.real

# ======================
# 3. MAIN GIF EXECUTION
# ======================
def run_gif_generator():
    
    # 1. Pre-computation (Runs only once)
    get_alm_and_grid(FITS_PATH, LMAX, N_RES)
    if ALMS_CACHE is None: return

    print(f"\n[*] Starting GIF generation over k-range {K_RANGE[0]:.4f} to {K_RANGE[-1]:.4f}...")

    frames_buffer = []
    
    # Determine Color scale based on the untwisted map (k=1)
    map_ref = synthesize_twisted_universe_fast(1.0, LMAX)
    v_min, v_max = map_ref.min(), map_ref.max()
    
    # Set up the colormap and normalization
    cmap = plt.get_cmap('coolwarm')
    norm = plt.Normalize(vmin=v_min, vmax=v_max)
    
    print(f"Rendering {GIF_FRAMES} frames...")
    
    for i, k_val in enumerate(K_RANGE):
        if (i + 1) % 5 == 0:
            print(f"  Frame {i+1}/{GIF_FRAMES} (k={k_val:.4f})...")

        # 2. FAST Synthesis
        map_twist = synthesize_twisted_universe_fast(k_val, LMAX)
        
        # 3. Plotting (Minimalist to keep it fast)
        fig, ax = plt.subplots(figsize=(8, 5))
        extent = (-180, 180, -90, 90)
        
        im = ax.imshow(map_twist, extent=extent, cmap=cmap, norm=norm, origin='lower')
        ax.set_title(f"CMB $\\varphi$-Twist Map: k = {k_val:.8f}")
        ax.set_xlabel("Galactic Longitude (deg)")
        ax.set_ylabel("Galactic Latitude (deg)")
        
        # Add colorbar for context (using the fixed vmin/vmax)
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Temperature $\\Delta T$")
        
        # Save frame to a temporary buffer
        frame_filename = f"temp_frame_{i:03d}.png"
        plt.savefig(frame_filename, bbox_inches='tight', dpi=100)
        plt.close(fig)

        # 4. FIX for PermissionError: Use context manager and copy to ensure
        # the file handle is closed before attempting to remove the file.
        with Image.open(frame_filename) as img:
            frames_buffer.append(img.copy()) 

        # Clean up temporary file
        os.remove(frame_filename) 

    # 5. Save GIF
    output_filename = f"cmb_twist_animation_lmax{LMAX}.gif"
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
    run_gif_generator()