import numpy as np
import matplotlib.pyplot as plt
from pirouette_engine import PirouetteEngine

class CunningEmpireSimulation:
    def __init__(self, actors, start_year, end_year, dt):
        self.actors = actors
        self.year = start_year
        self.end_year = end_year
        self.dt = dt
        self.time_axis = np.linspace(start_year, end_year, int((end_year - start_year) / dt) + 1)
        self.event_log = []
        # USA's secret project
        self.usa_hidden_tech_level = 0.0
        self.breakthrough_threshold = 100.0
        self.breakthrough_achieved = False

    def run(self):
        print("Executing the 'Cunning Empire' Simulation (2025-2100)...")
        steps = int((self.end_year - self.year) / self.dt)
        for i in range(steps):
            self.year = self.time_axis[i]
            self.update_interactions()
            for actor in self.actors:
                actor.step(self.dt)
                actor.record_history()
        print("Simulation complete.")

    def update_interactions(self):
        usa = next(a for a in self.actors if a.name == 'USA')
        biosphere = next(a for a in self.actors if a.name == 'Biosphere')
        
        # --- USA's Cunning Strategy ---
        if not self.breakthrough_achieved:
            # 1. Feign Weakness: Actively suppress its own coherence
            usa.ext_Ta_ddot -= 2.0 * (usa.Ta - 0.7) # Force Ta down to a low value
            
            # 2. Secretly Develop Tech: Channel power into the hidden project
            self.usa_hidden_tech_level += usa.Gamma * self.dt * 0.1
            
            # 3. Project Chaos: Use its high Gamma to sow discord
            for other in self.actors:
                if other.name not in ['USA', 'Biosphere', 'Innovation']:
                    other.ext_Ta_ddot -= 0.1 * usa.Gamma # A subtle coherence attack

            # 4. Check for Breakthrough
            if self.usa_hidden_tech_level >= self.breakthrough_threshold:
                self.breakthrough_achieved = True
                self.event_log.append(f"{self.year:.1f}: USA TECHNOLOGICAL BREAKTHROUGH.")
                # The Reveal: The mask comes off
                usa.Ta = 2.0 # Instant, superhuman coherence
                usa.Gamma = 3.0 # Power level unmatched
                usa.Phi = np.deg2rad(0) # It now dictates the global goal
        else:
            # Post-Breakthrough: Enforce dominance
            usa.ext_Ta_ddot = 10 * (2.0 - usa.Ta) # Lock Ta at a high value
            usa.ext_Gamma_ddot = 10 * (3.0 - usa.Gamma) # Lock Gamma
            for other in self.actors:
                if other.name not in ['USA', 'Biosphere']:
                    # Directly suppress rivals' power
                    other.ext_Gamma_ddot -= 2.0 * other.Gamma

        # --- Other Actors' Standard Logic ---
        # (Simplified from previous sim for clarity)
        human_gamma_total = sum(a.Gamma for a in self.actors if a.name != 'Biosphere')
        biosphere.ext_Ta_ddot -= 0.01 * human_gamma_total
        if biosphere.Ta < 1.0 and not any("Tipping Point" in e for e in self.event_log):
             self.event_log.append(f"{self.year:.1f}: Biosphere Tipping Point Reached.")

# --- Setup and Run ---
actors = [
    PirouetteEngine(name='USA', initial_Ta=1.0, initial_Gamma=1.5, initial_Phi=np.deg2rad(45)),
    PirouetteEngine(name='China', initial_Ta=1.4, initial_Gamma=1.2, initial_Phi=np.deg2rad(-90)),
    PirouetteEngine(name='Multipolar Bloc', initial_Ta=1.1, initial_Gamma=1.0, initial_Phi=np.deg2rad(120)),
    PirouetteEngine(name='Biosphere', initial_Ta=1.5, initial_Gamma=2.0, initial_Phi=np.deg2rad(0)),
]
sim_manager = CunningEmpireSimulation(actors, 2025, 2100, 0.1)
sim_manager.run()

# --- Plotting ---
fig, axs = plt.subplots(3, 1, figsize=(16, 18), sharex=True)
colors = {'USA': 'blue', 'China': 'goldenrod', 'Multipolar Bloc': 'red', 'Biosphere': 'green'}
styles = {'USA': '-', 'China': '--', 'Multipolar Bloc': '--', 'Biosphere': '-'}
fig.suptitle('The "Cunning Empire" Simulation: A Strategy of Deception', fontsize=20)

for actor in actors:
    axs[0].plot(sim_manager.time_axis, actor.history['Gamma'], color=colors[actor.name], linestyle=styles[actor.name], lw=2.5, label=actor.name)
    axs[1].plot(sim_manager.time_axis, actor.history['Ta'], color=colors[actor.name], linestyle=styles[actor.name], lw=2.5, label=actor.name)
    axs[2].plot(sim_manager.time_axis, np.rad2deg(np.unwrap(actor.history['Phi'])), color=colors[actor.name], linestyle=styles[actor.name], lw=2.5, label=actor.name)

axs[0].set_title('Gladiator Force ($\Gamma$): The Illusion of Decline and the Reality of Power', fontsize=14)
axs[0].set_ylabel('System Power')
axs[1].set_title('Time-Adherence ($T_a$): The Mask of Chaos and the Face of Control', fontsize=14)
axs[1].set_ylabel('System Stability')
axs[2].set_title('Phase ($\phi$): The War for Reality', fontsize=14)
axs[2].set_ylabel('Goal Alignment (Deg)')
axs[2].set_xlabel('Year')

for ax in axs:
    ax.grid(True, alpha=0.3)
    for event in sim_manager.event_log:
        year, desc = event.split(':', 1)
        ax.axvline(float(year), color='magenta', linestyle=':', lw=3)
        ax.text(float(year) + 1, ax.get_ylim()[0] * 0.9, desc.strip(), color='magenta', rotation=90, verticalalignment='bottom')

handles, labels = axs[0].get_legend_handles_labels()
by_label = dict(zip(labels, handles))
fig.legend(by_label.values(), by_label.keys(), loc='upper left')
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

print("\n--- Simulation Event Log ---")
for event in sim_manager.event_log:
    print(event)