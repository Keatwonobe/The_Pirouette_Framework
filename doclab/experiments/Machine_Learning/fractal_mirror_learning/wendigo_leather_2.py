#!/usr/bin/env python3
"""
wendigo_geodesic_mirage.py
---------------------------
Geodesic Navigation + Reverse Pareto + Mirage Module + Span-Aware Rollback

NEW ORGANS:
1. Mirage Module: Injects stochastic noise into prophet training based on local DR
2. Lagrangian Prophet: Predicts future ℒ_p trajectory instead of just DR
3. Span-Gated Learning: Modulates agent learning rate based on predictive span
4. Catastrophe Rollback: Reverts to last stable state when span collapses

The Mirage prevents premature crystallization. The Lagrangian gives richer signal.
"""
import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional
import json
import os
import time
import copy

# --------------------------------------------------------------------------- #
# CONFIGURATION
# --------------------------------------------------------------------------- #

TASK_CONFIGS = {
    'CartPole': {
        'env_id': 'CartPole-v1',
        'is_discrete': True,
        'mastery_threshold': 495,
        'max_episodes': 200,
        'mirage_base': 0.03,
        'mirage_gain': 1.2,
        'mirage_max': 0.55,
        'span_horizon': 20,
        'span_threshold': 5,  # Minimum span to trust learning
        'gamma_coherence': 1.5,
        'beta_duration': 0.05,
        'delta_dissonance': 1.0,
    },
    'Ant': {
        'env_id': 'Ant-v5',
        'is_discrete': False,
        'mastery_threshold': 5000,
        'max_episodes': 1000,
        'mirage_base': 0.05,
        'mirage_gain': 0.8,
        'mirage_max': 0.45,
        'span_horizon': 30,
        'span_threshold': 10,
        'gamma_coherence': 1.0,
        'beta_duration': 0.5,
        'delta_dissonance': 0.2,
    },
    'Humanoid': {
        'env_id': 'Humanoid-v5',
        'is_discrete': False,
        'mastery_threshold': 8000,
        'max_episodes': 2000,
        'mirage_base': 0.07,
        'mirage_gain': 0.6,
        'mirage_max': 0.40,
        'span_horizon': 40,
        'span_threshold': 15,
        'gamma_coherence': 0.8,
        'beta_duration': 1.0,
        'delta_dissonance': 0.1,
    }
}

GALLERY_DIR = "gallery_mirage"
os.makedirs(GALLERY_DIR, exist_ok=True)

# --------------------------------------------------------------------------- #
# DARK RESIDUE & LAGRANGIAN
# --------------------------------------------------------------------------- #

class UniversalDR:
    """Task-agnostic Dark Residue calculator with running statistics."""
    
    def __init__(self, obs_dim: int):
        self.obs_dim = obs_dim
        self.obs_scale = np.ones(obs_dim)
        self.obs_history = deque(maxlen=1000)
        
    def calculate(self, obs: np.ndarray, prev_obs: Optional[np.ndarray] = None) -> float:
        """Calculate DR from state deviation and velocity."""
        self.obs_history.append(obs)
        
        # Update scales periodically
        if len(self.obs_history) > 10 and len(self.obs_history) % 100 == 0:
            obs_array = np.array(list(self.obs_history))
            self.obs_scale = np.std(obs_array, axis=0) + 1e-6
        
        # State deviation
        dr = 0.3 * np.sum(np.abs(obs / self.obs_scale)) / self.obs_dim
        
        # Velocity component
        if prev_obs is not None:
            velocity = np.linalg.norm((obs - prev_obs) / self.obs_scale)
            dr += 0.7 * velocity
        
        return max(0.01, dr)


def calculate_lagrangian(dr: float, dr_derivative: float, 
                         gamma: float, beta: float, delta: float) -> float:
    """
    Calculate Pirouette Lagrangian: ℒ_p = K_τ - V_Γ
    
    K_τ (coherence): Gain from reducing DR
    V_Γ (pressure): Current DR state + cost of existence
    """
    coherence_gain = gamma * max(0, -dr_derivative)  # K_τ component
    temporal_pressure = delta * dr  # V_Γ component
    survival_bonus = beta  # Base existence term
    
    lagrangian = coherence_gain + survival_bonus - temporal_pressure
    return lagrangian


# --------------------------------------------------------------------------- #
# LAGRANGIAN PROPHET + MIRAGE MODULE
# --------------------------------------------------------------------------- #

