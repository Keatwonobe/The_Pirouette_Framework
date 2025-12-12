"""
VAGABOND: Minimal Δ-Powered Reinforcement Learning Agent
==========================================================

A clean implementation of the Pirouette Framework's temporal field theory
applied to reinforcement learning. Uses Δ (Time as dynamic field) and Dark 
Residue to dramatically accelerate learning across diverse tasks.

Core Principles:
- Δ as explicit Lagrangian parameter with conjugate momentum
- Dark Residue (DR) = |K_τ - V_Γ| as primary learning signal
- Geodesic map for efficient state-action memory
- Closure dynamics to minimize residual imbalance
"""

import numpy as np
import gymnasium as gym
from collections import deque, defaultdict
import torch
import torch.nn as nn
import torch.optim as optim
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List
import json


@dataclass
class VagabondConfig:
    """Configuration for Vagabond agent"""
    # Core Pirouette parameters
    gamma_weight: float = 0.5  # Weight for coherence gain reward
    beta_weight: float = 0.1   # Persistence bonus
    delta_weight: float = 0.1  # Dark Residue penalty
    
    # Δ (temporal field) parameters
    delta_learning_rate: float = 0.01  # How fast Δ adapts
    delta_momentum_decay: float = 0.95  # Conjugate momentum decay
    
    # Learning parameters
    learning_rate: float = 3e-4
    batch_size: int = 64
    buffer_size: int = 100_000
    gamma_discount: float = 0.99
    tau: float = 0.005  # Soft update parameter
    
    # Exploration
    exploration_noise: float = 0.1
    
    # Network architecture
    hidden_dims: List[int] = None
    
    def __post_init__(self):
        if self.hidden_dims is None:
            self.hidden_dims = [256, 256]


class TemporalField:
    """
    Δ as an explicit Lagrangian parameter with conjugate momentum.
    
    The temporal field tracks the "pressure" or "cost" of maintaining 
    coherence in different regions of state-action space. It has:
    - Position: Δ(s,a) - the field value
    - Momentum: p_Δ - rate of change
    - Dynamics governed by Euler-Lagrange equations
    """
    
    def __init__(self, config: VagabondConfig):
        self.config = config
        self.field = defaultdict(lambda: 0.0)  # Δ values
        self.momentum = defaultdict(lambda: 0.0)  # p_Δ conjugate momentum
        self.visits = defaultdict(int)  # Visit counts for each state
        
    def get(self, state_hash: int) -> float:
        """Get Δ value for a state"""
        return self.field[state_hash]
    
    def update(self, state_hash: int, dark_residue: float):
        """
        Update Δ using Euler-Lagrange dynamics.
        
        The field responds to Dark Residue by adjusting its local value,
        with momentum providing inertial stability.
        """
        current_delta = self.field[state_hash]
        current_momentum = self.momentum[state_hash]
        
        # Force from Dark Residue gradient
        force = dark_residue
        
        # Update momentum (with decay)
        new_momentum = (self.config.delta_momentum_decay * current_momentum + 
                       self.config.delta_learning_rate * force)
        
        # Update field position
        new_delta = current_delta + new_momentum
        
        self.momentum[state_hash] = new_momentum
        self.field[state_hash] = new_delta
        self.visits[state_hash] += 1
        
    def get_temporal_pressure(self, state_hash: int) -> float:
        """
        V_Γ: Temporal Pressure as function of Δ.
        
        High Δ = high pressure = this region is expensive to traverse
        """
        delta = self.get(state_hash)
        visits = self.visits[state_hash]
        
        # Pressure increases with field strength and decreases with familiarity
        base_pressure = abs(delta)
        familiarity_discount = 1.0 / (1.0 + np.sqrt(visits))
        
        return base_pressure * familiarity_discount


