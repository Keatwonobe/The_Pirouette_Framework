#!/usr/bin/env python3
"""
Wendigo-FIT Universal: Adaptive Utility Staircase
--------------------------------------------------
A generalized system that automatically scales three core utilities
to match task difficulty:

UTILITY 1 (FIT): Survival Pressure
- Normalizes reward by survival time
- Creates baseline: "don't die" > "do task badly"

UTILITY 2 (FIT): Exploration Pressure  
- Risk bonus for bold actions
- Prevents collapse into passive local minima

UTILITY 3 (Wendigo): Coherence Memory
- Adaptive manifold learns successful action patterns
- Provides consistency bias from past success

THE STAIRCASE CONCEPT:
----------------------
Each utility creates a "step" in the learning landscape:
1. Survival gets you to step 1 (agent stays alive)
2. Exploration gets you to step 2 (agent finds solutions)
3. Memory gets you to step 3 (agent refines and stabilizes)

For harder tasks (Humanoid), we adjust the staircase:
- Stronger survival pressure (harder to stay alive)
- More exploration bonus (need bolder search)
- Faster manifold learning (capture rare successes quickly)
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal
import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
from collections import deque, OrderedDict
import random
import time
import math
import os
import shutil
import copy

# --- Task Configuration ---
ENV_NAME = 'Humanoid-v5'  # The challenge
NUM_EPISODES = 6000
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 10
EVAL_EPISODES = 5
SEED = 42
MODEL_PATH = "./wendigo_fit_universal/"

# --- Core Hyperparameters (Stable across tasks) ---
RESET_PATIENCE = 10
GENETIC_POOL_SIZE = 10
GENE_TRANSFER_RATE = 0.6
MAX_ACCEPTABLE_STD = 2.0

# --- Adaptive Utility Parameters ---
# These scale automatically based on task difficulty
class TaskDifficulty:
    """Encodes task-specific scaling for the three utilities."""
    
    @staticmethod
    def get_params(env_name: str):
        """
        Returns (survival_mode, exploration_scale, memory_scale, dr_params)
        
        survival_mode: 'normalize' or 'weighted'
        exploration_scale: multiplier for risk bonus
        memory_scale: manifold learning rate and bonus
        dr_params: dark residue calculation weights
        """
        if 'CartPole' in env_name:
            return {
                'survival_mode': 'normalize',
                'exploration_scale': 0.05,
                'memory_scale': 0.3,
                'dr_weights': {'primary': 1.5, 'secondary': 0.3, 'target': 0.0},
                'action_threshold': 0.5,
            }
        
        elif 'Ant' in env_name:
            return {
                'survival_mode': 'normalize',
                'exploration_scale': 0.1,
                'memory_scale': 0.05,
                'dr_weights': {'primary': 1.5, 'secondary': 0.05, 'target': 0.6},
                'action_threshold': 0.1,
            }
        
        elif 'Humanoid' in env_name:
            # Humanoid is HARD: needs stronger utilities
            return {
                'survival_mode': 'weighted',  # Not just normalize - weight survival heavily
                'exploration_scale': 0.15,     # More exploration needed
                'memory_scale': 0.08,          # Faster manifold learning
                'dr_weights': {'primary': 2.0, 'secondary': 0.08, 'target': 1.4},
                'action_threshold': 0.15,      # Encourage bolder actions
            }
        
        else:
            # Default: conservative settings
            return {
                'survival_mode': 'normalize',
                'exploration_scale': 0.1,
                'memory_scale': 0.05,
                'dr_weights': {'primary': 1.0, 'secondary': 0.05, 'target': 0.0},
                'action_threshold': 0.1,
            }


# --- Dark Residue Calculator ---
class DarkResidueCalculator:
    """
    Task-agnostic instability metric.
    Measures "how far from ideal stable state".
    """
    def __init__(self, params):
        self.primary_weight = params['primary']
        self.secondary_weight = params['secondary']
        self.target_value = params['target']
    
    def calculate(self, obs: np.ndarray) -> float:
        """
        Generic DR calculation:
        - Primary metric: position/orientation deviation
        - Secondary metric: velocity/angular velocity magnitude
        """
        # For humanoid: obs[0] is z-height, want ~1.4
        # For ant: obs[2] is z-height, want ~0.6
        primary_dim = 0 if 'z' not in str(obs.shape) else 2  # adaptive
        
        if len(obs) > primary_dim:
            primary_val = obs[primary_dim]
        else:
            primary_val = self.target_value
        
        primary_error = abs(primary_val - self.target_value)
        
        # Secondary: velocity energy (typically last 10-20% of obs)
        vel_start = int(len(obs) * 0.5)  # second half usually velocities
        velocity_energy = np.sum(np.abs(obs[vel_start:]))
        
        dr = (self.primary_weight * primary_error + 
              self.secondary_weight * velocity_energy)
        
        return float(dr)


# --- Adaptive Success-Learning Manifold ---
class AdaptiveManifold:
    """
    The coherence memory utility.
    Learns what successful actions look like.
    """
    def __init__(self, action_dim, learning_scale):
        self.action_dim = action_dim
        self.center = np.zeros(action_dim, dtype=np.float32)
        self.velocity = np.zeros(action_dim, dtype=np.float32)
        
        # Scale learning rate by task difficulty
        self.learning_rate = 0.05 * learning_scale
        self.momentum = 0.95
        self.bonus_coeff = 0.02 * learning_scale
        
        self.success_history = deque(maxlen=100)
        self.update_counter = 0
    
    def observe_action(self, action: np.ndarray, reward: float, dr: float):
        """Learn from actions that yield stable success."""
        self.success_history.append((action, reward, dr))
        self.update_counter += 1
        
        # Update manifold periodically (not every step - too noisy)
        if self.update_counter % 10 == 0 and len(self.success_history) >= 20:
            recent = list(self.success_history)[-20:]
            
            # Success = high reward AND low instability
            rewards = [r for _, r, _ in recent]
            drs = [dr for _, _, dr in recent]
            
            avg_reward = np.mean(rewards)
            avg_dr = np.mean(drs)
            
            # Only learn from genuinely good outcomes
            # (high reward, stable execution)
            success_score = avg_reward - 0.5 * avg_dr
            
            if success_score > np.percentile([s[1] for s in self.success_history], 60):
                # This is better than usual - learn from it
                avg_action = np.mean([a for a, _, _ in recent], axis=0)
                
                # Momentum-based smooth update
                target_direction = avg_action - self.center
                self.velocity = (self.momentum * self.velocity + 
                               (1 - self.momentum) * target_direction)
                self.center += self.learning_rate * self.velocity
    
    def get_alignment_bonus(self, action: np.ndarray) -> float:
        """Reward actions similar to past successes."""
        distance = np.linalg.norm(action - self.center)
        bonus = self.bonus_coeff * math.exp(-2.0 * distance)
        return bonus
    
    def get_info(self) -> dict:
        return {
            'manifold_center_norm': np.linalg.norm(self.center),
            'manifold_velocity_norm': np.linalg.norm(self.velocity),
        }


# --- Survival Utility ---
class SurvivalReward:
    """
    Utility 1: Make survival the primary objective.
    Two modes:
    - 'normalize': reward / steps (standard)
    - 'weighted': reward + survival_bonus * steps (for very hard tasks)
    """
    def __init__(self, mode='normalize', weight=0.1):
        self.mode = mode
        self.weight = weight
    
    def apply(self, episode_reward: float, steps: int, max_steps: int) -> float:
        if self.mode == 'normalize':
            return episode_reward / steps if steps > 0 else episode_reward
        
        elif self.mode == 'weighted':
            # For hard tasks: explicitly reward staying alive
            survival_fraction = steps / max_steps
            survival_bonus = self.weight * survival_fraction
            normalized = episode_reward / steps if steps > 0 else episode_reward
            return normalized + survival_bonus
        
        return episode_reward / steps if steps > 0 else episode_reward


# --- SAC Agent (Unchanged from synthesis) ---
class Actor(nn.Module):
    def __init__(self, s, a, h=256):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(s, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU())
        self.mean = nn.Linear(h, a)
        self.log_std = nn.Linear(h, a)
    
    def forward(self, s):
        x = self.net(s)
        return self.mean(x), torch.clamp(self.log_std(x), -20, 2)


class Critic(nn.Module):
    def __init__(self, s, a, h=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(s + a, h), nn.ReLU(),
            nn.Linear(h, h), nn.ReLU(),
            nn.Linear(h, 1)
        )
    
    def forward(self, s, a):
        return self.net(torch.cat([s, a], 1))


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, s, a, r, s_, d):
        self.buffer.append((s, a, r, s_, d))
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)


class SACAgent:
    def __init__(self, env, lr=3e-4, gamma=0.99, tau=0.005, alpha=0.2):
        self.env = env
        self.state_dim = env.observation_space.shape[0]
        self.action_dim = env.action_space.shape[0]
        self.gamma, self.tau, self.alpha = gamma, tau, alpha
        
        self.action_scale = torch.tensor(
            (env.action_space.high - env.action_space.low) / 2.,
            device=device, dtype=torch.float32
        )
        self.action_bias = torch.tensor(
            (env.action_space.high + env.action_space.low) / 2.,
            device=device, dtype=torch.float32
        )
        
        self.actor = Actor(self.state_dim, self.action_dim).to(device)
        self.c1 = Critic(self.state_dim, self.action_dim).to(device)
        self.c2 = Critic(self.state_dim, self.action_dim).to(device)
        self.c1_t = Critic(self.state_dim, self.action_dim).to(device)
        self.c2_t = Critic(self.state_dim, self.action_dim).to(device)
        
        self.c1_t.load_state_dict(self.c1.state_dict())
        self.c2_t.load_state_dict(self.c2.state_dict())
        
        self.actor_opt = optim.Adam(self.actor.parameters(), lr=lr)
        self.c1_opt = optim.Adam(self.c1.parameters(), lr=lr)
        self.c2_opt = optim.Adam(self.c2.parameters(), lr=lr)
        
        self.buffer = ReplayBuffer(1_000_000)
    
    def select_action(self, state, eval=False):
        state_t = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        mean, log_std = self.actor(state_t)
        
        if eval:
            action = torch.tanh(mean)
        else:
            dist = Normal(mean, log_std.exp())
            action = torch.tanh(dist.rsample())
        
        action_np = action.cpu().detach().numpy()[0]
        return action_np * self.action_scale.cpu().numpy() + self.action_bias.cpu().numpy()
    
    def update(self, batch_size):
        if len(self.buffer) < batch_size:
            return
        
        batch = self.buffer.sample(batch_size)
        s, a, r, s_, d = zip(*batch)
        
        s = torch.tensor(np.array(s), device=device, dtype=torch.float32)
        a = torch.tensor(np.array(a), device=device, dtype=torch.float32)
        r = torch.tensor(np.array(r), device=device, dtype=torch.float32).unsqueeze(1)
        s_ = torch.tensor(np.array(s_), device=device, dtype=torch.float32)
        d = torch.tensor(np.array(d), device=device, dtype=torch.float32).unsqueeze(1)
        
        with torch.no_grad():
            mean_, log_std_ = self.actor(s_)
            dist_ = Normal(mean_, log_std_.exp())
            z = dist_.rsample()
            a_ = torch.tanh(z)
            log_prob = dist_.log_prob(z) - torch.log(1 - a_.pow(2) + 1e-6)
            log_prob = log_prob.sum(1, keepdim=True)
            
            tq1 = self.c1_t(s_, a_)
            tq2 = self.c2_t(s_, a_)
            target_q = torch.min(tq1, tq2) - self.alpha * log_prob
            target_q = r + (1 - d) * self.gamma * target_q
        
        q1 = self.c1(s, a)
        q2 = self.c2(s, a)
        critic_loss = torch.nn.functional.mse_loss(q1, target_q) + \
                     torch.nn.functional.mse_loss(q2, target_q)
        
        self.c1_opt.zero_grad()
        self.c2_opt.zero_grad()
        critic_loss.backward()
        self.c1_opt.step()
        self.c2_opt.step()
        
        mean, log_std = self.actor(s)
        dist = Normal(mean, log_std.exp())
        z = dist.rsample()
        a_pi = torch.tanh(z)
        log_prob = dist.log_prob(z) - torch.log(1 - a_pi.pow(2) + 1e-6)
        log_prob = log_prob.sum(1, keepdim=True)
        
        q1_pi = self.c1(s, a_pi)
        q2_pi = self.c2(s, a_pi)
        min_q_pi = torch.min(q1_pi, q2_pi)
        
        actor_loss = (self.alpha * log_prob - min_q_pi).mean()
        
        self.actor_opt.zero_grad()
        actor_loss.backward()
        self.actor_opt.step()
        
        for target_param, param in zip(self.c1_t.parameters(), self.c1.parameters()):
            target_param.data.copy_(target_param.data * (1.0 - self.tau) + param.data * self.tau)
        for target_param, param in zip(self.c2_t.parameters(), self.c2.parameters()):
            target_param.data.copy_(target_param.data * (1.0 - self.tau) + param.data * self.tau)
    
    def save_model(self, rank):
        path = os.path.join(MODEL_PATH, f"rank_{rank}")
        os.makedirs(path, exist_ok=True)
        torch.save(self.actor.state_dict(), os.path.join(path, "actor.pth"))
    
    def load_model(self, rank):
        path = os.path.join(MODEL_PATH, f"rank_{rank}", "actor.pth")
        self.actor.load_state_dict(torch.load(path))
    
    def genetic_crossover(self, high_scores_data):
        print("  > Performing genetic crossover...")
        sorted_scores = sorted(high_scores_data.items(), key=lambda x: x[0], reverse=True)
        
        if len(sorted_scores) < 2:
            print("  > Not enough parents for crossover.")
            return None
        
        p1_rank = sorted_scores[0][1]['rank']
        p2_rank = sorted_scores[1][1]['rank']
        p1_score = sorted_scores[0][0]
        
        print(f"  > Parents: Rank {p1_rank} (Score: {p1_score:.2f}) and Rank {p2_rank}")
        
        self.load_model(p1_rank)
        best_parent_weights = copy.deepcopy(self.actor.state_dict())
        
        p1_weights = torch.load(os.path.join(MODEL_PATH, f"rank_{p1_rank}", "actor.pth"))
        p2_weights = torch.load(os.path.join(MODEL_PATH, f"rank_{p2_rank}", "actor.pth"))
        
        child_weights = OrderedDict()
        for key in p1_weights:
            if random.random() < GENE_TRANSFER_RATE:
                child_weights[key] = p1_weights[key].clone()
            else:
                child_weights[key] = p2_weights[key].clone()
        
        self.actor.load_state_dict(child_weights)
        print("  > Crossover complete.")
        
        return best_parent_weights, p1_score


# --- Universal Trainer ---
class UniversalTrainer:
    """
    Adaptive trainer that scales utilities based on task difficulty.
    """
    def __init__(self, env_name):
        self.env_name = env_name
        self.env = gym.make(env_name, render_mode=None)
        self.agent = SACAgent(self.env)
        
        # Get task-specific parameters
        self.params = TaskDifficulty.get_params(env_name)
        
        # Initialize utilities with task-specific scaling
        self.survival_utility = SurvivalReward(
            mode=self.params['survival_mode'],
            weight=0.1
        )
        
        self.manifold = AdaptiveManifold(
            self.agent.action_dim,
            learning_scale=self.params['memory_scale'] / 0.05  # normalize to base
        )
        
        self.dr_calculator = DarkResidueCalculator(self.params['dr_weights'])
        
        self.exploration_scale = self.params['exploration_scale']
        self.action_threshold = self.params['action_threshold']
        
        self.batch_size = 256
        self.eval_history = []
        self.dr_history = []
        self.high_scores = {}
        self.consecutive_bad_cycles = 0
        
        print(f"\n{'='*60}")
        print(f"ADAPTIVE UTILITY CONFIGURATION FOR {env_name}")
        print(f"{'='*60}")
        print(f"Survival Mode: {self.params['survival_mode']}")
        print(f"Exploration Scale: {self.exploration_scale}")
        print(f"Memory Learning Scale: {self.params['memory_scale']}")
        print(f"Action Threshold: {self.action_threshold}")
        print(f"{'='*60}\n")
    
    def train(self):
        start_time = time.time()
        
        for ep in range(1, NUM_EPISODES + 1):
            s, _ = self.env.reset(seed=SEED + ep)
            ep_reward = 0
            ep_dr_sum = 0
            steps_in_episode = 0
            
            for step in range(1, MAX_STEPS_PER_EPISODE + 1):
                a = self.agent.select_action(s)
                s_, r_env, terminated, truncated, _ = self.env.step(a)
                done = terminated or truncated
                
                # Calculate DR for diagnostics
                dr = self.dr_calculator.calculate(s_)
                ep_dr_sum += dr
                
                # UTILITY 2: Exploration pressure
                action_magnitude = np.linalg.norm(a)
                risk_bonus = ((action_magnitude - self.action_threshold) * 
                            self.exploration_scale 
                            if action_magnitude > self.action_threshold else 0)
                
                # UTILITY 3: Coherence memory
                manifold_bonus = self.manifold.get_alignment_bonus(a)
                
                # Total reward
                total_reward = r_env + risk_bonus + manifold_bonus
                
                # Let manifold learn
                self.manifold.observe_action(a, r_env, dr)
                
                self.agent.buffer.push(s, a, total_reward, s_, done)
                self.agent.update(self.batch_size)
                
                s = s_
                ep_reward += r_env
                steps_in_episode += 1
                
                if done:
                    break
            
            # UTILITY 1: Survival pressure
            ep_reward_processed = self.survival_utility.apply(
                ep_reward, steps_in_episode, MAX_STEPS_PER_EPISODE
            )
            avg_dr = ep_dr_sum / steps_in_episode if steps_in_episode > 0 else ep_dr_sum
            
            if ep % 10 == 0:
                manifold_info = self.manifold.get_info()
                print(f"Ep:{ep:04d} | R:{ep_reward_processed:7.2f} | "
                      f"Steps:{steps_in_episode:4d} | DR:{avg_dr:.3f} | "
                      f"M:{manifold_info['manifold_center_norm']:.2f}")
            
            if ep % EVAL_FREQUENCY == 0:
                self.run_evaluation_and_manage_pool(ep)
        
        elapsed = time.time() - start_time
        print(f"\nTraining finished in {elapsed:.2f}s.")
        self.plot_results()
    
    def run_evaluation_and_manage_pool(self, ep, post_crossover=False, parent_score=None):
        eval_rewards = []
        eval_drs = []
        
        for i in range(EVAL_EPISODES):
            s, _ = self.env.reset(seed=SEED * 100 + i)
            ep_reward = 0
            ep_dr_sum = 0
            steps = 0
            
            for _ in range(MAX_STEPS_PER_EPISODE):
                a = self.agent.select_action(s, eval=True)
                s, r, terminated, truncated, _ = self.env.step(a)
                
                dr = self.dr_calculator.calculate(s)
                ep_dr_sum += dr
                ep_reward += r
                steps += 1
                
                if terminated or truncated:
                    break
            
            processed_reward = self.survival_utility.apply(ep_reward, steps, MAX_STEPS_PER_EPISODE)
            avg_dr = ep_dr_sum / steps if steps > 0 else ep_dr_sum
            
            eval_rewards.append(processed_reward)
            eval_drs.append(avg_dr)
        
        current_score = np.mean(eval_rewards)
        score_std = np.std(eval_rewards)
        avg_dr = np.mean(eval_drs)
        
        if not post_crossover:
            self.eval_history.append(current_score)
            self.dr_history.append(avg_dr)
        
        best_pool_score = max(self.high_scores.keys()) if self.high_scores else -np.inf
        
        print(f"  > Eval @ {ep} | Score:{current_score:7.2f} | Std:{score_std:.2f} | "
              f"DR:{avg_dr:.3f} | Best:{best_pool_score:7.2f}")
        
        if post_crossover:
            if current_score < parent_score:
                print(f"  > Crossover FAILED! Rolling back...")
                return False
            else:
                print(f"  > Crossover SUCCESS!")
                return True
        
        is_stable = score_std <= MAX_ACCEPTABLE_STD
        is_improvement = (len(self.high_scores) < GENETIC_POOL_SIZE or 
                         current_score > min(self.high_scores.keys()))
        
        if is_stable and is_improvement:
            if len(self.high_scores) == GENETIC_POOL_SIZE:
                worst_score = min(self.high_scores.keys())
                worst_rank = self.high_scores.pop(worst_score)['rank']
                shutil.rmtree(os.path.join(MODEL_PATH, f"rank_{worst_rank}"), 
                            ignore_errors=True)
            
            used_ranks = {data['rank'] for data in self.high_scores.values()}
            new_rank = next(r for r in range(1, GENETIC_POOL_SIZE + 2) 
                          if r not in used_ranks)
            
            self.high_scores[current_score] = {'rank': new_rank}
            self.agent.save_model(new_rank)
            print(f"  > Added to pool at rank {new_rank}")
            self.consecutive_bad_cycles = 0
            
        elif not is_stable:
            print(f"  > Rejected: unstable (Std: {score_std:.2f})")
        else:
            self.consecutive_bad_cycles += 1
            print(f"  > No improvement. Bad cycles: {self.consecutive_bad_cycles}/{RESET_PATIENCE}")
        
        if self.consecutive_bad_cycles >= RESET_PATIENCE:
            self.perform_genetic_crossover(ep)
            self.consecutive_bad_cycles = 0
    
    def perform_genetic_crossover(self, ep):
        print("\n  ! STAGNATED. GENETIC TRANSFER !")
        
        result = self.agent.genetic_crossover(self.high_scores)
        if result is None:
            return
        
        best_parent_weights, parent_score = result
        
        print("  > Validating...")
        success = self.run_evaluation_and_manage_pool(ep, post_crossover=True, 
                                                      parent_score=parent_score)
        
        if not success:
            self.agent.actor.load_state_dict(best_parent_weights)
            print("  > Rollback complete.")
        else:
            print("  > New generation validated.")
    
    def plot_results(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        ax1.set_title(f"Universal Trainer: {self.env_name}")
        ax1.set_xlabel("Episode")
        ax1.set_ylabel("Evaluation Score")
        eval_episodes = np.arange(EVAL_FREQUENCY, 
                                 len(self.eval_history) * EVAL_FREQUENCY + 1, 
                                 EVAL_FREQUENCY)
        ax1.plot(eval_episodes, self.eval_history, color='tab:blue', lw=2)
        ax1.grid(True)
        
        ax2.set_title("Dark Residue (Stability)")
        ax2.set_xlabel("Episode")
        ax2.set_ylabel("Average DR")
        ax2.plot(eval_episodes, self.dr_history, color='tab:red', lw=2)
        ax2.grid(True)
        
        plt.tight_layout()
        save_path = f"universal_trainer_{self.env_name.lower()}.png"
        plt.savefig(save_path)
        print(f"\nPlot saved to {save_path}")


# --- Main Execution ---
if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    
    if os.path.exists(MODEL_PATH):
        shutil.rmtree(MODEL_PATH)
    os.makedirs(MODEL_PATH, exist_ok=True)
    
    print(f"Using device: {device}")
    print(f"Models will be saved in: {MODEL_PATH}")
    
    trainer = UniversalTrainer(ENV_NAME)
    trainer.train()