import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
import shutil

# =========================================================
#  PIRouette Vectorized Giffer
#  Visualizes the emergence of the Proton Basin and Nexuses
# =========================================================

# ---------- Dynamics parameters (Matching your Source) ----------
TWIST = 3.8        
GAMMA = 0.5
DT    = 0.015
MAX_STEPS = 150    # Reduced slightly for GIF file size, increase if needed
EPSILON = 1e-5

# ---------- Viewport (Zoom in here to see Nexuses) ----------
# Current setting: Wide view. 
# To find a nexus, shrink these ranges around a coordinate of interest.
M_MIN, M_MAX = -8.0, 8.0
L_MIN, L_MAX = -8.0, 8.0
RES = 800          # Resolution (800x800 is good for GIF generation speed)

# ---------- Output Settings ----------
OUTPUT_DIR = "fractal_frames"
GIF_NAME = "proton_basin_formation.gif"
FRAME_SKIP = 2     # Save a frame every N steps (1 = every step, 5 = faster GIF)

def vectorized_get_force(m, lam):
    """
    Vectorized version of the PIRouette force law.
    Accepts 2D arrays (meshgrids) for m and lam.
    """
    # Teal
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red with parity/twist violation
    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold nonlinear
    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    # Note: adding epsilon to avoid div/0 in sqrt if exactly 0
    mag     = np.sqrt(sum_m**2 + sum_lam**2) 
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale

    # Angular weights calculation
    # arctan2 returns radians (-pi to pi). Convert to degrees 0-360
    angle_rad = np.arctan2(lam, m)
    angle_deg = np.degrees(angle_rad) % 360.0

    # Vectorized angular difference helper
    def angle_dist(a, target):
        diff = np.abs(a - target)
        return np.minimum(diff, 360.0 - diff)

    diff_g = angle_dist(angle_deg, 30.0)
    w_gold = np.exp(-(diff_g / 80.0)**2)

    diff_t = angle_dist(angle_deg, 150.0)
    w_teal = np.exp(-(diff_t / 80.0)**2)

    diff_r = angle_dist(angle_deg, 270.0)
    w_red  = np.exp(-(diff_r / 80.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6

    nw_red  = w_red  / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot

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
    # create meshgrid (Use sparse=False to get full 2D arrays)
    M_grid, L_grid = np.meshgrid(m_space, l_space)

    # 2. Initialize Trajectories (Real vs Shadow)
    # Real
    m1 = M_grid.copy()
    l1 = L_grid.copy()
    pm1 = np.zeros_like(m1)
    pl1 = np.zeros_like(l1)

    # Shadow (perturbed)
    m2 = M_grid.copy() + EPSILON
    l2 = L_grid.copy() + EPSILON
    pm2 = np.zeros_like(m2)
    pl2 = np.zeros_like(l2)

    # Metric tracking
    max_diff_angle = np.zeros_like(m1)
    
    # Directory Prep
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    frames = []

    print("Starting time evolution...")
    
    # 3. Time Loop
    for step in range(MAX_STEPS):
        # --- Dynamics Update (Real) ---
        Fm1, Flam1, w_red1 = vectorized_get_force(m1, l1)
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Flam1) * drag1
        m1 += DT * pm1
        l1 += DT * pl1
        
        # Second half-step (Leapfrog/Verlet style from original code)
        Fm1, Flam1, w_red1 = vectorized_get_force(m1, l1)
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Flam1) * drag1

        # --- Dynamics Update (Shadow) ---
        Fm2, Flam2, w_red2 = vectorized_get_force(m2, l2)
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Flam2) * drag2
        m2 += DT * pm2
        l2 += DT * pl2

        Fm2, Flam2, w_red2 = vectorized_get_force(m2, l2)
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Flam2) * drag2

        # --- Measure Divergence (Helicity) ---
        ang1 = np.arctan2(l1, m1)
        ang2 = np.arctan2(l2, m2)
        diff = normalize_angle_diff_vec(ang1 - ang2)
        adiff = np.abs(diff)
        
        # Update the max divergence seen so far for each pixel
        max_diff_angle = np.maximum(max_diff_angle, adiff)

        # --- Frame Capture ---
        if step % FRAME_SKIP == 0:
            print(f"Rendering frame {step}/{MAX_STEPS}...")
            
            fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
            
            # Log scale helps visualize the "Nexuses" (high chaos) 
            # against the "Basin" (low chaos)
            # Adding epsilon to log to avoid log(0)
            viz_data = np.log(max_diff_angle + 1e-9)
            
            im = ax.imshow(viz_data, origin="lower", cmap='magma', 
                           extent=[M_MIN, M_MAX, L_MIN, L_MAX])
            
            # Optional: Add a contour for the specific "Proton Basin" definition
            # (Assuming low helicity = basin, using a rough threshold)
            ax.contour(viz_data, levels=[-4], colors='cyan', linewidths=0.5, alpha=0.5)

            ax.set_title(f"Evolution Step: {step}")
            ax.axis('off') # Cleaner look
            
            # Save to file
            filename = os.path.join(OUTPUT_DIR, f"frame_{step:04d}.png")
            plt.tight_layout()
            plt.savefig(filename)
            frames.append(filename)
            plt.close(fig)

    # 4. GIF Assembly
    print("Compiling GIF...")
    with imageio.get_writer(GIF_NAME, mode='I', duration=0.1) as writer:
        for filename in frames:
            image = imageio.imread(filename)
            writer.append_data(image)

    print(f"Done! GIF saved to {GIF_NAME}")
    # Optional cleanup
    # shutil.rmtree(OUTPUT_DIR) 

if __name__ == "__main__":
    run_evolution()