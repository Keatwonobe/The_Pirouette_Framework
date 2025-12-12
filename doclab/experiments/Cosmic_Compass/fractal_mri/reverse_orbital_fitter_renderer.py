import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class PirouetteFitter:
    def __init__(self):
        # Physics Constants (Standard Hénon-Heiles)
        self.dt = 0.05 
        self.max_steps = 20000 # Increased to catch slow escapes
        
    def gradient(self, m, l):
        """The Force Field of the Pirouette"""
        dm = m + 2 * m * l
        dl = l + (m**2 - l**2)
        return dm, dl

    def integrate_probe(self, m_start, l_start):
        """Runs a single particle until it escapes."""
        m, l = m_start, l_start
        pm, pl = 0.0, 0.0
        
        for t in range(self.max_steps):
            # Leapfrog Integration
            dm, dl = self.gradient(m, l)
            pm -= 0.5 * self.dt * dm
            pl -= 0.5 * self.dt * dl
            m += self.dt * pm
            l += self.dt * pl
            dm, dl = self.gradient(m, l)
            pm -= 0.5 * self.dt * dm
            pl -= 0.5 * self.dt * dl
            
            # Escape Condition
            if (m**2 + l**2) > 20.0:
                # Return Escape Time (Z) and Exit Angle (Phase)
                return t * self.dt, np.arctan2(l, m)
                
        return None, None # Did not escape (stuck in core)

    def find_event_horizon(self):
        """
        Scans from the center outward to find where the stable core ends 
        and the chaotic cliffs begin.
        """
        logger.info("[-] SEARCHING FOR EVENT HORIZON...")
        
        # Scan wide: 0.0 (Center) to 1.2 (Likely Escape)
        scan_points = 100
        test_m = np.linspace(0.0, 1.2, scan_points)
        test_l = 0.0 # Scan along the symmetry axis
        
        escapes = []
        
        for m in test_m:
            t, _ = self.integrate_probe(m, test_l)
            if t is not None:
                escapes.append((m, t))
            else:
                # Mark stable points with -1
                escapes.append((m, -1))
        
        # Analyze the boundary
        escapes = np.array(escapes)
        mask_escaped = escapes[:, 1] > 0
        
        if not np.any(mask_escaped):
            logger.error("[!] CRITICAL: No escapes found even in wide scan.")
            logger.error("    The system might be too stable or max_steps too low.")
            sys.exit(1)
            
        # Find the first point that escaped
        first_escape_idx = np.argmax(mask_escaped)
        boundary_m = escapes[first_escape_idx, 0]
        
        logger.info(f"[+] Event Horizon detected at M ≈ {boundary_m:.4f}")
        return boundary_m

    def run_calibration(self):
        # 1. Find where the action is
        horizon_m = self.find_event_horizon()
        
        # 2. Define the High-Res Probe Zone
        # We look specifically at the transition zone (just past the horizon)
        logger.info("[-] INITIATING FORENSIC PROBE ON HORIZON...")
        
        # Scan a small window around the horizon
        start_m = horizon_m
        end_m = horizon_m + 0.2 
        
        scan_points = 400
        m_vals = np.linspace(start_m, end_m, scan_points)
        l_fixed = 0.0
        
        results_r = [] # Distance from "Singularity"
        results_t = [] # Escape Time
        results_theta = [] # Exit Angle
        
        logger.info(f"[-] Scanning {scan_points} trajectories ({start_m:.2f} to {end_m:.2f})...")
        
        times = []
        coords = []
        thetas = []
        
        for m in m_vals:
            t, theta = self.integrate_probe(m, l_fixed)
            if t is not None:
                times.append(t)
                coords.append(m)
                thetas.append(theta)
                
        if len(times) < 10:
             logger.error("Not enough data points collected for a fit.")
             sys.exit(1)

        # In this zone, higher M = faster escape (usually)
        # So the "Singularity" (Infinite time) is actually backwards -> towards the center.
        # We treat 'horizon_m' as the effective singularity for this local region.
        
        times = np.array(times)
        coords = np.array(coords)
        thetas = np.unwrap(np.array(thetas))
        
        # Distance from the cliff edge
        r_dist = coords - (horizon_m - 0.001) 
        
        self.fit_models(r_dist, times, thetas)

    def fit_models(self, r, t, theta):
        logger.info("[-] FITTING 'REVERSE ORBITAL' MODELS...")
        
        # Clean data (remove NaNs or Infs)
        valid = (r > 0) & (t > 0)
        r = r[valid]
        t = t[valid]
        theta = theta[valid]
        
        # MODEL 1: DECOHERENCE TIME
        # Theory: T = C - (1/lambda) * ln(r)
        # We approximate the "singularity" as the cliff edge.
        def time_model(r, lam, const):
            # Add small epsilon to r to prevent log(0) error during fitting search
            return const - (1.0/lam) * np.log(r + 1e-9)
        
        try:
            popt_time, _ = curve_fit(time_model, r, t, p0=[0.5, 100], maxfev=5000)
            calc_lambda = popt_time[0]
            logger.info(f"[+] CALCULATED LYAPUNOV LAMBDA: {calc_lambda:.5f}")
        except Exception as e:
            logger.warning(f"Lambda Fit failed: {e}. Defaulting to 1.0")
            calc_lambda = 1.0
            popt_time = [1.0, 100]
        
        # MODEL 2: PHASE ROTATION
        # Theory: Theta = Theta0 + Omega * T
        def phase_model(t, omega, theta0):
            return theta0 + omega * t
        
        try:
            popt_phase, _ = curve_fit(phase_model, t, theta, p0=[1.0, 0], maxfev=5000)
            calc_omega = popt_phase[0]
            logger.info(f"[+] CALCULATED ANGULAR OMEGA: {calc_omega:.5f}")
        except Exception as e:
            logger.warning(f"Omega Fit failed: {e}. Defaulting to 1.0")
            calc_omega = 1.0
            popt_phase = [1.0, 0]
        
        self.plot_results(r, t, theta, time_model, phase_model, popt_time, popt_phase)
        return calc_lambda, calc_omega

    def plot_results(self, r, t, theta, time_func, phase_func, popt_t, popt_p):
        fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor='#111')
        
        # Plot 1: Distance vs Time
        axes[0].scatter(r, t, c='cyan', s=10, alpha=0.5, label='Real Physics')
        r_smooth = np.linspace(min(r), max(r), 100)
        axes[0].plot(r_smooth, time_func(r_smooth, *popt_t), 'r--', linewidth=2, label=f'Fit (Lambda={popt_t[0]:.3f})')
        axes[0].set_xlabel("Distance from Edge", color='white')
        axes[0].set_ylabel("Escape Time", color='white')
        axes[0].set_title("Decoherence Profile", color='white')
        axes[0].legend()
        axes[0].grid(True, alpha=0.2)
        
        # Plot 2: Time vs Angle
        axes[1].scatter(t, theta, c='magenta', s=10, alpha=0.5, label='Real Physics')
        t_smooth = np.linspace(min(t), max(t), 100)
        axes[1].plot(t_smooth, phase_func(t_smooth, *popt_p), 'g--', linewidth=2, label=f'Fit (Omega={popt_p[0]:.3f})')
        axes[1].set_xlabel("Escape Time", color='white')
        axes[1].set_ylabel("Exit Angle", color='white')
        axes[1].set_title("Pirouette Rotation", color='white')
        axes[1].legend()
        axes[1].grid(True, alpha=0.2)
        
        for ax in axes:
            ax.tick_params(colors='white')
            ax.set_facecolor('#111')
        
        plt.suptitle(f"FRACTAL GENETICS: λ={popt_t[0]:.4f} | ω={popt_p[0]:.4f}", color='white', fontsize=16)
        plt.tight_layout()
        plt.savefig("pirouette_calibration_fixed.png")
        logger.info("Calibration plot saved to 'pirouette_calibration_fixed.png'")
        plt.show()

if __name__ == "__main__":
    fitter = PirouetteFitter()
    fitter.run_calibration()