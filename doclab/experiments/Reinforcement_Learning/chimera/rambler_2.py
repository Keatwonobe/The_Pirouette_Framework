#!/usr/bin/env python3
"""
Rambler v2
================

A multi-head PPO agent that combines:

- ENGRAM-PPO: standard PPO actor-critic (Rambler-style)
- ENGRAM-Δ+DR: Dark Residue shaping (Vagabond-style)
- ENGRAM-MANIFOLD: autopoietic latent manifold + resonance + ratchet (Wanderer-style)

Targets:
- CartPole-v1      (Discrete)
- Acrobot-v1       (Discrete, negative rewards)
- Pendulum-v1      (Continuous)

Usage:
  python rambler_hydra.py --env CartPole-v1
  python rambler_hydra.py --env Pendulum-v1
  python rambler_hydra.py --env Acrobot-v1
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

# ---------------------------------------------------
# Utils
# ---------------------------------------------------

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


# ---------------------------------------------------
# Env configs (borrowed from Rambler)
# ---------------------------------------------------

class EnvConfig:
    def __init__(self, gamma=0.99, reward_scale=1.0,
                 solved_threshold=None, max_steps=1_000_000):
        self.gamma = gamma
        self.reward_scale = reward_scale
        self.solved_threshold = solved_threshold
        self.max_steps = max_steps

ENV_CONFIGS = {
    "CartPole-v1": EnvConfig(
        gamma=0.99,
        reward_scale=1.0,
        solved_threshold=475.0,
        max_steps=300_000,
    ),
    "Acrobot-v1": EnvConfig(
        gamma=0.99,
        reward_scale=1.0,
        solved_threshold=-100.0,
        max_steps=600_000,
    ),
    "Pendulum-v1": EnvConfig(
        gamma=0.99,
        reward_scale=0.1,    # shrink magnitude for stability
        solved_threshold=-200.0,
        max_steps=600_000,
    ),
}

def get_env_config(env_id: str) -> EnvConfig:
    return ENV_CONFIGS.get(env_id, EnvConfig())


# ---------------------------------------------------
# Running mean/std (from Rambler)
# ---------------------------------------------------

class RunningMeanStd:
    def __init__(self, shape, eps=1e-4, momentum=0.01):
        self.mean = np.zeros(shape, dtype=np.float64)
        self.var = np.ones(shape, dtype=np.float64)
        self.count = eps
        self.momentum = momentum

    def update(self, x: np.ndarray):
        x = np.asarray(x, dtype=np.float64)
        batch_mean = x.mean(axis=0)
        batch_var = x.var(axis=0)

        self.mean = (1 - self.momentum) * self.mean + self.momentum * batch_mean
        self.var = (1 - self.momentum) * self.var + self.momentum * batch_var

    def normalize(self, x: np.ndarray):
        return (x - self.mean) / (np.sqrt(self.var) + 1e-8)


# ---------------------------------------------------
# Dark Residue light version (ENGRAM-Δ+DR)
# ---------------------------------------------------

def cartpole_dark_residue(state: np.ndarray) -> float:
    x, x_dot, theta, theta_dot = state
    # similar spirit to Wendigo + Vagabond
    return (
        0.4 * abs(x) +
        0.2 * abs(x_dot) +
        1.5 * abs(theta) +
        0.3 * abs(theta_dot)
    )

def pendulum_dark_residue(state: np.ndarray) -> float:
    # Using angle + angular velocity
    cos_th, sin_th, thdot = state
    # upright ~ (cos=1, sin=0)
    angle_dev = math.acos(max(-1.0, min(1.0, cos_th)))
    return 2.0 * abs(angle_dev) + 0.5 * abs(thdot)

def acrobot_dark_residue(state: np.ndarray) -> float:
    # Based loosely on Vagabond's link coherence
    cos_th1, sin_th1, cos_th2, sin_th2, th1dot, th2dot = state
    vel = math.sqrt(th1dot ** 2 + th2dot ** 2)
    # prefer both links aligned and not flailing
    angle1 = math.atan2(sin_th1, cos_th1)
    angle2 = math.atan2(sin_th2, cos_th2)
    coupling = abs(angle1 - angle2)
    return 1.5 * coupling + 0.4 * vel

def compute_dark_residue(env_id: str, state: np.ndarray) -> float:
    if "CartPole" in env_id:
        return cartpole_dark_residue(state)
    if "Pendulum" in env_id:
        return pendulum_dark_residue(state)
    if "Acrobot" in env_id:
        return acrobot_dark_residue(state)
    return float(np.linalg.norm(state))


# ---------------------------------------------------
# Hydra network: policy + value + DR-value + manifold
# ---------------------------------------------------

class HydraActorCritic(nn.Module):
    def __init__(self, obs_dim: int, action_space):
        super().__init__()
        self.obs_dim = obs_dim
        self.is_discrete = isinstance(action_space, gym.spaces.Discrete)

        hidden = 128

        self.backbone = nn.Sequential(
            nn.Linear(obs_dim, hidden),
            nn.Tanh(),
            nn.Linear(hidden, hidden),
            nn.Tanh(),
        )

        # Policy head
        if self.is_discrete:
            self.policy_head = nn.Linear(hidden, action_space.n)
            self.log_std = None
        else:
            act_dim = action_space.shape[0]
            self.policy_mean = nn.Linear(hidden, act_dim)
            self.log_std = nn.Parameter(torch.zeros(act_dim))

        # Value heads
        self.value_head = nn.Linear(hidden, 1)        # task reward
        self.dr_value_head = nn.Linear(hidden, 1)     # DR-related auxiliary value

        # Manifold head (ENGRAM-MANIFOLD)
        manifold_dim = 64
        self.manifold_map = nn.Linear(hidden, manifold_dim)
        self.manifold_predictor = nn.Linear(manifold_dim, manifold_dim)

    def forward_backbone(self, obs: torch.Tensor):
        return self.backbone(obs)

    def get_action_and_value(self, obs: torch.Tensor):
        """
        Returns:
          action_tensor, logprob, value, dr_value, manifold_state, predicted_next_manifold
        (Predicted_next_manifold is used only when we stitch trajectories.)
        """
        h = self.forward_backbone(obs)

        # Policy
        if self.is_discrete:
            logits = self.policy_head(h)
            dist = Categorical(logits=logits)
            action = dist.sample()
            logprob = dist.log_prob(action)
        else:
            mean = self.policy_mean(h)
            std = self.log_std.exp().expand_as(mean)
            dist = Normal(mean, std)
            action = dist.sample()
            logprob = dist.log_prob(action).sum(-1)

        value = self.value_head(h).squeeze(-1)
        dr_value = self.dr_value_head(h).squeeze(-1)

        # Manifold
        manifold_state = torch.relu(self.manifold_map(h))
        predicted_next = self.manifold_predictor(manifold_state)

        return action, logprob, value, dr_value, manifold_state, predicted_next

    def evaluate_actions(self, obs: torch.Tensor, actions: torch.Tensor):
        """
        For PPO update: returns logprob, values, entropy, dr_values, manifold_state, predicted_next
        """
        h = self.forward_backbone(obs)

        if self.is_discrete:
            logits = self.policy_head(h)
            dist = Categorical(logits=logits)
            logprob = dist.log_prob(actions)
            entropy = dist.entropy()
        else:
            mean = self.policy_mean(h)
            std = self.log_std.exp().expand_as(mean)
            dist = Normal(mean, std)
            logprob = dist.log_prob(actions).sum(-1)
            entropy = dist.entropy().sum(-1)

        value = self.value_head(h).squeeze(-1)
        dr_value = self.dr_value_head(h).squeeze(-1)
        manifold_state = torch.relu(self.manifold_map(h))
        predicted_next = self.manifold_predictor(manifold_state)

        return logprob, value, dr_value, entropy, manifold_state, predicted_next


# ---------------------------------------------------
# GAE & PPO
# ---------------------------------------------------

def compute_gae(
    rewards, values, dones,
    gamma: float, gae_lambda: float
):
    """
    rewards, values, dones: np arrays of length T+1 for values, T for rewards/dones.
    """
    T = len(rewards)
    advantages = np.zeros(T, dtype=np.float32)
    gae = 0.0
    for t in reversed(range(T)):
        delta = rewards[t] + gamma * values[t + 1] * (1.0 - dones[t]) - values[t]
        gae = delta + gamma * gae_lambda * (1.0 - dones[t]) * gae
        advantages[t] = gae
    returns = advantages + values[:-1]
    return advantages, returns

def ppo_update(
    model: HydraActorCritic,
    optimizer: optim.Optimizer,
    obs: torch.Tensor,
    actions: torch.Tensor,
    logprobs_old: torch.Tensor,
    advantages: torch.Tensor,
    returns: torch.Tensor,
    dr_targets: torch.Tensor,
    manifold_states: torch.Tensor,
    predicted_next_states: torch.Tensor,
    clip_coef: float,
    vf_coef: float,
    dr_vf_coef: float,
    manifold_coef: float,
    ent_coef: float,
    max_grad_norm: float,
    epochs: int,
    batch_size: int,
):
    N = obs.shape[0]
    idxs = np.arange(N)

    for _ in range(epochs):
        np.random.shuffle(idxs)
        for start in range(0, N, batch_size):
            end = start + batch_size
            b_idx = idxs[start:end]

            b_obs = obs[b_idx]
            b_actions = actions[b_idx]
            b_logprobs_old = logprobs_old[b_idx]
            b_adv = advantages[b_idx]
            b_returns = returns[b_idx]
            b_dr_targets = dr_targets[b_idx]

            # Forward
            new_logprobs, values, dr_values, entropy, m_states, m_pred = \
                model.evaluate_actions(b_obs, b_actions)

            # PPO surrogate
            ratio = torch.exp(new_logprobs - b_logprobs_old)
            unclipped = ratio * b_adv
            clipped = torch.clamp(ratio, 1.0 - clip_coef, 1.0 + clip_coef) * b_adv
            policy_loss = -torch.min(unclipped, clipped).mean()

            # Value losses
            value_loss = ((values - b_returns) ** 2).mean()
            dr_value_loss = ((dr_values - b_dr_targets) ** 2).mean()

            # Manifold autopoiesis loss: we use offsets just like Wanderer does
            if len(m_states) > 1:
                # align batch manifold states by indices
                m_states_b = m_states
                m_pred_b = m_pred

                # approximate next-manifold using shuffle of indices +1 where possible
                # (we're not strictly time-aligned in minibatches, but this still
                # pushes predictive consistency).
                shift_idxs = torch.roll(torch.arange(len(m_states_b)), shifts=-1)
                actual_next = m_states_b[shift_idxs].detach()
                auto_loss = ((m_pred_b - actual_next) ** 2).mean()
            else:
                auto_loss = torch.tensor(0.0, device=obs.device)

            entropy_loss = -entropy.mean()

            loss = (
                policy_loss
                + vf_coef * value_loss
                + dr_vf_coef * dr_value_loss
                + manifold_coef * auto_loss
                + ent_coef * entropy_loss
            )

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()


# ---------------------------------------------------
# Training loop with Ratchet & DR shaping
# ---------------------------------------------------

def train_rambler_hydra(
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
    dr_vf_coef: float = 0.2,
    manifold_coef: float = 0.1,
    base_ent_coef: float = 0.01,
    ratchet_tolerance: float = 0.15,
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

    model = HydraActorCritic(obs_dim, env.action_space).to(device)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, eps=1e-5)

    obs_rms = RunningMeanStd(shape=obs_dim)
    episode_returns = deque(maxlen=100)
    episode_lengths = deque(maxlen=100)

    # Ratchet state (Wanderer-style)
    best_rolling_avg = -float("inf")
    current_rolling_avg = -float("inf")

    global_step = 0
    episode_return = 0.0
    episode_length = 0

    print(f"🌀 Rambler-Hydra starting on {env_id} with device={device}")

    while global_step < total_timesteps:
        obs_buf = []
        actions_buf = []
        logprobs_buf = []
        rewards_buf = []
        dr_buf = []
        dones_buf = []
        values_buf = []
        dr_values_buf = []
        manifold_states_buf = []
        predicted_buf = []

        for _ in range(rollout_horizon):
            obs_rms.update(np.expand_dims(obs, axis=0))
            norm_obs = obs_rms.normalize(obs)

            obs_tensor = torch.as_tensor(
                norm_obs, dtype=torch.float32, device=device
            ).unsqueeze(0)

            with torch.no_grad():
                action_t, logprob_t, value_t, dr_value_t, m_state_t, m_pred_t = \
                    model.get_action_and_value(obs_tensor)

            # Convert to env action
            if model.is_discrete:
                action = int(action_t.cpu().numpy()[0])
            else:
                action = action_t.cpu().numpy()[0]

            next_obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            # Env-specific handling
            scaled_reward = cfg.reward_scale * reward

            # Compute DR for this state
            dr_value = compute_dark_residue(env.spec.id, next_obs)

            obs_buf.append(norm_obs)
            actions_buf.append(action)
            logprobs_buf.append(logprob_t.cpu().numpy()[0])
            rewards_buf.append(scaled_reward)
            dr_buf.append(dr_value)
            dones_buf.append(float(done))
            values_buf.append(value_t.cpu().numpy()[0])
            dr_values_buf.append(dr_value_t.cpu().numpy()[0])
            manifold_states_buf.append(m_state_t.cpu().numpy()[0])
            predicted_buf.append(m_pred_t.cpu().numpy()[0])

            episode_return += reward
            episode_length += 1
            global_step += 1

            obs = next_obs

            if done:
                episode_returns.append(episode_return)
                episode_lengths.append(episode_length)
                episode_return = 0.0
                episode_length = 0
                obs, info = env.reset()

                # update rolling stats for ratchet
                if len(episode_returns) > 0:
                    current_rolling_avg = float(np.mean(episode_returns))
                    best_rolling_avg = max(best_rolling_avg, current_rolling_avg)

            if global_step >= total_timesteps:
                break

        # Prepare tensors
        T = len(rewards_buf)
        if T == 0:
            break

        rewards_np = np.array(rewards_buf, dtype=np.float32)
        dones_np = np.array(dones_buf, dtype=np.float32)
        values_np = np.array(values_buf + [0.0], dtype=np.float32)  # bootstrap value at T+1 = 0

        # GAE over *composite* reward: task - alpha*DR
        dr_np = np.array(dr_buf, dtype=np.float32)
        # Reward shaping: encourage DR decrease like Wendigo
        # baseline DR penalty plus derivative reward
        dr_penalty = dr_np
        dr_deriv = np.diff(np.concatenate([[dr_np[0]], dr_np]))
        dr_improvement = -np.clip(dr_deriv, a_max=0.0, a_min=None)  # positive when DR goes down

        composite_reward = rewards_np - 0.1 * dr_penalty + 0.5 * dr_improvement

        advantages_np, returns_np = compute_gae(
            composite_reward, values_np, dones_np,
            gamma=cfg.gamma, gae_lambda=gae_lambda
        )

        # DR targets: want dr_value_head to approximate (-DR)
        dr_targets_np = -dr_np

        # Normalize advantages
        advantages_np = (advantages_np - advantages_np.mean()) / (advantages_np.std() + 1e-8)

        obs_tensor = torch.as_tensor(obs_buf, dtype=torch.float32, device=device)
        returns_tensor = torch.as_tensor(returns_np, dtype=torch.float32, device=device)
        adv_tensor = torch.as_tensor(advantages_np, dtype=torch.float32, device=device)
        dr_targets_tensor = torch.as_tensor(dr_targets_np, dtype=torch.float32, device=device)

        if model.is_discrete:
            actions_tensor = torch.as_tensor(actions_buf, dtype=torch.long, device=device)
        else:
            actions_tensor = torch.as_tensor(
                np.array(actions_buf), dtype=torch.float32, device=device
            )

        logprobs_tensor = torch.as_tensor(logprobs_buf, dtype=torch.float32, device=device)
        m_states_tensor = torch.as_tensor(manifold_states_buf, dtype=torch.float32, device=device)
        m_preds_tensor = torch.as_tensor(predicted_buf, dtype=torch.float32, device=device)

        # Ratchet: if we are backsliding vs best, boost entropy
        if best_rolling_avg != -float("inf") and current_rolling_avg != -float("inf"):
            if current_rolling_avg < best_rolling_avg - abs(best_rolling_avg) * ratchet_tolerance:
                # shattered manifold: push entropy up a lot
                ent_coef = base_ent_coef * 5.0
            else:
                ent_coef = base_ent_coef
        else:
            ent_coef = base_ent_coef

        # PPO update
        ppo_update(
            model=model,
            optimizer=optimizer,
            obs=obs_tensor,
            actions=actions_tensor,
            logprobs_old=logprobs_tensor,
            advantages=adv_tensor,
            returns=returns_tensor,
            dr_targets=dr_targets_tensor,
            manifold_states=m_states_tensor,
            predicted_next_states=m_preds_tensor,
            clip_coef=clip_coef,
            vf_coef=vf_coef,
            dr_vf_coef=dr_vf_coef,
            manifold_coef=manifold_coef,
            ent_coef=ent_coef,
            max_grad_norm=0.5,
            epochs=ppo_epochs,
            batch_size=batch_size,
        )

        # Logging
        if len(episode_returns) > 0:
            mean_return = float(np.mean(episode_returns))
            mean_length = float(np.mean(episode_lengths))
        else:
            mean_return = float("nan")
            mean_length = float("nan")

        print(
            f"Step {global_step:7d} | "
            f"Return(avg100) = {mean_return:7.2f} | "
            f"Len(avg100) = {mean_length:6.1f} | "
            f"Best = {best_rolling_avg:7.2f} | "
            f"EntCoef = {ent_coef:.4f}"
        )

        # Early stop if solved-ish
        if cfg.solved_threshold is not None and len(episode_returns) == episode_returns.maxlen:
            if env_id in ["CartPole-v1", "Pendulum-v1"]:
                if mean_return >= cfg.solved_threshold:
                    print(f"✅ Hydra solved {env_id} with mean return {mean_return:.2f}")
                    break
            elif env_id == "Acrobot-v1":
                if mean_return >= cfg.solved_threshold:
                    print(f"✅ Hydra solved-ish {env_id} with mean return {mean_return:.2f}")
                    break

    env.close()
    print("🏁 Rambler-Hydra training complete.")
    return model


# ---------------------------------------------------
# CLI
# ---------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Rambler-Hydra Multi-Head PPO Agent")
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
    parser.add_argument("--dr-vf-coef", type=float, default=0.2)
    parser.add_argument("--manifold-coef", type=float, default=0.1)
    parser.add_argument("--ent-coef", type=float, default=0.01)
    parser.add_argument("--ratchet-tolerance", type=float, default=0.15)
    parser.add_argument("--cpu-only", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    device = get_device(prefer_gpu=not args.cpu_only)

    train_rambler_hydra(
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
        dr_vf_coef=args.dr_vf_coef,
        manifold_coef=args.manifold_coef,
        base_ent_coef=args.ent_coef,
        ratchet_tolerance=args.ratchet_tolerance,
    )
