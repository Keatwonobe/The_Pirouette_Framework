"""
Pirouette PRG‑Regularized RL for MuJoCo (PyTorch, v2.1 - Corrected)

Core idea:
  Reward' = env_reward
            + wK * K_tau
            - wG * V_Gamma
            - wBeat * prg_penalty

Where K_τ, V_Γ, τ_p are estimated online from recent trajectory windows,
implementing the principles of CORE-015: The Predictive Fractal.
"""

from dataclasses import dataclass
from typing import Tuple, Dict
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import gymnasium as gym

# ---------------------
# Utilities
# ---------------------

def mlp(sizes, act=nn.Tanh, out_act=nn.Identity):
    """Creates a simple multi-layer perceptron."""
    layers = []
    for i in range(len(sizes)-1):
        layers += [nn.Linear(sizes[i], sizes[i+1]), act() if i < len(sizes)-2 else out_act()]
    return nn.Sequential(*layers)

# ---------------------
# World model for K_tau (Coherence as Predictability/Compressibility)
# ---------------------

class WorldModel(nn.Module):
    """
    A small autoregressive model over (obs, action) -> next obs.
    K_tau is proxied by the model's ability to predict the future, representing
    the compressibility of the agent's experience. A predictable, coherent
    trajectory is a compressible one.
    """
    def __init__(self, obs_dim, act_dim, hid=64):
        super().__init__()
        self.net = mlp([obs_dim + act_dim, hid, hid, obs_dim])

    def forward(self, obs, act):
        x = torch.cat([obs, act], dim=-1)
        return self.net(x)

    @torch.no_grad()
    def k_tau(self, obs_seq, act_seq, eps=1e-8):
        """
        Calculates the coherence gain K_τ.
        obs_seq: [T, obs_dim], act_seq: [T, act_dim]
        """
        # Ensure sequences are long enough
        if obs_seq.shape[0] <= 1:
            return 0.0

        pred = self.forward(obs_seq[:-1], act_seq[:-1])
        target = obs_seq[1:]
        
        mse_model = F.mse_loss(pred, target)
        
        # Baseline: naive persistence (predicting the last state doesn't change)
        mse_base = F.mse_loss(obs_seq[:-1], target)
        
        gain = (mse_base - mse_model).clamp(min=0.0)
        denom = (mse_base + eps)
        
        # K_τ is the normalized predictability gain
        return (gain / denom).item()

# ---------------------
# Pressure V_Gamma (Residual Volatility / Exogenous Drive)
# ---------------------

def v_gamma(obs_seq, act_seq):
    """
    Estimates pressure as the variance of residuals unexplained by a simple
    linear model. High variance implies a chaotic, high-pressure environment.
    """
    if obs_seq.shape[0] <= 1:
        return 0.0
        
    x = obs_seq[:-1]
    y = obs_seq[1:]
    actions = act_seq[:-1]
    
    # Simple linear regression: y ≈ A*x + B*a
    X = torch.cat([x, actions, torch.ones_like(x[:, :1])], dim=-1)
    
    try:
        # Use torch.linalg.lstsq for modern PyTorch
        solution = torch.linalg.lstsq(X, y).solution
        y_hat = X @ solution
        resid = y - y_hat
        return resid.var().item()
    except torch.linalg.LinAlgError:
        # Handle cases where the matrix is singular
        return 0.0


# ---------------------
# Beat τ_p via Short-Time Spectrum
# ---------------------

def tau_p(obs_seq, samp_rate=50.0, fmin=0.5, fmax=10.0):
    """
    Estimates the dominant period (τ_p) of the agent's motion using FFT.
    We look at the first dimension of observation space (e.g., torso height in Hopper).
    """
    if obs_seq.shape[0] < 10: # Need enough data for a meaningful FFT
        return float('inf')

    # Select a meaningful channel for rhythm analysis (e.g., Hopper's torso height)
    x = obs_seq[:, 0]
    x = x - x.mean()
    
    # FFT over the time window
    X = torch.fft.rfft(x)
    freqs = torch.fft.rfftfreq(x.size(0), d=1.0/samp_rate)
    
    # Band-limit to plausible motion frequencies
    mask = (freqs >= fmin) & (freqs <= fmax)
    if not torch.any(mask):
        return float('inf')
        
    mag = X.abs()[mask]
    
    if len(mag) == 0:
        return float('inf')
        
    peak_idx = torch.argmax(mag)
    f0 = freqs[mask][peak_idx].item()
    
    return float('inf') if f0 <= 1e-6 else 1.0 / f0

