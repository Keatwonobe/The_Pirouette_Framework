import numpy as np
import gymnasium as gym
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from collections import deque, defaultdict
import random
from dataclasses import dataclass
from typing import Tuple, List, Optional

# ============================================================================
# CONFIGURATION & GENETICS
# ============================================================================

@dataclass
class ChimeraConfig:
    # Environment
    env_name: str = "LunarLanderContinuous-v3"  # Works well for continuous
    
    # Wendigo (Pirouette) Parameters
    gamma_coherence: float = 1.5   # Reward for improving state
    delta_dissonance: float = 1.0  # Penalty for chaos
    beta_duration: float = 0.05    # Survival bonus
    
    # Vagabond (Temporal Field) Parameters
    delta_momentum: float = 0.95
    
    # Wanderer (Ratchet) Parameters
    ratchet_tolerance: float = 0.15 # Allow 15% drop before panic
    
    # SAC Hyperparameters
    gamma: float = 0.99
    tau: float = 0.005
    alpha: float = 0.2            # Entropy coefficient
    lr: float = 3e-4
    hidden_dim: int = 256
    manifold_dim: int = 64        # Latent bottleneck (Wanderer)
    batch_size: int = 256
    buffer_size: int = 100_000

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ============================================================================
# 1. THE BRAIN: IDEA MANIFOLD & WORLD MODEL (Wanderer + Saclet)
# ============================================================================

class IdeaManifold(nn.Module):
    """
    Combines Wanderer's Latent Space with Saclet's World Model.
    Inputs -> Manifold (Latent) -> Actor/Critic/Prediction
    """
    def __init__(self, state_dim, action_dim, hidden_dim, manifold_dim, action_space):
        super().__init__()
        
        # 1. Perception (Encoder)
        self.encoder = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, manifold_dim),
            nn.LayerNorm(manifold_dim),
            nn.Tanh() # Compress into [-1, 1] idea space
        )
        
        # 2. Actor Head (Policy)
        self.actor_mean = nn.Linear(manifold_dim, action_dim)
        self.actor_log_std = nn.Linear(manifold_dim, action_dim)
        
        # 3. Critic Heads (Twin Q) - Note: Critics usually take (s,a), 
        # but here we project s to manifold first.
        self.critic_1 = nn.Linear(manifold_dim + action_dim, 1)
        self.critic_2 = nn.Linear(manifold_dim + action_dim, 1)
        
        # 4. World Model Head (Saclet's K_tau)
        # Predicts NEXT manifold state given current manifold + action
        self.predictor = nn.Sequential(
            nn.Linear(manifold_dim + action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, manifold_dim)
        )
        
        # Action Scaling
        self.register_buffer('action_scale', torch.tensor((action_space.high - action_space.low) / 2.0, dtype=torch.float32))
        self.register_buffer('action_bias', torch.tensor((action_space.high + action_space.low) / 2.0, dtype=torch.float32))

    def encode(self, state):
        return self.encoder(state)

    def act(self, state):
        manifold = self.encode(state)
        mean = self.actor_mean(manifold)
        log_std = self.actor_log_std(manifold).clamp(-20, 2)
        return mean, log_std, manifold

    def get_q(self, state, action):
        manifold = self.encode(state)
        xu = torch.cat([manifold, action], dim=1)
        return self.critic_1(xu), self.critic_2(xu)

    def predict_next(self, state, action):
        manifold = self.encode(state)
        xu = torch.cat([manifold, action], dim=1)
        return self.predictor(xu)

# ============================================================================
# 2. THE MEMORY: TEMPORAL FIELD & GEODESICS (Vagabond)
# ============================================================================

