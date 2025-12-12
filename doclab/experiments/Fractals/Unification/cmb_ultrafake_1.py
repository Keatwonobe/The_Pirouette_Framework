import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord
import os
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits" 
LMAX = 40           # Keep this manageable for speed
N_RES = 200         # Resolution for the visualization/metric grid
K_SCAN = np.linspace(0.5, 3.5, 100) # Scan from below Traveler to past Pi

# ======================
# 1. ANALYSIS METRIC: VERTICALITY
# ======================
def calculate_verticality_score(image):
    """
    Quantifies 'how much does this look like vertical lines?'
    Calculates the ratio of horizontal gradients (crossing lines) 
    to vertical gradients (along lines).
    """
    # Gradient returns (gradient_axis_0, gradient_axis_1) -> (y, x)
    grad_y, grad_x = np.gradient(image)
    
    # We want high variation in X (Longitude) and low variation in Y (Latitude)
    # Energy of the gradient
    E_x = np.sum(np.abs(grad_x))
    E_y = np.sum(np.abs(grad_y))
    
    if E_y == 0: return 0.0
    return E_x / E_y

# ======================
# 2. CORE UTILITIES (Adapted from your code)
# ======================
def get_alm_and_cl(fits_path, lmax):
    """
    Loads Real CMB, calculates a_lm, and extracts the Power Spectrum C_l.
    """
    print(f"[*] Loading Real CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    # Simple infill
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # Grid for integration
    n_theta = lmax * 4
    n_phi = lmax * 8
    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')

    # Sample map
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]

    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]
    weights = np.sin(TH) * dtheta * dphi

    print("[*] Extracting Real Power Spectrum (C_l)...")
    alms = {}
    cl = np.zeros(lmax + 1)
    
    for l in range(lmax + 1):
        sum_alm_sq = 0
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH, TH)
            val = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            alms[(l, m)] = val
            sum_alm_sq += np.abs(val)**2
        
        # Calculate C_l for this multipole
        cl[l] = sum_alm_sq / (2 * l + 1)

    return alms, cl

def generate_fake_universe(cl, lmax):
    """
    Generates a 'Perfect Faker' universe using the provided C_l 
    but with random phases.
    """
    print("[*] Generating Synthetic Universe (Synfast equivalent)...")
    fake_alms = {}
    np.random.seed(None) # Random seed

    for l in range(lmax + 1):
        if cl[l] <= 0:
            for m in range(-l, l + 1): fake_alms[(l,m)] = 0j
            continue
            
        # Variance for Re/Im parts is Cl/2
        sigma = np.sqrt(cl[l] / 2.0)
        
        # m=0 must be real
        fake_alms[(l, 0)] = np.random.normal(0, np.sqrt(cl[l])) + 0j
        
        for m in range(1, l + 1):
            re = np.random.normal(0, sigma)
            im = np.random.normal(0, sigma)
            val = re + 1j * im
            fake_alms[(l, m)] = val
            fake_alms[(l, -m)] = (-1)**m * np.conjugate(val)
            
    return fake_alms

def synthesize_map(alms, lmax, n_res, k=1.0):
    """ Synthesize map with Twist k """
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    
    map_out = np.zeros_like(TH, dtype=np.complex128)
    
    # Pre-compute untwisted Ylm is faster, but for k-scan we just loop
    # Twist logic: effective phase shift = exp(i * m * (k-1) * phi)
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            
            # Standard Spherical Harmonic
            Y_lm = sph_harm(m, l, PH, TH)
            
            # The Topological Twist Phase
            twist_phase = np.exp(1j * m * (k - 1.0) * PH)
            
            map_out += alms[(l, m)] * Y_lm * twist_phase
            
    return map_out.real

# ======================
# 3. MAIN EXECUTION
# ======================
def main():
    # 1. Get Real DNA
    real_alms, cl_real = get_alm_and_cl(FITS_PATH, LMAX)
    
    # 2. Create Frankenstein
    fake_alms = generate_fake_universe(cl_real, LMAX)
    
    # 3. Reference Maps (k=1)
    print("[*] Synthesizing Reference Maps (k=1)...")
    ref_real = synthesize_map(real_alms, LMAX, N_RES, k=1.0)
    ref_fake = synthesize_map(fake_alms, LMAX, N_RES, k=1.0)
    
    scores_real = []
    scores_fake = []
    
    print(f"[*] Scanning k from {K_SCAN[0]} to {K_SCAN[-1]}...")
    
    for i, k in enumerate(K_SCAN):
        if i % 10 == 0: print(f"    Scanning k={k:.2f}...")
        
        # Twist
        twist_real = synthesize_map(real_alms, LMAX, N_RES, k=k)
        twist_fake = synthesize_map(fake_alms, LMAX, N_RES, k=k)
        
        # Interfere
        inter_real = np.abs(ref_real - twist_real)
        inter_fake = np.abs(ref_fake - twist_fake)
        
        # Score
        scores_real.append(calculate_verticality_score(inter_real))
        scores_fake.append(calculate_verticality_score(inter_fake))

    # ======================
    # 4. PLOTTING THE PROOF
    # ======================
    print("[*] Plotting Results...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(K_SCAN, scores_real, label="Real Universe", color='blue', linewidth=2)
    ax.plot(K_SCAN, scores_fake, label="Fake Universe (Random Phases)", color='red', linestyle='--', linewidth=2)
    
    # Mark Pi
    ax.axvline(np.pi, color='green', linestyle=':', label="Pi")
    ax.axvline(1.0, color='black', alpha=0.3)
    
    ax.set_title(f"Topological Resonance: Real vs Fake Universe (LMAX={LMAX})")
    ax.set_ylabel("Verticality Score (Anisotropy)")
    ax.set_xlabel("Twist Index k")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.savefig("cmb_significance_test.png")
    print("✅ Evidence saved to 'cmb_significance_test.png'")

if __name__ == "__main__":
    main()