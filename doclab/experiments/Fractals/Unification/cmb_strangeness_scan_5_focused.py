"""
COSMIC CORE MICRO-SCANNER
Ultra-high temporal resolution to detect nested manifold oscillations
Looking for the 24 Hz signature within the cellular structure
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LinearSegmentedColormap
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import gaussian_filter
from scipy.signal import welch, find_peaks
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Core location (from your results)
CENTER_L = -30.35
CENTER_B = 13.06
CORE_RADIUS_DEG = 40

# Resolution
LMAX = 40
N_RES = 200

# ULTRA-NARROW temporal scan (10x finer than before)
# This is key - we're zooming into the manifold boundary
K_MIN = 0.9999990
K_MAX = 1.0000010
N_FRAMES = 120  # Keep frame count reasonable for gif size

K_RANGE = np.linspace(K_MIN, K_MAX, N_FRAMES)

print("=" * 70)
print("COSMIC CORE MICRO-SCANNER")
print("=" * 70)
print(f"Target: l={CENTER_L:.2f}°, b={CENTER_B:.2f}°")
print(f"Temporal range: k={K_MIN:.7f} to {K_MAX:.7f}")
print(f"Temporal resolution: Δk={K_RANGE[1]-K_RANGE[0]:.10f}")
print(f"Frames: {N_FRAMES}")
print("=" * 70)

# ======================
# LOAD & PRE-COMPUTE
# ======================

def load_alms_fast(fits_path, lmax):
    """Load CMB and compute a_lm coefficients"""
    print(f"\n[1/6] Loading CMB from {fits_path}...")
    
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
    
    print(f"[1/6] Computing a_lm coefficients (lmax={lmax})...")
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
    """Create focused grid around core"""
    print(f"\n[2/6] Creating core grid ({n_res}x{n_res})...")
    
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
    """Pre-compute Y_lm on core grid"""
    print(f"\n[3/6] Pre-computing Y_lm cache...")
    
    ylm_cache = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            ylm_cache[(l, m)] = sph_harm(m, l, PH, TH)
    
    return ylm_cache

def synthesize_core_fast(alms, ylm_cache, TH, PH, k_twist):
    """Fast synthesis using pre-computed Y_lm"""
    field = np.zeros_like(TH, dtype=np.complex128)
    delta_phi = (k_twist - 1) * PH
    
    for l in range(LMAX + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms:
                continue
            
            alm = alms[(l, m)]
            Y_lm = ylm_cache[(l, m)]
            phase = np.exp(1j * m * delta_phi)
            
            field += alm * Y_lm * phase
    
    return field.real

# ======================
# MICRO-TEMPORAL ANALYSIS
# ======================

def compute_microtemporal_evolution(alms, ylm_cache, TH, PH, mask, k_range):
    """
    Compute full temporal evolution at high resolution.
    Store ALL fields for detailed analysis.
    """
    print(f"\n[4/6] Computing micro-temporal evolution ({len(k_range)} steps)...")
    
    n_steps = len(k_range)
    fields = []
    
    for i, k in enumerate(k_range):
        if (i + 1) % 20 == 0:
            print(f"    Step {i+1}/{n_steps}")
        
        field = synthesize_core_fast(alms, ylm_cache, TH, PH, k)
        fields.append(field)
    
    fields = np.array(fields)  # Shape: (n_steps, n_res, n_res)
    
    return fields

def analyze_cellular_structure(fields, mask, k_range):
    """
    Analyze the cellular structure:
    1. Identify cell boundaries (edges in spatial variation)
    2. Measure oscillation frequency within cells
    3. Compare to surrounding regions
    """
    print(f"\n[5/6] Analyzing cellular structure...")
    
    n_steps = len(fields)
    n_res = fields.shape[1]
    
    # Compute temporal variance at each spatial point
    temporal_variance = np.var(fields, axis=0)
    temporal_variance[~mask] = np.nan
    
    # Compute spatial structure (gradient magnitude) over time
    spatial_structure = np.zeros_like(fields)
    for i in range(n_steps):
        gy, gx = np.gradient(fields[i])
        spatial_structure[i] = np.sqrt(gx**2 + gy**2)
    
    # Average spatial structure
    avg_structure = np.mean(spatial_structure, axis=0)
    avg_structure[~mask] = np.nan
    
    # Find cell boundaries (high spatial gradient)
    boundaries = gaussian_filter(avg_structure, sigma=2)
    boundaries[~mask] = np.nan
    
    # Compute local oscillation frequency
    # For each pixel, compute power spectrum
    print("    Computing local oscillation frequencies...")
    freq_map = np.zeros((n_res, n_res))
    power_map = np.zeros((n_res, n_res))
    
    # Sample spacing in k
    dk = k_range[1] - k_range[0]
    
    # Only analyze pixels in mask (speeds things up)
    valid_pixels = np.where(mask)
    
    for idx in range(0, len(valid_pixels[0]), 10):  # Sample every 10th pixel for speed
        i = valid_pixels[0][idx]
        j = valid_pixels[1][idx]
        
        # Time series at this pixel
        time_series = fields[:, i, j]
        time_series = time_series - np.mean(time_series)  # Detrend
        
        # Power spectrum
        freqs, power = welch(time_series, fs=1.0/dk, nperseg=min(32, n_steps//2))
        
        # Find dominant frequency (skip DC)
        if len(freqs) > 1:
            peak_idx = np.argmax(power[1:]) + 1
            freq_map[i, j] = freqs[peak_idx]
            power_map[i, j] = power[peak_idx]
    
    freq_map[~mask] = np.nan
    power_map[~mask] = np.nan
    
    # Overall statistics
    core_fields = fields[:, mask]
    global_variance = np.var(core_fields)
    
    print(f"\n✓ Cellular Analysis Complete:")
    print(f"  Global temporal variance: {global_variance:.2e}")
    print(f"  Mean boundary strength: {np.nanmean(boundaries):.2e}")
    print(f"  Frequency range: {np.nanmin(freq_map):.1f} to {np.nanmax(freq_map):.1f} cycles/k")
    
    return temporal_variance, boundaries, freq_map, power_map

# ======================
# VISUALIZATION
# ======================

def create_micro_visualization(fields, mask, X, Y, k_range,
                               temporal_variance, boundaries, freq_map):
    """
    Create animation showing:
    1. Differential field evolution (main)
    2. Cell boundaries overlay
    3. Frequency map (static reference)
    """
    print(f"\n[6/6] Creating visualization...")
    
    fig = plt.figure(figsize=(16, 10), facecolor='#000000')
    gs = fig.add_gridspec(2, 2, height_ratios=[2, 1], wspace=0.3, hspace=0.3)
    
    # Main: Differential evolution
    ax_main = fig.add_subplot(gs[0, :])
    ax_main.set_facecolor('#000000')
    
    # Bottom left: Cell boundary map
    ax_boundaries = fig.add_subplot(gs[1, 0])
    ax_boundaries.set_facecolor('#0a0a0a')
    
    # Bottom right: Frequency map
    ax_freq = fig.add_subplot(gs[1, 1])
    ax_freq.set_facecolor('#0a0a0a')
    
    extent = [-CORE_RADIUS_DEG, CORE_RADIUS_DEG, -CORE_RADIUS_DEG, CORE_RADIUS_DEG]
    
    # Plot static references
    # Boundaries
    bounds_plot = boundaries.copy()
    bounds_plot[~mask] = np.nan
    im_bounds = ax_boundaries.imshow(bounds_plot, extent=extent, origin='lower',
                                     cmap='hot', aspect='auto')
    ax_boundaries.plot(0, 0, 'c+', markersize=15, markeredgewidth=2)
    ax_boundaries.set_title("CELL BOUNDARIES", color='white', fontsize=10)
    ax_boundaries.set_xlabel("Degrees from Center", color='gray', fontsize=8)
    ax_boundaries.tick_params(colors='gray', labelsize=8)
    
    # Frequency map
    freq_plot = freq_map.copy()
    freq_plot[~mask] = np.nan
    im_freq = ax_freq.imshow(freq_plot, extent=extent, origin='lower',
                             cmap='viridis', aspect='auto')
    ax_freq.plot(0, 0, 'c+', markersize=15, markeredgewidth=2)
    ax_freq.set_title("LOCAL OSCILLATION FREQUENCY", color='white', fontsize=10)
    ax_freq.set_xlabel("Degrees from Center", color='gray', fontsize=8)
    ax_freq.tick_params(colors='gray', labelsize=8)
    plt.colorbar(im_freq, ax=ax_freq, label='cycles/k')
    
    # Initialize main plot
    reference_field = fields[len(fields)//2]  # Middle frame as reference
    diff_0 = np.abs(fields[0] - reference_field)
    diff_0[~mask] = np.nan
    
    im_main = ax_main.imshow(diff_0, extent=extent, origin='lower',
                            cmap='inferno', aspect='auto')
    ax_main.plot(0, 0, 'r+', markersize=20, markeredgewidth=3)
    
    # Overlay cell boundaries
    boundary_contour = ax_main.contour(X, Y, boundaries, levels=5, 
                                       colors='cyan', linewidths=0.5, alpha=0.3)
    
    ax_main.set_title(f"MICRO-TEMPORAL EVOLUTION | k={k_range[0]:.7f}",
                     color='white', fontsize=16, pad=20)
    ax_main.set_xlabel("Degrees from Center (longitude)", color='gray')
    ax_main.set_ylabel("Degrees from Center (latitude)", color='gray')
    ax_main.tick_params(colors='gray')
    
    def init():
        return im_main,
    
    def animate(frame):
        k = k_range[frame]
        
        # Compute differential
        diff = np.abs(fields[frame] - reference_field)
        diff[~mask] = np.nan
        
        # Update
        im_main.set_data(diff)
        ax_main.set_title(f"MICRO-TEMPORAL EVOLUTION | k={k:.7f} | Frame {frame+1}/{N_FRAMES}",
                         color='white', fontsize=16, pad=20)
        
        return im_main,
    
    anim = FuncAnimation(fig, animate, init_func=init, frames=N_FRAMES,
                        interval=50, blit=True, repeat=True)
    
    return fig, anim

# ======================
# MAIN
# ======================

def main():
    # Load
    alms = load_alms_fast(FITS_PATH, LMAX)
    TH, PH, mask, X, Y = create_core_grid(CENTER_L, CENTER_B, CORE_RADIUS_DEG, N_RES)
    ylm_cache = precompute_ylm_cache(LMAX, TH, PH)
    
    # Compute
    fields = compute_microtemporal_evolution(alms, ylm_cache, TH, PH, mask, K_RANGE)
    
    # Analyze
    temporal_var, boundaries, freq_map, power_map = analyze_cellular_structure(fields, mask, K_RANGE)
    
    # Visualize
    fig, anim = create_micro_visualization(fields, mask, X, Y, K_RANGE,
                                           temporal_var, boundaries, freq_map)
    
    # Save
    output_file = "cosmic_core_microscan.gif"
    print(f"\n[*] Saving to {output_file}...")
    writer = PillowWriter(fps=20)
    anim.save(output_file, writer=writer, dpi=100)
    
    print(f"\n✓ Complete! Saved: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()