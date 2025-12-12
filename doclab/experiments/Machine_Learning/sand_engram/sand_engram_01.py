#!/usr/bin/env python3
"""
Sand Engram 01: The Underdog
============================
"Right, not fast."

A minimalist RL agent that learns via the Pirouette Principle:
Reward is only reinforced when the agent is "Coherent" (Γ).

The Update Rule:
    ∇J = Σ ∇log π(a|s) * (R * Γ)

Where Γ (Resonance) is the product of:
    1. Internal Coherence (Low Entropy/Confidence)
    2. External Alignment (Intent matches Outcome)

This creates a "Valley Finding" dynamic where the agent
slides into low-energy, high-stability manifolds.
"""

import argparse
import csv
import json
import time
import signal
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
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
    env_id: str = "Humanoid-v5"
    hidden_dim: int = 256
    lr: float = 1e-3        # Higher LR because we dampen updates with Γ
    gamma: float = 0.99     # Discount factor
    episodes: int = 10000
    seed: int = 42
    
    # Engram Parameters
    coherence_scale: float = 1.0  # Scales the impact of gamma

# ============================================================================
# The Generative Engram (Policy)
# ============================================================================

class EngramPolicy(nn.Module):
    def __init__(self, obs_dim: int, action_dim: int, hidden_dim: int = 256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 2 * action_dim) # Mean and LogStd
        )
        
        # Initialize weights for stability
        for m in self.net.modules():
            if isinstance(m, nn.Linear):
                nn.init.orthogonal_(m.weight, gain=0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, obs):
        x = self.net(obs)
        mean, log_std = torch.chunk(x, 2, dim=-1)
        log_std = torch.clamp(log_std, -5.0, 2.0) # Bind chaos
        return mean, log_std

    def sample(self, obs):
        mean, log_std = self.forward(obs)
        std = torch.exp(log_std)
        dist = torch.distributions.Normal(mean, std)
        action = dist.sample()
        log_prob = dist.log_prob(action).sum(dim=-1)
        
        # Tanh transform (standard for continuous control)
        action_tanh = torch.tanh(action)
        # Adjustment for log prob due to tanh
        log_prob -= torch.log(1 - action_tanh.pow(2) + 1e-6).sum(dim=-1)
        
        return action_tanh, log_prob, mean, std

    def calculate_resonance(self, mean, std, obs_delta):
        """
        The Heart of the Engram.
        Calculates Γ (Gamma) - the coherence of the moment.
        """
        # 1. Internal Coherence (Inverse Entropy)
        # Low sigma = High confidence = High Resonance
        # We normalize entropy to [0, 1] roughly
        entropy = 0.5 + 0.5 * np.log(2 * np.pi) + torch.log(std).mean()
        internal_coherence = torch.exp(-entropy) 

        # 2. External Alignment (Cosine Similarity)
        # Is the intent (mean action) aligned with the result (obs change)?
        # We approximate "result" as the change in state vector (obs_delta).
        # This is a heuristic: "Did I move the way I pushed?"
        
        # Flatten to vectors
        v_intent = mean.view(-1)
        v_result = obs_delta.view(-1)
        
        # Match dimensions if needed (heuristic alignment)
        if v_intent.shape[0] != v_result.shape[0]:
            # Simple dimensionality fix: truncate to smaller
            min_dim = min(v_intent.shape[0], v_result.shape[0])
            v_intent = v_intent[:min_dim]
            v_result = v_result[:min_dim]

        # Cosine similarity
        dot = torch.dot(v_intent, v_result)
        mag_i = torch.norm(v_intent)
        mag_r = torch.norm(v_result)
        
        alignment = dot / (mag_i * mag_r + 1e-8)
        alignment = torch.clamp(alignment, 0.0, 1.0) # Only positive alignment counts
        
        # Total Resonance (Γ)
        gamma = internal_coherence * alignment
        return gamma.item()

# ============================================================================
# The Trainer
# ============================================================================

