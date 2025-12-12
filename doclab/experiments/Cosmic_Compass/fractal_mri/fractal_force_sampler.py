import numpy as np
import matplotlib.pyplot as plt
import logging
from scipy.interpolate import make_interp_spline

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def henon_heiles_grad(m, l):
    """Gradient of the Hénon–Heiles potential."""
    dV_dm = m + 2*m*l
    dV_dl = l + (m**2 - l**2)
    return np.array([dV_dm, dV_dl])

class FractalForceSampler:
    def __init__(self, samples=60, scan_depth=50):
        self.samples = samples
        self.scan_depth = scan_depth # How many steps to scan across the boundary
        self.dt = 0.1
        self.kick = 1e-5
        self.max_sim_steps = 400
        
        # Colors for the basins
        self.palette = {
            1: "#ff3333", # Weak (Red)
            2: "#ffaa00", # EM (Gold)
            3: "#00cccc"  # Strong (Teal)
        }
        self.labels = {
            1: "Weak (Red)",
            2: "EM (Gold)",
            3: "Strong (Teal)"
        }

    def get_fate(self, m, l):
        """Runs a particle to determine which basin it falls into."""
        pm, pl = 0.0, 0.0
        for _ in range(self.max_sim_steps):
            g = henon_heiles_grad(m, l)
            pm -= 0.5 * self.dt * g[0]
            pl -= 0.5 * self.dt * g[1]
            m += self.dt * pm
            l += self.dt * pl
            g = henon_heiles_grad(m, l)
            pm -= 0.5 * self.dt * g[0]
            pl -= 0.5 * self.dt * g[1]
            
            if (m**2 + l**2) > 20.0:
                angle = np.arctan2(l, m)
                # Map angle to basin ID
                # Top: 1, Right: 2, Left: 3 (approximate sectors)
                if 0.5 < angle < 2.5: return 1 # Red/Top
                elif angle > 2.5 or angle < -2.5: return 3 # Teal/Left
                else: return 2 # Gold/Right
        return 0 # Trapped

    def measure_tension(self, m, l):
        """Measures local Lyapunov divergence (Tension)."""
        m1, l1 = m, l
        m2, l2 = m + self.kick, l + self.kick
        pm1, pl1, pm2, pl2 = 0.0, 0.0, 0.0, 0.0
        
        max_div = 0.0
        
        # Short burst simulation for local tension
        for _ in range(100):
            # Reality
            g1 = henon_heiles_grad(m1, l1)
            pm1 -= 0.5 * self.dt * g1[0]
            pl1 -= 0.5 * self.dt * g1[1]
            m1 += self.dt * pm1
            l1 += self.dt * pl1
            g1 = henon_heiles_grad(m1, l1)
            pm1 -= 0.5 * self.dt * g1[0]
            pl1 -= 0.5 * self.dt * g1[1]

            # Shadow
            g2 = henon_heiles_grad(m2, l2)
            pm2 -= 0.5 * self.dt * g2[0]
            pl2 -= 0.5 * self.dt * g2[1]
            m2 += self.dt * pm2
            l2 += self.dt * pl2
            g2 = henon_heiles_grad(m2, l2)
            pm2 -= 0.5 * self.dt * g2[0]
            pl2 -= 0.5 * self.dt * g2[1]

            dist = np.sqrt((m1-m2)**2 + (l1-l2)**2)
            max_div = max(max_div, dist)
            
            if (m1**2 + l1**2) > 20.0: break
            
        return np.log(max_div + self.kick)

    def find_shoreline(self, angle):
        """Marches out from center to find the exact edge of stability."""
        # Binary search for the edge
        r_min = 0.0
        r_max = 2.0
        boundary_r = None
        basin_id = 0
        
        # Coarse search
        for r in np.linspace(0, 1.5, 30):
            m = r * np.cos(angle)
            l = r * np.sin(angle)
            fate = self.get_fate(m, l)
            if fate != 0:
                r_max = r
                r_min = r - (1.5/30)
                basin_id = fate
                break
        
        if basin_id == 0: return None, 0 # Never escaped
        
        # Fine search (Binary)
        for _ in range(10):
            r_mid = (r_min + r_max) / 2
            m = r_mid * np.cos(angle)
            l = r_mid * np.sin(angle)
            fate = self.get_fate(m, l)
            if fate == 0:
                r_min = r_mid
            else:
                r_max = r_mid
                basin_id = fate # Update fate just in case
                
        return r_max, basin_id

    def run_sampler(self):
        logger.info(f"Launching {self.samples} probes into the fractal...")

        results = {1: [], 2: [], 3: []}
        angles = np.random.uniform(0, 2*np.pi, self.samples)

        for i, angle in enumerate(angles):
            if i % 10 == 0:
                logger.info(f"...probe {i}/{self.samples}")

            edge_r, basin_id = self.find_shoreline(angle)
            if basin_id == 0:
                continue

            scan_window = 0.2
            r_points = np.linspace(edge_r - scan_window/2, edge_r + scan_window/2, self.scan_depth)

            tensions = []
            for r in r_points:
                m = r * np.cos(angle)
                l = r * np.sin(angle)
                tensions.append(self.measure_tension(m, l))

            x_vals = np.linspace(-0.5, 0.5, self.scan_depth)
            results[basin_id].append((x_vals, np.array(tensions)))

        return self._plot_results(results)


    def _plot_results(self, results):
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 8))

        logger.info("Plotting statistical families...")

        avg_data = {1: [], 2: [], 3: []}

        for basin_id, profiles in results.items():
            color = self.palette[basin_id]
            label = self.labels[basin_id]

            first = True
            for x, y in profiles:
                ax.plot(x, y, color=color, alpha=0.15, linewidth=1)
                avg_data[basin_id].append(y)

                if first:
                    ax.plot([], [], color=color, label=label, linewidth=2)
                    first = False

        # RETURNABLES
        strong_mean = None
        em_mean = None
        weak_mean = None
        x_coords = None

        for basin_id, y_list in avg_data.items():
            if not y_list:
                continue

            y_stack = np.vstack(y_list)
            y_mean = np.mean(y_stack, axis=0)
            x_axis = np.linspace(-0.5, 0.5, len(y_mean))

            # Save into returnables
            if basin_id == 1:
                weak_mean = y_mean
            elif basin_id == 2:
                em_mean = y_mean
            elif basin_id == 3:
                strong_mean = y_mean

            x_coords = x_axis  # all basins share same x-axis

            X_Y_Spline = make_interp_spline(x_axis, y_mean)
            X_ = np.linspace(x_axis.min(), x_axis.max(), 500)
            Y_ = X_Y_Spline(X_)

            ax.plot(X_, Y_, color=self.palette[basin_id], linewidth=4)
            ax.plot(X_, Y_, color='white', linewidth=1, linestyle="--", alpha=0.7)

        ax.axvline(0, color='white', linestyle=':', alpha=0.5, label="Shoreline (Stability Edge)")
        ax.set_title("Universal Force Profiles: Statistical Shoreline Scan", fontsize=16)
        ax.set_xlabel("Distance relative to Stability Edge")
        ax.set_ylabel("Manifold Tension (Lyapunov)")
        ax.legend()
        ax.grid(True, alpha=0.2)

        plt.tight_layout()
        plt.savefig("fractal_force_statistics.png", dpi=150)
        plt.show()

        return x_coords, strong_mean, em_mean, weak_mean


