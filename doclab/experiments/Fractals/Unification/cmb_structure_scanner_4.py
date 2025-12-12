import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.spatial import Delaunay
from scipy.ndimage import maximum_filter
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 400
K_REALITY = 1.0
CHAOS_DAMPING = 5.0
PATHWAY_THRESHOLD = 0.4  # Minimum average chaos required to validate an edge (0-1)

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
    return alms, theta_vec, phi_vec, TH, PH

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
# 2. TRIANGULATION LOGIC
# ======================

def find_universes(field, neighborhood_size=20):
    field_norm = (field - field.min()) / (field.max() - field.min())
    local_max = maximum_filter(field_norm, size=neighborhood_size) == field_norm
    peak_values = field_norm[local_max]
    threshold = np.percentile(peak_values, 50) 
    return (local_max) & (field_norm > threshold)

def check_pathway_strength(p1, p2, chaos_map):
    """ Samples the chaos map along the line segment p1-p2 """
    num_samples = int(np.hypot(p2[0]-p1[0], p2[1]-p1[1]))
    if num_samples < 2: return 0
    y_vals = np.linspace(p1[0], p2[0], num_samples).astype(int)
    x_vals = np.linspace(p1[1], p2[1], num_samples).astype(int)
    
    # Wrap boundaries
    y_vals = np.clip(y_vals, 0, chaos_map.shape[0]-1)
    x_vals = x_vals % chaos_map.shape[1]
    
    samples = chaos_map[y_vals, x_vals]
    return np.mean(samples)

def calculate_circulation(p1, p2, p3, field):
    """ Calculates Curl (Line Integral) around the triangle p1->p2->p3->p1 """
    # Simplification: Sum of (Value_next - Value_curr) along edges isn't quite curl.
    # We want Circulation of Gradient flow.
    # Curl = Sum( (Field_gradient dot Edge_Vector) )
    
    points = [p1, p2, p3]
    circulation = 0
    
    gy, gx = np.gradient(field)
    
    for i in range(3):
        start = points[i]; end = points[(i+1)%3]
        
        # Midpoint of edge
        mid_y = int((start[0] + end[0])/2)
        mid_x = int((start[1] + end[1])/2)
        
        # Wrap
        mid_y = np.clip(mid_y, 0, field.shape[0]-1)
        mid_x = mid_x % field.shape[1]
        
        # Gradient at midpoint
        grad_vector = np.array([gy[mid_y, mid_x], gx[mid_y, mid_x]])
        
        # Edge vector
        edge_vector = np.array([end[0]-start[0], end[1]-start[1]])
        
        circulation += np.dot(grad_vector, edge_vector)
        
    return circulation

# ======================
# 3. MAIN
# ======================

def run_orbiter_test():
    alms, theta_vec, phi_vec, TH, PH = get_alms_and_coords(FITS_PATH, LMAX, N_RES)
    profiles, m_range = precompute_profiles(alms, LMAX, theta_vec)
    
    print(f"[*] Synthesizing Reality...")
    map_10 = synthesize_band(profiles['L10'], m_range, phi_vec, K_REALITY)
    map_20 = synthesize_band(profiles['L20'], m_range, phi_vec, K_REALITY)
    
    chaos_10 = get_gradient_magnitude(map_10)
    chaos_20 = get_gradient_magnitude(map_20)
    
    # Clean Maps
    clean_10 = map_10 * np.exp(-CHAOS_DAMPING * (chaos_10/np.max(chaos_10)))
    clean_20 = map_20 * np.exp(-CHAOS_DAMPING * (chaos_20/np.max(chaos_20)))
    
    # Substrate (Traveler Pathways)
    map_sub = synthesize_band(profiles['Substrate'], m_range, phi_vec, K_REALITY)
    chaos_sub = get_gradient_magnitude(map_sub)
    chaos_sub_norm = (chaos_sub - chaos_sub.min()) / (chaos_sub.max() - chaos_sub.min())
    
    # Find Vertices
    print("[*] Detecting Vertices (Quarks)...")
    mask_10 = find_universes(clean_10, 15)
    mask_20 = find_universes(clean_20, 10)
    
    y10, x10 = np.where(mask_10); y20, x20 = np.where(mask_20)
    points = np.vstack((np.column_stack((y10, x10)), np.column_stack((y20, x20))))
    
    print(f"   -> Found {len(points)} vertices.")
    
    # Delaunay Triangulation
    tri = Delaunay(points)
    simplices = tri.simplices
    
    print("[*] Validating Triangles (Check Pathway Strength)...")
    valid_triangles = []
    circulations = []
    
    for simplex in simplices:
        p1, p2, p3 = points[simplex[0]], points[simplex[1]], points[simplex[2]]
        
        # Check if all edges lie on High Chaos (Traveler Pathways)
        s1 = check_pathway_strength(p1, p2, chaos_sub_norm)
        s2 = check_pathway_strength(p2, p3, chaos_sub_norm)
        s3 = check_pathway_strength(p3, p1, chaos_sub_norm)
        
        avg_strength = (s1 + s2 + s3) / 3.0
        
        if avg_strength > PATHWAY_THRESHOLD:
            # Calculate Circulation
            circ = calculate_circulation(p1, p2, p3, map_sub)
            valid_triangles.append((p1, p2, p3))
            circulations.append(circ)
            
    print(f"   -> {len(valid_triangles)} Triangles formed on Traveler Pathways.")
    
    # Plot
    fig = plt.figure(figsize=(14, 8), facecolor='#050505')
    ax = plt.gca()
    
    # Background: The Traveler Chaos
    plt.imshow(chaos_sub_norm, origin='lower', cmap='gray', alpha=0.5, extent=[0, N_RES, 0, N_RES])
    
    # Plot Triangles
    cw_count = 0
    ccw_count = 0
    
    for triangle, circ in zip(valid_triangles, circulations):
        p1, p2, p3 = triangle
        ys = [p1[0], p2[0], p3[0], p1[0]]
        xs = [p1[1], p2[1], p3[1], p1[1]]
        
        # Color by Circulation Direction (Chirality)
        color = 'cyan' if circ > 0 else 'magenta' 
        if circ > 0: cw_count += 1
        else: ccw_count += 1
        
        # Line width by strength of circulation
        lw = min(3, max(0.5, abs(circ) * 0.1))
        
        plt.plot(xs, ys, color=color, linewidth=lw, alpha=0.8)
        
        # Centroid Marker
        cy = np.mean(ys[:3])
        cx = np.mean(xs[:3])
        # plt.text(cx, cy, f"{circ:.1f}", color=color, fontsize=6, ha='center')

    plt.title(f"THE TRIANGULAR ORBITER: Chromodynamic Topology\nCyan = CW Orbit ({cw_count}) | Magenta = CCW Orbit ({ccw_count})", 
              color='white', fontsize=14)
    plt.axis('off')
    
    # Asymmetry Stats
    print("\n" + "="*40)
    print("      CHIRALITY & ASYMMETRY REPORT      ")
    print("="*40)
    print(f"Total Triangles: {len(valid_triangles)}")
    print(f"Clockwise (CW):  {cw_count}")
    print(f"Counter-CW:      {ccw_count}")
    print(f"Net Chirality:   {abs(cw_count - ccw_count)} (Imbalance)")
    print("-" * 40)
    
    plt.savefig("cmb_triangular_orbiter.png", dpi=120, bbox_inches='tight', facecolor='#050505')
    print("✅ Experiment Complete. Saved to cmb_triangular_orbiter.png")

if __name__ == "__main__":
    run_orbiter_test()