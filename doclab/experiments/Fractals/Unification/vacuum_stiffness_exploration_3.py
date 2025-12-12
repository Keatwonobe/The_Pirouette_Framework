import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math

# ============================================================
# CONFIGURATION: THE MICROSCOPE
# ============================================================
RES = 1000           # High Resolution for the Map
FLOW_RES = 50        # Lower Resolution for Streamlines (to avoid clutter)
CENTER_M = 0.0       
CENTER_L = 0.0
ZOOM_WIDTH = 6     

TWIST = 3.8          
DT = 0.01            
STEPS = 150          

# ============================================================
# 1. THE PHYSICS KERNEL
# ============================================================

@njit(fastmath=True)
def get_physics_components(m, lam, twist):
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

    # Weights (Unused for flow, but kept for consistency)
    angle = math.degrees(math.atan2(lam, m)) % 360.0
    
    # ... (Weight calculation omitted for speed, logic same as before) ...
    # We just need the forces for the flow lines
    
    # Simple Weight Approx for Force Calculation
    # (Full calculation handles the mixing, but for flow lines 
    # we can use the composite result directly if we fully calc it, 
    # but let's stick to the full physics to be safe)
    
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

    return Fm, Flam

# ============================================================
# 2. THE SOLVERS
# ============================================================

@njit(fastmath=True)
def rk2_step(m, l, twist, dt):
    fm1, fl1 = get_physics_components(m, l, twist)
    m_pred = m + fm1 * dt
    l_pred = l + fl1 * dt
    fm2, fl2 = get_physics_components(m_pred, l_pred, twist)
    m_new = m + (fm1 + fm2) * 0.5 * dt
    l_new = l + (fl1 + fl2) * 0.5 * dt
    return m_new, l_new

@njit(parallel=True)
def compute_precision_lyapunov(center_m, center_l, width, res, twist, dt, steps):
    lyap_grid = np.zeros((res, res), dtype=np.float64)
    min_m = center_m - width/2
    min_l = center_l - width/2
    step_size = width / res
    delta = width * 1e-5 

    for j in prange(res):
        lam0 = min_l + j * step_size
        for i in range(res):
            m0 = min_m + i * step_size
            
            # 3-Point Evolution for Jacobian
            m, l = m0, lam0
            m_dx, l_dx = m0 + delta, lam0
            m_dy, l_dy = m0, lam0 + delta
            
            for _ in range(steps):
                m, l       = rk2_step(m, l, twist, dt)
                m_dx, l_dx = rk2_step(m_dx, l_dx, twist, dt)
                m_dy, l_dy = rk2_step(m_dy, l_dy, twist, dt)

            J11, J12 = (m_dx - m)/delta, (m_dy - m)/delta
            J21, J22 = (l_dx - l)/delta, (l_dy - l)/delta

            C11 = J11*J11 + J21*J21
            C12 = J11*J12 + J21*J22
            C22 = J12*J12 + J22*J22
            
            Tr = C11 + C22
            Det = C11*C22 - C12*C12
            term = (Tr/2.0)**2 - Det
            if term < 0: term = 0
            lambda_max = (Tr/2.0) + math.sqrt(term)
            
            if lambda_max <= 0: lyap_grid[j, i] = 0.0
            else: lyap_grid[j, i] = math.log(math.sqrt(lambda_max)) / (steps * dt)

    return lyap_grid

@njit(parallel=True)
def compute_flow_field(center_m, center_l, width, res, twist):
    """
    Computes the instantaneous velocity field for streamlines.
    """
    U = np.zeros((res, res), dtype=np.float64)
    V = np.zeros((res, res), dtype=np.float64)
    min_m = center_m - width/2
    min_l = center_l - width/2
    step_size = width / res

    for j in prange(res):
        lam = min_l + j * step_size
        for i in range(res):
            m = min_m + i * step_size
            fm, fl = get_physics_components(m, lam, twist)
            # Normalize for visualization uniformity (optional, but helps streamlines)
            mag = math.sqrt(fm*fm + fl*fl) + 1e-9
            U[j, i] = fm / mag
            V[j, i] = fl / mag
            
    return U, V

# ============================================================
# 3. VISUALIZATION
# ============================================================

def run_analysis():
    print(f"[-] Tracking the 'Braided Twist'...")
    print(f"    Target: ({CENTER_M}, {CENTER_L}) width={ZOOM_WIDTH}")
    
    # 1. The Chaos Map (Background)
    print("    Computing Lyapunov Surface...")
    lyap_map = compute_precision_lyapunov(
        CENTER_M, CENTER_L, ZOOM_WIDTH, RES, TWIST, DT, STEPS
    )
    
    # 2. The Flow Field (Overlay)
    print("    Computing Vector Flow...")
    U, V = compute_flow_field(CENTER_M, CENTER_L, ZOOM_WIDTH, FLOW_RES, TWIST)
    
    # 3. Render
    print("    Rendering Composite...")
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # A. Lyapunov Heatmap
    im = ax.imshow(
        lyap_map, 
        origin='lower', 
        cmap='magma', 
        extent=[CENTER_M - ZOOM_WIDTH/2, CENTER_M + ZOOM_WIDTH/2, 
                CENTER_L - ZOOM_WIDTH/2, CENTER_L + ZOOM_WIDTH/2],
        interpolation='bicubic',
        alpha=0.9
    )
    
    # B. Streamlines (The Dye)
    # Generate grid for streamplot
    x = np.linspace(CENTER_M - ZOOM_WIDTH/2, CENTER_M + ZOOM_WIDTH/2, FLOW_RES)
    y = np.linspace(CENTER_L - ZOOM_WIDTH/2, CENTER_L + ZOOM_WIDTH/2, FLOW_RES)
    
    # Streamplot color
    strm = ax.streamplot(x, y, U, V, color='cyan', linewidth=0.8, arrowsize=1.0, density=1.5)
    
    ax.set_title(f"Homoclinic Tangle: Lyapunov Braid + Flow\nTwist={TWIST}")
    ax.set_xlabel("Mass Field (m)")
    ax.set_ylabel("Coupling Field (λ)")
    
    ax.scatter([0], [0], color='white', marker='+', s=100, label='Puncture Point (Saddle)')
    
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Instability (FTLE)")
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    filename = "vacuum_braid_flow.png"
    plt.savefig(filename, dpi=200)
    print(f"[+] Diagnostic Map saved to {filename}")
    plt.show()

if __name__ == "__main__":
    run_analysis()