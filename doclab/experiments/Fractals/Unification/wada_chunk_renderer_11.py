import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import sys

# ==========================================
# 1. THE PHYSICS KERNEL (Stability Fixes Applied)
# ==========================================

@njit(fastmath=True)
def get_basin_single(m, l, t_max=60.0, dt=0.05, escape_r2=16.0):
    pm, pl = 0.0, 0.0
    steps = int(t_max / dt)
    sigma = 1.0
    
    # FIX 1a: Check for potential overflow at the start
    if m*m + l*l > 1e100: 
        return 0 
        
    for _ in range(steps):
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        m += dt * pm; l += dt * pl
        
        # FIX 1b: Check for runaway growth (pre-NAN) during integration
        if m*m + l*l > 1e100: 
            return 0 
            
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
            
            # FIX 2: Skip calculation if input coordinates are invalid (NaN or Inf)
            if not (np.isfinite(px) and np.isfinite(py)): 
                out_map[y, x] = 0
                continue

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
# 2. THE TRACKING SCANNER (HIGH RES)
# ==========================================

def extract_layer_adaptive(zoom, center_x, center_y, res=2048, tracking_max_sample=5000):
    """
    Scans at 'res'. Higher res = More points = Higher density model.
    """
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
    # We only need a few thousand points to find the center of mass
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
# 3. THE PRECISION SEEKER
# ==========================================

def seek_absolute_tip(start_zoom, start_cx, start_cy):
    print("[-] Initiating Deep Dive to find Precision Limit...")
    
    curr_zoom = start_zoom
    curr_cx = start_cx
    curr_cy = start_cy
    
    last_valid_zoom = curr_zoom
    last_valid_cx = curr_cx
    last_valid_cy = curr_cy
    
    max_iterations = 300 
    
    for i in range(max_iterations):
        # Use low res for seeker to be fast (we don't need HD here, just position)
        _, _, _, _, new_cx, new_cy, count, span, _, _ = extract_layer_adaptive(
            curr_zoom, curr_cx, curr_cy, res=400 
        )
        
        if count == 0:
            print(f"   [STOP] Chaos vanished at Zoom={curr_zoom:.4e}. Backing up.")
            break
            
        last_valid_zoom = curr_zoom
        last_valid_cx = new_cx 
        last_valid_cy = new_cy
        
        curr_cx = new_cx
        curr_cy = new_cy
        
        # Aggressive Zoom In
        target_zoom = span * 1.5 
        if target_zoom > 0 and target_zoom < curr_zoom:
             curr_zoom = target_zoom
        else:
             curr_zoom *= 0.5 
             
        if i % 20 == 0:
            print(f"   [DIVE] Iter {i}: Zoom={curr_zoom:.4e} | Span={span:.4e} | Pts={count}")
            
        if curr_zoom < 1e-14:
            print(f"   [STOP] Hit Machine Precision Limit (~1e-14).")
            break
            
    print(f"[-] Deepest Valid Point Found:\n    Zoom={last_valid_zoom:.4e}")
    return last_valid_zoom, last_valid_cx, last_valid_cy

# ==========================================
# 4. EXPORT LOGIC (Stability Fixes Applied)
# ==========================================

def save_to_ply_colored(filename, x, y, z, scale_factor=1.0):
    
    # FIX 3: Filter out any non-finite coordinates before saving
    finite_mask = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    if not np.all(finite_mask):
        print(f"[!] Warning: Filtering out {len(x) - np.sum(finite_mask)} non-finite points (NaN/Inf) from {filename}.")
        x = x[finite_mask]
        y = y[finite_mask]
        z = z[finite_mask]
    
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
        data['x'] = x_out; data['y'] = y_out; data['z'] = z
        data['r'] = colors[:,0]; data['g'] = colors[:,1]; data['b'] = colors[:,2]
        f.write(data.tobytes())
    print(f"[+] Saved {filename}.")

# ==========================================
# 5. MAIN EXECUTION (Revised for Tallest Part)
# ==========================================

# CONFIGURATION
# ------------------------------------
SCAN_RESOLUTION = 2048  # High Def (was 800). Set to 4096 for Ultra HD (slower).
MAX_LAYERS = 800        # Hard limit safety stop
EXPANSION_RATE = 1.005  # Slower expansion to keep camera tight on the spire
SAFE_MARGIN_FACTOR = 1.2 # Multiplier for FOV. 1.2 = Object takes up ~80% of screen.
SPAN_DROP_THRESHOLD = 0.8 # New: Stop if current span is < 80% of previous span
# ------------------------------------

