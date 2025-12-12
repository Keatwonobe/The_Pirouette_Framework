import gymnasium as gym
import numpy as np
import os
import pickle
import time
from multiprocessing import Pool

# ---------------------------------------------------------------------
# Checkpoint Manager
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
# Deep MLP Reader with Layer Normalization-like Scaling
# ---------------------------------------------------------------------
class DeepMLPReader:
    """
    3-layer MLP with careful weight scaling to prevent explosion.
    Key insight: For high-dim continuous control, we need:
    1. Small initial weights (Xavier-like init)
    2. Bounded activations
    3. Output scaling that matches action space
    """
    def __init__(self, obs_dim, action_space, h1=64, h2=32):
        self.obs_dim = obs_dim
        self.action_space = action_space
        self.h1 = h1
        self.h2 = h2

        assert isinstance(action_space, gym.spaces.Box)
        self.n_actions = action_space.shape[0]
        
        # Layer dims with biases
        self.l1_size = h1 * (obs_dim + 1)
        self.l2_size = h2 * (h1 + 1)
        self.l3_size = self.n_actions * (h2 + 1)
        
        self.dim = self.l1_size + self.l2_size + self.l3_size
        self.max_action = float(action_space.high[0])
        
        # Scaling factors for weight initialization (Xavier-like)
        self.scale1 = np.sqrt(2.0 / obs_dim)
        self.scale2 = np.sqrt(2.0 / h1)
        self.scale3 = np.sqrt(2.0 / h2)

    def init_weights(self):
        """Initialize with scaled random weights"""
        vec = np.zeros(self.dim, dtype=np.float32)
        
        # Layer 1
        w1_size = self.h1 * self.obs_dim
        vec[:w1_size] = np.random.randn(w1_size) * self.scale1
        
        # Layer 2
        l2_start = self.l1_size
        w2_size = self.h2 * self.h1
        vec[l2_start:l2_start + w2_size] = np.random.randn(w2_size) * self.scale2
        
        # Layer 3
        l3_start = self.l1_size + self.l2_size
        w3_size = self.n_actions * self.h2
        vec[l3_start:l3_start + w3_size] = np.random.randn(w3_size) * self.scale3
        
        return vec

    def act(self, static_vec, obs):
        # Sanitize inputs
        obs = np.asarray(obs, dtype=np.float32)
        if not np.isfinite(obs).all():
            obs = np.nan_to_num(obs, nan=0.0, posinf=1.0, neginf=-1.0)
        
        # Layer 1: obs -> h1
        w1_end = self.h1 * self.obs_dim
        w1 = static_vec[:w1_end].reshape(self.h1, self.obs_dim)
        b1 = static_vec[w1_end:self.l1_size]
        
        z1 = w1 @ obs + b1
        if not np.isfinite(z1).all():
            z1 = np.nan_to_num(z1, nan=0.0, posinf=1.0, neginf=-1.0)
        h1 = np.tanh(z1)
        
        # Layer 2: h1 -> h2
        l2_start = self.l1_size
        w2_end = l2_start + self.h2 * self.h1
        w2 = static_vec[l2_start:w2_end].reshape(self.h2, self.h1)
        b2 = static_vec[w2_end:l2_start + self.l2_size]
        
        z2 = w2 @ h1 + b2
        if not np.isfinite(z2).all():
            z2 = np.nan_to_num(z2, nan=0.0, posinf=1.0, neginf=-1.0)
        h2 = np.tanh(z2)
        
        # Layer 3: h2 -> action
        l3_start = self.l1_size + self.l2_size
        w3_end = l3_start + self.n_actions * self.h2
        w3 = static_vec[l3_start:w3_end].reshape(self.n_actions, self.h2)
        b3 = static_vec[w3_end:]
        
        z3 = w3 @ h2 + b3
        if not np.isfinite(z3).all():
            z3 = np.nan_to_num(z3, nan=0.0, posinf=1.0, neginf=-1.0)
        
        action = np.tanh(z3) * self.max_action
        return action


def evaluate_ant_worker(args):
    """Worker function for parallel evaluation"""
    static_vec, seed = args
    try:
        env = gym.make("Ant-v5", terminate_when_unhealthy=True)
        env.reset(seed=seed)
    except Exception as e:
        return -1000.0, 0.0, 0
    
    # Create reader (needs to match main)
    obs_dim = env.observation_space.shape[0]
    reader = DeepMLPReader(obs_dim, env.action_space, h1=64, h2=32)
    
    try:
        obs, _ = env.reset(seed=seed)
    except:
        env.close()
        return -1000.0, 0.0, 0

    total_reward = 0.0
    steps = 0
    max_steps = 1000
    
    for _ in range(max_steps):
        action = reader.act(static_vec, obs)
        
        try:
            obs, reward, terminated, truncated, _ = env.step(action)
        except Exception:
            env.close()
            return -1000.0, total_reward, steps
        
        total_reward += reward
        steps += 1
        
        if terminated or truncated:
            break
    
    env.close()
    
    # Fitness shaping: heavily penalize instant death
    fitness = total_reward
    if steps < 50:
        fitness -= 500
    elif steps < 100:
        fitness -= 200
    
    # Small bonus for survival
    fitness += steps * 0.1
    
    return fitness, total_reward, steps


