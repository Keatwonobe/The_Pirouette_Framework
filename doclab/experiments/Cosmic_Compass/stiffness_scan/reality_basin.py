import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class PirouetteHamiltonian:
    """
    PHYSICS ENGINE
    Standard Hénon-Heiles Potential
    """
    def __init__(self):
        self.coupling = 1.0 # Strong coupling to force decision making
        
    def gradient(self, m, l):
        # Force = -Grad(V)
        # V = 0.5(m^2 + l^2) + (m^2*l - l^3/3)
        dV_dm = m + 2 * m * l
        dV_dl = l + (m**2 - l**2)
        return np.array([dV_dm, dV_dl])

class BasinScanner:
    """
    THE FATE MAPPER
    ================
    Scans a 2D grid of starting positions.
    Colors pixels based on their final destiny (Escape Route vs Trapped).
    """
    def __init__(self, resolution=800):
        self.physics = PirouetteHamiltonian()
        self.res = resolution
        self.dt = 0.1
        
    def get_destiny(self, m_start, l_start, max_steps=200):
        """
        Simulate a particle.
        Returns:
        0: TRAPPED (Stable)
        1: ESCAPE TOP (l -> inf)
        2: ESCAPE RIGHT (m -> inf)
        3: ESCAPE LEFT (m -> -inf)
        """
        m, l = m_start, l_start
        pm, pl = 0.0, 0.0 # Start from rest
        
        for t in range(max_steps):
            # Symplectic Step (Verlet-ish)
            grad = self.physics.gradient(m, l)
            
            # Update momentum
            pm -= 0.5 * self.dt * grad[0]
            pl -= 0.5 * self.dt * grad[1]
            
            # Update position
            m += self.dt * pm
            l += self.dt * pl
            
            # Recalculate grad at new pos
            grad = self.physics.gradient(m, l)
            
            # Finish momentum
            pm -= 0.5 * self.dt * grad[0]
            pl -= 0.5 * self.dt * grad[1]
            
            # CHECK ESCAPE CONDITIONS
            # The Hénon-Heiles potential has 3 escape channels
            r2 = m**2 + l**2
            if r2 > 20.0: # Escaped the center
                # Which way did it go?
                angle = np.arctan2(l, m)
                
                # Top sector (approx 90 deg)
                if angle > 0.5 and angle < 2.5: return 1
                # Left sector
                elif angle > 2.5 or angle < -2.5: return 3
                # Right sector
                else: return 2
                
        return 0 # Trapped

    def run_scan(self):
        logger.info(f"\n{'='*60}")
        logger.info(f"FRACTAL BASIN SCAN ({self.res}x{self.res})")
        logger.info("Mapping the Surface Tension of Reality...")
        logger.info(f"{'='*60}")
        
        # Grid range
        m_range = np.linspace(-1.5, 1.5, self.res)
        l_range = np.linspace(-1.0, 2.0, self.res)
        
        M, L = np.meshgrid(m_range, l_range)
        grid = np.zeros_like(M, dtype=int)
        
        # Flatten for processing
        total = self.res * self.res
        
        # We process row by row to log progress
        for i in range(self.res):
            if i % 50 == 0: logger.info(f"Scanning row {i}/{self.res}...")
            for j in range(self.res):
                m = m_range[j]
                l = l_range[i]
                
                # Check energy first (Optimization)
                # If Potential Energy > 1/6, escape is possible.
                # If V < 0, it's already in the deep chaos.
                grid[i,j] = self.get_destiny(m, l)
                
        self._plot_basin(grid, m_range, l_range)

    def _plot_basin(self, grid, m_range, l_range):
        plt.figure(figsize=(10, 10), facecolor='black')
        
        # Custom Colormap
        # 0=Black (Trapped/Stable)
        # 1=Red (Escape A)
        # 2=Gold (Escape B)
        # 3=Teal (Escape C)
        cmap = ListedColormap(['#000000', '#ff3333', '#ffaa00', '#00cccc'])
        
        plt.imshow(grid, origin='lower', extent=[m_range[0], m_range[-1], l_range[0], l_range[-1]], 
                   cmap=cmap, interpolation='nearest')
        
        # Aesthetic Cleanup
        plt.axis('off')
        plt.title("The Wada Property: Fractal Surface Tension", color='white', pad=20)
        
        # Add scale bar or notion of 'm' and 'lambda'
        plt.text(0.5, 0.02, "m-field (Mass)", color='white', transform=plt.gca().transAxes, ha='center')
        plt.text(0.02, 0.5, "λ-field (Coupling)", color='white', transform=plt.gca().transAxes, va='center', rotation='vertical')
        
        plt.tight_layout()
        plt.savefig('fractal_fate_map.png', dpi=300, facecolor='black')
        logger.info("[Saved high-res fractal map to 'fractal_fate_map.png']")

if __name__ == "__main__":
    scanner = BasinScanner(resolution=800) # 800x800 is good for detail
    scanner.run_scan()