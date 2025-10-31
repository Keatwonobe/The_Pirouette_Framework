import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from collections import deque

# --- 1. Shield Simulation Engine (from your fractal mesh code) ---
# A lightweight version that runs for a single (J, lam) point.
def run_shield_simulation(J, lam, n_spins=30, n_iters=50):
    """
    Runs a single, fast shield simulation for a given J and lambda.
    Returns the final spin coherence (M).
    """
    theta = np.random.rand(n_spins) * 2 * np.pi
    beta = 1.0  # T(a) feedback strength, kept constant for this model
    M_hist = deque(maxlen=10) # MODIFIED: Initialized M_hist here

    for _ in range(n_iters):
        # Calculate Time-Adherence from variance of M in the last 5 steps
        # MODIFIED: Added a length check and converted deque to list for slicing
        if len(M_hist) > 5:
            M_variance = np.var(list(M_hist)[-5:])
            Ta = 1 / (1 + beta * M_variance)
        else:
            Ta = 1.0

        # Ki-Modulated effective J
        J_eff = J * np.sin(Ta * np.pi)

        # Update spins (vectorized)
        mean_field = np.sum(np.cos(theta - theta[:, np.newaxis]), axis=1) / n_spins
        theta += lam * np.sin(2 * theta) + J_eff * mean_field
        theta %= (2 * np.pi)

        # Calculate spin coherence M
        M = np.abs(np.sum(np.exp(1j * theta))) / n_spins
        M_hist.append(M)

    return M # Return the final coherence

# --- 2. The Traveler (Unchanged) ---
class Traveler:
    def __init__(self):
        self.path_t = np.linspace(0, 4 * np.pi, 240)
        self.x = 2.0 * np.cos(self.path_t)
        self.y = 2.0 * np.sin(self.path_t)
        self.z = self.path_t / np.pi
        self.current_frame = 0

    def get_position(self, frame):
        return self.x[frame], self.y[frame], self.z[frame]

    def get_projected_position(self, frame):
        return self.x[frame], self.y[frame]

# --- 3. The Compass Field (Now with Shield Interaction) ---
class CompassField:
    def __init__(self, traveler, grid_size=200, wake_memory=25):
        self.traveler = traveler
        gamma_vals = np.linspace(-3, 3, grid_size)
        ta_vals = np.linspace(-3, 3, grid_size)
        self.Gamma, self.Ta = np.meshgrid(gamma_vals, ta_vals)
        self.wake_history = deque(maxlen=wake_memory)
        self.wake_field = np.zeros_like(self.Gamma)
        self.shield_resonance_field = np.zeros_like(self.Gamma)

    def base_potential(self, gamma, ta, z):
        return (np.sin(gamma) * np.cos(ta) +
                np.sin(ta) * np.cos(z) +
                np.sin(z) * np.cos(gamma))

    def update_wake(self, traveler_proj_pos):
        self.wake_history.append(traveler_proj_pos)
        self.wake_field.fill(0)
        max_strength = 1.0
        for i, (hist_gamma, hist_ta) in enumerate(self.wake_history):
            strength = max_strength * ((i + 1) / len(self.wake_history))**2
            sq_dist = (self.Gamma - hist_gamma)**2 + (self.Ta - hist_ta)**2
            gaussian_influence = strength * np.exp(-sq_dist * 5)
            self.wake_field += gaussian_influence
            
    def update_shield_resonance(self, traveler_proj_pos, shield_coherence):
        """Creates a local disturbance based on the Shield's output."""
        self.shield_resonance_field.fill(0)
        gamma_pos, ta_pos = traveler_proj_pos
        
        # Strength of resonance is proportional to shield coherence M
        strength = 2.0 * shield_coherence
        
        sq_dist = (self.Gamma - gamma_pos)**2 + (self.Ta - ta_pos)**2
        # A sharper Gaussian for the immediate resonance
        self.shield_resonance_field = strength * np.exp(-sq_dist * 20)

    def get_total_potential(self, traveler_z):
        # Total potential is now Base + Wake + Shield
        base_V = self.base_potential(self.Gamma, self.Ta, traveler_z)
        return base_V - self.wake_field + self.shield_resonance_field

# --- 4. Simulation and Visualization ---
def run_full_simulation():
    traveler = Traveler()
    compass = CompassField(traveler)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    def update(frame):
        ax.clear()
        
        # --- The Core Feedback Loop ---
        
        # 1. Get Traveler's position in Compass space
        traveler_gamma, traveler_ta, traveler_z = traveler.get_position(frame)
        
        # 2. MAP Compass coordinates to Shield parameters
        J_param = traveler_gamma
        lambda_param = traveler_ta
        
        # 3. SIMULATE the underlying Shield dynamics
        shield_coherence_M = run_shield_simulation(J=J_param, lam=lambda_param)
        
        # 4. FEEDBACK from Shield to Compass
        compass.update_shield_resonance((traveler_gamma, traveler_ta), shield_coherence_M)
        
        # --- Update fields and visualize ---
        compass.update_wake((traveler_gamma, traveler_ta))
        V_total = compass.get_total_potential(traveler_z)
        
        # Plotting
        ax.contourf(compass.Gamma, compass.Ta, V_total, levels=50, cmap='inferno')
        ax.contour(compass.Gamma, compass.Ta, V_total, levels=50, colors='white', linewidths=0.5, alpha=0.3)
        
        wake_points = np.array(list(compass.wake_history))
        ax.plot(wake_points[:, 0], wake_points[:, 1], 'c-', lw=2.5, alpha=0.7, label="Traveler's Wake")
        
        # Traveler marker color now reflects the shield coherence
        traveler_color = plt.cm.viridis(shield_coherence_M)
        ax.plot(traveler_gamma, traveler_ta, '*', markersize=18, color=traveler_color, 
                markeredgecolor='white', label=f"Traveler (Shield M={shield_coherence_M:.2f})")
        
        ax.set_title(f"Compass Field with Shield Resonance (z={traveler_z:.2f})")
        ax.set_xlabel("Gladiator Force (Γ) / Shield J")
        ax.set_ylabel("Time-Adherence (Ta) / Shield λ")
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_aspect('equal', adjustable='box')
        ax.legend(loc='upper right')
        
    ani = FuncAnimation(fig, update, frames=len(traveler.path_t), repeat=False)
    ani.save("traveler_shield_resonance.gif", writer=PillowWriter(fps=30))
    plt.close()
    print("Animation saved as traveler_shield_resonance.gif")

# Run the simulation
run_full_simulation()