def fit_coupling_from_profile(x, T, fit_window=(0.0, 0.08)):
    """
    Estimate a coupling 'g' from a shoreline tension profile T(x).

    Parameters
    ----------
    x : 1D array
        Distance relative to stability edge (same units as your plots).
    T : 1D array
        Mean manifold tension (Lyapunov) for one force.
    fit_window : (float, float)
        Interval [x_min, x_max] *inside* the manifold over which to fit
        a straight line. Default is [0.0, 0.08].

    Returns
    -------
    g : float
        Coupling strength, defined as minus the best-fit slope dT/dx
        over the chosen window (so larger g = steeper drop = stronger coupling).
    a, b : float
        Raw slope and intercept (T ≈ a x + b) for reference.
    """
    x_min, x_max = fit_window

    # mask just inside the shoreline
    mask = (x >= x_min) & (x <= x_max)
    x_fit = x[mask]
    T_fit = T[mask]

    if x_fit.size < 3:
        raise ValueError("Not enough points in fit window – adjust fit_window or resolution.")

    # least-squares fit: T = a x + b
    A = np.vstack([x_fit, np.ones_like(x_fit)]).T
    a, b = np.linalg.lstsq(A, T_fit, rcond=None)[0]

    g = -a  # define coupling as minus the slope (positive number)
    return g, a, b


def compare_couplings(x_coords, strong_mean, em_mean, weak_mean,
                      fit_window=(0.0, 0.08)):
    """
    Fit couplings for the three forces and print the ratios.
    """
    g_s, a_s, b_s = fit_coupling_from_profile(x_coords, strong_mean, fit_window)
    g_em, a_em, b_em = fit_coupling_from_profile(x_coords, em_mean, fit_window)
    g_w, a_w, b_w = fit_coupling_from_profile(x_coords, weak_mean, fit_window)

    print("\n=== Coupling fit (shoreline gradient method) ===")
    print(f"Fit window: x in [{fit_window[0]}, {fit_window[1]}]")
    print(f"g_strong  ≈ {g_s:.4g}   (slope a_s = {a_s:.4g})")
    print(f"g_EM      ≈ {g_em:.4g}   (slope a_em = {a_em:.4g})")
    print(f"g_weak    ≈ {g_w:.4g}   (slope a_w = {a_w:.4g})")

    # Ratios
    print("\nRatios (unnormalized):")
    print(f"g_strong / g_EM   ≈ {g_s / g_em:.4g}")
    print(f"g_strong / g_weak ≈ {g_s / g_w:.4g}")
    print(f"g_EM / g_weak     ≈ {g_em / g_w:.4g}")

    # Optionally return if you want to use them in v10
    return {
        "g_strong": g_s,
        "g_EM": g_em,
        "g_weak": g_w,
        "ratio_s_EM": g_s / g_em,
        "ratio_s_w": g_s / g_w,
        "ratio_EM_w": g_em / g_w,
    }

if __name__ == "__main__":
    sampler = FractalForceSampler(samples=6000)
    x_coords, strong_mean, em_mean, weak_mean = sampler.run_sampler()

    coupling_info = compare_couplings(
        x_coords,
        strong_mean,
        em_mean,
        weak_mean,
        fit_window=(0.0, 0.08)
    )

    print(coupling_info)
