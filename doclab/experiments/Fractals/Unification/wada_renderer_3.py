import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time
import sys

# Configure numpy for diagnostic printing (optional for final script)
np.set_printoptions(precision=60, suppress=False, floatmode='unique')

# --- Final Coordinates from Solver ---
CRASH_ZOOM = 4.069833027880832e-26
CX_ND = np.array([1.8957546994896471e-01, -7.8646858760256740e-18, 1.9470281951771243e-35, 0.0], dtype=np.float64)
CY_ND = np.array([8.9253006402176494e-01, -2.0606566938730768e-17, -1.3099289236722358e-33, 0.0], dtype=np.float64)


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
    # This function is a slightly streamlined version of the solver/renderer
    # kernel, returning the raw basin ID (1, 2, or 3) based on escape angle.
    mh, ml = m_in_dd[0], m_in_dd[1]
    lh, ll = l_in_dd[0], l_in_dd[1]
    
    t_max = 60.0; dt = 0.05; escape_r2 = 16.0; sigma = 1.0
    dt_half = 0.5 * dt; dt_full = dt
    steps = int(t_max / dt)
    s_val = 2.0 * sigma
    
    pmh, pml = 0.0, 0.0
    plh, pll = 0.0, 0.0

    # The full optimized velocity-Verlet integration loop is retained for accuracy
    for _ in range(steps):
        # 1. Half Step Velocity (Force calculation 1 & Velocity update 1)
        p_h, p_l = two_prod(mh, lh); p_l += mh * ll + ml * lh; ml_h, ml_l = two_sum(p_h, p_l)
        t1_h, t1_l = two_prod(ml_h, s_val); t1_l += ml_l * s_val; t1_h, t1_l = two_sum(t1_h, t1_l)
        fm_h, e = two_sum(mh, t1_h); e += ml + t1_l; fm_h, fm_l = two_sum(fm_h, e)
        fm_h = -fm_h; fm_l = -fm_l

        msq_h, msq_l = two_prod(mh, mh); msq_l += 2.0 * mh * ml; msq_h, msq_l = two_sum(msq_h, msq_l)
        lsq_h, lsq_l = two_prod(lh, lh); lsq_l += 2.0 * lh * ll; lsq_h, lsq_l = two_sum(lsq_h, lsq_l)
        diff_h, e = two_sum(msq_h, -lsq_h); e += msq_l - lsq_l; diff_h, diff_l = two_sum(diff_h, e)
        term2_h, term2_l = two_prod(diff_h, sigma); term2_l += diff_l * sigma; term2_h, term2_l = two_sum(term2_h, term2_l)
        fl_h, e = two_sum(lh, term2_h); e += ll + term2_l; fl_h, fl_l = two_sum(fl_h, e)
        fl_h = -fl_h; fl_l = -fl_l
        
        dh, dl = two_prod(fm_h, dt_half); dl += fm_l * dt_half; dh, dl = two_sum(dh, dl)
        pmh, e = two_sum(pmh, dh); e += pml + dl; pmh, pml = two_sum(pmh, e)
        dh, dl = two_prod(fl_h, dt_half); dl += fl_l * dt_half; dh, dl = two_sum(dh, dl)
        plh, e = two_sum(plh, dh); e += pll + dl; plh, pll = two_sum(plh, e)
        
        # 2. Position Update (Full Step)
        dh, dl = two_prod(pmh, dt_full); dl += pml * dt_full; dh, dl = two_sum(dh, dl)
        mh, e = two_sum(mh, dh); e += ml + dl; mh, ml = two_sum(mh, e)
        dh, dl = two_prod(plh, dt_full); dl += pll * dt_full; dh, dl = two_sum(dh, dl)
        lh, e = two_sum(lh, dh); e += ll + dl; lh, ll = two_sum(lh, e)

        # 3. Final Half Step Velocity (Force calculation 2 & Velocity update 2)
        p_h, p_l = two_prod(mh, lh); p_l += mh * ll + ml * lh; ml_h, ml_l = two_sum(p_h, p_l)
        t1_h, t1_l = two_prod(ml_h, s_val); t1_l += ml_l * s_val; t1_h, t1_l = two_sum(t1_h, t1_l)
        fm_h, e = two_sum(mh, t1_h); e += ml + t1_l; fm_h, fm_l = two_sum(fm_h, e)
        fm_h = -fm_h; fm_l = -fm_l
        msq_h, msq_l = two_prod(mh, mh); msq_l += 2.0 * mh * ml; msq_h, msq_l = two_sum(msq_h, msq_l)
        lsq_h, lsq_l = two_prod(lh, lh); lsq_l += 2.0 * lh * ll; lsq_h, lsq_l = two_sum(lsq_h, lsq_l)
        diff_h, e = two_sum(msq_h, -lsq_h); e += msq_l - lsq_l; diff_h, diff_l = two_sum(diff_h, e)
        term2_h, term2_l = two_prod(diff_h, sigma); term2_l += diff_l * sigma; term2_h, term2_l = two_sum(term2_h, term2_l)
        fl_h, e = two_sum(lh, term2_h); e += ll + term2_l; fl_h, fl_l = two_sum(fl_h, e)
        fl_h = -fl_h; fl_l = -fl_l
        
        dh, dl = two_prod(fm_h, dt_half); dl += fm_l * dt_half; dh, dl = two_sum(dh, dl)
        pmh, e = two_sum(pmh, dh); e += pml + dl; pmh, pml = two_sum(pmh, e)
        dh, dl = two_prod(fl_h, dt_half); dl += fl_l * dt_half; dh, dl = two_sum(dh, dl)
        plh, e = two_sum(plh, dh); e += pll + dl; plh, pll = two_sum(plh, e)

        # Escape Check
        if mh*mh + lh*lh > escape_r2:
            angle = np.arctan2(lh, mh)
            # The raw basin logic:
            if angle > 0.5 and angle < 2.6: return 1   # Basin 1
            elif angle <= -2.6 or angle >= 2.6: return 2 # Basin 2
            else: return 3 # Basin 3
            
    return 0 # Did not escape

