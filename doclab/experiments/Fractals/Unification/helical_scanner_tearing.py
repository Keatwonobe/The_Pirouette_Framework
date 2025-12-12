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
TARGET_MODES = [10, 20, 30, 40]  # The "Chords" to test
K_SCAN = np.linspace(0.5, 3.5, 50) # Coarse scan for speed
N_RES = 150 # Resolution for metric calc

# ======================
# CORE FUNCTIONS
# ======================
def get_ylm(m, l, phi, theta):
    """Handles SciPy version differences for Spherical Harmonics"""
    try:
        return sph_harm_y(l, m, phi, theta)
    except AttributeError:
        return sph_harm(m, l, phi, theta)

def calculate_verticality_score(image):
    """Metric: Ratio of Horizontal vs Vertical Gradients"""
    grad_y, grad_x = np.gradient(image)
    E_x = np.sum(np.abs(grad_x))
    E_y = np.sum(np.abs(grad_y))
    if E_y == 0: return 0.0
    return E_x / E_y

def extract_alms(fits_path, lmax):
    """Loads CMB and extracts all alms up to lmax"""
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)
        
    # Handle data structure
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    
    # Infill
    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    
    # Healpix Setup
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Integration Grid
    n_theta = lmax * 3
    n_phi = lmax * 4
    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    
    # Sampling
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]
    weights = np.sin(TH) * dtheta * dphi
    
    alms = {}
    print(f"[*] Extracting alms (LMAX={lmax})...")
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = get_ylm(m, l, PH, TH)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    return alms

def synthesize_band(alms, target_l, n_res, k=1.0):
    """Synthesize ONLY a specific L-mode with twist k"""
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    
    map_out = np.zeros_like(TH, dtype=np.complex128)
    
    # Only loop over the specific Target L
    l = target_l
    for m in range(-l, l + 1):
        if (l, m) not in alms: continue
        
        Y_lm = get_ylm(m, l, PH, TH)
        twist_phase = np.exp(1j * m * (k - 1.0) * PH)
        map_out += alms[(l, m)] * Y_lm * twist_phase
            
    return map_out.real

# ======================
# MAIN
# ======================
def main():
    max_l_needed = max(TARGET_MODES)
    alms = extract_alms(FITS_PATH, max_l_needed)
    
    results = {}
    
    print(f"[*] Scanning Modes: {TARGET_MODES}")
    
    plt.figure(figsize=(12, 7))
    
    for l_mode in TARGET_MODES:
        print(f"    Processing L={l_mode}...")
        scores = []
        
        # Get Reference (k=1) for this mode
        ref_map = synthesize_band(alms, l_mode, N_RES, k=1.0)
        
        for k in K_SCAN:
            # Twist this specific mode
            twist_map = synthesize_band(alms, l_mode, N_RES, k=k)
            
            # Interference
            diff_map = np.abs(ref_map - twist_map)
            
            # Score
            s = calculate_verticality_score(diff_map)
            scores.append(s)
            
        # Normalize score to start at 0 for easier comparison
        # (We want to see the rate of divergence)
        scores = np.array(scores)
        # scores = scores - scores[np.argmin(np.abs(K_SCAN - 1.0))] 
        
        plt.plot(K_SCAN, scores, label=f"Mode L={l_mode}", linewidth=2)
        
    plt.axvline(1.0, color='black', alpha=0.3)
    plt.axvline(np.pi, color='green', linestyle=':', label="Pi")
    plt.title("Harmonic Structural Integrity: Which Scale Resists the Twist?")
    plt.xlabel("Twist Factor k")
    plt.ylabel("Verticality (Anisotropy) Score")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    outfile = "cmb_harmonic_mode_scan.png"
    plt.savefig(outfile)
    print(f"✅ Results saved to {outfile}")

if __name__ == "__main__":
    main()