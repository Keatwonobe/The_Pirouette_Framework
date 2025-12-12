import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# --- Physics Engine ---
def potential(x, y, lam):
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1/3) * y**3)

def equations_of_motion(t, state, m, lam):
    x, y, px, py = state
    Fx = -x - 2 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)
    return [px / m, py / m, Fx, Fy]

# --- THE DECISION TREE VISUALIZER ---
def trace_decision_moments(theta_center, delta_theta, n_angles, m, lam, E, x0, y0):
    """
    Traces multiple nearby trajectories and identifies the moments where
    they diverge from each other - the "decision points" in phase space.
    
    Returns a list of trajectories with their decision tree structure.
    """
    
    V_start = potential(x0, y0, lam)
    if V_start > E:
        print("Starting position inaccessible at this energy.")
        return None
    
    p_mag = np.sqrt(2 * m * (E - V_start))
    
    # Generate cluster of angles around boundary
    thetas = np.linspace(theta_center - delta_theta, 
                        theta_center + delta_theta, 
                        n_angles)
    
    print(f"Tracing {n_angles} trajectories around θ={theta_center:.5f}")
    
    trajectories = []
    colors = []
    
    for i, theta in enumerate(thetas):
        print(f"  Trajectory {i+1}/{n_angles}...", end="")
        
        # Integrate with dense output to capture full path
        sol = solve_ivp(
            equations_of_motion,
            [0, 2000.0],
            [x0, y0, p_mag*np.cos(theta), p_mag*np.sin(theta)],
            args=(m, lam),
            method='DOP853',  # High-order method for smoothness
            dense_output=True,
            rtol=1e-9, atol=1e-12
        )
        
        # Sample trajectory at regular intervals
        t_samples = np.linspace(0, sol.t[-1], 1000)
        path = sol.sol(t_samples)
        
        x_path, y_path = path[0], path[1]
        
        # Determine exit
        r_final = np.sqrt(x_path[-1]**2 + y_path[-1]**2)
        if r_final > 5.0:
            angle_exit = np.arctan2(y_path[-1], x_path[-1]) % (2 * np.pi)
            exit_id = int(angle_exit // (2 * np.pi / 3)) + 1
        else:
            exit_id = 0
            
        # Color by exit
        color_map = {0: 'black', 1: 'red', 2: 'green', 3: 'blue'}
        colors.append(color_map[exit_id])
        
        trajectories.append({
            'theta': theta,
            'exit': exit_id,
            'x': x_path,
            'y': y_path,
            't': t_samples,
            'color': color_map[exit_id]
        })
        
        print(f" Exit {exit_id}")
    
    return trajectories

# --- DIVERGENCE ANALYSIS ---
def measure_trajectory_divergence(trajectories):
    """
    Computes pairwise distance between trajectories as function of time
    to identify when they separate (decision moments).
    """
    
    n_traj = len(trajectories)
    
    # Find shortest trajectory length for alignment
    min_len = min(len(traj['x']) for traj in trajectories)
    
    # Compute separation matrix over time
    times = trajectories[0]['t'][:min_len]
    separation_matrix = np.zeros((n_traj, n_traj, min_len))
    
    for i in range(n_traj):
        for j in range(i+1, n_traj):
            dx = trajectories[i]['x'][:min_len] - trajectories[j]['x'][:min_len]
            dy = trajectories[i]['y'][:min_len] - trajectories[j]['y'][:min_len]
            dist = np.sqrt(dx**2 + dy**2)
            separation_matrix[i, j, :] = dist
            separation_matrix[j, i, :] = dist
    
    # Find divergence onset for each pair
    divergence_times = np.zeros((n_traj, n_traj))
    
    threshold = 0.1  # When we consider them "separated"
    
    for i in range(n_traj):
        for j in range(i+1, n_traj):
            sep = separation_matrix[i, j, :]
            idx = np.where(sep > threshold)[0]
            if len(idx) > 0:
                divergence_times[i, j] = times[idx[0]]
                divergence_times[j, i] = times[idx[0]]
            else:
                divergence_times[i, j] = times[-1]
                divergence_times[j, i] = times[-1]
    
    return times, separation_matrix, divergence_times

# --- VISUALIZATION: THE PHASE PORTRAIT ---
def plot_decision_tree(trajectories, show_potential=True):
    """
    Plots all trajectories color-coded by exit, overlaid on potential surface.
    """
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Optional: Show potential background
    if show_potential:
        xx = np.linspace(-2, 2, 200)
        yy = np.linspace(-2, 2, 200)
        XX, YY = np.meshgrid(xx, yy)
        ZZ = potential(XX, YY, 1.0)
        
        ax.contourf(XX, YY, ZZ, levels=20, cmap='gray', alpha=0.3)
        ax.contour(XX, YY, ZZ, levels=[0.1667], colors='white', linewidths=2, linestyles='--')
    
    # Plot trajectories
    for traj in trajectories:
        ax.plot(traj['x'], traj['y'], color=traj['color'], alpha=0.6, linewidth=1.5)
    
    # Mark starting point
    ax.scatter([0], [0], s=200, c='yellow', edgecolors='black', linewidths=2, zorder=10, marker='*')
    
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_xlabel('x position')
    ax.set_ylabel('y position')
    ax.set_title('The Decision Tree: How Boundary Trajectories Diverge')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    
    plt.tight_layout()
    plt.show()

# --- VISUALIZATION: TEMPORAL DIVERGENCE ---
def plot_separation_dynamics(trajectories, times, separation_matrix):
    """
    Shows how trajectories separate over time - the temporal unfolding of chaos.
    """
    
    n_traj = len(trajectories)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # 1. Pairwise Separation Over Time
    for i in range(n_traj):
        for j in range(i+1, n_traj):
            sep = separation_matrix[i, j, :]
            
            # Color by whether they end in same basin
            same_basin = (trajectories[i]['exit'] == trajectories[j]['exit'])
            color = 'gray' if same_basin else 'red'
            alpha = 0.2 if same_basin else 0.8
            linewidth = 0.5 if same_basin else 1.5
            
            ax1.plot(times, sep, color=color, alpha=alpha, linewidth=linewidth)
    
    ax1.set_yscale('log')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Trajectory Separation')
    ax1.set_title('Divergence Dynamics (Red = Different Exits, Gray = Same Exit)')
    ax1.grid(True, alpha=0.3)
    
    # 2. Mean Separation by Exit Group
    exit_groups = {}
    for traj in trajectories:
        ex = traj['exit']
        if ex not in exit_groups:
            exit_groups[ex] = []
        exit_groups[ex].append(traj)
    
    # For each exit group, compute internal vs external separation
    for exit_id, group in exit_groups.items():
        if len(group) < 2:
            continue
            
        # Internal separation (within group)
        internal_seps = []
        for i, traj_i in enumerate(group):
            for traj_j in group[i+1:]:
                idx_i = trajectories.index(traj_i)
                idx_j = trajectories.index(traj_j)
                internal_seps.append(separation_matrix[idx_i, idx_j, :])
        
        if internal_seps:
            mean_internal = np.mean(internal_seps, axis=0)
            color_map = {0: 'black', 1: 'red', 2: 'green', 3: 'blue'}
            ax2.plot(times, mean_internal, color=color_map[exit_id], 
                    linewidth=2, label=f'Exit {exit_id} (Internal)')
    
    ax2.set_yscale('log')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Mean Separation')
    ax2.set_title('How Quickly Do Basin Siblings Separate?')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# --- EXECUTION ---
if __name__ == "__main__":
    MASS = 1.0
    LAMBDA = 1.0
    E_SADDLE = 1.0 / (6.0 * LAMBDA**2)
    ENERGY = E_SADDLE + 0.01
    
    print("="*60)
    print("DECISION TREE VISUALIZER")
    print("Watching trajectories diverge at the fractal boundary")
    print("="*60)
    print()
    
    # Focus on your discovered spike
    THETA_CENTER = 3.173
    DELTA_THETA = 0.01  # Small window to see fractal structure
    N_TRAJECTORIES = 20  # Number of test angles
    
    # 1. Trace the trajectories
    trajectories = trace_decision_moments(
        THETA_CENTER, DELTA_THETA, N_TRAJECTORIES,
        MASS, LAMBDA, ENERGY, 0.0, 0.0
    )
    
    if trajectories is None:
        exit()
    
    print("\nAnalyzing divergence patterns...")
    times, sep_matrix, div_times = measure_trajectory_divergence(trajectories)
    
    # 2. Visualize phase space
    print("\nGenerating Phase Portrait...")
    plot_decision_tree(trajectories, show_potential=True)
    
    # 3. Visualize temporal dynamics
    print("\nGenerating Temporal Analysis...")
    plot_separation_dynamics(trajectories, times, sep_matrix)
    
    print("\nDone. The fractal reveals itself in time.")