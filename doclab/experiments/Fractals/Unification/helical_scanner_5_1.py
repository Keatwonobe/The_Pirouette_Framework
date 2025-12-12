import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.special import sph_harm
import os
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 40                # Low LMAX captures the large-scale topology (Traveler)
N_POINTS = 50000         # Resolution along the helical path
W_STAR = 1.0047468850    # The "Squaring the Circle" Resonance
K_SCAN = np.linspace(0.5, 3.5, 100) # Wide scan to catch Traveler(0.9) and Pi(3.14)

# ======================
# 1. GEOMETRY: THE HELICAL PROBE
# ======================
def get_helical_path(w, n_points):
    """
    Generates the coordinates (theta, phi) for the resonant helix.
    """
    k_indices = np.arange(n_points) + 0.5
    t = k_indices / n_points # t goes 0 -> 1
    
    # Helical Calculus: z = 2t - 1 mapping
    z = 2 * t - 1
    phi = 2 * np.pi * w * t
    
    # Clip z to avoid numerical errors at poles
    z = np.clip(z, -1.0, 1.0)
    theta = np.arccos(z)
    
    # Wrap phi to [-pi, pi] for Spherical Harmonics
    phi = (phi + np.pi) % (2 * np.pi) - np.pi
    
    return theta, phi

# ======================
# 2. PHYSICS: FAST TWIST SYNTHESIS
# ======================
def synthesize_along_helix(alms, lmax, theta_path, phi_path, k_twist=1.0):
    """
    Synthesizes the signal ONLY at the coordinates of the helix.
    Includes the Topological Twist (phase shift).
    """
    signal = np.zeros_like(theta_path, dtype=np.complex128)
    
    # Pre-calculate phase shifts to avoid re-computing Y_lm if possible,
    # but inside the loop is cleaner for the twist logic.
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            
            # 1. Standard Geometric Component (The Shape)
            Y_lm = sph_harm(m, l, phi_path, theta_path)
            
            # 2. Topological Twist (The Phase Shift)
            # Twist: phi -> phi * k
            # Phase Delta: m * (phi_new - phi_old) = m * phi * (k - 1)
            twist_phase = np.exp(1j * m * (k_twist - 1.0) * phi_path)
            
            signal += alms[(l, m)] * Y_lm * twist_phase
            
    return signal.real

# ======================
# 3. DATA: DNA EXTRACTION & FAKE GENERATION
# ======================
def extract_dna_from_fits(fits_path, lmax):
    """
    Manually integrates the FITS map to get a_lm and C_l.
    Uses Astropy to handle the HEALPix grid.
    """
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    
    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Grid for integration
    n_theta = lmax * 4
    n_phi = lmax * 8
    theta_grid = np.linspace(0, np.pi, n_theta)
    phi_grid = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta_grid, phi_grid, indexing='ij')
    
    print("[*] Sampling map onto integration grid...")
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sampled = cmb[ipix]
    
    dtheta = theta_grid[1] - theta_grid[0]
    dphi = phi_grid[1] - phi_grid[0]
    weights = np.sin(TH) * dtheta * dphi
    
    print(f"[*] Extracting a_lm (LMAX={lmax})...")
    alms = {}
    cl = np.zeros(lmax + 1)
    
    for l in range(lmax + 1):
        sum_alm_sq = 0
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH, TH)
            val = np.sum(T_sampled * np.conjugate(Y_lm) * weights)
            alms[(l, m)] = val
            sum_alm_sq += np.abs(val)**2
        
        cl[l] = sum_alm_sq / (2 * l + 1)
        
    return alms, cl

def generate_fake_universe(cl, lmax):
    """
    Creates the 'Perfect Fake': Same Power Spectrum (Energy), Random Phases (Geometry).
    """
    print("[*] Generating Fake Universe (Random Phases)...")
    fake_alms = {}
    np.random.seed(42) 
    
    for l in range(lmax + 1):
        if cl[l] <= 0:
            for m in range(-l, l + 1): fake_alms[(l, m)] = 0j
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

# ======================
# 4. MAIN EXECUTION
# ======================
def main():
    # 1. Load Data
    real_alms, cl = extract_dna_from_fits(FITS_PATH, LMAX)
    fake_alms = generate_fake_universe(cl, LMAX)
    
    # 2. Setup Geometry
    theta_path, phi_path = get_helical_path(W_STAR, N_POINTS)
    
    # 3. Pre-calculate Reference (k=1)
    print("[*] Computing Reference Paths (k=1)...")
    ref_real = synthesize_along_helix(real_alms, LMAX, theta_path, phi_path, k_twist=1.0)
    ref_fake = synthesize_along_helix(fake_alms, LMAX, theta_path, phi_path, k_twist=1.0)
    
    scores_real = []
    scores_fake = []
    
    print(f"[*] Running Differential Scan ({K_SCAN[0]} to {K_SCAN[-1]})...")
    
    for i, k in enumerate(K_SCAN):
        if i % 10 == 0: print(f"    Scanning k={k:.2f}...")
        
        twist_real = synthesize_along_helix(real_alms, LMAX, theta_path, phi_path, k_twist=k)
        twist_fake = synthesize_along_helix(fake_alms, LMAX, theta_path, phi_path, k_twist=k)
        
        # Interference Amplitude
        diff_real = np.abs(ref_real - twist_real)
        diff_fake = np.abs(ref_fake - twist_fake)
        
        scores_real.append(np.mean(diff_real))
        scores_fake.append(np.mean(diff_fake))

    # 4. Compute Differential
    differential = np.array(scores_real) - np.array(scores_fake)

    # 5. Plot
    print("[*] Plotting Results...")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    
    # Panel 1: Raw Scores
    ax1.plot(K_SCAN, scores_real, label="Real Universe", color='blue', linewidth=2)
    ax1.plot(K_SCAN, scores_fake, label="Fake Universe (Geometric Baseline)", color='gray', linestyle='--')
    ax1.axvline(1.0, color='black', alpha=0.3)
    ax1.set_ylabel("Interference Amplitude")
    ax1.set_title("Raw Helical Scan: Real vs Fake")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: The Differential (The Signal)
    ax2.plot(K_SCAN, differential, label="Anomaly (Real - Fake)", color='red', linewidth=2)
    ax2.axhline(0, color='black', alpha=0.5)
    
    # Mark Features
    ax2.axvline(0.9, color='orange', linestyle=':', label="The Traveler (0.9)", linewidth=2)
    ax2.axvline(np.pi, color='green', linestyle=':', label="Pi (3.14)", linewidth=2)
    
    ax2.set_ylabel("Differential Signal Magnitude")
    ax2.set_xlabel("Twist Index k")
    ax2.set_title("The Differential: Isolating the Topological Anomaly")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("helical_differential_scan.png")
    print("\n✅ Scan Complete. Check 'helical_differential_scan.png' for the anomaly.")

if __name__ == "__main__":
    main()