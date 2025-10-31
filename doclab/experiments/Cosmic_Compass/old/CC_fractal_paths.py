import numpy as np
import matplotlib.pyplot as plt
from numba import jit

# Using the detailed lattice generator from before
@jit(nopython=True)
def compute_attractor_lattice_detailed(gamma_vals, ta_vals, max_iters, escape_radius):
    height, width = len(ta_vals), len(gamma_vals)
    exterior = np.zeros((height, width))
    interior = np.zeros((height, width))
    alpha = 4 * np.pi / 3

    for i in range(height):
        for j in range(width):
            c = gamma_vals[j] + 1j * ta_vals[i]
            z = 0 + 0j
            for n in range(max_iters):
                if np.abs(z) > escape_radius:
                    exterior[i, j] = n - np.log2(np.log2(np.abs(z))) + 4.0
                    break
                z = alpha * np.sin(z) + c
            else:
                exterior[i, j] = 0
                interior[i, j] = np.abs(z)
    return exterior, interior

# --- 3. Path Integration (Trajectory Projection) ---
def project_trajectory(start_gamma, start_ta, num_steps, step_size, force_gamma, force_ta, gamma_ax, ta_ax):
    """Calculates the path of a system on the potential field."""
    path = [(start_gamma, start_ta)]
    current_gamma, current_ta = start_gamma, start_ta

    for _ in range(num_steps):
        # Find the closest grid indices for the current position
        j = np.argmin(np.abs(gamma_ax - current_gamma))
        i = np.argmin(np.abs(ta_ax - current_ta))

        # Get the force vector at that grid point
        fg = force_gamma[i, j]
        ft = force_ta[i, j]

        # Update the position along the force vector
        current_gamma += step_size * fg
        current_ta += step_size * ft
        
        # Stop if the path goes out of bounds
        if not (gamma_ax.min() < current_gamma < gamma_ax.max() and \
                ta_ax.min() < current_ta < ta_ax.max()):
            break
            
        path.append((current_gamma, current_ta))
        
    return np.array(path)

# --- 1. Generate the Lattice and its Potential Field ---
resolution = 1000
gamma_range = (2.0, 3.0)
ta_range = (-0.5, 0.5)
max_iterations = 200

gamma_ax = np.linspace(gamma_range[0], gamma_range[1], resolution)
ta_ax = np.linspace(ta_range[0], ta_range[1], resolution)

print("Generating the detailed lattice...")
exterior_data, interior_data = compute_attractor_lattice_detailed(gamma_ax, ta_ax, max_iterations, 10.0)

# Create a single, continuous potential field V
# Stable interiors are deep wells (negative potential)
# Chaotic exterior is a high plateau (positive potential)
potential_field = np.zeros_like(exterior_data)
interior_mask = (exterior_data == 0)
potential_field[interior_mask] = -1.0 + (interior_data[interior_mask] / interior_data[interior_mask].max())
potential_field[~interior_mask] = exterior_data[~interior_mask] / exterior_data[~interior_mask].max()

# --- 2. Calculate the Gradient (The 'Force Field') ---
print("Calculating the force field...")
dT, dG = np.gradient(potential_field)
force_gamma = -dG
force_ta = -dT

# Normalize the force vectors for more stable path integration
magnitude = np.sqrt(force_gamma**2 + force_ta**2)
# Avoid division by zero
magnitude[magnitude == 0] = 1.0
force_gamma /= magnitude
force_ta /= magnitude

# --- 4. Simulation and Visualization ---
print("Projecting system trajectories...")

# Define several starting points to test different outcomes
start_points = {
    "A: Unstable Precipice": (2.2, 0),
    "B: The Filament Bridge": (2.4, 0),
    "C: Chaotic Drift": (2.6, 0),
    "D: Edge of Chaos": (2.8, 0)
}

# Simulate the trajectory for each starting point
trajectories = {}
for name, start_pos in start_points.items():
    path = project_trajectory(start_pos[0], start_pos[1], 
                              num_steps=500, step_size=0.03,
                              force_gamma=force_gamma, force_ta=force_ta,
                              gamma_ax=gamma_ax, ta_ax=ta_ax)
    trajectories[name] = path

# --- Plotting the Final Map ---
fig, ax = plt.subplots(figsize=(12, 12))
ax.imshow(potential_field, extent=[gamma_range[0], gamma_range[1], ta_range[0], ta_range[1]], 
          cmap='viridis', origin='lower')

# Plot each trajectory
colors = ['#FF6B6B', '#4D96FF', '#6BCB77', '#FFD93D']
for i, (name, path) in enumerate(trajectories.items()):
    ax.plot(path[:, 0], path[:, 1], color=colors[i], lw=2.5)
    # Plot start point and an arrow showing direction
    ax.scatter(path[0, 0], path[0, 1], color='white', s=150, zorder=5, ec='black', marker='o')
    ax.text(path[0, 0] + 0.1, path[0, 1] + 0.1, name, color='white', fontsize=12, ha='left')

ax.set_title("State Space Projector: Predicting System Outcomes on the Lattice", fontsize=16)
ax.set_xlabel("Γ (Temporal Complexity)", fontsize=12)
ax.set_ylabel("$T_a$ (Temporal Coherence)", fontsize=12)
ax.set_xlim(gamma_range)
ax.set_ylim(ta_range)
plt.savefig("state_space_projections.png", dpi=300, bbox_inches='tight')
plt.show()