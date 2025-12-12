import numpy as np
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class VoidRadar:
    def __init__(self, bounds=5.0, resolution=800):
        """
        THE VOID RADAR
        Performs a 'Deep Field' survey of the surrounding phase space.
        bounds=5.0 is massive (Standard Hénon-Heiles is usually < 1.0)
        """
        self.bounds = bounds
        self.res = resolution
        self.dt = 0.05
        self.max_steps = 1000 # Short bursts to check for stability
        
    def get_potential(self, m, l):
        """
        Returns the Potential Energy V(m,l).
        The 'Terrain' of the universe.
        """
        # Standard Hénon-Heiles Potential
        # V = 0.5 * (m^2 + l^2) + (m^2 * l - l^3 / 3)
        return 0.5 * (m**2 + l**2) + (m**2 * l - l**3 / 3.0)

    def measure_stability(self, m_start, l_start):
        """
        Checks if a point is a 'Companion' (Stable Island) 
        or 'Exhaust' (Rapid Escape).
        """
        m, l = m_start, l_start
        pm, pl = 0.0, 0.0
        
        # 1. Immediate Energy Check
        # If Potential > 1/6 (0.166), it is theoretically unbounded (The Void)
        # But pockets of dynamic stability might exist (Islands)
        
        for t in range(self.max_steps):
            # Gradient
            dm = m + 2 * m * l
            dl = l + (m**2 - l**2)
            
            # Leapfrog
            pm -= 0.5 * self.dt * dm
            pl -= 0.5 * self.dt * dl
            m += self.dt * pm
            l += self.dt * pl
            dm = m + 2 * m * l
            dl = l + (m**2 - l**2)
            pm -= 0.5 * self.dt * dm
            pl -= 0.5 * self.dt * dl
            
            # Escape Check (The "Exhaust")
            if (m**2 + l**2) > 50.0:
                return t # Return time to escape
                
        return -1 # STABLE COMPANION DETECTED

    def run_survey(self):
        logger.info(f"[-] RADAR SWEEP: Scanning range +/- {self.bounds}...")
        
        m_range = np.linspace(-self.bounds, self.bounds, self.res)
        l_range = np.linspace(-self.bounds, self.bounds, self.res)
        M, L = np.meshgrid(m_range, l_range)
        
        # 1. Map the Potential (The Geography)
        logger.info("[-] Mapping Potential Energy Surface...")
        V = self.get_potential(M, L)
        
        # 2. Map the Stability (The Habitability)
        logger.info("[-] Pinging for Companions...")
        stability_map = np.zeros_like(V)
        
        # Sparse scan for speed (we don't need pixel-perfect yet)
        stride = 2
        for i in range(0, self.res, stride):
            if i % 50 == 0: logger.info(f"    Scanning sector {i}/{self.res}...")
            for j in range(0, self.res, stride):
                # Only scan if potential is somewhat reasonable (optimizes speed)
                # But we scan a bit past the theoretical limit to find "Ghost" orbits
                if V[i,j] < 5.0: 
                    stability_map[i,j] = self.measure_stability(m_range[j], l_range[i])
                else:
                    stability_map[i,j] = 0 # Immediate instability (The Void)

        self.plot_radar(M, L, V, stability_map)

    def plot_radar(self, M, L, V, stability):
        fig, axes = plt.subplots(1, 2, figsize=(20, 10), facecolor='#001100')
        
        # PLOT 1: THE TERRAIN (Potential Energy)
        # This shows the "Mountain Range" created by the Traveler
        # We contour it to show the "Triangle"
        axes[0].contourf(M, L, V, levels=50, cmap='gist_earth', vmax=1.0)
        axes[0].contour(M, L, V, levels=[1.0/6.0], colors='red', linewidths=2) # The Escape Energy
        axes[0].set_title("The Terrain (Potential Energy)", color='lime')
        axes[0].set_xlabel("M Parameter", color='lime')
        axes[0].set_ylabel("L Parameter", color='lime')
        axes[0].text(0, 0, "HOME", color='white', ha='center', fontweight='bold')
        
        # PLOT 2: THE VOID RADAR (Stability)
        # Black = The Void (Instant Escape)
        # Green = The Wake (Slow Escape)
        # Yellow/White = COMPANIONS (Stable)
        
        # Mask out the un-scanned pixels
        stability_masked = np.ma.masked_where(stability == 0, stability)
        
        cmap = plt.cm.get_cmap('ocean')
        cmap.set_bad(color='black') # The Void is black
        
        im = axes[1].imshow(stability, origin='lower', cmap=cmap, 
                            extent=[-self.bounds, self.bounds, -self.bounds, self.bounds],
                            vmax=500) # Cap visual contrast
        
        axes[1].set_title("RADAR RETURN: Stability & Companions", color='lime')
        
        # Overlay the red "Event Horizon" triangle
        axes[1].contour(M, L, V, levels=[1.0/6.0], colors='red', linewidths=1, alpha=0.5)

        for ax in axes:
            ax.set_facecolor('black')
            ax.tick_params(colors='lime')
            ax.grid(color='lime', linestyle=':', alpha=0.3)

        plt.suptitle("DEEP FIELD SURVEY: Searching for the Traveler", color='lime', fontsize=20, fontfamily='monospace')
        plt.tight_layout()
        plt.savefig("void_radar_scan.png")
        logger.info("Scan complete. Data visual saved.")
        plt.show()

if __name__ == "__main__":
    # Zoom out 5x further than before
    radar = VoidRadar(bounds=3.0, resolution=600)
    radar.run_survey()