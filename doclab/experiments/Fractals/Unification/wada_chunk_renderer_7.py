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
    
    # --- BOUNDING BOX (Using ALL points for accuracy) ---
    min_px, max_px = np.min(x_idxs), np.max(x_idxs)
    min_py, max_py = np.min(y_idxs), np.max(y_idxs)
    phys_width = (max_px - min_px) * scale
    phys_height = (max_py - min_py) * scale
    structure_span = max(phys_width, phys_height)
    
    # --- EXPORT COORDINATES (ALL points) ---
    # 1. Local Coordinates (Relative to camera)
    local_x = (x_idxs - img_cx) * scale
    local_y = (y_idxs - img_cy) * scale
    
    # 2. World Coordinates
    phys_x = local_x + center_x
    phys_y = local_y + center_y
    
    return phys_x, phys_y, local_x, local_y, new_center_x, new_center_y, total_count, structure_span, scale, boundaries_mask

# ==========================================
# 3. EXPORT LOGIC (UPDATED FOR PRECISION)
# ==========================================

def save_to_ply_colored(filename, x, y, z, scale_factor=1.0):
    n = len(x)
    if n == 0:
        print(f"[!] Warning: No points to save for {filename}")
        return

    print(f"[-] Writing {n} points to {filename} (Scale x{scale_factor})...")
    
    # Apply Scaling for Visualization
    x_out = x * scale_factor
    y_out = y * scale_factor
    z_out = z * scale_factor # Usually we don't scale Z if it's layer steps, but if 'scale_factor' is huge (1e6), we might need to? 
    # Actually, let's only scale XY for the shape, and keep Z as is, OR scale all.
    # If we are magnifying a microscopic tip, we want XY scaled. Z is already "0.1" steps usually. 
    # Let's Scale ALL to preserve aspect ratio if it's a true 3D shape, 
    # BUT since Z is artificial (time/layers), let's keep Z distinct or handled by the user.
    # For now: Scale X and Y. Keep Z relative to layers.
    
    # Color based on twist/angle
    angles = np.arctan2(y, x)
    norm_a = (angles + np.pi) / (2*np.pi)
    
    cmap = plt.get_cmap('hsv')
    colors = cmap(norm_a)[:, :3]
    colors = (colors * 255).astype(np.uint8)
    
    with open(filename, 'wb') as f:
        # Note: 'double' (float64) for coordinates to handle tiny values
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
        # Use 'f8' for double precision
        data = np.zeros(n, dtype=[('x','f8'),('y','f8'),('z','f8'),('r','u1'),('g','u1'),('b','u1')])
        data['x'] = x_out; data['y'] = y_out; data['z'] = z # Z is usually 0, 0.1, 0.2... so it doesn't need scaling
        data['r'] = colors[:,0]; data['g'] = colors[:,1]; data['b'] = colors[:,2]
        f.write(data.tobytes())
    print(f"[+] Saved {filename}.")

# ==========================================
# 4. EXECUTION
# ==========================================

MAX_LAYERS = 800
INITIAL_ZOOM = 20.0
SPARSE_THRESHOLD = 1000
EXPANSION_RATE = 1.01

cx, cy = 0.0, 0.0
current_zoom = INITIAL_ZOOM
active_recording = False
trigger_layer = 0

world_x, world_y, world_z = [], [], []
delta_x, delta_y, delta_z = [], [], []

prev_boundaries_mask = None 

print(f"[-] Starting Auto-Seeking Drill (Scientific Notation + Vis Scale).")

for i in range(MAX_LAYERS):
    # Scan
    wx, wy, lx, ly, new_cx, new_cy, count, span, pixel_scale, current_mask = extract_layer_adaptive(
        current_zoom, cx, cy, res=800
    )
    
    # Update Camera
    if count > 0:
        cx = cx * 0.2 + new_cx * 0.8
        cy = cy * 0.2 + new_cy * 0.8
        
    if active_recording:
        # === RECORDING ===
        if count == 0:
            print(f"[!] Structure lost at Layer {i}. Stopping.")
            break
            
        current_z = (i - trigger_layer) * 0.1
        
        # 1. World Map (ALL POINTS)
        zs_world = np.full_like(wx, current_z)
        world_x.append(wx); world_y.append(wy); world_z.append(zs_world)
        
        # 2. Delta Map (NEW POINTS ONLY)
        if prev_boundaries_mask is not None:
            diff_mask = current_mask & (~prev_boundaries_mask)
            dy_idxs, dx_idxs = np.where(diff_mask)
            
            if len(dx_idxs) > 0:
                img_cx = 800 / 2.0; img_cy = 800 / 2.0
                dl_x = (dx_idxs - img_cx) * pixel_scale
                dl_y = (dy_idxs - img_cy) * pixel_scale
                dl_z = np.full_like(dl_x, current_z)
                
                delta_x.append(dl_x); delta_y.append(dl_y); delta_z.append(dl_z)
        
        prev_boundaries_mask = current_mask
        
        # Log with Scientific Notation
        if i % 10 == 0:
            print(f"    [REC] Layer {i}: Zoom={current_zoom:.4e} | Pts={count} (All Saved)")
            
        # Expansion
        safe_margin = pixel_scale * 4.0
        target_zoom = (span / 2.0) + safe_margin
        forced_zoom = current_zoom * EXPANSION_RATE
        current_zoom = max(target_zoom, forced_zoom)
        
    else:
        # === SEEKING ===
        prev_boundaries_mask = None
        
        if count == 0:
            print(f"    [SEEK] Layer {i}: 0 Points. Expanding...")
            current_zoom *= 1.2 
        elif count > SPARSE_THRESHOLD:
            if i % 10 == 0:
                print(f"    [SEEK] Layer {i}: Too Dense ({count} pts). Diving... (Zoom {current_zoom:.4e})")
            current_zoom *= 0.90
        else:
            print(f"[!] TRIGGER: Sparse Tip Found at Layer {i} (Count: {count}). RECORDING.")
            active_recording = True
            trigger_layer = i

# SAVE FILES
if len(world_x) > 0:
    WX = np.concatenate(world_x); WY = np.concatenate(world_y); WZ = np.concatenate(world_z)
    
    # Save Real Scale (Double Precision)
    save_to_ply_colored("wada_structure_real.ply", WX, WY, WZ, scale_factor=1.0)
    
    # Save Visual Scale (Multiplied by 1,000,000 so it looks good in Blender/MeshLab)
    save_to_ply_colored("wada_structure_visual.ply", WX, WY, WZ, scale_factor=1000000.0)
    
    if len(delta_x) > 0:
        DX = np.concatenate(delta_x); DY = np.concatenate(delta_y); DZ = np.concatenate(delta_z)
        save_to_ply_colored("wada_delta_real.ply", DX, DY, DZ, scale_factor=1.0)
        save_to_ply_colored("wada_delta_visual.ply", DX, DY, DZ, scale_factor=1000000.0)
else:
    print("[!] No data recorded.")