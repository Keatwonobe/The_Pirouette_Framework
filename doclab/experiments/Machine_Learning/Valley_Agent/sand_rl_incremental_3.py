#!/usr/bin/env python3
"""
Sand RL Incremental - BOMB PROOF Edition
========================================

Lightweight RL trainer for Ant-v5 and Humanoid-v5 that:
- Writes metrics incrementally (no memory buildup)
- Checkpoints every N episodes
- Resumes from exact point of crash
- Tracks Pirouette metrics (Γ, DR, S) during execution
- Can run indefinitely

Inspired by sand_agent_sand.py incremental writing pattern.
"""

import argparse
import csv
import json
import signal
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional
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
    """Lightweight RL configuration."""
    # Environment
    env_id: str = "Humanoid-v5"
    max_steps: int = 2000
    
    # Training
    episodes: int = 10000
    gamma: float = 0.99
    lr: float = 3e-4
    
    # Early stopping
    early_stop_reward: Optional[float] = None  # Set to enable (e.g., 950 for Ant)
    
    # Network
    hidden_dim: int = 256
    
    # Checkpointing
    checkpoint_interval: int = 50  # Save every N episodes
    metric_log_interval: int = 10  # Write metrics every N episodes
    
    # Pirouette metrics
    compute_sand_metrics: bool = True


# ============================================================================
# Incremental Writers (Bomb-Proof Pattern)
# ============================================================================

class IncrementalMetricsWriter:
    """
    Writes episode metrics one at a time, flushes immediately.
    Zero memory accumulation.
    """
    
    def __init__(self, output_path: Path):
        self.output_path = Path(output_path)
        
        # Open CSV writer with line buffering
        self.file_exists = self.output_path.exists()
        self.csv_file = open(self.output_path, 'a', newline='', buffering=1)
        
        # Columns
        self.columns = [
            'episode', 'total_reward', 'steps', 'avg_DR', 'avg_S', 'avg_Gamma',
            'final_DR', 'coherence_proxy', 'valley_count_estimate', 'elapsed_time'
        ]
        
        # Write header if new file
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=self.columns)
        if not self.file_exists:
            self.csv_writer.writeheader()
            self.csv_file.flush()
    
    def write_episode(self, episode_data: dict):
        """Write single episode metrics immediately."""
        self.csv_writer.writerow(episode_data)
        self.csv_file.flush()
    
    def close(self):
        """Close file handle."""
        self.csv_file.close()


class CheckpointManager:
    """
    Manages checkpoints and resume state.
    """
    
    def __init__(self, checkpoint_dir: Path):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.checkpoint_dir / 'training_state.json'
    
    def save_checkpoint(self, episode: int, policy_state: dict, value_state: dict,
                       policy_optimizer_state: dict, value_optimizer_state: dict, 
                       metrics: dict):
        """Save checkpoint atomically."""
        # Save policy, value, and optimizers
        checkpoint = {
            'episode': episode,
            'policy_state': policy_state,
            'value_state': value_state,
            'policy_optimizer_state': policy_optimizer_state,
            'value_optimizer_state': value_optimizer_state,
            'metrics': metrics
        }
        
        checkpoint_path = self.checkpoint_dir / f'checkpoint_ep{episode}.pt'
        torch.save(checkpoint, checkpoint_path)
        
        # Update state file
        state = {
            'last_episode': episode,
            'last_checkpoint': str(checkpoint_path)
        }
        
        with open(self.state_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_checkpoint(self) -> Optional[dict]:
        """Load latest checkpoint if exists."""
        if not self.state_path.exists():
            return None
        
        with open(self.state_path, 'r') as f:
            state = json.load(f)
        
        checkpoint_path = Path(state['last_checkpoint'])
        if not checkpoint_path.exists():
            return None
        
        checkpoint = torch.load(checkpoint_path)
        print(f"\n✓ Resuming from episode {checkpoint['episode']}")
        return checkpoint
    
    def get_start_episode(self) -> int:
        """Get episode to start from (0 if new, last+1 if resuming)."""
        if not self.state_path.exists():
            return 0
        
        with open(self.state_path, 'r') as f:
            state = json.load(f)
        return state['last_episode'] + 1


# ============================================================================
# Policy and Value Networks (Actor-Critic)
# ============================================================================

class GaussianPolicy(nn.Module):
    """Simple Gaussian policy for continuous control."""
    
    def __init__(self, obs_dim: int, action_dim: int, hidden_dim: int = 256):
        super().__init__()
        self.action_dim = action_dim
        
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 2 * action_dim)
        )
        
        # Initialize last layer small
        with torch.no_grad():
            self.net[-1].weight *= 0.01
            self.net[-1].bias[action_dim:].fill_(-1.0)  # log_std starts low
    
    def forward(self, obs):
        """Returns mean and log_std."""
        out = self.net(obs)
        mean, log_std = torch.chunk(out, 2, dim=-1)
        log_std = torch.clamp(log_std, -5.0, 2.0)
        return mean, log_std
    
    def sample_action(self, obs):
        """Sample action with log probability."""
        mean, log_std = self.forward(obs)
        std = torch.exp(log_std)
        
        eps = torch.randn_like(mean)
        pre_tanh = mean + std * eps
        action = torch.tanh(pre_tanh)
        
        # Log probability
        log_prob = -0.5 * ((eps**2) + 2 * log_std + np.log(2 * np.pi))
        log_prob = log_prob.sum(dim=-1, keepdim=True)
        
        # Correction for tanh
        log_prob -= torch.log(1 - action**2 + 1e-6).sum(dim=-1, keepdim=True)
        
        return action, log_prob


