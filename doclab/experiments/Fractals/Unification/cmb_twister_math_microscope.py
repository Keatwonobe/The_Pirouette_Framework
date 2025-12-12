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

# ZOOM CONFIGURATION
LMAX = 300          # High Res Mode (Was 60). Unlocks fine detail.
                    # Warning: Setting > 400 may freeze standard RAM/CPU.
FOV_DEG = 8.0       # Field of View (Degrees). 8.0 is a tight zoom on the center.
N_RES = 400         # Resolution of the window (400x400 pixels)

GIF_FRAMES = 60
GIF_DURATION = 100 

# THE SINGULARITY CROSSING
# We scan extremely close to k=1 to see the "node" structure
K_RANGE = np.linspace(0.9995, 1.0005, GIF_FRAMES) 

# ======================
# GLOBAL CACHE
# ======================
YLM_CACHE = None
ALMS_CACHE = None
TH_GRID = None
PH_GRID = None

def get_alm_and_zoom_grid(fits_path, lmax, n_res, fov_deg):
    global YLM_CACHE, ALMS_CACHE, TH_GRID, PH_GRID
    if ALMS_CACHE is not None: return
        
    print(f"[*] Initializing Planck Microscope...")
    print(f"    Target: Galactic Center (0,0)")
    print(f"    Zoom Level: {fov_deg}° FOV")
    print(f"    Harmonic Resolution: LMAX={lmax} (High Detail)")

    # 1. Load FITS
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        return

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    # 2. Healpix Setup for Analysis
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # 3. Compute a_lm (Global Decomposition)
    # We need global a_lm first, even for a local zoom.
    print("    Phase 1: Computing Spherical Harmonic Coefficients...")
    # Sampling grid for integration
    n_theta = lmax * 3
    n_phi = lmax * 3
    theta_alm = np.linspace(0, np.pi, n_theta)
    phi_alm = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(theta_alm, phi_alm, indexing='ij')
    
    # Project sphere to map
    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    # Weights
    dtheta = theta_alm[1] - theta_alm[0]
    dphi = phi_alm[1] - phi_alm[0]
    weights = np.sin(TH_ALM) * dtheta * dphi
    
    alms = {}
    # Optimization: Only compute m up to l (symmetric) but Python loop is bottleneck
    # We stick to full loop for correctness of phase twist
    count = 0
    total = (lmax*(lmax+1))/2 + lmax
    
    # This loop is heavy. 
    for l in range(lmax + 1):
        # Progress check
        if l % 50 == 0: print(f"      Processing L={l}/{lmax}...")
        
        # Vectorize m calculation for this l
        m_range = np.arange(-l, l + 1)
        # scipy sph_harm supports broadcasting: sph_harm(m, l, phi, theta)
        # But we must iterate m to store in dict for the synthesizer
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM) 
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    ALMS_CACHE = alms
    
    # 4. Generate ZOOM Grid (The Microscope)
    print("    Phase 2: Generating Zoom Coordinates...")
    
    # Center is Theta=pi/2 (90 deg), Phi=0
    # FOV to Radians
    fov_rad = np.deg2rad(fov_deg)
    
    # Theta range: pi/2 - fov/2 to pi/2 + fov/2
    th_min = (np.pi/2) - (fov_rad/2)
    th_max = (np.pi/2) + (fov_rad/2)
    
    # Phi range: -fov/2 to +fov/2
    ph_min = -fov_rad/2
    ph_max = fov_rad/2
    
    theta = np.linspace(th_min, th_max, n_res)
    phi = np.linspace(ph_min, ph_max, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')

    # 5. Cache Y_lm for the ZOOM GRID
    print(f"    Phase 3: Caching Local Y_lm values for {n_res}x{n_res} grid...")
    YLM_CACHE = {}
    for l in range(lmax + 1):
        if l % 50 == 0: print(f"      Caching L={l}...")
        for m in range(-l, l + 1):
            YLM_CACHE[(l, m)] = sph_harm(m, l, PH_GRID, TH_GRID)

    print("    [*] Initialization Complete.")

def synthesize_twisted_zoom(k, lmax):
    # Same logic, but operates on the tiny ZOOM grid
    map_out = np.zeros_like(TH_GRID, dtype=np.complex128)
    delta_phi_multiplier = (k - 1) * PH_GRID
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            alm = ALMS_CACHE[(l, m)]
            Y_lm_untwisted = YLM_CACHE[(l, m)]
            # The Twist Logic
            phase_corr = np.exp(1j * m * delta_phi_multiplier)
            map_out += alm * Y_lm_untwisted * phase_corr
            
    return map_out.real

def run_microscope():
    get_alm_and_zoom_grid(FITS_PATH, LMAX, N_RES, FOV_DEG)
    if ALMS_CACHE is None: return

    print(f"\n[*] Starting Micro-Scan of the Singularity...")
    frames_buffer = []
    
    # Reference (k=1)
    T_ref = synthesize_twisted_zoom(1.0, LMAX)
    T_ref_std = np.std(T_ref)
    T_ref_norm = T_ref / T_ref_std
    
    for i, k_val in enumerate(K_RANGE):
        if (i + 1) % 5 == 0:
            print(f"  Frame {i+1}/{GIF_FRAMES} (k={k_val:.6f})...")

        # Synthesize Twist
        T_twist = synthesize_twisted_zoom(k_val, LMAX)
        T_twist_norm = T_twist / T_ref_std
        
        # --- PHYSICS ---
        # 1. Interference (The Structure)
        # We use a harder power law (0.4) to see the faint details near the nulls
        L1_Interference = np.abs(T_ref_norm - T_twist_norm)
        vis_interference = np.power(L1_Interference, 0.6)

        # 2. The Flash (The Singularity)
        # Tighter tolerance for the flash since we are zoomed in
        diff_mag = np.abs(T_ref_norm - T_twist_norm)
        L2_Flash = np.exp(-1.0 * (diff_mag**2) * 200.0) # Sharper flash
        
        # Composite
        vis_data = vis_interference + (L2_Flash * 0.9)
        
        # Plotting
        fig, ax = plt.subplots(figsize=(8, 8)) # Square aspect for the zoom
        
        # Coordinate labels for the zoom
        extent = (-FOV_DEG/2, FOV_DEG/2, -FOV_DEG/2, FOV_DEG/2)
        
        im = ax.imshow(vis_data, extent=extent, cmap='magma', 
                       norm=colors.Normalize(vmin=0, vmax=np.max(vis_data)), 
                       origin='lower')
        
        # HUD
        if abs(k_val - 1.0) < 0.00001:
            title = ">>> SINGULARITY [CENTER] <<<"
        else:
            title = f"Zoom {FOV_DEG} deg | k = {k_val:.6f}"
            
        ax.set_title(title, fontsize=12, color='white', pad=10)
        ax.set_xlabel("Galactic Longitude Offset (deg)", fontsize=8, color='gray')
        ax.set_ylabel("Galactic Latitude Offset (deg)", fontsize=8, color='gray')
        
        # Styling
        ax.tick_params(axis='x', colors='gray')
        ax.tick_params(axis='y', colors='gray')
        for spine in ax.spines.values(): spine.set_color('#333333')
        
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')

        fname = f"temp_zoom_{i:03d}.png"
        plt.savefig(fname, bbox_inches='tight', dpi=100, facecolor='black')
        plt.close(fig)

        with Image.open(fname) as img:
            frames_buffer.append(img.copy())
        os.remove(fname)

    out_name = "cmb_singularity_microscope.gif"
    if frames_buffer:
        frames_buffer[0].save(out_name, save_all=True, append_images=frames_buffer[1:], 
                              duration=GIF_DURATION, loop=0)
        print(f"\n✅ Microscope Scan Complete: {out_name}")

if __name__ == "__main__":
    run_microscope()