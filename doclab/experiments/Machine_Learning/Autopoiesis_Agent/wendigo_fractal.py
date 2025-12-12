#!/usr/bin/env python3
"""
Wendigo-FIT Synthesis: Adaptive Manifold Learning
--------------------------------------------------
This combines the best of both approaches:

FROM FIT (Keep These):
1. Survival normalization (reward / steps)
2. Risk bonus for exploration (bold actions)
3. Genetic memory with rollback
4. Stability filtering

FROM WENDIGO (Reimagined):
5. Dark Residue as stability metric (not penalty!)
6. Adaptive Manifold that learns from success (not random motion!)

KEY INNOVATION: The manifold center becomes a learned "attractor" 
that captures the action patterns of successful episodes, giving 
the agent a memory of what worked.
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

# --- Configuration ---
ENV_NAME = 'Ant-v5'
NUM_EPISODES = 4000
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 10
EVAL_EPISODES = 5
SEED = 42
MODEL_PATH = "./wendigo_fit_models/"

# --- Hyperparameters ---
RESET_PATIENCE = 10
GENETIC_POOL_SIZE = 10
GENE_TRANSFER_RATE = 0.6
RISK_REWARD_MULTIPLIER = 0.1
ACTION_MAGNITUDE_THRESHOLD = 0.1
MAX_ACCEPTABLE_STD = 2.0

# Manifold learning rates
MANIFOLD_LEARN_RATE = 0.05      # How fast manifold adapts to success
MANIFOLD_ALIGN_BONUS = 0.02     # Reward for matching successful patterns
MANIFOLD_MOMENTUM = 0.95        # Smoothing of manifold updates

# Dark Residue (stability tracking, not penalty!)
DR_WEIGHT_HEIGHT = 1.5
DR_WEIGHT_VELOCITY = 0.05
TARGET_HEIGHT = 0.6

# --- Setup ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if os.path.exists(MODEL_PATH):
    shutil.rmtree(MODEL_PATH)
os.makedirs(MODEL_PATH, exist_ok=True)
print(f"Using device: {device}")
print(f"Wendigo-FIT models will be saved in: {MODEL_PATH}")


# --- Wendigo Dark Residue (Diagnostic Only) ---
def calculate_dark_residue(obs: np.ndarray) -> float:
    """
    Measures instability without penalizing it in reward.
    Used for diagnostics and adaptive manifold learning.
    """
    height = obs[2] if len(obs) > 2 else TARGET_HEIGHT
    vel_energy = np.sum(np.abs(obs[-10:]))
    height_err = abs(height - TARGET_HEIGHT)
    return DR_WEIGHT_HEIGHT * height_err + DR_WEIGHT_VELOCITY * vel_energy


# --- Adaptive Success-Learning Manifold ---
class AdaptiveManifold:
    """
    A manifold that learns from successful actions.
    Instead of moving randomly, it adapts to capture 
    the action patterns that lead to good outcomes.
    """
    def __init__(self, action_dim):
        self.action_dim = action_dim
        self.center = np.zeros(action_dim, dtype=np.float32)
        self.velocity = np.zeros(action_dim, dtype=np.float32)
        self.success_history = deque(maxlen=100)  # Track recent performance
        
    def observe_action(self, action: np.ndarray, reward: float, dr: float):
        """
        Learn from actions that lead to good outcomes.
        Good = high reward AND low dark residue (stable success).
        """
        self.success_history.append((action, reward, dr))
        
        # Calculate success score (reward normalized by stability)
        if len(self.success_history) >= 10:
            recent = list(self.success_history)[-10:]
            avg_reward = np.mean([r for _, r, _ in recent])
            avg_dr = np.mean([dr for _, _, dr in recent])
            
            # Good outcomes are high reward with low instability
            success_score = avg_reward - 0.5 * avg_dr
            
            # If doing well, pull manifold toward these actions
            if success_score > 0:
                avg_action = np.mean([a for a, _, _ in recent], axis=0)
                # Momentum-based smooth update
                self.velocity = (MANIFOLD_MOMENTUM * self.velocity + 
                               (1 - MANIFOLD_MOMENTUM) * (avg_action - self.center))
                self.center += MANIFOLD_LEARN_RATE * self.velocity
    
    def get_alignment_bonus(self, action: np.ndarray) -> float:
        """
        Reward actions similar to successful past actions.
        This gives the agent a gentle "memory" of what worked.
        """
        distance = np.linalg.norm(action - self.center)
        # Exponential decay: close actions get bigger bonus
        bonus = MANIFOLD_ALIGN_BONUS * math.exp(-2.0 * distance)
        return bonus
    
    def get_info(self) -> dict:
        """Diagnostic information."""
        return {
            'manifold_center_norm': np.linalg.norm(self.center),
            'manifold_velocity_norm': np.linalg.norm(self.velocity),
        }


# --- SAC Agent (Compact Implementation) ---
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
        
        # Update critics
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
        
        # Update actor
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
        
        # Soft update target networks
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
        """Perform genetic crossover between top two parents."""
        print("  > Performing genetic crossover...")
        sorted_scores = sorted(high_scores_data.items(), key=lambda x: x[0], reverse=True)
        
        if len(sorted_scores) < 2:
            print("  > Not enough parents for crossover.")
            return None
        
        p1_rank = sorted_scores[0][1]['rank']
        p2_rank = sorted_scores[1][1]['rank']
        p1_score = sorted_scores[0][0]
        
        print(f"  > Parents: Rank {p1_rank} (Score: {p1_score:.2f}) and Rank {p2_rank}")
        
        # Save current best parent weights for potential rollback
        self.load_model(p1_rank)
        best_parent_weights = copy.deepcopy(self.actor.state_dict())
        
        # Load both parents
        p1_weights = torch.load(os.path.join(MODEL_PATH, f"rank_{p1_rank}", "actor.pth"))
        p2_weights = torch.load(os.path.join(MODEL_PATH, f"rank_{p2_rank}", "actor.pth"))
        
        # Create child
        child_weights = OrderedDict()
        for key in p1_weights:
            if random.random() < GENE_TRANSFER_RATE:
                child_weights[key] = p1_weights[key].clone()
            else:
                child_weights[key] = p2_weights[key].clone()
        
        self.actor.load_state_dict(child_weights)
        print("  > Crossover complete.")
        
        return best_parent_weights, p1_score


# --- Main Trainer ---
class WendigoFITTrainer:
    def __init__(self):
        self.env = gym.make(ENV_NAME, render_mode=None)
        self.agent = SACAgent(self.env)
        self.manifold = AdaptiveManifold(self.agent.action_dim)
        self.batch_size = 256
        
        self.eval_history = []
        self.dr_history = []
        self.high_scores = {}
        self.consecutive_bad_cycles = 0
    
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
                
                # Calculate dark residue for diagnostics
                dr = calculate_dark_residue(s_)
                ep_dr_sum += dr
                
                # FIT-style reward shaping
                action_magnitude = np.linalg.norm(a)
                risk_bonus = ((action_magnitude - ACTION_MAGNITUDE_THRESHOLD) * 
                            RISK_REWARD_MULTIPLIER 
                            if action_magnitude > ACTION_MAGNITUDE_THRESHOLD else 0)
                
                # Adaptive manifold alignment (learned from success)
                manifold_bonus = self.manifold.get_alignment_bonus(a)
                
                # Total reward combines task reward with learned biases
                total_reward = r_env + risk_bonus + manifold_bonus
                
                # Let manifold learn from this experience
                self.manifold.observe_action(a, r_env, dr)
                
                self.agent.buffer.push(s, a, total_reward, s_, done)
                self.agent.update(self.batch_size)
                
                s = s_
                ep_reward += r_env
                steps_in_episode += 1
                
                if done:
                    break
            
            # FIT-style survival normalization
            ep_reward_normalized = ep_reward / steps_in_episode if steps_in_episode > 0 else ep_reward
            avg_dr = ep_dr_sum / steps_in_episode if steps_in_episode > 0 else ep_dr_sum
            
            if ep % 10 == 0:
                manifold_info = self.manifold.get_info()
                print(f"Ep:{ep:04d} | Reward:{ep_reward_normalized:7.2f} | "
                      f"Steps:{steps_in_episode:4d} | DR:{avg_dr:.3f} | "
                      f"M_center:{manifold_info['manifold_center_norm']:.2f}")
            
            if ep % EVAL_FREQUENCY == 0:
                self.run_evaluation_and_manage_pool(ep)
        
        elapsed = time.time() - start_time
        print(f"\nTraining finished in {elapsed:.2f}s.")
        self.plot_results()
    
    def run_evaluation_and_manage_pool(self, ep, post_crossover=False, parent_score=None):
        """Evaluate agent and manage genetic pool."""
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
                
                dr = calculate_dark_residue(s)
                ep_dr_sum += dr
                ep_reward += r
                steps += 1
                
                if terminated or truncated:
                    break
            
            normalized_reward = ep_reward / steps if steps > 0 else ep_reward
            avg_dr = ep_dr_sum / steps if steps > 0 else ep_dr_sum
            
            eval_rewards.append(normalized_reward)
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
        
        # Handle post-crossover validation
        if post_crossover:
            if current_score < parent_score:
                print(f"  > Crossover FAILED! {current_score:.2f} < {parent_score:.2f}. Rolling back...")
                return False
            else:
                print(f"  > Crossover SUCCESS! {current_score:.2f} >= {parent_score:.2f}")
                return True
        
        # Check stability and improvement
        is_stable = score_std <= MAX_ACCEPTABLE_STD
        is_improvement = (len(self.high_scores) < GENETIC_POOL_SIZE or 
                         current_score > min(self.high_scores.keys()))
        
        if is_stable and is_improvement:
            # Add to pool
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
            print(f"  > New stable model added to pool at rank {new_rank}")
            self.consecutive_bad_cycles = 0
            
        elif not is_stable:
            print(f"  > Score rejected: unstable (Std: {score_std:.2f})")
        else:
            self.consecutive_bad_cycles += 1
            print(f"  > No improvement. Bad cycles: {self.consecutive_bad_cycles}/{RESET_PATIENCE}")
        
        # Trigger genetic crossover if stagnating
        if self.consecutive_bad_cycles >= RESET_PATIENCE:
            self.perform_genetic_crossover(ep)
            self.consecutive_bad_cycles = 0
    
    def perform_genetic_crossover(self, ep):
        """Perform genetic crossover with rollback protection."""
        print("\n  ! PERFORMANCE STAGNATED. INITIATING GENETIC TRANSFER !")
        
        result = self.agent.genetic_crossover(self.high_scores)
        if result is None:
            return
        
        best_parent_weights, parent_score = result
        
        print("  > Validating new generation...")
        success = self.run_evaluation_and_manage_pool(ep, post_crossover=True, 
                                                      parent_score=parent_score)
        
        if not success:
            # Rollback to best parent
            self.agent.actor.load_state_dict(best_parent_weights)
            print("  > Rollback complete. Best parent restored.")
        else:
            print("  > New generation validated. Continuing training.")
    
    def plot_results(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Plot 1: Evaluation Score
        ax1.set_title("Wendigo-FIT: Evaluation Score Over Training")
        ax1.set_xlabel("Episode")
        ax1.set_ylabel("Normalized Reward")
        eval_episodes = np.arange(EVAL_FREQUENCY, 
                                 len(self.eval_history) * EVAL_FREQUENCY + 1, 
                                 EVAL_FREQUENCY)
        ax1.plot(eval_episodes, self.eval_history, color='tab:blue', lw=2)
        ax1.grid(True)
        
        # Plot 2: Dark Residue (Stability Metric)
        ax2.set_title("Dark Residue (Lower = More Stable)")
        ax2.set_xlabel("Episode")
        ax2.set_ylabel("Average Dark Residue")
        ax2.plot(eval_episodes, self.dr_history, color='tab:red', lw=2)
        ax2.grid(True)
        
        plt.tight_layout()
        save_path = "wendigo_fit_results.png"
        plt.savefig(save_path)
        print(f"\nPlot saved to {save_path}")


# --- Main Execution ---
if __name__ == "__main__":
    trainer = WendigoFITTrainer()
    trainer.train()