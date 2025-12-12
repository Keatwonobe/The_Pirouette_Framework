#!/usr/bin/env python3

import argparse
from pathlib import Path
import copy
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# <--- ENGRAM: Import dataclass for trajectories ---
from dataclasses import dataclass
from typing import List
# --------------------------------------------------

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


# <--- ENGRAM: Dataclass to store good trajectories ---
# (Adapted from Skogsvatt_pendulum_3.py)
@dataclass
class Trajectory:
    obs: np.ndarray
    acts: np.ndarray
    brain_features: np.ndarray
    hiddens: np.ndarray
    R_raw: float
    origin_ep: int
# ----------------------------------------------------


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
    episodes = 2500 # (Increased episodes for HRL)
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

    # <--- ENGRAM: Settings from Skogsvatt_pendulum_3.py ---
    top_k = 10           # Max number of "engram" trajectories to store
    distill_every = 200  # Distill engrams into policy every N episodes
    distill_steps = 50   # Number of gradient steps for distillation
    distill_lr_scale = 0.1 # Temporarily reduce LR for stable cloning
    # --------------------------------------------------------


# =====================================================================
# Wind Wrapper for Humanoid
# =====================================================================

try:
    from gymnasium import spaces
except ImportError:
    from gym import spaces

class WindyHumanoid(gym.Wrapper):
    """ Applies random lateral 'wind' forces to the Humanoid torso. """
    def __init__(self, env, cfg: Config):
        super().__init__(env)
        self.cfg = cfg
        self.mj_env = env.unwrapped
        self.model = getattr(self.mj_env, "model", None)
        self.data = getattr(self.mj_env, "data", None)
        self.body_name = getattr(cfg, "wind_body", "torso")
        self.body_id = None
        if self.model is not None:
            try:
                self.body_id = self.model.body_name2id(self.body_name)
            except Exception:
                self.body_id = 1
        self._step_count = 0
        self._remaining_wind = 0
        self._current_wind = np.zeros(3, dtype=np.float32)

    def _apply_wind_force(self):
        if self.data is None or self.body_id is None: return
        self.data.xfrc_applied[:] = 0.0
        self.data.xfrc_applied[self.body_id, 0:3] = self._current_wind

    def _maybe_update_wind(self):
        if self._remaining_wind > 0:
            self._remaining_wind -= 1
            if self._remaining_wind == 0: self._current_wind[:] = 0.0
            return
        if (self._step_count >= self.cfg.wind_start_step and 
            np.random.rand() < self.cfg.wind_prob):
            mag = np.random.uniform(self.cfg.wind_force_min, self.cfg.wind_force_max)
            theta = np.random.uniform(0.0, 2.0 * np.pi)
            self._current_wind[:] = np.array([mag * np.cos(theta), mag * np.sin(theta), 0.0], dtype=np.float32)
            self._remaining_wind = np.random.randint(self.cfg.wind_min_duration, self.cfg.wind_max_duration + 1)

    def reset(self, **kwargs):
        self._step_count = 0
        self._remaining_wind = 0
        self._current_wind[:] = 0.0
        result = self.env.reset(**kwargs)
        obs, info = result if isinstance(result, tuple) and len(result) == 2 else (result, {})
        self._apply_wind_force()
        return obs, info

    def step(self, action):
        self._step_count += 1
        if self.cfg.wind_enabled:
            self._maybe_update_wind()
            self._apply_wind_force()
        else:
            self._current_wind[:] = 0.0
            self._apply_wind_force()
        obs, reward, terminated, truncated, info = self.env.step(action)
        return obs, reward, terminated, truncated, info


# =====================================================================
# Humanoid Runner (Worker for Hydra)
# =====================================================================

