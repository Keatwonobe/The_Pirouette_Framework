import gymnasium as gym
import numpy as np

# --- Static policy representation -----------------------------------------

class StaticReader:
    """
    Maps a low-D static vector -> action logits for CartPole (0 or 1).
    You already have something like this; this is a minimal stand-in.
    """
    def __init__(self, dim, n_actions=2):
        self.dim = dim
        self.n_actions = n_actions

    def act(self, static_vec, obs):
        # Example: dot product of obs with reshaped static → logits
        # static_vec: shape [dim]
        # obs: shape [4]
        # You can get fancier; this is just to illustrate the hook.
        w = static_vec.reshape(self.n_actions, -1)  # [2, dim/2] in a simple case
        o = obs[:w.shape[1]]                       # slice state to match
        logits = w @ o                             # [2]
        probs = np.exp(logits - logits.max())
        probs /= probs.sum()
        return np.random.choice(self.n_actions, p=probs)


# --- Safety / counterfactual hook -----------------------------------------

def safety_hook(obs, terminated, truncated, x_thresh, theta_thresh):
    x, x_dot, theta, theta_dot = obs

    margin_x = max(0.0, 1.0 - abs(x) / x_thresh)
    margin_theta = max(0.0, 1.0 - abs(theta) / theta_thresh)
    stability = 0.5 * (margin_x + margin_theta)

    failure_dir = 0.0
    if terminated or truncated:
        failure_dir = np.sign(theta)

    return stability, failure_dir


# --- Evaluate a single static macro with hooks ----------------------------

def evaluate_macro(env, reader, static_vec, n_episodes=5,
                   lambda_stab=5.0, lambda_margin=10.0,
                   last_k_margin=10):
    """
    Returns:
      total_fitness, mean_return, mean_stability, mean_margin_last_k
    """
    returns = []
    stab_scores = []
    margins_last = []

    x_thresh = env.unwrapped.x_threshold
    theta_thresh = env.unwrapped.theta_threshold_radians

    for _ in range(n_episodes):
        obs, _ = env.reset()
        done = False
        episode_return = 0.0
        stability_traj = []

        while not done:
            action = reader.act(static_vec, obs)
            obs_next, reward, terminated, truncated, _info = env.step(action)

            stability, failure_dir = safety_hook(
                obs_next, terminated, truncated, x_thresh, theta_thresh
            )
            stability_traj.append(stability)

            episode_return += reward
            obs = obs_next
            done = terminated or truncated

        returns.append(episode_return)
        stab_scores.append(np.mean(stability_traj))

        # Margin near end = average stability over last_k steps
        if len(stability_traj) >= last_k_margin:
            margins_last.append(
                np.mean(stability_traj[-last_k_margin:])
            )
        else:
            margins_last.append(np.mean(stability_traj))

    mean_return = float(np.mean(returns))
    mean_stab = float(np.mean(stab_scores))
    mean_margin_last = float(np.mean(margins_last))

    # Composite fitness (“what did you do” + “what didn’t happen”)
    fitness = (
        mean_return +
        lambda_stab * mean_stab +
        lambda_margin * mean_margin_last
    )

    return fitness, mean_return, mean_stab, mean_margin_last

def eval_return_only(env, reader, static_vec, n_episodes=20):
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
    return np.mean(returns)


# --- Population loop skeleton (evolutionary static) -----------------------

def run_static_evolution(
    env_id="CartPole-v1",
    pop_size=64,
    dim=8,
    generations=25,
    sigma_init=0.5,
    elite_frac=0.2,
    n_eval=5
):
    env = gym.make(env_id)
    reader = StaticReader(dim=dim, n_actions=2)

    # Initialize population: Gaussian static vectors
    pop = np.random.randn(pop_size, dim) * sigma_init
    hall_best = None
    hall_fitness = -np.inf

    for gen in range(1, generations + 1):
        fitnesses = []
        returns = []
        stabs = []
        margins = []

        for i in range(pop_size):
            fit, r, s, m = evaluate_macro(
                env, reader, pop[i],
                n_episodes=n_eval,
                lambda_stab=5.0,
                lambda_margin=10.0,
                last_k_margin=10
            )
            fitnesses.append(fit)
            returns.append(r)
            stabs.append(s)
            margins.append(m)

        fitnesses = np.array(fitnesses)
        returns = np.array(returns)

        # Track hall-of-fame
        gen_best_idx = int(np.argmax(fitnesses))
        gen_best_fit = fitnesses[gen_best_idx]
        gen_best_ret = returns[gen_best_idx]

        if gen_best_fit > hall_fitness:
            hall_fitness = gen_best_fit
            hall_best = pop[gen_best_idx].copy()

        print(f"[Gen {gen:4d}] "
              f"GenBestRet={gen_best_ret:5.1f}  "
              f"GenMeanRet={returns.mean():4.1f}  "
              f"HallFit={hall_fitness:7.2f}")

        # Selection: keep elites
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

    # Final hall-of-fame eval
    fit, r, s, m = evaluate_macro(env, reader, hall_best, n_episodes=10)
    print("\n=== Final Hall-of-Fame Evaluation ===")
    print(f"Hall mean return: {r:.1f} (fitness {fit:.1f})")
    true_mean = eval_return_only(env, reader, hall_best, n_episodes=50)
    print(f"Hall mean *true* return (no bonuses): {true_mean:.1f}")

    env.close()
    return hall_best


if __name__ == "__main__":
    run_static_evolution()