#!/usr/bin/env python3
"""
Sand Humanoid with Generative Engram Architecture
=================================================

This is a MODULAR refactor that makes the engram the solution, not the script.

Key Design Principles:
---------------------
1. Engram Library is the PRIMARY knowledge store
2. Policy learns BY RESONATING with engrams
3. Each mode (pure/touch/brain/fusion) QUERIES engrams differently
4. The architecture DISCOVERS the bifurcated structure through coherence optimization

Architecture Components:
-----------------------
- SandBrain: Computes Pirouette metrics (Γ, DR, S, O_P, O_S, O_C)
- SandPolicyRecurrent: GRU-based "Ki core rhythm" 
- EngramLibrary: Resonance-addressable memory (from pirouette_engram.py)
- HydraHumanoid: Multi-mode orchestrator with engram-driven learning
"""

import argparse
from pathlib import Path
import copy
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Dict, List, Optional
from collections import deque

# Gym compatibility
try:
    import gymnasium as gym
except ImportError:
    import gym

# Sand agent imports
from sand_agent_sand import SandAgentConfig, BasinPrior, SandAgentIncremental

# Engram system
from pirouette_engram import (
    GenerativeEngram, 
    EngramLibrary, 
    EngramDistiller,
    EngramFactory
)

# Import RPA enhancements
from engram_rpa_selector import (
    RPAWeightedDistiller,
    CriticalMomentExtractor,
    RPAAnalyzer
)

# Fractal intelligence transfer (optional)
try:
    from fractal_intelligence_transfer import ManifoldWell
except ImportError:
    print("Warning: ManifoldWell not found. 'touch' mode will fall back to 'pure'.")
    class ManifoldWell:
        def __init__(self, *args, **kwargs): pass
        def step(self, t): pass
        def get_reward(self, action): return 0.0

from valley_guided_reward import ValleyRewardConfig, build_valley_reward

# =====================================================================
# §1: Configuration
# =====================================================================

class Config:
    """Centralized configuration for the engram-driven agent."""
    
    # Environment
    env_id = "Humanoid-v5"
    max_steps = 2000
    render = False
    
    # Training
    episodes = 2500
    gamma = 0.99
    lr = 3e-4
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Engram system (COG-RES-004 + INST-NALY-001 RPA parameters)
    engram_capacity = 20           # Max engrams in library
    engram_distill_every = 100     # Distill every N episodes
    engram_distill_steps = 50      # Gradient steps per distillation
    engram_lr_scale = 0.1          # LR reduction during distillation
    
    # RPA parameters (NEW - INST-NALY-001)
    rpa_enabled = True             # Use RPA-weighted distillation
    rpa_weight = 5.0               # How much more to weight critical moments
    rpa_pareto_threshold = 0.8     # Find moments accounting for 80% of impact
    rpa_use_highlights = False     # If True, use condensed highlight reels
    
    # Hydra reward composition
    alpha_touch = 0.05   # ManifoldWell intrinsic reward
    alpha_brain = 0.05   # Sand-brain intrinsic reward
    
    # Ratchet (plateau escape)
    ratchet_start_ep = 50
    ratchet_patience = 50
    
    # Wind disturbance
    wind_enabled = True
    wind_force_min = 40.0
    wind_force_max = 120.0
    wind_prob = 0.12
    wind_min_duration = 15
    wind_max_duration = 80
    wind_start_step = 50
    wind_body = "torso"

    # Valley-shaped intrinsic reward (from successful_valleys.csv)
    valley_csv = None          # set via CLI or manually
    alpha_valley = 0.05        # weight of valley bonus in total return
    valley_bonus_scale = 1.0   # scales the intrinsic before alpha_valley


# =====================================================================
# §2: Sand Brain (Pirouette Metrics Computer)
# =====================================================================

