"""
Pirouette Synthesis Agent - The Monster Mash
=============================================
Combining: Wanderer's manifold architecture, Wendigo's multi-objective SAC,
Skogsvätt's triadic operators, and Sand Agent's coherence metrics.

Architecture:
- Bilateral hemispheric structure (left=critic, right=actor)
- Triadic operator dynamics with phase gating
- Multi-objective coherence-based reward shaping
- Forward ratchet mechanism for anti-backsliding
- Dark residue optimization with autopoietic prediction
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import gymnasium as gym
import numpy as np
from collections import deque
from dataclasses import dataclass

# ============================================================================
# Pirouette Framework Configuration
# ============================================================================

@dataclass
class PirouetteConfig:
    """Unified configuration for all Pirouette subsystems."""
    # Triadic operator weights (from Sand Agent)
    eta_P: float = 0.05
    eta_S: float = 0.02
    eta_Q: float = 0.08
    eta_C: float = 0.03
    eta_B: float = 0.10
    
    # Precision function parameters
    alpha_0: float = -1.0
    alpha_S: float = 1.2
    alpha_DR: float = 0.8
    alpha_Gamma: float = 0.3
    
    # Phase gating (from Skogsvätt)
    omega: float = 0.25 * np.pi
    update_window: tuple = (0.0, np.pi / 2)
    
    # Resonance sharpening (from Wanderer)
    critical_resonance_scale: float = 10.0
    enthalpy_floor: float = 0.05
    ratchet_tolerance: float = 0.15
    
    # Multi-objective reward weights (from Wendigo)
    gamma_coherence: float = 1.5
    beta_duration: float = 0.05
    delta_dissonance: float = 1.0
    
    # Dark Residue thresholds
    DR_shadow: float = 1.5
    
    # Network dimensions
    manifold_dim: int = 128
    hidden_dim: int = 256


# ============================================================================
# Bilateral Hemispheric Manifold Network
# ============================================================================

class BilateralManifold(nn.Module):
    """
    Dual-hemisphere architecture with autopoietic prediction.
    
    Left Hemisphere: Critic (value estimation, stability assessment)
    Right Hemisphere: Actor (action selection, motor control)
    Corpus Callosum: Shared manifold space for inter-hemispheric transfer
    """
    
    def __init__(self, state_dim: int, action_dim: int, config: PirouetteConfig):
        super().__init__()
        self.config = config
        self.manifold_dim = config.manifold_dim
        
        # Shared perception layer
        self.perception = nn.Sequential(
            nn.Linear(state_dim, config.hidden_dim),
            nn.LayerNorm(config.hidden_dim),
            nn.Tanh()
        )
        
        # LEFT HEMISPHERE: Critic pathway
        self.left_encoder = nn.Sequential(
            nn.Linear(config.hidden_dim, config.manifold_dim),
            nn.LayerNorm(config.manifold_dim),
            nn.ReLU()
        )
        self.critic = nn.Linear(config.manifold_dim, 1)
        
        # RIGHT HEMISPHERE: Actor pathway
        self.right_encoder = nn.Sequential(
            nn.Linear(config.hidden_dim, config.manifold_dim),
            nn.LayerNorm(config.manifold_dim),
            nn.ReLU()
        )
        self.actor_mean = nn.Linear(config.manifold_dim, action_dim)
        self.actor_log_std = nn.Linear(config.manifold_dim, action_dim)
        
        # CORPUS CALLOSUM: Shared manifold bridge
        self.corpus_callosum = nn.Sequential(
            nn.Linear(config.manifold_dim * 2, config.manifold_dim),
            nn.LayerNorm(config.manifold_dim),
            nn.ReLU()
        )
        
        # AUTOPOIETIC PREDICTOR: Self-prediction head
        self.autopoiesis_predictor = nn.Linear(config.manifold_dim, config.manifold_dim)
        
    def forward(self, x):
        """
        Forward pass through bilateral architecture.
        
        Returns:
            action_mean: Mean of action distribution
            action_log_std: Log std of action distribution
            value: State value estimate
            unified_manifold: Unified representation
            predicted_next: Autopoietic prediction
            left_manifold: Left hemisphere state
            right_manifold: Right hemisphere state
        """
        # Shared perception
        perceived = self.perception(x)
        
        # Bilateral encoding
        left_manifold = self.left_encoder(perceived)
        right_manifold = self.right_encoder(perceived)
        
        # Hemispheric outputs
        value = self.critic(left_manifold)
        action_mean = self.actor_mean(right_manifold)
        action_log_std = self.actor_log_std(right_manifold)
        action_log_std = torch.clamp(action_log_std, -20, 2)
        
        # Unified manifold via corpus callosum
        unified_manifold = self.corpus_callosum(
            torch.cat([left_manifold, right_manifold], dim=-1)
        )
        
        # Autopoietic prediction
        predicted_next = self.autopoiesis_predictor(unified_manifold)
        
        return (action_mean, action_log_std, value, unified_manifold, 
                predicted_next, left_manifold, right_manifold)


# ============================================================================
# Triadic Operator Dynamics
# ============================================================================

class TriadicOperator:
    """
    Implements the triadic operator from Pirouette Framework.
    O = O_P + O_S + O_C
    
    Where:
    O_P: Precision-weighted gradient (active inference)
    O_S: Stochastic exploration (entropy injection)
    O_C: Coherence optimization (Q, C, B terms)
    """
    
    def __init__(self, config: PirouetteConfig):
        self.config = config
        self.phi = 0.0  # Phase accumulator
        
    def compute_metrics(self, obs: np.ndarray, obs_prev: np.ndarray):
        """Compute Pirouette metrics from observations."""
        # Dark Residue (instability measure)
        if len(obs) == 4:  # CartPole
            cart_pos, cart_vel, pole_angle, pole_vel = obs
            DR = 0.4 * abs(cart_pos) + 0.2 * abs(cart_vel) + 1.5 * abs(pole_angle) + 0.3 * abs(pole_vel)
        else:
            DR = np.linalg.norm(obs) ** 2
        
        # Transition rate (magnitude of state change)
        S = np.linalg.norm(obs - obs_prev)
        
        # Coherence gain (DR reduction)
        DR_prev = np.linalg.norm(obs_prev) ** 2
        Q = max(0.0, DR_prev - DR)
        
        # Coherence contrast (DR change magnitude)
        C = abs(DR - DR_prev)
        
        # Boundary crossing (danger zone)
        B = 1.0 if DR > self.config.DR_shadow else 0.0
        
        return DR, S, Q, C, B
    
    def compute_precision(self, DR: float, S: float, Gamma: float):
        """Precision function: π = σ(α₀ + α_S·S - α_DR·DR - α_Γ·Γ)"""
        cfg = self.config
        logit = cfg.alpha_0 + cfg.alpha_S * S - cfg.alpha_DR * DR - cfg.alpha_Gamma * Gamma
        return 1.0 / (1.0 + np.exp(-logit))
    
    def phase_gate(self):
        """Compute phase gate value."""
        self.phi = (self.phi + self.config.omega + 0.1 * np.random.randn()) % (2 * np.pi)
        g = 1.0 if self.config.update_window[0] <= self.phi <= self.config.update_window[1] else 0.0
        return g
    
    def compute_operator(self, DR: float, S: float, Q: float, C: float, B: float, 
                        Gamma: float, grad_DR: np.ndarray, state_delta: np.ndarray):
        """Compute triadic operator components."""
        cfg = self.config
        
        # Precision and phase gate
        pi = self.compute_precision(DR, S, Gamma)
        g = self.phase_gate()
        
        # O_P: Precision-weighted gradient descent on DR
        O_P = -g * cfg.eta_P * pi * grad_DR
        
        # O_S: Stochastic exploration
        O_S = g * cfg.eta_S * S * np.random.randn(*grad_DR.shape)
        
        # O_C: Coherence optimization
        O_C = g * (
            cfg.eta_Q * Q * state_delta +
            cfg.eta_C * C * np.tanh(grad_DR) -
            cfg.eta_B * B * grad_DR
        )
        
        return O_P, O_S, O_C, pi, g


# ============================================================================
# Monster Mash Agent
# ============================================================================

class PirouetteSynthesisAgent:
    """
    The Monster Mash: Unified Pirouette RL Agent
    
    Combines:
    - Bilateral hemispheric architecture (Wanderer)
    - Multi-objective reward shaping (Wendigo)
    - Triadic operator dynamics (Skogsvätt)
    - Coherence metrics and precision (Sand Agent)
    - Forward ratchet mechanism (Wanderer v2)
    """
    
    def __init__(self, env_name: str, config: PirouetteConfig = None):
        self.env = gym.make(env_name)
        self.env_name = env_name
        self.config = config or PirouetteConfig()
        
        # State/action dimensions
        self.state_dim = self.env.observation_space.shape[0]
        if isinstance(self.env.action_space, gym.spaces.Box):
            self.is_continuous = True
            self.action_dim = self.env.action_space.shape[0]
            self.action_low = self.env.action_space.low
            self.action_high = self.env.action_space.high
        else:
            self.is_continuous = False
            self.action_dim = self.env.action_space.n
        
        # Device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Network
        self.manifold = BilateralManifold(
            self.state_dim, self.action_dim, self.config
        ).to(self.device)
        
        # Optimizer with separate learning rates for actor/critic
        actor_params = list(self.manifold.right_encoder.parameters()) + \
                      list(self.manifold.actor_mean.parameters()) + \
                      list(self.manifold.actor_log_std.parameters())
        critic_params = list(self.manifold.left_encoder.parameters()) + \
                       list(self.manifold.critic.parameters())
        shared_params = list(self.manifold.perception.parameters()) + \
                       list(self.manifold.corpus_callosum.parameters()) + \
                       list(self.manifold.autopoiesis_predictor.parameters())
        
        self.optimizer = optim.Adam([
            {'params': actor_params, 'lr': 3e-4},
            {'params': critic_params, 'lr': 1e-3},
            {'params': shared_params, 'lr': 3e-4}
        ])
        
        # Triadic operator
        self.operator = TriadicOperator(self.config)
        
        # Episode buffers
        self.reset_buffers()
        
        # Ratchet state
        self.best_rolling_avg = -float('inf')
        self.current_rolling_avg = -float('inf')
        self.resonance_history = deque(maxlen=100)
        
        # Previous observation for triadic metrics
        self.obs_prev = None
        
    def reset_buffers(self):
        """Reset episode buffers."""
        self.log_probs = []
        self.values = []
        self.rewards = []
        self.masks = []
        self.entropies = []
        self.unified_manifolds = []
        self.predicted_manifolds = []
        self.left_manifolds = []
        self.right_manifolds = []
        self.dr_values = []
        
    def select_action(self, state: np.ndarray, deterministic: bool = False):
        """Select action using bilateral manifold."""
        state_t = torch.FloatTensor(state).to(self.device).unsqueeze(0)
        
        with torch.no_grad() if deterministic else torch.enable_grad():
            (action_mean, action_log_std, value, unified_manifold, 
             predicted_next, left_manifold, right_manifold) = self.manifold(state_t)
        
        if deterministic:
            action = action_mean
            log_prob = None
            entropy = None
        else:
            # Sample from Gaussian policy
            action_std = torch.exp(action_log_std)
            dist = torch.distributions.Normal(action_mean, action_std)
            action = dist.sample()
            log_prob = dist.log_prob(action).sum(dim=-1)
            entropy = dist.entropy().sum(dim=-1)
            
            # Store for learning
            self.log_probs.append(log_prob)
            self.values.append(value)
            self.entropies.append(entropy)
            self.unified_manifolds.append(unified_manifold)
            self.predicted_manifolds.append(predicted_next)
            self.left_manifolds.append(left_manifold)
            self.right_manifolds.append(right_manifold)
        
        # Convert to env action
        action_np = action.cpu().numpy().flatten()
        
        if self.is_continuous:
            # Clip to action space
            action_np = np.clip(action_np, self.action_low, self.action_high)
        else:
            # Convert to discrete
            action_np = int(np.argmax(action_np))
        
        return action_np
    
    def compute_pirouette_reward(self, obs: np.ndarray, obs_prev: np.ndarray, 
                                base_reward: float):
        """
        Multi-objective Pirouette reward function.
        
        Combines:
        1. Coherence gain (rewarding DR reduction)
        2. Duration bonus (survival reward)
        3. Dissonance penalty (current instability)
        """
        # Compute metrics
        DR, S, Q, C, B = self.operator.compute_metrics(obs, obs_prev)
        self.dr_values.append(DR)
        
        # Coherence gain: reward for reducing DR
        coherence_gain = self.config.gamma_coherence * Q
        
        # Dissonance penalty: penalize current instability
        dissonance_penalty = self.config.delta_dissonance * DR
        
        # Duration bonus: small reward for survival
        duration_bonus = self.config.beta_duration
        
        # Combined reward
        pirouette_reward = coherence_gain + duration_bonus - dissonance_penalty
        
        return pirouette_reward, DR, S, Q, C, B
    
    def calculate_loss(self, next_value: float, gamma: float = 0.99):
        """
        Calculate multi-component loss with forward ratchet.
        
        Components:
        1. Actor loss (policy gradient with advantage)
        2. Critic loss (value function TD error)
        3. Autopoietic loss (self-prediction error)
        4. Entropy bonus (modulated by resonance)
        5. Hemispheric coherence loss (bilateral sync)
        """
        # Compute returns
        returns = []
        R = next_value
        for step in reversed(range(len(self.rewards))):
            R = self.rewards[step] + gamma * R * self.masks[step]
            returns.insert(0, R)
        
        returns = torch.tensor(returns, dtype=torch.float32).to(self.device)
        
        # Normalize returns
        if len(returns) > 1:
            returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        
        # Stack buffers
        log_probs = torch.stack(self.log_probs)
        values = torch.stack(self.values).squeeze()
        entropies = torch.stack(self.entropies)
        
        # Advantage
        advantage = returns - values
        
        # 1. Actor loss
        actor_loss = -(log_probs * advantage.detach()).mean()
        
        # 2. Critic loss
        critic_loss = advantage.pow(2).mean()
        
        # 3. Autopoietic loss (self-prediction)
        unified_manifolds = torch.stack(self.unified_manifolds)
        predicted_next = torch.stack(self.predicted_manifolds)
        
        if len(unified_manifolds) > 1:
            pred_t = predicted_next[:-1]
            actual_t_plus_1 = unified_manifolds[1:].detach()
            autopoiesis_loss = F.mse_loss(pred_t, actual_t_plus_1)
            
            # Raw resonance from autopoietic accuracy
            raw_resonance = torch.exp(
                -autopoiesis_loss * self.config.critical_resonance_scale
            ).item()
        else:
            autopoiesis_loss = torch.tensor(0.0).to(self.device)
            raw_resonance = 0.5
        
        # 4. Forward Ratchet: penalize backsliding
        dissonance_penalty = 0.0
        if self.best_rolling_avg != -float('inf'):
            tolerance = abs(self.best_rolling_avg) * self.config.ratchet_tolerance
            if self.current_rolling_avg < (self.best_rolling_avg - tolerance):
                # Shatter resonance on backsliding
                dissonance_penalty = 1.0
        
        final_resonance = raw_resonance * (1.0 - dissonance_penalty)
        self.resonance_history.append(final_resonance)
        
        # 5. Entropy bonus (modulated by resonance)
        # Low resonance = high entropy (exploration)
        entropy_weight = 0.1 * (1.0 - final_resonance)
        entropy_loss = -entropies.mean() * entropy_weight
        
        # 6. Hemispheric coherence loss (bilateral synchronization)
        left_manifolds = torch.stack(self.left_manifolds)
        right_manifolds = torch.stack(self.right_manifolds)
        hemispheric_loss = F.mse_loss(left_manifolds, right_manifolds) * 0.1
        
        # Total loss
        total_loss = (
            actor_loss + 
            0.5 * critic_loss + 
            0.5 * autopoiesis_loss + 
            entropy_loss +
            hemispheric_loss
        )
        
        return total_loss, final_resonance, {
            'actor_loss': actor_loss.item(),
            'critic_loss': critic_loss.item(),
            'autopoiesis_loss': autopoiesis_loss.item(),
            'entropy_bonus': entropy_loss.item(),
            'hemispheric_loss': hemispheric_loss.item(),
            'resonance': final_resonance,
            'mean_dr': np.mean(self.dr_values) if self.dr_values else 0.0
        }
    
    def update(self, next_state: np.ndarray):
        """Update network using collected experience."""
        next_state_t = torch.FloatTensor(next_state).to(self.device).unsqueeze(0)
        
        with torch.no_grad():
            _, _, next_value, _, _, _, _ = self.manifold(next_state_t)
            next_value = next_value.item()
        
        # Calculate loss
        loss, resonance, metrics = self.calculate_loss(next_value)
        
        # Optimization step
        self.optimizer.zero_grad()
        loss.backward()
        
        # Gradient clipping (modulated by resonance)
        # High resonance = larger steps allowed
        max_grad_norm = 0.5 + (2.0 * resonance)
        nn.utils.clip_grad_norm_(self.manifold.parameters(), max_grad_norm)
        
        self.optimizer.step()
        
        # Clear buffers
        self.reset_buffers()
        
        return loss.item(), resonance, metrics
    
    def train_episode(self, max_steps: int = 1000):
        """Train for one episode."""
        obs, _ = self.env.reset()
        self.obs_prev = obs.copy()
        
        episode_reward = 0.0
        pirouette_reward_total = 0.0
        
        for t in range(max_steps):
            # Select action
            action = self.select_action(obs)
            
            # Step environment
            next_obs, base_reward, done, truncated, _ = self.env.step(action)
            
            # Compute Pirouette reward
            pirouette_reward, DR, S, Q, C, B = self.compute_pirouette_reward(
                next_obs, self.obs_prev, base_reward
            )
            
            # Store experience
            self.rewards.append(pirouette_reward)
            self.masks.append(1.0 - done)
            
            # Update state
            self.obs_prev = obs.copy()
            obs = next_obs
            
            episode_reward += base_reward
            pirouette_reward_total += pirouette_reward
            
            if done or truncated:
                break
        
        # Update policy
        loss, resonance, metrics = self.update(obs)
        
        return episode_reward, pirouette_reward_total, resonance, metrics
    
    def train(self, max_episodes: int = 500, goal_reward: float = None):
        """Main training loop."""
        print(f"\n{'='*70}")
        print(f"PIROUETTE SYNTHESIS AGENT - {self.env_name}")
        print(f"{'='*70}")
        print(f"Configuration:")
        print(f"  Manifold dim: {self.config.manifold_dim}")
        print(f"  Action type: {'Continuous' if self.is_continuous else 'Discrete'}")
        print(f"  Device: {self.device}")
        print(f"{'='*70}\n")
        
        running_reward = deque(maxlen=20)
        best_reward = -float('inf')
        
        for ep in range(1, max_episodes + 1):
            ep_reward, pir_reward, resonance, metrics = self.train_episode()
            
            running_reward.append(ep_reward)
            self.current_rolling_avg = np.mean(running_reward)
            
            # Update ratchet
            if self.current_rolling_avg > self.best_rolling_avg:
                self.best_rolling_avg = self.current_rolling_avg
                best_reward = ep_reward
            
            # Logging
            if ep % 20 == 0 or ep == 1:
                # Determine resonance status
                if resonance < 0.1:
                    status = "DISSONANCE"
                elif resonance < 0.8:
                    status = "WANDERING"
                else:
                    status = "RESONANT"
                
                print(f"Ep {ep:4d} | "
                      f"Reward: {ep_reward:6.1f} | "
                      f"Avg20: {self.current_rolling_avg:6.1f} | "
                      f"Best: {self.best_rolling_avg:6.1f} | "
                      f"Res: {resonance:.2f} ({status}) | "
                      f"DR: {metrics['mean_dr']:.3f}")
            
            # Check for mastery
            if goal_reward is not None and self.current_rolling_avg >= goal_reward:
                print(f"\n{'='*70}")
                print(f"*** MASTERY ACHIEVED in {ep} episodes! ***")
                print(f"Goal: {goal_reward:.1f} | Achieved: {self.current_rolling_avg:.1f}")
                print(f"{'='*70}\n")
                break
        
        self.env.close()
        return self.manifold


# ============================================================================
# Main
# ============================================================================

def main():
    """Train the Monster Mash agent on multiple environments."""
    config = PirouetteConfig()
    
    # Test environments
    envs = [
        ("CartPole-v1", 475),
        ("Acrobot-v1", -90),
        ("Pendulum-v1", -200),
    ]
    
    for env_name, goal in envs:
        print(f"\n\n{'#'*70}")
        print(f"# Training on: {env_name}")
        print(f"{'#'*70}\n")
        
        agent = PirouetteSynthesisAgent(env_name, config)
        agent.train(max_episodes=500, goal_reward=goal)
        
        print(f"\n{'='*70}")
        print(f"Completed {env_name}")
        print(f"{'='*70}\n")


if __name__ == "__main__":
    main()