# pirouette_regime_trainer_v6.py
# This version provides a robust fix for the tensor shape mismatch in the A2C update,
# ensuring the computation graph remains intact.
#
## FIX & FEATURE UPDATE:
# - Corrected RuntimeError by ensuring the computation graph is not detached during training action selection.
# - Fixed the evaluation loop to correctly step through the environment.
# - Added a feature to save the top 10 best-performing models during training.

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Normal, Categorical
import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
from collections import deque
import time
import os
import shutil
import random

# --- Configuration ---
ENV_NAME = 'Ant-v5'
NUM_EPISODES = 5000
MAX_STEPS_PER_EPISODE = 500
EVAL_FREQUENCY = 50
EVAL_EPISODES = 10
SEED = 42
LIDAR_RAYS = 16
## FEATURE: Directory to save the best models
MODEL_SAVE_DIR = "top_10_models"


# --- Regime & RL Hyperparameters ---
NUM_APERTURES = 3
NUM_OBJECTIVES = 2
GAMMA = 0.99
LEARNING_RATE = 1e-4
ENTROPY_COEFF = 0.01

# Set device and seeds
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
np.random.seed(SEED); torch.manual_seed(SEED); random.seed(SEED)
print(f"Using device: {device}")


### --- Regime-Switching Crucible Environment (Unchanged) --- ###
class RegimeSwitchingCrucibleEnv:
    def __init__(self, env_name, max_steps):
        print("Initializing Regime-Switching Crucible Environment...")
        self.env = gym.make(env_name, render_mode=None)

        self.objectives = { 0: self._reward_traversal, 1: self._reward_hold_the_zone }
        self.control_apertures = { 0: lambda a: a, 1: lambda a: -a, 2: lambda a: a[[2, 3, 0, 1, 6, 7, 4, 5]] }

        self.gravity_w1 = (2 * np.pi) / (max_steps * 2)
        self.gravity_w2 = (2 * np.pi) / (max_steps * 0.75)

        flat_obs_dim = self.env.observation_space.shape[0] + LIDAR_RAYS
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(flat_obs_dim,), dtype=np.float32
        )
        self.action_space = self.env.action_space

    def reset(self, seed=None):
        self.current_objective = random.choice(list(self.objectives.keys()))
        self.current_aperture = random.choice(list(self.control_apertures.keys()))
        self.current_step = 0
        self.zone_center = np.random.uniform(-2, 2, size=2) if self.current_objective == 1 else None
        obs, info = self.env.reset(seed=seed)
        return self._get_obs(obs), info

    def step(self, agent_action):
        aperture_choice, control_input = agent_action
        motor_command = self.control_apertures[self.current_aperture](control_input)
        self.current_step += 1
        self._update_gravity()
        obs, reward, term, trunc, info = self.env.step(motor_command)
        regime_reward = self.objectives[self.current_objective](obs, reward, info)
        aperture_penalty = -1.0 if aperture_choice != self.current_aperture else 0.0
        total_reward = regime_reward + aperture_penalty
        return self._get_obs(obs), total_reward, term, trunc, info

    def _get_obs(self, obs):
        return np.concatenate([obs, self._perform_lidar_scan()])

    def _update_gravity(self):
        t = self.current_step
        g = -9.8 + 3.0 * np.sin(self.gravity_w1 * t) + 1.5 * np.cos(self.gravity_w2 * t)
        self.env.unwrapped.model.opt.gravity[2] = g

    def _reward_traversal(self, obs, reward, info):
        return info.get('reward_forward', 0)

    def _reward_hold_the_zone(self, obs, reward, info):
        agent_pos = self.env.unwrapped.data.qpos[:2]
        distance = np.linalg.norm(agent_pos - self.zone_center)
        return 1.0 if distance < 1.0 else -0.1

    def _perform_lidar_scan(self):
        agent_pos = self.env.unwrapped.data.qpos[:2]
        distances = np.ones(LIDAR_RAYS)
        if self.current_objective == 1:
            for i in range(LIDAR_RAYS):
                angle = (2 * np.pi * i) / LIDAR_RAYS
                distances[i] = np.linalg.norm(self.zone_center - agent_pos) * (1 + 0.1 * np.cos(angle))
        return np.clip(distances / 10.0, 0, 1).astype(np.float32)


### --- Advantage Actor-Critic (A2C) Agent (Update Corrected) --- ###
class ActorCritic(nn.Module):
    def __init__(self, state_dim, continuous_dim, discrete_dim, hidden_dim=256):
        super().__init__()
        self.shared_net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim), nn.ReLU()
        )
        self.mean_head = nn.Linear(hidden_dim, continuous_dim)
        self.log_std_head = nn.Linear(hidden_dim, continuous_dim)
        self.discrete_head = nn.Linear(hidden_dim, discrete_dim)
        self.value_head = nn.Linear(hidden_dim, 1)

    def forward(self, state):
        shared_features = self.shared_net(state)
        mean = self.mean_head(shared_features)
        log_std = torch.clamp(self.log_std_head(shared_features), -20, 2)
        discrete_logits = self.discrete_head(shared_features)
        value = self.value_head(shared_features)
        return mean, log_std, discrete_logits, value

