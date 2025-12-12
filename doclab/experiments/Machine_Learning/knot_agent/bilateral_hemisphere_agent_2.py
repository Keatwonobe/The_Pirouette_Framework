import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal
import pickle
import os
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
        """Extract all parameters as flat numpy array"""
        return torch.cat([p.data.view(-1) for p in self.parameters()]).cpu().numpy()
    
    def set_flat_params(self, flat_params):
        """Load flat numpy array into parameters"""
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
    # Render mode None for speed
    try:
        _worker_env = gym.make("Ant-v4", terminate_when_unhealthy=True, render_mode=None)
        _worker_env.reset()
    except:
        pass

def worker_eval(args):
    """Evaluate static weight vector"""
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
    
    # Fitness shaping for stability
    fitness = total_reward
    if steps < 20: fitness -= 500
    elif steps < 100: fitness -= 100
    fitness += steps * 0.2
    
    return fitness, steps

class LeftHemisphere:
    """Static Evolution: explores weight space geometrically"""
    def __init__(self, policy_template, pop_size=128):
        self.policy = policy_template
        self.dim = len(policy_template.get_flat_params())
        self.pop_size = pop_size
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
        """Run one generation"""
        self.gen += 1
        sigma = 0.02 if self.gen > 100 else 0.1
        if self.best_fitness < 50: sigma = 0.2
        
        seeds = [self.gen * self.pop_size + i for i in range(self.pop_size)]
        args = [(self.pop[i], seeds[i]) for i in range(self.pop_size)]
        results = self.pool.map(worker_eval, args)
        
        fits = np.array([r[0] for r in results])
        steps = np.array([r[1] for r in results])
        
        best_idx = np.argmax(fits)
        if fits[best_idx] > self.best_fitness:
            self.best_fitness = fits[best_idx]
            self.best_params = self.pop[best_idx].copy()
        
        self.fitness_history.append(self.best_fitness)
        
        # Elitism + Mutation
        n_elites = max(4, int(self.pop_size * 0.15))
        elite_indices = np.argsort(fits)[-n_elites:]
        elites = self.pop[elite_indices]
        
        new_pop = [self.best_params.copy()]
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
            'mean_fitness': np.mean(fits),
            'mean_steps': np.mean(steps),
            'is_plateau': self.is_plateau()
        }
    
    def inject_genome(self, params):
        """Inject a refined genome back into the population (Lamarckian Evolution)"""
        # Replace the first few slots with the RL-refined version and mutated copies
        self.pop[0] = params.copy()
        self.pop[1] = params.copy()
        # Add a slightly mutated version to encourage local exploration around the new peak
        self.pop[2] = params + np.random.randn(self.dim).astype(np.float32) * 0.01
        
        # Update best_params so we don't lose this progress
        self.best_params = params.copy()
        # We reset best_fitness to force re-evaluation
        # self.best_fitness = -np.inf 

    def is_plateau(self):
        if len(self.fitness_history) < 20: return False
        return (self.fitness_history[-1] - self.fitness_history[0]) < 15
    
    def get_best_policy(self):
        return self.best_params
    
    def cleanup(self):
        self.pool.close()
        self.pool.join()

# ============================================================================
# RIGHT HEMISPHERE: PPO REFINEMENT
# ============================================================================
class RightHemisphere:
    """PPO: gradient-based refinement"""
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
        # We reset the optimizer to allow fresh adaptation
        self.policy_optimizer = optim.Adam(self.policy.parameters(), lr=3e-4)
        
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
                # Exploration noise
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
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        for _ in range(epochs):
            action_pred = self.policy(states)
            # Simple Gaussian Loss for PPO (assuming fixed std dev for simplicity in this hybrid)
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
        self.left = LeftHemisphere(self.policy_template, pop_size=128)
        # We initialize Right Hemisphere but only use it in the loop
        self.right = RightHemisphere(self.policy_template)
        self.env = gym.make("Ant-v4", terminate_when_unhealthy=True)
        
    def run_interleaved(self, cycles=50, gens_per_cycle=10, updates_per_cycle=5):
        """
        INTERLEAVED MODE:
        Running 'Left' (Evolution) and 'Right' (RL) in a tight loop.
        Weights are passed back and forth to maximize training signal.
        """
        print("=" * 60)
        print("BILATERAL AGENT: INTERLEAVED TRAINING (Hybrid Mode)")
        print("Left (Static) provides Exploration | Right (RL) provides Exploitation")
        print("=" * 60)
        
        total_gens = 0
        
        for cycle in range(1, cycles + 1):
            print(f"\n>>> CYCLE {cycle}/{cycles} <<<")
            
            # --- PHASE 1: EVOLUTION (Global Search) ---
            print(f"--- Left Hemisphere: Evolving for {gens_per_cycle} gens ---")
            best_gen_fit = -np.inf
            
            for g in range(gens_per_cycle):
                result = self.left.step()
                total_gens += 1
                best_gen_fit = result['best_fitness']
                
                if total_gens % 5 == 0:
                     print(f"  [L-Gen {total_gens}] Best={result['best_fitness']:6.1f} | "
                           f"Mean={result['mean_fitness']:6.1f} | Steps={result['mean_steps']:4.0f}")

            # Transfer Best Static -> PPO
            print(f"  > Transferring Best Static Policy (Fit: {best_gen_fit:.1f}) to Right Hemisphere...")
            best_static = self.left.get_best_policy()
            self.right.load_from_static(best_static)
            
            # --- PHASE 2: PPO LEARNING (Local Refinement) ---
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
    # Run in Interleaved mode to "double the training"
    agent.run_interleaved(cycles=20, gens_per_cycle=10, updates_per_cycle=5)