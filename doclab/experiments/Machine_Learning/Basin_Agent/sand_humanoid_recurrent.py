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

# =====================================================================
# Policy Network (Recurrent)
# =====================================================================

class SandPolicyRecurrent(nn.Module):
    """
    Recurrent Gaussian policy for Humanoid, with sand-brain gating
    and a GRU cell to act as the "Ki" core rhythm.
    """

    def __init__(
        self,
        obs_dim,
        brain_dim,
        action_dim,
        hidden_dim=256, # <-- Dimension of the core rhythm (Ki)
        action_scale=1.0,
    ):
        super().__init__()
        self.action_dim = action_dim
        self.action_scale = action_scale
        self.hidden_dim = hidden_dim

        inp_dim = obs_dim + brain_dim
        
        # Input layer
        self.input_layer = nn.Linear(inp_dim, hidden_dim)
        
        # The "Ki" or "Core Rhythm"
        # We use a GRUCell for explicit step-by-step state management
        self.gru_cell = nn.GRUCell(hidden_dim, hidden_dim) 
        
        # Output layer
        self.output_layer = nn.Linear(hidden_dim, 2 * action_dim)

        # Encourage stable early behavior (narrower std)
        with torch.no_grad():
            self.output_layer.bias[action_dim:].fill_(-1.0)

    def forward(self, obs, brain, h_in):
        """
        Performs one step of the recurrent policy.
        - obs: (B, obs_dim)
        - brain: (B, brain_dim)
        - h_in: (B, hidden_dim)
        """
        # 1. Combine inputs and pass through input layer
        x = torch.cat([obs, brain], dim=-1)
        x = torch.tanh(self.input_layer(x)) # (B, hidden_dim)
        
        # 2. Update the "core rhythm" (hidden state)
        h_out = self.gru_cell(x, h_in) # (B, hidden_dim)
        
        # 3. Generate action parameters from the new rhythm
        out = self.output_layer(h_out)
        mean, log_std = torch.chunk(out, 2, dim=-1)
        log_std = torch.clamp(log_std, -5.0, 1.0)
        
        return mean, log_std, h_out

    def sample_action(self, obs, brain, h_in):
        """
        Samples an action for one step, given the current state.
        - obs: (1, obs_dim)
        - brain: (1, brain_dim)
        - h_in: (1, hidden_dim)
        """
        # Get parameters and new hidden state from the forward pass
        mean, log_std, h_out = self.forward(obs, brain, h_in)
        
        std = torch.exp(log_std)
        eps = torch.randn_like(mean)
        pre_tanh = mean + std * eps
        action = torch.tanh(pre_tanh) * self.action_scale

        # Calculate log_prob
        log_prob = -0.5 * ((eps**2) + 2 * log_std + np.log(2 * np.pi))
        log_prob = log_prob.sum(dim=-1, keepdim=True)
        
        return action, log_prob, h_out # h_out is (1, hidden_dim)


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
    ratchet_patience = 49       # (Global ratchet patience)

    # --- Wind / disturbance settings ---
    wind_enabled = True          # master switch
    wind_force_min = 40.0        # lower bound on gust magnitude (N)
    wind_force_max = 120.0       # upper bound on gust magnitude (N)
    wind_prob = 0.12             # chance per step to *start* a new gust
    wind_min_duration = 15       # steps
    wind_max_duration = 80       # steps
    wind_start_step = 50         # don’t gust in the first few steps
    wind_body = "torso"          # body name to push on (Humanoid uses "torso")


# =====================================================================
# Humanoid Runner (Worker for Hydra)
# =====================================================================
# =====================================================================
# Wind Wrapper for Humanoid (Random Lateral Gusts)
# =====================================================================

try:
    from gymnasium import spaces
except ImportError:
    from gym import spaces


