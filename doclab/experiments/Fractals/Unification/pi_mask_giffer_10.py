import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math
from PIL import Image

# =========================================================
#  PIROUETTE: GEOMETRY CAPTURE PROTOCOL (STATIC RENDER)
# =========================================================

# --- INPUT FROM LINE HUNTER PROTOCOL ---
# These values are pulled directly from your successful trace output:
FINAL_M = -2.666016e+07
FINAL_L = -2.666016e+07
FINAL_WIDTH = 25000
FINAL_STEPS = 25

# RENDER PARAMETERS
HD_RES = 1000  # High Resolution for detail
OUTPUT_FILENAME = "captured_chaos_geometry.png"

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
#  VISUALIZATION
# =========================================================

def geometry_capture():
    print(f"--- 📸 Capturing Geometry at m={FINAL_M:.2e}, λ={FINAL_L:.2e} ---")
    
    # 1. Render the High-Definition Heatmap
    heatmap = scan_sector(FINAL_M, FINAL_L, FINAL_WIDTH, HD_RES, FINAL_STEPS)
    
    # 2. Smart Contrast Normalization (Night Vision Mode)
    structure_mask = heatmap < 5.0
    
    if not np.any(structure_mask):
        print("Error: Target area is solid escape zone. Cannot analyze structure.")
        return

    structure_data = heatmap[structure_mask]
    v_min = np.percentile(structure_data, 1)  
    v_max = np.percentile(structure_data, 99.5) # Slight bump to capture max chaos
    
    if v_max <= v_min: v_max = v_min + 1e-9
    
    clipped = np.clip(heatmap, v_min, v_max)
    norm = (clipped - v_min) / (v_max - v_min)
    
    # 3. Save Image
    plt.figure(figsize=(10, 10))
    plt.imshow(np.flipud(norm), 
               extent=[FINAL_M - FINAL_WIDTH/2, FINAL_M + FINAL_WIDTH/2, 
                       FINAL_L - FINAL_WIDTH/2, FINAL_L + FINAL_WIDTH/2],
               cmap='magma', 
               origin='lower')
               
    plt.title(f"Captured Geometry (T={FINAL_STEPS} steps, Zoom={FINAL_WIDTH:.1e})")
    plt.xlabel("Mass field m")
    plt.ylabel("Coupling field λ")
    plt.colorbar(label=r'$\ln(\Delta\theta)$ - Helicity')
    plt.tight_layout()
    plt.savefig(OUTPUT_FILENAME, dpi=150)
    plt.close()

    print(f"✅ Geometry saved to {OUTPUT_FILENAME}")
    print(f"Contrast Range (Visible Structure): [{v_min:.2f}, {v_max:.2f}]")

if __name__ == "__main__":
    geometry_capture()