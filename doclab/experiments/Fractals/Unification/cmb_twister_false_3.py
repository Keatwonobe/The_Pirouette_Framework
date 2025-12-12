import numpy as np
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb 
from scipy.special import sph_harm
from scipy.ndimage import gaussian_filter

# ======================
# CONFIG
# ======================
TWIST_MODE = "untwist"
LMAX = 40
N_THETA = 320 
N_PHI = 640
NSIDE = 2048 # Same resolution as the original CMB file

# We will just look at one known "line-heavy" K value for speed
TEST_K_VALUES = [1.96994992] 

# ======================
# HELPERS
# ======================

def twist_phi(phi, k, mode="untwist"):
    if mode == "twist":
        src = phi * k
    else:
        src = phi / k
    return (src + np.pi) % (2.0 * np.pi) - np.pi

def build_equatorial_grid(n_theta, n_phi):
    theta = np.linspace(0.0, np.pi, n_theta)
    phi   = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")
    return TH, PH

def healpix_sample(cmb, hpix, TH, PH):
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH) 
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    return cmb[ipix]

def render_helicity_view(T, PH):
    hue = (PH + np.pi) / (2 * np.pi)
    T_clean = T.copy()
    T_clean[np.isnan(T_clean)] = np.nanmedian(T)
    log_amp = np.log1p(np.abs(T_clean - T_clean.mean())) 
    structure = np.sin(log_amp * 30.0)
    val = 0.6 + 0.4 * structure
    sat = np.ones_like(hue) * 0.95
    hsv = np.dstack((hue, sat, val))
    return hsv_to_rgb(hsv)

def calculate_laplacian(image):
    grad_y, grad_x = np.gradient(image)
    return np.gradient(grad_x, axis=1) + np.gradient(grad_y, axis=0)

# ======================
# MAIN
# ======================

def main_round_trip():
    print("[*] STEP 1: Generating Smooth Red Noise (The 'Fake' Universe)...")
    np.random.seed(42)
    # Generate on a high-res grid first
    temp_theta = np.linspace(0, np.pi, 1000)
    temp_phi = np.linspace(-np.pi, np.pi, 2000)
    TH_gen, PH_gen = np.meshgrid(temp_theta, temp_phi, indexing='ij')
    
    noise = np.random.normal(0, 1, size=TH_gen.shape)
    smooth_noise = gaussian_filter(noise, sigma=5.0) # Nice big blobs
    
    print("[*] STEP 2: Projecting Red Noise into HEALPix (Mimicking the file format)...")
    hpix = HEALPix(nside=NSIDE, order="ring", frame="galactic")
    
    # Convert generator grid to HEALPix indices
    lon_deg = np.rad2deg((PH_gen + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_gen)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix_gen = hpix.lonlat_to_healpix(coords.l, coords.b)
    
    # Fill the HEALPix array
    cmb_healpix = np.zeros(hpix.npix)
    # Use simple averaging for projection (mapping grid to pixels)
    # (In a real scenario we'd use spherical harmonics, but this is enough to create the grid structure)
    cmb_healpix[ipix_gen.ravel()] = smooth_noise.ravel()
    
    # Fill gaps (simple nearest neighbor fill for empty pixels to avoid black spots)
    zero_mask = cmb_healpix == 0
    cmb_healpix[zero_mask] = np.mean(cmb_healpix[~zero_mask])

    print("[*] STEP 3: Sampling twisted map from the HEALPix array...")
    
    TH, PH = build_equatorial_grid(N_THETA, N_PHI)
    cmb_orig = healpix_sample(cmb_healpix, hpix, TH, PH)
    
    for k_val in TEST_K_VALUES:
        print(f"    -> Twisting with k={k_val}...")
        PH_src = twist_phi(PH, k_val, mode=TWIST_MODE)
        cmb_twisted = healpix_sample(cmb_healpix, hpix, TH, PH_src)
        
        # Plotting
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # Original
        axes[0].imshow(cmb_orig, origin="lower", cmap="coolwarm")
        axes[0].set_title("1. Red Noise (via HEALPix)")
        
        # Twisted
        axes[1].imshow(cmb_twisted, origin="lower", cmap="coolwarm")
        axes[1].set_title(f"2. Twisted Red Noise (k={k_val})")
        
        # Laplacian
        lap = calculate_laplacian(cmb_twisted)
        axes[2].imshow(lap, origin="lower", cmap="bwr")
        axes[2].set_title("3. Laplacian (Look for lines!)")
        
        filename = f"healpix_roundtrip_k_{k_val}.png"
        plt.savefig(filename)
        print(f"[+] Saved {filename}. Check this image for lines!")
        plt.close(fig)

if __name__ == "__main__":
    main_round_trip()