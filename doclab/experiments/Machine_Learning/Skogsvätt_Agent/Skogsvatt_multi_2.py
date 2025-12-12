import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import namedtuple
import os
import copy

# ------------------------------------------------------------
# Environment factory with discrete actions for Pendulum
# ------------------------------------------------------------

class DiscretePendulumWrapper:
    """
    Wraps Pendulum-v1 to use a small discrete action space,
    e.g. 5 actions in [-2, 2].
    """
    def __init__(self, n_actions=5, render_mode=None):
        self.env = gym.make("Pendulum-v1", render_mode=render_mode)
        self.n_actions = n_actions
        self.actions = np.linspace(-2.0, 2.0, n_actions)

        self.observation_space = self.env.observation_space
        self.action_space_n = n_actions

    def reset(self):
        obs, info = self.env.reset()
        return obs, info

    def step(self, action_idx):
        torque = self.actions[action_idx]
        obs, reward, terminated, truncated, info = self.env.step([torque])
        return obs, reward, terminated, truncated, info

    def close(self):
        self.env.close()


class DiscreteBipedalWrapper:
    """
    Wraps BipedalWalker-v3 to use a small discrete action space.
    Actions are:
      0: No-op
      1: Extend Left Leg
      2: Extend Right Leg
      3: Retract Left Leg
      4: Retract Right Leg
    """
    def __init__(self, render_mode=None):
        self.env = gym.make("BipedalWalker-v3", render_mode=render_mode)
        self.n_actions = 5
        self.actions = [
            [0, 0, 0, 0],         # 0: No-op
            [+1, -0.2, 0, 0],     # 1: Extend Left (Hip, Knee)
            [0, 0, +1, -0.2],     # 2: Extend Right (Hip, Knee)
            [-1, 0, 0, 0],        # 3: Retract Left Hip
            [0, 0, -1, 0],        # 4: Retract Right Hip
        ]

        self.observation_space = self.env.observation_space
        self.action_space_n = self.n_actions

    def reset(self):
        obs, info = self.env.reset()
        return obs, info

    def step(self, action_idx):
        torques = self.actions[action_idx]
        obs, reward, terminated, truncated, info = self.env.step(torques)
        return obs, reward, terminated, truncated, info

    def close(self):
        self.env.close()

def make_env(env_name: str, render_mode=None):
    """
    Returns (env, obs_dim, n_actions, action_scale)
    """
    env = gym.make(env_name, render_mode=render_mode)
    obs_dim = env.observation_space.shape[0]
    
    # Continuous action space
    n_actions = env.action_space.shape[0]
    
    # Get the max action value (e.g., 2.0 for Pendulum, 1.0 for Bipedal)
    action_scale = env.action_space.high[0]

    return env, obs_dim, n_actions, action_scale

# ------------------------------------------------------------
# Reward shaping hook
# ------------------------------------------------------------

def shape_reward(env_name: str, raw_reward: float) -> float:
    """
    Returns the reward actually used for learning.
    We still log the *raw* reward for scores.
    """
    if env_name == "Pendulum-v1":
        # Raw rewards are roughly [-1800, 0].
        # Center them around -1000 and scale.
        # e.g., -1800 -> -1.0
        # e.g., -1000 ->  0.0
        # e.g., -200  -> +1.0
        return (raw_reward + 1000.0) / 800.0
    elif env_name == "BipedalWalker-v3":
        # Raw rewards are ~[-200, 300].
        # Scale down to prevent huge returns.
        return raw_reward / 100.0
    else:
        # CartPole and others: use raw directly
        return raw_reward

# ------------------------------------------------------------
# Simple, environment-agnostic Dark Residue
# ------------------------------------------------------------

def dark_residue_simple(state: np.ndarray) -> float:
    """
    Smooth, general DR: *MEAN* squared norm of the state vector.
    This normalizes for different state dimensions.
    """
    return float(np.dot(state, state)) / len(state)


