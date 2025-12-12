import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import njit, prange
import math

# ============================================================
# CONFIGURATION: THE SANDCASTLE (HIGH ENERGY WAKE)
# ============================================================
# We increase particle count to build a solid "structure"
PARTICLE_COUNT = 100000 
TRACE_STEPS = 120      # Optimal length to show the "walls" without clutter

# "Zooming Out" to see the form emerge
CENTER_M = -0.0      
CENTER_L = -0.0
ZOOM_WIDTH = 36000000.0       # Wide view

TWIST = 3.8          
DT = 0.01            

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
# 2. SOLVERS (RK2 & ACCELERATION TRACER)
# ============================================================

@njit(fastmath=True)
def rk2_step(m, l, twist, dt):
    fm1, fl1 = get_physics_components(m, l, twist)
    m_pred = m + fm1 * dt
    l_pred = l + fl1 * dt
    fm2, fl2 = get_physics_components(m_pred, l_pred, twist)
    m_new = m + (fm1 + fm2) * 0.5 * dt
    l_new = l + (fl1 + fl2) * 0.5 * dt
    
    # Physics Calculation for Analysis
    fm_new, fl_new = get_physics_components(m_new, l_new, twist)
    vel_mag = math.sqrt(fm_new*fm_new + fl_new*fl_new)
    
    return m_new, l_new, vel_mag

@njit(parallel=True)
def generate_sandcastle_traces(center_m, center_l, width, count, twist, dt, steps):
    """
    Returns traces of shape (count, steps, 4)
    Dim 4: [m, lambda, velocity, acceleration]
    """
    traces = np.zeros((count, steps, 4), dtype=np.float64)
    
    side = int(math.sqrt(count))
    start_step = width / side
    min_m = center_m - width/2
    min_l = center_l - width/2
    
    idx = 0
    for j in range(side):
        for i in range(side):
            if idx >= count: break
            
            m = min_m + i * start_step + start_step/2
            l = min_l + j * start_step + start_step/2
            
            curr_m, curr_l = m, l
            
            # Record start
            fm, fl = get_physics_components(m, l, twist)
            v0 = math.sqrt(fm*fm + fl*fl)
            
            traces[idx, 0, 0] = m
            traces[idx, 0, 1] = l
            traces[idx, 0, 2] = v0
            traces[idx, 0, 3] = 0.0 # Initial accel undefined/zero
            
            prev_v = v0
            
            for t in range(1, steps):
                curr_m, curr_l, vel = rk2_step(curr_m, curr_l, twist, dt)
                
                # Calculate Acceleration (dv/dt)
                accel = (vel - prev_v) / dt
                prev_v = vel
                
                traces[idx, t, 0] = curr_m
                traces[idx, t, 1] = curr_l
                traces[idx, t, 2] = vel
                traces[idx, t, 3] = accel
                
            idx += 1
    return traces

# ============================================================
# 3. 3D VISUALIZATION (THE SANDCASTLE BUILDER)
# ============================================================

def run_3d_analysis():
    print(f"[-] Building Velocity Sandcastle...")
    print(f"    Zoom: {ZOOM_WIDTH} | Particles: {PARTICLE_COUNT}")
    
    # 1. Generate Traces
    raw_traces = generate_sandcastle_traces(CENTER_M, CENTER_L, ZOOM_WIDTH, PARTICLE_COUNT, TWIST, DT, TRACE_STEPS)
    
    # 2. Setup 3D Plot
    print("    Rendering Structure...")
    fig = plt.figure(figsize=(14, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Dark Void Theme
    ax.set_facecolor('black')
    ax.grid(False) 
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # 3. The "Sandcastle" Logic
    # We want to see the SHAPE of the high energy wake.
    # We flatten the trace array to a point cloud for volumetric feel
    
    # Filter: Drop points with very low velocity (The "Sand" on the floor)
    # This leaves only the "Castle" (The Wake Structure)
    
    pts_m = raw_traces[:, :, 0].flatten()
    pts_l = raw_traces[:, :, 1].flatten()
    pts_v = raw_traces[:, :, 2].flatten()
    pts_a = raw_traces[:, :, 3].flatten()
    
    # Filter mask: Height > 0.5 (Escape the floor)
    mask = pts_v > 0.5
    
    clean_m = pts_m[mask]
    clean_l = pts_l[mask]
    clean_v = pts_v[mask]
    clean_a = pts_a[mask]
    
    print(f"    Rendering {len(clean_m)} structural points...")
    
    # Scatter Plot
    # Color by ACCELERATION (pts_a)
    # Positive (Gold/White) = Still Accelerating
    # Negative (Purple/Dark) = Slowing Down
    
    sc = ax.scatter(
        clean_m, clean_l, clean_v,
        c=clean_a,
        cmap='twilight_shifted', # Good for +/- data. Center is dark, edges bright.
        s=1.5,                   # Small points for "Sand" effect
        alpha=0.6,
        vmin=-5.0, vmax=5.0      # Clamp acceleration range for contrast
    )
    
    # 4. Reference Floor
    # Optional: Plot the poles on the floor for orientation
    ax.scatter([0], [-1], [0], color='red', marker='x', s=200, label='Red Pole')
    ax.scatter([-0.866], [0.5], [0], color='cyan', marker='x', s=200, label='Teal Pole')

    # 5. Labels and View
    ax.set_xlabel('Mass Field (m)', color='gray')
    ax.set_ylabel('Coupling Field (λ)', color='gray')
    ax.set_zlabel('Velocity (Height)', color='gray')
    ax.set_title(f"The Vacuum Sandcastle: Velocity Structure\nColor = Acceleration (Gold=Gain, Purple=Loss)", color='white')
    
    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')
    ax.tick_params(axis='z', colors='gray')
    
    # Cinematic Angle
    ax.view_init(elev=25, azim=-60)
    
    # Colorbar
    cbar = plt.colorbar(sc, shrink=0.5, pad=0.1)
    cbar.set_label('Acceleration (Energy Gain/Loss)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    plt.tight_layout()
    filename = "vacuum_sandcastle_structure.png"
    plt.savefig(filename, dpi=200, facecolor='black')
    print(f"[+] Sandcastle Built: {filename}")
    plt.show()

if __name__ == "__main__":
    run_3d_analysis()