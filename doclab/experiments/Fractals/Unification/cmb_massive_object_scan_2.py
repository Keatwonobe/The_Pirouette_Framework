import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm, sph_harm_y
from scipy.ndimage import gaussian_filter
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 40
N_RES = 300
K_REALITY = 1.0
K_TRAVELER = 0.9
SMOOTHING_SIGMA = 10  # The "Defocus" factor to reveal large structures

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

# ======================
# MAIN
# ======================
def main():
    alms = get_data(FITS_PATH, LMAX)
    
    # 1. Synthesize
    print(f"[*] Synthesizing Reality vs Traveler...")
    map_real, TH, PH = synthesize_map(alms, LMAX, N_RES, K_REALITY)
    map_traveler, _, _ = synthesize_map(alms, LMAX, N_RES, K_TRAVELER)
    
    # 2. Calculate Raw Healing (Difference in Tension)
    # Positive = Healing (Reality has more tension than Traveler)
    healing_raw = get_gradient_magnitude(map_real) - get_gradient_magnitude(map_traveler)
    
    # 3. APPLY "MASSIVE OBJECT" SMOOTHING
    print(f"[*] Applying Gaussian Smoothing (Sigma={SMOOTHING_SIGMA})...")
    healing_smooth = gaussian_filter(healing_raw, sigma=SMOOTHING_SIGMA)
    
    # 4. Find the Peaks
    max_idx = np.unravel_index(np.argmax(healing_smooth), healing_smooth.shape)
    min_idx = np.unravel_index(np.argmin(healing_smooth), healing_smooth.shape)
    
    # Convert index to Galactic Coords for logging
    theta_max, phi_max = TH[max_idx], PH[max_idx]
    l_max = np.rad2deg((phi_max + 2*np.pi) % (2*np.pi))
    if l_max > 180: l_max -= 360
    b_max = np.rad2deg(0.5*np.pi - theta_max)
    
    theta_min, phi_min = TH[min_idx], PH[min_idx]
    l_min = np.rad2deg((phi_min + 2*np.pi) % (2*np.pi))
    if l_min > 180: l_min -= 360
    b_min = np.rad2deg(0.5*np.pi - theta_min)
    
    print("\n" + "="*40)
    print("      STRUCTURAL ANOMALY DETECTOR      ")
    print("="*40)
    print(f"MAX HEALING (The Biggest 'Knot' Untied):")
    print(f"  Coords: (l={l_max:.1f}, b={b_max:.1f})")
    print(f"  Score:  {healing_smooth[max_idx]:.4f}")
    print("-" * 40)
    print(f"MAX TENSION (The Stiffest Anchor):")
    print(f"  Coords: (l={l_min:.1f}, b={b_min:.1f})")
    print(f"  Score:  {healing_smooth[min_idx]:.4f}")
    print("="*40)
    
    # 5. Plot
    plt.figure(figsize=(12, 7))
    plt.imshow(healing_smooth.T, extent=[-180, 180, -90, 90], origin='lower', cmap='RdBu_r')
    plt.colorbar(label="Smoothed Healing Score")
    
    # Plot Markers
    plt.plot(l_max, b_max, 'g*', markersize=20, label='Max Healing (Void?)')
    plt.plot(l_min, b_min, 'rX', markersize=20, label='Max Tension (Mass?)')
    
    # Known Objects
    plt.plot(209-360, -57, 'go', fillstyle='none', markersize=15, markeredgewidth=2, label='Cold Spot')
    plt.plot(309-360, 10, 'rx', markersize=15, markeredgewidth=2, label='Great Attractor')
    
    plt.title(f"The 'Massive Object' Map (Smoothed sigma={SMOOTHING_SIGMA})\nRed = Released by Twist | Blue = Stressed by Twist")
    plt.xlabel("Galactic Longitude")
    plt.ylabel("Galactic Latitude")
    plt.legend(loc='lower right')
    
    outfile = "cmb_massive_object_scan_2.png"
    plt.savefig(outfile)
    print(f"✅ Scan complete. Saved to {outfile}")

if __name__ == "__main__":
    main()