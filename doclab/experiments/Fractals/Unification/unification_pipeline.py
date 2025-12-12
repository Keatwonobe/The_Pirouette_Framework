import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
import sys

# ======================
# GLOBAL CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
UNIFIED_TWIST = 1.0  # The "Moment of Impact"
CMB_RES = 512        # High Res for Macro View
FRACTAL_RES = 400    # Resolution for Fractals

# ======================
# 1. CMB ENGINE (Macro View)
# ======================
def get_cmb_field(fits_path, lmax, n_res, k_twist):
    print(f"[*] [CMB] Synthesizing Impact Geometry at K={k_twist}...")
    try:
        data = fits.getdata(fits_path)
        if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else: cmb = data.astype(np.float64)
        cmb[np.isnan(cmb)] = np.nanmean(cmb)
    except FileNotFoundError:
        print("[!] CMB File not found. Generating Mock Field for testing.")
        # Create a mock "impact" field if file missing (for robust testing)
        theta = np.linspace(0, np.pi, n_res)
        phi = np.linspace(-np.pi, np.pi, n_res)
        M, L = np.meshgrid(theta, phi, indexing='ij')
        return np.sin(5*M)*np.cos(5*L) * np.exp(-((M-np.pi/2)**2 + (L)**2))

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    n_theta = lmax * 3; n_phi = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta)
    p_alm = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')
    
    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi)) * u.deg
    lat = np.rad2deg(0.5*np.pi - TH_ALM) * u.deg
    ipix = hpix.lonlat_to_healpix(lon, lat)
    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    # Synthesis Grid
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    # Synthesize at K
    m_range = np.arange(-lmax, lmax + 1)
    n_theta = len(theta)
    zeros_phi = np.zeros_like(theta)
    
    profiles = np.zeros((len(m_range), n_theta), dtype=np.complex128)
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) not in alms: continue
            profiles[i, :] += alms[(l, m)] * sph_harm(m, l, zeros_phi, theta)
            
    phase_matrix = np.exp(1j * m_range[:, None] * k_twist * phi[None, :])
    field = (profiles.T @ phase_matrix).real
    return field

# ======================
# 2. FRACTAL PHYSICS ENGINE
# ======================
def get_force_unified(m, lam, twist):
    # Unified Field Laws
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = twist * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling = np.sqrt(magnitude)
    
    F_gold_m = sum_m * scaling
    F_gold_lam = sum_lam * scaling
    
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Mixing
    d_g = np.minimum(np.abs(angle - 30), 360-np.abs(angle - 30)); w_g = np.exp(-(d_g/80)**2)
    d_t = np.minimum(np.abs(angle - 150), 360-np.abs(angle - 150)); w_t = np.exp(-(d_t/80)**2)
    d_r = np.minimum(np.abs(angle - 270), 360-np.abs(angle - 270)); w_r = np.exp(-(d_r/80)**2)
    
    tot = w_g + w_t + w_r + 1e-6
    Fm = (w_t*F_teal_m + w_r*F_red_m + w_g*F_gold_m) / tot
    Flam = (w_t*F_teal_lam + w_r*F_red_lam + w_g*F_gold_lam) / tot
    
    return Fm, Flam

def compute_stiffness_map(res, twist, bounds):
    print(f"[*] [Fractal] Mapping Stiffness at Zoom {bounds}x...")
    m = np.linspace(-bounds, bounds, res)
    l = np.linspace(-bounds, bounds, res)
    M, L = np.meshgrid(m, l)
    EPS = 1e-3
    
    Fm, Flam = get_force_unified(M, L, twist)
    Fm_m, Flam_m = get_force_unified(M + EPS, L, twist)
    Fm_l, Flam_l = get_force_unified(M, L + EPS, twist)
    
    dFx_dm = (Fm_m - Fm)/EPS
    dFx_dl = (Fm_l - Fm)/EPS
    dFy_dm = (Flam_m - Flam)/EPS
    dFy_dl = (Flam_l - Flam)/EPS
    
    g11 = dFx_dm**2 + dFy_dm**2
    g12 = dFx_dm*dFx_dl + dFy_dm*dFy_dl
    g22 = dFx_dl**2 + dFy_dl**2
    
    T = g11 + g22
    D = g11*g22 - g12**2
    L1 = T/2 + np.sqrt(np.maximum(T**2/4 - D, 0))
    return np.log1p(np.sqrt(L1))

