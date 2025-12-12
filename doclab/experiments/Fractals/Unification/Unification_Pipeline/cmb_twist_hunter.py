import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json

# ======================
# CONFIGURATION
# ======================

# CMB synthesis parameters
LMAX = 40  # Spherical harmonic max (trade-off: speed vs resolution)
CMB_RES = 200  # Grid resolution for analysis

# Search parameters
K_SEARCH = np.linspace(0.98, 1.02, 20)  # Twist parameter scan
LON_STEP = 15  # Degrees between longitude samples
LAT_STEP = 15  # Degrees between latitude samples
PATCH_RADIUS = 30  # Degrees around each search point

# Matching threshold
SIMILARITY_THRESHOLD = 0.55  # Report matches above this

# ======================
# TARGET SIGNATURES (from calibration)
# ======================

# Combined target from proton + GC
TARGET_SIGNATURE = {
    'relative_angles_set': [
        [23.0, 48.0, 26.0, 263.0],  # Proton 30M
        [48.0, 20.0, 33.0, 259.0],  # Proton 100M
        [23.64, 32.13, 304.23]      # Galactic Center
    ],
    'n_peaks_range': (3, 5),
    'tolerance': 15.0  # Degrees
}

print("=" * 70)
print("CMB TWIST HUNTER")
print("Searching for rotation-invariant knot signatures in CMB")
print("=" * 70)
print("\nTarget signatures loaded:")
for i, angles in enumerate(TARGET_SIGNATURE['relative_angles_set']):
    print(f"  Pattern {i+1}: {angles}")
print(f"\nTolerance: ±{TARGET_SIGNATURE['tolerance']}°")
print("=" * 70)

# ======================
# CMB SYNTHESIS (Simplified - Mock Data)
# ======================

def synthesize_cmb_mock(k_twist, res=CMB_RES):
    """
    Generate mock CMB with twist parameter k
    In production, this would use real Planck data
    
    For now, we create a synthetic field with known twist structure
    """
    theta = np.linspace(0, np.pi, res)
    phi = np.linspace(-np.pi, np.pi, res)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    
    # Create base temperature field
    T_base = np.random.randn(res, res) * 0.1
    
    # Add coherent structure with twist
    # Simulate wound channels at specific longitudes
    l_channels = [0, 120, 240]  # Three-fold structure
    
    for l_center in l_channels:
        l_rad = np.deg2rad(l_center)
        
        # Apply twist modulation
        twisted_phi = PH + k_twist * TH  # Helical twist
        
        # Add channel structure
        channel_strength = np.exp(-((twisted_phi - l_rad) ** 2) / (0.5**2))
        T_base += channel_strength * np.sin(3 * TH) * 0.5
    
    # Add dipole
    T_base += np.cos(TH) * 0.3
    
    # Add realistic CMB power spectrum structure
    for l in range(2, 20):
        for m in range(-l, l+1):
            amp = np.random.randn() * (1.0 / l**1.5)
            phase = np.random.rand() * 2 * np.pi
            
            # Simplified spherical harmonic
            Y_lm = np.sin(l * TH) * np.cos(m * PH + phase)
            T_base += amp * Y_lm
    
    return T_base, theta, phi

# ======================
# TWIST SIGNATURE EXTRACTION
# ======================

