#!/usr/bin/env python3
"""
Sand Engram 02: The Helical Operator
====================================
"The integral path is derivative of a spiral precession."

Fixes the 'Panic Collapse' of Engram 01 by introducing TPCI 
(Triadic Phase Coupling Index) as a phase switch.

The TPCI Triad:
1. Intent (Current Action)
2. Hysteresis (Previous Action)
3. Reality (Velocity Vector)

The Helical Update Logic:
- IF TPCI > Threshold (Flow State):
    Gradient points toward MAXIMIZING REWARD.
    (The agent dances.)

- IF TPCI < Threshold (Stress State):
    Gradient points toward MINIMIZING ENTROPY.
    (The agent centers itself. It ignores external reward to fix internal state.)

This forces the agent to "spiral" down into the valley of stability 
before attempting to climb the mountain of reward.
"""

import argparse
import csv
import time
import sys
from dataclasses import dataclass
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

try:
    import gymnasium as gym
except ImportError:
    import gym

# ============================================================================
# Configuration
# ============================================================================

@dataclass
class Config:
    env_id: str = "Humanoid-v5" # Switch to Ant-v5 if desired
    hidden_dim: int = 256
    lr: float = 3e-4
    gamma: float = 0.99
    episodes: int = 10000
    
    # The Helical Parameters
    tpci_threshold: float = 0.9  # Below this, we enter "Stabilization Mode"
    spiral_damping: float = 0.1  # How hard we force stability in stress
    

# ============================================================================
# The Helical Policy (Engram)
# ============================================================================

class HelicalPolicy(nn.Module):
    def __init__(self, obs_dim: int, action_dim: int, hidden_dim: int):
        super().__init__()
        # Standard MLP Actor
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim), # Added for manifold stability
            nn.Tanh(),
            nn.Linear(hidden_dim, 2 * action_dim) 
        )
        
        # Orthogonal init for rotational symmetry in weight space
        for m in self.net.modules():
            if isinstance(m, nn.Linear):
                nn.init.orthogonal_(m.weight, gain=np.sqrt(2))
                nn.init.constant_(m.bias, 0)

    def forward(self, obs):
        x = self.net(obs)
        mean, log_std = torch.chunk(x, 2, dim=-1)
        # Tighter constraints on variance to prevent explosion
        log_std = torch.clamp(log_std, -5.0, 1.0) 
        return mean, log_std

    def sample(self, obs):
        mean, log_std = self.forward(obs)
        std = torch.exp(log_std)
        dist = torch.distributions.Normal(mean, std)
        
        # Reparameterization trick (essential for gradient flow)
        z = dist.rsample() 
        action_tanh = torch.tanh(z)
        
        # Log prob adjustment for Tanh
        log_prob = dist.log_prob(z).sum(dim=-1)
        log_prob -= torch.log(1 - action_tanh.pow(2) + 1e-6).sum(dim=-1)
        
        return action_tanh, log_prob, mean, std, dist

    def calculate_tpci(self, current_action, prev_action, velocity):
        """
        Triadic Phase Coupling Index (TPCI).
        Measures the synchronization of the Triad:
        1. Action (Intent)
        2. d_Action (Smoothness/Hysteresis)
        3. Velocity (Reality)
        """
        # Normalize vectors
        def norm_vec(v):
            n = torch.norm(v)
            return v / (n + 1e-8), n

        # 1. Intent vs Reality (Alignment)
        # Do I move where I push?
        a_vec, a_mag = norm_vec(current_action)
        v_vec, v_mag = norm_vec(velocity)
        # Match dims if necessary
        min_dim = min(a_vec.shape[0], v_vec.shape[0])
        alignment = torch.dot(a_vec[:min_dim], v_vec[:min_dim])

        # 2. Intent vs Hysteresis (Smoothness)
        # Am I jerking around? (Derivative of the spiral)
        if prev_action is None:
            smoothness = torch.tensor(1.0).to(current_action.device)
        else:
            p_vec, _ = norm_vec(prev_action)
            smoothness = torch.dot(a_vec, p_vec)

        # TPCI is the harmonic mean of Alignment and Smoothness
        # We map it to [0, 1]
        # Alignment is [-1, 1], Smoothness is [-1, 1]
        
        # Shift to positive domain
        align_score = (alignment + 1) / 2
        smooth_score = (smoothness + 1) / 2
        
        tpci = 2 * (align_score * smooth_score) / (align_score + smooth_score + 1e-8)
        return tpci.item()

# ============================================================================
# The Operator (Trainer)
# ============================================================================

