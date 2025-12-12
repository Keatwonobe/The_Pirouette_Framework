import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time
import sys

# Configure numpy for diagnostic printing
np.set_printoptions(precision=60, suppress=False, floatmode='unique')

# ==============================================================================
# I. ACCURATE ARITHMETIC CORE (N-D and DD)
# ==============================================================================

SPLIT = 134217729.0 

@njit(fastmath=True)
def split_double(a):
    c = SPLIT * a
    a_h = c - (c - a)
    a_l = a - a_h
    return a_h, a_l

@njit(fastmath=True)
def two_sum(a, b):
    s = a + b
    v = s - a
    e = (a - (s - v)) + (b - v) 
    return s, e

@njit(fastmath=True)
def two_prod(a, b):
    p = a * b
    a_h, a_l = split_double(a)
    b_h, b_l = split_double(b)
    e = ((a_h * b_h - p) + a_h * b_l + a_l * b_h) + a_l * b_l
    return p, e

@njit(fastmath=True)
def renormalize_nd(x):
    for i in range(len(x) - 1, 0, -1):
        x[i-1], x[i] = two_sum(x[i-1], x[i])
    return x

@njit(fastmath=True)
def nd_translate(center_nd, offset_s):
    N = len(center_nd)
    result_nd = np.zeros_like(center_nd)
    remainder = offset_s 
    for i in range(N):
        s, e = two_sum(center_nd[i], remainder)
        result_nd[i] = s
        remainder = e 
    result_nd = renormalize_nd(result_nd)
    return result_nd

# ==============================================================================
# II. SCALAR PHYSICS KERNEL (DD Optimized)
# ==============================================================================

