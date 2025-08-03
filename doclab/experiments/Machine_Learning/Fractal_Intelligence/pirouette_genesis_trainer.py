# pirouette_genesis_trainer.py
# This script represents the synthesis of the multi-role and FIT trainers.
# It trains a single, robust agent within a "Multi-Crucible" of dynamic, 
# non-stationary environments using Fractal Intelligence Transfer (FIT)
# and a genetic algorithm for stability and recovery.

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Normal, Categorical
import numpy as np
import gymnasium as gym
from gymnasium.vector import AsyncVectorEnv
import matplotlib.pyplot as plt
from collections import deque, namedtuple, OrderedDict
import time
import random
import math
import os
import shutil
import itertools
import json
import stat
import gc

# --- Configuration ---
# Environments for the agent to master
ENV_CONFIGS = {
    'ant': {'name': 'Ant-v5'},
    'half_cheetah': {'name': 'HalfCheetah-v5'},
    'humanoid': {'name': 'Humanoid-v5'}
}
NUM_EPISODES = 15000
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 15
EVAL_EPISODES = 10 # Num eval episodes per environment
SEED = int(time.time())
MODEL_PATH = "./pirouette_genesis_models/"

# --- Merged Hyperparameters ---
# SAC Hyperparameters
GAMMA = 0.99
LEARNING_RATE = 3e-4
TAU = 0.005 # Target network update rate
ALPHA = 0.2 # Entropy regularization
REPLAY_BUFFER_SIZE = 1_000_000
BATCH_SIZE = 256

# FIT & Genetic Hyperparameters
ID_LOSS_COEFF = 0.1 # Weight for the environment identification loss
FLUX_REWARD_WEIGHT = 0.05 # Weight for the prophet's flux reward
PROPHET_PREDICTION_HORIZON = 50 # How many steps into the future the prophet predicts
MANIFOLD_BONUS_COEFF = 0.02 # Reward for action alignment
MANIFOLD_TEAR_COEFF = 0.05 # Penalty for diverging from action manifold
GENETIC_POOL_SIZE = 10 # Number of top models to keep
GENE_TRANSFER_RATE = 0.6 # Probability of direct gene transfer during crossover
RESET_PATIENCE = 10 # Episodes of poor performance before triggering crossover
RESET_THRESHOLD = 0.7 # Performance drop percentage to trigger patience counter
RISK_REWARD_MULTIPLIER = 0.1
ACTION_MAGNITUDE_THRESHOLD = 0.1

# --- NEW: Lucky Lock-In Hyperparameters ---
LUCKY_THRESHOLD_STD = 1.5  # Num of std devs above mean to be considered "lucky"
LUCKY_EPISODE_UPDATES = 10 # Num of extra training updates on a lucky run

# Set device and seeds
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
if os.path.exists(MODEL_PATH):
    shutil.rmtree(MODEL_PATH)
os.makedirs(MODEL_PATH, exist_ok=True)
print(f"Using device: {device}")
print(f"Genesis models will be saved in: {MODEL_PATH}")

