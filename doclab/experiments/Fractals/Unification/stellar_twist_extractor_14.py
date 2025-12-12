import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.ndimage import gaussian_laplace

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Target: The Soliton Core (Refined from Spine Scan)
# You found the "Right" (East) side is deeper. Let's shift focus slightly East.
TARGET_L = -158.0 # Shifted slightly West (-155 -> -158) to center the body?
# Actually, East is *smaller* negative numbers in Galactic coords?
# Longitude 0 is center. +180 is left (East), -180 is right (West) usually.
# Let's stick to the previous TARGET_L as the center of the spine.
TARGET_L = -155.9
TARGET_B = -63.9

ZOOM_DEG = 12.0  # Tight zoom on the "Beast"
RES = 400        # Ultra-High Res for Edge Detection

def extract_patch(fits_path):
    print(f"[*] Extracting Soliton Core for Radar Scan...")
    data = fits.getdata(fits_path)
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    grid_l = np.linspace(TARGET_L - ZOOM_DEG/2, TARGET_L + ZOOM_DEG/2, RES)
    grid_b = np.linspace(TARGET_B - ZOOM_DEG/2, TARGET_B + ZOOM_DEG/2, RES)
    L, B = np.meshgrid(grid_l, grid_b)
    
    coords = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    patch = cmb[ipix]
    
    return patch, L, B

def calculate_shockwaves(patch):
    print("[*] Running Laplacian Edge Detection (Searching for Skin/Boundary)...")
    
    # 1. Gaussian Laplacian (LoG)
    # This detects "Edges" and "Blobs" by looking for 2nd derivative zero-crossings
    # Sigma controls the scale of the edge we are looking for.
    # Sigma=2 pixels (~0.06 deg) looks for sharp, fine boundaries.
    shockwave = gaussian_laplace(patch, sigma=2.0)
    
    # Invert contrast for visibility (Edges = Bright)
    shockwave = np.abs(shockwave)
    
    return shockwave

def main():
    # 1. Load
    patch, L, B = extract_patch(FITS_PATH)
    
    # 2. Radar Scan
    shockwave = calculate_shockwaves(patch)
    
    # 3. Visualize
    fig = plt.figure(figsize=(14, 12), facecolor='#001100') # Radar Theme
    
    # Plot A: The Raw Thermal Signature
    ax1 = fig.add_subplot(221)
    im1 = ax1.imshow(patch, cmap='magma', origin='lower')
    ax1.set_title("1. Thermal Mass (Temperature)", color='lime')
    ax1.axis('off')
    
    # Plot B: The Shockwave (Laplacian)
    ax2 = fig.add_subplot(222)
    # Enhance contrast
    vmax = np.percentile(shockwave, 98)
    im2 = ax2.imshow(shockwave, cmap='gray', origin='lower', vmax=vmax)
    ax2.set_title("2. Tension Boundary (The Skin)", color='lime')
    ax2.axis('off')
    
    # Plot C: The Composite Radar
    ax3 = fig.add_subplot(212)
    ax3.set_facecolor('#000000')
    
    # Background: Faint Thermal
    ax3.imshow(patch, cmap='magma', origin='lower', alpha=0.5, extent=[-ZOOM_DEG/2, ZOOM_DEG/2, -ZOOM_DEG/2, ZOOM_DEG/2])
    
    # Overlay: Bright Shockwaves
    # Create a mask for strong edges
    edge_mask = np.ma.masked_where(shockwave < np.mean(shockwave) + 1.0*np.std(shockwave), shockwave)
    ax3.imshow(edge_mask, cmap='spring', origin='lower', alpha=0.9, extent=[-ZOOM_DEG/2, ZOOM_DEG/2, -ZOOM_DEG/2, ZOOM_DEG/2])
    
    # Grid lines for "Radar" feel
    ax3.grid(True, color='lime', linestyle='--', alpha=0.3)
    ax3.set_title("3. SOLITON RADAR: Structure Identification", color='lime', fontsize=16)
    ax3.set_xlabel("Relative Longitude (deg)", color='lime')
    ax3.set_ylabel("Relative Latitude (deg)", color='lime')
    ax3.tick_params(colors='lime')
    
    # Crosshair at center
    ax3.axhline(0, color='lime', alpha=0.5)
    ax3.axvline(0, color='lime', alpha=0.5)
    
    plt.savefig("cmb_soliton_radar.png")
    print("✅ Radar Scan Saved: cmb_soliton_radar.png")
    
    print("\n" + "="*50)
    print("RADAR INTERPRETATION:")
    print("Look at Plot 3 (Composite).")
    print(" - If you see a coherent RING or SHELL (Magenta) enclosing the Heat (Orange/Black),")
    print("   you have found the Event Horizon of the Soliton.")
    print(" - If the edges are scattered/random, the object is unbound/dispersing.")

if __name__ == "__main__":
    main()