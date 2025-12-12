import gymnasium as gym
import numpy as np

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
# Speciation Static Agent: Maintains diverse sub-populations
# ---------------------------------------------------------------------

class SpeciatedStaticReader:
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


def compute_distance(vec1, vec2):
    """Compute normalized distance between parameter vectors"""
    return float(np.linalg.norm(vec1 - vec2))


def assign_species(pop, fitnesses, species_threshold=3.0, max_species=8):
    """Assign individuals to species based on parameter similarity"""
    n = len(pop)
    species = [[] for _ in range(max_species)]
    species_reps = []  # Representative for each species
    
    for i in range(n):
        assigned = False
        # Try to assign to existing species
        for s_idx, rep in enumerate(species_reps):
            if compute_distance(pop[i], rep) < species_threshold:
                species[s_idx].append(i)
                assigned = True
                break
        
        # Create new species if needed
        if not assigned and len(species_reps) < max_species:
            species_reps.append(pop[i].copy())
            species[len(species_reps) - 1].append(i)
    
    # Clean up empty species
    species = [s for s in species if len(s) > 0]
    return species


def evaluate_cartpole_speciated(env, reader, static_vec, n_episodes=5):
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

def evaluate_pendulum_speciated(env, reader, static_vec, n_episodes=5):
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

def run_cartpole_speciated(pop_size=64, generations=40, species_threshold=3.0):
    # 1. Setup Checkpoint Name
    ckpt = CheckpointManager("ckpt_speciated_cartpole.pkl") 
    
    env = gym.make("CartPole-v1")
    # 2. Initialize Specific Reader
    reader = SpeciatedStaticReader(env.observation_space.shape[0], env.action_space)
    
    # 3. Load or Init
    state = ckpt.load()
    if state:
        print(f"\n>>> Resuming from Gen {state['gen']} <<<")
        pop = state['pop']
        start_gen = state['gen'] + 1
        hall_best = state['hall_best']
        hall_fit = state['hall_fit']
    else:
        print("\n>>> Starting New Run <<<")
        pop = np.random.randn(pop_size, reader.dim).astype(np.float32) * 0.5
        start_gen = 1
        hall_best = None
        hall_fit = -np.inf

    try:
        for gen in range(start_gen, generations + 1):
            fits, rets = [], []
            
            # 4. Evaluation Loop
            for i in range(pop_size):
                # CHANGE THIS LINE FOR MLP / ENSEMBLE FILES:
                f, r = evaluate_cartpole_speciated(env, reader, pop[i]) 
                
                fits.append(f)
                rets.append(r)
                if f > hall_fit:
                    hall_fit = f
                    hall_best = pop[i].copy()

            # --- Speciation Logic (Only for Speciated File) ---
            species = assign_species(pop, fits, species_threshold)
            best_ret = float(np.max(rets))
            mean_ret = float(np.mean(rets))
            print(f"[Speciated Gen {gen:3d}] BestRet={best_ret:7.1f} MeanRet={mean_ret:7.1f} Species={len(species)}")
            
            # --- Save State ---
            ckpt.save({'gen': gen, 'pop': pop, 'hall_best': hall_best, 'hall_fit': hall_fit})

            # --- Reproduction (Keep your original logic here) ---
            new_pop = []
            for species_indices in species:
                if len(species_indices) == 0: continue
                species_fits = [fits[i] for i in species_indices]
                species_size = max(2, int(pop_size * len(species_indices) / len(pop)))
                species_pop = pop[species_indices]
                species_elite_count = max(1, len(species_indices) // 5)
                elite_indices = np.argsort(species_fits)[-species_elite_count:]
                elites = species_pop[elite_indices]
                for _ in range(species_size):
                    parent = elites[np.random.randint(len(elites))]
                    child = parent + np.random.randn(reader.dim).astype(np.float32) * 0.5
                    child = np.clip(child, -10, 10)
                    new_pop.append(child)
            while len(new_pop) < pop_size:
                new_pop.append(np.random.randn(reader.dim).astype(np.float32) * 0.5)
            pop = np.stack(new_pop[:pop_size])
            # --------------------------------------------------

    except KeyboardInterrupt:
        print("\n!!! Interrupted. Saved. !!!")
    except Exception as e:
        print(f"\n!!! Crash: {e} !!!")
        raise
    finally:
        env.close()
    return hall_best

def run_pendulum_speciated(pop_size=64, generations=40, species_threshold=3.0):
    # 1. Setup Checkpoint Name
    ckpt = CheckpointManager("ckpt_speciated_pendulum.pkl") 
    
    env = gym.make("Pendulum-v1")
    # 2. Initialize Specific Reader
    reader = SpeciatedStaticReader(env.observation_space.shape[0], env.action_space)
    
    # 3. Load or Init
    state = ckpt.load()
    if state:
        print(f"\n>>> Resuming from Gen {state['gen']} <<<")
        pop = state['pop']
        start_gen = state['gen'] + 1
        hall_best = state['hall_best']
        hall_fit = state['hall_fit']
    else:
        print("\n>>> Starting New Run <<<")
        pop = np.random.randn(pop_size, reader.dim).astype(np.float32) * 0.5
        start_gen = 1
        hall_best = None
        hall_fit = -np.inf

    try:
        for gen in range(start_gen, generations + 1):
            fits, rets = [], []
            
            # 4. Evaluation Loop
            for i in range(pop_size):
                # CHANGE THIS LINE FOR MLP / ENSEMBLE FILES:
                f, r = evaluate_pendulum_speciated(env, reader, pop[i]) 
                
                fits.append(f)
                rets.append(r)
                if f > hall_fit:
                    hall_fit = f
                    hall_best = pop[i].copy()

            # --- Speciation Logic (Only for Speciated File) ---
            species = assign_species(pop, fits, species_threshold)
            best_ret = float(np.max(rets))
            mean_ret = float(np.mean(rets))
            print(f"[Speciated Gen {gen:3d}] BestRet={best_ret:7.1f} MeanRet={mean_ret:7.1f} Species={len(species)}")
            
            # --- Save State ---
            ckpt.save({'gen': gen, 'pop': pop, 'hall_best': hall_best, 'hall_fit': hall_fit})

            # --- Reproduction (Keep your original logic here) ---
            new_pop = []
            for species_indices in species:
                if len(species_indices) == 0: continue
                species_fits = [fits[i] for i in species_indices]
                species_size = max(2, int(pop_size * len(species_indices) / len(pop)))
                species_pop = pop[species_indices]
                species_elite_count = max(1, len(species_indices) // 5)
                elite_indices = np.argsort(species_fits)[-species_elite_count:]
                elites = species_pop[elite_indices]
                for _ in range(species_size):
                    parent = elites[np.random.randint(len(elites))]
                    child = parent + np.random.randn(reader.dim).astype(np.float32) * 0.5
                    child = np.clip(child, -10, 10)
                    new_pop.append(child)
            while len(new_pop) < pop_size:
                new_pop.append(np.random.randn(reader.dim).astype(np.float32) * 0.5)
            pop = np.stack(new_pop[:pop_size])
            # --------------------------------------------------

    except KeyboardInterrupt:
        print("\n!!! Interrupted. Saved. !!!")
    except Exception as e:
        print(f"\n!!! Crash: {e} !!!")
        raise
    finally:
        env.close()
    return hall_best


if __name__ == "__main__":
    print("=== Speciated Static Agent: Niching for Diversity ===")
    print("\n[CartPole with Speciation]")
    best_cp = run_cartpole_speciated()
    print("\n[Pendulum with Speciation]")
    best_pend = run_pendulum_speciated()
    print("\nDone!")