class TemporalField:
    """
    Tracks 'Pressure' (V_gamma) across state space.
    Used to calculate Dark Residue.
    """
    def __init__(self, config: ChimeraConfig):
        self.field = defaultdict(float) # Delta values
        self.momentum = defaultdict(float)
        self.visits = defaultdict(int)
        self.decay = config.delta_momentum
        
    def _hash(self, state):
        # Discretize for hashing
        return hash(tuple((state * 10).astype(int)))
        
    def get_pressure(self, state) -> float:
        h = self._hash(state)
        # Pressure = Field Value * Familiarity Discount
        return abs(self.field[h]) / (1.0 + np.log1p(self.visits[h]))
        
    def update(self, state, dark_residue):
        h = self._hash(state)
        
        # Euler-Lagrange dynamics from Vagabond
        force = dark_residue
        self.momentum[h] = (self.decay * self.momentum[h]) + (1 - self.decay) * force
        self.field[h] += self.momentum[h]
        self.visits[h] += 1

class GeodesicMap:
    """
    Associative memory. If we found a path with near-zero Dark Residue
    from this state before, just repeat it.
    """
    def __init__(self, capacity=10000):
        self.map = {} # hash -> (action, dark_residue)
        self.capacity = capacity
        
    def query(self, state_hash) -> Optional[np.ndarray]:
        if state_hash in self.map:
            action, dr = self.map[state_hash]
            # Only return if it was a "Resonant" action (low DR)
            if dr < 0.15: 
                return action
        return None
        
    def update(self, state_hash, action, dr):
        # Overwrite if we found a cleaner path (lower DR)
        if state_hash not in self.map or dr < self.map[state_hash][1]:
            self.map[state_hash] = (action, dr)
            
        if len(self.map) > self.capacity:
            # Random eviction (simple)
            k = next(iter(self.map))
            del self.map[k]

# ============================================================================
# 3. THE AGENT: CHIMERA
# ============================================================================

