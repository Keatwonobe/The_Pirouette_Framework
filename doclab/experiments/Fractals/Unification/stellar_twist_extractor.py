import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.signal import find_peaks
import json

# ======================
# CONFIGURATION
# ======================
W_RESONANCE = 1.0047
LOCKED_TURNS = 30.00

# Full Kinematic Data (RA, Dec, Dist, pmRA, pmDec, RV)
STARS_KINEMATICS = {
    "Sirius":        (101.28, -16.71, 2.64,  -546.0,  -1223.1, -5.5),
    "Betelgeuse":    (88.79,   7.40,  168.0, 26.4,    9.6,     21.9),
    "Aldebaran":     (68.98,   16.50, 20.4,  63.5,   -188.9,   54.3),
    "Vega":          (279.23,  38.78, 7.68,  200.9,   286.2,  -13.9),
    "Rigel":         (78.63,  -8.20,  260.0, 1.31,    0.50,    17.8),
    "Alpha Centauri":(219.90, -60.83, 1.33,  -3679.3, 473.7,  -21.4),
    "Antares":       (247.35, -26.43, 170.0, -12.1,  -23.3,   -3.4),
    "Arcturus":      (213.91,  19.18, 11.26, -1093.4, -1999.4, -5.2),
    "Procyon":       (114.82,  5.22,  3.5,   -716.6,  -1034.6, -3.2),
    "Galactic Center":(266.41, -29.00, 8178, 0, 0, 0),
    "Capella":       (79.17, 45.99, 12.9, 75.5, -427.1, 30.2),
    "Pollux":        (116.32, 28.02, 10.3, -626.5, -45.8, 3.2),
    "Deneb":         (310.35, 45.28, 802.0, 1.56, 1.55, -4.5),
    "Regulus":       (152.09, 11.96, 23.8, -248.5, 6.0, 5.9),
    "Castor":        (113.65, 31.88, 15.6, -192.4, -146.7, 14.4),
    "Spica":         (201.29, -11.16, 77.0, -42.5, -31.7, 1.0)
}

# Solar motion for LSR correction
SOLAR_U = 11.1
SOLAR_V = 12.24
SOLAR_W = 7.25

# ======================
# COORDINATE TRANSFORMATIONS (replacing astropy)
# ======================

def icrs_to_galactic(ra_deg, dec_deg):
    """
    Convert ICRS (RA, Dec) to Galactic (l, b) coordinates
    Uses IAU standard transformation
    """
    # North Galactic Pole in ICRS: (192.859508, 27.128336)
    # Galactic Center in ICRS: (266.405, -28.936)
    
    ra = np.deg2rad(ra_deg)
    dec = np.deg2rad(dec_deg)
    
    # NGP coordinates
    ra_ngp = np.deg2rad(192.859508)
    dec_ngp = np.deg2rad(27.128336)
    
    # Galactic longitude of North Celestial Pole
    l_ncp = np.deg2rad(122.932)
    
    # Transformation
    sin_b = (np.sin(dec) * np.sin(dec_ngp) + 
             np.cos(dec) * np.cos(dec_ngp) * np.cos(ra - ra_ngp))
    
    b = np.arcsin(sin_b)
    
    cos_l_minus_lncp = (np.cos(dec) * np.sin(ra - ra_ngp) / np.cos(b))
    sin_l_minus_lncp = ((np.sin(dec) * np.cos(dec_ngp) - 
                         np.cos(dec) * np.sin(dec_ngp) * np.cos(ra - ra_ngp)) / np.cos(b))
    
    l = l_ncp + np.arctan2(cos_l_minus_lncp, sin_l_minus_lncp)
    
    # Convert to degrees and wrap
    l_deg = np.rad2deg(l) % 360
    b_deg = np.rad2deg(b)
    
    return l_deg, b_deg

