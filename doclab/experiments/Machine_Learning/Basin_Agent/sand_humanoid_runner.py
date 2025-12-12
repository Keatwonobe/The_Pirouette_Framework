#!/usr/bin/env python3

import argparse
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# Gym / Gymnasium compatibility
try:
    import gymnasium as gym
except ImportError:
    import gym

# Import your sand brain
from sand_agent_sand import SandAgentConfig, BasinPrior, SandAgentIncremental


# =====================================================================
# Sand Brain Wrapper
# =====================================================================

class SandBrain:
    """
    Same idea as before, but with Humanoid-specific scaling:
    - In Humanoid, exploration is essential early;
      so we expose additional knobs for modulation.
    """

    def __init__(self, basin_json: Path):
        cfg = SandAgentConfig()
        self.basin_prior = BasinPrior(basin_json)
        self.agent = SandAgentIncremental(cfg, self.basin_prior)

    @property
    def feature_dim(self):
        return 10

    def sample(self):
        basin_id = self.basin_prior.sample_basin()
        sample = self.agent.generate_sample(basin_id)

        features = np.array([
            sample["DR"],
            sample["S"],
            sample["Gamma"],
            sample["pi"],
            sample["g"],
            sample["O_P"],
            sample["O_S"],
            sample["O_C"],
            sample["operator_norm"],
            sample["B"]
        ], dtype=np.float32)

        return basin_id, features, sample


# =====================================================================
# Policy Network tuned for Humanoid
# =====================================================================

class SandPolicyHumanoid(nn.Module):
    """
    Large Gaussian policy for Humanoid, with sand-brain gating.
    """

    def __init__(
        self,
        obs_dim,
        brain_dim,
        action_dim,
        hidden=(512, 512, 256),
        action_scale=1.0,
    ):
        super().__init__()
        self.action_dim = action_dim
        self.action_scale = action_scale

        h1, h2, h3 = hidden
        inp = obs_dim + brain_dim

        self.net = nn.Sequential(
            nn.Linear(inp, h1),
            nn.Tanh(),
            nn.Linear(h1, h2),
            nn.Tanh(),
            nn.Linear(h2, h3),
            nn.Tanh(),
            nn.Linear(h3, 2 * action_dim),
        )

        # Encourage stable early behavior
        with torch.no_grad():
            self.net[-1].bias[action_dim:].fill_(-1.0)

    def forward(self, obs, brain):
        x = torch.cat([obs, brain], dim=-1)
        out = self.net(x)
        mean, log_std = torch.chunk(out, 2, dim=-1)
        log_std = torch.clamp(log_std, -5.0, 1.0)
        return mean, log_std

    def sample_action(self, obs, brain):
        mean, log_std = self.forward(obs, brain)
        std = torch.exp(log_std)

        eps = torch.randn_like(mean)
        pre_tanh = mean + std * eps
        action = torch.tanh(pre_tanh) * self.action_scale

        # Gaussian log prob
        log_prob = -0.5 * (
            (eps**2) + 2 * log_std + np.log(2 * np.pi)
        ).sum(dim=-1, keepdim=True)

        return action, log_prob


# =====================================================================
# Runner Config
# =====================================================================

class Config:
    env_id = "Humanoid-v5"
    episodes = 1500
    max_steps = 2000
    gamma = 0.99
    lr = 3e-4
    render = False
    device = "cuda" if torch.cuda.is_available() else "cpu"


# =====================================================================
# Humanoid Runner
# =====================================================================

