import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.ndimage import rotate

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Target: The Cold Spot Core
TARGET_L = -155.9
TARGET_B = -63.9

# Scan Parameters
ZOOM_DEG = 15.0      # Width of the patch
PIXEL_RES = 300      # Resolution
CHANNEL_ANGLE = -90.0 # From your previous result

def load_patch(fits_path):
    print(f"[*] Extracting Channel Region (l={TARGET_L}, b={TARGET_B})...")
    data = fits.getdata(fits_path)
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Extract square patch
    grid_l = np.linspace(TARGET_L - ZOOM_DEG/2, TARGET_L + ZOOM_DEG/2, PIXEL_RES)
    grid_b = np.linspace(TARGET_B - ZOOM_DEG/2, TARGET_B + ZOOM_DEG/2, PIXEL_RES)
    L, B = np.meshgrid(grid_l, grid_b)
    coords = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    patch = cmb[ipix]
    
    # Normalize
    patch = (patch - np.mean(patch)) / np.std(patch)
    return patch

def profile_channel(patch, angle):
    print(f"[*] Rotating Channel by {angle}° to align Horizon...")
    # Rotate so the channel runs Left-Right (Horizontal)
    # If gradients point North/South (-90), the channel runs East/West (0).
    # We rotate by -angle to bring the gradients to vertical, meaning channel is horizontal.
    # Actually, we just want to slice perpendicular to the channel.
    # If channel runs East-West, we want a North-South slice.
    
    # Let's rotate the PATCH so the channel is vertical, then slice horizontally?
    # No, let's rotate so channel is horizontal, then column-average (North-South profile).
    
    # Your result: Dominant Gradient Axis = -90 (Vertical). 
    # This means steep slopes are Top-to-Bottom. The Channel runs Left-Right.
    # No rotation needed to align with array axes! (Already roughly aligned with Lat/Lon).
    
    # We will refine alignment just in case.
    rot_patch = rotate(patch, 0, reshape=False) # 0 rotation for now as -90 is vertical axis
    
    # Collapse along the channel length (Longitude/X-axis) to get average Profile (Latitude/Y-axis)
    profile = np.mean(rot_patch, axis=1) 
    
    # Calculate Wall Steepness (Derivative of profile)
    walls = np.gradient(profile)
    
    return rot_patch, profile, walls

def main():
    patch = load_patch(FITS_PATH)
    
    # We profile perpendicular to the channel
    # Since channel runs East-West (gradients are North-South), we profile the Y-axis.
    aligned_patch, profile, walls = profile_channel(patch, CHANNEL_ANGLE)
    
    fig = plt.figure(figsize=(14, 8), facecolor='#0a0a0a')
    
    # 1. The Channel Map
    ax1 = fig.add_subplot(221)
    im = ax1.imshow(aligned_patch, cmap='RdBu_r', origin='lower', aspect='auto')
    ax1.set_title("1. The Cold Channel (Aligned)", color='white')
    ax1.set_ylabel("Cross-Section Axis", color='gray')
    ax1.set_xlabel("Channel Length", color='gray')
    ax1.axhline(PIXEL_RES//2, color='lime', linestyle='--', alpha=0.5)
    
    # 2. The Cross-Section Profile
    ax2 = fig.add_subplot(222)
    ax2.set_facecolor('#111111')
    x_axis = np.linspace(-ZOOM_DEG/2, ZOOM_DEG/2, len(profile))
    
    ax2.plot(x_axis, profile, color='cyan', linewidth=2, label='Temperature Depth')
    ax2.fill_between(x_axis, profile, min(profile), color='cyan', alpha=0.1)
    
    ax2.set_title("2. Channel Cross-Section (The Shape of the Cut)", color='white')
    ax2.set_xlabel("Degrees from Center", color='gray')
    ax2.set_ylabel("Depth (Sigma)", color='gray')
    ax2.grid(True, color='#333333')
    
    # 3. The Wall Steepness (Surface Tension)
    ax3 = fig.add_subplot(212)
    ax3.set_facecolor('#111111')
    
    ax3.plot(x_axis, np.abs(walls), color='magenta', linewidth=2)
    ax3.set_title("3. Wall Steepness (Surface Tension Detector)", color='white')
    ax3.set_xlabel("Degrees from Center", color='gray')
    ax3.set_ylabel("Gradient Magnitude", color='gray')
    
    # Peak Detection
    peaks = np.where(np.abs(walls) > np.max(np.abs(walls))*0.6)[0]
    if len(peaks) >= 2:
        width_idx = peaks[-1] - peaks[0]
        width_deg = width_idx * (ZOOM_DEG / PIXEL_RES)
        ax3.axvline(x_axis[peaks[0]], color='white', linestyle='--')
        ax3.axvline(x_axis[peaks[-1]], color='white', linestyle='--')
        ax3.text(0, np.max(np.abs(walls))*0.8, f"CHANNEL WIDTH: {width_deg:.2f}°", 
                 color='white', ha='center', fontsize=14, fontweight='bold')
        print(f"\n[!] MEASURED CHANNEL WIDTH: {width_deg:.4f} degrees")
    
    ax3.grid(True, color='#333333')
    ax3.tick_params(colors='gray')
    
    plt.tight_layout()
    plt.savefig("cmb_channel_profile.png")
    print("✅ Profile Analysis Saved: cmb_channel_profile.png")

if __name__ == "__main__":
    main()