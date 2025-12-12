import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================================
# Dynamic Spiral Potential Solver V3: Non-Symmetric Wake
# ==========================================================

# --- Configuration (Kept for tight zoom) ---
N_TRAVELERS = 2          
R_BOWL      = 10.0       
DT          = 0.0001     # Smaller time step for high-fidelity force
N_STEPS     = 200000     # Increased steps for capturing multiple spirals

# --- Physics Constants (Tuned for Dynamic Potential) ---
K_SHRINK     = 100.0     # Shrinking/Attractive Potential Factor (Retrograde)
K_STRETCH    = 100.0     # Stretching/Repulsive Potential Factor (Forward)
DRIVE_FORCE  = 1.0       # Minimal forward engine drive
K_TEAR       = 50.0      # Manifold Tear (Z-flip) - stronger now
R_CORE       = 2.0       # Radius where we start recording the knot
GAMMA_DRAG   = 0.005     # Minimal drag

# --- Initial Conditions ---
# Traveler 1: Forward (Red), Traveler 2: Retrograde (Blue)
def init_travelers():
    # Start opposite sides
    pos = np.array([[-R_BOWL, 0.0, 0.0], [R_BOWL, 0.0, 0.0]])
    
    # Velocity: High but not too high, to allow capture.
    # The sign of the initial velocity dictates FORWARD/RETROGRADE nature.
    V_MAG = 15.0 
    
    # T1 (Forward/Stretching): +X velocity (outward sweep)
    # T2 (Retrograde/Shrinking): -X velocity (inward pull)
    vel = np.array([[V_MAG, 2.0, 0.0], [-V_MAG, -2.0, 0.0]])
    
    # Store the potential type (1: Forward/Stretching, 2: Retrograde/Shrinking)
    potential_type = np.array([1, 2])
    
    return pos, vel, potential_type

def get_dynamic_forces_3d(pos, vel, potential_type):
    """
    Calculates 3D forces based on dynamic, non-symmetric potential.
    """
    forces = np.zeros_like(pos)
    
    p1, p2 = pos[0], pos[1]
    v1, v2 = vel[0], vel[1]
    
    r_vec = p2 - p1
    r_dist = np.linalg.norm(r_vec)
    r_center = np.linalg.norm((p1 + p2) / 2)
    r_safe = max(r_dist, 0.1) # Softening length

    # -----------------------------------------------------------------
    # 1. Dynamic Spiral Potential (Non-Symmetric Wake)
    # -----------------------------------------------------------------

    # Force ON T1 (Forward/Stretching) due to T2 (Retrograde/Shrinking)
    # T2 is Retrograde (Shrinking), which PULLS T1 towards it.
    G_eff_1 = K_SHRINK * np.linalg.norm(v2) 
    
    F_1_mag = G_eff_1 / (r_safe**2) 
    F_1_on_2 = (r_vec / r_safe) * F_1_mag # T1 is pulled toward T2
    
    forces[0] += F_1_on_2

    # Force ON T2 (Retrograde/Shrinking) due to T1 (Forward/Stretching)
    # T1 is Forward (Stretching), which PUSHES T2 AWAY from it.
    G_eff_2 = -K_STRETCH * np.linalg.norm(v1) # Negative G_eff for Repulsion
    
    F_2_mag = abs(G_eff_2) / (r_safe**2) 
    F_2_on_1 = (r_vec / r_safe) * F_2_mag # T2 is pushed away from T1
    
    # F_2_on_1 is the magnitude of repulsion. We apply it in the -r_vec direction
    forces[1] -= F_2_on_1

    # --- 2. Manifold Tear (Z-Axis Force in the Core) ---
    if r_center < R_CORE:
        # Simple alternating pressure based on inverse distance
        z_mag = K_TEAR / (r_safe**2)
        
        # T1 (Forward) is pushed +Z, T2 (Retrograde) is pushed -Z
        forces[0] += np.array([0, 0, z_mag])
        forces[1] -= np.array([0, 0, z_mag])

    # --- 3. Self-Propulsion and Drag ---
    for i in range(N_TRAVELERS):
        # Constant Drive: Propels them forward in their current direction
        speed = np.linalg.norm(vel[i])
        if speed > 0.001:
            v_hat = vel[i] / speed
            forces[i] += v_hat * DRIVE_FORCE
            
    # Drag: Dissipation
    forces -= vel * GAMMA_DRAG
            
    return forces

def run_3d_solver():
    pos, vel, potential_type = init_travelers()
    
    knot_core_history = []
    
    print(f"[*] Simulating Dynamic Spiral Potential for {N_STEPS} steps...")
    
    for step in range(N_STEPS):
        forces = get_dynamic_forces_3d(pos, vel, potential_type)
        
        # Integration
        vel += forces * DT
        pos += vel * DT
        
        # Record only if we are in the "Knot Zone"
        if np.linalg.norm(pos[0]) < R_CORE and np.linalg.norm(pos[1]) < R_CORE:
            knot_core_history.append(pos.copy())
            
        # Stop condition: if they escape the universe boundary
        if np.linalg.norm(pos[0]) > R_BOWL * 3 or np.linalg.norm(pos[1]) > R_BOWL * 3:
            print(f"[*] Travelers escaped the region at step {step}. Ending simulation.")
            break
            
    return np.array(knot_core_history)

def plot_zoomed_knot(knot_core):

        
    print(f"[*] Analyzing {knot_core.shape[0]} dynamic interaction frames...")
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    t1 = knot_core[:, 0, :]
    t2 = knot_core[:, 1, :]
    
    # --- Plot the Trajectories ---
    for i in range(0, len(t1)-1, 1):
        # T1 (Forward/Stretching) - Red/Orange
        ax.plot(t1[i:i+2, 0], t1[i:i+2, 1], t1[i:i+2, 2], 
                color=plt.cm.autumn(i/len(t1)), lw=1.5, alpha=0.9)
        # T2 (Retrograde/Shrinking) - Blue/Cyan
        ax.plot(t2[i:i+2, 0], t2[i:i+2, 1], t2[i:i+2, 2], 
                color=plt.cm.winter(i/len(t2)), lw=1.5, alpha=0.9)

    # --- AUTO-ZOOM ---
    all_pts = np.vstack([t1, t2])
    max_range = np.abs(all_pts).max() * 1.1 # Add 10% padding
    
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)
    
    ax.set_title(f"Dynamic Spiral Potential Knot | Max Range: {max_range:.2f}", fontsize=15)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z (Tear Height)")
    
    ax.view_init(elev=40, azim=40)
    
    plt.tight_layout()
    plt.savefig('dynamic_spiral_potential_knot.png')
    print("[*] Zoomed dynamic solution saved to 'dynamic_spiral_potential_knot.png'")
    plt.show()

if __name__ == "__main__":
    knot_data = run_3d_solver()
    plot_zoomed_knot(knot_data)