def extract_local_twist_cmb(T_map, theta_grid, phi_grid, center_lon, center_lat, radius_deg):
    """
    Extract twist signature from a local CMB patch
    Similar to proton basin extraction but adapted for spherical coordinates
    """
    # Convert center to indices
    res = len(theta_grid)
    
    lat_idx = np.argmin(np.abs(theta_grid - np.deg2rad(90 - center_lat)))
    lon_idx = np.argmin(np.abs(phi_grid - np.deg2rad(center_lon)))
    
    # Define patch extent
    radius_idx = int(radius_deg / 180 * res / 2)
    
    i_min = max(0, lat_idx - radius_idx)
    i_max = min(res, lat_idx + radius_idx)
    j_min = max(0, lon_idx - radius_idx)
    j_max = min(res, lon_idx + radius_idx)
    
    # Extract patch
    T_patch = T_map[i_min:i_max, j_min:j_max]
    
    if T_patch.size < 100:  # Too small
        return None
    
    # Compute radial profiles from patch center
    patch_h, patch_w = T_patch.shape
    center_i, center_j = patch_h // 2, patch_w // 2
    
    angles = np.linspace(0, 360, 360, endpoint=False)
    radial_profiles = []
    
    max_r = min(patch_h, patch_w) // 2 - 1
    
    for angle_deg in angles:
        angle_rad = np.deg2rad(angle_deg)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        
        # Sample along ray
        radii = np.linspace(0, max_r, 30)
        values = []
        
        for r in radii:
            i = int(center_i + r * sin_a)
            j = int(center_j + r * cos_a)
            
            if 0 <= i < patch_h and 0 <= j < patch_w:
                values.append(T_patch[i, j])
            else:
                values.append(np.nan)
        
        values = np.array(values)
        valid = ~np.isnan(values)
        
        if np.sum(valid) > 5:
            grad = np.gradient(values[valid])
            twist_mag = np.std(grad)
        else:
            twist_mag = 0.0
        
        radial_profiles.append(twist_mag)
    
    radial_profiles = np.array(radial_profiles)
    
    # Find peaks
    from scipy.ndimage import gaussian_filter1d
    smoothed = gaussian_filter1d(radial_profiles, sigma=5, mode='wrap')
    
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(smoothed, height=np.median(smoothed) * 0.3)
    
    if len(peaks) < 2:
        # Not enough structure
        return None
    
    if len(peaks) > 8:
        # Too many peaks, take strongest
        peak_strengths = smoothed[peaks]
        strongest = np.argsort(peak_strengths)[-6:]
        peaks = peaks[strongest]
    
    peak_angles = angles[peaks]
    peak_mags = radial_profiles[peaks]
    
    # Sort by angle
    sort_idx = np.argsort(peak_angles)
    peak_angles = peak_angles[sort_idx]
    peak_mags = peak_mags[sort_idx]
    
    # Calculate relative angles
    if len(peak_angles) >= 2:
        relative_angles = np.diff(peak_angles)
        wrap_angle = (360 - peak_angles[-1] + peak_angles[0])
        relative_angles = np.append(relative_angles, wrap_angle)
    else:
        relative_angles = np.array([])
    
    signature = {
        'peak_angles': peak_angles,
        'peak_magnitudes': peak_mags,
        'relative_angles': relative_angles,
        'n_peaks': len(peak_angles),
        'center': (center_lon, center_lat),
        'total_twist': np.sum(radial_profiles)
    }
    
    return signature

def match_to_targets(signature, targets):
    """
    Check if signature matches any of the target patterns
    Returns best match score and which target
    """
    if signature is None:
        return 0.0, -1
    
    if len(signature['relative_angles']) < 2:
        return 0.0, -1
    
    # Check number of peaks
    n_peaks = signature['n_peaks']
    n_min, n_max = targets['n_peaks_range']
    
    if n_peaks < n_min or n_peaks > n_max:
        return 0.0, -1
    
    # Compare to each target pattern
    best_score = 0.0
    best_target = -1
    
    sig_rel = np.sort(signature['relative_angles'])
    
    for target_idx, target_rel in enumerate(targets['relative_angles_set']):
        target_rel = np.array(target_rel)
        
        # Try all rotations of signature to find best match
        n_sig = len(sig_rel)
        n_tgt = len(target_rel)
        
        for rotation in range(n_sig):
            rotated_sig = np.roll(sig_rel, rotation)
            
            # Pad/trim to match lengths
            min_len = min(n_sig, n_tgt)
            
            # Compute angular differences
            diffs = np.abs(rotated_sig[:min_len] - target_rel[:min_len])
            
            # Wrap differences (angles are modulo 360)
            diffs = np.minimum(diffs, 360 - diffs)
            
            # Check if within tolerance
            matches = diffs < targets['tolerance']
            
            if np.sum(matches) == 0:
                score = 0.0
            else:
                # Score based on fraction matching and tightness of match
                match_fraction = np.sum(matches) / min_len
                match_quality = 1.0 - np.mean(diffs[matches]) / targets['tolerance']
                score = match_fraction * match_quality
            
            if score > best_score:
                best_score = score
                best_target = target_idx
    
    return best_score, best_target

