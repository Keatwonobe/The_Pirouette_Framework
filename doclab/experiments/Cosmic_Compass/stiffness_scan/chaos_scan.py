import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import logging
import pandas as pd
from scipy.optimize import minimize

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
class PhasePortraitScanner:
    """
    PASSIVE DIAGNOSTIC MODE
    =======================
    Instead of searching for specific ratios, this scanner:
    1. Locates the two dominant attractors (High Peak and Low Peak).
    2. 'Hovers' over them for N steps to record their time-evolution.
    3. Generates a Phase Portrait to visualize the 'breathing' topology.
    """
    
    def __init__(self, m_range, l_range, simulator_func):
        self.m_range = m_range
        self.l_range = l_range
        self.simulator_func = simulator_func
        self.potential_samples = []

    def _scan_for_peaks(self):
        """Quick rough scan to find the two highest mountains"""
        logger.info("  > Ping-scanning landscape for dominant peaks...")
        
        # 1. Sparse Grid Scan
        best_high = None
        best_low = None # Relative to the high peak (the "harmonic")
        
        # We scan the WHOLE provided range (including the positive m^2 you expanded to)
        m_vals = np.linspace(self.m_range[0], self.m_range[1], 15)
        l_vals = np.linspace(self.l_range[0], self.l_range[1], 15)
        
        samples = []
        for m in m_vals:
            for l in l_vals:
                xi = self.simulator_func(m, l)
                samples.append((m, l, xi))
        
        # Sort by stiffness
        samples.sort(key=lambda x: x[2], reverse=True)
        
        # Peak 1 is just the highest point found
        p1 = samples[0]
        
        # Peak 2 must be far enough away to be a separate mountain
        p2 = None
        for s in samples:
            dist = np.sqrt((s[0]-p1[0])**2 + (s[1]-p1[1])**2)
            if dist > 1.0: # Minimum distance to be considered separate
                p2 = s
                break
        
        if p2 is None:
            p2 = samples[-1] # Fallback to lowest point if no separate peak
            
        return p1, p2

    def run_diagnostic(self, steps=100):
        logger.info(f"\n{'='*60}")
        logger.info("PHASE PORTRAIT DIAGNOSTIC (Passive Mode)")
        logger.info(f"{'='*60}")
        
        # 1. Locate the targets
        p1_rough, p2_rough = self._scan_for_peaks()
        logger.info(f"Target Acquired A: (m={p1_rough[0]:.2f}, l={p1_rough[1]:.2f}) ~ {p1_rough[2]:.2f}")
        logger.info(f"Target Acquired B: (m={p2_rough[0]:.2f}, l={p2_rough[1]:.2f}) ~ {p2_rough[2]:.2f}")
        
        # 2. Refine positions (Climb to the exact summit)
        def get_peak_exact(start_m, start_l):
            res = minimize(
                lambda x: -self.simulator_func(x[0], x[1]),
                [start_m, start_l],
                bounds=[self.m_range, self.l_range],
                method='Nelder-Mead',
                options={'maxiter': 20}
            )
            return res.x[0], res.x[1]

        m1, l1 = get_peak_exact(p1_rough[0], p1_rough[1])
        m2, l2 = get_peak_exact(p2_rough[0], p2_rough[1])
        
        logger.info(f"Locked on Peak A: ({m1:.3f}, {l1:.3f})")
        logger.info(f"Locked on Peak B: ({m2:.3f}, {l2:.3f})")
        
        # 3. The "Stare" (Time Series Recording)
        logger.info(f"\nrecording {steps} frames of breathing data...")
        
        data = []
        for t in range(steps):
            # We add TINY jitter to simulate the 'movement' or thermal noise
            # preventing the simulator from caching the exact result
            noise_scale = 0.001 
            
            # Measure Peak A
            val_a = self.simulator_func(m1 + np.random.randn()*noise_scale, 
                                      l1 + np.random.randn()*noise_scale)
            
            # Measure Peak B
            val_b = self.simulator_func(m2 + np.random.randn()*noise_scale, 
                                      l2 + np.random.randn()*noise_scale)
            
            ratio = val_a / val_b if val_b != 0 else 0
            
            data.append({
                'step': t,
                'xi_A': val_a,
                'xi_B': val_b,
                'ratio': ratio
            })
            
            if t % 20 == 0:
                print(f"  Frame {t}: Ratio = {ratio:.4f}")

        # 4. Analysis & Output
        df = pd.DataFrame(data)
        
        mean_ratio = df['ratio'].mean()
        std_ratio = df['ratio'].std()
        
        logger.info(f"\nDiagnostic Complete.")
        logger.info(f"Mean Ratio: {mean_ratio:.4f}")
        logger.info(f"Stability (StdDev): {std_ratio:.4f}")
        logger.info(f"Noise Floor A: {df['xi_A'].std():.4f}")
        logger.info(f"Noise Floor B: {df['xi_B'].std():.4f}")
        
        # 5. Generate Phase Portrait Plot (Saved to disk)
        self._plot_phase_portrait(df)
        
        return df

    def _plot_phase_portrait(self, df):
        """
        Creates the visualization:
        1. Time Series of the Ratio (The 'Heartbeat')
        2. Phase Portrait (Peak A vs Peak B)
        """
        plt.figure(figsize=(12, 5))
        
        # Subplot 1: The Heartbeat
        plt.subplot(1, 2, 1)
        plt.plot(df['step'], df['ratio'], 'b-', alpha=0.6, label='Instantaneous Ratio')
        plt.axhline(y=df['ratio'].mean(), color='r', linestyle='--', label='Mean')
        plt.fill_between(df['step'], 
                         df['ratio'].mean() - df['ratio'].std(),
                         df['ratio'].mean() + df['ratio'].std(),
                         color='r', alpha=0.1)
        plt.title(f"Resonance Breathing (Mean: {df['ratio'].mean():.3f})")
        plt.xlabel("Simulation Step")
        plt.ylabel("Ratio ξA / ξB")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Subplot 2: Phase Portrait (The physical topology)
        plt.subplot(1, 2, 2)
        plt.scatter(df['xi_A'], df['xi_B'], c=df['step'], cmap='viridis', alpha=0.5)
        plt.colorbar(label='Time Step')
        plt.title("Phase Portrait (Stiffness A vs B)")
        plt.xlabel("Stiffness Peak A")
        plt.ylabel("Stiffness Peak B")
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('resonance_diagnostic.png')
        logger.info("\n[Saved diagnostic plot to 'resonance_diagnostic.png']")
        logger.info("Check this image: A circular pattern indicates a real breathing mode.")
        logger.info("A fuzzy blob indicates pure noise.")

