import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord
import matplotlib.colors as colors

# ======================
# CONFIGURATION (Re-run for state guarantee)
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 40
N_RES = 300
k_pi = np.pi*2

# ======================
# GLOBAL CACHE
# ======================
YLM_CACHE = None
ALMS_CACHE = None
TH_GRID = None
PH_GRID = None

# ======================
# 1. HELPER: Get ALM (Initialization/Caching)
# (Copied from previous steps)
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
# 2. FAST HARMONIC SYNTHESIS (MODIFIED TO RETURN COMPLEX)
# ======================
def synthesize_twisted_universe_fast(k, lmax, return_complex=False):
    """
    Synthesizes the map by reusing cached Y_lm and only applying
    the phase correction factor exp(i * m * (k-1) * phi).
    """
    if TH_GRID is None or ALMS_CACHE is None:
        raise RuntimeError("Caches not initialized. Call get_alm_and_grid first.")

    map_out = np.zeros_like(TH_GRID, dtype=np.complex128)
    
    delta_phi_multiplier = (k - 1) * PH_GRID
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            # Check for cache existence inside the loop for robustness
            if (l, m) not in ALMS_CACHE or (l, m) not in YLM_CACHE:
                continue

            alm = ALMS_CACHE[(l, m)]
            Y_lm_untwisted = YLM_CACHE[(l, m)]
            
            phase_corr = np.exp(1j * m * delta_phi_multiplier)

            map_out += alm * Y_lm_untwisted * phase_corr
            
    if return_complex:
        return map_out
    else:
        return map_out.real


# ======================
# 3. PHASE ANALYSIS EXECUTION
# ======================
def analyze_pi_phase_singularity():
    print("\n[!!!] Analyzing k=PI PHASE Singularity...")
    
    # 1. Ensure Caches are ready
    get_alm_and_grid(FITS_PATH, LMAX, N_RES)
    if ALMS_CACHE is None: return

    # 2. Synthesize Complex Maps
    print("[*] Synthesizing complex maps for k=1.0 and k=PI...")
    T_ref_c = synthesize_twisted_universe_fast(1.0, LMAX, return_complex=True)
    T_twist_c = synthesize_twisted_universe_fast(k_pi, LMAX, return_complex=True)

    # 3. Calculate Complex Interference and Phase
    I_c = T_ref_c - T_twist_c
    Phase_map = np.angle(I_c) # Phase is in radians [-pi, pi]
    
    # 4. Plot the Phase Map
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), constrained_layout=True)
    extent = (-180, 180, -90, 90)

    # --- Plot 1: Interference Magnitude (for context) ---
    I_map = np.abs(I_c)
    vis_data_mag = np.power(I_map, 0.4) 
    v_min, v_max = vis_data_mag.min(), vis_data_mag.max()
    
    im0 = axes[0].imshow(vis_data_mag, extent=extent, cmap='inferno', 
                         norm=plt.Normalize(vmin=v_min, vmax=v_max), 
                         origin='lower')
    axes[0].set_title(f"A) Interference Magnitude $|T_{{ref}} - T_{{ \\pi }}|$ (Enhanced)")
    plt.colorbar(im0, ax=axes[0], label="Magnitude (Enhanced)")

    # --- Plot 2: Phase Map (The topological signature check) ---
    # Use a cyclical colormap (e.g., 'twilight_shifted') to show the wrap from -pi to pi
    im1 = axes[1].imshow(Phase_map, extent=extent, cmap='twilight_shifted', 
                         vmin=-np.pi, vmax=np.pi, 
                         origin='lower')
                         
    axes[1].set_title(f"B) Phase $\\Phi = \\arg(T_{{ref}} - T_{{ \\pi }})$")
    cbar1 = plt.colorbar(im1, ax=axes[1], ticks=[-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
    cbar1.set_ticklabels(['$-\\pi$', '$-\\pi/2$', '0', '$\\pi/2$', '$\\pi$'])
    cbar1.set_label("Phase (Radians)", rotation=270, labelpad=15)

    # Add the detected line from the previous step for reference (at 0/180 deg)
    for ax in axes:
        ax.set_xlabel("Galactic Longitude (deg)")
        ax.axvline(180, color='lime', linestyle=':', linewidth=3, alpha=0.7)
        ax.axvline(-180, color='lime', linestyle=':', linewidth=3, alpha=0.7)
        ax.axvline(0, color='lime', linestyle=':', linewidth=3, alpha=0.7, label='Line Meridian')
        ax.legend(loc='lower left', fontsize='small')

    outfile = "cmb_pi_phase_singularity_analysis.png"
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    print(f"[+] Saved Phase Analysis to {outfile}")

    # 5. Extract phase values near the critical meridian (0/180 deg)
    center_row = N_RES // 2
    zero_deg_index = N_RES // 2
    
    # Phase values are mapped from -pi to pi. A 2pi jump means a topological defect.
    phase_at_minus_180 = Phase_map[center_row, -1]
    phase_at_plus_180 = Phase_map[center_row, 0]
    phase_at_zero = Phase_map[center_row, zero_deg_index]
    
    # Check phase winding by comparing points immediately left and right of the critical meridian
    # We average the phase difference across the boundary (column N_RES-1 vs column 0)
    phase_jump_raw = Phase_map[:, 0] - Phase_map[:, -1]
    
    # Ensure jump is measured cyclically, forcing it into the [-pi, pi] range.
    # This is not strictly necessary for analysis but makes the jump value cleaner.
    phase_jump_cyclic = np.arctan2(np.sin(phase_jump_raw), np.cos(phase_jump_raw))
    
    mean_phase_jump_cyclic = np.mean(phase_jump_cyclic)

    print(f"\n[Phase Check at Central Latitude (b=0)]")
    print(f"    -> Phase at Longitude -180.0°: {phase_at_minus_180:.4f} radians")
    print(f"    -> Phase at Longitude +180.0° (same point): {phase_at_plus_180:.4f} radians")
    print(f"    -> Phase at Longitude 0.0° (Galactic Center): {phase_at_zero:.4f} radians")
    print(f"    -> Mean Cyclic Phase Jump across -180/+180 meridian: {mean_phase_jump_cyclic:.4f} radians")
    
analyze_pi_phase_singularity()