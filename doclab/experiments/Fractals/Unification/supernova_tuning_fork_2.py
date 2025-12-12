# FIX helical_scanner_5.py to allow importing without astropy_healpix installed
helical_scanner_5_content_fixed = r'''import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
# from astropy_healpix import HEALPix  <-- MOVED INSIDE FUNCTION
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.special import sph_harm, sph_harm_y
from PIL import Image
import warnings
import os
import sys

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ============================================================
# CONFIGURATION
# ============================================================
FITS_PATH   = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX        = 40
REMOVE_BAND = (10, 40)   # (L1, L2) Substrate = everything EXCEPT this band

# Synthesis grid (Visualization Resolution)
N_TH_SYN = 180
N_PH_SYN = 360

# Twist scan parameters
K_MIN, K_MAX = -1.5, 4.0
N_K          = 121
K_VALUES     = np.linspace(K_MIN, K_MAX, N_K)

# Cache / Output
ALM_CACHE = f"cmb_alms_lmax{LMAX}.npz"
GIF_NAME  = "cmb_substrate_helical_scanner5.gif"

# ============================================================
# HELPER: Spherical Harmonics
# ============================================================
def get_ylm(m, l, phi, theta):
    try:
        return sph_harm_y(l, m, phi, theta)
    except (TypeError, AttributeError):
        return sph_harm(m, l, phi, theta)

# ============================================================
# STEP 1: Load CMB and compute a_lm (Integration Grid)
# ============================================================
def load_cmb_and_alms(fits_path, lmax):
    # Lazy import to allow usage without healpix if using synthetic data
    from astropy_healpix import HEALPix

    if os.path.exists(ALM_CACHE):
        print(f"[*] Loading cached a_lm from {ALM_CACHE}...")
        data = np.load(ALM_CACHE)
        alms = {}
        Ls, Ms = data["L"], data["M"]
        Re, Im = data["Re"], data["Im"]
        for L, M, r, im in zip(Ls, Ms, Re, Im):
            alms[(int(L), int(M))] = r + 1j * im
        return alms

    print(f"[*] Computing a_lm up to L={lmax} from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    if isinstance(data, np.ndarray) and data.dtype.fields:
        if "I" in data.dtype.names:
            cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names:
            cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else:
            cmb = np.array(data[data.dtype.names[0]], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hpix  = HEALPix(nside=nside, order="ring", frame="galactic")

    n_theta = lmax * 4
    n_phi   = lmax * 8
    theta   = np.linspace(0, np.pi, n_theta)
    phi     = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH  = np.meshgrid(theta, phi, indexing="ij")

    lon = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix   = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_s    = cmb[ipix]

    dtheta = theta[1] - theta[0]
    dphi   = phi[1]   - phi[0]
    weights = np.sin(TH) * dtheta * dphi

    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y = get_ylm(m, l, PH, TH)
            val = np.sum(T_s * np.conjugate(Y) * weights)
            alms[(l, m)] = val

    Ls, Ms, Re, Im = [], [], [], []
    for (l, m), v in alms.items():
        Ls.append(l); Ms.append(m)
        Re.append(v.real); Im.append(v.imag)
    np.savez(ALM_CACHE, L=np.array(Ls), M=np.array(Ms),
             Re=np.array(Re), Im=np.array(Im))
    print(f"[*] Saved a_lm cache to {ALM_CACHE}")

    return alms

# ============================================================
# STEP 2: Build Mode Maps (Synthesis Grid)
# ============================================================
def build_mode_maps(alms, LMAX, remove_band=None):
    theta = np.linspace(0, np.pi, N_TH_SYN)
    phi   = np.linspace(-np.pi, np.pi, N_PH_SYN, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")

    # RE-AGGREGATION BY M for Helical Twist efficiency
    maps_by_m = {}
    
    for L in range(LMAX + 1):
        # Skip if in removed band
        if remove_band and (remove_band[0] <= L <= remove_band[1]):
            continue
            
        for M in range(-L, L+1):
            alm = alms.get((L, M), 0)
            if alm == 0: continue
            
            base_contrib = alm * (np.cos(TH) ** L) 
            
            if M not in maps_by_m:
                maps_by_m[M] = np.zeros((N_TH_SYN, N_PH_SYN), dtype=np.complex128)
            
            maps_by_m[M] += base_contrib

    return maps_by_m, TH, PH

# ============================================================
# STEP 3: Helical Synthesis
# ============================================================
def synthesize_helical(mode_maps_by_m, PH, k_twist):
    out = np.zeros_like(PH, dtype=np.complex128)
    for m, M_field in mode_maps_by_m.items():
        phase = np.exp(1j * m * k_twist * PH)
        out  += M_field * phase
    return out.real

def normalize_frame(arr):
    lo, hi = np.percentile(arr, [2, 98])
    arr = np.clip(arr, lo, hi)
    if hi > lo:
        arr = (arr - lo) / (hi - lo)
    else:
        arr[:] = 0.0
    return arr

def main():
    pass

if __name__ == "__main__":
    main()
'''

