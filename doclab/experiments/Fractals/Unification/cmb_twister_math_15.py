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
LMAX = 60          # Higher LMAX = More Fractal Detail (v4 was 40, v14 was blurred)
N_RES = 400        # Resolution
GIF_FRAMES = 60
GIF_DURATION = 100 

# The Singularity Crossing (Crossing k=1.0)
K_RANGE = np.linspace(0.9999999990, 1.0000000010, GIF_FRAMES) 

# ======================
# GLOBAL CACHE (The Harmonic Engine)
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

    # Handle various FITS structures
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    # Healpix Setup
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Pre-compute spherical harmonics for analysis
    n_theta_alm = lmax * 4
    n_phi_alm = lmax * 8
    theta_alm = np.linspace(0, np.pi, n_theta_alm)
    phi_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(theta_alm, phi_alm, indexing='ij')
    
    # Project to find a_lm
    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    # Integration weights
    dtheta = theta_alm[1] - theta_alm[0]
    dphi = phi_alm[1] - phi_alm[0]
    weights = np.sin(TH_ALM) * dtheta * dphi
    
    print(f"[*] Computing Harmonic Coefficients (LMAX={lmax})...")
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM) 
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    
    ALMS_CACHE = alms
    
    # Create Output Grid
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')

    print(f"[*] Caching UNTWISTED Y_lm on {n_res}x{n_res} grid...")
    YLM_CACHE = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            YLM_CACHE[(l, m)] = sph_harm(m, l, PH_GRID, TH_GRID)

def synthesize_twisted_universe(k, lmax):
    """
    Synthesizes the map with a phase twist multiplier k.
    """
    map_out = np.zeros_like(TH_GRID, dtype=np.complex128)
    # The Twist: Multiplies the azimuthal angle phi
    delta_phi_multiplier = (k - 1) * PH_GRID
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            alm = ALMS_CACHE[(l, m)]
            Y_lm_untwisted = YLM_CACHE[(l, m)]
            # Apply phase shift analytically (Preserves Fractals)
            phase_corr = np.exp(1j * m * delta_phi_multiplier)
            map_out += alm * Y_lm_untwisted * phase_corr
            
    return map_out.real

# ======================
# MAIN EXECUTION
# ======================
def run_hybrid_generator():
    
    get_alm_and_grid(FITS_PATH, LMAX, N_RES)
    if ALMS_CACHE is None: return

    print(f"\n[*] Starting Composite Fractal Scan...")

    frames_buffer = []
    
    # 1. Synthesize Reference ONCE (k=1)
    print("[*] Generating Reference Manifold...")
    T_ref = synthesize_twisted_universe(1.0, LMAX)
    
    # Normalize Reference for consistent math
    T_ref_std = np.std(T_ref)
    T_ref_norm = T_ref / T_ref_std
    
    for i, k_val in enumerate(K_RANGE):
        if (i + 1) % 5 == 0:
            print(f"  Frame {i+1}/{GIF_FRAMES} (k={k_val:.6f})...")

        # 2. Synthesize Twisted Reality
        T_twist = synthesize_twisted_universe(k_val, LMAX)
        T_twist_norm = T_twist / T_ref_std # Use ref std to keep scales locked
        
        # --- LAYER A: FRACTAL INTERFERENCE (The "Body") ---
        # Logic: |A - B|. This is 0 at k=1, High at k!=1.
        # This creates the dark interference fringes.
        L1_Interference = np.abs(T_ref_norm - T_twist_norm)
        
        # Enhance contrast for fractals (Gamma Compression)
        L1_Interference = np.power(L1_Interference, 0.5) 

        # --- LAYER B: COHERENCE FLASH (The "Spirit") ---
        # Logic: 1.0 at k=1 (Perfect alignment), drops off quickly.
        # We model this as the inverse of the difference, smoothed slightly.
        diff_mag = np.abs(T_ref_norm - T_twist_norm)
        
        # A bell curve that peaks at diff=0 (Singularity)
        # This creates the white flash when the maps align.
        L2_Flash = np.exp(-1.0 * (diff_mag**2) * 50.0) 
        
        # --- COMPOSITE ---
        # When far from k=1: Interference dominates.
        # When at k=1: Flash dominates.
        vis_data = L1_Interference + (L2_Flash * 0.8)
        
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6.2))
        extent = (-180, 180, -90, 90)
        
        # Use Inferno for that "Energy" look
        im = ax.imshow(vis_data, extent=extent, cmap='inferno', 
                       norm=colors.Normalize(vmin=0, vmax=np.max(vis_data)), 
                       origin='lower')
        
        # Dynamic Title
        if abs(k_val - 1.0) < 0.00005:
            title_text = ">>> SINGULARITY ALIGNMENT <<<"
        else:
            title_text = f"Topological Stress: k = {k_val:.6f}"

        ax.set_title(title_text, fontsize=14, color='white')
        ax.axis('off')
        
        # Dark Background for maximum contrast
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')

        # Save frame
        frame_filename = f"temp_hybrid_{i:03d}.png"
        plt.savefig(frame_filename, bbox_inches='tight', dpi=100, facecolor='black')
        plt.close(fig)

        with Image.open(frame_filename) as img:
            frames_buffer.append(img.copy()) 
        os.remove(frame_filename) 

    # Save GIF
    output_filename = f"cmb_fractal_singularity.gif"
    if frames_buffer:
        frames_buffer[0].save(
            output_filename,
            save_all=True,
            append_images=frames_buffer[1:],
            duration=GIF_DURATION,
            loop=0
        )
        print(f"\n✅ GIF saved: {output_filename}")

if __name__ == "__main__":
    run_hybrid_generator()