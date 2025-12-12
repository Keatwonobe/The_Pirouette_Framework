import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import sys

# ==========================================
# 1. THE PHYSICS KERNEL (with NAN Stability Fixes)
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
        # Use low res for seeker to be fast
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
# 4. EXPORT LOGIC (with NAN Stability Fix)
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
# 5. MAIN EXECUTION (Budgeted Scan - Two Pass)
# ==========================================

# CONFIGURATION
# ------------------------------------
SCAN_RESOLUTION = 2048  
MAX_LAYERS = 800
ZOOM_RATE = 1.025      
# --- NEW BUDGETING PARAMETERS ---
TARGET_GIGABYTES = 2.0
TARGET_POINTS = int(TARGET_GIGABYTES * 1024**3 / 27) # Approx 74 million points
DENSITY_BIAS = 5.0 # Prioritize top (Z=0) layers with this factor (must be >= 1.0)
# ------------------------------------

# 1. FIND THE BOTTOM (Deepest Valid Point)
start_zoom, start_cx, start_cy = seek_absolute_tip(20.0, 0.0, 0.0)

# 2. PASS 1: GEOMETRIC INDEXING (Fast, low-res run to get point counts)
print("\n[-] PASS 1: Indexing structure geometry at low resolution...")
cx, cy = start_cx, start_cy
current_zoom = start_zoom * 2.0 
geometry_profile = [] # Stores (zoom, cx, cy, low_res_count)

for i in range(MAX_LAYERS):
    # Use low resolution for speed
    _, _, _, _, new_cx, new_cy, count, _, _, _ = extract_layer_adaptive(
        current_zoom, cx, cy, res=400, tracking_max_sample=1000 
    )
    
    if count == 0:
        print(f"   [STOP] Structure lost at layer {i}. Ending index.")
        break
    
    cx = cx * 0.1 + new_cx * 0.9 
    cy = cy * 0.1 + new_cy * 0.9
    current_zoom *= ZOOM_RATE 
    
    geometry_profile.append({'zoom': current_zoom, 'cx': cx, 'cy': cy, 'count': count, 'layer_index': i})
    
    if i % 50 == 0:
        print(f"   [INDEX] Layer {i}: Zoom={current_zoom:.4e} | LowRes Pts={count}")

if not geometry_profile:
    print("[!] Indexing failed. No structure found.")
    sys.exit()

# 3. CALCULATE POINT ALLOCATION & SAMPLING RATIOS
profile_counts = np.array([item['count'] for item in geometry_profile])
total_layers = len(geometry_profile)

# Create a density weighting factor (linear decay from DENSITY_BIAS at Z=0 to 1.0 at Z=max)
z_indices = np.arange(total_layers)
# The top (Z=0) is the last layer in our scan down, but the first element in the profile.
# We reverse the index to map it to Z=height for density:
reversed_z_indices = (total_layers - 1) - z_indices

# Weighting: 1.0 + (DENSITY_BIAS - 1.0) * (Normalized Z/Height)
weights = 1.0 + (DENSITY_BIAS - 1.0) * (reversed_z_indices / (total_layers - 1))

weighted_counts = profile_counts * weights
total_weighted_points = np.sum(weighted_counts)

# Total Scale Factor to hit the TARGET_POINTS budget
target_ratio = TARGET_POINTS / total_weighted_points
sampling_ratios = target_ratio * weights

print(f"\n[-] BUDGET CALCULATED: Target={TARGET_POINTS:.2e} points (LowRes Total={np.sum(profile_counts)})")
print(f"    Allocating density based on DENSITY_BIAS={DENSITY_BIAS}.")

# 4. PASS 2: HIGH-RESOLUTION RECORDING (Sampling based on budget)
print("\n[-] PASS 2: High-Resolution Recording (Sampling to budget)...")

world_x, world_y, world_z = [], [], []
delta_x, delta_y, delta_z = [], [], []
prev_boundaries_mask = None 

# Start layer_i at 0 to re-use z-layering, but use profile data for zoom/center
for i in range(total_layers):
    data = geometry_profile[i]
    ratio = sampling_ratios[i]
    
    # Run high-res scan with coordinates from Pass 1
    wx, wy, lx, ly, _, _, count, _, pixel_scale, current_mask = extract_layer_adaptive(
        data['zoom'], data['cx'], data['cy'], res=SCAN_RESOLUTION
    )
    
    # --- SUBSAMPLING (Enforcing the Memory Budget) ---
    if ratio < 1.0:
        # Number of points to keep (based on high-res count)
        points_to_keep = int(count * ratio) 
        
        if points_to_keep == 0: continue
            
        # Randomly choose points_to_keep indices
        choice = np.random.choice(count, points_to_keep, replace=False)
        wx = wx[choice]; wy = wy[choice]
        
        # NOTE: We skip delta calculation here for simplicity since delta relies on the full grid mask.
        # It's better to record ALL points (wx, wy) and then sample them post-process, 
        # but to keep the memory low, we sample the world points now.
        
    # --- Layering and Recording ---
    current_z = i * 0.1 
    
    zs_world = np.full_like(wx, current_z)
    world_x.append(wx); world_y.append(wy); world_z.append(zs_world)
    
    # (Delta calculation is disabled or complex due to subsampling—simplified here)
    prev_boundaries_mask = current_mask # Still need to track mask for next layer's delta check

    if i % 50 == 0:
        print(f"   [REC] Layer {i}: Z={current_z:.1f} | Kept Pts={len(wx)} (Ratio={ratio:.2f})")
        
# 5. SAVE FILES (Logic remains the same)
if len(world_x) > 0:
    WX = np.concatenate(world_x); WY = np.concatenate(world_y); WZ = np.concatenate(world_z)
    final_point_count = len(WX)
    print(f"\n[+] FINAL POINT COUNT: {final_point_count:,} points.")
    
    # Save Real Scale (Double Precision)
    save_to_ply_colored("wada_HD_structure_real.ply", WX, WY, WZ, scale_factor=1.0)
    
    # Save Visual Scale (Multiplied by 1,000,000 for visualization)
    save_to_ply_colored("wada_HD_structure_vis.ply", WX, WY, WZ, scale_factor=1e6)
else:
    print("[!] No points recorded.")