import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import time

# ==============================================================================
# I. CORE PRECISION LOGIC (Must match the solver exactly)
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
# II. PHYSICS KERNEL
# ==============================================================================

@njit(fastmath=True)
def get_basin_pixel(m_in_dd, l_in_dd):
    # Standard Wada Parameters
    mh, ml = m_in_dd[0], m_in_dd[1]
    lh, ll = l_in_dd[0], l_in_dd[1]
    
    t_max = 60.0
    dt = 0.05
    escape_r2 = 16.0
    sigma = 1.0
    dt_half = 0.5 * dt
    dt_full = dt
    steps = int(t_max / dt)
    s_val = 2.0 * sigma
    
    pmh, pml = 0.0, 0.0
    plh, pll = 0.0, 0.0

    for _ in range(steps):
        # Half Step Velocity
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
        
        # Position Update
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

        # Recalculate Forces
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
        
        # Final Velocity Half Step
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

        # Escape Check
        if mh*mh + lh*lh > escape_r2:
            angle = np.arctan2(lh, mh)
            # Basin Classification
            if angle > 0.5 and angle < 2.6: return 1   # Basin A
            elif angle <= -2.6 or angle >= 2.6: return 2 # Basin B
            else: return 3 # Basin C
            
    return 0 # Boundary/Slow Escape

# ==============================================================================
# III. RENDERER
# ==============================================================================

@njit(parallel=True)
def render_image(width, height, zoom, cx_nd, cy_nd):
    image = np.zeros((height, width), dtype=np.int32)
    
    img_cx = (width - 1) / 2.0
    img_cy = (height - 1) / 2.0
    scale = (2.0 * zoom) / width # 2.0 is the physical width of the view
    
    deg120 = 2.094395
    deg240 = 4.188790 
    
    for y in prange(height):
        for x in range(width):
            # 1. Coordinate mapping
            offset_x = (x - img_cx) * scale 
            offset_y = (y - img_cy) * scale
            
            # 2. Translate N-D Center
            abs_x_nd = nd_translate(cx_nd, offset_x)
            abs_y_nd = nd_translate(cy_nd, offset_y)
            
            # 3. Extract High/Low parts for Physics
            m_dd = abs_x_nd[:2]
            l_dd = abs_y_nd[:2]
            
            # 4. Run Physics
            basin = get_basin_pixel(m_dd, l_dd)
            
            # 5. Apply Rotational Symmetry (Visual only)
            if basin != 0:
                # Reconstruct full float for angle check
                m_real = abs_x_nd[0] + abs_x_nd[1]
                l_real = abs_y_nd[0] + abs_y_nd[1]
                
                theta = np.arctan2(l_real, m_real)
                if theta < 0: theta += 2*np.pi
                
                rot = 0
                if theta >= deg240: rot = 2
                elif theta >= deg120: rot = 1
                
                final_color = (basin - 1 + rot) % 3 + 1
                image[y, x] = final_color
                
    return image

if __name__ == '__main__':
    # --- CONFIGURATION ---
    WIDTH, HEIGHT = 1200, 1200
    
    # --- DATA FROM SOLVER (HARDCODED) ---
    ZOOM = 4.069833027880832e-26
    
    # Reconstructing the exact N-D arrays found by the solver
    CX_ND = np.array([
        1.8957546994896471e-01, 
        -7.8646858760256740e-18, 
        1.9470281951771243e-35, 
        0.0
    ], dtype=np.float64)
    
    CY_ND = np.array([
        8.9253006402176494e-01, 
        -2.0606566938730768e-17, 
        -1.3099289236722358e-33, 
        0.0
    ], dtype=np.float64)

    print(f"[-] Rendering High-Precision Wada Basin at Zoom {ZOOM:.2e}")
    print(f"[-] Resolution: {WIDTH}x{HEIGHT}")
    print("[-] Please wait (This uses software emulation of 128-bit floats)...")
    
    t0 = time.time()
    raw_img = render_image(WIDTH, HEIGHT, ZOOM, CX_ND, CY_ND)
    print(f"[+] Render complete in {time.time() - t0:.2f} seconds.")
    
    # --- COLOR MAPPING ---
    # 0: Black (Boundary)
    # 1: Cyan
    # 2: Magenta
    # 3: Yellow
    
    rgb_img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    # Vectorized Coloring
    mask1 = (raw_img == 1)
    mask2 = (raw_img == 2)
    mask3 = (raw_img == 3)
    
    # Cyberpunk / Neon Palette
    rgb_img[mask1] = [0, 255, 255]    # Cyan
    rgb_img[mask2] = [255, 0, 255]    # Magenta
    rgb_img[mask3] = [255, 220, 0]    # Yellowish
    
    # Save
    plt.imsave("wada_deep_field_e26.png", rgb_img)
    print("[+] Image saved to: wada_deep_field_e26.png")