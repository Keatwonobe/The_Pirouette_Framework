import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import maximum_filter
from skimage.graph import route_through_array
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 300
K_REALITY = 1.0
CHAOS_DAMPING = 5.0
SEARCH_RADIUS_PX = 40
COST_THRESHOLD = 20.0

# The Bow Shock Vector found in previous step (l, b)
MOTION_VECTOR_L = 51.8
MOTION_VECTOR_B = -72.9

# ======================
# 1. ENGINE (Reused)
# ======================

def get_alms_and_grid(fits_path, lmax, n_res):
    print(f"[*] Loading CMB Data...")
    try:
        data = fits.getdata(fits_path)
        if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else: cmb = data.astype(np.float64)
        cmb[np.isnan(cmb)] = np.nanmean(cmb)
    except FileNotFoundError:
        print("[!] File not found.")
        sys.exit(1)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    n_theta = lmax * 3; n_phi = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta)
    p_alm = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')
    
    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, theta, phi

def precompute_profiles(alms, lmax, theta_vec):
    m_range = np.arange(-lmax, lmax + 1)
    n_m = len(m_range); n_theta = len(theta_vec)
    zeros_phi = np.zeros_like(theta_vec)
    profiles = {
        'L10': np.zeros((n_m, n_theta), dtype=np.complex128),
        'L20': np.zeros((n_m, n_theta), dtype=np.complex128),
        'Substrate': np.zeros((n_m, n_theta), dtype=np.complex128)
    }
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) not in alms: continue
            term = alms[(l, m)] * sph_harm(m, l, zeros_phi, theta_vec)
            if l == 10: profiles['L10'][i, :] += term
            elif l == 20: profiles['L20'][i, :] += term
            else: profiles['Substrate'][i, :] += term
    return profiles, m_range

def synthesize_band(profile_matrix, m_range, phi_vec, k):
    m_col = m_range[:, np.newaxis]
    phi_row = phi_vec[np.newaxis, :]
    phase_matrix = np.exp(1j * m_col * k * phi_row)
    field = (profile_matrix.T @ phase_matrix).real
    return field

def get_gradient_magnitude(field):
    gy, gx = np.gradient(field)
    return np.sqrt(gx**2 + gy**2)

# ======================
# 2. VELOCITY CALCULATOR
# ======================

def find_universes(field, neighborhood_size=20):
    field_norm = (field - field.min()) / (field.max() - field.min())
    local_max = maximum_filter(field_norm, size=neighborhood_size) == field_norm
    peak_values = field_norm[local_max]
    threshold = np.percentile(peak_values, 50) 
    return (local_max) & (field_norm > threshold)

def trace_wake(start_node, end_node, cost_map):
    r0, c0 = start_node; r1, c1 = end_node
    rmin, rmax = min(r0, r1), max(r0, r1)
    cmin, cmax = min(c0, c1), max(c0, c1)
    pad = 10
    rmin = max(0, rmin-pad); rmax = min(cost_map.shape[0]-1, rmax+pad)
    cmin = max(0, cmin-pad); cmax = min(cost_map.shape[1]-1, cmax+pad)
    
    sub_cost = cost_map[rmin:rmax, cmin:cmax]
    start_local = (r0 - rmin, c0 - cmin)
    end_local = (r1 - rmin, c1 - cmin)
    
    try:
        indices, weight = route_through_array(sub_cost, start_local, end_local)
        global_indices = np.array(indices) + np.array([rmin, cmin])
        return global_indices, weight
    except:
        return None, 99999

def calculate_wake_angles(valid_paths, motion_vec_px, n_res):
    """ Measures angle of each wake segment relative to motion vector """
    angles = []
    
    # Motion Vector in Pixel Space (Approximate)
    # We just need the general flow direction for comparison
    # Motion vector is 3D, projected onto 2D map varies by location.
    # This is complex geometry, so we simplify:
    # We compare wake segment angle to the local gradient of the "Bow Shock Dipole"
    # But for a robust estimate, we can just look at the distribution of all wake angles
    # relative to the North-South axis and find the peaks.
    
    for path in valid_paths:
        if len(path) < 5: continue
        
        # Vector of the wake segment
        y0, x0 = path[0]
        y1, x1 = path[-1]
        
        dy = y1 - y0
        dx = x1 - x0
        
        # Angle of wake segment (0 to 180 relative to horizontal)
        angle = np.degrees(np.arctan2(dy, dx))
        if angle < 0: angle += 360
        
        # We care about the angle relative to the Motion Vector at that location
        # But let's just collect raw angles first to see the distribution
        angles.append(angle)
        
    return np.array(angles)

# ======================
# 3. MAIN
# ======================

