import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.gridspec import GridSpec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord
import json
import os

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Synthesis Parameters
LMAX = 40          # Max spherical harmonic degree (Increase to 60+ for finer detail if you have RAM)
N_RES = 300        # Grid resolution (300x300)

# Search Parameters
# Searching a tight range around k=1 to find subtle anomalies
K_SEARCH = np.linspace(0.99999999, 1.00000001, 10) 
LON_STEP = 15      # Degrees between longitude samples
LAT_STEP = 15      # Degrees between latitude samples
PATCH_RADIUS = 30  # Degrees around each search point

# Matching threshold
SIMILARITY_THRESHOLD = 0.55 

# ======================
# GLOBAL CACHE
# ======================
YLM_CACHE = None
ALMS_CACHE = None
TH_GRID = None
PH_GRID = None
TH_1D = None  # 1D arrays needed for the hunter search logic
PH_1D = None

# ======================
# DATA LOADING & SYNTHESIS (From Good Edition)
# ======================

def get_alm_and_grid(fits_path, lmax, n_res):
    """
    Loads real Planck data, computes alms, and caches Ylms for fast twisting.
    """
    global YLM_CACHE, ALMS_CACHE, TH_GRID, PH_GRID, TH_1D, PH_1D
    
    if ALMS_CACHE is not None: 
        return
        
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {fits_path}")
        return

    # Handle different FITS structures
    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    # Basic masking
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    
    # Setup HEALPix
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Sampling grid for a_lm computation
    n_theta_alm = lmax * 4
    n_phi_alm = lmax * 8
    theta_alm = np.linspace(0, np.pi, n_theta_alm)
    phi_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(theta_alm, phi_alm, indexing='ij')
    
    # Convert to galactic coordinates for sampling
    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    # Integration weights
    dtheta = theta_alm[1] - theta_alm[0]
    dphi = phi_alm[1] - phi_alm[0]
    weights = np.sin(TH_ALM) * dtheta * dphi
    
    print(f"[*] Computing a_lm (lmax={lmax})...")
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM) 
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    
    ALMS_CACHE = alms
    
    # Create final resolution grid
    TH_1D = np.linspace(0, np.pi, n_res)
    PH_1D = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(TH_1D, PH_1D, indexing='ij')

    print(f"[*] Caching UNTWISTED Y_lm on {n_res}x{n_res} grid...")
    YLM_CACHE = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            YLM_CACHE[(l, m)] = sph_harm(m, l, PH_GRID, TH_GRID)

def synthesize_twisted_universe_fast(k, lmax):
    """
    Reconstructs the CMB using cached Ylms, applying the twist factor k.
    """
    map_out = np.zeros_like(TH_GRID, dtype=np.complex128)
    delta_phi_multiplier = (k - 1) * PH_GRID
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            alm = ALMS_CACHE[(l, m)]
            Y_lm_untwisted = YLM_CACHE[(l, m)]
            # The Twist Logic: Phase shift based on m and twist k
            phase_corr = np.exp(1j * m * delta_phi_multiplier)
            map_out += alm * Y_lm_untwisted * phase_corr
            
    return map_out.real

# ======================
# TARGET SIGNATURES (From Twist Hunter)
# ======================

TARGET_SIGNATURE = {
    'relative_angles_set': [
        [23.0, 48.0, 26.0, 263.0],  # Proton 30M
        [48.0, 20.0, 33.0, 259.0],  # Proton 100M
        [23.64, 32.13, 304.23]      # Galactic Center
    ],
    'n_peaks_range': (3, 5),
    'tolerance': 15.0
}

# ======================
# TWIST SIGNATURE EXTRACTION
# ======================

