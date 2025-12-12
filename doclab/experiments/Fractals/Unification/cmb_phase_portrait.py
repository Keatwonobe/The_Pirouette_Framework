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
L_SKELETON = 10         # The "Container"
L_FLUID = 20            # The "Content"
N_RES = 200             # Resolution
K_SCAN = np.linspace(0.8, 1.2, 100) # High res scan for smooth phase lines

# ======================
# UTILITIES
# ======================
def get_ylm(m, l, phi, theta):
    try:
        return sph_harm_y(l, m, phi, theta)
    except AttributeError:
        return sph_harm(m, l, phi, theta)

def extract_specific_mode_alms(fits_path, target_l):
    print(f"[*] Loading CMB and extracting ONLY L={target_l}...")
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

    n_theta = target_l * 4
    n_phi = target_l * 8
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
    l = target_l
    for m in range(-l, l + 1):
        Y_lm = get_ylm(m, l, PH, TH)
        val = np.sum(T_sample * np.conjugate(Y_lm) * weights)
        alms[(l, m)] = val
        
    return alms

def synthesize_map(alms, target_l, n_res, k):
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    map_out = np.zeros_like(TH, dtype=np.complex128)
    l = target_l
    for m in range(-l, l + 1):
        if (l, m) not in alms: continue
        Y_lm = get_ylm(m, l, PH, TH)
        twist_phase = np.exp(1j * m * (k - 1.0) * PH)
        map_out += alms[(l, m)] * Y_lm * twist_phase
    return map_out.real

# ======================
# PHASE PORTRAIT LOGIC
# ======================
def main():
    alms_skel = extract_specific_mode_alms(FITS_PATH, L_SKELETON)
    alms_fluid = extract_specific_mode_alms(FITS_PATH, L_FLUID)
    
    correlations = []
    
    print(f"[*] Scanning Phase Space (k={K_SCAN[0]} to {K_SCAN[-1]})...")
    
    for k in K_SCAN:
        map_skel = synthesize_map(alms_skel, L_SKELETON, N_RES, k)
        map_fluid = synthesize_map(alms_fluid, L_FLUID, N_RES, k)
        
        flat_skel = np.abs(map_skel).flatten()
        flat_fluid = np.abs(map_fluid).flatten()
        
        corr = np.corrcoef(flat_skel, flat_fluid)[0, 1]
        correlations.append(corr)

    # Calculate Velocity (Derivative)
    correlations = np.array(correlations)
    velocity = np.gradient(correlations, K_SCAN)

    # Plotting
    plt.figure(figsize=(10, 8))
    
    # The Phase Portrait
    plt.plot(correlations, velocity, color='black', linewidth=1, alpha=0.5)
    plt.scatter(correlations, velocity, c=K_SCAN, cmap='twilight', s=50, label='Twist Evolution')
    
    # Mark the Start/End/Center
    plt.plot(correlations[0], velocity[0], 'go', markersize=10, label='Start (k=0.8)')
    plt.plot(correlations[-1], velocity[-1], 'ro', markersize=10, label='End (k=1.2)')
    
    # Find k=1 index
    idx_1 = np.argmin(np.abs(K_SCAN - 1.0))
    plt.plot(correlations[idx_1], velocity[idx_1], 'b*', markersize=20, label='Identity (k=1)')
    
    plt.title(f"Cosmic Phase Portrait: Attractor Geometry\n(L={L_SKELETON} vs L={L_FLUID})")
    plt.xlabel("Shear Stress (Correlation)")
    plt.ylabel("Instability (Rate of Change dC/dk)")
    plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(0, color='gray', linestyle='--', alpha=0.5)
    plt.colorbar(label='Twist k')
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    plt.savefig("cmb_phase_portrait.png")
    print("✅ Phase Portrait saved to cmb_phase_portrait.png")

if __name__ == "__main__":
    main()