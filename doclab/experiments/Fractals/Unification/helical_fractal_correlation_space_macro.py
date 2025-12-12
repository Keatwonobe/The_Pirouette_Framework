import numpy as np
import matplotlib.pyplot as plt
import logging
from matplotlib.colors import ListedColormap, LogNorm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("SPACE_SCANNER")

# --- GLOBAL CONSTANTS from space_fractal.py ---
TWIST = 3.8
GAMMA = 0.5 
DT = 0.015
STEPS = 1000
EPSILON = 1e-5

# --- STANDARDIZED VIEWPORT (Aligned with Cosmic Caustic) ---
# Zoomed out to [-20, 20] to reveal macro-structure
M_MIN, M_MAX = -20.0, 20.0
L_MIN, L_MAX = -20.0, 20.0
RES = 400 # Using 400 for speed, as the range is large (1600x the area of the original)

# --- HELPER FUNCTION FOR ANGULAR MEASUREMENT ---
def normalize_angle_diff(angle):
    """Normalizes the angular difference to the range [-pi, pi] (shortest path rotation)."""
    return np.arctan2(np.sin(angle), np.cos(angle))

class StandardSpaceHelicityScanner:
    def __init__(self, resolution=RES):
        self.res = resolution
        self.dt = DT
        self.max_steps = STEPS
        self.epsilon = EPSILON
        
    def get_force_and_weight(self, m, lam):
        # --- 1. Force Calculation (Unmodified from space_fractal.py) ---
        F_teal_m = -(m + 0.866) 
        F_teal_lam = -(lam - 0.5)

        F_red_m = -(m - 0.0)
        p_violation = TWIST * np.sin(m * 2.5) 
        F_red_lam = -(lam + 1.0) + p_violation

        sum_m = (F_teal_m + F_red_m)
        sum_lam = (F_teal_lam + F_red_lam)
        magnitude = np.sqrt(sum_m**2 + sum_lam**2)
        scaling_factor = np.sqrt(magnitude)
        
        F_gold_m = sum_m * scaling_factor
        F_gold_lam = sum_lam * scaling_factor
        
        # --- 2. Weighting ---
        angle = np.degrees(np.arctan2(lam, m)) % 360
        
        diff_g = np.abs(angle - 30); diff_g = np.minimum(diff_g, 360-diff_g)
        w_gold = np.exp(-(diff_g/80)**2)
        
        diff_t = np.abs(angle - 150); diff_t = np.minimum(diff_t, 360-diff_t)
        w_teal = np.exp(-(diff_t/80)**2)
        
        diff_r = np.abs(angle - 270); diff_r = np.minimum(diff_r, 360-diff_r)
        w_red = np.exp(-(diff_r/80)**2) 
        
        tot = w_gold + w_teal + w_red + 1e-6
        
        nw_red = w_red / tot
        nw_teal = w_teal / tot
        nw_gold = w_gold / tot
        
        Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
        Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
        
        return Fm, Flam, nw_red

    def measure_helicity_difference(self, m_start, l_start):
        # ... Differential Helicity Measurement (Unmodified) ...
        m1, l1 = m_start, l_start
        pm1, pl1 = 0.0, 0.0
        m2, l2 = m_start + self.epsilon, l_start + self.epsilon
        pm2, pl2 = 0.0, 0.0
        max_diff_angle = 0.0
        
        for t in range(self.max_steps):
            
            # --- REALITY UPDATE ---
            Fm1, Flam1, w_red1 = self.get_force_and_weight(m1, l1)
            drag1 = 1.0 / (1.0 + 0.5 * self.dt * GAMMA * w_red1)
            pm1 = (pm1 + 0.5 * self.dt * Fm1) * drag1
            pl1 = (pl1 + 0.5 * self.dt * Flam1) * drag1
            m1 += self.dt * pm1
            l1 += self.dt * pl1
            Fm1, Flam1, w_red1 = self.get_force_and_weight(m1, l1)
            drag1 = 1.0 / (1.0 + 0.5 * self.dt * GAMMA * w_red1)
            pm1 = (pm1 + 0.5 * self.dt * Fm1) * drag1
            pl1 = (pl1 + 0.5 * self.dt * Flam1) * drag1

            # --- SHADOW UPDATE ---
            Fm2, Flam2, w_red2 = self.get_force_and_weight(m2, l2)
            drag2 = 1.0 / (1.0 + 0.5 * self.dt * GAMMA * w_red2)
            pm2 = (pm2 + 0.5 * self.dt * Fm2) * drag2
            pl2 = (pl2 + 0.5 * self.dt * Flam2) * drag2
            m2 += self.dt * pm2
            l2 += self.dt * pl2
            Fm2, Flam2, w_red2 = self.get_force_and_weight(m2, l2)
            drag2 = 1.0 / (1.0 + 0.5 * self.dt * GAMMA * w_red2)
            pm2 = (pm2 + 0.5 * self.dt * Fm2) * drag2
            pl2 = (pl2 + 0.5 * self.dt * Flam2) * drag2
            
            # --- Measure The Rotational Stretch (Differential Helicity) ---
            ang1 = np.arctan2(l1, m1)
            ang2 = np.arctan2(l2, m2)
            raw_diff = ang1 - ang2
            normalized_diff = normalize_angle_diff(raw_diff) 
            abs_diff = np.abs(normalized_diff)
            
            if abs_diff > max_diff_angle:
                max_diff_angle = abs_diff
                
            if max_diff_angle > np.pi * 0.95: break
            if (m1**2 + l1**2) > 30.0: break
                
        return np.log(max_diff_angle + self.epsilon)

    def run_scan(self):
        logger.info(f"\n{'='*60}")
        logger.info(f"STANDARDIZED SPACE HELICITY PROBE ({self.res}x{self.res})")
        logger.info(f"Viewport: M, L in [{M_MIN}, {M_MAX}]")
        logger.info(f"{'='*60}")
        
        m_range = np.linspace(M_MIN, M_MAX, self.res)
        l_range = np.linspace(L_MIN, L_MAX, self.res)
        helicity_grid = np.zeros((self.res, self.res))

        for i in range(self.res):
            if i % 20 == 0: 
                pct = (i / self.res) * 100
                logger.info(f"Probing row {i}/{self.res} ({pct:.1f}%)")

            for j in range(self.res):
                m = m_range[j]
                l = l_range[i]
                helicity_grid[i,j] = self.measure_helicity_difference(m, l)
        
        self._plot_map(helicity_grid, m_range, l_range)

    def _plot_map(self, helicity, m_range, l_range):
        logger.info("Generating Standardized Differential Helicity Map...")
        
        fig, ax = plt.subplots(figsize=(10, 10), facecolor='#111111')
        
        # Use HSV for maximum angular contrast
        im = ax.imshow(helicity, origin='lower', extent=[m_range[0], m_range[-1], l_range[0], l_range[-1]], 
                   cmap='hsv', interpolation='bilinear')
        
        ax.set_title("Standardized Differential κ-Helicity (Space Fractal)", color='cyan', fontsize=15)
        ax.set_xlabel('Mass Field (m)', color='white')
        ax.set_ylabel('Coupling Field (λ)', color='white')
        ax.tick_params(colors='white')
        
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label(r'Rotational Sensitivity $(\log |\Delta \theta|_{\max})$', color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

        plt.tight_layout()
        plt.savefig('standard_space_differential_helicity.png', dpi=150, facecolor='#111111')
        logger.info("Saved analysis to 'standard_space_differential_helicity.png'")


if __name__ == "__main__":
    scanner = StandardSpaceHelicityScanner()
    scanner.run_scan()