class DarkResidueCalculator:
    """
    Computes Dark Residue: D = |K_τ - V_Γ|
    
    The fundamental imbalance between temporal coherence (K_τ) and 
    temporal pressure (V_Γ). Minimizing this is the agent's true goal.
    """
    
    def __init__(self, env_name: str):
        self.env_name = env_name
        
        # Environment-specific weights for K_τ and V_Γ
        self.weights = self._get_env_weights(env_name)
        
    def _get_env_weights(self, env_name: str) -> Dict[str, float]:
        """Environment-specific weightings for coherence vs pressure"""
        weights = {
            'CartPole-v1': {
                'angle_weight': 1.0,
                'velocity_weight': 0.3,
                'position_weight': 0.1,
                'action_cost': 0.05
            },
            'Pendulum-v1': {
                'angle_weight': 2.0,
                'velocity_weight': 0.5,
                'action_cost': 0.1
            },
            'Acrobot-v1': {
                'angle_weight': 1.5,
                'velocity_weight': 0.4,
                'link_coupling': 0.3,
                'action_cost': 0.05
            },
            'MountainCarContinuous-v0': {
                'position_weight': 2.0,
                'velocity_weight': 1.0,
                'action_cost': 0.1
            }
        }
        return weights.get(env_name, {
            'default_state_weight': 1.0,
            'default_action_cost': 0.1
        })
    
    def compute(self, state: np.ndarray, action: np.ndarray, 
                next_state: np.ndarray, reward: float,
                temporal_field: TemporalField, 
                state_hash: int) -> float:
        """
        Compute Dark Residue for this transition.
        
        K_τ (Temporal Coherence): How well does this maintain rhythm?
        V_Γ (Temporal Pressure): What's the cost in this region?
        D = |K_τ - V_Γ|: The residual imbalance
        """
        env = self.env_name
        
        if env == 'CartPole-v1':
            K_tau = self._cartpole_coherence(state, next_state, action)
            V_gamma = temporal_field.get_temporal_pressure(state_hash)
            
        elif env == 'Pendulum-v1':
            K_tau = self._pendulum_coherence(state, next_state, action)
            V_gamma = temporal_field.get_temporal_pressure(state_hash)
            
        elif env == 'Acrobot-v1':
            K_tau = self._acrobot_coherence(state, next_state, action)
            V_gamma = temporal_field.get_temporal_pressure(state_hash)
            
        elif env == 'MountainCarContinuous-v0':
            K_tau = self._mountaincar_coherence(state, next_state, action)
            V_gamma = temporal_field.get_temporal_pressure(state_hash)
            
        else:
            # Generic fallback
            K_tau = self._generic_coherence(state, next_state, action, reward)
            V_gamma = temporal_field.get_temporal_pressure(state_hash)
        
        # Dark Residue is the absolute imbalance
        dark_residue = abs(K_tau - V_gamma)
        
        return dark_residue
    
    def _cartpole_coherence(self, state, next_state, action) -> float:
        """CartPole: favor small angles and smooth velocities"""
        w = self.weights
        
        # Angle coherence (smaller is better)
        angle = state[2] if len(state) > 2 else 0
        angle_coherence = w['angle_weight'] * (1.0 - abs(angle) / 0.2095)
        
        # Velocity coherence (smooth motion)
        velocity = abs(state[3]) if len(state) > 3 else 0
        velocity_coherence = w['velocity_weight'] * np.exp(-velocity)
        
        # Position stability
        position = abs(state[0]) if len(state) > 0 else 0
        position_coherence = w['position_weight'] * (1.0 - position / 2.4)
        
        # Action cost (prefer smooth control)
        action_penalty = w['action_cost'] * abs(float(action[0]) if hasattr(action, '__len__') else action)
        
        return angle_coherence + velocity_coherence + position_coherence - action_penalty
    
    def _pendulum_coherence(self, state, next_state, action) -> float:
        """Pendulum: favor upright position with low energy cost"""
        w = self.weights
        
        # Angle coherence (upright = coherent)
        cos_theta = state[0] if len(state) > 0 else 0
        angle_coherence = w['angle_weight'] * (1.0 + cos_theta) / 2.0
        
        # Angular velocity (smooth spin)
        ang_velocity = abs(state[2]) if len(state) > 2 else 0
        velocity_coherence = w['velocity_weight'] * np.exp(-ang_velocity / 8.0)
        
        # Torque cost
        torque = abs(float(action[0])) if hasattr(action, '__len__') else abs(action)
        action_penalty = w['action_cost'] * torque / 2.0
        
        return angle_coherence + velocity_coherence - action_penalty
    
    def _acrobot_coherence(self, state, next_state, action) -> float:
        """Acrobot: favor reaching above threshold with coordinated links"""
        w = self.weights
        
        # Link angles
        cos_theta1 = state[0] if len(state) > 0 else 0
        cos_theta2 = state[1] if len(state) > 1 else 0
        
        # Angle coherence (links coordinated)
        angle_coherence = w['angle_weight'] * (cos_theta1 + cos_theta2) / 2.0
        
        # Velocity coherence
        velocity = np.sqrt(state[4]**2 + state[5]**2) if len(state) > 5 else 0
        velocity_coherence = w['velocity_weight'] * np.exp(-velocity / 4.0)
        
        # Link coupling (they should move together)
        coupling = w['link_coupling'] * (1.0 - abs(cos_theta1 - cos_theta2))
        
        # Action cost
        action_penalty = w['action_cost'] * abs(float(action[0]) if hasattr(action, '__len__') else action)
        
        return angle_coherence + velocity_coherence + coupling - action_penalty
    
    def _mountaincar_coherence(self, state, next_state, action) -> float:
        """MountainCar: favor rightward position and velocity building"""
        w = self.weights
        
        # Position (rightward is good)
        position = state[0] if len(state) > 0 else -0.5
        position_coherence = w['position_weight'] * (position + 0.5) / 1.2
        
        # Velocity (building momentum)
        velocity = state[1] if len(state) > 1 else 0
        velocity_coherence = w['velocity_weight'] * abs(velocity) / 0.07
        
        # Action cost (prefer less action)
        action_cost = w['action_cost'] * abs(float(action[0]))
        
        return position_coherence + velocity_coherence - action_cost
    
    def _generic_coherence(self, state, next_state, action, reward) -> float:
        """Generic: use reward as proxy for coherence"""
        w = self.weights
        
        # Use normalized reward
        coherence = reward / (1.0 + abs(reward))
        
        # Penalize large actions
        action_norm = np.linalg.norm(action) if hasattr(action, '__len__') else abs(action)
        action_penalty = w.get('default_action_cost', 0.1) * action_norm
        
        return coherence - action_penalty


