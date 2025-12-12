import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
from multiprocessing import Pool, cpu_count
import time

# ============================================================================
# SHARED ARCHITECTURE DEFINITIONS
# ============================================================================
OBS_DIM = 27
ACT_DIM = 8
H1 = 64
H2 = 32

class SharedPolicy(nn.Module):
    """
    PyTorch Version (Right Hemisphere).
    """
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(OBS_DIM, H1)
        self.fc2 = nn.Linear(H1, H2)
        self.fc3 = nn.Linear(H2, ACT_DIM)
        
    def forward(self, x):
        x = torch.tanh(self.fc1(x))
        x = torch.tanh(self.fc2(x))
        return torch.tanh(self.fc3(x))
    
    def get_flat_params(self):
        return torch.cat([p.data.view(-1) for p in self.parameters()]).cpu().numpy()
    
    def set_flat_params(self, flat_params):
        params = torch.from_numpy(flat_params).float()
        offset = 0
        for p in self.parameters():
            numel = p.numel()
            p.data.copy_(params[offset:offset+numel].view_as(p))
            offset += numel

# ============================================================================
# LEFT HEMISPHERE: STATIC EVOLUTION (PURE NUMPY WORKERS)
# ============================================================================
_worker_env = None

def worker_init():
    """
    Initializes the worker environment.
    NO PyTorch imports here to prevent Windows Deadlocks.
    """
    global _worker_env
    import warnings
    warnings.filterwarnings("ignore")
    try:
        _worker_env = gym.make("Ant-v5", terminate_when_unhealthy=True, render_mode=None)
        _worker_env.reset()
    except Exception as e:
        print(f"!!! WORKER INIT FAILED: {e}")

def worker_eval(args):
    """
    Evaluates agent 5 times to validate score.
    """
    static_vec, seed = args
    global _worker_env
    
    if _worker_env is None:
        return -1000.0, 0
    
    # --- UNPACK WEIGHTS ---
    idx = 0
    w1_size = H1 * OBS_DIM
    w1 = static_vec[idx : idx + w1_size].reshape(H1, OBS_DIM)
    idx += w1_size
    b1_size = H1
    b1 = static_vec[idx : idx + b1_size]
    idx += b1_size
    w2_size = H2 * H1
    w2 = static_vec[idx : idx + w2_size].reshape(H2, H1)
    idx += w2_size
    b2_size = H2
    b2 = static_vec[idx : idx + b2_size]
    idx += b2_size
    w3_size = ACT_DIM * H2
    w3 = static_vec[idx : idx + w3_size].reshape(ACT_DIM, H2)
    idx += w3_size
    b3 = static_vec[idx:]
    
    # --- ROBUST EVALUATION LOOP ---
    n_evals = 5
    fit_sum = 0.0
    steps_sum = 0.0
    
    for i in range(n_evals):
        try:
            # Vary seed slightly for each run to test robustness
            run_seed = seed + (i * 1000)
            obs, _ = _worker_env.reset(seed=run_seed)
            total_reward = 0.0
            steps = 0
            
            for _ in range(1000):
                obs = np.asarray(obs, dtype=np.float32)
                
                # Numpy Forward Pass
                z1 = np.tanh(w1 @ obs + b1)
                z2 = np.tanh(w2 @ z1 + b2)
                action = np.tanh(w3 @ z2 + b3)
                
                obs, reward, terminated, truncated, _ = _worker_env.step(action)
                total_reward += reward
                steps += 1
                
                if terminated or truncated:
                    break
            
            # Per-Run Fitness Shaping
            fitness = total_reward
            # Mask: If it dies instantly (<300 steps) in ANY run, it gets penalized heavily
            if steps < 300:
                fitness = -500.0 + steps 
            else:
                fitness += steps * 0.1
            
            fit_sum += fitness
            steps_sum += steps

        except Exception:
            fit_sum += -1000.0
            steps_sum += 0
            
    return fit_sum / n_evals, steps_sum / n_evals