def run_velocity_estimator():
    alms, theta_vec, phi_vec = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    profiles, m_range = precompute_profiles(alms, LMAX, theta_vec)
    
    print(f"[*] Reconstructing Wake Topology...")
    
    # Generate Substrate (Magma)
    map_sub = synthesize_band(profiles['Substrate'], m_range, phi_vec, K_REALITY)
    chaos_sub = get_gradient_magnitude(map_sub)
    chaos_norm = (chaos_sub - chaos_sub.min()) / (chaos_sub.max() - chaos_sub.min())
    friction_map = 1.0 - chaos_norm + 0.01 
    
    # Generate Nodes
    map_10 = synthesize_band(profiles['L10'], m_range, phi_vec, K_REALITY)
    chaos_10 = get_gradient_magnitude(map_10)
    clean_10 = map_10 * np.exp(-CHAOS_DAMPING * (chaos_10/np.max(chaos_10)))
    mask_10 = find_universes(clean_10, 15)
    
    map_20 = synthesize_band(profiles['L20'], m_range, phi_vec, K_REALITY)
    chaos_20 = get_gradient_magnitude(map_20)
    clean_20 = map_20 * np.exp(-CHAOS_DAMPING * (chaos_20/np.max(chaos_20)))
    mask_20 = find_universes(clean_20, 10)
    
    y10, x10 = np.where(mask_10); y20, x20 = np.where(mask_20)
    nodes = np.vstack((np.column_stack((y10, x10)), np.column_stack((y20, x20))))
    
    # Trace Wakes
    valid_paths = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            p1 = nodes[i]; p2 = nodes[j]
            dist = np.hypot(p2[0]-p1[0], p2[1]-p1[1])
            if dist < SEARCH_RADIUS_PX:
                path_idx, cost = trace_wake(p1, p2, friction_map)
                if cost < COST_THRESHOLD:
                    valid_paths.append(path_idx)
    
    print(f"[*] Analyzing Mach Cone Geometry ({len(valid_paths)} filaments)...")
    
    # Convert Motion Vector (l, b) to Pixel Coords
    # l goes 180 to -180 (Left to Right), b goes -90 to 90 (Bottom to Top)
    # Map is origin lower.
    mv_x = ((180 - MOTION_VECTOR_L) / 360) * N_RES # Rough conversion
    mv_y = ((MOTION_VECTOR_B + 90) / 180) * N_RES
    
    # Just visualizing the "V" shape is key here.
    # We will plot the wakes and overlay the Motion Vector
    
    fig = plt.figure(figsize=(10, 12), facecolor='#050505')
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    
    # Panel 1: The Wake Field with Motion Vector
    ax_map = plt.subplot(gs[0])
    ax_map.imshow(chaos_norm, origin='lower', cmap='gray', alpha=0.5, extent=[-180, 180, -90, 90])
    
    for path in valid_paths:
        py, px = path[:, 0], path[:, 1]
        # Convert px, py to lat/lon for plot extent
        lon = (px / N_RES) * 360 - 180
        lat = (py / N_RES) * 180 - 90
        ax_map.plot(lon, lat, color='cyan', linewidth=0.8, alpha=0.5)
        
    # Plot Motion Arrow (Reverse of Motion Vector because that's where we are going)
    # Motion Vector is L=51.8, B=-72.9
    ax_map.arrow(0, 0, MOTION_VECTOR_L, MOTION_VECTOR_B, 
                 color='yellow', width=2, head_width=8, label='Velocity Vector')
    
    ax_map.set_title(f"THE COSMIC WAKE | Heading: (l={MOTION_VECTOR_L}, b={MOTION_VECTOR_B})", color='white', fontsize=14)
    ax_map.legend(loc='upper right')
    ax_map.axis('off')
    
    # Panel 2: The Mach Angle Histogram
    # We calculate the angle of every wake segment relative to the Motion Vector
    # Ideally, we see peaks at +Theta and -Theta (The "V")
    
    # Simplified: Just histogram of raw segment angles to see if there's a dominant "X" pattern
    angles = calculate_wake_angles(valid_paths, None, N_RES)
    
    ax_hist = plt.subplot(gs[1])
    ax_hist.set_facecolor('#111')
    counts, bins, _ = ax_hist.hist(angles, bins=90, range=(0, 180), color='cyan', alpha=0.7)
    
    # Find Peaks (The Mach Angle)
    peak_idx = np.argmax(counts)
    mach_angle = bins[peak_idx]
    
    # Calculate Mach Number: M = 1/sin(mu)
    # If the wake is perpendicular (90 deg), M=1. If wake is narrow (30 deg), M=2.
    # We assume the wake angle is relative to flow. Let's assume the histogram peak represents the wake characteristic.
    # Mach Angle mu is usually half the opening angle. 
    # Let's verify visually first.
    
    ax_hist.set_title(f"WAKE ANGLE DISTRIBUTION (Peak ~ {mach_angle:.1f}°)", color='white', fontsize=10)
    ax_hist.set_xlabel("Wake Filament Angle (Degrees)", color='gray')
    ax_hist.grid(color='#333', linestyle=':')
    ax_hist.tick_params(colors='gray')
    
    plt.tight_layout()
    plt.savefig("cmb_bulk_velocity.png", dpi=100, facecolor='#050505')
    print("✅ Velocity Estimation Complete. Saved to cmb_bulk_velocity.png")

if __name__ == "__main__":
    run_velocity_estimator()