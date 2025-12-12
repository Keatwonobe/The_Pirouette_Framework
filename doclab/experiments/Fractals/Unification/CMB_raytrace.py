import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import gaussian_filter
import astropy.units as u
from astropy.coordinates import SkyCoord
import os
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits" # Requires this file to run
LMAX = 40          
N_RES = 300        
K_TRACE = 3.14159265 # k = pi for a complex, non-singular map
GAMMA = 0.5        # Drag/Damping
DT = 0.05          # Time step
STEPS = 500        # Simulation steps

# ======================
# GLOBAL CACHE (Copied from cmb_pi_gif.py)
# ======================
YLM_CACHE = None
ALMS_CACHE = None
TH_GRID = None
PH_GRID = None
I_MAP_CMB = None # The static interference map

# ======================
# 1. HELPER: Get ALM (Initialization/Caching) - Minimal Changes
# ======================
# (Function get_alm_and_grid is defined here, exactly as in cmb_pi_gif.py)
def get_alm_and_grid(fits_path, lmax, n_res):
    global YLM_CACHE, ALMS_CACHE, TH_GRID, PH_GRID
    
    if ALMS_CACHE is not None:
        return
        
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {fits_path}. Please ensure {fits_path} is available.")
        sys.exit(1)

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

# ======================
# 2. FAST HARMONIC SYNTHESIS (Copied from cmb_pi_gif.py)
# ======================
def synthesize_twisted_universe_fast(k, lmax):
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
# 3. FORCE FUNCTION (New - Derived from CMB Gradient)
# ======================
def get_force_from_cmb(theta_idx, phi_idx, I_map):
    """
    Calculates the force vector for a particle at (theta_idx, phi_idx)
    using the negative gradient of the Interference Map (I_map).
    The map is an N_RES x N_RES array.
    """
    
    # Use a small finite difference approximation for the gradient at a point
    
    # 1. Gradient in the Latitude/Theta direction (rows/index 0)
    # Clamp indices to ensure they are within bounds
    # F_theta ~ -(I[i+1, j] - I[i-1, j]) / (2 * dtheta)
    i_plus = min(theta_idx + 1, N_RES - 1)
    i_minus = max(theta_idx - 1, 0)
    
    dI_dtheta = (I_map[i_plus, phi_idx] - I_map[i_minus, phi_idx]) / 2.0
    
    # 2. Gradient in the Longitude/Phi direction (columns/index 1)
    # F_phi ~ -(I[i, j+1] - I[i, j-1]) / (2 * dphi)
    j_plus = (phi_idx + 1) % N_RES # Wrap around longitude
    j_minus = (phi_idx - 1) % N_RES # Wrap around longitude
    
    dI_dphi = (I_map[theta_idx, j_plus] - I_map[theta_idx, j_minus]) / 2.0
    
    # The force is the negative gradient: F = -nabla I
    F_theta = -dI_dtheta
    F_phi = -dI_dphi
    
    return F_theta, F_phi

