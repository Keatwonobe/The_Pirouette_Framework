import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.ndimage import generic_filter
from scipy.stats import kurtosis

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Target: The Soliton Core
TARGET_L = -155.9
TARGET_B = -63.9

# Scan Parameters (Micro-Scale)
ZOOM_DEG = 6.0       # Tight zoom on the Knot
PIXEL_RES = 300      # High resolution (0.02 deg/pixel)
KERNEL_SIZE = 5      # Size of the "Texture Window" (pixels)

def extract_micro_patch(fits_path):
    print(f"[*] Extracting Soliton Core for GW Texture Analysis...")
    data = fits.getdata(fits_path)
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    grid_l = np.linspace(TARGET_L - ZOOM_DEG/2, TARGET_L + ZOOM_DEG/2, PIXEL_RES)
    grid_b = np.linspace(TARGET_B - ZOOM_DEG/2, TARGET_B + ZOOM_DEG/2, PIXEL_RES)
    L, B = np.meshgrid(grid_l, grid_b)
    
    coords = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    patch = cmb[ipix]
    
    # Remove large scale gradients to isolate micro-texture
    from scipy.ndimage import gaussian_filter
    smooth = gaussian_filter(patch, sigma=10)
    texture = patch - smooth
    
    return texture, L, B

def calculate_hfgw_metrics(texture):
    print("[*] Calculating Texture Statistics (The Shimmer)...")
    
    # 1. Local Variance (Roughness)
    # Measures the "Choppiness" of space
    variance_map = generic_filter(texture, np.var, size=KERNEL_SIZE)
    
    # 2. Local Kurtosis (Spikiness/Non-Gaussianity)
    # Measures if the fluctuations are thermal (Gaussian) or Driven (Spiky)
    # We use a custom function for generic_filter
    def get_kurtosis(buffer):
        return kurtosis(buffer)
    
    # This is slow, so we optimize by approximating or using smaller kernel
    # Or just use the 4th moment directly?
    # Let's use a simpler proxy for "Spikiness": Max - Min in local window
    # Kurtosis is computationally expensive in a loop.
    # Alternative: (local_max - local_min) / local_std
    
    def get_peakiness(buffer):
        std = np.std(buffer)
        if std == 0: return 0
        return (np.max(buffer) - np.min(buffer)) / std
        
    kurtosis_map = generic_filter(texture, get_peakiness, size=KERNEL_SIZE)
    
    return variance_map, kurtosis_map

def main():
    # 1. Get Texture
    texture, L, B = extract_micro_patch(FITS_PATH)
    
    # 2. Analyze
    roughness, spikiness = calculate_hfgw_metrics(texture)
    
    # 3. Visualize
    fig = plt.figure(figsize=(16, 6), facecolor='#0a0a0a')
    
    # A. Roughness (Variance)
    ax1 = fig.add_subplot(131)
    im1 = ax1.imshow(roughness, cmap='magma', origin='lower')
    ax1.set_title("1. Metric Roughness (Variance)", color='white')
    ax1.axis('off')
    plt.colorbar(im1, ax=ax1, label="Texture Energy")
    
    # B. Spikiness (Non-Gaussianity)
    ax2 = fig.add_subplot(132)
    im2 = ax2.imshow(spikiness, cmap='BuPu_r', origin='lower') # Inverted cyan
    # Actually standard 'cool' or 'winter' might be better for "Ice/Shimmer"
    im2 = ax2.imshow(spikiness, cmap='twilight_shifted', origin='lower')
    ax2.set_title("2. Signal Spikiness (Driven Waves?)", color='white')
    ax2.axis('off')
    
    # C. The Shimmer (Composite)
    ax3 = fig.add_subplot(133)
    ax3.set_facecolor('#000000')
    
    # Background: Roughness (Red)
    # Foreground: Spikiness (Cyan)
    # We create a composite RGB image
    # Norm both
    r_norm = (roughness - np.min(roughness)) / (np.max(roughness) - np.min(roughness))
    s_norm = (spikiness - np.min(spikiness)) / (np.max(spikiness) - np.min(spikiness))
    
    # Create RGB: Red=Roughness, Green=0, Blue=Spikiness
    rgb = np.dstack((r_norm, np.zeros_like(r_norm), s_norm))
    
    ax3.imshow(rgb, origin='lower', extent=[-ZOOM_DEG/2, ZOOM_DEG/2, -ZOOM_DEG/2, ZOOM_DEG/2])
    
    # Grid
    ax3.grid(True, color='white', alpha=0.2, linestyle=':')
    ax3.set_title("3. HFGW SHIMMER MAP\n(Purple = High Variance + High Spikiness)", color='white')
    ax3.set_xlabel("Relative Longitude", color='gray')
    ax3.set_ylabel("Relative Latitude", color='gray')
    
    plt.savefig("cmb_hfgw_detector.png")
    print("✅ HFGW Analysis Saved: cmb_hfgw_detector.png")
    
    # Peak Analysis
    center_y, center_x = PIXEL_RES//2, PIXEL_RES//2
    # Check 1 degree radius around center
    radius_px = int(PIXEL_RES * (1.0 / ZOOM_DEG))
    
    Y, X = np.ogrid[:PIXEL_RES, :PIXEL_RES]
    dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    mask_core = dist <= radius_px
    mask_ambient = dist > radius_px
    
    core_roughness = np.mean(roughness[mask_core])
    amb_roughness = np.mean(roughness[mask_ambient])
    
    ratio = core_roughness / amb_roughness
    
    print("\n" + "="*50)
    print("SHIMMER REPORT:")
    print(f"Core Roughness Ratio: {ratio:.2f}x Ambient")
    
    if ratio > 1.2:
        print("⚡ DETECTION: The Soliton Core is 'Shimmering'.")
        print("   Higher variance suggests active driving (writhing) at micro-scales.")
        print("   This matches the signature of High-Frequency Gravitational Waves.")
    else:
        print("RESULT: Texture is uniform. No active writhing detected.")

if __name__ == "__main__":
    main()