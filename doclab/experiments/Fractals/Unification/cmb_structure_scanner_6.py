import numpy as np
import matplotlib.pyplot as plt
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
N_RES = 300                 # Medium res for pathfinding speed
K_REALITY = 1.0
CHAOS_DAMPING = 5.0
SEARCH_RADIUS_PX = 40       # Max distance to look for a neighbor (approx 20-30 degrees)
COST_THRESHOLD = 20.0       # Max "Friction" allowed for a valid wake connection

# ======================
# 1. OPTIMIZED ENGINE
# ======================

def get_alms_and_coords(fits_path, lmax, n_res):
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
    
    n_theta_alm = lmax * 3; n_phi_alm = lmax * 4
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
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta_vec = np.linspace(0, np.pi, n_res)
    phi_vec = np.linspace(-np.pi, np.pi, n_res)
    TH, PH = np.meshgrid(theta_vec, phi_vec, indexing='ij')
    return alms, theta_vec, phi_vec

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
# 2. FLUID PATHFINDING
# ======================

def find_universes(field, neighborhood_size=20):
    field_norm = (field - field.min()) / (field.max() - field.min())
    local_max = maximum_filter(field_norm, size=neighborhood_size) == field_norm
    peak_values = field_norm[local_max]
    threshold = np.percentile(peak_values, 50) 
    return (local_max) & (field_norm > threshold)

def trace_wake(start_node, end_node, cost_map):
    """
    Finds the 'Least Resistance' path through the Chaos Magma.
    Uses 'route_through_array' (Dijkstra-like).
    """
    # Wrap coordinates logic is hard for Dijkstra on flat array.
    # We will just clip for now to avoid crashes.
    
    # Crop a sub-region to speed up pathfinding
    r0, c0 = start_node
    r1, c1 = end_node
    
    rmin, rmax = min(r0, r1), max(r0, r1)
    cmin, cmax = min(c0, c1), max(c0, c1)
    
    pad = 10
    rmin = max(0, rmin-pad); rmax = min(cost_map.shape[0]-1, rmax+pad)
    cmin = max(0, cmin-pad); cmax = min(cost_map.shape[1]-1, cmax+pad)
    
    # Extract Sub-Cost Map
    sub_cost = cost_map[rmin:rmax, cmin:cmax]
    
    # Local coords
    start_local = (r0 - rmin, c0 - cmin)
    end_local = (r1 - rmin, c1 - cmin)
    
    try:
        indices, weight = route_through_array(sub_cost, start_local, end_local)
        # Convert back to global
        global_indices = np.array(indices) + np.array([rmin, cmin])
        return global_indices, weight
    except:
        return None, 99999

# ======================
# 3. MAIN
# ======================

def run_wake_topology():
    alms, theta_vec, phi_vec = get_alms_and_coords(FITS_PATH, LMAX, N_RES)
    profiles, m_range = precompute_profiles(alms, LMAX, theta_vec)
    
    print(f"[*] Synthesizing The 'Magma' (Substrate)...")
    map_sub = synthesize_band(profiles['Substrate'], m_range, phi_vec, K_REALITY)
    chaos_sub = get_gradient_magnitude(map_sub)
    chaos_norm = (chaos_sub - chaos_sub.min()) / (chaos_sub.max() - chaos_sub.min())
    
    # CREATE FRICTION MAP (Inverted Chaos)
    # High Chaos (1.0) -> Low Friction (0.01)
    # Low Chaos (0.0) -> High Friction (1.0)
    friction_map = 1.0 - chaos_norm + 0.01 
    
    print(f"[*] Identifying Turning Points (Universes)...")
    map_10 = synthesize_band(profiles['L10'], m_range, phi_vec, K_REALITY)
    chaos_10 = get_gradient_magnitude(map_10)
    clean_10 = map_10 * np.exp(-CHAOS_DAMPING * (chaos_10/np.max(chaos_10)))
    
    map_20 = synthesize_band(profiles['L20'], m_range, phi_vec, K_REALITY)
    chaos_20 = get_gradient_magnitude(map_20)
    clean_20 = map_20 * np.exp(-CHAOS_DAMPING * (chaos_20/np.max(chaos_20)))
    
    mask_10 = find_universes(clean_10, 15)
    mask_20 = find_universes(clean_20, 10)
    
    y10, x10 = np.where(mask_10); y20, x20 = np.where(mask_20)
    nodes = np.vstack((np.column_stack((y10, x10)), np.column_stack((y20, x20))))
    print(f"   -> Found {len(nodes)} anchors.")
    
    print(f"[*] Tracing Fluid Wakes (This may take a moment)...")
    valid_paths = []
    
    # Naive connectivity: check neighbors
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            p1 = nodes[i]; p2 = nodes[j]
            dist = np.hypot(p2[0]-p1[0], p2[1]-p1[1])
            
            if dist < SEARCH_RADIUS_PX:
                path_idx, cost = trace_wake(p1, p2, friction_map)
                
                # Check "Efficiency": Cost per pixel
                # If path is long but follows magma, cost is low.
                # If path crosses void, cost is high.
                if cost < COST_THRESHOLD:
                    valid_paths.append(path_idx)

    print(f"   -> Traced {len(valid_paths)} valid wake filaments.")

    # Plotting
    fig = plt.figure(figsize=(14, 8), facecolor='#050505')
    
    # 1. Background: The Magma
    plt.imshow(chaos_norm, origin='lower', cmap='inferno', alpha=0.4, extent=[0, N_RES, 0, N_RES])
    
    # 2. The Wakes (Curved Paths)
    for path in valid_paths:
        py, px = path[:, 0], path[:, 1]
        plt.plot(px, py, color='cyan', linewidth=1.2, alpha=0.6)
        
    # 3. The Anchors
    plt.scatter(x10, y10, c='white', s=20, edgecolors='none', zorder=10, alpha=0.8)
    plt.scatter(x20, y20, c='yellow', s=10, edgecolors='none', zorder=10, alpha=0.8)
    
    plt.title(f"THE WAKE TOPOLOGY: Tracing the Stirring Patterns\n(Cyan = Fluid Paths of Least Resistance)", 
              color='white', fontsize=14)
    plt.axis('off')
    
    plt.savefig("cmb_wake_topology.png", dpi=120, bbox_inches='tight', facecolor='#050505')
    print("✅ Wakes Traced. Saved to cmb_wake_topology.png")

if __name__ == "__main__":
    run_wake_topology()