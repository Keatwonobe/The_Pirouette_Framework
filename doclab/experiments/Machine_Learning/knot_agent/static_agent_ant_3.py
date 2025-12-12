import gymnasium as gym
import numpy as np
import os
import pickle
import time
import signal
import multiprocessing
from multiprocessing import Pool, cpu_count

# ---------------------------------------------------------------------
# Global Worker State
# ---------------------------------------------------------------------
_worker_env = None

def worker_init():
    """
    Initializes the environment.
    With maxtasksperchild, this will run periodically to create fresh envs.
    """
    global _worker_env
    import warnings
    warnings.filterwarnings("ignore")
    
    try:
        # Explicitly disable rendering to prevent OpenGL window handles leaking
        _worker_env = gym.make("Ant-v4", terminate_when_unhealthy=True, render_mode=None)
        _worker_env.reset()
    except Exception as e:
        print(f"Worker init failed: {e}")

def worker_eval(args):
    static_vec, seed = args
    global _worker_env
    
    # Safety check: if init failed or env died
    if _worker_env is None:
        return -1000.0, 0.0, 0

    # Standard Ant config
    h1, h2 = 64, 32
    obs_dim = 27 # Ant-v4 fixed size
    action_dim = 8
    max_action = 1.0

    try:
        obs, _ = _worker_env.reset(seed=seed)
    except:
        return -1000.0, 0.0, 0

    # Pre-calculate layout indices for speed
    l1_size = h1 * (obs_dim + 1)
    l2_size = h2 * (h1 + 1)
    l3_size = action_dim * (h2 + 1)

    total_reward = 0.0
    steps = 0
    max_steps = 1000
    
    try:
        for _ in range(max_steps):
            # --- FAST FORWARD PASS ---
            obs = np.asarray(obs, dtype=np.float32)
            
            # Layer 1
            w1_end = h1 * obs_dim
            w1 = static_vec[:w1_end].reshape(h1, obs_dim)
            b1 = static_vec[w1_end:l1_size]
            h1_out = np.tanh(w1 @ obs + b1)
            
            # Layer 2
            l2_start = l1_size
            w2_end = l2_start + h2 * h1
            w2 = static_vec[l2_start:w2_end].reshape(h2, h1)
            b2 = static_vec[w2_end:l2_start + l2_size]
            h2_out = np.tanh(w2 @ h1_out + b2)
            
            # Layer 3
            l3_start = l1_size + l2_size
            w3_end = l3_start + action_dim * h2
            w3 = static_vec[l3_start:w3_end].reshape(action_dim, h2)
            b3 = static_vec[w3_end:]
            action = np.tanh(w3 @ h2_out + b3) * max_action
            # -------------------------

            obs, reward, terminated, truncated, _ = _worker_env.step(action)
            total_reward += reward
            steps += 1
            
            if terminated or truncated:
                break
    except Exception:
        return -1000.0, total_reward, steps

    # Fitness shaping
    fitness = total_reward
    # Penalize instant death
    if steps < 20: fitness -= 500
    elif steps < 100: fitness -= 100
    
    # Reward survival explicitly to encourage standing up
    fitness += steps * 0.2
    
    return fitness, total_reward, steps

# ---------------------------------------------------------------------
# Utilities
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

class DeepMLPReader:
    def __init__(self, obs_dim, action_space, h1=64, h2=32):
        self.obs_dim = obs_dim
        self.action_space = action_space
        self.h1 = h1
        self.h2 = h2
        self.n_actions = action_space.shape[0]
        self.l1_size = h1 * (obs_dim + 1)
        self.l2_size = h2 * (h1 + 1)
        self.l3_size = self.n_actions * (h2 + 1)
        self.dim = self.l1_size + self.l2_size + self.l3_size
        self.max_action = float(action_space.high[0])
        
    def init_weights(self):
        vec = np.zeros(self.dim, dtype=np.float32)
        s1 = np.sqrt(2.0 / self.obs_dim)
        s2 = np.sqrt(2.0 / self.h1)
        s3 = np.sqrt(2.0 / self.h2)
        
        end1 = self.h1 * self.obs_dim
        vec[:end1] = np.random.randn(end1) * s1
        start2 = self.l1_size
        end2 = start2 + (self.h2 * self.h1)
        vec[start2:end2] = np.random.randn(end2-start2) * s2
        start3 = self.l1_size + self.l2_size
        end3 = start3 + (self.n_actions * self.h2)
        vec[start3:end3] = np.random.randn(end3-start3) * s3
        
        return vec

