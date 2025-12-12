import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class SniperFitter:
    def __init__(self):
        # Physics Constants
        self.dt = 0.02  # Finer time step for precision
        self.max_steps = 30000 
        
    def gradient(self, m, l):
        dm = m + 2 * m * l
        dl = l + (m**2 - l**2)
        return dm, dl

    def integrate_probe(self, m_start, l_start):
        m, l = m_start, l_start
        pm, pl = 0.0, 0.0
        
        for t in range(self.max_steps):
            # Leapfrog
            dm, dl = self.gradient(m, l)
            pm -= 0.5 * self.dt * dm
            pl -= 0.5 * self.dt * dl
            m += self.dt * pm
            l += self.dt * pl
            dm, dl = self.gradient(m, l)
            pm -= 0.5 * self.dt * dm
            pl -= 0.5 * self.dt * dl
            
            # Escape
            if (m**2 + l**2) > 20.0:
                return t * self.dt, np.arctan2(l, m)
                
        return None, None

    def find_highest_peak(self):
        """Finds the sharpest separatrix (highest escape time) in a broad region."""
        logger.info("[-] BROAD SCAN: Hunting for a Spire...")
        
        # Scan the transition zone we found earlier
        m_vals = np.linspace(0.8, 1.2, 1000) # Known active area for Henon-Heiles
        times = []
        
        for m in m_vals:
            t, _ = self.integrate_probe(m, 0.0)
            if t is None: t = 0
            times.append(t)
            
        times = np.array(times)
        
        # Find the absolute tallest spike
        peak_idx = np.argmax(times)
        peak_m = m_vals[peak_idx]
        peak_time = times[peak_idx]
        
        logger.info(f"[+] TARGET ACQUIRED: Spire at M={peak_m:.6f} (Height: {peak_time:.2f})")
        return peak_m

    def run_sniper_shot(self):
        # 1. Locate the Mountain
        target_m = self.find_highest_peak()
        
        # 2. Zoom in MICROSCOPICALLY
        # We scan just one side of the mountain to get the clean logarithmic slope
        width = 0.0005 # Tiny window
        
        logger.info(f"[-] SNIPER SCOPE: Zooming to {target_m} +/- {width}...")
        
        # We scan moving AWAY from the peak (down the slope)
        m_vals = np.linspace(target_m, target_m + width, 200)
        
        r_vals = [] # Distance from peak
        t_vals = [] # Escape time
        theta_vals = [] # Exit angle
        
        for m in m_vals:
            t, theta = self.integrate_probe(m, 0.0)
            if t is not None:
                # Distance from the peak (r)
                r = m - target_m
                if r > 1e-9: # Avoid log(0)
                    r_vals.append(r)
                    t_vals.append(t)
                    theta_vals.append(theta)
        
        # Convert to arrays
        r_vals = np.array(r_vals)
        t_vals = np.array(t_vals)
        theta_vals = np.unwrap(np.array(theta_vals))
        
        if len(t_vals) < 10:
            logger.error("Not enough data on the slope. Try adjusting the window.")
            return

        self.fit_and_report(r_vals, t_vals, theta_vals)

    def fit_and_report(self, r, t, theta):
        logger.info("[-] PERFORMING GENETIC SEQUENCING...")
        
        # Model 1: Decoherence (T ~ -ln(r))
        def model_time(r, lam, offset):
            return offset - (1.0/lam) * np.log(r)
        
        # Initial guess: Lambda usually ~1.0, Offset ~peak height
        popt_t, _ = curve_fit(model_time, r, t, p0=[1.0, np.max(t)], maxfev=10000)
        lam = popt_t[0]
        
        # Model 2: Rotation (Theta ~ omega * T)
        def model_phase(t, omega, offset):
            return offset + omega * t
            
        popt_p, _ = curve_fit(model_phase, t, theta, p0=[1.0, 0], maxfev=10000)
        omega = popt_p[0]
        
        logger.info("\n" + "="*40)
        logger.info(f" FRACTAL GENOME SEQUENCED")
        logger.info(f" ="*40)
        logger.info(f" [+] LYAPUNOV STRENGTH (Lambda): {lam:.5f}")
        logger.info(f" [+] ROTATION SPEED (Omega):     {omega:.5f}")
        logger.info("="*40 + "\n")
        
        self.plot_sniper_results(r, t, theta, model_time, model_phase, popt_t, popt_p)

    def plot_sniper_results(self, r, t, theta, func_t, func_p, popt_t, popt_p):
        fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor='#0f0f0f')
        
        # Plot 1: The Slope
        axes[0].scatter(r, t, c='cyan', s=15, alpha=0.6, label='Real Physics')
        axes[0].plot(r, func_t(r, *popt_t), 'r--', lw=2, label=f'Fit (λ={popt_t[0]:.4f})')
        axes[0].set_title("The Cliff Edge (Logarithmic Decay)", color='white')
        axes[0].set_xlabel("Distance from Peak (r)", color='white')
        axes[0].set_ylabel("Escape Time", color='white')
        axes[0].legend()
        axes[0].grid(alpha=0.2)
        
        # Plot 2: The Spiral
        axes[1].scatter(t, theta, c='magenta', s=15, alpha=0.6, label='Real Physics')
        axes[1].plot(t, func_p(t, *popt_p), 'g--', lw=2, label=f'Fit (ω={popt_p[0]:.4f})')
        axes[1].set_title("The Pirouette (Rotation vs Time)", color='white')
        axes[1].set_xlabel("Escape Time", color='white')
        axes[1].set_ylabel("Exit Angle", color='white')
        axes[1].legend()
        axes[1].grid(alpha=0.2)
        
        for ax in axes:
            ax.set_facecolor('#0f0f0f')
            ax.tick_params(colors='white')
            
        plt.suptitle(f"SNIPER ANALYSIS: λ={popt_t[0]:.4f} | ω={popt_p[0]:.4f}", color='white', fontsize=16)
        plt.tight_layout()
        plt.savefig("sniper_calibration.png")
        plt.show()

if __name__ == "__main__":
    sniper = SniperFitter()
    sniper.run_sniper_shot()