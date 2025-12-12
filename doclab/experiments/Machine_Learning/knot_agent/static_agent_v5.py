import gymnasium as gym
import numpy as np


# ---------------------------------------------------------------------
# Linear static policy: one vector per agent, no learning, just evolution
# ---------------------------------------------------------------------

class LinearStaticReader:
    """
    Static linear policy:
      - For Discrete actions (CartPole): logits = W x + b, argmax
      - For Box(1,) actions (Pendulum): u = tanh(w·x + b) * max_action
    The entire policy is encoded in a single vector `static_vec`.
    """

    def __init__(self, obs_dim, action_space):
        self.obs_dim = obs_dim
        self.action_space = action_space

        if isinstance(action_space, gym.spaces.Discrete):
            self.mode = "discrete"
            self.n_actions = action_space.n
            # one row per action + bias per action
            self.dim = self.n_actions * (self.obs_dim + 1)
            self.max_action = None
        else:
            # assume 1D Box action (Pendulum-style)
            assert isinstance(action_space, gym.spaces.Box)
            assert action_space.shape == (1,)
            self.mode = "continuous"
            self.n_actions = 1
            self.dim = self.obs_dim + 1
            self.max_action = float(action_space.high[0])

    def act(self, static_vec, obs):
        """
        Map (static_vec, obs) -> action compatible with env.action_space.
        No context managers, no side effects, just pure math.
        """
        obs = np.asarray(obs, dtype=np.float32)

        if self.mode == "discrete":
            # W: (n_actions, obs_dim), b: (n_actions,)
            W_flat = static_vec[: self.n_actions * self.obs_dim]
            b = static_vec[self.n_actions * self.obs_dim:]
            W = W_flat.reshape(self.n_actions, self.obs_dim)
            logits = W @ obs + b
            a = int(np.argmax(logits))
            return a

        else:  # continuous
            w = static_vec[: self.obs_dim]
            b = static_vec[self.obs_dim]
            u = float(np.dot(w, obs) + b)
            u = np.tanh(u) * self.max_action
            return np.array([u], dtype=np.float32)


# ---------------------------------------------------------------------
# CartPole evaluation (same flavor as v3)
# ---------------------------------------------------------------------

def cartpole_safety_hook(obs_traj):
    """
    Simple stability proxy: penalize large pole angles and positions.
    obs = [x, x_dot, theta, theta_dot]
    """
    obs_arr = np.asarray(obs_traj, dtype=np.float32)  # (T, 4)
    x = obs_arr[:, 0]
    theta = obs_arr[:, 2]
    # Penalize RMS deviation
    pos_penalty = np.mean(x ** 2)
    ang_penalty = np.mean(theta ** 2)
    # Negative penalty, so more stable = less negative
    return -0.5 * pos_penalty - 2.0 * ang_penalty


def evaluate_cartpole_macro(env, reader, static_vec, n_episodes=5, gamma=1.0):
    """Evaluate one static vector on CartPole with a macro fitness."""
    total_return = 0.0
    traj_stability = 0.0
    returns = []

    for _ in range(n_episodes):
        obs, _info = env.reset()
        done = False
        ep_ret = 0.0
        obs_traj = []

        while not done:
            obs_traj.append(obs)
            action = reader.act(static_vec, obs)
            obs, reward, terminated, truncated, _info = env.step(action)
            done = terminated or truncated
            ep_ret += reward

        total_return += ep_ret
        returns.append(ep_ret)
        traj_stability += cartpole_safety_hook(obs_traj)

    mean_ret = total_return / n_episodes
    mean_stab = traj_stability / n_episodes
    ret_std = np.std(returns) if len(returns) > 1 else 0.0

    # Fitness: reward + small stability bonus - small variance penalty
    fitness = mean_ret + 0.1 * mean_stab - 0.01 * ret_std
    return fitness, mean_ret, mean_stab, -ret_std


def run_static_evolution_cartpole(
    pop_size=64,
    generations=25,
    sigma_init=0.5,
    elite_frac=0.2,
):
    env = gym.make("CartPole-v1")
    obs_dim = env.observation_space.shape[0]
    reader = LinearStaticReader(obs_dim, env.action_space)
    dim = reader.dim

    pop = np.random.randn(pop_size, dim) * sigma_init
    hall_best = None
    hall_fitness = -np.inf

    elite_count = max(1, int(pop_size * elite_frac))

    for gen in range(1, generations + 1):
        fits = []
        rets = []
        stabs = []
        margins = []

        for i in range(pop_size):
            fit, r, s, m = evaluate_cartpole_macro(env, reader, pop[i])
            fits.append(fit)
            rets.append(r)
            stabs.append(s)
            margins.append(m)

            # Hall-of-fame update
            if fit > hall_fitness or hall_best is None:
                hall_fitness = fit
                hall_best = pop[i].copy()

        fits = np.asarray(fits)
        rets = np.asarray(rets)
        gen_best_ret = float(np.max(rets))
        gen_mean_ret = float(np.mean(rets))

        print(
            f"[Gen {gen:4d}] GenBestRet={gen_best_ret:6.1f}  "
            f"GenMeanRet={gen_mean_ret:4.1f}  HallFit={hall_fitness:7.2f}"
        )

        # Select elites
        elite_idx = np.argsort(fits)[-elite_count:]
        elites = pop[elite_idx]

        # Re-sample population around elites
        new_pop = []
        for _ in range(pop_size):
            parent = elites[np.random.randint(elite_count)]
            child = parent + np.random.randn(dim) * sigma_init
            new_pop.append(child)
        pop = np.stack(new_pop, axis=0)

    # Final eval with hall-of-fame
    fit, r, s, m = evaluate_cartpole_macro(env, reader, hall_best, n_episodes=10)
    print("\n=== Final Hall-of-Fame Evaluation (CartPole) ===")
    print(f"Hall mean return: {r:.1f} (fitness {fit:.1f})")
    env.close()
    return hall_best