class GeodesicMap:
    """
    Memory of geodesic paths through state-action space.
    
    Tracks which (state, action) pairs lead to low Dark Residue,
    enabling rapid reuse of known-good trajectories.
    """
    
    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.map = {}  # state_hash -> (action, dark_residue, visits)
        self.lru_queue = deque(maxlen=capacity)
        
    def update(self, state_hash: int, action: np.ndarray, dark_residue: float):
        """Update or add a geodesic entry"""
        if state_hash in self.map:
            old_action, old_dr, visits = self.map[state_hash]
            # Keep the better (lower DR) action
            if dark_residue < old_dr:
                self.map[state_hash] = (action.copy(), dark_residue, visits + 1)
        else:
            self.map[state_hash] = (action.copy(), dark_residue, 1)
            self.lru_queue.append(state_hash)
            
            # Evict if over capacity
            if len(self.map) > self.capacity:
                oldest = self.lru_queue.popleft()
                if oldest in self.map:
                    del self.map[oldest]
    
    def query(self, state_hash: int) -> Optional[Tuple[np.ndarray, float]]:
        """Query if we've seen a good path from this state"""
        if state_hash in self.map:
            action, dr, visits = self.map[state_hash]
            return action, dr
        return None
    
    def get_hit_rate(self) -> float:
        """Fraction of states with known geodesics"""
        return len(self.map) / max(self.capacity, 1)


