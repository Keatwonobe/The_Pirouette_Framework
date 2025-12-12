import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math
from PIL import Image
import imageio.v2 as imageio

# =========================================================
#  PIROUETTE: CINEMATIC TRACE (Final Render Protocol)
# =========================================================

# --- INPUT FROM LINE HUNTER PROTOCOL ---
# These coordinates define the geometry we are chasing.
FINAL_M = -2.666016e+07
FINAL_L = -2.666016e+07
FINAL_WIDTH = 3.91e+04
START_STEPS = 25 
RENDER_VIEWPORT_WIDTH = 10000000.0 # <--- NEW WIDE RENDER SETTING (10 Million Units)

# PATH GENERATION PARAMETERS (Used for the loop structure only)
TOTAL_PATH_STEPS = 150 
SEARCH_RES = 200       
TERMINATION_THRESHOLD = 50.0 

# RENDER PARAMETERS
HD_RES = 600
OUTPUT_FILENAME = "proton_wound_channel_cinematic.gif"

# --- DYNAMICS (Re-use from previous scripts) ---
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
EPSILON = 1e-5
R_ESCAPE = 100.0
HELICITY_STOP = np.pi * 0.95

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
#  RENDERING PROTOCOLS
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

def generate_cinematic_path():
    """Reruns Phase 1 logic internally to get the path."""
    print("--- 🎬 PHASE 1: RE-GENERATING PATH DATA ---")
    
    cam_m, cam_l = FINAL_M, FINAL_L
    cam_width = FINAL_WIDTH
    
    slew_rate = 0.95
    path_history = []
    
    for t in range(START_STEPS, START_STEPS + TOTAL_PATH_STEPS):
        heatmap = scan_sector(cam_m, cam_l, cam_width, SEARCH_RES, t)
        peak_m, peak_l, peak_val = find_hotspot_coords(heatmap, cam_m, cam_l, cam_width)
        
        path_history.append((cam_m, cam_l, cam_width, t))
        
        dist_to_origin = np.sqrt(peak_m**2 + peak_l**2)
        if dist_to_origin < TERMINATION_THRESHOLD:
            print(f"TERMINATION: Puncture point reached at T={t}.")
            break
        
        cam_m += (peak_m - cam_m) * slew_rate
        cam_l += (peak_l - cam_l) * slew_rate
        
        if t % 50 == 0:
            print(f"Path step T={t}: Pos ({cam_m:.2e}, {cam_l:.2e}) | Signal: {peak_val:.2f}")

    return path_history

def render_cinematic_path(path_history):
    print("\n--- 🎥 PHASE 2: RENDERING WOUND CHANNEL GIF ---")
    print(f"Rendering {len(path_history)} frames at a fixed {RENDER_VIEWPORT_WIDTH:.1e} width.")
    
    frames_buffer = []
    
    for i, (m, l, original_width, t) in enumerate(path_history):
        # A. Render the frame using the tracked center (m, l) but the wide RENDER_VIEWPORT_WIDTH
        hd_data = scan_sector(m, l, RENDER_VIEWPORT_WIDTH, HD_RES, t)
        
        # B. Night Vision Normalization
        structure_mask = hd_data < 5.0
        
        # We must handle the case where the whole view is uniform (even in wide view)
        if not np.any(structure_mask):
             print(f"Warning: Frame {i} solid escape/stable. Skipping.")
             continue
             
        structure_data = hd_data[structure_mask]
        v_min = np.percentile(structure_data, 1)  
        v_max = np.percentile(structure_data, 99.5) 
        if v_max <= v_min: v_max = v_min + 1e-9
        
        clipped = np.clip(hd_data, v_min, v_max)
        norm = (clipped - v_min) / (v_max - v_min)
        
        # C. Create Image
        cm = plt.get_cmap('magma')
        colored = (cm(norm)[:, :, :3] * 255).astype(np.uint8)
        img = Image.fromarray(np.flipud(colored), mode='RGB')
    

        
        frames_buffer.append(img)
        
        if i % 20 == 0:
            print(f"Rendered frame {i}/{len(path_history)}")

    # E. Save GIF
    if frames_buffer:
        print(f"Saving final GIF to {OUTPUT_FILENAME}")
        imageio.mimsave(OUTPUT_FILENAME, frames_buffer, fps=30)
    else:
        print("No frames rendered.")

if __name__ == "__main__":
    path_data = generate_cinematic_path()
    if path_data:
        render_cinematic_path(path_data)