class ValueNetwork(nn.Module):
    """Baseline value function to reduce variance."""
    
    def __init__(self, obs_dim: int, hidden_dim: int = 256):
        super().__init__()
        
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, obs):
        """Returns state value estimate."""
        return self.net(obs)


# ============================================================================
# Pirouette Metrics Computer (Lightweight)
# ============================================================================

class SandMetrics:
    """
    Lightweight Pirouette metrics computation during RL execution.
    
    Tracks coherence, DR, S, Gamma using only policy and reward signals.
    """
    
    def __init__(self, obs_dim: int, action_dim: int):
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        self.reset()
    
    def reset(self):
        """Reset for new episode."""
        self.rewards = []
        self.actions = []
        self.obs_history = []
        
        self.DR_history = []
        self.S_history = []
        self.Gamma_history = []
    
    def update(self, obs, action, reward, done):
        """Update metrics for current timestep."""
        self.rewards.append(reward)
        self.actions.append(action)
        self.obs_history.append(obs)
        
        # Compute Pirouette-inspired metrics
        
        # Dark Residue (DR): Unexplained variance in reward
        if len(self.rewards) > 5:
            recent_rewards = self.rewards[-5:]
            expected_reward = np.mean(recent_rewards)
            DR = abs(reward - expected_reward) / (abs(expected_reward) + 1e-6)
        else:
            DR = 0.5  # Default
        
        # Surprise (S): Observation change magnitude
        if len(self.obs_history) > 1:
            obs_diff = np.linalg.norm(obs - self.obs_history[-2])
            S = np.clip(obs_diff, 0, 5)
        else:
            S = 0.0
        
        # Gamma (Γ): Temporal pressure (inverse of reward smoothness)
        if len(self.rewards) > 3:
            reward_variance = np.var(self.rewards[-3:])
            Gamma = np.clip(reward_variance, 0, 2)
        else:
            Gamma = 0.5
        
        self.DR_history.append(DR)
        self.S_history.append(S)
        self.Gamma_history.append(Gamma)
    
    def get_episode_summary(self) -> dict:
        """Get summary metrics for episode."""
        return {
            'avg_DR': np.mean(self.DR_history) if self.DR_history else 0,
            'avg_S': np.mean(self.S_history) if self.S_history else 0,
            'avg_Gamma': np.mean(self.Gamma_history) if self.Gamma_history else 0,
            'final_DR': self.DR_history[-1] if self.DR_history else 0,
            'coherence_proxy': 1.0 - np.mean(self.DR_history) if self.DR_history else 0.5,
            'valley_count_estimate': self._estimate_valleys()
        }
    
    def _estimate_valleys(self) -> int:
        """
        Estimate number of valley-like events in episode.
        
        A valley is: DR spike → coherence drop → recovery
        """
        if len(self.DR_history) < 40:
            return 0
        
        valleys = 0
        i = 0
        while i < len(self.DR_history) - 40:
            # Look for DR spike
            if self.DR_history[i] > 0.3:
                # Check for recovery window
                window = self.DR_history[i:i+40]
                if len(window) > 20:
                    early = np.mean(window[:10])
                    late = np.mean(window[-10:])
                    if late < early * 0.8:  # 20% reduction
                        valleys += 1
                        i += 40  # Skip past this valley
                        continue
            i += 1
        
        return valleys


