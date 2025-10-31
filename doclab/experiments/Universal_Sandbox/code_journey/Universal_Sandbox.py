import numpy as np
import matplotlib.pyplot as plt

class PirouetteCavity:
    """
    A simulation cavity governed by the Pirouette Framework Lagrangian.
    This simulates the evolution of the core fields (Ta, Gamma, Phi)
    at a single point in space.
    """
    def __init__(self, initial_Ta=1.0, initial_Gamma=1.0, initial_Phi=0.0, g=0.1, Ki=0.0):
        # State Variables: The fields and their time derivatives ("velocities")
        self.Ta = initial_Ta
        self.Gamma = initial_Gamma
        self.Phi = initial_Phi
        self.Ta_dot = 0.0
        self.Gamma_dot = 0.0
        self.Phi_dot = 0.0

        # Framework Parameters
        self.g = g          # Coupling constant from the Lagrangian
        self.Ki = Ki        # Ki Constant for phase reference

        # Modular potential function, V(Ta, Gamma, Phi)
        self.potential_func = lambda Ta, Gamma, Phi: 0
        
        # History for plotting
        self.history = {'t': [], 'Ta': [], 'Gamma': [], 'Phi': []}

    def set_potential(self, potential_func):
        """Sets the potential V(Ta, Gamma, Phi) for the cavity."""
        self.potential_func = potential_func

    def get_potential_gradient(self):
        """Numerically calculates the gradient of V with respect to the fields."""
        eps = 1e-6 # A small step for numerical differentiation
        
        # Partial derivative with respect to Ta
        V_Ta_plus = self.potential_func(self.Ta + eps, self.Gamma, self.Phi)
        V_Ta_minus = self.potential_func(self.Ta - eps, self.Gamma, self.Phi)
        dV_dTa = (V_Ta_plus - V_Ta_minus) / (2 * eps)

        # Partial derivative with respect to Gamma
        V_Gamma_plus = self.potential_func(self.Ta, self.Gamma + eps, self.Phi)
        V_Gamma_minus = self.potential_func(self.Ta, self.Gamma - eps, self.Phi)
        dV_dGamma = (V_Gamma_plus - V_Gamma_minus) / (2 * eps)

        # Partial derivative with respect to Phi
        V_Phi_plus = self.potential_func(self.Ta, self.Gamma, self.Phi + eps)
        V_Phi_minus = self.potential_func(self.Ta, self.Gamma, self.Phi - eps)
        dV_dPhi = (V_Phi_plus - V_Phi_minus) / (2 * eps)

        return dV_dTa, dV_dGamma, dV_dPhi

    def step(self, dt):
        """
        Evolves the simulation by one time step using the Euler-Lagrange equations
        derived from the core Lagrangian.
        """
        # Get partial derivatives of the potential V
        dV_dTa, dV_dGamma, dV_dPhi = self.get_potential_gradient()

        # The interaction term's phase difference
        delta_Phi = self.Phi - self.Ki
        cos_delta_Phi = np.cos(delta_Phi)
        sin_delta_Phi = np.sin(delta_Phi)

        # Calculate second derivatives ("accelerations") of the fields
        # These are the Euler-Lagrange equations of motion
        Ta_ddot = -dV_dTa - self.g * self.Gamma_dot * cos_delta_Phi
        Gamma_ddot = -dV_dGamma + self.g * self.Ta_dot * cos_delta_Phi
        Phi_ddot = -dV_dPhi - self.g * self.Gamma * self.Ta_dot * sin_delta_Phi
        
        # Update field velocities (Euler integration)
        self.Ta_dot += Ta_ddot * dt
        self.Gamma_dot += Gamma_ddot * dt
        self.Phi_dot += Phi_ddot * dt

        # Update field values
        self.Ta += self.Ta_dot * dt
        self.Gamma += self.Gamma_dot * dt
        self.Phi += self.Phi_dot * dt

    def record_history(self, t):
        """Stores the current state of the fields."""
        self.history['t'].append(t)
        self.history['Ta'].append(self.Ta)
        self.history['Gamma'].append(self.Gamma)
        self.history['Phi'].append(self.Phi)

# --- Example of a Modular Scenario ---

# This entire section could be in a separate file, e.g., `scenario_resonant_decay.py`
# It just needs to `from pirouette_engine import PirouetteCavity`

# 1. Define a potential for this scenario
# This potential creates a "bowl" that tries to pull the fields
# back to a stable state (Ta=1, Gamma=1, Phi=0).
def harmonic_potential(Ta, Gamma, Phi):
    k_Ta = 2.0     # "Stiffness" for Ta
    k_Gamma = 2.0  # "Stiffness" for Gamma
    k_Phi = 1.0    # "Stiffness" for Phi
    
    # Simple harmonic oscillator potential
    V = 0.5 * k_Ta * (Ta - 1.0)**2 + \
        0.5 * k_Gamma * (Gamma - 1.0)**2 + \
        0.5 * k_Phi * (Phi - 0.0)**2
    return V

# 2. Setup and run the simulation
print("Running Pirouette Cavity Simulation...")
# Create an instance of the engine
cavity = PirouetteCavity(g=0.5, Ki=0.0)

# Set the potential for this specific simulation
cavity.set_potential(harmonic_potential)

# Give the system an initial "kick" by displacing it from equilibrium
cavity.Ta = 1.5
cavity.Gamma = 0.5
cavity.Phi = 0.2

# Simulation parameters
total_time = 40.0
dt = 0.01
steps = int(total_time / dt)

for i in range(steps):
    t = i * dt
    cavity.step(dt)
    cavity.record_history(t)

print("Simulation complete.")

# 3. Visualize the results
fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
fig.suptitle('Pirouette Cavity: Field Evolution Over Time', fontsize=16)

# Plot Time-Adherence (Ta)
axs[0].plot(cavity.history['t'], cavity.history['Ta'], label='$T_a$ (Time-Adherence)', color='crimson')
axs[0].axhline(1.0, linestyle='--', color='gray', alpha=0.7, label='Equilibrium ($T_a=1$)')
axs[0].set_ylabel('Field Value')
axs[0].legend()
axs[0].grid(True, alpha=0.3)

# Plot Gladiator Force (Gamma)
axs[1].plot(cavity.history['t'], cavity.history['Gamma'], label='$\Gamma$ (Gladiator Force)', color='royalblue')
axs[1].axhline(1.0, linestyle='--', color='gray', alpha=0.7, label='Equilibrium ($\Gamma=1$)')
axs[1].set_ylabel('Field Value')
axs[1].legend()
axs[1].grid(True, alpha=0.3)

# Plot Phase (Phi)
axs[2].plot(cavity.history['t'], cavity.history['Phi'], label='$\phi$ (Phase)', color='forestgreen')
axs[2].axhline(0.0, linestyle='--', color='gray', alpha=0.7, label='Equilibrium ($\phi=0$)')
axs[2].set_xlabel('Time (s)')
axs[2].set_ylabel('Field Value (radians)')
axs[2].legend()
axs[2].grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()