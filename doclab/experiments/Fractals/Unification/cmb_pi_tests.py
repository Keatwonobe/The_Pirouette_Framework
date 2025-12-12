import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord
import math
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 40          # Maximum multipole moment to synthesize
N_RES = 300        # Grid resolution for analysis (must match earlier runs)
N_PI_TESTS = 5     # Test n = 1, 2, 3, 4, 5

# ======================
# GLOBAL CACHE
# ======================
YLM_CACHE = None
ALMS_CACHE = None
TH_GRID = None
PH_GRID = None

# ===============================================
# 1. CORE FUNCTIONS (Initialization and Synthesis)
# ===============================================

def get_alm_and_grid(fits_path, lmax, n_res):
    """Loads CMB data and computes/caches a_lm and Y_lm coefficients."""
    global YLM_CACHE, ALMS_CACHE, TH_GRID, PH_GRID
    
    print(f"[*] Loading CMB from {fits_path} and computing a_lm (LMAX={lmax})...")
    
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: FITS file not found: {fits_path}")
        sys.exit(1)

    # ... [FITS loading and sampling logic identical to previous runs] ...
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
    
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM) 
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    
    ALMS_CACHE = alms
    
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')

    YLM_CACHE = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            YLM_CACHE[(l, m)] = sph_harm(m, l, PH_GRID, TH_GRID)
    
    print("[+] Initialization complete. Caches ready.")

def synthesize_complex_map(k, target_l=None, lmax=LMAX):
    """
    Synthesizes the complex twisted map. 
    If target_l is specified, synthesizes ONLY that single multipole mode.
    """
    if TH_GRID is None:
        raise RuntimeError("Caches not initialized.")

    map_out = np.zeros_like(TH_GRID, dtype=np.complex128)
    delta_phi_multiplier = (k - 1) * PH_GRID
    
    l_start = target_l if target_l is not None else 0
    l_end   = target_l + 1 if target_l is not None else lmax + 1
    
    for l in range(l_start, l_end):
        for m in range(-l, l + 1):
            alm = ALMS_CACHE.get((l, m), 0)
            Y_lm_untwisted = YLM_CACHE.get((l, m))
            
            if Y_lm_untwisted is not None:
                phase_corr = np.exp(1j * m * delta_phi_multiplier)
                map_out += alm * Y_lm_untwisted * phase_corr
            
    return map_out


# ===============================================
# 2. ANALYSIS FUNCTIONS
# ===============================================

def detect_singularity_longitude(I_map):
    """Detects the longitude of the sharpest line in the interference map 
       by finding the maximum gradient."""
    
    # Ignore noisy poles (top/bottom 5% of N_RES rows)
    n_res_rows = I_map.shape[0]
    ignore_rows = n_res_rows // 20
    lon_profile = np.mean(I_map[ignore_rows:-ignore_rows, :], axis=0) 
    
    gradient = np.abs(np.gradient(lon_profile))
    max_grad_index = np.argmax(gradient)
    
    # PH_GRID is guaranteed to exist
    longitude_rad = PH_GRID[n_res_rows // 2, max_grad_index]
    longitude_deg = np.rad2deg(longitude_rad)
    return longitude_deg

def check_l_n_coupling(n, k_n, l_sing_full):
    """
    Tests the hypothesis: Is the singularity line at l_sing_full
    caused predominantly by the single l=n mode?
    """
    # 1. Synthesize reference and twisted maps using ONLY l=n
    T_n_ref_c = synthesize_complex_map(1.0, target_l=n, lmax=LMAX)
    T_n_twist_c = synthesize_complex_map(k_n, target_l=n, lmax=LMAX)

    # 2. Calculate the interference magnitude for ONLY l=n
    I_n_map = np.abs(T_n_ref_c - T_n_twist_c)

    # 3. Find the longitude of the singularity in this restricted map
    l_sing_restricted = detect_singularity_longitude(I_n_map)
    
    # 4. Check alignment (The crucial test)
    # The measured line (l_sing_full) must match the restricted line (l_sing_restricted)
    # We use cyclical distance to account for -180/180 wrap-around
    l_diff = np.abs(l_sing_full - l_sing_restricted)
    l_diff_cyclic = min(l_diff, 360 - l_diff)
    
    # Define a stringent match threshold (1 degree)
    is_coupled = l_diff_cyclic < 1.0 
    
    return is_coupled, l_sing_restricted


# ===============================================
# 3. MAIN REPRODUCIBLE ANALYSIS
# ===============================================

def run_reproducible_analysis():
    
    # 1. Initialization
    get_alm_and_grid(FITS_PATH, LMAX, N_RES)
    
    # 2. Reference Map (k=1)
    T_ref_c = synthesize_complex_map(1.0, target_l=None, lmax=LMAX)

    results = []
    
    print("\n=======================================================")
    print(f"[*] Running N*PI Reproducible Analysis (n=1 to {N_PI_TESTS})")
    print("=======================================================")

    # 3. Loop through n=1 to N_PI_TESTS
    for n in range(1, N_PI_TESTS + 1):
        k_n_theory = n * np.pi
        
        # A. Find the k value closest to n*pi in the dataset (or just use n*pi)
        # For precision, we use n*pi directly, trusting its exact theoretical value.
        
        # B. Synthesize the twisted map T_n*pi
        T_n_twist_c = synthesize_complex_map(k_n_theory, target_l=None, lmax=LMAX)
        
        # C. Calculate Interference and find the singularity longitude (l_sing_full)
        I_map = np.abs(T_ref_c - T_n_twist_c)
        l_sing_full = detect_singularity_longitude(I_map)
        
        # D. Test the L=n Coupling Hypothesis
        is_coupled, l_sing_restricted = check_l_n_coupling(n, k_n_theory, l_sing_full)
        
        results.append({
            'n': n,
            'k_theory': k_n_theory,
            'l_sing_full': l_sing_full,
            'l_sing_restricted': l_sing_restricted,
            'is_coupled': is_coupled
        })
        
        coupling_status = "✅ Confirmed" if is_coupled else "❌ Rejected"
        print(f"  -> n={n}: L-Coupling {coupling_status} (Full={l_sing_full:.2f}° | L=n Only={l_sing_restricted:.2f}°)")
        
    # 4. Print Final Results Table
    print("\n=========================================================================================")
    print("✨ FINAL REPRODUCIBLE N*PI SINGULARITY ANALYSIS RESULTS ✨")
    print("=========================================================================================")
    print(f"{'n':<3} | {'k_theory':<15} | {'L_sing_FULL':<13} | {'L_sing_L=n_ONLY':<18} | {'L=n Coupling?':<15}")
    print("-----------------------------------------------------------------------------------------")
    for res in results:
        coupling_status = "YES" if res['is_coupled'] else "NO"
        print(f"{res['n']:<3} | {res['k_theory']:<15.8f} | {res['l_sing_full']:<13.4f}° | {res['l_sing_restricted']:<18.4f}° | {coupling_status:<15}")

    print("=========================================================================================")
    print("NOTE: The L=n Coupling Test determines if the n*pi singularity is caused exclusively")
    print("      by the corresponding l=n multipole moment (e.g., k=2pi is caused by l=2 only).")

if __name__ == "__main__":
    run_reproducible_analysis()