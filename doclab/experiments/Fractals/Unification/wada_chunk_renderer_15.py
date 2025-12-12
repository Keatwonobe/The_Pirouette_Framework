import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import sys

# ==========================================
# 1. THE PHYSICS KERNEL & ORACLE MAP
# (Identical to the robust version in wada_chunk_renderer_13.py)
# ==========================================

@njit(fastmath=True)
def get_basin_single(m, l, t_max=60.0, dt=0.05, escape_r2=16.0):
    pm, pl = 0.0, 0.0
    steps = int(t_max / dt)
    sigma = 1.0
    if m*m + l*l > 1e100: return 0 
        
    for _ in range(steps):
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        m += dt * pm; l += dt * pl
        
        if m*m + l*l > 1e100: return 0 
            
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
    
    deg120 = 2.094395; deg240 = 4.188790
    
    for y in prange(res):
        for x in range(res):
            px = (x - img_cx) * scale + center_x
            py = (y - img_cy) * scale + center_y
            
            if not (np.isfinite(px) and np.isfinite(py)): 
                out_map[y, x] = 0
                continue

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
# 2. THE TRACKING SCANNER
# (Modified to return only necessary tracking info for speed)
# ==========================================

def extract_layer_adaptive(zoom, center_x, center_y, res=2048, tracking_max_sample=5000):
    
    oracle = generate_oracle_map_centered(res, zoom, center_x, center_y)
    
    # Detect Boundaries
    grad_x = np.abs(np.diff(oracle, axis=1, append=oracle[:, -1:]))
    grad_y = np.abs(np.diff(oracle, axis=0, append=oracle[-1:, :]))
    boundaries_mask = (grad_x + grad_y) > 0
    
    y_idxs, x_idxs = np.where(boundaries_mask)
    total_count = len(x_idxs)
    
    if total_count == 0:
        empty = np.array([])
        # Only return the bare minimum: center stays the same, count/span are zero
        return empty, empty, center_x, center_y, 0, 0.0, 0.0, boundaries_mask 
        
    img_cx, img_cy = res / 2.0, res / 2.0
    scale = (2.0 * zoom) / res

    # --- TRACKING LOGIC ---
    if total_count > tracking_max_sample:
        choice = np.random.choice(total_count, tracking_max_sample, replace=False)
        track_x, track_y = x_idxs[choice], y_idxs[choice]
    else:
        track_x, track_y = x_idxs, y_idxs
        
    avg_px, avg_py = np.mean(track_x), np.mean(track_y)
    
    drift_x = (avg_px - img_cx) * scale
    drift_y = (avg_py - img_cy) * scale
    
    new_center_x = center_x + drift_x
    new_center_y = center_y + drift_y
    
    # --- BOUNDING BOX (For Zooming) ---
    min_px, max_px = np.min(x_idxs), np.max(x_idxs)
    min_py, max_py = np.min(y_idxs), np.max(y_idxs)
    phys_width = (max_px - min_px) * scale
    phys_height = (max_py - min_py) * scale
    structure_span = max(phys_width, phys_height)
    
    # --- EXPORT COORDINATES ---
    phys_x = (x_idxs - img_cx) * scale + center_x
    phys_y = (y_idxs - img_cy) * scale + center_y
    
    return phys_x, phys_y, new_center_x, new_center_y, total_count, structure_span, scale, boundaries_mask

# ==========================================
# 3. THE PRECISION SEEKER
# (Dive to the floor)
# ==========================================

def seek_absolute_tip(start_zoom, start_cx, start_cy):
    print("[-] Initiating Deep Dive to find Precision Limit...")
    
    curr_zoom, curr_cx, curr_cy = start_zoom, start_cx, start_cy
    last_valid_zoom, last_valid_cx, last_valid_cy = curr_zoom, curr_cx, curr_cy
    
    max_iterations = 300 
    
    for i in range(max_iterations):
        # Use low res for speed (res=400)
        _, _, new_cx, new_cy, count, span, _, _ = extract_layer_adaptive(
            curr_zoom, curr_cx, curr_cy, res=400 
        )
        
        if count == 0:
            print(f"   [STOP] Chaos vanished at Zoom={curr_zoom:.4e}. Backing up.")
            break
            
        last_valid_zoom = curr_zoom
        last_valid_cx = new_cx 
        last_valid_cy = new_cy
        
        # Move camera aggressively to the new center
        curr_cx, curr_cy = new_cx, new_cy
        
        # Aggressive Zoom In (Target FOV 1.5x the size of the structure)
        target_zoom = span * 0.75 
        if target_zoom > 0 and target_zoom < curr_zoom:
             curr_zoom = target_zoom
        else:
             curr_zoom *= 0.5 
             
        if i % 20 == 0:
            print(f"   [DIVE] Iter {i}: Zoom={curr_zoom:.4e} | Span={span:.4e} | Pts={count}")
            
        if curr_zoom < 1e-14:
            print(f"   [STOP] Hit Machine Precision Limit (~1e-14).")
            break
            
    print(f"[-] Deepest Valid Point Found:\n    Zoom={last_valid_zoom:.4e}\n    Center=({last_valid_cx:.16f}, {last_valid_cy:.16f})")
    return last_valid_zoom, last_valid_cx, last_valid_cy