class HelicalOperator:
    def __init__(self, env, config: Config):
        self.env = env
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.policy = HelicalPolicy(
            env.observation_space.shape[0],
            env.action_space.shape[0],
            config.hidden_dim
        ).to(self.device)
        
        self.optimizer = optim.Adam(self.policy.parameters(), lr=config.lr)

    def train_episode(self, episode_idx):
        obs, _ = self.env.reset()
        obs_t = torch.FloatTensor(obs).to(self.device)
        
        # Trajectory buffers
        log_probs = []
        rewards = []
        entropies = []
        tpcis = []
        
        prev_action = None
        total_reward = 0
        steps = 0
        
        done = False
        while not done:
            # 1. Sample
            action, log_prob, mean, std, dist = self.policy.sample(obs_t)
            action_np = action.cpu().detach().numpy()
            
            # 2. Step
            next_obs, reward, terminated, truncated, _ = self.env.step(action_np)
            done = terminated or truncated
            
            # 3. Calculate TPCI (The Triad)
            # We approximate velocity as change in obs (simple heuristic)
            # For Ant/Humanoid, obs[0:2] is often xy-coord or velocity, but delta obs works generically
            velocity_est = torch.FloatTensor(next_obs - obs).to(self.device)
            
            tpci = self.policy.calculate_tpci(action, prev_action, velocity_est)
            
            # Store
            log_probs.append(log_prob)
            rewards.append(reward)
            entropies.append(dist.entropy().sum(dim=-1))
            tpcis.append(tpci)
            
            total_reward += reward
            steps += 1
            
            prev_action = action
            obs = next_obs
            obs_t = torch.FloatTensor(obs).to(self.device)

        # 4. The Helical Update
        self.update_helical(log_probs, rewards, entropies, tpcis)
        
        avg_tpci = sum(tpcis) / len(tpcis)
        return total_reward, avg_tpci, steps

    def update_helical(self, log_probs, rewards, entropies, tpcis):
        R = 0
        returns = []
        
        # Discounted Returns
        for r in reversed(rewards):
            R = r + self.config.gamma * R
            returns.insert(0, R)
        
        returns = torch.tensor(returns).to(self.device)
        # Normalize returns (Critical for stability)
        returns = (returns - returns.mean()) / (returns.std() + 1e-9)
        
        policy_loss = []
        
        # --- THE HELICAL CALCULUS ---
        # We iterate through time (the integral path)
        for log_prob, R_val, entropy, tpci in zip(log_probs, returns, entropies, tpcis):
            
            # The Switch:
            # If TPCI is HIGH: We are coupled. Focus on Reward.
            # If TPCI is LOW: We are decoupled (Stress). Focus on Stability.
            
            if tpci > self.config.tpci_threshold:
                # FLOW STATE (Reward Integral)
                # Standard Policy Gradient
                # We Encourage the behavior that got us here.
                loss_component = -log_prob * R_val
            else:
                # STRESS STATE (Spiral Correction)
                # We ignore the Reward (because it's likely noise/lucky).
                # We actively punish Entropy. We force the agent to "tuck and roll."
                # Minimizing entropy = Maximizing negative entropy
                
                # We want: minimize H(pi) -> loss = +H(pi)
                loss_component = entropy * self.config.spiral_damping
            
            policy_loss.append(loss_component)
            
        # Backprop
        self.optimizer.zero_grad()
        policy_loss = torch.stack(policy_loss).mean() # Mean over batch for stability
        policy_loss.backward()
        
        # Gradient Clipping (The Limit on Velocity)
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
        self.optimizer.step()

# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str, default="Humanoid-v5")
    parser.add_argument("--episodes", type=int, default=5000)
    args = parser.parse_args()
    
    config = Config(env_id=args.env, episodes=args.episodes)
    
    env = gym.make(config.env_id)
    operator = HelicalOperator(env, config)
    
    out_file = "sand_helical_run.csv"
    
    with open(out_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["episode", "reward", "tpci", "steps"])
        
        start_time = time.time()
        
        try:
            for ep in range(config.episodes):
                reward, tpci, steps = operator.train_episode(ep)
                
                writer.writerow([ep, reward, tpci, steps])
                f.flush()
                
                if ep % 10 == 0:
                    elapsed = time.time() - start_time
                    print(f"Ep {ep:4d} | Reward: {reward:6.1f} | TPCI: {tpci:.3f} | Steps: {steps:4d} | Time: {elapsed:.1f}s")
                    
        except KeyboardInterrupt:
            print("\nPaused.")
            
    print("Operator Shutdown.")
    env.close()

if __name__ == "__main__":
    main()