class SandBrain:
    """
    Computes Pirouette Framework metrics: Γ, DR, S, operators.
    This is the "diagnostic exhaust" per COG-RES-006.
    """
    
    def __init__(self, basin_json: Path):
        cfg = SandAgentConfig()
        self.basin_prior = BasinPrior(basin_json)
        self.agent = SandAgentIncremental(cfg, self.basin_prior)
    
    @property
    def feature_dim(self):
        return 10
    
    def sample(self) -> tuple:
        """
        Sample brain state.
        Returns: (basin_id, features, full_sample_dict)
        """
        basin_id = self.basin_prior.sample_basin()
        sample = self.agent.generate_sample(basin_id)
        
        features = np.array([
            sample["DR"],           # 0: Dark Residue
            sample["S"],            # 1: Surprise
            sample["Gamma"],        # 2: Temporal pressure/load
            sample["pi"],           # 3: Precision
            sample["g"],            # 4: Gate
            sample["O_P"],          # 5: Precision operator
            sample["O_S"],          # 6: Surprise operator
            sample["O_C"],          # 7: Coherence operator
            sample["operator_norm"], # 8: Total operator magnitude
            sample["B"]             # 9: Shadow basin indicator
        ], dtype=np.float32)
        
        return basin_id, features, sample


# =====================================================================
# §3: Recurrent Policy (Ki Core Rhythm)
# =====================================================================

class SandPolicyRecurrent(nn.Module):
    """
    Recurrent Gaussian policy with GRU as "Ki core rhythm".
    
    The GRU hidden state represents the attractor coordinates in
    the generative engram's DDE phase space (COG-RES-004 §4).
    """
    
    def __init__(self, obs_dim, brain_dim, action_dim, 
                 hidden_dim=256, action_scale=1.0):
        super().__init__()
        self.action_dim = action_dim
        self.action_scale = action_scale
        self.hidden_dim = hidden_dim
        
        inp_dim = obs_dim + brain_dim
        
        self.input_layer = nn.Linear(inp_dim, hidden_dim)
        self.gru_cell = nn.GRUCell(hidden_dim, hidden_dim)
        self.output_layer = nn.Linear(hidden_dim, 2 * action_dim)
        
        # Initialize for stable early behavior
        with torch.no_grad():
            self.output_layer.bias[action_dim:].fill_(-1.0)
    
    def forward(self, obs, brain, h_in):
        """
        Single step forward pass.
        Returns: (mean, log_std, h_out)
        """
        x = torch.cat([obs, brain], dim=-1)
        x = torch.tanh(self.input_layer(x))
        h_out = self.gru_cell(x, h_in)
        
        out = self.output_layer(h_out)
        mean, log_std = torch.chunk(out, 2, dim=-1)
        log_std = torch.clamp(log_std, -5.0, 1.0)
        
        return mean, log_std, h_out
    
    def sample_action(self, obs, brain, h_in):
        """Sample action with log probability."""
        mean, log_std, h_out = self.forward(obs, brain, h_in)
        
        std = torch.exp(log_std)
        eps = torch.randn_like(mean)
        pre_tanh = mean + std * eps
        action = torch.tanh(pre_tanh) * self.action_scale
        
        log_prob = -0.5 * ((eps**2) + 2 * log_std + np.log(2 * np.pi))
        log_prob = log_prob.sum(dim=-1, keepdim=True)
        
        return action, log_prob, h_out


# =====================================================================
# §4: Wind Wrapper (Environmental Disturbance)
# =====================================================================

class WindWrapper(gym.Wrapper):
    """Adds stochastic wind gusts to humanoid."""
    
    def __init__(self, env, cfg: Config):
        super().__init__(env)
        self.cfg = cfg
        self.gust_active = False
        self.gust_remaining = 0
        self.gust_force = np.zeros(3)
        self.step_count = 0
    
    def reset(self, **kwargs):
        self.gust_active = False
        self.gust_remaining = 0
        self.step_count = 0
        return self.env.reset(**kwargs)
    
    def step(self, action):
        obs, reward, done, trunc, info = self.env.step(action)
        self.step_count += 1
        
        if not self.cfg.wind_enabled or self.step_count < self.cfg.wind_start_step:
            return obs, reward, done, trunc, info
        
        # Update gust state
        if self.gust_active:
            self.gust_remaining -= 1
            if self.gust_remaining <= 0:
                self.gust_active = False
        else:
            if np.random.rand() < self.cfg.wind_prob:
                self._start_gust()
        
        # Apply force
        if self.gust_active:
            try:
                body_id = self.env.unwrapped.model.body(self.cfg.wind_body).id
                self.env.unwrapped.data.xfrc_applied[body_id, :3] = self.gust_force
            except:
                pass
        
        return obs, reward, done, trunc, info
    
    def _start_gust(self):
        """Initialize a new wind gust."""
        self.gust_active = True
        self.gust_remaining = np.random.randint(
            self.cfg.wind_min_duration, 
            self.cfg.wind_max_duration + 1
        )
        
        # Random direction in XY plane
        angle = np.random.uniform(0, 2 * np.pi)
        magnitude = np.random.uniform(self.cfg.wind_force_min, self.cfg.wind_force_max)
        
        self.gust_force = np.array([
            magnitude * np.cos(angle),
            magnitude * np.sin(angle),
            0.0
        ])