class WindyHumanoid(gym.Wrapper):
    """
    Applies random lateral 'wind' forces to the Humanoid torso.

    - Does not change the action space.
    - Does not change the reward directly.
    - Uses MuJoCo's xfrc_applied to push the torso horizontally.
    """

    def __init__(self, env, cfg: Config):
        super().__init__(env)
        self.cfg = cfg

        # Access underlying mujoco env
        self.mj_env = env.unwrapped
        self.model = getattr(self.mj_env, "model", None)
        self.data = getattr(self.mj_env, "data", None)

        # Body to push
        self.body_name = getattr(cfg, "wind_body", "torso")
        self.body_id = None
        if self.model is not None:
            try:
                self.body_id = self.model.body_name2id(self.body_name)
            except Exception:
                # Fallback: just pick body 1 if lookup fails
                self.body_id = 1

        # Internal state
        self._step_count = 0
        self._remaining_wind = 0
        self._current_wind = np.zeros(3, dtype=np.float32)  # (fx, fy, fz)

    # Utility: apply current wind force to the chosen body
    def _apply_wind_force(self):
        if self.data is None or self.body_id is None:
            return

        # Clear all forces first
        self.data.xfrc_applied[:] = 0.0
        # Apply only lateral forces (x, y); z left as 0
        self.data.xfrc_applied[self.body_id, 0:3] = self._current_wind

    # Utility: maybe start/stop a gust
    def _maybe_update_wind(self):
        # If currently in a gust, decrement countdown
        if self._remaining_wind > 0:
            self._remaining_wind -= 1
            if self._remaining_wind == 0:
                # Gust ends
                self._current_wind[:] = 0.0
            return

        # No gust right now: maybe start a new one
        if (
            self._step_count >= self.cfg.wind_start_step
            and np.random.rand() < self.cfg.wind_prob
        ):
            # Sample magnitude
            mag = np.random.uniform(
                self.cfg.wind_force_min, self.cfg.wind_force_max
            )

            # Sample random horizontal direction
            theta = np.random.uniform(0.0, 2.0 * np.pi)
            fx = mag * np.cos(theta)
            fy = mag * np.sin(theta)

            self._current_wind[:] = np.array([fx, fy, 0.0], dtype=np.float32)
            self._remaining_wind = np.random.randint(
                self.cfg.wind_min_duration,
                self.cfg.wind_max_duration + 1,
            )

    def reset(self, **kwargs):
        self._step_count = 0
        self._remaining_wind = 0
        self._current_wind[:] = 0.0

        result = self.env.reset(**kwargs)
        # Normalize to gymnasium-style (obs, info)
        if isinstance(result, tuple) and len(result) == 2:
            obs, info = result
        else:
            obs, info = result, {}

        # Ensure no residual force on reset
        self._apply_wind_force()
        return obs, info

    def step(self, action):
        self._step_count += 1

        if self.cfg.wind_enabled:
            self._maybe_update_wind()
            self._apply_wind_force()
        else:
            # Ensure forces are zeroed if wind disabled mid-run
            self._current_wind[:] = 0.0
            self._apply_wind_force()

        obs, reward, terminated, truncated, info = self.env.step(action)
        return obs, reward, terminated, truncated, info



class SandHumanoidRunner:
    def __init__(self, basin_json: Path, cfg=Config(), mode: str = "pure"):
        self.cfg = cfg
        self.mode = mode # <-- 4.2: Store the mode
        self.env = gym.make(cfg.env_id)
        # Wrap with wind disturbances if enabled
        if getattr(cfg, "wind_enabled", False):
            self.env = WindyHumanoid(self.env, cfg)
        self.device = torch.device(cfg.device)

        obs_dim = int(np.prod(self.env.observation_space.shape))
        act_dim = int(np.prod(self.env.action_space.shape))
        act_scale = float(self.env.action_space.high[0])

        self.brain = SandBrain(basin_json)
        brain_dim = self.brain.feature_dim

        self.hidden_dim = 256  # <-- Define the agent's memory size
        self.policy = SandPolicyRecurrent(
            obs_dim=obs_dim,
            brain_dim=brain_dim,
            action_dim=act_dim,
            hidden_dim=self.hidden_dim,
            action_scale=act_scale,
        ).to(self.device)

        self.optimizer = optim.Adam(self.policy.parameters(), lr=cfg.lr)

        # --- 4.2: ManifoldWell "sense of touch" ---
        self.manifold = ManifoldWell(action_dim=act_dim, max_steps=cfg.max_steps)

        # (Old ratchet state is removed, Hydra class handles it)

    # --------------------------------------------------------------
