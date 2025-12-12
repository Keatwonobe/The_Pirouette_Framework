import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.optimize import curve_fit

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Target: The Soliton Core
TARGET_L = -155.9
TARGET_B = -63.9

# Geometry
CORE_RADIUS = 4.0   # Degrees (The Bulge)
REF_RADIUS_IN = 8.0 # Reference Ring Inner
REF_RADIUS_OUT = 12.0 # Reference Ring Outer
PIXEL_RES = 400     # High Res for texture analysis

def extract_regions(fits_path):
    print(f"[*] Extracting Lens Regions at l={TARGET_L}, b={TARGET_B}...")
    
    # Load Data
    data = fits.getdata(fits_path)
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Create a large grid to sample from
    grid_l = np.linspace(TARGET_L - REF_RADIUS_OUT, TARGET_L + REF_RADIUS_OUT, PIXEL_RES)
    grid_b = np.linspace(TARGET_B - REF_RADIUS_OUT, TARGET_B + REF_RADIUS_OUT, PIXEL_RES)
    L, B = np.meshgrid(grid_l, grid_b)
    
    # Calculate radial distance map
    # Simple Euclidean approx is fine for local patches, but let's be decent
    dist = np.sqrt((L - TARGET_L)**2 + (B - TARGET_B)**2)
    
    coords = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    patch = cmb[ipix]
    
    # Isolate Core vs Reference
    core_mask = dist <= CORE_RADIUS
    ref_mask = (dist >= REF_RADIUS_IN) & (dist <= REF_RADIUS_OUT)
    
    return patch, core_mask, ref_mask

def calculate_psd(patch, mask):
    # Extract just the pixels in the mask
    pixels = patch[mask]
    
    # Remove mean/trend
    pixels = (pixels - np.mean(pixels)) / np.std(pixels)
    
    # We can't do a 2D FFT easily on a masked irregular shape.
    # Instead, we use the 1D Autocorrelation Function (ACF) to find characteristic scale.
    # Or simply: Histogram of gradients? No, we need Scale.
    
    # Robust Method: Isotropic Radial Power Spectrum via Autocorrelation
    # 1. Place masked data in a zero-padded box
    # This is complex. Let's use a simpler proxy:
    # The "Texture Coarseness" can be estimated by the standard deviation of the Gradients.
    # Coarse texture (Magnified) = Low Gradients. Fine texture (Unmagnified) = High Gradients.
    # BUT, amplitude affects this.
    
    # Better Method: 1D PSD of random chords (slices) through the region.
    # We take N random slices through the mask and average their PSDs.
    
    psds = []
    
    # Identify valid indices
    y_idxs, x_idxs = np.where(mask)
    
    if len(y_idxs) < 100: return None, None
    
    # Take horizontal and vertical slices
    # Iterate unique rows
    unique_rows = np.unique(y_idxs)
    for r in unique_rows:
        row_pixels = patch[r, mask[r, :]]
        if len(row_pixels) > 10:
            # Hanning window to reduce edge effects
            window = np.hanning(len(row_pixels))
            # FFT
            f = np.fft.rfftfreq(len(row_pixels))
            p = np.abs(np.fft.rfft(row_pixels * window))**2
            # Interpolate to common frequency base
            common_f = np.linspace(0, 0.5, 50)
            p_interp = np.interp(common_f, f, p)
            psds.append(p_interp)
            
    avg_psd = np.mean(psds, axis=0)
    freqs = np.linspace(0, 0.5, 50)
    
    return freqs, avg_psd