# ============================================================================
# Actor-Critic Trainer (Stable, Anti-Forgetting)
# ============================================================================

class ActorCriticTrainer:
    """
    Actor-Critic with baseline to prevent catastrophic forgetting.
    
    Key anti-forgetting features:
    - Value baseline (reduces variance)
    - Entropy regularization (maintains exploration)
    - Experience buffer (learns from multiple episodes)
    - Gradient clipping (prevents large destructive updates)
    - Adaptive normalization (doesn't penalize success)
    """
    
    def __init__(self, policy: GaussianPolicy, config: Config, device: str = 'cpu'):
        self.policy = policy
        self.value = ValueNetwork(policy.net[0].in_features, config.hidden_dim).to(device)
        self.config = config
        self.device = device
        
        # Separate optimizers (different learning rates)
        self.policy_optimizer = optim.Adam(policy.parameters(), lr=config.lr)
        self.value_optimizer = optim.Adam(self.value.parameters(), lr=config.lr * 3)
        
        # Experience buffer (prevents forgetting)
        self.buffer_size = 10  # Keep last 10 episodes
        self.episode_buffer = []
        
        # Performance tracking (for buffer health check)
        self.best_avg_reward = -float('inf')
        self.recent_rewards_for_buffer = []
        
        # Entropy coefficient (decays over time but never too low)
        self.entropy_coef = 0.01
        self.entropy_decay = 0.99995  # Slower decay
        self.entropy_floor = 0.005  # CRITICAL: Never go below this
    
    def train_episode(self, env, metrics_tracker: Optional[SandMetrics] = None):
        """
        Run single episode and update policy with baseline.
        
        Returns episode metrics.
        """
        obs, _ = env.reset()
        if metrics_tracker:
            metrics_tracker.reset()
        
        episode_obs = []
        episode_actions = []
        episode_rewards = []
        episode_log_probs = []
        episode_values = []
        steps = 0
        
        for step in range(self.config.max_steps):
            # Convert to tensor
            obs_t = torch.FloatTensor(obs).unsqueeze(0).to(self.device)
            
            # Sample action (with gradients for policy loss)
            action, log_prob = self.policy.sample_action(obs_t)
            
            # Get value estimate (with gradients for value loss)
            value = self.value(obs_t)
            
            # Detach for environment
            action_np = action.detach().cpu().numpy()[0]
            
            # Environment step
            next_obs, reward, terminated, truncated, info = env.step(action_np)
            done = terminated or truncated
            
            # Store transition
            episode_obs.append(obs_t)
            episode_actions.append(action)
            episode_rewards.append(reward)
            episode_log_probs.append(log_prob)
            episode_values.append(value)
            
            if metrics_tracker:
                metrics_tracker.update(obs, action_np, reward, done)
            
            obs = next_obs
            steps += 1
            
            if done:
                break
        
        # Compute returns
        returns = []
        G = 0
        for r in reversed(episode_rewards):
            G = r + self.config.gamma * G
            returns.insert(0, G)
        
        returns = torch.FloatTensor(returns).unsqueeze(1).to(self.device)
        
        # Stack tensors
        obs_batch = torch.cat(episode_obs)
        log_probs = torch.cat(episode_log_probs)
        values = torch.cat(episode_values)
        
        # Compute advantages (returns - baseline)
        advantages = returns - values.detach()
        
        # Normalize advantages (but preserve sign!)
        if len(advantages) > 1:
            adv_mean = advantages.mean()
            adv_std = advantages.std() + 1e-8
            advantages = (advantages - adv_mean) / adv_std
        
        # Clip advantages to prevent catastrophic updates (FIX 4)
        advantages = torch.clamp(advantages, -10, 10)
        
        # Policy loss (with entropy bonus)
        mean, log_std = self.policy(obs_batch)
        entropy = -(log_std + 0.5 * np.log(2 * np.pi * np.e)).sum(dim=-1).mean()
        
        policy_loss = -(log_probs * advantages.detach()).mean()
        policy_loss -= self.entropy_coef * entropy  # Encourage exploration
        
        # Value loss (with clipping to prevent divergence)
        value_loss_raw = (returns - values) ** 2
        value_loss = torch.clamp(value_loss_raw, 0, 100).mean()  # Clip extreme losses
        
        # Update policy
        self.policy_optimizer.zero_grad()
        policy_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
        self.policy_optimizer.step()
        
        # Update value
        self.value_optimizer.zero_grad()
        value_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.value.parameters(), 0.5)
        self.value_optimizer.step()
        
        # Multi-episode learning (anti-forgetting)
        self.episode_buffer.append({
            'obs': obs_batch,
            'returns': returns,
            'log_probs': log_probs.detach(),
        })
        
        if len(self.episode_buffer) > self.buffer_size:
            self.episode_buffer.pop(0)
        
        # Return episode metrics
        total_reward = sum(episode_rewards)

        # Buffer health check (FIX 3)
        self.recent_rewards_for_buffer.append(total_reward)
        if len(self.recent_rewards_for_buffer) > 50:
            self.recent_rewards_for_buffer.pop(0)
        
        if len(self.recent_rewards_for_buffer) >= 20:
            recent_avg = np.mean(self.recent_rewards_for_buffer[-20:])
            self.best_avg_reward = max(self.best_avg_reward, recent_avg)
            
            # Clear buffer if catastrophic performance drop
            if recent_avg < 0.3 * self.best_avg_reward and self.best_avg_reward > 0:
                print(f"\n  ⚠ Buffer cleared! Performance dropped: {recent_avg:.0f} < 30% of best ({self.best_avg_reward:.0f})")
                self.episode_buffer.clear()
                self.recent_rewards_for_buffer.clear()
        
        # Learn from buffer every few episodes
        if len(self.episode_buffer) >= 5:
            self._replay_buffer()
        
        # Decay entropy (but respect floor)
        self.entropy_coef = max(self.entropy_floor, self.entropy_coef * self.entropy_decay)
        
        result = {
            'total_reward': total_reward,
            'steps': steps,
            'loss': policy_loss.item(),
            'value_loss': value_loss.item(),
            'entropy': entropy.item(),
            'entropy_coef': self.entropy_coef,
        }
        
        if metrics_tracker:
            result.update(metrics_tracker.get_episode_summary())
        
        return result
    
    def _replay_buffer(self):
        """
        Learn from past episodes to prevent forgetting.
        
        This is the key anti-forgetting mechanism.
        """
        if len(self.episode_buffer) < 3:
            return
        
        # Sample random subset of buffer
        import random
        sample_size = min(3, len(self.episode_buffer))
        sampled = random.sample(self.episode_buffer, sample_size)
        
        for episode_data in sampled:
            obs_batch = episode_data['obs']
            returns = episode_data['returns']
            
            # Recompute values
            values = self.value(obs_batch)
            
            # Value loss only (don't update policy on old data)
            value_loss = ((returns - values) ** 2).mean()
            
            self.value_optimizer.zero_grad()
            value_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.value.parameters(), 0.5)
            self.value_optimizer.step()


