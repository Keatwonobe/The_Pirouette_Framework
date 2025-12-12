import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import sys

# ==========================================
# 1. THE PHYSICS KERNEL
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
def generate_oracle_map_centered(res, zoom, center_x, center_y):
    out_map = np.zeros((res, res), dtype=np.int8)
    
    img_cx = (res - 1) / 2.0
    img_cy = (res - 1) / 2.0
    scale = (2.0 * zoom) / res
    
    for y in prange(res):
        for x in range(res):
            px = (x - img_cx) * scale + center_x
            py = (y - img_cy) * scale + center_y
            
            r = np.sqrt(px*px + py*py); theta = np.arctan2(py, px)
            if theta < 0: theta += 2*np.pi
            
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
    # Generate Map
    oracle = generate_oracle_map_centered(res, zoom, center_x, center_y)
    
    # Detect Boundaries
    grad_x = np.abs(np.diff(oracle, axis=1, append=oracle[:, -1:]))
    grad_y = np.abs(np.diff(oracle, axis=0, append=oracle[-1:, :]))
    boundaries = (grad_x + grad_y) > 0
    
    y_idxs, x_idxs = np.where(boundaries)
    count = len(x_idxs)
    
    if count == 0:
        return np.array([]), np.array([]), np.array([]), np.array([]), center_x, center_y, 0, 0.0, 0.0
        
    # --- TRACKING LOGIC ---
    img_cx = res / 2.0
    img_cy = res / 2.0
    scale = (2.0 * zoom) / res
    
    # Calculate drift based on center of mass of the boundary points
    avg_px = np.mean(x_idxs)
    avg_py = np.mean(y_idxs)
    
    drift_x = (avg_px - img_cx) * scale
    drift_y = (avg_py - img_cy) * scale
    
    new_center_x = center_x + drift_x
    new_center_y = center_y + drift_y
    
    # --- BOUNDING BOX CALCULATION ---
    # Find the extent of the points in pixel space
    min_px, max_px = np.min(x_idxs), np.max(x_idxs)
    min_py, max_py = np.min(y_idxs), np.max(y_idxs)
    
    # Convert pixel extent to physical extent
    phys_width = (max_px - min_px) * scale
    phys_height = (max_py - min_py) * scale
    
    # This is the physical size of the structure found
    structure_span = max(phys_width, phys_height)
    
    # --- POINT EXTRACTION ---
    if count > max_points:
        choice = np.random.choice(count, max_points, replace=False)
        x_idxs = x_idxs[choice]
        y_idxs = y_idxs[choice]
    
    # 1. Local Coordinates (Relative to the camera center 0,0)
    local_x = (x_idxs - img_cx) * scale
    local_y = (y_idxs - img_cy) * scale
    
    # 2. World Coordinates (Absolute position in space)
    phys_x = local_x + center_x
    phys_y = local_y + center_y
    
    return phys_x, phys_y, local_x, local_y, new_center_x, new_center_y, count, structure_span, scale

# ==========================================
# 3. EXPORT LOGIC
# ==========================================

def save_to_ply_colored(filename, x, y, z):
    n = len(x)
    if n == 0:
        print(f"[!] Warning: No points to save for {filename}")
        return

    print(f"[-] Writing {n} points to {filename}...")
    
    # Color based on twist/angle
    angles = np.arctan2(y, x)
    norm_a = (angles + np.pi) / (2*np.pi)
    
    cmap = plt.get_cmap('hsv')
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
    print(f"[+] Saved {filename}.")

# ==========================================
# 4. EXECUTION: REVERSE SPARSE DRILL (TIP -> BASE)
# ==========================================

# CONFIGURATION
MAX_LAYERS = 800
ZOOM_TIP = 1     # Starting tiny (Micro)
SPARSE_THRESHOLD = 1000 
MAX_POINTS_PER_LAYER = 3000
EXPANSION_RATE = 1.01 # Minimum forced zoom-out per step (1%)

# Initial State
cx, cy = 0.0, 0.0
current_zoom = ZOOM_TIP
active_recording = False
trigger_layer = 0

# Storage
world_x, world_y, world_z = [], [], []
local_x, local_y, local_z = [], [], []

print(f"[-] Starting Reverse Drill (Tip -> Base).")
print(f"[-] Initial Zoom: {current_zoom}. Waiting for sparse region (<= {SPARSE_THRESHOLD})...")

for i in range(MAX_LAYERS):
    # Scan
    wx, wy, lx, ly, new_cx, new_cy, count, span, pixel_scale = extract_layer_adaptive(
        current_zoom, cx, cy, res=800, max_points=MAX_POINTS_PER_LAYER
    )
    
    # 1. STOP CONDITION: If we lose the structure entirely
    if count == 0:
        print(f"[!] Zero points at Layer {i}. Structure ended or lost.")
        break

    # 2. TRIGGER LOGIC
    # We are looking for the "tiny tippy top", so valid low counts trigger recording
    if not active_recording:
        if count <= SPARSE_THRESHOLD:
            active_recording = True
            trigger_layer = i
            print(f"[!] TRIGGER: Sparse Tip Found at Layer {i} (Count: {count}). BEGIN RECORDING.")
        else:
            # Too dense/big? Maybe we aren't at the tip yet, or the tip is huge. 
            # In reverse mode, if we start too zoomed in, we might just see a wall.
            # But assuming we are at the tip, high counts mean we might need to zoom OUT to find the edge.
            pass

    # 3. RECORDING
    if active_recording:
        # Z grows UPWARDS (0, 0.1, 0.2...)
        current_z = (i - trigger_layer) * 0.1
        
        zs_world = np.full_like(wx, current_z)
        world_x.append(wx); world_y.append(wy); world_z.append(zs_world)
        
        zs_local = np.full_like(lx, current_z)
        local_x.append(lx); local_y.append(ly); local_z.append(zs_local)
        
        if i % 10 == 0:
            print(f"    [REC] Layer {i}: Zoom={current_zoom:.5f} | Pts={count} | Span={span:.5f}")

    # 4. TRACKING & ZOOM UPDATE
    cx = cx * 0.2 + new_cx * 0.8
    cy = cy * 0.2 + new_cy * 0.8
    
    # DYNAMIC ZOOM LOGIC (The "Tight Bounding Box")
    # We want the window to cover the structure (span) plus a margin.
    # The margin is "one point length" (roughly pixel_scale) or a safety factor.
    # We also enforce a minimum expansion so we actually move "up" the fractal.
    
    safe_margin = pixel_scale * 4.0 # 4 pixels buffer
    target_zoom = (span / 2.0) + safe_margin
    
    # Forced expansion: Ensure we zoom out at least by EXPANSION_RATE
    forced_zoom = current_zoom * EXPANSION_RATE
    
    # The new zoom is the max of "what fits the object" and "forced step out"
    current_zoom = max(target_zoom, forced_zoom)

# COMBINE AND SAVE
if len(world_x) > 0:
    WX = np.concatenate(world_x); WY = np.concatenate(world_y); WZ = np.concatenate(world_z)
    save_to_ply_colored("wada_reverse_tip.ply", WX, WY, WZ)
    
    LX = np.concatenate(local_x); LY = np.concatenate(local_y); LZ = np.concatenate(local_z)
    save_to_ply_colored("wada_reverse_change_map.ply", LX, LY, LZ)
else:
    print("[!] No data recorded.")