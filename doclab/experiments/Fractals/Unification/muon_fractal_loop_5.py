import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("DUAL_POTENTIAL_REACTOR")

class DualPotentialReactor:
    def __init__(self, cycles=12):
        self.cycles = cycles
        self.dt = 0.005
        
        # --- GEOMETRY & BOUNDARIES ---
        self.r_inner = 0.5   # Switch to Ejection
        self.r_outer = 12.0  # Switch to Capture (The Wall)
        
        # --- POTENTIAL PARAMETERS ---
        self.coupling = 1.0  # The Hénon-Heiles "Twist"
        self.wall_strength = 0.002 # Soft wall to catch it at r~12
        
        # --- DISSIPATION ---
        # We still need some drag in Proton phase to ensure it actually falls into the well
        # otherwise it orbits forever.
        self.friction = 0.02
        
    def get_forces(self, m, l, phase):
        r2 = m**2 + l**2
        
        # Base Gradients (dV/dm, dV/dl)
        # Harmonic: 0.5*r^2 -> m, l
        # Cubic: coupling*(m^2*l - l^3/3)
        #   d/dm: 2*m*l
        #   d/dl: m^2 - l^2
        # Quartic (Wall): alpha * (r^2)^2 -> alpha * r^4
        #   d/dm: 4 * alpha * r^2 * m
        #   d/dl: 4 * alpha * r^2 * l
        
        grad_harmonic_m = m
        grad_harmonic_l = l
        
        grad_cubic_m = 2 * self.coupling * m * l
        grad_cubic_l = self.coupling * (m**2 - l**2)
        
        grad_wall_m = 4 * self.wall_strength * r2 * m
        grad_wall_l = 4 * self.wall_strength * r2 * l
        
        if phase == "PROTON":
            # POSITIVE POTENTIAL (Well)
            # F = -Gradient
            fm = -(grad_harmonic_m + grad_cubic_m + grad_wall_m)
            fl = -(grad_harmonic_l + grad_cubic_l + grad_wall_l)
            
        elif phase == "MUON":
            # NEGATIVE CORE POTENTIAL (Hill) + POSITIVE WALL
            # We flip the Harmonic and Cubic terms to create a "Hill"
            # But we keep the Wall positive to catch it.
            
            # V_muon = -0.5*r^2 - cubic + wall
            # F_muon = -(-grad_harmonic - grad_cubic + grad_wall)
            #        = grad_harmonic + grad_cubic - grad_wall
            
            fm = (grad_harmonic_m + grad_cubic_m) - grad_wall_m
            fl = (grad_harmonic_l + grad_cubic_l) - grad_wall_l
            
        return fm, fl

    def run_simulation(self):
        logger.info(f"[-] INITIALIZING DUAL POTENTIAL REACTOR ({self.cycles} Cycles)...")
        
        m_hist, l_hist = [], []
        r_hist, e_hist, p_hist = [], [], []
        
        # Initial State: Proton Phase (Falling In)
        # Start near the Wall
        theta = 0.5
        m = 10.0 * np.cos(theta)
        l = 10.0 * np.sin(theta)
        
        # Initial Velocity
        vm, vl = 0.0, 0.0
        
        phase = "PROTON"
        cycle_count = 0
        total_steps = 0
        max_steps = 300000 
        
        while cycle_count < self.cycles and total_steps < max_steps:
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
            
            # --- PHASE SWITCHING ---
            if phase == "PROTON":
                # Job: Fall into the well
                # Switch: If we hit the bottom (singularity)
                if r < self.r_inner:
                    phase = "MUON"
                    # No artificial energy kick needed!
                    # The potential inversion turns the well into a hill.
                    # We just nudge it slightly so it's not perfectly balanced on the peak.
                    m *= 1.05
                    l *= 1.05
                    
            elif phase == "MUON":
                # Job: Slide down the hill (Eject)
                # Switch: If we hit the wall (Outer Boundary)
                # We detect the turnaround point where radial velocity goes to zero?
                # Or just a fixed radius? Let's use fixed radius for robustness.
                if r > self.r_outer:
                    phase = "PROTON"
                    cycle_count += 1
                    # No artificial reset needed!
                    # We are at the wall, high potential energy.
                    # Switching to Proton turns the Hill into a Well.
                    # Gravity takes over immediately.
            
            # --- PHYSICS ---
            fm, fl = self.get_forces(m, l, phase)
            
            # Add Friction ONLY in Proton phase (Drag/Carving)
            if phase == "PROTON":
                fm -= self.friction * vm
                fl -= self.friction * vl
            
            # Symplectic Euler
            vm += fm * self.dt
            vl += fl * self.dt
            
            m += vm * self.dt
            l += vl * self.dt
            
            total_steps += 1
            
        return np.array(m_hist), np.array(l_hist), np.array(r_hist), np.array(e_hist), np.array(p_hist)

    def render(self):
        m, l, r, e, p = self.run_simulation()
        
        logger.info("[-] Visualizing Dual Potential Dynamics...")
        
        fig = plt.figure(figsize=(14, 10), facecolor='#050505')
        gs = fig.add_gridspec(2, 2)
        
        # PLOT 1: Trajectory
        ax1 = fig.add_subplot(gs[:, 0], facecolor='#000000')
        points = np.array([m, l]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        cmap = LinearSegmentedColormap.from_list("phase", ["#00ffff", "#ff00ff"]) # Cyan (Proton) -> Magenta (Muon)
        
        lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(0, 1))
        lc.set_array(p)
        lc.set_linewidth(0.8)
        ax1.add_collection(lc)
        
        ax1.set_xlim(-15, 15)
        ax1.set_ylim(-15, 15)
        ax1.set_aspect('equal')
        ax1.axis('off')
        
        # Draw Wall
        wall = plt.Circle((0,0), self.r_outer, color='white', fill=False, ls='--', alpha=0.3)
        ax1.add_artist(wall)
        ax1.set_title("Trajectory: Well (Cyan) vs Hill (Magenta)", color='white')

        # PLOT 2: Energy
        ax2 = fig.add_subplot(gs[0, 1], facecolor='#000000')
        steps = np.arange(len(e))
        ax2.plot(steps, e, color='white', lw=0.5)
        ax2.scatter(steps[::50], e[::50], c=p[::50], cmap=cmap, s=2)
        ax2.set_title("Kinetic Energy Cycle", color='white')
        ax2.tick_params(colors='white')
        
        # PLOT 3: Radius
        ax3 = fig.add_subplot(gs[1, 1], facecolor='#000000')
        ax3.plot(steps, r, color='gray', lw=0.5)
        ax3.scatter(steps[::50], r[::50], c=p[::50], cmap=cmap, s=2)
        ax3.set_title("Radial Breathing Mode", color='white')
        ax3.tick_params(colors='white')
        
        plt.tight_layout()
        plt.savefig("dual_potential_reactor.png", dpi=150)
        logger.info("[+] Diagram Saved: 'dual_potential_reactor.png'")
        plt.show()

if __name__ == "__main__":
    reactor = DualPotentialReactor(cycles=10)
    reactor.render()