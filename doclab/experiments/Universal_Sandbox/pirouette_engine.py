# pirouette_engine.py
import numpy as np

class PirouetteEngine:
    """
    The definitive Pirouette simulation engine for a single cavity (actor/entity).
    It evolves the core fields (Ta, Gamma, Phi) based on the full Lagrangian,
    allowing for complex internal dynamics and external forces.
    """
    def __init__(self, name, initial_Ta=1.0, initial_Gamma=1.0, initial_Phi=0.0):
        self.name = name
        # State Variables: Fields and their time derivatives ("velocities")
        self.Ta, self.Gamma, self.Phi = initial_Ta, initial_Gamma, initial_Phi
        self.Ta_dot, self.Gamma_dot, self.Phi_dot = 0.0, 0.0, 0.0

        # External forces/accelerations, to be calculated by the simulation manager
        self.ext_Ta_ddot, self.ext_Gamma_ddot, self.ext_Phi_ddot = 0.0, 0.0, 0.0

        # Internal framework parameters
        self.g = 0.1  # Default coupling constant
        self.Ki = 0.0 # Default Ki constant (phase reference)
        
        # Modular potential function, V(Ta, Gamma, Phi)
        self.potential_func = lambda Ta, Gamma, Phi: 0
        
        # History for plotting
        self.history = {'Ta': [self.Ta], 'Gamma': [self.Gamma], 'Phi': [self.Phi]}

    def set_parameters(self, g=None, Ki=None, potential_func=None):
        if g is not None: self.g = g
        if Ki is not None: self.Ki = Ki
        if potential_func is not None: self.potential_func = potential_func

    def _get_potential_gradient(self):
        """Numerically calculates the gradient of V with respect to the fields."""
        eps = 1e-6
        V_center = self.potential_func(self.Ta, self.Gamma, self.Phi)
        dV_dTa = (self.potential_func(self.Ta + eps, self.Gamma, self.Phi) - V_center) / eps
        dV_dGamma = (self.potential_func(self.Ta, self.Gamma + eps, self.Phi) - V_center) / eps
        dV_dPhi = (self.potential_func(self.Ta, self.Gamma, self.Phi + eps) - V_center) / eps
        return dV_dTa, dV_dGamma, dV_dPhi

    def step(self, dt):
        """Evolves the simulation by one time step."""
        # --- 1. Calculate internal forces from the Lagrangian ---
        dV_dTa, dV_dGamma, dV_dPhi = self._get_potential_gradient()
        delta_Phi = self.Phi - self.Ki
        cos_delta_Phi = np.cos(delta_Phi)
        sin_delta_Phi = np.sin(delta_Phi)

        # Euler-Lagrange equations for internal dynamics
        internal_Ta_ddot = -dV_dTa - self.g * self.Gamma_dot * cos_delta_Phi
        internal_Gamma_ddot = -dV_dGamma + self.g * self.Ta_dot * cos_delta_Phi
        internal_Phi_ddot = -dV_dPhi - self.g * self.Gamma * self.Ta_dot * sin_delta_Phi
        
        # --- 2. Combine with external forces ---
        total_Ta_ddot = internal_Ta_ddot + self.ext_Ta_ddot
        total_Gamma_ddot = internal_Gamma_ddot + self.ext_Gamma_ddot
        total_Phi_ddot = internal_Phi_ddot + self.ext_Phi_ddot
        
        # --- 3. Update state via Euler integration ---
        self.Ta_dot += total_Ta_ddot * dt
        self.Gamma_dot += total_Gamma_ddot * dt
        self.Phi_dot += total_Phi_ddot * dt

        self.Ta += self.Ta_dot * dt
        self.Gamma += self.Gamma_dot * dt
        self.Phi += self.Phi_dot * dt

    def record_history(self):
        self.history['Ta'].append(self.Ta)
        self.history['Gamma'].append(self.Gamma)
        self.history['Phi'].append(self.Phi)