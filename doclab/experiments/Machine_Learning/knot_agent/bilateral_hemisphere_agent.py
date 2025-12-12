"""
Bilateral Hemisphere Agent: Ant-v4
=====================================
Left Hemisphere (Static/Geometric): Finds coherent gaits through evolution
Right Hemisphere (PPO/Adaptive): Refines trajectories through gradient descent

The agent switches hemispheres when progress plateaus.
"""

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
# SHARED ARCHITECTURE (both hemispheres use same network shape)
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
# LEFT HEMISPHERE: STATIC EVOLUTION (Geometric Exploration)
# ============================================================================
_worker_env = None

def worker_init():
    global _worker_env
    import warnings
    warnings.filterwarnings("ignore")
    _worker_env = gym.make("Ant-v4", terminate_when_unhealthy=True, render_mode=None)
    _worker_env.reset()

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
    
    # Fitness shaping
    fitness = total_reward
    if steps < 20:
        fitness -= 500
    elif steps < 100:
        fitness -= 100
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
        """Initialize with He scaling"""
        pop = []
        for _ in range(self.pop_size):
            params = self.policy.get_flat_params()
            params = np.random.randn(len(params)) * 0.1  # Simple init
            pop.append(params.astype(np.float32))
        return np.stack(pop)
    
    def step(self):
        """Run one generation of evolution"""
        self.gen += 1
        
        # Adaptive sigma
        sigma = 0.02 if self.gen > 100 else 0.1
        if self.best_fitness < 50:
            sigma = 0.2  # Panic exploration
        
        # Evaluate population
        seeds = [self.gen * self.pop_size + i for i in range(self.pop_size)]
        args = [(self.pop[i], seeds[i]) for i in range(self.pop_size)]
        results = self.pool.map(worker_eval, args)
        
        fits = np.array([r[0] for r in results])
        steps = np.array([r[1] for r in results])
        
        # Update best
        best_idx = np.argmax(fits)
        if fits[best_idx] > self.best_fitness:
            self.best_fitness = fits[best_idx]
            self.best_params = self.pop[best_idx].copy()
        
        self.fitness_history.append(self.best_fitness)
        
        # Selection + Crossover + Mutation
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
        
        # Diversity injection if stuck
        if self.gen % 50 == 0 and len(self.fitness_history) == 20:
            improvement = self.fitness_history[-1] - self.fitness_history[0]
            if improvement < 10:
                n_fresh = int(self.pop_size * 0.25)
                for i in range(n_fresh):
                    self.pop[i] = np.random.randn(self.dim).astype(np.float32) * 0.1
        
        return {
            'best_fitness': self.best_fitness,
            'mean_fitness': np.mean(fits),
            'mean_steps': np.mean(steps),
            'is_plateau': self.is_plateau()
        }
    
    def is_plateau(self):
        """Detect if evolution has stalled"""
        if len(self.fitness_history) < 20:
            return False
        improvement = self.fitness_history[-1] - self.fitness_history[0]
        return improvement < 15  # Less than 15 point gain over 20 gens
    
    def get_best_policy(self):
        """Return best discovered parameters"""
        return self.best_params
    
    def cleanup(self):
        self.pool.close()
        self.pool.join()

