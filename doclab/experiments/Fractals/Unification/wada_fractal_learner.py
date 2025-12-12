import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple, Dict, Any, List


# ============================================================
# 1. Prism / Hénon–Heiles dynamics
#    (same core as get_basin_single + stress from wada_randomizer.ts)
# ============================================================

def step_prism(m: float, l: float,
               pm: float, pl: float,
               dt: float,
               sigma: float = 1.0) -> Tuple[float, float, float, float, float]:
    """
    One velocity-Verlet step of the prism system.
    Returns (m_new, l_new, pm_new, pl_new, step_stress).
    """
    # First force evaluation
    fm = -(m + 2 * sigma * m * l)
    fl = -(l + sigma * (m * m - l * l))

    # 'Stress' ~ integrated |F| * dt (energy-like cost)
    force_mag = np.sqrt(fm * fm + fl * fl)
    step_stress = force_mag * dt

    # Half kick momenta
    pm += 0.5 * dt * fm
    pl += 0.5 * dt * fl

    # Drift positions
    m += dt * pm
    l += dt * pl

    # Second force evaluation
    fm2 = -(m + 2 * sigma * m * l)
    fl2 = -(l + sigma * (m * m - l * l))

    # Half kick again
    pm += 0.5 * dt * fm2
    pl += 0.5 * dt * fl2

    return m, l, pm, pl, step_stress


@dataclass
class OrbitMetrics:
    m_traj: np.ndarray
    l_traj: np.ndarray
    pm_traj: np.ndarray
    pl_traj: np.ndarray
    lifetime: float
    escaped: bool
    path_length: float
    stress: float
    efficiency: float
    score: float


def integrate_orbit(m0: float, l0: float,
                    pm0: float, pl0: float,
                    t_max: float = 80.0,
                    dt: float = 0.05,
                    escape_r2: float = 16.0,
                    sigma: float = 1.0,
                    lifetime_weight: float = 1.0,
                    efficiency_weight: float = 1.0) -> OrbitMetrics:
    """
    Integrate a single orbit and compute metrics:
      - lifetime (time before escape or t_max)
      - path_length in (m, l)
      - stress (integrated |F| dt)
      - efficiency = path_length / (stress + eps)
      - score = lifetime_factor * efficiency

    This is the core “environment” the learner is trying to exploit.
    """
    steps = int(t_max / dt)

    m = m0
    l = l0
    pm = pm0
    pl = pl0

    # Trajectories (for best-orbit visualization / instructions)
    m_hist = np.empty(steps + 1, dtype=np.float32)
    l_hist = np.empty(steps + 1, dtype=np.float32)
    pm_hist = np.empty(steps + 1, dtype=np.float32)
    pl_hist = np.empty(steps + 1, dtype=np.float32)

    m_hist[0] = m
    l_hist[0] = l
    pm_hist[0] = pm
    pl_hist[0] = pl

    stress = 0.0
    path_length = 0.0
    escaped = False
    t_alive = 0.0

    for k in range(1, steps + 1):
        m_prev, l_prev = m, l

        m, l, pm, pl, step_stress = step_prism(m, l, pm, pl, dt, sigma)

        m_hist[k] = m
        l_hist[k] = l
        pm_hist[k] = pm
        pl_hist[k] = pl

        stress += step_stress
        # Path length in configuration space
        path_length += np.sqrt((m - m_prev) ** 2 + (l - l_prev) ** 2)

        t_alive += dt

        if m * m + l * l > escape_r2:
            escaped = True
            break

    # Trim arrays to actual length
    steps_used = int(t_alive / dt)
    m_hist = m_hist[:steps_used + 1]
    l_hist = l_hist[:steps_used + 1]
    pm_hist = pm_hist[:steps_used + 1]
    pl_hist = pl_hist[:steps_used + 1]

    # Metrics
    lifetime = t_alive
    eps = 1e-8
    efficiency = path_length / (stress + eps)

    lifetime_factor = lifetime / t_max  # 0–1
    score = lifetime_weight * lifetime_factor + efficiency_weight * efficiency

    return OrbitMetrics(
        m_traj=m_hist,
        l_traj=l_hist,
        pm_traj=pm_hist,
        pl_traj=pl_hist,
        lifetime=lifetime,
        escaped=escaped,
        path_length=path_length,
        stress=stress,
        efficiency=efficiency,
        score=score
    )


# ============================================================
# 2. Evolutionary learner over initial conditions
# ============================================================