# ======================
# 4. RAY TRACE MAIN FUNCTION
# ======================
def run_cmb_raytrace_analysis():
    global I_MAP_CMB
    
    # 1. Pre-computation (a_lm)
    get_alm_and_grid(FITS_PATH, LMAX, N_RES)
    if ALMS_CACHE is None: return

    # 2. Generate Static CMB Interference Landscape (I_map)
    print(f"\n[*] Generating Reference Map (k=1.0)...")
    T_ref = synthesize_twisted_universe_fast(1.0, LMAX)
    print(f"[*] Generating Twisted Map (k={K_TRACE:.4f})...")
    T_twist = synthesize_twisted_universe_fast(K_TRACE, LMAX)
    I_map = np.abs(T_ref - T_twist)
    
    # Smooth the map slightly to get a more stable gradient (optional, but recommended)
    I_MAP_CMB = gaussian_filter(I_map, sigma=1.0) 
    
    print(f"\n[*] Starting CMB Ray-Tracing Simulation ({STEPS} steps)...")
    
    # Initial particle positions (indices into the N_RES x N_RES grid)
    # m = longitude index, lam = latitude index
    # Note: We use the array indices directly as the coordinate space
    l_range = np.arange(N_RES)
    m_range = np.arange(N_RES)
    
    L_START, M_START = np.meshgrid(l_range, m_range, indexing='ij')
    
    # Position: m (longitude index), lam (latitude index)
    m_pos = M_START.flatten().astype(np.float64)
    lam_pos = L_START.flatten().astype(np.float64)
    
    # Momentum/Velocity
    pm = np.zeros_like(m_pos)
    plam = np.zeros_like(lam_pos)
    
    # Coherence Accumulator (Inverse Lyapunov)
    coherence = np.zeros_like(m_pos)
    
    prev_pm = np.zeros_like(m_pos)
    prev_plam = np.zeros_like(lam_pos)
    
    num_particles = m_pos.size
    
    for step in range(STEPS):
        
        # Get Force (F_theta = F_lam, F_phi = F_m)
        # We need to map the float position back to integer indices for gradient lookup
        m_idx = np.clip(m_pos.astype(int), 0, N_RES - 1)
        lam_idx = np.clip(lam_pos.astype(int), 0, N_RES - 1)
        
        Fm = np.zeros_like(m_pos)
        Flam = np.zeros_like(lam_pos)

        # Vectorized force lookup (Loop is unavoidable here for efficiency in a large array)
        # In a production environment, this would be done with interpolation, 
        # but the simple index lookup simulates a discrete field influence.
        for i in range(num_particles):
             # Force in phi (longitude/m) direction, Force in theta (latitude/lam) direction
            F_theta, F_phi = get_force_from_cmb(lam_idx[i], m_idx[i], I_MAP_CMB)
            Flam[i] = F_theta
            Fm[i] = F_phi


        # Full Step (Velocity Verlet-like integration)
        
        # 1. Update Momentum (p = p + 0.5 * F * dt)
        pm += 0.5 * DT * Fm
        plam += 0.5 * DT * Flam
        
        # 2. Apply Drag and Update Position (r = r + p * dt)
        drag_factor = 1.0 / (1.0 + 0.5 * DT * GAMMA) # Constant drag
        pm *= drag_factor
        plam *= drag_factor
        
        m_pos += DT * pm
        lam_pos += DT * plam
        
        # Wrap positions (Longitude: m_pos)
        m_pos = m_pos % N_RES
        # Reflect positions (Latitude: lam_pos)
        # If lam_pos goes outside [0, N_RES-1], reflect the position and reverse the velocity
        out_upper = lam_pos >= N_RES
        lam_pos[out_upper] = (N_RES - 1) - (lam_pos[out_upper] - (N_RES - 1))
        plam[out_upper] *= -1.0 # Reverse velocity upon reflection
        
        out_lower = lam_pos < 0
        lam_pos[out_lower] = -lam_pos[out_lower] # Reflect from 0
        plam[out_lower] *= -1.0 # Reverse velocity upon reflection
        
        # 3. Update Momentum (p = p + 0.5 * F * dt) - Look up force at new position
        m_idx = np.clip(m_pos.astype(int), 0, N_RES - 1)
        lam_idx = np.clip(lam_pos.astype(int), 0, N_RES - 1)
        
        for i in range(num_particles):
            F_theta, F_phi = get_force_from_cmb(lam_idx[i], m_idx[i], I_MAP_CMB)
            Flam[i] = F_theta
            Fm[i] = F_phi
            
        pm += 0.5 * DT * Fm
        plam += 0.5 * DT * Flam
        
        # --- Coherence Calculation ---
        v_mag = np.sqrt(pm**2 + plam**2) + 1e-9
        prev_mag = np.sqrt(prev_pm**2 + prev_plam**2) + 1e-9
        
        dot = (pm * prev_pm + plam * prev_plam) / (v_mag * prev_mag)
        
        # Accumulate smoothness
        coherence += np.maximum(0, dot)
        
        prev_pm = pm.copy()
        prev_plam = plam.copy()
        
        if step % 50 == 0: print(f"  Exposure {step}/{STEPS}...")

    # 5. Process and Plot Image
    luminosity = coherence.reshape(N_RES, N_RES)
    luminosity = np.log1p(luminosity)
    
    # Longitude/Latitude Extent for Plotting
    extent = (np.rad2deg(PH_GRID.min()), np.rad2deg(PH_GRID.max()), 
              np.rad2deg(0.5*np.pi - TH_GRID.max()), np.rad2deg(0.5*np.pi - TH_GRID.min()))

    plt.figure(figsize=(10, 6.2), facecolor='black')
    
    plt.imshow(luminosity, extent=extent, 
               origin='lower', cmap='plasma')
    
    plt.title(f"CMB Topological Field Coherence (k={K_TRACE:.4f}, LMAX={LMAX})", 
              color='white', fontsize=14)
    plt.xlabel("Galactic Longitude (deg)", color='white')
    plt.ylabel("Galactic Latitude (deg)", color='white')
    
    # Set tick colors
    ax = plt.gca()
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    plt.tight_layout()
    plt.savefig('cmb_topological_coherence.png')
    # plt.show() # Disabled for automated execution
    
    print("\n✅ Analysis Complete. Image saved to cmb_topological_coherence.png")

if __name__ == "__main__":
    # Note: Requires COM_CompMap_CMB-smica_2048_R1.20.fits to run
    run_cmb_raytrace_analysis()