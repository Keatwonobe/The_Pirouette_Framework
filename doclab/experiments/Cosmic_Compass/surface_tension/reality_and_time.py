import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class PirouetteHamiltonian:
    """
    PHYSICS ENGINE
    """
    def __init__(self):
        self.coupling = 1.0 
        
    def gradient(self, m, l):
        dV_dm = m + 2 * m * l
        dV_dl = l + (m**2 - l**2)
        return np.array([dV_dm, dV_dl])

class ChronologyScanner:
    """
    THE TIME KEEPER
    Measures the 'Depth' of the fractal by counting survival time.
    """
    def __init__(self, resolution=800):
        self.physics = PirouetteHamiltonian()
        self.res = resolution
        self.dt = 0.1
        self.checkpoint_file = "time_checkpoint.npy"
        
    def measure_lifespan(self, m_start, l_start, max_steps=1000):
        """
        Simulates the particle and counts how many steps it survives.
        Returns: Integer (number of steps)
        """
        m, l = m_start, l_start
        pm, pl = 0.0, 0.0
        
        for t in range(max_steps):
            # Leapfrog Integration (Symplectic)
            grad = self.physics.gradient(m, l)
            pm -= 0.5 * self.dt * grad[0]
            pl -= 0.5 * self.dt * grad[1]
            m += self.dt * pm
            l += self.dt * pl
            grad = self.physics.gradient(m, l)
            pm -= 0.5 * self.dt * grad[0]
            pl -= 0.5 * self.dt * grad[1]
            
            # Escape Condition
            if (m**2 + l**2) > 20.0:
                return t # Returned the exact step count of death
        
        return max_steps # It survived the whole time (The Black Hole)

    def run_scan(self):
        logger.info(f"\n{'='*60}")
        logger.info(f"CHRONOLOGY SCAN ({self.res}x{self.res})")
        logger.info("Mapping the Depth of the Knot...")
        logger.info(f"{'='*60}")
        
        # Focused Wada Zoom (Same coordinates as before for comparison)
        zoom_width = 0.3
        center_m = 0.312
        center_l = 0.591
        
        m_range = np.linspace(center_m - zoom_width/2, center_m + zoom_width/2, self.res)
        l_range = np.linspace(center_l - zoom_width/2, center_l + zoom_width/2, self.res)
        
        # The Time Grid
        time_grid = np.zeros((self.res, self.res))

        # Checkpoint Logic
        start_row = 0
        if os.path.exists(self.checkpoint_file):
            logger.info("Resuming from checkpoint...")
            time_grid = np.load(self.checkpoint_file)
            # Find where we left off (assuming 0 means uncalculated)
            # Note: 0 is technically a valid time (instant death), but rare in this zoom.
            # Ideally use -1 initialization, but for simplicity:
            incomplete = np.where(time_grid[:,0] == 0)[0]
            if len(incomplete) > 0: start_row = incomplete[0]
        
        for i in range(start_row, self.res):
            if i % 20 == 0: 
                pct = (i / self.res) * 100
                logger.info(f"Scanning Time Depth row {i}/{self.res} ({pct:.1f}%)")
                if i > 0: np.save(self.checkpoint_file, time_grid)

            for j in range(self.res):
                m = m_range[j]
                l = l_range[i]
                time_grid[i,j] = self.measure_lifespan(m, l)
        
        np.save(self.checkpoint_file, time_grid)
        self._plot_chronology(time_grid, m_range, l_range)

    def _plot_chronology(self, grid, m_range, l_range):
        logger.info("Generating Chronology Map...")
        plt.figure(figsize=(12, 10), facecolor='black')
        
        # We use 'inferno' or 'gist_heat' to make the deep spots look hot/intense
        # LogNorm is CRITICAL here to see detail in both shallow and deep regions
        plt.imshow(grid, origin='lower', extent=[m_range[0], m_range[-1], l_range[0], l_range[-1]], 
                   cmap='inferno', interpolation='bilinear', norm=LogNorm(vmin=10, vmax=np.max(grid)))
        
        cbar = plt.colorbar(fraction=0.046, pad=0.04)
        cbar.set_label('Survival Time (Iterations)', color='white', size=12)
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
        
        plt.title("The Chronology Map: Escape Time Analysis", color='white', fontsize=16, pad=20)
        plt.axis('off')
        
        plt.tight_layout()
        plt.savefig('wada_chronology_map.png', dpi=300, facecolor='black')
        logger.info("Saved time map to 'wada_chronology_map.png'")

if __name__ == "__main__":
    # High resolution is recommended for Time Maps to see the "Dust"
    scanner = ChronologyScanner(resolution=800)
    scanner.run_scan()