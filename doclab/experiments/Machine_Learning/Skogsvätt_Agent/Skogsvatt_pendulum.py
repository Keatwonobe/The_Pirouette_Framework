import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import namedtuple
import os

# ------------------------------
# Reward shaping (Pendulum-tuned)
# ------------------------------

def shape_reward(env_name: str, raw_reward: float) -> float:
    if env_name == "Pendulum-v1":
        # Keep sign, just shrink magnitude
        return raw_reward / 10.0
    else:
        return raw_reward

# ------------------------------
# Dark Residue (same as before)
# ------------------------------

def dark_residue_simple(state: np.ndarray) -> float:
    return float(np.dot(state, state)) / len(state)

# ------------------------------
# Triadic Supervisor (Pendulum tuned)
# ------------------------------

class TriadicSupervisor:
    def __init__(self, dr_shadow=3.0):
        self.dr_shadow = dr_shadow
        self.last_dr = None

        # phase / rhythm
        self.phi = 0.0
        self.omega = 0.4 * np.pi
        self.update_window = (0.0, np.pi / 2)

        # precision coefficients
        self.a0  = -1.0
        self.aS  =  0.8
        self.aDR =  0.3
        self.aG  =  0.2

        # triadic weights (gentler)
        self.w_Q = 0.3   # coherence drop
        self.w_C = 0.1   # contrast
        self.w_B = 0.5   # shadow penalty

    def step_metrics(self, state, gamma_load=0.1):
        dr = dark_residue_simple(state)

        if self.last_dr is None:
            self.last_dr = dr

        delta_dr = dr - self.last_dr
        Q = max(0.0, -delta_dr)   # coherence gain
        C = abs(delta_dr)         # contrast
        B = 1.0 if dr > self.dr_shadow else 0.0
        S = C                     # surprise proxy

        # phase gate
        self.phi = (self.phi + self.omega + 0.05 * np.random.randn()) % (2 * np.pi)
        g = 1.0 if self.update_window[0] <= self.phi <= self.update_window[1] else 0.0

        # precision: open under surprise, close under high DR/load
        Pi = 1.0 / (1.0 + np.exp(
            -(self.a0 + self.aS * S - self.aDR * dr - self.aG * gamma_load)
        ))

        raw_w = Pi + self.w_Q * Q + self.w_C * C - self.w_B * B
        w = g * raw_w

        self.last_dr = dr

        return {
            "DR": dr,
            "ΔDR": delta_dr,
            "Q": Q,
            "C": C,
            "B": B,
            "S": S,
            "Pi": Pi,
            "g": g,
            "w": w,
        }

# ------------------------------
# Policy network (same structure as yours)
# ------------------------------

class PolicyNet(nn.Module):
    def __init__(self, obs_dim, hidden, n_actions):
        super().__init__()
        self.actor_base = nn.Sequential(
            nn.Linear(obs_dim, hidden),
            nn.Tanh(),
            nn.Linear(hidden, hidden),
            nn.Tanh(),
        )
        self.actor_mu = nn.Linear(hidden, n_actions)
        self.actor_log_std = nn.Parameter(torch.zeros(1, n_actions))

    def forward(self, x):
        base_out = self.actor_base(x)
        mu = self.actor_mu(base_out)
        std = torch.exp(self.actor_log_std)
        return mu, std

    def act(self, obs):
        # Flatten obs (handles (3,) and (3,1) shapes)
        obs_t = torch.as_tensor(obs, dtype=torch.float32).flatten()
        mu, std = self.forward(obs_t)

        dist = torch.distributions.Normal(mu, std)
        action_raw = dist.sample()
        logp = dist.log_prob(action_raw).sum(dim=-1).squeeze()
        entropy = dist.entropy().sum(dim=-1).squeeze()

        action_out = torch.tanh(action_raw).squeeze()
        return action_out, logp, entropy

# ------------------------------
# Pendulum-specific trainer
# ------------------------------

StepRecord = namedtuple("StepRecord", ["logp", "reward_learn", "w", "entropy"])

def train_pendulum_skogsvatt(
    episodes=3000,
    gamma=0.99,
    lr=3e-4,
    entropy_coeff=0.01,
    render_every=None,
):
    env = gym.make("Pendulum-v1")
    obs_dim = env.observation_space.shape[0]
    n_actions = env.action_space.shape[0]
    action_scale = env.action_space.high[0]

    policy = PolicyNet(obs_dim, hidden=64, n_actions=n_actions)
    optimizer = optim.Adam(policy.parameters(), lr=lr)
    supervisor = TriadicSupervisor()

    last_ep_loss = 0.0

    for ep in range(1, episodes + 1):
        obs, _ = env.reset()
        supervisor.last_dr = None

        step_records = []
        done = False
        trunc = False
        ep_reward_raw = 0.0

        while not (done or trunc):
            if render_every and ep % render_every == 0:
                env.render()

            action_tanh, logp, entropy = policy.act(obs)

            action_env = np.array([action_tanh.item() * action_scale])
            obs_next, reward_raw, done, trunc, info = env.step(action_env)

            reward_learn = shape_reward("Pendulum-v1", reward_raw)
            metrics = supervisor.step_metrics(obs, gamma_load=abs(last_ep_loss))
            w = metrics["w"]

            step_records.append(StepRecord(
                logp=logp,
                reward_learn=reward_learn,
                w=w,
                entropy=entropy,
            ))
            ep_reward_raw += float(reward_raw)
            obs = obs_next

        # ----- Triad-weighted REINFORCE update -----

        returns = []
        G = 0.0
        for r in reversed([r.reward_learn for r in step_records]):
            G = r + gamma * G
            returns.append(G)
        returns.reverse()

        returns = torch.as_tensor(returns, dtype=torch.float32)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

        logps = torch.stack([rec.logp for rec in step_records])
        weights = torch.as_tensor([rec.w for rec in step_records], dtype=torch.float32)
        weights = torch.tanh(weights)  # keep modulation bounded

        advantages = returns * (1.0 + weights)

        # use all entropies, not just the last one
        entropies = torch.stack([rec.entropy for rec in step_records])
        policy_loss = -(logps * advantages).mean()
        entropy_loss = -entropy_coeff * entropies.mean()

        loss = policy_loss + entropy_loss

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), max_norm=0.5)
        optimizer.step()

        last_ep_loss = float(loss.item())

        print(
            f"[Pendulum] Ep {ep:04d} | "
            f"R_raw={ep_reward_raw:7.2f} | "
            f"len={len(step_records):3d} | "
            f"loss={loss.item():.3f}"
        )

    env.close()
    return policy

if __name__ == "__main__":
    policy = train_pendulum_skogsvatt(
        episodes=3000,
        lr=3e-4,
        entropy_coeff=0.01,
        render_every=None,  # or 100 to peek
    )