class LeftHemisphere:
    def __init__(self, policy_template, pop_size=128, warmup_gens=20, use_multiprocessing=True):
        self.policy = policy_template
        self.dim = len(policy_template.get_flat_params())
        self.pop_size = pop_size
        self.warmup_gens = warmup_gens

        self.pop = self._init_population()
        self.best_fitness = -np.inf
        self.best_params = None
        self.gen = 0
        self.fitness_history = deque(maxlen=20)

        self.use_multiprocessing = use_multiprocessing
        self.pool = None

        if self.use_multiprocessing:
            n_workers = max(1, cpu_count() - 2)
            print(f"Left Hemisphere initializing {n_workers} Numpy workers (5-Run Validation Mode)...")
            self.pool = Pool(
                processes=n_workers,
                initializer=worker_init,
                maxtasksperchild=20
            )
        else:
            print("Left Hemisphere running in SINGLE-PROCESS mode (no multiprocessing).")
        
    def _init_population(self):
        pop = []
        for _ in range(self.pop_size):
            params = self.policy.get_flat_params()
            params = np.random.randn(len(params)) * 0.1
            pop.append(params.astype(np.float32))
        return np.stack(pop)
    
    def step(self):
        self.gen += 1
        
        sigma = 0.02 if self.gen > 100 else 0.1
        if self.gen < self.warmup_gens: sigma = 0.15
        
        seeds = [self.gen * self.pop_size + i for i in range(self.pop_size)]
        args = [(self.pop[i], seeds[i]) for i in range(self.pop_size)]
        
        # ---- HERE: choose multi vs single process ----
        if self.use_multiprocessing and self.pool is not None:
            results = self.pool.map(worker_eval, args)
        else:
            results = [worker_eval(a) for a in args]

        fits = np.array([r[0] for r in results])
        steps = np.array([r[1] for r in results])
        # Map to workers (each runs 5 times now)
        results = self.pool.map(worker_eval, args)
        
        fits = np.array([r[0] for r in results])
        steps = np.array([r[1] for r in results])
        
        best_idx = np.argmax(fits)
        current_best_fit = fits[best_idx]
        
        if self.gen >= self.warmup_gens:
            if current_best_fit > self.best_fitness:
                self.best_fitness = current_best_fit
                self.best_params = self.pop[best_idx].copy()
        else:
            if current_best_fit > self.best_fitness:
                self.best_fitness = current_best_fit
                self.best_params = self.pop[best_idx].copy()

        n_elites = max(4, int(self.pop_size * 0.15))
        elite_indices = np.argsort(fits)[-n_elites:]
        elites = self.pop[elite_indices]
        
        new_pop = []
        if self.best_params is not None:
            new_pop.append(self.best_params.copy())
            
        while len(new_pop) < self.pop_size:
            p1 = elites[np.random.randint(len(elites))]
            p2 = elites[np.random.randint(len(elites))]
            mask = np.random.rand(self.dim) > 0.5
            child = np.where(mask, p1, p2)
            child += np.random.randn(self.dim).astype(np.float32) * sigma
            new_pop.append(child)
        
        self.pop = np.stack(new_pop)
        
        return {
            'best_fitness': self.best_fitness,
            'current_best': current_best_fit,
            'mean_fitness': np.mean(fits),
            'mean_steps': np.mean(steps),
            'is_warmup': self.gen < self.warmup_gens
        }
    
    def inject_genome(self, params):
        for i in range(10): 
            self.pop[i] = params.copy()
            if i > 0: self.pop[i] += np.random.randn(self.dim) * 0.05
        self.best_params = params.copy()

    def get_best_policy(self):
        return self.best_params if self.best_params is not None else self.pop[0]
    
    def cleanup(self):
        if self.pool is not None:
            self.pool.close()
            self.pool.join()


