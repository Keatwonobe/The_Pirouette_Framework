import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from collections import deque

# --- 1. The Traveler ---
# This class defines the entity moving in a higher dimension.
class Traveler:
    """Represents the Traveler moving in a 3D conceptual space."""
    def __init__(self):
        # Position in a conceptual (x, y, z) space
        self.path_t = np.linspace(0, 4 * np.pi, 240) # Full path for 240 frames
        # Helical path: projects as a circle on the (x,y) plane, moves along z
        self.x = 1.5 * np.cos(self.path_t)
        self.y = 1.5 * np.sin(self.path_t)
        self.z = self.path_t / (2 * np.pi) # z progresses with the path
        self.current_frame = 0

    def get_position(self, frame):
        """Gets the traveler's 3D position at a given frame."""
        return self.x[frame], self.y[frame], self.z[frame]

    def get_projected_position(self, frame):
        """Gets the 2D projection onto the Gamma-Ta plane."""
        return self.x[frame], self.y[frame]

# --- 2. The Compass Field ---
# This class manages the Gamma-Ta plane and the wake.
class CompassField:
    """Represents the Gamma-Ta plane and its potential, affected by the Traveler's wake."""
    def __init__(self, traveler, grid_size=200, wake_memory=25):
        self.traveler = traveler
        
        # Define the Gamma-Ta grid
        gamma_vals = np.linspace(-3, 3, grid_size)
        ta_vals = np.linspace(-3, 3, grid_size)
        self.Gamma, self.Ta = np.meshgrid(gamma_vals, ta_vals)
        
        # Wake parameters
        self.wake_history = deque(maxlen=wake_memory)
        self.wake_field = np.zeros_like(self.Gamma)

    def base_potential(self, gamma, ta, z):
        """A foundational potential field, here a gyroid structure."""
        return (np.sin(gamma) * np.cos(ta) +
                np.sin(ta) * np.cos(z) +
                np.sin(z) * np.cos(gamma))

    def update_wake(self, traveler_proj_pos):
        """Updates the wake based on the traveler's history."""
        self.wake_history.append(traveler_proj_pos)
        
        # Reset the wake and rebuild it from history
        self.wake_field.fill(0)
        max_strength = 1.0 # Strength of the most recent point
        
        for i, (hist_gamma, hist_ta) in enumerate(self.wake_history):
            # Strength decays for older points in the wake
            strength = max_strength * ((i + 1) / len(self.wake_history))**2
            
            # Add a Gaussian disturbance for each historical point
            sq_dist = (self.Gamma - hist_gamma)**2 + (self.Ta - hist_ta)**2
            gaussian_influence = strength * np.exp(-sq_dist * 5)
            self.wake_field += gaussian_influence

    def get_total_potential(self, traveler_z):
        """Combines the base potential with the dynamic wake field."""
        base_V = self.base_potential(self.Gamma, self.Ta, traveler_z)
        # The wake perturbs the base potential
        return base_V - self.wake_field

# --- 3. Simulation and Visualization ---
def run_simulation():
    """Sets up and runs the animation."""
    traveler = Traveler()
    compass = CompassField(traveler)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # This function is called for each frame of the animation
    def update(frame):
        ax.clear()
        
        # Get Traveler's current state
        traveler_x, traveler_y, traveler_z = traveler.get_position(frame)
        
        # Update and get the total potential field
        compass.update_wake((traveler_x, traveler_y))
        V_total = compass.get_total_potential(traveler_z)
        
        # Plotting
        ax.contourf(compass.Gamma, compass.Ta, V_total, levels=50, cmap='inferno')
        ax.contour(compass.Gamma, compass.Ta, V_total, levels=50, colors='white', linewidths=0.5, alpha=0.3)
        
        # Plot the Traveler's projected path and current position
        wake_points = np.array(list(compass.wake_history))
        ax.plot(wake_points[:, 0], wake_points[:, 1], 'c-', lw=2.5, alpha=0.7, label="Traveler's Wake")
        ax.plot(traveler_x, traveler_y, 'w*', markersize=15, markeredgecolor='black', label="Traveler (Projected)")
        
        # Aesthetics
        ax.set_title(f"Compass Field at Time-Slice z={traveler_z:.2f}")
        ax.set_xlabel("Gladiator Force (Γ)")
        ax.set_ylabel("Time-Adherence (Ta)")
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_aspect('equal', adjustable='box')
        ax.legend(loc='upper right')
        
    # Create and save the animation
    ani = FuncAnimation(fig, update, frames=len(traveler.path_t), repeat=False)
    ani.save("traveler_wake_simulation.gif", writer=PillowWriter(fps=30))
    plt.close()
    print("Animation saved as traveler_wake_simulation.gif")

# Run the simulation
run_simulation()