# ============================================================================
# Main Training Loop (Bomb-Proof)
# ============================================================================

class IncrementalRLTrainer:
    """
    Main training orchestrator using incremental pattern.
    
    Features:
    - Checkpoints every N episodes
    - Writes metrics incrementally
    - Handles interrupts gracefully
    - Resumes from exact point
    """
    
    def __init__(self, config: Config, output_dir: Path):
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup components
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"\nDevice: {self.device}")
        
        # Environment
        self.env = gym.make(config.env_id)
        obs_dim = self.env.observation_space.shape[0]
        action_dim = self.env.action_space.shape[0]
        
        print(f"Environment: {config.env_id}")
        print(f"  Observation dim: {obs_dim}")
        print(f"  Action dim: {action_dim}")
        
        # Policy and Value
        self.policy = GaussianPolicy(obs_dim, action_dim, config.hidden_dim).to(self.device)
        
        # Trainer (Actor-Critic with anti-forgetting)
        self.trainer = ActorCriticTrainer(self.policy, config, self.device)
        
        # Metrics
        self.metrics_writer = IncrementalMetricsWriter(
            self.output_dir / 'episode_metrics.csv'
        )
        
        # Checkpoints
        self.checkpoint_mgr = CheckpointManager(self.output_dir / 'checkpoints')
        
        # Sand metrics (optional)
        self.sand_metrics = SandMetrics(obs_dim, action_dim) if config.compute_sand_metrics else None
        
        # Resume state
        self.start_episode = self.checkpoint_mgr.get_start_episode()
        checkpoint = self.checkpoint_mgr.load_checkpoint()
        if checkpoint:
            self.policy.load_state_dict(checkpoint['policy_state'])
            self.trainer.value.load_state_dict(checkpoint['value_state'])
            self.trainer.policy_optimizer.load_state_dict(checkpoint['policy_optimizer_state'])
            self.trainer.value_optimizer.load_state_dict(checkpoint['value_optimizer_state'])
        
        # Interrupt handling
        self.interrupted = False
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        self.interrupted = True
        print("\n\n⚠ Interrupt received - finishing current episode...")
    
    def train(self):
        """Main training loop."""
        print("\n" + "="*70)
        print("SAND RL INCREMENTAL - BOMB PROOF MODE")
        print("="*70)
        print(f"\nTotal episodes: {self.config.episodes}")
        print(f"Output: {self.output_dir}")
        print(f"Checkpoints every: {self.config.checkpoint_interval} episodes")
        print(f"\nPress Ctrl+C to pause (safe to resume)")
        
        if self.start_episode > 0:
            print(f"\n✓ Resuming from episode {self.start_episode}")
        
        print(f"\nStarting training...")
        
        start_time = time.time()
        last_checkpoint_time = start_time
        
        recent_rewards = []
        
        try:
            for ep in range(self.start_episode, self.config.episodes):
                if self.interrupted:
                    print(f"\nStopping at episode {ep}")
                    break
                
                # Train episode
                ep_start = time.time()
                ep_metrics = self.trainer.train_episode(self.env, self.sand_metrics)
                ep_time = time.time() - ep_start
                
                # Track recent performance
                recent_rewards.append(ep_metrics['total_reward'])
                if len(recent_rewards) > 100:
                    recent_rewards.pop(0)
                
                # Write metrics
                if (ep + 1) % self.config.metric_log_interval == 0:
                    metric_data = {
                        'episode': ep,
                        'total_reward': ep_metrics['total_reward'],
                        'steps': ep_metrics['steps'],
                        'avg_DR': ep_metrics.get('avg_DR', 0),
                        'avg_S': ep_metrics.get('avg_S', 0),
                        'avg_Gamma': ep_metrics.get('avg_Gamma', 0),
                        'final_DR': ep_metrics.get('final_DR', 0),
                        'coherence_proxy': ep_metrics.get('coherence_proxy', 0),
                        'valley_count_estimate': ep_metrics.get('valley_count_estimate', 0),
                        'elapsed_time': ep_time
                    }
                    self.metrics_writer.write_episode(metric_data)
                
                # Progress report
                if (ep + 1) % 10 == 0:
                    avg_reward = np.mean(recent_rewards[-10:]) if recent_rewards else 0
                    avg_reward_100 = np.mean(recent_rewards) if len(recent_rewards) >= 100 else avg_reward
                    
                    print(f"  Episode {ep+1:5d}/{self.config.episodes} | "
                          f"Reward: {ep_metrics['total_reward']:7.1f} | "
                          f"Avg(10): {avg_reward:7.1f} | "
                          f"Steps: {ep_metrics['steps']:4d}")
                    
                    # Early stopping check (FIX 5)
                    if self.config.early_stop_reward is not None:
                        if avg_reward_100 >= self.config.early_stop_reward:
                            print(f"\n🎯 Performance target reached! Avg reward: {avg_reward_100:.1f}")
                            print(f"   Stopping early at episode {ep+1}")
                            break
                
                # Checkpoint
                if (ep + 1) % self.config.checkpoint_interval == 0:
                    checkpoint_metrics = {
                        'avg_reward_last_100': np.mean(recent_rewards) if recent_rewards else 0
                    }
                    
                    self.checkpoint_mgr.save_checkpoint(
                        ep,
                        self.policy.state_dict(),
                        self.trainer.value.state_dict(),
                        self.trainer.policy_optimizer.state_dict(),
                        self.trainer.value_optimizer.state_dict(),
                        checkpoint_metrics
                    )
                    
                    elapsed = time.time() - last_checkpoint_time
                    print(f"\n  ✓ Checkpoint saved (ep {ep}, {elapsed:.1f}s since last)\n")
                    last_checkpoint_time = time.time()
        
        finally:
            # Always close cleanly
            self.metrics_writer.close()
            self.env.close()
            
            total_time = time.time() - start_time
            episodes_trained = (ep + 1) - self.start_episode
            
            print(f"\n{'='*70}")
            print(f"SESSION COMPLETE")
            print(f"{'='*70}")
            print(f"  Episodes trained: {episodes_trained}")
            print(f"  Total episodes: {ep+1}/{self.config.episodes}")
            print(f"  Time: {total_time:.1f}s ({total_time/episodes_trained:.1f}s/ep)")
            
            if ep + 1 >= self.config.episodes:
                print(f"\n✓ ALL EPISODES COMPLETE!")
            else:
                print(f"\n⚠ Paused at episode {ep+1}")
                print(f"  To resume: rerun the same command")
            
            # Final checkpoint
            if episodes_trained > 0:
                self.checkpoint_mgr.save_checkpoint(
                    ep,
                    self.policy.state_dict(),
                    self.trainer.value.state_dict(),
                    self.trainer.policy_optimizer.state_dict(),
                    self.trainer.value_optimizer.state_dict(),
                    {'final': True}
                )
                print(f"  Final checkpoint saved")


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Sand RL Incremental - Bomb-proof RL training"
    )
    parser.add_argument(
        '--env',
        type=str,
        default='Humanoid-v5',
        choices=['Ant-v5', 'Humanoid-v5'],
        help="Environment to train on"
    )
    parser.add_argument(
        '--episodes',
        type=int,
        default=10000,
        help="Total episodes to train (default: 10000)"
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('./rl_incremental_output'),
        help="Output directory for checkpoints and metrics"
    )
    parser.add_argument(
        '--checkpoint-interval',
        type=int,
        default=50,
        help="Save checkpoint every N episodes (default: 50)"
    )
    parser.add_argument(
        '--no-sand-metrics',
        action='store_true',
        help="Disable Pirouette sand metrics computation"
    )
    parser.add_argument(
        '--hidden-dim',
        type=int,
        default=256,
        help="Policy network hidden dimension (default: 256)"
    )
    parser.add_argument(
        '--lr',
        type=float,
        default=3e-4,
        help="Learning rate (default: 3e-4)"
    )
    parser.add_argument(
        '--early-stop',
        type=float,
        default=None,
        help="Stop training when avg reward reaches this value (default: None = no early stop)"
    )
    
    args = parser.parse_args()
    
    # Create config
    config = Config(
        env_id=args.env,
        episodes=args.episodes,
        checkpoint_interval=args.checkpoint_interval,
        compute_sand_metrics=not args.no_sand_metrics,
        hidden_dim=args.hidden_dim,
        lr=args.lr,
        early_stop_reward=args.early_stop
    )
    
    # Create trainer
    trainer = IncrementalRLTrainer(config, args.output_dir)
    
    # Train
    trainer.train()


if __name__ == '__main__':
    main()
