import numpy as np
import matplotlib.pyplot as plt
import os
import shutil

# =========================================================
#  PIRouette Adaptive Manifold Tracker (Based on 14's architecture)
# =========================================================

# ---------- Dynamics parameters (Unchanged) ----------
TWIST = 3.8        
GAMMA = 0.5
DT    = 0.015
MAX_STEPS = 10     # Max T-steps for divergence (can be increased for final render)
EPSILON = 1e-5     # Initial perturbation for helicity calculation
R_ESCAPE = 100.0   

# ---------- Scanning Parameters ----------
RES = 800          # High resolution for detailed rendering
SCAN_STEP = 5e8    # Amount to pan in each step (500 million units)
MAX_SCAN_ITER = 30 # Limit for the panning loop
TARGET_ZOOM = 0.1  # Target final half-width for the zoom-in (0.1 units)
RENDER_DIST = 1.0  # Final half-width for the zoom-out render (1 unit)

# ---------- Output Settings ----------
OUTPUT_DIR = "manifold_scan_frames"
OUTPUT_FILE = "manifold_boundary_map.png"

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
    nw_red  = w_red  / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam
    return Fm, Flam, nw_red

def normalize_angle_diff_vec(delta):
    """Vectorized angle normalization (-pi to pi)"""
    return np.arctan2(np.sin(delta), np.cos(delta))

def calculate_helicity(M_MIN, M_MAX, L_MIN, L_MAX, MAX_STEPS, grid_res):
    """Calculates the max angular divergence over MAX_STEPS for a given viewport."""
    m_space = np.linspace(M_MIN, M_MAX, grid_res)
    l_space = np.linspace(L_MIN, L_MAX, grid_res)
    M_grid, L_grid = np.meshgrid(m_space, l_space)

    m1 = M_grid.copy(); l1 = L_grid.copy()
    pm1 = np.zeros_like(m1); pl1 = np.zeros_like(l1)
    m2 = M_grid.copy() + EPSILON; l2 = L_grid.copy() + EPSILON
    pm2 = np.zeros_like(m2); pl2 = np.zeros_like(l2)
    max_diff_angle = np.zeros_like(m1)

    for _ in range(1, MAX_STEPS + 1):
        # Two sub-steps for accurate integration (Leapfrog/Verlet)
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

        ang1 = np.arctan2(l1, m1)
        # CORRECTED: The original code in 14.py had a bug: ang2 = np.arctan2(l2, l2). Corrected here to l2/m2.
        ang2 = np.arctan2(l2, m2) 
        diff = normalize_angle_diff_vec(ang1 - ang2)
        adiff = np.abs(diff)
        max_diff_angle = np.maximum(max_diff_angle, adiff)
    
    return np.log(max_diff_angle + 1e-9)


def render_map(viz_data, M_MIN, M_MAX, L_MIN, L_MAX, title, filename):
    """Renders a single frame."""
    LOG_MAX = np.log(np.pi) 
    LOG_MIN = np.log(1e-6) 
    
    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
    
    im = ax.imshow(viz_data, origin="lower", cmap='magma', 
                   extent=[M_MIN, M_MAX, L_MIN, L_MAX],
                   vmin=LOG_MIN, vmax=LOG_MAX) 

    ax.set_title(title)
    ax.set_xlabel("Mass field m")
    ax.set_ylabel("Coupling field λ")
    
    fig.colorbar(im, ax=ax).set_label("Log Angular Divergence (Helicity)")
    plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0)) # Scientific notation
    plt.tight_layout()
    plt.savefig(filename)
    plt.close(fig)

