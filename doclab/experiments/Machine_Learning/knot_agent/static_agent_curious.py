import gymnasium as gym
import numpy as np
from collections import deque

import os
import pickle
import signal
import sys
import time

# --- Robustness Utilities ---
class CheckpointManager:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        """Safely saves data to a temporary file then renames it (Atomic Write)."""
        temp_name = self.filename + ".tmp"
        try:
            with open(temp_name, 'wb') as f:
                pickle.dump(data, f)
            # Atomic replace on POSIX; usually safe enough on Windows
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
# Curiosity-Driven Static Agent: Novelty rewarding exploration
# ---------------------------------------------------------------------

class CuriousStaticReader:
    def __init__(self, obs_dim, action_space):
        self.obs_dim = obs_dim
        self.action_space = action_space

        if isinstance(action_space, gym.spaces.Discrete):
            self.mode = "discrete"
            self.n_actions = action_space.n
            self.dim = self.n_actions * (self.obs_dim + 1)
            self.max_action = None
        else:
            assert isinstance(action_space, gym.spaces.Box)
            self.mode = "continuous"
            self.n_actions = 1
            self.dim = self.obs_dim + 1
            self.max_action = float(action_space.high[0])

    def act(self, static_vec, obs):
        obs = np.array(obs, dtype=np.float32, copy=False)
        static_vec = np.array(static_vec, dtype=np.float32, copy=False)

        if not np.isfinite(obs).all():
            obs[~np.isfinite(obs)] = 0.0
        if not np.isfinite(static_vec).all():
            static_vec[~np.isfinite(static_vec)] = 0.0

        if self.mode == "discrete":
            limit = self.n_actions * self.obs_dim
            W_flat = static_vec[:limit]
            b = static_vec[limit:]
            W = W_flat.reshape(self.n_actions, self.obs_dim)
            logits = W @ obs + b
            
            if not np.isfinite(logits).all():
                return 0
            return int(np.argmax(logits))
        else:
            w = static_vec[:self.obs_dim]
            b = static_vec[self.obs_dim]
            val = float(np.dot(w, obs) + b)
            
            if not np.isfinite(val):
                val = 0.0
            u = np.tanh(val) * self.max_action
            
            if not np.isfinite(u):
                return np.array([0.0], dtype=np.float32)
            return np.array([u], dtype=np.float32)


class NoveltyTracker:
    """Tracks state visitation for novelty bonuses"""
    def __init__(self, obs_dim, buffer_size=10000):
        self.obs_dim = obs_dim
        self.buffer = deque(maxlen=buffer_size)
        
    def add(self, obs):
        self.buffer.append(obs.copy())
    
    def get_novelty(self, obs, k=5):
        """Return novelty as average distance to k nearest neighbors"""
        if len(self.buffer) < k:
            return 1.0  # Everything is novel at first
        
        # Sample for efficiency
        sample_size = min(len(self.buffer), 500)
        samples = np.random.choice(len(self.buffer), sample_size, replace=False)
        neighbors = np.array([self.buffer[i] for i in samples])
        
        # Compute distances
        dists = np.linalg.norm(neighbors - obs, axis=1)
        k_nearest = np.partition(dists, min(k, len(dists)-1))[:k]
        return float(np.mean(k_nearest))


def evaluate_cartpole_curious(env, reader, static_vec, novelty_tracker, n_episodes=5, curiosity_weight=0.1):
    total_return = 0.0
    total_novelty = 0.0
    returns = []

    for _ in range(n_episodes):
        try:
            obs, _ = env.reset()
        except:
            return -1000.0, 0.0, 0.0

        ep_ret = 0.0
        ep_novelty = 0.0
        done = False
        steps = 0

        while not done:
            # Get novelty bonus
            novelty = novelty_tracker.get_novelty(obs)
            ep_novelty += novelty
            novelty_tracker.add(obs)
            
            action = reader.act(static_vec, obs)
            try:
                obs, reward, terminated, truncated, _ = env.step(action)
            except Exception:
                ep_ret -= 500.0
                break
            
            ep_ret += reward
            steps += 1
            done = terminated or truncated

        total_return += ep_ret
        total_novelty += ep_novelty / max(steps, 1)
        returns.append(ep_ret)

    mean_ret = total_return / n_episodes
    mean_novelty = total_novelty / n_episodes
    ret_std = np.std(returns) if len(returns) > 1 else 0.0
    
    fitness = mean_ret + curiosity_weight * mean_novelty - 0.01 * ret_std
    return fitness, mean_ret, mean_novelty

def evaluate_pendulum_curious(env, reader, static_vec, novelty_tracker, n_episodes=5, curiosity_weight=1.0):
    total_return = 0.0
    total_novelty = 0.0
    
    for _ in range(n_episodes):
        try:
            obs, _ = env.reset()
        except:
            return -10000.0, -1000.0, 0.0
            
        ep_ret = 0.0
        ep_novelty = 0.0
        steps = 0
        
        for _ in range(200):
            novelty = novelty_tracker.get_novelty(obs)
            ep_novelty += novelty
            novelty_tracker.add(obs)
            
            action = reader.act(static_vec, obs)
            try:
                obs, reward, terminated, truncated, _ = env.step(action)
            except Exception:
                ep_ret -= 1000.0
                break
            
            ep_ret += reward
            steps += 1
            if terminated or truncated:
                break
        
        total_return += ep_ret
        total_novelty += ep_novelty / max(steps, 1)

    mean_ret = total_return / n_episodes
    mean_novelty = total_novelty / n_episodes
    fitness = mean_ret + curiosity_weight * mean_novelty
    return fitness, mean_ret, mean_novelty