# ============================================================================
# RIGHT HEMISPHERE: PPO (Gradient-Based Refinement)
# ============================================================================
class RightHemisphere:
    """PPO: refines policy through gradient descent"""
    def __init__(self, policy_template, lr=3e-4):
        self.policy = SharedPolicy()
        self.policy.load_state_dict(policy_template.state_dict())
        
        self.value_net = nn.Sequential(
            nn.Linear(27, 64),
            nn.Tanh(),
            nn.Linear(64, 32),
            nn.Tanh(),
            nn.Linear(32, 1)
        )
        
        self.policy_optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        self.value_optimizer = optim.Adam(self.value_net.parameters(), lr=lr)
        
        self.episode_rewards = deque(maxlen=20)
        self.steps_trained = 0
        
    def collect_rollout(self, env, n_steps=2048):
        """Collect experience"""
        states, actions, rewards, values, log_probs = [], [], [], [], []
        dones = []
        
        obs, _ = env.reset()
        episode_reward = 0
        
        for _ in range(n_steps):
            state_t = torch.FloatTensor(obs).unsqueeze(0)
            
            with torch.no_grad():
                action = self.policy(state_t)
                value = self.value_net(state_t)
                # Add exploration noise
                action = action + torch.randn_like(action) * 0.1
                action = torch.clamp(action, -1, 1)
            
            states.append(obs)
            actions.append(action.squeeze().numpy())
            values.append(value.item())
            
            obs, reward, terminated, truncated, _ = env.step(action.squeeze().numpy())
            episode_reward += reward
            
            rewards.append(reward)
            dones.append(terminated or truncated)
            
            if terminated or truncated:
                self.episode_rewards.append(episode_reward)
                obs, _ = env.reset()
                episode_reward = 0
        
        return {
            'states': np.array(states),
            'actions': np.array(actions),
            'rewards': np.array(rewards),
            'values': np.array(values),
            'dones': np.array(dones)
        }
    
    def compute_gae(self, rewards, values, dones, gamma=0.99, lam=0.95):
        """Compute Generalized Advantage Estimation"""
        advantages = np.zeros_like(rewards)
        last_gae = 0
        
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = 0
            else:
                next_value = values[t + 1]
            
            delta = rewards[t] + gamma * next_value * (1 - dones[t]) - values[t]
            advantages[t] = last_gae = delta + gamma * lam * (1 - dones[t]) * last_gae
        
        returns = advantages + values
        return advantages, returns
    
    def update(self, rollout, epochs=10, clip_eps=0.2):
        """PPO update"""
        states = torch.FloatTensor(rollout['states'])
        actions = torch.FloatTensor(rollout['actions'])
        old_values = rollout['values']
        rewards = rollout['rewards']
        dones = rollout['dones']
        
        advantages, returns = self.compute_gae(rewards, old_values, dones)
        advantages = torch.FloatTensor(advantages)
        returns = torch.FloatTensor(returns)
        
        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        for _ in range(epochs):
            # Policy loss
            action_pred = self.policy(states)
            log_probs = -0.5 * ((action_pred - actions) ** 2).sum(dim=1)
            
            # Value loss
            values_pred = self.value_net(states).squeeze()
            value_loss = ((values_pred - returns) ** 2).mean()
            
            # Policy gradient with PPO clipping
            policy_loss = -(log_probs * advantages).mean()
            
            # Update
            self.policy_optimizer.zero_grad()
            policy_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
            self.policy_optimizer.step()
            
            self.value_optimizer.zero_grad()
            value_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.value_net.parameters(), 0.5)
            self.value_optimizer.step()
        
        self.steps_trained += len(states)
    
    def step(self, env, n_rollouts=4):
        """Run multiple PPO updates"""
        for _ in range(n_rollouts):
            rollout = self.collect_rollout(env, n_steps=512)
            self.update(rollout)
        
        mean_reward = np.mean(self.episode_rewards) if self.episode_rewards else 0
        
        return {
            'mean_reward': mean_reward,
            'steps_trained': self.steps_trained,
            'is_plateau': self.is_plateau()
        }
    
    def is_plateau(self):
        """Detect if PPO has stalled"""
        if len(self.episode_rewards) < 20:
            return False
        improvement = np.mean(list(self.episode_rewards)[-5:]) - np.mean(list(self.episode_rewards)[:5])
        return improvement < 10
    
    def load_from_static(self, static_params):
        """Initialize from static evolution parameters"""
        self.policy.set_flat_params(static_params)
    
    def get_policy_params(self):
        """Extract current policy parameters"""
        return self.policy.get_flat_params()

