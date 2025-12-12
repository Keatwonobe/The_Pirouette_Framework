import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math

# ============================================================
# CONFIGURATION: THE ANOMALY SCANNER
# ============================================================
# We use the coordinates from the "Shadow" file to target the anomaly.
RES = 800            # Resolution (High enough for detail, low enough for speed)
CENTER_M = 1333689.982       
CENTER_L = 770007.6
ZOOM_WIDTH = 0.1     # The microscope window

TWIST = 3.8          # The tension of the system
DT = 0.01            # Time step
STEPS = 1000         # How long we let the particle run to see if it "zooms"

# ============================================================
# 1. THE PHYSICS KERNEL (Standard Pirouette v3)
# ============================================================

@njit(fastmath=True)
def get_physics_components(m, lam, twist):
    # --- 1. Constituent Weights ---
    angle = math.degrees(math.atan2(lam, m)) % 360.0

    d_gold = abs(angle - 30.0); d_gold = 360.0 - d_gold if d_gold > 180.0 else d_gold
    d_teal = abs(angle - 150.0); d_teal = 360.0 - d_teal if d_teal > 180.0 else d_teal
    d_red = abs(angle - 270.0); d_red = 360.0 - d_red if d_red > 180.0 else d_red

    width = 80.0
    w_gold_raw = math.exp(-(d_gold / width)**2)
    w_teal_raw = math.exp(-(d_teal / width)**2)
    w_red_raw  = math.exp(-(d_red / width)**2)

    total_w = w_gold_raw + w_teal_raw + w_red_raw + 1e-12
    nw_gold = w_gold_raw / total_w
    nw_teal = w_teal_raw / total_w
    nw_red  = w_red_raw  / total_w

    # --- 2. Component Forces ---
    # Teal (Geometric/Linear)
    F_teal_m = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # Red (Violating/Sinusoidal)
    F_red_m = -m
    p_violation = twist * math.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold (Emergent/Non-linear)
    sum_m = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    magnitude = math.sqrt(sum_m*sum_m + sum_lam*sum_lam)
    
    scaling_factor = math.sqrt(magnitude) if magnitude > 1e-16 else 0.0
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor

    # --- 3. Composite Force ---
    Fm = nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam

# ============================================================
# 2. THE VELOCITY PROBE (Hybrid Solver)
# ============================================================

@njit(fastmath=True)
def rk2_step_vel(m, l, twist, dt):
    """
    Returns new position AND current velocity.
    """
    fm1, fl1 = get_physics_components(m, l, twist)
    
    # Predictor
    m_pred = m + fm1 * dt
    l_pred = l + fl1 * dt
    fm2, fl2 = get_physics_components(m_pred, l_pred, twist)
    
    # Corrector
    m_new = m + (fm1 + fm2) * 0.5 * dt
    l_new = l + (fl1 + fl2) * 0.5 * dt
    
    # Velocity Check (Force Magnitude at new position)
    fm_new, fl_new = get_physics_components(m_new, l_new, twist)
    v = math.sqrt(fm_new**2 + fl_new**2)
    
    return m_new, l_new, v

@njit(parallel=True)
def compute_velocity_manifold(center_m, center_l, width, res, twist, dt, steps):
    """
    Instead of Lyapunov divergence, we map the Maximum Velocity
    achieved by a particle starting at (x,y).
    """
    vel_grid = np.zeros((res, res), dtype=np.float64)
    
    min_m = center_m - width/2
    min_l = center_l - width/2
    step_size = width / res
    
    for j in prange(res):
        lam0 = min_l + j * step_size
        for i in range(res):
            m0 = min_m + i * step_size
            
            # Spawn particle
            curr_m, curr_l = m0, lam0
            max_v = 0.0
            
            # Let it run and record its "Panic" (Max Velocity)
            for _ in range(steps):
                curr_m, curr_l, v = rk2_step_vel(curr_m, curr_l, twist, dt)
                if v > max_v:
                    max_v = v
            
            vel_grid[j, i] = max_v

    return vel_grid

# ============================================================
# 3. VISUALIZATION
# ============================================================

def run_analysis():
    print(f"[-] Initializing Anomaly Scanner...")
    print(f"    Target: ({CENTER_M}, {CENTER_L})")
    print(f"    Mode:   Kinetic Potential (Max Velocity Mapping)")
    
    # 1. Compute the Grid
    vel_map = compute_velocity_manifold(
        CENTER_M, CENTER_L, ZOOM_WIDTH, RES, TWIST, DT, STEPS
    )
    
    # 2. Visualization
    print("    Rendering...")
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # We use 'inferno' because it makes high-velocity zones look like 
    # glowing heat sources.
    im = ax.imshow(
        vel_map, 
        origin='lower', 
        cmap='inferno', 
        extent=[CENTER_M - ZOOM_WIDTH/2, CENTER_M + ZOOM_WIDTH/2, 
                CENTER_L - ZOOM_WIDTH/2, CENTER_L + ZOOM_WIDTH/2],
        interpolation='bicubic'
    )
    
    # Add contour lines to show the "slope" of the velocity well
    # This helps identify the "event horizon" of the invisible object
    print("    Calculating Contours...")
    cnt = ax.contour(
        vel_map, 
        levels=15, 
        colors='cyan', 
        linewidths=0.5, 
        alpha=0.5,
        extent=[CENTER_M - ZOOM_WIDTH/2, CENTER_M + ZOOM_WIDTH/2, 
                CENTER_L - ZOOM_WIDTH/2, CENTER_L + ZOOM_WIDTH/2]
    )
    
    ax.set_title(f"Manifold Velocity Profile\nLocation: {CENTER_M}, {CENTER_L}", color='black')
    ax.set_xlabel("Mass Field (m)")
    ax.set_ylabel("Coupling Field (λ)")
    
    # Center Marker
    ax.scatter([CENTER_M], [CENTER_L], color='white', marker='+', s=100, alpha=0.8, label='Scan Center')
    
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Peak Velocity Achieved")
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    filename = "anomaly_velocity_scan.png"
    plt.savefig(filename, dpi=200)
    print(f"[+] Scan Complete. Data saved to {filename}")
    plt.show()

if __name__ == "__main__":
    run_analysis()