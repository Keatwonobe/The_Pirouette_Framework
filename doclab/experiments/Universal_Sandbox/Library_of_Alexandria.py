import numpy as np
import matplotlib.pyplot as plt
from pirouette_engine import PirouetteCavity # Assumes the class is in this file

# --- 1. The Diorama Matrix: Define the Players ---

# Let's set the State's goal of "Civic Stability" as our reference point: 0.0
# The Scholars' goal is adjacent to this. The Hierarchy's goal is orthogonal, a different axis of value.
GOAL_STABILITY = 0.0
GOAL_KNOWLEDGE = np.deg2rad(20)    # Valued, but secondary to stability.
GOAL_PURITY = np.deg2rad(90)      # A new, perpendicular value system (Faith).

diorama_matrix = [
    # The Scholars of the Library: Holding onto a fading worldview.
    PirouetteCavity(
        name='Scholars',
        initial_Ta=1.1,    # High Ta: Their knowledge feels timeless and stable.
        initial_Gamma=0.9, # High Gamma initially, but poised to fall.
        initial_Phi=GOAL_KNOWLEDGE
    ),
    # The Ascendant Hierarchy: A new, highly resonant paradigm.
    PirouetteCavity(
        name='Hierarchy',
        initial_Ta=1.2,    # Very High Ta: The conviction of singular, eternal truth.
        initial_Gamma=0.6, # Starts lower, but is rapidly gaining influence.
        initial_Phi=GOAL_PURITY
    ),
    # The Roman State: The powerful, pragmatic arbiter.
    PirouetteCavity(
        name='State',
        initial_Ta=1.0,    # Ta=1.0: The definition of 'normal' time.
        initial_Gamma=1.2, # Very High Gamma: Holds the monopoly on force.
        initial_Phi=GOAL_STABILITY
    )
]

# --- 2. The Interaction Physics ---

def update_interactions(matrix, time):
    """
    Calculates forces, including a term for the Hierarchy's growing influence.
    """
    ALIGNMENT_STRENGTH = 1.2 # Phase alignment is now a more powerful force
    INFLUENCE_STRENGTH = 0.5

    # Model the Hierarchy's historical rise in influence
    hierarchy_growth_factor = (time / 50.0) # Simple linear growth over the simulation

    for cavity in matrix:
        cavity.Ta_ddot, cavity.Gamma_ddot, cavity.Phi_ddot = 0.0, 0.0, 0.0
        
        # Self-correction: All systems feel a slight pull back to their starting ideals
        cavity.Phi_ddot -= 0.1 * (cavity.Phi - cavity.history['Phi'][0])

        # Specific growth model for the Hierarchy's Gamma
        if cavity.name == 'Hierarchy':
            cavity.Gamma_ddot += hierarchy_growth_factor * 0.1

        for other_cavity in matrix:
            if cavity is other_cavity:
                continue

            phase_difference = other_cavity.Phi - cavity.Phi
            # The "force" of another's phase is weighted by their Gamma (influence)
            phase_force = ALIGNMENT_STRENGTH * np.sin(phase_difference) * other_cavity.Gamma
            cavity.Phi_ddot += phase_force

            gamma_difference = other_cavity.Gamma - cavity.Gamma
            # Softer pressure this time, more about phase alignment
            gamma_force = INFLUENCE_STRENGTH * gamma_difference * 0.1 
            cavity.Gamma_ddot += gamma_force


# --- 3. Run the Simulation ---

print("Simulating the decline of the Library of Alexandria...")
total_time = 100.0
dt = 0.1
steps = int(total_time / dt)
time_axis = np.linspace(0, total_time, steps + 1)

for i in range(steps):
    t = i * dt
    update_interactions(diorama_matrix, t)
    for cavity in diorama_matrix:
        cavity.step(dt)
        cavity.record_history()
print("Simulation complete.")

# --- 4. Visualize the Outcome ---

fig, axs = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
fig.suptitle('Pirouette Simulation: The Decline of the Library of Alexandria', fontsize=18)
colors = {'Scholars': 'gold', 'Hierarchy': 'purple', 'State': 'darkgray'}
styles = {'Scholars': '-', 'Hierarchy': '-', 'State': '--'}

# Plot Phase (Goal Alignment)
axs[0].set_title('Phase ($\phi$): The War of Worldviews', fontsize=12)
for cavity in diorama_matrix:
    phase_degrees = np.rad2deg(np.unwrap(cavity.history['Phi']))
    axs[0].plot(time_axis, phase_degrees, label=cavity.name, color=colors[cavity.name], linestyle=styles[cavity.name], lw=2.5)
axs[0].set_ylabel('Worldview Alignment (Degrees)')
axs[0].legend()

# Plot Gamma (Influence/Strength)
axs[1].set_title('Gladiator Force ($\Gamma$): The Transfer of Power', fontsize=12)
for cavity in diorama_matrix:
    axs[1].plot(time_axis, cavity.history['Gamma'], label=cavity.name, color=colors[cavity.name], linestyle=styles[cavity.name], lw=2.5)
axs[1].set_ylabel('Societal Influence')
axs[1].legend()

# Plot Ta (Stability/Coherence)
axs[2].set_title('Time-Adherence ($T_a$): Paradigm Coherence', fontsize=12)
for cavity in diorama_matrix:
    axs[2].plot(time_axis, cavity.history['Ta'], label=cavity.name, color=colors[cavity.name], linestyle=styles[cavity.name], lw=2.5)
axs[2].set_ylabel('Ideological Stability')
axs[2].set_xlabel('Time (Centuries)')
axs[2].legend()

for ax in axs:
    ax.grid(True, linestyle=':', alpha=0.6)
    # Highlight the tipping point where the State's goals align with the Hierarchy
    tipping_point_time = np.argmax(np.isclose(
        np.rad2deg(np.unwrap(diorama_matrix[2].history['Phi'])), # State's Phi
        np.rad2deg(np.unwrap(diorama_matrix[1].history['Phi'])), # Hierarchy's Phi
        atol=10 # within 10 degrees
    )) * dt
    if tipping_point_time > 0:
        ax.axvline(tipping_point_time, color='red', linestyle=':', lw=2, label='Tipping Point')

handles, labels = axs[0].get_legend_handles_labels()
by_label = dict(zip(labels, handles))
fig.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(0.95, 0.95))
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()