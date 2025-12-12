import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math

# ============================================================
# CONFIGURATION: THE SOUTH-WEST PARTICLE ACCELERATOR
# ============================================================
RES = 800            # Map Resolution
FLOW_RES = 40        # Streamline Resolution
PARTICLE_COUNT = 500 # Number of test particles to inject

# Targeting the "South-West Eddy" (Interference between Red and Teal poles)
CENTER_M = -0.6      
CENTER_L = -0.8
ZOOM_WIDTH = 2000000     # A balanced view of the eddy

TWIST = 3.8          
DT = 0.01            
STEPS = 200          # Longer integration to see the "firing" distance

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

    # Weights
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

    return Fm, Flam

# ============================================================
# 2. THE SOLVERS (RK2 & Lyapunov)
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
            mag = math.sqrt(fm*fm + fl*fl) + 1e-9
            U[j, i] = fm / mag
            V[j, i] = fl / mag
            
    return U, V

# ============================================================
# 3. PARTICLE INJECTOR (NEW)
# ============================================================

@njit
def simulate_particle_cloud(center_m, center_l, width, count, twist, dt, steps):
    """
    Injects a cloud of particles uniformly in the view and tracks their paths.
    Returns: Array of shape (count, steps, 2)
    """
    paths = np.zeros((count, steps, 2), dtype=np.float64)
    
    # Random seed is not supported in parallel njit easily without setup, 
    # so we use deterministic distribution or simple random if available.
    # We will use a grid distribution for clarity.
    
    grid_side = int(math.sqrt(count))
    step_dist = width / grid_side
    min_m = center_m - width/2
    min_l = center_l - width/2
    
    idx = 0
    for j in range(grid_side):
        for i in range(grid_side):
            if idx >= count: break
            
            # Start position
            m = min_m + i * step_dist + step_dist/2
            l = min_l + j * step_dist + step_dist/2
            
            paths[idx, 0, 0] = m
            paths[idx, 0, 1] = l
            
            # Integrate path
            curr_m, curr_l = m, l
            for t in range(1, steps):
                curr_m, curr_l = rk2_step(curr_m, curr_l, twist, dt)
                paths[idx, t, 0] = curr_m
                paths[idx, t, 1] = curr_l
            
            idx += 1
            
    return paths

# ============================================================
# 4. VISUALIZATION
# ============================================================

def run_analysis():
    print(f"[-] Calibrating Particle Accelerator...")
    print(f"    Target: South-West Eddy ({CENTER_M}, {CENTER_L})")
    
    # 1. Background Chaos
    print("    Computing Lyapunov Surface...")
    lyap_map = compute_precision_lyapunov(
        CENTER_M, CENTER_L, ZOOM_WIDTH, RES, TWIST, DT, STEPS
    )
    
    # 2. Particle Simulation
    print(f"    Injecting {PARTICLE_COUNT} test particles...")
    # Reduce steps for trajectory visual to avoid clutter, or keep high for long paths
    particle_paths = simulate_particle_cloud(
        CENTER_M, CENTER_L, ZOOM_WIDTH, PARTICLE_COUNT, TWIST, DT, 80
    )
    
    # 3. Render
    print("    Rendering...")
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # A. Lyapunov Heatmap (The Terrain)
    im = ax.imshow(
        lyap_map, 
        origin='lower', 
        cmap='inferno', # 'inferno' is great for 'fiery' acceleration
        extent=[CENTER_M - ZOOM_WIDTH/2, CENTER_M + ZOOM_WIDTH/2, 
                CENTER_L - ZOOM_WIDTH/2, CENTER_L + ZOOM_WIDTH/2],
        interpolation='bicubic',
        alpha=0.9
    )
    
    # B. Particle Trajectories (The Accelerator Beam)
    # We plot the paths. We can color them by velocity or time.
    # Let's plot faint white lines for paths, and dots for heads.
    
    for p_idx in range(len(particle_paths)):
        path = particle_paths[p_idx]
        # Check if path stays somewhat in bounds (optional)
        # Plot full path faint
        ax.plot(path[:, 0], path[:, 1], color='cyan', alpha=0.15, linewidth=0.5)
        # Plot head bright
        ax.scatter(path[-1, 0], path[-1, 1], color='white', s=1, alpha=0.6)

    ax.set_title(f"Particle Accelerator View\nSouth-West Eddy (m={CENTER_M}, λ={CENTER_L})")
    ax.set_xlabel("Mass Field (m)")
    ax.set_ylabel("Coupling Field (λ)")
    
    # Poles for reference
    ax.scatter([0], [-1], color='red', marker='x', s=100, label='Red Pole (Violation)')
    ax.scatter([-0.866], [0.5], color='green', marker='x', s=100, label='Teal Pole (Geometry)')
    
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Instability (FTLE)")
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    filename = "vacuum_particle_accelerator.png"
    plt.savefig(filename, dpi=200)
    print(f"[+] Accelerator Map saved to {filename}")
    plt.show()

if __name__ == "__main__":
    run_analysis()