class SuccessfulValleyGuide:
    """
    Online valley-shape intrinsic reward.

    - Loads successful valley stats from successful_valleys.csv
    - Reconstructs a "target band" in (duration, coherence_drop, net_coherence_gain)
    - During an episode, tracks a coherence proxy from sand-brain features and
      uses a sliding window to detect valley crossings with similar shape.
    - Returns a small bonus when a window matches (score-agnostic).
    """

    def __init__(self, csv_path: Path, bonus_scale: float = 1.0):
        self.enabled = False
        self.bonus_scale = bonus_scale

        if csv_path is None:
            print("[ValleyGuide] No CSV provided, disabling valley reward.")
            return

        if not csv_path.exists():
            print(f"[ValleyGuide] CSV not found at {csv_path}, disabling valley reward.")
            return

        try:
            df = pd.read_csv(csv_path)

            # Normalize boolean column if it's "TRUE"/"FALSE" strings
            if df["is_successful"].dtype == object:
                df["is_successful"] = (
                    df["is_successful"]
                    .astype(str)
                    .str.upper()
                    .map({"TRUE": True, "FALSE": False})
                )

            successful = df[df["is_successful"] == True].copy()

            if successful.empty:
                print("[ValleyGuide] No successful valleys found, disabling.")
                return

            # Duration band
            self.window_size = int(successful["duration"].median())  # ~40–50
            self.min_duration = int(successful["duration"].quantile(0.25))
            self.max_duration = int(successful["duration"].quantile(0.90))

            # Coherence shape
            self.min_drop = float(successful["coherence_drop"].quantile(0.25))
            self.max_drop = float(successful["coherence_drop"].quantile(0.90))

            # We want non-trivial reconstruction
            self.min_gain = float(successful["net_coherence_gain"].quantile(0.40))
            self.avg_gain = max(
                1e-6, float(successful["net_coherence_gain"].mean())
            )

            # How often we allow separate valleys to be counted
            self.min_steps_between = self.min_duration

            # Internal state for streaming coherence
            self.reset()

            print(
                f"[ValleyGuide] Loaded {len(successful)} successful valleys "
                f"(window≈{self.window_size}, "
                f"drop∈[{self.min_drop:.3f},{self.max_drop:.3f}], "
                f"net_gain≥{self.min_gain:.3f})"
            )
            self.enabled = True

        except Exception as e:
            print(f"[ValleyGuide] Failed to initialize: {e}")
            self.enabled = False

    # ---- lifecycle -------------------------------------------------

    def reset(self):
        """Reset per-episode state."""
        # Sliding buffer of (DR, coherence)
        self.buffer = deque(maxlen=getattr(self, "window_size", 64))
        self.t = 0
        self.last_valley_step = -1

        # Running stats for normalization / coherence proxy
        self.dr_min = None
        self.dr_max = None
        self.pi_min = None
        self.pi_max = None
        self.op_min = None
        self.op_max = None
        self.op_ema = None  # smoothed operator_norm for stability

    # ---- core functionality ----------------------------------------

    def _update_coherence(self, brain_full: Dict) -> float:
        """
        Approximate coherence online using the same ingredients as the
        offline valley detector: DR, pi, operator_norm.

        - DR_norm: high when DR is low
        - pi_norm: high when precision is high
        - op_stability: high when operator_norm is near its smoothed value
        """
        DR = float(brain_full["DR"])
        pi = float(brain_full["pi"])
        op = float(brain_full["operator_norm"])

        # Track ranges
        if self.dr_min is None:
            self.dr_min = self.dr_max = DR
            self.pi_min = self.pi_max = pi
            self.op_min = self.op_max = op
            self.op_ema = op
        else:
            self.dr_min = min(self.dr_min, DR)
            self.dr_max = max(self.dr_max, DR)
            self.pi_min = min(self.pi_min, pi)
            self.pi_max = max(self.pi_max, pi)
            self.op_min = min(self.op_min, op)
            self.op_max = max(self.op_max, op)
            # simple EMA for operator_norm
            self.op_ema = 0.99 * self.op_ema + 0.01 * op

        # Normalize
        dr_range = (self.dr_max - self.dr_min) + 1e-6
        pi_range = (self.pi_max - self.pi_min) + 1e-6
        op_range = (self.op_max - self.op_min) + 1e-6

        DR_norm = 1.0 - (DR - self.dr_min) / dr_range
        pi_norm = (pi - self.pi_min) / pi_range
        op_stability = 1.0 - abs(op - self.op_ema) / op_range

        # Bound for safety
        DR_norm = float(np.clip(DR_norm, 0.0, 1.0))
        pi_norm = float(np.clip(pi_norm, 0.0, 1.0))
        op_stability = float(np.clip(op_stability, 0.0, 1.0))

        # Same weighting structure as the offline proxy
        coherence = 0.5 * DR_norm + 0.3 * pi_norm + 0.2 * op_stability
        return coherence

    def step(self, brain_full: Dict) -> float:
        """
        Advance one timestep and return an intrinsic bonus if the most
        recent window looks like a successful valley crossing.

        Returns:
            valley_bonus (float), usually 0, occasionally >0 when a
            valley-shaped transition is detected.
        """
        if not self.enabled:
            return 0.0

        self.t += 1

        coherence = self._update_coherence(brain_full)
        DR = float(brain_full["DR"])

        # Update sliding window
        self.buffer.append((DR, coherence))
        if len(self.buffer) < self.window_size:
            return 0.0

        # Prevent double-counting overlapping windows
        if (
            self.last_valley_step >= 0
            and self.t - self.last_valley_step < self.min_steps_between
        ):
            return 0.0

        # Analyze current window
        drs, cohs = zip(*self.buffer)
        cohs = np.array(cohs, dtype=np.float32)

        # Duration: effectively fixed by buffer size, but we can still gate it
        duration = len(cohs)
        if duration < self.min_duration or duration > self.max_duration:
            return 0.0

        # Drop and net gain, relative to window start
        coh_start = float(cohs[0])
        coh_min = float(cohs.min())
        coh_end = float(cohs[-1])

        coherence_drop = coh_start - coh_min
        net_gain = coh_end - coh_start

        # Apply thresholds derived from successful_valleys
        if not (self.min_drop <= coherence_drop <= self.max_drop):
            return 0.0
        if net_gain < self.min_gain:
            return 0.0

        # We have a valley-like transition!
        self.last_valley_step = self.t

        # Reward magnitude scales with how strong the gain is relative
        # to the average successful valley
        gain_ratio = float(np.clip(net_gain / self.avg_gain, 0.1, 3.0))
        bonus = self.bonus_scale * gain_ratio

        return bonus