# ==========================================
# 5. MAIN EXECUTION (Revised to Skip Layer 0 Span Check)
# ==========================================

# ... (Configuration block remains the same) ...

# 1. FIND THE BOTTOM
start_zoom, start_cx, start_cy = seek_absolute_tip(20.0, 0.0, 0.0)

# 2. CONFIGURE SCAN
cx, cy = start_cx, start_cy
current_zoom = start_zoom * 2.0 

world_x, world_y, world_z = [], [], []
delta_x, delta_y, delta_z = [], [], []
prev_boundaries_mask = None 

# --- REVISION: Initialize prev_span to 0.0 or a safe low number ---
# This ensures the first check (Layer 0) is bypassed, 
# and the span value is properly set for Layer 1.
prev_span = 0.0 

print(f"[-] Starting HIGH RES Structural Scan (Focusing on Tallest Tip)...")

for i in range(MAX_LAYERS):
    # Scan at high resolution
    wx, wy, lx, ly, new_cx, new_cy, count, span, pixel_scale, current_mask = extract_layer_adaptive(
        current_zoom, cx, cy, res=SCAN_RESOLUTION
    )
    
    # --- STOPPING CONDITION 1: LOST STRUCTURE ---
    if count == 0:
        print(f"[!] Lost structure at Layer {i}. Stopping.")
        break
    
    # --- STOPPING CONDITION 2: STRUCTURE SIMPLIFICATION/SHRINKAGE ---
    # NEW LOGIC: Only perform the check if it's not the first layer (i > 0) AND 
    # the previous span was valid (prev_span > 0).
    if i > 0 and prev_span > 0.0 and span < prev_span * SPAN_DROP_THRESHOLD:
         print(f"[!] Span shrank significantly at Layer {i} ({span:.4e} vs {prev_span:.4e}). Assuming highest complexity point reached.")
         break
    
    # --- REVISION: Update prev_span unconditionally after the check ---
    prev_span = span 
        
    # Standard Tracking and Layering Logic (Unchanged)
    cx = cx * 0.1 + new_cx * 0.9 
    cy = cy * 0.1 + new_cy * 0.9
    
    current_z = i * 0.1
    
    zs_world = np.full_like(wx, current_z)
    world_x.append(wx); world_y.append(wy); world_z.append(zs_world)
    
    if prev_boundaries_mask is not None:
        diff_mask = current_mask & (~prev_boundaries_mask)
        dy_idxs, dx_idxs = np.where(diff_mask)
        
        if len(dx_idxs) > 0:
            img_cx, img_cy = SCAN_RESOLUTION/2.0, SCAN_RESOLUTION/2.0
            dl_x = (dx_idxs - img_cx) * pixel_scale
            dl_y = (dy_idxs - img_cy) * pixel_scale
            dl_z = np.full_like(dl_x, current_z)
            delta_x.append(dl_x); delta_y.append(dl_y); delta_z.append(dl_z)
            
    prev_boundaries_mask = current_mask
    
    if i % 10 == 0:
        print(f"    [SCAN] Layer {i}: Zoom={current_zoom:.4e} | Span={span:.4e} | Pts={count}")
        
    # TIGHT EXPANSION LOGIC
    target_zoom = (span / 2.0) * SAFE_MARGIN_FACTOR
    forced_zoom = current_zoom * EXPANSION_RATE
    current_zoom = max(target_zoom, forced_zoom)

if len(world_x) > 0:
    WX = np.concatenate(world_x); WY = np.concatenate(world_y); WZ = np.concatenate(world_z)
    save_to_ply_colored("wada_HD_structure_real.ply", WX, WY, WZ, scale_factor=1.0)
    save_to_ply_colored("wada_HD_structure_vis.ply", WX, WY, WZ, scale_factor=1e6)
    
    if len(delta_x) > 0:
        DX = np.concatenate(delta_x); DY = np.concatenate(delta_y); DZ = np.concatenate(delta_z)
        save_to_ply_colored("wada_HD_delta_real.ply", DX, DY, DZ, scale_factor=1.0)
        save_to_ply_colored("wada_HD_delta_vis.ply", DX, DY, DZ, scale_factor=1e6)
else:
    print("[!] No points found.")