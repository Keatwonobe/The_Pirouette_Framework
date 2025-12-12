import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math

# =========================================================
#  PIROUETTE: LINE-CAPTURE PROTOCOL (Phase 1 Only)
# =========================================================

# --- CONFIGURATION (Match previous stable physics) ---
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
EPSILON = 1e-5
R_ESCAPE = 100.0
HELICITY_STOP = np.pi * 0.95

# SEARCH PARAMETERS
OBSERVATION_WIDTH = 40000000.0   # 40M wide initial search field
OBSERVATION_CENTER_M = 0.0
OBSERVATION_CENTER_L = 0.0
SEARCH_RES = 400                 # High res to ensure we hit the thin line
SIGNAL_THRESHOLD = -9.0          # Line detection trigger (log divergence)
STEP_INCREMENT = 25              # Increase time by 25 steps per failed attempt
MAX_SEARCH_STEPS = 500           # Max time to wait

# DRILL PARAMETERS
TARGET_ZOOM_WIDTH = 50000.0      # Final target width for definition

# =========================================================
#  NUMBA PHYSICS KERNEL
# =========================================================

@njit(fastmath=True)
def get_force_numba(m, lam):
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)
    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation
    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2 + 1e-12)
    scale   = np.sqrt(mag)
    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale
    angle_rad = np.arctan2(lam, m)
    angle_deg = np.degrees(angle_rad) % 360.0
    d_g = np.abs(angle_deg - 30.0);  d_g = np.minimum(d_g, 360.0-d_g)
    d_t = np.abs(angle_deg - 150.0); d_t = np.minimum(d_t, 360.0-d_t)
    d_r = np.abs(angle_deg - 270.0); d_r = np.minimum(d_r, 360.0-d_r)
    w_gold = np.exp(-(d_g / 80.0)**2)
    w_teal = np.exp(-(d_t / 80.0)**2)
    w_red  = np.exp(-(d_r / 80.0)**2)
    tot = w_gold + w_teal + w_red + 1e-6
    Fm   = (w_teal*F_teal_m + w_red*F_red_m + w_gold*F_gold_m)/tot
    Flam = (w_teal*F_teal_lam + w_red*F_red_lam + w_gold*F_gold_lam)/tot
    return Fm, Flam, w_red/tot

@njit(fastmath=True)
def compute_divergence(m0, l0, steps):
    m1, l1 = m0, l0; m2, l2 = m0 + EPSILON, l0 + EPSILON
    pm1, pl1 = 0.0, 0.0; pm2, pl2 = 0.0, 0.0
    max_diff_angle = 0.0
    
    for _ in range(steps):
        for _ in range(2): 
            Fm1, Flam1, w_red1 = get_force_numba(m1, l1)
            drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
            pm1 = (pm1 + 0.5 * DT * Fm1) * drag1; pl1 = (pl1 + 0.5 * DT * Flam1) * drag1
            m1 += DT * pm1; l1 += DT * pl1
            Fm2, Flam2, w_red2 = get_force_numba(m2, l2)
            drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
            pm2 = (pm2 + 0.5 * DT * Fm2) * drag2; pl2 = (pl2 + 0.5 * DT * Flam2) * drag2
            m2 += DT * pm2; l2 += DT * pl2

        ang1 = np.arctan2(l1, m1); ang2 = np.arctan2(l2, m2)
        diff = np.arctan2(np.sin(ang1 - ang2), np.cos(ang1 - ang2))
        adiff = np.abs(diff)
        if adiff > max_diff_angle: max_diff_angle = adiff
        
        if (m1**2 + l1**2) > R_ESCAPE: return 10.0 

    return np.log(max_diff_angle + EPSILON)

@njit(parallel=True, fastmath=True)
def scan_sector(center_m, center_l, width, res, depth_steps):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    heatmap = np.zeros((res, res), dtype=np.float64)
    
    for i in prange(res):
        l_curr = l_vals[i]
        for j in range(res):
            m_curr = m_vals[j]
            heatmap[i, j] = compute_divergence(m_curr, l_curr, depth_steps)
            
    return heatmap

# =========================================================
#  PROTOCOL EXECUTION
# =========================================================

def find_hotspot_coords(heatmap, center_m, center_l, width):
    """Returns world coords of the max value (brightest signal)."""
    idx = np.unravel_index(np.argmax(heatmap), heatmap.shape)
    res = heatmap.shape[0]
    px_scale = width / (res - 1)
    
    peak_l = (center_l - width/2.0) + idx[0] * px_scale
    peak_m = (center_m - width/2.0) + idx[1] * px_scale
    val = heatmap[idx]
    
    return peak_m, peak_l, val

def run_line_hunter():
    print("--- 🔬 PIROUETTE: LINE-CAPTURE PROTOCOL ---")
    
    # PHASE 1: TEMPORAL HUNT (Find the time depth)
    cam_m, cam_l = OBSERVATION_CENTER_M, OBSERVATION_CENTER_L
    cam_width = OBSERVATION_WIDTH
    current_steps = STEP_INCREMENT
    found = False
    
    print(f"[PHASE 1] Hunting for first divergence (Trigger: {SIGNAL_THRESHOLD:.2f})...")
    
    while current_steps <= MAX_SEARCH_STEPS:
        scan_data = scan_sector(cam_m, cam_l, cam_width, SEARCH_RES, current_steps)
        peak_m, peak_l, peak_val = find_hotspot_coords(scan_data, cam_m, cam_l, cam_width)
        
        print(f"  SimSteps: {current_steps:4d} | Max Signal: {peak_val:.4f}")
        
        if peak_val > SIGNAL_THRESHOLD:
            print(f"  >>> LINE DETECTED! Signal: {peak_val:.2f} <<<")
            cam_m, cam_l = peak_m, peak_l
            found = True
            break
        
        current_steps += STEP_INCREMENT
        
    if not found:
        print("FAILURE: Line never crossed signal threshold after max search steps.")
        return

    # PHASE 2: SPATIAL DRILL DOWN (Hone in on the coordinate)
    print("\n[PHASE 2] Drilling down to target width...")
    
    initial_width = cam_width
    
    while cam_width > TARGET_ZOOM_WIDTH:
        cam_width /= 4.0 # Aggressive zoom step
        
        # Use the established time depth (current_steps)
        scan_data = scan_sector(cam_m, cam_l, cam_width, SEARCH_RES, current_steps)
        peak_m, peak_l, peak_val = find_hotspot_coords(scan_data, cam_m, cam_l, cam_width)
        
        # Re-center (lock onto the new, finer-grained peak)
        cam_m = peak_m
        cam_l = peak_l
        
        print(f"  Width: {cam_width:.2e} | Center: ({cam_m:.2e}, {cam_l:.2e})")
        
    print(f"\n✅ TARGET ACQUIRED.")
    print(f"Final Time Depth Required: {current_steps} steps")
    print(f"Final Coordinate: m={cam_m:.6e}, λ={cam_l:.6e}")
    print(f"Final Zoom Width: {cam_width:.2e}")

if __name__ == "__main__":
    run_line_hunter()