def evaluate_ant(env, reader, static_vec, seed=None):
    """Single-threaded evaluation for checkpointing"""
    try:
        obs, _ = env.reset(seed=seed)
    except:
        return -1000.0, 0.0, 0

    total_reward = 0.0
    steps = 0
    max_steps = 1000
    
    for _ in range(max_steps):
        action = reader.act(static_vec, obs)
        
        try:
            obs, reward, terminated, truncated, _ = env.step(action)
        except Exception:
            return -1000.0, total_reward, steps
        
        total_reward += reward
        steps += 1
        
        if terminated or truncated:
            break
    
    # Same fitness shaping as worker
    fitness = total_reward
    if steps < 50:
        fitness -= 500
    elif steps < 100:
        fitness -= 200
    fitness += steps * 0.1
    
    return fitness, total_reward, steps


def run_ant_evolution(pop_size=256, generations=2000, use_parallel=True, n_workers=8):
    ckpt = CheckpointManager("ckpt_ant_deep_v2.pkl")
    
    try:
        env = gym.make("Ant-v5", terminate_when_unhealthy=True)
    except Exception as e:
        print(f"Error: Could not make Ant-v5. Do you have mujoco installed? ({e})")
        return

    reader = DeepMLPReader(env.observation_space.shape[0], env.action_space, h1=64, h2=32)
    
    # Adaptive mutation schedule
    def get_sigma(gen, hall_fit):
        """Adaptive: if stuck, increase exploration"""
        base_sigma = 0.05 if gen > 100 else 0.15
        # Add noise if stuck at low fitness
        if hall_fit < 100:
            base_sigma *= 2.0
        return base_sigma
    
    # Load or Init
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
        # Initialize population with scaled weights
        pop = np.stack([reader.init_weights() for _ in range(pop_size)])
        start_gen = 1
        hall_best = None
        hall_fit = -np.inf
        hall_history = []

    # Setup parallel pool
    pool = Pool(processes=n_workers) if use_parallel else None
    
    try:
        for gen in range(start_gen, generations + 1):
            fits, rets, step_counts = [], [], []
            sigma = get_sigma(gen, hall_fit)
            
            start_time = time.time()
            
            if use_parallel and pool:
                # Parallel evaluation with different seeds
                seeds = [np.random.randint(0, 100000) for _ in range(pop_size)]
                results = pool.map(evaluate_ant_worker, [(pop[i], seeds[i]) for i in range(pop_size)])
                
                for f, r, s in results:
                    fits.append(f)
                    rets.append(r)
                    step_counts.append(s)
            else:
                # Serial evaluation
                for i in range(pop_size):
                    f, r, s = evaluate_ant(env, reader, pop[i], seed=gen*pop_size + i)
                    fits.append(f)
                    rets.append(r)
                    step_counts.append(s)
            
            # Update hall of fame
            best_idx = np.argmax(fits)
            if fits[best_idx] > hall_fit:
                hall_fit = fits[best_idx]
                hall_best = pop[best_idx].copy()
                print(f"  >>> New Hall Best! Fitness={hall_fit:.1f} Return={rets[best_idx]:.1f} Steps={step_counts[best_idx]}")
            
            hall_history.append(hall_fit)
            
            # Stats
            best_ret = float(np.max(rets))
            mean_ret = float(np.mean(rets))
            mean_steps = float(np.mean(step_counts))
            duration = time.time() - start_time
            
            print(f"[Ant Gen {gen:4d}] Best={best_ret:7.1f} | Mean={mean_ret:7.1f} | Steps={mean_steps:.0f} | Sigma={sigma:.3f} | {duration:.1f}s")
            
            # Checkpoint every 10 generations
            if gen % 10 == 0:
                ckpt.save({
                    'gen': gen,
                    'pop': pop,
                    'hall_best': hall_best,
                    'hall_fit': hall_fit,
                    'hall_history': hall_history
                })
            
            # Evolution: Rank-based selection
            # Top 20% are elites
            n_elites = max(2, int(pop_size * 0.20))
            elite_indices = np.argsort(fits)[-n_elites:]
            elites = pop[elite_indices]
            
            # Always keep absolute best
            new_pop = [hall_best.copy()]
            
            # Mate elites with mutation
            while len(new_pop) < pop_size:
                # Tournament selection
                parent1 = elites[np.random.randint(len(elites))]
                parent2 = elites[np.random.randint(len(elites))]
                
                # Crossover (blend)
                alpha = np.random.uniform(0.3, 0.7)
                child = alpha * parent1 + (1 - alpha) * parent2
                
                # Mutation
                child += np.random.randn(reader.dim).astype(np.float32) * sigma
                
                new_pop.append(child)
            
            pop = np.stack(new_pop)
            
            # Diversity injection every 50 gens if stuck
            if gen % 50 == 0 and len(hall_history) > 50:
                recent_improvement = hall_history[-1] - hall_history[-50]
                if recent_improvement < 50:  # Less than 50 improvement in 50 gens
                    print("  >>> Injecting diversity! <<<")
                    # Replace bottom 20% with new random individuals
                    n_new = int(pop_size * 0.2)
                    for i in range(n_new):
                        pop[i] = reader.init_weights()

    except KeyboardInterrupt:
        print("\n!!! Interrupted. Progress Saved. !!!")
        ckpt.save({
            'gen': gen,
            'pop': pop,
            'hall_best': hall_best,
            'hall_fit': hall_fit,
            'hall_history': hall_history
        })
    except Exception as e:
        print(f"\n!!! CRASH: {e} !!!")
        import traceback
        traceback.print_exc()
    finally:
        if pool:
            pool.close()
            pool.join()
        env.close()
    
    return hall_best


if __name__ == "__main__":
    print("=== Deep Static MLP: Ant-v5 ===")
    print("Parameters: 3-layer (64-32), Xavier init, adaptive mutation")
    run_ant_evolution(pop_size=256, use_parallel=True, n_workers=8)