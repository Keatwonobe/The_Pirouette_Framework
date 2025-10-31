import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class ResonanceCavity:
    """
    Represents a single 'diorama' or simulation space.
    It contains entities and the potential fields that govern their motion.
    """
    def __init__(self, initial_pos, initial_ta=1.0, initial_gamma=1.0):
        # State Vectors
        self.position = np.array(initial_pos, dtype=float)
        self.velocity = np.array([0.0, 0.0])
        
        # Pirouette Coordinates
        self.Ta = initial_ta    # Time-Adherence (speed of time)
        self.Gamma = initial_gamma # Gladiator Force (boundary strength)
        
        # Modular list of potential-generating functions
        self.potential_sources = []
        self.history = [self.position.copy()]

    def add_potential(self, potential_func):
        """Adds a new 'dimension' or force to the simulation."""
        self.potential_sources.append(potential_func)

    def get_total_force(self):
        """Calculates the total force by summing the gradients of all potentials."""
        # A small step 'epsilon' for calculating the gradient numerically
        eps = 1e-5
        
        total_force = np.array([0.0, 0.0])
        
        for source in self.potential_sources:
            # Calculate gradient (slope) for the potential source
            grad_x = (source(self.position + [eps, 0]) - source(self.position - [eps, 0])) / (2 * eps)
            grad_y = (source(self.position + [0, eps]) - source(self.position - [0, eps])) / (2 * eps)
            
            # The force is the negative gradient ("rolling downhill")
            total_force += -np.array([grad_x, grad_y])
            
        return total_force

    def step(self, dt):
        """Evolves the simulation forward by one time step."""
        force = self.get_total_force()
        
        # Update velocity and position (simplified Euler integration)
        # Note: The effective change is scaled by Time-Adherence (Ta)
        acceleration = force # Assume mass = 1 for simplicity
        self.velocity += acceleration * dt * self.Ta
        self.position += self.velocity * dt * self.Ta
        
        self.history.append(self.position.copy())

# --- Define some modular potential functions ---

def create_gravity_well(center, strength):
    """Models a physical depression, like a valley."""
    def potential(pos):
        dist_sq = np.sum((pos - center)**2)
        return -strength / (1 + dist_sq)
    return potential

def create_desire_attractor(target, strength, peak_dist=0.5):
    """Models desire: increases as you approach, then falls off sharply."""
    def potential(pos):
        dist = np.linalg.norm(pos - target)
        # A function that peaks at 'peak_dist'
        return -strength * np.exp(-(dist - peak_dist)**2 / (2 * peak_dist**2))
    return potential

# --- Setup the Simulation "Senate" ---
num_dioramas = 3
dioramas = []

# Diorama 1: Strong gravity, weak desire
cavity1 = ResonanceCavity(initial_pos=[-2.0, 2.5])
cavity1.add_potential(create_gravity_well(center=np.array([0.0, 0.0]), strength=5.0))
cavity1.add_potential(create_desire_attractor(target=np.array([2.0, -2.0]), strength=1.0))
dioramas.append(cavity1)

# Diorama 2: Weak gravity, strong desire, slower time
cavity2 = ResonanceCavity(initial_pos=[-2.0, 2.5], initial_ta=0.7)
cavity2.add_potential(create_gravity_well(center=np.array([0.0, 0.0]), strength=1.0))
cavity2.add_potential(create_desire_attractor(target=np.array([2.0, -2.0]), strength=5.0))
dioramas.append(cavity2)

# Diorama 3: Balanced forces, but starts with a push
cavity3 = ResonanceCavity(initial_pos=[-2.0, 2.5])
cavity3.velocity = np.array([1.0, -0.5]) # Initial "nudge"
cavity3.add_potential(create_gravity_well(center=np.array([0.0, 0.0]), strength=2.5))
cavity3.add_potential(create_desire_attractor(target=np.array([2.0, -2.0]), strength=2.5))
dioramas.append(cavity3)

# --- Run the Simulation ---
time_steps = 200
dt = 0.05
for i in range(time_steps):
    for d in dioramas:
        d.step(dt)

# --- Visualize the Results ---
fig, ax = plt.subplots(figsize=(8, 8))

# Plot Potential Fields as a background
grid_res = 100
x = np.linspace(-4, 4, grid_res)
y = np.linspace(-4, 4, grid_res)
X, Y = np.meshgrid(x, y)
Z_total = np.zeros_like(X)
for d in dioramas: # Just use the first diorama's potential for visualization
    for source in d.potential_sources:
        # Vectorize the potential calculation for plotting
        Z_total += np.vectorize(lambda px, py: source(np.array([px, py])))(X, Y)
    break

ax.contourf(X, Y, Z_total, levels=50, cmap='viridis', alpha=0.6)
ax.set_title("'Senate of Ideas': Three Dioramas Evolving on a Potential Surface")
ax.set_xlabel("X Dimension")
ax.set_ylabel("Y Dimension")

# Plot trajectories
colors = ['cyan', 'magenta', 'yellow']
for i, d in enumerate(dioramas):
    path = np.array(d.history)
    ax.plot(path[:, 0], path[:, 1], color=colors[i], label=f'Diorama {i+1} (Ta={d.Ta})')
    ax.plot(path[0, 0], path[0, 1], 'o', color=colors[i], markeredgecolor='black') # Start
    ax.plot(path[-1, 0], path[-1, 1], 'X', color=colors[i], markeredgecolor='black', markersize=10) # End

# Mark the potential sources
ax.plot(0, 0, 'o', color='white', markersize=12, label='Gravity Well Center')
ax.plot(2, -2, '*', color='red', markersize=15, label='Desire Attractor')

ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_aspect('equal', adjustable='box')
plt.show()