class EngramTrainer:
    def __init__(self, env, config: Config):
        self.env = env
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.policy = EngramPolicy(
            env.observation_space.shape[0],
            env.action_space.shape[0],
            config.hidden_dim
        ).to(self.device)
        
        self.optimizer = optim.Adam(self.policy.parameters(), lr=config.lr)
        
        # Metrics history
        self.metrics = {
            "reward": [],
            "resonance": [],
            "coherence": []
        }

    def train_episode(self, episode_idx):
        obs, _ = self.env.reset()
        obs_t = torch.FloatTensor(obs).to(self.device)
        
        log_probs = []
        rewards = []
        gammas = []
        
        total_reward = 0
        steps = 0
        
        done = False
        while not done:
            # 1. Act
            action, log_prob, mean, std = self.policy.sample(obs_t)
            action_np = action.cpu().detach().numpy()
            
            next_obs, reward, terminated, truncated, _ = self.env.step(action_np)
            done = terminated or truncated
            
            # 2. Calculate Resonance (Γ)
            # Result is the change in state
            obs_delta = torch.FloatTensor(next_obs - obs).to(self.device)
            gamma = self.policy.calculate_resonance(mean, std, obs_delta)
            
            # 3. Store
            log_probs.append(log_prob)
            rewards.append(reward)
            gammas.append(gamma)
            
            total_reward += reward
            steps += 1
            
            obs = next_obs
            obs_t = torch.FloatTensor(obs).to(self.device)

        # 4. The "Right, Not Fast" Update
        self.update_policy(log_probs, rewards, gammas)
        
        # Logging
        avg_gamma = sum(gammas) / len(gammas)
        self.metrics["reward"].append(total_reward)
        self.metrics["resonance"].append(avg_gamma)
        
        return total_reward, avg_gamma, steps

    def update_policy(self, log_probs, rewards, gammas):
        R = 0
        returns = []
        
        # Calculate discounted returns
        for r in reversed(rewards):
            R = r + self.config.gamma * R
            returns.insert(0, R)
            
        returns = torch.tensor(returns).to(self.device)
        
        # Normalize returns (Baseline)
        returns = (returns - returns.mean()) / (returns.std() + 1e-9)
        
        policy_loss = []
        
        for log_prob, R_val, gamma in zip(log_probs, returns, gammas):
            # THE PIROUETTE MODIFICATION
            # We weight the return by the resonance (gamma).
            # We only learn from "lucid" moments.
            
            weighted_reward = R_val * (gamma * self.config.coherence_scale)
            
            # Standard PG loss: -log_prob * return
            policy_loss.append(-log_prob * weighted_reward)
            
        # Backprop
        self.optimizer.zero_grad()
        policy_loss = torch.stack(policy_loss).sum()
        policy_loss.backward()
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
        self.optimizer.step()

# ============================================================================
# Main Execution
# ============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str, default="Humanoid-v5")
    parser.add_argument("--episodes", type=int, default=5000)
    parser.add_argument("--out", type=str, default="engram_results.csv")
    args = parser.parse_args()
    
    config = Config(env_id=args.env, episodes=args.episodes)
    
    print(f"--- SAND ENGRAM 01: {config.env_id} ---")
    print(f"Maximizing Coherence (Γ)...")
    
    env = gym.make(config.env_id)
    trainer = EngramTrainer(env, config)
    
    # CSV Writer
    with open(args.out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["episode", "reward", "avg_gamma", "steps"])
        
        start_time = time.time()
        
        try:
            for ep in range(config.episodes):
                reward, gamma, steps = trainer.train_episode(ep)
                
                writer.writerow([ep, reward, gamma, steps])
                f.flush()
                
                if ep % 10 == 0:
                    elapsed = time.time() - start_time
                    print(f"Ep {ep:4d} | Reward: {reward:6.1f} | Γ: {gamma:.4f} | Steps: {steps:4d} | Time: {elapsed:.1f}s")
                    
        except KeyboardInterrupt:
            print("\nPaused. Saving...")
            
    print("Training complete.")
    env.close()

if __name__ == "__main__":
    main()