class LagrangianProphet(nn.Module):
    """
    Predicts future Lagrangian trajectory ℒ_p(t+1:t+H).
    
    Richer signal than pure DR: captures coherence dynamics, not just state.
    """
    
    def __init__(self, obs_dim: int, horizon: int = 20, lr: float = 1e-3):
        super().__init__()
        self.horizon = horizon
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, horizon),
        )
        self.opt = optim.Adam(self.parameters(), lr=lr)
        self.loss_fn = nn.SmoothL1Loss()  # Huber loss - robust to outliers
        
        self.span_history = deque(maxlen=50)
        self.last_span = 0
        
    def train_with_mirage(self, x: np.ndarray, y_clean: np.ndarray, 
                          corruption_prob: float):
        """
        Train on corrupted signal to build robustness.
        
        Mirage: Inject static proportional to local chaos (DR).
        """
        # Create corruption mask
        mask = (np.random.rand(self.horizon) < corruption_prob).astype(np.float32)
        
        # Generate static scaled to signal
        signal_scale = np.std(y_clean) + 1e-3
        static = np.random.normal(loc=0.0, scale=signal_scale, size=self.horizon)
        
        # Corrupted target
        y_corrupted = y_clean * (1.0 - mask) + static * mask
        
        # Train
        x_t = torch.tensor(x, dtype=torch.float32).unsqueeze(0)
        y_t = torch.tensor(y_corrupted, dtype=torch.float32).unsqueeze(0)
        
        pred = self.net(x_t)
        loss = self.loss_fn(pred, y_t)
        
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()
        
        return float(loss.item())
    
    def measure_span(self, x: np.ndarray, y_true: np.ndarray, 
                     abs_err: float = 0.05, rel_err: float = 0.25) -> int:
        """
        Measure predictive span: how far ahead can we see clearly?
        
        Hybrid error: Accepts either absolute or relative accuracy.
        """
        x_t = torch.tensor(x, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            pred = self.net(x_t).squeeze(0).numpy()
        
        span = 0
        for i in range(len(y_true)):
            error = abs(pred[i] - y_true[i])
            threshold = max(abs_err, rel_err * (abs(y_true[i]) + 1e-6))
            
            if error <= threshold:
                span += 1
            else:
                break
        
        self.last_span = span
        self.span_history.append(span)
        return span
    
    def get_span_volatility(self) -> float:
        """Measure how much span is oscillating (sign of exploration)."""
        if len(self.span_history) < 5:
            return 0.0
        
        recent = list(self.span_history)[-10:]
        return float(np.std(recent))


# --------------------------------------------------------------------------- #
# SPAN-AWARE AGENT (with rollback)
# --------------------------------------------------------------------------- #

@dataclass
class Checkpoint:
    """Snapshot of agent state for rollback."""
    episode: int
    actor_state: Dict
    span: int
    avg_reward: float
    timestamp: float = field(default_factory=time.time)


class SpanAwareAgent:
    """
    SAC agent with span-gated learning and catastrophe rollback.
    
    Low span = don't trust learning
    Span collapse = rollback to last stable state
    """
    
    def __init__(self, env, config: Dict):
        self.env = env
        self.config = config
        self.agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))
        
        # Span-aware learning
        self.base_learning_rate = 3e-4
        self.span_threshold = config['span_threshold']
        
        # Checkpointing for rollback
        self.checkpoints: List[Checkpoint] = []
        self.max_checkpoints = 5
        
        # Statistics
        self.episode_rewards = deque(maxlen=50)
        
    def train_step(self, span: int, gradient_steps: int = 1):
        """
        Train with span-modulated learning rate.
        
        Low span → reduced learning (don't trust this data)
        """
        original_actor_lr = self.agent.policy.actor.optimizer.param_groups[0]['lr']
        original_critic_lr = self.agent.policy.critic.optimizer.param_groups[0]['lr']

        if span < self.span_threshold:
            # Reduce learning rate when blind
            lr_scale = span / self.span_threshold
            lr_scale = max(0.1, lr_scale)  # Never go below 10%
            
            # Temporarily modify optimizer learning rates
            for param_group in self.agent.policy.actor.optimizer.param_groups:
                param_group['lr'] = self.base_learning_rate * lr_scale
            for param_group in self.agent.policy.critic.optimizer.param_groups:
                param_group['lr'] = self.base_learning_rate * lr_scale
        
        self.agent.train(gradient_steps=gradient_steps)
        
        # Restore base learning rate
        for param_group in self.agent.policy.actor.optimizer.param_groups:
            param_group['lr'] = original_actor_lr
        for param_group in self.agent.policy.critic.optimizer.param_groups:
            param_group['lr'] = original_critic_lr
    
    def checkpoint(self, episode: int, span: int):
        """Save current state for potential rollback."""
        avg_reward = np.mean(list(self.episode_rewards)) if self.episode_rewards else 0.0
        
        checkpoint = Checkpoint(
            episode=episode,
            actor_state=copy.deepcopy(self.agent.policy.actor.state_dict()),
            span=span,
            avg_reward=avg_reward,
        )
        
        self.checkpoints.append(checkpoint)
        
        # Keep only recent checkpoints
        if len(self.checkpoints) > self.max_checkpoints:
            self.checkpoints.pop(0)
    
    def should_rollback(self, current_span: int, span_volatility: float) -> bool:
        """
        Detect catastrophic divergence.
        
        Triggers:
        - Span suddenly collapsed to near-zero
        - High span volatility (thrashing)
        """
        if not self.checkpoints:
            return False
        
        recent_spans = [cp.span for cp in self.checkpoints[-3:]]
        avg_recent_span = np.mean(recent_spans)
        
        # Catastrophic span collapse
        if current_span == 0 and avg_recent_span > 10:
            return True
        
        # Violent oscillation
        if span_volatility > 15:
            return True
        
        return False
    
    def rollback(self):
        """Revert to most stable checkpoint."""
        if not self.checkpoints:
            print("  ! No checkpoints available for rollback")
            return False
        
        # Find checkpoint with best span
        best_checkpoint = max(self.checkpoints, key=lambda cp: cp.span)
        
        print(f"  ! Rolling back to Episode {best_checkpoint.episode} "
              f"(span={best_checkpoint.span}, reward={best_checkpoint.avg_reward:.1f})")
        
        # Restore actor weights
        self.agent.policy.actor.load_state_dict(best_checkpoint.actor_state)
        
        # Clear checkpoints newer than rollback point
        self.checkpoints = [cp for cp in self.checkpoints 
                           if cp.episode <= best_checkpoint.episode]
        
        return True