def compute_basin_map(res, twist, bounds):
    print(f"[*] [Proton] Mapping Basin Stability...")
    m = np.linspace(-bounds, bounds, res)
    l = np.linspace(-bounds, bounds, res)
    M, L = np.meshgrid(m, l)
    
    # Simulating sedimentation/entropy anchor
    vm = np.zeros_like(M)
    vl = np.zeros_like(L)
    active = np.ones_like(M, dtype=bool)
    lifetime = np.zeros_like(M, dtype=float)
    
    dt = 0.05
    gamma = 0.015
    steps = 150 # Short run for "formation" view
    
    for t in range(steps):
        Fm, Flam = get_force_unified(M, L, twist)
        
        vm[active] += (Fm[active] - gamma*vm[active]) * dt
        vl[active] += (Flam[active] - gamma*vl[active]) * dt
        
        M[active] += vm[active] * dt
        L[active] += vl[active] * dt
        
        speed = np.sqrt(vm[active]**2 + vl[active]**2)
        lifetime[active] += speed
        
        active[active] &= (speed > 0.01)
        
    return np.log1p(lifetime)

# ======================
# 3. MAIN DASHBOARD
# ======================
def run_unification_pipeline():
    fig = plt.figure(figsize=(16, 12), facecolor='#050505')
    gs = gridspec.GridSpec(2, 3, height_ratios=[1.5, 1])
    
    # --- PANEL 1: CMB MACRO IMPACT ---
    print("\n--- PHASE 1: MACRO COSMOS ---")
    cmb_map = get_cmb_field(FITS_PATH, 60, CMB_RES, UNIFIED_TWIST)
    ax_cmb = plt.subplot(gs[0, :])
    ax_cmb.imshow(cmb_map, origin='lower', cmap='twilight', extent=[-180, 180, -90, 90])
    ax_cmb.set_title(f"THE MOMENT OF IMPACT | CMB Macro Structure (Twist K={UNIFIED_TWIST})", color='cyan', fontsize=16)
    ax_cmb.axis('off')
    
    # --- PANEL 2: VACUUM STIFFNESS (Zoom 2.5) ---
    print("\n--- PHASE 2: VACUUM MANIFOLD ---")
    stiff_25 = compute_stiffness_map(FRACTAL_RES, UNIFIED_TWIST, 2.5)
    ax_s1 = plt.subplot(gs[1, 0])
    ax_s1.imshow(stiff_25, origin='lower', cmap='magma', extent=[-2.5, 2.5, -2.5, 2.5])
    ax_s1.set_title("VACUUM STIFFNESS | Zoom 2.5x\n(The Buckle)", color='gold', fontsize=12)
    ax_s1.axis('off')
    
    # --- PANEL 3: VACUUM STIFFNESS (Zoom 1.25) ---
    stiff_125 = compute_stiffness_map(FRACTAL_RES, UNIFIED_TWIST, 1.25)
    ax_s2 = plt.subplot(gs[1, 1])
    ax_s2.imshow(stiff_125, origin='lower', cmap='magma', extent=[-1.25, 1.25, -1.25, 1.25])
    ax_s2.set_title("VACUUM STIFFNESS | Zoom 1.25x\n(The Spike)", color='gold', fontsize=12)
    ax_s2.axis('off')
    
    # --- PANEL 4: PROTON BASIN FORMATION ---
    print("\n--- PHASE 3: PROTON GENESIS ---")
    basin = compute_basin_map(FRACTAL_RES, UNIFIED_TWIST, 2.5)
    ax_b = plt.subplot(gs[1, 2])
    # Custom "Bone" colormap for the basin
    ax_b.imshow(basin, origin='lower', cmap='bone', extent=[-2.5, 2.5, -2.5, 2.5])
    ax_b.set_title("PROTON BASIN | Formation\n(The Scar)", color='white', fontsize=12)
    ax_b.axis('off')
    
    plt.tight_layout()
    plt.savefig("unification_dashboard.png", dpi=120, facecolor='#050505')
    print("\n✅ UNIFICATION COMPLETE. Dashboard saved to unification_dashboard.png")

if __name__ == "__main__":
    run_unification_pipeline()