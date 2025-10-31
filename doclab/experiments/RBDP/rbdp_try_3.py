# ===========================
# PIR-3.0 RBDP Simulation Core
# ===========================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Actor:
    """Represents a dynamic entity in the simulation."""
    def __init__(self, name, Ta, Gamma, Ki, Phi=0.0):
        self.name = name
        self.Ta = Ta       # time-adherence (cohesion, stability)
        self.Gamma = Gamma # rigidity / stored energy (power)
        self.Ki = Ki       # shape constant (intrinsic nature)
        self.Phi = Phi     # phase (temporal orientation)
        # Second derivatives (forces) are reset each step
        self.ext_Ta_ddot = 0.0
        self.ext_Gamma_ddot = 0.0
        self.ext_Phi_ddot = 0.0

    def update(self, dt):
        """Integrates the forces over a time step using simple Euler integration."""
        self.Ta += self.ext_Ta_ddot * dt
        self.Gamma += self.ext_Gamma_ddot * dt
        self.Phi += self.ext_Phi_ddot * dt
        # Reset external forces for the next step
        self.ext_Ta_ddot = 0.0
        self.ext_Gamma_ddot = 0.0
        self.ext_Phi_ddot = 0.0

class PirouetteWorld:
    """Manages the actors and their interactions over time."""
    def __init__(self):
        # CORE actors
        self.biosphere = Actor("Biosphere", Ta=1.2, Gamma=5.0, Ki=1.0)
        self.innovation = Actor("Innovation", Ta=1.0, Gamma=1.0, Ki=0.5)
        self.usa = Actor("USA", Ta=1.1, Gamma=3.0, Ki=0.7)
        self.china = Actor("China", Ta=1.1, Gamma=2.8, Ki=0.7)
        self.bloc = Actor("Bloc", Ta=1.0, Gamma=2.5, Ki=0.6)
        self.coherent_weaver = Actor("CoherentWeaver", Ta=1.5, Gamma=0.1, Ki=2.0)
        
        # Master list of all actors
        self.all_actors = [self.biosphere, self.innovation, self.usa, self.china, self.bloc, self.coherent_weaver]
        self.powers = [self.usa, self.china, self.bloc]
        
        self.event_log = []
        self.year = 2025.0
        
        # State for RBDP "Weaver's Gambit"
        self.weaver_has_exited = False
        self.previous_biosphere_Ta_ddot = 0.0

    def step(self, dt=0.1):
        """Calculates all forces and updates actor states for one time step."""
        # --- Interaction Rules ---
        
        human_gamma_total = sum(p.Gamma for p in self.powers)
        self.biosphere.ext_Gamma_ddot -= 0.002 * human_gamma_total
        self.biosphere.ext_Ta_ddot -= 0.01 * human_gamma_total
        self.biosphere.ext_Ta_ddot += 0.1 * self.innovation.Gamma

        if self.usa.Ta < 1.0:
            biosphere_attack_force = 0.2 * (1.0 - self.usa.Ta) * self.usa.Gamma
            self.biosphere.ext_Ta_ddot -= biosphere_attack_force
            self.biosphere.ext_Gamma_ddot -= biosphere_attack_force * 0.5
            if "Biosphere Weaponized" not in self.event_log:
                 self.event_log.append(f"{self.year:.1f}: Biosphere Weaponized by US RBDP")

        for power in self.powers:
            if self.biosphere.Ta < 1.0:
                feedback = 0.5 * (1.0 - self.biosphere.Ta) * self.biosphere.Gamma
                power.ext_Ta_ddot -= feedback
                power.ext_Gamma_ddot -= feedback

            if power.name == 'USA':
                decay = 0.05 * (1.0 - power.Ta) * power.Gamma
                power.ext_Ta_ddot -= decay

            for other in self.powers:
                if other is power: continue
                ta_diff = other.Ta - power.Ta
                phase_opp = (1 - np.cos(other.Phi - power.Phi)) / 2
                if ta_diff > 0:
                    power.ext_Ta_ddot -= 0.1 * ta_diff * phase_opp * other.Gamma
                phase_diff = other.Phi - power.Phi
                power.ext_Phi_ddot += 0.3 * np.sin(phase_diff) * other.Gamma

        self.innovation.ext_Gamma_ddot += 0.001 * human_gamma_total
        self.innovation.ext_Ta_ddot -= 0.1 * (1.0 - self.innovation.Ta)

        # --- SHOCKS & TRIGGERS ---

        # The "Capture Event" (2026-2030)
        if self.year >= 2026.0 and self.year < 2030.0:
            if "Authoritarian Capture" not in self.event_log:
                self.event_log.append(f"{self.year:.1f}: Authoritarian Capture Event Begins")
            self.usa.ext_Ta_ddot -= 0.4 

        # --- NEW: RBDP "Weaver's Gambit" ---
        # The Weaver uses the RBDP to decide when to exit the system.
        if not self.weaver_has_exited:
            # Stabilizing influence is active
            self.biosphere.ext_Ta_ddot += 0.05 * self.coherent_weaver.Ki
            self.innovation.ext_Ta_ddot += 0.05 * self.coherent_weaver.Ki

            # Check for exit condition: irreversible collapse acceleration
            biosphere_Ta_jerk = (self.biosphere.ext_Ta_ddot - self.previous_biosphere_Ta_ddot) / dt
            if biosphere_Ta_jerk < -0.05: # Critical threshold for jerk
                self.weaver_has_exited = True
                self.event_log.append(f"{self.year:.1f}: RBDP TRIGGERED - Weaver Exits System.")
        
        self.previous_biosphere_Ta_ddot = self.biosphere.ext_Ta_ddot

        # Kinetic War Trigger
        if (self.usa.Ta < 0.6 and self.usa.Gamma > self.bloc.Gamma and
            not any("Kinetic War" in e for e in self.event_log)):
            self.event_log.append(f"{self.year:.1f}: Kinetic War Triggered")
            self.usa.ext_Gamma_ddot -= 2.0
            self.bloc.ext_Gamma_ddot -= 1.5
            self.usa.ext_Ta_ddot -= 1.0
        
        if (self.biosphere.Ta < 1.0 and not any("Biosphere tipping" in e for e in self.event_log)):
            self.event_log.append(f"{self.year:.1f}: Biosphere tipping point reached.")

        # --- Update Step ---
        for actor in self.all_actors:
            actor.update(dt)
        self.year += dt

