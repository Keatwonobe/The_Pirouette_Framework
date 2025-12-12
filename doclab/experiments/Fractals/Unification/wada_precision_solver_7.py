import numpy as np
from numba import njit, prange
import sys

# Configure numpy to show us the truth (all digits, no scientific suppression)
np.set_printoptions(precision=60, suppress=False, floatmode='unique')

# ==============================================================================
# I. ACCURATE ARITHMETIC CORE (NO FASTMATH)
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

# --- N-D ARRAY TOOLS ---

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
# II. SCALAR PHYSICS KERNEL
# ==============================================================================

@njit
def get_basin_single_dd_optimized(m_in_dd, l_in_dd, t_max=60.0, dt=0.05, escape_r2=16.0):
    mh, ml = m_in_dd[0], m_in_dd[1]
    lh, ll = l_in_dd[0], l_in_dd[1]
    
    pmh, pml = 0.0, 0.0
    plh, pll = 0.0, 0.0
    
    sigma = 1.0; dt_half = 0.5 * dt; dt_full = dt
    steps = int(t_max / dt)
    s_val = 2.0 * sigma
    
    for _ in range(steps):
        # --- 1. HALF STEP VELOCITY ---
        p_h, p_l = two_prod(mh, lh)
        p_l += mh * ll + ml * lh
        ml_h, ml_l = two_sum(p_h, p_l)
        
        t1_h, t1_l = two_prod(ml_h, s_val)
        t1_l += ml_l * s_val
        t1_h, t1_l = two_sum(t1_h, t1_l)
        
        fm_h, e = two_sum(mh, t1_h)
        e += ml + t1_l
        fm_h, fm_l = two_sum(fm_h, e)
        fm_h = -fm_h; fm_l = -fm_l

        msq_h, msq_l = two_prod(mh, mh)
        msq_l += 2.0 * mh * ml
        msq_h, msq_l = two_sum(msq_h, msq_l)
        
        lsq_h, lsq_l = two_prod(lh, lh)
        lsq_l += 2.0 * lh * ll
        lsq_h, lsq_l = two_sum(lsq_h, lsq_l)
        
        diff_h, e = two_sum(msq_h, -lsq_h)
        e += msq_l - lsq_l
        diff_h, diff_l = two_sum(diff_h, e)
        
        term2_h, term2_l = two_prod(diff_h, sigma)
        term2_l += diff_l * sigma
        term2_h, term2_l = two_sum(term2_h, term2_l)
        
        fl_h, e = two_sum(lh, term2_h)
        e += ll + term2_l
        fl_h, fl_l = two_sum(fl_h, e)
        fl_h = -fl_h; fl_l = -fl_l
        
        dh, dl = two_prod(fm_h, dt_half)
        dl += fm_l * dt_half
        dh, dl = two_sum(dh, dl)
        pmh, e = two_sum(pmh, dh)
        e += pml + dl
        pmh, pml = two_sum(pmh, e)

        dh, dl = two_prod(fl_h, dt_half)
        dl += fl_l * dt_half
        dh, dl = two_sum(dh, dl)
        plh, e = two_sum(plh, dh)
        e += pll + dl
        plh, pll = two_sum(plh, e)
        
        # --- 2. POSITION UPDATE (Full Step) ---
        dh, dl = two_prod(pmh, dt_full)
        dl += pml * dt_full
        dh, dl = two_sum(dh, dl)
        mh, e = two_sum(mh, dh)
        e += ml + dl
        mh, ml = two_sum(mh, e)
        
        dh, dl = two_prod(plh, dt_full)
        dl += pll * dt_full
        dh, dl = two_sum(dh, dl)
        lh, e = two_sum(lh, dh)
        e += ll + dl
        lh, ll = two_sum(lh, e)

        # --- 3. RECALCULATE FORCES ---
        p_h, p_l = two_prod(mh, lh)
        p_l += mh * ll + ml * lh
        ml_h, ml_l = two_sum(p_h, p_l)
        
        t1_h, t1_l = two_prod(ml_h, s_val)
        t1_l += ml_l * s_val
        t1_h, t1_l = two_sum(t1_h, t1_l)
        
        fm_h, e = two_sum(mh, t1_h)
        e += ml + t1_l
        fm_h, fm_l = two_sum(fm_h, e)
        fm_h = -fm_h; fm_l = -fm_l

        msq_h, msq_l = two_prod(mh, mh)
        msq_l += 2.0 * mh * ml
        msq_h, msq_l = two_sum(msq_h, msq_l)
        lsq_h, lsq_l = two_prod(lh, lh)
        lsq_l += 2.0 * lh * ll
        lsq_h, lsq_l = two_sum(lsq_h, lsq_l)
        diff_h, e = two_sum(msq_h, -lsq_h)
        e += msq_l - lsq_l
        diff_h, diff_l = two_sum(diff_h, e)
        term2_h, term2_l = two_prod(diff_h, sigma)
        term2_l += diff_l * sigma
        term2_h, term2_l = two_sum(term2_h, term2_l)
        fl_h, e = two_sum(lh, term2_h)
        e += ll + term2_l
        fl_h, fl_l = two_sum(fl_h, e)
        fl_h = -fl_h; fl_l = -fl_l
        
        # --- 4. HALF STEP VELOCITY (Final) ---
        dh, dl = two_prod(fm_h, dt_half)
        dl += fm_l * dt_half
        dh, dl = two_sum(dh, dl)
        pmh, e = two_sum(pmh, dh)
        e += pml + dl
        pmh, pml = two_sum(pmh, e)

        dh, dl = two_prod(fl_h, dt_half)
        dl += fl_l * dt_half
        dh, dl = two_sum(dh, dl)
        plh, e = two_sum(plh, dh)
        e += pll + dl
        plh, pll = two_sum(plh, e)

        if mh*mh + lh*lh > escape_r2:
            angle = np.arctan2(lh, mh)
            if angle > 0.5 and angle < 2.6: return 1
            elif angle <= -2.6 or angle >= 2.6: return 2
            else: return 3
            
    return 0

