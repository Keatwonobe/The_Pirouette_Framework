import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import gaussian_filter
import astropy.units as u
from astropy.coordinates import SkyCoord
from PIL import Image
import os
import sys

# ======================
# CONFIGURATION
# ======================
# NOTE: This FITS file must be present in the working directory to run.
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits" 
LMAX = 40          # Max spherical harmonic degree
N_RES = 150        # Resolution for the trace grid 
GIF_FRAMES = 50    # Number of frames for the animation (lowered for speed)
GIF_DURATION = 100 # Frame duration in ms

# Ray-Tracing Parameters
GAMMA = 0.5        # Drag/Damping
DT = 0.05          # Time step
STEPS = 200        # Simulation steps per frame (lowered for speed)

# k-sweep around pi (The 'cycle 1' traversal)
K_START = 2.8
K_END = 3.5
K_RANGE = np.linspace(K_START, K_END, GIF_FRAMES, endpoint=True) 

# ======================
# GLOBAL CACHE 
# ======================
YLM_CACHE = None
ALMS_CACHE = None
TH_GRID = None
PH_GRID = None

# ======================
# 1. CMB Initialization & Synthesis Functions
# ======================
def get_alm_and_grid(fits_path, lmax, n_res):
    global YLM_CACHE, ALMS_CACHE, TH_GRID, PH_GRID
    
    if ALMS_CACHE is not None:
        return
        
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {fits_path}. Please ensure it is in the working directory.")
        sys.exit(1)

    # Data extraction logic from cmb_pi_gif.py
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
    
    # a_lm computation setup
    n_theta_alm = lmax * 4
    n_phi_alm = lmax * 8
    theta_alm = np.linspace(0, np.pi, n_theta_alm)
    phi_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(theta_alm, phi_alm, indexing='ij')
    
    # Coordinate sampling
    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    # Integration weights
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
    
    # Generate Synthesis Grid for plotting/tracing
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')

    print(f"[*] Caching UNTWISTED Y_lm on {n_res}x{n_res} grid...")
    YLM_CACHE = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            YLM_CACHE[(l, m)] = sph_harm(m, l, PH_GRID, TH_GRID)


def synthesize_twisted_universe_fast(k, lmax):
    # Synthesis logic from cmb_pi_gif.py
    if TH_GRID is None or ALMS_CACHE is None:
        return np.zeros((N_RES, N_RES))

    map_out = np.zeros_like(TH_GRID, dtype=np.complex128)
    delta_phi_multiplier = (k - 1) * PH_GRID
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            alm = ALMS_CACHE.get((l, m), 0)
            Y_lm_untwisted = YLM_CACHE.get((l, m))
            
            if Y_lm_untwisted is not None:
                phase_corr = np.exp(1j * m * delta_phi_multiplier)
                map_out += alm * Y_lm_untwisted * phase_corr
            
    return map_out.real

# ======================
# 2. FORCE FUNCTION (Gradient Lookup)
# ======================
def get_force_from_cmb(theta_idx, phi_idx, I_map):
    """
    Calculates the force vector using the negative gradient of the Interference Map (I_map).
    F = -nabla I (The ray is attracted to minima in the interference field).
    """
    
    # 1. Gradient in the Latitude/Theta direction (rows/index 0)
    i_plus = min(theta_idx + 1, N_RES - 1)
    i_minus = max(theta_idx - 1, 0)
    dI_dtheta = (I_map[i_plus, phi_idx] - I_map[i_minus, phi_idx]) / 2.0
    
    # 2. Gradient in the Longitude/Phi direction (columns/index 1)
    j_plus = (phi_idx + 1) % N_RES 
    j_minus = (phi_idx - 1) % N_RES 
    dI_dphi = (I_map[theta_idx, j_plus] - I_map[theta_idx, j_minus]) / 2.0
    
    F_theta = -dI_dtheta
    F_phi = -dI_dphi
    
    return F_theta, F_phi

