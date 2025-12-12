import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math

# ============================================================
# CONFIGURATION
# ============================================================
RES = 800           # Resolution (800x800 is good for detail)
ZOOM_RANGE = 0.004    # Range of the plot (-4 to 4)
TWIST = 3.8         # The universe's tension parameter
DT = 0.05           # Time step for Lyapunov integration
STEPS = 50          # How long to track the particle trajectories

# ============================================================
# 1. THE PHYSICS KERNEL (Numba Accelerated)
# ============================================================

@njit(fastmath=True)
def get_physics_components(m, lam, twist):
    """
    Calculates both the Force vector and the Constituent Weights (RGB).
    Returns: Fm, Flam, w_red, w_teal, w_gold
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
    
    # Gold only emerges if there is "energy" in the system
    scaling_factor = math.sqrt(magnitude) if magnitude > 1e-16 else 0.0
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor

    # --- Angular Mixing (The "Grain") ---
    angle = math.degrees(math.atan2(lam, m)) % 360.0

    # Gaussian weights for the three poles
    # Gold at 30 deg, Teal at 150 deg, Red at 270 deg
    
    # Helper for circular distance
    d_gold = abs(angle - 30.0)
    if d_gold > 180.0: d_gold = 360.0 - d_gold
    
    d_teal = abs(angle - 150.0)
    if d_teal > 180.0: d_teal = 360.0 - d_teal
    
    d_red = abs(angle - 270.0)
    if d_red > 180.0: d_red = 360.0 - d_red

    # Width of the influence sectors
    width = 80.0
    w_gold_raw = math.exp(-(d_gold / width)**2)
    w_teal_raw = math.exp(-(d_teal / width)**2)
    w_red_raw  = math.exp(-(d_red / width)**2)

    # Normalize weights so they sum to 1
    total_w = w_gold_raw + w_teal_raw + w_red_raw + 1e-12
    nw_gold = w_gold_raw / total_w
    nw_teal = w_teal_raw / total_w
    nw_red  = w_red_raw  / total_w

    # Final Composite Force
    Fm = nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam, nw_red, nw_teal, nw_gold

# ============================================================
# 2. SOLVERS (RGB & LYAPUNOV)
# ============================================================

@njit(parallel=True)
def compute_rgb_map(min_val, max_val, res, twist):
    """
    Generates a map where:
    R = Red Force Dominance
    G = Teal Force Dominance
    B = Gold Force Dominance
    """
    rgb_grid = np.zeros((res, res, 3), dtype=np.float32)
    step = (max_val - min_val) / res

    for j in prange(res):
        lam = min_val + j * step
        for i in range(res):
            m = min_val + i * step
            
            _, _, r, t, g = get_physics_components(m, lam, twist)
            
            # Direct mapping of weights to color channels
            rgb_grid[j, i, 0] = r  # Red channel
            rgb_grid[j, i, 1] = t  # Green channel (Teal)
            rgb_grid[j, i, 2] = g  # Blue channel (Gold)

    return rgb_grid

@njit(parallel=True)
def compute_lyapunov_map(min_val, max_val, res, twist, dt, steps):
    """
    Computes the Finite Time Lyapunov Exponent (FTLE).
    Measures how fast nearby points diverge.
    """
    lyap_grid = np.zeros((res, res), dtype=np.float64)
    step_size = (max_val - min_val) / res
    
    # Perturbation size for finite difference Jacobian
    delta = 1e-5

    for j in prange(res):
        lam0 = min_val + j * step_size
        for i in range(res):
            m0 = min_val + i * step_size

            # We track a reference point (m, l) and two neighbors
            # (m+d, l) and (m, l+d) to estimate the deformation tensor.
            
            m, l = m0, lam0
            m_dx, l_dx = m0 + delta, lam0
            m_dy, l_dy = m0, lam0 + delta
            
            # Evolve the three points through the force field
            for _ in range(steps):
                # Point 1 (Center)
                fm, fl, _, _, _ = get_physics_components(m, l, twist)
                m += fm * dt
                l += fl * dt
                
                # Point 2 (Right neighbor)
                fm_dx, fl_dx, _, _, _ = get_physics_components(m_dx, l_dx, twist)
                m_dx += fm_dx * dt
                l_dx += fl_dx * dt
                
                # Point 3 (Top neighbor)
                fm_dy, fl_dy, _, _, _ = get_physics_components(m_dy, l_dy, twist)
                m_dy += fm_dy * dt
                l_dy += fl_dy * dt

            # Calculate the deformation gradient tensor F (approximate)
            # F = [ (x_final - x_initial)/delta   (y_final - y_initial)/delta ]
            # Note: We only care about the final spread relative to the current position
            # Jacobian J approx:
            J11 = (m_dx - m) / delta
            J12 = (m_dy - m) / delta
            J21 = (l_dx - l) / delta
            J22 = (l_dy - l) / delta

            # Cauchy-Green Deformation Tensor C = J^T * J
            # We want the max eigenvalue of C to find max stretching
            C11 = J11*J11 + J21*J21
            C12 = J11*J12 + J21*J22
            C22 = J12*J12 + J22*J22
            
            # Eigenvalues of 2x2 symmetric matrix
            # lambda = (Tr/2) +/- sqrt((Tr/2)^2 - Det)
            Tr = C11 + C22
            Det = C11*C22 - C12*C12
            
            # Avoid negative under sqrt due to float precision
            term = (Tr/2.0)**2 - Det
            if term < 0: term = 0
            
            lambda_max = (Tr/2.0) + math.sqrt(term)
            
            # FTLE formula: (1 / |T|) * ln(sqrt(lambda_max))
            # T = steps * dt
            if lambda_max <= 0:
                lyap_grid[j, i] = 0.0
            else:
                lyap_grid[j, i] = math.log(math.sqrt(lambda_max)) / (steps * dt)

    return lyap_grid

# ============================================================
# 3. VISUALIZATION
# ============================================================

def run_analysis():
    print(f"[-] Starting Solver (Res: {RES}x{RES})...")
    
    # 1. Compute RGB Map
    print("    Calculating RGB Constituent Map...")
    rgb_map = compute_rgb_map(-ZOOM_RANGE, ZOOM_RANGE, RES, TWIST)
    
    # 2. Compute Lyapunov Map
    print(f"    Calculating Lyapunov Chaos Map ({STEPS} steps)...")
    lyap_map = compute_lyapunov_map(-ZOOM_RANGE, ZOOM_RANGE, RES, TWIST, DT, STEPS)
    
    # 3. Plotting
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # --- Plot 1: RGB Constituents ---
    # We rotate the array 90 degrees or flip to match standard cartesian (origin bottom-left)
    # Origin='lower' in imshow handles the Y-axis direction, but the loops filled it (row, col).
    # row 0 is min_val (bottom). So origin='lower' is correct.
    
    axes[0].imshow(rgb_map, origin='lower', extent=[-ZOOM_RANGE, ZOOM_RANGE, -ZOOM_RANGE, ZOOM_RANGE])
    axes[0].set_title("Vacuum Composition (RGB)\nRed=Violation, Green=Teal/Base, Blue=Gold/Emergent")
    axes[0].set_xlabel("Mass Field (m)")
    axes[0].set_ylabel("Coupling Field (λ)")
    
    # Add simple markers for the 'Poles'
    axes[0].scatter([0], [-1], color='red', marker='x', label='Red Pole')
    axes[0].scatter([-0.866], [0.5], color='cyan', marker='x', label='Teal Pole')
    axes[0].legend(loc='upper right')

    # --- Plot 2: Lyapunov Chaos ---
    # We use a logarithmic scale or robust colormap to see the ridges
    im_lyap = axes[1].imshow(lyap_map, origin='lower', cmap='inferno', 
                             extent=[-ZOOM_RANGE, ZOOM_RANGE, -ZOOM_RANGE, ZOOM_RANGE])
    axes[1].set_title(f"Finite-Time Lyapunov Exponent (Chaos)\nBright = High Divergence / Instability")
    axes[1].set_xlabel("Mass Field (m)")
    axes[1].set_ylabel("Coupling Field (λ)")
    plt.colorbar(im_lyap, ax=axes[1], fraction=0.046, pad=0.04, label="Separation Rate (FTLE)")

    plt.tight_layout()
    plt.savefig("vacuum_rgb_lyapunov.png", dpi=150)
    print("[+] Analysis Complete. Saved to vacuum_rgb_lyapunov.png")
    plt.show()

if __name__ == "__main__":
    run_analysis()