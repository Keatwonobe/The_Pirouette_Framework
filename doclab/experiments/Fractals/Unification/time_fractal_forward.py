import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LogNorm
import logging
import os

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

class ElasticityScanner:
    """
    THE TENSION MAPPER
    Measures how 'springy' or 'volatile' the manifold is by using a Shadow Particle.
    """
    def __init__(self, resolution=400): # Lower res default for speed, double calc is heavy
        self.physics = PirouetteHamiltonian()
        self.res = resolution
        self.dt = 0.1
        self.epsilon = 1e-5  # The size of the "Kick" (perturbation)
        self.checkpoint_file = "tension_checkpoint.npy"
        
    def measure_tension(self, m_start, l_start, max_steps=150):
        """
        Runs two particles: Reality and Shadow.
        Returns the maximum separation distance (log scale) they achieved.
        """
        # 1. Reality
        m1, l1 = m_start, l_start
        pm1, pl1 = 0.0, 0.0
        
        # 2. Shadow (The "Kick")
        m2, l2 = m_start + self.epsilon, l_start + self.epsilon
        pm2, pl2 = 0.0, 0.0
        
        # Track the maximum separation
        max_divergence = 0.0
        
        for t in range(max_steps):
            # --- Update Reality ---
            grad1 = self.physics.gradient(m1, l1)
            pm1 -= 0.5 * self.dt * grad1[0]
            pl1 -= 0.5 * self.dt * grad1[1]
            m1 += self.dt * pm1
            l1 += self.dt * pl1
            grad1 = self.physics.gradient(m1, l1)
            pm1 -= 0.5 * self.dt * grad1[0]
            pl1 -= 0.5 * self.dt * grad1[1]

            # --- Update Shadow ---
            grad2 = self.physics.gradient(m2, l2)
            pm2 -= 0.5 * self.dt * grad2[0]
            pl2 -= 0.5 * self.dt * grad2[1]
            m2 += self.dt * pm2
            l2 += self.dt * pl2
            grad2 = self.physics.gradient(m2, l2)
            pm2 -= 0.5 * self.dt * grad2[0]
            pl2 -= 0.5 * self.dt * grad2[1]
            
            # --- Measure The Stretch ---
            # Euclidean distance between Reality and Shadow
            dist = np.sqrt((m1 - m2)**2 + (l1 - l2)**2)
            
            # We capture the max separation to see "peak stress"
            if dist > max_divergence:
                max_divergence = dist
                
            # Optimization: If they separate too much, it's already "Infinite Elasticity"
            if max_divergence > 1.0:
                break
            
            # Escape condition (check only Reality for speed)
            if (m1**2 + l1**2) > 20.0:
                break
                
        # Return Log divergence to compress the scale (Visually better for fractals)
        # We add epsilon to avoid log(0)
        return np.log(max_divergence + self.epsilon)

    def get_destiny_simple(self, m_start, l_start, max_steps=200):
        # A stripped down version just for the basin map overlay
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
            if (m**2 + l**2) > 20.0: 
                angle = np.arctan2(l, m)
                if angle > 0.5 and angle < 2.5: return 1
                elif angle > 2.5 or angle < -2.5: return 3
                else: return 2
        return 0 

    def run_scan(self):
        logger.info(f"\n{'='*60}")
        logger.info(f"ELASTICITY PROBE ({self.res}x{self.res})")
        logger.info("Measuring Manifold Tension & Sensitivity...")
        logger.info(f"{'='*60}")
        
        # Focused Wada Zoom
        zoom_width = 2
        center_m = 0.0
        center_l = 0.0
        
        m_range = np.linspace(center_m - zoom_width/2, center_m + zoom_width/2, self.res)
        l_range = np.linspace(center_l - zoom_width/2, center_l + zoom_width/2, self.res)
        
        # Arrays to hold data
        # tension_grid: float (how much it stretches)
        # basin_grid: int (where it ends up)
        tension_grid = np.zeros((self.res, self.res))
        basin_grid = np.zeros((self.res, self.res))

        # Checkpoint logic omitted for brevity, but recommended for large runs
        
        for i in range(self.res):
            if i % 20 == 0: 
                pct = (i / self.res) * 100
                logger.info(f"Probing row {i}/{self.res} ({pct:.1f}%)")

            for j in range(self.res):
                m = m_range[j]
                l = l_range[i]
                
                # 1. Measure Physics (Tension)
                tension_grid[i,j] = self.measure_tension(m, l)
                
                # 2. Measure Fate (Basin) - for comparison
                basin_grid[i,j] = self.get_destiny_simple(m, l)
        
        self._plot_comparison(tension_grid, basin_grid, m_range, l_range)

    def _plot_comparison(self, tension, basin, m_range, l_range):
        logger.info("Generating comparative analysis...")
        
        fig, axes = plt.subplots(1, 2, figsize=(20, 10), facecolor='#111111')
        
        # PLOT 1: The Fate Map (Basins)
        cmap_fate = ListedColormap(['#000000', '#ff3333', '#ffaa00', '#00cccc'])
        axes[0].imshow(basin, origin='lower', extent=[m_range[0], m_range[-1], l_range[0], l_range[-1]], 
                   cmap=cmap_fate, interpolation='nearest', vmin=0, vmax=3)
        axes[0].set_title("The Fate Map (Basins)", color='white', fontsize=15)
        axes[0].axis('off')

        # PLOT 2: The Tension Map (Elasticity)
        # We use 'magma' or 'inferno' because they look like heat/stress
        im = axes[1].imshow(tension, origin='lower', extent=[m_range[0], m_range[-1], l_range[0], l_range[-1]], 
                   cmap='magma', interpolation='bilinear')
        axes[1].set_title("The Tension Map (Lyapunov Instability)", color='white', fontsize=15)
        axes[1].axis('off')
        
        # Add a colorbar for tension
        cbar = plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)
        cbar.set_label('Sensitivity (Log Divergence)', color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

        plt.suptitle(f"Manifold Properties: Determinism vs. Elasticity (Kick={self.epsilon})", color='white', fontsize=20)
        plt.tight_layout()
        plt.savefig('wada_elasticity_analysis_2.png', dpi=150, facecolor='#111111')
        logger.info("Saved analysis to 'wada_elasticity_analysis.png'")

if __name__ == "__main__":
    # Resolution 400 is good for testing. Go to 800+ for high detail.
    scanner = ElasticityScanner(resolution=400)
    scanner.run_scan()