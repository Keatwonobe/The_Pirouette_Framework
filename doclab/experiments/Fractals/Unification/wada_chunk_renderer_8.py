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

def extract_layer_adaptive(zoom, center_x, center_y, res=500, tracking_max_sample=4000):
    # Generate Map
    oracle = generate_oracle_map_centered(res, zoom, center_x, center_y)
    
    # Detect Boundaries
    grad_x = np.abs(np.diff(oracle, axis=1, append=oracle[:, -1:]))
    grad_y = np.abs(np.diff(oracle, axis=0, append=oracle[-1:, :]))
    boundaries_mask = (grad_x + grad_y) > 0
    
    y_idxs, x_idxs = np.where(boundaries_mask)
    total_count = len(x_idxs)
    
    # Defaults if empty
    if total_count == 0:
        empty = np.array([])
        return empty, empty, empty, empty, center_x, center_y, 0, 0.0, 0.0, boundaries_mask
        
    img_cx = res / 2.0
    img_cy = res / 2.0
    scale = (2.0 * zoom) / res

    # --- TRACKING LOGIC (Sub-sampled for speed) ---
    if total_count > tracking_max_sample:
        choice = np.random.choice(total_count, tracking_max_sample, replace=False)
        track_x = x_idxs[choice]
        track_y = y_idxs[choice]
    else:
        track_x = x_idxs
        track_y = y_idxs
        
    avg_px = np.mean(track_x)
    avg_py = np.mean(track_y)
    
    drift_x = (avg_px - img_cx) * scale
    drift_y = (avg_py - img_cy) * scale
    
    new_center_x = center_x + drift_x
    new_center_y = center_y + drift_y
    
    # --- BOUNDING BOX ---
    min_px, max_px = np.min(x_idxs), np.max(x_idxs)
    min_py, max_py = np.min(y_idxs), np.max(y_idxs)
    phys_width = (max_px - min_px) * scale
    phys_height = (max_py - min_py) * scale
    structure_span = max(phys_width, phys_height)
    
    # --- EXPORT COORDINATES ---
    local_x = (x_idxs - img_cx) * scale
    local_y = (y_idxs - img_cy) * scale
    phys_x = local_x + center_x
    phys_y = local_y + center_y
    
    return phys_x, phys_y, local_x, local_y, new_center_x, new_center_y, total_count, structure_span, scale, boundaries_mask

# ==========================================
# 3. THE PRECISION SEEKER (NEW)
# ==========================================

def seek_absolute_tip(start_zoom, start_cx, start_cy):
    """
    Dives deep until the structure vanishes or precision limit is hit.
    Returns the (zoom, cx, cy) of the deepest valid layer.
    """
    print("[-] Initiating Deep Dive to find Precision Limit...")
    
    curr_zoom = start_zoom
    curr_cx = start_cx
    curr_cy = start_cy
    
    # Keep track of the last valid state where we actually saw structure
    last_valid_zoom = curr_zoom
    last_valid_cx = curr_cx
    last_valid_cy = curr_cy
    
    max_iterations = 300 # Safety break
    
    for i in range(max_iterations):
        # Use a smaller resolution for the seeker to be fast
        _, _, _, _, new_cx, new_cy, count, span, _, _ = extract_layer_adaptive(
            curr_zoom, curr_cx, curr_cy, res=200
        )
        
        if count == 0:
            print(f"   [STOP] Chaos vanished at Zoom={curr_zoom:.4e}. Backing up to last valid point.")
            break
            
        # Update valid state
        last_valid_zoom = curr_zoom
        last_valid_cx = new_cx # Use the RE-CENTERED coordinates
        last_valid_cy = new_cy
        
        # Move camera
        curr_cx = new_cx
        curr_cy = new_cy
        
        # AGGRESSIVE ZOOM
        # We want to zoom in fast. 
        # If the span is tiny, snap to it. Otherwise, force a 2x zoom in.
        target_zoom = span * 1.5 
        if target_zoom > 0 and target_zoom < curr_zoom:
             curr_zoom = target_zoom
        else:
             curr_zoom *= 0.5 # Forced march
             
        if i % 10 == 0:
            print(f"   [DIVE] Iter {i}: Zoom={curr_zoom:.4e} | Span={span:.4e} | Pts={count}")
            
        # Float64 Precision Limit is roughly 1e-15 to 1e-16
        if curr_zoom < 1e-14:
            print(f"   [STOP] Hit Machine Precision Limit (~1e-14).")
            break
            
    print(f"[-] Deepest Valid Point Found:\n    Zoom={last_valid_zoom:.4e}\n    Center=({last_valid_cx:.16f}, {last_valid_cy:.16f})")
    return last_valid_zoom, last_valid_cx, last_valid_cy

