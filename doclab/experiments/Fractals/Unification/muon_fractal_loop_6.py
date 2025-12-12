import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("KNOT_TOPOLOGY")

class KnotTopologyReactor:
    def __init__(self, knots=7, cycles=8):
        self.knots = knots  # The "Depth Level" (5, 7, 13...)
        self.cycles = cycles
        self.dt = 0.005
        
        # --- GEOMETRY ---
        self.r_inner = 0.5   # Switch to Ejection
        self.r_outer = 16.0  # The Containment Wall
        
        # --- POTENTIAL PARAMETERS ---
        self.coupling = 0.05 # Strength of the knot lobes (Lower for higher n to avoid instability)
        self.wall_strength = 0.0001
        self.friction = 0.03 # Drag for "Carving"
        
    def get_forces(self, m, l, phase):
        # Using Complex Coordinates for N-fold symmetry
        z = m + 1j * l
        r = np.abs(z)
        
        # 1. Harmonic Term (The Bowl)
        # V_h = 0.5 * r^2
        # F_h = -z
        f_harmonic = -z
        
        # 2. Knot Term (The N-Lobes)
        # V_k = (coupling / n) * Re(z^n)
        # Force is related to the conjugate of the derivative
        # d/dz (z^n/n) = z^(n-1)
        # Gradient of Re(f(z)) is conjugate(f'(z))
        # So Force_k = -coupling * conj(z^(n-1))
        if r > 1e-6: # Avoid singularity at 0
            d_knot = self.coupling * np.conj(z**(self.knots - 1))
            f_knot = -d_knot
        else:
            f_knot = 0j
            
        # 3. Wall Term (Containment)
        # V_w = wall * r^4
        # F_w = -4 * wall * r^2 * z
        f_wall = -4 * self.wall_strength * (r**2) * z
        
        # --- PHASE LOGIC ---
        if phase == "PROTON":
            # Forward Time: Positive Potential
            # F = F_harmonic + F_knot + F_wall (Drag added in loop)
            # The "Knot" term creates the attractive wells (lobes)
            f_total = f_harmonic + f_knot + f_wall
            
        elif phase == "MUON":
            # Retrograde Time: Inverted Potential
            # V_muon = -V_harmonic - V_knot + V_wall
            # We invert the geometry but keep the wall to catch it.
            # This turns Wells into Spires and Ridges into Valleys (Braiding Channels).
            f_total = -f_harmonic - f_knot + f_wall
            
        return np.real(f_total), np.imag(f_total)

    def run_simulation(self):
        logger.info(f"[-] INITIALIZING KNOT SIMULATION ({self.knots}-Fold Symmetry)...")
        
        m_hist, l_hist = [], []
        r_hist, e_hist, p_hist = [], [], []
        
        # Initial State
        # Start offset to fall into a specific lobe
        theta_start = np.pi / self.knots + 0.1 # Slightly off-axis to induce spiral
        start_r = 12.0
        m = start_r * np.cos(theta_start)
        l = start_r * np.sin(theta_start)
        
        vm, vl = 0.0, 0.0
        
        phase = "PROTON"
        cycle_count = 0
        total_steps = 0
        max_steps = 300000 
        
        while cycle_count < self.cycles and total_steps < max_steps:
            z = m + 1j*l
            r = np.abs(z)
            v_sq = vm**2 + vl**2
            ke = 0.5 * v_sq
            
            if total_steps % 20 == 0:
                m_hist.append(m)
                l_hist.append(l)
                r_hist.append(r)
                e_hist.append(ke)
                p_hist.append(0 if phase == "PROTON" else 1)
            
            # --- SWITCHING ---
            if phase == "PROTON":
                if r < self.r_inner:
                    phase = "MUON"
                    # Slight nudge to ensure it doesn't get stuck on the "Spire" tip
                    # We rotate it slightly to guide it into a "Valley" (Braiding channel)
                    # The valley is pi/n away from the lobe.
                    # Actually, simply inverting the potential turns the Lobe (Well) into a Spire.
                    # It will naturally roll off. The "Ridge" between lobes becomes the "Valley".
                    # So it should exit *between* the entry paths.
                    m *= 1.1; l *= 1.1
                    
            elif phase == "MUON":
                if r > self.r_outer:
                    phase = "PROTON"
                    cycle_count += 1
                    # It hit the wall. Gravity takes over.
            
            # --- PHYSICS ---
            fm, fl = self.get_forces(m, l, phase)
            
            if phase == "PROTON":
                fm -= self.friction * vm
                fl -= self.friction * vl
            
            # Integration
            vm += fm * self.dt
            vl += fl * self.dt
            m += vm * self.dt
            l += vl * self.dt
            
            total_steps += 1
            
        return np.array(m_hist), np.array(l_hist), np.array(p_hist)

    def render(self):
        m, l, p = self.run_simulation()
        
        logger.info("[-] Visualizing Knot Topology...")
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='#050505')
        
        # 1. Background Potential (Visual Guide)
        grid_limit = 18
        x = np.linspace(-grid_limit, grid_limit, 400)
        y = np.linspace(-grid_limit, grid_limit, 400)
        M, L = np.meshgrid(x, y)
        Z = M + 1j*L
        # V = 0.5 r^2 + Re(z^n)/n
        V = 0.5*np.abs(Z)**2 + (self.coupling/self.knots)*np.real(Z**self.knots)
        ax.contour(M, L, V, levels=30, colors='white', alpha=0.1, linewidths=0.5)
        
        # 2. Trajectory
        points = np.array([m, l]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        # Cyan (Proton/In) -> Magenta (Muon/Out)
        cmap = LinearSegmentedColormap.from_list("phase", ["#00ffff", "#ff00ff"]) 
        
        lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(0, 1))
        lc.set_array(p)
        lc.set_linewidth(1.0)
        lc.set_alpha(0.8)
        ax.add_collection(lc)
        
        ax.set_xlim(-grid_limit, grid_limit)
        ax.set_ylim(-grid_limit, grid_limit)
        ax.set_aspect('equal')
        ax.axis('off')
        
        ax.set_title(f"Knot Topology ({self.knots}-Fold Braiding)\nCyan=Carving (In) | Magenta=Resolving (Out)", color='white', fontsize=14)
        
        plt.tight_layout()
        plt.savefig("knot_topology_reactor.png", dpi=150)
        logger.info("[+] Output Saved: 'knot_topology_reactor.png'")
        plt.show()

if __name__ == "__main__":
    # The user asked for 5, 7, or 13. Let's do 7 for high complexity.
    reactor = KnotTopologyReactor(knots=7, cycles=6)
    reactor.render()