# ============================================================================
# RIGHT HEMISPHERE: PPO REFINEMENT
# ============================================================================
class RightHemisphere:
    def __init__(self, policy_template, lr=3e-4):
        self.policy = SharedPolicy()
        self.policy.load_state_dict(policy_template.state_dict())
        
        self.value_net = nn.Sequential(
            nn.Linear(OBS_DIM, 64), nn.Tanh(),
            nn.Linear(64, 32), nn.Tanh(),
            nn.Linear(32, 1)
        )
        
        self.policy_optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        self.value_optimizer = optim.Adam(self.value_net.parameters(), lr=lr)
        self.episode_rewards = deque(maxlen=20)
        
    def load_from_static(self, static_params):
        self.policy.set_flat_params(static_params)
        self.policy_optimizer = optim.Adam(self.policy.parameters(), lr=1e-4)
        
    def get_policy_params(self):
        return self.policy.get_flat_params()
        
    def step(self, env):
        states, actions, rewards, values, dones = [], [], [], [], []
        obs, _ = env.reset()
        ep_rew = 0
        
        for _ in range(2048):
            state_t = torch.FloatTensor(obs).unsqueeze(0)
            with torch.no_grad():
                action = self.policy(state_t)
                value = self.value_net(state_t)
                action = action + torch.randn_like(action) * 0.2
                action = torch.clamp(action, -1, 1)
            
            states.append(obs)
            actions.append(action.squeeze().numpy())
            values.append(value.item())
            
            obs, reward, terminated, truncated, _ = env.step(action.squeeze().numpy())
            ep_rew += reward
            rewards.append(reward)
            dones.append(terminated or truncated)
            
            if terminated or truncated:
                self.episode_rewards.append(ep_rew)
                obs, _ = env.reset()
                ep_rew = 0
                
        states = torch.FloatTensor(np.array(states))
        actions = torch.FloatTensor(np.array(actions))
        old_values = np.array(values)
        rewards = np.array(rewards)
        
        # PPO Update (Simplified)
        advantages = np.zeros_like(rewards)
        last_gae = 0
        gamma, lam = 0.99, 0.95
        for t in reversed(range(len(rewards))):
            next_val = 0 if t == len(rewards)-1 else old_values[t+1]
            delta = rewards[t] + gamma * next_val * (1-dones[t]) - old_values[t]
            advantages[t] = last_gae = delta + gamma * lam * (1-dones[t]) * last_gae
            
        advantages = torch.FloatTensor(advantages)
        returns = advantages + torch.FloatTensor(old_values)
        if advantages.std() > 1e-8:
            advantages = (advantages - advantages.mean()) / advantages.std()
            
        for _ in range(4):
            action_pred = self.policy(states)
            log_probs = -0.5 * ((action_pred - actions) ** 2).sum(dim=1)
            values_pred = self.value_net(states).squeeze()
            
            policy_loss = -(log_probs * advantages).mean()
            value_loss = ((values_pred - returns) ** 2).mean()
            
            self.policy_optimizer.zero_grad()
            policy_loss.backward()
            self.policy_optimizer.step()
            
            self.value_optimizer.zero_grad()
            value_loss.backward()
            self.value_optimizer.step()
            
        return {'mean_reward': np.mean(self.episode_rewards) if self.episode_rewards else 0}