# =====================================================================
# §5: Runner (Single-Mode Episode Executor)
# =====================================================================

class SandHumanoidRunner:
    """
    Executes episodes in a specific reward mode.
    
    Modes:
    - pure: Environment reward only
    - touch: + ManifoldWell intrinsic
    - brain: + Sand brain intrinsic (low DR, high coherence)
    - fusion: Both intrinsics
    """
    
    def __init__(self, basin_json: Path, cfg: Config, mode: str = "pure"):
        self.cfg = cfg
        self.mode = mode
        
        # Environment
        env = gym.make(cfg.env_id, render_mode="human" if cfg.render else None)
        self.env = WindWrapper(env, cfg)
        
        obs_dim = self.env.observation_space.shape[0]
        act_dim = self.env.action_space.shape[0]
        
        # Sand brain
        self.brain = SandBrain(basin_json)
        brain_dim = self.brain.feature_dim
        
        # Valley guide (optional, score-agnostic intrinsic)
        self.valley_guide = None
        valley_csv = getattr(cfg, "valley_csv", None)
        if valley_csv is not None:
            try:
                self.valley_guide = SuccessfulValleyGuide(
                    valley_csv,
                    bonus_scale=cfg.valley_bonus_scale
                )
                print(f"[{mode}] Valley guide enabled from {valley_csv}")
            except Exception as e:
                print(f"[{mode}] Valley guide init failed: {e}")
                self.valley_guide = None


        # Policy
        self.policy = SandPolicyRecurrent(
            obs_dim, brain_dim, act_dim, 
            hidden_dim=256, action_scale=1.0
        ).to(cfg.device)
        
        self.optimizer = optim.Adam(self.policy.parameters(), lr=cfg.lr)
        
        # Manifold well (for 'touch' and 'fusion' modes)
        if mode in ["touch", "fusion"]:
            try:
                self.well = ManifoldWell(
                    action_dim=act_dim,
                    model_dir="./fractal_intelligence_transfer_models/"
                )
            except:
                print(f"Warning: ManifoldWell init failed for mode={mode}")
                self.well = None
        else:
            self.well = None
    
    def run_episode(self) -> dict:
        """
        Run one episode and return trajectory data.
        
        Returns dict with:
        - obs, actions, brain_features, hiddens: trajectory arrays
        - return: total environment return
        - brain: dict of brain metrics
        """
        obs, _ = self.env.reset()
        obs_t = torch.tensor(obs, dtype=torch.float32).unsqueeze(0).to(self.cfg.device)
        
        # Initialize hidden state
        h_t = torch.zeros(1, self.policy.hidden_dim).to(self.cfg.device)
        
        if self.valley_guide is not None:
            self.valley_guide.reset()

        # Storage
        obs_list, act_list, brain_list, hidden_list = [], [], [], []
        logp_list = []
        logp_list, reward_env_list, reward_touch_list, reward_brain_list = [], [], [], []
        reward_valley_list = []
        
        done = False
        step = 0
        
        while not done and step < self.cfg.max_steps:
            # Sample brain state
            _, brain_features, brain_full = self.brain.sample()
            brain_t = torch.tensor(brain_features, dtype=torch.float32).unsqueeze(0).to(self.cfg.device)
            
            # Valley-shaped intrinsic (score-agnostic)
            valley_bonus = 0.0
            if self.valley_guide is not None:
                valley_bonus = float(self.valley_guide.step(brain_full))

            # Select action
            with torch.no_grad():
                action_t, logp_t, h_next = self.policy.sample_action(obs_t, brain_t, h_t)
            
            action = action_t.cpu().numpy()[0]
            
            # Step environment
            obs_next, reward_env, terminated, truncated, info = self.env.step(action)
            done = terminated or truncated
            
            # Intrinsic rewards
            reward_touch = 0.0
            reward_brain = 0.0
            
            if self.mode in ["touch", "fusion"] and self.well is not None:
                self.well.step(step)
                reward_touch = self.well.get_reward(action)
            
            if self.mode in ["brain", "fusion"]:
                # Reward low DR and high coherence
                reward_brain = -brain_full["DR"] + 0.5 * brain_full["operator_norm"]
            
            # Store
            obs_list.append(obs)
            act_list.append(action)
            brain_list.append(brain_features)
            hidden_list.append(h_t.cpu().numpy()[0])
            logp_list.append(logp_t.item())
            reward_env_list.append(reward_env)
            reward_touch_list.append(reward_touch)
            reward_brain_list.append(reward_brain)
            reward_valley_list.append(valley_bonus)
            
            # Update
            obs = obs_next
            obs_t = torch.tensor(obs, dtype=torch.float32).unsqueeze(0).to(self.cfg.device)
            h_t = h_next
            step += 1
        
        # Compute returns
        R_env = sum(reward_env_list)
        R_touch = sum(reward_touch_list)
        R_brain = sum(reward_brain_list)
        R_valley = sum(reward_valley_list)

        # Composite return (for policy gradient)
        # Valley intrinsic is score-agnostic and always included (small weight)
        if self.mode == "pure":
            R_total = R_env + self.cfg.alpha_valley * R_valley
        elif self.mode == "touch":
            R_total = (
                R_env
                + self.cfg.alpha_touch * R_touch
                + self.cfg.alpha_valley * R_valley
            )
        elif self.mode == "brain":
            R_total = (
                R_env
                + self.cfg.alpha_brain * R_brain
                + self.cfg.alpha_valley * R_valley
            )
        else:  # fusion
            R_total = (
                R_env
                + self.cfg.alpha_touch * R_touch
                + self.cfg.alpha_brain * R_brain
                + self.cfg.alpha_valley * R_valley
            )
        
        return {
            "obs": np.array(obs_list),
            "actions": np.array(act_list),
            "brain_features": np.array(brain_list),
            "hiddens": np.array(hidden_list),
            "logprobs": np.array(logp_list),
            "return": R_env,  # Always report raw env return
            "return_total": R_total,
            "brain": {
                "DR": np.array([b[0] for b in brain_list]),
                "S": np.array([b[1] for b in brain_list]),
                "Gamma": np.array([b[2] for b in brain_list])
            },
            "valley_intrinsic": np.array(reward_valley_list),
        }
    
    def update(self, traj: dict) -> float:
        """Simple policy gradient update."""
        
        # --- 1. Get trajectory data (from rollout) ---
        obs = torch.tensor(traj["obs"], dtype=torch.float32).to(self.cfg.device)
        actions = torch.tensor(traj["actions"], dtype=torch.float32).to(self.cfg.device)
        brain = torch.tensor(traj["brain_features"], dtype=torch.float32).to(self.cfg.device)
        # hiddens[t] was the hidden state *used to* create action[t]
        hiddens = torch.tensor(traj["hiddens"], dtype=torch.float32).to(self.cfg.device)
        T = len(obs)

        # --- 2. Re-compute logprobs (to build the graph) ---
        # We must re-run the policy on the trajectory data
        # to get "live" logprobs with a gradient.
        logprobs_list = []
        for t in range(T):
            obs_t = obs[t].unsqueeze(0)
            brain_t = brain[t].unsqueeze(0)
            h_t = hiddens[t].unsqueeze(0)
            action_t = actions[t].unsqueeze(0)
            
            # Re-run the policy's forward pass
            mean, log_std, _ = self.policy.forward(obs_t, brain_t, h_t)
            std_t = torch.exp(log_std)
            
            # Inverse of tanh to get pre_tanh_t from action_t
            # This must match the math in `sample_action`
            pre_tanh_t = action_t / self.policy.action_scale
            pre_tanh_t = torch.clamp(pre_tanh_t, -1 + 1e-6, 1 - 1e-6) # avoid inf
            pre_tanh_t = torch.atanh(pre_tanh_t)
            
            # Inverse of sampling to get eps_t
            eps_t = (pre_tanh_t - mean) / std_t
            
            # Re-calculate the exact log_prob from sample_action
            log_prob_t = -0.5 * ((eps_t**2) + 2 * log_std + np.log(2 * np.pi))
            log_prob_t = log_prob_t.sum(dim=-1, keepdim=True)
            
            logprobs_list.append(log_prob_t)

        # `logprobs` is now a "live" tensor connected to the policy
        logprobs = torch.cat(logprobs_list).squeeze(1) # Shape [T]

        # --- 3. Use the original returns calculation ---
        # This calculation is unusual, but we'll preserve it.
        R = traj["return_total"]
        returns = torch.zeros(T, device=self.cfg.device)
        running = 0.0
        for t in reversed(range(T)):
            # Note: This is not a standard returns-to-go calculation,
            # but we preserve it as it was in your original code.
            running = traj["return_total"] / T + self.cfg.gamma * running
            returns[t] = running
        
        # --- 4. Policy gradient loss ---
        loss = -(logprobs * returns).mean()
        
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
        self.optimizer.step()
        
        return loss.item()