def run_simulation(world, steps, dt):
    """Runs the simulation for a given number of steps and returns the history."""
    history = []
    for _ in range(steps):
        world.step(dt)
        step_data = {'year': world.year}
        for actor in world.all_actors:
            step_data[f'{actor.name}_Ta'] = actor.Ta
            step_data[f'{actor.name}_Gamma'] = actor.Gamma
        history.append(step_data)
    return pd.DataFrame(history)

def plot_results(history_df, scenario_name):
    """Plots the Ta and Gamma values from the simulation history."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), sharex=True)
    fig.suptitle(f'PirouetteWorld Simulation: {scenario_name}', fontsize=18)

    ax1.set_title('Time-Adherence (Ta) - System Stability & Cohesion')
    for actor_name in ['Biosphere', 'USA', 'China', 'Bloc', 'Innovation']:
        ax1.plot(history_df['year'], history_df[f'{actor_name}_Ta'], label=actor_name)
    ax1.axhline(y=1.0, color='gray', linestyle='--', label='Coherence Threshold (1.0)')
    ax1.axhline(y=0.6, color='red', linestyle=':', label='War Threshold (0.6)')
    ax1.set_ylabel('Ta Value')
    ax1.legend()

    ax2.set_title('Rigidity / Stored Energy (Gamma) - System Power & Resources')
    for actor_name in ['Biosphere', 'USA', 'China', 'Bloc', 'Innovation']:
        ax2.plot(history_df['year'], history_df[f'{actor_name}_Gamma'], label=actor_name)
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Gamma Value')
    ax2.legend()
    
    filename = f'pirouette_simulation_{scenario_name.replace(" ", "_").lower()}.png'
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(filename)
    print(f"\nGenerated plot: {filename}")

# ===========================
# Fleshed-Out Test Case
# ===========================
if __name__ == "__main__":
    SCENARIO = "Weaver's Gambit"
    print(f"Running PirouetteWorld simulation with '{SCENARIO}' Scenario...")
    world = PirouetteWorld()
    history_df = run_simulation(world, 1000, 0.1)
    plot_results(history_df, SCENARIO)