# ==============================================================================
# III. SEEKER AND DRIFT LOGIC
# ==============================================================================

@njit(parallel=True)
def get_drift_and_span_nd(res, zoom, center_x_nd, center_y_nd):
    out_map = np.zeros((res, res), dtype=np.int8)
    
    img_cx = (res - 1) / 2.0
    img_cy = (res - 1) / 2.0
    scale = (2.0 * zoom) / res
    deg120 = 2.094395; deg240 = 4.188790 
    
    for y in prange(res):
        for x in range(res):
            offset_x = (x - img_cx) * scale 
            offset_y = (y - img_cy) * scale
            
            abs_x_nd = nd_translate(center_x_nd, offset_x)
            abs_y_nd = nd_translate(center_y_nd, offset_y)
            
            m_dd_in = abs_x_nd[:2]
            l_dd_in = abs_y_nd[:2]

            basin = get_basin_single_dd_optimized(m_dd_in, l_dd_in)
            
            if basin != 0: 
                m_in = abs_x_nd[0] + abs_x_nd[1] 
                l_in = abs_y_nd[0] + abs_y_nd[1]
                theta = np.arctan2(l_in, m_in)
                if theta < 0: theta += 2*np.pi
                rot = 0
                if theta >= deg240: rot = 2
                elif theta >= deg120: rot = 1
                out_map[y, x] = (basin - 1 + rot) % 3 + 1
            
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

    if np.abs(drift_x) < 1e-10 * scale: 
        drift_x += 1e-6 * scale 
        drift_y -= 1e-6 * scale 
        
    min_px, max_px = np.min(x_idxs), np.max(x_idxs)
    min_py, max_py = np.min(y_idxs), np.max(y_idxs)
    structure_span = max((max_px - min_px) * scale, (max_py - min_py) * scale)
    if structure_span == 0.0: structure_span = 1e-12 
    
    return drift_x, drift_y, structure_span, total_count

@njit
def seek_absolute_tip_hyper_optimized(start_zoom, start_cx, start_cy, N_parts, res_low, max_iterations):
    curr_cx_nd = np.zeros(N_parts, dtype=np.float64)
    curr_cy_nd = np.zeros(N_parts, dtype=np.float64)
    curr_cx_nd[0] = start_cx
    curr_cy_nd[0] = start_cy
    
    curr_zoom = start_zoom
    
    last_valid_zoom = start_zoom
    last_valid_cx_nd = curr_cx_nd.copy()
    last_valid_cy_nd = curr_cy_nd.copy()

    for i in range(max_iterations):
        drift_x, drift_y, span, count = get_drift_and_span_nd(
            res_low, curr_zoom, curr_cx_nd, curr_cy_nd
        )
        
        if count == 0:
            print("Structure Lost! Stopping.")
            break
            
        last_valid_zoom = curr_zoom
        last_valid_cx_nd[:] = curr_cx_nd[:]
        last_valid_cy_nd[:] = curr_cy_nd[:]
            
        curr_cx_nd = nd_translate(curr_cx_nd, drift_x)
        curr_cy_nd = nd_translate(curr_cy_nd, drift_y)
        
        # --- FIX: REMOVED F-STRING FORMATTING ---
        if i < 3 or i % 20 == 0:
            # Simple print that Numba can handle
            print("Iter:", i, "Zoom:", curr_zoom, "Span:", span)
            
            if curr_zoom < 1e-16 and abs(curr_cx_nd[1]) < 1e-30:
                 print("  WARNING: Tail is zero! Precision loss suspected.")

        target_zoom = span * 0.55
        potential_new_zoom = max(target_zoom, curr_zoom * 0.1) 
        curr_zoom = min(curr_zoom, potential_new_zoom)
        
        if curr_zoom < 1e-60:
            print("Target Precision Reached.")
            break
            
    return last_valid_zoom, last_valid_cx_nd, last_valid_cy_nd

# ==============================================================================
# IV. EXECUTION
# ==============================================================================

if __name__ == '__main__':
    N_PARTS = 4          
    RES_LOW = 400
    MAX_ITER = 300
    
    START_ZOOM = 1.0
    START_CX = 0.5
    START_CY = 0.5
    
    print(f"[-] Starting DIAGNOSTIC Deep Dive (N={N_PARTS}) from ({START_CX}, {START_CY})...")
    
    final_zoom, final_cx_nd, final_cy_nd = seek_absolute_tip_hyper_optimized(
        START_ZOOM, START_CX, START_CY, N_PARTS, RES_LOW, MAX_ITER
    )
    
    print(f"\n[+] Deepest Valid Point Found:")
    print(f"    Final Zoom: {final_zoom}")
    print(f"    Center X N-D: {final_cx_nd}")
    print(f"    Center Y N-D: {final_cy_nd}")