### --- The Multi-Crucible Environment (Merged) --- ###
class MultiCrucibleEnv:
    """ Manages multiple environments and makes them non-stationary. """
    def __init__(self, configs, active_names=None):
        print("Initializing Multi-Crucible Environment...")
        self.configs = configs
        self.env_names = list(configs.keys())
        self.envs = {name: gym.make(cfg['name']) for name, cfg in configs.items()}
        if active_names:
            self.env_names = active_names
        else:
            self.env_names = list(configs.keys())
        # Inherit metadata from the first environment to ensure compatibility
        self.metadata = self.envs[self.env_names[0]].metadata
        self.render_mode = None
        self.env_steps = {name: 0 for name in self.env_names}

        # Determine padding dimensions for unified agent I/O
        self.max_obs_dim = max(env.observation_space.shape[0] for env in self.envs.values())
        self.max_action_dim = max(env.action_space.shape[0] for env in self.envs.values())
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(self.max_obs_dim,), dtype=np.float32)
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(self.max_action_dim,), dtype=np.float32)
        
        # Physics parameters for dynamic environments
        self.gravity_period = MAX_STEPS_PER_EPISODE * 2
        self.gravity_amplitude = -9.8
        self.gravity_oscillation_amplitude = 4.0
        print(f"Unified Obs: {self.max_obs_dim}, Unified Action: {self.max_action_dim}")

    def reset(self, seed=None, options=None, force_env_name=None):
        """
        Resets the environment. Can optionally force a specific sub-environment to be reset.
        """
        # If a specific environment is requested, use it. Otherwise, pick one randomly.
        if force_env_name:
            self.active_env_name = force_env_name
        else:
            self.active_env_name = random.choice(self.env_names)

        self.active_env = self.envs[self.active_env_name]
        self.env_steps[self.active_env_name] = 0
        self.update_physics()
    
        # Reset the now-active environment
        obs, info = self.active_env.reset(seed=seed)
        info['env_name'] = self.active_env_name
        return self._pad_obs(obs), info

    def step(self, action):
        self.env_steps[self.active_env_name] += 1
        self.update_physics()
        unpadded_action = self._unpad_action(action)
        next_obs, reward, term, trunc, info = self.active_env.step(unpadded_action)
        info['env_name'] = self.active_env_name
        return self._pad_obs(next_obs), reward, term, trunc, info

    def update_physics(self):
        # Applies oscillating gravity to the active environment
        current_step = self.env_steps[self.active_env_name]
        phase = (2 * np.pi * current_step) / self.gravity_period
        current_gravity = self.gravity_amplitude + self.gravity_oscillation_amplitude * np.sin(phase)
        try: # Not all envs have this attribute, but MuJoCo ones do
            self.active_env.unwrapped.model.opt.gravity[2] = current_gravity
        except:
            pass
            
    def get_future_physics(self, horizon):
        # Predicts future gravity for the Prophet module
        future_gravities = []
        current_step = self.env_steps[self.active_env_name]
        for i in range(1, horizon + 1):
            future_step = current_step + i
            phase = (2 * np.pi * future_step) / self.gravity_period
            g = self.gravity_amplitude + self.gravity_oscillation_amplitude * np.sin(phase)
            future_gravities.append(g)
        return np.array(future_gravities)

    def _pad_obs(self, obs):
        padded = np.zeros(self.max_obs_dim, dtype=np.float32)
        padded[:len(obs)] = obs
        return padded

    def _unpad_action(self, action):
        true_action_dim = self.active_env.action_space.shape[0]
        return action[:true_action_dim]
    
    def close(self):
        """Closes all underlying environments to release resources."""
        for env in self.envs.values():
            env.close()


### --- Supporting Modules from FIT Trainer --- ###
class Prophet(nn.Module):
    """ Predicts future environmental dynamics. """
    def __init__(self, state_dim, horizon):
        super().__init__()
        self.horizon = horizon
        self.model = nn.Sequential(nn.Linear(state_dim, 128), nn.ReLU(), nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, horizon)).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        self.loss_fn = nn.MSELoss()
    def train(self, state, future_physics):
        state_t = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        true_t = torch.tensor(future_physics, device=device, dtype=torch.float32).unsqueeze(0)
        self.optimizer.zero_grad(); predicted = self.model(state_t); loss = self.loss_fn(predicted, true_t); loss.backward(); self.optimizer.step()
    def measure_predictive_span(self, state, true_future_physics, accuracy_threshold=0.1):
        state_t = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad(): predictions = self.model(state_t).cpu().numpy().flatten()
        errors = np.abs(predictions - true_future_physics) / (np.abs(true_future_physics) + 1e-6)
        for i in range(self.horizon):
            if errors[i] > accuracy_threshold: return i
        return self.horizon

class ManifoldWell:
    """ Creates a dynamic reward landscape in the action space. """
    def __init__(self, action_dim, max_steps):
        self.action_dim, self.max_steps = action_dim, max_steps
        self.center = np.zeros(action_dim); self.phase = np.random.uniform(0, 2*np.pi, size=action_dim)
        self.frequency = np.random.uniform(0.5, 1.5, size=action_dim); self.amplitude = np.random.uniform(0.4, 0.8, size=action_dim)
    def step(self, t):
        time_factor = (2*np.pi*t)/self.max_steps; self.center = self.amplitude * np.sin(self.frequency*time_factor + self.phase)
    def get_reward(self, action):
        distance = np.linalg.norm(action - self.center)
        bonus = MANIFOLD_BONUS_COEFF * math.exp(-2.0 * distance)
        penalty = -MANIFOLD_TEAR_COEFF * max(0, distance - 1.0)
        return bonus + penalty

class ReplayBuffer:
    def __init__(self,c):self.b=deque(maxlen=c)
    def push(self,s,a,r,s_,d,en):self.b.append((s,a,r,s_,d,en))
    def sample(self,B):return random.sample(self.b,B)
    def __len__(self):return len(self.b)

