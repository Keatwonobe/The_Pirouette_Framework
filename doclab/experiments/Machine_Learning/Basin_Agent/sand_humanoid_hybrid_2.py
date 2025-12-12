#!/usr/bin/env python3

import argparse
from pathlib import Path
import copy
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

# --- HYDRA IMPORT ---
# (Make sure this is in your Python path)
try:
    from fractal_intelligence_transfer import ManifoldWell
except ImportError:
    print("Warning: ManifoldWell not found. 'touch' and 'fusion' modes will fail.")
    # Mock class to allow script to load
    class ManifoldWell:
        def __init__(self, *args, **kwargs): pass
        def step(self, t): pass
        def get_reward(self, action): return 0.0


# =====================================================================
# Sand Brain Wrapper
# =====================================================================

class SandBrain:
    """
    Wraps the sand agent and exposes a fixed-length feature vector.
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

        # Encourage stable early behavior (narrower std)
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

        # Gaussian log prob of eps under N(0, I) with scaling
        log_prob = -0.5 * ((eps**2) + 2 * log_std + np.log(2 * np.pi))
        log_prob = log_prob.sum(dim=-1, keepdim=True)

        return action, log_prob


# =====================================================================
# Runner Config (with Hydra weights)
# =====================================================================

class Config:
    env_id = "Humanoid-v5"
    episodes = 1500
    max_steps = 2000
    gamma = 0.99
    lr = 3e-4
    render = False
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # --- Hydra reward weights ---
    alpha_touch = 0.05   # weight for ManifoldWell intrinsic
    alpha_brain = 0.05   # weight for sand-brain intrinsic (e.g. -DR)
    
    # --- Ratchet settings (now used by HydraHumanoid) ---
    ratchet_start_ep = 50       
    ratchet_patience = 24       # (Global ratchet patience)


# =====================================================================
# Humanoid Runner (Worker for Hydra)
# =====================================================================

class SandHumanoidRunner:
    def __init__(self, basin_json: Path, cfg=Config(), mode: str = "pure"):
        self.cfg = cfg
        self.mode = mode # <-- 4.2: Store the mode
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

        # --- 4.2: ManifoldWell "sense of touch" ---
        self.manifold = ManifoldWell(action_dim=act_dim, max_steps=cfg.max_steps)

        # (Old ratchet state is removed, Hydra class handles it)

    # --------------------------------------------------------------
    def run_episode(self):
        """
        Runs one episode using the runner's mode to calculate hybrid rewards.
        Returns:
            traj (dict): Trajectory data.
                         "rewards" = total hybrid reward (for REINFORCE)
                         "return"  = raw env reward (for plateau tracking)
        """
        obs, _ = self.env.reset()
        obs = obs.astype(np.float32)

        log_probs = []
        rewards = []      # <-- 4.3: Total reward (env + intrinsic)
        env_rewards = []  # <-- 4.3: Raw env reward for logging
        
        brain_log = {"DR": [], "S": [], "Gamma": [], "pi": [], "operator_norm": []}

        observations = []
        actions = []
        brain_features = []
        
        previous_DR = None # <-- 4.3: For Wendigo-style delta-DR

        for t in range(self.cfg.max_steps):
            if self.cfg.render:
                self.env.render()

            # --- 1) Brain step ---
            _, brain_feat, sample = self.brain.sample()
            observations.append(obs.copy())
            brain_features.append(brain_feat.copy())

            for k in brain_log:
                if k in sample:
                    brain_log[k].append(float(sample[k]))

            # --- 2) Policy forward ---
            obs_t = torch.as_tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
            brain_t = torch.as_tensor(brain_feat, dtype=torch.float32, device=self.device).unsqueeze(0)

            with torch.no_grad():
                # (Using sample_action as it returns logp_t)
                action_t, logp_t = self.policy.sample_action(obs_t, brain_t)

            action = action_t.cpu().numpy()[0]
            actions.append(action.copy())
            log_probs.append(logp_t)

            # --- 3) Env step ---
            next_obs, r_env, term, trunc, _ = self.env.step(action)
            env_rewards.append(float(r_env))

            # --- 4) Intrinsic rewards (Hydra heads) ---
            r_touch = 0.0
            r_brain = 0.0

            # Manifold "sense of touch"
            if self.mode in ("touch", "fusion"):
                self.manifold.step(t)
                r_touch = self.manifold.get_reward(action)

            # Sand-brain intrinsic (e.g., reward reductions in DR)
            if self.mode in ("brain", "fusion"):
                DR_t = float(sample["DR"])
                if previous_DR is not None:
                    dDR = DR_t - previous_DR
                    r_brain = max(0.0, -dDR) # reward reducing DR
                previous_DR = DR_t

            # --- 5) Combine ---
            total_reward = (
                float(r_env)
                + self.cfg.alpha_touch * r_touch
                + self.cfg.alpha_brain * r_brain
            )

            rewards.append(total_reward) # Append the hybrid reward
            obs = next_obs.astype(np.float32)

            if term or trunc:
                break

        return {
            "log_probs": torch.cat(log_probs),
            "rewards": rewards,         # <-- Used for REINFORCE
            "brain": brain_log,
            "return": sum(env_rewards), # <-- *Env* return for plateau tracking
            "obs": np.array(observations),
            "actions": np.array(actions),
            "brain_features": np.array(brain_features),
        }

    # --------------------------------------------------------------
    def update(self, traj):
        """
        This method stays the same. It uses traj["rewards"], which
        now correctly points to the total_reward (hybrid) list.
        """
        rewards = traj["rewards"]
        actions = traj["actions"]
        obs = traj["obs"]
        brain = traj["brain_features"]

        T = len(rewards)

        # ---- Returns (no grad) ----
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

        # ---- Recompute log_probs on-graph ----
        obs_t = torch.as_tensor(obs, dtype=torch.float32, device=self.device)
        brain_t = torch.as_tensor(brain, dtype=torch.float32, device=self.device)
        acts_t = torch.as_tensor(actions, dtype=torch.float32, device=self.device)

        mean, log_std = self.policy.forward(obs_t, brain_t)
        std = torch.exp(log_std)
        dist = torch.distributions.Normal(mean, std)

        log_probs = dist.log_prob(acts_t).sum(dim=-1, keepdim=True)

        # ---- REINFORCE loss ----
        loss = -(log_probs * returns_t).sum()

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 1.0)
        self.optimizer.step()

        return loss.item()

    # (--- The old _ratchet_step and train methods are removed ---)
    # (--- HydraHumanoid will now handle training and ratcheting ---)


# =====================================================================
# 5. Hydra Orchestrator
# =====================================================================

MODES = ["pure", "touch", "brain", "fusion"]

class HydraHumanoid:
    def __init__(self, basin_json: Path, cfg=Config()):
        self.cfg = cfg
        print(f"\n=== Hydra Humanoid Orchestrator ===")
        print(f"Modes: {MODES}")
        print(f"Device: {cfg.device}\n")
        
        self.runners = {
            mode: SandHumanoidRunner(basin_json, cfg, mode=mode)
            for mode in MODES
        }

        # All start from same weights as "pure"
        base_state = self.runners["pure"].policy.state_dict()
        for mode in MODES:
            if mode != "pure":
                self.runners[mode].policy.load_state_dict(base_state)

        self.best_return = -1e9
        self.best_state = copy.deepcopy(base_state) # Use deepcopy
        self.no_improve = 0
        self.ep = 0

    def train(self):
        while self.ep < self.cfg.episodes:
            for mode in MODES:
                if self.ep >= self.cfg.episodes: break
                
                self.ep += 1
                runner = self.runners[mode]
                
                # Sync policy to best global policy before running
                runner.policy.load_state_dict(self.best_state)
                
                # Run and update this runner
                traj = runner.run_episode()
                loss = runner.update(traj)

                R_env = traj["return"] # Get raw env return
                
                if R_env > self.best_return:
                    self.best_return = R_env
                    # Store the new best state from *this* runner
                    self.best_state = copy.deepcopy(runner.policy.state_dict())
                    self.no_improve = 0
                    print(f"   ↳ [Hydra] New global plateau: {self.best_return:.1f} (mode={mode})")
                else:
                    self.no_improve += 1

                # Log stats
                mean_DR = np.mean(traj["brain"]["DR"])
                mean_G = np.mean(traj["brain"]["Gamma"])
                print(
                    f"[{mode:6s}] Ep {self.ep:04d} | "
                    f"EnvRet: {R_env:7.1f} | "
                    f"Loss: {loss:9.3f} | "
                    f"DR: {mean_DR:.3f} | "
                    f"Γ: {mean_G:.3f}"
                )

                # Global ratchet
                if (
                    self.ep > self.cfg.ratchet_start_ep and
                    self.no_improve > self.cfg.ratchet_patience
                ):
                    print(f"   ↳ [Hydra] Ratchet: no improvement for {self.no_improve} eps.")
                    print(f"   ↳ Reverting all heads to best_state (Return={self.best_return:.1f})")
                    # The sync at the start of the loop handles the revert
                    self.no_improve = 0


# =====================================================================
# CLI (Now launches Hydra)
# =====================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--basin-json", type=Path, required=True)
    args = parser.parse_args()

    # Pass config object to Hydra
    hydra = HydraHumanoid(args.basin_json, cfg=Config())
    hydra.train()


if __name__ == "__main__":
    main()