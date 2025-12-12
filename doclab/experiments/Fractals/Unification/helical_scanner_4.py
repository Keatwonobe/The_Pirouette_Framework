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
LMAX = 40
N_POINTS = 50000
W_STAR = 1.0047468850
# WIDER SCAN to catch the Pi resonance and the 0.9 Traveler
K_SCAN = np.linspace(0.5, 3.5, 100) 

# -----------------------
# SciPy spherical harmonics wrapper
# -----------------------
try:
    from scipy.special import sph_harm_y

    def my_sph_harm(m, l, phi_az, theta_pol):
        """
        Wrapper around sph_harm_y with the same calling convention
        you used before: my_sph_harm(m, l, phi, theta).

        SciPy >=1.15: sph_harm_y(l, m, theta_pol, phi_az)
        """
        return sph_harm_y(l, m, theta_pol, phi_az)

except ImportError:
    # Fallback for older SciPy; this may be deprecated but keeps compatibility.
    from scipy.special import sph_harm as _sph_harm

    def my_sph_harm(m, l, phi_az, theta_pol):
        # Original SciPy sph_harm signature: sph_harm(m, l, theta_az, phi_pol)
        # Your previous calls used (phi_az, theta_pol) in that order.
        return _sph_harm(m, l, phi_az, theta_pol)

# ======================
# 1. HELIX GEOMETRY
# ======================
def get_helical_path(w, n_points):
    """
    Generates (theta, phi) along the resonant helix on S^2.

    t in (0,1) -> z = 2t - 1 (north to south), phi = 2π w t.
    """
    k_indices = np.arange(n_points) + 0.5
    t = k_indices / n_points

    z = 2.0 * t - 1.0
    z = np.clip(z, -1.0, 1.0)
    theta = np.arccos(z)

    phi = 2.0 * np.pi * w * t
    phi = (phi + np.pi) % (2.0 * np.pi) - np.pi

    return theta, phi


# ======================
# 2. MANUAL a_lm EXTRACTION (same as scanner 2)
# ======================
def extract_dna_from_fits(fits_path, lmax):
    """
    Integrate the HEALPix CMB map onto a (theta,phi) grid and extract a_lm, C_l.

    This runs once per script, so we leave it mostly as-is.
    """
    print(f"[*] Loading CMB from {fits_path}...")
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

    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    n_theta = lmax * 4
    n_phi = lmax * 8
    theta_grid = np.linspace(0.0, np.pi, n_theta)
    phi_grid = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta_grid, phi_grid, indexing="ij")

    print("[*] Sampling map onto integration grid...")
    lon_deg = np.rad2deg((PH + 2.0 * np.pi) % (2.0 * np.pi))
    lat_deg = np.rad2deg(0.5 * np.pi - TH)
    coords = SkyCoord(l=lon_deg * u.deg, b=lat_deg * u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sampled = cmb[ipix]

    dtheta = theta_grid[1] - theta_grid[0]
    dphi = phi_grid[1] - phi_grid[0]
    weights = np.sin(TH) * dtheta * dphi

    print(f"[*] Extracting a_lm (LMAX={lmax})...")
    alms = {}
    cl = np.zeros(lmax + 1)

    for l in range(lmax + 1):
        sum_alm_sq = 0.0
        for m in range(-l, l + 1):
            Y_lm = my_sph_harm(m, l, PH, TH)
            val = np.sum(T_sampled * np.conjugate(Y_lm) * weights)
            alms[(l, m)] = val
            sum_alm_sq += np.abs(val) ** 2
        cl[l] = sum_alm_sq / (2 * l + 1)

    return alms, cl


def generate_fake_universe(cl, lmax, seed=42):
    """
    Create a fake universe with the SAME C_l but random phases (Gaussian alms).
    """
    print("[*] Generating Fake Universe (Random Phases)...")
    fake_alms = {}
    rng = np.random.default_rng(seed)

    for l in range(lmax + 1):
        if cl[l] <= 0.0:
            for m in range(-l, l + 1):
                fake_alms[(l, m)] = 0j
            continue

        sigma = np.sqrt(cl[l] / 2.0)

        # m=0 real
        fake_alms[(l, 0)] = rng.normal(0.0, np.sqrt(cl[l])) + 0j

        for m in range(1, l + 1):
            re = rng.normal(0.0, sigma)
            im = rng.normal(0.0, sigma)
            val = re + 1j * im
            fake_alms[(l, m)] = val
            fake_alms[(l, -m)] = (-1) ** m * np.conjugate(val)

    return fake_alms


# ======================
# 3. NEW: per-m mode-line compression on the helix
# ======================
def build_mode_lines(alms, lmax, theta_path, phi_path):
    """
    Compress all (l,m) contributions along the helix into per-m mode lines:

        S_m(t) = sum_{l >= |m|} a_{l m} * Y_{l m}(theta(t), phi(t))

    Returns:
        mode_lines: dict[m] -> complex array of shape (N_POINTS,)
    """
    print("[*] Building mode lines along helix...")
    n_points = theta_path.size
    mode_lines = {m: np.zeros(n_points, dtype=np.complex128)
                  for m in range(-lmax, lmax + 1)}

    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            alm = alms.get((l, m), 0j)
            if alm == 0j:
                continue
            Y_lm = my_sph_harm(m, l, phi_path, theta_path)
            mode_lines[m] += alm * Y_lm

    return mode_lines


def synthesize_along_helix_fast(mode_lines, phi_path, k_twist=1.0):
    """
    Fast synthesis along helix using compressed mode lines.

    signal(t; k) = sum_m S_m(t) * exp(i m (k-1) phi(t))

    Special case k=1: twist factor 0 -> just sum mode_lines[m].
    """
    signal = np.zeros_like(phi_path, dtype=np.complex128)
    twist_factor = k_twist - 1.0

    if abs(twist_factor) < 1e-15:
        # No twist: direct sum over m
        for m, line in mode_lines.items():
            if np.any(line):
                signal += line
        return signal.real

    phi = phi_path
    for m, line in mode_lines.items():
        if not np.any(line):
            continue
        twist_phase = np.exp(1j * m * twist_factor * phi)
        signal += line * twist_phase

    return signal.real

def get_helical_path(w, n_points):
    k_indices = np.arange(n_points) + 0.5
    t = k_indices / n_points
    z = 2 * t - 1
    phi = 2 * np.pi * w * t
    z = np.clip(z, -1.0, 1.0)
    theta = np.arccos(z)
    phi = (phi + np.pi) % (2 * np.pi) - np.pi
    return theta, phi

def synthesize_along_helix(alms, lmax, theta_path, phi_path, k_twist=1.0):
    signal = np.zeros_like(theta_path, dtype=np.complex128)
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            Y_lm = sph_harm(m, l, phi_path, theta_path)
            twist_phase = np.exp(1j * m * (k_twist - 1.0) * phi_path)
            signal += alms[(l, m)] * Y_lm * twist_phase
    return signal.real

def extract_dna_from_fits(fits_path, lmax):
    # ... (Same as before) ...
    # [Brief re-implementation for completeness if running standalone]
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
    n_theta = lmax * 4; n_phi = lmax * 8
    theta_grid = np.linspace(0, np.pi, n_theta)
    phi_grid = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta_grid, phi_grid, indexing='ij')
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sampled = cmb[ipix]
    dtheta = theta_grid[1] - theta_grid[0]
    dphi = phi_grid[1] - phi_grid[0]
    weights = np.sin(TH) * dtheta * dphi
    alms = {}; cl = np.zeros(lmax + 1)
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
    fake_alms = {}; np.random.seed(42)
    for l in range(lmax + 1):
        if cl[l] <= 0:
            for m in range(-l, l + 1): fake_alms[(l, m)] = 0j
            continue
        sigma = np.sqrt(cl[l] / 2.0)
        fake_alms[(l, 0)] = np.random.normal(0, np.sqrt(cl[l])) + 0j
        for m in range(1, l + 1):
            re = np.random.normal(0, sigma); im = np.random.normal(0, sigma)
            val = re + 1j * im
            fake_alms[(l, m)] = val; fake_alms[(l, -m)] = (-1)**m * np.conjugate(val)
    return fake_alms

