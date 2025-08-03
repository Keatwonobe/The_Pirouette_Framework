import numpy as np
import matplotlib.pyplot as plt
from pirouette_engine import PirouetteEngine

# --- 1. The Diorama Matrix: Information Age Players ---

# Phase Goals: The core strategic objectives in the information space.
# Let's set Status Quo as the 0-degree reference.
GOAL_STATUS_QUO = np.deg2rad(0)      # Maintain existing global order (US)
GOAL_DISRUPTION = np.deg2rad(120)     # Destabilize & create multipolar world (Russia)
GOAL_HEGEMONY = np.deg2rad(-90)     # Achieve economic/tech dominance (China)
GOAL_ASYMMETRIC_INFLUENCE = np.deg2rad(45) # Secure specific national interests (Info-Powers)

diorama_matrix = [
    PirouetteEngine(
        name='USA',
        initial_Ta=0.9,    # Starts high but below 1, indicating latent internal divisions.
        initial_Gamma=1.5, # Superpower-level conventional influence.
        initial_Phi=GOAL_STATUS_QUO
    ),
    PirouetteEngine(
        name='Russia',
        initial_Ta=1.2,    # Highly coherent and practiced in information doctrine.
        initial_Gamma=0.8, # Less conventional power, relies on info-war.
        initial_Phi=GOAL_DISRUPTION
    ),
    PirouetteEngine(
        name='China',
        initial_Ta=1.4,    # Extremely high internal coherence and control.
        initial_Gamma=1.2, # Massive and growing conventional power.
        initial_Phi=GOAL_HEGEMONY
    ),
    PirouetteEngine(
        name='Info-Powers', # Represents states like Israel, UAE, etc.
        initial_Ta=1.3,    # Very agile and coherent in their specific domains.
        initial_Gamma=0.4, # Low conventional power, high asymmetric impact.
        initial_Phi=GOAL_ASYMMETRIC_INFLUENCE
    )
]

# --- 2. The Interaction Physics: Coherence Warfare ---

def update_interactions(matrix, year):
    """Calculates forces, including the new 'coherence attack' mechanic."""
    # The potency of information warfare increases with technology.
    coupling_g = 0.05 + (year - 1990) / 400.0 # 'g' constant grows over time
    
    # --- Event Shocks ---
    # COVID-19 Pandemic: A global shock that temporarily damages everyone's stability.
    covid_shock = 0
    if 2020 <= year < 2022:
        covid_shock = -0.8

    for cavity in matrix:
        cavity.ext_Ta_ddot, cavity.ext_Gamma_ddot, cavity.ext_Phi_ddot = 0.0, 0.0, 0.0
        cavity.g = coupling_g
        
        # Apply the COVID Ta shock
        if covid_shock != 0:
            cavity.ext_Ta_ddot += covid_shock * (1 / cavity.Ta) # Less stable are hit harder

        for other_cavity in matrix:
            if cavity is other_cavity: continue

            # --- KEY MECHANIC: Coherence Attack ---
            # An actor with high Ta can attack the coherence of a low Ta actor.
            # The more coherent the attacker, the more damaging the attack.
            if other_cavity.Ta > cavity.Ta:
                ta_difference = other_cavity.Ta - cavity.Ta
                # Attack is most effective when goals are opposed.
                phase_opposition = (1 - np.cos(other_cavity.Phi - cavity.Phi)) / 2
                coherence_attack_force = 0.1 * ta_difference * phase_opposition * other_cavity.Gamma
                cavity.ext_Ta_ddot -= coherence_attack_force

            # Standard phase alignment and gamma pressure
            phase_difference = other_cavity.Phi - cavity.Phi
            phase_force = 0.4 * np.sin(phase_difference) * other_cavity.Gamma
            cavity.ext_Phi_ddot += phase_force

            gamma_difference = other_cavity.Gamma - other_cavity.Gamma
            gamma_force = 0.05 * gamma_difference
            cavity.ext_Gamma_ddot -= gamma_force


# --- 3. Run the Simulation ---
print("Simulating the landscape of modern coherence warfare...")
start_year = 1990
end_year = 2025
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
colors = {'USA': 'blue', 'Russia': 'red', 'China': 'goldenrod', 'Info-Powers': 'green'}
styles = {'USA': '-', 'Russia': '--', 'China': '-', 'Info-Powers': ':'}
fig.suptitle('Pirouette Simulation: The Age of Coherence Warfare (1990-2025)', fontsize=18)

# --- Plotting ---
# Phase Plot
axs[0].set_title('Phase ($\phi$): The Global Competition of Narratives', fontsize=12)
# Gamma Plot
axs[1].set_title('Gladiator Force ($\Gamma$): The Balance of Influence (Conventional & Informational)', fontsize=12)
# Ta Plot
axs[2].set_title('Time-Adherence ($T_a$): National Coherence & Susceptibility to Attack', fontsize=12)

for cavity in diorama_matrix:
    name = cavity.name
    # Plot Phase
    phase_degrees = np.rad2deg(np.unwrap(cavity.history['Phi']))
    axs[0].plot(time_axis, phase_degrees, label=name, color=colors[name], linestyle=styles[name], lw=2.5)
    # Plot Gamma
    axs[1].plot(time_axis, cavity.history['Gamma'], label=name, color=colors[name], linestyle=styles[name], lw=2.5)
    # Plot Ta
    axs[2].plot(time_axis, cavity.history['Ta'], label=name, color=colors[name], linestyle=styles[name], lw=2.5)

axs[2].set_xlabel('Year')
axs[0].set_ylabel('Narrative Alignment (Deg)')
axs[1].set_ylabel('Global Influence')
axs[2].set_ylabel('Internal Coherence')

for ax in axs:
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.axvspan(2020, 2022, color='gray', alpha=0.2, label='COVID-19 Pandemic')
    ax.legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()