@dataclass
class Genome:
    m0: float
    l0: float
    pm0: float
    pl0: float
    metrics: OrbitMetrics = None


class FractalOrbitLearner:
    """
    Evolutionary search over the space of initial conditions.

    Genome = (m0, l0, pm0, pl0)

    Objective: maximize score = f(lifetime, path length, stress).
    """

    def __init__(self,
                 pop_size: int = 64,
                 elite_frac: float = 0.20,
                 mutation_scale_pos: float = 0.2,
                 mutation_scale_mom: float = 0.15,
                 t_max: float = 80.0,
                 dt: float = 0.05,
                 escape_r2: float = 16.0,
                 seed: int = 0):
        self.pop_size = pop_size
        self.elite_frac = elite_frac
        self.mutation_scale_pos = mutation_scale_pos
        self.mutation_scale_mom = mutation_scale_mom
        self.t_max = t_max
        self.dt = dt
        self.escape_r2 = escape_r2
        self.rng = np.random.default_rng(seed)

        self.best_genome: Genome | None = None

    # --- Helpers -------------------------------------------------

    def random_genome(self) -> Genome:
        """
        Sample an initial condition from a broad prior.
        Positions near origin, small momenta.
        """
        # Positions in a disk of radius ~2
        r = self.rng.uniform(0.0, 2.0)
        theta = self.rng.uniform(0.0, 2 * np.pi)
        m0 = r * np.cos(theta)
        l0 = r * np.sin(theta)

        # Small random momenta
        pm0 = self.rng.normal(0.0, 0.5)
        pl0 = self.rng.normal(0.0, 0.5)
        return Genome(m0, l0, pm0, pl0)

    def mutate(self, g: Genome) -> Genome:
        """
        Gaussian mutation with different scales for positions and momenta.
        """
        m0 = g.m0 + self.rng.normal(0.0, self.mutation_scale_pos)
        l0 = g.l0 + self.rng.normal(0.0, self.mutation_scale_pos)
        pm0 = g.pm0 + self.rng.normal(0.0, self.mutation_scale_mom)
        pl0 = g.pl0 + self.rng.normal(0.0, self.mutation_scale_mom)

        # Optional: keep positions in a reasonable band
        r = np.sqrt(m0 * m0 + l0 * l0)
        if r > 3.0:
            m0 *= 3.0 / (r + 1e-8)
            l0 *= 3.0 / (r + 1e-8)

        return Genome(m0, l0, pm0, pl0)

    def evaluate_genome(self, g: Genome) -> None:
        """
        Attach OrbitMetrics to genome.
        """
        metrics = integrate_orbit(
            g.m0, g.l0, g.pm0, g.pl0,
            t_max=self.t_max,
            dt=self.dt,
            escape_r2=self.escape_r2
        )
        g.metrics = metrics

    # --- Main loop -----------------------------------------------

    def run(self, generations: int = 40, verbose: bool = True) -> Genome:
        """
        Run the evolutionary search and return the best genome found.
        """
        # Initial population
        pop: List[Genome] = [self.random_genome() for _ in range(self.pop_size)]

        for gen in range(generations):
            # Evaluate all
            for g in pop:
                if g.metrics is None:
                    self.evaluate_genome(g)

            # Sort by score (descending)
            pop.sort(key=lambda x: x.metrics.score, reverse=True)

            best = pop[0]
            if self.best_genome is None or best.metrics.score > self.best_genome.metrics.score:
                self.best_genome = best

            if verbose:
                mean_score = np.mean([g.metrics.score for g in pop])
                print(f"[Gen {gen:02d}] "
                      f"Best score = {best.metrics.score:.4f} "
                      f"(life {best.metrics.lifetime:.1f}, "
                      f"eff {best.metrics.efficiency:.4f}), "
                      f"mean = {mean_score:.4f}")

            # Elitism
            n_elite = max(1, int(self.elite_frac * self.pop_size))
            elites = pop[:n_elite]

            # Create new population
            new_pop: List[Genome] = []
            # Keep elites (copy to avoid overwriting metrics later)
            for e in elites:
                new_pop.append(Genome(e.m0, e.l0, e.pm0, e.pl0, metrics=e.metrics))

            # Fill the rest by mutated elites
            while len(new_pop) < self.pop_size:
                parent = self.rng.choice(elites)
                child = self.mutate(parent)
                new_pop.append(child)

            # Reset metrics for those that haven't been evaluated
            for g in new_pop:
                if g.metrics is not None and g not in elites:
                    g.metrics = None

            pop = new_pop

        if verbose and self.best_genome is not None:
            m = self.best_genome.metrics
            print("\n[FractalOrbitLearner] Best overall:")
            print(f"  score      = {m.score:.4f}")
            print(f"  lifetime   = {m.lifetime:.2f} (t_max={self.t_max})")
            print(f"  escaped    = {m.escaped}")
            print(f"  path_len   = {m.path_length:.3f}")
            print(f"  stress     = {m.stress:.3f}")
            print(f"  efficiency = {m.efficiency:.4f}")
            print(f"  initial    = (m0={self.best_genome.m0:.3f}, "
                  f"l0={self.best_genome.l0:.3f}, "
                  f"pm0={self.best_genome.pm0:.3f}, "
                  f"pl0={self.best_genome.pl0:.3f})")

        return self.best_genome


