"""
Rambler: PPO-style actor-critic that can train on:
  - CartPole-v1      (Discrete)
  - Acrobot-v1       (Discrete)
  - Pendulum-v1      (Continuous)

Usage examples:
  python rambler.py --env CartPole-v1
  python rambler.py --env Acrobot-v1
  python rambler.py --env Pendulum-v1

You can tweak hyperparameters at the bottom of this file or via CLI flags.
"""

import argparse
import math
import random
from collections import deque

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical, Normal


# -------------------------
# Utility: Seeding & Device
# -------------------------

def make_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def get_device(prefer_gpu: bool = True):
    if prefer_gpu and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


# -------------------------
# Environment Config Map
# -------------------------

class EnvConfig:
    def __init__(
        self,
        gamma=0.99,
        reward_scale=1.0,
        solved_threshold=None,
        max_steps=1_000_000,
    ):
        self.gamma = gamma
        self.reward_scale = reward_scale
        self.solved_threshold = solved_threshold
        self.max_steps = max_steps


ENV_CONFIGS = {
    "CartPole-v1": EnvConfig(
        gamma=0.99,
        reward_scale=1.0,
        solved_threshold=475.0,  # running mean over last 100 episodes
        max_steps=300_000,
    ),
    "Acrobot-v1": EnvConfig(
        gamma=0.99,
        reward_scale=1.0,
        solved_threshold=-100.0,  # mean return ≥ -100 is "solved-ish"
        max_steps=600_000,
    ),
    "Pendulum-v1": EnvConfig(
        gamma=0.99,
        reward_scale=0.1,        # shrink magnitude to stabilize learning
        solved_threshold=-200.0, # mean ≥ -200 is decent control
        max_steps=600_000,
    ),
}


def get_env_config(env_id: str) -> EnvConfig:
    return ENV_CONFIGS.get(env_id, EnvConfig())


# -------------------------
# Normalization Helpers
# -------------------------

class RunningMeanStd:
    """
    Track running mean and variance for observation normalization.
    """

    def __init__(self, shape, eps=1e-4, momentum=0.01):
        self.mean = np.zeros(shape, dtype=np.float64)
        self.var = np.ones(shape, dtype=np.float64)
        self.count = eps
        self.momentum = momentum

    def update(self, x: np.ndarray):
        x = np.asarray(x, dtype=np.float64)
        batch_mean = x.mean(axis=0)
        batch_var = x.var(axis=0)
        batch_count = x.shape[0]

        # Update via exponential moving average for stability
        self.mean = (1 - self.momentum) * self.mean + self.momentum * batch_mean
        self.var = (1 - self.momentum) * self.var + self.momentum * batch_var
        self.count += batch_count

    def normalize(self, x: np.ndarray):
        return (x - self.mean) / (np.sqrt(self.var) + 1e-8)


# -------------------------
# Actor-Critic Network
# -------------------------

class ActorCritic(nn.Module):
    def __init__(self, obs_dim, action_space, hidden_sizes=(128, 128)):
        super().__init__()
        self.is_discrete = isinstance(action_space, gym.spaces.Discrete)
        self.obs_dim = obs_dim

        # Shared torso
        layers = []
        last = obs_dim
        for h in hidden_sizes:
            layers.append(nn.Linear(last, h))
            layers.append(nn.Tanh())
            last = h
        self.shared = nn.Sequential(*layers)

        # Policy head(s)
        if self.is_discrete:
            self.n_actions = action_space.n
            self.policy_head = nn.Linear(last, self.n_actions)
            self.log_std = None
        else:
            # Continuous (e.g. Pendulum)
            self.action_dim = action_space.shape[0]
            self.policy_mean = nn.Linear(last, self.action_dim)
            # Log-std is a learned parameter (state-independent)
            self.log_std = nn.Parameter(torch.zeros(self.action_dim))
            self.action_low = torch.as_tensor(action_space.low, dtype=torch.float32)
            self.action_high = torch.as_tensor(action_space.high, dtype=torch.float32)

        # Value head
        self.value_head = nn.Linear(last, 1)

    def forward(self, obs):
        raise NotImplementedError("Use get_action_and_value / evaluate_actions")

    def _shared_forward(self, obs: torch.Tensor):
        return self.shared(obs)

    def get_dist(self, obs: torch.Tensor):
        x = self._shared_forward(obs)
        if self.is_discrete:
            logits = self.policy_head(x)
            return Categorical(logits=logits)
        else:
            mean = self.policy_mean(x)
            std = torch.exp(self.log_std)
            return Normal(mean, std)

    def get_value(self, obs: torch.Tensor):
        x = self._shared_forward(obs)
        return self.value_head(x).squeeze(-1)

    def get_action_and_value(self, obs: torch.Tensor):
        dist = self.get_dist(obs)
        if self.is_discrete:
            action = dist.sample()
        else:
            action = dist.sample()
            # clamp instead of tanh-squash for simplicity
            action = torch.clamp(
                action,
                self.action_low.to(action.device),
                self.action_high.to(action.device),
            )
        log_prob = dist.log_prob(action)
        if not self.is_discrete:
            log_prob = log_prob.sum(-1)
        value = self.get_value(obs)
        return action, log_prob, value

    def evaluate_actions(self, obs: torch.Tensor, actions: torch.Tensor):
        dist = self.get_dist(obs)
        if self.is_discrete:
            log_probs = dist.log_prob(actions)
            entropy = dist.entropy()
        else:
            log_probs = dist.log_prob(actions).sum(-1)
            entropy = dist.entropy().sum(-1)
        values = self.get_value(obs)
        return log_probs, values, entropy