# ---------------------------------------------------------------------
# Main Evolution Loop
# ---------------------------------------------------------------------
def run_ant_evolution(pop_size=256, generations=2000):
    ckpt = CheckpointManager("ckpt_ant_deep_v3.pkl")
    
    # Dummy env to get shapes
    temp_env = gym.make("Ant-v4")
    reader = DeepMLPReader(temp_env.observation_space.shape[0], temp_env.action_space, h1=64, h2=32)
    temp_env.close()
    
    def get_sigma(gen, hall_fit):
        # Exploration schedule
        base_sigma = 0.02 if gen > 200 else 0.1
        if hall_fit < 50: base_sigma = 0.2 # Panic mode: explore hard if failing
        return base_sigma
    
    state = ckpt.load()
    if state:
        print(f"\n>>> Resuming Ant (Params={reader.dim}) from Gen {state['gen']} <<<")
        pop = state['pop']
        start_gen = state['gen'] + 1
        hall_best = state['hall_best']
        hall_fit = state['hall_fit']
        hall_history = state.get('hall_history', [])
    else:
        print(f"\n>>> Starting New Ant Run (Params={reader.dim}) <<<")
        pop = np.stack([reader.init_weights() for _ in range(pop_size)])
        start_gen = 1
        hall_best = None
        hall_fit = -np.inf
        hall_history = []

    # 1. Detect Cores
    n_workers = max(1, cpu_count() - 2) # Leave 2 cores for Windows background tasks
    
    # 2. The Magic Fix: maxtasksperchild
    # This restarts the worker process every 20 episodes.
    # It adds slight overhead but GUARANTEES that handle leaks are cleared.
    pool = Pool(processes=n_workers, initializer=worker_init, maxtasksperchild=20)
    
    try:
        print(f"Running on {n_workers} cores (Recycling workers every 20 tasks)...")
        
        for gen in range(start_gen, generations + 1):
            start_time = time.time()
            sigma = get_sigma(gen, hall_fit)

            # Deterministic seeds per generation for reproducibility
            seeds = [gen * pop_size + i for i in range(pop_size)]
            args = [(pop[i], seeds[i]) for i in range(pop_size)]
            
            # map() blocks until done. If it hangs here, maxtasksperchild usually fixes it.
            results = pool.map(worker_eval, args)
            
            fits = np.array([r[0] for r in results])
            rets = np.array([r[1] for r in results])
            steps = np.array([r[2] for r in results])

            # Stats & Hall of Fame
            best_idx = np.argmax(fits)
            if fits[best_idx] > hall_fit:
                hall_fit = fits[best_idx]
                hall_best = pop[best_idx].copy()
                print(f"  >>> New Hall Best! Fitness={hall_fit:.1f} Return={rets[best_idx]:.1f}")

            hall_history.append(hall_fit)
            
            duration = time.time() - start_time
            print(f"[Gen {gen:4d}] BestRet={np.max(rets):6.1f} | MeanRet={np.mean(rets):6.1f} | Steps={np.mean(steps):4.0f} | Time={duration:.1f}s")

            # Save
            ckpt.save({'gen': gen, 'pop': pop, 'hall_best': hall_best, 'hall_fit': hall_fit, 'hall_history': hall_history})

            # Elitism Selection
            n_elites = max(4, int(pop_size * 0.15))
            elite_indices = np.argsort(fits)[-n_elites:]
            elites = pop[elite_indices]
            
            new_pop = [hall_best.copy()]
            
            while len(new_pop) < pop_size:
                # Tournament
                p1 = elites[np.random.randint(len(elites))]
                p2 = elites[np.random.randint(len(elites))]
                
                # Crossover
                mask = np.random.rand(reader.dim) > 0.5
                child = np.where(mask, p1, p2)
                
                # Mutate
                child += np.random.randn(reader.dim).astype(np.float32) * sigma
                new_pop.append(child)
            
            pop = np.stack(new_pop)
            
            # Stuck detection
            if gen % 50 == 0 and len(hall_history) > 50:
                if hall_history[-1] - hall_history[-50] < 10:
                    print("  >> Stagnation: Injecting diversity <<")
                    # Replace bottom 25% with fresh randoms
                    n_fresh = int(pop_size * 0.25)
                    for i in range(n_fresh):
                        pop[i] = reader.init_weights()

    except KeyboardInterrupt:
        print("\n!!! Interrupted. Cleaning up... !!!")
        pool.terminate()
        pool.join()
    except Exception as e:
        print(f"\n!!! CRASH: {e} !!!")
        pool.terminate()
        raise
    finally:
        if 'pool' in locals():
            pool.close()
            pool.join()

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn', force=True)
    print("=== Deep Static MLP: Ant-v4 (Bomb-Proof V3) ===")
    run_ant_evolution(pop_size=256, generations=5000)