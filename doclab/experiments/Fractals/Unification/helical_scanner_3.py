#!/usr/bin/env python
"""
helical_scanner_3.py

Helical resonance scanner with per-m mode-line compression.

Optimizations vs helical_scanner_2:
- Compute Y_lm along the helix ONCE per (l,m) per a_lm set.
- Compress into "mode lines" S_m(t) = sum_l a_lm * Y_lm(t).
- For each twist k, we only apply phase exp(i m (k-1) phi(t))
  and sum over m, no more spherical harmonic calls inside the k-loop.

Result: massive speedup vs calling sph_harm for every (l,m,k).
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
import os
import sys

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
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 40               # Large-scale structure only
N_POINTS = 50000        # Helix resolution
W_STAR = 1.0047468850   # Resonant winding number from helical calculus
K_SCAN = np.linspace(0.8, 1.2, 50)   # Twist scan around Traveler region


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


# ======================
# 4. MAIN LOOP (Scanner 3)
# ======================
def main():
    # 1. Extract a_lm from the real map
    real_alms, cl = extract_dna_from_fits(FITS_PATH, LMAX)
    fake_alms = generate_fake_universe(cl, LMAX)

    # 2. Helical path geometry
    print(f"[*] Generating Helical Path (w*={W_STAR:.6f}, N={N_POINTS})...")
    theta_path, phi_path = get_helical_path(W_STAR, N_POINTS)

    # 3. Build mode lines ONCE for real & fake
    real_mode_lines = build_mode_lines(real_alms, LMAX, theta_path, phi_path)
    fake_mode_lines = build_mode_lines(fake_alms, LMAX, theta_path, phi_path)

    # 4. Reference (k=1) – no twist, just sum per-m lines
    print("[*] Computing reference (k=1) along helix...")
    ref_real = synthesize_along_helix_fast(real_mode_lines, phi_path, k_twist=1.0)
    ref_fake = synthesize_along_helix_fast(fake_mode_lines, phi_path, k_twist=1.0)

    # 5. Scan in k
    scores_real = []
    scores_fake = []

    print(f"[*] Scanning {len(K_SCAN)} twist values (Scanner 3 fast mode)...")
    for i, k in enumerate(K_SCAN):
        if i % 10 == 0:
            print(f"    k={k:.3f} ({i+1}/{len(K_SCAN)})")

        twist_real = synthesize_along_helix_fast(real_mode_lines, phi_path, k_twist=k)
        twist_fake = synthesize_along_helix_fast(fake_mode_lines, phi_path, k_twist=k)

        diff_real = np.abs(ref_real - twist_real)
        diff_fake = np.abs(ref_fake - twist_fake)

        scores_real.append(np.mean(diff_real))
        scores_fake.append(np.mean(diff_fake))

    # 6. Plot results
    print("[*] Plotting results...")
    plt.figure(figsize=(10, 6))

    plt.plot(K_SCAN, scores_real, label="Real Universe", linewidth=2)
    plt.plot(K_SCAN, scores_fake, label="Fake Universe (Random)", linestyle="--", alpha=0.7)

    plt.axvline(0.9, color="orange", linestyle=":", label="Traveler (k=0.9)")
    plt.axvline(1.0, color="black", alpha=0.3)

    plt.title(f"Helical Null Hypothesis Test (Scanner 3, w*={W_STAR:.6f})")
    plt.xlabel("Twist index k")
    plt.ylabel("Mean interference amplitude along helix")
    plt.grid(True, alpha=0.3)
    plt.legend()

    out_file = "helical_scan_fast_scanner3.png"
    plt.savefig(out_file, dpi=150)
    print(f"✅ Scanner 3 complete. Results saved to {out_file}")


if __name__ == "__main__":
    main()