# --------------------------------------------------------------------------- #
# DISCRETE → BOX WRAPPER
# --------------------------------------------------------------------------- #

class DiscreteToBoxWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
    
    def action(self, action: np.ndarray) -> int:
        return 0 if action[0] < 0.0 else 1


# --------------------------------------------------------------------------- #
# MAIN TRAINING LOOP
# --------------------------------------------------------------------------- #

def train_task(task_name: str, config: Dict):
    """Train with Mirage Module and Span-Aware Rollback."""
    
    print("\n" + "=" * 80)
    print(f"TASK: {task_name} ({config['env_id']})")
    print(f"Mirage: base={config['mirage_base']}, gain={config['mirage_gain']}, max={config['mirage_max']}")
    print(f"Span: horizon={config['span_horizon']}, threshold={config['span_threshold']}")
    print("=" * 80 + "\n")
    
    # Setup
    base_env = gym.make(config['env_id'])
    if config['is_discrete']:
        env = DiscreteToBoxWrapper(base_env)
    else:
        env = base_env
    
    obs_dim = env.observation_space.shape[0]
    
    # Organs
    dr_calc = UniversalDR(obs_dim)
    prophet = LagrangianProphet(obs_dim, horizon=config['span_horizon'])
    agent_wrapper = SpanAwareAgent(env, config)
    agent = agent_wrapper.agent

    new_logger = configure(f"./{GALLERY_DIR}/{task_name}_logs/", ["stdout", "csv"])
    agent.set_logger(new_logger)
    
    # Warmup
    print("Warming up replay buffer...")
    obs, _ = env.reset()
    for _ in range(5000):
        action = env.action_space.sample()
        next_obs, _, done, truncated, _ = env.step(action)
        agent.replay_buffer.add(obs, next_obs, action, 0.0, done or truncated, [{}])
        obs = next_obs
        if done or truncated:
            obs, _ = env.reset()
    print("Warmup complete.\n")
    
    # Training
    top_scores = []
    episode_rewards = []
    
    for ep in range(1, config['max_episodes'] + 1):
        obs, _ = env.reset()
        done, truncated = False, False
        
        episode_reward = 0.0
        episode_score = 0
        prev_obs = None
        previous_dr = dr_calc.calculate(obs)
        
        # Episode trajectory for prophet
        ep_obs = []
        ep_lagrangians = []
        
        while not done and not truncated:
            action, _ = agent.predict(obs, deterministic=True)
            next_obs, base_reward, done, truncated, _ = env.step(action)
            
            # Compute DR and Lagrangian
            current_dr = dr_calc.calculate(next_obs, prev_obs)
            dr_derivative = current_dr - previous_dr
            
            lagrangian = calculate_lagrangian(
                current_dr, 
                dr_derivative,
                config['gamma_coherence'],
                config['beta_duration'],
                config['delta_dissonance']
            )
            
            # Store trajectory
            ep_obs.append(obs.copy())
            ep_lagrangians.append(lagrangian)
            
            # Train with span-gated learning rate
            agent.replay_buffer.add(obs, next_obs, action, lagrangian, done or truncated, [{}])
            agent_wrapper.train_step(span=prophet.last_span, gradient_steps=1)
            
            episode_reward += lagrangian
            episode_score += 1
            prev_obs = obs
            obs = next_obs
            previous_dr = current_dr
        
        # Train prophet with mirage
        if len(ep_obs) > 2:
            ep_lagrangians = np.array(ep_lagrangians, dtype=np.float32)
            
            for t in range(len(ep_obs) - 1):
                x = ep_obs[t]
                
                # Build clean future
                future_clean = []
                for k in range(1, config['span_horizon'] + 1):
                    idx = t + k
                    if idx < len(ep_lagrangians):
                        future_clean.append(ep_lagrangians[idx])
                    else:
                        future_clean.append(ep_lagrangians[-1])
                future_clean = np.array(future_clean, dtype=np.float32)
                
                # Compute corruption based on local DR
                local_dr = dr_calc.calculate(ep_obs[t])
                corruption = config['mirage_base'] + config['mirage_gain'] * local_dr
                corruption = min(config['mirage_max'], corruption)
                
                # Train with mirage
                prophet.train_with_mirage(x, future_clean, corruption)
            
            # Measure span on clean signal
            x0 = ep_obs[0]
            future_clean_0 = []
            for k in range(1, config['span_horizon'] + 1):
                if k < len(ep_lagrangians):
                    future_clean_0.append(ep_lagrangians[k])
                else:
                    future_clean_0.append(ep_lagrangians[-1])
            future_clean_0 = np.array(future_clean_0, dtype=np.float32)
            
            span = prophet.measure_span(x0, future_clean_0)
        else:
            span = prophet.last_span
        
        # Track performance
        episode_rewards.append(episode_reward)
        agent_wrapper.episode_rewards.append(episode_reward)
        top_scores.append(episode_score)
        top_scores.sort(reverse=True)
        top_scores = top_scores[:15]
        
        # Checkpoint periodically
        if ep % 10 == 0:
            agent_wrapper.checkpoint(ep, span)
        
        # Check for catastrophic divergence
        span_volatility = prophet.get_span_volatility()
        if agent_wrapper.should_rollback(span, span_volatility):
            print(f"\n{'!' * 80}")
            print(f"CATASTROPHIC DIVERGENCE DETECTED at Episode {ep}")
            print(f"Span={span}, Volatility={span_volatility:.1f}")
            print(f"{'!' * 80}")
            agent_wrapper.rollback()
            print()
        
        # Report
        avg_top = np.mean(top_scores)
        avg_reward = np.mean(list(agent_wrapper.episode_rewards)[-10:])
        
        print(
            f"Ep {ep:04d} | "
            f"Score={episode_score:4d} | "
            f"Reward={episode_reward:7.1f} | "
            f"Span={span:2d}/{config['span_horizon']} | "
            f"SpanVol={span_volatility:4.1f} | "
            f"Top15={avg_top:6.1f} | "
            f"AvgR={avg_reward:7.1f}"
        )
        
        # Check mastery
        if len(top_scores) == 15 and avg_top >= config['mastery_threshold']:
            print(f"\n{'*' * 80}")
            print(f"*** MASTERY ACHIEVED for {task_name} at episode {ep} ***")
            print(f"Top-15 Average: {avg_top:.1f}")
            print(f"Final Span: {span}/{config['span_horizon']}")
            print(f"{'*' * 80}\n")
            
            agent.save(os.path.join(GALLERY_DIR, f"{task_name}_mastery.zip"))
            break
    
    env.close()


# --------------------------------------------------------------------------- #
# MAIN
# --------------------------------------------------------------------------- #

def main():
    print("=" * 80)
    print("WENDIGO MIRAGE: Geodesic + Lagrangian Prophet + Span-Aware Rollback")
    print("=" * 80)
    
    # Start with CartPole
    train_task('CartPole', TASK_CONFIGS['CartPole'])
    
    # Then try Ant
    try:
        train_task('Ant', TASK_CONFIGS['Ant'])
    except KeyboardInterrupt:
        print("\nTraining interrupted.")
    except Exception as e:
        print(f"\nAnt training failed: {e}")


if __name__ == "__main__":
    main()