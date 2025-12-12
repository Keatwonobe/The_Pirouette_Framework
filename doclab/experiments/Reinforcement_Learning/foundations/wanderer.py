import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import gymnasium as gym
import numpy as np
from collections import deque
import random
import math

# --- PIROUETTE FRAMEWORK CONSTANTS ---
# Tuned for "Sharp" behavior
CRITICAL_RESONANCE_SCALE = 10.0  # Multiplier to make Resonance harder to achieve (Sharpening the curve)
ENTHALPY_FLOOR = 0.05            # Minimum entropy even when resonant
RATCHET_TOLERANCE = 0.15         # How much backsliding is allowed before the Ratchet shatters the manifold
MANIFOLD_DIM = 64

class IdeaManifold(nn.Module):
    """
    Project: COG-RES-004: The Generative Engram.
    """
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super(IdeaManifold, self).__init__()
        
        # 1. Perception Layer
        self.perception = nn.Linear(state_dim, hidden_dim)
        
        # 2. The Internal Manifold (Latent Space)
        self.resonance_bridge = nn.Linear(hidden_dim, MANIFOLD_DIM)
        
        # 3. Action Head
        self.actor = nn.Linear(MANIFOLD_DIM, action_dim)
        
        # 4. Value Head
        self.critic = nn.Linear(MANIFOLD_DIM, 1)
        
        # 5. Autopoietic Head (The Predictor)
        self.autopoiesis_predictor = nn.Linear(MANIFOLD_DIM, MANIFOLD_DIM)

    def forward(self, x):
        x = F.tanh(self.perception(x))
        manifold_state = F.relu(self.resonance_bridge(x))
        
        # Standard Actor-Critic outputs
        action_probs = F.softmax(self.actor(manifold_state), dim=-1)
        value = self.critic(manifold_state)
        
        # Autopoietic Prediction
        predicted_next_manifold = self.autopoiesis_predictor(manifold_state)
        
        return action_probs, value, manifold_state, predicted_next_manifold

