import numpy as np
import matplotlib.pyplot as plt
from pirouette_engine import PirouetteEngine # Import our upgraded engine

# --- 1. The Diorama Matrix: Define the Players ---

# Phase Goals (what each entity is trying to achieve)
GOAL_MAINTAIN_BORDERS = np.deg2rad(0)   # The traditional Roman ideal
GOAL_CONSOLIDATE_POWER = np.deg2rad(30)  # A pragmatic shift in focus
GOAL_ACQUIRE_TERRITORY = np.deg2rad(-45) # An external, challenging goal

diorama_matrix = [
    PirouetteEngine(
        name='West',
        initial_Ta=0.8,    # Lower stability due to crises, overextension
        initial_Gamma=1.2, # High initial power, but brittle
        initial_Phi=GOAL_MAINTAIN_BORDERS
    ),
    PirouetteEngine(
        name='East',
        initial_Ta=1.1,    # More stable, better administration
        initial_Gamma=1.0, # Strong, but more compact and defensible
        initial_Phi=GOAL_MAINTAIN_BORDERS # Starts aligned with the West
    ),
    PirouetteEngine(
        name='Migrating Tribes',
        initial_Ta=0.5,    # Chaotic, non-state actor
        initial_Gamma=0.3, # Low initial power, but will grow
        initial_Phi=GOAL_ACQUIRE_TERRITORY
    )
]

# --- 2. The Interaction Physics & Scenario Logic ---

def update_interactions(matrix, time):
    """Calculates all external forces between entities."""
    ALIGNMENT_STRENGTH = 0.5
    PRESSURE_STRENGTH = 0.3
    
    # --- Scenario-Specific Dynamics ---
    # The Migrating Tribes gain influence over time, simulating demographic/military growth
    tribes = next(c for c in matrix if c.name == 'Migrating Tribes')
    tribes_gamma_growth = 0.0005 * time 
    tribes.ext_Gamma_ddot = tribes_gamma_growth

    for cavity in matrix:
        cavity.ext_Ta_ddot, cavity.ext_Gamma_ddot, cavity.ext_Phi_ddot = 0.0, 0.0, 0.0
        # Add the growth factor for the tribes specifically
        if cavity.name == 'Migrating Tribes':
            cavity.ext_Gamma_ddot += tribes_gamma_growth

        for other_cavity in matrix:
            if cavity is other_cavity: continue

            # Phase alignment force: entities pull each other toward their goals
            phase_difference = other_cavity.Phi - cavity.Phi
            phase_force = ALIGNMENT_STRENGTH * np.sin(phase_difference) * other_cavity.Gamma
            cavity.ext_Phi_ddot += phase_force

            # Gamma pressure: Stronger entities exert pressure on weaker ones
            gamma_difference = other_cavity.Gamma - cavity.Gamma
            # This pressure is felt most when goals are opposed (cos is negative)
            cos_phase_diff = np.cos(phase_difference)
            gamma_force = PRESSURE_STRENGTH * gamma_difference * (1 - cos_phase_diff)
            
            # The West is uniquely vulnerable to pressure from the Tribes
            if cavity.name == 'West' and other_cavity.name == 'Migrating Tribes':
                 cavity.ext_Gamma_ddot -= gamma_force * 2.0 # Extra vulnerability
            else:
                 cavity.ext_Gamma_ddot -= gamma_force


# --- 3. Run the Simulation ---
print("Simulating the fracture of the Roman Empire...")
total_time = 400 # Represents ~400 years
dt = 0.2
steps = int(total_time / dt)
time_axis = np.linspace(0, total_time, steps + 1)

# Set the East's true goal as a potential it's trying to reach
east = next(c for c in diorama_matrix if c.name == 'East')
east_potential = lambda Ta, Gamma, Phi: 0.1 * (Phi - GOAL_CONSOLIDATE_POWER)**2
east.set_parameters(potential_func=east_potential)


for i in range(steps):
    t = i * dt
    update_interactions(diorama_matrix, t)
    for cavity in diorama_matrix:
        cavity.step(dt)
        cavity.record_history()
print("Simulation complete.")

# --- 4. Visualization & Analysis ---
fig, axs = plt.subplots(3, 1, figsize=(15, 14), sharex=True)
colors = {'West': 'maroon', 'East': 'darkcyan', 'Migrating Tribes': 'goldenrod'}
styles = {'West': '-', 'East': '-', 'Migrating Tribes': '--'}
fig.suptitle('Pirouette Simulation: The Fracture of the Roman Empire', fontsize=18)

# Find the fracture point for visualization
west_phi = np.rad2deg(np.unwrap(diorama_matrix[0].history['Phi']))
east_phi = np.rad2deg(np.unwrap(diorama_matrix[1].history['Phi']))
phi_diff = np.abs(west_phi - east_phi)
fracture_idx = np.argmax(phi_diff > 45) # Point where goals differ by > 45 degrees
fracture_time = fracture_idx * dt if fracture_idx > 0 else -1

# Phase Plot
axs[0].set_title('Phase ($\phi$): The Great Schism of Imperial Goals', fontsize=12)
for cavity in diorama_matrix:
    phase_degrees = np.rad2deg(np.unwrap(cavity.history['Phi']))
    axs[0].plot(time_axis, phase_degrees, label=cavity.name, color=colors[cavity.name], linestyle=styles[cavity.name], lw=2)
axs[0].set_ylabel('Goal Alignment (Degrees)')

# Gamma Plot
axs[1].set_title('Gladiator Force ($\Gamma$): The Balance of Imperial & External Power', fontsize=12)
for cavity in diorama_matrix:
    axs[1].plot(time_axis, cavity.history['Gamma'], label=cavity.name, color=colors[cavity.name], linestyle=styles[cavity.name], lw=2)
axs[1].set_ylabel('Relative Power / Control')

# Ta Plot
axs[2].set_title('Time-Adherence ($T_a$): Imperial Stability & Coherence', fontsize=12)
for cavity in diorama_matrix:
    axs[2].plot(time_axis, cavity.history['Ta'], label=cavity.name, color=colors[cavity.name], linestyle=styles[cavity.name], lw=2)
axs[2].set_ylabel('System Stability')
axs[2].set_xlabel('Time (Years, arbitrary start)')

for ax in axs:
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.legend()
    if fracture_time > 0:
        ax.axvline(fracture_time, color='red', linestyle='--', lw=2, label=f'Fracture Point (~{fracture_time:.0f} years)')
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()