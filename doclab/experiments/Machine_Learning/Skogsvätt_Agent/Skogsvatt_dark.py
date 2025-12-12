import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import namedtuple

# -------------------------------------------------------------------
# Pirouette-style Dark Residue for CartPole (from Wendigo)
# -------------------------------------------------------------------

def calculate_dark_residue(state: np.ndarray) -> float:
    """
    Dark Residue as used in Wendigo-Minimalist:
    weighted absolute deviation of cart and pole variables.
    """
    cart_pos, cart_vel, pole_angle, pole_vel = state
    return (
        0.4 * abs(cart_pos)
        + 0.2 * abs(cart_vel)
        + 1.5 * abs(pole_angle)
        + 0.3 * abs(pole_vel)
    )

# -------------------------------------------------------------------
# Triadic Supervisor (Skogsvätt Operator Core, Pirouette-flavored)
# -------------------------------------------------------------------

class TriadicSupervisor:
    """
    Computes triadic operator weights using:
      - DR (Pirouette dark residue)
      - coherence gain (drop in DR)
      - dissonance penalty (current DR)
      - contrast (|ΔDR|)
      - shadow flag (high DR)
    Outputs a scalar weight w_t used to modulate REINFORCE gradients.
    """

    def __init__(self, dr_shadow=2.5):
        self.dr_shadow = dr_shadow
        self.last_dr = None

        # phase / rhythm
        self.phi = 0.0
        self.omega = 0.4 * np.pi           # "theta"-like update frequency
        self.update_window = (0.0, np.pi/2)

        # precision coefficients
        self.a0  = -1.0
        self.aS  =  1.0
        self.aDR =  0.7
        self.aG  =  0.2

        # Pirouette-style gains
        self.gamma_coherence = 1.5   # reward for actively reducing DR
        self.delta_dissonance = 1.0  # penalty for current DR

        # weighting for combining terms into w_t
        self.w_Q  = 0.4   # coherence gain influence
        self.w_C  = 0.2   # contrast
        self.w_B  = 0.8   # shadow penalty
        self.w_DR = 0.6   # steady dissonance penalty

    def step_metrics(self, state, gamma_load=0.1):
        """
        Given the current state, update operator metrics and return dict.
        """
        dr = calculate_dark_residue(state)

        if self.last_dr is None:
            self.last_dr = dr

        # basic triadic differentials
        delta_dr = dr - self.last_dr
        Q = max(0.0, -delta_dr)             # coherence gain (drop in DR)
        C = abs(delta_dr)                   # contrast / edge-of-basin
        B = 1.0 if dr > self.dr_shadow else 0.0  # shadow flag
        S = C                               # treat surprise as ΔDR magnitude

        # phase gate
        self.phi = (self.phi + self.omega + 0.1*np.random.randn()) % (2*np.pi)
        g = 1.0 if self.update_window[0] <= self.phi <= self.update_window[1] else 0.0

        # precision: open when surprised, close under high DR/load
        Pi = 1.0 / (1.0 + np.exp(
            -(self.a0 + self.aS*S - self.aDR*dr - self.aG*gamma_load)
        ))

        # Pirouette-flavored stability terms
        coherence_gain     = self.gamma_coherence * Q          # ∝ drop in DR
        dissonance_penalty = self.delta_dissonance * dr        # ∝ current DR

        # combine into a scalar weight that will modulate policy gradient
        # positive: good steps (coherence gain, some contrast, high precision)
        # negative: bad steps (shadow, high ongoing DR)
        raw_w = (
            Pi
            + self.w_Q  * coherence_gain
            + self.w_C  * C
            - self.w_B  * B
            - self.w_DR * dissonance_penalty
        )

        w = g * raw_w  # only acts during update phase

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
            "coh_gain": coherence_gain,
            "diss_pen": dissonance_penalty,
            "w": w
        }

# -------------------------------------------------------------------
# Policy Network: tiny Skogsvätt mind
# -------------------------------------------------------------------

class PolicyNet(nn.Module):
    def __init__(self, obs_dim, hidden=32, n_actions=2):
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

# -------------------------------------------------------------------
# Training Loop: Skogsvätt in CartPole Grove (no SAC, pure REINFORCE)
# -------------------------------------------------------------------

StepRecord = namedtuple("StepRecord", ["logp", "reward", "w"])

def train_skogsvatt_cartpole(
    episodes=500,
    gamma=0.99,
    lr=1e-2,
    render_every=None
):
    env = gym.make("CartPole-v1")
    obs_dim = env.observation_space.shape[0]
    n_actions = env.action_space.n

    policy = PolicyNet(obs_dim, hidden=32, n_actions=n_actions)
    optimizer = optim.Adam(policy.parameters(), lr=lr)

    supervisor = TriadicSupervisor()

    for ep in range(1, episodes+1):
        obs, _ = env.reset()
        supervisor.last_dr = None

        step_records = []
        done = False
        trunc = False
        ep_reward = 0

        while not (done or trunc):
            if render_every and ep % render_every == 0:
                env.render()

            action, logp = policy.act(obs)
            obs_next, reward, done, trunc, info = env.step(action)

            metrics = supervisor.step_metrics(obs)
            w = metrics["w"]

            step_records.append(StepRecord(logp=logp, reward=reward, w=w))
            ep_reward += reward
            obs = obs_next

        # --- REINFORCE update, triad-weighted ---

        # compute returns
        returns = []
        G = 0.0
        for r in reversed([r.reward for r in step_records]):
            G = r + gamma*G
            returns.append(G)
        returns.reverse()
        returns = torch.as_tensor(returns, dtype=torch.float32)

        # normalize returns for stability
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)

        # collect logps and weights
        logps = torch.stack([rec.logp for rec in step_records])
        weights = torch.as_tensor([rec.w for rec in step_records], dtype=torch.float32)

        # clamp / squash weights so operator cannot explode the gradients
        weights = torch.tanh(weights)

        # combined advantage-like term = returns * (1 + weights)
        advantages = returns * (1.0 + weights)

        loss = -(logps * advantages).mean()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(
            f"Ep {ep:04d} | R={ep_reward:4.0f} | "
            f"len={len(step_records):3d} | "
            f"loss={loss.item():.3f} "
        )

    env.close()
    return policy

if __name__ == "__main__":
    train_skogsvatt_cartpole(episodes=500)
