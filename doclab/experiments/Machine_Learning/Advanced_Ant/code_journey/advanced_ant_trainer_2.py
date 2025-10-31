import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Normal
import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
from collections import deque, namedtuple
import random
import time
import os
import pywt # You may need to run: pip install PyWavelets

# --- Configuration ---
# You can change these parameters to experiment
ENV_NAME = 'Ant-v5'
NUM_EPISODES = 300
MAX_STEPS_PER_EPISODE = 1000
SHADOW_ANALYSIS_FREQUENCY = 10 # Analyze and adapt every 10 episodes
SEED = 42

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Set random seeds for reproducibility
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

# --- 1. Pirouette Analytics (Simplified Core) ---
class ContinuousPirouetteAnalytics:
    """A minimal implementation of Pirouette analytics needed for shadow detection."""
    def __init__(self):
        self.Ki_rest = 4.14159

    def temporal_coherence_spectrum(self, data, scales=None, wavelet='cmor1.0-1.0'):
        """
        Calculates the temporal coherence (Time-Adherence) of a time-series
        signal using a continuous wavelet transform. Low coherence indicates a
        "shadow" where the learning process is inconsistent.
        """
        if len(data) < 20: return None, None, None
        if scales is None:
            scales = np.arange(1, min(len(data) // 4, 128)) # CHANGED: Increased max scale
        
        coeffs, _ = pywt.cwt(data, scales, wavelet)
        phase = np.angle(coeffs)
        time_adherence = np.abs(np.mean(np.exp(1j * phase), axis=1))
        
        return coeffs, scales, time_adherence

# --- 2. Shadow Region Detection ---
class ContinuousShadowRegionDetector:
    """Detects shadow regions and suggests hyperparameter changes."""
    def __init__(self, analytics):
        self.analytics = analytics
        self.ki_rest = analytics.Ki_rest

    # CHANGED: Reworked the entire suggestion logic for more nuance.
    def analyze_and_suggest(self, data):
        """
        Analyzes data (like TD errors) for shadow regions and suggests new
        hyperparameters to escape them. This logic is now tiered.
        """
        if data is None or len(data) < 50:
            return {}

        # Preprocess data
        data_norm = (data - np.mean(data)) / (np.std(data) + 1e-6)
        
        # Get coherence spectrum
        _, _, coherence, = self.analytics.temporal_coherence_spectrum(data_norm)
        if coherence is None:
            return {}
            
        suggestions = {}
        mean_coherence = np.mean(coherence)
        print(f"INFO: Mean coherence of TD error is {mean_coherence:.4f}.")

        # Tier 1: Deep Shadow (Chaos) -> Focus on STABILITY
        if mean_coherence < 0.15:
            print("INFO: Deep shadow detected (chaos). Prioritizing stability.")
            suggestions['critic_lr'] = 1e-4    # Lower LR to stabilize
            suggestions['actor_lr'] = 1e-4     # Lower LR to stabilize
            suggestions['batch_size'] = 1024   # Larger batch to average out noise
            suggestions['alpha'] = 0.05        # Lower alpha for less random exploration

        # Tier 2: Moderate Shadow (Struggling) -> Methodical Exploration
        elif mean_coherence < 0.4:
            print("INFO: Moderate shadow detected (struggling). Using Ki-based exploration.")
            suggestions['critic_lr'] = self.ki_rest / 10000 # ~0.0004
            suggestions['actor_lr'] = self.ki_rest / 15000 # ~0.00027
            suggestions['batch_size'] = 512
            suggestions['alpha'] = 0.2                     # Standard alpha for exploration

        # Tier 3: Shallow Shadow (Fine-Tuning) -> Converge on good policy
        else: # mean_coherence >= 0.4
            print("INFO: Shallow shadow or stable learning detected. Fine-tuning.")
            suggestions['critic_lr'] = 5e-5    # Very low LR to converge carefully
            suggestions['actor_lr'] = 5e-5     # Very low LR to converge carefully
            suggestions['batch_size'] = 256
            suggestions['alpha'] = 0.1         # Less exploration, more exploitation
        
        return suggestions

# --- 3. SAC Agent (The Learner) ---
class ReplayBuffer:
    """A simple replay buffer for storing experiences."""
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)

class Actor(nn.Module):
    """Policy network."""
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super(Actor, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim), nn.ReLU()
        )
        self.mean = nn.Linear(hidden_dim, action_dim)
        self.log_std = nn.Linear(hidden_dim, action_dim)

    def forward(self, state):
        x = self.net(state)
        mean = self.mean(x)
        log_std = self.log_std(x)
        log_std = torch.clamp(log_std, -20, 2)
        return mean, log_std

class Critic(nn.Module):
    """Q-value network."""
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super(Critic, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, state, action):
        return self.net(torch.cat([state, action], 1))

