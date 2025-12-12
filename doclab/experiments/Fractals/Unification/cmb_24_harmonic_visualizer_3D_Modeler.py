import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import maximum_filter
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 512                 # High resolution for dense point cloud
K_REALITY = 1.0
HEADING_L = 51.8
HEADING_B = -72.9

# ======================
# 1. ENGINE
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
            try: 
                Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            except: 
                # Fallback for newer SciPy
                from scipy.special import sph_harm as sh
                Y_lm = sh(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, TH_GRID, PH_GRID

def synthesize_fields(alms, TH, PH):
    field = np.zeros_like(TH, dtype=np.complex128)
    for l in range(LMAX + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            try: 
                Y_lm = sph_harm(m, l, PH, TH)
            except:
                from scipy.special import sph_harm as sh
                Y_lm = sh(m, l, PH, TH)
            field += alms[(l, m)] * Y_lm
            
    gy, gx = np.gradient(field.real)
    chaos = np.sqrt(gx**2 + gy**2)
    structure = field.real
    return structure, chaos

# ======================
# 2. PLY EXPORTER
# ======================

def save_ply(filename, points, colors=None):
    """
    Saves a point cloud to a PLY file (ASCII format).
    """
    print(f"[*] Writing {filename} ({len(points)} points)...")
    
    header = "ply\n"
    header += "format ascii 1.0\n"
    header += f"element vertex {len(points)}\n"
    header += "property float x\n"
    header += "property float y\n"
    header += "property float z\n"
    if colors is not None:
        header += "property uchar red\n"
        header += "property uchar green\n"
        header += "property uchar blue\n"
    header += "end_header\n"
    
    with open(filename, "w") as f:
        f.write(header)
        for i in range(len(points)):
            x, y, z = points[i]
            if colors is not None:
                r, g, b = colors[i]
                f.write(f"{x:.6f} {y:.6f} {z:.6f} {int(r)} {int(g)} {int(b)}\n")
            else:
                f.write(f"{x:.6f} {y:.6f} {z:.6f}\n")

# ======================
# 3. MAIN
# ======================

def run_exporter():
    alms, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    structure, chaos = synthesize_fields(alms, TH, PH)
    
    # Normalize Maps
    s_norm = (structure - structure.min()) / (structure.max() - structure.min())
    c_norm = (chaos - chaos.min()) / (chaos.max() - chaos.min())
    
    # --- 1. THE HULL (Deformed Sphere) ---
    print("[*] Generating Hull Geometry...")
    R_BASE = 1.0
    R_AMP = 0.3
    R = R_BASE + R_AMP * s_norm
    
    # Convert Spherical to Cartesian
    # x = R * sin(theta) * cos(phi)
    x = (R * np.sin(TH) * np.cos(PH)).flatten()
    y = (R * np.sin(TH) * np.sin(PH)).flatten()
    z = (R * np.cos(TH)).flatten()
    
    # Map Chaos to Colors (Inferno)
    cmap = plt.cm.inferno(c_norm.flatten())
    colors = (cmap[:, :3] * 255).astype(int)
    
    hull_points = np.column_stack((x, y, z))
    save_ply("cmb_particle_hull.ply", hull_points, colors)
    
    # --- 2. THE SKELETON (Nodes) ---
    print("[*] Extracting Skeleton Nodes...")
    # Find peaks in structure (Top 1.5%)
    threshold = np.percentile(s_norm, 98.5)
    local_max = maximum_filter(s_norm, size=15) == s_norm
    mask = (local_max) & (s_norm > threshold)
    
    # Elevate nodes slightly so they are visible above the hull
    R_node = R[mask] * 1.05 
    th_node = TH[mask]
    ph_node = PH[mask]
    
    xn = R_node * np.sin(th_node) * np.cos(ph_node)
    yn = R_node * np.sin(th_node) * np.sin(ph_node)
    zn = R_node * np.cos(th_node)
    
    node_points = np.column_stack((xn, yn, zn))
    # Cyan Color for Nodes
    node_colors = np.tile([0, 255, 255], (len(node_points), 1))
    
    save_ply("cmb_particle_nodes.ply", node_points, node_colors)
    
    # --- 3. MOTION VECTOR (Line) ---
    print("[*] Generating Motion Vector...")
    # Convert Heading (Galactic l,b) to vector
    th_h = np.deg2rad(90 - HEADING_B)
    ph_h = np.deg2rad(HEADING_L)
    
    # Length = 2.5x Radius
    vx = np.sin(th_h) * np.cos(ph_h) * 2.5
    vy = np.sin(th_h) * np.sin(ph_h) * 2.5
    vz = np.cos(th_h) * 2.5
    
    # Create line points
    t_line = np.linspace(0, 1, 100)
    lx = vx * t_line
    ly = vy * t_line
    lz = vz * t_line
    
    line_points = np.column_stack((lx, ly, lz))
    line_colors = np.tile([255, 255, 0], (len(line_points), 1)) # Yellow
    
    save_ply("cmb_particle_motion.ply", line_points, line_colors)
    
    print("✅ Export Complete. Files saved: hull.ply, nodes.ply, motion.ply")

if __name__ == "__main__":
    run_exporter()