def run_manifold_tracker():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    # ----------------------------------------------
    # Phase 1: Deep Pan (Left and Down)
    # ----------------------------------------------
    print("--- Phase 1: Panning to find the boundary ---")
    
    # Start near the known edge of the Proton Basin from previous analysis (~2.8e10)
    M_HALF = 3e10  # Initial half-width to confirm the line is still visible
    CENTER_M, CENTER_L = 0.0, 0.0 # Start centered
    
    # Scan until the light diagonal line (low divergence) is not visible in the center
    for i in range(1, MAX_SCAN_ITER + 1):
        
        # Define current viewport
        M_MIN = CENTER_M - M_HALF; M_MAX = CENTER_M + M_HALF
        L_MIN = CENTER_L - M_HALF; L_MAX = CENTER_L + M_HALF

        # Calculate helicity (use low T-steps for fast scanning)
        viz_data = calculate_helicity(M_MIN, M_MAX, L_MIN, L_MAX, MAX_STEPS=5, grid_res=100)
        
        # Check the divergence value at the center (where the diagonal line should be)
        # The center index is roughly RES/2. We check a small box near the center.
        center_val = np.mean(viz_data[45:55, 45:55]) 
        
        # Low divergence (light yellow/orange) is near log(pi) to -6. Check for a log divergence > -9
        # If the central value is below -9, the low-divergence line is GONE.
        if center_val < -9.0: 
            print(f"Boundary found! Central divergence is {center_val:.2f} (dark).")
            # Go back one step to the last known position of the line's presence
            CENTER_M += SCAN_STEP 
            CENTER_L += SCAN_STEP 
            break
        
        # Pan the center further into the low/left quadrant
        CENTER_M -= SCAN_STEP 
        CENTER_L -= SCAN_STEP 
        
        print(f"Iteration {i}/{MAX_SCAN_ITER}: Panning to M={CENTER_M:.1e}, L={CENTER_L:.1e}. Center Helicity: {center_val:.2f}")
        
    else:
        print("Max iterations reached. Could not find the boundary with the current SCAN_STEP.")
        return # Exit if boundary wasn't found

    # Set the boundary point for the final renders
    BOUNDARY_M, BOUNDARY_L = CENTER_M, CENTER_L
    print(f"\nPotential boundary point set at M={BOUNDARY_M:.1e}, L={BOUNDARY_L:.1e}")

    # ----------------------------------------------
    # Phase 2: Zoom and Heavy Render
    # ----------------------------------------------
    
    # 1. Zoom In (High Magnification)
    print("\n--- Phase 2a: Zooming in for fine structure (Heavy Render) ---")
    M_HALF_IN = TARGET_ZOOM # 0.1
    M_MIN_IN = BOUNDARY_M - M_HALF_IN; M_MAX_IN = BOUNDARY_M + M_HALF_IN
    L_MIN_IN = BOUNDARY_L - M_HALF_IN; L_MAX_IN = BOUNDARY_L + M_HALF_IN
    
    viz_data_in = calculate_helicity(M_MIN_IN, M_MAX_IN, L_MIN_IN, L_MAX_IN, MAX_STEPS=300, grid_res=RES) 
    
    filename_in = os.path.join(OUTPUT_DIR, "01_boundary_zoom_in.png")
    render_map(viz_data_in, M_MIN_IN, M_MAX_IN, L_MIN_IN, L_MAX_IN, 
               f"Zoom-In: Boundary at M={BOUNDARY_M:.1e}, Extent +/- {M_HALF_IN}", filename_in)
    print(f"Zoom-in map rendered to {filename_in}")

    # 2. Zoom Out (Contextual View)
    print("\n--- Phase 2b: Zooming out for contextual structure (Heavy Render) ---")
    M_HALF_OUT = RENDER_DIST # 1.0
    M_MIN_OUT = BOUNDARY_M - M_HALF_OUT; M_MAX_OUT = BOUNDARY_M + M_HALF_OUT
    L_MIN_OUT = BOUNDARY_L - M_HALF_OUT; L_MAX_OUT = BOUNDARY_L + M_HALF_OUT
    
    viz_data_out = calculate_helicity(M_MIN_OUT, M_MAX_OUT, L_MIN_OUT, L_MAX_OUT, MAX_STEPS=300, grid_res=RES)
    
    filename_out = os.path.join(OUTPUT_DIR, "02_boundary_zoom_out.png")
    render_map(viz_data_out, M_MIN_OUT, M_MAX_OUT, L_MIN_OUT, L_MAX_OUT, 
               f"Zoom-Out: Boundary at M={BOUNDARY_M:.1e}, Extent +/- {M_HALF_OUT}", filename_out)
    print(f"Zoom-out map rendered to {filename_out}")
    
    # Final cleanup (optional based on user preference)
    # shutil.rmtree(OUTPUT_DIR) # Commented out for inspection
    print(f"\nExecution Complete. Check the '{OUTPUT_DIR}' directory for the rendered maps.")

if __name__ == "__main__":
    run_manifold_tracker()