class SandHumanoidRunner:
    def __init__(self, basin_json: Path, cfg=Config()):
        self.cfg = cfg
        self.env = gym.make(cfg.env_id)
        self.device = torch.device(cfg.device)

        obs_dim = int(np.prod(self.env.observation_space.shape))
        act_dim = int(np.prod(self.env.action_space.shape))
        act_scale = float(self.env.action_space.high[0])

        self.brain = SandBrain(basin_json)
        brain_dim = self.brain.feature_dim

        self.policy = SandPolicyHumanoid(
            obs_dim=obs_dim,
            brain_dim=brain_dim,
            action_dim=act_dim,
            action_scale=act_scale,
        ).to(self.device)

        self.optimizer = optim.Adam(self.policy.parameters(), lr=cfg.lr)

    # --------------------------------------------------------------
    def run_episode(self):
        obs, _ = self.env.reset()
        obs = obs.astype(np.float32)

        log_probs = []
        rewards = []
        brain_log = {"DR": [], "S": [], "Gamma": [], "pi": [], "operator_norm": []}

        # --- ADD THESE ---
        observations = []
        actions = []
        brain_features = []

        for t in range(self.cfg.max_steps):

            if self.cfg.render:
                self.env.render()

            # Brain step
            _, brain_feat, sample = self.brain.sample()

            observations.append(obs.copy())
            brain_features.append(brain_feat.copy())

            # Track for logs
            for k in brain_log:
                brain_log[k].append(float(sample[k]))

            obs_t = torch.as_tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
            brain_t = torch.as_tensor(brain_feat, dtype=torch.float32, device=self.device).unsqueeze(0)

            with torch.no_grad():
                action_t, logp_t = self.policy.sample_action(obs_t, brain_t)

            action = action_t.cpu().numpy()[0]
            actions.append(action.copy())
            log_probs.append(logp_t)

            next_obs, reward, term, trunc, _ = self.env.step(action)
            rewards.append(float(reward))

            obs = next_obs.astype(np.float32)

        

            if term or trunc:
                break

        return {
            "log_probs": torch.cat(log_probs),
            "rewards": rewards,
            "brain": brain_log,
            "return": sum(rewards),
            
            # --- ADD THESE ---
            "obs": np.array(observations),
            "actions": np.array(actions),
            "brain_features": np.array(brain_features)
            # -----------------
        }

    # --------------------------------------------------------------
    def update(self, traj):
        # Unpack
        rewards = traj["rewards"]
        actions = traj["actions"]             # <-- MUST add this to your traj dict
        obs     = traj["obs"]                 # <-- MUST add this to your traj dict
        brain   = traj["brain_features"]      # <-- MUST add this as well

        T = len(rewards)
    
        # ---- Compute returns (no grad needed here) ----
        returns = np.zeros(T, dtype=np.float32)
        G = 0.0
        for t in reversed(range(T)):
            G = rewards[t] + self.cfg.gamma * G
            returns[t] = G

        returns_t = torch.as_tensor(
            (returns - returns.mean()) / (returns.std() + 1e-8),
            dtype=torch.float32,
            device=self.device,
        ).unsqueeze(-1)

        # ---- Recompute log_probs ON-GRAPH ----
        obs_t   = torch.as_tensor(obs, dtype=torch.float32, device=self.device)
        brain_t = torch.as_tensor(brain, dtype=torch.float32, device=self.device)
        acts_t  = torch.as_tensor(actions, dtype=torch.float32, device=self.device)

        mean, log_std = self.policy.forward(obs_t, brain_t)
        std = torch.exp(log_std)
        dist = torch.distributions.Normal(mean, std)

        # Sum over action dimensions -> (T,1)
        log_probs = dist.log_prob(acts_t).sum(dim=-1, keepdim=True)

        # ---- Proper REINFORCE loss ----
        loss = -(log_probs * returns_t).sum()

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 1.0)
        self.optimizer.step()

        return loss.item()


    # --------------------------------------------------------------
    def train(self):
        print("\n=== Sand Humanoid Runner ===")
        for ep in range(1, self.cfg.episodes + 1):
            traj = self.run_episode()
            loss = self.update(traj)

            mean_DR = np.mean(traj["brain"]["DR"])
            mean_G = np.mean(traj["brain"]["Gamma"])
            mean_pi = np.mean(traj["brain"]["pi"])

            print(
                f"Ep {ep:04d} | "
                f"Return: {traj['return']:8.1f} | "
                f"Loss: {loss:7.3f} | "
                f"DR: {mean_DR:.3f} | "
                f"Γ: {mean_G:.3f} | "
                f"π: {mean_pi:.3f}"
            )


# =====================================================================
# CLI
# =====================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--basin-json", type=Path, required=True)
    args = parser.parse_args()

    runner = SandHumanoidRunner(args.basin_json)
    runner.train()


if __name__ == "__main__":
    main()
