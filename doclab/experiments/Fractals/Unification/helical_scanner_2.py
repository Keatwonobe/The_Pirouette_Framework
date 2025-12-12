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
LMAX = 40               # Keep low for speed, captures large-scale features (The Traveler)
N_POINTS = 50000        # Resolution along the helical path
W_STAR = 1.0047468850   # The Resonance Winding Number (from your calculus)
K_SCAN = np.linspace(0.8, 1.2, 50) # Scan around The Traveler (0.9)

# ======================
# 1. HELIX GEOMETRY (Inlined for Portability)
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
# 2. FAST SYNTHESIS ALONG PATH
# ======================
def synthesize_along_helix(alms, lmax, theta_path, phi_path, k_twist=1.0):
    """
    Synthesizes the signal ONLY at the coordinates of the helix.
    Includes the Topological Twist (phase shift).
    """
    signal = np.zeros_like(theta_path, dtype=np.complex128)
    
    # Pre-calculate untwisted Y_lm for the path
    # We apply the twist as a phase factor: exp(i * m * (k-1) * phi)
    
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
# 3. MANUAL DATA EXTRACTION (No Healpy)
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

    # Handle FITS structure
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    
    # Infill NaNs
    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    
    # Setup Grid for Integration (The "Scanner")
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Use a high-res grid for accurate integration
    n_theta = lmax * 4
    n_phi = lmax * 8
    theta_grid = np.linspace(0, np.pi, n_theta)
    phi_grid = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta_grid, phi_grid, indexing='ij')
    
    # Sample the FITS map onto this grid
    print("[*] Sampling map onto integration grid...")
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sampled = cmb[ipix]
    
    # Integration Weights (Riemann Sum on Sphere)
    dtheta = theta_grid[1] - theta_grid[0]
    dphi = phi_grid[1] - phi_grid[0]
    weights = np.sin(TH) * dtheta * dphi
    
    # Perform Forward Transform (Get a_lm)
    print(f"[*] Extracting a_lm (LMAX={lmax})...")
    alms = {}
    cl = np.zeros(lmax + 1)
    
    for l in range(lmax + 1):
        sum_alm_sq = 0
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH, TH)
            # Integration: Sum( T * Y_lm* * weight )
            val = np.sum(T_sampled * np.conjugate(Y_lm) * weights)
            alms[(l, m)] = val
            sum_alm_sq += np.abs(val)**2
        
        # Power Spectrum
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
        
        # m=0 is real
        fake_alms[(l, 0)] = np.random.normal(0, np.sqrt(cl[l])) + 0j
        
        for m in range(1, l + 1):
            re = np.random.normal(0, sigma)
            im = np.random.normal(0, sigma)
            val = re + 1j * im
            fake_alms[(l, m)] = val
            fake_alms[(l, -m)] = (-1)**m * np.conjugate(val)
            
    return fake_alms

# ======================
# 4. MAIN LOOP
# ======================
def main():
    # 1. Get DNA
    real_alms, cl = extract_dna_from_fits(FITS_PATH, LMAX)
    fake_alms = generate_fake_universe(cl, LMAX)
    
    # 2. Setup Geometry
    print(f"[*] Generating Helical Path (w*={W_STAR:.4f})...")
    theta_path, phi_path = get_helical_path(W_STAR, N_POINTS)
    
    # 3. Pre-calculate Reference (k=1, The Shadow)
    print("[*] Computing Reference Paths (k=1)...")
    ref_real = synthesize_along_helix(real_alms, LMAX, theta_path, phi_path, k_twist=1.0)
    ref_fake = synthesize_along_helix(fake_alms, LMAX, theta_path, phi_path, k_twist=1.0)
    
    # 4. Scan
    scores_real = []
    scores_fake = []
    
    print(f"[*] Scanning {len(K_SCAN)} twist values (Fast Mode)...")
    for k in K_SCAN:
        # Synthesize Twisted Path
        twist_real = synthesize_along_helix(real_alms, LMAX, theta_path, phi_path, k_twist=k)
        twist_fake = synthesize_along_helix(fake_alms, LMAX, theta_path, phi_path, k_twist=k)
        
        # Interfere (Difference from Reference)
        diff_real = np.abs(ref_real - twist_real)
        diff_fake = np.abs(ref_fake - twist_fake)
        
        # Metric: Average Amplitude of Interference along the Helix
        scores_real.append(np.mean(diff_real))
        scores_fake.append(np.mean(diff_fake))

    # 5. Plot
    print("[*] Plotting Results...")
    plt.figure(figsize=(10, 6))
    
    plt.plot(K_SCAN, scores_real, label="Real Universe", color='blue', linewidth=2)
    plt.plot(K_SCAN, scores_fake, label="Fake Universe (Random)", color='red', linestyle='--', alpha=0.7)
    
    # Markers
    plt.axvline(0.9, color='orange', linestyle=':', label="The Traveler (k=0.9)")
    plt.axvline(1.0, color='black', alpha=0.3)
    
    plt.title(f"Helical Null Hypothesis Test (w*={W_STAR:.4f})")
    plt.xlabel("Twist Index k")
    plt.ylabel("Interference Amplitude (Mean along Helix)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    out_file = "helical_scan_fast_astropy.png"
    plt.savefig(out_file)
    print(f"✅ Fast Scan Complete. Results saved to {out_file}")

if __name__ == "__main__":
    main()