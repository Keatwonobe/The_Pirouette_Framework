import gymnasium as gym
import numpy as np
import os
import pickle
import signal
import sys
import time

# ---------------------------------------------------------------------
# Robustness Utilities
# ---------------------------------------------------------------------
class CheckpointManager:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        """Safely saves data to a temporary file then renames it (Atomic Write)."""
        temp_name = self.filename + ".tmp"
        try:
            with open(temp_name, 'wb') as f:
                pickle.dump(data, f)
            if os.path.exists(self.filename):
                os.remove(self.filename)
            os.rename(temp_name, self.filename)
        except Exception as e:
            print(f"!! Warning: Failed to save checkpoint: {e}")

    def load(self):
        """Loads data if the file exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"!! Warning: Checkpoint found but corrupted: {e}")
        return None

# ---------------------------------------------------------------------
# Multi-Layer Static Policy
# ---------------------------------------------------------------------

class MLPStaticReader:
    def __init__(self, obs_dim, action_space, hidden_size=16):
        self.obs_dim = obs_dim
        self.action_space = action_space
        self.hidden_size = hidden_size

        if isinstance(action_space, gym.spaces.Discrete):
            self.mode = "discrete"
            self.n_actions = action_space.n
            dim1 = hidden_size * (obs_dim + 1)
            dim2 = self.n_actions * (hidden_size + 1)
            self.dim = dim1 + dim2
            self.max_action = None
        else:
            assert isinstance(action_space, gym.spaces.Box)
            self.mode = "continuous"
            self.n_actions = 1
            dim1 = hidden_size * (obs_dim + 1)
            dim2 = self.n_actions * (hidden_size + 1)
            self.dim = dim1 + dim2
            self.max_action = float(action_space.high[0])

    def act(self, static_vec, obs):
        obs = np.array(obs, dtype=np.float32, copy=False)
        static_vec = np.array(static_vec, dtype=np.float32, copy=False)

        if not np.isfinite(obs).all():
            obs[~np.isfinite(obs)] = 0.0
        if not np.isfinite(static_vec).all():
            static_vec[~np.isfinite(static_vec)] = 0.0

        # Parse layer 1
        dim1 = self.hidden_size * (self.obs_dim + 1)
        W1_flat = static_vec[:self.hidden_size * self.obs_dim]
        b1 = static_vec[self.hidden_size * self.obs_dim:dim1]
        
        W1 = W1_flat.reshape(self.hidden_size, self.obs_dim)
        h = W1 @ obs + b1
        
        if not np.isfinite(h).all():
            h[~np.isfinite(h)] = 0.0
        h = np.tanh(h)

        # Parse layer 2
        rem = static_vec[dim1:]
        if self.mode == "discrete":
            W2_flat = rem[:self.n_actions * self.hidden_size]
            b2 = rem[self.n_actions * self.hidden_size:]
            W2 = W2_flat.reshape(self.n_actions, self.hidden_size)
            logits = W2 @ h + b2
            
            if not np.isfinite(logits).all():
                return 0
            return int(np.argmax(logits))
        else:
            W2_flat = rem[:self.hidden_size]
            b2 = rem[self.hidden_size]
            val = float(np.dot(W2_flat, h) + b2)
            
            if not np.isfinite(val):
                val = 0.0
            u = np.tanh(val) * self.max_action
            
            if not np.isfinite(u):
                return np.array([0.0], dtype=np.float32)
            return np.array([u], dtype=np.float32)


def evaluate_cartpole(env, reader, static_vec, n_episodes=5):
    total_return = 0.0
    returns = []
    for _ in range(n_episodes):
        try:
            obs, _ = env.reset()
        except:
            return -1000.0, 0.0
        ep_ret = 0.0
        done = False
        while not done:
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

    mean_ret = total_return / n_episodes
    ret_std = np.std(returns) if len(returns) > 1 else 0.0
    fitness = mean_ret - 0.01 * ret_std
    return fitness, mean_ret


def evaluate_pendulum(env, reader, static_vec, n_episodes=5):
    total_return = 0.0
    for _ in range(n_episodes):
        try:
            obs, _ = env.reset()
        except:
            return -10000.0, -1000.0
        ep_ret = 0.0
        for _ in range(200):
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
    mean_ret = total_return / n_episodes
    return mean_ret, mean_ret


def run_cartpole_mlp(pop_size=64, generations=25, hidden_size=16):
    ckpt = CheckpointManager("ckpt_mlp_cartpole.pkl")
    env = gym.make("CartPole-v1")
    reader = MLPStaticReader(env.observation_space.shape[0], env.action_space, hidden_size)
    
    # Load or Init
    state = ckpt.load()
    if state:
        print(f"\n>>> Resuming CartPole MLP from Gen {state['gen']} <<<")
        pop = state['pop']
        start_gen = state['gen'] + 1
        hall_best = state['hall_best']
        hall_fit = state['hall_fit']
    else:
        print("\n>>> Starting New CartPole MLP Run <<<")
        pop = np.random.randn(pop_size, reader.dim).astype(np.float32) * 0.3
        start_gen = 1
        hall_best = None
        hall_fit = -np.inf

    try:
        for gen in range(start_gen, generations + 1):
            fits, rets = [], []
            for i in range(pop_size):
                f, r = evaluate_cartpole(env, reader, pop[i])
                fits.append(f)
                rets.append(r)
                if f > hall_fit:
                    hall_fit = f
                    hall_best = pop[i].copy()

            best_ret = float(np.max(rets))
            mean_ret = float(np.mean(rets))
            print(f"[MLP Gen {gen:3d}] BestRet={best_ret:7.1f} MeanRet={mean_ret:7.1f} HallFit={hall_fit:.1f}")

            # Checkpoint
            ckpt.save({'gen': gen, 'pop': pop, 'hall_best': hall_best, 'hall_fit': hall_fit})

            # Elite selection + mutation
            elites = pop[np.argsort(fits)[-int(pop_size*0.2):]]
            new_pop = []
            for _ in range(pop_size):
                parent = elites[np.random.randint(len(elites))]
                child = parent + np.random.randn(reader.dim).astype(np.float32) * 0.3
                child = np.clip(child, -10, 10)
                new_pop.append(child)
            pop = np.stack(new_pop)

    except KeyboardInterrupt:
        print("\n!!! Interrupted by User. Progress Saved. !!!")
    except Exception as e:
        print(f"\n!!! CRASH DETECTED: {e} !!!")
        raise
    finally:
        env.close()
    return hall_best


def run_pendulum_mlp(pop_size=64, generations=80, hidden_size=16):
    ckpt = CheckpointManager("ckpt_mlp_pendulum.pkl")
    env = gym.make("Pendulum-v1")
    reader = MLPStaticReader(env.observation_space.shape[0], env.action_space, hidden_size)
    
    state = ckpt.load()
    if state:
        print(f"\n>>> Resuming Pendulum MLP from Gen {state['gen']} <<<")
        pop = state['pop']
        start_gen = state['gen'] + 1
        hall_best = state['hall_best']
        hall_fit = state['hall_fit']
    else:
        print("\n>>> Starting New Pendulum MLP Run <<<")
        pop = np.random.randn(pop_size, reader.dim).astype(np.float32) * 0.3
        start_gen = 1
        hall_best = None
        hall_fit = -np.inf

    try:
        for gen in range(start_gen, generations + 1):
            fits, rets = [], []
            for i in range(pop_size):
                f, r = evaluate_pendulum(env, reader, pop[i])
                fits.append(f)
                rets.append(r)
                if f > hall_fit:
                    hall_fit = f
                    hall_best = pop[i].copy()

            best_ret = float(np.max(rets))
            mean_ret = float(np.mean(rets))
            print(f"[MLP Pend Gen {gen:3d}] BestRet={best_ret:7.1f} MeanRet={mean_ret:7.1f}")

            ckpt.save({'gen': gen, 'pop': pop, 'hall_best': hall_best, 'hall_fit': hall_fit})

            elites = pop[np.argsort(fits)[-int(pop_size*0.2):]]
            new_pop = []
            for _ in range(pop_size):
                parent = elites[np.random.randint(len(elites))]
                child = parent + np.random.randn(reader.dim).astype(np.float32) * 0.3
                child = np.clip(child, -10, 10)
                new_pop.append(child)
            pop = np.stack(new_pop)

    except KeyboardInterrupt:
        print("\n!!! Interrupted by User. Progress Saved. !!!")
    except Exception as e:
        print(f"\n!!! CRASH DETECTED: {e} !!!")
        raise
    finally:
        env.close()
    return hall_best


if __name__ == "__main__":
    print("=== Static MLP Agent: Evolution with Hidden Layers ===")
    print("\n[CartPole]")
    best_cp = run_cartpole_mlp()
    print("\n[Pendulum]")
    best_pend = run_pendulum_mlp()
    print("\nDone!")