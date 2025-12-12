"""
NESTED MANIFOLD DETECTOR
Recursive zoom into the core to find fractal structure layers
Each layer should oscillate faster than its parent
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import gaussian_filter
from scipy.signal import welch
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Layer 0: The core we found
CENTER_L_0 = -30.35
CENTER_B_0 = 13.06
RADIUS_0 = 40  # degrees

# Layer 1: Zoom into hottest region (from your gif, around 10-20° east, 10° south of center)
# We'll compute this automatically
CENTER_L_1 = None  # To be computed
CENTER_B_1 = None
RADIUS_1 = 15  # degrees (smaller zoom)

# Layer 2: The core within the core
RADIUS_2 = 5  # degrees (even smaller)

# Resolution
LMAX = 45  # Higher for finer detail
N_RES = 180  # Balanced for speed

# Temporal parameters for EACH layer
# Layer 0: Normal scan
K_RANGE_0 = np.linspace(0.9999990, 1.0000010, 60)
# Layer 1: 3x faster oscillation (tighter wound)
K_RANGE_1 = np.linspace(0.9999970, 1.0000030, 60)
# Layer 2: 9x faster oscillation (even tighter)
K_RANGE_2 = np.linspace(0.9999910, 1.0000090, 60)

print("=" * 70)
print("NESTED MANIFOLD DETECTOR")
print("=" * 70)
print("Searching for fractal structure hierarchy...")
print("=" * 70)

# ======================
# CORE FUNCTIONS (same as before)
# ======================

def load_alms_fast(fits_path, lmax):
    """Load CMB and compute a_lm coefficients"""
    print(f"\n[*] Loading CMB from {fits_path}...")
    
    try:
        data = fits.getdata(fits_path)
        if "I" in data.dtype.names: 
            cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names: 
            cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else: 
            cmb = data.astype(np.float64)
        cmb[np.isnan(cmb)] = np.nanmean(cmb)
    except FileNotFoundError:
        print(f"ERROR: {fits_path} not found")
        sys.exit(1)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    print(f"[*] Computing a_lm (lmax={lmax})...")
    n_theta_alm = lmax * 3
    n_phi_alm = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta_alm)
    p_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')
    
    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    alms = {}
    for l in range(lmax + 1):
        if (l+1) % 10 == 0:
            print(f"    l={l+1}/{lmax+1}")
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    
    return alms

def create_core_grid(center_l, center_b, radius_deg, n_res):
    """Create focused grid"""
    center_theta = np.deg2rad(90 - center_b)
    center_phi = np.deg2rad(center_l)
    
    x = np.linspace(-radius_deg, radius_deg, n_res)
    y = np.linspace(-radius_deg, radius_deg, n_res)
    X, Y = np.meshgrid(x, y, indexing='ij')
    R = np.sqrt(X**2 + Y**2)
    mask = R <= radius_deg
    
    R_rad = np.deg2rad(R)
    azimuth = np.arctan2(X, Y)
    
    TH = np.clip(center_theta + R_rad * np.cos(azimuth), 0, np.pi)
    PH = center_phi + R_rad * np.sin(azimuth) / np.sin(center_theta)
    PH = (PH + np.pi) % (2*np.pi) - np.pi
    
    return TH, PH, mask, X, Y

def precompute_ylm_cache(lmax, TH, PH):
    """Pre-compute Y_lm"""
    ylm_cache = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            ylm_cache[(l, m)] = sph_harm(m, l, PH, TH)
    return ylm_cache

def synthesize_core_fast(alms, ylm_cache, TH, PH, k_twist, lmax):
    """Fast synthesis"""
    field = np.zeros_like(TH, dtype=np.complex128)
    delta_phi = (k_twist - 1) * PH
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms:
                continue
            
            alm = alms[(l, m)]
            Y_lm = ylm_cache[(l, m)]
            phase = np.exp(1j * m * delta_phi)
            
            field += alm * Y_lm * phase
    
    return field.real

# ======================
# LAYER ANALYZER
# ======================

def analyze_layer(alms, ylm_cache, TH, PH, mask, k_range, lmax, layer_name):
    """
    Analyze one nested layer:
    1. Compute temporal evolution
    2. Find hotspot (next layer center)
    3. Measure dominant frequency
    """
    print(f"\n[*] Analyzing {layer_name}...")
    
    n_steps = len(k_range)
    fields = []
    
    print(f"    Computing {n_steps} frames...")
    for i, k in enumerate(k_range):
        if (i + 1) % 15 == 0:
            print(f"      Frame {i+1}/{n_steps}")
        
        field = synthesize_core_fast(alms, ylm_cache, TH, PH, k, lmax)
        fields.append(field)
    
    fields = np.array(fields)
    
    # Compute statistics
    reference_field = fields[len(fields)//2]
    
    # Temporal variance (activity map)
    temporal_var = np.var(fields, axis=0)
    temporal_var[~mask] = np.nan
    
    # Find hotspot
    hotspot_idx = np.unravel_index(np.nanargmax(temporal_var), temporal_var.shape)
    
    # Spatial structure
    spatial_structure = np.zeros_like(fields)
    for i in range(n_steps):
        gy, gx = np.gradient(fields[i])
        spatial_structure[i] = np.sqrt(gx**2 + gy**2)
    
    avg_structure = np.mean(spatial_structure, axis=0)
    avg_structure[~mask] = np.nan
    
    # Measure frequency at hotspot
    hotspot_signal = fields[:, hotspot_idx[0], hotspot_idx[1]]
    hotspot_signal = hotspot_signal - np.mean(hotspot_signal)
    
    dk = k_range[1] - k_range[0]
    freqs, power = welch(hotspot_signal, fs=1.0/dk, nperseg=min(32, n_steps//2))
    
    if len(freqs) > 1:
        peak_idx = np.argmax(power[1:]) + 1
        dominant_freq = freqs[peak_idx]
    else:
        dominant_freq = 0
    
    print(f"    ✓ Hotspot at pixel ({hotspot_idx[0]}, {hotspot_idx[1]})")
    print(f"    ✓ Dominant frequency: {dominant_freq:.2f} cycles/k")
    print(f"    ✓ Temporal variance range: {np.nanmin(temporal_var):.2e} to {np.nanmax(temporal_var):.2e}")
    
    return fields, reference_field, temporal_var, avg_structure, hotspot_idx, dominant_freq

# ======================
# RECURSIVE DETECTOR
# ======================

def detect_nested_structure():
    """
    Recursively zoom into nested layers
    """
    global CENTER_L_1, CENTER_B_1
    
    # Load once
    print("\n" + "=" * 70)
    print("PHASE 1: Loading Data")
    print("=" * 70)
    alms = load_alms_fast(FITS_PATH, LMAX)
    
    # === LAYER 0: The core ===
    print("\n" + "=" * 70)
    print("PHASE 2: Layer 0 Analysis (40° region)")
    print("=" * 70)
    
    TH_0, PH_0, mask_0, X_0, Y_0 = create_core_grid(CENTER_L_0, CENTER_B_0, RADIUS_0, N_RES)
    ylm_cache_0 = precompute_ylm_cache(LMAX, TH_0, PH_0)
    
    fields_0, ref_0, var_0, struct_0, hot_0, freq_0 = analyze_layer(
        alms, ylm_cache_0, TH_0, PH_0, mask_0, K_RANGE_0, LMAX, "Layer 0 (Core)"
    )
    
    # Convert hotspot pixel to galactic coordinates
    hot_x_0 = X_0[hot_0]
    hot_y_0 = Y_0[hot_0]
    CENTER_L_1 = CENTER_L_0 + hot_x_0
    CENTER_B_1 = CENTER_B_0 + hot_y_0
    
    print(f"\n    → Layer 1 center: l={CENTER_L_1:.2f}°, b={CENTER_B_1:.2f}°")
    
    # === LAYER 1: Zoom into hotspot ===
    print("\n" + "=" * 70)
    print("PHASE 3: Layer 1 Analysis (15° region)")
    print("=" * 70)
    
    TH_1, PH_1, mask_1, X_1, Y_1 = create_core_grid(CENTER_L_1, CENTER_B_1, RADIUS_1, N_RES)
    ylm_cache_1 = precompute_ylm_cache(LMAX, TH_1, PH_1)
    
    fields_1, ref_1, var_1, struct_1, hot_1, freq_1 = analyze_layer(
        alms, ylm_cache_1, TH_1, PH_1, mask_1, K_RANGE_1, LMAX, "Layer 1 (Hotspot)"
    )
    
    # Layer 2 center
    hot_x_1 = X_1[hot_1]
    hot_y_1 = Y_1[hot_1]
    CENTER_L_2 = CENTER_L_1 + hot_x_1
    CENTER_B_2 = CENTER_B_1 + hot_y_1
    
    print(f"\n    → Layer 2 center: l={CENTER_L_2:.2f}°, b={CENTER_B_2:.2f}°")
    
    # === LAYER 2: The core within the core ===
    print("\n" + "=" * 70)
    print("PHASE 4: Layer 2 Analysis (5° region)")
    print("=" * 70)
    
    TH_2, PH_2, mask_2, X_2, Y_2 = create_core_grid(CENTER_L_2, CENTER_B_2, RADIUS_2, N_RES)
    ylm_cache_2 = precompute_ylm_cache(LMAX, TH_2, PH_2)
    
    fields_2, ref_2, var_2, struct_2, hot_2, freq_2 = analyze_layer(
        alms, ylm_cache_2, TH_2, PH_2, mask_2, K_RANGE_2, LMAX, "Layer 2 (Core Core)"
    )
    
    # === ANALYSIS ===
    print("\n" + "=" * 70)
    print("FRACTAL HIERARCHY ANALYSIS")
    print("=" * 70)
    
    freq_ratio_1_0 = freq_1 / freq_0 if freq_0 > 0 else 0
    freq_ratio_2_1 = freq_2 / freq_1 if freq_1 > 0 else 0
    
    print(f"\nLayer 0: {RADIUS_0}° radius, frequency = {freq_0:.2f} cycles/k")
    print(f"Layer 1: {RADIUS_1}° radius, frequency = {freq_1:.2f} cycles/k")
    print(f"Layer 2: {RADIUS_2}° radius, frequency = {freq_2:.2f} cycles/k")
    print(f"\nFrequency ratio Layer1/Layer0: {freq_ratio_1_0:.3f}")
    print(f"Frequency ratio Layer2/Layer1: {freq_ratio_2_1:.3f}")
    
    size_ratio_1_0 = RADIUS_1 / RADIUS_0
    size_ratio_2_1 = RADIUS_2 / RADIUS_1
    
    print(f"\nSize ratio Layer1/Layer0: {size_ratio_1_0:.3f}")
    print(f"Size ratio Layer2/Layer1: {size_ratio_2_1:.3f}")
    
    # Test for scaling relations
    phi = (1 + np.sqrt(5)) / 2
    print(f"\nTesting scaling relations:")
    print(f"  Golden ratio φ = {phi:.3f}")
    print(f"  π = {np.pi:.3f}")
    print(f"  Size ratio ≈ 1/φ? {abs(size_ratio_1_0 - 1/phi) < 0.1}")
    print(f"  Freq ratio ≈ φ? {abs(freq_ratio_1_0 - phi) < 0.5}")
    
    return (fields_0, ref_0, var_0, X_0, Y_0, mask_0,
            fields_1, ref_1, var_1, X_1, Y_1, mask_1,
            fields_2, ref_2, var_2, X_2, Y_2, mask_2,
            freq_0, freq_1, freq_2)

# ======================
# VISUALIZATION
# ======================

def create_nested_visualization(data_tuple):
    """
    Show all three layers side by side
    """
    (fields_0, ref_0, var_0, X_0, Y_0, mask_0,
     fields_1, ref_1, var_1, X_1, Y_1, mask_1,
     fields_2, ref_2, var_2, X_2, Y_2, mask_2,
     freq_0, freq_1, freq_2) = data_tuple
    
    print("\n[*] Creating nested visualization...")
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor='#000000')
    
    for ax in axes:
        ax.set_facecolor('#000000')
    
    extent_0 = [-RADIUS_0, RADIUS_0, -RADIUS_0, RADIUS_0]
    extent_1 = [-RADIUS_1, RADIUS_1, -RADIUS_1, RADIUS_1]
    extent_2 = [-RADIUS_2, RADIUS_2, -RADIUS_2, RADIUS_2]
    
    # Initialize
    diff_0 = np.abs(fields_0[0] - ref_0)
    diff_0[~mask_0] = np.nan
    
    diff_1 = np.abs(fields_1[0] - ref_1)
    diff_1[~mask_1] = np.nan
    
    diff_2 = np.abs(fields_2[0] - ref_2)
    diff_2[~mask_2] = np.nan
    
    im0 = axes[0].imshow(diff_0, extent=extent_0, origin='lower', cmap='inferno', aspect='auto')
    axes[0].plot(0, 0, 'r+', markersize=15, markeredgewidth=2)
    axes[0].set_title(f"Layer 0: {RADIUS_0}° | {freq_0:.1f} cycles/k", color='white', fontsize=12)
    axes[0].tick_params(colors='gray')
    
    im1 = axes[1].imshow(diff_1, extent=extent_1, origin='lower', cmap='inferno', aspect='auto')
    axes[1].plot(0, 0, 'r+', markersize=15, markeredgewidth=2)
    axes[1].set_title(f"Layer 1: {RADIUS_1}° | {freq_1:.1f} cycles/k", color='white', fontsize=12)
    axes[1].tick_params(colors='gray')
    
    im2 = axes[2].imshow(diff_2, extent=extent_2, origin='lower', cmap='inferno', aspect='auto')
    axes[2].plot(0, 0, 'r+', markersize=15, markeredgewidth=2)
    axes[2].set_title(f"Layer 2: {RADIUS_2}° | {freq_2:.1f} cycles/k", color='white', fontsize=12)
    axes[2].tick_params(colors='gray')
    
    plt.suptitle("NESTED MANIFOLD LAYERS", color='white', fontsize=16, y=0.98)
    
    def animate(frame):
        # Use same frame index for all (they have same length)
        diff_0 = np.abs(fields_0[frame] - ref_0)
        diff_0[~mask_0] = np.nan
        im0.set_data(diff_0)
        
        diff_1 = np.abs(fields_1[frame] - ref_1)
        diff_1[~mask_1] = np.nan
        im1.set_data(diff_1)
        
        diff_2 = np.abs(fields_2[frame] - ref_2)
        diff_2[~mask_2] = np.nan
        im2.set_data(diff_2)
        
        return im0, im1, im2
    
    anim = FuncAnimation(fig, animate, frames=60, interval=50, blit=True, repeat=True)
    
    return fig, anim

# ======================
# MAIN
# ======================

def main():
    # Detect nested structure
    data = detect_nested_structure()
    
    # Visualize
    fig, anim = create_nested_visualization(data)
    
    # Save
    output_file = "nested_manifolds.gif"
    print(f"\n[*] Saving to {output_file}...")
    writer = PillowWriter(fps=20)
    anim.save(output_file, writer=writer, dpi=100)
    
    print(f"\n✓ Complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()