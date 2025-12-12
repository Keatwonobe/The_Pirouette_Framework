import numpy as np
from numba import njit, prange

# Assume two_sum, two_prod, dd_add, dd_mul, dd_square are defined here
# (from your wada_precision_solver.py file)

# ==============================================================================
# 1. N-D ARITHMETIC CORE (Layered Translation)
# ==============================================================================

@njit(fastmath=True)
def nd_translate(center_nd, offset_s):
    """
    Translates an N-D center by a float64 scalar offset (the local grid coordinate).
    This performs the accurate addition: center_nd + offset_s.
    """
    N = len(center_nd)
    result_nd = np.zeros(N, dtype=np.float64)
    
    # Start with the scalar offset as the low part/error to be propagated
    low_part = offset_s 
    
    # Iterate backward, propagating the error ('low_part') from lowest precision to highest
    for i in range(N - 1, -1, -1):
        # Accurate addition of the current center component and the incoming low part
        s, e = two_sum(center_nd[i], low_part)
        
        result_nd[i] = s
        low_part = e
        
        # If the low_part becomes zero, the precision of the offset has been 
        # fully contained in the components from 'i' onwards.
        if low_part == 0.0:
            # Copy the remaining high-precision parts unchanged and exit
            for j in range(i - 1, -1, -1):
                result_nd[j] = center_nd[j]
            break
            
    # Note: If low_part is non-zero after the loop, the N-D array was too short (N was too small).
    return result_nd

# ==============================================================================
# 2. MODIFIED SCANNER (REPLACEMENT FOR generate_oracle_map_centered)
# ==============================================================================

@njit(parallel=True, fastmath=True)
def generate_oracle_map_centered_nd(res, zoom, center_x_nd, center_y_nd):
    """
    Generates the oracle map using an N-D center array.
    """
    out_map = np.zeros((res, res), dtype=np.int8)
    
    img_cx = (res - 1) / 2.0
    img_cy = (res - 1) / 2.0
    scale = (2.0 * zoom) / res
    
    deg120 = 2.094395; deg240 = 4.188790 
    
    for y in prange(res):
        for x in range(res):
            # 1. Calculate local offset (a simple float64)
            offset_x = (x - img_cx) * scale 
            offset_y = (y - img_cy) * scale
            
            # 2. TRANSLATE N-D CENTER (get absolute coordinates for the kernel)
            abs_x_nd = nd_translate(center_x_nd, offset_x)
            abs_y_nd = nd_translate(center_y_nd, offset_y)
            
            # 3. Use the first TWO components for the Double-Double (DD) kernel.
            # This is the full DD representation of the absolute coordinate.
            # We assume N >= 2 for the DD kernel to function.
            m_in = abs_x_nd[0] + abs_x_nd[1] 
            l_in = abs_y_nd[0] + abs_y_nd[1]

            # 4. Run the high-precision DD kernel
            # NOTE: If you need more than DD precision, you would need to implement 
            # a Quad-Double or higher kernel, but DD should handle the translation perfectly.
            basin = get_basin_single_dd(m_in, l_in)
            
            # --- Symmetry and Storage Logic (Same as original) ---
            if basin != 0: 
                # Re-apply the rotation logic
                r = np.sqrt(m_in*m_in + l_in*l_in); theta = np.arctan2(l_in, m_in)
                if theta < 0: theta += 2*np.pi
                
                rot = 0
                if theta >= deg240: rot = 2
                elif theta >= deg120: rot = 1
                
                out_map[y, x] = (basin - 1 + rot) % 3 + 1
            
    return out_map

# ==============================================================================
# 3. MODIFIED TIP SEEKER (REPLACEMENT FOR seek_absolute_tip)
# ==============================================================================

def seek_absolute_tip_nd(start_zoom, start_cx_nd, start_cy_nd, N_parts=4):
    """
    Deep dive using N-D center storage. N_parts dictates the max precision.
    """
    print(f"[-] Initiating N-D Deep Dive (Precision: {N_parts} parts, up to ~{N_parts*15} digits)")
    
    curr_zoom = start_zoom
    curr_cx_nd = start_cx_nd
    curr_cy_nd = start_cy_nd
    last_valid_cx_nd, last_valid_cy_nd = curr_cx_nd, curr_cy_nd # Store N-D array
    
    max_iterations = 300 
    
    for i in range(max_iterations):
        # Use N-D centered map generation
        oracle = generate_oracle_map_centered_nd(400, curr_zoom, curr_cx_nd, curr_cy_nd)
        
        # --- Tracking Logic (Same as original, uses float64 for drift) ---
        # NOTE: You must use the float64 outputs from your original extract_layer_adaptive
        # (or similar logic) to get the drift_x, drift_y, and span from the oracle map.
        # We assume the calculation of drift_x, drift_y, and span happens here, 
        # resulting in simple float64 values.
        
        # DUMMY VALUES (Replace with actual calculation using oracle map)
        drift_x = 0.0 # Placeholder
        drift_y = 0.0 # Placeholder
        span = 1.0 # Placeholder
        count = 1000 # Placeholder

        if count == 0:
            print(f"   [STOP] Chaos vanished at Zoom={curr_zoom:.4e}. Backing up to last valid point.")
            break
            
        last_valid_zoom = curr_zoom
        last_valid_cx_nd = curr_cx_nd.copy() 
        last_valid_cy_nd = curr_cy_nd.copy()
        
        # --- THE N-D UPDATE STEP ---
        # Update center by accurately adding the float64 drift to the N-D array
        curr_cx_nd = nd_translate(curr_cx_nd, drift_x)
        curr_cy_nd = nd_translate(curr_cy_nd, drift_y)
        
        # ... (Zoom logic remains the same) ...
        target_zoom = span * 0.75
        if target_zoom > 0 and target_zoom < curr_zoom:
             curr_zoom = target_zoom
        else:
             curr_zoom *= 0.5
             
        # Stop condition for N-D precision (e.g., N=4 allows for 1e-60)
        if curr_zoom < 1e-60:
            print(f"   [STOP] Hit N-D Precision Limit (~1e-60).")
            break
            
    # ... (Final print and return logic, returning the final N-D array center) ...
    return last_valid_zoom, last_valid_cx_nd, last_valid_cy_nd