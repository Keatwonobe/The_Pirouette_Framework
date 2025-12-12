import gymnasium as gym
import numpy as np

# --- Static policy for Pendulum (continuous torque) ------------------------

class StaticPendulumReader:
    """
    Maps a low-D static vector -> continuous torque for Pendulum-v1.
    Policy is a simple linear map + tanh squashing into [-max_torque, max_torque].
    """
    def __init__(self, dim, obs_dim, action_space):
        self.dim = dim
        self.obs_dim = obs_dim
        self.max_torque = float(action_space.high[0])

    def act(self, static_vec, obs):
        # Use first obs_dim weights + optional bias; ignore any extra dims for now.
        w = static_vec[:self.obs_dim]
        b = static_vec[self.obs_dim] if self.dim > self.obs_dim else 0.0

        o = obs[:self.obs_dim]
        z = np.dot(w, o) + b          # scalar
        u = np.tanh(z)                # in [-1, 1]
        torque = u * self.max_torque  # scale to env range

        # Gymnasium Pendulum expects shape (1,) float array
        return np.array([torque], dtype=np.float32)


# --- Safety / static hook for Pendulum ------------------------------------

def pendulum_safety_hook(obs, action, max_speed, max_torque):
    """
    obs = [cos(theta), sin(theta), theta_dot]
    action = np.array([torque])
    We reward what *didn't* happen: big angle, huge speed, and maxed-out torque.
    Returns a stability score in [0, 1]-ish.
    """
    cos_th, sin_th, thdot = obs
    theta = np.arctan2(sin_th, cos_th)

    # Angle margin: 1 when upright, 0 when fully inverted (|theta| ~ pi)
    angle_margin = 1.0 - min(1.0, abs(theta) / np.pi)

    # Speed margin: 1 when still, 0 when at max_speed
    speed_margin = 1.0 - min(1.0, abs(thdot) / (max_speed + 1e-8))

    # Torque margin: 1 when gentle, 0 when saturating torque
    torque = float(action[0])
    torque_margin = 1.0 - min(1.0, abs(torque) / (max_torque + 1e-8))

    # Simple average: "static" = didn't swing far, didn't spin fast, didn't yank hard
    stability = (angle_margin + speed_margin + torque_margin) / 3.0
    return stability


# --- Evaluate a single static vector on Pendulum --------------------------

def evaluate_pendulum_macro(
    env,
    reader,
    static_vec,
    n_episodes=5,
    lambda_stab=5.0,
    lambda_margin=10.0,
    last_k_margin=10
):
    """
    Returns:
      fitness, mean_return, mean_stability, mean_margin_last_k

    mean_return is the *true* environment return (no bonuses).
    fitness adds bonuses for stability and for being stable near the end.
    """
    returns = []
    stab_scores = []
    margins_last = []

    max_speed = env.unwrapped.max_speed
    max_torque = env.unwrapped.max_torque

    for _ in range(n_episodes):
        obs, _ = env.reset()
        done = False
        episode_return = 0.0
        stability_traj = []

        while not done:
            action = reader.act(static_vec, obs)
            obs_next, reward, terminated, truncated, _info = env.step(action)

            stability = pendulum_safety_hook(
                obs_next, action, max_speed, max_torque
            )
            stability_traj.append(stability)

            episode_return += reward
            obs = obs_next
            done = terminated or truncated

        returns.append(episode_return)
        stab_scores.append(float(np.mean(stability_traj)))

        # Margin near end: average stability over last_k steps
        if len(stability_traj) >= last_k_margin:
            margins_last.append(
                float(np.mean(stability_traj[-last_k_margin:]))
            )
        else:
            margins_last.append(float(np.mean(stability_traj)))

    mean_return = float(np.mean(returns))
    mean_stab = float(np.mean(stab_scores))
    mean_margin_last = float(np.mean(margins_last))

    # Composite fitness = "what happened" + "what didn't happen"
    fitness = (
        mean_return +
        lambda_stab * mean_stab +
        lambda_margin * mean_margin_last
    )

    return fitness, mean_return, mean_stab, mean_margin_last


# --- Evolutionary static loop for Pendulum --------------------------------

def run_static_evolution_pendulum(
    env_id="Pendulum-v1",
    pop_size=64,
    dim=8,
    generations=50,
    sigma_init=0.5,
    elite_frac=0.2,
    n_eval=5
):
    env = gym.make(env_id)

    # Pendulum obs is 3-D: [cos(theta), sin(theta), theta_dot]
    obs_dim = env.observation_space.shape[0]
    reader = StaticPendulumReader(dim=dim,
                                  obs_dim=obs_dim,
                                  action_space=env.action_space)

    # Initialize population: Gaussian static vectors
    pop = np.random.randn(pop_size, dim) * sigma_init
    hall_best = None
    hall_fitness = -np.inf
    hall_true_return = -np.inf

    for gen in range(1, generations + 1):
        fitnesses = []
        returns = []
        stabs = []
        margins = []

        for i in range(pop_size):
            fit, r, s, m = evaluate_pendulum_macro(
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

        fitnesses = np.array(fitnesses, dtype=np.float32)
        returns = np.array(returns, dtype=np.float32)

        # Track hall-of-fame based on fitness
        gen_best_idx = int(np.argmax(fitnesses))
        gen_best_fit = float(fitnesses[gen_best_idx])
        gen_best_ret = float(returns[gen_best_idx])

        if gen_best_fit > hall_fitness:
            hall_fitness = gen_best_fit
            hall_true_return = gen_best_ret
            hall_best = pop[gen_best_idx].copy()

        print(f"[Gen {gen:4d}] "
              f"GenBestRet={gen_best_ret:6.1f}  "
              f"GenMeanRet={returns.mean():5.1f}  "
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

    # Final hall-of-fame eval with more episodes
    fit, r, s, m = evaluate_pendulum_macro(env, reader, hall_best, n_episodes=10)
    print("\n=== Final Hall-of-Fame Evaluation (Pendulum) ===")
    print(f"Hall mean return (true env): {r:.1f}")
    print(f"Hall fitness (with static bonuses): {fit:.1f}")
    env.close()
    return hall_best


if __name__ == "__main__":
    run_static_evolution_pendulum()
