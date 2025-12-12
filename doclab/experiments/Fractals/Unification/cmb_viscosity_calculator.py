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
L_SKELETON = 10         # The "Container" (Bass)
L_FLUID = 20            # The "Content" (Tenor)
N_RES = 200             # Lower resolution for faster calc
K_SCAN = np.linspace(0.8, 1.2, 50) # The Stirring Range

# ======================
# CORE UTILITIES
# ======================
def get_ylm(m, l, phi, theta):
    try:
        return sph_harm_y(l, m, phi, theta)
    except AttributeError:
        return sph_harm(m, l, phi, theta)

def extract_specific_mode_alms(fits_path, target_l):
    """
    Extracts ONLY the alms for a specific L mode.
    """
    print(f"[*] Loading CMB and extracting ONLY L={target_l}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    
    # Infill
    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # Integration grid
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
# MAIN EXECUTION
# ======================
def main():
    # 1. Load the Two Layers
    alms_skeleton = extract_specific_mode_alms(FITS_PATH, L_SKELETON)
    alms_fluid = extract_specific_mode_alms(FITS_PATH, L_FLUID)
    
    correlations = []
    
    print(f"[*] Calculating Shear Stress (Correlation) from k={K_SCAN[0]} to {K_SCAN[-1]}...")
    
    for k in K_SCAN:
        # Synthesize both layers with the same twist
        # If they are "locked", the correlation of their ENERGY (abs val) should be high
        map_skel = synthesize_map(alms_skeleton, L_SKELETON, N_RES, k)
        map_fluid = synthesize_map(alms_fluid, L_FLUID, N_RES, k)
        
        # We compare the "Shape" (Absolute Magnitude), not the raw phase (which is orthogonal)
        # This checks if the "Bubbles" of L=20 stay inside the "Cells" of L=10
        flat_skel = np.abs(map_skel).flatten()
        flat_fluid = np.abs(map_fluid).flatten()
        
        # Pearson Correlation Coefficient
        corr = np.corrcoef(flat_skel, flat_fluid)[0, 1]
        correlations.append(corr)
        
        if abs(k - 1.0) < 0.01:
            print(f"    [k=1.00] Baseline Friction: {corr:.4f}")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(K_SCAN, correlations, color='purple', linewidth=2.5, label='Shear Coupling')
    
    plt.axvline(1.0, color='black', linestyle='--', alpha=0.5, label='Identity (k=1)')
    plt.title(f"Cosmic Viscosity: Coupling between L={L_SKELETON} and L={L_FLUID}")
    plt.xlabel("Twist Factor k (Stirring)")
    plt.ylabel("Energy Correlation Coefficient")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    filename = "cmb_viscosity_curve.png"
    plt.savefig(filename)
    print(f"✅ Viscosity Curve saved to {filename}")

if __name__ == "__main__":
    main()