import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math

# ============================================================
# CONFIGURATION: THE SHADOW ALIGNMENT
# ============================================================
# We are looking for the "Smaller Lobe" near the origin.
# A zoom of 2.5 should capture the inner lobe structure.
ZOOM_WIDTH = 2.5     
RES = 800            # Resolution for the Shadow (Lyapunov)

# Traveler Settings
PARTICLE_COUNT = 50000 
SOURCE_RADIUS = 0.1  # Lob from singularity
TRACE_STEPS = 5000   

TWIST = 3.8          
DT = 0.02            

# ============================================================
# 1. THE PHYSICS KERNEL
# ============================================================

@njit(fastmath=True)
def get_physics_components(m, lam, twist):
    # Weights
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

    # Forces
    F_teal_m = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    F_red_m = -m
    p_violation = twist * math.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = F_teal_m + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    magnitude = math.sqrt(sum_m*sum_m + sum_lam*sum_lam)
    
    scaling_factor = math.sqrt(magnitude) if magnitude > 1e-16 else 0.0
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor

    Fm = nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam

# ============================================================
# 2. SOLVER A: THE SHADOW (LYAPUNOV MAP)
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
def compute_lyapunov_background(width, res, twist, dt, steps):
    lyap_grid = np.zeros((res, res), dtype=np.float64)
    min_val = -width/2
    step_size = width / res
    delta = width * 1e-5 

    for j in prange(res):
        lam0 = min_val + j * step_size
        for i in range(res):
            m0 = min_val + i * step_size
            
            m, l = m0, lam0
            m_dx, l_dx = m0 + delta, lam0
            m_dy, l_dy = m0, lam0 + delta
            
            # Short integration for the background structure
            for _ in range(150): 
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
            else: lyap_grid[j, i] = math.log(math.sqrt(lambda_max))

    return lyap_grid

# ============================================================
# 3. SOLVER B: THE TRAVELER (BALLISTIC SHELL)
# ============================================================

@njit(fastmath=True)
def rk2_step_vel(m, l, twist, dt):
    fm1, fl1 = get_physics_components(m, l, twist)
    m_pred = m + fm1 * dt
    l_pred = l + fl1 * dt
    fm2, fl2 = get_physics_components(m_pred, l_pred, twist)
    m_new = m + (fm1 + fm2) * 0.5 * dt
    l_new = l + (fl1 + fl2) * 0.5 * dt
    
    fm_new, fl_new = get_physics_components(m_new, l_new, twist)
    v = math.sqrt(fm_new**2 + fl_new**2)
    return m_new, l_new, v

@njit(parallel=True)
def find_ballistic_shell(radius, count, twist, dt, steps):
    peaks = np.zeros((count, 3), dtype=np.float64) 
    
    for i in prange(count):
        theta = (i / count) * 2.0 * math.pi
        m = radius * math.cos(theta)
        l = radius * math.sin(theta)
        
        curr_m, curr_l = m, l
        max_v = 0.0
        max_m = m
        max_l = l
        
        for _ in range(steps):
            curr_m, curr_l, v = rk2_step_vel(curr_m, curr_l, twist, dt)
            if v > max_v:
                max_v = v
                max_m = curr_m
                max_l = curr_l
                
        peaks[i, 0] = max_m
        peaks[i, 1] = max_l
        peaks[i, 2] = max_v

    return peaks

# ============================================================
# 4. VISUALIZATION: THE COMPOSITE
# ============================================================

def run_analysis():
    print(f"[-] Running Shadow Alignment Test...")
    print(f"    Zoom: {ZOOM_WIDTH}")
    
    # 1. Compute The Shadow (Lyapunov)
    print("    Computing Lyapunov Shadow...")
    lyap_map = compute_lyapunov_background(ZOOM_WIDTH, RES, TWIST, DT, 150)
    
    # 2. Compute The Traveler (Shell)
    print("    Tracking Traveler Shell...")
    shell_points = find_ballistic_shell(SOURCE_RADIUS, PARTICLE_COUNT, TWIST, DT, TRACE_STEPS)
    
    # Filter points that barely moved (stuck at origin)
    mask = shell_points[:, 2] > 0.1
    shell_points = shell_points[mask]
    
    # 3. Render Composite
    print("    Aligning Layers...")
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Layer 1: Lyapunov (The Dark Background)
    # Using 'magma' so ridges are bright orange/white
    extent = [-ZOOM_WIDTH/2, ZOOM_WIDTH/2, -ZOOM_WIDTH/2, ZOOM_WIDTH/2]
    ax.imshow(lyap_map, origin='lower', cmap='magma', extent=extent, alpha=0.9)
    
    # Layer 2: Traveler Points (The Structure)
    # We color them CYAN to contrast with Magma
    # We only plot points that fall within the zoom window
    
    in_view_mask = (np.abs(shell_points[:, 0]) < ZOOM_WIDTH/2) & (np.abs(shell_points[:, 1]) < ZOOM_WIDTH/2)
    visible_points = shell_points[in_view_mask]
    
    print(f"    Plotting {len(visible_points)} visible Traveler points...")
    
    ax.scatter(
        visible_points[:, 0], 
        visible_points[:, 1], 
        s=1.5, 
        color='cyan', 
        alpha=0.6,
        label='Traveler (Peak Velocity)'
    )
    
    # Decoration
    ax.set_title(f"Shadow Alignment Test\nBackground: Lyapunov Instability | Foreground: Traveler Shell", color='black')
    ax.set_xlabel("Mass Field (m)")
    ax.set_ylabel("Coupling Field (λ)")
    
    # Mark Origin
    ax.scatter([0], [0], color='white', marker='+', s=100, alpha=0.5)
    
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    filename = "vacuum_shadow_alignment.png"
    plt.savefig(filename, dpi=200)
    print(f"[+] Composite saved to {filename}")
    plt.show()

if __name__ == "__main__":
    run_analysis()