class Actor(nn.Module):
    """Policy network: state -> action"""
    
    def __init__(self, state_dim: int, action_dim: int, hidden_dims: List[int], 
                 action_space):
        super().__init__()
        
        layers = []
        prev_dim = state_dim
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU()
            ])
            prev_dim = hidden_dim
        
        self.backbone = nn.Sequential(*layers)
        self.action_head = nn.Linear(prev_dim, action_dim)
        
        self.action_space = action_space
        
        # Determine action scaling
        if hasattr(action_space, 'low'):
            self.action_scale = torch.FloatTensor(
                (action_space.high - action_space.low) / 2.0
            )
            self.action_bias = torch.FloatTensor(
                (action_space.high + action_space.low) / 2.0
            )
        else:
            self.action_scale = None
            self.action_bias = None
    
    def forward(self, state):
        x = self.backbone(state)
        action = self.action_head(x)
        
        if self.action_scale is not None:
            # Continuous action space
            action = torch.tanh(action)
            action = action * self.action_scale.to(action.device) + \
                    self.action_bias.to(action.device)
        else:
            # Discrete action space
            action = torch.softmax(action, dim=-1)
        
        return action


class Critic(nn.Module):
    """Value network: state, action -> Q-value"""
    
    def __init__(self, state_dim: int, action_dim: int, hidden_dims: List[int]):
        super().__init__()
        
        layers = []
        prev_dim = state_dim + action_dim
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU()
            ])
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, 1))
        self.network = nn.Sequential(*layers)
    
    def forward(self, state, action):
        x = torch.cat([state, action], dim=-1)
        return self.network(x)


class ReplayBuffer:
    """Experience replay with Dark Residue tracking"""
    
    def __init__(self, capacity: int, state_dim: int, action_dim: int):
        self.capacity = capacity
        self.size = 0
        self.pos = 0
        
        self.states = np.zeros((capacity, state_dim))
        self.actions = np.zeros((capacity, action_dim))
        self.rewards = np.zeros((capacity, 1))
        self.next_states = np.zeros((capacity, state_dim))
        self.dones = np.zeros((capacity, 1))
        self.dark_residues = np.zeros((capacity, 1))
    
    def add(self, state, action, reward, next_state, done, dark_residue):
        self.states[self.pos] = state
        self.actions[self.pos] = action
        self.rewards[self.pos] = reward
        self.next_states[self.pos] = next_state
        self.dones[self.pos] = done
        self.dark_residues[self.pos] = dark_residue
        
        self.pos = (self.pos + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)
    
    def sample(self, batch_size: int):
        indices = np.random.randint(0, self.size, size=batch_size)
        
        return (
            torch.FloatTensor(self.states[indices]),
            torch.FloatTensor(self.actions[indices]),
            torch.FloatTensor(self.rewards[indices]),
            torch.FloatTensor(self.next_states[indices]),
            torch.FloatTensor(self.dones[indices]),
            torch.FloatTensor(self.dark_residues[indices])
        )
    
    def __len__(self):
        return self.size


