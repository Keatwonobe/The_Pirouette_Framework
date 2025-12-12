import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("EXTREME_REACTOR")

class ExtremeReactor:
    def __init__(self):
        self.dt = 0.01
        
        # --- EXTREME RANGE SETTINGS ---
        self.proton_intake_r = 8.0
        self.singularity_r = 0.05
        self.muon_exhaust_r = 2000.0   # CHECKING "WAY FARTHER"
        
        # Physics
        self.proton_friction = 0.08
        self.muon_pressure = 0.15 
        self.coupling_efficiency = 0.95
        
    def gradient(self, m, l):
        dm = m + 2 * m * l
        dl = l + m**2 - l**2
        return dm, dl

    def run_reactor(self):
        logger.info("[-] IGNITING LONG-RANGE FRACTAL REACTOR...")
        
        history_r = []
        history_e = []
        history_phase = [] # 0=Proton, 1=Muon
        
        # Start at Intake
        m, l = self.proton_intake_r, 0.0
        vm, vl = -0.5, 0.0
        
        phase = "PROTON"
        step = 0
        max_steps = 100000 # Need more steps for long distance
        
        while step < max_steps:
            r = np.sqrt(m**2 + l**2)
            ke = 0.5 * (vm**2 + vl**2)
            
            history_r.append(r)
            history_e.append(ke)
            history_phase.append(0 if phase == "PROTON" else 1)
            
            # --- PHYSICS ---
            grad_m, grad_l = self.gradient(m, l)
            
            if phase == "PROTON":
                # Compression
                fm = -grad_m - (self.proton_friction * vm)
                fl = -grad_l - (self.proton_friction * vl)
                
                if r < self.singularity_r:
                    phase = "MUON"
                    vm *= self.coupling_efficiency
                    vl *= self.coupling_efficiency
                    m, l = m * 1.5, l * 1.5 # Pop out of singularity
            
            elif phase == "MUON":
                # Extreme Expansion
                fm = -grad_m + (self.muon_pressure * m)
                fl = -grad_l + (self.muon_pressure * l)
                
                if r > self.muon_exhaust_r:
                    logger.info(f"    [+] MAXIMUM RANGE REACHED at Step {step}")
                    break
            
            # Integration
            vm += fm * self.dt
            vl += fl * self.dt
            m += vm * self.dt
            l += vl * self.dt
            
            step += 1
            
        return np.array(history_r), np.array(history_e), np.array(history_phase)

    def render(self):
        r, e, p = self.run_reactor()
        
        logger.info(f"[-] Peak Energy Generated: {np.max(e):.2e}")
        logger.info("[-] Plotting Extreme Phase Diagram...")
        
        fig, ax = plt.subplots(figsize=(14, 8), facecolor='#050505')
        ax.set_facecolor('#050505')
        
        # Line Collection for Multicolor
        points = np.array([r, e]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        cmap = LinearSegmentedColormap.from_list("reactor_mode", ["#00ccff", "#ffaa00"])
        
        lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(0, 1))
        lc.set_array(p)
        lc.set_linewidth(2.5)
        ax.add_collection(lc)
        
        ax.set_xlim(0, self.muon_exhaust_r)
        ax.set_yscale('log') # LOG SCALE IS NECESSARY
        ax.set_ylim(1e-1, np.max(e)*2)
        
        # Annotations
        ax.axvline(self.proton_intake_r, color='#00ccff', linestyle='--', alpha=0.3)
        ax.text(self.proton_intake_r, 1e0, "Proton Intake (r=8)", color='#00ccff', rotation=90, verticalalignment='bottom')
        
        # Peak Marker
        peak_e = np.max(e)
        peak_r = r[np.argmax(e)]
        ax.plot(peak_r, peak_e, 'ro')
        ax.text(peak_r, peak_e, f" PEAK OUTPUT\n {peak_e:.2e} Joules", color='white', ha='right')

        ax.set_xlabel("Manifold Radius (r)", color='white', fontsize=12)
        ax.set_ylabel("Kinetic Energy (Log Scale)", color='white', fontsize=12)
        ax.set_title(f"EXTREME REACTOR OUTPUT (Range r={self.muon_exhaust_r})", color='white', fontsize=16)
        
        ax.tick_params(colors='white', which='both')
        ax.grid(color='#333333', linestyle=':', which='both')
        
        plt.tight_layout()
        plt.savefig("reactor_extreme_range.png", dpi=150)
        logger.info("[+] Diagram Saved: 'reactor_extreme_range.png'")
        plt.show()

if __name__ == "__main__":
    reactor = ExtremeReactor()
    reactor.render()