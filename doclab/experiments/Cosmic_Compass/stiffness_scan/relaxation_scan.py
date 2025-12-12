import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.fft import fft, fftfreq
import logging
import pandas as pd

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


class SpectralBreathingAnalyzer:
    """
    Takes the time-series 'heartbeat' from the PhasePortraitScanner
    and performs Fourier Analysis to find the characteristic frequency (Mass).
    """
    
    def analyze_spectrum(self, dataframe, sampling_rate=1.0):
        logger.info(f"\n{'='*60}")
        logger.info("SPECTRAL FREQUENCY ANALYSIS")
        logger.info(f"{'='*60}")
        
        # We analyze the Ratio, as it cancels out global mode fluctuations
        # and isolates the relative breathing of the two peaks.
        signal = dataframe['ratio'].values
        
        # Remove the DC offset (mean) so we only see oscillations
        signal = signal - np.mean(signal)
        
        N = len(signal)
        T = 1.0 / sampling_rate
        
        # Perform FFT
        yf = fft(signal)
        xf = fftfreq(N, T)[:N//2]
        
        # Power Spectral Density (PSD)
        power = 2.0/N * np.abs(yf[0:N//2])
        
        # Find dominant frequency
        idx_max = np.argmax(power)
        dom_freq = xf[idx_max]
        dom_power = power[idx_max]
        
        logger.info(f"Dominant Frequency found: {dom_freq:.4f} Hz (simulated)")
        logger.info(f"Spectral Power: {dom_power:.4f}")
        
        if dom_power < 0.001:
            logger.warning("Signal is very weak. Might be pure noise.")
        else:
            logger.info("Strong periodic signal detected!")
            
        self._plot_spectrum(xf, power, dom_freq)
        
        return dom_freq, dom_power

    def _plot_spectrum(self, freq, power, peak_freq):
        plt.figure(figsize=(10, 6))
        
        # Plot the Power Spectrum
        plt.plot(freq, power, 'k-', linewidth=1.5)
        plt.fill_between(freq, power, color='purple', alpha=0.3)
        
        # Mark the peak
        plt.axvline(x=peak_freq, color='r', linestyle='--', label=f'Peak: {peak_freq:.3f}')
        
        plt.title(f"Breathing Spectrum (Characteristic Frequency: {peak_freq:.3f})")
        plt.xlabel("Frequency (Cycles/Step)")
        plt.ylabel("Power Spectral Density")
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        plt.savefig('spectral_analysis.png')
        logger.info("[Saved spectral plot to 'spectral_analysis.png']")

if __name__ == "__main__":
    # --- COMBINED WORKFLOW ---
    
    # 1. Define Simulator (Replace with your logic)
    def mock_simulator(m, l):
        # A mock that actually breathes at frequency 0.15
        t = np.random.randint(0, 100) # Mock time coupling
        base = np.sin(m)*np.cos(l) + 3.0
        breathing = 0.1 * np.sin(2 * np.pi * 0.15 * t)
        return base + breathing + 0.01*np.random.randn()

    # 2. Run Phase Scan (Get the time series)
    # Note: Increase steps to get better frequency resolution!
    scanner = PhasePortraitScanner(
        m_range=(-2.5, 1.5), 
        l_range=(0.0, 5.0),
        simulator_func=mock_simulator
    )
    df_results = scanner.run_diagnostic(steps=500) # Need more steps for FFT
    
    # 3. Run Spectral Analysis
    analyzer = SpectralBreathingAnalyzer()
    analyzer.analyze_spectrum(df_results)