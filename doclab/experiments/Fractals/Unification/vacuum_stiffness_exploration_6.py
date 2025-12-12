import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import njit, prange
import math

# ============================================================
# CONFIGURATION: 3D VELOCITY MANIFOLD
# ============================================================
RES = 800             # Resolution for the floor map
PARTICLE_COUNT = 3000 # Number of tracers for 3D visualization
TRACE_STEPS = 300     # Length of the "time" tail

# The South-West Eddy (The Source)
CENTER_M = -0.6      
CENTER_L = -0.8
ZOOM_WIDTH = 8      

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
# 2. SOLVERS (RK2 & TRACER)
# ============================================================

@njit(fastmath=True)
def rk2_step(m, l, twist, dt):
    fm1, fl1 = get_physics_components(m, l, twist)
    m_pred = m + fm1 * dt
    l_pred = l + fl1 * dt
    fm2, fl2 = get_physics_components(m_pred, l_pred, twist)
    m_new = m + (fm1 + fm2) * 0.5 * dt
    l_new = l + (fl1 + fl2) * 0.5 * dt
    
    # Calculate Velocity Magnitude for Z-Axis
    # We use the velocity at the NEW point
    fm_new, fl_new = get_physics_components(m_new, l_new, twist)
    vel_mag = math.sqrt(fm_new*fm_new + fl_new*fl_new)
    
    return m_new, l_new, vel_mag

@njit(parallel=True)
def generate_3d_traces(center_m, center_l, width, count, twist, dt, steps):
    """
    Returns traces of shape (count, steps, 3)
    Where dim 3 is [m, lambda, velocity]
    """
    traces = np.zeros((count, steps, 3), dtype=np.float64)
    
    side = int(math.sqrt(count))
    start_step = width / side
    min_m = center_m - width/2
    min_l = center_l - width/2
    
    idx = 0
    # Serial loop for setup, parallel logic handled inside if needed, 
    # but for N=3000 serial is instant. Numba handles it well.
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
            
            for t in range(1, steps):
                curr_m, curr_l, vel = rk2_step(curr_m, curr_l, twist, dt)
                traces[idx, t, 0] = curr_m
                traces[idx, t, 1] = curr_l
                traces[idx, t, 2] = vel
                
            idx += 1
    return traces

# ============================================================
# 3. 3D VISUALIZATION
# ============================================================

def run_3d_analysis():
    print(f"[-] Calculating 3D Velocity Wake...")
    print(f"    Target: ({CENTER_M}, {CENTER_L})")
    
    # 1. Generate Traces
    traces = generate_3d_traces(CENTER_M, CENTER_L, ZOOM_WIDTH, PARTICLE_COUNT, TWIST, DT, TRACE_STEPS)
    
    # 2. Setup 3D Plot
    print("    Rendering 3D Manifold...")
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Aesthetic Settings
    ax.set_facecolor('black')
    ax.grid(False) 
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # 3. Plot Traces
    # We plot the lines to show the "Wake"
    # To save rendering time, we plot a subset of lines, but all termination points
    
    # A. The Lines (The "Upward" Trajectory)
    # Color by Z-height (Speed) using a colormap
    
    print("    Drawing Trajectories...")
    subset = 500 # Plot 500 lines for clarity
    for i in range(min(subset, len(traces))):
        x = traces[i, :, 0]
        y = traces[i, :, 1]
        z = traces[i, :, 2] # Velocity
        
        # Color line by its final velocity (simple approximation for gradient)
        # For true gradient lines we need LineCollection3D, but simple plot is faster/easier here
        ax.plot(x, y, z, color=plt.cm.magma(z[-1]/4.0), alpha=0.3, linewidth=0.5)

    # B. The Terminations (The "Farthest Flung")
    # We plot the final point of ALL particles
    print("    Placing Termination Points...")
    final_x = traces[:, -1, 0]
    final_y = traces[:, -1, 1]
    final_z = traces[:, -1, 2]
    
    sc = ax.scatter(final_x, final_y, final_z, c=final_z, cmap='afmhot', s=2, alpha=0.8, depthshade=False)
    
    # 4. Labels and View
    ax.set_xlabel('Mass Field (m)', color='white')
    ax.set_ylabel('Coupling Field (λ)', color='white')
    ax.set_zlabel('Velocity / Kinetic Energy', color='white')
    ax.set_title(f"3D Velocity Wake: The Traveler's Shape\n(Height = Speed)", color='white')
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')
    
    # Side-on View (Low Elevation)
    ax.view_init(elev=20, azim=-45)
    
    # Colorbar
    cbar = plt.colorbar(sc, shrink=0.5, pad=0.1)
    cbar.set_label('Terminal Velocity', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    plt.tight_layout()
    filename = "vacuum_3d_velocity_wake.png"
    plt.savefig(filename, dpi=200, facecolor='black')
    print(f"[+] 3D Render saved to {filename}")
    plt.show()

if __name__ == "__main__":
    run_3d_analysis()