# ============================================================
# 3. Turning an orbit into “instructions for the player”
# ============================================================

def orbit_to_player_instructions(metrics: OrbitMetrics,
                                 n_waypoints: int = 32) -> List[Dict[str, Any]]:
    """
    Compress an orbit into a list of waypoints in polar coordinates.

    Each waypoint:
      {
        "t": time,
        "r": radius,
        "theta": angle (radians),
        "m": m,
        "l": l
      }

    This is the thing you can hand to:
      - FractalHypernet.generate_weights(m_list, lam_list)
      - A TTRPG spell / orbit description
      - Any “player” that wants an orbital script.
    """
    m_traj = metrics.m_traj
    l_traj = metrics.l_traj
    total_steps = len(m_traj)
    if total_steps <= 1:
        return []

    idxs = np.linspace(0, total_steps - 1, n_waypoints, dtype=int)
    dt = metrics.lifetime / max(1, total_steps - 1)

    waypoints = []
    for k, idx in enumerate(idxs):
        m = float(m_traj[idx])
        l = float(l_traj[idx])
        r = float(np.sqrt(m * m + l * l))
        theta = float(np.arctan2(l, m))
        t = k * (metrics.lifetime / max(1, n_waypoints - 1))

        waypoints.append({
            "t": t,
            "r": r,
            "theta": theta,
            "m": m,
            "l": l,
        })
    return waypoints


# ============================================================
# 4. Visualization helpers
# ============================================================

def plot_best_orbit(metrics: OrbitMetrics,
                    title: str = "Best Fractal Orbit") -> None:
    """
    Quick phase-space plot of the best orbit.
    """
    m = metrics.m_traj
    l = metrics.l_traj

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    # Phase portrait in (m, l)
    ax[0].plot(m, l, lw=0.8)
    ax[0].set_xlabel("m")
    ax[0].set_ylabel("λ")
    ax[0].set_title(title)
    ax[0].axis("equal")
    ax[0].grid(True, alpha=0.3)

    # Radius vs time
    t = np.linspace(0.0, metrics.lifetime, len(m))
    r = np.sqrt(m * m + l * l)
    ax[1].plot(t, r)
    ax[1].set_xlabel("time")
    ax[1].set_ylabel("radius r")
    ax[1].set_title("Radial profile")
    ax[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# ============================================================
# 5. Example main
# ============================================================

if __name__ == "__main__":
    learner = FractalOrbitLearner(
        pop_size=64,
        elite_frac=0.25,
        mutation_scale_pos=0.15,
        mutation_scale_mom=0.10,
        t_max=80.0,
        dt=0.05,
        escape_r2=16.0,
        seed=42,
    )

    best = learner.run(generations=40, verbose=True)
    best_metrics = best.metrics

    # Plot orbit
    plot_best_orbit(best_metrics)

    # Extract player instructions
    instructions = orbit_to_player_instructions(best_metrics, n_waypoints=24)

    print("\n[Player Instructions]")
    for wp in instructions[:8]:  # print a few
        print(f" t={wp['t']:6.2f}  r={wp['r']:5.3f}  θ={wp['theta']:6.3f}  "
              f"(m={wp['m']:5.3f}, l={wp['l']:5.3f})")

    # If you want to feed these directly into your FractalHypernet:
    # m_list = [wp['m'] for wp in instructions]
    # lam_list = [wp['l'] for wp in instructions]
    # hyper = FractalHypernet(output_dim=56)
    # weights, kP_scores, colors = hyper.generate_weights(m_list, lam_list)
