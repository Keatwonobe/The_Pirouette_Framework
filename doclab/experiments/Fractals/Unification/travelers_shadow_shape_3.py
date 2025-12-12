import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange # Keep Numba imports
import math

# ============================================================
# CONFIGURATION: THE FRACTAL HUNTER
# ============================================================
# Coarse Search Settings
COARSE_RES = 100
BLOCK_SIZE = 16

# Target Coords (The Tip of the Spine)
CENTER_M = 1333689.982       
CENTER_L = 770007.6
ZOOM_WIDTH = 99

# Physics Settings
TWIST = 3.8
DT = 0.01
STEPS = 1200
THRESHOLD = 50.0

# ============================================================
# 1. OPTIMIZED PHYSICS KERNEL (RADIAN MODE)
# ============================================================

RAD_30  = 0.5235987756
RAD_150 = 2.617993878
RAD_270 = 4.71238898
RAD_360 = 6.283185307
WIDTH_RAD = 1.39626

# FIX: Pre-calculate the inverse square width OUTSIDE Numba
# This isolates the floating-point division that caused the compilation crash.
W_INV_SQ = 1.0 / (WIDTH_RAD * WIDTH_RAD) if WIDTH_RAD != 0.0 else 1e12 


@njit # Numba is back!
def get_physics_optimized(m, lam, twist, w_inv_sq):
    # --- 1. Constituent Weights (Radians) ---
    angle = math.atan2(lam, m)
    if angle < 0:
        angle += RAD_360

    d_gold = abs(angle - RAD_30)
    if d_gold > math.pi: d_gold = RAD_360 - d_gold
    
    d_teal = abs(angle - RAD_150)
    if d_teal > math.pi: d_teal = RAD_360 - d_teal
    
    d_red = abs(angle - RAD_270)
    if d_red > math.pi: d_red = RAD_360 - d_red

    # w_inv_sq is passed as an argument
    w_gold_raw = math.exp(-(d_gold*d_gold) * w_inv_sq)
    w_teal_raw = math.exp(-(d_teal*d_teal) * w_inv_sq)
    w_red_raw  = math.exp(-(d_red*d_red) * w_inv_sq)

    total_w = w_gold_raw + w_teal_raw + w_red_raw + 1e-12
    nw_gold = w_gold_raw / total_w
    nw_teal = w_teal_raw / total_w
    nw_red  = w_red_raw  / total_w

    # --- 2. Component Forces ---
    F_teal_m = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    F_red_m = -m
    p_violation = twist * math.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag_sq = sum_m*sum_m + sum_lam*sum_lam
    
    scaling_factor = math.sqrt(math.sqrt(mag_sq)) if mag_sq > 1e-16 else 0.0
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor

    # --- 3. Composite Force ---
    Fm = nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam

# ============================================================
# 2. THE SOLVER
# ============================================================

@njit # Numba is back!
def run_particle(m, l, twist, dt, steps, w_inv_sq):
    """
    Returns the Peak Velocity experienced by the particle.
    """
    curr_m, curr_l = m, l
    max_v_sq = 0.0
    
    for _ in range(steps):
        # Pass the w_inv_sq constant
        fm1, fl1 = get_physics_optimized(curr_m, curr_l, twist, w_inv_sq)
        
        m_pred = curr_m + fm1 * dt
        l_pred = curr_l + fl1 * dt
        
        fm2, fl2 = get_physics_optimized(m_pred, l_pred, twist, w_inv_sq)
        
        curr_m = curr_m + (fm1 + fm2) * 0.5 * dt
        curr_l = curr_l + (fl1 + fl2) * 0.5 * dt
        
        fm_new, fl_new = get_physics_optimized(curr_m, curr_l, twist, w_inv_sq)
        v_sq = fm_new**2 + fl_new**2
        
        if v_sq > max_v_sq:
            max_v_sq = v_sq
            
    return math.sqrt(max_v_sq)

# ============================================================
# 3. THE ADAPTIVE HUNTER (COARSE -> FINE)
# ============================================================

@njit # Numba is back!
def adaptive_render(center_m, center_l, width, coarse_res, block_size, twist, dt, steps, threshold, w_inv_sq):
    
    f_coarse_res = float(coarse_res)
    f_block_size = float(block_size)
    
    if f_coarse_res == 0.0 or f_block_size == 0.0:
        return np.full((1, 1), np.nan, dtype=np.float64)
        
    full_res = coarse_res * block_size
    final_grid = np.full((full_res, full_res), np.nan, dtype=np.float64)
    
    min_m = center_m - width/2
    min_l = center_l - width/2
    
    coarse_step = width / f_coarse_res
    fine_step = coarse_step / f_block_size
    
    # 2. COARSE PASS (The "Shake")
    for cy in range(coarse_res):
        for cx in range(coarse_res):
            
            sample_m = min_m + (cx * coarse_step) + (coarse_step * 0.5)
            sample_l = min_l + (cy * coarse_step) + (coarse_step * 0.5)
            
            # Pass the w_inv_sq constant
            val = run_particle(sample_m, sample_l, twist, dt, steps, w_inv_sq)
            
            # 3. DECISION & FINE PASS
            if val > threshold:
                base_pixel_y = cy * block_size
                base_pixel_x = cx * block_size
                
                for by in range(block_size):
                    for bx in range(block_size):
                        
                        pixel_m = min_m + (base_pixel_x + bx) * fine_step
                        pixel_l = min_l + (base_pixel_y + by) * fine_step
                        
                        # Pass the w_inv_sq constant
                        fine_val = run_particle(pixel_m, pixel_l, twist, dt, steps, w_inv_sq)
                        
                        final_grid[base_pixel_y + by, base_pixel_x + bx] = fine_val
                        
    return final_grid

# ============================================================
# 4. VISUALIZATION
# ============================================================

def run_hunt():
    print(f"[-] Initializing Fractal Hunter...")
    print(f"    Resolution: {COARSE_RES*BLOCK_SIZE}x{COARSE_RES*BLOCK_SIZE} (Adaptive)")
    
    # Pass the pre-calculated constant to the adaptive renderer
    result = adaptive_render(
        CENTER_M, CENTER_L, ZOOM_WIDTH, 
        COARSE_RES, BLOCK_SIZE, 
        TWIST, DT, STEPS, THRESHOLD,
        W_INV_SQ # The fix!
    )
    
    print("    Rendering...")
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    
    masked_data = np.ma.masked_invalid(result)
    
    im = ax.imshow(
        masked_data, 
        origin='lower', 
        cmap='inferno', 
        extent=[CENTER_M - ZOOM_WIDTH/2, CENTER_M + ZOOM_WIDTH/2, 
                CENTER_L - ZOOM_WIDTH/2, CENTER_L + ZOOM_WIDTH/2],
        interpolation='nearest'
    )
    
    ax.set_title(f"Adaptive Scan: Feathery Tips\nThreshold: {THRESHOLD} | Steps: {STEPS}", color='white')
    ax.axis('off')
    
    cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
    cbar.set_label("Peak Velocity", color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    plt.tight_layout()
    filename = "fractal_hunter_result_fast.png"
    plt.savefig(filename, dpi=200, facecolor='black')
    print(f"[+] Hunt Complete. Image saved to {filename}")

if __name__ == "__main__":
    run_hunt()