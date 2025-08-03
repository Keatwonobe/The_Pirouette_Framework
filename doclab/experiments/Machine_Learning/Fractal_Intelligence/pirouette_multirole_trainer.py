# pirouette_multirole_trainer.py
# The capstone experiment: A multi-role agent trained in a "Meta-Crucible"
# with random environments and random seeds for each episode.

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Normal, Categorical
import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
from collections import deque, namedtuple
import time
import random

# --- Configuration ---
# A dictionary defining the environments we want the agent to master
ENV_CONFIGS = {
    'ant': {'name': 'Ant-v5'},
    'pendulum': {'name': 'Pendulum-v1'},
    'half_cheetah': {'name': 'HalfCheetah-v5'}
}
NUM_EPISODES = 10000 # This task requires significantly more training
MAX_STEPS_PER_EPISODE = 500 
EVAL_FREQUENCY = 100
EVAL_EPISODES = 20

# --- RL Hyperparameters ---
GAMMA = 0.99 
LEARNING_RATE = 3e-4 
ENTROPY_COEFF = 0.01
ID_LOSS_COEFF = 0.5 # Weight for the environment identification loss

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
# We will generate seeds on the fly, so the global seed is less important
torch.manual_seed(int(time.time()))

### --- The Meta-Crucible Environment --- ###
class MetaCrucibleEnv:
    def __init__(self, configs):
        print("Initializing Meta-Crucible Environment...")
        self.configs = configs
        self.env_names = list(configs.keys())
        self.envs = {name: gym.make(cfg['name']) for name, cfg in configs.items()}
        
        # Determine padding dimensions
        self.max_obs_dim = max(env.observation_space.shape[0] for env in self.envs.values())
        self.max_action_dim = max(env.action_space.shape[0] for env in self.envs.values())
        
        # Unified observation and action spaces
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(self.max_obs_dim,), dtype=np.float32)
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(self.max_action_dim,), dtype=np.float32)
        print(f"Unified Obs Dim: {self.max_obs_dim}, Unified Action Dim: {self.max_action_dim}")

    def reset(self):
        # Randomly select an environment and a seed for this episode
        self.active_env_name = random.choice(self.env_names)
        self.active_env = self.envs[self.active_env_name]
        seed = int(time.time() * 1000) % (2**32)
        
        obs, info = self.active_env.reset(seed=seed)
        info['env_name'] = self.active_env_name
        info['seed'] = seed
        return self._pad_obs(obs), info

    def step(self, action):
        unpadded_action = self._unpad_action(action)
        next_obs, reward, term, trunc, info = self.active_env.step(unpadded_action)
        info['env_name'] = self.active_env_name
        return self._pad_obs(next_obs), reward, term, trunc, info

    def _pad_obs(self, obs):
        padded = np.zeros(self.max_obs_dim, dtype=np.float32)
        padded[:len(obs)] = obs
        return padded

    def _unpad_action(self, action):
        true_action_dim = self.active_env.action_space.shape[0]
        return action[:true_action_dim]

### --- The Multi-Role Agent Architecture --- ###
class MultiRoleAgent(nn.Module):
    def __init__(self, obs_dim, action_dim, env_configs, hidden_dim=256):
        super().__init__()
        self.env_names = list(env_configs.keys())
        
        # Shared perception trunk
        self.perception_trunk = nn.Sequential(nn.Linear(obs_dim, hidden_dim), nn.ReLU(), nn.Linear(hidden_dim, hidden_dim), nn.ReLU())
        
        # Head for identifying the environment
        self.identification_head = nn.Linear(hidden_dim, len(self.env_names))
        
        # Specialized heads for policy (actor) and value (critic) for each environment
        self.policy_heads = nn.ModuleDict()
        self.value_heads = nn.ModuleDict()
        for name, config in env_configs.items():
            env = gym.make(config['name'])
            action_d = env.action_space.shape[0]
            self.policy_heads[name] = nn.Sequential(nn.Linear(hidden_dim, action_d * 2)) # For mean and log_std
            self.value_heads[name] = nn.Linear(hidden_dim, 1)

        self.optimizer = optim.Adam(self.parameters(), lr=LEARNING_RATE)
        self.memory = []

    def select_action(self, state):
        state = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            shared_features = self.perception_trunk(state)
            id_logits = self.identification_head(shared_features)
            
            # Identify environment
            predicted_env_idx = torch.argmax(id_logits, dim=1).item()
            predicted_env_name = self.env_names[predicted_env_idx]
            
            # Use the correct policy head
            policy_output = self.policy_heads[predicted_env_name](shared_features)
            mean, log_std = torch.chunk(policy_output, 2, dim=-1)
            dist = Normal(mean, log_std.exp())
            action = torch.tanh(dist.sample())
        
        return action.squeeze(0).cpu().numpy(), predicted_env_name

    def update(self):
        if not self.memory: return
        
        # Unpack trajectory
        states, actions, rewards, true_env_names = zip(*self.memory)
        
        # Convert to tensors
        states = torch.tensor(np.array(states), device=device, dtype=torch.float32)
        actions = torch.tensor(np.array(actions), device=device, dtype=torch.float32)
        rewards = torch.tensor(rewards, device=device, dtype=torch.float32)
        true_env_indices = torch.tensor([self.env_names.index(name) for name in true_env_names], device=device)
        
        # --- Forward pass for the whole trajectory ---
        shared_features = self.perception_trunk(states)
        id_logits = self.identification_head(shared_features)
        
        # --- 1. Calculate Identification Loss ---
        id_loss = F.cross_entropy(id_logits, true_env_indices)

        # --- 2. Calculate Actor-Critic Loss (A2C style) ---
        actor_loss = 0
        critic_loss = 0
        entropy = 0
        
        # Process each environment's data separately
        for i, name in enumerate(self.env_names):
            mask = (true_env_indices == i)
            if not mask.any(): continue
            
            # Get data for this environment
            env_features = shared_features[mask]
            env_actions = actions[mask]
            env_rewards = rewards[mask]
            
            # Value estimates (critic)
            values = self.value_heads[name](env_features).squeeze()
            
            # Policy estimates (actor)
            policy_output = self.policy_heads[name](env_features)
            mean, log_std = torch.chunk(policy_output, 2, dim=-1)
            dist = Normal(mean, log_std.exp())
            
            # Calculate advantage
            returns = []
            R = values[-1].item() # Bootstrap from the last state's value
            for r in reversed(env_rewards):
                R = r + GAMMA * R
                returns.insert(0, R)
            returns = torch.tensor(returns, device=device)
            advantages = returns - values.detach()
            
            # Accumulate losses
            log_probs = dist.log_prob(torch.atanh(torch.clamp(env_actions, -0.999, 0.999))).sum(dim=-1)
            actor_loss += -(log_probs * advantages).mean()
            critic_loss += F.mse_loss(values, returns)
            entropy += dist.entropy().mean()

        # --- Combine losses and update ---
        total_loss = actor_loss + 0.5 * critic_loss - ENTROPY_COEFF * entropy + ID_LOSS_COEFF * id_loss
        
        self.optimizer.zero_grad()
        total_loss.backward()
        self.optimizer.step()

        self.memory = [] # Clear memory after update

