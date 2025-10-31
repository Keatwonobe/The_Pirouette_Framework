import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

class PirouetteRenormalizationGroup:
    """
    A simulator for the scale dynamics described in CORE-015.
    """
    def __init__(self, d_K, d_Gamma, phi, psi, eta, zeta_K, zeta_Gamma):
        # Store the fundamental exponents and couplings
        self.d_K = d_K
        self.d_Gamma = d_Gamma
        self.phi = phi
        self.psi = psi
        self.eta = eta
        self.zeta_K = zeta_K
        self.zeta_Gamma = zeta_Gamma

    def beta_functions(self, s, y):
        """
        The core differential equations (β-functions) from CORE-015.
        s: scale parameter (s = ln L)
        y: state vector [K_tau, V_Gamma, tau_p]
        """
        K_tau, V_Gamma, tau_p = y

        # β-Operator for Coherence (K_tau)
        dK_tau_ds = self.d_K * K_tau - self.phi * V_Gamma * K_tau - self.eta * K_tau**3

        # β-Operator for Pressure (V_Gamma)
        dV_Gamma_ds = self.d_Gamma * V_Gamma - self.psi * K_tau * V_Gamma

        # β-Operator for Pulse (tau_p)
        # Note: The original equation in CORE-015 seems to have a typo.
        # d(tau_p)/ds should likely depend on tau_p itself.
        # I've used the form β_τ * τ_p as is standard for scale evolution.
        beta_tau = self.zeta_Gamma * V_Gamma - self.zeta_K * K_tau
        dtau_p_ds = beta_tau * tau_p

        return [dK_tau_ds, dV_Gamma_ds, dtau_p_ds]

    def solve(self, initial_conditions, s_span, s_eval):
        """
        Solves the system of ODEs using a numerical integrator.
        """
        solution = solve_ivp(
            self.beta_functions,
            s_span,
            initial_conditions,
            t_eval=s_eval,
            method='RK45'
        )
        return solution.t, solution.y

def plot_prg_flow(s, results, title):
    """Visualizes the results of the PRG simulation."""
    K_tau, V_Gamma, tau_p = results
    
    fig, axs = plt.subplots(3, 1, figsize=(12, 15), sharex=True)
    fig.suptitle(f"The Fractal at the Heart of Time: {title}", fontsize=16)

    # Plot 1: Coherence (Kτ)
    axs[0].plot(s, K_tau, color='dodgerblue', lw=2)
    axs[0].set_ylabel('Temporal Coherence ($K_τ$)')
    axs[0].set_title('Coherence vs. Scale')
    axs[0].grid(True, linestyle='--', alpha=0.6)

    # Plot 2: Pressure (VΓ)
    axs[1].plot(s, V_Gamma, color='crimson', lw=2)
    axs[1].set_ylabel('Temporal Pressure ($V_Γ$)')
    axs[1].set_title('Pressure vs. Scale')
    axs[1].grid(True, linestyle='--', alpha=0.6)

    # Plot 3: Pulse (τp)
    axs[2].plot(s, tau_p, color='forestgreen', lw=2)
    axs[2].set_xlabel('Scale Parameter (s = ln L)')
    axs[2].set_ylabel('Pirouette Cycle ($τ_p$)')
    axs[2].set_title('Rhythm vs. Scale')
    axs[2].grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == '__main__':
    # --- Simulation Setup ---
    # Define the scale of observation. s=0 is micro, s=10 is macro.
    s_span = [0, 10]
    s_eval = np.linspace(s_span[0], s_span[1], 500)

    # --- Scenario 1: "Laminar Phase" ---
    # In this scenario, we choose parameters that lead to a stable fixed point.
    # The system organizes itself into a coherent state as we zoom out.
    laminar_params = {
        'd_K': -0.1, 'd_Gamma': -0.5, 'phi': 0.2, 'psi': 0.1,
        'eta': 0.1, 'zeta_K': 0.05, 'zeta_Gamma': 0.02
    }
    prg_laminar = PirouetteRenormalizationGroup(**laminar_params)
    initial_conditions_laminar = [1.0, 2.0, 1.0] # Start with some coherence and pressure
    
    s, results_laminar = prg_laminar.solve(initial_conditions_laminar, s_span, s_eval)
    plot_prg_flow(s, results_laminar, "Laminar Flow - Stable Fixed Point")

    # --- Scenario 2: "Turbulent Phase" ---
    # Here, we choose parameters where interactions are stronger, leading to
    # oscillatory or chaotic behavior as scale changes.
    turbulent_params = {
        'd_K': 0.5, 'd_Gamma': 0.2, 'phi': 0.8, 'psi': 0.6,
        'eta': 0.1, 'zeta_K': 0.5, 'zeta_Gamma': 0.1
    }
    prg_turbulent = PirouetteRenormalizationGroup(**turbulent_params)
    initial_conditions_turbulent = [0.8, 1.2, 1.0]

    s, results_turbulent = prg_turbulent.solve(initial_conditions_turbulent, s_span, s_eval)
    plot_prg_flow(s, results_turbulent, "Turbulent Flow - Oscillatory Dynamics")