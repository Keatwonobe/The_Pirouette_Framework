#!/usr/bin/env python3
"""
Sand Agent Continuous Runner
============================

Uses the Sand "brain" as an engrammatic prior for continuous-control tasks.

Core idea (v0.1):
-----------------
- At every environment step we sample an internal Sand state:
    basin_id, DR, S, Gamma, pi, g, O_P, O_S, O_C, operator_norm, ...
- We concatenate those brain features onto the environment observation.
- A small Gaussian policy network maps [obs || brain_state] -> action.
- We train with REINFORCE and log both task reward and brain statistics.

This is deliberately simple: it's an *engram-mating harness*.
You can later swap in fancier losses, critics, or your existing RL cores.
"""

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Dict, List

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# Gym / Gymnasium compatibility
try:
    import gymnasium as gym
except ImportError:
    import gym

# --- Import your Sand agent pieces ------------------------------------------
from sand_agent_sand import SandAgentConfig, BasinPrior, SandAgentIncremental
# :contentReference[oaicite:1]{index=1}


# ============================================================================
# Sand "Brain" Wrapper
# ============================================================================

class SandBrain:
    """
    Thin wrapper that exposes a 'sample()' interface returning
    (basin_id, feature_vector).

    Features (v0.1):
        [DR, S, Gamma, pi, g, O_P, O_S, O_C, operator_norm, B]
    """

    def __init__(self, basin_json: Path, config: SandAgentConfig | None = None):
        self.basin_prior = BasinPrior(basin_json)
        self.config = config or SandAgentConfig()
        self.agent = SandAgentIncremental(self.config, self.basin_prior)

    @property
    def feature_dim(self) -> int:
        return 10

    def sample(self) -> Tuple[int, np.ndarray, Dict]:
        """
        Returns:
            basin_id (int)
            features (np.ndarray, shape [10])
            raw_sample (dict) – full dictionary from SandAgentIncremental
        """
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
            sample["B"],
        ], dtype=np.float32)

        return basin_id, features, sample


# ============================================================================
# Policy Network
# ============================================================================

