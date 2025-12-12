import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time

# Configure numpy for diagnostic printing
np.set_printoptions(precision=60, suppress=False, floatmode='unique')

# ==============================================================================
# I. ACCURATE ARITHMETIC CORE (N-D and DD)
# STRICTLY NO FASTMATH HERE - IT BREAKS ERROR TRACKING
# ==============================================================================

SPLIT = 134217729.0 

@njit
def split_double(a):
    c = SPLIT * a
    a_h = c - (c - a)
    a_l = a - a_h
    return a_h, a_l

@njit
def two_sum(a, b):
    s = a + b
    v = s - a
    e = (a - (s - v)) + (b - v) 
    return s, e

@njit
def two_prod(a, b):
    p = a * b
    a_h, a_l = split_double(a)
    b_h, b_l = split_double(b)
    e = ((a_h * b_h - p) + a_h * b_l + a_l * b_h) + a_l * b_l
    return p, e

@njit
def renormalize_nd(x):
    for i in range(len(x) - 1, 0, -1):
        x[i-1], x[i] = two_sum(x[i-1], x[i])
    return x

@njit
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

# Fastmath is generally okay for the loop logic, just not the DD ops above
@njit(fastmath=True) 
def get_basin_raw_dd_optimized(m_in_dd, l_in_dd):
    mh, ml = m_in_dd[0], m_in_dd[1]
    lh, ll = l_in_dd[0], l_in_dd[1]
    
    t_max = 60.0; dt = 0.05; escape_r2 = 16.0; sigma = 1.0
    dt_half = 0.5 * dt; dt_full = dt
    steps = int(t_max / dt)
    s_val = 2.0 * sigma
    
    pmh, pml = 0.0, 0.0
    plh, pll = 0.0, 0.0

    for _ in range(steps):
        # 1. Half Step Velocity
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
        
        # 2. Position Update
        dh, dl = two_prod(pmh, dt_full); dl += pml * dt_full; dh, dl = two_sum(dh, dl); mh, e = two_sum(mh, dh); e += ml + dl; mh, ml = two_sum(mh, e)
        dh, dl = two_prod(plh, dt_full); dl += pll * dt_full; dh, dl = two_sum(dh, dl); lh, e = two_sum(lh, dh); e += ll + dl; lh, ll = two_sum(lh, e)

        # 3. Final Half Step Velocity
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

        if mh*mh + lh*lh > escape_r2:
            angle = np.arctan2(lh, mh)
            if angle > 0.5 and angle < 2.6: return 1   
            elif angle <= -2.6 or angle >= 2.6: return 2 
            else: return 3 
            
    return 0 

# ==============================================================================
# III. SEEKER (Boundary Drift Finder)
# ==============================================================================

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
            
            # Extract high parts for physics (but passed as DD)
            m_dd_in = abs_x_nd[:2]
            l_dd_in = abs_y_nd[:2]

            out_map[y, x] = get_basin_raw_dd_optimized(m_dd_in, l_dd_in)
            
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
    zoom_history = [(start_zoom, curr_cx_nd.copy(), curr_cy_nd.copy())] 

    for i in range(max_iterations):
        drift_x, drift_y, span, count = get_drift_and_span_nd(
            res_low, curr_zoom, curr_cx_nd, curr_cy_nd
        )
        
        if count == 0:
            print(f"Structure Lost at Iteration {i}. Stopping.")
            break
            
        zoom_history.append((curr_zoom, curr_cx_nd.copy(), curr_cy_nd.copy()))
            
        curr_cx_nd = nd_translate(curr_cx_nd, drift_x)
        curr_cy_nd = nd_translate(curr_cy_nd, drift_y)
        
        if i < 5 or i % 10 == 0:
            print("Iter:", i, "Zoom:", curr_zoom, "Span:", span, "Points:", count)

        target_from_span = span * 0.6
        force_min_decay = curr_zoom * 0.8  
        force_max_decay = curr_zoom * 0.01 
        
        if target_from_span > force_min_decay:
            curr_zoom = force_min_decay
        elif target_from_span < force_max_decay:
            curr_zoom = force_max_decay
        else:
            curr_zoom = target_from_span
        
        # Stop before underflow
        if curr_zoom < 1e-100:
            print("Target Precision Reached.")
            break
            
    if len(zoom_history) <= safety_margin:
        safe_index = -1
    else:
        safe_index = -(safety_margin + 1)
        
    final_zoom, final_cx_nd, final_cy_nd = zoom_history[safe_index]
    return final_zoom, final_cx_nd, final_cy_nd

# ==============================================================================
# IV. RENDERER (Boundary Point Cloud Generator)
# ==============================================================================