class RecurrenceScanner:
    """
    VISUALIZING CHAOS
    =================
    Constructs a Recurrence Plot to detect deterministic structure
    hidden inside apparent noise.
    
    White points = System state is "far" from history.
    Black points = System has returned to a previous state ("Ghost").
    """
    
    def scan_texture(self, dataframe, threshold_percentile=10):
        logger.info(f"\n{'='*60}")
        logger.info("RECURRENCE TEXTURE SCAN")
        logger.info(f"{'='*60}")
        
        # 1. Extract the Phase Space Trajectory
        # We use both Peak A and Peak B to define the "State"
        data = dataframe[['xi_A', 'xi_B']].values
        
        # Normalize dimensions so they contribute equally
        data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
        
        # 2. Calculate Distance Matrix
        # Computes distance between every single step and every other step
        dist_matrix = squareform(pdist(data, metric='euclidean'))
        
        # 3. Apply Threshold (The "Epsilon" ball)
        # We define "Recurrence" as being within the top X% closest points
        threshold = np.percentile(dist_matrix, threshold_percentile)
        recurrence_matrix = dist_matrix < threshold
        
        logger.info(f"Recurrence Threshold: {threshold:.4f} (Euclidean Distance)")
        logger.info(f"analyzing {len(data)}x{len(data)} state interactions...")
        
        # 4. Plotting
        self._plot_recurrence(recurrence_matrix, dist_matrix)
        
    def _plot_recurrence(self, binary_matrix, dist_matrix):
        plt.figure(figsize=(12, 5))
        
        # Plot 1: The Distance Matrix (The "Texture")
        plt.subplot(1, 2, 1)
        plt.imshow(dist_matrix, cmap='magma_r', origin='lower')
        plt.colorbar(label='State Distance')
        plt.title("Distance Matrix (Texture)")
        plt.xlabel("Time Step")
        plt.ylabel("Time Step")
        
        # Plot 2: The Recurrence Plot (The "Structure")
        plt.subplot(1, 2, 2)
        # We plot black dots for recurrence
        plt.imshow(binary_matrix, cmap='Greys', origin='lower')
        plt.title("Recurrence Plot (Structure)")
        plt.xlabel("Time Step")
        plt.ylabel("Time Step")
        
        plt.tight_layout()
        plt.savefig('recurrence_plot.png')
        logger.info("[Saved recurrence plot to 'recurrence_plot.png']")
        logger.info("\nINTERPRETATION GUIDE:")
        logger.info("1. Diagonal Lines: Deterministic Chaos (The system follows rules).")
        logger.info("2. Vertical/Horizontal Blocks: Laminarity (The system gets stuck).")
        logger.info("3. Scattered Dust: Pure Noise (No physics).")

if __name__ == "__main__":
    # --- COMBINED WORKFLOW ---
    # 1. Define Simulator (Replace with your REAL one)
    def mock_simulator(m, l):
        # A chaotic map (Logistic Map behavior)
        # This simulates a system that is deterministic but looks random
        import time
        t = (time.time() * 1000) % 100 # Seeding from system time for jitter
        val = np.sin(m * l) * np.cos(t/10.0) 
        if val > 0.5: val = 0.5 # The "Wall" (Saturation)
        if val < -0.5: val = -0.5
        return val + 0.05 * np.random.randn()

    # 2. Run Phase Scan (Get data)
    # Note: Recurrence plots are heavy (N^2), so keep steps around 200-400
    scanner = PhasePortraitScanner(
        m_range=(-2.5, 1.5), 
        l_range=(0.0, 5.0),
        simulator_func=mock_simulator
    )
    df_results = scanner.run_diagnostic(steps=300)
    
    # 3. Run Recurrence Scan
    rec_scanner = RecurrenceScanner()
    rec_scanner.scan_texture(df_results)