# ============================================================================
# BILATERAL COORDINATOR
# ============================================================================
class BilateralAgent:
    def __init__(self):
        self.policy_template = SharedPolicy()
        # Warmup set to 20 generations to avoid early glitch-locking
        self.left = LeftHemisphere(self.policy_template, pop_size=128, warmup_gens=20)
        self.right = RightHemisphere(self.policy_template)
        self.env = gym.make("Ant-v5", terminate_when_unhealthy=True)
        
    def run_interleaved(self, cycles=50, gens_per_cycle=10, updates_per_cycle=5):
        print("=" * 60)
        print("BILATERAL AGENT: ROBUST INTERLEAVED TRAINING")
        print("Filters physics glitches & enforces warmup period")
        print("=" * 60)
        
        total_gens = 0
        
        for cycle in range(1, cycles + 1):
            print(f"\n>>> CYCLE {cycle}/{cycles} <<<")
            
            # --- PHASE 1: EVOLUTION ---
            # Force at least 20 gens in first cycle for warmup
            current_gens = 20 if cycle == 1 else gens_per_cycle
            
            print(f"--- Left Hemisphere: Evolving for {current_gens} gens ---")
            best_gen_fit = -np.inf
            
            for g in range(current_gens):
                result = self.left.step()
                total_gens += 1
                
                status = "WARMUP" if result['is_warmup'] else "ACTIVE"
                if total_gens % 5 == 0:
                     print(f"  [L-Gen {total_gens}] ({status}) "
                           f"Best={result['best_fitness']:6.1f} | "
                           f"Cur={result['current_best']:6.1f} | "
                           f"Steps={result['mean_steps']:4.0f}")

            best_static = self.left.get_best_policy()
            fit = self.left.best_fitness
            print(f"  > Transferring Valid Policy (Fit: {fit:.1f}) to Right Hemisphere...")
            
            self.right.load_from_static(best_static)
            
            # --- PHASE 2: PPO LEARNING ---
            print(f"--- Right Hemisphere: Refining for {updates_per_cycle} updates ---")
            last_ppo_reward = -np.inf
            
            for u in range(updates_per_cycle):
                result = self.right.step(self.env)
                last_ppo_reward = result['mean_reward']
                print(f"  [R-Update {u+1}] MeanReward={result['mean_reward']:.1f}")
            
            # Transfer Refined -> Static
            print(f"  > Injecting Refined Policy (Rew: {last_ppo_reward:.1f}) back into Left Hemisphere...")
            refined_params = self.right.get_policy_params()
            self.left.inject_genome(refined_params)
            
        self.cleanup()

    def cleanup(self):
        self.left.cleanup()
        self.env.close()

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method('spawn', force=True)

    # Use a single template and hemisphere pair
    template = SharedPolicy()

    # IMPORTANT: make sure env version matches worker env
    left = LeftHemisphere(template, pop_size=64, warmup_gens=20, use_multiprocessing=True)
    right = RightHemisphere(template)
    main_env = gym.make("Ant-v5", terminate_when_unhealthy=True)

    try:
        total_gens = 0
        cycles = 50
        for cycle in range(1, cycles + 1):
            print(f"\n>>> CYCLE {cycle}/{cycles} <<<")

            gens = 20 if cycle == 1 else 10
            print(f"--- Left Hemisphere (Evolution): {gens} gens ---")

            for g in range(gens):
                res = left.step()
                total_gens += 1
                tag = "WARMUP" if res['is_warmup'] else "ACTIVE"
                if total_gens % 5 == 0 or g == gens - 1:
                    print(
                        f"  [L-Gen {total_gens}] ({tag}) "
                        f"Best={res['best_fitness']:6.1f} | "
                        f"Cur={res['current_best']:6.1f} | "
                        f"Steps={res['mean_steps']:4.0f}"
                    )

            best_static = left.get_best_policy()
            print(f"  > Transferring Policy (Fit: {left.best_fitness:.1f}) to Right Hemisphere...")
            right.load_from_static(best_static)

            print(f"--- Right Hemisphere (PPO): 5 updates ---")
            last_rew = 0.0
            for u in range(5):
                res = right.step(main_env)
                last_rew = res['mean_reward']
                print(f"  [R-Update {u+1}] MeanReward={last_rew:.1f}")

            print(f"  > Injecting Refined Policy (Rew: {last_rew:.1f}) back into Left Hemisphere...")
            right_params = right.get_policy_params()
            left.inject_genome(right_params)

    except KeyboardInterrupt:
        print("\n!!! Interrupted !!!")
    finally:
        left.cleanup()
        main_env.close()
