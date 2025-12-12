import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LogNorm
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# --- HELPER FUNCTION FOR ANGULAR MEASUREMENT ---
def normalize_angle(angle):
    """
    Normalizes an angle (or angular difference) to the range (-pi, pi] 
    using the atan2 method for robust principal value determination.
    """
    return np.arctan2(np.sin(angle), np.cos(angle))

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

class HelicityScanner:
    """
    THE HELICITY SCANNER
    Measures the Rotational Sensitivity (Differential Helicity) of the manifold.
    """
    def __init__(self, resolution=400): # Lower res default for speed, double calc is heavy
        self.physics = PirouetteHamiltonian()
        self.res = resolution
        self.dt = 0.1
        self.epsilon = 1e-5  # The size of the "Kick" (perturbation)
        
    def measure_helicity_difference(self, m_start, l_start, max_steps=150):
        """
        Runs two particles: Reality and Shadow.
        Returns the maximum angular separation (Differential Helicity, log scale) 
        they achieved.
        """
        # 1. Reality
        m1, l1 = m_start, l_start
        pm1, pl1 = 0.0, 0.0
        
        # 2. Shadow (The "Kick")
        m2, l2 = m_start + self.epsilon, l_start + self.epsilon
        pm2, pl2 = 0.0, 0.0
        
        # Track the maximum angular separation
        max_diff_angle = 0.0
        
        for t in range(max_steps):
            # --- Update Reality (Symplectic Integration) ---
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
            
            # --- Measure The Rotational Stretch (Differential Helicity) ---
            # 1. Get current angles
            ang1 = np.arctan2(l1, m1)
            ang2 = np.arctan2(l2, m2)
            
            # 2. Get the raw difference
            raw_diff = ang1 - ang2
            
            # 3. Normalize difference to (-pi, pi] (shortest path rotation)
            normalized_diff = normalize_angle(raw_diff) 
            
            # 4. We track the MAX absolute separation in angle (Helicity)
            abs_diff = np.abs(normalized_diff)
            
            if abs_diff > max_diff_angle:
                max_diff_angle = abs_diff
                
            # Optimization: If the rotation is already maxed out
            if max_diff_angle > np.pi * 0.95: 
                break
            
            # Escape condition (check only Reality for speed)
            if (m1**2 + l1**2) > 20.0:
                break
                
        # Return Log differential helicity
        return np.log(max_diff_angle + self.epsilon)

    def get_destiny_simple(self, m_start, l_start, max_steps=200):
        # A stripped down version just for the basin map overlay (UNMODIFIED)
        m, l = m_start, l_start
        pm, pl = 0.0, 0.0 
        # Integration loop (same as measure_helicity_difference but only one particle)
        for t in range(max_steps):
            grad = self.physics.gradient(m, l)
            pm -= 0.5 * self.dt * grad[0]
            pl -= 0.5 * self.dt * grad[1]
            m += self.dt * pm
            l += self.dt * pl
            grad = self.physics.gradient(m, l)
            pm -= 0.5 * self.dt * grad[0]
            pl -= 0.5 * self.dt * grad[1]
            
            # Check escape basin based on angle
            if (m**2 + l**2) > 20.0: 
                angle = np.arctan2(l, m)
                if angle > 0.5 and angle < 2.5: return 1
                elif angle > 2.5 or angle < -2.5: return 3
                else: return 2
        return 0 

    def run_scan(self):
        logger.info(f"\n{'='*60}")
        logger.info(f"HELICITY PROBE ({self.res}x{self.res})")
        logger.info("Measuring Differential Helicity & Rotational Memory...")
        logger.info(f"{'='*60}")
        
        # Focused Wada Zoom
        zoom_width = 2
        center_m = 0.0
        center_l = 0.0
        
        m_range = np.linspace(center_m - zoom_width/2, center_m + zoom_width/2, self.res)
        l_range = np.linspace(center_l - zoom_width/2, center_l + zoom_width/2, self.res)
        
        tension_grid = np.zeros((self.res, self.res))
        basin_grid = np.zeros((self.res, self.res))

        for i in range(self.res):
            if i % 20 == 0: 
                pct = (i / self.res) * 100
                logger.info(f"Probing row {i}/{self.res} ({pct:.1f}%)")

            for j in range(self.res):
                m = m_range[j]
                l = l_range[i]
                
                # 1. Measure Physics (Differential Helicity)
                tension_grid[i,j] = self.measure_helicity_difference(m, l)
                
                # 2. Measure Fate (Basin) - for comparison
                basin_grid[i,j] = self.get_destiny_simple(m, l)
        
        self._plot_comparison(tension_grid, basin_grid, m_range, l_range)

    def _plot_comparison(self, helicity, basin, m_range, l_range):
        logger.info("Generating comparative analysis...")
        
        fig, axes = plt.subplots(1, 2, figsize=(20, 10), facecolor='#111111')
        
        # PLOT 1: The Fate Map (Basins) - UNMODIFIED
        cmap_fate = ListedColormap(['#000000', '#ff3333', '#ffaa00', '#00cccc'])
        axes[0].imshow(basin, origin='lower', extent=[m_range[0], m_range[-1], l_range[0], l_range[-1]], 
                   cmap=cmap_fate, interpolation='nearest', vmin=0, vmax=3)
        axes[0].set_title("The Fate Map (Basins)", color='white', fontsize=15)
        axes[0].set_xlabel('Mass Field (m)', color='white')
        axes[0].set_ylabel('Coupling Field (λ)', color='white')
        axes[0].tick_params(colors='white')

        # PLOT 2: The Differential Helicity Map (Rotational Sensitivity)
        im = axes[1].imshow(helicity, origin='lower', extent=[m_range[0], m_range[-1], l_range[0], l_range[-1]], 
                   cmap='hsv', interpolation='bilinear') # Use HSV for angular difference visualization
        axes[1].set_title("The Differential Helicity Map (Rotational Sensitivity)", color='cyan', fontsize=15)
        axes[1].set_xlabel('Mass Field (m)', color='white')
        axes[1].set_ylabel('Coupling Field (λ)', color='white')
        axes[1].tick_params(colors='white')
        
        # Add a colorbar for helicity
        cbar = plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)
        cbar.set_label('Sensitivity (Log Max Angular Difference)', color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

        plt.suptitle(f"Manifold Properties: Determinism vs. Differential Helicity (Kick={self.epsilon})", color='white', fontsize=20)
        plt.tight_layout()
        plt.savefig('wada_differential_helicity_analysis.png', dpi=150, facecolor='#111111')
        logger.info("Saved analysis to 'wada_differential_helicity_analysis.png'")

if __name__ == "__main__":
    scanner = HelicityScanner(resolution=400)
    scanner.run_scan()