# ---------------------
# PRG Penalty
# ---------------------

def prg_penalty(K, V, tau, prev_tau, zeta_G=0.1, zeta_K=0.1, ds=1.0):
    """
    Calculates the penalty for deviating from the PRG's predicted beat scaling.
    This enforces the fractal consistency proposed in CORE-015.
    """
    if math.isinf(tau) or math.isinf(prev_tau) or prev_tau == 0:
        return 0.0
        
    # Approximate ∂_s ln(τ_p) with finite differences
    d_s_log_tau = (math.log(tau) - math.log(prev_tau)) / ds
    
    # The PRG's prediction for how the beat should scale
    target_scaling = zeta_G * V - zeta_K * K
    
    return (d_s_log_tau - target_scaling) ** 2

# ---------------------
# Actor-Critic Agent (PPO)
# ---------------------

class ActorCritic(nn.Module):
    def __init__(self, obs_dim, act_dim, hid=64):
        super().__init__()
        self.pi_net = mlp([obs_dim, hid, hid, act_dim], act=nn.Tanh, out_act=nn.Tanh)
        self.v_net  = mlp([obs_dim, hid, hid, 1], act=nn.Tanh, out_act=nn.Identity)
        log_std = -0.5 * np.ones(act_dim, dtype=np.float32)
        self.log_std = nn.Parameter(torch.as_tensor(log_std))

    def step(self, obs):
        """Take a step in the environment."""
        mu = self.pi_net(obs)
        std = torch.exp(self.log_std)
        dist = torch.distributions.Normal(mu, std)
        
        a = dist.sample()
        logp_a = dist.log_prob(a).sum(axis=-1)
        v = self.v_net(obs).squeeze(-1)
        
        # --- FIX #1: Detach tensors from the computation graph before converting to numpy ---
        return a.cpu().detach().numpy(), v.cpu().detach().numpy(), logp_a.cpu().detach().numpy()

    def get_value(self, obs):
        return self.v_net(obs).squeeze(-1)

    def get_logp_and_entropy(self, obs, act):
        mu = self.pi_net(obs)
        std = torch.exp(self.log_std)
        dist = torch.distributions.Normal(mu, std)
        logp_a = dist.log_prob(act).sum(axis=-1)
        entropy = dist.entropy().sum(axis=-1)
        return logp_a, entropy


# ---------------------
# PPO Training Loop with PRG Regularization
# ---------------------

@dataclass
class Config:
    env_id: str = "Hopper-v5"
    steps_per_epoch: int = 4000
    epochs: int = 50
    gamma: float = 0.99
    lam: float = 0.95 # Lambda for GAE
    train_pi_iters: int = 80
    train_v_iters: int = 80
    clip_ratio: float = 0.2
    pi_lr: float = 3e-4
    vf_lr: float = 1e-3
    target_kl: float = 0.01
    
    # --- PRG Hyperparameters ---
    prg_window_size: int = 128
    wK: float = 0.1
    wG: float = 0.05
    wBeat: float = 0.01
    zeta_G: float = 0.1
    zeta_K: float = 0.1

