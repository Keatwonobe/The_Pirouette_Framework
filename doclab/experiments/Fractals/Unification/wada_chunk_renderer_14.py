import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import sys

# ==========================================
# 1. THE PHYSICS KERNEL
# (From all original files - defining the chaotic system)
# ==========================================

@njit(fastmath=True)
def get_basin_single(m, l, t_max=60.0, dt=0.05, escape_r2=16.0):
    pm, pl = 0.0, 0.0
    steps = int(t_max / dt)
    sigma = 1.0
    
    # Stability Check 1: Initial Overflow
    if m*m + l*l > 1e100: 
        return 0 
        
    for _ in range(steps):
        # Velocity Update (Half-step)
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        # Position Update
        m += dt * pm; l += dt * pl
        
        # Stability Check 2: Runaway Growth
        if m*m + l*l > 1e100: 
            return 0 
            
        # Velocity Update (Full-step)
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        
        # Escape Check
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
    
    deg120 = 2.094395; deg240 = 4.188790 # 120 and 240 degrees in radians
    
    for y in prange(res):
        for x in range(res):
            px = (x - img_cx) * scale + center_x
            py = (y - img_cy) * scale + center_y
            
            # Stability Check 3: NaN/Inf Coordinates
            if not (np.isfinite(px) and np.isfinite(py)): 
                out_map[y, x] = 0
                continue

            r = np.sqrt(px*px + py*py); theta = np.arctan2(py, px)
            if theta < 0: theta += 2*np.pi
            
            # Apply 3-fold rotational symmetry to the coordinates
            rot = 0
            if theta >= deg240: theta -= deg240; rot = 2
            elif theta >= deg120: theta -= deg120; rot = 1
            eff_px = r * np.cos(theta); eff_py = r * np.sin(theta)
            
            basin = get_basin_single(eff_px, eff_py)
            if basin != 0: 
                # Re-apply the rotation to the basin ID
                out_map[y, x] = (basin - 1 + rot) % 3 + 1
            
    return out_map

# ==========================================
# 2. THE TRACKING SCANNER
# (High-resolution layer extraction and dynamic center-of-mass tracking)
# ==========================================

def extract_layer_adaptive(zoom, center_x, center_y, res=2048, tracking_max_sample=5000):
    
    oracle = generate_oracle_map_centered(res, zoom, center_x, center_y)
    
    # Detect Boundaries (The "Skeleton")
    grad_x = np.abs(np.diff(oracle, axis=1, append=oracle[:, -1:]))
    grad_y = np.abs(np.diff(oracle, axis=0, append=oracle[-1:, :]))
    boundaries_mask = (grad_x + grad_y) > 0
    
    y_idxs, x_idxs = np.where(boundaries_mask)
    total_count = len(x_idxs)
    
    if total_count == 0:
        empty = np.array([])
        return empty, empty, center_x, center_y, 0, 0.0, 0.0, boundaries_mask
        
    img_cx, img_cy = res / 2.0, res / 2.0
    scale = (2.0 * zoom) / res

    # --- TRACKING LOGIC (Using subset for speed) ---
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
    
    # --- BOUNDING BOX ---
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
# (Deep dive to find the absolute tip, minimizing 'zoom' to machine precision)
# ==========================================

