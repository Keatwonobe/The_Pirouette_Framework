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
LMAX = 40
N_RES = 400  # High resolution for precise biopsy
K_REALITY = 1.0
K_TRAVELER = 0.9

# Targets (Galactic Coordinates l, b in degrees)
# Cold Spot: approx (209, -57)
# Axis of Evil: roughly aligned with (260, 60)
TARGETS = {
    "The Cold Spot": (209.0, -57.0),
    "Axis of Evil (Dipole)": (260.0, 60.0), 
    "Great Attractor": (309.0, 10.0),
    "Galactic Center (Control)": (0.0, 0.0) 
}
BIOPSY_RADIUS_DEG = 7.0 # Integrating over a patch to capture the structure

# ======================
# UTILITIES
# ======================
def get_ylm(m, l, phi, theta):
    try:
        return sph_harm_y(l, m, phi, theta)
    except AttributeError:
        return sph_harm(m, l, phi, theta)

def get_data(fits_path, lmax):
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
    
    n_theta = lmax * 3
    n_phi = lmax * 4
    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]
    weights = np.sin(TH) * dtheta * dphi
    
    alms = {}
    print("[*] Extracting DNA...")
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = get_ylm(m, l, PH, TH)
            val = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            alms[(l, m)] = val
            
    return alms

def synthesize_map(alms, lmax, n_res, k):
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    map_out = np.zeros_like(TH, dtype=np.complex128)
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            Y_lm = get_ylm(m, l, PH, TH)
            twist_phase = np.exp(1j * m * (k - 1.0) * PH)
            map_out += alms[(l, m)] * Y_lm * twist_phase
            
    return map_out.real, TH, PH

def get_gradient_magnitude(image):
    gy, gx = np.gradient(image)
    return np.sqrt(gx**2 + gy**2)

def extract_region_stat(data, l_target, b_target, radius_deg, TH, PH):
    # Convert map coordinates to l, b
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    
    # Calculate angular separation
    c_target = SkyCoord(l=l_target*u.deg, b=b_target*u.deg, frame='galactic')
    c_map = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame='galactic')
    sep = c_target.separation(c_map).deg
    
    mask = sep < radius_deg
    if np.sum(mask) == 0: return 0.0
    return np.mean(data[mask])

# ======================
# MAIN
# ======================
def main():
    print("========================================")
    print("      CMB ANOMALY BIOPSY PROTOCOL       ")
    print("========================================")
    
    alms = get_data(FITS_PATH, LMAX)
    
    print(f"[*] Synthesizing Reality (k={K_REALITY}) & Traveler (k={K_TRAVELER})...")
    map_real, TH, PH = synthesize_map(alms, LMAX, N_RES, K_REALITY)
    map_traveler, _, _ = synthesize_map(alms, LMAX, N_RES, K_TRAVELER)
    
    print("[*] Calculating Tension Fields...")
    tension_real = get_gradient_magnitude(map_real)
    tension_traveler = get_gradient_magnitude(map_traveler)
    
    # Healing = Tension Real - Tension Traveler
    # Positive = Healing (Stress Removed)
    healing_map = tension_real - tension_traveler
    
    # Normalize for context (Z-score relative to full map)
    global_mean = np.mean(healing_map)
    global_std = np.std(healing_map)
    
    print(f"[*] Global Healing Mean: {global_mean:.4f}")
    print(f"[*] Global Healing Std:  {global_std:.4f}")
    
    results = {}
    z_scores = {}
    
    print("\n[*] BIOPSY RESULTS:")
    print("-" * 65)
    print(f"{'TARGET':<25} | {'HEALING SCORE':<15} | {'SIGMA':<10}")
    print("-" * 65)
    
    for name, (l, b) in TARGETS.items():
        score = extract_region_stat(healing_map, l, b, BIOPSY_RADIUS_DEG, TH, PH)
        z = (score - global_mean) / global_std
        results[name] = score
        z_scores[name] = z
        print(f"{name:<25} | {score:15.5f} | {z:10.2f}σ")

    print("-" * 65)
    
    # Plotting
    names = list(results.keys())
    zs = list(z_scores.values())
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, zs, color=['red' if z > 0 else 'blue' for z in zs], alpha=0.7)
    plt.axhline(0, color='black', linewidth=1)
    
    # Sigma Lines
    plt.axhline(1, color='gray', linestyle='--', alpha=0.3, label='1$\sigma$')
    plt.axhline(2, color='gray', linestyle='--', alpha=0.5, label='2$\sigma$')
    plt.axhline(3, color='gray', linestyle='--', alpha=0.8, label='3$\sigma$')
    
    plt.ylabel("Healing Significance ($\sigma$)")
    plt.title(f"Targeted Biopsy: Where does the Twist (k={K_TRAVELER}) heal the Sky?")
    plt.grid(True, axis='y', alpha=0.3)
    plt.legend()
    
    # Labels
    for bar, z in zip(bars, zs):
        yval = bar.get_height()
        offset = 0.1 if yval > 0 else -0.3
        plt.text(bar.get_x() + bar.get_width()/2, yval + offset, f"{z:.2f}σ", ha='center', fontweight='bold')
        
    plt.savefig("cmb_biopsy_results.png")
    print("✅ Biopsy chart saved to cmb_biopsy_results.png")

if __name__ == "__main__":
    main()