# ---------------------------------------------------------------------
# Pendulum evaluation
# ---------------------------------------------------------------------

def pendulum_safety_hook(obs_traj):
    """
    Stability term for Pendulum:
      obs = [cos(theta), sin(theta), theta_dot]
    We penalize large |theta| and |theta_dot|.
    """
    obs_arr = np.asarray(obs_traj, dtype=np.float32)  # (T, 3)
    cos_th = obs_arr[:, 0]
    sin_th = obs_arr[:, 1]
    thdot = obs_arr[:, 2]

    theta = np.arctan2(sin_th, cos_th)
    ang_penalty = np.mean(theta ** 2)
    vel_penalty = np.mean(thdot ** 2)

    # Negative penalty => more stable trajectories are less negative
    return -0.5 * ang_penalty - 0.05 * vel_penalty


def evaluate_pendulum_macro(env, reader, static_vec, n_episodes=5, max_steps=200):
    """
    Evaluate a static vector on Pendulum-v1.
    Gymnasium Pendulum returns *negative* rewards, so "less negative" is better.
    """
    total_return = 0.0
    traj_stability = 0.0
    returns = []

    for _ in range(n_episodes):
        obs, _info = env.reset()
        ep_ret = 0.0
        obs_traj = []

        for t in range(max_steps):
            obs_traj.append(obs)
            action = reader.act(static_vec, obs)  # np.array([u])
            obs, reward, terminated, truncated, _info = env.step(action)
            ep_ret += reward
            done = terminated or truncated
            if done:
                break

        total_return += ep_ret
        returns.append(ep_ret)
        traj_stability += pendulum_safety_hook(obs_traj)

    mean_ret = total_return / n_episodes
    mean_stab = traj_stability / n_episodes
    ret_std = np.std(returns) if len(returns) > 1 else 0.0

    # Fitness: push return toward 0 (less negative) and add stability bonus
    fitness = mean_ret + 0.1 * mean_stab - 0.01 * ret_std
    return fitness, mean_ret, mean_stab, -ret_std


def run_static_evolution_pendulum(
    pop_size=64,
    generations=25,
    sigma_init=0.5,
    elite_frac=0.2,
):
    env = gym.make("Pendulum-v1")
    obs_dim = env.observation_space.shape[0]
    reader = LinearStaticReader(obs_dim, env.action_space)
    dim = reader.dim

    pop = np.random.randn(pop_size, dim) * sigma_init
    hall_best = None
    hall_fitness = -np.inf

    elite_count = max(1, int(pop_size * elite_frac))

    for gen in range(1, generations + 1):
        fits = []
        rets = []
        stabs = []
        margins = []

        for i in range(pop_size):
            fit, r, s, m = evaluate_pendulum_macro(env, reader, pop[i])
            fits.append(fit)
            rets.append(r)
            stabs.append(s)
            margins.append(m)

            if fit > hall_fitness or hall_best is None:
                hall_fitness = fit
                hall_best = pop[i].copy()

        fits = np.asarray(fits)
        rets = np.asarray(rets)
        gen_best_ret = float(np.max(rets))
        gen_mean_ret = float(np.mean(rets))

        print(
            f"[Gen {gen:4d}] GenBestRet={gen_best_ret:7.1f}  "
            f"GenMeanRet={gen_mean_ret:7.1f}  HallFit={hall_fitness:8.2f}"
        )

        elite_idx = np.argsort(fits)[-elite_count:]
        elites = pop[elite_idx]

        new_pop = []
        for _ in range(pop_size):
            parent = elites[np.random.randint(elite_count)]
            child = parent + np.random.randn(dim) * sigma_init
            new_pop.append(child)
        pop = np.stack(new_pop, axis=0)

    fit, r, s, m = evaluate_pendulum_macro(env, reader, hall_best, n_episodes=10)
    print("\n=== Final Hall-of-Fame Evaluation (Pendulum) ===")
    print(f"Hall mean return: {r:.1f} (fitness {fit:.1f})")
    env.close()
    return hall_best


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Static Agent v4: CartPole ===")
    best_cartpole = run_static_evolution_cartpole()

    print("\n\n=== Static Agent v4: Pendulum ===")
    best_pendulum = run_static_evolution_pendulum()