def seek_absolute_tip(start_zoom, start_cx, start_cy):
    print("[-] Initiating Deep Dive to find Precision Limit...")
    
    curr_zoom, curr_cx, curr_cy = start_zoom, start_cx, start_cy
    last_valid_zoom, last_valid_cx, last_valid_cy = curr_zoom, curr_cx, curr_cy
    
    max_iterations = 300 
    
    for i in range(max_iterations):
        # Use low res for speed
        _, _, new_cx, new_cy, count, span, _, _ = extract_layer_adaptive(
            curr_zoom, curr_cx, curr_cy, res=400 
        )
        
        if count == 0:
            print(f"   [STOP] Chaos vanished at Zoom={curr_zoom:.4e}. Backing up to last valid point.")
            break
            
        last_valid_zoom = curr_zoom
        last_valid_cx = new_cx 
        last_valid_cy = new_cy
        
        # Move camera aggressively to the new center
        curr_cx, curr_cy = new_cx, new_cy
        
        # Aggressive Zoom In: Target a FOV 1.5x the size of the structure.
        target_zoom = span * 0.75 # Since span is full width, target_zoom is half width.
        if target_zoom > 0 and target_zoom < curr_zoom:
             curr_zoom = target_zoom
        else:
             curr_zoom *= 0.5 # Forced march in
             
        if i % 20 == 0:
            print(f"   [DIVE] Iter {i}: Zoom={curr_zoom:.4e} | Span={span:.4e} | Pts={count}")
            
        # Float64 Precision Limit is roughly 1e-15
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
    
    # Stability Fix: Filter out any non-finite coordinates
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
    
    # Color based on twist/angle (HSV Colormap)
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
        # Using double (f8) for high precision of coordinates
        data = np.zeros(n, dtype=[('x','f8'),('y','f8'),('z','f8'),('r','u1'),('g','u1'),('b','u1')])
        data['x'] = x_out; data['y'] = y_out; data['z'] = z_out # Use z_out
        data['r'] = colors[:,0]; data['g'] = colors[:,1]; data['b'] = colors[:,2]
        f.write(data.tobytes())
    print(f"[+] Saved {filename}.")

# ==========================================
# 5. MAIN EXECUTION: FILAMENT SCAN
# ==========================================

# CONFIGURATION FOR THE NEEDLE SCAN
SCAN_RESOLUTION = 2048  # High Def for sharp edges
MAX_LAYERS = 600        # Height of the tower (fewer than 800 for faster run)
SAFE_MARGIN_FACTOR = 1.1 # Tighter margin (1.1 = Object takes up ~90% of screen)
EXPANSION_RATE = 1.005  # Minimum zoom-out to ensure upward movement

# 1. FIND THE BOTTOM (The Absolute Tip)
start_zoom, start_cx, start_cy = seek_absolute_tip(20.0, 0.0, 0.0)

# 2. CONFIGURE SCAN
cx, cy = start_cx, start_cy
current_zoom = start_zoom * 2.0 # Back off slightly to catch the first layer

world_x, world_y, world_z = [], [], []

print(f"\n[-] Starting HIGH RES FILAMENT SCAN (Zooming OUT from absolute tip)...")

for i in range(MAX_LAYERS):
    # Scan at high resolution
    wx, wy, new_cx, new_cy, count, span, pixel_scale, _ = extract_layer_adaptive(
        current_zoom, cx, cy, res=SCAN_RESOLUTION
    )
    
    if count == 0:
        print(f"[!] Structure lost at Layer {i}. Stopping.")
        break
        
    # Tracking (Heavy blend to keep camera precisely centered)
    cx = cx * 0.1 + new_cx * 0.9 
    cy = cy * 0.1 + new_cy * 0.9
    
    # Layering (Z-depth) - We use linear Z for a uniform tower height
    current_z = i * 0.1 
    
    # Store World Data
    zs_world = np.full_like(wx, current_z)
    world_x.append(wx); world_y.append(wy); world_z.append(zs_world)
    
    if i % 20 == 0:
        print(f"    [REC] Layer {i}: Z={current_z:.1f} | Zoom={current_zoom:.4e} | Pts={count} | Span={span:.4e}")
        
    # 3. TIGHT EXPANSION LOGIC
    # We want the camera (zoom) to tightly hug the object (span)
    target_zoom = (span / 2.0) * SAFE_MARGIN_FACTOR
    
    # Forced expansion: Ensure we move up the spire even if the span doesn't change
    forced_zoom = current_zoom * EXPANSION_RATE
    
    # The new zoom is the max of "what fits the object" and "forced step out"
    current_zoom = max(target_zoom, forced_zoom)

# 4. SAVE FILES
if len(world_x) > 0:
    WX = np.concatenate(world_x); WY = np.concatenate(world_y); WZ = np.concatenate(world_z)
    final_point_count = len(WX)
    print(f"\n[+] FINAL POINT COUNT: {final_point_count:,} points.")
    
    # Save Real Scale (Double Precision for high fidelity)
    save_to_ply_colored("wada_needle_real.ply", WX, WY, WZ, scale_factor=1.0)
    
    # Save Visual Scale (Multiplied by 1,000,000 for viewing)
    save_to_ply_colored("wada_needle_vis.ply", WX, WY, WZ, scale_factor=1e6)
else:
    print("[!] No points recorded. The structure may be too small or tracking failed early.")