# -------------------------
# GAE & PPO Update
# -------------------------

def compute_gae(
    rewards,
    values,
    dones,
    last_value,
    gamma=0.99,
    gae_lambda=0.95,
):
    """
    rewards, values, dones: lists/arrays of length T
    last_value: V(s_T)
    """
    T = len(rewards)
    advantages = np.zeros(T, dtype=np.float32)
    last_adv = 0.0

    for t in reversed(range(T)):
        if t == T - 1:
            next_non_terminal = 1.0 - dones[t]
            next_value = last_value
        else:
            next_non_terminal = 1.0 - dones[t + 1]
            next_value = values[t + 1]
        delta = rewards[t] + gamma * next_value * next_non_terminal - values[t]
        last_adv = delta + gamma * gae_lambda * next_non_terminal * last_adv
        advantages[t] = last_adv

    returns = advantages + values
    return advantages, returns


def ppo_update(
    model: ActorCritic,
    optimizer: optim.Optimizer,
    obs,
    actions,
    logprobs,
    advantages,
    returns,
    clip_coef=0.2,
    vf_coef=0.5,
    ent_coef=0.01,
    max_grad_norm=0.5,
    epochs=4,
    batch_size=64,
):

    N = obs.shape[0]
    idxs = np.arange(N)

    for _ in range(epochs):
        np.random.shuffle(idxs)
        for start in range(0, N, batch_size):
            end = start + batch_size
            batch_idx = idxs[start:end]

            b_obs = obs[batch_idx]
            b_actions = actions[batch_idx]
            b_logprobs = logprobs[batch_idx]
            b_adv = advantages[batch_idx]
            b_ret = returns[batch_idx]

            new_logprobs, values, entropy = model.evaluate_actions(b_obs, b_actions)

            ratio = torch.exp(new_logprobs - b_logprobs)

            # PPO clipped surrogate
            unclipped = ratio * b_adv
            clipped = torch.clamp(ratio, 1.0 - clip_coef, 1.0 + clip_coef) * b_adv
            policy_loss = -torch.min(unclipped, clipped).mean()

            # Value loss
            value_loss = ((values - b_ret) ** 2).mean()

            # Entropy bonus
            entropy_loss = -entropy.mean()

            loss = policy_loss + vf_coef * value_loss + ent_coef * entropy_loss

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()


# -------------------------
# Training Loop
# -------------------------

