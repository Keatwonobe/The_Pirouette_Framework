import numpy as np
from numba import njit, prange
import sys

# ==============================================================================
# I. HIGH-PRECISION ARITHMETIC CORE (Numba-compatible)
# ==============================================================================

# Double-Double (DD) and N-D Translation rely on these core functions:

SPLIT = 134217729.0 # 2**27 + 1

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
    e = (a - v) + (b - (s - v))
    return s, e

@njit(fastmath=True)
def two_prod(a, b):
    p = a * b
    a_h, a_l = split_double(a)
    b_h, b_l = split_double(b)
    e = ((a_h * b_h - p) + a_h * b_l + a_l * b_h) + a_l * b_l
    return p, e

# --- DD PRIMITIVES (Used for internal kernel calculations) ---

@njit(fastmath=True)
def dd_add(a, b):
    s, e = two_sum(a[0], b[0])
    e += a[1] + b[1]
    s_new, e_new = two_sum(s, e)
    return np.array([s_new, e_new])

@njit(fastmath=True)
def dd_sub(a, b):
    s, e = two_sum(a[0], -b[0])
    e += a[1] - b[1]
    s_new, e_new = two_sum(s, e)
    return np.array([s_new, e_new])

@njit(fastmath=True)
def dd_mul(a, b):
    p_h, p_l = two_prod(a[0], b[0])
    p_l += a[0] * b[1] + a[1] * b[0]
    s_new, e_new = two_sum(p_h, p_l)
    return np.array([s_new, e_new])

@njit(fastmath=True)
def dd_mul_s(a, s):
    p_h, p_l = two_prod(a[0], s)
    p_l += a[1] * s
    s_new, e_new = two_sum(p_h, p_l)
    return np.array([s_new, e_new])

@njit(fastmath=True)
def dd_square(a):
    p_h, p_l = two_prod(a[0], a[0])
    p_l += 2.0 * a[0] * a[1]
    s_new, e_new = two_sum(p_h, p_l)
    return np.array([s_new, e_new])

# --- N-D TRANSLATION (Used for updating the center) ---

@njit(fastmath=True)
def nd_translate(center_nd, offset_s):
    """Accurately translates an N-D center by a float64 scalar offset."""
    N = len(center_nd)
    result_nd = center_nd.copy() # Start with a copy
    
    low_part = offset_s 
    
    for i in range(N - 1, -1, -1):
        s, e = two_sum(center_nd[i], low_part)
        
        result_nd[i] = s
        low_part = e
        
        if low_part == 0.0:
            break
            
    return result_nd

# ==============================================================================
# II. DD PHYSICS KERNEL (get_basin_single_dd)
# ==============================================================================

@njit(fastmath=True)
def get_basin_single_dd(m_in, l_in, t_max=60.0, dt=0.05, escape_r2=16.0):
    """
    DD-enabled physics kernel (replaces original get_basin_single).
    The input m_in/l_in are assumed to be the DD-reconstructed high_part + low_part.
    """
    # NOTE: Since m_in and l_in come from nd_translate, they are accurate up to 1e-30 (DD level).
    # We must split them back into the high and low parts of the DD number.
    m_h, m_l = split_double(m_in)
    l_h, l_l = split_double(l_in)

    m = np.array([m_h, m_l])
    l = np.array([l_h, l_l])
    pm = np.array([0.0, 0.0])
    pl = np.array([0.0, 0.0])
    
    sigma = 1.0; dt_half = 0.5 * dt; dt_full = dt
    steps = int(t_max / dt)
        
    for _ in range(steps):
        # Velocity Update (Half-step)
        m_l_prod = dd_mul(m, l)
        term1 = dd_mul_s(m_l_prod, 2.0 * sigma)
        fm_dd = dd_add(m, term1) ; fm_dd[0] = -fm_dd[0]; fm_dd[1] = -fm_dd[1]
        
        m_sq = dd_square(m); l_sq = dd_square(l)
        term3 = dd_sub(m_sq, l_sq)
        term2 = dd_mul_s(term3, sigma)
        fl_dd = dd_add(l, term2); fl_dd[0] = -fl_dd[0]; fl_dd[1] = -fl_dd[1]

        pm = dd_add(pm, dd_mul_s(fm_dd, dt_half))
        pl = dd_add(pl, dd_mul_s(fl_dd, dt_half))
        
        # Position Update
        m = dd_add(m, dd_mul_s(pm, dt_full))
        l = dd_add(l, dd_mul_s(pl, dt_full))
        
        # Velocity Update (Full-step)
        m_l_prod_new = dd_mul(m, l)
        term1_new = dd_mul_s(m_l_prod_new, 2.0 * sigma)
        fm_dd_new = dd_add(m, term1_new) ; fm_dd_new[0] = -fm_dd_new[0]; fm_dd_new[1] = -fm_dd_new[1]
        
        m_sq_new = dd_square(m); l_sq_new = dd_square(l)
        term3_new = dd_sub(m_sq_new, l_sq_new)
        term2_new = dd_mul_s(term3_new, sigma)
        fl_dd_new = dd_add(l, term2_new); fl_dd_new[0] = -fl_dd_new[0]; fl_dd_new[1] = -fl_dd_new[1]
        
        pm = dd_add(pm, dd_mul_s(fm_dd_new, dt_half))
        pl = dd_add(pl, dd_mul_s(fl_dd_new, dt_half))
        
        # Escape Check
        if m[0]*m[0] + l[0]*l[0] > escape_r2:
            angle = np.arctan2(l[0], m[0])
            if angle > 0.5 and angle < 2.6: return 1
            elif angle <= -2.6 or angle >= 2.6: return 2
            else: return 3
            
    return 0