class SandHumanoidRunner:
    def __init__(self, basin_json: Path, cfg=Config(), mode: str = "pure"):
        self.cfg = cfg
        self.mode = mode 
        self.env = gym.make(cfg.env_id)
        if getattr(cfg, "wind_enabled", False):
            self.env = WindyHumanoid(self.env, cfg)
        self.device = torch.device(cfg.device)

        obs_dim = int(np.prod(self.env.observation_space.shape))
        act_dim = int(np.prod(self.env.action_space.shape))
        act_scale = float(self.env.action_space.high[0])

        self.brain = SandBrain(basin_json)
        brain_dim = self.brain.feature_dim

        # <--- Use Recurrent Policy ---
        self.hidden_dim = 256  # Agent's memory size
        self.policy = SandPolicyRecurrent(
            obs_dim=obs_dim,
            brain_dim=brain_dim,
            action_dim=act_dim,
            hidden_dim=self.hidden_dim,
            action_scale=act_scale,
        ).to(self.device)
        # ----------------------------

        self.optimizer = optim.Adam(self.policy.parameters(), lr=cfg.lr)
        self.manifold = ManifoldWell(action_dim=act_dim, max_steps=cfg.max_steps)

    def run_episode(self):
        """
        Runs one episode, storing all data for REINFORCE and Engram buffer.
        """
        obs, _ = self.env.reset()
        obs = obs.astype(np.float32)

        log_probs_list = []
        rewards_list = []      
        env_rewards_list = []  
        brain_log = {"DR": [], "S": [], "Gamma": [], "pi": [], "operator_norm": []}
        obs_list = []
        actions_list = []
        brain_features_list = []
        hiddens_list = [] 
        
        previous_DR = None 

        # --- Brain is sampled ONCE, held constant ---
        _, brain_feat, sample = self.brain.sample()
        brain_t = torch.as_tensor(brain_feat, dtype=torch.float32, device=self.device).unsqueeze(0)
        
        for k in brain_log:
            if k in sample:
                brain_log[k].append(float(sample[k]))
        DR_t = float(sample["DR"]) 

        # --- Initialize the "core rhythm" (hidden state) ---
        h_t = torch.zeros((1, self.hidden_dim), dtype=torch.float32, device=self.device)

        for t in range(self.cfg.max_steps):
            if self.cfg.render:
                self.env.render()

            # --- 1) Store states for this step ---
            obs_list.append(obs.copy())
            brain_features_list.append(brain_feat.copy())
            hiddens_list.append(h_t.cpu().numpy()) 
            
            # --- 2) Policy forward (Recurrent) ---
            obs_t = torch.as_tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
            
            with torch.no_grad():
                action_t, logp_t, h_next = self.policy.sample_action(obs_t, brain_t, h_t) 

            h_t = h_next # Update rhythm for next step
            
            action = action_t.cpu().numpy()[0]
            actions_list.append(action.copy())
            log_probs_list.append(logp_t)

            # --- 3) Env step ---
            next_obs, r_env, term, trunc, _ = self.env.step(action)
            env_rewards_list.append(float(r_env))

            # --- 4) Intrinsic rewards (Hydra heads) ---
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
            total_reward = (
                float(r_env)
                + self.cfg.alpha_touch * r_touch
                + self.cfg.alpha_brain * r_brain
            )
            rewards_list.append(total_reward) 
            
            obs = next_obs.astype(np.float32)
            if term or trunc:
                break

        return {
            "log_probs": torch.cat(log_probs_list),
            "rewards": rewards_list,         
            "brain": brain_log,
            "return": sum(env_rewards_list), 
            "obs": np.array(obs_list),
            "actions": np.array(actions_list),
            "brain_features": np.array(brain_features_list),
            "hiddens": np.array(hiddens_list),
        }

    def update(self, traj):
        """
        REINFORCE update, modified for recurrence.
        """
        rewards = traj["rewards"]
        actions = traj["actions"]
        obs = traj["obs"]
        brain = traj["brain_features"]
        hiddens = traj["hiddens"]

        T = len(rewards)

        # ---- 1. Calculate Returns (G_t) (no grad) ----
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
        hiddens_t = torch.as_tensor(hiddens, dtype=torch.float32, device=self.device).squeeze(1)

        log_probs_list = []
        h_step = hiddens_t[0].unsqueeze(0) # <-- (1, H)
        
        for t in range(T):
            obs_step = obs_t[t].unsqueeze(0)
            brain_step = brain_t[t].unsqueeze(0)
            act_step = acts_t[t].unsqueeze(0)
            
            mean, log_std, h_next = self.policy.forward(obs_step, brain_step, h_step)
            
            std = torch.exp(log_std)
            dist = torch.distributions.Normal(mean, std)
            logp_step = dist.log_prob(act_step).sum(dim=-1, keepdim=True)
            
            log_probs_list.append(logp_step)
            h_step = h_next 
            
        log_probs = torch.cat(log_probs_list) # (T, 1)

        # ---- 3. REINFORCE loss ----
        loss = -(log_probs * returns_t).sum()

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 1.0)
        self.optimizer.step()

        return loss.item()