class SACAgent:
    """The Soft Actor-Critic agent."""
    def __init__(self, env, hidden_dim=256, lr=3e-4, gamma=0.99, tau=0.005, alpha=0.2):
        self.env = env
        self.state_dim = env.observation_space.shape[0]
        self.action_dim = env.action_space.shape[0]
        self.action_scale = torch.FloatTensor((env.action_space.high - env.action_space.low) / 2.).to(device)
        self.action_bias = torch.FloatTensor((env.action_space.high + env.action_space.low) / 2.).to(device)
        
        self.gamma = gamma
        self.tau = tau
        self.alpha = alpha
        
        self.actor = Actor(self.state_dim, self.action_dim, hidden_dim).to(device)
        self.critic1 = Critic(self.state_dim, self.action_dim, hidden_dim).to(device)
        self.critic2 = Critic(self.state_dim, self.action_dim, hidden_dim).to(device)
        self.critic1_target = Critic(self.state_dim, self.action_dim, hidden_dim).to(device)
        self.critic2_target = Critic(self.state_dim, self.action_dim, hidden_dim).to(device)

        self.critic1_target.load_state_dict(self.critic1.state_dict())
        self.critic2_target.load_state_dict(self.critic2.state_dict())

        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=lr)
        self.critic1_optimizer = optim.Adam(self.critic1.parameters(), lr=lr)
        self.critic2_optimizer = optim.Adam(self.critic2.parameters(), lr=lr)
        
        self.replay_buffer = ReplayBuffer(1_000_000)
        self.td_errors = deque(maxlen=5000) # For shadow analysis

    def select_action(self, state, evaluate=False):
        state = torch.FloatTensor(state).to(device).unsqueeze(0)
        mean, log_std = self.actor(state)
        std = log_std.exp()
        normal = Normal(mean, std)
        
        if evaluate:
            action = torch.tanh(mean)
        else:
            x_t = normal.rsample()
            action = torch.tanh(x_t)
            
        return (action.cpu().detach().numpy()[0] * self.action_scale.cpu().numpy()) + self.action_bias.cpu().numpy()

    def update(self, batch_size):
        if len(self.replay_buffer) < batch_size:
            return

        state, action, reward, next_state, done = zip(*self.replay_buffer.sample(batch_size))
        
        state = torch.FloatTensor(np.array(state)).to(device)
        action = torch.FloatTensor(np.array(action)).to(device)
        reward = torch.FloatTensor(np.array(reward)).to(device).unsqueeze(1)
        next_state = torch.FloatTensor(np.array(next_state)).to(device)
        done = torch.FloatTensor(np.array(done)).to(device).unsqueeze(1)

        with torch.no_grad():
            next_mean, next_log_std = self.actor(next_state)
            next_std = next_log_std.exp()
            next_normal = Normal(next_mean, next_std)
            z = next_normal.rsample()
            next_action = torch.tanh(z)
            log_prob = next_normal.log_prob(z) - torch.log(1 - next_action.pow(2) + 1e-6)
            log_prob = log_prob.sum(1, keepdim=True)
            
            target_q1 = self.critic1_target(next_state, next_action)
            target_q2 = self.critic2_target(next_state, next_action)
            target_q = torch.min(target_q1, target_q2) - self.alpha * log_prob
            target_q = reward + (1 - done) * self.gamma * target_q
            
        current_q1 = self.critic1(state, action)
        current_q2 = self.critic2(state, action)

        td_error = (F.mse_loss(current_q1, target_q) + F.mse_loss(current_q2, target_q)).detach().cpu().item()
        self.td_errors.append(td_error)
        
        critic1_loss = F.mse_loss(current_q1, target_q)
        critic2_loss = F.mse_loss(current_q2, target_q)
        
        self.critic1_optimizer.zero_grad()
        critic1_loss.backward()
        self.critic1_optimizer.step()
        
        self.critic2_optimizer.zero_grad()
        critic2_loss.backward()
        self.critic2_optimizer.step()

        mean, log_std = self.actor(state)
        std = log_std.exp()
        normal = Normal(mean, std)
        z = normal.rsample()
        actor_action = torch.tanh(z)
        log_prob = normal.log_prob(z) - torch.log(1 - actor_action.pow(2) + 1e-6)
        log_prob = log_prob.sum(1, keepdim=True)
        
        q1_pi = self.critic1(state, actor_action)
        q2_pi = self.critic2(state, actor_action)
        min_q_pi = torch.min(q1_pi, q2_pi)
        
        actor_loss = ((self.alpha * log_prob) - min_q_pi).mean()
        
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()
        
        for target, source in zip(self.critic1_target.parameters(), self.critic1.parameters()):
            target.data.copy_(target.data * (1.0 - self.tau) + source.data * self.tau)
        for target, source in zip(self.critic2_target.parameters(), self.critic2.parameters()):
            target.data.copy_(target.data * (1.0 - self.tau) + source.data * self.tau)
            
    # CHANGED: Reworked suggestion application to provide clear before/after logging.
    def apply_suggestions(self, suggestions):
        """Applies hyperparameter suggestions with clear logging."""
        if not suggestions: return

        print("--- Applying Shadow-Aware Suggestions ---")
        if 'critic_lr' in suggestions:
            old_lr = self.critic1_optimizer.param_groups[0]['lr']
            new_lr = suggestions['critic_lr']
            print(f"Critic LR:     {old_lr:.6f} -> {new_lr:.6f}")
            for g in self.critic1_optimizer.param_groups: g['lr'] = new_lr
            for g in self.critic2_optimizer.param_groups: g['lr'] = new_lr
                
        if 'actor_lr' in suggestions:
            old_lr = self.actor_optimizer.param_groups[0]['lr']
            new_lr = suggestions['actor_lr']
            print(f"Actor LR:      {old_lr:.6f} -> {new_lr:.6f}")
            for g in self.actor_optimizer.param_groups: g['lr'] = new_lr
            
        if 'alpha' in suggestions:
            old_alpha = self.alpha
            self.alpha = suggestions['alpha']
            print(f"Alpha:         {old_alpha:.4f} -> {self.alpha:.4f}")
        print("----------------------------------------")