def compute_velocity_galactic(ra_deg, dec_deg, dist_pc, pm_ra_mas, pm_dec_mas, rv_kms):
    """
    Compute U, V, W velocities in Galactic frame
    U: toward Galactic Center
    V: in direction of Galactic rotation
    W: toward North Galactic Pole
    """
    # Convert to Galactic coordinates
    l_deg, b_deg = icrs_to_galactic(ra_deg, dec_deg)
    l = np.deg2rad(l_deg)
    b = np.deg2rad(b_deg)
    
    # Convert proper motions from mas/yr to rad/yr
    pm_ra_rad = np.deg2rad(pm_ra_mas / 3600000.0)
    pm_dec_rad = np.deg2rad(pm_dec_mas / 3600000.0)
    
    # Tangential velocities in km/s (v = d * pm * 4.74)
    # Factor 4.74 converts (pc * rad/yr) to km/s
    k = 4.74047  # km/s per (pc * arcsec/yr)
    v_ra = dist_pc * pm_ra_mas * k
    v_dec = dist_pc * pm_dec_mas * k
    
    # Transform to Galactic coordinates
    # This is a simplified transformation
    ra = np.deg2rad(ra_deg)
    dec = np.deg2rad(dec_deg)
    
    # Rotation matrices (simplified)
    cos_b = np.cos(b)
    sin_b = np.sin(b)
    cos_l = np.cos(l)
    sin_l = np.sin(l)
    
    # Approximate transformation
    # (This is simplified - full transformation requires proper rotation matrices)
    u_helio = rv_kms * cos_b * cos_l - v_ra * sin_l - v_dec * sin_b * cos_l
    v_helio = rv_kms * cos_b * sin_l + v_ra * cos_l - v_dec * sin_b * sin_l
    w_helio = rv_kms * sin_b + v_dec * cos_b
    
    return l_deg, b_deg, u_helio, v_helio, w_helio

# ======================
# HELPER FUNCTIONS
# ======================

def get_galactic_kinematics(name, data):
    """
    Extract position and velocity in Galactic coordinates
    Returns: (l, b, u, v, w, du, dv, dw)
    where d* = actual - ideal (the twist deviation)
    """
    ra, dec, dist, pm_ra, pm_dec, rv = data
    
    # Convert to Galactic coordinates and compute velocities
    l, b, u_helio, v_helio, w_helio = compute_velocity_galactic(
        ra, dec, dist, pm_ra, pm_dec, rv
    )
    
    # Apply LSR correction
    u_act = u_helio + SOLAR_U
    v_act = v_helio + SOLAR_V
    w_act = w_helio + SOLAR_W
    
    # Ideal helical velocity (Canyon dweller)
    # Stars in stable helical orbit should have:
    # U ~ 0 (no radial drift)
    # V ~ -10 (slight retrograde relative to LSR)
    # W ~ 0 (stays on plane)
    u_ideal = 0.0
    v_ideal = -10.0
    w_ideal = 0.0
    
    # Deviation from ideal (the "phantom force" / twist signature)
    du = u_act - u_ideal
    dv = v_act - v_ideal
    dw = w_act - w_ideal
    
    return l, b, u_act, v_act, w_act, du, dv, dw

def calculate_helical_phase(l, b, turns, w, offset=0):
    """
    Calculate helical phase angle for a position on the sky
    """
    phi = np.deg2rad(l)
    theta = np.deg2rad(90 - b)
    z = np.cos(theta)
    h_idx = (z + 1) / 2.0  # Height index [0, 1]
    
    ideal_phi = (h_idx * turns * 2 * np.pi * w) % (2 * np.pi)
    phase = (phi - ideal_phi - offset) % (2 * np.pi)
    
    return h_idx, np.degrees(phase)

