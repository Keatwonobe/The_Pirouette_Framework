import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math
from PIL import Image
import imageio

# =========================================================
#  PIROUETTE: PHASE 1 - PATH GENERATION (RETAINED KERNELS)
# =========================================================

# PATH GENERATION PARAMETERS (RETAINED FOR KERNEL USE)
TOTAL_PATH_STEPS = 150
SEARCH_RES = 200
TERMINATION_THRESHOLD = 50.0

# --- DYNAMICS (Re-use from previous scripts) ---
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
EPSILON = 1e-5
R_ESCAPE = 100.0
HELICITY_STOP = np.pi * 0.95

# =========================================================
#  NUMBA PHYSICS KERNEL (Unchanged)
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
            # Use 'depth_steps' as the T-value for the fractal iteration
            heatmap[i, j] = compute_divergence(m_curr, l_curr, depth_steps)
            
    return heatmap

# =========================================================
#  NEW: STATIC ROI RENDER PROTOCOL
# =========================================================

def render_static_roi(center_m, center_l, width, time_steps, output_filename="static_roi_fractal_progression.gif", hd_res=600, fps=30):
    """
    Renders a fixed region (ROI) over a sequence of time steps (T-values)
    to show the progression of the fractal structure.
    """
    print(f"\n--- 🎥 PHASE 2: RENDERING STATIC ROI ---")
    print(f"Center: ({center_m:.2e}, {center_l:.2e}) | Width: {width:.2e} | T-Range: {time_steps[0]} to {time_steps[-1]}")
    
    frames_buffer = []
    
    for i, t in enumerate(time_steps):
        # A. Render the frame using the fixed coordinates and the current time 't'.
        hd_data = scan_sector(center_m, center_l, width, hd_res, t)
        
        # B. Night Vision Normalization (The same logic from the original script)
        structure_mask = hd_data < 5.0
        
        if not np.any(structure_mask):
             # Fallback if no structure found
             print(f"Warning: Frame T={t} rendered solid, skipping normalization.")
             v_min, v_max = hd_data.min(), hd_data.max()
        else:
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
        
        # Optional: Add text overlay for T-value and ROI center
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        text = f"T = {t} | ({center_m:.1e}, {center_l:.1e})"
        draw.text((10, 10), text, fill=(255, 255, 255))
        
        frames_buffer.append(img)
        
        if i % 10 == 0:
            print(f"Rendered frame {i}/{len(time_steps)} at T={t}")

    # E. Save GIF
    if frames_buffer:
        print(f"Saving final GIF to {output_filename} with {fps} FPS.")
        imageio.mimsave(output_filename, frames_buffer, fps=fps)
    else:
        print("No frames rendered.")

# =========================================================
#  MAIN EXECUTION
# =========================================================

if __name__ == "__main__":
    
    # --- 🎯 USER-DEFINED INPUTS ---
    
    # 1. DEFINE YOUR REGION OF INTEREST (ROI)
    # The 'FINAL_M' and 'FINAL_L' from your original script were: 
    # M = -2.666016e+07, L = -2.666016e+07
    # Use a location you know the traveler passes through:
    ROI_M    = -2.5e+07  # Center M-coordinate
    ROI_L    = -2.5e+07  # Center L-coordinate
    ROI_WIDTH = 5.0e+05  # Width of the view (zoom level)
    
    # 2. DEFINE TIME STEPS (T-values) AND FRAMERATE
    # T is the iteration count for the fractal-generating physics (compute_divergence)
    START_T  = 250        # The starting time step (start of activity)
    END_T    = 1500        # The final time step
    STEP_SIZE = 10         # The increment in T (1 for high-framerate/slow-motion)
    GIF_FPS  = 60         # Frames per second for the final GIF
    
    # Generate the sequence of T-values
    # This list of T-values IS your GIF frames
    time_steps = list(range(START_T, END_T + 1, STEP_SIZE))
    
    # --- 🎬 RUN RENDER ---
    render_static_roi(
        center_m=ROI_M, 
        center_l=ROI_L, 
        width=ROI_WIDTH, 
        time_steps=time_steps, 
        output_filename="high_fps_fractal_motion.gif",
        hd_res=800, # Higher resolution for better detail
        fps=GIF_FPS
    )