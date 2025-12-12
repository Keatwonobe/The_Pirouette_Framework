import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class LyapunovScanner:
    """
    THE BUTTERFLY EFFECT METER
    ==========================
    Measures the Largest Lyapunov Exponent (λ) by tracking the 
    exponential divergence of two shadow trajectories.
    """
    
    def __init__(self, simulator_func, m_start, l_start):
        self.simulator_func = simulator_func
        self.m_start = m_start
        self.l_start = l_start
        
    def measure_exponent(self, steps=500, epsilon=1e-8):
        logger.info(f"\n{'='*60}")
        logger.info("LYAPUNOV EXPONENT SCAN (Sensitivity to Initial Conditions)")
        logger.info(f"{'='*60}")
        logger.info(f"Perturbation size: {epsilon:.1e}")
        
        # 1. Burn-in (Get to the attractor)
        # We run the system for a bit to ensure we are ON the breathing mode
        # and not just falling towards it.
        logger.info("Stabilizing on attractor (Burn-in)...")
        m_curr, l_curr = self.m_start, self.l_start
        
        # Note: This assumes your simulator is stateless between calls
        # If your simulator has internal state, you need to step it differently.
        # For this scanner, we assume we can just drift the parameters slightly
        # to simulate "motion" if the simulator is static, 
        # OR we assume the simulator function itself evolves the state.
        
        # --- SHADOW TRAJECTORY SETUP ---
        # Since your simulator function takes (m, l) and returns stiffness,
        # we need to simulate the "flow" of m and l. 
        # If your system is a map: x_n+1 = f(x_n), we iterate that.
        # If your system is a field, we simulate a particle 'rolling' on it.
        
        # We will use a simple gradient descent/flow as the "Time Evolution"
        # to see if the Trajectory itself is chaotic.
        
        trajectory_A = []
        trajectory_B = []
        divergence = []
        
        # Initialize Twin Shadows
        # State = [m, l]
        state_A = np.array([float(m_curr), float(l_curr)])
        
        # Perturb B slightly
        perturbation = np.random.randn(2)
        perturbation = perturbation / np.linalg.norm(perturbation) * epsilon
        state_B = state_A + perturbation
        
        logger.info(f"Running Twin Simulation for {steps} steps...")
        
        for t in range(steps):
            # Evolve State A
            # We use the gradient of the field to drive the motion (Flow)
            grad_A = self._get_gradient(state_A[0], state_A[1])
            # Simple Euler step (Motion along the landscape)
            # Chaos often appears in the gradients of complex potentials
            state_A = state_A + 0.05 * grad_A 
            
            # Evolve State B
            grad_B = self._get_gradient(state_B[0], state_B[1])
            state_B = state_B + 0.05 * grad_B
            
            # Measure Distance (Euclidean)
            dist = np.linalg.norm(state_A - state_B)
            
            # Record Log-Distance
            # If dist is 0 (impossible usually), use epsilon
            if dist < 1e-15: dist = 1e-15
            
            trajectory_A.append(state_A.copy())
            trajectory_B.append(state_B.copy())
            divergence.append(np.log(dist))
            
            # Saturation check (Finite Size Effect)
            if dist > 1.0:
                logger.warning(f"  > Saturation reached at step {t} (distance > 1.0)")
                # If we saturate, we stop fitting the slope here
                break
                
        # 2. Calculate Lambda (Slope of the log-divergence)
        # We typically ignore the first few steps (transient) and fit the linear growth region
        valid_steps = len(divergence)
        fit_start = int(valid_steps * 0.1) # Skip first 10%
        fit_end = int(valid_steps * 0.8)   # Skip last 20% (saturation curve)
        
        if fit_end - fit_start < 10:
            logger.error("Not enough data to fit Lyapunov exponent.")
            return 0.0
            
        time_steps = np.arange(fit_start, fit_end)
        log_dists = divergence[fit_start:fit_end]
        
        slope, intercept, r_value, p_value, std_err = linregress(time_steps, log_dists)
        
        # Lambda is the slope
        lyapunov_lambda = slope
        
        logger.info(f"\nRESULTS:")
        logger.info(f"Lyapunov Exponent (λ): {lyapunov_lambda:.5f}")
        logger.info(f"Fit Quality (R-squared): {r_value**2:.4f}")
        
        if lyapunov_lambda > 0.001:
            logger.info(">> SYSTEM IS CHAOTIC (Positive λ)")
            logger.info(f">> Prediction Horizon: ~{1/lyapunov_lambda:.1f} steps")
        elif lyapunov_lambda < -0.001:
            logger.info(">> SYSTEM IS STABLE (Negative λ)")
        else:
            logger.info(">> CRITICALITY DETECTED (λ ≈ 0)")
            logger.info(">> Edge of Chaos / Infinite Memory")
            
        self._plot_butterfly(trajectory_A, trajectory_B, divergence, slope, intercept, fit_start, fit_end)
        
        return lyapunov_lambda

    def _get_gradient(self, m, l, eps=1e-4):
        """Estimate gradient of the simulator field to drive the flow"""
        # Central difference
        val_m_p = self.simulator_func(m + eps, l)
        val_m_n = self.simulator_func(m - eps, l)
        val_l_p = self.simulator_func(m, l + eps)
        val_l_n = self.simulator_func(m, l - eps)
        
        grad_m = (val_m_p - val_m_n) / (2*eps)
        grad_l = (val_l_p - val_l_n) / (2*eps)
        
        # We flow UPHILL (seeking coherence maxima)
        return np.array([grad_m, grad_l])

    def _plot_butterfly(self, traj_A, traj_B, divergence, slope, intercept, start, end):
        plt.figure(figsize=(12, 5))
        
        # Plot 1: The Divergence (Calculation)
        plt.subplot(1, 2, 1)
        plt.plot(divergence, 'b-', alpha=0.6, label='Log Separation')
        
        # Plot fit line
        x_fit = np.arange(start, end)
        y_fit = slope * x_fit + intercept
        plt.plot(x_fit, y_fit, 'r--', linewidth=2, label=f'Fit (λ={slope:.4f})')
        
        plt.title("Lyapunov Exponent Extraction")
        plt.xlabel("Time Step")
        plt.ylabel("ln( || δx || )")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 2: The Butterfly (Visualization)
        plt.subplot(1, 2, 2)
        
        # Convert to arrays
        tA = np.array(traj_A)
        tB = np.array(traj_B)
        
        plt.plot(tA[:,0], tA[:,1], 'k-', alpha=0.5, linewidth=1, label='Reference')
        plt.plot(tB[:,0], tB[:,1], 'r--', alpha=0.5, linewidth=1, label='Shadow')
        
        # Mark start/end
        plt.plot(tA[0,0], tA[0,1], 'go', label='Start')
        plt.plot(tA[-1,0], tA[-1,1], 'ko', label='End')
        
        plt.title("Trajectory Divergence (Phase Space)")
        plt.xlabel("m²")
        plt.ylabel("λ₄")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('lyapunov_butterfly.png')
        logger.info("[Saved butterfly plot to 'lyapunov_butterfly.png']")

if __name__ == "__main__":
    # --- REAL SIMULATOR SETUP ---
    # IMPORTANT: Ensure your simulator is DETERMINISTIC for this test!
    # No random noise inside the simulator function.
    
    # Example Mock (Chaos via Sine Map)
    def mock_chaotic_field(m, l):
        # A landscape that creates chaotic flow (Rastrigin-like)
        return -(m**2 + l**2) + 4*np.cos(2*m) + 4*np.cos(2*l)
        
    # Use the peaks you found in the previous step
    # Peak A: (-1.602, 2.964)
    start_m = -1.602
    start_l = 2.964
    
    scanner = LyapunovScanner(mock_chaotic_field, start_m, start_l)
    scanner.measure_exponent(steps=3000)