def extract_twist_signature(positions, deviations, center_lon, center_lat, radius=60):
    """
    Extract rotation-invariant twist signature around a center point
    
    Returns:
        signature: dict containing:
            - peak_angles: List of angles where twist magnitude peaks
            - peak_magnitudes: Twist magnitude at each peak
            - relative_angles: Differences between consecutive peaks (rotation-invariant!)
            - twist_pattern: Fourier components
            - center: (lon, lat) of analysis center
    """
    # Convert to numpy arrays
    lons = np.array([p[0] for p in positions])
    lats = np.array([p[1] for p in positions])
    dvs = np.array([d[0] for d in deviations])
    dws = np.array([d[1] for d in deviations])
    
    # Calculate angular distance from center
    dlons = lons - center_lon
    dlats = lats - center_lat
    
    # Wrap longitude differences
    dlons = np.where(dlons > 180, dlons - 360, dlons)
    dlons = np.where(dlons < -180, dlons + 360, dlons)
    
    distances = np.sqrt(dlons**2 + dlats**2)
    
    # Select stars within radius
    mask = distances < radius
    
    if np.sum(mask) < 3:
        return None
    
    # Get local coordinates relative to center
    local_lons = dlons[mask]
    local_lats = dlats[mask]
    local_dvs = dvs[mask]
    local_dws = dws[mask]
    
    # Calculate twist magnitude and direction
    twist_mag = np.sqrt(local_dvs**2 + local_dws**2)
    twist_angle = np.arctan2(local_dws, local_dvs)
    
    # Position angles relative to center
    pos_angles = np.arctan2(local_lats, local_lons)
    pos_angles_deg = np.degrees(pos_angles) % 360
    
    # Sort by position angle
    sort_idx = np.argsort(pos_angles_deg)
    sorted_pos = pos_angles_deg[sort_idx]
    sorted_mag = twist_mag[sort_idx]
    
    # Find peaks in twist magnitude as function of angle
    # Use smoothed version for peak finding
    if len(sorted_mag) >= 5:
        from scipy.ndimage import gaussian_filter1d
        smoothed = gaussian_filter1d(sorted_mag, sigma=1.0, mode='wrap')
        peaks, properties = find_peaks(smoothed, height=np.median(smoothed))
        
        if len(peaks) > 0:
            peak_angles = sorted_pos[peaks]
            peak_mags = sorted_mag[peaks]
        else:
            # No clear peaks, use strongest points
            top_idx = np.argsort(sorted_mag)[-3:]
            peak_angles = sorted_pos[top_idx]
            peak_mags = sorted_mag[top_idx]
    else:
        # Too few points, use all
        peak_angles = sorted_pos
        peak_mags = sorted_mag
    
    # Sort peaks by angle
    peak_sort = np.argsort(peak_angles)
    peak_angles = peak_angles[peak_sort]
    peak_mags = peak_mags[peak_sort]
    
    # Calculate relative angles (rotation-invariant!)
    if len(peak_angles) >= 2:
        relative_angles = np.diff(peak_angles)
        # Add wrap-around angle
        wrap_angle = (360 - peak_angles[-1] + peak_angles[0])
        relative_angles = np.append(relative_angles, wrap_angle)
    else:
        relative_angles = np.array([])
    
    # Fourier decomposition for harmonic analysis
    # Look for 3-fold, 6-fold symmetry
    n_harmonics = 6
    fourier_amps = []
    
    for m in range(1, n_harmonics + 1):
        # Compute mth harmonic amplitude
        cos_sum = np.sum(sorted_mag * np.cos(m * np.deg2rad(sorted_pos)))
        sin_sum = np.sum(sorted_mag * np.sin(m * np.deg2rad(sorted_pos)))
        amp = np.sqrt(cos_sum**2 + sin_sum**2) / len(sorted_mag)
        fourier_amps.append(amp)
    
    signature = {
        'peak_angles': peak_angles,
        'peak_magnitudes': peak_mags,
        'relative_angles': relative_angles,
        'n_peaks': len(peak_angles),
        'fourier_amplitudes': np.array(fourier_amps),
        'total_twist': np.sum(twist_mag),
        'mean_twist': np.mean(twist_mag),
        'center': (center_lon, center_lat),
        'radius': radius
    }
    
    return signature

