import gymnasium as gym
import numpy as np

# ---------------------------------------------------------------------
# Linear static policy: Manual Sanitization Edition
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
        Act method with manual, non-recursive sanitization.
        """
        # 1. Force simple float32 arrays (strips weird numpy attributes)
        obs = np.array(obs, dtype=np.float32, copy=False)
        static_vec = np.array(static_vec, dtype=np.float32, copy=False)

        # 2. Manual Clean: Observation
        # If any value is NaN or Inf, replace ONLY those values with 0
        if not np.isfinite(obs).all():
            mask = ~np.isfinite(obs)
            obs[mask] = 0.0

        # 3. Manual Clean: Weights
        # (Rarely needed, but prevents the crash you just saw)
        if not np.isfinite(static_vec).all():
            mask = ~np.isfinite(static_vec)
            static_vec[mask] = 0.0

        if self.mode == "discrete":
            # Slicing
            limit = self.n_actions * self.obs_dim
            W_flat = static_vec[:limit]
            b = static_vec[limit:]
            
            W = W_flat.reshape(self.n_actions, self.obs_dim)
            logits = W @ obs + b
            
            # Sanitize Logits
            if not np.isfinite(logits).all():
                return 0
            
            return int(np.argmax(logits))

        else:  # continuous
            w = static_vec[: self.obs_dim]
            b = static_vec[self.obs_dim]
            
            val = float(np.dot(w, obs) + b)
            
            # Sanitize pre-activation scalar
            if np.isnan(val) or np.isinf(val):
                val = 0.0
                
            u = np.tanh(val) * self.max_action
            
            # Final check
            if np.isnan(u) or np.isinf(u):
                return np.array([0.0], dtype=np.float32)
                
            return np.array([u], dtype=np.float32)


# ---------------------------------------------------------------------
# CartPole evaluation
# ---------------------------------------------------------------------

def evaluate_cartpole_macro(env, reader, static_vec, n_episodes=5):
    total_return = 0.0
    total_stab = 0.0
    returns = []

    for _ in range(n_episodes):
        try:
            obs, _ = env.reset()
        except:
            return -1000.0, 0.0, 0.0, 0.0

        ep_ret = 0.0
        obs_traj = []
        done = False

        while not done:
            obs_traj.append(obs)
            action = reader.act(static_vec, obs)
            
            try:
                obs, reward, terminated, truncated, _ = env.step(action)
            except Exception:
                ep_ret -= 500.0
                break
            
            ep_ret += reward
            done = terminated or truncated

        total_return += ep_ret
        returns.append(ep_ret)
        
        obs_arr = np.array(obs_traj, dtype=np.float32)
        if len(obs_arr) > 0:
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
    # Recast explicit float32
    env = gym.make("CartPole-v1")
    reader = LinearStaticReader(env.observation_space.shape[0], env.action_space)
    
    pop = np.random.randn(pop_size, reader.dim).astype(np.float32) * 0.5
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

        gen_best_ret = float(np.max(rets))
        gen_mean_ret = float(np.mean(rets))

        print(
            f"[Gen {gen:4d}] GenBestRet={gen_best_ret:7.1f}  "
            f"GenMeanRet={gen_mean_ret:7.1f}"
        )

        print(f"[CartPole Gen {gen}] BestRet={max(rets):.1f} HallFit={hall_fit:.1f}")

        elites = pop[np.argsort(fits)[-int(pop_size*0.2):]]
        new_pop = []
        for _ in range(pop_size):
            parent = elites[np.random.randint(len(elites))]
            child = parent + np.random.randn(reader.dim).astype(np.float32) * 0.5
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
        
        for _ in range(200):
            obs_traj.append(obs)
            action = reader.act(static_vec, obs)
            
            try:
                obs, reward, terminated, truncated, _ = env.step(action)
            except Exception:
                ep_ret -= 1000.0
                break
                
            ep_ret += reward
            if terminated or truncated:
                break
        
        total_return += ep_ret
        
        obs_arr = np.array(obs_traj, dtype=np.float32)
        if len(obs_arr) > 0:
            # theta is arctan2(sin, cos)
            # obs: [cos, sin, theta_dot]
            thetas = np.arctan2(obs_arr[:, 1], obs_arr[:, 0])
            stab = -0.5 * np.mean(thetas**2) - 0.05 * np.mean(obs_arr[:, 2]**2)
        else:
            stab = -100.0
        total_stab += stab

    mean_ret = total_return / n_episodes
    mean_stab = total_stab / n_episodes
    
    fitness = mean_ret + 10.0 * mean_stab
    return fitness, mean_ret, mean_stab, 0.0


def run_pendulum_evo(pop_size=64, generations=50):
    env = gym.make("Pendulum-v1")
    reader = LinearStaticReader(env.observation_space.shape[0], env.action_space)
    
    pop = np.random.randn(pop_size, reader.dim).astype(np.float32) * 0.5
    hall_best = None
    hall_fit = -np.inf

    gen_mean_ret = float(np.mean(rets))

    for gen in range(1, generations + 1):
        fits, rets = [], []
        for i in range(pop_size):
            f, r, _, _ = evaluate_pendulum_macro(env, reader, pop[i])
            fits.append(f)
            rets.append(r)
            if f > hall_fit:
                hall_fit = f
                hall_best = pop[i].copy() 
                     

        print(f"[Pendulum Gen {gen}] GenMeanRet = {gen_mean_ret} BestRet={max(rets):.1f} HallFit={hall_fit:.1f}")

        elites = pop[np.argsort(fits)[-int(pop_size*0.2):]]
        new_pop = []
        for _ in range(pop_size):
            parent = elites[np.random.randint(len(elites))]
            child = parent + np.random.randn(reader.dim).astype(np.float32) * 0.5
            child = np.clip(child, -10, 10)
            new_pop.append(child)
        pop = np.stack(new_pop)

    env.close()
    return hall_best


if __name__ == "__main__":
    print("=== Static Agent v8: Manual Sanitize ===")
    best_cp = run_cartpole_evo()
    print("\n=== Starting Pendulum ===")
    best_pend = run_pendulum_evo()
    print("done")