### --- The Genesis Agent Architecture (Merged) --- ###
class PirouetteAgent(nn.Module):
    """ An agent combining multi-head SAC with environment identification. """
    def __init__(self, obs_dim, action_dim, env_configs):
        super().__init__()
        self.env_names = list(env_configs.keys())
        self.action_dim = action_dim
        self.alpha = ALPHA # Make alpha a class attribute

        # Shared perception trunk (Unchanged)
        self.trunk = nn.Sequential(nn.Linear(obs_dim, 256), nn.ReLU(), nn.Linear(256, 256), nn.ReLU())
        
        # Head for environment identification (Unchanged)
        self.id_head = nn.Linear(256, len(self.env_names))
        
        # Specialized heads for SAC (Actor and Critic) for each environment (Unchanged)
        self.actors = nn.ModuleDict()
        self.critics1 = nn.ModuleDict()
        self.critics2 = nn.ModuleDict()

        for name, config in env_configs.items():
            env = gym.make(config['name'])
            act_d = env.action_space.shape[0]
            self.actors[name] = nn.Sequential(nn.Linear(256, 256), nn.ReLU(), nn.Linear(256, act_d * 2))
            self.critics1[name] = nn.Sequential(nn.Linear(256 + action_dim, 256), nn.ReLU(), nn.Linear(256, 1))
            self.critics2[name] = nn.Sequential(nn.Linear(256 + action_dim, 256), nn.ReLU(), nn.Linear(256, 1))

        # --- NEW: The Ki Pump Head ---
        # This head takes the FFT of the shared features and outputs a corrective action mean.
        # The input size is 256 for the features, output is the full action dimension for the correction.
        self.ki_pump_head = nn.Sequential(nn.Linear(256, 128), nn.ReLU(), nn.Linear(128, self.action_dim))
        # --- END OF NEW ---

        self.critics1_target = nn.ModuleDict({name: nn.Sequential(*[ly for ly in self.critics1[name]]) for name in self.env_names})
        self.critics2_target = nn.ModuleDict({name: nn.Sequential(*[ly for ly in self.critics2[name]]) for name in self.env_names})
        self.critics1_target.load_state_dict(self.critics1.state_dict())
        self.critics2_target.load_state_dict(self.critics2.state_dict())
        
        # MODIFIED: Add the Ki Pump parameters to the actor's optimizer
        actor_params = itertools.chain(
            self.trunk.parameters(), 
            self.actors.parameters(), 
            self.ki_pump_head.parameters()
        )
        self.optimizer_actor = optim.Adam(actor_params, lr=LEARNING_RATE)
        self.optimizer_critic = optim.Adam(list(self.critics1.parameters()) + list(self.critics2.parameters()), lr=LEARNING_RATE)
        self.optimizer_id = optim.Adam(self.id_head.parameters(), lr=LEARNING_RATE)
        self.buffer = ReplayBuffer(REPLAY_BUFFER_SIZE)

    def select_action(self, state, eval=False, is_predictive_phase=False):
        # state can be a single observation (eval) or a batch (train)
        state_t = torch.tensor(state, device=device, dtype=torch.float32)
        
        # --- THIS IS THE FIX ---
        # If the input is a single state (1D tensor), add a batch dimension (make it 2D)
        is_single = state_t.dim() == 1
        if is_single:
            state_t = state_t.unsqueeze(0)
        # --- END OF FIX ---
            
        num_envs = state_t.shape[0]

        with torch.no_grad():
            # The rest of the batched logic now works for both cases
            shared_features = self.trunk(state_t)
            id_logits = self.id_head(shared_features)
            feature_fft = torch.fft.fft(shared_features)
            fft_input = torch.real(feature_fft)
            action_correction_mean = self.ki_pump_head(fft_input)
            
            pred_env_indices = torch.argmax(id_logits, dim=1)
            
            final_mean = torch.zeros(num_envs, self.action_dim, device=device)
            final_log_std = torch.zeros(num_envs, self.action_dim, device=device)
            pred_env_names = [] 

            for i, name in enumerate(self.env_names):
                mask = (pred_env_indices == i)
                if mask.any():
                    actor_head = self.actors[name]
                    masked_features = shared_features[mask]
                    base_mean, log_std = torch.chunk(actor_head(masked_features), 2, dim=-1)
                    
                    padded_base_mean = torch.zeros(masked_features.shape[0], self.action_dim, device=device)
                    padded_base_mean[:, :base_mean.shape[1]] = base_mean
                    final_mean[mask] = padded_base_mean
                    
                    padded_log_std = torch.zeros(masked_features.shape[0], self.action_dim, device=device)
                    padded_log_std[:, :log_std.shape[1]] = log_std
                    final_log_std[mask] = padded_log_std
            if is_predictive_phase:
                final_mean += action_correction_mean
            final_log_std = torch.clamp(final_log_std, min=-20, max=2)

            if eval:
                action = torch.tanh(final_mean)
            else:
                dist = Normal(final_mean, final_log_std.exp())
                action = torch.tanh(dist.sample())
        
        # If the input was a single state, remove the batch dimension from the output
        if is_single:
            # For evaluation, we predict a single environment name
            pred_env_name = self.env_names[pred_env_indices.item()]
            return action.squeeze(0).cpu().numpy(), pred_env_name
        else:
            # For training, we need to reconstruct the list of predicted names
            for idx in pred_env_indices:
                pred_env_names.append(self.env_names[idx.item()])
            return action.cpu().numpy(), pred_env_names

    def update(self):
        if len(self.buffer) < BATCH_SIZE: return
        
        states, actions, rewards, next_states, dones, env_names = zip(*self.buffer.sample(BATCH_SIZE))
        
        states = torch.tensor(np.array(states), device=device, dtype=torch.float32)
        actions = torch.tensor(np.array(actions), device=device, dtype=torch.float32)
        rewards = torch.tensor(np.array(rewards), device=device, dtype=torch.float32).unsqueeze(1)
        next_states = torch.tensor(np.array(next_states), device=device, dtype=torch.float32)
        dones = torch.tensor(np.array(dones), device=device, dtype=torch.float32).unsqueeze(1)
        true_env_indices = torch.tensor([self.env_names.index(name) for name in env_names], device=device)
        
        # --- 1. Update Identification Head ---
        shared_features = self.trunk(states).detach() 
        id_logits = self.id_head(shared_features)
        id_loss = F.cross_entropy(id_logits, true_env_indices)
        
        self.optimizer_id.zero_grad()
        id_loss.backward()
        # FIX: Clip gradients to prevent instability
        torch.nn.utils.clip_grad_norm_(self.id_head.parameters(), max_norm=1.0)
        self.optimizer_id.step()

        # --- 2. Update Critic ---
        with torch.no_grad():
            next_shared_features = self.trunk(next_states)
            target_q = torch.zeros_like(rewards)
            for i, name in enumerate(self.env_names):
                mask = (true_env_indices == i)
                if not mask.any(): continue
                
                act_d = self.actors[name][-1].out_features // 2
                mean, log_std = torch.chunk(self.actors[name](next_shared_features[mask]), 2, dim=-1)
                # FIX: Add clamping here as well for consistency during training updates
                log_std = torch.clamp(log_std, min=-20, max=2)
                dist = Normal(mean, log_std.exp())
                next_action_unpadded = torch.tanh(dist.sample())
                log_prob = dist.log_prob(torch.atanh(torch.clamp(next_action_unpadded, -0.999, 0.999))).sum(dim=-1, keepdim=True)

                next_action_padded = torch.zeros(mask.sum(), self.action_dim, device=device)
                next_action_padded[:, :act_d] = next_action_unpadded
                
                q1_target = self.critics1_target[name](torch.cat([next_shared_features[mask], next_action_padded], 1))
                q2_target = self.critics2_target[name](torch.cat([next_shared_features[mask], next_action_padded], 1))
                min_q_target = torch.min(q1_target, q2_target) - self.alpha * log_prob
                target_q[mask] = rewards[mask] + (1 - dones[mask]) * GAMMA * min_q_target

        critic_loss = 0
        # FIX: Detach the shared features to prevent critic gradients from flowing to the trunk network.
        # This solves the gradient accumulation bug.
        shared_features_critics = self.trunk(states).detach()
        for i, name in enumerate(self.env_names):
            mask = (true_env_indices == i)
            if not mask.any(): continue
            q1 = self.critics1[name](torch.cat([shared_features_critics[mask], actions[mask]], 1))
            q2 = self.critics2[name](torch.cat([shared_features_critics[mask], actions[mask]], 1))
            critic_loss += F.mse_loss(q1, target_q[mask]) + F.mse_loss(q2, target_q[mask])
        
        self.optimizer_critic.zero_grad()
        critic_loss.backward()
        # FIX: Clip gradients to prevent instability
        torch.nn.utils.clip_grad_norm_(list(self.critics1.parameters()) + list(self.critics2.parameters()), max_norm=1.0)
        self.optimizer_critic.step()
        