@njit(fastmath=True)
def get_basin_raw_dd_optimized(m_in_dd, l_in_dd):
    # This kernel is used by BOTH the solver (for boundary detection) and the renderer.
    mh, ml = m_in_dd[0], m_in_dd[1]
    lh, ll = l_in_dd[0], l_in_dd[1]
    
    t_max = 60.0; dt = 0.05; escape_r2 = 16.0; sigma = 1.0
    dt_half = 0.5 * dt; dt_full = dt
    steps = int(t_max / dt)
    s_val = 2.0 * sigma
    
    pmh, pml = 0.0, 0.0
    plh, pll = 0.0, 0.0

    for _ in range(steps):
        # Velocity-Verlet integration steps... (physics kernel is retained)
        # 1. Half Step Velocity (Force calculation 1 & Velocity update 1)
        p_h, p_l = two_prod(mh, lh); p_l += mh * ll + ml * lh; ml_h, ml_l = two_sum(p_h, p_l)
        t1_h, t1_l = two_prod(ml_h, s_val); t1_l += ml_l * s_val; t1_h, t1_l = two_sum(t1_h, t1_l)
        fm_h, e = two_sum(mh, t1_h); e += ml + t1_l; fm_h, fm_l = two_sum(fm_h, e); fm_h = -fm_h; fm_l = -fm_l

        msq_h, msq_l = two_prod(mh, mh); msq_l += 2.0 * mh * ml; msq_h, msq_l = two_sum(msq_h, msq_l)
        lsq_h, lsq_l = two_prod(lh, lh); lsq_l += 2.0 * lh * ll; lsq_h, lsq_l = two_sum(lsq_h, lsq_l)
        diff_h, e = two_sum(msq_h, -lsq_h); e += msq_l - lsq_l; diff_h, diff_l = two_sum(diff_h, e)
        term2_h, term2_l = two_prod(diff_h, sigma); term2_l += diff_l * sigma; term2_h, term2_l = two_sum(term2_h, term2_l)
        fl_h, e = two_sum(lh, term2_h); e += ll + term2_l; fl_h, fl_l = two_sum(fl_h, e); fl_h = -fl_h; fl_l = -fl_l
        
        dh, dl = two_prod(fm_h, dt_half); dl += fm_l * dt_half; dh, dl = two_sum(dh, dl); pmh, e = two_sum(pmh, dh); e += pml + dl; pmh, pml = two_sum(pmh, e)
        dh, dl = two_prod(fl_h, dt_half); dl += fl_l * dt_half; dh, dl = two_sum(dh, dl); plh, e = two_sum(plh, dh); e += pll + dl; plh, pll = two_sum(plh, e)
        
        # 2. Position Update (Full Step)
        dh, dl = two_prod(pmh, dt_full); dl += pml * dt_full; dh, dl = two_sum(dh, dl); mh, e = two_sum(mh, dh); e += ml + dl; mh, ml = two_sum(mh, e)
        dh, dl = two_prod(plh, dt_full); dl += pll * dt_full; dh, dl = two_sum(dh, dl); lh, e = two_sum(lh, dh); e += ll + dl; lh, ll = two_sum(lh, e)

        # 3. Final Half Step Velocity (Force calculation 2 & Velocity update 2)
        p_h, p_l = two_prod(mh, lh); p_l += mh * ll + ml * lh; ml_h, ml_l = two_sum(p_h, p_l)
        t1_h, t1_l = two_prod(ml_h, s_val); t1_l += ml_l * s_val; t1_h, t1_l = two_sum(t1_h, t1_l)
        fm_h, e = two_sum(mh, t1_h); e += ml + t1_l; fm_h, fm_l = two_sum(fm_h, e); fm_h = -fm_h; fm_l = -fm_l
        msq_h, msq_l = two_prod(mh, mh); msq_l += 2.0 * mh * ml; msq_h, msq_l = two_sum(msq_h, msq_l)
        lsq_h, lsq_l = two_prod(lh, lh); lsq_l += 2.0 * lh * ll; lsq_h, lsq_l = two_sum(lsq_h, lsq_l)
        diff_h, e = two_sum(msq_h, -lsq_h); e += msq_l - lsq_l; diff_h, diff_l = two_sum(diff_h, e)
        term2_h, term2_l = two_prod(diff_h, sigma); term2_l += diff_l * sigma; term2_h, term2_l = two_sum(term2_h, term2_l)
        fl_h, e = two_sum(lh, term2_h); e += ll + term2_l; fl_h, fl_l = two_sum(fl_h, e); fl_h = -fl_h; fl_l = -fl_l
        
        dh, dl = two_prod(fm_h, dt_half); dl += fm_l * dt_half; dh, dl = two_sum(dh, dl); pmh, e = two_sum(pmh, dh); e += pml + dl; pmh, pml = two_sum(pmh, e)
        dh, dl = two_prod(fl_h, dt_half); dl += fl_l * dt_half; dh, dl = two_sum(dh, dl); plh, e = two_sum(plh, dh); e += pll + dl; plh, pll = two_sum(plh, e)

        # Escape Check
        if mh*mh + lh*lh > escape_r2:
            angle = np.arctan2(lh, mh)
            # Raw basin logic (1, 2, or 3)
            if angle > 0.5 and angle < 2.6: return 1   
            elif angle <= -2.6 or angle >= 2.6: return 2 
            else: return 3 
            
    return 0 

# ==============================================================================
# III. SEEKER (Boundary Drift Finder)
# ==============================================================================

# Helper function for the seeker logic
@njit(parallel=True)
def get_drift_and_span_nd(res, zoom, center_x_nd, center_y_nd):
    out_map = np.zeros((res, res), dtype=np.int8)
    
    img_cx = (res - 1) / 2.0
    img_cy = (res - 1) / 2.0
    scale = (2.0 * zoom) / res
    
    for y in prange(res):
        for x in range(res):
            offset_x = (x - img_cx) * scale 
            offset_y = (y - img_cy) * scale
            
            abs_x_nd = nd_translate(center_x_nd, offset_x)
            abs_y_nd = nd_translate(center_y_nd, offset_y)
            
            m_dd_in = abs_x_nd[:2]
            l_dd_in = abs_y_nd[:2]

            out_map[y, x] = get_basin_raw_dd_optimized(m_dd_in, l_dd_in)
            
    # --- Boundary/Centroid Calculation ---
    # Simplified boundary detection for drift calculation (not for final render)
    grad_x = np.zeros_like(out_map, dtype=np.int8)
    grad_x[:, 1:] = np.abs(out_map[:, 1:] - out_map[:, :-1])
    grad_y = np.zeros_like(out_map, dtype=np.int8)
    grad_y[1:, :] = np.abs(out_map[1:, :] - out_map[:-1, :])

    boundaries_mask = (grad_x + grad_y) > 0
    y_idxs, x_idxs = np.where(boundaries_mask)
    total_count = len(x_idxs)
    
    if total_count == 0:
        return 0.0, 0.0, 0.0, 0 

    avg_px = np.mean(x_idxs)
    avg_py = np.mean(y_idxs)
    drift_x = (avg_px - img_cx) * scale
    drift_y = (avg_py - img_cy) * scale

    min_px, max_px = np.min(x_idxs), np.max(x_idxs)
    min_py, max_py = np.min(y_idxs), np.max(y_idxs)
    structure_span = max((max_px - min_px) * scale, (max_py - min_py) * scale)
    if structure_span == 0.0: structure_span = 1e-12 
    
    return drift_x, drift_y, structure_span, total_count

