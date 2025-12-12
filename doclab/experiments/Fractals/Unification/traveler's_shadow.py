import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math

# ============================================================
# CONFIGURATION: THE MICROSCOPE
# ============================================================
RES = 1000           # High Resolution for "Delicate" Braids
CENTER_M = 1300050       # The "Puncture" (Origin)
CENTER_L = 770005
ZOOM_WIDTH = 15000    # Zoom level (smaller = closer)

TWIST = 3.8          # Tension
DT = 0.01            # Smaller time step for precision
STEPS = 150          # Longer tracking to see the full "braid" develop

# ============================================================
# 1. THE PHYSICS KERNEL (Unchanged)
# ============================================================

@njit(fastmath=True)
def get_physics_components(m, lam, twist):
    """
    Calculates both the Force vector and the Constituent Weights (RGB).
    """
    # --- Component Forces ---
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

    # --- Angular Mixing ---
    angle = math.degrees(math.atan2(lam, m)) % 360.0

    d_gold = abs(angle - 30.0)
    if d_gold > 180.0: d_gold = 360.0 - d_gold
    
    d_teal = abs(angle - 150.0)
    if d_teal > 180.0: d_teal = 360.0 - d_teal
    
    d_red = abs(angle - 270.0)
    if d_red > 180.0: d_red = 360.0 - d_red

    width = 80.0
    w_gold_raw = math.exp(-(d_gold / width)**2)
    w_teal_raw = math.exp(-(d_teal / width)**2)
    w_red_raw  = math.exp(-(d_red / width)**2)

    total_w = w_gold_raw + w_teal_raw + w_red_raw + 1e-12
    nw_gold = w_gold_raw / total_w
    nw_teal = w_teal_raw / total_w
    nw_red  = w_red_raw  / total_w

    Fm = nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam, nw_red, nw_teal, nw_gold

# ============================================================
# 2. THE LYAPUNOV MAPPER (Upgraded)
# ============================================================

@njit(fastmath=True)
def rk2_step(m, l, twist, dt):
    """
    Runge-Kutta 2 (Heun's Method) for smoother trajectories.
    Essential for seeing 'delicate' structures without noise.
    """
    # k1
    fm1, fl1, _, _, _ = get_physics_components(m, l, twist)
    
    # k2 (predictor)
    m_pred = m + fm1 * dt
    l_pred = l + fl1 * dt
    fm2, fl2, _, _, _ = get_physics_components(m_pred, l_pred, twist)
    
    # Update
    m_new = m + (fm1 + fm2) * 0.5 * dt
    l_new = l + (fl1 + fl2) * 0.5 * dt
    
    return m_new, l_new

@njit(parallel=True)
def compute_precision_lyapunov(center_m, center_l, width, res, twist, dt, steps):
    """
    Computes the FTLE with high sensitivity.
    """
    lyap_grid = np.zeros((res, res), dtype=np.float64)
    
    # Calculate bounds
    min_m = center_m - width/2
    min_l = center_l - width/2
    step_size = width / res
    
    # --- FIX: Set a fixed, small perturbation for stability at high zoom ---
    # The perturbation must be small relative to the dynamics, not the zoom window.
    delta = 1e-8  # Fixed small value, independent of 'width'

    for j in prange(res):
        lam0 = min_l + j * step_size
        for i in range(res):
            m0 = min_m + i * step_size

            # Setup three nearby points (Original, Right, Up)
            m, l = m0, lam0
            m_dx, l_dx = m0 + delta, lam0
            m_dy, l_dy = m0, lam0 + delta
            
            # Evolve them
            for _ in range(steps):
                m, l       = rk2_step(m, l, twist, dt)
                m_dx, l_dx = rk2_step(m_dx, l_dx, twist, dt)
                m_dy, l_dy = rk2_step(m_dy, l_dy, twist, dt)

            # Jacobian approximation
            J11 = (m_dx - m) / delta
            J12 = (m_dy - m) / delta
            J21 = (l_dx - l) / delta
            J22 = (l_dy - l) / delta

            # Cauchy-Green Tensor C = J^T * J
            C11 = J11*J11 + J21*J21
            C12 = J11*J12 + J21*J22
            C22 = J12*J12 + J22*J22
            
            # Max Eigenvalue
            Tr = C11 + C22
            Det = C11*C22 - C12*C12
            
            # Ensure the term is non-negative for the square root
            term = (Tr/2.0)**2 - Det
            if term < 0: term = 0
            
            lambda_max = (Tr/2.0) + math.sqrt(term)
            
            # FTLE
            if lambda_max <= 0:
                lyap_grid[j, i] = 0.0
            else:
                lyap_grid[j, i] = math.log(math.sqrt(lambda_max)) / (steps * dt)

    return lyap_grid

# ============================================================
# 3. VISUALIZATION
# ============================================================

def run_analysis():
    print(f"[-] Tracking the 'Braided Twist'...")
    print(f"    Target: ({CENTER_M}, {CENTER_L}) width={ZOOM_WIDTH}")
    
    lyap_map = compute_precision_lyapunov(
        CENTER_M, CENTER_L, ZOOM_WIDTH, RES, TWIST, DT, STEPS
    )
    
    # Normalize for High Contrast ("Delicate" tracking)
    # We clip the bottom 2% to make the black truly black, 
    # and use a power law to enhance the faint filaments.
    
    print("    Rendering...")
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Gamma correction (power < 1.0) boosts the dark, delicate structures
    # 'magma' or 'inferno' are best for seeing 'heat'
    im = ax.imshow(
        lyap_map, 
        origin='lower', 
        cmap='magma', 
        extent=[CENTER_M - ZOOM_WIDTH/2, CENTER_M + ZOOM_WIDTH/2, 
                CENTER_L - ZOOM_WIDTH/2, CENTER_L + ZOOM_WIDTH/2],
        interpolation='bicubic' # Smooths pixelation for a 'field' look
    )
    
    ax.set_title(f"Lyapunov Braid Map\nSensitivity Scan at Twist={TWIST}")
    ax.set_xlabel("Mass Field (m)")
    ax.set_ylabel("Coupling Field (λ)")
    
    # Add a marker for the exact center
    ax.scatter([0], [0], color='cyan', marker='+', s=100, alpha=0.5, label='Origin')
    
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Separation Rate (FTLE)")
    plt.legend()
    
    plt.tight_layout()
    filename = "vacuum_lyapunov_braid.png"
    plt.savefig(filename, dpi=200)
    print(f"[+] Map saved to {filename}")
    plt.show()

if __name__ == "__main__":
    run_analysis()