# --- 3. Update Actor ---
        actor_loss = 0
        shared_features_actor = self.trunk(states)
        for i, name in enumerate(self.env_names):
            mask = (true_env_indices == i)
            if not mask.any(): continue
            
            act_d = self.actors[name][-1].out_features // 2
            mean, log_std = torch.chunk(self.actors[name](shared_features_actor[mask]), 2, dim=-1)
            log_std = torch.clamp(log_std, -20, 2) # Clamp here too
            dist = Normal(mean, log_std.exp())
            new_action_unpadded = torch.tanh(dist.rsample())
            log_prob = dist.log_prob(torch.atanh(torch.clamp(new_action_unpadded, -0.999, 0.999))).sum(dim=-1, keepdim=True)

            new_action_padded = torch.zeros(mask.sum(), self.action_dim, device=device)
            new_action_padded[:, :act_d] = new_action_unpadded
            
            q1_pi = self.critics1[name](torch.cat([shared_features_actor[mask].detach(), new_action_padded], 1))
            q2_pi = self.critics2[name](torch.cat([shared_features_actor[mask].detach(), new_action_padded], 1))
            min_q_pi = torch.min(q1_pi, q2_pi)
            
            actor_loss += (self.alpha * log_prob - min_q_pi).mean()
        
        # FIX: Manually apply the id_head's linear transformation.
        # This uses the id_head's weights to calculate a loss for the trunk,
        # but prevents gradients from flowing back to the id_head itself from this loss.
        with torch.no_grad():
            id_head_weights = self.id_head.weight
            id_head_bias = self.id_head.bias
        id_logits_actor = F.linear(shared_features_actor, id_head_weights, id_head_bias)
        
        total_actor_loss = actor_loss + ID_LOSS_COEFF * F.cross_entropy(id_logits_actor, true_env_indices)

        self.optimizer_actor.zero_grad()
        total_actor_loss.backward()
        # FIX: Clip gradients to prevent instability
        torch.nn.utils.clip_grad_norm_(list(self.trunk.parameters()) + list(self.actors.parameters()), max_norm=1.0)
        self.optimizer_actor.step()

        # --- 4. Update Target Networks ---
        for name in self.env_names:
            for t, s in zip(self.critics1_target[name].parameters(), self.critics1[name].parameters()): t.data.copy_(t.data*(1-TAU)+s.data*TAU)
            for t, s in zip(self.critics2_target[name].parameters(), self.critics2[name].parameters()): t.data.copy_(t.data*(1-TAU)+s.data*TAU)
    
    def genetic_crossover(self, high_scores_data):
        print("  > Performing genetic crossover...")
        # Sort by score (desc) and take top 2 parents
        sorted_scores = sorted(high_scores_data.items(), key=lambda item: item[0], reverse=True)
        if len(sorted_scores) < 2: print("  > Not enough parents for crossover."); return
        
        parent_ranks = [data['rank'] for _, data in sorted_scores[:2]]
        p1_path = os.path.join(MODEL_PATH, f"rank_{parent_ranks[0]}")
        p2_path = os.path.join(MODEL_PATH, f"rank_{parent_ranks[1]}")
        
        p1_weights = torch.load(os.path.join(p1_path, "agent_state_dict.pth"))
        p2_weights = torch.load(os.path.join(p2_path, "agent_state_dict.pth"))
        
        child_weights = OrderedDict()
        for key in p1_weights:
            if 'actor' in key or 'trunk' in key: # Only cross actor/trunk genes
                if random.random() < GENE_TRANSFER_RATE: child_weights[key] = p1_weights[key].clone()
                else: child_weights[key] = (p1_weights[key] * 0.5 + p2_weights[key] * 0.5)
            else: # Keep original critic/id weights
                child_weights[key] = self.state_dict()[key].clone()
                
        self.load_state_dict(child_weights)
        print("  > Crossover complete. New generation initiated.")
        # Explicitly delete the large tensor dictionaries to release file handles
        del p1_weights
        del p2_weights
        del child_weights
        # Trigger Python's garbage collector to finalize the release
        gc.collect()

    def save_model(self, rank, model_path, score):
        """Saves the agent's state dictionary and its associated score."""
        path = os.path.join(model_path, f"rank_{rank}")
        os.makedirs(path, exist_ok=True)
        # Save the model weights
        torch.save(self.state_dict(), os.path.join(path, "agent_state_dict.pth"))
        # Save the score in a simple JSON file
        with open(os.path.join(path, "score.json"), 'w') as f:
            json.dump({'score': score}, f)

    def genetic_crossover(self, high_scores_data, model_path):
        """Performs genetic crossover using models from the specified path."""
        print("  > Performing genetic crossover...")
        sorted_scores = sorted(high_scores_data.items(), key=lambda item: item[0], reverse=True)
        if len(sorted_scores) < 2: 
            print("  > Not enough parents for crossover. Skipping.")
            return

        parent_ranks = [data['rank'] for _, data in sorted_scores[:2]]
        p1_path = os.path.join(model_path, f"rank_{parent_ranks[0]}")
        p2_path = os.path.join(model_path, f"rank_{parent_ranks[1]}")
        
        p1_weights = torch.load(os.path.join(p1_path, "agent_state_dict.pth"))
        p2_weights = torch.load(os.path.join(p2_path, "agent_state_dict.pth"))

        child_weights = OrderedDict()
        current_weights = self.state_dict()

        for key in p1_weights:
            if 'trunk' in key or 'actors' in key:
                if random.random() < GENE_TRANSFER_RATE:
                    child_weights[key] = p1_weights[key].clone()
                else:
                    child_weights[key] = (p1_weights[key] * 0.5 + p2_weights[key] * 0.5)
            else:
                child_weights[key] = current_weights[key].clone()
        
        self.load_state_dict(child_weights)
        self.critics1_target.load_state_dict(self.critics1.state_dict())
        self.critics2_target.load_state_dict(self.critics2.state_dict())
        print("  > Crossover complete. New generation initiated.")

