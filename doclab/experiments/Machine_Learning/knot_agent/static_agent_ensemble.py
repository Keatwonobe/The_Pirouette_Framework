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
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"!! Warning: Checkpoint found but corrupted: {e}")
        return None
    
# ---------------------------------------------------------------------
# Ensemble Static Agent
# ---------------------------------------------------------------------

class EnsembleStaticReader:
    def __init__(self, obs_dim, action_space, n_heads=3):
        self.obs_dim = obs_dim
        self.action_space = action_space
        self.n_heads = n_heads

        if isinstance(action_space, gym.spaces.Discrete):
            self.mode = "discrete"
            self.n_actions = action_space.n
            head_dim = self.n_actions * (self.obs_dim + 1)
            self.dim = head_dim * n_heads
            self.max_action = None
        else:
            assert isinstance(action_space, gym.spaces.Box)
            self.mode = "continuous"
            self.n_actions = 1
            head_dim = self.obs_dim + 1
            self.dim = head_dim * n_heads
            self.max_action = float(action_space.high[0])
        
        self.head_dim = head_dim

    def act(self, static_vec, obs):
        obs = np.array(obs, dtype=np.float32, copy=False)
        static_vec = np.array(static_vec, dtype=np.float32, copy=False)

        if not np.isfinite(obs).all():
            obs[~np.isfinite(obs)] = 0.0
        if not np.isfinite(static_vec).all():
            static_vec[~np.isfinite(static_vec)] = 0.0

        if self.mode == "discrete":
            votes = []
            for i in range(self.n_heads):
                head_params = static_vec[i * self.head_dim:(i + 1) * self.head_dim]
                limit = self.n_actions * self.obs_dim
                W_flat = head_params[:limit]
                b = head_params[limit:]
                
                W = W_flat.reshape(self.n_actions, self.obs_dim)
                logits = W @ obs + b
                
                if not np.isfinite(logits).all():
                    votes.append(0)
                else:
                    votes.append(int(np.argmax(logits)))
            return int(np.bincount(votes).argmax())
        
        else:
            outputs = []
            for i in range(self.n_heads):
                head_params = static_vec[i * self.head_dim:(i + 1) * self.head_dim]
                w = head_params[:self.obs_dim]
                b = head_params[self.obs_dim]
                
                val = float(np.dot(w, obs) + b)
                if not np.isfinite(val):
                    val = 0.0
                u = np.tanh(val) * self.max_action
                
                if not np.isfinite(u):
                    u = 0.0
                outputs.append(u)
            
            mean_u = np.mean(outputs)
            return np.array([mean_u], dtype=np.float32)


def evaluate_cartpole_ensemble(env, reader, static_vec, n_episodes=5):
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
    fitness = mean_ret - 0.02 * ret_std
    return fitness, mean_ret


def evaluate_pendulum_ensemble(env, reader, static_vec, n_episodes=5):
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


def run_cartpole_ensemble(pop_size=64, generations=40, n_heads=3):
    # Note: filename includes head count to avoid overwriting different tests
    ckpt = CheckpointManager(f"ckpt_ensemble_cartpole_h{n_heads}.pkl")
    
    env = gym.make("CartPole-v1")
    reader = EnsembleStaticReader(env.observation_space.shape[0], env.action_space, n_heads=n_heads)
    
    state = ckpt.load()
    if state:
        print(f"\n>>> Resuming Ensemble (h={n_heads}) from Gen {state['gen']} <<<")
        pop = state['pop']
        start_gen = state['gen'] + 1
        hall_best = state['hall_best']
        hall_fit = state['hall_fit']
    else:
        print(f"\n>>> Starting New Ensemble (h={n_heads}) Run <<<")
        pop = np.random.randn(pop_size, reader.dim).astype(np.float32) * 0.5
        start_gen = 1
        hall_best = None
        hall_fit = -np.inf

    try:
        for gen in range(start_gen, generations + 1):
            fits, rets = [], []
            for i in range(pop_size):
                f, r = evaluate_cartpole_ensemble(env, reader, pop[i]) 
                fits.append(f)
                rets.append(r)
                if f > hall_fit:
                    hall_fit = f
                    hall_best = pop[i].copy()

            best_ret = float(np.max(rets))
            mean_ret = float(np.mean(rets))
            print(f"[Ensemble h={n_heads} Gen {gen:3d}] BestRet={best_ret:7.1f} MeanRet={mean_ret:7.1f}")

            # Save Checkpoint
            ckpt.save({'gen': gen, 'pop': pop, 'hall_best': hall_best, 'hall_fit': hall_fit})

            # Evolution Strategy (Standard Elitism)
            elites = pop[np.argsort(fits)[-int(pop_size*0.2):]]
            new_pop = []
            for _ in range(pop_size):
                parent = elites[np.random.randint(len(elites))]
                child = parent + np.random.randn(reader.dim).astype(np.float32) * 0.5
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


def run_pendulum_ensemble(pop_size=64, generations=40, n_heads=3):
    ckpt = CheckpointManager(f"ckpt_ensemble_pendulum_h{n_heads}.pkl")
    
    env = gym.make("Pendulum-v1")
    reader = EnsembleStaticReader(env.observation_space.shape[0], env.action_space, n_heads=n_heads)
    
    state = ckpt.load()
    if state:
        print(f"\n>>> Resuming Pendulum Ensemble (h={n_heads}) from Gen {state['gen']} <<<")
        pop = state['pop']
        start_gen = state['gen'] + 1
        hall_best = state['hall_best']
        hall_fit = state['hall_fit']
    else:
        print(f"\n>>> Starting New Pendulum Ensemble (h={n_heads}) Run <<<")
        pop = np.random.randn(pop_size, reader.dim).astype(np.float32) * 0.5
        start_gen = 1
        hall_best = None
        hall_fit = -np.inf

    try:
        for gen in range(start_gen, generations + 1):
            fits, rets = [], []
            for i in range(pop_size):
                f, r = evaluate_pendulum_ensemble(env, reader, pop[i]) 
                fits.append(f)
                rets.append(r)
                if f > hall_fit:
                    hall_fit = f
                    hall_best = pop[i].copy()
            
            best_ret = float(np.max(rets))
            mean_ret = float(np.mean(rets))
            print(f"[Ensemble h={n_heads} Pend Gen {gen:3d}] BestRet={best_ret:7.1f} MeanRet={mean_ret:7.1f}")

            ckpt.save({'gen': gen, 'pop': pop, 'hall_best': hall_best, 'hall_fit': hall_fit})

            elites = pop[np.argsort(fits)[-int(pop_size*0.2):]]
            new_pop = []
            for _ in range(pop_size):
                parent = elites[np.random.randint(len(elites))]
                child = parent + np.random.randn(reader.dim).astype(np.float32) * 0.5
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
    print("=== Ensemble Static Agent ===")
    
    # Only running one config by default to keep it simple, 
    # but you can uncomment the loop if you want to train multiple in sequence.
    
    print("\n[CartPole with 3 heads]")
    best_cp = run_cartpole_ensemble(n_heads=3, generations=25)
        
    print("\n[Pendulum with 3 heads]")
    best_pend = run_pendulum_ensemble(n_heads=3)
    print("\nDone!")