# =====================================================================
# §6: Hydra Orchestrator (Engram-Driven Multi-Mode Learning)
# =====================================================================

class HydraHumanoid:
    """
    Multi-mode orchestrator with engram-driven learning.
    
    Key insight: Each mode explores different regions of the (Γ, DR, S) space.
    Engrams capture successful attractors, and distillation transfers
    knowledge across modes via resonance.
    """
    
    def __init__(self, basin_json: Path, cfg: Config):
        self.cfg = cfg
        print(f"\n{'='*60}")
        print(f"Hydra Humanoid with Generative Engram Architecture")
        print(f"{'='*60}")
        print(f"Device: {cfg.device}")
        print(f"Engram capacity: {cfg.engram_capacity}")
        print(f"Distill every: {cfg.engram_distill_every} episodes")
        print(f"{'='*60}\n")
        
        # Create runners
        self.modes = ["pure", "touch", "brain", "fusion"]
        self.runners = {
            mode: SandHumanoidRunner(basin_json, cfg, mode=mode)
            for mode in self.modes
        }
        
        # NEW: valley reward engine
        v_cfg = ValleyRewardConfig(
            csv_path="successful_valleys.csv",
            reward_scale=0.3,        # start small
            min_window=30,
            max_window=120,
            use_hemispheric_only=False,
        )
        self.valley_reward = build_valley_reward(v_cfg)

        # Initialize all from same weights
        base_state = self.runners["pure"].policy.state_dict()
        for mode in self.modes:
            if mode != "pure":
                self.runners[mode].policy.load_state_dict(copy.deepcopy(base_state))
        
        # Global best tracking
        self.best_return = -1e9
        self.best_state = copy.deepcopy(base_state)
        self.no_improve = 0
        self.ep = 0
        
        # ENGRAM SYSTEM with RPA (INST-NALY-001)
        self.engram_library = EngramLibrary(capacity=cfg.engram_capacity)
        
        if cfg.rpa_enabled:
            self.engram_distiller = RPAWeightedDistiller(
                rpa_weight=cfg.rpa_weight,
                pareto_threshold=cfg.rpa_pareto_threshold,
                lr_scale=cfg.engram_lr_scale
            )
            print(f"✓ RPA-weighted distillation enabled (weight={cfg.rpa_weight}x)")
        else:
            self.engram_distiller = EngramDistiller(
                lr_scale=cfg.engram_lr_scale,
                coherence_weight=True
            )
        
        # Critical moment extractor (optional)
        if cfg.rpa_use_highlights:
            self.moment_extractor = CriticalMomentExtractor(
                pareto_threshold=cfg.rpa_pareto_threshold,
                context_window=5
            )
            print(f"✓ Highlight reel extraction enabled")
        else:
            self.moment_extractor = None
    
    def train(self):
        """Main training loop with periodic engram distillation."""
        
        while self.ep < self.cfg.episodes:
            
            # ENGRAM DISTILLATION (the key moment)
            if (self.ep > 0 and 
                self.ep % self.cfg.engram_distill_every == 0 and 
                len(self.engram_library) > 0):
                
                self._distill_engrams()
            
            # Run episodes in all modes
            for mode in self.modes:
                if self.ep >= self.cfg.episodes:
                    break
                
                self.ep += 1
                runner = self.runners[mode]
                
                # Sync to best global policy
                runner.policy.load_state_dict(copy.deepcopy(self.best_state))
                
                # Execute episode
                traj = runner.run_episode()
                loss = runner.update(traj)
                
                R_env = traj["return"]
                
                # Track global best
                if R_env > self.best_return:
                    self.best_return = R_env
                    self.best_state = copy.deepcopy(runner.policy.state_dict())
                    self.no_improve = 0
                    print(f"   ★ NEW PLATEAU: {self.best_return:.1f} (mode={mode})")
                else:
                    self.no_improve += 1
                
                # Add to engram library if worthy
                self._maybe_add_engram(traj, mode)
                
                # Log
                mean_DR = np.mean(traj["brain"]["DR"])
                mean_Gamma = np.mean(traj["brain"]["Gamma"])
                print(
                    f"[{mode:6s}] Ep {self.ep:04d} | "
                    f"R={R_env:7.1f} | Loss={loss:8.3f} | "
                    f"DR={mean_DR:.3f} | Γ={mean_Gamma:.3f} | "
                    f"Engrams={len(self.engram_library)}"
                )
                
                # Ratchet (plateau escape)
                if (self.ep > self.cfg.ratchet_start_ep and 
                    self.no_improve > self.cfg.ratchet_patience):
                    print(f"   ⚡ RATCHET: Reverting to best (R={self.best_return:.1f})")
                    self.no_improve = 0
        
        # Final report
        self._print_final_stats()
    
    def _maybe_add_engram(self, traj: dict, mode: str):
        """Add trajectory to engram library if it's valuable."""
        engram = EngramFactory.from_trajectory(
            obs=traj["obs"],
            actions=traj["actions"],
            brain_features=traj["brain_features"],
            hiddens=traj["hiddens"],
            return_raw=traj["return"],
            episode=self.ep
        )
        
        if self.engram_library.add(engram):
            print(f"   → Engram added: R={engram.return_raw:.1f}, "
                  f"Γ={engram.mean_gamma:.2f}, DR={engram.mean_DR:.2f}, "
                  f"coherence={engram.mean_coherence:.3f}")
    
    def _distill_engrams(self):
        """Transfer engram knowledge to best policy using RPA weighting."""
        print(f"\n{'='*60}")
        print(f"ENGRAM DISTILLATION @ Episode {self.ep}")
        if self.cfg.rpa_enabled:
            print(f"MODE: RPA-Weighted (Pareto {self.cfg.rpa_pareto_threshold:.0%})")
        print(f"{'='*60}")
        
        # Get best engrams
        engrams = self.engram_library.get_best(n=min(10, len(self.engram_library)))
        
        # Optional: Create highlight reels
        if self.moment_extractor:
            print(f"\nCreating highlight reels...")
            highlights = []
            for eng in engrams:
                highlight = self.moment_extractor.create_highlight_reel(eng)
                if highlight:
                    highlights.append(highlight)
                    compression = 1 - (highlight.length / eng.length)
                    print(f"  Engram ep={eng.origin_episode}: "
                          f"{eng.length} → {highlight.length} steps ({compression:.1%} compression)")
            
            if highlights:
                engrams = highlights
                print(f"✓ Using {len(highlights)} highlight reels for distillation")
        
        # Show what we're distilling
        print(f"\nDistilling {len(engrams)} engrams:")
        for i, eng in enumerate(engrams[:5]):  # Show top 5
            print(f"  {i+1}. R={eng.return_raw:.1f}, Γ={eng.mean_gamma:.2f}, "
                  f"DR={eng.mean_DR:.2f}, len={eng.length}")
        
        # Load best policy for distillation
        temp_policy = self.runners["pure"].policy
        temp_policy.load_state_dict(copy.deepcopy(self.best_state))
        temp_optimizer = self.runners["pure"].optimizer
        
        # Distill (RPA-weighted or standard)
        loss = self.engram_distiller.distill(
            policy=temp_policy,
            optimizer=temp_optimizer,
            engrams=engrams,
            n_steps=self.cfg.engram_distill_steps,
            device=self.cfg.device
        )
        
        # Update best policy
        self.best_state = copy.deepcopy(temp_policy.state_dict())
        self.no_improve = 0  # Reset patience
        
        print(f"✓ Policy updated with engram knowledge (loss={loss:.4f})")
        print(f"{'='*60}\n")
    
    def _print_final_stats(self):
        """Print final training statistics."""
        print(f"\n{'='*60}")
        print(f"TRAINING COMPLETE")
        print(f"{'='*60}")
        print(f"Best return: {self.best_return:.1f}")
        print(f"Total episodes: {self.ep}")
        
        stats = self.engram_library.stats()
        print(f"\nEngram Library Stats:")
        for k, v in stats.items():
            print(f"  {k}: {v:.2f}")
        
        print(f"\n{'='*60}\n")


# =====================================================================
# §7: CLI
# =====================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Sand Humanoid with Generative Engram Architecture"
    )
    parser.add_argument("--basin-json", type=Path, required=True,
                       help="Path to basin structure JSON")
    parser.add_argument("--engram-capacity", type=int, default=20,
                       help="Max engrams to store")
    parser.add_argument("--distill-every", type=int, default=100,
                       help="Distill engrams every N episodes")
    parser.add_argument("--valley-csv", type=Path, default=None,
                       help="Path to successful_valleys.csv for valley-shaped intrinsic reward")

    args = parser.parse_args()
    
    cfg = Config()
    cfg.engram_capacity = args.engram_capacity
    cfg.engram_distill_every = args.distill_every
    cfg.valley_csv = args.valley_csv
    
    hydra = HydraHumanoid(args.basin_json, cfg)
    hydra.train()


if __name__ == "__main__":
    main()