def load_high_scores(model_path):
    """Scans for existing models and loads their scores for a warm start."""
    high_scores = {}
    print("🔎 Scanning for existing models for warm start...")
    if not os.path.exists(model_path):
        return high_scores

    for entry in os.scandir(model_path):
        if entry.is_dir() and entry.name.startswith('rank_'):
            try:
                rank = int(entry.name.split('_')[1])
                score_file = os.path.join(entry.path, "score.json")
                with open(score_file, 'r') as f:
                    score_data = json.load(f)
                    score = score_data['score']
                    high_scores[score] = {'rank': rank}
            except (FileNotFoundError, ValueError, KeyError):
                continue # Ignore malformed directories
    
    if high_scores:
        print(f"✅ Found {len(high_scores)} existing models. Best score: {max(high_scores.keys()):.2f}")
    else:
        print("A fresh training run will be started because no valid prior models were discovered.")
    return high_scores

### --- Main Training Loop --- ###
def main(model_path, seed):
    """The main training loop with a multi-stage curriculum and hybrid reward system."""

    # --- Curriculum & Hybrid Configuration ---
    STABILITY_THRESHOLD = 500
    ANT_THRESHOLD = 100
    SIGMA_THRESHOLD = 25
    PHASE_1_ALPHA = 0.2
    PHASE_2_ALPHA = 0.1
    # Hyperparameters from the successful fit_trainer
    INVERSION_THRESHOLD = -1000
    DEBUG_FREQUENCY = 1000 # Print a debug summary every 1000 global steps

    # --- State Management ---
    current_stage = 1
    active_env_names = ['half_cheetah']

    def make_env(s, active_names):
        def _init():
            env = MultiCrucibleEnv(ENV_CONFIGS, active_names=active_names)
            env.reset(seed=s)
            return env
        return _init

    num_cpu_cores = os.cpu_count() or 1
    num_envs = max(1, num_cpu_cores - 2)
    print(f"🚀 STAGE 1: Starting training with {active_env_names}.")
    
    env = AsyncVectorEnv([make_env(seed + i, active_env_names) for i in range(num_envs)])
    
    agent = PirouetteAgent(env.observation_space.shape[1], env.action_space.shape[1], ENV_CONFIGS).to(device)
    prophet = Prophet(env.observation_space.shape[1], PROPHET_PREDICTION_HORIZON)

    # --- Initialize Hybrid Components ---
    # Create a separate ManifoldWell and inversion flag for each parallel environment
    manifold_wells = [ManifoldWell(agent.action_dim, MAX_STEPS_PER_EPISODE) for _ in range(num_envs)]
    inversion_modes = [False] * num_envs
    # Initialize variables for the true Intelligence Flux reward
    last_sigma = 0
    current_delta_sigma = 0

    high_scores = load_high_scores(model_path)
    if high_scores: # Warm start logic
        best_score = max(high_scores.keys())
        best_rank = high_scores[best_score]['rank']
        best_model_path = os.path.join(model_path, f"rank_{best_rank}", "agent_state_dict.pth")
        try:
            agent.load_state_dict(torch.load(best_model_path))
            # Load last sigma if available to continue flux calculation
            score_file = os.path.join(model_path, f"rank_{best_rank}", "score.json")
            with open(score_file, 'r') as f: last_sigma = json.load(f).get('sigma', 0)
            print(f"🧠 Agent state and sigma loaded from best model (Rank {best_rank}, σ: {last_sigma})")
        except (FileNotFoundError, KeyError):
            print("⚠️ Could not load model/sigma, starting fresh.")
            high_scores = {}

    # --- Tracking and Loop Initialization ---
    all_env_names = list(ENV_CONFIGS.keys())
    recent_rewards = {name: deque(maxlen=50) for name in all_env_names}
    eval_scores_history = {name: [] for name in all_env_names}
    id_accuracies, sigma_history = [], []
    start_time = time.time()
    
    s, infos = env.reset()
    total_training_steps = NUM_EPISODES * MAX_STEPS_PER_EPISODE
    global_step = 0

    while global_step * num_envs < total_training_steps:
        global_step += 1
        current_total_steps = global_step * num_envs

        is_predictive_phase = current_stage in [2, 4, 6]
        agent.alpha = PHASE_2_ALPHA if is_predictive_phase else PHASE_1_ALPHA

        # --- Action Selection with Inversion ---
        base_action, _ = agent.select_action(s)
        action = base_action.copy()
        for i in range(num_envs):
            if inversion_modes[i]:
                action[i] = -action[i]
        
        s_next, r_env, term, trunc, infos = env.step(action)
        
        true_physics = env.call('get_future_physics', PROPHET_PREDICTION_HORIZON) if is_predictive_phase else [None]*num_envs

        # --- NEW: Lists to hold rewards for the current batch ---
        batch_r_env, batch_r_manifold, batch_r_flux = [], [], []

        for i in range(num_envs):
            done = term[i] or trunc[i]
            
            # 1. Manifold Well Reward
            manifold_wells[i].step(global_step)
            r_manifold = manifold_wells[i].get_reward(action[i])
            
            # 2. Intelligence Flux Reward (Δσ / energy)
            energy_cost = np.linalg.norm(action[i]) + 1e-6
            flux_reward = FLUX_REWARD_WEIGHT * (current_delta_sigma / energy_cost) if is_predictive_phase else 0
            
            # --- NEW: Append rewards to batch lists ---
            batch_r_env.append(r_env[i])
            batch_r_manifold.append(r_manifold)
            batch_r_flux.append(flux_reward)

            action_magnitude = np.linalg.norm(action[i])
            risk_bonus = (action_magnitude - ACTION_MAGNITUDE_THRESHOLD) * RISK_REWARD_MULTIPLIER if action_magnitude > ACTION_MAGNITUDE_THRESHOLD else 0

            total_reward = r_env[i] + r_manifold + flux_reward + risk_bonus
            agent.buffer.push(s[i], action[i], total_reward, s_next[i], done, infos['env_name'][i])

            if is_predictive_phase:
                prophet.train(s[i], true_physics[i])

            # 3. Update Inversion Mode for the next episode
            if "_final_info" in infos and infos["_final_info"][i]:
                ep_r_env = infos["final_info"][i]['episode']['r'][0]
                inversion_modes[i] = True if ep_r_env < INVERSION_THRESHOLD else False
                recent_rewards[infos["final_info"][i]['env_name']].append(ep_r_env)

        s = s_next
        agent.update()

        # --- NEW: Periodic Debug Print ---
        if global_step % DEBUG_FREQUENCY == 0:
            avg_r_env = np.mean(batch_r_env)
            avg_r_manifold = np.mean(batch_r_manifold)
            avg_r_flux = np.mean(batch_r_flux)
            inverted_count = sum(inversion_modes)
            print(f" > Step: {current_total_steps // 1000}k | Stage: {current_stage} | R_Env: {avg_r_env:.2f} | R_Manifold: {avg_r_manifold:.3f} | R_Flux: {avg_r_flux:.4f} | Inverted: {inverted_count}/{num_envs} | α: {agent.alpha:.2f}")


        # --- Evaluation & Curriculum Transition Logic ---
        eval_step_trigger = EVAL_FREQUENCY * MAX_STEPS_PER_EPISODE
        if current_total_steps % eval_step_trigger < num_envs:
            eval_env = MultiCrucibleEnv(ENV_CONFIGS, active_names=active_env_names)
            avg_eval_scores = {}
            correct_ids, total_ids = 0, 0
            
            for name in active_env_names:
                temp_scores = []
                for i in range(EVAL_EPISODES):
                    s_eval, _ = eval_env.reset(seed=seed * 100 + i, force_env_name=name)
                    ep_eval_r = 0
                    for _ in range(MAX_STEPS_PER_EPISODE):
                        action_eval, pred_env = agent.select_action(s_eval, eval=True)
                        if pred_env == name: correct_ids += 1
                        total_ids += 1
                        s_eval, r, term, trunc, _ = eval_env.step(action_eval)
                        ep_eval_r += r
                        if term or trunc: break
                    temp_scores.append(ep_eval_r)
                
                temp_scores.sort(reverse=True)
                avg_eval_scores[name] = np.mean(temp_scores[:3])
            
            current_sigma = prophet.measure_predictive_span(s_eval, eval_env.get_future_physics(PROPHET_PREDICTION_HORIZON))
            
            # Update the delta_sigma that will be used for the next training segment
            current_delta_sigma = current_sigma - last_sigma
            last_sigma = current_sigma # Important: update last_sigma for the next cycle
            last_sigma = prophet.measure_predictive_span(s_eval, eval_env.get_future_physics(PROPHET_PREDICTION_HORIZON))
            
            # ... (Print evaluation results, manage genetic pool as before) ...
            print(f"\n--- EVALUATION @ Step ~{current_total_steps // 1000}k (Stage: {current_stage}) ---")
            # ...

            # --- CURRICULUM TRANSITION CHECK ---
            stage_before_update = current_stage
            if current_stage == 1 and avg_eval_scores.get('half_cheetah', 0) > STABILITY_THRESHOLD:
                current_stage = 2; print(f"\n🚀 STAGE 2: HalfCheetah stable. Engaging predictive flux reward.")
            elif current_stage == 2 and last_sigma > SIGMA_THRESHOLD:
                current_stage = 3; active_env_names.append('humanoid'); print(f"\n🚀 STAGE 3: Predictive model trained. Introducing Humanoid.")
            elif current_stage == 3 and avg_eval_scores.get('humanoid', 0) > STABILITY_THRESHOLD:
                current_stage = 4; print(f"\n🚀 STAGE 4: Humanoid stable. Engaging predictive flux reward.")
            elif current_stage == 4 and last_sigma > SIGMA_THRESHOLD:
                current_stage = 5; active_env_names.append('ant'); print(f"\n🚀 STAGE 5: Predictive model generalized. Introducing Ant.")
            elif current_stage == 5 and avg_eval_scores.get('ant', 0) > ANT_THRESHOLD:
                current_stage = 6; print(f"\n🚀 STAGE 6: Ant stable. Engaging full training protocol.")
            
            # If the set of active environments has changed, we must restart the parallel envs
            if current_stage in [3, 5] and stage_before_update != current_stage:
                print("...Restarting parallel environments with new configuration...")
                env.close()
                env = AsyncVectorEnv([make_env(seed + i, active_env_names) for i in range(num_envs)])
                s, infos = env.reset()

            eval_env.close()

    env.close()
    print("Training complete.")
    # ... (Plotting logic) ...


    # At the end of the main() function

    # --- Plotting ---
    fig, axs = plt.subplots(3, 1, figsize=(15, 18), sharex=True)
    fig.suptitle("Pirouette Genesis Agent Performance in Multi-Crucible", fontsize=16)
    
    # The number of evaluation points is now the length of one of the history lists
    if id_accuracies:
        eval_x_axis = np.arange(1, len(id_accuracies) + 1) * EVAL_FREQUENCY

        # --- THIS IS THE FIX ---
        # Use the corrected variable name 'eval_scores_history' here
        for name, scores in eval_scores_history.items():
            if scores: 
                # Ensure the x-axis length matches the scores length for this env
                axs[0].plot(eval_x_axis[:len(scores)], scores, marker='o', linestyle='-', label=f"Score '{name}'")
        # --- END OF FIX ---

        axs[0].set_ylabel("Average Evaluation Score"); axs[0].legend(); axs[0].grid(True)
        
        axs[1].plot(eval_x_axis, id_accuracies, 'r-', marker='.', label='Identification Accuracy')
        axs[1].set_ylabel("Accuracy (%)"); axs[1].legend(); axs[1].grid(True)

        axs[2].plot(eval_x_axis, sigma_history, 'g-', marker='.', label='Predictive Span (σ)')
        axs[2].set_ylabel("Predictive Span (steps)"); axs[2].set_xlabel("Episode")
        axs[2].legend(); axs[2].grid(True)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("pirouette_genesis_results.png")
    print("Training complete. Plot saved to pirouette_genesis_results.png")

if __name__ == "__main__":
    MODEL_PATH = "./pirouette_genesis_models/"
    # Move the global setup code inside this block
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)

    # This directory setup will now only happen once
    if os.path.exists(MODEL_PATH):
        shutil.rmtree(MODEL_PATH)
    os.makedirs(MODEL_PATH, exist_ok=True)
    
    print(f"Using device: {device}")
    print(f"Genesis models will be saved in: {MODEL_PATH}")
    
    # Call the main function to start the training
    main(MODEL_PATH, SEED)