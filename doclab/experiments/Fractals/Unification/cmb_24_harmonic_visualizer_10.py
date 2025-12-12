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
N_RES = 400
HEADING_L = 51.8
HEADING_B = -72.9
SEARCH_RADIUS_PX = 50
COST_THRESHOLD = 25.0

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
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, TH_GRID, PH_GRID, theta, phi

def synthesize_fields(alms, TH, PH):
    field = np.zeros_like(TH, dtype=np.complex128)
    for l in range(LMAX + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            Y_lm = sph_harm(m, l, PH, TH)
            field += alms[(l, m)] * Y_lm
            
    # Structure = Real Field
    # Chaos = Gradient Magnitude
    gy, gx = np.gradient(field.real)
    chaos = np.sqrt(gx**2 + gy**2)
    return field.real, chaos

# ======================
# 2. CHIRALITY CALCULATOR
# ======================

def calculate_path_curvature(path):
    """
    Calculates the cumulative 'turning' of a path.
    Positive = Counter-Clockwise (Left)
    Negative = Clockwise (Right)
    """
    if len(path) < 5: return 0
    
    curvature_sum = 0
    
    # We look at 3 points at a time: p1, p2, p3
    for i in range(len(path) - 2):
        p1 = path[i]
        p2 = path[i+1]
        p3 = path[i+2]
        
        # Vectors
        v1 = p2 - p1
        v2 = p3 - p2
        
        # Normalize
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0: continue
        
        # 2D Cross Product (determinant)
        # cp = x1*y2 - y1*x2
        # Note: Image coords (row, col) map to (y, x) but orientation matters
        # Let's stick to standard vector math: p = [r, c] -> v = [dr, dc]
        cross_prod = v1[0]*v2[1] - v1[1]*v2[0]
        
        # Angle
        # sin(theta) = cross / (mag1 * mag2)
        curvature_sum += cross_prod # Accumulate the turn
        
    return curvature_sum

def trace_and_measure(nodes, cost_map):
    paths = []
    chiralities = []
    
    print(f"[*] Tracing filaments between {len(nodes)} nodes...")
    
    # Iterate through node pairs
    # Limit to nearest neighbors to save time
    for i in range(len(nodes)):
        r0, c0 = nodes[i]
        
        # Look for other nodes within search radius
        for j in range(len(nodes)):
            if i == j: continue
            r1, c1 = nodes[j]
            
            dist = np.hypot(r1-r0, c1-c0)
            if dist > SEARCH_RADIUS_PX: continue
            
            # Trace
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
                if weight < COST_THRESHOLD:
                    # Convert back to global
                    global_path = np.array(indices) + np.array([rmin, cmin])
                    
                    # MEASURE CHIRALITY
                    chirality = calculate_path_curvature(global_path)
                    
                    paths.append(global_path)
                    chiralities.append(chirality)
            except:
                continue
                
    return paths, np.array(chiralities)

# ======================
# 3. MAIN
# ======================

def run_chirality_test():
    alms, TH, PH, th_vec, ph_vec = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    structure, chaos = synthesize_fields(alms, TH, PH)
    
    # 1. Prepare Maps
    chaos_norm = (chaos - chaos.min()) / (chaos.max() - chaos.min())
    friction_map = 1.0 - chaos_norm + 0.01 # Paths like to follow the "Ridge" (Low Chaos? Or High Structure?)
    # Usually filaments follow structure ridges. 
    # Let's invert: Paths follow HIGH Structure (Low Cost)
    struct_norm = (structure - structure.min()) / (structure.max() - structure.min())
    cost_map = 1.0 - struct_norm + 0.01
    
    # 2. Find Nodes (The Lattice Vertices)
    # Using the same logic as your Lattice Decoder
    threshold = np.percentile(struct_norm, 99.0)
    local_max = maximum_filter(struct_norm, size=15) == struct_norm
    mask = (local_max) & (struct_norm > threshold)
    y_nodes, x_nodes = np.where(mask)
    nodes = np.column_stack((y_nodes, x_nodes))
    
    # 3. Measure Wakes
    paths, curls = trace_and_measure(nodes, cost_map)
    
    # 4. Analyze Results
    left_twist = curls[curls > 5]  # Threshold to ignore straight lines
    right_twist = curls[curls < -5]
    neutral = curls[(curls >= -5) & (curls <= 5)]
    
    n_left = len(left_twist)
    n_right = len(right_twist)
    total_sig = n_left + n_right
    bias = (n_left - n_right) / total_sig if total_sig > 0 else 0
    
    print(f"[*] RESULTS:")
    print(f"    Total Filaments: {len(paths)}")
    print(f"    Left-Handed (CCW): {n_left}")
    print(f"    Right-Handed (CW): {n_right}")
    print(f"    Chiral Bias: {bias:.3f} (Pos=Left, Neg=Right)")
    
    # --- PLOTTING ---
    fig = plt.figure(figsize=(12, 12), facecolor='#050505')
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    
    # Panel 1: The Chiral Network
    ax_map = plt.subplot(gs[0])
    ax_map.imshow(chaos_norm, origin='lower', cmap='gray', alpha=0.4, extent=[-180, 180, -90, 90])
    
    for i, path in enumerate(paths):
        py, px = path[:, 0], path[:, 1]
        lon = (px / N_RES) * 360 - 180
        lat = (py / N_RES) * 180 - 90
        
        c_val = curls[i]
        if c_val > 5: color = 'cyan'   # Left/CCW
        elif c_val < -5: color = 'magenta' # Right/CW
        else: color = 'yellow' # Straight
        
        ax_map.plot(lon, lat, color=color, linewidth=0.8, alpha=0.6)
        
    ax_map.set_title(f"THE CHIRAL SKELETON | Bias: {bias:.2f}", color='white', fontsize=14)
    # Add Legend
    ax_map.plot([],[], color='cyan', label=f'Left Twist ({n_left})')
    ax_map.plot([],[], color='magenta', label=f'Right Twist ({n_right})')
    ax_map.legend(loc='upper right', facecolor='black', labelcolor='white')
    ax_map.axis('off')
    
    # Panel 2: The Bias Histogram
    ax_hist = plt.subplot(gs[1])
    ax_hist.set_facecolor('#111')
    
    ax_hist.hist(curls, bins=50, range=(-100, 100), color='white', alpha=0.3)
    # Colorize bars manually? Hard with hist. Just overlay areas.
    ax_hist.axvspan(5, 100, color='cyan', alpha=0.2, label='Left-Handed')
    ax_hist.axvspan(-100, -5, color='magenta', alpha=0.2, label='Right-Handed')
    
    ax_hist.set_title("WAKE CURVATURE DISTRIBUTION (Coriolis Signature)", color='white', fontsize=10)
    ax_hist.set_xlabel("Filament Curvature (Negative=CW, Positive=CCW)", color='gray')
    ax_hist.legend()
    ax_hist.tick_params(colors='gray')
    
    plt.tight_layout()
    plt.savefig("cmb_chiral_anomaly.png", dpi=100, facecolor='#050505')
    print("✅ Chirality Test Complete. Saved to cmb_chiral_anomaly.png")

if __name__ == "__main__":
    run_chirality_test()