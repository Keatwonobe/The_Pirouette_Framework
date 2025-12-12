import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm, sph_harm_y
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 40                 # The "Chords" we are testing
N_FAKES = 50              # How many universes to simulate (Stress Test depth)
N_RES = 150               # Grid resolution
K_TARGET = 0.9            # The specific "Traveler" twist we want to test significance for
APPLY_MASK = True        # Set True to Lobotomize the Galaxy (Test #2)
MASK_LAT = 20             # Degrees +/- to cut from equator

# ======================
# UTILITIES
# ======================
def get_ylm(m, l, phi, theta):
    try:
        return sph_harm_y(l, m, phi, theta)
    except AttributeError:
        return sph_harm(m, l, phi, theta)

def calculate_verticality_score(image, mask=None):
    """
    Calculates anisotropy. If mask is provided, ignores masked pixels.
    """
    grad_y, grad_x = np.gradient(image)
    
    abs_gx = np.abs(grad_x)
    abs_gy = np.abs(grad_y)
    
    if mask is not None:
        abs_gx = abs_gx[~mask]
        abs_gy = abs_gy[~mask]
        
    E_x = np.sum(abs_gx)
    E_y = np.sum(abs_gy)
    
    if E_y == 0: return 0.0
    return E_x / E_y

def get_base_data(fits_path, lmax):
    print(f"[*] Loading Real CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    # Handle FITS structure
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    
    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    
    # Grid Setup
    n_theta = lmax * 3
    n_phi = lmax * 4
    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    
    # Galactic Mask Creation (Geometry based)
    mask = None
    if APPLY_MASK:
        print(f"[*] APPYLING GALACTIC CUT: +/- {MASK_LAT} degrees")
        # TH is 0 at North Pole, pi at South Pole. Equator is pi/2.
        # Convert lat limit to radians
        rad_lim = np.deg2rad(MASK_LAT)
        # Mask region where theta is close to pi/2
        mask = (TH > (np.pi/2 - rad_lim)) & (TH < (np.pi/2 + rad_lim))

    # Sampling for Real Alms
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]
    weights = np.sin(TH) * dtheta * dphi

    # Extract Alms & Power Spectrum
    alms = {}
    cl = np.zeros(lmax + 1)
    for l in range(lmax + 1):
        sum_alm_sq = 0
        for m in range(-l, l + 1):
            Y_lm = get_ylm(m, l, PH, TH)
            val = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            alms[(l, m)] = val
            sum_alm_sq += np.abs(val)**2
        cl[l] = sum_alm_sq / (2 * l + 1)
        
    return alms, cl, mask, PH, TH

def generate_fake_alms(cl, lmax):
    fake_alms = {}
    for l in range(lmax + 1):
        if cl[l] <= 0:
            for m in range(-l, l + 1): fake_alms[(l,m)] = 0j
            continue
        
        sigma = np.sqrt(cl[l] / 2.0)
        fake_alms[(l, 0)] = np.random.normal(0, np.sqrt(cl[l])) + 0j
        
        for m in range(1, l + 1):
            re = np.random.normal(0, sigma)
            im = np.random.normal(0, sigma)
            val = re + 1j * im
            fake_alms[(l, m)] = val
            fake_alms[(l, -m)] = (-1)**m * np.conjugate(val)
    return fake_alms

def synthesize_and_score(alms, lmax, k, PH, TH, mask):
    map_out = np.zeros_like(TH, dtype=np.complex128)
    
    # Synthesize Loop
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            Y_lm = get_ylm(m, l, PH, TH)
            twist_phase = np.exp(1j * m * (k - 1.0) * PH)
            map_out += alms[(l, m)] * Y_lm * twist_phase
            
    real_map = map_out.real
    
    # Calculate Score
    return calculate_verticality_score(real_map, mask)

# ======================
# MAIN
# ======================
def main():
    print("========================================")
    print("   CMB STRESS TEST: MONTE CARLO SIGMA   ")
    print("========================================")
    
    # 1. Get Real Data
    real_alms, cl, mask, PH, TH = get_base_data(FITS_PATH, LMAX)
    
    # 2. Score Real Universe
    print(f"[*] Scoring Real Universe at Twist k={K_TARGET}...")
    real_score = synthesize_and_score(real_alms, LMAX, K_TARGET, PH, TH, mask)
    print(f"    -> Real Score: {real_score:.5f}")
    
    # 3. Run Monte Carlo
    print(f"[*] Generating {N_FAKES} Fake Universes...")
    fake_scores = []
    
    for i in range(N_FAKES):
        if i % 5 == 0: sys.stdout.write(f"\r    Processing Fake {i+1}/{N_FAKES}")
        sys.stdout.flush()
        
        f_alms = generate_fake_alms(cl, LMAX)
        s = synthesize_and_score(f_alms, LMAX, K_TARGET, PH, TH, mask)
        fake_scores.append(s)
        
    print("\n[*] Processing Statistics...")
    fake_scores = np.array(fake_scores)
    mean_score = np.mean(fake_scores)
    std_score = np.std(fake_scores)
    
    z_score = (real_score - mean_score) / std_score
    
    print("-" * 30)
    print(f"Real Score: {real_score:.5f}")
    print(f"Fake Mean:  {mean_score:.5f}")
    print(f"Fake Std:   {std_score:.5f}")
    print(f"Z-SCORE:    {z_score:.2f} SIGMA")
    print("-" * 30)
    
    # 4. Plot
    plt.figure(figsize=(10, 6))
    plt.hist(fake_scores, bins=15, color='gray', alpha=0.7, label='Random Universes')
    plt.axvline(real_score, color='red', linewidth=3, linestyle='--', label=f'Real Universe ({z_score:.2f}σ)')
    plt.axvline(mean_score, color='black', linestyle=':', label='Mean')
    
    title_str = f"Significance Test | Twist k={K_TARGET} | LMAX={LMAX}"
    if APPLY_MASK: title_str += " | MASKED"
    
    plt.title(title_str)
    plt.xlabel("Verticality Score")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    fname = "cmb_monte_carlo_test_lobotomy.png"
    plt.savefig(fname)
    print(f"✅ Results saved to {fname}")

if __name__ == "__main__":
    main()