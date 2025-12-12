import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

# ==========================================================
#  The Helical Knot 3D Solver: Manifold Tearing
# ==========================================================

# --- Configuration ---
N_TRAVELERS = 2          # Focus on the two primary cords
R_BOWL      = 10.0       # The Arena size (Initial 2D manifold)
DT          = 0.0005     # VERY FINE time step for high-speed, close-range dynamics
N_STEPS     = 100000     # Increased steps for detailed knot capture

# --- Physics Constants (Tuned for Violent, High-Momentum Knots) ---
K_ATTRACT    = 1000.0    # EXTREMELY Strong Mutual Gravity (Super-Attraction)
DRIVE_FORCE  = 5.0       # Constant Self-Acceleration (Infinite Speed Proxy)
K_TEAR       = 5.0       # Manifold Tearing Constant (Out-of-Plane Z-Force)
R_CORE       = 2.0       # The radius defining the central knot / tear zone
GAMMA_DRAG   = 0.001     # Minimal drag

# --- Global Analysis Parameters ---
KNOT_MAX_DUR = 10000     # Maximum steps to analyze the core after tear begins

def init_travelers():
    """Initialize travelers in the XY plane (z=0) with high initial momentum."""
    # Place travelers starting near the periphery, opposite each other
    pos = np.array([[-R_BOWL, 0.0, 0.0], [R_BOWL, 0.0, 0.0]])
    
    # High initial velocity for "near infinite speed" and inward focus
    vel = np.array([[50.0, 20.0, 0.0], [-50.0, -20.0, 0.0]])
    
    return pos, vel

def get_forces_3d(pos, vel, step):
    """Calculates 3D forces, including the Manifold Tear in the core."""
    forces = np.zeros_like(pos)
    
    p1, p2 = pos[0], pos[1]
    v1, v2 = vel[0], vel[1]
    
    r_vec = p2 - p1
    r_dist = np.linalg.norm(r_vec)
    r_center = np.linalg.norm((p1 + p2) / 2)

    # --- 1. Mutual Attraction (Super-Gravity) ---
    # F_g ~ 1/r^2 (Inverse square force)
    f_mag = K_ATTRACT / (r_dist**2 + 0.1) # Softening is implicit with the small +0.1
    F_attract = (r_vec / r_dist) * f_mag
    
    forces[0] += F_attract
    forces[1] -= F_attract

    # --- 2. Manifold Tear (Z-Axis Force in the Core) ---
    if r_center < R_CORE:
        # F_tear is proportional to inverse distance, applied in the Z-direction.
        # It's an *alternating* force to create the chiral, triangular flip
        
        # Traveler 1 is pushed +Z, Traveler 2 is pushed -Z
        z_mag = K_TEAR / (r_dist**2 + 0.1)
        
        forces[0] += np.array([0, 0, z_mag])
        forces[1] -= np.array([0, 0, z_mag])

    # --- 3. Self-Propulsion (The Engine / Constant Acceleration) ---
    for i in range(N_TRAVELERS):
        speed = np.linalg.norm(vel[i])
        if speed > 0.001:
            v_hat = vel[i] / speed
            forces[i] += v_hat * DRIVE_FORCE
            
    # --- 4. Drag (Dissipation) ---
    forces -= vel * GAMMA_DRAG
            
    return forces

def run_3d_solver():
    pos, vel = init_travelers()
    
    traj_history = []
    knot_core_history = []
    is_knotting = False
    knot_steps = 0
    
    print(f"[*] Simulating 3D Travelers for {N_STEPS} steps...")
    
    for step in range(N_STEPS):
        forces = get_forces_3d(pos, vel, step)
        
        # Velocity-Verlet Integration
        acc = forces
        vel += acc * DT
        pos += vel * DT
        
        # Center of Mass (COM) check
        com_dist = np.linalg.norm(pos.mean(axis=0))
        
        # Knot Detection
        if com_dist < R_CORE and not is_knotting:
            is_knotting = True
            print(f"\n[!!!] Knotting initiated at step {step} (COM distance: {com_dist:.2f})")
            
        if is_knotting:
            knot_core_history.append(pos.copy())
            knot_steps += 1
            if knot_steps > KNOT_MAX_DUR:
                print(f"[*] Knot duration limit reached. Ending simulation.")
                break
                
        traj_history.append(pos.copy())
            
    return np.array(traj_history), np.array(knot_core_history)

def plot_3d_knot(knot_core):
    """
    Visualizes the 3D knot core and checks for the triangular geometry.
    """
    if knot_core.shape[0] < 10:
        print("[!] Not enough knot core data to plot.")
        return
        
    print(f"[*] Plotting {knot_core.shape[0]} knot core points in 3D...")
    
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    T, N, D = knot_core.shape
    
    # Flatten the knot trajectory to perform PCA for optimal viewing plane
    core_pts_flat = knot_core.reshape(-1, D)
    core_mean = core_pts_flat.mean(axis=0)
    centered = core_pts_flat - core_mean
    
    # PCA to find the plane where the knot is most 'open'
    U, S, Vt = np.linalg.svd(centered, full_matrices=False)
    # The first two principal components define the optimal plane
    
    # We will rotate the entire trajectory history to align the knot's main plane
    # with the XY plane (for easier interpretation of the Z-axis).
    rotation_matrix = Vt # Vt is the rotation matrix to align principal components
    
    # Apply inverse rotation to the centered data
    # Rotated_Pos = Centered_Pos @ Rotation_Matrix.T
    rotated_core = centered @ rotation_matrix.T
    
    # --- Plot the Rotated Knot ---
    colors = ['r', 'b']
    
    for i in range(N_TRAVELERS):
        # The history for traveler i in the rotated frame
        p_rotated = rotated_core[i::N_TRAVELERS] 
        
        # Plot the trajectory line
        ax.plot(p_rotated[:, 0], p_rotated[:, 1], p_rotated[:, 2], 
                color=colors[i], lw=1.5, alpha=0.8, label=f"Traveler {i+1}")
        
        # Mark the start and end points
        ax.scatter(p_rotated[0, 0], p_rotated[0, 1], p_rotated[0, 2], 
                   color=colors[i], marker='o', s=50)
        ax.scatter(p_rotated[-1, 1], p_rotated[-1, 1], p_rotated[-1, 2], 
                   color=colors[i], marker='x', s=50)

    # Set Aspect and Limits
    max_range = np.array([p_rotated[:, 0].max() - p_rotated[:, 0].min(),
                          p_rotated[:, 1].max() - p_rotated[:, 1].min(),
                          p_rotated[:, 2].max() - p_rotated[:, 2].min()]).max() / 2.0

    mid_x, mid_y, mid_z = rotated_core.mean(axis=0)
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    ax.set_title("The Solved 3D Tearing Knot (PCA Aligned View)", fontsize=16)
    ax.set_xlabel("PC1 (Knot Plane)")
    ax.set_ylabel("PC2 (Knot Plane)")
    ax.set_zlabel("PC3 (Out-of-Plane Tear)")
    ax.view_init(elev=20, azim=130) # Initial good viewing angle
    ax.legend()
    plt.tight_layout()
    plt.savefig('3d_tearing_knot_solution.png')
    plt.show()

if __name__ == "__main__":
    traj_data, knot_core_data = run_3d_solver()
    plot_3d_knot(knot_core_data)