def fit_scale_shift(f, p_core, p_ref):
    print("[*] Calculating Magnification Factor...")
    
    # Normalize PSDs to peak 1.0 to compare SHAPE (Scale), not Amplitude
    p_core_norm = p_core / np.max(p_core)
    p_ref_norm = p_ref / np.max(p_ref)
    
    # Find the "Half-Power Point" or characteristic frequency
    # This is where the power drops to 0.5
    def find_half_power(freqs, psd):
        # descending sort just in case
        idx = np.where(psd < 0.5)[0]
        if len(idx) > 0:
            return freqs[idx[0]]
        return 0.5
        
    f_core_half = find_half_power(f, p_core_norm)
    f_ref_half = find_half_power(f, p_ref_norm)
    
    print(f"    Characteristic Freq (Core): {f_core_half:.4f}")
    print(f"    Characteristic Freq (Ref):  {f_ref_half:.4f}")
    
    # Frequency is inverse to Scale.
    # Lower Freq = Larger Scale = Magnification
    # M = F_ref / F_core
    
    if f_core_half > 0:
        mag_factor = f_ref_half / f_core_half
    else:
        mag_factor = 1.0
        
    return mag_factor, p_core_norm, p_ref_norm

def main():
    # 1. Extract
    patch, core_mask, ref_mask = extract_regions(FITS_PATH)
    
    # 2. Analyze Texture
    f, p_core = calculate_psd(patch, core_mask)
    _, p_ref = calculate_psd(patch, ref_mask)
    
    if p_core is None or p_ref is None:
        print("[!] Error: Region too small.")
        return

    # 3. Measure Lensing
    M, p_c_n, p_r_n = fit_scale_shift(f, p_core, p_ref)
    
    # 4. Visualize
    fig = plt.figure(figsize=(12, 6), facecolor='#0a0a0a')
    
    # A. The Regions
    ax1 = fig.add_subplot(121)
    # create composite map
    vis_map = np.zeros_like(patch)
    vis_map[ref_mask] = 0.5
    vis_map[core_mask] = 1.0
    
    ax1.imshow(patch, cmap='gray', origin='lower', alpha=0.6)
    ax1.imshow(vis_map, cmap='spring', origin='lower', alpha=0.3)
    ax1.set_title("1. Lensing Zones (Core vs Reference)", color='white')
    ax1.axis('off')
    
    # B. The Spectral Shift
    ax2 = fig.add_subplot(122)
    ax2.set_facecolor('#111111')
    
    ax2.plot(f, p_r_n, color='gray', linestyle='--', label='Background Texture', linewidth=2)
    ax2.plot(f, p_c_n, color='cyan', label='Bulge Texture (Core)', linewidth=3)
    
    # Shift Arrow
    if M > 1.05:
        ax2.arrow(0.2, 0.5, -0.05, 0, color='lime', head_width=0.05, label='Redshift (Magnification)')
    elif M < 0.95:
        ax2.arrow(0.1, 0.5, 0.05, 0, color='red', head_width=0.05, label='Blueshift (Minification)')
        
    ax2.set_title(f"2. Texture Power Spectrum\nMagnification M = {M:.3f}x", color='white', fontsize=14)
    ax2.set_xlabel("Frequency (1/Scale)", color='gray')
    ax2.set_ylabel("Normalized Power", color='gray')
    ax2.grid(True, color='#333333')
    ax2.legend()
    
    plt.savefig("cmb_lens_magnifier.png")
    print("✅ Lensing Analysis Saved: cmb_lens_magnifier.png")
    
    print("\n" + "="*50)
    print(f"LENSING REPORT:")
    print(f"Magnification Factor: {M:.3f}x")
    
    if M > 1.1:
        print("⚡ CONFIRMED: The Bulge acts as a MAGNIFYING LENS.")
        print("   The CMB texture inside is larger than the background.")
        print("   This implies a convex geometry (Mass/Bubble).")
    elif M < 0.9:
        print("⚡ CONFIRMED: The Bulge acts as a MINIFYING LENS.")
        print("   The CMB texture inside is smaller/tighter.")
        print("   This implies a concave geometry (Pinch/Knot).")
    else:
        print("RESULT: No lensing detected. The texture is uniform.")

if __name__ == "__main__":
    main()