import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Target: The Cold Spot Core
TARGET_L = -155.9
TARGET_B = -63.9

# Zoom Level (Deep Micro-Scan)
ZOOM_DEG = 10.0      # 10x10 degree patch
PIXEL_RES = 400      # High resolution grid (0.025 deg/pixel)

def load_hires_patch(fits_path):
    print(f"[*] Loading High-Res Planck Data (Microscope Mode)...")
    
    # Load FULL resolution data
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print("[!] File not found.")
        return None
        
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    
    # Handle NaNs
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    
    # Determine NSIDE from array size
    nside = int(np.sqrt(cmb.size / 12))
    print(f"    Native Resolution: NSIDE {nside}")
    
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Create the Microscope Grid
    grid_l = np.linspace(TARGET_L - ZOOM_DEG/2, TARGET_L + ZOOM_DEG/2, PIXEL_RES)
    grid_b = np.linspace(TARGET_B - ZOOM_DEG/2, TARGET_B + ZOOM_DEG/2, PIXEL_RES)
    L, B = np.meshgrid(grid_l, grid_b)
    
    # Interpolate
    coords = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    patch = cmb[ipix]
    
    return patch, L, B

def analyze_tension(patch):
    print("[*] Calculating Gradient Tension Field...")
    
    # Calculate Gradients (The "Stress" Vectors)
    grad_y, grad_x = np.gradient(patch)
    
    # Tension Magnitude (How tight is the squeeze?)
    tension = np.sqrt(grad_x**2 + grad_y**2)
    
    # Flow Orientation (0 to 180 degrees)
    # We want to know if they align like a channel
    angle = np.arctan2(grad_y, grad_x)
    
    return tension, angle, grad_x, grad_y

def measure_coherence(angle_map, tension_map):
    # Coherence = How parallel are the vectors?
    # We use the structure tensor approach or simple angular variance weighted by tension
    
    # Create a Rose Plot (Histogram of Angles)
    # We weight by tension so low-energy noise doesn't matter
    hist, bins = np.histogram(angle_map.flatten(), bins=72, weights=tension_map.flatten(), range=(-np.pi, np.pi))
    
    return hist, bins

def main():
    # 1. Load Data
    patch, L, B = load_hires_patch(FITS_PATH)
    if patch is None: return
    
    # 2. Analyze
    tension, angle, gx, gy = analyze_tension(patch)
    hist, bins = measure_coherence(angle, tension)
    
    # 3. Visualize
    fig = plt.figure(figsize=(16, 10), facecolor='#0a0a0a')
    
    # Plot A: The Tension Map (Where is the stress?)
    ax1 = fig.add_subplot(221)
    # We emphasize high gradients (Edges/Channels)
    im1 = ax1.imshow(tension, cmap='inferno', origin='lower', extent=[-ZOOM_DEG/2, ZOOM_DEG/2, -ZOOM_DEG/2, ZOOM_DEG/2])
    ax1.set_title("1. Tension Map (Gradient Magnitude)", color='white')
    ax1.set_xlabel("Relative Longitude", color='gray')
    ax1.set_ylabel("Relative Latitude", color='gray')
    plt.colorbar(im1, ax=ax1, label="Stress Intensity")
    
    # Plot B: The Flow Field (The Channel)
    ax2 = fig.add_subplot(222)
    ax2.set_facecolor('#0a0a0a')
    
    # Downsample for quiver
    skip = 15
    ax2.quiver(L[::skip, ::skip], B[::skip, ::skip], 
               gx[::skip, ::skip], gy[::skip, ::skip], 
               color='cyan', headlength=3, headwidth=2, scale=50)
    
    ax2.set_title("2. Micro-Flow Field (The Channel)", color='white')
    ax2.set_xlabel("Longitude", color='gray')
    ax2.set_ylabel("Latitude", color='gray')
    
    # Plot C: Coherence Rose (The Alignment)
    ax3 = fig.add_subplot(212, projection='polar')
    ax3.set_facecolor('#0a0a0a')
    
    # Plot histogram
    width = bins[1] - bins[0]
    ax3.bar(bins[:-1], hist, width=width, color='lime', alpha=0.7, edgecolor='white')
    
    ax3.set_title("3. Alignment Scanner (Is there a preferred axis?)", color='white', pad=20)
    ax3.tick_params(colors='gray')
    ax3.grid(True, color='#333333')
    
    plt.savefig("cmb_tension_microscope.png")
    print("✅ Microscope Scan Saved: cmb_tension_microscope.png")
    
    # Interpret
    peak_angle_idx = np.argmax(hist)
    peak_angle = bins[peak_angle_idx]
    peak_deg = np.degrees(peak_angle)
    
    # Calculate Variance (Dispersion)
    # Low variance = High Alignment (Channel)
    # High variance = Isotropic (Noise/Swirl)
    # Circular variance approx
    
    print("\n" + "="*50)
    print(f"DOMINANT CHANNEL AXIS: {peak_deg:.1f}°")
    print("INTERPRETATION:")
    print("   Look at the Rose Plot (Bottom).")
    print("   - Sharp Spikes = Taut Channel (Linear Structure)")
    print("   - Round/Uniform = Noise or Isotropic Hole")

if __name__ == "__main__":
    main()