# ==========================================
# 4. EXPORT LOGIC
# (Double precision PLY exporter with NaN stability fix)
# ==========================================

def save_to_ply_colored(filename, x, y, z, scale_factor=1.0):
    
    finite_mask = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    if not np.all(finite_mask):
        print(f"[!] Warning: Filtering out {len(x) - np.sum(finite_mask)} non-finite points (NaN/Inf) from {filename}.")
        x = x[finite_mask]
        y = y[finite_mask]
        z = z[finite_mask]
    
    n = len(x)
    if n == 0: return

    print(f"[-] Writing {n} points to {filename} (Scale x{scale_factor:.1e})...")
    
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
        data['x'] = x_out; data['y'] = y_out; data['z'] = z_out 
        data['r'] = colors[:,0]; data['g'] = colors[:,1]; data['b'] = colors[:,2]
        f.write(data.tobytes())
    print(f"[+] Saved {filename}.")

# ==========================================
# 5. MAIN EXECUTION: DEEP DIVE & REVERSE SCAN
# ==========================================

def dive_and_scan_upwards(max_scan_layers=400, scan_resolution=2048):
    """
    Executes the two-phase scanning strategy: Deep Dive, then Scan Upwards.
    """
    TIGHT_MARGIN = 1.05       # Extremely tight FOV (5% buffer around structure)
    MIN_EXPANSION_RATE = 1.005 # Smallest step outward (0.5% zoom out)

    # PHASE 1: FIND THE ABSOLUTE TIP (Z=0)
    print("=========================================")
    start_zoom, start_cx, start_cy = seek_absolute_tip(20.0, 0.0, 0.0)
    print("=========================================")

    # PHASE 2: REVERSE SCAN OUTWARD (UPWARDS)
    cx, cy = start_cx, start_cy
    current_zoom = start_zoom * 2.0 # Start slightly backed off from the limit
    
    world_x, world_y, world_z = [], [], []

    print(f"\n[-] PHASE 2: Scanning UPWARDS for {max_scan_layers} layers...")
    
    # We use i=0 for the deepest layer (the tip)
    for i in range(max_scan_layers):
        
        # 1. SCAN
        wx, wy, new_cx, new_cy, count, span, pixel_scale, _ = extract_layer_adaptive(
            current_zoom, cx, cy, res=scan_resolution
        )
        
        if count == 0:
            print(f"[!] Structure lost at Layer {i}. Ending scan.")
            break
            
        # 2. TRACKING & Z-LAYERING
        cx = cx * 0.1 + new_cx * 0.9 # Aggressive tracking
        cy = cy * 0.1 + new_cy * 0.9
        
        current_z = i * 0.1 # Constant Z-step
        
        # Store Data
        zs_world = np.full_like(wx, current_z)
        world_x.append(wx); world_y.append(wy); world_z.append(zs_world)
        
        if i % 50 == 0:
            print(f"    [REC] Layer {i}: Z={current_z:.1f} | Zoom={current_zoom:.4e} | Pts={count} | Span={span:.4e}")
            
        # 3. TIGHT EXPANSION LOGIC
        # Target Zoom: The FOV must be just slightly larger than the span of the structure.
        target_zoom = (span / 2.0) * TIGHT_MARGIN
        
        # Forced expansion: Ensure we progress upwards
        forced_zoom = current_zoom * MIN_EXPANSION_RATE
        
        # New zoom is the max of the two (fit the structure or take a minimum step)
        current_zoom = max(target_zoom, forced_zoom)
        
    # PHASE 3: SAVE FILES
    if len(world_x) > 0:
        WX = np.concatenate(world_x); WY = np.concatenate(world_y); WZ = np.concatenate(world_z)
        final_point_count = len(WX)
        print(f"\n[+] FINAL POINT COUNT: {final_point_count:,} points.")
        
        # Save Real Scale (for precise measurement of wavy features)
        save_to_ply_colored("wada_needle_tip_real.ply", WX, WY, WZ, scale_factor=1.0)
        
        # Save Visual Scale (scaled up by 1e6 for viewing)
        save_to_ply_colored("wada_needle_tip_vis.ply", WX, WY, WZ, scale_factor=1e6)
    else:
        print("[!] Scan failed: No points recorded.")

# Execute the combined scan
if __name__ == "__main__":
    dive_and_scan_upwards()