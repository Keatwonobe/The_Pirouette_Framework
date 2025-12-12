import gymnasium as gym
import numpy as np

# ---------------------------------------------------------------------
# Linear static policy: Paranoid Edition
# ---------------------------------------------------------------------

class LinearStaticReader:
    def __init__(self, obs_dim, action_space):
        self.obs_dim = obs_dim
        self.action_space = action_space

        if isinstance(action_space, gym.spaces.Discrete):
            self.mode = "discrete"
            self.n_actions = action_space.n
            # W: [n_actions, obs_dim], b: [n_actions]
            self.dim = self.n_actions * (self.obs_dim + 1)
            self.max_action = None
        else:
            # Box(1,) for Pendulum
            assert isinstance(action_space, gym.spaces.Box)
            self.mode = "continuous"
            self.n_actions = 1
            self.dim = self.obs_dim + 1
            self.max_action = float(action_space.high[0])

    def act(self, static_vec, obs):
        """
        Paranoid act method. 
        Sanitizes inputs to prevent NaN propagation into the physics engine.
        """
        # 1. Sanitize Observation
        # Replace NaN with 0.0, Inf with large finite numbers
        obs = np.nan_to_num(np.asarray(obs, dtype=np.float32), nan=0.0, posinf=1e6, neginf=-1e6)

        # 2. Sanitize Weights (just in case mutation broke them)
        static_vec = np.nan_to_num(static_vec, nan=0.0, posinf=10.0, neginf=-10.0)

        if self.mode == "discrete":
            # Slicing
            limit = self.n_actions * self.obs_dim
            W_flat = static_vec[:limit]
            b = static_vec[limit:]
            
            # Reshape
            W = W_flat.reshape(self.n_actions, self.obs_dim)
            
            # Math
            logits = W @ obs + b
            
            # Sanitize Logits before argmax
            if not np.isfinite(logits).all():
                return 0 # Default safe action
            
            return int(np.argmax(logits))

        else:  # continuous
            w = static_vec[: self.obs_dim]
            b = static_vec[self.obs_dim]
            
            val = np.dot(w, obs) + b
            
            # Sanitize pre-activation
            if np.isnan(val) or np.isinf(val):
                val = 0.0
                
            u = float(val)
            u = np.tanh(u) * self.max_action
            
            # Final output sanity check
            if np.isnan(u) or np.isinf(u):
                u = 0.0
                
            return np.array([u], dtype=np.float32)


# ---------------------------------------------------------------------
# CartPole evaluation
# ---------------------------------------------------------------------

def evaluate_cartpole_macro(env, reader, static_vec, n_episodes=5):
    total_return = 0.0
    total_stab = 0.0
    returns = []

    for _ in range(n_episodes):
        # Safe Reset
        try:
            obs, _ = env.reset()
        except:
            return -1000.0, 0.0, 0.0, 0.0

        ep_ret = 0.0
        obs_traj = []
        done = False

        while not done:
            obs_traj.append(obs)
            
            # Agent Act
            action = reader.act(static_vec, obs)
            
            # Env Step (Protected)
            try:
                obs, reward, terminated, truncated, _ = env.step(action)
            except BaseException:
                # Silent fail: environment crashed.
                # Penalize heavily and stop this episode.
                ep_ret -= 500.0
                break
            
            ep_ret += reward
            done = terminated or truncated

        total_return += ep_ret
        returns.append(ep_ret)
        
        # Calc stability
        obs_arr = np.asarray(obs_traj, dtype=np.float32)
        if len(obs_arr) > 0:
            # Penalize high angles/positions
            stab = -0.5 * np.mean(obs_arr[:, 0]**2) - 2.0 * np.mean(obs_arr[:, 2]**2)
        else:
            stab = -100.0
        total_stab += stab

    mean_ret = total_return / n_episodes
    mean_stab = total_stab / n_episodes
    ret_std = np.std(returns) if len(returns) > 1 else 0.0

    fitness = mean_ret + 0.1 * mean_stab - 0.01 * ret_std
    return fitness, mean_ret, mean_stab, -ret_std