class Wanderer:
    """
    The 'Wanderer' Agent (Version 2.0: Ratcheted)
    
    New Mechanic: The Forward Ratchet.
    If performance drops below the historical high-water mark, Resonance is shattered.
    This prevents "Confident Failure" (High prediction accuracy, low reward).
    """
    def __init__(self, env_name):
        self.env = gym.make(env_name)
        self.state_dim = self.env.observation_space.shape[0]
        
        if isinstance(self.env.action_space, gym.spaces.Box):
            self.is_continuous = True
            self.action_dim = 11 
            self.action_map = np.linspace(self.env.action_space.low[0], self.env.action_space.high[0], self.action_dim)
        else:
            self.is_continuous = False
            self.action_dim = self.env.action_space.n
            
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.manifold = IdeaManifold(self.state_dim, self.action_dim).to(self.device)
        self.optimizer = optim.Adam(self.manifold.parameters(), lr=0.002)
        
        # Memory buffers
        self.log_probs = []
        self.values = []
        self.manifold_states = []
        self.predicted_manifolds = []
        self.rewards = []
        self.masks = []
        self.entropies = []
        
        # --- THE RATCHET STATE ---
        self.best_rolling_avg = -float('inf')
        self.current_rolling_avg = -float('inf')
        self.ratchet_locked = False # Debug flag
        self.resonance_history = deque(maxlen=100)

    def select_action(self, state):
        state = torch.FloatTensor(state).to(self.device).unsqueeze(0)
        probs, value, manifold_state, predicted_next = self.manifold(state)
        
        # --- ENTHALPIC INJECTION (Modulated by Ratchet) ---
        if len(self.resonance_history) > 0:
            avg_resonance = np.mean(self.resonance_history)
            
            # The Ratchet Logic is applied in the Update phase, but affects 
            # future resonance values stored in history, which we read here.
            # If the ratchet triggered recently, avg_resonance will be low.
            
            # Target Entropy: High if Resonance is Low.
            current_entropy_target = max(ENTHALPY_FLOOR, 1.0 - avg_resonance) 
        else:
            current_entropy_target = 0.5

        dist = torch.distributions.Categorical(probs)
        action = dist.sample()
        
        self.log_probs.append(dist.log_prob(action))
        self.values.append(value)
        self.entropies.append(dist.entropy())
        self.manifold_states.append(manifold_state)
        self.predicted_manifolds.append(predicted_next)
        
        action_idx = action.item()
        
        if self.is_continuous:
            return [self.action_map[action_idx]], action_idx
        return action_idx, action_idx

    def calculate_triadic_loss(self, next_value):
        returns = []
        R = next_value
        
        for step in reversed(range(len(self.rewards))):
            R = self.rewards[step] + 0.99 * R * self.masks[step]
            returns.insert(0, R)
            
        returns = torch.tensor(returns).to(self.device)
        log_probs = torch.stack(self.log_probs)
        values = torch.stack(self.values).squeeze()
        returns = (returns - returns.mean()) / (returns.std() + 1e-5)
        advantage = returns - values

        # --- AUTOPOIETIC LOSS & RAW RESONANCE ---
        current_manifolds = torch.stack(self.manifold_states)
        predicted_next = torch.stack(self.predicted_manifolds)
        
        if len(current_manifolds) > 1:
            pred_t = predicted_next[:-1]
            actual_t_plus_1 = current_manifolds[1:].detach()
            autopoiesis_loss = F.mse_loss(pred_t, actual_t_plus_1)
            
            # SHARPENING: Multiply loss by scale to make 1.0 harder to reach
            raw_resonance = torch.exp(-autopoiesis_loss * CRITICAL_RESONANCE_SCALE).item()
        else:
            autopoiesis_loss = torch.tensor(0.0).to(self.device)
            raw_resonance = 0.5

        # --- THE FORWARD RATCHET MECHANISM ---
        # "You cannot be resonant if you are backsliding."
        
        # 1. Check if we are failing relative to our best self
        # We give a tolerance buffer (e.g., 15% drop allowed before panic)
        # Note: Handling negative rewards (Acrobot) requires care with ratios.
        
        # Normalize for comparison logic
        # If best is -100 and current is -200, we are failing.
        # If best is +100 and current is +80, we are failing.
        
        dissonance_penalty = 0.0
        
        # Only apply ratchet if we have a baseline established
        if self.best_rolling_avg != -float('inf'):
            if self.current_rolling_avg < (self.best_rolling_avg - abs(self.best_rolling_avg) * RATCHET_TOLERANCE):
                # SHATTER THE MANIFOLD
                # We force resonance to 0. This triggers high entropy and high learning rates.
                dissonance_penalty = 1.0
                self.ratchet_locked = False
            else:
                self.ratchet_locked = True
        
        final_resonance = raw_resonance * (1.0 - dissonance_penalty)
        self.resonance_history.append(final_resonance)

        # Dynamic Entropy Weighting
        # If resonance is 0 (due to Ratchet or Confusion), Entropy Weight is MAX (0.1)
        # If resonance is 1, Entropy Weight is FLOOR
        entropy_weight = 0.1 * (1.0 - final_resonance) 

        # --- Triadic Loss ---
        actor_loss = -(log_probs * advantage.detach()).mean()
        critic_loss = advantage.pow(2).mean()
        manifold_loss = autopoiesis_loss 
        entropy_loss = -torch.stack(self.entropies).mean() * entropy_weight

        # Total Loss
        total_loss = actor_loss + 0.5 * critic_loss + 0.5 * manifold_loss + entropy_loss
        
        return total_loss, final_resonance

    def update(self, next_state):
        next_state = torch.FloatTensor(next_state).to(self.device).unsqueeze(0)
        _, next_value, _, _ = self.manifold(next_state)
        
        loss, resonance = self.calculate_triadic_loss(next_value.item())
        
        self.optimizer.zero_grad()
        loss.backward()
        
        # --- PULSE MODULATION ---
        # High Resonance = High Confidence = Larger Steps allowed
        # Low Resonance (Ratchet Triggered) = Caution? 
        # Actually, in the framework, "Chaos" usually implies high plasticity but potentially volatile gradients.
        # We will keep the clipping tighter when chaotic to prevent exploding gradients during the "panic" phase,
        # but the entropy injection will handle the exploration.
        max_grad_norm = 0.5 + (2.0 * resonance)
        nn.utils.clip_grad_norm_(self.manifold.parameters(), max_grad_norm)
        
        self.optimizer.step()
        
        # Clear buffers
        self.log_probs = []
        self.values = []
        self.rewards = []
        self.masks = []
        self.entropies = []
        self.manifold_states = []
        self.predicted_manifolds = []
        
        return loss.item(), resonance

    def train_episode(self, max_steps=1000):
        state, _ = self.env.reset()
        episode_reward = 0
        
        for t in range(max_steps):
            if self.is_continuous:
                action_gym, action_idx = self.select_action(state)
                next_state, reward, done, truncated, _ = self.env.step(action_gym)
            else:
                action_idx, _ = self.select_action(state)
                next_state, reward, done, truncated, _ = self.env.step(action_idx)
            
            # Reward shaping
            if "Acrobot" in self.env.spec.id:
                 reward += abs(next_state[0]) * 0.1 
            elif "Pendulum" in self.env.spec.id:
                # Pendulum standard reward is close to 0 for upright, large neg for down.
                # No shaping needed usually, but let's normalize slightly
                pass

            self.rewards.append(reward)
            self.masks.append(1 - done)
            
            state = next_state
            episode_reward += reward
            
            if done or truncated:
                break
        
        # Post-Episode Updates
        loss, res = self.update(state)
        return episode_reward, res

def train_wanderer(env_name, goal_reward, max_episodes=500):
    print(f"\n--- Initiating Wanderer in Domain: {env_name} (Mode: RATCHETED) ---")
    agent = Wanderer(env_name)
    
    running_reward_deque = deque(maxlen=20)
    
    for ep in range(max_episodes):
        reward, resonance = agent.train_episode()
        running_reward_deque.append(reward)
        avg_reward = np.mean(running_reward_deque)
        
        # Update Agent's Internal Ratchet State
        agent.current_rolling_avg = avg_reward
        if avg_reward > agent.best_rolling_avg:
            agent.best_rolling_avg = avg_reward
            
        # Logging
        if ep % 20 == 0:
            # Determine status string
            if resonance < 0.1:
                status = "DISSONANCE (RATCHET TRIGGERED)" 
            elif resonance < 0.8:
                status = "WANDERING"
            else:
                status = "RESONANT (LOCKED)"
                
            print(f"Episode {ep:3d} | Avg Reward: {avg_reward:6.1f} | Best: {agent.best_rolling_avg:6.1f} | Res: {resonance:.2f} | {status}")
        
        if avg_reward >= goal_reward:
            print(f"--> SOLVED in {ep} episodes! The Wanderer has found closure.")
            break
            
    return agent

if __name__ == "__main__":
    # 1. CartPole: High target to test stability
    train_wanderer("CartPole-v1", goal_reward=475)
    
    # 2. Acrobot: Negative reward domain
    train_wanderer("Acrobot-v1", goal_reward=-90)
    
    # 3. Pendulum
    train_wanderer("Pendulum-v1", goal_reward=-200)