# ==============================================================================
# III. HIGH-RES BOUNDARY RENDERER
# ==============================================================================

@njit(parallel=True)
def render_boundary_point_cloud(width, height, zoom, cx_nd, cy_nd):
    
    # Pre-allocate for the point cloud (max possible size for Numba)
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

        basin_curr = 0 # Initialize for the horizontal (X) gradient check

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
# IV. EXECUTION
# ==============================================================================

if __name__ == '__main__':
    WIDTH, HEIGHT = 8000, 8000 # High-resolution grid

    # BACKTRACK: Using a slightly coarser zoom from the solver's log (approx. Iter 250)
    BACKTRACK_ZOOM = 5.922386521532941e-25
    
    # Use the FINAL, most precise coordinates
    CX_ND = np.array([1.8957546994896471e-01, -7.8646858760256740e-18, 1.9470281951771243e-35, 0.0], dtype=np.float64)
    CY_ND = np.array([8.9253006402176494e-01, -2.0606566938730768e-17, -1.3099289236722358e-33, 0.0], dtype=np.float64)
    
    print(f"[-] Starting Backtrack Render.")
    print(f"    Target Zoom: {BACKTRACK_ZOOM:.2e} at {WIDTH}x{HEIGHT} resolution.")

    print(f"[-] Starting Boundary Point Cloud Rescue Render.")
    print(f"    Target Zoom: {CRASH_ZOOM:.2e} at {WIDTH}x{HEIGHT} resolution.")
    
    t0 = time.time()
    point_cloud = render_boundary_point_cloud(WIDTH, HEIGHT, BACKTRACK_ZOOM, CX_ND, CY_ND)
    t_render = time.time() - t0
    
    print(f"[+] Render complete in {t_render:.2f} seconds.")
    
    if point_cloud.shape[0] > 0:
        print(f"[+] Total boundary points found: {point_cloud.shape[0]:,}")
        
        # --- Visualization ---
        plt.figure(figsize=(10, 10))
        
        # Plot the boundary points in 'regular-land' (real-world coordinates)
        # We use a small point size (s=0.1) because the boundary is fractal
        plt.scatter(point_cloud[:, 0], point_cloud[:, 1], s=0.1, color='magenta', marker='.')
        
        # The center of the image is just the high part of the N-D coordinates
        center_m = CX_ND[0] 
        center_l = CY_ND[0]
        
        plt.title(f"Wada Basin Tip Boundary Point Cloud (Zoom: {CRASH_ZOOM:.2e})")
        plt.xlabel(f"m (Center: {center_m:.4f} + O(1e-17))")
        plt.ylabel(f"l (Center: {center_l:.4f} + O(1e-17))")
        plt.gca().set_aspect('equal', adjustable='box')
        
        # Save the plot
        output_filename = "wada_boundary_point_cloud_4000x4000.png"
        plt.savefig(output_filename, dpi=300)
        print(f"[+] Visualization saved to: {output_filename}")
        
        # Optionally save the raw data
        # np.savetxt("wada_tip_point_cloud.csv", point_cloud, delimiter=",")
        
    else:
        print("[!] Warning: No non-zero boundary points were found. The structure may have been lost.")