# <--- ENGRAM: Distillation Function ---
# (Adapted from Skogsvatt_pendulum_3.py)
def distill_engrams_humanoid(
    policy: SandPolicyRecurrent,
    optimizer: optim.Optimizer,
    engram_buffer: List[Trajectory],
    cfg: Config
):
    """
    Behavioral cloning: distill top-K trajectories into the policy.
    This version is adapted for the recurrent policy.
    """
    if not engram_buffer:
        return 0.0

    # 1. Collate all (obs, brain, act) steps from all engrams
    obs_list = []
    brain_list = []
    act_list = []
    hiddens_list = [] # We need the *initial* hidden state for each traj
    
    for traj in engram_buffer:
        obs_list.append(torch.as_tensor(traj.obs, dtype=torch.float32))
        brain_list.append(torch.as_tensor(traj.brain_features, dtype=torch.float32))
        act_list.append(torch.as_tensor(traj.acts, dtype=torch.float32))
        # Get h_0 for this trajectory: (1, H) -> (H,)
        hiddens_list.append(torch.as_tensor(traj.hiddens[0], dtype=torch.float32).squeeze(0))

    # Pad sequences to max length T in this batch
    obs_batch = nn.utils.rnn.pad_sequence(obs_list, batch_first=True).to(cfg.device)
    brain_batch = nn.utils.rnn.pad_sequence(brain_list, batch_first=True).to(cfg.device)
    act_batch = nn.utils.rnn.pad_sequence(act_list, batch_first=True).to(cfg.device)
    
    # (B, H)
    h_0_batch = torch.stack(hiddens_list).to(cfg.device)
    
    B, T, _ = obs_batch.shape # Batch size, Max Trajectory Length

    # 2. Reduce LR temporarily for engram tuning
    orig_lrs = [g["lr"] for g in optimizer.param_groups]
    for g in optimizer.param_groups:
        g["lr"] *= cfg.distill_lr_scale

    # 3. Run gradient descent
    print(f"[DISTILL] Cloning {B} engrams over {T} steps...")
    for i in range(cfg.distill_steps):
        
        # We must unroll the RNN step-by-step
        h_step = h_0_batch # (B, H)
        total_bc_loss = 0.0
        
        for t in range(T):
            obs_step = obs_batch[:, t, :]   # (B, obs_dim)
            brain_step = brain_batch[:, t, :] # (B, brain_dim)
            act_step = act_batch[:, t, :]   # (B, act_dim)
            
            mu, _, h_next = policy.forward(obs_step, brain_step, h_step)
            pred = torch.tanh(mu)  # mean-based deterministic intent
            
            # Masked loss (don't penalize for padding)
            # We assume actions are non-zero, so 0.0 act_mag = padding
            act_mag = torch.abs(act_step).sum(dim=-1)
            mask = (act_mag > 1e-5).float()
            
            loss_t = ((pred - act_step) ** 2).mean(dim=-1)
            masked_loss_t = (loss_t * mask).sum() / mask.sum().clamp(min=1.0)
            
            total_bc_loss = total_bc_loss + masked_loss_t
            h_step = h_next
        
        bc_loss = total_bc_loss / T # Average loss over time

        optimizer.zero_grad()
        bc_loss.backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), max_norm=0.5)
        optimizer.step()
        
        if i % 10 == 0:
            print(f"  [DISTILL] step {i:02d}, BC_loss={bc_loss.item():.4f}")

    # 4. Restore LR
    for g, lr in zip(optimizer.param_groups, orig_lrs):
        g["lr"] = lr
        
    return bc_loss.item()
# ----------------------------------------------------


# =====================================================================
# 5. Hydra Orchestrator (with Engram Distillation)
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
        
        # <--- ENGRAM: Global buffer for best trajectories ---
        self.engram_buffer: List[Trajectory] = []
        # ---------------------------------------------------

    def train(self):
        while self.ep < self.cfg.episodes:
            
            # <--- ENGRAM: Periodic distillation step ---
            if (self.ep > 0 and 
                self.ep % self.cfg.distill_every == 0 and 
                self.engram_buffer):
                
                print(f"\n{'='*60}")
                print(f"[HYDRA-DISTILL] Ep {self.ep}: Distilling {len(self.engram_buffer)} engrams into BEST policy.")
                
                # Load best policy into a temp model for updating
                # We use 'pure' runner as a template for policy/optimizer
                temp_policy = self.runners["pure"].policy
                temp_policy.load_state_dict(self.best_state)
                temp_optimizer = self.runners["pure"].optimizer
                
                # Run the distillation (behavioral cloning)
                distill_loss = distill_engrams_humanoid(
                    temp_policy,
                    temp_optimizer,
                    self.engram_buffer,
                    self.cfg
                )
                
                # Save the newly-distilled policy as the new best
                self.best_state = copy.deepcopy(temp_policy.state_dict())
                print(f"[HYDRA-DISTILL] Best policy updated with engram knowledge. BC_Loss={distill_loss:.4f}")
                print(f"{'='*60}\n")
                
                # Reset ratchet, since we've "staircased"
                self.no_improve = 0
            # --------------------------------------------

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
                
                # --- Global Plateau Tracking ---
                if R_env > self.best_return:
                    self.best_return = R_env
                    # Store the new best state from *this* runner
                    self.best_state = copy.deepcopy(runner.policy.state_dict())
                    self.no_improve = 0
                    print(f"   ↳ [Hydra] New global plateau: {self.best_return:.1f} (mode={mode})")
                else:
                    self.no_improve += 1
                    
                # <--- ENGRAM: Add high-scoring trajectories to buffer ---
                if (len(self.engram_buffer) < self.cfg.top_k or 
                    R_env > self.engram_buffer[-1].R_raw):
                    
                    new_traj = Trajectory(
                        obs=traj["obs"],
                        acts=traj["actions"],
                        brain_features=traj["brain_features"],
                        hiddens=traj["hiddens"],
                        R_raw=R_env,
                        origin_ep=self.ep
                    )
                    self.engram_buffer.append(new_traj)
                    self.engram_buffer.sort(key=lambda t: t.R_raw, reverse=True)
                    self.engram_buffer = self.engram_buffer[:self.cfg.top_k]
                    print(f"   ↳ [Engram] New Top-K trajectory saved (R={R_env:.1f}). Buffer size: {len(self.engram_buffer)}")
                # --------------------------------------------------------

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