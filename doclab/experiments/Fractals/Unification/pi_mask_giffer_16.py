import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
import shutil

# =========================================================
#  PIRouette Vectorized Giffer (EXTREME WIDE VIEW, T=1)
# =========================================================

# ---------- Dynamics parameters (Unchanged) ----------
TWIST = 3.8        
GAMMA = 0.5
DT    = 0.015
MAX_STEPS = 100      # <--- Only render the initial condition (T=1)
EPSILON = 1e-5
R_ESCAPE = 100.0   

# ---------- Viewport (Zoomed out to the Proton Basin edge) ----------
# Max extent from pi_scanner_3.py: 2.8e10
M_MIN, M_MAX = -28000000000.0, 28000000000.0
L_MIN, L_MAX = -28000000000.0, 28000000000.0
RES = 800          # Resolution
FRAME_SKIP = 1     
FPS = 1            # Not used, but kept for function structure

# ---------- Output Settings ----------
OUTPUT_DIR = "fractal_frames_t1_max_zoom"
GIF_NAME = "initial_spread_t1_max_zoom.png" # Saving as PNG since it's one frame

def vectorized_get_force(m, lam):
    """Vectorized version of the PIRouette force law."""
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
    def angle_dist(a, target):
        diff = np.abs(a - target)
        return np.minimum(diff, 360.0 - diff)
    diff_g = angle_dist(angle_deg, 30.0); w_gold = np.exp(-(diff_g / 80.0)**2)
    diff_t = angle_dist(angle_deg, 150.0); w_teal = np.exp(-(diff_t / 80.0)**2)
    diff_r = angle_dist(angle_deg, 270.0); w_red  = np.exp(-(diff_r / 80.0)**2)
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red  = w_red  / tot; nw_teal = w_teal / tot; nw_gold = w_gold / tot
    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam
    return Fm, Flam, nw_red

def normalize_angle_diff_vec(delta):
    """Vectorized angle normalization (-pi to pi)"""
    return np.arctan2(np.sin(delta), np.cos(delta))

def run_evolution():
    # 1. Setup Grid
    print(f"Initializing {RES}x{RES} simulation grid...")
    m_space = np.linspace(M_MIN, M_MAX, RES)
    l_space = np.linspace(L_MIN, L_MAX, RES)
    M_grid, L_grid = np.meshgrid(m_space, l_space)

    # 2. Initialize Trajectories
    m1 = M_grid.copy(); l1 = L_grid.copy()
    pm1 = np.zeros_like(m1); pl1 = np.zeros_like(l1)
    m2 = M_grid.copy() + EPSILON; l2 = L_grid.copy() + EPSILON
    pm2 = np.zeros_like(m2); pl2 = np.zeros_like(l2)
    max_diff_angle = np.zeros_like(m1)
    
    # Directory Prep
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    print(f"Starting time evolution for T=1 on a +/- {M_MAX:.1e} extent...")
    
    # Visualization Range
    LOG_MAX = np.log(np.pi) 
    LOG_MIN = np.log(1e-6) 
    
    # 3. Time Loop (Only runs for step=1)
    for step in range(1, MAX_STEPS + 1):
        
        # Two sub-steps per main step (matching original kernel integration)
        for _ in range(2):
            Fm1, Flam1, w_red1 = vectorized_get_force(m1, l1)
            drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
            pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
            pl1 = (pl1 + 0.5 * DT * Flam1) * drag1
            m1 += DT * pm1; l1 += DT * pl1
            
            Fm2, Flam2, w_red2 = vectorized_get_force(m2, l2)
            drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
            pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
            pl2 = (pl2 + 0.5 * DT * Flam2) * drag2
            m2 += DT * pm2; l2 += DT * pl2


        # --- Measure Divergence (Helicity) ---
        ang1 = np.arctan2(l1, m1)
        ang2 = np.arctan2(l2, m2)
        diff = normalize_angle_diff_vec(ang1 - ang2)
        adiff = np.abs(diff)
        max_diff_angle = np.maximum(max_diff_angle, adiff)

        # --- Frame Capture ---
        print(f"Rendering frame {step}/{MAX_STEPS}...")
        
        fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
        
        viz_data = np.log(max_diff_angle + 1e-9)
        
        im = ax.imshow(viz_data, origin="lower", cmap='magma', 
                       extent=[M_MIN, M_MAX, L_MIN, L_MAX],
                       vmin=LOG_MIN, vmax=LOG_MAX) 

        ax.set_title(f"Evolution Step (T): {step} (Max Extent)")
        ax.set_xlabel("Mass field m")
        ax.set_ylabel("Coupling field λ")
        
        fig.colorbar(im, ax=ax).set_label("Log Angular Divergence (Helicity)")
        
        # Save to file (single PNG)
        filename = os.path.join(OUTPUT_DIR, GIF_NAME)
        plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0)) # Scientific notation for axes
        plt.tight_layout()
        plt.savefig(filename)
        plt.close(fig)

    print(f"Done! Single frame saved to {filename}")
    shutil.rmtree(OUTPUT_DIR) 

if __name__ == "__main__":
    run_evolution()