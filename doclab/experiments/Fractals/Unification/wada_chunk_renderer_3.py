import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange

# ==========================================
# 1. THE PHYSICS KERNEL
# ==========================================
# (Standard Wada Integrator)

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
def generate_oracle_map_centered(res, zoom, center_x, center_y):
    # Modified to accept a dynamic center point
    out_map = np.zeros((res, res), dtype=np.int8)
    
    # Grid centered on (0,0) relative to the image
    img_cx = (res - 1) / 2.0
    img_cy = (res - 1) / 2.0
    scale = (2.0 * zoom) / res
    
    for y in prange(res):
        for x in range(res):
            # Map pixel to physical space, adding the offset
            px = (x - img_cx) * scale + center_x
            py = (y - img_cy) * scale + center_y
            
            r = np.sqrt(px*px + py*py); theta = np.arctan2(py, px)
            if theta < 0: theta += 2*np.pi
            
            # Symmetry Fold
            deg120 = 2.094395; deg240 = 4.188790
            rot = 0
            if theta >= deg240: theta -= deg240; rot = 2
            elif theta >= deg120: theta -= deg120; rot = 1
            eff_px = r * np.cos(theta); eff_py = r * np.sin(theta)
            
            basin = get_basin_single(eff_px, eff_py)
            if basin != 0: out_map[y, x] = (basin - 1 + rot) % 3 + 1
            
    return out_map

# ==========================================
# 2. THE TRACKING SCANNER
# ==========================================

def extract_layer_adaptive(zoom, center_x, center_y, res=500, max_points=4000):
    """
    1. Scans a window.
    2. Identifies chaos.
    3. Returns points AND the new center of mass for the next layer.
    """
    # Generate Map
    oracle = generate_oracle_map_centered(res, zoom, center_x, center_y)
    
    # Detect Boundaries
    grad_x = np.abs(np.diff(oracle, axis=1, append=oracle[:, -1:]))
    grad_y = np.abs(np.diff(oracle, axis=0, append=oracle[-1:, :]))
    boundaries = (grad_x + grad_y) > 0
    
    y_idxs, x_idxs = np.where(boundaries)
    
    if len(x_idxs) == 0:
        return np.array([]), np.array([]), center_x, center_y # Lost the signal
        
    # CALCULATE NEW CENTER OF MASS (Physics Tracking)
    # We want to keep the camera pointed at the densest part of the chaos
    img_cx = res / 2.0
    img_cy = res / 2.0
    
    avg_px = np.mean(x_idxs)
    avg_py = np.mean(y_idxs)
    
    scale = (2.0 * zoom) / res
    
    # Calculate drift in physical units
    drift_x = (avg_px - img_cx) * scale
    drift_y = (avg_py - img_cy) * scale
    
    # Update the global center for the NEXT frame
    new_center_x = center_x + drift_x
    new_center_y = center_y + drift_y
    
    # Extract Points for THIS frame
    if len(x_idxs) > max_points:
        choice = np.random.choice(len(x_idxs), max_points, replace=False)
        x_idxs = x_idxs[choice]
        y_idxs = y_idxs[choice]
        
    phys_x = (x_idxs - img_cx) * scale + center_x
    phys_y = (y_idxs - img_cy) * scale + center_y
    
    return phys_x, phys_y, new_center_x, new_center_y

# ==========================================
# 3. EXPORT LOGIC
# ==========================================

def save_to_ply_colored(filename, x, y, z):
    n = len(x)
    print(f"[-] Writing {n} points to {filename}...")
    
    # Color based on twist (Angle around Z axis)
    # This emphasizes the braiding structure of the spike
    angles = np.arctan2(y, x)
    # Normalize -pi,pi to 0,1
    norm_a = (angles + np.pi) / (2*np.pi)
    
    cmap = plt.get_cmap('hsv') # Rainbow for rotation
    colors = cmap(norm_a)[:, :3]
    colors = (colors * 255).astype(np.uint8)
    
    with open(filename, 'wb') as f:
        header = f"""ply
format binary_little_endian 1.0
element vertex {n}
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
"""
        f.write(header.encode('ascii'))
        data = np.zeros(n, dtype=[('x','f4'),('y','f4'),('z','f4'),('r','u1'),('g','u1'),('b','u1')])
        data['x'] = x; data['y'] = y; data['z'] = z
        data['r'] = colors[:,0]; data['g'] = colors[:,1]; data['b'] = colors[:,2]
        f.write(data.tobytes())
    print("[+] Saved.")

# ==========================================
# 4. EXECUTION: DRILLING THE SPIKE
# ==========================================

LAYERS = 600
ZOOM_START = 30.0   # Macro (Base)
ZOOM_END = 0.005   # Micro (Tip) - Going very deep!

# Initial tracking position
cx, cy = 0.0, 0.0

all_x, all_y, all_z = [], [], []

# Logspace for smooth zoom
zooms = np.logspace(np.log10(ZOOM_START), np.log10(ZOOM_END), LAYERS)

print(f"[-] Starting Auto-Tracking Drill...")

for i, z_level in enumerate(zooms):
    # Run the adaptive scanner
    xs, ys, new_cx, new_cy = extract_layer_adaptive(z_level, cx, cy, res=800, max_points=3000)
    
    if len(xs) > 0:
        # Z-depth: We stretch it out to visualize the braid
        z_depth = i * 0.1 
        zs = np.full_like(xs, z_depth)
        
        all_x.append(xs)
        all_y.append(ys)
        all_z.append(zs)
        
        # Update tracking for next layer
        # Damping factor to prevent camera jitter
        cx = cx * 0.2 + new_cx * 0.8
        cy = cy * 0.2 + new_cy * 0.8
    
    if i % 20 == 0:
        print(f"    Layer {i}: Zoom={z_level:.4f} | Tracking Center=({cx:.4f}, {cy:.4f})")

X = np.concatenate(all_x)
Y = np.concatenate(all_y)
Z = np.concatenate(all_z)

save_to_ply_colored("wada_spike_drill.ply", X, Y, Z)