# ------------------------------------------------------------
# Triadic Supervisor (original Skogsvätt style, non-Wendigo DR)
# ------------------------------------------------------------

class TriadicSupervisor:
    """
    Minimal triadic operator:
      - DR: dark_residue_simple
      - Q: coherence drop (DR_{t-1} - DR_t)+
      - C: contrast |ΔDR|
      - B: shadow flag (DR above threshold)
    Outputs scalar weight w_t to modulate policy gradients.
    """

    def __init__(self, dr_shadow=8.0):
        self.dr_shadow = dr_shadow
        self.last_dr = None

        # phase / rhythm
        self.phi = 0.0
        self.omega = 0.4 * np.pi
        self.update_window = (0.0, np.pi / 2)

        # precision coefficients
        self.a0  = -0.5
        self.aS  =  1.0
        self.aDR =  0.5
        self.aG  =  0.2

        # weights to combine triadic terms
        self.w_Q = 0.7   # coherence drop
        self.w_C = 0.3   # contrast
        self.w_B = 0.8   # shadow penalty

    def step_metrics(self, state, gamma_load=0.1):
        dr = dark_residue_simple(state)

        if self.last_dr is None:
            self.last_dr = dr

        delta_dr = dr - self.last_dr
        Q = max(0.0, -delta_dr)   # coherence gain
        C = abs(delta_dr)         # contrast
        B = 1.0 if dr > self.dr_shadow else 0.0
        S = C                     # surprise

        # phase gate
        self.phi = (self.phi + self.omega + 0.05 * np.random.randn()) % (2 * np.pi)
        g = 1.0 if self.update_window[0] <= self.phi <= self.update_window[1] else 0.0

        # precision: open when surprised, close under high DR/load
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

# ------------------------------------------------------------
# Policy Network
# ------------------------------------------------------------

class PolicyNet(nn.Module):
    def __init__(self, obs_dim, hidden, n_actions):
        super().__init__()
        # Actor network
        self.actor_base = nn.Sequential(
            nn.Linear(obs_dim, hidden),
            nn.Tanh(),
            nn.Linear(hidden, hidden),
            nn.Tanh(),
        )
        self.actor_mu = nn.Linear(hidden, n_actions)
        # We learn log_std, it's more stable
        self.actor_log_std = nn.Parameter(torch.zeros(1, n_actions))

    def forward(self, x):
        # Pass obs through base
        base_out = self.actor_base(x)
        # Get action mean
        mu = self.actor_mu(base_out)
        # Get action std
        std = torch.exp(self.actor_log_std)
        return mu, std

    def act(self, obs):
        # FIX 1: Flatten the obs tensor. Handles (3,) and (3, 1)
        obs_t = torch.as_tensor(obs, dtype=torch.float32).flatten() 
        mu, std = self.forward(obs_t)
        
        # ... (distribution sampling) ...
        dist = torch.distributions.Normal(mu, std)
        action_raw = dist.sample()
        
        # .sum(dim=-1) sums over the action dim (which is 1)
        logp = dist.log_prob(action_raw).sum(dim=-1).squeeze()
        entropy = dist.entropy().sum(dim=-1).squeeze()

        # FIX 2: Squeeze the action to a scalar tensor
        action_out = torch.tanh(action_raw).squeeze() 

        return action_out, logp, entropy

# ------------------------------------------------------------
# Training loop (REINFORCE + triadic weighting + quota snapshots)
# ------------------------------------------------------------

StepRecord = namedtuple("StepRecord", ["logp", "reward_learn", "w", "entropy"])

