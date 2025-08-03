import numpy as np
import matplotlib.pyplot as plt
from pirouette_engine import PirouetteCavity # Assumes the class is in this file

# --- 1. The Diorama Matrix: Define the Players ---

# We represent each player's goals with a Phase angle (in radians).
# Let's set the Croatan goal of "Integration" as our reference point: 0.0
# Survival for the colonists is close to this goal. Hostility is opposite.
GOAL_INTEGRATION = 0.0
GOAL_SURVIVAL = np.deg2rad(15)    # Slightly different from pure integration
GOAL_REPEL = np.deg2rad(180)  # Directly opposite integration

diorama_matrix = [
    # The English Colonists: Desperate, isolated, but hopeful for survival.
    PirouetteCavity(
        name='Colonists',
        initial_Ta=0.6,    # Low Ta: Sense of urgency, unstable supplies.
        initial_Gamma=0.5, # Low Gamma: Weak, confined, and isolated.
        initial_Phi=GOAL_SURVIVAL
    ),
    # The Croatan Tribe: Stable, strong, and open to alliance.
    PirouetteCavity(
        name='Croatan',
        initial_Ta=1.0,    # High Ta: Stable, in their element.
        initial_Gamma=1.2, # High Gamma: Strong, influential in their own land.
        initial_Phi=GOAL_INTEGRATION
    ),
    # The Secotan Tribes: Stable, strong, and hostile to the newcomers.
    PirouetteCavity(
        name='Secotan',
        initial_Ta=1.0,    # High Ta: Stable.
        initial_Gamma=1.0, # High Gamma: A significant regional force.
        initial_Phi=GOAL_REPEL
    )
]

# --- 2. The Interaction Physics: How Cavities Influence Each Other ---

def update_interactions(matrix):
    """
    Calculates the 'forces' (accelerations) on each cavity based on the others.
    This is the core of the multi-body simulation.
    """
    # Phase alignment strength (how strongly goals attract/repel)
    ALIGNMENT_STRENGTH = 0.8
    # Influence strength (how much Gamma disparity matters)
    INFLUENCE_STRENGTH = 0.5

    for cavity in matrix:
        # Reset accelerations for this time step
        cavity.Ta_ddot, cavity.Gamma_ddot, cavity.Phi_ddot = 0.0, 0.0, 0.0

        for other_cavity in matrix:
            if cavity is other_cavity:
                continue

            # --- Phase Interaction (Alignment of Goals) ---
            # The "force" to align goals is proportional to the cosine of their difference.
            # A small difference is a strong pull; a 180-degree difference is a strong push.
            phase_difference = other_cavity.Phi - cavity.Phi
            # Influence is weighted by the other cavity's strength (Gamma)
            phase_force = ALIGNMENT_STRENGTH * np.sin(phase_difference) * other_cavity.Gamma
            cavity.Phi_ddot += phase_force

            # --- Gamma Interaction (Influence/Pressure) ---
            # A stronger cavity (high Gamma) pushes a weaker one to become even weaker.
            # We model this as a pressure proportional to the difference in Gamma.
            gamma_difference = other_cavity.Gamma - cavity.Gamma
            gamma_force = INFLUENCE_STRENGTH * gamma_difference
            cavity.Gamma_ddot += gamma_force

            # --- Ta Interaction (Stability/Urgency) ---
            # A stable cavity (high Ta) tends to stabilize its neighbors.
            ta_difference = other_cavity.Ta - cavity.Ta
            ta_force = 0.1 * ta_difference # A weaker effect
            cavity.Ta_ddot += ta_force


# --- 3. Run the Simulation ---

print("Calibrating simulation to the Roanoke Colony historical event...")
total_time = 25.0
dt = 0.05
steps = int(total_time / dt)
time_axis = np.linspace(0, total_time, steps + 1)

for i in range(steps):
    update_interactions(diorama_matrix)
    for cavity in diorama_matrix:
        cavity.step(dt)
        cavity.record_history()
print("Simulation complete.")


# --- 4. Visualize the Outcome ---

fig, axs = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
fig.suptitle('Pirouette Simulation of the Roanoke Colony Dynamics', fontsize=18)
colors = {'Colonists': 'royalblue', 'Croatan': 'forestgreen', 'Secotan': 'firebrick'}

# Plot Phase (Goal Alignment)
axs[0].set_title('Phase ($\phi$): Evolution of Goals and Alliances', fontsize=12)
for cavity in diorama_matrix:
    # Convert phase back to degrees for intuitive plotting
    phase_degrees = np.rad2deg(np.unwrap(cavity.history['Phi']))
    axs[0].plot(time_axis, phase_degrees, label=cavity.name, color=colors[cavity.name], lw=2)
axs[0].axhline(np.rad2deg(GOAL_INTEGRATION), ls='--', c='forestgreen', alpha=0.7, label='Croatan Goal (Integration)')
axs[0].axhline(np.rad2deg(GOAL_REPEL), ls='--', c='firebrick', alpha=0.7, label='Secotan Goal (Repel)')
axs[0].set_ylabel('Goal Alignment (Degrees)')
axs[0].legend()

# Plot Gamma (Influence/Strength)
axs[1].set_title('Gladiator Force ($\Gamma$): Evolution of Power and Influence', fontsize=12)
for cavity in diorama_matrix:
    axs[1].plot(time_axis, cavity.history['Gamma'], label=cavity.name, color=colors[cavity.name], lw=2)
axs[1].set_ylabel('Relative Strength')
axs[1].legend()

# Plot Ta (Stability/Urgency)
axs[2].set_title('Time-Adherence ($T_a$): Evolution of Stability and Urgency', fontsize=12)
for cavity in diorama_matrix:
    axs[2].plot(time_axis, cavity.history['Ta'], label=cavity.name, color=colors[cavity.name], lw=2)
axs[2].set_ylabel('Stability Level')
axs[2].set_xlabel('Time (Arbitrary Units)')
axs[2].legend()

for ax in axs:
    ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()