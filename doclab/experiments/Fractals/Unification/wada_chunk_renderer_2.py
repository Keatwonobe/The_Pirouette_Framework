import numpy as np
import struct
import matplotlib.pyplot as plt
from numba import njit, prange

# ==========================================
# 1. THE GEOMETRY ENGINE
# ==========================================

@njit(fastmath=True)
def get_basin_single(m, l, t_max=60.0, dt=0.05, escape_r2=16.0):
    pm, pl = 0.0, 0.0
    steps = int(t_max / dt)
    sigma = 1.0
    for _ in range(steps):
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        m += dt * pm; l += dt * pl
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        if m*m + l*l > escape_r2:
            angle = np.arctan2(l, m)
            if angle > 0.5 and angle < 2.6: return 1
            elif angle <= -2.6 or angle >= 2.6: return 2
            else: return 3
    return 0

@njit(parallel=True, fastmath=True)
def generate_oracle_map(res, zoom):
    out_map = np.zeros((res, res), dtype=np.int8)
    cx = (res - 1) / 2.0; cy = (res - 1) / 2.0; scale = (2.0 * zoom) / res
    deg120 = 2.094395; deg240 = 4.188790
    for y in prange(res):
        for x in range(res):
            px = (x - cx) * scale; py = (y - cy) * scale
            r = np.sqrt(px*px + py*py); theta = np.arctan2(py, px)
            if theta < 0: theta += 2*np.pi
            rot = 0
            if theta >= deg240: theta -= deg240; rot = 2
            elif theta >= deg120: theta -= deg120; rot = 1
            eff_px = r * np.cos(theta); eff_py = r * np.sin(theta)
            basin = get_basin_single(eff_px, eff_py)
            if basin != 0: out_map[y, x] = (basin - 1 + rot) % 3 + 1
    return out_map

# ==========================================
# 2. THE SCANNER
# ==========================================

def extract_layer_points(zoom, res=800, max_points=5000):
    """
    Extracts the 'Skeleton' (Boundaries) from a specific zoom level.
    """
    # Generate Map
    oracle = generate_oracle_map(res, zoom)
    
    # Detect Boundaries
    grad_x = np.abs(np.diff(oracle, axis=1, append=oracle[:, -1:]))
    grad_y = np.abs(np.diff(oracle, axis=0, append=oracle[-1:, :]))
    boundaries = (grad_x + grad_y) > 0
    
    # Get Coordinates
    y_idxs, x_idxs = np.where(boundaries)
    
    # Downsample if too dense (for file size sanity)
    if len(x_idxs) > max_points:
        choice = np.random.choice(len(x_idxs), max_points, replace=False)
        x_idxs = x_idxs[choice]
        y_idxs = y_idxs[choice]
        
    # Convert to physical coords
    scale = (2.0 * zoom) / res
    cx, cy = res/2, res/2
    phys_x = (x_idxs - cx) * scale
    phys_y = (y_idxs - cy) * scale
    
    return phys_x, phys_y

# ==========================================
# 3. THE EXPORTER
# ==========================================

def save_to_ply(filename, points_x, points_y, points_z):
    """
    Saves points to a Binary PLY file with color mapping based on Z-depth.
    """
    n_points = len(points_x)
    print(f"[-] Writing {n_points} points to {filename}...")
    
    # Prepare Colors (Magma Colormap based on Z)
    # Z is roughly 0.1 to 3.0 (or inverted log). Normalize to 0-1
    z_min, z_max = np.min(points_z), np.max(points_z)
    z_norm = (points_z - z_min) / (z_max - z_min + 1e-9)
    
    # Use Matplotlib to get RGB values
    cmap = plt.get_cmap('magma')
    colors = cmap(z_norm)[:, :3] # Get RGB, drop Alpha
    colors = (colors * 255).astype(np.uint8)
    
    with open(filename, 'wb') as f:
        # Header
        header = f"""ply
format binary_little_endian 1.0
element vertex {n_points}
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
"""
        f.write(header.encode('ascii'))
        
        # Data (Interleaved x, y, z, r, g, b)
        # We use struct.pack for efficiency or numpy tobytes
        # Construct structured array
        data = np.zeros(n_points, dtype=[
            ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
            ('r', 'u1'), ('g', 'u1'), ('b', 'u1')
        ])
        
        data['x'] = points_x
        data['y'] = points_y
        data['z'] = points_z
        data['r'] = colors[:, 0]
        data['g'] = colors[:, 1]
        data['b'] = colors[:, 2]
        
        f.write(data.tobytes())
        
    print(f"[+] Saved successfully.")

# ==========================================
# 4. EXECUTION
# ==========================================

LAYERS = 600
ZOOM_START = 0.5
ZOOM_END = 5.0
POINTS_PER_LAYER = 8000
OUTPUT_FILE = "wada_chaos_skeleton.ply"

print(f"[-] Starting Tomographic Scan ({LAYERS} layers)...")

all_x = []
all_y = []
all_z = []

# Logarithmic spacing
zooms = np.logspace(np.log10(ZOOM_START), np.log10(ZOOM_END), LAYERS)

for i, z_level in enumerate(zooms):
    if i % 10 == 0: print(f"    Scanning Layer {i}/{LAYERS} (Zoom={z_level:.4f})...")
    
    xs, ys = extract_layer_points(z_level, res=1000, max_points=POINTS_PER_LAYER)
    
    # Z-Axis: We use -log(zoom) so 'Zoom In' = 'Go Down'
    z_val = -np.log10(z_level) * 2.0 # Scale Z for visual drama
    zs = np.full_like(xs, z_val)
    
    all_x.append(xs)
    all_y.append(ys)
    all_z.append(zs)

# Flatten
X = np.concatenate(all_x)
Y = np.concatenate(all_y)
Z = np.concatenate(all_z)

# Export
save_to_ply(OUTPUT_FILE, X, Y, Z)