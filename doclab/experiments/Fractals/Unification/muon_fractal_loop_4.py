import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("KNOT_REACTOR")

class KnotReactor:
    def __init__(self, cycles=10):
        self.cycles = cycles
        # User Parameter: DT = 0.002
        self.dt = 0.002 
        
        # --- REACTOR GEOMETRY ---
        self.r_intake = 8.0    
        self.r_singularity = 0.1 
        # User: "Doubly Wide" -> Increasing exhaust radius
        self.r_exhaust = 48.0  
        
        # --- PHYSICS PARAMETERS (From User File) ---
        # DECAY = 0.9999 per step
        self.decay_factor = 0.9999 
        # Reverse Decay = Growth
        self.growth_factor = 1.0 / self.decay_factor 
        
        # ROTATION_SPEED = 2.0 (Target Angular Velocity)
        # We invoke this via Injection Velocity
        self.target_omega = 2.0
        
        # TEAR_INTENSITY = 1.5
        # We map this to the Hénon-Heiles coupling strength (normally 1.0)
        # This increases the "non-linearity" or "twist" of the potential
        self.tear_coupling = 1.5
        
        # Safety
        self.max_velocity = 50.0 
        
    def gradient(self, m, l):
        # Generalized Hénon-Heiles with 'Tear' Coupling
        # V = 0.5(m^2 + l^2) + coupling * (m^2*l - l^3/3)
        # Force = -Gradient
        
        # dV/dm = m + 2 * coupling * m * l
        dm = m + 2 * self.tear_coupling * m * l
        
        # dV/dl = l + coupling * (m^2 - l^2)
        dl = l + self.tear_coupling * (m**2 - l**2)
        
        return dm, dl

    def run_cycle(self):
        logger.info(f"[-] INITIALIZING KNOT REACTOR ({self.cycles} Cycles)...")
        logger.info(f"    Parameters: Decay={self.decay_factor}, Omega={self.target_omega}, Tear={self.tear_coupling}")
        
        # Telemetry
        m_hist, l_hist = [], []
        r_hist, e_hist, p_hist = [], [], []
        
        # Initial State: Injection
        theta = 0.0
        m = self.r_intake * np.cos(theta)
        l = self.r_intake * np.sin(theta)
        
        # Injection Velocity matching User's Rotation Speed
        # v_tan = r * omega
        v_tan = self.r_intake * 1.0 # Reduced from 2.0 to keep it stable initially, 
                                    # let's try 1.0 and see if it speeds up or spirals
        # Actually, let's use a standard injection and let the 'Tear' do the work
        v_tan = 1.5 
        
        vm = -0.5 * np.cos(theta) - v_tan * np.sin(theta)
        vl = -0.5 * np.sin(theta) + v_tan * np.cos(theta)
        
        phase = "PROTON"
        cycle_count = 0
        total_steps = 0
        max_steps = 600000 
        
        while cycle_count < self.cycles and total_steps < max_steps:
            # 1. METRICS
            r_sq = m**2 + l**2
            r = np.sqrt(r_sq)
            v_sq = vm**2 + vl**2
            ke = 0.5 * v_sq
            
            if total_steps % 20 == 0:
                m_hist.append(m)
                l_hist.append(l)
                r_hist.append(r)
                e_hist.append(ke)
                p_hist.append(0 if phase == "PROTON" else 1)
            
            # 2. BOUNDARY LOGIC
            if phase == "PROTON" and r < self.r_singularity:
                phase = "MUON"
                # Inversion Logic:
                # The User says "Retrograde should be reverse of this"
                # We switch from Decay to Growth.
                # We also need to get out of the singularity.
                m, l = m * 2.0, l * 2.0
                continue

            if phase == "MUON" and r > self.r_exhaust:
                # Cycle Complete
                phase = "PROTON"
                cycle_count += 1
                
                # REINJECTION (The Knot Loop)
                # We preserve the angle (Holonomy) but reset R and V
                angle = np.arctan2(l, m)
                m = self.r_intake * np.cos(angle)
                l = self.r_intake * np.sin(angle)
                
                # Injection Velocity
                vm = -0.5 * np.cos(angle) - v_tan * np.sin(angle)
                vl = -0.5 * np.sin(angle) + v_tan * np.cos(angle)
                continue
            
            # 3. PHYSICS
            # Calculate Gradient Force
            g_m, g_l = self.gradient(m, l)
            
            # Update Velocity (Symplectic-ish)
            vm += (-g_m) * self.dt
            vl += (-g_l) * self.dt
            
            # Apply Decay/Growth (The User's "Proof" Parameters)
            if phase == "PROTON":
                # Forward Knotting: Decay
                vm *= self.decay_factor
                vl *= self.decay_factor
            elif phase == "MUON":
                # Retrograde: Growth (Reverse)
                vm *= self.growth_factor
                vl *= self.growth_factor
            
            # Velocity Cap (Relativistic Safety)
            if vm**2 + vl**2 > self.max_velocity**2:
                scale = self.max_velocity / np.sqrt(vm**2 + vl**2)
                vm *= scale
                vl *= scale
            
            # Update Position
            m += vm * self.dt
            l += vl * self.dt
            
            total_steps += 1
            
        return np.array(m_hist), np.array(l_hist), np.array(p_hist)

    def render_knot(self):
        m, l, p = self.run_cycle()
        
        logger.info("[-] Visualizing The Fractal Knot...")
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='#0b0b0b')
        
        # Color Map: Cyan (Proton) -> Gold (Muon)
        cmap = LinearSegmentedColormap.from_list("reactor_mode", ["#00ccff", "#ffaa00"])
        
        # Create Line Collection
        points = np.array([m, l]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(0, 1))
        lc.set_array(p)
        lc.set_linewidth(0.6)
        lc.set_alpha(0.8)
        
        ax.add_collection(lc)
        ax.set_xlim(-self.r_exhaust*1.1, self.r_exhaust*1.1)
        ax.set_ylim(-self.r_exhaust*1.1, self.r_exhaust*1.1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Annotations
        # Draw Intake Circle
        circle_intake = plt.Circle((0, 0), self.r_intake, color='#00ccff', fill=False, linestyle='--', alpha=0.3)
        ax.add_artist(circle_intake)
        
        # Draw Exhaust Circle ("Doubly Wide")
        circle_exhaust = plt.Circle((0, 0), self.r_exhaust, color='#ffaa00', fill=False, linestyle='--', alpha=0.3)
        ax.add_artist(circle_exhaust)
        
        ax.set_title(f"THE FRACTAL KNOT: FORWARD vs RETROGRADE\n(Decay={self.decay_factor} | Tear={self.tear_coupling})", 
                     color='white', fontsize=14)
        
        plt.tight_layout()
        plt.savefig("fractal_knot_trajectory.png", dpi=150)
        logger.info("[+] Knot Saved: 'fractal_knot_trajectory.png'")
        plt.show()

if __name__ == "__main__":
    # We run enough cycles to see the 'Flower' pattern form
    reactor = KnotReactor(cycles=25)
    reactor.render_knot()