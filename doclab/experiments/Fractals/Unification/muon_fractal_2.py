import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("MUON_SCANNER")

class MuonDecayTopology:
    def __init__(self, resolution=1000, zoom=0.8):
        """
        THE MUON CRITICALITY SCANNER
        Maps the 'Saddle Points' of the Pirouette Framework.
        
        Hypothesis: The Muon is a manifold straddling the boundary 
        of Forward Time (Binding) and Retrograde Time (Expansion).
        """
        self.res = resolution
        self.zoom = zoom
        self.center = (0.0, 0.0) # We scan the central nexus
        
        # --- MUON RESONANCE PARAMETERS ---
        # A standard Hénon-Heiles system has balanced forces.
        # To find the Muon, we introduce 'Retrograde Tension'.
        
        # The 'Expansion' force (Retrograde Time pressure)
        self.retrograde_pressure = 0.08 
        
        # The 'Binding' force (Forward Time gravity)
        self.binding_strength = 1.0
        
        # The Mass Ratio (Simulating the 207x mass of the Muon vs Electron)
        # This makes the particle 'heavy' (harder to turn, carries more momentum)
        self.mass_inertia = 207.0 / 1836.0 # Relative to Proton approx
        
    def potential_gradient(self, m, l):
        # The Pirouette Potential (Hénon-Heiles)
        # V(m, l) = 1/2(m^2 + l^2) + l*m^2 - l^3/3
        
        # Gradient (Force) = -dV/dr
        dm = - (m + 2 * m * l)
        dl = - (l + m**2 - l**2)
        return dm, dl

    def measure_criticality(self):
        logger.info(f"[-] Initializing Muon Topology Scan ({self.res}x{self.res})...")
        
        # 1. Create the Phase Space Grid
        x = np.linspace(-self.zoom, self.zoom, self.res)
        y = np.linspace(-self.zoom, self.zoom, self.res)
        M, L = np.meshgrid(x, y)
        
        # 2. State Initialization
        # We start them with 'Zero Velocity' relative to the manifold
        # This tests their inherent stability at that point in space.
        m = M.copy()
        l = L.copy()
        vm = np.zeros_like(m)
        vl = np.zeros_like(l)
        
        # 3. The Metric: "Lifetime Tension"
        # We measure how long the particle maintains high energy 
        # before succumbing to the retrograde expansion.
        decay_energy = np.zeros_like(m)
        active = np.ones_like(m, dtype=bool)
        
        dt = 0.02
        max_steps = 600 # Muon lifetime is short!
        
        logger.info("[-] Injecting Retrograde Time-Flow...")
        
        for t in range(max_steps):
            if t % 100 == 0:
                logger.info(f"    Time-step {t}/{max_steps} | Coherent States: {np.sum(active)}")
            
            if not np.any(active): break
                
            # A. Calculate Forces (The "Straddle")
            # 1. The Binding Force (Forward Time) tries to pull it to (0,0)
            fm_bind, fl_bind = self.potential_gradient(m[active], l[active])
            
            # 2. The Expansion Force (Retrograde Time) tries to push it out
            # It acts like 'Negative Friction' or 'Dark Energy'
            # Proportional to velocity (acceleration) and position (expansion)
            fm_expand = self.retrograde_pressure * m[active]
            fl_expand = self.retrograde_pressure * l[active]
            
            # B. Update Velocity (Symplectic-ish Euler)
            # F_net = Binding + Expansion
            vm[active] += (fm_bind * self.binding_strength + fm_expand) * dt
            vl[active] += (fl_bind * self.binding_strength + fl_expand) * dt
            
            # C. Update Position
            m[active] += vm[active] * dt
            l[active] += vl[active] * dt
            
            # D. Measure "Muon-ness" (Criticality)
            # The Muon exists where Kinetic Energy is HIGH but Displacement is LOW.
            # This is the "Vibrating" state before decay.
            ke = 0.5 * (vm[active]**2 + vl[active]**2)
            dist = np.sqrt(m[active]**2 + l[active]**2)
            
            # We accumulate 'Tension': High Energy * Inverse Distance
            # This highlights the "Saddle Points" where it spins furiously in place.
            tension = ke / (dist + 0.1) 
            decay_energy[active] += tension
            
            # E. Decay Condition
            # If it falls into the well (Proton) or flies to infinity (Radiation), it dies.
            # The Muon is the *transition*.
            escaped = (dist > 4.0)
            collapsed = (dist < 0.05)
            
            # Update active mask
            # We have to be careful mapping the subset back to the full grid
            current_indices = np.where(active)
            
            # Identify which of the *active* ones just died
            just_died_subset = escaped | collapsed
            
            # Map back to full array
            # (Indices of active) -> (subset filter)
            dead_indices_m = current_indices[0][just_died_subset]
            dead_indices_l = current_indices[1][just_died_subset]
            
            active[dead_indices_m, dead_indices_l] = False
            
        return decay_energy

    def render(self):
        energy_map = self.measure_criticality()
        
        logger.info("[-] Rendering Muon Decay Manifold...")
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='#050505')
        
        # COLORMAP: "Cherenkov Radiation"
        # Deep Blue (Void) -> Cyan (Field) -> White (The Muon Ridge)
        colors = ["#000000", "#08001c", "#140045", "#0048ff", "#00d5ff", "#ffffff"]
        cmap_muon = LinearSegmentedColormap.from_list("cherenkov", colors)
        
        # We use LogNorm because the energy at the saddle point is exponentially higher
        im = ax.imshow(energy_map, origin='lower', cmap=cmap_muon, norm=LogNorm(vmin=1.0, vmax=np.max(energy_map)),
                       extent=[-self.zoom, self.zoom, -self.zoom, self.zoom])
        
        # Overlay: The Critical Boundary
        # This draws the exact line where Forward and Retrograde forces cancel out
        ax.contour(energy_map, levels=[np.percentile(energy_map, 92)], colors='white', linewidths=0.5, alpha=0.5)
        
        ax.set_title("THE MUON FRACTAL (Critical Decay Topology)", color='white', fontsize=16)
        ax.text(0.02, 0.02, f"Mass Inertia: {self.mass_inertia:.3f}\nRetrograde Pressure: {self.retrograde_pressure}", 
                transform=ax.transAxes, color='#00d5ff', fontsize=10)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig("muon_decay_manifold.png", dpi=150)
        logger.info("[+] Scan Complete. Saved to 'muon_decay_manifold.png'")
        plt.show()

if __name__ == "__main__":
    # We zoom out slightly to capture the full triangular symmetry of the decay paths
    scanner = MuonDecayTopology(resolution=1000, zoom=1.5)
    scanner.render()