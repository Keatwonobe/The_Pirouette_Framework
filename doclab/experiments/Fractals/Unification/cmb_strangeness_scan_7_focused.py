"""
COSMIC STRANGENESS SCANNER
Detect regions with anomalous temporal behavior:
- Blueshift (moving toward us in time)
- Phase inversions (π out of phase)
- Helicity reversals (opposite winding)
- Temporal discontinuities
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import gaussian_filter
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Focus on the anomalous region we found
CENTER_L = -45.0  # Near Layer 1 center
CENTER_B = 35.0
RADIUS = 25  # degrees

LMAX = 40
N_RES = 200

# Temporal scan
K_RANGE = np.linspace(0.9999980, 1.0000020, 80)

print("=" * 70)
print("COSMIC STRANGENESS SCANNER")
print("=" * 70)
print(f"Target: l={CENTER_L:.2f}°, b={CENTER_B:.2f}°")
print(f"Looking for: blueshifts, phase inversions, helicity reversals")
print("=" * 70)

# ======================
# LOAD DATA
# ======================

def load_alms_fast(fits_path, lmax):
    """Load CMB and compute a_lm"""
    print(f"\n[1/5] Loading CMB...")
    
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
    
    print(f"[1/5] Computing a_lm (lmax={lmax})...")
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

def create_grid(center_l, center_b, radius_deg, n_res):
    """Create grid"""
    print(f"\n[2/5] Creating grid...")
    
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
    print(f"\n[3/5] Pre-computing Y_lm cache...")
    ylm_cache = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            ylm_cache[(l, m)] = sph_harm(m, l, PH, TH)
    return ylm_cache

def synthesize_field(alms, ylm_cache, TH, PH, k_twist, lmax):
    """Synthesize field"""
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
    
    return field

# ======================
# STRANGENESS DETECTORS
# ======================

def compute_temporal_evolution(alms, ylm_cache, TH, PH, mask, k_range, lmax):
    """Compute full temporal evolution"""
    print(f"\n[4/5] Computing temporal evolution ({len(k_range)} frames)...")
    
    n_steps = len(k_range)
    fields_real = []
    fields_complex = []
    
    for i, k in enumerate(k_range):
        if (i + 1) % 20 == 0:
            print(f"    Frame {i+1}/{n_steps}")
        
        field_complex = synthesize_field(alms, ylm_cache, TH, PH, k, lmax)
        fields_complex.append(field_complex)
        fields_real.append(field_complex.real)
    
    fields_real = np.array(fields_real)
    fields_complex = np.array(fields_complex)
    
    return fields_real, fields_complex

def detect_strangeness(fields_real, fields_complex, mask, k_range):
    """
    Detect anomalous behavior:
    1. Blueshift: dT/dk < 0 (getting hotter as k increases, backward in time)
    2. Phase inversion: phase flips by π
    3. Helicity reversal: sign change in phase gradient
    4. Temporal discontinuity: sudden jumps
    """
    print(f"\n[5/5] Detecting strangeness...")
    
    n_steps = len(fields_real)
    n_res = fields_real.shape[1]
    
    # 1. BLUESHIFT DETECTOR
    # Compute dT/dk at each point
    dt_dk = np.gradient(fields_real, axis=0) / (k_range[1] - k_range[0])
    
    # Average over time
    blueshift_map = np.mean(dt_dk, axis=0)
    blueshift_map[~mask] = np.nan
    
    # Negative means getting hotter (blueshift)
    blueshift_strength = -blueshift_map
    blueshift_strength[blueshift_strength < 0] = 0
    
    # 2. PHASE INVERSION DETECTOR
    # Phase of complex field
    phase = np.angle(fields_complex)
    
    # Look for sudden π flips
    phase_diff = np.diff(phase, axis=0)
    phase_diff = np.abs(phase_diff)
    
    # Count number of large jumps (near π)
    phase_inversions = np.sum(phase_diff > 2.5, axis=0)  # Threshold near π
    phase_inversions = phase_inversions.astype(float)
    phase_inversions[~mask] = np.nan
    
    # 3. HELICITY REVERSAL DETECTOR
    # Helicity = sign of ∂phase/∂phi
    # Compute spatial phase gradient
    phase_avg = np.mean(phase, axis=0)
    gy, gx = np.gradient(phase_avg)
    
    # Helicity field (simplified: magnitude of phase gradient)
    helicity = np.sqrt(gx**2 + gy**2)
    helicity[~mask] = np.nan
    
    # Look for sign changes in temporal evolution
    temporal_phase_grad = np.gradient(phase, axis=0)
    helicity_flips = np.sum(np.diff(np.sign(temporal_phase_grad), axis=0) != 0, axis=0)
    helicity_flips = helicity_flips.astype(float)
    helicity_flips[~mask] = np.nan
    
    # 4. TEMPORAL DISCONTINUITY DETECTOR
    # Variance of temporal derivative
    temporal_variance = np.var(dt_dk, axis=0)
    temporal_variance[~mask] = np.nan
    
    # Statistics
    n_blueshift_pixels = np.sum(blueshift_strength[mask] > 0)
    n_inversion_pixels = np.sum(phase_inversions[mask] > 2)
    n_helicity_pixels = np.sum(helicity_flips[mask] > 5)
    total_pixels = np.sum(mask)
    
    print(f"\n✓ Strangeness Analysis:")
    print(f"  Blueshift regions: {n_blueshift_pixels}/{total_pixels} pixels ({100*n_blueshift_pixels/total_pixels:.1f}%)")
    print(f"  Phase inversions: {n_inversion_pixels}/{total_pixels} pixels ({100*n_inversion_pixels/total_pixels:.1f}%)")
    print(f"  Helicity reversals: {n_helicity_pixels}/{total_pixels} pixels ({100*n_helicity_pixels/total_pixels:.1f}%)")
    
    # Identify "strange regions" (any two anomalies present)
    strange_mask = np.zeros_like(blueshift_strength, dtype=bool)
    strange_mask[mask] = (
        ((blueshift_strength[mask] > np.nanpercentile(blueshift_strength[mask], 75)) +
         (phase_inversions[mask] > 2) +
         (helicity_flips[mask] > 5)) >= 2
    )
    
    n_strange = np.sum(strange_mask)
    print(f"  Strange regions (2+ anomalies): {n_strange}/{total_pixels} pixels ({100*n_strange/total_pixels:.1f}%)")
    
    return blueshift_strength, phase_inversions, helicity_flips, temporal_variance, strange_mask

# ======================
# VISUALIZATION
# ======================

def create_strangeness_visualization(fields_real, fields_complex, mask, X, Y, k_range,
                                    blueshift, inversions, helicity_flips, strange_mask):
    """
    Create visualization showing:
    1. Field evolution with strange regions highlighted
    2. Strangeness maps
    """
    print(f"\n[*] Creating visualization...")
    
    fig = plt.figure(figsize=(16, 12), facecolor='#000000')
    gs = fig.add_gridspec(3, 2, height_ratios=[2, 1, 1], wspace=0.3, hspace=0.4)
    
    # Main: Field with strange regions
    ax_main = fig.add_subplot(gs[0, :])
    ax_main.set_facecolor('#000000')
    
    # Strangeness maps
    ax_blue = fig.add_subplot(gs[1, 0])
    ax_blue.set_facecolor('#0a0a0a')
    
    ax_inversion = fig.add_subplot(gs[1, 1])
    ax_inversion.set_facecolor('#0a0a0a')
    
    ax_helicity = fig.add_subplot(gs[2, 0])
    ax_helicity.set_facecolor('#0a0a0a')
    
    ax_strange = fig.add_subplot(gs[2, 1])
    ax_strange.set_facecolor('#0a0a0a')
    
    extent = [-RADIUS, RADIUS, -RADIUS, RADIUS]
    
    # Static maps
    blue_plot = blueshift.copy()
    blue_plot[~mask] = np.nan
    im_blue = ax_blue.imshow(blue_plot, extent=extent, origin='lower', cmap='hot', aspect='auto')
    ax_blue.plot(0, 0, 'c+', markersize=10, markeredgewidth=1.5)
    ax_blue.set_title("BLUESHIFT STRENGTH", color='white', fontsize=10)
    ax_blue.tick_params(colors='gray', labelsize=8)
    
    inv_plot = inversions.copy()
    inv_plot[~mask] = np.nan
    im_inv = ax_inversion.imshow(inv_plot, extent=extent, origin='lower', cmap='plasma', aspect='auto')
    ax_inversion.plot(0, 0, 'c+', markersize=10, markeredgewidth=1.5)
    ax_inversion.set_title("PHASE INVERSIONS", color='white', fontsize=10)
    ax_inversion.tick_params(colors='gray', labelsize=8)
    
    hel_plot = helicity_flips.copy()
    hel_plot[~mask] = np.nan
    im_hel = ax_helicity.imshow(hel_plot, extent=extent, origin='lower', cmap='viridis', aspect='auto')
    ax_helicity.plot(0, 0, 'c+', markersize=10, markeredgewidth=1.5)
    ax_helicity.set_title("HELICITY REVERSALS", color='white', fontsize=10)
    ax_helicity.tick_params(colors='gray', labelsize=8)
    
    strange_plot = strange_mask.astype(float)
    strange_plot[~mask] = np.nan
    im_strange = ax_strange.imshow(strange_plot, extent=extent, origin='lower', cmap='Reds', aspect='auto', vmin=0, vmax=1)
    ax_strange.plot(0, 0, 'c+', markersize=10, markeredgewidth=1.5)
    ax_strange.set_title("STRANGE REGIONS (2+ anomalies)", color='white', fontsize=10)
    ax_strange.tick_params(colors='gray', labelsize=8)
    
    # Main plot initialization
    ref_field = fields_real[len(fields_real)//2]
    diff_0 = fields_real[0] - ref_field
    diff_0[~mask] = np.nan
    
    # Use diverging colormap centered at zero
    vmax = np.nanmax(np.abs(diff_0))
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    
    im_main = ax_main.imshow(diff_0, extent=extent, origin='lower', 
                             cmap='RdBu_r', norm=norm, aspect='auto')
    
    # Overlay strange regions
    strange_contour = ax_main.contour(X, Y, strange_mask, levels=[0.5], 
                                      colors='yellow', linewidths=2, alpha=0.8)
    
    ax_main.plot(0, 0, 'r+', markersize=20, markeredgewidth=3)
    ax_main.set_title(f"TEMPORAL EVOLUTION | k={k_range[0]:.7f}",
                     color='white', fontsize=14, pad=15)
    ax_main.set_xlabel("Degrees from Center (longitude)", color='gray')
    ax_main.set_ylabel("Degrees from Center (latitude)", color='gray')
    ax_main.tick_params(colors='gray')
    
    def init():
        return im_main,
    
    def animate(frame):
        k = k_range[frame]
        
        diff = fields_real[frame] - ref_field
        diff[~mask] = np.nan
        
        im_main.set_data(diff)
        ax_main.set_title(f"TEMPORAL EVOLUTION | k={k:.7f} | Frame {frame+1}/{len(k_range)}",
                         color='white', fontsize=14, pad=15)
        
        return im_main,
    
    anim = FuncAnimation(fig, animate, init_func=init, frames=len(k_range),
                        interval=50, blit=True, repeat=True)
    
    return fig, anim

# ======================
# MAIN
# ======================

def main():
    # Load
    alms = load_alms_fast(FITS_PATH, LMAX)
    TH, PH, mask, X, Y = create_grid(CENTER_L, CENTER_B, RADIUS, N_RES)
    ylm_cache = precompute_ylm_cache(LMAX, TH, PH)
    
    # Evolve
    fields_real, fields_complex = compute_temporal_evolution(
        alms, ylm_cache, TH, PH, mask, K_RANGE, LMAX
    )
    
    # Detect
    blueshift, inversions, helicity_flips, temp_var, strange_mask = detect_strangeness(
        fields_real, fields_complex, mask, K_RANGE
    )
    
    # Visualize
    fig, anim = create_strangeness_visualization(
        fields_real, fields_complex, mask, X, Y, K_RANGE,
        blueshift, inversions, helicity_flips, strange_mask
    )
    
    # Save
    output_file = "cosmic_strangeness_scan.gif"
    print(f"\n[*] Saving to {output_file}...")
    writer = PillowWriter(fps=20)
    anim.save(output_file, writer=writer, dpi=100)
    
    print(f"\n✓ Complete! Saved: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()