# ============================================================================
# BILATERAL COORDINATOR
# ============================================================================
class BilateralAgent:
    """Switches between Static (L) and PPO (R) based on plateau detection"""
    def __init__(self):
        self.policy_template = SharedPolicy()
        self.active_hemisphere = 'left'
        self.left = LeftHemisphere(self.policy_template, pop_size=128)
        self.right = None
        self.env = gym.make("Ant-v4", terminate_when_unhealthy=True)
        
        self.switch_count = 0
        self.history = []
        
    def run(self, max_switches=10):
        """Main training loop with hemisphere switching"""
        print("=" * 60)
        print("BILATERAL HEMISPHERE AGENT - Ant-v4")
        print("=" * 60)
        
        while self.switch_count < max_switches:
            if self.active_hemisphere == 'left':
                print(f"\n{'='*60}")
                print(f"LEFT HEMISPHERE ACTIVE (Static Evolution)")
                print(f"{'='*60}")
                
                for gen in range(200):  # Run up to 200 generations
                    result = self.left.step()
                    
                    if gen % 10 == 0:
                        print(f"[Gen {self.left.gen:3d}] "
                              f"Best={result['best_fitness']:6.1f} | "
                              f"Mean={result['mean_fitness']:6.1f} | "
                              f"Steps={result['mean_steps']:4.0f}")
                    
                    if result['is_plateau']:
                        print(f"\n>>> LEFT HEMISPHERE PLATEAU DETECTED <<<")
                        print(f"Final Best Fitness: {result['best_fitness']:.1f}")
                        self._switch_to_right()
                        break
                else:
                    # Ran 200 gens without plateau
                    print("\n>>> LEFT HEMISPHERE: MAX GENERATIONS REACHED <<<")
                    self._switch_to_right()
                    
            else:  # right hemisphere
                print(f"\n{'='*60}")
                print(f"RIGHT HEMISPHERE ACTIVE (PPO Refinement)")
                print(f"{'='*60}")
                
                for update in range(100):  # Run up to 100 updates
                    result = self.right.step(self.env, n_rollouts=4)
                    
                    if update % 5 == 0:
                        print(f"[Update {update:3d}] "
                              f"MeanReward={result['mean_reward']:6.1f} | "
                              f"Steps={result['steps_trained']}")
                    
                    if result['is_plateau']:
                        print(f"\n>>> RIGHT HEMISPHERE PLATEAU DETECTED <<<")
                        print(f"Final Mean Reward: {result['mean_reward']:.1f}")
                        self._switch_to_left()
                        break
                else:
                    print("\n>>> RIGHT HEMISPHERE: MAX UPDATES REACHED <<<")
                    self._switch_to_left()
        
        print("\n" + "="*60)
        print(f"TRAINING COMPLETE: {self.switch_count} hemisphere switches")
        print("="*60)
        
        self.cleanup()
    
    def _switch_to_right(self):
        """Switch from Static to PPO"""
        self.switch_count += 1
        print(f"\n>>> SWITCHING TO RIGHT HEMISPHERE (Switch #{self.switch_count}) <<<")
        
        # Transfer best static parameters to PPO
        best_params = self.left.get_best_policy()
        self.right = RightHemisphere(self.policy_template)
        self.right.load_from_static(best_params)
        
        self.active_hemisphere = 'right'
        
    def _switch_to_left(self):
        """Switch from PPO back to Static"""
        self.switch_count += 1
        print(f"\n>>> SWITCHING TO LEFT HEMISPHERE (Switch #{self.switch_count}) <<<")
        
        # Transfer refined PPO parameters back to static population
        refined_params = self.right.get_policy_params()
        # Seed the static population with the refined policy
        self.left.pop[0] = refined_params
        self.left.best_params = refined_params
        
        self.active_hemisphere = 'left'
    
    def cleanup(self):
        self.left.cleanup()
        self.env.close()

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method('spawn', force=True)
    
    agent = BilateralAgent()
    agent.run(max_switches=10)