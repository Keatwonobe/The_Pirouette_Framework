import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
from multiprocessing import Pool, cpu_count
import time

# ============================================================================
# SHARED ARCHITECTURE
# ============================================================================
class SharedPolicy(nn.Module):
    """64->32 MLP used by both hemispheres"""
    def __init__(self, obs_dim=27, act_dim=8, h1=64, h2=32):
        super().__init__()
        self.fc1 = nn.Linear(obs_dim, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.fc3 = nn.Linear(h2, act_dim)
        
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
# LEFT HEMISPHERE: STATIC EVOLUTION
# ============================================================================
_worker_env = None

def worker_init():
    global _worker_env
    import warnings
    warnings.filterwarnings("ignore")
    try:
        # render_mode=None for speed
        _worker_env = gym.make("Ant-v5", terminate_when_unhealthy=True, render_mode=None)
        _worker_env.reset()
    except:
        pass

def worker_eval(args):
    """Evaluate static weight vector with Physics Sanity Checks"""
    static_vec, seed = args
    global _worker_env
    if _worker_env is None:
        return -1000.0, 0
    
    policy = SharedPolicy()
    policy.set_flat_params(static_vec)
    
    try:
        obs, _ = _worker_env.reset(seed=seed)
        total_reward = 0.0
        steps = 0
        
        for _ in range(1000):
            with torch.no_grad():
                obs_t = torch.FloatTensor(obs)
                action = policy(obs_t).numpy()
            
            obs, reward, terminated, truncated, _ = _worker_env.step(action)
            total_reward += reward
            steps += 1
            
            if terminated or truncated:
                break
                
    except Exception:
        return -1000.0, 0
    
    # --- FITNESS SHAPING & MASKING ---
    fitness = total_reward
    
    # 1. MASK: Minimum Survival Requirement
    # We discount the score of any agent that didn't survive at least 300 steps.
    # This filters out "Physics Explosions" (glitches that give huge velocity in 5 frames).
    if steps < 300:
        # Heavy penalty ensures these are never selected as "Best"
        fitness = -500.0 + steps 
    else:
        # Bonus for stable walking (surviving long)
        fitness += steps * 0.1

    return fitness, steps

class LeftHemisphere:
    def __init__(self, policy_template, pop_size=128, warmup_gens=20):
        self.policy = policy_template
        self.dim = len(policy_template.get_flat_params())
        self.pop_size = pop_size
        self.warmup_gens = warmup_gens
        
        self.pop = self._init_population()
        self.best_fitness = -np.inf
        self.best_params = None
        self.gen = 0
        self.fitness_history = deque(maxlen=20)
        
        n_workers = max(1, cpu_count() - 2)
        self.pool = Pool(processes=n_workers, initializer=worker_init, maxtasksperchild=20)
        
    def _init_population(self):
        pop = []
        for _ in range(self.pop_size):
            params = self.policy.get_flat_params()
            params = np.random.randn(len(params)) * 0.1
            pop.append(params.astype(np.float32))
        return np.stack(pop)
    
    def step(self):
        self.gen += 1
        
        # Adaptive Sigma: Higher during warmup
        sigma = 0.02 if self.gen > 100 else 0.1
        if self.gen < self.warmup_gens:
            sigma = 0.15  # Encourage exploration during warmup
            
        seeds = [self.gen * self.pop_size + i for i in range(self.pop_size)]
        args = [(self.pop[i], seeds[i]) for i in range(self.pop_size)]
        results = self.pool.map(worker_eval, args)
        
        fits = np.array([r[0] for r in results])
        steps = np.array([r[1] for r in results])
        
        # --- WARMUP LOGIC ---
        # Only record a new "Hall of Fame" Best if we are past warmup.
        # This prevents locking onto early lucky glitches.
        best_idx = np.argmax(fits)
        current_best_fit = fits[best_idx]
        
        record_best = False
        if self.gen >= self.warmup_gens:
            if current_best_fit > self.best_fitness:
                self.best_fitness = current_best_fit
                self.best_params = self.pop[best_idx].copy()
                record_best = True
        else:
            # During warmup, we track it internally but don't lock it permanently
            # just in case the next gen is better.
            if current_best_fit > self.best_fitness:
                self.best_fitness = current_best_fit
                self.best_params = self.pop[best_idx].copy()

        self.fitness_history.append(np.mean(fits)) # Track mean for plateau detection
        
        # Selection
        n_elites = max(4, int(self.pop_size * 0.15))
        elite_indices = np.argsort(fits)[-n_elites:]
        elites = self.pop[elite_indices]
        
        new_pop = []
        
        # If we have a stored best, keep it
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
        """Inject RL-refined genome back into population"""
        # Replace the elites with the RL version
        for i in range(5):
            self.pop[i] = params.copy()
            if i > 0: # Add noise to copies
                self.pop[i] += np.random.randn(self.dim).astype(np.float32) * 0.05
        
        # Crucial: We update best_params so evolution builds on it
        self.best_params = params.copy()
        # But we slightly lower best_fitness to ensure it has to re-prove itself
        # or at least allows new mutations to compete
        # self.best_fitness = -1000 # Force re-evaluation logic to take over

    def get_best_policy(self):
        return self.best_params if self.best_params is not None else self.pop[0]
    
    def cleanup(self):
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
            nn.Linear(27, 64), nn.Tanh(),
            nn.Linear(64, 32), nn.Tanh(),
            nn.Linear(32, 1)
        )
        
        self.policy_optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        self.value_optimizer = optim.Adam(self.value_net.parameters(), lr=lr)
        self.episode_rewards = deque(maxlen=20)
        
    def load_from_static(self, static_params):
        self.policy.set_flat_params(static_params)
        # Reset optimizer to adapt to new landscape
        self.policy_optimizer = optim.Adam(self.policy.parameters(), lr=2e-4)
        
    def get_policy_params(self):
        return self.policy.get_flat_params()
        
    def collect_rollout(self, env, n_steps=2048):
        states, actions, rewards, values, log_probs, dones = [], [], [], [], [], []
        obs, _ = env.reset()
        ep_rew = 0
        
        for _ in range(n_steps):
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
        
        return {
            'states': np.array(states), 'actions': np.array(actions),
            'rewards': np.array(rewards), 'values': np.array(values),
            'dones': np.array(dones)
        }
    
    def compute_gae(self, rewards, values, dones, gamma=0.99, lam=0.95):
        advantages = np.zeros_like(rewards)
        last_gae = 0
        for t in reversed(range(len(rewards))):
            next_val = 0 if t == len(rewards)-1 else values[t+1]
            delta = rewards[t] + gamma * next_val * (1-dones[t]) - values[t]
            advantages[t] = last_gae = delta + gamma * lam * (1-dones[t]) * last_gae
        return advantages, advantages + values
    
    def update(self, rollout, epochs=4):
        states = torch.FloatTensor(rollout['states'])
        actions = torch.FloatTensor(rollout['actions'])
        old_values = rollout['values']
        rewards = rollout['rewards']
        dones = rollout['dones']
        
        advantages, returns = self.compute_gae(rewards, old_values, dones)
        advantages = torch.FloatTensor(advantages)
        returns = torch.FloatTensor(returns)
        if advantages.std() > 1e-8:
            advantages = (advantages - advantages.mean()) / advantages.std()
        
        for _ in range(epochs):
            action_pred = self.policy(states)
            log_probs = -0.5 * ((action_pred - actions) ** 2).sum(dim=1)
            
            values_pred = self.value_net(states).squeeze()
            value_loss = ((values_pred - returns) ** 2).mean()
            policy_loss = -(log_probs * advantages).mean()
            
            self.policy_optimizer.zero_grad()
            policy_loss.backward()
            self.policy_optimizer.step()
            
            self.value_optimizer.zero_grad()
            value_loss.backward()
            self.value_optimizer.step()

    def step(self, env):
        rollout = self.collect_rollout(env, n_steps=1024)
        self.update(rollout)
        mean_rew = np.mean(self.episode_rewards) if self.episode_rewards else 0
        return {'mean_reward': mean_rew}

# ============================================================================
# BILATERAL COORDINATOR
# ============================================================================
class BilateralAgent:
    def __init__(self):
        self.policy_template = SharedPolicy()
        # Warmup set to 20 generations to avoid early glitch-locking
        self.left = LeftHemisphere(self.policy_template, pop_size=128, warmup_gens=20)
        self.right = RightHemisphere(self.policy_template)
        self.env = gym.make("Ant-v4", terminate_when_unhealthy=True)
        
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

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method('spawn', force=True)
    
    agent = BilateralAgent()
    agent.run_interleaved(cycles=20, gens_per_cycle=10, updates_per_cycle=5)