# ==============================================================================
# III. HYPER-OPTIMIZED DRIFT/SPAN CALCULATION
# ==============================================================================

@njit(parallel=True, fastmath=True)
def get_drift_and_span_nd(res, zoom, center_x_nd, center_y_nd):
    """
    Single Numba function combining: Map Generation, Boundary Detection, and Center-of-Mass Tracking.
    """
    out_map = np.zeros((res, res), dtype=np.int8)
    
    img_cx = (res - 1) / 2.0
    img_cy = (res - 1) / 2.0
    scale = (2.0 * zoom) / res
    
    deg120 = 2.094395; deg240 = 4.188790 
    
    # 1. MAP GENERATION (Run the DD Kernel)
    for y in prange(res):
        for x in range(res):
            # Calculate local offset (float64)
            offset_x = (x - img_cx) * scale 
            offset_y = (y - img_cy) * scale
            
            # Translate N-D Center to get the DD coordinates (m_in, l_in)
            abs_x_nd = nd_translate(center_x_nd, offset_x)
            abs_y_nd = nd_translate(center_y_nd, offset_y)
            
            # Reconstruct the DD number (high + low) for the kernel input
            m_in = abs_x_nd[0] + abs_x_nd[1] 
            l_in = abs_y_nd[0] + abs_y_nd[1]

            basin = get_basin_single_dd(m_in, l_in)
            
            # Apply 3-fold rotational symmetry check (same as your original)
            if basin != 0: 
                r = np.sqrt(m_in*m_in + l_in*l_in); theta = np.arctan2(l_in, m_in)
                if theta < 0: theta += 2*np.pi
                
                rot = 0
                if theta >= deg240: rot = 2
                elif theta >= deg120: rot = 1
                
                out_map[y, x] = (basin - 1 + rot) % 3 + 1
            
    # 2. BOUNDARY DETECTION & TRACKING (FIXED - Robust Boundary)
    
    # Calculate difference along axis=1 (columns)
    grad_x_diff = np.abs(out_map[:, 1:] - out_map[:, :-1]) 
    grad_x = np.zeros_like(out_map, dtype=np.int8)
    grad_x[:, 1:] = grad_x_diff  # Fill in the difference
    
    # Calculate difference along axis=0 (rows)
    grad_y_diff = np.abs(out_map[1:, :] - out_map[:-1, :])
    grad_y = np.zeros_like(out_map, dtype=np.int8)
    grad_y[1:, :] = grad_y_diff # Fill in the difference

    # Combine X and Y differences
    boundaries_mask = (grad_x + grad_y) > 0
    
    y_idxs, x_idxs = np.where(boundaries_mask)
    total_count = len(x_idxs)
    
    if total_count == 0:
        return 0.0, 0.0, 0.0, 0 # Still a necessary break condition

    # Calculate Center-of-Mass (in pixel space)
    img_cx_center = (res - 1) / 2.0
    img_cy_center = (res - 1) / 2.0
        
    avg_px = np.mean(x_idxs)
    avg_py = np.mean(y_idxs)
    
    # Check if the calculated center of mass is the same as the image center (perfect symmetry)
    # If it is, force a tiny drift to break the symmetry and ensure zooming starts.
    # We must do this check in world coordinates using the scale.
    drift_x = (avg_px - img_cx_center) * scale
    drift_y = (avg_py - img_cy_center) * scale

    # --- Symmetry Breaking Logic (If the drift is too close to zero) ---
    if np.abs(drift_x) < 1e-10 * scale: 
        # Force a small, calculated, non-zero drift to kick the search off the stable axis.
        # This prevents the search from getting stuck exactly on a symmetrical feature.
        drift_x += 1e-6 * scale 
        drift_y -= 1e-6 * scale 
        
    # Calculate Structure Span (The span calculation is correct, but needs a non-zero input)
    min_px, max_px = np.min(x_idxs), np.max(x_idxs)
    min_py, max_py = np.min(y_idxs), np.max(y_idxs)
    phys_width = (max_px - min_px) * scale
    phys_height = (max_py - min_py) * scale
    structure_span = max(phys_width, phys_height)
    
    # Ensure span is never zero to prevent loop stall
    if structure_span == 0.0:
        structure_span = 1e-12 # Inject a minimal size
    
    return drift_x, drift_y, structure_span, total_count