@njit
def seek_absolute_tip_hyper_optimized(start_zoom, start_cx, start_cy, N_parts, res_low, max_iterations, safety_margin):
    curr_cx_nd = np.zeros(N_parts, dtype=np.float64)
    curr_cy_nd = np.zeros(N_parts, dtype=np.float64)
    curr_cx_nd[0] = start_cx
    curr_cy_nd[0] = start_cy
    
    curr_zoom = start_zoom
    
    # Store history for the safe backtrack point
    zoom_history = [(start_zoom, curr_cx_nd.copy(), curr_cy_nd.copy())] 

    for i in range(max_iterations):
        drift_x, drift_y, span, count = get_drift_and_span_nd(
            res_low, curr_zoom, curr_cx_nd, curr_cy_nd
        )
        
        if count == 0:
            print(f"Structure Lost at Iteration {i}. Stopping.")
            # Return a safe, known-good point from history
            break
            
        zoom_history.append((curr_zoom, curr_cx_nd.copy(), curr_cy_nd.copy()))
            
        curr_cx_nd = nd_translate(curr_cx_nd, drift_x)
        curr_cy_nd = nd_translate(curr_cy_nd, drift_y)
        
        # --- DIAGNOSTICS ---
        if i < 5 or i % 10 == 0:
            print("Iter:", i, "Zoom:", curr_zoom, "Span:", span, "Points:", count)

        # --- ZOOM STRATEGY ---
        target_from_span = span * 0.6
        force_min_decay = curr_zoom * 0.8  
        force_max_decay = curr_zoom * 0.01 
        
        if target_from_span > force_min_decay:
            curr_zoom = force_min_decay
        elif target_from_span < force_max_decay:
            curr_zoom = force_max_decay
        else:
            curr_zoom = target_from_span
        
        if curr_zoom < 1e-60:
            print("Target Precision Reached.")
            break
            
    # --- Final Safe Point Selection ---
    if len(zoom_history) <= safety_margin:
        # If the dive was too shallow, just use the last point
        safe_index = -1
    else:
        # Backtrack by the safety margin to a known-visible point
        safe_index = -(safety_margin + 1)
        
    final_zoom, final_cx_nd, final_cy_nd = zoom_history[safe_index]
            
    return final_zoom, final_cx_nd, final_cy_nd

# ==============================================================================
# IV. RENDERER (Boundary Point Cloud Generator)
# ==============================================================================