def run_cartpole_curious(pop_size=64, generations=30, curiosity_weight=0.5):
    ckpt = CheckpointManager("ckpt_curious_cartpole.pkl")
    env = gym.make("CartPole-v1")
    reader = CuriousStaticReader(env.observation_space.shape[0], env.action_space)
    
    # Attempt load
    state = ckpt.load()
    if state:
        print(f"\n>>> Resuming CartPole from Gen {state['gen']} <<<")
        pop = state['pop']
        novelty_tracker = state['novelty_tracker']
        start_gen = state['gen'] + 1
        hall_best = state['hall_best']
        hall_fit = state['hall_fit']
    else:
        print("\n>>> Starting New CartPole Run <<<")
        novelty_tracker = NoveltyTracker(env.observation_space.shape[0])
        pop = np.random.randn(pop_size, reader.dim).astype(np.float32) * 0.5
        start_gen = 1
        hall_best = None
        hall_fit = -np.inf

    try:
        for gen in range(start_gen, generations + 1):
            fits, rets, novs = [], [], []
            for i in range(pop_size):
                f, r, n = evaluate_cartpole_curious(env, reader, pop[i], novelty_tracker, curiosity_weight=curiosity_weight)
                fits.append(f)
                rets.append(r)
                novs.append(n)
                if f > hall_fit:
                    hall_fit = f
                    hall_best = pop[i].copy()

            best_ret = float(np.max(rets))
            mean_ret = float(np.mean(rets))
            mean_nov = float(np.mean(novs))
            print(f"[Curious Gen {gen:3d}] BestRet={best_ret:7.1f} MeanRet={mean_ret:7.1f} MeanNov={mean_nov:.3f}")

            # Checkpoint at end of generation
            ckpt.save({
                'gen': gen,
                'pop': pop,
                'novelty_tracker': novelty_tracker, # CRITICAL: Save memory of visited states
                'hall_best': hall_best,
                'hall_fit': hall_fit
            })

            # Evolution (Elitism + Mutation)
            elites = pop[np.argsort(fits)[-int(pop_size*0.2):]]
            new_pop = []
            for _ in range(pop_size):
                parent = elites[np.random.randint(len(elites))]
                child = parent + np.random.randn(reader.dim).astype(np.float32) * 0.6
                child = np.clip(child, -10, 10)
                new_pop.append(child)
            pop = np.stack(new_pop)

    except KeyboardInterrupt:
        print("\n!!! Interrupted by User. Progress Saved. !!!")
    except Exception as e:
        print(f"\n!!! CRASH DETECTED: {e} !!!")
        # Optional: try to save emergency dump
        raise
    finally:
        env.close()

    return hall_best

def run_pendulum_curious(pop_size=64, generations=60, curiosity_weight=2.0):
    ckpt = CheckpointManager("ckpt_curious_pendulum.pkl")
    env = gym.make("Pendulum-v1")
    reader = CuriousStaticReader(env.observation_space.shape[0], env.action_space)
    
    state = ckpt.load()
    if state:
        print(f"\n>>> Resuming Pendulum from Gen {state['gen']} <<<")
        pop = state['pop']
        novelty_tracker = state['novelty_tracker']
        start_gen = state['gen'] + 1
        hall_best = state['hall_best']
        hall_fit = state['hall_fit']
    else:
        print("\n>>> Starting New Pendulum Run <<<")
        novelty_tracker = NoveltyTracker(env.observation_space.shape[0])
        pop = np.random.randn(pop_size, reader.dim).astype(np.float32) * 0.5
        start_gen = 1
        hall_best = None
        hall_fit = -np.inf

    try:
        for gen in range(start_gen, generations + 1):
            fits, rets, novs = [], [], []
            for i in range(pop_size):
                f, r, n = evaluate_pendulum_curious(env, reader, pop[i], novelty_tracker, curiosity_weight=curiosity_weight)
                fits.append(f)
                rets.append(r)
                novs.append(n)
                if f > hall_fit:
                    hall_fit = f
                    hall_best = pop[i].copy()

            best_ret = float(np.max(rets))
            mean_ret = float(np.mean(rets))
            mean_nov = float(np.mean(novs))
            print(f"[Curious Pend Gen {gen:3d}] BestRet={best_ret:7.1f} MeanRet={mean_ret:7.1f} MeanNov={mean_nov:.3f}")

            ckpt.save({
                'gen': gen,
                'pop': pop,
                'novelty_tracker': novelty_tracker,
                'hall_best': hall_best,
                'hall_fit': hall_fit
            })

            elites = pop[np.argsort(fits)[-int(pop_size*0.2):]]
            new_pop = []
            for _ in range(pop_size):
                parent = elites[np.random.randint(len(elites))]
                child = parent + np.random.randn(reader.dim).astype(np.float32) * 0.6
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
    print("=== Curiosity-Driven Static Agent ===")
    print("\n[CartPole with Novelty]")
    best_cp = run_cartpole_curious()
    print("\n[Pendulum with Novelty]")
    best_pend = run_pendulum_curious()
    print("\nDone!")