def train():
    """Main training loop."""
    cfg = Config()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    env = gym.make(cfg.env_id)
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.shape[0]

    ac = ActorCritic(obs_dim, act_dim).to(device)
    pi_optimizer = optim.Adam(ac.pi_net.parameters(), lr=cfg.pi_lr)
    vf_optimizer = optim.Adam(ac.v_net.parameters(), lr=cfg.vf_lr)
    
    world_model = WorldModel(obs_dim, act_dim).to(device)
    wm_optimizer = optim.Adam(world_model.parameters(), lr=1e-3)
    
    obs_buf_prg = torch.zeros(cfg.prg_window_size, obs_dim, device=device)
    act_buf_prg = torch.zeros(cfg.prg_window_size, act_dim, device=device)
    prev_tau = float('inf')

    o, _ = env.reset()
    ep_ret, ep_len = 0, 0

    for epoch in range(cfg.epochs):
        obs_buf = torch.zeros(cfg.steps_per_epoch, obs_dim, device=device)
        act_buf = torch.zeros(cfg.steps_per_epoch, act_dim, device=device)
        adv_buf = torch.zeros(cfg.steps_per_epoch, device=device)
        rew_buf = torch.zeros(cfg.steps_per_epoch, device=device)
        ret_buf = torch.zeros(cfg.steps_per_epoch, device=device)
        val_buf = torch.zeros(cfg.steps_per_epoch, device=device)
        logp_buf = torch.zeros(cfg.steps_per_epoch, device=device)
        
        # --- FIX #2: Corrected data collection loop logic ---
        t = 0
        while t < cfg.steps_per_epoch:
            obs_tensor = torch.as_tensor(o, dtype=torch.float32, device=device)
            a, v, logp_a = ac.step(obs_tensor)
            
            next_o, r, d, _, _ = env.step(a)
            ep_ret += r
            ep_len += 1

            obs_buf[t] = obs_tensor
            act_buf[t] = torch.as_tensor(a, device=device)
            rew_buf[t] = r
            val_buf[t] = torch.as_tensor(v, device=device)
            logp_buf[t] = torch.as_tensor(logp_a, device=device)
            t += 1

            obs_buf_prg = torch.roll(obs_buf_prg, -1, dims=0)
            act_buf_prg = torch.roll(act_buf_prg, -1, dims=0)
            obs_buf_prg[-1] = obs_tensor
            act_buf_prg[-1] = torch.as_tensor(a, device=device)

            if t > 0 and t % cfg.prg_window_size == 0:
                with torch.no_grad():
                    K = world_model.k_tau(obs_buf_prg, act_buf_prg)
                    V = v_gamma(obs_buf_prg, act_buf_prg)
                    tau = tau_p(obs_buf_prg)
                    beat_pen = prg_penalty(K, V, tau, prev_tau, cfg.zeta_G, cfg.zeta_K)
                
                shaped_reward = cfg.wK * K - cfg.wG * V - cfg.wBeat * beat_pen
                rew_buf[t-1] += shaped_reward
                
                prev_tau = tau

                wm_optimizer.zero_grad()
                pred_obs = world_model(obs_buf_prg[:-1], act_buf_prg[:-1])
                wm_loss = F.mse_loss(pred_obs, obs_buf_prg[1:])
                wm_loss.backward()
                wm_optimizer.step()

            o = next_o
            
            timeout = ep_len == 1000
            terminal = d or timeout

            if terminal or t == cfg.steps_per_epoch:
                if not terminal:
                    print(f"Warning: trajectory cut off by epoch end at {ep_len} steps.")
                
                with torch.no_grad():
                    if timeout or t == cfg.steps_per_epoch:
                        v = ac.get_value(torch.as_tensor(o, dtype=torch.float32, device=device)).cpu().numpy()
                    else:
                        v = 0

                # --- GAE Calculation for the finished trajectory ---
                path_slice = slice(0, t)
                path_rews = rew_buf[path_slice]
                path_vals = val_buf[path_slice]

                deltas = torch.zeros_like(path_rews)
                for i in reversed(range(len(path_rews))):
                    next_val = v if i == len(path_rews) - 1 else path_vals[i+1]
                    deltas[i] = path_rews[i] + cfg.gamma * next_val - path_vals[i]

                last_adv = 0
                for i in reversed(range(len(path_rews))):
                    adv_buf[i] = deltas[i] + cfg.gamma * cfg.lam * last_adv
                    last_adv = adv_buf[i]
                
                ret_buf = adv_buf + val_buf

                print(f"Epoch: {epoch}, Episodic Return: {ep_ret:.3f}, Episodic Length: {ep_len}")

                o, _ = env.reset()
                ep_ret, ep_len = 0, 0
                # Do not break the inner loop; continue collecting until buffer is full.

        # --- PPO Update ---
        adv_mean, adv_std = torch.mean(adv_buf), torch.std(adv_buf)
        adv_buf = (adv_buf - adv_mean) / (adv_std + 1e-8)
        
        for i in range(cfg.train_pi_iters):
            pi_optimizer.zero_grad()
            logp, entropy = ac.get_logp_and_entropy(obs_buf, act_buf)
            ratio = torch.exp(logp - logp_buf)
            clip_adv = torch.clamp(ratio, 1 - cfg.clip_ratio, 1 + cfg.clip_ratio) * adv_buf
            loss_pi = -(torch.min(ratio * adv_buf, clip_adv)).mean()
            
            with torch.no_grad():
                approx_kl = (logp_buf - logp).mean().item()
            if approx_kl > 1.5 * cfg.target_kl:
                print(f"Stopping pi training at iter {i} due to high KL: {approx_kl:.4f}")
                break
                
            loss_pi.backward()
            pi_optimizer.step()
        
        for i in range(cfg.train_v_iters):
            vf_optimizer.zero_grad()
            v = ac.get_value(obs_buf)
            loss_v = F.mse_loss(v, ret_buf)
            loss_v.backward()
            vf_optimizer.step()
            
if __name__ == '__main__':
    train()