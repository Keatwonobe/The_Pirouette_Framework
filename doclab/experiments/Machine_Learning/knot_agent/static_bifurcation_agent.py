import gymnasium as gym
import numpy as np


# ---------------------------------------------------------------------------
# Static Reader: maps a low-D static vector to action probabilities
# ---------------------------------------------------------------------------

class StaticReader:
    """
    Minimal static policy for CartPole.

    - static_vec: R^D
    - We reshape into [n_actions, D_per_action] and take a dot with the obs.

    Assumes D is divisible by n_actions.
    """

    def __init__(self, dim: int, n_actions: int = 2):
        assert dim % n_actions == 0, "dim must be divisible by n_actions"
        self.dim = dim
        self.n_actions = n_actions
        self.d_per_action = dim // n_actions

    def act(self, static_vec: np.ndarray, obs: np.ndarray) -> int:
        """
        Given the current observation, produce an action.

        We simply do: logits = W @ o_slice, then sample from softmax.
        """
        # reshape static into a tiny "weight matrix"
        W = static_vec.reshape(self.n_actions, self.d_per_action)

        # slice obs to match; CartPole has 4 dims so we just truncate or pad
        o = obs[: self.d_per_action]
        if o.shape[0] < self.d_per_action:
            o = np.pad(o, (0, self.d_per_action - o.shape[0]))

        logits = W @ o  # shape [n_actions]

        # softmax
        logits = logits - np.max(logits)
        probs = np.exp(logits)
        probs /= np.sum(probs)

        # sample action
        return int(np.random.choice(self.n_actions, p=probs))


# ---------------------------------------------------------------------------
# Safety / "what didn’t happen" hook
# ---------------------------------------------------------------------------

def safety_hook(obs, terminated, truncated, x_thresh, theta_thresh):
    """
    Returns:
      stability in [0, 1] ~ how far from failure we are on this step.
      failure_dir in {-1, 0, +1} ~ direction of pole at failure (for future use).
    """
    x, x_dot, theta, theta_dot = obs

    # margins: 1.0 when centered and upright, 0.0 at the threshold
    margin_x = max(0.0, 1.0 - abs(x) / x_thresh)
    margin_theta = max(0.0, 1.0 - abs(theta) / theta_thresh)

    stability = 0.5 * (margin_x + margin_theta)

    failure_dir = 0.0
    if terminated or truncated:
        failure_dir = np.sign(theta)

    return stability, failure_dir


# ---------------------------------------------------------------------------
# Evaluation with composite fitness (return + stability + late margin)
# ---------------------------------------------------------------------------

def evaluate_static(
    env,
    reader: StaticReader,
    static_vec: np.ndarray,
    n_episodes: int = 5,
    lambda_stab: float = 5.0,
    lambda_margin: float = 10.0,
    last_k_margin: int = 10,
):
    """
    Evaluate a single static vector by running multiple episodes.

    Returns:
      fitness, mean_return, mean_stability, mean_margin_last_k
    """
    returns = []
    stab_scores = []
    margins_last = []

    x_thresh = env.unwrapped.x_threshold
    theta_thresh = env.unwrapped.theta_threshold_radians

    for _ in range(n_episodes):
        obs, _ = env.reset()
        done = False
        ep_ret = 0.0
        stability_traj = []

        while not done:
            action = reader.act(static_vec, obs)
            obs_next, reward, terminated, truncated, _info = env.step(action)

            stability, failure_dir = safety_hook(
                obs_next, terminated, truncated, x_thresh, theta_thresh
            )
            stability_traj.append(stability)

            ep_ret += reward
            obs = obs_next
            done = terminated or truncated

        returns.append(ep_ret)
        stab_scores.append(float(np.mean(stability_traj)))

        # stability over the last_k steps = how "clean" the landing was
        if len(stability_traj) >= last_k_margin:
            margins_last.append(
                float(np.mean(stability_traj[-last_k_margin:]))
            )
        else:
            margins_last.append(float(np.mean(stability_traj)))

    mean_return = float(np.mean(returns))
    mean_stab = float(np.mean(stab_scores))
    mean_margin_last = float(np.mean(margins_last))

    # Composite fitness: "what we did" + "what didn't happen"
    fitness = (
        mean_return
        + lambda_stab * mean_stab
        + lambda_margin * mean_margin_last
    )

    return fitness, mean_return, mean_stab, mean_margin_last