class Vagabond:
    """
    The Vagabond Agent: A wanderer through state-action space,
    guided by the temporal field Δ and seeking to minimize Dark Residue.
    """
    
    def __init__(self, env: gym.Env, config: VagabondConfig = None):
        self.env = env
        self.config = config or VagabondConfig()
        
        # Environment properties
        self.state_dim = env.observation_space.shape[0]
        if isinstance(env.action_space, gym.spaces.Discrete):
            self.action_dim = env.action_space.n
            self.continuous = False
        else:
            self.action_dim = env.action_space.shape[0]
            self.continuous = True
        
        # Core Pirouette components
        self.temporal_field = TemporalField(self.config)
        self.dark_residue_calc = DarkResidueCalculator(env.spec.id)
        self.geodesic_map = GeodesicMap()
        
        # Neural networks
        self.actor = Actor(self.state_dim, self.action_dim, 
                          self.config.hidden_dims, env.action_space)
        self.actor_target = Actor(self.state_dim, self.action_dim,
                                  self.config.hidden_dims, env.action_space)
        self.actor_target.load_state_dict(self.actor.state_dict())
        
        self.critic_1 = Critic(self.state_dim, self.action_dim, 
                              self.config.hidden_dims)
        self.critic_2 = Critic(self.state_dim, self.action_dim,
                              self.config.hidden_dims)
        self.critic_1_target = Critic(self.state_dim, self.action_dim,
                                     self.config.hidden_dims)
        self.critic_2_target = Critic(self.state_dim, self.action_dim,
                                     self.config.hidden_dims)
        self.critic_1_target.load_state_dict(self.critic_1.state_dict())
        self.critic_2_target.load_state_dict(self.critic_2.state_dict())
        
        # Optimizers
        self.actor_optimizer = optim.Adam(
            self.actor.parameters(), lr=self.config.learning_rate
        )
        self.critic_1_optimizer = optim.Adam(
            self.critic_1.parameters(), lr=self.config.learning_rate
        )
        self.critic_2_optimizer = optim.Adam(
            self.critic_2.parameters(), lr=self.config.learning_rate
        )
        
        # Replay buffer
        self.replay_buffer = ReplayBuffer(
            self.config.buffer_size, self.state_dim, self.action_dim
        )
        
        # Training state
        self.total_steps = 0
        self.episode_count = 0
        self.dark_residue_history = deque(maxlen=100)
        
    def _hash_state(self, state: np.ndarray) -> int:
        """Create hash of state for geodesic map"""
        # Discretize continuous states for hashing
        discretized = (state * 10).astype(int)
        return hash(tuple(discretized))
    
    def select_action(self, state: np.ndarray, 
                     evaluate: bool = False) -> np.ndarray:
        """
        Select action using:
        1. Geodesic map (if known good path exists)
        2. Policy network (with optional exploration noise)
        """
        state_hash = self._hash_state(state)
        
        # Check geodesic map first
        if not evaluate:
            geodesic_result = self.geodesic_map.query(state_hash)
            if geodesic_result is not None:
                action, dr = geodesic_result
                # Use geodesic with high probability if DR is low
                if dr < 0.1 and np.random.random() < 0.3:
                    return action
        
        # Use policy network
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            action = self.actor(state_tensor).cpu().numpy()[0]
        
        # Add exploration noise
        if not evaluate and self.continuous:
            noise = np.random.normal(0, self.config.exploration_noise, 
                                   size=action.shape)
            action = action + noise
            action = np.clip(action, 
                           self.env.action_space.low, 
                           self.env.action_space.high)
        elif not evaluate and not self.continuous:
            # Epsilon-greedy for discrete
            if np.random.random() < self.config.exploration_noise:
                action = np.random.randint(0, self.action_dim)
            else:
                action = np.argmax(action)
        
        return action
    
    def compute_closure_reward(self, dark_residue: float, 
                              previous_dr: float) -> float:
        """
        Compute Closure Engine reward:
        r = γ·max(0, -ΔDR) + β - δ·DR
        
        Rewards closing the loop (reducing DR) and penalizes distance from closure
        """
        delta_dr = dark_residue - previous_dr
        
        closure_gain = self.config.gamma_weight * max(0, -delta_dr)
        persistence = self.config.beta_weight
        residue_penalty = self.config.delta_weight * dark_residue
        
        return closure_gain + persistence - residue_penalty
    
    def train_step(self):
        """Single training step using Pirouette-enhanced TD learning"""
        if len(self.replay_buffer) < self.config.batch_size:
            return {}
        
        # Sample batch
        states, actions, rewards, next_states, dones, dark_residues = \
            self.replay_buffer.sample(self.config.batch_size)
        
        # Compute target Q-values with Dark Residue augmentation
        with torch.no_grad():
            next_actions = self.actor_target(next_states)
            target_q1 = self.critic_1_target(next_states, next_actions)
            target_q2 = self.critic_2_target(next_states, next_actions)
            target_q = torch.min(target_q1, target_q2)
            
            # Augment with Dark Residue signal
            dr_bonus = -self.config.delta_weight * dark_residues
            target_q = rewards + dr_bonus + \
                      (1 - dones) * self.config.gamma_discount * target_q
        
        # Update critics
        current_q1 = self.critic_1(states, actions)
        current_q2 = self.critic_2(states, actions)
        
        critic_1_loss = nn.MSELoss()(current_q1, target_q)
        critic_2_loss = nn.MSELoss()(current_q2, target_q)
        
        self.critic_1_optimizer.zero_grad()
        critic_1_loss.backward()
        self.critic_1_optimizer.step()
        
        self.critic_2_optimizer.zero_grad()
        critic_2_loss.backward()
        self.critic_2_optimizer.step()
        
        # Update actor
        new_actions = self.actor(states)
        actor_loss = -self.critic_1(states, new_actions).mean()
        
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()
        
        # Soft update target networks
        self._soft_update(self.actor, self.actor_target)
        self._soft_update(self.critic_1, self.critic_1_target)
        self._soft_update(self.critic_2, self.critic_2_target)
        
        return {
            'critic_1_loss': critic_1_loss.item(),
            'critic_2_loss': critic_2_loss.item(),
            'actor_loss': actor_loss.item(),
            'mean_q': current_q1.mean().item()
        }
    
    def _soft_update(self, source: nn.Module, target: nn.Module):
        """Soft update target network"""
        for source_param, target_param in zip(source.parameters(), 
                                              target.parameters()):
            target_param.data.copy_(
                self.config.tau * source_param.data + 
                (1 - self.config.tau) * target_param.data
            )
    
    def train_episode(self) -> Dict:
        """Run one episode of training"""
        state, _ = self.env.reset()
        episode_reward = 0
        episode_dr = 0
        episode_steps = 0
        previous_dr = 0
        
        done = False
        while not done:
            # Select action
            action = self.select_action(state, evaluate=False)
            
            # Environment step
            if self.continuous:
                next_state, reward, terminated, truncated, _ = \
                    self.env.step(action)
            else:
                # Convert to discrete action
                action_idx = action if isinstance(action, (int, np.integer)) \
                            else np.argmax(action)
                next_state, reward, terminated, truncated, _ = \
                    self.env.step(action_idx)
                # Convert back to array for storage
                action = np.array([action_idx], dtype=np.float32)
            
            done = terminated or truncated
            
            # Compute Dark Residue
            state_hash = self._hash_state(state)
            dark_residue = self.dark_residue_calc.compute(
                state, action, next_state, reward,
                self.temporal_field, state_hash
            )
            
            # Update temporal field
            self.temporal_field.update(state_hash, dark_residue)
            
            # Update geodesic map
            self.geodesic_map.update(state_hash, action, dark_residue)
            
            # Compute closure reward
            closure_reward = self.compute_closure_reward(dark_residue, previous_dr)
            
            # Store in replay buffer (with both rewards)
            total_reward = reward + closure_reward
            self.replay_buffer.add(state, action, total_reward, 
                                  next_state, done, dark_residue)
            
            # Training step
            if self.total_steps % 1 == 0:  # Train every step
                self.train_step()
            
            episode_reward += reward
            episode_dr += dark_residue
            episode_steps += 1
            self.total_steps += 1
            previous_dr = dark_residue
            
            state = next_state
        
        self.episode_count += 1
        avg_dr = episode_dr / max(episode_steps, 1)
        self.dark_residue_history.append(avg_dr)
        
        return {
            'episode': self.episode_count,
            'reward': episode_reward,
            'steps': episode_steps,
            'avg_dark_residue': avg_dr,
            'geodesic_hit_rate': self.geodesic_map.get_hit_rate(),
            'total_steps': self.total_steps
        }
    
    def evaluate(self, num_episodes: int = 10) -> Dict:
        """Evaluate agent performance"""
        rewards = []
        dark_residues = []
        
        for _ in range(num_episodes):
            state, _ = self.env.reset()
            episode_reward = 0
            episode_dr = 0
            steps = 0
            
            done = False
            while not done:
                action = self.select_action(state, evaluate=True)
                
                if self.continuous:
                    next_state, reward, terminated, truncated, _ = \
                        self.env.step(action)
                else:
                    action_idx = action if isinstance(action, (int, np.integer)) \
                                else np.argmax(action)
                    next_state, reward, terminated, truncated, _ = \
                        self.env.step(action_idx)
                    action = np.array([action_idx], dtype=np.float32)
                
                done = terminated or truncated
                
                state_hash = self._hash_state(state)
                dark_residue = self.dark_residue_calc.compute(
                    state, action, next_state, reward,
                    self.temporal_field, state_hash
                )
                
                episode_reward += reward
                episode_dr += dark_residue
                steps += 1
                state = next_state
            
            rewards.append(episode_reward)
            dark_residues.append(episode_dr / max(steps, 1))
        
        return {
            'mean_reward': np.mean(rewards),
            'std_reward': np.std(rewards),
            'mean_dark_residue': np.mean(dark_residues),
            'std_dark_residue': np.std(dark_residues)
        }