# ==========================================
# 4. EXPORT LOGIC
# ==========================================

def save_to_ply_colored(filename, x, y, z, scale_factor=1.0):
    n = len(x)
    if n == 0: return

    print(f"[-] Writing {n} points to {filename} (Scale x{scale_factor})...")
    
    x_out = x * scale_factor; y_out = y * scale_factor; z_out = z * scale_factor
    
    angles = np.arctan2(y, x)
    norm_a = (angles + np.pi) / (2*np.pi)
    cmap = plt.get_cmap('hsv')
    colors = (cmap(norm_a)[:, :3] * 255).astype(np.uint8)
    
    with open(filename, 'wb') as f:
        header = f"""ply
format binary_little_endian 1.0
element vertex {n}
property double x
property double y
property double z
property uchar red
property uchar green
property uchar blue
end_header
"""
        f.write(header.encode('ascii'))
        data = np.zeros(n, dtype=[('x','f8'),('y','f8'),('z','f8'),('r','u1'),('g','u1'),('b','u1')])
        data['x'] = x_out; data['y'] = y_out; data['z'] = z # Keep Z as layers usually
        data['r'] = colors[:,0]; data['g'] = colors[:,1]; data['b'] = colors[:,2]
        f.write(data.tobytes())
    print(f"[+] Saved {filename}.")

# ==========================================
# 5. MAIN EXECUTION
# ==========================================

MAX_LAYERS = 600
EXPANSION_RATE = 1.01

# 1. FIND THE BOTTOM
# Start scanning from macro scale (20.0) at origin (0,0)
start_zoom, start_cx, start_cy = seek_absolute_tip(20.0, 0.0, 0.0)

# 2. CONFIGURE SCAN FROM BOTTOM
cx, cy = start_cx, start_cy
current_zoom = start_zoom * 2.0 # Back off slightly to ensure we catch the tip

world_x, world_y, world_z = [], [], []
delta_x, delta_y, delta_z = [], [], []
prev_boundaries_mask = None 

print(f"[-] Starting Structural Scan (Upwards from Tip)...")

for i in range(MAX_LAYERS):
    # Scan at high resolution for output
    wx, wy, lx, ly, new_cx, new_cy, count, span, pixel_scale, current_mask = extract_layer_adaptive(
        current_zoom, cx, cy, res=800
    )
    
    if count == 0:
        print(f"[!] Lost structure during scan at Layer {i}. Stopping.")
        break
        
    # Update Tracking
    cx = cx * 0.2 + new_cx * 0.8
    cy = cy * 0.2 + new_cy * 0.8
    
    # Calculate Z (growing upwards)
    current_z = i * 0.1
    
    # Store World Data
    zs_world = np.full_like(wx, current_z)
    world_x.append(wx); world_y.append(wy); world_z.append(zs_world)
    
    # Store Delta Data (Difference from previous layer)
    if prev_boundaries_mask is not None:
        diff_mask = current_mask & (~prev_boundaries_mask)
        dy_idxs, dx_idxs = np.where(diff_mask)
        
        if len(dx_idxs) > 0:
            img_cx, img_cy = 400.0, 400.0 # 800/2
            dl_x = (dx_idxs - img_cx) * pixel_scale
            dl_y = (dy_idxs - img_cy) * pixel_scale
            dl_z = np.full_like(dl_x, current_z)
            delta_x.append(dl_x); delta_y.append(dl_y); delta_z.append(dl_z)
            
    prev_boundaries_mask = current_mask
    
    if i % 20 == 0:
        print(f"    [SCAN] Layer {i}: Zoom={current_zoom:.4e} | Pts={count}")
        
    # Expand
    safe_margin = pixel_scale * 4.0
    target_zoom = (span / 2.0) + safe_margin
    forced_zoom = current_zoom * EXPANSION_RATE
    current_zoom = max(target_zoom, forced_zoom)

# SAVE
if len(world_x) > 0:
    WX = np.concatenate(world_x); WY = np.concatenate(world_y); WZ = np.concatenate(world_z)
    save_to_ply_colored("wada_deep_structure.ply", WX, WY, WZ, scale_factor=1.0)
    save_to_ply_colored("wada_deep_structure_vis.ply", WX, WY, WZ, scale_factor=1e6)
    
    if len(delta_x) > 0:
        DX = np.concatenate(delta_x); DY = np.concatenate(delta_y); DZ = np.concatenate(delta_z)
        save_to_ply_colored("wada_deep_delta.ply", DX, DY, DZ, scale_factor=1.0)
        save_to_ply_colored("wada_deep_delta_vis.ply", DX, DY, DZ, scale_factor=1e6)
else:
    print("[!] No points found.")