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
N_RES = 300
K_REALITY = 1.0
K_TRAVELER = 0.9  # The "Relaxed" State

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
            
    return map_out.real

def get_gradient_magnitude(image):
    gy, gx = np.gradient(image)
    return np.sqrt(gx**2 + gy**2)

# ======================
# MAIN
# ======================
def main():
    alms = get_data(FITS_PATH, LMAX)
    
    print(f"[*] Synthesizing Reality (k={K_REALITY})...")
    map_real = synthesize_map(alms, LMAX, N_RES, K_REALITY)
    
    print(f"[*] Synthesizing Traveler (k={K_TRAVELER})...")
    map_traveler = synthesize_map(alms, LMAX, N_RES, K_TRAVELER)
    
    # Calculate Tension (Gradient Magnitude)
    tension_real = get_gradient_magnitude(map_real)
    tension_traveler = get_gradient_magnitude(map_traveler)
    
    # The Delta: Positive means Reality is MORE stressed than Traveler
    delta_tension = tension_real - tension_traveler
    
    # Visualization
    plt.figure(figsize=(12, 8))
    
    # Use a diverging colormap
    # Red = Relief (Reality was tighter)
    # Blue = Stress (Traveler is tighter)
    limit = np.max(np.abs(delta_tension)) * 0.8
    
    plt.imshow(delta_tension.T, extent=[-180, 180, -90, 90], origin='lower', 
               cmap='RdBu_r', vmin=-limit, vmax=limit)
    
    plt.colorbar(label='Tension Relief (Positive = Relief)')
    plt.title(f"The Healing Map: Where does k={K_TRAVELER} fix the Universe?\n(Red = Tension Released, Blue = Tension Added)")
    plt.xlabel("Galactic Longitude")
    plt.ylabel("Galactic Latitude")
    
    plt.contour(delta_tension.T, levels=[0], colors='black', linewidths=0.5, extent=[-180, 180, -90, 90], origin='lower')
    
    outfile = "cmb_tension_relief_map.png"
    plt.savefig(outfile)
    print(f"✅ Map saved to {outfile}")

if __name__ == "__main__":
    main()