@njit(parallel=True)
def render_boundary_point_cloud_pixels(width, height, zoom, cx_nd, cy_nd):
    
    max_pts = width * height 
    # Store X, Y PIXEL coordinates (Int32) to avoid float64 precision collapse
    boundary_pts = np.zeros((max_pts, 2), dtype=np.int32) 
    basin_map = np.zeros((height, width), dtype=np.int32)
    point_count = 0
    
    img_cx = (width - 1) / 2.0
    img_cy = (height - 1) / 2.0
    scale = (2.0 * zoom) / width 
    
    for y in prange(height):
        offset_y = (y - img_cy) * scale
        abs_y_nd = nd_translate(cy_nd, offset_y)
        l_dd = abs_y_nd[:2]

        basin_curr = 0 

        for x in range(width):
            offset_x = (x - img_cx) * scale 
            abs_x_nd = nd_translate(cx_nd, offset_x)
            m_dd = abs_x_nd[:2]
            
            basin_next = get_basin_raw_dd_optimized(m_dd, l_dd)
            basin_map[y, x] = basin_next
            
            is_boundary = False
            
            if x > 0 and basin_next != basin_curr and basin_next != 0 and basin_curr != 0:
                is_boundary = True
            
            if y > 0 and basin_next != basin_map[y-1, x] and basin_next != 0 and basin_map[y-1, x] != 0:
                is_boundary = True
            
            if is_boundary:
                # Thread-safe increment is tricky in Numba parallel without atomics
                # BUT for a simple render, we can just fill and slice later, or use atomics.
                # However, for simplicity/speed in this context, let's just use a relaxed 
                # index calculation or return the MAP and post-process?
                # Actually, standard pattern for Numba parallel filling:
                # We will output the WHOLE map to avoid race conditions on the index,
                # then extract points in Python (fast enough).
                pass
            
            basin_curr = basin_next
            
    return basin_map

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
    SAFETY_MARGIN = 5 

    # --- Renderer Parameters ---
    RENDER_WIDTH, RENDER_HEIGHT = 8000, 8000 

    # 1. RUN THE SOLVER
    print(f"[-] Starting AGGRESSIVE Deep Dive (N={N_PARTS}) to find safe point...")
    t0_solve = time.time()
    
    safe_zoom, safe_cx_nd, safe_cy_nd = seek_absolute_tip_hyper_optimized(
        START_ZOOM, START_CX, START_CY, N_PARTS, RES_LOW, MAX_ITER, SAFETY_MARGIN
    )
    
    t_solve = time.time() - t0_solve
    print(f"[+] Solver complete in {t_solve:.2f} seconds.")
    
    print(f"\n[+] SAFE RESCUE POINT ACQUIRED:")
    print(f"    Zoom: {safe_zoom}")
    print(f"    Center X N-D: {safe_cx_nd}") # You should see non-zero lower components now!
    print(f"    Center Y N-D: {safe_cy_nd}")

    print("---")
    
    # 2. RUN THE RENDERER
    print(f"[-] Starting High-Resolution Raster Render.")
    
    t0_render = time.time()
    # We get the full map back now to avoid race conditions and precision loss
    basin_map = render_boundary_point_cloud_pixels(
        RENDER_WIDTH, RENDER_HEIGHT, safe_zoom, safe_cx_nd, safe_cy_nd
    )
    t_render = time.time() - t0_render
    print(f"[+] Render complete in {t_render:.2f} seconds.")

    # 3. EXTRACT BOUNDARIES (Python Side)
    # This is fast enough for 8k images and avoids complex Numba atomics
    print("[-] extracting boundaries...")
    grad_x = np.abs(basin_map[:, 1:] - basin_map[:, :-1])
    grad_y = np.abs(basin_map[1:, :] - basin_map[:-1, :])
    boundary_mask = np.zeros_like(basin_map, dtype=bool)
    boundary_mask[:, 1:] |= (grad_x > 0)
    boundary_mask[1:, :] |= (grad_y > 0)
    
    y_idxs, x_idxs = np.where(boundary_mask)
    
    print(f"[+] Total boundary points found: {len(x_idxs):,}")

    if len(x_idxs) > 0:
        plt.figure(figsize=(10, 10))
        # Plot PIXELS, not coordinates. This guarantees visualization.
        # Invert Y to match image coordinates
        plt.scatter(x_idxs, RENDER_HEIGHT - y_idxs, s=0.01, color='magenta', marker='.')
        
        plt.title(f"Wada Basin Tip (Zoom: {safe_zoom:.2e})\nPixel Space View")
        plt.xlabel("X Pixels")
        plt.ylabel("Y Pixels")
        plt.gca().set_aspect('equal')
        plt.tight_layout()
        
        output_filename = f"wada_fusion_tip_PIXEL_VIEW.png"
        plt.savefig(output_filename, dpi=300)
        print(f"[+] Visualization saved to: {output_filename}")
        
    else:
        print("[!] Final Warning: Structure not found.")