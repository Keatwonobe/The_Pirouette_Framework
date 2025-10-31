import numpy as np
import matplotlib.pyplot as plt
from pirouette_engine import PirouetteEngine

# --- 1. The Diorama Matrix: A Planet in Crisis ---

# Phase Goals: The intrinsic objectives of the systems.
GOAL_EQUILIBRIUM = np.deg2rad(0)      # The Biosphere's natural state of balance.
GOAL_GROWTH = np.deg2rad(175)     # Industrial Civilization's goal, almost perfectly opposed to equilibrium.

diorama_matrix = [
    PirouetteEngine(
        name='Biosphere',
        initial_Ta=1.5,    # Starts as a highly stable, resilient system.
        initial_Gamma=2.0, # Immense power to self-regulate.
        initial_Phi=GOAL_EQUILIBRIUM
    ),
    PirouetteEngine(
        name='Humanity',
        initial_Ta=1.1,    # A relatively stable socio-economic order.
        initial_Gamma=0.2, # Starts with low global impact, but will grow exponentially.
        initial_Phi=GOAL_GROWTH
    )
]

# --- 2. The Interaction Physics: A War on a System ---

def update_interactions(matrix, year):
    """
    Calculates forces, including resource extraction and biosphere destabilization.
    """
    humanity = next(c for c in matrix if c.name == 'Humanity')
    biosphere = next(c for c in matrix if c.name == 'Biosphere')

    # Reset external forces
    humanity.ext_Ta_ddot, humanity.ext_Gamma_ddot, humanity.ext_Phi_ddot = 0, 0, 0
    biosphere.ext_Ta_ddot, biosphere.ext_Gamma_ddot, biosphere.ext_Phi_ddot = 0, 0, 0

    # --- Humanity's Growth & Impact ---
    # Humanity's Gamma (industrial output) grows, fueled by extracting it from the Biosphere.
    # This represents resource extraction, pollution, habitat loss, etc.
    extraction_rate = 0.001 * humanity.Gamma # Extraction accelerates as industrial power grows
    humanity.ext_Gamma_ddot += extraction_rate * 5 # Humanity's growth is amplified
    biosphere.ext_Gamma_ddot -= extraction_rate * 20 # The Biosphere pays a heavy price

    # --- The Attack on Coherence ---
    # Humanity's industrial activity directly damages the Biosphere's stability (Ta).
    # This is climate change: turning a stable system into a chaotic one.
    coherence_attack = 0.05 * humanity.Gamma
    biosphere.ext_Ta_ddot -= coherence_attack

    # --- The Feedback Loop (The Critical Mechanic) ---
    # As the Biosphere becomes unstable (Ta drops), it starts to damage Humanity.
    # This represents crop failures, supply chain collapse, climate refugees, social chaos.
    if biosphere.Ta < 1.0:
        biosphere_feedback_damage = 0.2 * (1.0 - biosphere.Ta) * biosphere.Gamma
        humanity.ext_Ta_ddot -= biosphere_feedback_damage # Social coherence collapses
        humanity.ext_Gamma_ddot -= biosphere_feedback_damage # Economic activity is crippled

# --- 3. Run the Simulation ---
print("Simulating the trajectory of the climate crisis...")
start_year = 1950
end_year = 2100
dt = 0.1
steps = int((end_year - start_year) / dt)
time_axis = np.linspace(start_year, end_year, steps + 1)

for i in range(steps):
    year = start_year + i * dt
    update_interactions(diorama_matrix, year)
    for cavity in diorama_matrix:
        cavity.step(dt)
        cavity.record_history()
print("Simulation complete.")

# --- 4. Visualization & Analysis ---
fig, axs = plt.subplots(3, 1, figsize=(15, 14), sharex=True)
colors = {'Biosphere': 'seagreen', 'Humanity': 'dimgray'}
styles = {'Biosphere': '-', 'Humanity': '--'}
fig.suptitle('Pirouette Simulation: The Climate Crisis Trajectory (1950-2100)', fontsize=18)

# Find Tipping Point
biosphere_ta = np.array(diorama_matrix[0].history['Ta'])
tipping_point_idx = np.argmax(biosphere_ta < 1.0)
tipping_point_year = time_axis[tipping_point_idx] if tipping_point_idx > 0 else -1

# --- Plotting ---
axs[0].set_title('Gladiator Force ($\Gamma$): The Great Extraction', fontsize=12)
axs[1].set_title('Time-Adherence ($T_a$): The Collapse of Stability', fontsize=12)
axs[2].set_title('Phase ($\phi$): The Irreconcilable Goals', fontsize=12)

for cavity in diorama_matrix:
    name = cavity.name
    axs[0].plot(time_axis, cavity.history['Gamma'], color=colors[name], linestyle=styles[name], lw=2.5, label=name)
    axs[1].plot(time_axis, cavity.history['Ta'], color=colors[name], linestyle=styles[name], lw=2.5, label=name)
    phase_deg = np.rad2deg(np.unwrap(cavity.history['Phi']))
    axs[2].plot(time_axis, phase_deg, color=colors[name], linestyle=styles[name], lw=2.5, label=name)

axs[0].set_ylabel('System Power / Capacity')
axs[1].set_ylabel('System Stability / Resilience')
axs[2].set_ylabel('Goal Alignment (Degrees)')
axs[2].set_xlabel('Year')

for ax in axs:
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.legend()
    if tipping_point_year > 0:
        ax.axvline(tipping_point_year, color='red', linestyle='--', lw=2, label=f'Biosphere Tipping Point (~{tipping_point_year:.0f})')
        ax.legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()