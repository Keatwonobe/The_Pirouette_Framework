import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import logging
import os  # <--- Added for file checking

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class PirouetteHamiltonian:
    """
    PHYSICS ENGINE
    Standard Hénon-Heiles Potential
    """
    def __init__(self):
        self.coupling = 1.0 
        
    def gradient(self, m, l):
        dV_dm = m + 2 * m * l
        dV_dl = l + (m**2 - l**2)
        return np.array([dV_dm, dV_dl])

class BasinScanner:
    """
    THE FATE MAPPER
    """
    def __init__(self, resolution=800):
        self.physics = PirouetteHamiltonian()
        self.res = resolution
        self.dt = 0.1
        self.checkpoint_file = "basin_checkpoint.npy" # <--- Checkpoint filename
        
    def get_destiny(self, m_start, l_start, max_steps=200):
        m, l = m_start, l_start
        pm, pl = 0.0, 0.0 
        
        for t in range(max_steps):
            grad = self.physics.gradient(m, l)
            pm -= 0.5 * self.dt * grad[0]
            pl -= 0.5 * self.dt * grad[1]
            m += self.dt * pm
            l += self.dt * pl
            grad = self.physics.gradient(m, l)
            pm -= 0.5 * self.dt * grad[0]
            pl -= 0.5 * self.dt * grad[1]
            
            r2 = m**2 + l**2
            if r2 > 20.0: 
                angle = np.arctan2(l, m)
                if angle > 0.5 and angle < 2.5: return 1
                elif angle > 2.5 or angle < -2.5: return 3
                else: return 2
                
        return 0 

    def run_scan(self):
        logger.info(f"\n{'='*60}")
        logger.info(f"FRACTAL BASIN SCAN ({self.res}x{self.res})")
        logger.info("Mapping the Surface Tension of Reality...")
        logger.info(f"{'='*60}")
        
        # Focused Wada Zoom (Centered on m=0.31, l=0.59)
        zoom_width = 0.3
        center_m = 0.312
        center_l = 0.591
        
        m_range = np.linspace(center_m - zoom_width/2, center_m + zoom_width/2, self.res)
        l_range = np.linspace(center_l - zoom_width/2, center_l + zoom_width/2, self.res)
        
        # --- CHECKPOINT LOGIC START ---
        # 1. Check if checkpoint exists
        if os.path.exists(self.checkpoint_file):
            logger.info(f"Found checkpoint: {self.checkpoint_file}. Resuming...")
            grid = np.load(self.checkpoint_file)
            
            # Find the first row that starts with -1 (meaning it wasn't calculated)
            # We assume if the first pixel is -1, the whole row is undone.
            incomplete_rows = np.where(grid[:,0] == -1)[0]
            
            if len(incomplete_rows) > 0:
                start_row = incomplete_rows[0]
            else:
                start_row = self.res # It's already done
                logger.info("Scan appears complete. Proceeding to plot.")
        else:
            logger.info("No checkpoint found. Starting fresh.")
            start_row = 0
            # Initialize with -1 so we can distinguish "Trapped (0)" from "Empty (-1)"
            grid = np.full((self.res, self.res), -1, dtype=int)
        # --- CHECKPOINT LOGIC END ---

        # Process row by row
        for i in range(start_row, self.res):
            
            # Save Checkpoint every 50 rows
            if i % 50 == 0 and i > 0: 
                logger.info(f"Saving checkpoint at row {i}...")
                np.save(self.checkpoint_file, grid)

            # Log progress
            if i % 10 == 0: # More frequent logging so you know it's alive
                pct = (i / self.res) * 100
                logger.info(f"Scanning row {i}/{self.res} ({pct:.1f}%)")

            for j in range(self.res):
                m = m_range[j]
                l = l_range[i]
                grid[i,j] = self.get_destiny(m, l)
        
        # Final Save
        np.save(self.checkpoint_file, grid)
        
        self._plot_basin(grid, m_range, l_range)

    def _plot_basin(self, grid, m_range, l_range):
        logger.info("Generating image...")
        plt.figure(figsize=(10, 10), facecolor='black')
        
        # Custom Colormap
        # -1=Grey (Uncalculated - if you stop early and plot)
        # 0=Black (Trapped)
        # 1=Red, 2=Gold, 3=Teal
        cmap = ListedColormap(['#333333', '#000000', '#ff3333', '#ffaa00', '#00cccc'])
        
        # We need to offset the values by +1 so that -1 maps to index 0, 0 to 1, etc.
        # But matplotlib handles mapping values to colors automatically if we set vmin/vmax
        # To match the list above: -1, 0, 1, 2, 3
        
        plt.imshow(grid, origin='lower', extent=[m_range[0], m_range[-1], l_range[0], l_range[-1]], 
                   cmap=cmap, interpolation='nearest', vmin=-1, vmax=3)
        
        plt.axis('off')
        plt.title("The Wada Property: Fractal Surface Tension", color='white', pad=20)
        
        plt.text(0.5, 0.02, "m-field (Mass)", color='white', transform=plt.gca().transAxes, ha='center')
        plt.text(0.02, 0.5, "λ-field (Coupling)", color='white', transform=plt.gca().transAxes, va='center', rotation='vertical')
        
        plt.tight_layout()
        plt.savefig('fractal_fate_map.png', dpi=300, facecolor='black')
        logger.info("Saved high-res fractal map to 'fractal_fate_map.png'")

if __name__ == "__main__":
    scanner = BasinScanner(resolution=800)
    scanner.run_scan()