# --- 4. The Trainer (Main Orchestrator) ---
class ShadowAwareTrainer:
    """The main trainer that orchestrates the agent and shadow analysis."""
    def __init__(self, env_name, num_episodes, max_steps, analysis_freq):
        try:
            self.env = gym.make(env_name)
        except Exception as e:
            print(f"Error creating environment '{env_name}'. Is MuJoCo installed?")
            print("Try: pip install gymnasium[mujoco]")
            raise e
            
        self.agent = SACAgent(self.env)
        self.analytics = ContinuousPirouetteAnalytics()
        self.shadow_detector = ContinuousShadowRegionDetector(self.analytics)
        
        self.num_episodes = num_episodes
        self.max_steps = max_steps
        self.analysis_freq = analysis_freq
        self.batch_size = 256 # Initial batch size
        
        self.reward_history = []

    def train(self):
        """The main training loop."""
        total_steps = 0
        start_time = time.time()
        
        for episode in range(self.num_episodes):
            state, _ = self.env.reset(seed=SEED + episode)
            episode_reward = 0
            
            for step in range(self.max_steps):
                action = self.agent.select_action(state)
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                
                self.agent.replay_buffer.push(state, action, reward, next_state, done)
                self.agent.update(self.batch_size)
                
                state = next_state
                episode_reward += reward
                total_steps += 1
                
                if done:
                    break
            
            self.reward_history.append(episode_reward)
            avg_reward = np.mean(self.reward_history[-100:])
            
            # CHANGED: Added current LR and Batch Size to the log line for clarity.
            current_lr = self.agent.actor_optimizer.param_groups[0]['lr']
            log_line = (f"Episode: {episode+1}, Reward: {episode_reward:.1f}, "
                        f"Avg Reward: {avg_reward:.1f}, LR: {current_lr:.6f}, "
                        f"Batch: {self.batch_size}")
            print(log_line)

            # --- Shadow Analysis and Adaptation Step ---
            if episode > 0 and (episode + 1) % self.analysis_freq == 0:
                print(f"\n--- Running Shadow Analysis at Episode {episode+1} ---")
                
                suggestions = self.shadow_detector.analyze_and_suggest(
                    np.array(self.agent.td_errors)
                )
                
                self.agent.apply_suggestions(suggestions)
                if 'batch_size' in suggestions:
                    old_batch = self.batch_size
                    self.batch_size = suggestions['batch_size']
                    print(f"Batch Size:    {old_batch} -> {self.batch_size}")
                print("-------------------------------------------\n")

        training_time = time.time() - start_time
        print(f"\nTraining finished in {training_time:.2f} seconds.")
        self.plot_rewards()
        self.env.close()

    def plot_rewards(self):
        """Generates and saves a plot of the training rewards."""
        plt.figure(figsize=(12, 6))
        plt.plot(self.reward_history, label='Episode Reward', alpha=0.6)
        if len(self.reward_history) >= 50:
            moving_avg = np.convolve(self.reward_history, np.ones(50)/50, mode='valid')
            plt.plot(np.arange(49, len(self.reward_history)), moving_avg, 'r', linewidth=2, label='50-episode MA')
        plt.title(f"Training Rewards for {ENV_NAME} with Shadow-Aware Tuning")
        plt.xlabel("Episode")
        plt.ylabel("Total Reward")
        plt.legend()
        plt.grid(True)
        plt.savefig("shadow_aware_training_rewards.png")
        print("\nTraining plot saved to 'shadow_aware_training_rewards.png'")

# --- Main Execution ---
if __name__ == "__main__":
    trainer = ShadowAwareTrainer(
        env_name=ENV_NAME,
        num_episodes=NUM_EPISODES,
        max_steps=MAX_STEPS_PER_EPISODE,
        analysis_freq=SHADOW_ANALYSIS_FREQUENCY
    )
    trainer.train()