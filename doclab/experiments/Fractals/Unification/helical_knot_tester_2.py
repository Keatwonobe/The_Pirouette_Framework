import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev

# ==========================================================
#  The Helical Knot Solver: Active Travelers
# ==========================================================

# --- Configuration ---
N_TRAVELERS = 3          # 3 is the magic number for chaotic knots (3-body problem)
R_BOUNDARY  = 20.0       # The "Arena" size
DT          = 0.005      # Finer time step for high-speed periapsis
STEPS       = 40000      # Long simulation to let the knot evolve

# --- Physics Constants ---
K_ATTRACT    = 50.0      # Strong Mutual Gravity (The "Desire" to merge)
K_CENTER     = 0.8       # Weak Centering Force (Keeps the fight in the middle)
DRIVE_FORCE  = 1.5       # Constant Self-Acceleration (The "Engine")
DRAG_COEFF   = 0.02      # Slight drag to prevent infinite energy explosion
SOFTENING    = 0.8       # Prevents divide-by-zero explosions at collision

# --- Core Analysis ---
R_CORE       = 4.0       # The radius defining "The Knot" (The Middle)

def init_travelers():
    """
    Initialize travelers on the periphery with high tangential velocity
    to ensure they spiral in rather than crashing directly.
    """
    angles = np.linspace(0, 2*np.pi, N_TRAVELERS, endpoint=False)
    pos = []
    vel = []
    
    for theta in angles:
        # Start at boundary
        p = np.array([R_BOUNDARY * np.cos(theta), R_BOUNDARY * np.sin(theta)])
        
        # Velocity tangent to circle (counter-clockwise)
        # We give them a push so they start with angular momentum
        v_dir = np.array([-np.sin(theta), np.cos(theta)])
        v = v_dir * 2.0 
        
        pos.append(p)
        vel.append(v)
        
    return np.array(pos), np.array(vel)

def get_forces(pos, vel):
    """
    Calculates the net force on each traveler:
    1. Mutual Attraction (Gravity)
    2. Central Tether (Bowl)
    3. Self-Propulsion (Drive)
    4. Drag (Atmosphere)
    """
    forces = np.zeros_like(pos)
    
    for i in range(N_TRAVELERS):
        p_i = pos[i]
        v_i = vel[i]
        
        # 1. Central Tether (Weak spring to origin)
        dist_center = np.linalg.norm(p_i)
        f_center = -K_CENTER * p_i / (dist_center + 0.1)
        forces[i] += f_center
        
        # 2. Self-Propulsion (Drive in direction of motion)
        speed = np.linalg.norm(v_i)
        if speed > 0.001:
            v_hat = v_i / speed
            f_drive = v_hat * DRIVE_FORCE
            forces[i] += f_drive
            
        # 3. Atmospheric Drag (Limits max speed)
        f_drag = -DRAG_COEFF * v_i * speed # Quadratic drag
        forces[i] += f_drag
        
        # 4. Mutual Attraction (The Knot Maker)
        for j in range(N_TRAVELERS):
            if i == j: continue
            
            p_j = pos[j]
            r_vec = p_j - p_i
            r_dist = np.linalg.norm(r_vec)
            
            # Gravity with Softening to prevent singularity
            f_gravity = (K_ATTRACT * r_vec) / (r_dist**2 + SOFTENING**2)**(1.5)
            forces[i] += f_gravity
            
    return forces

def run_solver():
    pos, vel = init_travelers()
    
    # History containers
    traj_history = []  # Full path
    core_history = []  # Only points inside R_CORE
    
    print(f"[*] Simulating {N_TRAVELERS} Active Travelers for {STEPS} steps...")
    
    for _ in range(STEPS):
        # Physics Step (Semi-Implicit Euler is stable enough here)
        forces = get_forces(pos, vel)
        vel += forces * DT
        pos += vel * DT
        
        # Store Data
        traj_history.append(pos.copy())
        
        # Check if ALL travelers are inside the Core (The Knot)
        # Or if we just want to track their path through the middle
        dists = np.linalg.norm(pos, axis=1)
        if np.all(dists < R_CORE):
            core_history.append(pos.copy())
            
    return np.array(traj_history), np.array(core_history)

def plot_knot(traj, core):
    """
    Visualizes the result with a focus on the central knot.
    """
    fig = plt.figure(figsize=(14, 6))
    
    # --- Plot 1: The Arena (Full Context) ---
    ax1 = fig.add_subplot(1, 2, 1)
    
    # Plot faint boundary
    boundary = plt.Circle((0, 0), R_BOUNDARY, color='gray', fill=False, ls='--', alpha=0.3)
    ax1.add_artist(boundary)
    
    # Plot Core Zone
    core_zone = plt.Circle((0, 0), R_CORE, color='red', fill=False, ls=':', alpha=0.5, label='Knot Core')
    ax1.add_artist(core_zone)
    
    colors = plt.cm.plasma(np.linspace(0, 1, N_TRAVELERS))
    
    for i in range(N_TRAVELERS):
        # Plot full trajectory faint
        ax1.plot(traj[:, i, 0], traj[:, i, 1], color=colors[i], alpha=0.2, lw=0.5)
        # Plot end point
        ax1.scatter(traj[-1, i, 0], traj[-1, i, 1], color=colors[i], s=50, edgecolors='white')

    ax1.set_title(f"The Arena\n(Drive={DRIVE_FORCE}, Attraction={K_ATTRACT})")
    ax1.set_aspect('equal')
    ax1.legend()

    # --- Plot 2: The Knot (Zoomed Core) ---
    ax2 = fig.add_subplot(1, 2, 2)
    
    if len(core) > 10:
        # We only plot the segments of history that happened INSIDE the core
        print(f"[*] Knot Density: {len(core)} interaction frames captured in core.")
        
        for i in range(N_TRAVELERS):
            # We scatter the core points to see the geometry better than a messy line
            ax2.plot(core[:, i, 0], core[:, i, 1], color=colors[i], alpha=0.6, lw=1.0)
            
        ax2.set_title("The Solved Knot (Central Interaction)")
    else:
        ax2.text(0, 0, "No Tight Knot Formed\n(Increase Attraction or Steps)", ha='center')
        ax2.set_title("The Solved Knot")
        
    ax2.set_xlim(-R_CORE, R_CORE)
    ax2.set_ylim(-R_CORE, R_CORE)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig('helical_knot_solution.png')
    print("[*] Saved visualization to 'helical_knot_solution.png'")
    plt.show()

if __name__ == "__main__":
    traj_data, core_data = run_solver()
    plot_knot(traj_data, core_data)