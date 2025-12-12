import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
import math

# ============================================================
# CONFIGURATION: THE AUTO-SCALING HOLOGRAPH
# ============================================================
PARTICLE_COUNT = 250000 
SOURCE_RADIUS = 0.5        # The "Event Horizon" ring size

# NOTE: ZOOM_WIDTH is now calculated automatically
TWIST = 3.8          
DT = 0.05                  
STEPS = 5000               

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

    # Weights for mixing
    angle = math.degrees(math.atan2(lam, m)) % 360.0
    
    # Gaussian weights
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
# 2. SOLVER: THE PROJECTION ENGINE
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
def run_holographic_projection(radius, count, twist, dt, steps):
    """
    Injects particles on a circle of radius 'radius'.
    """
    final_pos = np.zeros((count, 2), dtype=np.float64)
    origin_angle = np.zeros(count, dtype=np.float64)
    final_vel = np.zeros(count, dtype=np.float64)
    
    for i in prange(count):
        theta = (i / count) * 2.0 * math.pi
        
        # Start on the ring
        m = radius * math.cos(theta)
        l = radius * math.sin(theta)
        
        origin_angle[i] = math.degrees(theta) % 360.0
        
        curr_m, curr_l = m, l
        for _ in range(steps):
            curr_m, curr_l = rk2_step(curr_m, curr_l, twist, dt)
            
        final_pos[i, 0] = curr_m
        final_pos[i, 1] = curr_l
        
        fm, fl = get_physics_components(curr_m, curr_l, twist)
        final_vel[i] = math.sqrt(fm*fm + fl*fl)

    return final_pos, origin_angle, final_vel

# ============================================================
# 3. VISUALIZATION
# ============================================================

def run_analysis():
    print(f"[-] Initializing Holographic Projector...")
    print(f"    Source Ring Radius: {SOURCE_RADIUS}")
    print(f"    Particles: {PARTICLE_COUNT}")
    
    # Run Simulation
    final_pos, origin_ids, speed = run_holographic_projection(
        SOURCE_RADIUS, PARTICLE_COUNT, TWIST, DT, STEPS
    )
    
    # --- AUTO-SCALING LOGIC ---
    # Find the maximum distance any particle traveled
    distances = np.sqrt(final_pos[:,0]**2 + final_pos[:,1]**2)
    max_dist = np.max(distances)
    avg_dist = np.mean(distances)
    
    print(f"    [!] TELEMETRY:")
    print(f"        Max Distance Traveled: {max_dist:.4f}")
    print(f"        Avg Distance Traveled: {avg_dist:.4f}")
    
    if max_dist < 10.0:
        print("        -> NOTE: The universe is bounded/attractive. Particles are trapped.")
    
    # Set zoom to fit the actual data with a 10% margin
    zoom_limit = max_dist * 1.1
    if zoom_limit < 1.0: zoom_limit = 1.0 # Minimum zoom
    
    print(f"    rendering at Auto-Zoom: {zoom_limit:.4f}...")
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    
    # Use smaller points if dense, larger if sparse
    pt_size = 0.5 if PARTICLE_COUNT < 50000 else 0.1
    
    # Color = Origin Angle (Holographic Information)
    sc = ax.scatter(
        final_pos[:, 0], 
        final_pos[:, 1], 
        c=origin_ids, 
        cmap='hsv', # Rainbow cycle for 360 degrees
        s=pt_size,       
        alpha=0.6
    )
    
    # Add the "Source Ring" for context
    circle = plt.Circle((0, 0), SOURCE_RADIUS, color='white', fill=False, linestyle='--', alpha=0.3)
    ax.add_artist(circle)
    
    ax.set_xlim(-zoom_limit, zoom_limit)
    ax.set_ylim(-zoom_limit, zoom_limit)
    
    ax.set_title(f"Holographic Projection Test\nAuto-Scaled to Max Travel ({max_dist:.2f})\nColor = Angle of Origin (Information Trace)", color='white')
    ax.set_xlabel("Mass Field", color='gray')
    ax.set_ylabel("Coupling Field", color='gray')
    
    ax.tick_params(colors='gray')
    for spine in ax.spines.values():
        spine.set_edgecolor('gray')
        
    cbar = plt.colorbar(sc, shrink=0.7, pad=0.05)
    cbar.set_label('Origin Angle (Degrees)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.tight_layout()
    filename = "vacuum_holographic_projection.png"
    plt.savefig(filename, dpi=250, facecolor='black')
    print(f"[+] Hologram captured: {filename}")
    plt.show()

if __name__ == "__main__":
    run_analysis()