def run_cartpole_evo(pop_size=64, generations=20):
    env = gym.make("CartPole-v1")
    reader = LinearStaticReader(env.observation_space.shape[0], env.action_space)
    
    # Init population
    pop = np.random.randn(pop_size, reader.dim) * 0.5
    hall_best = None
    hall_fit = -np.inf

    for gen in range(1, generations + 1):
        fits, rets = [], []
        for i in range(pop_size):
            f, r, _, _ = evaluate_cartpole_macro(env, reader, pop[i])
            fits.append(f)
            rets.append(r)
            if f > hall_fit:
                hall_fit = f
                hall_best = pop[i].copy()

        print(f"[CartPole Gen {gen}] BestRet={max(rets):.1f} HallFit={hall_fit:.1f}")

        # Elitism & Mutation
        elites = pop[np.argsort(fits)[-int(pop_size*0.2):]]
        new_pop = []
        for _ in range(pop_size):
            parent = elites[np.random.randint(len(elites))]
            child = parent + np.random.randn(reader.dim) * 0.5
            # Clamp weights to prevent float overflow over time
            child = np.clip(child, -10, 10)
            new_pop.append(child)
        pop = np.stack(new_pop)

    env.close()
    return hall_best


# ---------------------------------------------------------------------
# Pendulum evaluation
# ---------------------------------------------------------------------

def evaluate_pendulum_macro(env, reader, static_vec, n_episodes=5):
    total_return = 0.0
    total_stab = 0.0
    
    for _ in range(n_episodes):
        try:
            obs, _ = env.reset()
        except:
            return -10000.0, -1000.0, 0.0, 0.0
            
        ep_ret = 0.0
        obs_traj = []
        
        # Pendulum usually max 200 steps
        for _ in range(200):
            obs_traj.append(obs)
            action = reader.act(static_vec, obs)
            
            try:
                obs, reward, terminated, truncated, _ = env.step(action)
            except BaseException:
                ep_ret -= 1000.0
                break
                
            ep_ret += reward
            if terminated or truncated:
                break
        
        total_return += ep_ret
        
        # Stability: minimize angle and velocity
        obs_arr = np.asarray(obs_traj, dtype=np.float32)
        if len(obs_arr) > 0:
            # theta is arctan2(sin, cos)
            thetas = np.arctan2(obs_arr[:, 1], obs_arr[:, 0])
            stab = -0.5 * np.mean(thetas**2) - 0.05 * np.mean(obs_arr[:, 2]**2)
        else:
            stab = -100.0
        total_stab += stab

    mean_ret = total_return / n_episodes
    mean_stab = total_stab / n_episodes
    
    # Pendulum returns are negative (0 is perfect)
    fitness = mean_ret + 10.0 * mean_stab
    return fitness, mean_ret, mean_stab, 0.0


def run_pendulum_evo(pop_size=64, generations=20):
    env = gym.make("Pendulum-v1")
    reader = LinearStaticReader(env.observation_space.shape[0], env.action_space)
    
    pop = np.random.randn(pop_size, reader.dim) * 0.5
    hall_best = None
    hall_fit = -np.inf

    for gen in range(1, generations + 1):
        fits, rets = [], []
        for i in range(pop_size):
            f, r, _, _ = evaluate_pendulum_macro(env, reader, pop[i])
            fits.append(f)
            rets.append(r)
            if f > hall_fit:
                hall_fit = f
                hall_best = pop[i].copy()

        print(f"[Pendulum Gen {gen}] BestRet={max(rets):.1f} HallFit={hall_fit:.1f}")

        elites = pop[np.argsort(fits)[-int(pop_size*0.2):]]
        new_pop = []
        for _ in range(pop_size):
            parent = elites[np.random.randint(len(elites))]
            child = parent + np.random.randn(reader.dim) * 0.5
            child = np.clip(child, -10, 10)
            new_pop.append(child)
        pop = np.stack(new_pop)

    env.close()
    return hall_best


if __name__ == "__main__":
    print("=== Static Agent v7: Paranoid Mode ===")
    best_cp = run_cartpole_evo()
    print("\n=== Starting Pendulum ===")
    best_pend = run_pendulum_evo()