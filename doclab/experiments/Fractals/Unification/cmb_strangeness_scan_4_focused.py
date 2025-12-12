"""
COSMIC CORE RESONANCE FINDER
Fast version - targets the pulsing behavior you observed
Runtime goal: < 30 minutes
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
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
LMAX = 40              # Reduced from 50
N_RES = 200            # Reduced from 256
N_FRAMES = 60          # Reduced from 120
CORE_RADIUS_DEG = 40   # Larger to capture the pulsing region

# From your run: Mathematical Center
CENTER_L = -30.35  # degrees
CENTER_B = 13.06   # degrees

# Finer twist range to capture the resonance
K_RANGE = np.linspace(0.99998, 1.00002, N_FRAMES)

print("=" * 70)
print("COSMIC CORE RESONANCE FINDER")
print("=" * 70)
print(f"Target: l={CENTER_L:.2f}°, b={CENTER_B:.2f}°")
print(f"Core radius: {CORE_RADIUS_DEG}°")
print(f"Resolution: {N_RES}x{N_RES}, Lmax={LMAX}")
print(f"Frames: {N_FRAMES}")
print("=" * 70)

# ======================
# 1. LOAD & PRE-COMPUTE
# ======================

def load_alms_fast(fits_path, lmax):
    """Load CMB and compute a_lm coefficients - ONCE"""
    print(f"\n[1/5] Loading CMB from {fits_path}...")
    
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
    
    print(f"[1/5] Computing a_lm coefficients (lmax={lmax})...")
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
            print(f"    Progress: l={l+1}/{lmax+1}")
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    
    return alms

def create_core_grid(center_l, center_b, radius_deg, n_res):
    """
    Create a focused grid around the core region ONLY.
    This is the key optimization - we don't synthesize the whole sky.
    """
    print(f"\n[2/5] Creating focused core grid ({n_res}x{n_res})...")
    
    # Convert center to spherical coords
    center_theta = np.deg2rad(90 - center_b)
    center_phi = np.deg2rad(center_l)
    
    # Create local tangent plane coordinates
    # x, y in degrees from center
    radius_rad = np.deg2rad(radius_deg)
    x = np.linspace(-radius_deg, radius_deg, n_res)
    y = np.linspace(-radius_deg, radius_deg, n_res)
    X, Y = np.meshgrid(x, y, indexing='ij')
    
    # Convert to angular distance
    R = np.sqrt(X**2 + Y**2)
    
    # Mask points outside radius
    mask = R <= radius_deg
    
    # Convert to spherical coordinates on the full sky
    # Using gnomonic projection for small regions
    R_rad = np.deg2rad(R)
    azimuth = np.arctan2(X, Y)
    
    # Rotate from local frame to galactic frame
    # This is approximate but fast for small regions
    TH = np.clip(center_theta + R_rad * np.cos(azimuth), 0, np.pi)
    PH = center_phi + R_rad * np.sin(azimuth) / np.sin(center_theta)
    PH = (PH + np.pi) % (2*np.pi) - np.pi
    
    return TH, PH, mask, X, Y

def precompute_ylm_cache(lmax, TH, PH):
    """Pre-compute all Y_lm on the core grid - ONCE"""
    print(f"\n[3/5] Pre-computing Y_lm cache for core region...")
    
    ylm_cache = {}
    total = (lmax + 1) * (lmax + 2) // 2
    count = 0
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            ylm_cache[(l, m)] = sph_harm(m, l, PH, TH)
            count += 1
            if count % 100 == 0:
                print(f"    Progress: {count}/{total*2} harmonics")
    
    return ylm_cache

# ======================
# 2. FAST SYNTHESIS
# ======================

def synthesize_core_fast(alms, ylm_cache, TH, PH, k_twist):
    """
    Fast synthesis using pre-computed Y_lm.
    This is the function called N_FRAMES times.
    """
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
# 3. ANALYZE RESONANCE
# ======================

def analyze_core_resonance(alms, ylm_cache, TH, PH, mask, k_range):
    """
    Compute the time evolution and find the resonant frequency
    """
    print(f"\n[4/5] Computing temporal evolution ({len(k_range)} steps)...")
    
    n_steps = len(k_range)
    
    # Store only aggregate statistics (not full fields)
    core_mean = np.zeros(n_steps)
    core_std = np.zeros(n_steps)
    core_energy = np.zeros(n_steps)
    
    # Store one reference field for differential analysis
    field_ref = None
    
    for i, k in enumerate(k_range):
        if (i + 1) % 10 == 0:
            print(f"    Step {i+1}/{n_steps}")
        
        field = synthesize_core_fast(alms, ylm_cache, TH, PH, k)
        
        if i == n_steps // 2:  # Middle frame as reference
            field_ref = field.copy()
        
        # Compute statistics only in the core
        core_field = field[mask]
        
        core_mean[i] = np.mean(core_field)
        core_std[i] = np.std(core_field)
        core_energy[i] = np.sum(core_field**2)
    
    # Compute differential signal
    print(f"\n[5/5] Analyzing resonance structure...")
    
    # Find dominant frequency in the pulsing
    # Detrend
    core_energy_detrend = core_energy - np.mean(core_energy)
    
    # Power spectrum
    freqs, power = welch(core_energy_detrend, fs=1.0/(k_range[1]-k_range[0]), 
                         nperseg=min(32, len(k_range)//2))
    
    # Find peak
    peak_idx = np.argmax(power[1:]) + 1  # Skip DC
    peak_freq = freqs[peak_idx]
    
    print(f"\n✓ Resonance Analysis Complete:")
    print(f"  Dominant frequency: {peak_freq:.6f} cycles/k")
    print(f"  Period: {1/peak_freq:.6f} k-units")
    print(f"  Mean temperature: {np.mean(core_mean):.2f} μK")
    print(f"  Temperature variation: {np.std(core_mean):.2f} μK")
    
    return core_mean, core_std, core_energy, field_ref, freqs, power, peak_freq

# ======================
# 4. VISUALIZATION
# ======================

def create_resonance_visualization(alms, ylm_cache, TH, PH, X, Y, mask, k_range,
                                   core_mean, core_energy, field_ref, freqs, power, peak_freq):
    """
    Create visualization showing:
    1. The core region with differential changes
    2. Time series of energy
    3. Power spectrum showing resonance
    """
    print(f"\n[*] Creating visualization...")
    
    fig = plt.figure(figsize=(16, 10), facecolor='#000000')
    gs = fig.add_gridspec(2, 2, height_ratios=[2, 1], wspace=0.3, hspace=0.3)
    
    # 1. Core differential map
    ax_core = fig.add_subplot(gs[0, :])
    ax_core.set_facecolor('#000000')
    
    # 2. Energy time series
    ax_energy = fig.add_subplot(gs[1, 0])
    ax_energy.set_facecolor('#0a0a0a')
    
    # 3. Power spectrum
    ax_spectrum = fig.add_subplot(gs[1, 1])
    ax_spectrum.set_facecolor('#0a0a0a')
    
    # Plot power spectrum (static)
    ax_spectrum.semilogy(freqs, power, color='cyan', linewidth=2)
    ax_spectrum.axvline(peak_freq, color='red', linestyle='--', linewidth=2, 
                       label=f'Peak: {peak_freq:.4f} cycles/k')
    ax_spectrum.set_title("RESONANCE SPECTRUM", color='white', fontsize=12)
    ax_spectrum.set_xlabel("Frequency (cycles/k)", color='gray')
    ax_spectrum.set_ylabel("Power", color='gray')
    ax_spectrum.legend(loc='upper right')
    ax_spectrum.tick_params(colors='gray')
    ax_spectrum.grid(color='#333', linestyle=':', alpha=0.3)
    
    # Initialize core and energy plots
    extent = [-CORE_RADIUS_DEG, CORE_RADIUS_DEG, -CORE_RADIUS_DEG, CORE_RADIUS_DEG]
    
    field_0 = synthesize_core_fast(alms, ylm_cache, TH, PH, k_range[0])
    diff_0 = np.abs(field_0 - field_ref)
    diff_0[~mask] = np.nan
    
    im_core = ax_core.imshow(diff_0, extent=extent, origin='lower', 
                             cmap='inferno', aspect='auto')
    ax_core.plot(0, 0, 'r+', markersize=20, markeredgewidth=3)
    ax_core.set_title(f"CORE RESONANCE | k={k_range[0]:.6f}", 
                     color='white', fontsize=16, pad=20)
    ax_core.set_xlabel("Degrees from Center (longitude)", color='gray')
    ax_core.set_ylabel("Degrees from Center (latitude)", color='gray')
    ax_core.tick_params(colors='gray')
    
    line_energy, = ax_energy.plot([], [], color='#ff4444', linewidth=2)
    ax_energy.set_xlim(0, len(k_range))
    ax_energy.set_ylim(core_energy.min()*0.95, core_energy.max()*1.05)
    ax_energy.set_title("CORE ENERGY EVOLUTION", color='white', fontsize=12)
    ax_energy.set_xlabel("Time Step", color='gray')
    ax_energy.set_ylabel("Total Energy", color='gray')
    ax_energy.tick_params(colors='gray')
    ax_energy.grid(color='#333', linestyle=':', alpha=0.3)
    
    time_steps = np.arange(len(k_range))
    
    def init():
        line_energy.set_data([], [])
        return line_energy, im_core
    
    def animate(frame):
        # Synthesize current frame
        k = k_range[frame]
        field = synthesize_core_fast(alms, ylm_cache, TH, PH, k)
        
        # Compute difference from reference
        diff = np.abs(field - field_ref)
        diff[~mask] = np.nan
        
        # Update core view
        im_core.set_data(diff)
        ax_core.set_title(f"CORE RESONANCE | k={k:.6f} | Frame {frame+1}/{N_FRAMES}", 
                         color='white', fontsize=16, pad=20)
        
        # Update energy plot
        line_energy.set_data(time_steps[:frame+1], core_energy[:frame+1])
        
        return line_energy, im_core
    
    anim = FuncAnimation(fig, animate, init_func=init, frames=N_FRAMES,
                        interval=50, blit=True, repeat=True)
    
    return fig, anim

# ======================
# 5. MAIN
# ======================

def main():
    # Load and pre-compute
    alms = load_alms_fast(FITS_PATH, LMAX)
    TH, PH, mask, X, Y = create_core_grid(CENTER_L, CENTER_B, CORE_RADIUS_DEG, N_RES)
    ylm_cache = precompute_ylm_cache(LMAX, TH, PH)
    
    # Analyze
    core_mean, core_std, core_energy, field_ref, freqs, power, peak_freq = \
        analyze_core_resonance(alms, ylm_cache, TH, PH, mask, K_RANGE)
    
    # Visualize
    fig, anim = create_resonance_visualization(
        alms, ylm_cache, TH, PH, X, Y, mask, K_RANGE,
        core_mean, core_energy, field_ref, freqs, power, peak_freq
    )
    
    # Save
    output_file = "cosmic_core_resonance.gif"
    print(f"\n[*] Saving animation to {output_file}...")
    writer = PillowWriter(fps=20)
    anim.save(output_file, writer=writer, dpi=100)
    
    print(f"\n✓ Complete! Saved: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()