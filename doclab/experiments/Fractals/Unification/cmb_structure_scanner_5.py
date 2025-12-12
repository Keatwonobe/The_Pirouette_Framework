import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import maximum_filter
import astropy.units as u
from astropy.coordinates import SkyCoord
import networkx as nx
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 400
K_REALITY = 1.0
CHAOS_DAMPING = 5.0
RIDGE_THRESHOLD = 0.5   # Minimum average chaos to count as a "Rail" (0-1)
SEARCH_RADIUS = 60      # Max distance (pixels) to look for next jump

# ======================
# 1. ENGINE (Standardized)
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
# 2. ORBITAL PATHFINDER
# ======================

def find_universes(field, neighborhood_size=20):
    field_norm = (field - field.min()) / (field.max() - field.min())
    local_max = maximum_filter(field_norm, size=neighborhood_size) == field_norm
    peak_values = field_norm[local_max]
    threshold = np.percentile(peak_values, 50) 
    return (local_max) & (field_norm > threshold)

def check_rail_strength(p1, p2, chaos_map):
    """ Checks if the path p1->p2 follows a High Chaos Ridge """
    dist = np.hypot(p2[0]-p1[0], p2[1]-p1[1])
    num_samples = int(dist)
    if num_samples < 2: return 0
    
    y_vals = np.linspace(p1[0], p2[0], num_samples).astype(int)
    x_vals = np.linspace(p1[1], p2[1], num_samples).astype(int)
    
    # Wrap boundaries
    y_vals = np.clip(y_vals, 0, chaos_map.shape[0]-1)
    x_vals = x_vals % chaos_map.shape[1]
    
    samples = chaos_map[y_vals, x_vals]
    return np.mean(samples)

def trace_orbits(nodes, chaos_map):
    """ Builds a graph of connected universes and finds the longest orbits """
    G = nx.Graph()
    
    # Add nodes
    for i, n in enumerate(nodes):
        G.add_node(i, pos=n)
        
    print(f"[*] Tracing connections between {len(nodes)} nodes...")
    
    # Build Edges (The "Rails")
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            p1 = nodes[i]
            p2 = nodes[j]
            
            # Distance Check (Don't jump across the whole sky)
            dist = np.hypot(p2[0]-p1[0], p2[1]-p1[1])
            # Handle wrapping for distance roughly (simplified)
            if dist > SEARCH_RADIUS: continue
            
            # Chaos Rail Check
            strength = check_rail_strength(p1, p2, chaos_map)
            
            if strength > RIDGE_THRESHOLD:
                G.add_edge(i, j, weight=strength)
                
    # Find Connected Components (The Orbits)
    components = list(nx.connected_components(G))
    print(f"   -> Found {len(components)} orbital chains.")
    
    # Extract edges for plotting
    valid_edges = []
    for u_idx, v_idx in G.edges():
        valid_edges.append((nodes[u_idx], nodes[v_idx], G[u_idx][v_idx]['weight']))
        
    return valid_edges, nodes

# ======================
# 3. MAIN EXECUTION
# ======================

def run_orbital_pathfinder():
    alms, theta_vec, phi_vec = get_alms_and_coords(FITS_PATH, LMAX, N_RES)
    profiles, m_range = precompute_profiles(alms, LMAX, theta_vec)
    
    print(f"[*] Synthesizing Landscape...")
    
    # 1. The Beacons (Universes)
    map_10 = synthesize_band(profiles['L10'], m_range, phi_vec, K_REALITY)
    map_20 = synthesize_band(profiles['L20'], m_range, phi_vec, K_REALITY)
    
    chaos_10 = get_gradient_magnitude(map_10)
    chaos_20 = get_gradient_magnitude(map_20)
    
    clean_10 = map_10 * np.exp(-CHAOS_DAMPING * (chaos_10/np.max(chaos_10)))
    clean_20 = map_20 * np.exp(-CHAOS_DAMPING * (chaos_20/np.max(chaos_20)))
    
    mask_10 = find_universes(clean_10, 15)
    mask_20 = find_universes(clean_20, 10)
    
    # 2. The Terrain (Substrate Chaos)
    map_sub = synthesize_band(profiles['Substrate'], m_range, phi_vec, K_REALITY)
    chaos_sub = get_gradient_magnitude(map_sub)
    chaos_sub_norm = (chaos_sub - chaos_sub.min()) / (chaos_sub.max() - chaos_sub.min())
    
    # 3. Extract Node List
    y10, x10 = np.where(mask_10); y20, x20 = np.where(mask_20)
    nodes = np.vstack((np.column_stack((y10, x10)), np.column_stack((y20, x20))))
    
    # 4. TRACE THE ORBITS
    edges, all_nodes = trace_orbits(nodes, chaos_sub_norm)
    
    # 5. Plotting
    fig = plt.figure(figsize=(14, 8), facecolor='#050505')
    
    # Background: The "Magma" (Traveler Pathways)
    plt.imshow(chaos_sub_norm, origin='lower', cmap='gray', alpha=0.6, extent=[0, N_RES, 0, N_RES])
    
    # Plot The Rails (Yellow Lines)
    print("[*] plotting trajectories...")
    for p1, p2, strength in edges:
        ys = [p1[0], p2[0]]
        xs = [p1[1], p2[1]]
        
        # Color by strength (Brighter = Better Rail)
        alpha = min(1.0, strength + 0.2)
        plt.plot(xs, ys, color='gold', linewidth=2.0, alpha=alpha)
        
    # Plot The Beacons (Blue/Pink Dots)
    # Re-plot for clarity on top of lines
    plt.scatter(x10, y10, c='cyan', s=60, edgecolors='black', zorder=10, label='L10 Nodes')
    plt.scatter(x20, y20, c='magenta', s=30, zorder=10, label='L20 Nodes')
    
    plt.title(f"THE ORBITAL PATHFINDER: Tracing the Sawtooth Trajectory\n(Yellow = Valid Chaos Rails connecting Universes)", 
              color='white', fontsize=14)
    plt.legend(loc='upper right')
    plt.axis('off')
    
    plt.savefig("cmb_orbital_pathfinder.png", dpi=120, bbox_inches='tight', facecolor='#050505')
    print("✅ Orbit Traced. Saved to cmb_orbital_pathfinder.png")

if __name__ == "__main__":
    run_orbital_pathfinder()