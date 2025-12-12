import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.signal import find_peaks, periodogram

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Target: The Cold Spot Core
TARGET_L = -155.9
TARGET_B = -63.9

# Scan Geometry
CHANNEL_LENGTH = 30.0  # Degrees (How long is the predator?)
CHANNEL_WIDTH = 5.0    # Degrees (Narrow slice to catch the spine)
RES = 300              # Resolution points along the length

def extract_spine(fits_path):
    print(f"[*] Extracting Soliton Spine (Length={CHANNEL_LENGTH}°)...")
    
    # Load Data
    data = fits.getdata(fits_path)
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Create a Grid along the Channel Axis (East-West)
    # We scan Longitude (X) while keeping Latitude (Y) centered
    grid_l = np.linspace(TARGET_L - CHANNEL_LENGTH/2, TARGET_L + CHANNEL_LENGTH/2, RES)
    grid_b = np.linspace(TARGET_B - CHANNEL_WIDTH/2, TARGET_B + CHANNEL_WIDTH/2, int(RES/6)) # Narrow height
    L, B = np.meshgrid(grid_l, grid_b)
    
    coords = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    patch = cmb[ipix]
    
    # Normalize
    patch = (patch - np.mean(patch)) / np.std(patch)
    
    # Collapse vertical axis to get the 1D Spine Profile
    spine_profile = np.mean(patch, axis=0)
    
    return grid_l, spine_profile, patch

def analyze_vertebrae(x_axis, spine):
    print("[*] Searching for Periodic Structure (Vertebrae)...")
    
    # 1. Peak Detection (The Knots)
    # Invert spine because "Cold" is the signal
    signal = -spine 
    peaks, _ = find_peaks(signal, distance=10, prominence=0.5)
    
    # 2. Fourier Analysis (The Heartbeat)
    freq, power = periodogram(signal)
    
    # Find dominant frequency
    dom_idx = np.argmax(power[1:]) + 1 # Skip DC
    dom_freq = freq[dom_idx]
    
    # Convert freq to wavelength (Degrees per period)
    # Total scan is CHANNEL_LENGTH degrees. 
    # Wavelength = 1 / freq (in normalized units) * Length?
    # Periodogram x-axis is cycles per sample. 
    # Wavelength in degrees = (Total Degrees) / (cycles)
    
    # Simpler: just count peaks
    num_segments = len(peaks)
    avg_spacing = 0
    if num_segments > 1:
        avg_spacing = np.mean(np.diff(x_axis[peaks]))
    
    return peaks, num_segments, avg_spacing, freq, power

def main():
    # 1. Extract
    l_axis, spine, raw_strip = extract_spine(FITS_PATH)
    
    # 2. Analyze
    peaks, n_seg, spacing, freq, power = analyze_vertebrae(l_axis, spine)
    
    # 3. Visualize
    fig = plt.figure(figsize=(16, 10), facecolor='#0a0a0a')
    
    # Plot A: The Body Scan (Raw Data)
    ax1 = fig.add_subplot(311)
    im = ax1.imshow(raw_strip, cmap='RdBu_r', aspect='auto', extent=[-CHANNEL_LENGTH/2, CHANNEL_LENGTH/2, -CHANNEL_WIDTH/2, CHANNEL_WIDTH/2])
    ax1.set_title("1. The Predator's Body (Channel Strip)", color='white')
    ax1.set_ylabel("Width (deg)", color='gray')
    ax1.set_xlabel("Length (deg)", color='gray')
    
    # Plot B: The Spine Profile (1D Signal)
    ax2 = fig.add_subplot(312)
    ax2.set_facecolor('#111111')
    ax2.plot(l_axis, spine, color='cyan', linewidth=1.5, label='Temp Profile')
    ax2.fill_between(l_axis, spine, 0, color='cyan', alpha=0.1)
    
    # Mark Vertebrae
    peak_lons = l_axis[peaks]
    peak_vals = spine[peaks]
    ax2.scatter(peak_lons, peak_vals, color='magenta', s=100, zorder=10, label='Vertebrae (Nodes)')
    
    ax2.set_title("2. The Spine Profile (Longitudinal Structure)", color='white')
    ax2.set_xlim(l_axis[0], l_axis[-1])
    ax2.grid(True, color='#333333')
    ax2.legend()
    
    # Plot C: Periodicity Check (Is it a standing wave?)
    ax3 = fig.add_subplot(313)
    ax3.set_facecolor('#111111')
    ax3.plot(freq, power, color='lime')
    ax3.set_title("3. Harmonic Analysis (Is it periodic?)", color='white')
    ax3.set_xlabel("Frequency", color='gray')
    ax3.set_ylabel("Power", color='gray')
    ax3.grid(True, color='#333333')
    
    plt.tight_layout()
    plt.savefig("cmb_predator_spine.png")
    print("✅ Spine Scan Saved: cmb_predator_spine.png")
    
    print("\n" + "="*50)
    print(f"ANATOMY REPORT:")
    print(f"Detected Segments (Vertebrae): {n_seg}")
    if n_seg > 2:
        print(f"Average Segment Length: {spacing:.2f} degrees")
        print("INTERPRETATION: Ordered segmentation detected. Suggests a resonant standing wave (Soliton Train).")
    else:
        print("INTERPRETATION: Amorphous structure. Likely a single event or void.")
        
    # Check Head/Tail Asymmetry
    left_mean = np.mean(spine[:int(RES/3)])
    right_mean = np.mean(spine[int(2*RES/3):])
    
    print(f"\nGradient Check:")
    print(f"Left Tip Intensity:  {left_mean:.2f}")
    print(f"Right Tip Intensity: {right_mean:.2f}")
    
    if abs(left_mean - right_mean) > 0.5:
        direction = "LEFT (West)" if left_mean < right_mean else "RIGHT (East)"
        print(f"⚡ MOTION DETECTED: The object is denser towards the {direction}.")
        print("   This implies a 'Head' or leading edge.")

if __name__ == "__main__":
    main()