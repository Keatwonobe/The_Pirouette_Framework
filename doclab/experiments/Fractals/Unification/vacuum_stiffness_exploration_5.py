import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from numba import njit, prange
import math

# ============================================================
# CONFIGURATION: VOLUMETRIC RENDERER
# ============================================================
RES = 1000           # Resolution of the density grid
PARTICLE_COUNT = 50000 # Massive cloud for volumetric density
FLOW_RES = 0         # Disable vector flow to focus on the beam

# The South-West Eddy
CENTER_M = -0.6      
CENTER_L = -0.8
ZOOM_WIDTH = 8     # Slightly wider to catch the spray

TWIST = 3.8          
DT = 0.01            
STEPS = 250          # How far the beam travels

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

    # Weights for mixing (optional for mechanics, vital for theory)
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

# ============================================================
# 3. VOLUMETRIC PARTICLE SIMULATOR
# ============================================================

@njit(parallel=True)
def simulate_and_accumulate(center_m, center_l, width, res, count, twist, dt, steps):
    """
    Simulates particles and accumulates their 'density' on a grid.
    This creates the volumetric 'plasma' look.
    """
    # High-precision density buffer (using float64 to avoid overflow before log)
    density_grid = np.zeros((res, res), dtype=np.float64)
    
    min_m = center_m - width/2
    min_l = center_l - width/2
    inv_step = res / width
    
    # We perform simulation in batches or parallel streams
    # To avoid race conditions on the grid in parallel, we can:
    # 1. Use atomics (slow in python/numba context sometimes)
    # 2. Have local grids (memory heavy)
    # 3. Just iterate serially for the 'write' but parallel for the 'math'? 
    #    Actually, standard Numba parallel loop with array write is race-prone.
    #    For visualization 'noise' is acceptable, but let's do a blocked approach 
    #    or just run the loop serially (it's fast enough for 50k particles).
    
    # Let's run the simulation. 
    # Generating start points:
    
    # We'll use a deterministic grid of particles to ensure uniform flux
    side = int(math.sqrt(count))
    total = side * side
    start_step = width / side
    
    # We will compute trajectories and bin them locally to avoid race conditions, 
    # OR since visualization noise is okay, we just accept the race condition 
    # for pure speed. The artifacts are usually invisible in high-density clouds.
    # HOWEVER, to be clean, let's run a simple serial loop. It is plenty fast.
    
    for j in range(side):
        for i in range(side):
            # Initial position
            m = min_m + i * start_step + start_step/2
            l = min_l + j * start_step + start_step/2
            
            # Trace
            curr_m, curr_l = m, l
            for _ in range(steps):
                # RK2 Step
                curr_m, curr_l = rk2_step(curr_m, curr_l, twist, dt)
                
                # Binning
                x_idx = int((curr_m - min_m) * inv_step)
                y_idx = int((curr_l - min_l) * inv_step)
                
                if 0 <= x_idx < res and 0 <= y_idx < res:
                    density_grid[y_idx, x_idx] += 1.0

    return density_grid

# ============================================================
# 4. VISUALIZATION
# ============================================================

def run_analysis():
    print(f"[-] Charging Volumetric Renderer...")
    print(f"    Target: South-West Eddy ({CENTER_M}, {CENTER_L})")
    print(f"    Particles: {PARTICLE_COUNT}")
    
    # 1. Background Chaos (The Terrain)
    print("    Mapping Lyapunov Manifold...")
    lyap_map = compute_precision_lyapunov(
        CENTER_M, CENTER_L, ZOOM_WIDTH, RES, TWIST, DT, STEPS
    )
    
    # 2. Volumetric Beam (The Plasma)
    print("    Accumulating Particle Density...")
    density_map = simulate_and_accumulate(
        CENTER_M, CENTER_L, ZOOM_WIDTH, RES, PARTICLE_COUNT, TWIST, DT, STEPS
    )
    
    # 3. Render
    print("    Compositing...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    extent = [CENTER_M - ZOOM_WIDTH/2, CENTER_M + ZOOM_WIDTH/2, 
              CENTER_L - ZOOM_WIDTH/2, CENTER_L + ZOOM_WIDTH/2]
    
    # A. Lyapunov Map (Context)
    ax0 = axes[0]
    im0 = ax0.imshow(lyap_map, origin='lower', cmap='magma', extent=extent)
    ax0.set_title("Lyapunov Chaos (Terrain)")
    ax0.set_xlabel("Mass Field (m)")
    ax0.set_ylabel("Coupling Field (λ)")
    plt.colorbar(im0, ax=ax0, fraction=0.046, pad=0.04, label="Instability (FTLE)")
    
    # B. Volumetric Density (The Beam)
    ax1 = axes[1]
    
    # Log-Normalization is CRITICAL for volumetric data
    # It reveals the internal structure of the beam (the "patterns")
    # epsilon added to avoid log(0)
    density_map += 1.0 
    
    im1 = ax1.imshow(
        density_map, 
        origin='lower', 
        cmap='afmhot',     # 'afmhot' or 'inferno' looks like glowing plasma
        norm=LogNorm(vmin=1, vmax=np.max(density_map)),
        extent=extent,
        interpolation='bicubic'
    )
    
    ax1.set_title(f"Volumetric Particle Density\n(Log-Scale Accumulation)")
    ax1.set_xlabel("Mass Field (m)")
    ax1.set_ylabel("Coupling Field (λ)")
    
    # Add Pole Markers to the density map for reference
    ax1.scatter([0], [-1], color='cyan', marker='x', label='Red Pole')
    ax1.scatter([-0.866], [0.5], color='green', marker='x', label='Teal Pole')
    ax1.legend(loc='upper right')
    
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04, label="Particle Density (Log Count)")
    
    plt.tight_layout()
    filename = "vacuum_volumetric_beam.png"
    plt.savefig(filename, dpi=200)
    print(f"[+] Volumetric Render saved to {filename}")
    plt.show()

if __name__ == "__main__":
    run_analysis()