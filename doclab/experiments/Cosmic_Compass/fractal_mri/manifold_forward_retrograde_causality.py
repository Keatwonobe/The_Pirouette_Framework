import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# Core Hénon–Heiles dynamics
# ------------------------------

def henon_potential(m, l):
    """Hénon–Heiles potential V(m,l)."""
    return 0.5 * (m**2 + l**2) + (m**2 * l - l**3 / 3.0)

def henon_grad(m, l):
    """Gradient ∇V for Hénon–Heiles."""
    dV_dm = m + 2.0 * m * l
    dV_dl = l + (m**2 - l**2)
    return dV_dm, dV_dl


# ------------------------------
# Forward-time: local Lyapunov tension
# ------------------------------

def forward_tension(m0, l0, dt=0.02, steps=120, kick=1e-5, escape_R=20.0):
    """
    Local Lyapunov proxy around (m0, l0).

    We launch two nearby trajectories, measure their separation,
    and return log(max separation) as an effective 'tension'.
    """
    m1, l1 = m0, l0
    m2, l2 = m0 + kick, l0 + kick
    pm1 = pl1 = pm2 = pl2 = 0.0

    max_div = 0.0

    for _ in range(steps):
        # trajectory 1
        g1m, g1l = henon_grad(m1, l1)
        pm1 -= 0.5 * dt * g1m
        pl1 -= 0.5 * dt * g1l
        m1  += dt * pm1
        l1  += dt * pl1

        # trajectory 2
        g2m, g2l = henon_grad(m2, l2)
        pm2 -= 0.5 * dt * g2m
        pl2 -= 0.5 * dt * g2l
        m2  += dt * pm2
        l2  += dt * pl2

        # separation
        d = np.hypot(m2 - m1, l2 - l1)
        max_div = max(max_div, d)

        # bail out if we clearly escaped
        if (m1**2 + l1**2) > escape_R**2:
            break

    return np.log(max_div + kick)


# ------------------------------
# Retrograde-time: dissipative lifetime
# ------------------------------

def retro_lifetime(m0, l0, dt=0.02, gamma=0.015,
                   steps=4000, escape_R=5.0, v_eps=1e-4):
    """
    A scalar version of the Entropy Anchor's sedimentation:

    - start at (m0, l0) with zero velocity;
    - evolve under Hénon–Heiles + linear friction;
    - integrate the path length until either:
        * particle escapes past escape_R, or
        * velocity falls below v_eps (frozen).
    Returns the total distance travelled.
    """
    m, l = m0, l0
    vm = vl = 0.0
    path = 0.0

    for _ in range(steps):
        # gradient
        g_m, g_l = henon_grad(m, l)

        # friction + force
        vm += dt * (-g_m - gamma * vm)
        vl += dt * (-g_l - gamma * vl)

        # move
        dm = dt * vm
        dl = dt * vl
        m += dm
        l += dl

        step_len = np.hypot(dm, dl)
        path += step_len

        r2 = m*m + l*l
        v2 = vm*vm + vl*vl

        if r2 > escape_R**2:
            break
        if v2 < v_eps**2:
            break

    return path


# ------------------------------
# Shoreline finder: energy contour V = 1/6
# ------------------------------

def find_energy_edge(angle, E=1.0/6.0, r_min=0.0, r_max=2.0, iters=40):
    """
    For a given polar angle θ, find r such that V(r cosθ, r sinθ) = E
    using a simple bisection search.
    """
    # Bracket the root by scanning outward until V > E
    r_hi = r_min
    for r in np.linspace(r_min, r_max, 60):
        m = r * np.cos(angle)
        l = r * np.sin(angle)
        if henon_potential(m, l) >= E:
            r_hi = r
            break
    else:
        # didn't cross within range; just return None
        return None

    r_lo = max(r_min, r_hi - (r_max - r_min) / 60.0)

    for _ in range(iters):
        r_mid = 0.5 * (r_lo + r_hi)
        m_mid = r_mid * np.cos(angle)
        l_mid = r_mid * np.sin(angle)
        V_mid = henon_potential(m_mid, l_mid)
        if V_mid > E:
            r_hi = r_mid
        else:
            r_lo = r_mid

    return 0.5 * (r_lo + r_hi)