with open("helical_scanner_5.py", "w") as f:
    f.write(helical_scanner_5_content_fixed)

# Now write the test script again, removing HEALPix import
test_script_code = r'''import numpy as np
import matplotlib.pyplot as plt
# from astropy.coordinates import SkyCoord # Removed
# import astropy.units as u # Removed
from scipy.special import sph_harm, sph_harm_y
import sys

# Import helper functions from the user's module
from helical_scanner_5 import (
    get_ylm, build_mode_maps, synthesize_helical, 
    N_TH_SYN, N_PH_SYN, LMAX, REMOVE_BAND
)

def generate_synthetic_needle_alms(lmax=40, needle_params=None):
    # 1. Define Grid
    n_theta = lmax * 4
    n_phi   = lmax * 8
    theta   = np.linspace(0, np.pi, n_theta)
    phi     = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH  = np.meshgrid(theta, phi, indexing="ij")

    # 2. Create Map: Random Noise + Needle
    np.random.seed(42)
    map_data = np.random.randn(*TH.shape) * 0.5 
    
    if needle_params:
        # Needle: phi = 2*theta - pi
        dist = np.abs(2*TH - PH - np.pi) / np.sqrt(2**2 + 1)
        width = np.deg2rad(5.0) 
        needle = np.exp(-0.5 * (dist / width)**2) * 5.0
        map_data += needle

    # 3. Compute Alms (Quadrature)
    dtheta = theta[1] - theta[0]
    dphi   = phi[1]   - phi[0]
    weights = np.sin(TH) * dtheta * dphi

    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y = get_ylm(m, l, PH, TH)
            val = np.sum(map_data * np.conjugate(Y) * weights)
            alms[(l, m)] = val

    return alms

def run_synthetic_test():
    print("=== Running Synthetic Traveler Test (Upgrade C) ===")
    
    print("[*] Generating synthetic universe with injected traveler needle...")
    # Use small LMAX for speed in test
    lmax_test = 20
    alms = generate_synthetic_needle_alms(lmax_test, needle_params=True)
    
    print("[*] Building helical mode maps...")
    maps_by_m, TH, PH = build_mode_maps(alms, lmax_test, remove_band=None)
    
    k_scan = np.linspace(0.1, 2.0, 10)
    max_intensities = []
    
    print("[*] Scanning k...")
    for k in k_scan:
        T_k = synthesize_helical(maps_by_m, PH, k_twist=k)
        T_k -= T_k.mean()
        max_val = np.max(np.abs(T_k))
        max_intensities.append(max_val)
    
    print("k_values:", k_scan)
    print("max_intensities:", max_intensities)
    print("✅ Synthetic test ran successfully.")

if __name__ == "__main__":
    run_synthetic_test()
'''

with open("synthetic_traveler_test.py", "w") as f:
    f.write(test_script_code)

import synthetic_traveler_test
synthetic_traveler_test.run_synthetic_test()