class SandPolicyNet(nn.Module):
    """
    Simple Gaussian policy:

        input:  [obs_dim + brain_dim]
        output: mean, log_std  (per action dimension)

    Action is sampled as:
        a = tanh(mean + std * eps) * action_scale
    """

    def __init__(
        self,
        obs_dim: int,
        brain_dim: int,
        action_dim: int,
        hidden_sizes: Tuple[int, int] = (256, 256),
        action_scale: float = 1.0,
    ):
        super().__init__()
        self.action_dim = action_dim
        self.action_scale = action_scale

        in_dim = obs_dim + brain_dim
        h1, h2 = hidden_sizes

        self.net = nn.Sequential(
            nn.Linear(in_dim, h1),
            nn.ReLU(),
            nn.Linear(h1, h2),
            nn.ReLU(),
            nn.Linear(h2, 2 * action_dim),  # mean and log_std
        )

        # Initialize log_std bias a bit negative to avoid crazy exploration
        with torch.no_grad():
            self.net[-1].bias[action_dim:].fill_(-0.5)

    def forward(self, obs: torch.Tensor, brain: torch.Tensor):
        x = torch.cat([obs, brain], dim=-1)
        out = self.net(x)
        mean, log_std = torch.chunk(out, 2, dim=-1)
        log_std = torch.clamp(log_std, -5.0, 2.0)
        return mean, log_std

    def sample_action(
        self, obs: torch.Tensor, brain: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        mean, log_std = self.forward(obs, brain)
        std = torch.exp(log_std)

        eps = torch.randn_like(mean)
        pre_tanh = mean + std * eps
        action = torch.tanh(pre_tanh) * self.action_scale

        # Log prob of tanh-squashed Gaussian (approx)
        # (for now we treat it as plain Gaussian to keep things simple)
        log_prob = (
            -0.5 * ((eps ** 2) + 2 * log_std + np.log(2 * np.pi))
        ).sum(dim=-1, keepdim=True)

        return action, log_prob


# ============================================================================
# Training Loop (REINFORCE)
# ============================================================================

@dataclass
class RunnerConfig:
    env_id: str = "Pendulum-v1"
    episodes: int = 200
    max_steps: int = 200
    gamma: float = 0.99
    lr: float = 3e-4
    render: bool = False
    device: str = "cuda" if torch.cuda.is_available() else "cpu"


class SandContinuousRunner:
    def __init__(self, env_id: str, basin_json: Path, cfg: RunnerConfig):
        self.cfg = cfg
        self.env = gym.make(env_id)
        self.device = torch.device(cfg.device)

        # --- Inspect spaces --------------------------------------------------
        assert isinstance(
            self.env.action_space, gym.spaces.Box
        ), "This runner currently supports Box (continuous) action spaces only."

        obs_dim = int(np.prod(self.env.observation_space.shape))
        action_dim = int(np.prod(self.env.action_space.shape))
        action_high = float(self.env.action_space.high[0])  # assume symmetric

        # --- Brain + Policy --------------------------------------------------
        self.brain = SandBrain(basin_json)
        brain_dim = self.brain.feature_dim

        self.policy = SandPolicyNet(
            obs_dim=obs_dim,
            brain_dim=brain_dim,
            action_dim=action_dim,
            action_scale=action_high,
        ).to(self.device)

        self.optimizer = optim.Adam(self.policy.parameters(), lr=cfg.lr)

    # --------------------------------------------------------------------- #
    def _collect_episode(self) -> Dict:
        obs, _ = self.env.reset()
        obs = obs.astype(np.float32)

        log_probs: List[torch.Tensor] = []
        rewards: List[float] = []
        brain_stats: Dict[str, List[float]] = {
            "DR": [],
            "S": [],
            "Gamma": [],
            "pi": [],
            "operator_norm": [],
        }

        observations: List[np.ndarray] = []
        brain_features: List[np.ndarray] = []
        actions: List[np.ndarray] = []

        for t in range(self.cfg.max_steps):
            if self.cfg.render:
                self.env.render()

            _, brain_feat, sample = self.brain.sample()

            observations.append(obs)
            brain_features.append(brain_feat)

            # --- Brain sample ------------------------------------------------

            for k in brain_stats.keys():
                brain_stats[k].append(float(sample[k]))

            # --- Torch tensors ----------------------------------------------
            obs_t = torch.as_tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
            brain_t = torch.as_tensor(brain_feat, dtype=torch.float32, device=self.device).unsqueeze(0)

            with torch.no_grad():
                action_t, log_prob_t = self.policy.sample_action(obs_t, brain_t)

            action = action_t.cpu().numpy()[0]
            actions.append(action) #added
            log_probs.append(log_prob_t)

            next_obs, reward, terminated, truncated, _ = self.env.step(action)
            rewards.append(float(reward))

            obs = next_obs.astype(np.float32)
            if terminated or truncated:
                break

        return {
            "log_probs": torch.cat(log_probs, dim=0),  # [T, 1]
            "rewards": rewards,
            "brain_stats": brain_stats,
            "length": len(rewards),
            "return": sum(rewards),
            # --- ADD THESE KEYS ---
            "observations": observations,
            "brain_features": brain_features,
            "actions": actions,
            # ------------------------
        }

    # --------------------------------------------------------------------- #
    def _update_policy(self, traj: Dict):
        # Compute returns G_t
        rewards = traj["rewards"]
        T = len(rewards)
        returns = np.zeros(T, dtype=np.float32)
        G = 0.0
        for t in reversed(range(T)):
            G = rewards[t] + self.cfg.gamma * G
            returns[t] = G

        # --- START FIX ---

        # 1. Convert trajectory data to tensors
        states = torch.as_tensor(np.array(traj["observations"]), dtype=torch.float32, device=self.device)
        actions = torch.as_tensor(np.array(traj["actions"]), dtype=torch.float32, device=self.device)
        
        # You were missing the brain features, which the policy needs
        brain_states = torch.as_tensor(np.array(traj["brain_features"]), dtype=torch.float32, device=self.device)
        
        returns_t = torch.as_tensor(
            (returns - returns.mean()) / (returns.std() + 1e-8),
            dtype=torch.float32,
            device=self.device,
        ) # Shape [T]

        # 2. Re-evaluate the policy to get "live" log_probs
        # This is the key step to build the computational graph
        # The policy needs BOTH observations (states) and brain_states
        mean, log_std = self.policy(states, brain_states)
        
        # 3. Calculate the log_prob for the *actions taken*
        # We must manually re-calculate the Gaussian log_prob,
        # replicating the logic from the `sample_action` method.
        
        std = torch.exp(log_std)
        
        # Invert the tanh: action = tanh(pre_tanh) * scale -> pre_tanh = atanh(action / scale)
        # Clamp actions for numerical stability of atanh
        clamped_actions = torch.clamp(actions / self.policy.action_scale, -0.9999, 0.9999)
        pre_tanh_actions = torch.atanh(clamped_actions)

        # Calculate 'eps' (the noise sample that *would* have produced this action)
        eps = (pre_tanh_actions - mean) / (std + 1e-8) # add epsilon to std

        # Calculate log_prob of a plain (non-squashed) Gaussian
        # This matches the simplified log_prob in sample_action
        log_probs = (
            -0.5 * ((eps ** 2) + 2 * log_std + np.log(2 * np.pi))
        ).sum(dim=-1) # Sum over action dimensions -> shape [T]
        
        # 4. Calculate loss using the "live" log_probs
        # log_probs has shape [T] and returns_t has shape [T]
        loss = -(log_probs * returns_t).sum()
        
        # --- END FIX ---

        self.optimizer.zero_grad()
        loss.backward() # This will work now
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 1.0)
        self.optimizer.step()

        return float(loss.item())

    # --------------------------------------------------------------------- #
    def train(self):
        print("\n=== Sand Agent Continuous Runner ===")
        print(f"Env: {self.env.unwrapped.spec.id}")
        print(f"Device: {self.device}")
        print(f"Episodes: {self.cfg.episodes}, max_steps: {self.cfg.max_steps}\n")

        for ep in range(1, self.cfg.episodes + 1):
            traj = self._collect_episode()
            loss = self._update_policy(traj)

            # Log basic stats
            ep_ret = traj["return"]
            ep_len = traj["length"]
            brain = traj["brain_stats"]

            msg = (
                f"Ep {ep:04d} | "
                f"Return: {ep_ret:8.3f} | Len: {ep_len:4d} | "
                f"Loss: {loss:7.3f} | "
                f"DR: {np.mean(brain['DR']):.3f} | "
                f"S: {np.mean(brain['S']):.3f} | "
                f"Γ: {np.mean(brain['Gamma']):.3f} | "
                f"π: {np.mean(brain['pi']):.3f} | "
                f"‖O‖: {np.mean(brain['operator_norm']):.3f}"
            )
            print(msg)

        self.env.close()


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Run Sand Agent brain on continuous control tasks."
    )
    parser.add_argument(
        "--env",
        type=str,
        default="Pendulum-v1",
        help="Gym/Gymnasium env id (e.g. Pendulum-v1, HalfCheetah-v4, Ant-v4).",
    )
    parser.add_argument(
        "--basin-json",
        type=Path,
        required=True,
        help="Path to basin structure JSON used by sand_agent_sand.py",
    )
    parser.add_argument("--episodes", type=int, default=200)
    parser.add_argument("--max-steps", type=int, default=200)
    parser.add_argument("--gamma", type=float, default=0.99)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument(
        "--render", action="store_true", help="Render the environment."
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        help='"auto", "cpu", or "cuda"',
    )

    args = parser.parse_args()

    device = (
        "cuda"
        if args.device == "auto" and torch.cuda.is_available()
        else ("cpu" if args.device == "auto" else args.device)
    )

    cfg = RunnerConfig(
        env_id=args.env,
        episodes=args.episodes,
        max_steps=args.max_steps,
        gamma=args.gamma,
        lr=args.lr,
        render=args.render,
        device=device,
    )

    runner = SandContinuousRunner(args.env, args.basin_json, cfg)
    runner.train()


if __name__ == "__main__":
    main()
