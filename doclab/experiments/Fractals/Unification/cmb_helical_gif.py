import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.special import sph_harm
from PIL import Image
import os
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Resonance Parameters
LMAX = 40                 # Low LMAX for large-scale topology
N_POINTS = 5000           # Resolution along the helical path (lower = faster GIF)
W_STAR = 1.0047468850     # The "Squaring the Circle" Resonance

# Animation Parameters
GIF_NAME = "helical_resonance_scan.gif"
FRAMES = 100
DURATION = 50             # ms per frame
K_START = 0.5             # Twist start
K_END = 1.5               # Twist end
K_SCAN = np.linspace(K_START, K_END, FRAMES)

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
    
    return theta, phi, z

# ======================
# 2. PHYSICS: FAST TWIST SYNTHESIS
# ======================
def synthesize_along_helix(alms, lmax, theta_path, phi_path, k_twist=1.0):
    """
    Synthesizes the signal ONLY at the coordinates of the helix.
    Includes the Topological Twist (phase shift).
    """
    signal = np.zeros_like(theta_path, dtype=np.complex128)
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            
            # 1. Standard Geometric Component
            Y_lm = sph_harm(m, l, phi_path, theta_path)
            
            # 2. Topological Twist (The Phase Shift)
            # Twist: phi -> phi * k
            twist_phase = np.exp(1j * m * (k_twist - 1.0) * phi_path)
            
            signal += alms[(l, m)] * Y_lm * twist_phase
            
    return signal.real

# ======================
# 3. DATA: DNA EXTRACTION & FAKE GENERATION
# ======================
def extract_dna_from_fits(fits_path, lmax):
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
    
    # Integration grid
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
    print("[*] Generating Fake Universe (Geometric Baseline)...")
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
# 4. GIF GENERATION
# ======================
def main():
    # 1. Load Data & Geometry
    real_alms, cl = extract_dna_from_fits(FITS_PATH, LMAX)
    fake_alms = generate_fake_universe(cl, LMAX)
    theta_path, phi_path, z_path = get_helical_path(W_STAR, N_POINTS)
    
    print(f"[*] Starting Helical GIF Generation ({FRAMES} frames)...")
    frames = []
    
    # Calculate global y-limits for stability
    # We do a quick check on k=1 to set reasonable bounds
    ref_real = synthesize_along_helix(real_alms, LMAX, theta_path, phi_path, 1.0)
    ref_diff = ref_real - synthesize_along_helix(fake_alms, LMAX, theta_path, phi_path, 1.0)
    y_max_sig = np.max(np.abs(ref_real)) * 1.5
    y_max_diff = np.max(np.abs(ref_diff)) * 2.0

    for i, k in enumerate(K_SCAN):
        sys.stdout.write(f"\r[>] Processing Frame {i+1}/{FRAMES} (k={k:.4f})")
        sys.stdout.flush()
        
        # Synthesize waveforms
        sig_real = synthesize_along_helix(real_alms, LMAX, theta_path, phi_path, k)
        sig_fake = synthesize_along_helix(fake_alms, LMAX, theta_path, phi_path, k)
        differential = sig_real - sig_fake
        
        # Plotting
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        
        # Panel 1: The Raw Waveforms
        ax1.plot(z_path, sig_real, color='blue', alpha=0.8, linewidth=1, label='Real Universe')
        ax1.plot(z_path, sig_fake, color='gray', alpha=0.5, linewidth=1, linestyle='--', label='Fake (Geometric)')
        ax1.set_ylim(-y_max_sig, y_max_sig)
        ax1.set_ylabel("CMB Temperature (K)")
        ax1.set_title(f"Helical Resonance Scan | Twist k = {k:.4f}")
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.2)
        
        # Panel 2: The Differential (Anomaly)
        ax2.plot(z_path, differential, color='red', linewidth=1.5)
        ax2.set_ylim(-y_max_diff, y_max_diff)
        ax2.set_xlabel("Helical Path Position (z = -1 to 1)")
        ax2.set_ylabel("Differential (Real - Fake)")
        ax2.set_title("Topological Anomaly (Coherence Check)")
        ax2.grid(True, alpha=0.2)
        
        # Mark resonance points visually
        if abs(k - 0.9) < 0.01:
            ax1.text(0, y_max_sig*0.8, "THE TRAVELER (0.9)", color='orange', ha='center', weight='bold')
        if abs(k - 1.0) < 0.01:
            ax1.text(0, y_max_sig*0.8, "IDENTITY (1.0)", color='green', ha='center', weight='bold')
            
        plt.tight_layout()
        
        # Save to buffer
        fname = f"temp_frame_{i}.png"
        plt.savefig(fname, dpi=100)
        plt.close(fig)
        
        frames.append(Image.open(fname))
        os.remove(fname)

    print(f"\n[*] Saving GIF to {GIF_NAME}...")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=DURATION, loop=0)
    print("✅ Done.")

if __name__ == "__main__":
    main()