def train_vagabond(env_name: str, num_episodes: int = 500,
                   eval_interval: int = 50,
                   config: VagabondConfig = None) -> Vagabond:
    """
    Train a Vagabond agent on a given environment.
    
    Args:
        env_name: Gymnasium environment name
        num_episodes: Number of training episodes
        eval_interval: Evaluate every N episodes
        config: Agent configuration
        
    Returns:
        Trained Vagabond agent
    """
    env = gym.make(env_name)
    agent = Vagabond(env, config)
    
    print(f"\n🌀 Training Vagabond on {env_name}")
    print(f"State dim: {agent.state_dim}, Action dim: {agent.action_dim}")
    print(f"Continuous: {agent.continuous}\n")
    
    best_reward = float('-inf')
    
    for episode in range(num_episodes):
        # Training episode
        stats = agent.train_episode()
        
        # Periodic evaluation
        if (episode + 1) % eval_interval == 0:
            eval_stats = agent.evaluate(num_episodes=10)
            
            print(f"Episode {episode + 1}/{num_episodes}")
            print(f"  Train Reward: {stats['reward']:.2f}")
            print(f"  Eval Reward: {eval_stats['mean_reward']:.2f} ± "
                  f"{eval_stats['std_reward']:.2f}")
            print(f"  Dark Residue: {eval_stats['mean_dark_residue']:.4f}")
            print(f"  Geodesic Hit Rate: {stats['geodesic_hit_rate']:.2%}")
            print(f"  Total Steps: {stats['total_steps']}")
            
            if eval_stats['mean_reward'] > best_reward:
                best_reward = eval_stats['mean_reward']
                print(f"  🎯 New best: {best_reward:.2f}")
            print()
    
    return agent


