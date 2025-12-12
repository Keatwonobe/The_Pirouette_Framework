import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import namedtuple

# -------------------------------------------------------------------
# Dark Residue for CartPole: "how close to losing the thread"
# -------------------------------------------------------------------

def dark_residue(state):
    x, x_dot, theta, theta_dot = state
    return (
        1.0 * theta**2 +
        0.1 * theta_dot**2 +
        0.01 * x**2 +
        0.01 * x_dot**2
    )

# -------------------------------------------------------------------
# Triadic Supervisor (Skogsvätt Operator Core)
# -------------------------------------------------------------------

class TriadicSupervisor:
    """
    Minimal implementation of the triadic operator signals for CartPole.
    It does NOT own the policy; it just computes weights for updates.
    """

    def __init__(self, dr_shadow=2.5):
        self.dr_shadow = dr_shadow
        self.last_dr = None

        # phase / rhythm
        self.phi = 0.0
        self.omega = 0.4 * np.pi           # "theta" frequency
        self.update_window = (0.0, np.pi/2)

        # precision coefficients
        self.a0  = -1.0
        self.aS  =  1.0
        self.aDR =  0.7
        self.aG  =  0.2

        # operator gain weights
        self.w_Q = 0.7   # coherence drop
        self.w_C = 0.3   # contrast
        self.w_B = 1.0   # shadow penalty

    def step_metrics(self, state, gamma_load=0.1):
        """
        Given the current state, update operator metrics and return weight.
        """
        dr = dark_residue(state)

        if self.last_dr is None:
            self.last_dr = dr

        # triadic metrics
        Q = max(0.0, self.last_dr - dr)         # coherence drop
        C = abs(dr - self.last_dr)              # contrast
        B = 1.0 if dr > self.dr_shadow else 0.0

        # treat surprise as magnitude of contrast for this minimal agent
        S = C

        # phase gate
        self.phi = (self.phi + self.omega + 0.1*np.random.randn()) % (2*np.pi)
        g = 1.0 if self.update_window[0] <= self.phi <= self.update_window[1] else 0.0

        # precision: open when surprised, close under high DR/load
        Pi = 1.0 / (1.0 + np.exp(
            -(self.a0 + self.aS*S - self.aDR*dr - self.aG*gamma_load)
        ))

        # combine into a scalar weight that will modulate the policy gradient
        # (P-branch via Pi*g, C-branch via Q,C,B)
        operator_weight = g * (Pi + self.w_Q*Q + self.w_C*C - self.w_B*B)

        self.last_dr = dr

        return {
            "DR": dr,
            "Q": Q,
            "C": C,
            "B": B,
            "S": S,
            "Pi": Pi,
            "g": g,
            "w": operator_weight
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
# Training Loop: Skogsvätt in CartPole Grove
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

            # policy action
            action, logp = policy.act(obs)

            # env step
            obs_next, reward, done, trunc, info = env.step(action)

            # operator metrics based on CURRENT state
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

        # you can clamp weights if they explode
        weights = torch.tanh(weights)  # keeps them in (-1,1)

        # combined advantage-like term = returns * operator weight
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