def compare_signatures(sig1, sig2):
    """
    Compare two twist signatures and return similarity score [0, 1]
    Higher score = better match
    """
    if sig1 is None or sig2 is None:
        return 0.0
    
    # 1. Compare number of peaks (should be similar for same topology)
    n_score = 1.0 - min(abs(sig1['n_peaks'] - sig2['n_peaks']) / 6.0, 1.0)
    
    # 2. Compare relative angles (KEY rotation-invariant feature!)
    if len(sig1['relative_angles']) > 0 and len(sig2['relative_angles']) > 0:
        # Normalize and compare patterns
        rel1 = np.sort(sig1['relative_angles'])
        rel2 = np.sort(sig2['relative_angles'])
        
        # Pad shorter array
        max_len = max(len(rel1), len(rel2))
        rel1_pad = np.pad(rel1, (0, max_len - len(rel1)), constant_values=0)
        rel2_pad = np.pad(rel2, (0, max_len - len(rel2)), constant_values=0)
        
        # Normalized correlation
        diff = np.abs(rel1_pad - rel2_pad)
        angle_score = 1.0 - np.mean(diff) / 180.0
    else:
        angle_score = 0.0
    
    # 3. Compare Fourier harmonics (especially m=3, m=6)
    f1 = sig1['fourier_amplitudes']
    f2 = sig2['fourier_amplitudes']
    
    # Normalize
    if np.max(f1) > 0:
        f1_norm = f1 / np.max(f1)
    else:
        f1_norm = f1
    
    if np.max(f2) > 0:
        f2_norm = f2 / np.max(f2)
    else:
        f2_norm = f2
    
    # Correlation coefficient
    if np.std(f1_norm) > 0 and np.std(f2_norm) > 0:
        fourier_score = np.corrcoef(f1_norm, f2_norm)[0, 1]
        fourier_score = (fourier_score + 1) / 2.0  # Map [-1, 1] to [0, 1]
    else:
        fourier_score = 0.0
    
    # 4. Compare magnitude patterns
    mag1 = sig1['peak_magnitudes']
    mag2 = sig2['peak_magnitudes']
    
    if len(mag1) > 0 and len(mag2) > 0:
        # Normalize
        mag1_norm = mag1 / np.max(mag1)
        mag2_norm = mag2 / np.max(mag2)
        
        # Pad and compare
        max_len = max(len(mag1_norm), len(mag2_norm))
        mag1_pad = np.pad(mag1_norm, (0, max_len - len(mag1_norm)), constant_values=0)
        mag2_pad = np.pad(mag2_norm, (0, max_len - len(mag2_norm)), constant_values=0)
        
        mag_score = 1.0 - np.mean(np.abs(mag1_pad - mag2_pad))
    else:
        mag_score = 0.0
    
    # Weighted combination
    total_score = (
        0.25 * n_score +
        0.35 * angle_score +
        0.30 * fourier_score +
        0.10 * mag_score
    )
    
    return total_score

# ======================
# MAIN ANALYSIS
# ======================

