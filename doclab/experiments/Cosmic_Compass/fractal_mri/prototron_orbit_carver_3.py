import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from numba import jit

# ----------------------------------------
# 1. Active Force Dynamics (JIT Compiled)
# ----------------------------------------

@jit(nopython=True)
def get_basin_properties_jit(m, lam):
    """
    JIT-compiled version of the basin property logic.
    Calculates stiffness and parity modifiers based on angular position.
    """
    # Calculate angle in degrees
    angle = (np.degrees(np.arctan2(lam, m))) % 360
    
    # Gaussian weights for the three basins
    # We use direct scalar math for speed within the JIT context
    
    # Gold (Strong): ~30 deg
    diff_gold = np.abs(angle - 30)
    dist_gold = np.minimum(diff_gold, 360 - diff_gold)
    w_gold = np.exp(-(dist_gold/45)**2)
    
    # Teal (EM): ~150 deg
    diff_teal = np.abs(angle - 150)
    dist_teal = np.minimum(diff_teal, 360 - diff_teal)
    w_teal = np.exp(-(dist_teal/45)**2)
    
    # Red (Weak): ~270 deg
    diff_red = np.abs(angle - 270)
    dist_red = np.minimum(diff_red, 360 - diff_red)
    w_red = np.exp(-(dist_red/45)**2)
    
    total = w_gold + w_teal + w_red + 1e-6
    
    # Physics Modifiers
    k_strong = 1.0 + (w_gold * 0.5) 
    p_weak = w_red * 0.15 
    
    # Color mixing calculation
    r = (w_gold * 1.0 + w_red * 1.0) / total
    g = (w_gold * 0.8 + w_teal * 0.8 + w_red * 0.2) / total
    b = (w_teal * 0.8 + w_red * 0.2) / total
    
    return k_strong, p_weak, r, g, b

@jit(nopython=True)
def compute_trajectory(steps, dt, sigma, m_val, lam_val, pm_val, plam_val):
    """
    Runs the entire Leapfrog integration loop in compiled machine code.
    Pre-allocates arrays for maximum memory efficiency.
    """
    # Pre-allocate output arrays
    traj_m = np.zeros(steps)
    traj_lam = np.zeros(steps)
    traj_t = np.zeros(steps)
    colors = np.zeros((steps, 3))
    
    t = 0.0
    
    for i in range(steps):
        # 1. Record State & Color
        # We calculate properties for the CURRENT state before moving
        k_mod, p_mod, r, g, b = get_basin_properties_jit(m_val, lam_val)
        
        traj_m[i] = m_val
        traj_lam[i] = lam_val
        traj_t[i] = t
        colors[i, 0] = r
        colors[i, 1] = g
        colors[i, 2] = b
        
        # 2. Force Calculation (Half Step)
        Fm = -k_mod * m_val - 2.0 * sigma * m_val * lam_val
        Flam = -k_mod * lam_val - sigma * (m_val**2 - lam_val**2) + p_mod
        
        pm_half = pm_val + 0.5 * dt * Fm
        plam_half = plam_val + 0.5 * dt * Flam
        
        # 3. Position Update (Full Step)
        m_new = m_val + dt * pm_half
        lam_new = lam_val + dt * plam_half
        
        # 4. Force Calculation (New Position)
        # We must re-evaluate basin properties for the new force, 
        # but for Leapfrog we need the force at the new position.
        k_mod_new, p_mod_new, _, _, _ = get_basin_properties_jit(m_new, lam_new)
        
        Fm_new = -k_mod_new * m_new - 2.0 * sigma * m_new * lam_new
        Flam_new = -k_mod_new * lam_new - sigma * (m_new**2 - lam_new**2) + p_mod_new
        
        # 5. Momentum Update (Full Step)
        pm_val = pm_half + 0.5 * dt * Fm_new
        plam_val = plam_half + 0.5 * dt * Flam_new
        
        # Update state variables
        m_val = m_new
        lam_val = lam_new
        t += dt
        
    return traj_m, traj_lam, traj_t, colors

# ----------------------------------------
# 2. Main Execution
# ----------------------------------------

def run_spacetime_knot_optimized():
    # Parameters
    steps = 4000 
    dt = 0.015
    sigma = 1.0
    
    # Initial Conditions
    m_val = 0.0
    lam_val = 0.1
    pm_val = 0.45 
    plam_val = 0.2
    
    print("Compiling and Simulating Active Force Interactions...")
    # This call runs via Numba (CPU optimized)
    traj_m, traj_lam, traj_t, colors = compute_trajectory(
        steps, dt, sigma, m_val, lam_val, pm_val, plam_val
    )

    # ----------------------------------------
    # 3. Visualization: Optimized Line3DCollection
    # ----------------------------------------
    
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # Create segments for the collection
    # Reshape to (N, 1, 3) to allow concatenation into segments (N, 2, 3)
    points = np.array([traj_m, traj_lam, traj_t]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create the collection
    # Note: We use colors[:-1] because there is one fewer segment than there are points
    lc = Line3DCollection(segments, colors=colors[:-1], lw=1.5, alpha=0.8)
    
    ax.add_collection(lc)

    # Styling
    ax.set_xlabel('Mass Field (m)', color='white')
    ax.set_ylabel('Coupling Field (λ)', color='white')
    ax.set_zlabel('Time (t)', color='white')
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(0, steps * dt)
    
    # Hide grid and panes
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    
    # White axis ticks
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')

    plt.title("The Spacetime Knot (Optimized)\nParticle 'Strand' undergoing Phase Transitions", color='white', fontsize=14)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_spacetime_knot_optimized()