class A2CAgent:
    def __init__(self, env):
        state_dim = env.observation_space.shape[0]
        continuous_dim = env.action_space.shape[0]

        self.model = ActorCritic(state_dim, continuous_dim, NUM_APERTURES).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE)

        self.log_probs = []
        self.values = []
        self.rewards = []
        self.entropy_term = 0

    ## FIX: Added 'evaluate' flag. The 'torch.no_grad()' wrapper was removed from here
    # to ensure that for training steps, the computation graph is built correctly.
    # When 'evaluate' is True, we skip storing values for backpropagation.
    def select_action(self, state, evaluate=False):
        state = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        mean, log_std, discrete_logits, value = self.model(state)

        dist_cont = Normal(mean, log_std.exp())
        cont_action = torch.tanh(dist_cont.sample())

        dist_disc = Categorical(logits=discrete_logits)
        disc_action = dist_disc.sample()

        # If not in evaluation mode, store the tensors required for the learning update.
        if not evaluate:
            log_prob_cont = dist_cont.log_prob(torch.atanh(torch.clamp(cont_action, -0.999, 0.999))).sum()
            log_prob_disc = dist_disc.log_prob(disc_action)

            self.log_probs.append(log_prob_cont + log_prob_disc)
            self.values.append(value)
            self.entropy_term += dist_cont.entropy().sum() + dist_disc.entropy()

        return disc_action.item(), cont_action.squeeze(0).cpu().numpy()

    def update(self, last_state):
        with torch.no_grad():
            _, _, _, last_value = self.model(torch.tensor(last_state, device=device, dtype=torch.float32).unsqueeze(0))

        returns = []
        R = last_value
        for r in reversed(self.rewards):
            R = r + GAMMA * R
            returns.insert(0, R)

        returns = torch.cat(returns).detach()
        values = torch.cat(self.values)

        returns = returns.view_as(values)
        advantages = returns - values
        log_probs = torch.cat(self.log_probs)

        actor_loss = -(log_probs * advantages.detach().squeeze()).mean()
        critic_loss = F.mse_loss(values, returns)
        loss = actor_loss + 0.5 * critic_loss - ENTROPY_COEFF * self.entropy_term

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Clear the buffers for the next episode
        self.log_probs = []
        self.values = []
        self.rewards = []
        self.entropy_term = 0

### --- Main Trainer (Updated) --- ###
def main():
    env = RegimeSwitchingCrucibleEnv(ENV_NAME, MAX_STEPS_PER_EPISODE)
    agent = A2CAgent(env)

    ## FEATURE: Set up model saving directory and a list to track top models
    if os.path.exists(MODEL_SAVE_DIR):
        print(f"Removing old model directory: {MODEL_SAVE_DIR}")
        shutil.rmtree(MODEL_SAVE_DIR)
    os.makedirs(MODEL_SAVE_DIR)
    top_models = [] # Will store tuples of (score, path)

    eval_scores = []
    print("Starting training with A2C Agent (v6 Fixed)...")
    for ep in range(1, NUM_EPISODES + 1):
        s, _ = env.reset(seed=SEED + ep)
        ep_r = 0
        agent.model.train() # Ensure model is in training mode

        for step in range(MAX_STEPS_PER_EPISODE):
            action_tuple = agent.select_action(s, evaluate=False) # 'evaluate=False' for training
            s_next, r, term, trunc, info = env.step(action_tuple)

            agent.rewards.append(r)

            s = s_next
            ep_r += r
            if term or trunc: break

        agent.update(s_next)

        print(f"Ep:{ep:04d} | Regime(Obj:{env.current_objective}, Apt:{env.current_aperture}) | Reward:{ep_r:7.2f}")

        ## FIX: The evaluation loop is now corrected and wrapped in torch.no_grad()
        if ep % EVAL_FREQUENCY == 0:
            total_eval_reward = 0
            agent.model.eval() # Set model to evaluation mode
            with torch.no_grad():
                for _ in range(EVAL_EPISODES):
                    s_eval, _ = env.reset()
                    ep_eval_r = 0
                    for _ in range(MAX_STEPS_PER_EPISODE):
                        # Pass evaluate=True to prevent storing tensors for backprop
                        action_tuple = agent.select_action(s_eval, evaluate=True)
                        s_next_eval, r_eval, term_eval, trunc_eval, _ = env.step(action_tuple)
                        s_eval = s_next_eval
                        ep_eval_r += r_eval # Use the reward from the evaluation step
                        if term_eval or trunc_eval: break
                    total_eval_reward += ep_eval_r

            avg_eval_score = total_eval_reward / EVAL_EPISODES
            eval_scores.append(avg_eval_score)
            print(f"  > EVALUATION | Avg Score: {avg_eval_score:.2f}")

            ## FEATURE: Logic to save the top 10 models
            is_top_model = False
            if len(top_models) < 10 or avg_eval_score > top_models[-1][0]:
                save_path = os.path.join(MODEL_SAVE_DIR, f"model_ep{ep}_score{avg_eval_score:.2f}.pth")
                torch.save(agent.model.state_dict(), save_path)
                top_models.append((avg_eval_score, save_path))
                # Sort descending by score
                top_models.sort(key=lambda x: x[0], reverse=True)
                is_top_model = True

                # If we have more than 10 models, remove the worst one
                if len(top_models) > 10:
                    model_to_remove = top_models.pop()
                    try:
                        os.remove(model_to_remove[1])
                    except OSError as e:
                        print(f"Error removing old model file: {e}")

            if is_top_model:
                print(f"  > Saved new top-10 model with score: {avg_eval_score:.2f}")


    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(np.arange(1, len(eval_scores) + 1) * EVAL_FREQUENCY, eval_scores)
    plt.title("Regime-Switching Crucible Performance (A2C Agent)")
    plt.xlabel("Episode"); plt.ylabel("Average Evaluation Score"); plt.grid(True)
    plt.savefig("regime_switching_results_v6_fixed.png")
    print("\nTraining complete. Plot saved to regime_switching_results_v6_fixed.png")
    print(f"Top 10 models saved in '{MODEL_SAVE_DIR}' directory.")


if __name__ == "__main__":
    main()