### --- Main Training Loop --- ###
def main():
    env = MetaCrucibleEnv(ENV_CONFIGS)
    agent = MultiRoleAgent(env.max_obs_dim, env.max_action_dim, ENV_CONFIGS)
    
    eval_scores = {}
    id_accuracies = []
    
    print("Starting Multi-Role training...")
    for ep in range(1, NUM_EPISODES + 1):
        s, info = env.reset()
        ep_r, ep_steps = 0, 0
        
        for step in range(MAX_STEPS_PER_EPISODE):
            action, _ = agent.select_action(s)
            s_next, r, term, trunc, info_next = env.step(action)
            
            agent.memory.append((s, action, r, info['env_name']))
            
            s = s_next; ep_r += r; ep_steps += 1
            info = info_next
            if term or trunc: break
        
        agent.update() # Update at the end of the episode
        
        print(f"Ep:{ep:05d} | Seed:{info['seed']} | Env:'{info['env_name']}' | Reward:{ep_r:8.2f}")
        
        if ep % EVAL_FREQUENCY == 0:
            # Evaluation
            correct_identifications = 0
            total_evals = 0
            temp_eval_scores = {name: [] for name in env.env_names}
            
            for _ in range(EVAL_EPISODES):
                s, info = env.reset()
                ep_eval_r = 0
                for _ in range(MAX_STEPS_PER_EPISODE):
                    action, predicted_env = agent.select_action(s)
                    if predicted_env == info['env_name']:
                        correct_identifications += 1
                    total_evals += 1
                    
                    s, r, term, trunc, info = env.step(action)
                    ep_eval_r += r
                    if term or trunc: break
                temp_eval_scores[info['env_name']].append(ep_eval_r)

            id_accuracy = (correct_identifications / total_evals) * 100
            id_accuracies.append(id_accuracy)
            
            print(f"\n--- EVALUATION @ Ep {ep} ---")
            print(f"  > Identification Accuracy: {id_accuracy:.2f}%")
            for name, scores in temp_eval_scores.items():
                if scores:
                    avg_score = np.mean(scores)
                    if name not in eval_scores: eval_scores[name] = []
                    eval_scores[name].append(avg_score)
                    print(f"  > Avg Score for '{name}': {avg_score:.2f}")
            print("---------------------------\n")

    # Plotting
    fig, axs = plt.subplots(2, 1, figsize=(15, 12), sharex=True)
    fig.suptitle("Multi-Role Agent Performance in Meta-Crucible")
    
    for name, scores in eval_scores.items():
        axs[0].plot(np.arange(1, len(scores) + 1) * EVAL_FREQUENCY, scores, marker='o', linestyle='-', label=f"Score '{name}'")
    axs[0].set_ylabel("Average Evaluation Score")
    axs[0].legend(); axs[0].grid(True)
    
    axs[1].plot(np.arange(1, len(id_accuracies) + 1) * EVAL_FREQUENCY, id_accuracies, 'r-', label='Identification Accuracy')
    axs[1].set_ylabel("Accuracy (%)")
    axs[1].set_xlabel("Episode")
    axs[1].legend(); axs[1].grid(True)
    
    plt.savefig("multirole_results.png")
    print("Training complete. Plot saved to multirole_results.png")

if __name__ == "__main__":
    main()