# --------------------------------------------------------------
    def run_episode(self):
        """
        Runs one episode using the runner's mode to calculate hybrid rewards.
        
        [MODIFIED FOR RECURRENCE]
        - Brain state is held constant (from previous fix).
        - Policy hidden state (Ki) is initialized and propagated step-by-step.
        """
        obs, _ = self.env.reset()
        obs = obs.astype(np.float32)

        log_probs = []
        rewards = []      
        env_rewards = []  
        
        brain_log = {"DR": [], "S": [], "Gamma": [], "pi": [], "operator_norm": []}

        observations = []
        actions = []
        brain_features = []
        hiddens = [] # <-- NEW: To store the hidden states
        
        previous_DR = None 

        # <--- CHANGE 1: Get persistent brain state (from previous fix) ---
        _, brain_feat, sample = self.brain.sample()
        # (1, brain_dim)
        brain_t = torch.as_tensor(brain_feat, dtype=torch.float32, device=self.device).unsqueeze(0)
        
        for k in brain_log:
            if k in sample:
                brain_log[k].append(float(sample[k]))
        
        DR_t = float(sample["DR"]) 

        # <--- NEW: Initialize the "core rhythm" (hidden state) ---
        # (1, hidden_dim)
        h_t = torch.zeros((1, self.hidden_dim), dtype=torch.float32, device=self.device)

        for t in range(self.cfg.max_steps):
            if self.cfg.render:
                self.env.render()

            # --- 1) Store states ---
            observations.append(obs.copy())
            brain_features.append(brain_feat.copy()) # Store persistent brain features
            hiddens.append(h_t.cpu().numpy()) # <-- NEW: Store current hidden state
            
            # --- 2) Policy forward ---
            # (1, obs_dim)
            obs_t = torch.as_tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
            
            with torch.no_grad():
                # <-- NEW: Pass h_t in, get h_next out -->
                action_t, logp_t, h_next = self.policy.sample_action(obs_t, brain_t, h_t) 

            h_t = h_next # <-- NEW: Update rhythm for next step
            
            action = action_t.cpu().numpy()[0]
            actions.append(action.copy())
            log_probs.append(logp_t)

            # --- 3) Env step ---
            next_obs, r_env, term, trunc, _ = self.env.step(action)
            env_rewards.append(float(r_env))

            # --- 4) Intrinsic rewards (Hydra heads) ---
            # (This section remains unchanged)
            r_touch = 0.0
            r_brain = 0.0
            if self.mode in ("touch", "fusion"):
                self.manifold.step(t)
                r_touch = self.manifold.get_reward(action)
            if self.mode in ("brain", "fusion"):
                if previous_DR is not None:
                    dDR = DR_t - previous_DR 
                    r_brain = max(0.0, -dDR) 
                previous_DR = DR_t 
 
            # --- 5) Combine ---
            # (This section remains unchanged)
            total_reward = (
                float(r_env)
                + self.cfg.alpha_touch * r_touch
                + self.cfg.alpha_brain * r_brain
            )

            rewards.append(total_reward) 
            obs = next_obs.astype(np.float32)

            if term or trunc:
                break

        return {
            "log_probs": torch.cat(log_probs),
            "rewards": rewards,         
            "brain": brain_log,
            "return": sum(env_rewards), 
            "obs": np.array(observations),
            "actions": np.array(actions),
            "brain_features": np.array(brain_features),
            "hiddens": np.array(hiddens), # <-- NEW: Pass hiddens to update
        }

    # --------------------------------------------------------------
    def update(self, traj):
        """
        [MODIFIED FOR RECURRENCE]
        Performs a REINFORCE update by re-calculating log_probs
        step-by-step to correctly propagate recurrent gradients.
        
        [FIXED BATCH_SIZE BUG]
        """
        rewards = traj["rewards"]
        actions = traj["actions"]
        obs = traj["obs"]
        brain = traj["brain_features"]
        hiddens = traj["hiddens"] # <-- NEW: Get saved hidden states

        T = len(rewards)

        # ---- 1. Calculate Returns (G_t) (no grad) ----
        # (This section is unchanged)
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

        # ---- 2. Recompute log_probs on-graph (RECURRENT) ----
        obs_t = torch.as_tensor(obs, dtype=torch.float32, device=self.device)
        brain_t = torch.as_tensor(brain, dtype=torch.float32, device=self.device)
        acts_t = torch.as_tensor(actions, dtype=torch.float32, device=self.device)
        
        # (T, 1, H) -> (T, H)
        hiddens_t = torch.as_tensor(hiddens, dtype=torch.float32, device=self.device).squeeze(1)

        log_probs_list = []
        
        # <--- THIS IS THE FIX ---
        # Get the *very first* hidden state for the sequence
        # Shape must be (1, H), not (H,)
        h_step = hiddens_t[0].unsqueeze(0) 
        # <--- END FIX ---
        
        # Loop through the trajectory step-by-step
        for t in range(T):
            # Get data for this step: (1, dim)
            obs_step = obs_t[t].unsqueeze(0)
            brain_step = brain_t[t].unsqueeze(0)
            act_step = acts_t[t].unsqueeze(0)
            
            # Re-run the policy's forward pass, one step at a time
            # This rebuilds the computational graph
            mean, log_std, h_next = self.policy.forward(obs_step, brain_step, h_step)
            
            # Re-calculate log_prob from the new distribution
            std = torch.exp(log_std)
            dist = torch.distributions.Normal(mean, std)
            logp_step = dist.log_prob(act_step).sum(dim=-1, keepdim=True)
            
            log_probs_list.append(logp_step)
            
            # Propagate the hidden state
            h_step = h_next 
            
        log_probs = torch.cat(log_probs_list) # (T, 1)

        # ---- 3. REINFORCE loss ----
        # (This section is unchanged)
        loss = -(log_probs * returns_t).sum()

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 1.0)
        self.optimizer.step()

        return loss.item()


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