def train_skogsvatt(
    env_name="CartPole-v1",
    episodes=500,
    gamma=0.99,
    lr=1e-2,
    entropy_coeff=0.01,
    render_every=None,
    quota_size=0,
    quota_threshold=490.0,
    quota_patience=3,
    quota_dir=None,
):
    """
    quota_size > 0:
      harvest up to quota_size snapshots when CartPole achieves
      >= quota_threshold reward for quota_patience consecutive episodes.
    """

    env, obs_dim, n_actions, action_scale = make_env(env_name, render_mode=None)

    policy = PolicyNet(obs_dim, hidden=64, n_actions=n_actions)
    optimizer = optim.Adam(policy.parameters(), lr=lr)
    supervisor = TriadicSupervisor()

    last_ep_loss = 0.0

    if quota_dir is not None and quota_size > 0:
        os.makedirs(quota_dir, exist_ok=True)

    # quota tracking
    quota_snapshots = []
    success_streak = 0

    for ep in range(1, episodes+1):
        obs, _ = env.reset()
        supervisor.last_dr = None

        step_records = []
        done = False
        trunc = False
        ep_reward_raw = 0.0   # what the env gives us, for logging
        ep_reward_learn = 0.0 # what we actually use for training

        while not (done or trunc):
            if render_every and ep % render_every == 0 and hasattr(env, "env"):
                env.env.render()

            # 1. Get action, logp, AND entropy from new policy
            action_tanh, logp, entropy = policy.act(obs)
            
            # 2. Scale action from [-1, 1] to [low, high]
            action_env = np.array([action_tanh.item() * action_scale])
            obs_next, reward_raw, done, trunc, info = env.step(action_env)

            reward_learn = shape_reward(env_name, reward_raw)
            metrics = supervisor.step_metrics(obs, gamma_load=last_ep_loss)
            w = metrics["w"]

            step_records.append(StepRecord(
                logp=logp,
                reward_learn=reward_learn,
                w=w,
                entropy=entropy # <-- Store entropy
            ))
            ep_reward_raw += float(reward_raw)
            obs = obs_next

        # ----- REINFORCE update, triad-weighted -----

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
        weights = torch.tanh(weights)

        advantages = returns * (1.0 + weights)
        # 3. Add the entropy bonus to the loss!
        # We *maximize* entropy, so we *subtract* it from the loss.
        policy_loss = -(logps * advantages).mean()
        entropy_loss = -entropy_coeff * entropy.mean()
        
        loss = policy_loss + entropy_loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        last_ep_loss = loss.item()

        print(
            f"[{env_name}] Ep {ep:04d} | "
            f"R_raw={ep_reward_raw:7.2f} | "
            f"len={len(step_records):3d} | "
            f"loss={loss.item():.3f}"
        )

        # ----- Quota harvesting (CartPole only for now) -----

        if quota_size > 0 and env_name == "CartPole-v1":
            if ep_reward_raw >= quota_threshold:
                success_streak += 1
            else:
                success_streak = 0

            if success_streak >= quota_patience and len(quota_snapshots) < quota_size:
                snap_idx = len(quota_snapshots)
                state_copy = copy.deepcopy(policy.state_dict())
                quota_snapshots.append({
                    "episode": ep,
                    "reward_raw": ep_reward_raw,
                    "state_dict": state_copy,
                })

                if quota_dir is not None:
                    filename = (
                        f"{env_name}_quota_{snap_idx}"
                        f"_ep{ep:04d}_R{int(ep_reward_raw)}.pth"
                    )
                    path = os.path.join(quota_dir, filename)
                    torch.save(state_copy, path)
                    print(f">>> Quota snapshot {snap_idx} saved to {path}")

                # reset streak so it has to prove itself again for next snapshot
                success_streak = 0

                # if we've harvested enough, we can stop early
                if len(quota_snapshots) >= quota_size:
                    print(">>> Quota filled, stopping training.")
                    break

    if hasattr(env, "close"):
        env.close()

    return policy, quota_snapshots

if __name__ == "__main__":
    
    # Run Pendulum with the new continuous engine!
    policy, _ = train_skogsvatt(
        env_name="Pendulum-v1",
        episodes=3000,
        lr=3e-4,            # <-- Lower LR is stabler for continuous
        entropy_coeff=0.01  # <-- Our exploration bonus
    )