class ChimeraAgent:
    def __init__(self, env, config: ChimeraConfig):
        self.env = env
        self.cfg = config
        self.state_dim = env.observation_space.shape[0]
        self.action_dim = env.action_space.shape[0]
        
        # Neural Network (The Brain)
        self.brain = IdeaManifold(
            self.state_dim, self.action_dim, 
            self.cfg.hidden_dim, self.cfg.manifold_dim, 
            env.action_space
        ).to(device)
        
        self.target_brain = IdeaManifold(
            self.state_dim, self.action_dim, 
            self.cfg.hidden_dim, self.cfg.manifold_dim, 
            env.action_space
        ).to(device)
        self.target_brain.load_state_dict(self.brain.state_dict())
        
        self.optimizer = optim.Adam(self.brain.parameters(), lr=self.cfg.lr)
        
        # Memory Systems
        self.replay_buffer = deque(maxlen=self.cfg.buffer_size)
        self.temporal_field = TemporalField(config)
        self.geodesic_map = GeodesicMap()
        
        # Ratchet State (Wanderer)
        self.best_rolling_avg = -float('inf')
        self.current_rolling_avg = -float('inf')
        self.ratchet_triggered = False
        
        # Precision (Sand Agent)
        self.precision_pi = 1.0

    def select_action(self, state, evaluate=False):
        # 1. VAGABOND CHECK: Do we have a Geodesic shortcut?
        if not evaluate and not self.ratchet_triggered:
            h = self.temporal_field._hash(state)
            geo_action = self.geodesic_map.query(h)
            if geo_action is not None and random.random() < 0.4: # 40% chance to trust memory
                return geo_action

        # 2. NEURAL NETWORK ACTION
        state_t = torch.FloatTensor(state).to(device).unsqueeze(0)
        mean, log_std, _ = self.brain.act(state_t)
        
        if evaluate:
            action = torch.tanh(mean) * self.brain.action_scale + self.brain.action_bias
        else:
            std = log_std.exp()
            dist = torch.distributions.Normal(mean, std)
            x_t = dist.rsample()
            y_t = torch.tanh(x_t)
            action = y_t * self.brain.action_scale + self.brain.action_bias
            
        return action.detach().cpu().numpy()[0]

    def calc_dark_residue(self, state, action, next_state) -> float:
        """
        D = |K_tau - V_gamma|
        K_tau: Prediction Error (Self-Knowledge)
        V_gamma: Temporal Pressure (Environmental Resistance)
        """
        # Calculate K_tau using World Model (Saclet)
        with torch.no_grad():
            s = torch.FloatTensor(state).to(device).unsqueeze(0)
            a = torch.FloatTensor(action).to(device).unsqueeze(0)
            ns = torch.FloatTensor(next_state).to(device).unsqueeze(0)
            
            # Predict next MANIFOLD state
            pred_manifold_next = self.brain.predict_next(s, a)
            actual_manifold_next = self.brain.encode(ns)
            
            # K_tau is high if error is low (Inverted error)
            prediction_error = F.mse_loss(pred_manifold_next, actual_manifold_next).item()
            K_tau = 1.0 / (1.0 + prediction_error * 10.0) # Normalized roughly 0-1
            
        # Calculate V_gamma (Vagabond)
        V_gamma = self.temporal_field.get_pressure(state)
        # Normalize V_gamma roughly 0-1
        V_gamma = np.tanh(V_gamma)
        
        return abs(K_tau - V_gamma)

    def train_step(self):
        if len(self.replay_buffer) < self.cfg.batch_size:
            return
        
        batch = random.sample(self.replay_buffer, self.cfg.batch_size)
        state, action, reward, next_state, done = zip(*batch)
        
        state = torch.FloatTensor(np.array(state)).to(device)
        action = torch.FloatTensor(np.array(action)).to(device)
        reward = torch.FloatTensor(np.array(reward)).unsqueeze(1).to(device)
        next_state = torch.FloatTensor(np.array(next_state)).to(device)
        done = torch.FloatTensor(np.array(done)).unsqueeze(1).to(device)

        # ----------------------------------------
        # 1. Update Critic (Wendigo/SAC style)
        # ----------------------------------------
        with torch.no_grad():
            next_mean, next_log_std, _ = self.brain.act(next_state)
            next_std = next_log_std.exp()
            next_dist = torch.distributions.Normal(next_mean, next_std)
            next_action_sample = next_dist.rsample()
            next_action_tanh = torch.tanh(next_action_sample)
            next_action = next_action_tanh * self.brain.action_scale + self.brain.action_bias
            
            # Target Q
            target_q1, target_q2 = self.target_brain.get_q(next_state, next_action)
            target_q = torch.min(target_q1, target_q2)
            
            # Entropy term
            next_log_prob = next_dist.log_prob(next_action_sample).sum(-1, keepdim=True)
            next_log_prob -= torch.log(self.brain.action_scale * (1 - next_action_tanh.pow(2)) + 1e-6).sum(-1, keepdim=True)
            
            # Ratchet modulation: If triggered, alpha increases (Panic mode)
            current_alpha = self.cfg.alpha * (5.0 if self.ratchet_triggered else 1.0)
            target_q = reward + (1 - done) * self.cfg.gamma * (target_q - current_alpha * next_log_prob)

        current_q1, current_q2 = self.brain.get_q(state, action)
        critic_loss = F.mse_loss(current_q1, target_q) + F.mse_loss(current_q2, target_q)

        # ----------------------------------------
        # 2. Update World Model (Saclet)
        # ----------------------------------------
        # Predict next manifold state
        pred_next_manifold = self.brain.predict_next(state, action)
        # We need the target encoder's view of next state for stability
        with torch.no_grad():
            target_next_manifold = self.target_brain.encode(next_state)
            
        world_model_loss = F.mse_loss(pred_next_manifold, target_next_manifold)

        # ----------------------------------------
        # 3. Update Actor
        # ----------------------------------------
        mean, log_std, _ = self.brain.act(state)
        std = log_std.exp()
        dist = torch.distributions.Normal(mean, std)
        act_sample = dist.rsample()
        act_tanh = torch.tanh(act_sample)
        act_real = act_tanh * self.brain.action_scale + self.brain.action_bias
        
        log_prob = dist.log_prob(act_sample).sum(-1, keepdim=True)
        log_prob -= torch.log(self.brain.action_scale * (1 - act_tanh.pow(2)) + 1e-6).sum(-1, keepdim=True)
        
        q1_pi, q2_pi = self.brain.get_q(state, act_real)
        q_pi = torch.min(q1_pi, q2_pi)
        
        actor_loss = (current_alpha * log_prob - q_pi).mean()

        # ----------------------------------------
        # 4. Total Optimization (Sand Agent Precision)
        # ----------------------------------------
        # Apply Precision Gating from Sand Agent
        # If Pi is high (stable), we learn normally. If low, we reduce learning rate.
        weighted_loss = self.precision_pi * (critic_loss + actor_loss + world_model_loss)
        
        self.optimizer.zero_grad()
        weighted_loss.backward()
        nn.utils.clip_grad_norm_(self.brain.parameters(), 1.0)
        self.optimizer.step()
        
        # Soft Update
        for param, target_param in zip(self.brain.parameters(), self.target_brain.parameters()):
            target_param.data.copy_(self.cfg.tau * param.data + (1 - self.cfg.tau) * target_param.data)


    def train(self, max_episodes=500):
        print(f"🐲 CHIMERA PRIME INITIALIZED | Env: {self.cfg.env_name}")
        print("   > Assets: Pirouette Rewards (Wendigo), World Model (Saclet), Delta Field (Vagabond), Ratchet (Wanderer)")
        
        scores = deque(maxlen=20)
        
        for ep in range(1, max_episodes + 1):
            state, _ = self.env.reset()
            episode_reward = 0
            episode_dr = 0
            steps = 0
            
            previous_dr = 0.5 # Init
            
            done = False
            while not done:
                action = self.select_action(state)
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                
                # --- WENDIGO: Pirouette Reward Calculation ---
                current_dr = self.calc_dark_residue(state, action, next_state)
                dr_change = current_dr - previous_dr
                
                # Reward: Base + Coherence Gain (improving DR) - Dissonance (high DR) + Duration
                pirouette_reward = reward + \
                                   self.cfg.gamma_coherence * max(0, -dr_change) - \
                                   self.cfg.delta_dissonance * current_dr + \
                                   self.cfg.beta_duration
                                   
                # --- VAGABOND: Update Fields ---
                self.temporal_field.update(state, current_dr)
                self.geodesic_map.update(self.temporal_field._hash(state), action, current_dr)
                
                # Store
                self.replay_buffer.append((state, action, pirouette_reward, next_state, done))
                
                # Train
                self.train_step()
                
                state = next_state
                episode_reward += reward # Track RAW gym reward for logging
                episode_dr += current_dr
                steps += 1
                previous_dr = current_dr
            
            # --- WANDERER: The Ratchet ---
            avg_score = np.mean(scores) if scores else -999
            self.current_rolling_avg = avg_score
            
            if avg_score > self.best_rolling_avg:
                self.best_rolling_avg = avg_score
                self.ratchet_triggered = False
            elif avg_score < (self.best_rolling_avg - abs(self.best_rolling_avg) * self.cfg.ratchet_tolerance) and ep > 20:
                # Performance dropped significantly -> Trigger Ratchet (Panic/High Entropy)
                self.ratchet_triggered = True
                
            # --- SAND AGENT: Update Precision ---
            avg_dr = episode_dr / steps
            # Precision is inverse to Dark Residue (High DR = Low Precision/Stability)
            self.precision_pi = 1.0 / (1.0 + avg_dr)
            
            scores.append(episode_reward)
            
            if ep % 10 == 0:
                status = "🚨 RATCHET" if self.ratchet_triggered else "🟢 STABLE"
                print(f"Ep {ep:03d} | Reward: {episode_reward:6.1f} | Avg: {avg_score:6.1f} | DR: {avg_dr:.3f} | Pi: {self.precision_pi:.2f} | {status}")

            if avg_score > 200: # Solved threshold for LunarLander
                print("🏆 CHIMERA HAS CONQUERED THE DOMAIN.")
                break

if __name__ == "__main__":
    # Create Environment
    # Note: LunarLanderContinuous is a good test for this "Heavy" architecture
    env = gym.make("LunarLanderContinuous-v3")
    
    config = ChimeraConfig()
    agent = ChimeraAgent(env, config)
    
    try:
        agent.train()
    except KeyboardInterrupt:
        print("\n🛑 Training Interrupted. Chimera sleeps.")