# ======================
# MAIN SEARCH
# ======================

def main():
    print("\n[1/3] Generating CMB maps at different twist values...")
    
    cmb_maps = {}
    for k in K_SEARCH:
        T_map, theta, phi = synthesize_cmb_mock(k)
        cmb_maps[k] = (T_map, theta, phi)
        if len(cmb_maps) % 5 == 0:
            print(f"  Generated {len(cmb_maps)}/{len(K_SEARCH)} maps")
    
    print(f"  ✓ {len(cmb_maps)} CMB maps ready")
    
    print("\n[2/3] Scanning sky for twist signatures...")
    
    # Create search grid
    longitudes = np.arange(-180, 180, LON_STEP)
    latitudes = np.arange(-90, 90, LAT_STEP)
    
    total_points = len(K_SEARCH) * len(longitudes) * len(latitudes)
    processed = 0
    
    matches = []
    
    for k in K_SEARCH:
        T_map, theta, phi = cmb_maps[k]
        
        for lon in longitudes:
            for lat in latitudes:
                processed += 1
                
                if processed % 100 == 0:
                    print(f"  Progress: {processed}/{total_points} "
                          f"({100*processed/total_points:.1f}%) | "
                          f"Matches found: {len(matches)}")
                
                # Extract local signature
                sig = extract_local_twist_cmb(T_map, theta, phi, lon, lat, PATCH_RADIUS)
                
                if sig is None:
                    continue
                
                # Check for match
                score, target_idx = match_to_targets(sig, TARGET_SIGNATURE)
                
                if score >= SIMILARITY_THRESHOLD:
                    matches.append({
                        'k': k,
                        'lon': lon,
                        'lat': lat,
                        'score': score,
                        'target_pattern': target_idx,
                        'signature': sig
                    })
    
    print(f"\n  ✓ Scan complete! Found {len(matches)} candidate matches")
    
    # Sort by score
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n[3/3] Analyzing results...")
    
    if len(matches) == 0:
        print("\n  ⚠ No matches above threshold")
        print("  This could mean:")
        print("    1. The CMB mock data doesn't have the right structure")
        print("    2. Threshold is too high")
        print("    3. Need real Planck data for actual search")
        return
    
    print(f"\n  Top {min(10, len(matches))} matches:")
    print(f"  {'Rank':<6} {'k':<10} {'Lon':<8} {'Lat':<8} {'Score':<8} {'Pattern'}")
    print("  " + "-" * 60)
    
    for i, match in enumerate(matches[:10]):
        pattern_name = ["Proton-30M", "Proton-100M", "GC"][match['target_pattern']]
        print(f"  {i+1:<6} {match['k']:<10.6f} {match['lon']:<8.1f} "
              f"{match['lat']:<8.1f} {match['score']:<8.3f} {pattern_name}")
    
    # Visualization
    print("\n  Generating visualization...")
    
    fig = plt.figure(figsize=(18, 12), facecolor='#0a0a0a')
    gs = GridSpec(2, 2, hspace=0.3, wspace=0.3)
    
    # Plot 1: Sky map with matches
    ax1 = fig.add_subplot(gs[0, :], projection='aitoff', facecolor='#0a0a0a')
    
    if len(matches) > 0:
        # Plot all matches
        for match in matches:
            lon_rad = np.deg2rad(match['lon'] - 180)
            lat_rad = np.deg2rad(match['lat'])
            
            # Color by pattern
            colors = ['cyan', 'lime', 'magenta']
            c = colors[match['target_pattern']]
            
            # Size by score
            s = 100 + 500 * match['score']
            
            ax1.scatter(lon_rad, lat_rad, c=c, s=s, alpha=0.6, 
                       edgecolors='white', linewidths=1)
        
        # Mark top match
        top = matches[0]
        lon_rad = np.deg2rad(top['lon'] - 180)
        lat_rad = np.deg2rad(top['lat'])
        ax1.scatter(lon_rad, lat_rad, c='red', s=800, marker='*',
                   edgecolors='white', linewidths=2, zorder=100)
    
    ax1.set_title("CMB Twist Signature Matches\n(Star = Best Match)", 
                 color='white', fontsize=14, pad=20)
    ax1.grid(True, color='#333333', alpha=0.3)
    
    # Plot 2: Score distribution
    if len(matches) > 0:
        ax2 = fig.add_subplot(gs[1, 0], facecolor='#0a0a0a')
        
        scores = [m['score'] for m in matches]
        ax2.hist(scores, bins=20, color='cyan', edgecolor='white', alpha=0.7)
        ax2.axvline(SIMILARITY_THRESHOLD, color='red', linestyle='--', 
                   label=f'Threshold ({SIMILARITY_THRESHOLD})')
        ax2.set_xlabel('Match Score', color='gray')
        ax2.set_ylabel('Count', color='gray')
        ax2.set_title('Match Quality Distribution', color='white')
        ax2.legend()
        ax2.grid(True, color='#333333', alpha=0.3)
        ax2.tick_params(colors='gray')
    
    # Plot 3: Best match signature
    if len(matches) > 0:
        ax3 = fig.add_subplot(gs[1, 1], projection='polar', facecolor='#0a0a0a')
        
        top_sig = matches[0]['signature']
        angles = np.deg2rad(top_sig['peak_angles'])
        mags = top_sig['peak_magnitudes']
        
        # Normalize magnitudes
        if np.max(mags) > 0:
            mags = mags / np.max(mags)
        
        ax3.scatter(angles, mags, c='red', s=200, edgecolors='white', zorder=10)
        
        angles_wrap = np.append(angles, angles[0])
        mags_wrap = np.append(mags, mags[0])
        ax3.plot(angles_wrap, mags_wrap, 'red', alpha=0.5, lw=2)
        
        ax3.set_title(f"Best Match Signature\n"
                     f"(k={matches[0]['k']:.4f}, "
                     f"score={matches[0]['score']:.3f})", 
                     color='white', fontsize=12)
        ax3.set_theta_zero_location('N')
        ax3.grid(True, color='#333333')
        ax3.set_facecolor('#0a0a0a')
    
    plt.savefig('/mnt/user-data/outputs/cmb_twist_matches.png',
                dpi=150, facecolor='#0a0a0a', bbox_inches='tight')
    
    print("  ✓ Saved: cmb_twist_matches.png")
    
    # Save results
    output_data = {
        'search_parameters': {
            'k_range': [float(K_SEARCH[0]), float(K_SEARCH[-1])],
            'n_k_values': len(K_SEARCH),
            'spatial_resolution': (LON_STEP, LAT_STEP),
            'patch_radius': PATCH_RADIUS,
            'similarity_threshold': SIMILARITY_THRESHOLD
        },
        'target_signatures': TARGET_SIGNATURE,
        'matches': []
    }
    
    for match in matches[:20]:  # Save top 20
        output_data['matches'].append({
            'rank': matches.index(match) + 1,
            'k': float(match['k']),
            'longitude': float(match['lon']),
            'latitude': float(match['lat']),
            'score': float(match['score']),
            'target_pattern': int(match['target_pattern']),
            'n_peaks': int(match['signature']['n_peaks']),
            'relative_angles': match['signature']['relative_angles'].tolist()
        })
    
    with open('/mnt/user-data/outputs/cmb_twist_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print("  ✓ Saved: cmb_twist_results.json")
    
    print("\n" + "=" * 70)
    print("SEARCH COMPLETE")
    print("=" * 70)
    print(f"\nFound {len(matches)} regions matching the twist signature")
    
    if len(matches) > 0:
        print(f"\nBest match:")
        top = matches[0]
        print(f"  Location: ({top['lon']:.1f}°, {top['lat']:.1f}°)")
        print(f"  Twist k: {top['k']:.6f}")
        print(f"  Score: {top['score']:.3f}")
        print(f"  Pattern: {['Proton-30M', 'Proton-100M', 'GC'][top['target_pattern']]}")
        print(f"  Relative angles: {top['signature']['relative_angles']}")
    
    print("\n" + "=" * 70)
    print("NOTE: This search used MOCK CMB data")
    print("For real results, replace synthesize_cmb_mock() with Planck data")
    print("=" * 70)

if __name__ == "__main__":
    main()