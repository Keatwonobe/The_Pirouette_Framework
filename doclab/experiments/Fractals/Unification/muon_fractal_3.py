import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("FLUX_SCANNER")

class MuonFluxScanner:
    def __init__(self, resolution=800, zoom=2.0):
        """
        THE FLUX SCANNER
        Maps the energy exchange rate of the manifold.
        """
        self.res = resolution
        self.zoom = zoom
        
        # --- FLUX PARAMETERS ---
        # 1. The "Entropy Drag" (Forward Time)
        # Sucks energy out of the system.
        self.friction = 0.04
        
        # 2. The "Retrograde Pressure" (Reverse Time)
        # Pumps energy into the system (Expansion).
        self.retro_pressure = 0.12
        
        # 3. Initial Injection Energy (The "Ton of Energy")
        self.initial_kick = 2.0 

    def get_forces(self, m, l, vm, vl):
        # 1. Hénon-Heiles Conservative Gradient (Gravity)
        d_pot_m = m + 2 * m * l
        d_pot_l = l + m**2 - l**2
        
        # 2. Friction (Opposes Velocity) - The Sink
        f_drag_m = -self.friction * vm
        f_drag_l = -self.friction * vl
        
        # 3. Retrograde Expansion (Radial Repulsion) - The Source
        # Pushes outward from center, adding energy to escaping particles
        f_exp_m = self.retro_pressure * m
        f_exp_l = self.retro_pressure * l
        
        # Net Force
        fm = -d_pot_m + f_drag_m + f_exp_m
        fl = -d_pot_l + f_drag_l + f_exp_l
        
        return fm, fl

    def run_scan(self):
        logger.info(f"[-] Charging Flux Capacitors ({self.res}x{self.res})...")
        
        # 1. Grid Setup
        x = np.linspace(-self.zoom, self.zoom, self.res)
        y = np.linspace(-self.zoom, self.zoom, self.res)
        M, L = np.meshgrid(x, y)
        
        # 2. High Energy Initialization
        # We give every particle a radial velocity OUTWARD.
        # This simulates a "decay attempt" - they all want to leave.
        angles = np.arctan2(L, M)
        vm = self.initial_kick * np.cos(angles)
        vl = self.initial_kick * np.sin(angles)
        
        m, l = M.copy(), L.copy()
        
        # Energy Tracking
        # Kinetic Energy (KE) = 0.5 * v^2
        initial_ke = 0.5 * (vm**2 + vl**2)
        
        # We integrate for a short "interaction window"
        # We don't care where they go, just how their energy changes.
        dt = 0.05
        steps = 100 
        
        logger.info("[-] Dropping particles...")
        
        for t in range(steps):
            # Symplectic-ish Integration
            fm, fl = self.get_forces(m, l, vm, vl)
            
            vm += fm * dt
            vl += fl * dt
            
            m += vm * dt
            l += vl * dt
            
        # 3. Calculate Net Flux
        # Positive Flux = Energy Gained (Manifold is a Source)
        # Negative Flux = Energy Lost (Manifold is a Sink)
        final_ke = 0.5 * (vm**2 + vl**2)
        delta_energy = final_ke - initial_ke
        
        return delta_energy

    def render(self):
        flux_map = self.run_scan()
        
        logger.info("[-] Visualizing Thermodynamics...")
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='#0b0b0b')
        
        # COLORMAP: "Thermodynamic War"
        # Blue = Energy Sink (Cooling/Entropy)
        # Black = Neutral / Zero Flux
        # Red/Gold = Energy Source (Heating/Retrograde)
        colors = ["#001133", "#004488", "#000000", "#cc4400", "#ffcc00"]
        # We adjust positions to ensure Black is at 0
        nodes = [0.0, 0.45, 0.5, 0.55, 1.0]
        cmap_flux = LinearSegmentedColormap.from_list("flux_war", list(zip(nodes, colors)))
        
        # Normalization centered at 0
        # This ensures 0 flux is always the middle color (Black)
        max_val = np.max(np.abs(flux_map))
        norm = TwoSlopeNorm(vmin=-max_val, vcenter=0, vmax=max_val)
        
        im = ax.imshow(flux_map, origin='lower', cmap=cmap_flux, norm=norm,
                       extent=[-self.zoom, self.zoom, -self.zoom, self.zoom])
        
        # Add contours to show the "Zero Flux" boundary (The Event Horizon)
        ax.contour(flux_map, levels=[0], colors='white', linewidths=0.5, alpha=0.3,
                   extent=[-self.zoom, self.zoom, -self.zoom, self.zoom])
        
        ax.set_title("MUON FLUX MANIFOLD\nBlue = Energy Sink (Stability) | Gold = Energy Source (Decay)", 
                     color='white', fontsize=14)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig("muon_flux_map.png", dpi=150)
        logger.info("[+] Map generated: 'muon_flux_map.png'")
        plt.show()

if __name__ == "__main__":
    scanner = MuonFluxScanner(resolution=1000, zoom=2.0)
    scanner.render()