def train_rambler(
    env_id: str = "CartPole-v1",
    total_timesteps: int = None,
    seed: int = 42,
    device: torch.device = None,
    rollout_horizon: int = 2048,
    ppo_epochs: int = 10,
    batch_size: int = 64,
    learning_rate: float = 3e-4,
    clip_coef: float = 0.2,
    gae_lambda: float = 0.95,
    vf_coef: float = 0.5,
    ent_coef: float = 0.01,
):

    cfg = get_env_config(env_id)
    if total_timesteps is None:
        total_timesteps = cfg.max_steps

    make_seed(seed)

    env = gym.make(env_id)
    obs, info = env.reset(seed=seed)

    obs_shape = env.observation_space.shape
    if len(obs_shape) != 1:
        raise ValueError("This script assumes 1D observation spaces.")
    obs_dim = obs_shape[0]

    model = ActorCritic(obs_dim, env.action_space).to(device)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, eps=1e-5)

    obs_rms = RunningMeanStd(shape=obs_dim)
    episode_returns = deque(maxlen=100)
    episode_lengths = deque(maxlen=100)

    global_step = 0
    episode_return = 0.0
    episode_length = 0

    print(f"🎒 Rambler starting on {env_id} with device={device}")

    while global_step < total_timesteps:
        # Storage for this rollout
        obs_buf = []
        actions_buf = []
        logprobs_buf = []
        rewards_buf = []
        dones_buf = []
        values_buf = []

        for _ in range(rollout_horizon):
            # Normalize obs
            obs_rms.update(np.expand_dims(obs, axis=0))
            norm_obs = obs_rms.normalize(obs)

            obs_tensor = torch.as_tensor(norm_obs, dtype=torch.float32, device=device).unsqueeze(0)
            with torch.no_grad():
                action_tensor, logprob_tensor, value_tensor = model.get_action_and_value(obs_tensor)

            if model.is_discrete:
                action = int(action_tensor.cpu().numpy()[0])
            else:
                action = action_tensor.cpu().numpy()[0]

            next_obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            # Scale reward (especially for Pendulum)
            scaled_reward = reward * cfg.reward_scale

            obs_buf.append(norm_obs.copy())
            actions_buf.append(action)
            logprobs_buf.append(logprob_tensor.cpu().numpy()[0])
            values_buf.append(value_tensor.cpu().numpy()[0])
            rewards_buf.append(scaled_reward)
            dones_buf.append(float(done))

            episode_return += reward  # track true reward for reporting
            episode_length += 1
            global_step += 1

            obs = next_obs

            if done:
                episode_returns.append(episode_return)
                episode_lengths.append(episode_length)
                obs, info = env.reset()
                episode_return = 0.0
                episode_length = 0

            if global_step >= total_timesteps:
                break

        # Bootstrap value for final state
        with torch.no_grad():
            obs_rms.update(np.expand_dims(obs, axis=0))
            norm_obs = obs_rms.normalize(obs)
            obs_tensor = torch.as_tensor(norm_obs, dtype=torch.float32, device=device).unsqueeze(0)
            last_value = model.get_value(obs_tensor).cpu().numpy()[0]

        obs_buf = np.asarray(obs_buf, dtype=np.float32)
        rewards_buf = np.asarray(rewards_buf, dtype=np.float32)
        dones_buf = np.asarray(dones_buf, dtype=np.float32)
        values_buf = np.asarray(values_buf, dtype=np.float32)

        advantages, returns = compute_gae(
            rewards=rewards_buf,
            values=values_buf,
            dones=dones_buf,
            last_value=last_value,
            gamma=cfg.gamma,
            gae_lambda=gae_lambda,
        )

        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # Convert to tensors
        obs_tensor = torch.as_tensor(obs_buf, dtype=torch.float32, device=device)
        returns_tensor = torch.as_tensor(returns, dtype=torch.float32, device=device)
        adv_tensor = torch.as_tensor(advantages, dtype=torch.float32, device=device)

        if model.is_discrete:
            actions_tensor = torch.as_tensor(actions_buf, dtype=torch.long, device=device)
        else:
            actions_tensor = torch.as_tensor(np.array(actions_buf), dtype=torch.float32, device=device)

        logprobs_tensor = torch.as_tensor(logprobs_buf, dtype=torch.float32, device=device)

        # PPO update
        ppo_update(
            model=model,
            optimizer=optimizer,
            obs=obs_tensor,
            actions=actions_tensor,
            logprobs=logprobs_tensor,
            advantages=adv_tensor,
            returns=returns_tensor,
            clip_coef=clip_coef,
            vf_coef=vf_coef,
            ent_coef=ent_coef,
            max_grad_norm=0.5,
            epochs=ppo_epochs,
            batch_size=batch_size,
        )

        # Logging
        if len(episode_returns) > 0:
            mean_return = np.mean(episode_returns)
            mean_length = np.mean(episode_lengths)
        else:
            mean_return = float("nan")
            mean_length = float("nan")

        print(
            f"Step {global_step:7d} | "
            f"MeanReturn (last 100) {mean_return:8.2f} | "
            f"MeanLen {mean_length:6.1f}"
        )

        # Early stopping if solved
        if cfg.solved_threshold is not None and len(episode_returns) == episode_returns.maxlen:
            if env_id in ["CartPole-v1", "Pendulum-v1"]:
                if mean_return >= cfg.solved_threshold:
                    print(f"✅ Rambler solved {env_id} with mean return {mean_return:.2f}")
                    break
            elif env_id == "Acrobot-v1":
                # For Acrobot, returns are negative; higher is better
                if mean_return >= cfg.solved_threshold:
                    print(f"✅ Rambler solved-ish {env_id} with mean return {mean_return:.2f}")
                    break

    env.close()
    print("🏁 Training complete.")
    return model


# -------------------------
# CLI
# -------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Rambler PPO Agent")
    parser.add_argument("--env", type=str, default="CartPole-v1", help="Gymnasium env id")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--total-steps", type=int, default=None, help="Override default max steps")
    parser.add_argument("--rollout-horizon", type=int, default=2048)
    parser.add_argument("--ppo-epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--clip", type=float, default=0.2)
    parser.add_argument("--gae-lambda", type=float, default=0.95)
    parser.add_argument("--vf-coef", type=float, default=0.5)
    parser.add_argument("--ent-coef", type=float, default=0.01)
    parser.add_argument("--cpu-only", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    device = get_device(prefer_gpu=not args.cpu_only)

    train_rambler(
        env_id=args.env,
        total_timesteps=args.total_steps,
        seed=args.seed,
        device=device,
        rollout_horizon=args.rollout_horizon,
        ppo_epochs=args.ppo_epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        clip_coef=args.clip,
        gae_lambda=args.gae_lambda,
        vf_coef=args.vf_coef,
        ent_coef=args.ent_coef,
    )
