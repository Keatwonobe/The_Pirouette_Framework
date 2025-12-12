import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import namedtuple

# ------------------------------------------------------------
# Environment factory with discrete actions for Pendulum too
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
        # We pretend we have a discrete action space for the policy
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


def make_env(env_name: str, render_mode=None):
    """
    Returns (env, obs_dim, n_actions, is_pendulum_flag)
    """
    if env_name == "CartPole-v1":
        env = gym.make("CartPole-v1", render_mode=render_mode)
        obs_dim = env.observation_space.shape[0]
        n_actions = env.action_space.n
        is_pendulum = False
    elif env_name == "Pendulum-v1":
        wrapper = DiscretePendulumWrapper(n_actions=5, render_mode=render_mode)
        env = wrapper
        obs_dim = env.observation_space.shape[0]
        n_actions = env.action_space_n
        is_pendulum = True
    else:
        raise ValueError(f"Unsupported env_name: {env_name}")

    return env, obs_dim, n_actions, is_pendulum

# ------------------------------------------------------------
# Simple, environment-agnostic Dark Residue
# ------------------------------------------------------------

def dark_residue_simple(state: np.ndarray) -> float:
    """
    Smooth, general DR: just the squared norm of the state vector.
    Works for both CartPole and Pendulum.
    """
    return float(np.dot(state, state))


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
    Outputs a scalar weight w_t to modulate policy gradients.
    """

    def __init__(self, dr_shadow=8.0):
        self.dr_shadow = dr_shadow
        self.last_dr = None

        # phase / rhythm
        self.phi = 0.0
        self.omega = 0.4 * np.pi           # "theta"-like update frequency
        self.update_window = (0.0, np.pi/2)

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
        Q = max(0.0, -delta_dr)        # coherence gain: DR drop
        C = abs(delta_dr)              # contrast
        B = 1.0 if dr > self.dr_shadow else 0.0
        S = C                          # surprise ~ |ΔDR|

        # phase gate
        self.phi = (self.phi + self.omega + 0.05*np.random.randn()) % (2*np.pi)
        g = 1.0 if self.update_window[0] <= self.phi <= self.update_window[1] else 0.0

        # precision: open when surprised, close under high DR/load
        Pi = 1.0 / (1.0 + np.exp(
            -(self.a0 + self.aS*S - self.aDR*dr - self.aG*gamma_load)
        ))

        # raw operator weight
        raw_w = Pi + self.w_Q * Q + self.w_C * C - self.w_B * B
        w = g * raw_w

        self.last_dr = dr

        # you can log any/all of these into a manifold later
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
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden),
            nn.Tanh(),
            nn.Linear(hidden, n_actions)
        )

    def forward(self, x):
        return self.net(x)

    def act(self, obs):
        obs_t = torch.as_tensor(obs, dtype=torch.float32)
        logits = self.forward(obs_t)
        probs = torch.softmax(logits, dim=-1)
        dist = torch.distributions.Categorical(probs=probs)
        action = dist.sample()
        logp = dist.log_prob(action)
        return int(action.item()), logp

# ------------------------------------------------------------
# Training loop (REINFORCE + triadic weighting)
# ------------------------------------------------------------

StepRecord = namedtuple("StepRecord", ["logp", "reward", "w"])

def train_skogsvatt(
    env_name="Pendulum-v1",
    episodes=200,
    gamma=0.99,
    lr=1e-2,
    render_every=None,
):
    env, obs_dim, n_actions, is_pendulum = make_env(env_name, render_mode=None)

    policy = PolicyNet(obs_dim, hidden=32, n_actions=n_actions)
    optimizer = optim.Adam(policy.parameters(), lr=lr)
    supervisor = TriadicSupervisor()

    for ep in range(1, episodes+1):
        obs, _ = env.reset()
        supervisor.last_dr = None

        step_records = []
        done = False
        trunc = False
        ep_reward = 0.0

        while not (done or trunc):
            if render_every and ep % render_every == 0:
                # Only actual gym.Env's have render();
                # our Pendulum wrapper uses underlying env.render()
                if hasattr(env, "render"):
                    env.env.render()

            # policy action
            action_idx, logp = policy.act(obs)

            # env step (CartPole expects int, Pendulum wrapper maps index->torque)
            obs_next, reward, done, trunc, info = env.step(action_idx)

            # operator metrics
            metrics = supervisor.step_metrics(obs)
            w = metrics["w"]

            step_records.append(StepRecord(logp=logp, reward=reward, w=w))
            ep_reward += float(reward)
            obs = obs_next

        # ----- REINFORCE update, triad-weighted -----

        returns = []
        G = 0.0
        for r in reversed([r.reward for r in step_records]):
            G = r + gamma * G
            returns.append(G)
        returns.reverse()

        returns = torch.as_tensor(returns, dtype=torch.float32)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

        logps = torch.stack([rec.logp for rec in step_records])
        weights = torch.as_tensor([rec.w for rec in step_records], dtype=torch.float32)

        # squash weights to avoid gradient explosions
        weights = torch.tanh(weights)

        advantages = returns * (1.0 + weights)

        loss = -(logps * advantages).mean()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(
            f"[{env_name}] Ep {ep:04d} | R={ep_reward:7.2f} | "
            f"len={len(step_records):3d} | loss={loss.item():.3f}"
        )

    # clean up
    if hasattr(env, "close"):
        env.close()
    return policy

if __name__ == "__main__":
    # Toggle which "grove" the Skogsvätt walks in:
    #   "CartPole-v1" or "Pendulum-v1"
    train_skogsvatt(env_name="CartPole-v1", episodes=300)
    # Then, for transfer, you can reuse the same code with:
    # train_skogsvatt(env_name="Pendulum-v1", episodes=300)