def main():
    print("=" * 70)
    print("STELLAR TWIST EXTRACTOR")
    print("Calibrating rotation-invariant knot signatures from star kinematics")
    print("=" * 70)
    
    # Process all stars
    positions = []
    deviations = []
    names = []
    
    print("\n[1/4] Processing stellar kinematics...")
    for name, data in STARS_KINEMATICS.items():
        if name == "Galactic Center":
            gc_data = data
            continue
        
        l, b, u, v, w, du, dv, dw = get_galactic_kinematics(name, data)
        positions.append((l, b))
        deviations.append((dv, dw))  # Tangential and vertical deviations
        names.append(name)
        
        twist_mag = np.sqrt(dv**2 + dw**2)
        print(f"  {name:20s}: (l={l:6.1f}°, b={b:6.1f}°) | Twist={twist_mag:5.1f} km/s")
    
    # Extract Galactic Center signature
    print("\n[2/4] Extracting Galactic Center twist signature...")
    gc_l, gc_b = 266.41, -29.00
    gc_signature = extract_twist_signature(positions, deviations, gc_l, gc_b, radius=90)
    
    if gc_signature:
        print(f"  Center: ({gc_l:.1f}°, {gc_b:.1f}°)")
        print(f"  Number of peaks: {gc_signature['n_peaks']}")
        print(f"  Peak angles: {gc_signature['peak_angles']}")
        print(f"  Relative angles: {gc_signature['relative_angles']}")
        print(f"  Fourier amplitudes (m=1-6): {gc_signature['fourier_amplitudes']}")
        print(f"  Strongest harmonic: m={np.argmax(gc_signature['fourier_amplitudes'])+1}")
    else:
        print("  WARNING: Could not extract GC signature!")
    
    # Search for other Maw candidates (high twist centers)
    print("\n[3/4] Searching for Maw candidates (twist convergence centers)...")
    
    # Grid search for twist concentration
    lon_grid = np.linspace(-180, 180, 36)
    lat_grid = np.linspace(-90, 90, 18)
    
    maw_candidates = []
    
    for lon in lon_grid:
        for lat in lat_grid:
            sig = extract_twist_signature(positions, deviations, lon, lat, radius=45)
            if sig and sig['total_twist'] > 50:  # Threshold for "interesting"
                # Compare to GC signature
                if gc_signature:
                    similarity = compare_signatures(sig, gc_signature)
                else:
                    similarity = 0.0
                
                maw_candidates.append({
                    'lon': lon,
                    'lat': lat,
                    'total_twist': sig['total_twist'],
                    'n_peaks': sig['n_peaks'],
                    'similarity_to_gc': similarity,
                    'signature': sig
                })
    
    # Sort by total twist
    maw_candidates.sort(key=lambda x: x['total_twist'], reverse=True)
    
    print(f"  Found {len(maw_candidates)} regions with significant twist")
    print(f"\n  Top 5 Maw candidates:")
    for i, maw in enumerate(maw_candidates[:5]):
        print(f"    {i+1}. (l={maw['lon']:6.1f}°, b={maw['lat']:5.1f}°) | "
              f"Twist={maw['total_twist']:6.1f} | "
              f"Peaks={maw['n_peaks']} | "
              f"GC similarity={maw['similarity_to_gc']:.3f}")
    
    # Visualize
    print("\n[4/4] Generating visualization...")
    
    fig = plt.figure(figsize=(18, 12), facecolor='#0a0a0a')
    gs = GridSpec(2, 3, hspace=0.3, wspace=0.3)
    
    # Plot 1: Sky map with twist vectors
    ax1 = fig.add_subplot(gs[0, :], projection='aitoff', facecolor='#0a0a0a')
    
    for i, (pos, dev, name) in enumerate(zip(positions, deviations, names)):
        l, b = pos
        dv, dw = dev
        
        # Convert to radians for Aitoff
        l_rad = np.deg2rad(l - 180)
        b_rad = np.deg2rad(b)
        
        # Color by twist magnitude
        mag = np.sqrt(dv**2 + dw**2)
        c = plt.cm.plasma(min(mag / 100, 1.0))
        
        ax1.scatter(l_rad, b_rad, c=[c], s=100, edgecolors='white', zorder=10)
        
        # Draw twist vector
        scale = 0.003
        dx = -dv * scale
        dy = dw * scale
        ax1.arrow(l_rad, b_rad, dx, dy, color=c, alpha=0.7, head_width=0.02, lw=1.5)
    
    # Mark GC
    gc_l_rad = np.deg2rad(gc_l - 180)
    gc_b_rad = np.deg2rad(gc_b)
    ax1.scatter(gc_l_rad, gc_b_rad, c='lime', s=400, marker='*', 
                edgecolors='white', zorder=15, label='Galactic Center')
    
    # Mark top Maw candidates
    for i, maw in enumerate(maw_candidates[:3]):
        if i == 0 and abs(maw['lon'] - gc_l) < 10:  # Skip if it's GC
            continue
        maw_l_rad = np.deg2rad(maw['lon'] - 180)
        maw_b_rad = np.deg2rad(maw['lat'])
        ax1.scatter(maw_l_rad, maw_b_rad, c='red', s=300, marker='x',
                   linewidths=3, zorder=15)
    
    ax1.set_title("Stellar Twist Field: Phantom Force Vectors", 
                  color='white', fontsize=14, pad=20)
    ax1.grid(True, color='#333333', alpha=0.3)
    ax1.legend(loc='upper right')
    
    # Plot 2: GC Twist Signature (polar)
    if gc_signature:
        ax2 = fig.add_subplot(gs[1, 0], projection='polar', facecolor='#0a0a0a')
        
        angles = np.deg2rad(gc_signature['peak_angles'])
        mags = gc_signature['peak_magnitudes']
        
        ax2.scatter(angles, mags, c='lime', s=200, edgecolors='white', zorder=10)
        
        # Connect peaks
        angles_wrap = np.append(angles, angles[0])
        mags_wrap = np.append(mags, mags[0])
        ax2.plot(angles_wrap, mags_wrap, 'lime', alpha=0.5, lw=2)
        
        ax2.set_title("GC Twist Signature\n(Rotation-Invariant)", 
                     color='white', fontsize=12)
        ax2.set_theta_zero_location('N')
        ax2.grid(True, color='#333333')
        ax2.set_facecolor('#0a0a0a')
    
    # Plot 3: Fourier harmonics
    if gc_signature:
        ax3 = fig.add_subplot(gs[1, 1], facecolor='#0a0a0a')
        
        harmonics = range(1, 7)
        amps = gc_signature['fourier_amplitudes']
        
        ax3.bar(harmonics, amps, color='cyan', edgecolor='white', alpha=0.7)
        ax3.set_xlabel('Harmonic m', color='gray')
        ax3.set_ylabel('Amplitude', color='gray')
        ax3.set_title('Fourier Decomposition\n(3-fold = m=3, 6-fold = m=6)', 
                     color='white', fontsize=12)
        ax3.grid(True, color='#333333', alpha=0.3)
        ax3.tick_params(colors='gray')
        
        # Highlight m=3 and m=6
        ax3.axvline(3, color='lime', linestyle='--', alpha=0.5)
        ax3.axvline(6, color='magenta', linestyle='--', alpha=0.5)
    
    # Plot 4: Relative angles (the KEY rotation-invariant feature!)
    if gc_signature and len(gc_signature['relative_angles']) > 0:
        ax4 = fig.add_subplot(gs[1, 2], facecolor='#0a0a0a')
        
        rel_angles = gc_signature['relative_angles']
        indices = range(len(rel_angles))
        
        ax4.bar(indices, rel_angles, color='orange', edgecolor='white', alpha=0.7)
        ax4.axhline(120, color='lime', linestyle='--', alpha=0.5, label='120° (3-fold)')
        ax4.axhline(60, color='magenta', linestyle='--', alpha=0.5, label='60° (6-fold)')
        ax4.set_xlabel('Peak pair', color='gray')
        ax4.set_ylabel('Angle (degrees)', color='gray')
        ax4.set_title('Relative Peak Angles\n(Rotation-Invariant!)', 
                     color='white', fontsize=12)
        ax4.legend()
        ax4.grid(True, color='#333333', alpha=0.3)
        ax4.tick_params(colors='gray')
    
    plt.savefig('/mnt/user-data/outputs/stellar_twist_signature.png', 
                dpi=150, facecolor='#0a0a0a')
    print("\n✅ Visualization saved: stellar_twist_signature.png")
    
    # Save signature data
    print("\n" + "=" * 70)
    print("SUMMARY: Galactic Center Twist Signature")
    print("=" * 70)
    if gc_signature:
        print(f"Number of peaks: {gc_signature['n_peaks']}")
        print(f"Peak positions: {gc_signature['peak_angles']}")
        print(f"Relative angles (rotation-invariant): {gc_signature['relative_angles']}")
        print(f"Dominant harmonic: m={np.argmax(gc_signature['fourier_amplitudes'])+1}")
        print(f"\nThis signature should be used to search CMB for matching knot structures!")
        
        # Determine expected symmetry
        dominant_m = np.argmax(gc_signature['fourier_amplitudes']) + 1
        if dominant_m == 3:
            print(f"\n⚡ PREDICTION: CMB knot should show 3-FOLD SYMMETRY (triskelion)")
        elif dominant_m == 6:
            print(f"\n⚡ PREDICTION: CMB knot should show 6-FOLD SYMMETRY (hexagonal)")
        
        # Save to file for next script
        import json
        output_data = {
            'gc_signature': {
                'peak_angles': gc_signature['peak_angles'].tolist(),
                'relative_angles': gc_signature['relative_angles'].tolist(),
                'fourier_amplitudes': gc_signature['fourier_amplitudes'].tolist(),
                'n_peaks': int(gc_signature['n_peaks']),
                'dominant_harmonic': int(np.argmax(gc_signature['fourier_amplitudes']) + 1)
            },
            'maw_candidates': [
                {
                    'lon': float(m['lon']),
                    'lat': float(m['lat']),
                    'total_twist': float(m['total_twist']),
                    'similarity_to_gc': float(m['similarity_to_gc'])
                }
                for m in maw_candidates[:5]
            ]
        }
        
        with open('/mnt/user-data/outputs/stellar_twist_reference.json', 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print("\n✅ Reference data saved: stellar_twist_reference.json")
    
    print("\n" + "=" * 70)
    print("Next step: Use this signature to search CMB with proton_twist_signature.py")
    print("=" * 70)

if __name__ == "__main__":
    main()