import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("REACTOR_CORE")

class ManifoldReactor:
    def __init__(self, cycles=5):
        self.cycles = cycles
        self.dt = 0.01
        
        # --- REACTOR SETTINGS ---
        # The radius where we hand off particles
        self.proton_intake_r = 8.0   # Start of Compression
        self.singularity_r = 0.05    # The Inversion Point
        self.muon_exhaust_r = 240000000000.0   # End of Expansion
        
        # Physics Parameters
        self.proton_friction = 0.08  # Compressive drag
        self.muon_pressure = 0.15    # Explosive retrograde force
        self.coupling_efficiency = 0.95 # Energy loss at the inversion point
        
    def gradient(self, m, l):
        # Hénon-Heiles Potential Gradient (The shape of the manifold)
        dm = m + 2 * m * l
        dl = l + m**2 - l**2
        return dm, dl

    def run_reactor(self):
        logger.info("[-] IGNITING FRACTAL LOOP REACTOR...")
        
        # Data storage for the Phase Diagram
        # We track Radius (r) vs Energy (E)
        history_r = []
        history_e = []
        history_phase = [] # 0=Proton, 1=Muon
        
        # Initial State: A particle falling into the Proton
        m, l = self.proton_intake_r, 0.0
        vm, vl = -0.5, 0.0 # Initial inward velocity
        
        phase = "PROTON" # Current Manifold Mode
        total_energy_generated = 0.0
        
        step = 0
        max_steps = 10000
        
        while step < max_steps:
            r = np.sqrt(m**2 + l**2)
            ke = 0.5 * (vm**2 + vl**2)
            
            # --- RECORD TELEMETRY ---
            history_r.append(r)
            history_e.append(ke)
            history_phase.append(0 if phase == "PROTON" else 1)
            
            # --- PHYSICS ENGINE SWITCHER ---
            
            # 1. Calculate Base Potential Forces
            grad_m, grad_l = self.gradient(m, l)
            
            if phase == "PROTON":
                # COMPRESSION PHASE
                # Force = Gravity - Friction (Drag)
                # We want it to spiral IN.
                fm = -grad_m - (self.proton_friction * vm)
                fl = -grad_l - (self.proton_friction * vl)
                
                # CHECK: Did we hit the Inversion Point?
                if r < self.singularity_r:
                    logger.info(f"    [!] SINGULARITY REACHED (Step {step}). INVERTING GEOMETRY.")
                    phase = "MUON"
                    # Apply Coupling Efficiency (Energy Loss at the 'Wound')
                    vm *= self.coupling_efficiency
                    vl *= self.coupling_efficiency
                    
                    # Teleport slightly outward to prevent div/0 errors
                    m, l = m * 1.5, l * 1.5 
            
            elif phase == "MUON":
                # EXPANSION PHASE
                # Force = Gravity + Retrograde Pressure (Expansion)
                # We want it to blast OUT.
                fm = -grad_m + (self.muon_pressure * m)
                fl = -grad_l + (self.muon_pressure * l)
                
                # CHECK: Did we hit the Decay Horizon?
                if r > self.muon_exhaust_r:
                    logger.info(f"    [+] CYCLE COMPLETE (Step {step}). RECYCLING.")
                    phase = "PROTON"
                    # Measure Energy Gain
                    total_energy_generated += ke
                    
                    # LOOP RESET:
                    # We strip the energy (Harvesting) and drop it back in the proton well
                    # This simulates a 'Closed Loop' engine
                    factor = self.proton_intake_r / r
                    m *= factor
                    l *= factor
                    # Reset velocity to 'cold' intake speed
                    norm_v = np.sqrt(vm**2 + vl**2)
                    vm = (vm / norm_v) * 0.5
                    vl = (vl / norm_v) * 0.5
            
            # --- INTEGRATION (Verlet) ---
            vm += fm * self.dt
            vl += fl * self.dt
            m += vm * self.dt
            l += vl * self.dt
            
            step += 1
            
            # Failsafe for runaway energy
            if ke > 5000:
                logger.warning("    [!] CRITICAL MASS EXCEEDED. REACTOR SCRAM.")
                break

        return np.array(history_r), np.array(history_e), np.array(history_phase)

    def render_diagram(self):
        r, e, p = self.run_reactor()
        
        logger.info("[-] Plotting Reactor Phase Diagram...")
        
        fig, ax = plt.subplots(figsize=(14, 8), facecolor='#0b0b0b')
        ax.set_facecolor('#0b0b0b')
        
        # Plot the Trajectory
        # Color code by Phase: Cyan = Proton (Compression), Gold = Muon (Expansion)
        
        # Create segments for multicolor line
        from matplotlib.collections import LineCollection
        points = np.array([r, e]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        # Custom Colormap based on phase array
        cmap = LinearSegmentedColormap.from_list("reactor_mode", ["#00ccff", "#ffaa00"])
        lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(0, 1))
        lc.set_array(p)
        lc.set_linewidth(2)
        
        ax.add_collection(lc)
        ax.set_xlim(0, 26)
        ax.set_ylim(0, np.max(e) * 1.1)
        
        # Annotations
        ax.axvline(self.proton_intake_r, color='#00ccff', linestyle=':', alpha=0.5)
        ax.text(self.proton_intake_r, np.max(e)*0.9, "Proton Intake\n(r=8)", color='#00ccff', ha='center')
        
        ax.axvline(self.muon_exhaust_r, color='#ffaa00', linestyle=':', alpha=0.5)
        ax.text(self.muon_exhaust_r, np.max(e)*0.9, "Muon Exhaust\n(r=24)", color='#ffaa00', ha='center')
        
        ax.set_xlabel("Manifold Radius (r)", color='white', fontsize=12)
        ax.set_ylabel("Kinetic Energy (E)", color='white', fontsize=12)
        ax.set_title("FRACTAL LOOP REACTOR: PHASE DIAGRAM\nCyan=Compression (Proton) | Gold=Expansion (Muon)", color='white', fontsize=14)
        
        ax.tick_params(colors='white')
        ax.grid(color='#333333', linestyle=':')
        
        plt.tight_layout()
        plt.savefig("reactor_phase_loop.png", dpi=150)
        logger.info("[+] Diagram Saved: 'reactor_phase_loop.png'")
        plt.show()

if __name__ == "__main__":
    reactor = ManifoldReactor()
    reactor.render_diagram()