import gymnasium as gym
import numpy as np
import os
import pickle
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
# Heavy MLP Reader (Scaled for Ant)
# ---------------------------------------------------------------------
class HeavyMLPReader:
    def __init__(self, obs_dim, action_space, hidden_size=64):
        self.obs_dim = obs_dim
        self.action_space = action_space
        self.hidden_size = hidden_size

        # Ant is Continuous
        assert isinstance(action_space, gym.spaces.Box)
        self.n_actions = action_space.shape[0]
        
        # Layer 1: obs -> hidden
        self.l1_size = hidden_size * (obs_dim + 1)
        # Layer 2: hidden -> action
        self.l2_size = self.n_actions * (hidden_size + 1)
        
        self.dim = self.l1_size + self.l2_size
        self.max_action = float(action_space.high[0])

    def act(self, static_vec, obs):
        # Fast strict type casting
        obs = np.asarray(obs, dtype=np.float32)
        
        # --- Layer 1 ---
        w1_end = self.hidden_size * self.obs_dim
        w1 = static_vec[:w1_end].reshape(self.hidden_size, self.obs_dim)
        b1 = static_vec[w1_end:self.l1_size]
        
        h = np.tanh(w1 @ obs + b1) # Tanh activation
        
        # --- Layer 2 ---
        remaining = static_vec[self.l1_size:]
        w2_end = self.n_actions * self.hidden_size
        w2 = remaining[:w2_end].reshape(self.n_actions, self.hidden_size)
        b2 = remaining[w2_end:]
        
        # Final output scaled to action space
        action = np.tanh(w2 @ h + b2) * self.max_action
        return action

def evaluate_ant(env, reader, static_vec):
    """
    Ant evaluation is expensive. We return:
    fitness: A score that penalizes dying early heavily.
    true_return: The actual gym reward.
    """
    try:
        obs, _ = env.reset()
    except:
        return -1000.0, 0.0

    total_reward = 0.0
    steps = 0
    # Limit steps to 1000 to speed up generations (Gym default is 1000 anyway)
    max_steps = 1000 
    
    for _ in range(max_steps):
        action = reader.act(static_vec, obs)
        try:
            obs, reward, terminated, truncated, _ = env.step(action)
        except Exception:
            # Simulation exploded
            return -1000.0, total_reward
        
        total_reward += reward
        steps += 1
        
        if terminated or truncated:
            break
            
    # Fitness shaping:
    # If it dies instantly (steps < 20), punish it.
    # If it survives, reward it.
    fitness = total_reward
    if steps < 20:
        fitness -= 500 # Heavy penalty for instant death
        
    return fitness, total_reward

def run_ant_evolution(pop_size=128, generations=1000, hidden_size=64):
    ckpt = CheckpointManager("ckpt_ant_heavy_2.pkl")
    
    # Create Environment
    try:
        env = gym.make("Ant-v5", terminate_when_unhealthy=True)
    except Exception as e:
        print(f"Error: Could not make Ant-v4. Do you have mujoco installed? ({e})")
        return

    reader = HeavyMLPReader(env.observation_space.shape[0], env.action_space, hidden_size)
    
    # Mutation Schedule: Start chaotic, end precise
    def get_sigma(gen):
        if gen < 50: return 0.5   # Exploration Phase
        if gen < 150: return 0.1  # Refinement Phase
        return 0.02               # Polishing Phase

    # Load or Init
    state = ckpt.load()
    if state:
        print(f"\n>>> Resuming Ant (Hidden={hidden_size}) from Gen {state['gen']} <<<")
        pop = state['pop']
        start_gen = state['gen'] + 1
        hall_best = state['hall_best']
        hall_fit = state['hall_fit']
    else:
        print(f"\n>>> Starting New Ant Run (Params: {reader.dim}) <<<")
        # Initialize with smaller variance to avoid exploding physics immediately
        pop = np.random.randn(pop_size, reader.dim).astype(np.float32) * 0.1
        start_gen = 1
        hall_best = None
        hall_fit = -np.inf

    try:
        for gen in range(start_gen, generations + 1):
            fits, rets = [], []
            sigma = get_sigma(gen)
            
            # --- Parallel Evaluation Hint ---
            # In a real scenario, you would parallelize this loop. 
            # For now, we keep it serial but it will be slower than CartPole.
            start_time = time.time()
            for i in range(pop_size):
                f, r = evaluate_ant(env, reader, pop[i])
                fits.append(f)
                rets.append(r)
                
                if f > hall_fit:
                    hall_fit = f
                    hall_best = pop[i].copy()
                    print(f"  > New Best! {hall_fit:.1f}")

            # Stats
            best_ret = float(np.max(rets))
            mean_ret = float(np.mean(rets))
            duration = time.time() - start_time
            
            print(f"[Ant Gen {gen:4d}] Best={best_ret:6.1f} | Mean={mean_ret:6.1f} | Sigma={sigma:.2f} | Time={duration:.1f}s")
            
            # Checkpoint
            ckpt.save({'gen': gen, 'pop': pop, 'hall_best': hall_best, 'hall_fit': hall_fit})

            # --- Evolution (Truncation Selection) ---
            # Keep top 10% (Elites)
            n_elites = max(2, int(pop_size * 0.10))
            elite_indices = np.argsort(fits)[-n_elites:]
            elites = pop[elite_indices]
            
            new_pop = [elites[-1]] # Always keep absolute best unchanged
            
            while len(new_pop) < pop_size:
                # Pick random elite parent
                parent = elites[np.random.randint(len(elites))]
                # Mutate
                child = parent + np.random.randn(reader.dim).astype(np.float32) * sigma
                new_pop.append(child)
                
            pop = np.stack(new_pop)

    except KeyboardInterrupt:
        print("\n!!! Interrupted. Saved. !!!")
    except Exception as e:
        print(f"\n!!! CRASH: {e} !!!")
        raise
    finally:
        env.close()
    return hall_best

if __name__ == "__main__":
    # Note: Ant requires 'gymnasium[mujoco]'
    print("=== Heavy Static MLP: Ant-v4 ===")
    run_ant_evolution()