def eval_return_only(env, reader: StaticReader, static_vec: np.ndarray,
                     n_episodes: int = 20) -> float:
    """
    For final evaluation: pure average return, no safety bonuses.
    """
    returns = []
    for _ in range(n_episodes):
        obs, _ = env.reset()
        done = False
        ep_ret = 0.0
        while not done:
            action = reader.act(static_vec, obs)
            obs, r, terminated, truncated, _ = env.step(action)
            ep_ret += r
            done = terminated or truncated
        returns.append(ep_ret)
    return float(np.mean(returns))


# ---------------------------------------------------------------------------
# Evolutionary loop: static → coherence via pressure
# ---------------------------------------------------------------------------

def run_static_bifurcation(
    env_id: str = "CartPole-v1",
    pop_size: int = 64,
    dim: int = 8,
    generations: int = 25,
    sigma_init: float = 0.5,
    elite_frac: float = 0.2,
    n_eval: int = 5,
    seed: int | None = None,
):
    """
    Ultralight ES loop:

    - Population of static vectors in R^dim
    - Composite fitness (return + stability)
    - Elitist selection + Gaussian mutation
    """
    if seed is not None:
        np.random.seed(seed)

    env = gym.make(env_id)
    reader = StaticReader(dim=dim, n_actions=2)

    # Initialize population with Gaussian noise
    pop = np.random.randn(pop_size, dim) * sigma_init

    hall_best = None
    hall_fitness = -np.inf

    for gen in range(1, generations + 1):
        fitnesses = np.zeros(pop_size, dtype=np.float32)
        returns = np.zeros(pop_size, dtype=np.float32)
        stabs = np.zeros(pop_size, dtype=np.float32)
        margins = np.zeros(pop_size, dtype=np.float32)

        # Evaluate each static vector
        for i in range(pop_size):
            fit, r, s, m = evaluate_static(
                env,
                reader,
                pop[i],
                n_episodes=n_eval,
                lambda_stab=5.0,
                lambda_margin=10.0,
                last_k_margin=10,
            )
            fitnesses[i] = fit
            returns[i] = r
            stabs[i] = s
            margins[i] = m

        # Track hall-of-fame (global best under composite fitness)
        gen_best_idx = int(np.argmax(fitnesses))
        gen_best_fit = float(fitnesses[gen_best_idx])
        gen_best_ret = float(returns[gen_best_idx])

        if gen_best_fit > hall_fitness or hall_best is None:
            hall_fitness = gen_best_fit
            hall_best = pop[gen_best_idx].copy()

        print(
            f"[Gen {gen:3d}] "
            f"GenBestRet={gen_best_ret:6.1f}  "
            f"GenMeanRet={returns.mean():6.1f}  "
            f"HallFit={hall_fitness:8.2f}"
        )

        # Selection: keep top elites
        elite_count = max(1, int(elite_frac * pop_size))
        elite_idx = np.argsort(fitnesses)[-elite_count:]
        elites = pop[elite_idx]

        # Reproduce with mutation around elites
        new_pop = []
        for _ in range(pop_size):
            parent = elites[np.random.randint(elite_count)]
            child = parent + np.random.randn(dim) * sigma_init
            new_pop.append(child)
        pop = np.stack(new_pop, axis=0)

    # Final hall-of-fame evaluation
    if hall_best is not None:
        fit, r, s, m = evaluate_static(env, reader, hall_best, n_episodes=10)
        print("\n=== Final Hall-of-Fame Evaluation ===")
        print(f"Hall mean composite fitness: {fit:.1f}")
        print(f"Hall mean return (with bonuses stepwise): {r:.1f}")
        true_mean = eval_return_only(env, reader, hall_best, n_episodes=50)
        print(f"Hall mean *true* return (no bonuses): {true_mean:.1f}")
    else:
        print("No hall-of-fame vector recorded; something went wrong.")

    env.close()
    return hall_best


if __name__ == "__main__":
    run_static_bifurcation()