def extract_local_twist_cmb(T_map, theta_grid, phi_grid, center_lon, center_lat, radius_deg):
    """
    Extract twist signature from a local CMB patch.
    """
    res = len(theta_grid)
    
    # Map (lon, lat) to grid indices (phi, theta)
    # Note: theta_grid is 0 to pi (colatitude), so we use 90 - lat
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
    
    if T_patch.size < 100:
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
            # We look for high variance/gradient along the ray as a proxy for "knot" tension
            grad = np.gradient(values[valid])
            twist_mag = np.std(grad)
        else:
            twist_mag = 0.0
        
        radial_profiles.append(twist_mag)
    
    radial_profiles = np.array(radial_profiles)
    
    # Peak finding
    from scipy.ndimage import gaussian_filter1d
    smoothed = gaussian_filter1d(radial_profiles, sigma=5, mode='wrap')
    
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(smoothed, height=np.median(smoothed) * 0.3)
    
    if len(peaks) < 2:
        return None
    
    if len(peaks) > 8:
        peak_strengths = smoothed[peaks]
        strongest = np.argsort(peak_strengths)[-6:]
        peaks = peaks[strongest]
    
    peak_angles = angles[peaks]
    peak_mags = radial_profiles[peaks]
    
    # Sort by angle
    sort_idx = np.argsort(peak_angles)
    peak_angles = peak_angles[sort_idx]
    peak_mags = peak_mags[sort_idx]
    
    # Relative angles
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
    """
    if signature is None: return 0.0, -1
    if len(signature['relative_angles']) < 2: return 0.0, -1
    
    n_peaks = signature['n_peaks']
    n_min, n_max = targets['n_peaks_range']
    if n_peaks < n_min or n_peaks > n_max: return 0.0, -1
    
    best_score = 0.0
    best_target = -1
    sig_rel = np.sort(signature['relative_angles'])
    
    for target_idx, target_rel in enumerate(targets['relative_angles_set']):
        target_rel = np.array(target_rel)
        n_sig = len(sig_rel)
        n_tgt = len(target_rel)
        
        for rotation in range(n_sig):
            rotated_sig = np.roll(sig_rel, rotation)
            min_len = min(n_sig, n_tgt)
            diffs = np.abs(rotated_sig[:min_len] - target_rel[:min_len])
            diffs = np.minimum(diffs, 360 - diffs)
            matches = diffs < targets['tolerance']
            
            if np.sum(matches) == 0:
                score = 0.0
            else:
                match_fraction = np.sum(matches) / min_len
                match_quality = 1.0 - np.mean(diffs[matches]) / targets['tolerance']
                score = match_fraction * match_quality
            
            if score > best_score:
                best_score = score
                best_target = target_idx
    
    return best_score, best_target

# ======================
# MAIN EXECUTION
# ======================

def main():
    print("=" * 70)
    print("CMB TWIST HUNTER (Real Data Edition)")
    print("Searching for rotation-invariant knot signatures in Planck Data")
    print("=" * 70)

    # 1. Initialize Real Data
    get_alm_and_grid(FITS_PATH, LMAX, N_RES)
    if ALMS_CACHE is None:
        print("[!] Data initialization failed. Exiting.")
        return

    print(f"\n[1/3] Generating twisted maps from K={K_SEARCH[0]:.8f} to {K_SEARCH[-1]:.8f}...")
    
    # Pre-generate maps (or generate on fly if memory is tight, but we'll store for now)
    cmb_maps = {}
    for i, k in enumerate(K_SEARCH):
        print(f"  Generating map for k={k:.8f}...")
        T_map = synthesize_twisted_universe_fast(k, LMAX)
        # Store map + 1D axes
        cmb_maps[k] = (T_map, TH_1D, PH_1D)
    
    print("\n[2/3] Scanning sky for twist signatures...")
    
    longitudes = np.arange(-180, 180, LON_STEP)
    latitudes = np.arange(-90, 90, LAT_STEP)
    total_points = len(K_SEARCH) * len(longitudes) * len(latitudes)
    processed = 0
    matches = []
    
    for k in K_SEARCH:
        T_map, theta_axis, phi_axis = cmb_maps[k]
        
        for lon in longitudes:
            for lat in latitudes:
                processed += 1
                if processed % 500 == 0:
                    print(f"  Progress: {processed}/{total_points} ({100*processed/total_points:.1f}%) | Matches: {len(matches)}")
                
                # Extract using the 1D axes
                sig = extract_local_twist_cmb(T_map, theta_axis, phi_axis, lon, lat, PATCH_RADIUS)
                
                if sig is None: continue
                
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
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    # --- VISUALIZATION & SAVING ---
    print("\n[3/3] Generating output...")
    
    if len(matches) == 0:
        print("[!] No matches found. Try lowering SIMILARITY_THRESHOLD or checking FITS data.")
        return

    # Print top matches
    print(f"\n  Top Matches:")
    print(f"  {'Rank':<6} {'k':<12} {'Lon':<8} {'Lat':<8} {'Score':<8} {'Pattern'}")
    print("  " + "-" * 65)
    for i, match in enumerate(matches[:10]):
        pattern_name = ["Proton-30M", "Proton-100M", "GC"][match['target_pattern']]
        print(f"  {i+1:<6} {match['k']:<12.8f} {match['lon']:<8.1f} {match['lat']:<8.1f} {match['score']:<8.3f} {pattern_name}")

    # Plotting
    fig = plt.figure(figsize=(18, 12), facecolor='#0a0a0a')
    gs = GridSpec(2, 2, hspace=0.3, wspace=0.3)
    
    # Plot 1: Sky Map
    ax1 = fig.add_subplot(gs[0, :], projection='aitoff', facecolor='#0a0a0a')
    # Background: Plot the UNTWISTED map (k=1) faint
    T_bg = synthesize_twisted_universe_fast(1.0, LMAX)
    # Re-orient for Aitoff (shift so center is 0)
    T_bg_rolled = np.roll(T_bg, int(N_RES/2), axis=1) 
    im = ax1.imshow(T_bg_rolled, extent=(-np.pi, np.pi, -np.pi/2, np.pi/2), 
                    cmap='gray', alpha=0.3, origin='lower')

    for match in matches:
        lon_rad = np.deg2rad(match['lon'])
        lat_rad = np.deg2rad(match['lat'])
        c = ['cyan', 'lime', 'magenta'][match['target_pattern']]
        s = 100 + 500 * match['score']
        ax1.scatter(lon_rad, lat_rad, c=c, s=s, alpha=0.6, edgecolors='white', linewidths=1)
        
    top = matches[0]
    ax1.scatter(np.deg2rad(top['lon']), np.deg2rad(top['lat']), c='red', s=800, marker='*', edgecolors='white', linewidths=2)
    ax1.set_title("Real CMB Twist Signature Matches", color='white', fontsize=14)
    ax1.grid(True, color='#333333', alpha=0.3)

    # Plot 2: Histogram
    ax2 = fig.add_subplot(gs[1, 0], facecolor='#0a0a0a')
    scores = [m['score'] for m in matches]
    ax2.hist(scores, bins=20, color='cyan', edgecolor='white', alpha=0.7)
    ax2.axvline(SIMILARITY_THRESHOLD, color='red', linestyle='--')
    ax2.set_title('Match Quality Distribution', color='white')
    ax2.tick_params(colors='gray', labelcolor='gray')

    # Plot 3: Polar Signature
    ax3 = fig.add_subplot(gs[1, 1], projection='polar', facecolor='#0a0a0a')
    top_sig = matches[0]['signature']
    angles = np.deg2rad(top_sig['peak_angles'])
    mags = top_sig['peak_magnitudes']
    if np.max(mags) > 0: mags = mags / np.max(mags)
    
    ax3.scatter(angles, mags, c='red', s=200, edgecolors='white', zorder=10)
    angles_wrap = np.append(angles, angles[0])
    mags_wrap = np.append(mags, mags[0])
    ax3.plot(angles_wrap, mags_wrap, 'red', alpha=0.5, lw=2)
    ax3.set_title(f"Best Match Signature (k={top['k']:.8f})", color='white', fontsize=12)
    ax3.set_theta_zero_location('N')
    ax3.grid(True, color='#333333')
    ax3.tick_params(colors='gray', labelcolor='gray')

    plt.savefig('cmb_twist_matches_real.png', dpi=150, facecolor='#0a0a0a', bbox_inches='tight')
    print("  ✓ Saved: cmb_twist_matches_real.png")

    # JSON Export
    output_data = {
        'source_file': FITS_PATH,
        'lmax': LMAX,
        'matches': []
    }
    for match in matches[:20]:
        output_data['matches'].append({
            'k': float(match['k']),
            'lon': float(match['lon']),
            'lat': float(match['lat']),
            'score': float(match['score']),
            'pattern': ["Proton-30M", "Proton-100M", "GC"][match['target_pattern']]
        })
    
    with open('cmb_twist_results_real.json', 'w') as f:
        json.dump(output_data, f, indent=2)
    print("  ✓ Saved: cmb_twist_results_real.json")

if __name__ == "__main__":
    main()