def main():
    real_alms, cl = extract_dna_from_fits(FITS_PATH, LMAX)
    fake_alms = generate_fake_universe(cl, LMAX)
    theta_path, phi_path = get_helical_path(W_STAR, N_POINTS)
    
    # Reference (k=1)
    ref_real = synthesize_along_helix(real_alms, LMAX, theta_path, phi_path, k_twist=1.0)
    ref_fake = synthesize_along_helix(fake_alms, LMAX, theta_path, phi_path, k_twist=1.0)
    
    scores_real = []
    scores_fake = []
    
    print(f"[*] Differential Scan (0.5 to 3.5)...")
    
    for k in K_SCAN:
        twist_real = synthesize_along_helix(real_alms, LMAX, theta_path, phi_path, k_twist=k)
        twist_fake = synthesize_along_helix(fake_alms, LMAX, theta_path, phi_path, k_twist=k)
        
        diff_real = np.abs(ref_real - twist_real)
        diff_fake = np.abs(ref_fake - twist_fake)
        
        scores_real.append(np.mean(diff_real))
        scores_fake.append(np.mean(diff_fake))

    # Calculate Differential
    differential = np.array(scores_real) - np.array(scores_fake)

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    
    # Raw Scores
    ax1.plot(K_SCAN, scores_real, label="Real Universe", color='blue')
    ax1.plot(K_SCAN, scores_fake, label="Fake Universe (Baseline)", color='gray', linestyle='--')
    ax1.set_ylabel("Interference Amplitude")
    ax1.set_title("Raw Helical Scan")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Differential
    ax2.plot(K_SCAN, differential, label="Difference (Real - Fake)", color='red', linewidth=2)
    ax2.axhline(0, color='black', alpha=0.5)
    
    # Mark Features
    ax2.axvline(0.9, color='orange', linestyle=':', label="Traveler (0.9)")
    ax2.axvline(np.pi, color='green', linestyle=':', label="Pi")
    
    ax2.set_ylabel("Anomalous Signal Magnitude")
    ax2.set_xlabel("Twist Index k")
    ax2.set_title("Differential Signal (The Anomaly)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("helical_differential_scan.png")
    print("✅ Differential Scan Saved.")

if __name__ == "__main__":
    main()