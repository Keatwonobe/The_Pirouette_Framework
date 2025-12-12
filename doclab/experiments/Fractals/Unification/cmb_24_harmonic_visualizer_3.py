import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import maximum_filter
from sklearn.manifold import MDS
from scipy.spatial import ConvexHull
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys
import warnings

# Suppress sklearn warnings for cleaner output
warnings.filterwarnings("ignore")

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 400
PEAK_THRESHOLD_PCT = 98.5   # Target the ~132 nodes
EMBEDDING_DIM = 3           # We unfold into 3D to visualize (mathematically it may be 4D)

# ======================
# 1. DATA ENGINE (Reused)
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
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, TH_GRID, PH_GRID

def synthesize_structure_map(alms, TH, PH):
    # Synthesize at K=1.0 (Reality)
    lmax = LMAX
    field = np.zeros_like(TH, dtype=np.complex128)
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            Y_lm = sph_harm(m, l, PH, TH)
            field += alms[(l, m)] * Y_lm
            
    # Calculate Gradient Energy (Structure)
    gy, gx = np.gradient(field.real)
    structure = np.sqrt(gx**2 + gy**2)
    return structure

# ======================
# 2. HYPER-UNFOLDER
# ======================

def extract_nodes_spherical(structure_map, n_res):
    # 1. Find Peaks
    f_norm = (structure_map - structure_map.min()) / (structure_map.max() - structure_map.min())
    threshold = np.percentile(f_norm, PEAK_THRESHOLD_PCT)
    local_max = maximum_filter(f_norm, size=15) == f_norm
    mask = (local_max) & (f_norm > threshold)
    y_idx, x_idx = np.where(mask)
    
    # 2. Convert to Spherical Coords (Radians)
    # Theta: 0 to pi (North to South)
    # Phi: -pi to pi (East to West)
    theta = np.linspace(0, np.pi, n_res)[y_idx]
    phi = np.linspace(-np.pi, np.pi, n_res)[x_idx]
    
    return theta, phi

def compute_geodesic_distance_matrix(theta, phi):
    """ Calculates the Great Circle distance between all pairs """
    n = len(theta)
    dist_matrix = np.zeros((n, n))
    
    # Convert to Cartesian Unit Vectors
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    vectors = np.column_stack((x, y, z))
    
    # Pairwise Dot Product
    # cos(angle) = v1 . v2
    dots = vectors @ vectors.T
    dots = np.clip(dots, -1.0, 1.0)
    
    # ArcCos to get angular distance
    dist_matrix = np.arccos(dots)
    return dist_matrix

def unfold_manifold(dist_matrix):
    """ Uses MDS to find the best 3D configuration that explains the surface distances """
    print(f"[*] Unfolding {len(dist_matrix)} nodes into 3D Space (MDS)...")
    
    # Metric MDS
    mds = MDS(n_components=EMBEDDING_DIM, dissimilarity='precomputed', random_state=42, max_iter=3000, eps=1e-6)
    embedding = mds.fit_transform(dist_matrix)
    
    stress = mds.stress_
    print(f"   -> Unfold Complete. Stress (Error): {stress:.4f}")
    return embedding

# ======================
# 3. MAIN
# ======================

def run_hyper_unfolder():
    alms, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    
    print(f"[*] Synthesizing Cosmic Structure...")
    structure_map = synthesize_structure_map(alms, TH, PH)
    
    theta, phi = extract_nodes_spherical(structure_map, N_RES)
    print(f"[*] Found {len(theta)} Nodes. Calculating Geodesics...")
    
    dist_matrix = compute_geodesic_distance_matrix(theta, phi)
    
    # The Unfolding
    embedding = unfold_manifold(dist_matrix)
    
    # --- VISUALIZATION ---
    fig = plt.figure(figsize=(14, 7), facecolor='#050505')
    
    # Panel 1: The Shadow (2D Map)
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(structure_map, origin='lower', cmap='magma', extent=[-180, 180, -90, 90])
    lon_deg = np.degrees(phi)
    lat_deg = np.degrees(np.pi/2 - theta) # Convert back to lat for plot
    ax1.scatter(lon_deg, lat_deg, c='cyan', s=15, edgecolors='none', alpha=0.8)
    ax1.set_title(f"THE SHADOW: {len(theta)} Nodes on 2D Sphere", color='white')
    ax1.axis('off')
    
    # Panel 2: The Object (3D Unfold)
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.set_facecolor('#050505')
    
    x, y, z = embedding[:, 0], embedding[:, 1], embedding[:, 2]
    
    # Plot Nodes
    ax2.scatter(x, y, z, c='cyan', s=30, alpha=0.9, depthshade=False)
    
    # Plot Hull / Connections
    # Draw lines between nearest neighbors in the 3D embedding to see the shape
    try:
        hull = ConvexHull(embedding)
        for simplex in hull.simplices:
            ax2.plot(x[simplex], y[simplex], z[simplex], 'w-', alpha=0.1)
    except:
        pass # Fallback if hull fails (e.g. coplanar)
        
    ax2.set_title("THE OBJECT: Unfolded Hyper-Polytope Geometry", color='white')
    ax2.set_axis_off()
    
    # Auto-rotate for best view (heuristic)
    ax2.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.savefig("cmb_hyper_unfolded.png", dpi=100, facecolor='#050505')
    print("✅ Unfolding Complete. Saved to cmb_hyper_unfolded.png")

if __name__ == "__main__":
    run_hyper_unfolder()