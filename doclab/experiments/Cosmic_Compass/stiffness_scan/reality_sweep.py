import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.spatial.distance import pdist
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class PirouetteQuantifier:
    """
    QUANTIFICATION SUITE
    ====================
    Modules:
    1. Lyapunov Scanner (Stability)
    2. Ratio Variance Analyzer (Tightening)
    3. Correlation Dimension (Fractal Geometry)
    """
    
    def __init__(self):
        self.coupling = 0.5
        self.dt = 0.05
        
    def gradient(self, m, l):
        dV_dm = m + 2 * self.coupling * m * l
        dV_dl = l + self.coupling * (m**2 - l**2)
        return np.array([dV_dm, dV_dl])
        
    def step(self, state):
        """Symplectic Step"""
        m, l, pm, pl = state
        grad = self.gradient(m, l)
        pm_half = pm - 0.5 * self.dt * grad[0]
        pl_half = pl - 0.5 * self.dt * grad[1]
        m_new = m + self.dt * pm_half
        l_new = l + self.dt * pl_half
        grad_new = self.gradient(m_new, l_new)
        pm_new = pm_half - 0.5 * self.dt * grad_new[0]
        pl_new = pl_half - 0.5 * self.dt * grad_new[1]
        return np.array([m_new, l_new, pm_new, pl_new])

    def get_stiffness_ratio(self, state):
        """
        Defines the 'Coupling Ratio' R.
        We use the ratio of the field amplitudes (energies) as the observable.
        R = m^2 / lambda^2 (protected against div/0)
        """
        m, l = state[0], state[1]
        # Add epsilon to prevent divide by zero
        return (m**2) / (l**2 + 1e-9)

    def measure_fractal_dimension(self, points):
        """
        Computes Correlation Dimension (D2) using Grassberger-Procaccia algorithm.
        Slope of log(C(r)) vs log(r).
        """
        if len(points) < 100: return 0.0
        
        # 1. Compute pairwise distances
        dists = pdist(points)
        
        # 2. Compute Correlation Integral C(r)
        # We scan radii from small to large
        radii = np.logspace(-3, 0, 20)
        counts = []
        
        for r in radii:
            count = np.sum(dists < r)
            counts.append(count)
            
        counts = np.array(counts)
        # Avoid log(0)
        counts = counts[counts > 0]
        radii = radii[:len(counts)]
        
        if len(counts) < 5: return 0.0
        
        # 3. Fit Slope (D2) in the linear region (scaling region)
        log_r = np.log(radii)
        log_C = np.log(counts)
        
        # We fit the middle 50% to avoid finite size effects
        mid = len(log_r)//2
        slope, _ = np.polyfit(log_r[mid-3:mid+3], log_C[mid-3:mid+3], 1)
        
        return slope, log_r, log_C

    def run_regime_scan(self, vacuum, kicks):
        logger.info(f"\n{'='*60}")
        logger.info("PIROUETTE QUANTIFICATION SCAN")
        logger.info(f"{'='*60}")
        
        results_lambda = []
        results_variance = []
        results_mean = []
        fractal_dims = []
        
        fig, axes = plt.subplots(3, 1, figsize=(10, 15))
        
        for kick in kicks:
            logger.info(f"Scanning Regime: Kick Energy {kick:.2f}...")
            
            state = np.array([vacuum[0], vacuum[1] + kick, 0.0, 0.0])
            shadow = state.copy()
            shadow[0] += 1e-8 # Perturbation
            
            ratios = []
            divergence = []
            poincare_points = []
            prev_l = state[1]
            
            # Run Trajectory
            for t in range(5000):
                # Evolve
                next_state = self.step(state)
                shadow = self.step(shadow)
                
                # 1. Lyapunov (Divergence)
                dist = np.linalg.norm(state - shadow)
                if dist > 0: divergence.append(np.log(dist))
                
                # 2. Ratio Statistics
                # We only record ratio when system has 'settled' (burn-in > 500)
                if t > 500:
                    r = self.get_stiffness_ratio(state)
                    # Filter outliers for clean stats
                    if r < 10: ratios.append(r)
                
                # 3. Poincaré Collection (for D2)
                curr_l = next_state[1]
                if prev_l < 0 and curr_l >= 0 and t > 1000:
                     # Interpolate
                    frac = (0 - prev_l)/(curr_l - prev_l + 1e-9)
                    pm = state[0] + frac*(next_state[0]-state[0])
                    ppm = state[2] + frac*(next_state[2]-state[2])
                    poincare_points.append([pm, ppm])
                
                state = next_state
                prev_l = curr_l
            
            # --- ANALYZE ---
            
            # Lambda
            if len(divergence) > 100:
                slope, _ = np.polyfit(np.arange(len(divergence)), divergence, 1)
                results_lambda.append(slope)
            else:
                results_lambda.append(0)
                
            # Ratio Stats
            if len(ratios) > 0:
                results_mean.append(np.mean(ratios))
                results_variance.append(np.std(ratios)) # Std Dev (tightness)
            else:
                results_mean.append(0)
                results_variance.append(0)
            
            # Fractal Dimension (Only for high energy)
            if kick > 0.5 and len(poincare_points) > 100:
                d2, lr, lc = self.measure_fractal_dimension(np.array(poincare_points))
                fractal_dims.append(d2)
                logger.info(f"  > Fractal Dimension D2: {d2:.4f}")
            else:
                fractal_dims.append(0)
                
        # --- PLOTTING ---
        
        # Plot 1: Lyapunov Transition
        ax1 = axes[0]
        ax1.plot(kicks, results_lambda, 'b-o')
        ax1.axhline(0, color='k', linestyle='--')
        ax1.set_title("I. Phase Transition: Stability (λ) vs Energy")
        ax1.set_ylabel("Lyapunov Exponent")
        ax1.grid(True, alpha=0.3)
        ax1.text(kicks[0], min(results_lambda), "Torus Regime", color='green')
        ax1.text(kicks[-1], max(results_lambda), "Chaotic Regime", color='red')
        
        # Plot 2: Ratio Tightening (Antifragility)
        ax2 = axes[1]
        ax2.errorbar(kicks, results_mean, yerr=results_variance, fmt='r-o', ecolor='gray', capsize=5)
        ax2.set_title("II. Invariant Statistics: Coupling Ratio Mean & Variance")
        ax2.set_ylabel("Stiffness Ratio (m²/λ²)")
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Fractal Dimension
        ax3 = axes[2]
        # Filter non-zeros
        valid_kicks = [k for k, d in zip(kicks, fractal_dims) if d > 0]
        valid_dims = [d for d in fractal_dims if d > 0]
        if valid_dims:
            ax3.plot(valid_kicks, valid_dims, 'purple', marker='D')
            ax3.set_title("III. Geometry: Correlation Dimension (D2)")
            ax3.set_ylabel("Dimension")
            ax3.set_xlabel("Kick Energy")
            ax3.axhline(1.0, color='gray', linestyle='--', label='Line (1D)')
            ax3.axhline(2.0, color='gray', linestyle='--', label='Plane (2D)')
            ax3.legend()
        else:
            ax3.text(0.5, 0.5, "Fractal Regime Not Reached", ha='center')
            
        plt.tight_layout()
        plt.savefig('quantification_dashboard.png')
        logger.info("[Saved dashboard to 'quantification_dashboard.png']")

if __name__ == "__main__":
    q = PirouetteQuantifier()
    
    # Find Vacuum
    res = minimize(lambda x: 0.5*(x[0]**2+x[1]**2) + 0.5*(x[0]**2*x[1] - x[1]**3/3), [0.1, 0.1], method='Nelder-Mead')
    vac = res.x
    
    # Run Sweep
    # We scan from low energy (0.1) to high energy (0.7)
    kicks_to_scan = np.linspace(0.1, 0.7, 10)
    q.run_regime_scan(vac, kicks_to_scan)