def main():
    """Run Vagabond on multiple environments"""
    
    # Test environments
    environments = [
        'CartPole-v1',
        'Pendulum-v1', 
        'Acrobot-v1',
    ]
    
    results = {}
    
    for env_name in environments:
        print(f"\n{'='*60}")
        print(f"Training on {env_name}")
        print(f"{'='*60}")
        
        # Environment-specific config
        if env_name == 'CartPole-v1':
            config = VagabondConfig(
                gamma_weight=0.6,
                delta_weight=0.15,
                exploration_noise=0.15,
                batch_size=64
            )
            num_episodes = 300
        elif env_name == 'Pendulum-v1':
            config = VagabondConfig(
                gamma_weight=0.5,
                delta_weight=0.1,
                exploration_noise=0.2,
                batch_size=128
            )
            num_episodes = 500
        elif env_name == 'Acrobot-v1':
            config = VagabondConfig(
                gamma_weight=0.55,
                delta_weight=0.12,
                exploration_noise=0.18,
                batch_size=64
            )
            num_episodes = 600
        else:
            config = VagabondConfig()
            num_episodes = 500
        
        agent = train_vagabond(env_name, num_episodes=num_episodes, config=config)
        
        # Final evaluation
        final_eval = agent.evaluate(num_episodes=50)
        results[env_name] = final_eval
        
        print(f"\n📊 Final Results for {env_name}:")
        print(f"  Reward: {final_eval['mean_reward']:.2f} ± "
              f"{final_eval['std_reward']:.2f}")
        print(f"  Dark Residue: {final_eval['mean_dark_residue']:.4f}")
    
    # Summary
    print(f"\n{'='*60}")
    print("VAGABOND SUMMARY")
    print(f"{'='*60}")
    for env_name, stats in results.items():
        print(f"{env_name:25s}: {stats['mean_reward']:8.2f} ± "
              f"{stats['std_reward']:6.2f}  (DR: {stats['mean_dark_residue']:.4f})")


if __name__ == "__main__":
    main()