# ------------------------------
# Scanner tying both faces together
# ------------------------------

class ForwardRetroScanner:
    def __init__(self,
                 n_angles=120,
                 scan_width=0.2,
                 scan_depth=120,
                 dt_forward=0.02,
                 dt_retro=0.02,
                 gamma=0.015):
        self.n_angles   = n_angles
        self.scan_width = scan_width
        self.scan_depth = scan_depth
        self.dt_f       = dt_forward
        self.dt_r       = dt_retro
        self.gamma      = gamma

    def scan_angle(self, theta):
        """
        For a single shoreline angle:
        - find energy contour r_edge;
        - sample a line across the edge;
        - compute forward tension & retro lifetime at each point.
        """
        r_edge = find_energy_edge(theta)
        if r_edge is None:
            return None

        rs = np.linspace(
            r_edge - self.scan_width/2,
            r_edge + self.scan_width/2,
            self.scan_depth
        )
        # normalized distance: 0 at the edge, [-0.5, 0.5] across window
        x = np.linspace(-0.5, 0.5, self.scan_depth)

        f_tension = []
        r_life    = []

        for r in rs:
            m = r * np.cos(theta)
            l = r * np.sin(theta)

            t_val = forward_tension(m, l, dt=self.dt_f)
            f_tension.append(t_val)

            life_val = retro_lifetime(m, l, dt=self.dt_r, gamma=self.gamma)
            # log to compress dynamic range, like your entropy-anchor map
            r_life.append(np.log1p(life_val))

        return x, np.array(f_tension), np.array(r_life)

    def run(self, seed=0):
        rng = np.random.default_rng(seed)
        angles = rng.uniform(0, 2*np.pi, self.n_angles)

        all_forward = []
        all_retro   = []

        for i, theta in enumerate(angles):
            res = self.scan_angle(theta)
            if res is None:
                continue
            x, f_t, r_l = res
            all_forward.append(f_t)
            all_retro.append(r_l)

        all_forward = np.vstack(all_forward)
        all_retro   = np.vstack(all_retro)

        # Averages along the shoreline
        mean_forward = all_forward.mean(axis=0)
        mean_retro   = all_retro.mean(axis=0)

        # --------------------------
        # Plot 1: averaged profiles
        # --------------------------
        fig, ax = plt.subplots(figsize=(10, 6), facecolor="#000000")
        ax.set_facecolor("#000000")

        ax.plot(x, mean_forward, label="Forward Tension (Lyapunov)", color="lime")
        ax.plot(x, mean_retro,   label="Retro Lifetime (log path)", color="cyan")

        ax.axvline(0.0, color="white", linestyle="--", alpha=0.4,
                   label="Stability Edge")

        ax.set_xlabel("Distance relative to stability edge", color="white")
        ax.set_ylabel("Metric value", color="white")
        ax.set_title("Forward vs Retrograde Profiles Across the Shoreline",
                     color="white")

        ax.tick_params(colors="white")
        ax.legend(facecolor="#111111", edgecolor="#444444")
        ax.grid(alpha=0.2, color="#444444")

        plt.tight_layout()
        plt.savefig("forward_retro_profiles.png", dpi=150,
                    facecolor="#000000")
        plt.show()

        # --------------------------
        # Plot 2: pointwise correlation
        # --------------------------
        fig2, ax2 = plt.subplots(figsize=(6, 6), facecolor="#000000")
        ax2.set_facecolor("#000000")

        ax2.scatter(all_forward.ravel(), all_retro.ravel(),
                    s=2, alpha=0.15, color="magenta")

        ax2.set_xlabel("Forward tension (Lyapunov)", color="white")
        ax2.set_ylabel("Retro lifetime (log path)", color="white")
        ax2.set_title("Pointwise correlation across all shoreline probes",
                      color="white")
        ax2.tick_params(colors="white")
        ax2.grid(alpha=0.2, color="#444444")

        plt.tight_layout()
        plt.savefig("forward_retro_correlation.png", dpi=150,
                    facecolor="#000000")
        plt.show()


if __name__ == "__main__":
    scanner = ForwardRetroScanner(
        n_angles=180,
        scan_width=0.2,
        scan_depth=140,
        dt_forward=0.02,
        dt_retro=0.02,
        gamma=0.015
    )
    scanner.run()