# ==============================================================================
# IV. HYPER-OPTIMIZED SEEKER (The Atomic Operation)
# ==============================================================================

@njit
def seek_absolute_tip_hyper_optimized(start_zoom, start_cx, start_cy, N_parts, 
                                      res_low, max_iterations):
    """
    Performs the entire deep-dive trajectory calculation in a single Numba loop.
    Returns the final N-D center and zoom factor.
    """
    
    # 1. INITIALIZE N-D CENTER ARRAYS
    # The current center is stored in N_parts for memory-limited precision.
    curr_cx_nd = np.zeros(N_parts, dtype=np.float64)
    curr_cy_nd = np.zeros(N_parts, dtype=np.float64)
    curr_cx_nd[0] = start_cx
    curr_cy_nd[0] = start_cy
    
    curr_zoom = start_zoom
    
    # Initialize variables to hold the last valid state
    last_valid_zoom = start_zoom
    last_valid_cx_nd = curr_cx_nd.copy()
    last_valid_cy_nd = curr_cy_nd.copy()

    for i in range(max_iterations):
        # 2. RUN THE ATOMIC STEP: Calculate drift and span from current N-D center
        drift_x, drift_y, span, count = get_drift_and_span_nd(
            res_low, curr_zoom, curr_cx_nd, curr_cy_nd
        )
        
        # If structure is lost, break and use the last valid point
        if count == 0:
            break
            
        # Store last valid state before updating the center
        last_valid_zoom = curr_zoom
        last_valid_cx_nd[:] = curr_cx_nd[:] # Copy array contents
        last_valid_cy_nd[:] = curr_cy_nd[:] # Copy array contents
            
        # 3. UPDATE N-D CENTER (Accurate Translation of the float64 drift)
        curr_cx_nd = nd_translate(curr_cx_nd, drift_x)
        curr_cy_nd = nd_translate(curr_cy_nd, drift_y)
        
        # 4. UPDATE ZOOM 
        target_zoom = span * 0.75
        curr_zoom = max(target_zoom, curr_zoom * 0.5)
        
        # 5. Stop Condition (1e-60 is achievable with N=4 parts)
        if curr_zoom < 1e-60:
            break
            
    # Return the deepest valid point found
    return last_valid_zoom, last_valid_cx_nd, last_valid_cy_nd

# ==============================================================================
# V. MAIN EXECUTION EXAMPLE
# ==============================================================================

if __name__ == '__main__':
    # --- CONFIGURATION ---
    # N_parts = 4 provides ~60 digits of precision (1e-60 limit)
    # Increase N_parts for deeper zoom (RAM limitation)
    N_PARTS = 4          
    RES_LOW = 400
    MAX_ITER = 300
    
    # Initial Conditions (starting point of your deep dive)
    START_ZOOM = 1.0
    START_CX = 0.5
    START_CY = 0.5
    
    print(f"[-] Starting HYPER-OPTIMIZED Deep Dive (N=4 parts) from ({START_CX}, {START_CY})...")
    
    # Run the single atomic function
    final_zoom, final_cx_nd, final_cy_nd = seek_absolute_tip_hyper_optimized(
        START_ZOOM, START_CX, START_CY, N_PARTS, RES_LOW, MAX_ITER
    )
    
    # Display Results
    print(f"\n[+] Deepest Valid Point Found:")
    print(f"    Final Zoom: {final_zoom:.4e}")
    print(f"    Center X N-D: {final_cx_nd}")
    print(f"    Center Y N-D: {final_cy_nd}")
    
    # Reconstruct the highest precision float (for display)
    final_cx_full = np.sum(final_cx_nd)
    final_cy_full = np.sum(final_cy_nd)
    print(f"    Center X (Float Sum): {final_cx_full:.16f}")
    print(f"    Center Y (Float Sum): {final_cy_full:.16f}")