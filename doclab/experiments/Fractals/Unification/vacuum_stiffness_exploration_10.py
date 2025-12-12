import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import njit, prange
import math

# ============================================================
# CONFIGURATION: THE BALLISTIC CEILING (MAX VELOCITY MAP)
# ============================================================
PARTICLE_COUNT = 500000 
SOURCE_RADIUS = 14        # "Lobbed from the origin"
TRACE_STEPS = 5000         # Long flight to find the true peak

# Auto-scaling will handle the view, but we expect it to be large
TWIST = 3.8          
DT = 0.02            

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
# 2. SOLVER: THE PEAK FINDER
# ============================================================

@njit(fastmath=True)
def rk2_step_vel(m, l, twist, dt):
    fm1, fl1 = get_physics_components(m, l, twist)
    m_pred = m + fm1 * dt
    l_pred = l + fl1 * dt
    fm2, fl2 = get_physics_components(m_pred, l_pred, twist)
    m_new = m + (fm1 + fm2) * 0.5 * dt
    l_new = l + (fl1 + fl2) * 0.5 * dt
    
    # Calc velocity at new pos
    fm_new, fl_new = get_physics_components(m_new, l_new, twist)
    v = math.sqrt(fm_new**2 + fl_new**2)
    
    return m_new, l_new, v

@njit(parallel=True)
def find_ballistic_ceiling(radius, count, twist, dt, steps):
    """
    Simulates particles and returns ONLY the point (m, l, v)
    where Velocity was Maximized.
    """
    peaks = np.zeros((count, 3), dtype=np.float64) # m, l, max_v
    
    for i in prange(count):
        # Lob from Origin
        theta = (i / count) * 2.0 * math.pi
        m = radius * math.cos(theta)
        l = radius * math.sin(theta)
        
        curr_m, curr_l = m, l
        max_v = 0.0
        max_m = m
        max_l = l
        
        # Flight
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
# 3. VISUALIZATION
# ============================================================

def run_analysis():
    print(f"[-] Calculating Ballistic Ceiling...")
    print(f"    Lobbing {PARTICLE_COUNT} rounds from Origin...")
    
    peaks = find_ballistic_ceiling(SOURCE_RADIUS, PARTICLE_COUNT, TWIST, DT, TRACE_STEPS)
    
    # Filter: remove points that never accelerated (stuck at origin)
    mask = peaks[:, 2] > 0.1
    peaks = peaks[mask]
    
    print(f"    Rendering {len(peaks)} Peak-Energy Points...")
    
    fig = plt.figure(figsize=(14, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Black Void
    ax.set_facecolor('black')
    ax.grid(False) 
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Scatter: X, Y, Z=Max_Velocity
    # Color also = Max_Velocity to make it glow
    sc = ax.scatter(
        peaks[:, 0], peaks[:, 1], peaks[:, 2],
        c=peaks[:, 2],
        cmap='inferno',  # Fire for energy
        s=1.0,           # Tiny points to see the shell surface
        alpha=0.8
    )
    
    # Calculate bounds for neatness
    max_range = max(np.max(np.abs(peaks[:,0])), np.max(np.abs(peaks[:,1])))
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    
    ax.set_title(f"The Ballistic Ceiling\n(Points where Acceleration stops and Return begins)", color='white')
    ax.set_xlabel('Mass Field (m)', color='gray')
    ax.set_ylabel('Coupling Field (λ)', color='gray')
    ax.set_zlabel('Peak Velocity', color='gray')
    
    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')
    ax.tick_params(axis='z', colors='gray')
    
    # View from above-ish to see the Shell Shape
    ax.view_init(elev=35, azim=-120)
    
    cbar = plt.colorbar(sc, shrink=0.5, pad=0.1)
    cbar.set_label('Maximum Achieved Velocity', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.tight_layout()
    filename = "vacuum_ballistic_ceiling.png"
    plt.savefig(filename, dpi=200, facecolor='black')
    print(f"[+] Ceiling Mapped: {filename}")
    plt.show()

if __name__ == "__main__":
    run_analysis()