# ======================
# 3. RAY TRACE MAIN FUNCTION
# ======================
def run_ray_trace_coherence(I_map_static):
    """
    Runs the coherence ray-tracing simulation for a single frame.
    """
    
    # Smooth the map slightly to get a more stable gradient
    I_map_filtered = gaussian_filter(I_map_static, sigma=1.0) 
    
    # Initial particle positions (indices into the N_RES x N_RES grid)
    l_range = np.arange(N_RES)
    m_range = np.arange(N_RES)
    L_START, M_START = np.meshgrid(l_range, m_range, indexing='ij')
    
    m_pos = M_START.flatten().astype(np.float64) 
    lam_pos = L_START.flatten().astype(np.float64) 
    
    pm = np.zeros_like(m_pos)
    plam = np.zeros_like(lam_pos)
    coherence = np.zeros_like(m_pos)
    
    prev_pm = np.zeros_like(m_pos)
    prev_plam = np.zeros_like(lam_pos)
    
    num_particles = m_pos.size
    
    for step in range(STEPS):
        
        # --- 1. First Half Step (p = p + 0.5 * F * dt) ---
        m_idx = np.clip(m_pos.astype(int), 0, N_RES - 1)
        lam_idx = np.clip(lam_pos.astype(int), 0, N_RES - 1)
        
        Fm = np.zeros_like(m_pos)
        Flam = np.zeros_like(lam_pos)
        
        for i in range(num_particles):
            F_theta, F_phi = get_force_from_cmb(lam_idx[i], m_idx[i], I_map_filtered)
            Flam[i] = F_theta
            Fm[i] = F_phi
            
        pm += 0.5 * DT * Fm
        plam += 0.5 * DT * Flam
        
        # --- 2. Update Position (r = r + p * dt) & Apply Drag ---
        drag_factor = 1.0 / (1.0 + 0.5 * DT * GAMMA) 
        pm *= drag_factor
        plam *= drag_factor
        
        m_pos += DT * pm
        lam_pos += DT * plam
        
        # Boundary Conditions: Wrap Longitude, Reflect Latitude
        m_pos = m_pos % N_RES
        
        out_upper = lam_pos >= N_RES
        lam_pos[out_upper] = (N_RES - 1) - (lam_pos[out_upper] - (N_RES - 1))
        plam[out_upper] *= -1.0 
        
        out_lower = lam_pos < 0
        lam_pos[out_lower] = -lam_pos[out_lower] 
        plam[out_lower] *= -1.0 
        
        # --- 3. Second Half Step (p = p + 0.5 * F * dt) ---
        m_idx = np.clip(m_pos.astype(int), 0, N_RES - 1)
        lam_idx = np.clip(lam_pos.astype(int), 0, N_RES - 1)
        
        for i in range(num_particles):
            F_theta, F_phi = get_force_from_cmb(lam_idx[i], m_idx[i], I_map_filtered)
            Flam[i] = F_theta
            Fm[i] = F_phi
            
        pm += 0.5 * DT * Fm
        plam += 0.5 * DT * Flam
        
        # --- 4. Coherence Accumulation (Light Source) ---
        v_mag = np.sqrt(pm**2 + plam**2) + 1e-9
        prev_mag = np.sqrt(prev_pm**2 + prev_plam**2) + 1e-9
        
        dot = (pm * prev_pm + plam * prev_plam) / (v_mag * prev_mag)
        coherence += np.maximum(0, dot)
        
        prev_pm = pm.copy()
        prev_plam = plam.copy()
        
    luminosity = coherence.reshape(N_RES, N_RES)
    return np.log1p(luminosity)

# ======================
# 4. MAIN GIF EXECUTION 
# ======================
def run_coherence_gif_generator():
    
    # 1. Pre-computation (a_lm)
    get_alm_and_grid(FITS_PATH, LMAX, N_RES)
    if ALMS_CACHE is None: return

    print(f"\n[*] Starting Coherence GIF generation over k-range {K_START:.4f} to {K_END:.4f}...")

    frames_buffer = []
    
    # 2. Synthesize T_ref (k=1) ONCE
    print("[*] Generating Reference Map (k=1.0)...")
    T_ref = synthesize_twisted_universe_fast(1.0, LMAX)

    # 3. Pre-calculate normalization for consistent coloring
    # We use a trace at k=pi to set the visualization range.
    T_k_pi = synthesize_twisted_universe_fast(np.pi, LMAX)
    I_map_pi = np.abs(T_ref - T_k_pi)
    coherence_ref = run_ray_trace_coherence(I_map_pi)
    v_min, v_max = coherence_ref.min(), coherence_ref.max()
    print(f"[*] Normalization set from k=pi trace: [{v_min:.2f}, {v_max:.2f}]")


    for i, k_val in enumerate(K_RANGE):
        
        print(f"  [-] Frame {i+1}/{GIF_FRAMES}: k = {k_val:.8f}")

        # 4. Generate Static CMB Interference Landscape (I_map) for this k
        T_twist = synthesize_twisted_universe_fast(k_val, LMAX)
        I_map = np.abs(T_ref - T_twist)
        
        # 5. Run the Ray Trace Coherence Simulation
        luminosity = run_ray_trace_coherence(I_map)

        # 6. Plotting
        fig, ax = plt.subplots(figsize=(10, 6.2), facecolor='black')
        
        # Coordinate extent for the plot
        extent = (np.rad2deg(PH_GRID.min()), np.rad2deg(PH_GRID.max()), 
                  np.rad2deg(0.5*np.pi - TH_GRID.max()), np.rad2deg(0.5*np.pi - TH_GRID.min()))
        
        im = ax.imshow(luminosity, extent=extent, 
                       origin='lower', cmap='plasma', 
                       norm=colors.Normalize(vmin=v_min, vmax=v_max))
                       
        ax.set_title(f"CMB Coherence Landscape: k = {k_val:.8f}", 
                     color='white', fontsize=14)
        ax.set_xlabel("Galactic Longitude (deg)", color='white')
        ax.set_ylabel("Galactic Latitude (deg)", color='white')
        
        # Set tick colors
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Log Coherence Accumulation (Enhanced)")

        # Save frame
        frame_filename = f"temp_coherence_frame_{i:03d}.png"
        plt.savefig(frame_filename, bbox_inches='tight', dpi=100, facecolor='black')
        plt.close(fig)

        with Image.open(frame_filename) as img:
            frames_buffer.append(img.copy()) 

        os.remove(frame_filename) 

    # 7. Save GIF
    output_filename = f"cmb_coherence_animation_lmax{LMAX}.gif"
    if frames_buffer:
        frames_buffer[0].save(
            output_filename,
            save_all=True,
            append_images=frames_buffer[1:],
            duration=GIF_DURATION,
            loop=0
        )
        print(f"\n✅ GIF saved: {output_filename}")
    
    print("Computation complete. Please check the GIF output.")


if __name__ == "__main__":
    run_coherence_gif_generator()