@njit(parallel=True)
def render_boundary_point_cloud(width, height, zoom, cx_nd, cy_nd):
    
    max_pts = width * height 
    boundary_pts = np.zeros((max_pts, 2), dtype=np.float64) 
    basin_map = np.zeros((height, width), dtype=np.int32)
    point_count = 0
    
    img_cx = (width - 1) / 2.0
    img_cy = (height - 1) / 2.0
    scale = (2.0 * zoom) / width 
    
    for y in prange(height):
        offset_y = (y - img_cy) * scale
        abs_y_nd = nd_translate(cy_nd, offset_y)
        l_dd = abs_y_nd[:2]
        l_real = abs_y_nd[0] + abs_y_nd[1]

        basin_curr = 0 

        for x in range(width):
            offset_x = (x - img_cx) * scale 
            abs_x_nd = nd_translate(cx_nd, offset_x)
            m_dd = abs_x_nd[:2]
            m_real = abs_x_nd[0] + abs_x_nd[1]
            
            basin_next = get_basin_raw_dd_optimized(m_dd, l_dd)
            basin_map[y, x] = basin_next
            
            is_boundary = False
            
            # Check X-gradient (change from previous column)
            if x > 0 and basin_next != basin_curr and basin_next != 0 and basin_curr != 0:
                is_boundary = True
            
            # Check Y-gradient (change from previous row)
            if y > 0 and basin_next != basin_map[y-1, x] and basin_next != 0 and basin_map[y-1, x] != 0:
                is_boundary = True
            
            if is_boundary and point_count < max_pts:
                boundary_pts[point_count, 0] = m_real
                boundary_pts[point_count, 1] = l_real
                point_count += 1
            
            basin_curr = basin_next

    return boundary_pts[:point_count, :]

# ==============================================================================
# V. FUSION EXECUTION
# ==============================================================================

if __name__ == '__main__':
    # --- Solver Parameters ---
    N_PARTS = 4          
    RES_LOW = 4000
    MAX_ITER = 300
    START_ZOOM = 1.0
    START_CX = 0.5
    START_CY = 0.5
    SAFETY_MARGIN = 5 # Backtrack 5 steps from the point where structure was lost

    # --- Renderer Parameters ---
    RENDER_WIDTH, RENDER_HEIGHT = 8000, 8000 # High-resolution target

    # 1. RUN THE SOLVER TO FIND A SAFE POINT
    print(f"[-] Starting AGGRESSIVE Deep Dive (N={N_PARTS}) to find safe point...")
    t0_solve = time.time()
    
    safe_zoom, safe_cx_nd, safe_cy_nd = seek_absolute_tip_hyper_optimized(
        START_ZOOM, START_CX, START_CY, N_PARTS, RES_LOW, MAX_ITER, SAFETY_MARGIN
    )
    
    t_solve = time.time() - t0_solve
    print(f"[+] Solver complete in {t_solve:.2f} seconds.")
    
    print(f"\n[+] SAFE RESCUE POINT ACQUIRED (Backtracked {SAFETY_MARGIN} steps):")
    print(f"    Zoom: {safe_zoom}")
    print(f"    Center X N-D: {safe_cx_nd}")
    print(f"    Center Y N-D: {safe_cy_nd}")

    print("---")
    
    # 2. RUN THE RENDERER AT THE SAFE POINT
    print(f"[-] Starting High-Resolution Point Cloud Render.")
    print(f"    Target Zoom: {safe_zoom:.2e} at {RENDER_WIDTH}x{RENDER_HEIGHT} resolution.")
    
    t0_render = time.time()
    point_cloud = render_boundary_point_cloud(
        RENDER_WIDTH, RENDER_HEIGHT, safe_zoom, safe_cx_nd, safe_cy_nd
    )
    t_render = time.time() - t0_render
    
    print(f"[+] Render complete in {t_render:.2f} seconds.")
    
    # 3. VISUALIZE AND SAVE
    if point_cloud.shape[0] > 0:
        print(f"[+] Total boundary points found: {point_cloud.shape[0]:,}")
        
        plt.figure(figsize=(10, 10))
        plt.scatter(point_cloud[:, 0], point_cloud[:, 1], s=0.05, color='magenta', marker='.')
        
        center_m = safe_cx_nd[0] 
        center_l = safe_cy_nd[0]
        
        plt.title(f"Wada Basin Tip Boundary Point Cloud (Zoom: {safe_zoom:.2e})")
        plt.xlabel(f"m (Center: {center_m:.4f} + O(1e-17))")
        plt.ylabel(f"l (Center: {center_l:.4f} + O(1e-17))")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.tight_layout()
        
        output_filename = f"wada_fusion_tip_{RENDER_WIDTH}x{RENDER_HEIGHT}_{safe_zoom:.2e}.png"
        plt.savefig(output_filename, dpi=300)
        print(f"[+] Visualization saved to: {output_filename}")
        
    else:
        print("[!] Final Warning: Structure not found even with safety backtrack. Check precision limit.")