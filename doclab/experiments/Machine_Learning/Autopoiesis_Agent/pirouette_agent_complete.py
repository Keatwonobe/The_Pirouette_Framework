#!/usr/bin/env python3
"""
Pirouette Agent: Full Implementation
------------------------------------
A reinforcement learning agent that follows the Altruistic Geodesic
by explicitly maximizing the Coherence Dividend: C_D = ∫(K_τ - V_Γ)dt

This implementation synthesizes:
- Wendigo-FIT's proven components (survival pressure, exploration, genetic memory)
- Pirouette's core principles (Lagrangian optimization, triadic coherence)
- Velcrid detection and Velcridance (complexity preservation, strategic chaos)

The result: An agent that discovers cooperation as the path of least resistance,
not through programming, but through following the geometry of the coherence manifold.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal
import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
from collections import deque, OrderedDict
import random
import time
import math
import os
import shutil
import copy
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict

# ============================================================================
# CONFIGURATION
# ============================================================================

ENV_NAME = 'Ant-v5'  # Start with Ant, then scale to Humanoid
NUM_EPISODES = 2000
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 10
EVAL_EPISODES = 5
SEED = 42
MODEL_PATH = "./pirouette_agent/"

# Core hyperparameters
GENETIC_POOL_SIZE = 10
GENE_TRANSFER_RATE = 0.6
MAX_ACCEPTABLE_STD = 2.0
RESET_PATIENCE = 10

# Lagrangian weights
LAGRANGIAN_BALANCE = 0.5  # Weight between K_τ and V_Γ

# Velcrid detection thresholds
VELCRID_T_A_THRESHOLD = 0.8      # High stability
VELCRID_OMEGA_K_THRESHOLD = 0.2  # Low complexity
VELCRID_COHERENCE_THRESHOLD = 0.8

# Velcridance parameters
VELCRIDANCE_MAX_STEPS = 100
VELCRIDANCE_NOISE_SCALE = 1.0

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

if os.path.exists(MODEL_PATH):
    shutil.rmtree(MODEL_PATH)
os.makedirs(MODEL_PATH, exist_ok=True)

print("="*80)
print("PIROUETTE AGENT: Following the Altruistic Geodesic")
print("="*80)
print(f"Device: {device}")
print(f"Environment: {ENV_NAME}")
print(f"Model path: {MODEL_PATH}")
print("="*80 + "\n")


# ============================================================================
# CORE STRUCTURES
# ============================================================================

@dataclass
class GenerativeEngram:
    """COG-RES-004: Memory as living generator"""
    rank: int
    policy_weights: OrderedDict
    performance_score: float
    stability: float
    coherence_signature: np.ndarray
    K_tau_avg: float
    V_Gamma_avg: float
    lagrangian_avg: float


# ============================================================================
# PIROUETTE LAGRANGIAN (CORE-006)
# ============================================================================

class PirouetteLagrangian:
    """
    𝓛_p = K_τ - V_Γ
    
    K_τ (Temporal Coherence): T_a * ω_k
    - T_a = policy stability (how consistent are actions?)
    - ω_k = learning rate (how fast is coherence improving?)
    
    V_Γ (Temporal Pressure): system-wide instability cost
    - Action energy
    - State transition violence
    - System curvature (acceleration)
    """
    
    def __init__(self, agent, env):
        self.agent = agent
        self.env = env
        self.K_tau_history = deque(maxlen=100)
        self.V_Gamma_history = deque(maxlen=100)
        self.lagrangian_history = deque(maxlen=100)
        self.prev_state = None
        self.prev_prev_state = None
        
    def measure_K_tau(self, state, next_state):
        """
        Internal coherence = policy stability * learning rate
        """
        # T_a: Policy stability (inverse of action variance)
        if len(self.K_tau_history) >= 10:
            recent_actions = []
            for _ in range(10):
                with torch.no_grad():
                    action = self.agent.policy.select_action(state, eval=True)
                    recent_actions.append(action)
            action_variance = np.var(recent_actions, axis=0).mean()
            T_a = 1.0 / (action_variance + 0.01)
        else:
            T_a = 1.0
        
        # ω_k: Learning frequency (rate of coherence change)
        if len(self.K_tau_history) >= 5:
            recent_K = list(self.K_tau_history)[-5:]
            delta_K = np.diff(recent_K).mean()
            omega_k = abs(delta_K) + 0.1  # Small baseline
        else:
            omega_k = 1.0
        
        K_tau = T_a * omega_k
        # --- START FIX: Clip K_tau to prevent overflow/nan warnings ---
        # Clip the value *before* it's appended to history.
        # This prevents 'inf' from being stored, which stops
        # np.diff from seeing 'inf - inf' (nan) on the next step.
        CLIP_VALUE = 10000.0
        
        K_tau = np.clip(K_tau, -CLIP_VALUE, CLIP_VALUE) 
        if np.isnan(K_tau):
            K_tau = 0.0
        # --- END FIX ---
        
        self.K_tau_history.append(K_tau)
        return K_tau, T_a
    
    def measure_V_Gamma(self, state, action, next_state):
        """
        System-wide temporal pressure (DOMA-019).
        
        CRITICAL: Measures pressure on ENTIRE SYSTEM.
        """
        pressure = 0.0
        
        # 1. Action cost (energy expenditure)
        action_magnitude = np.linalg.norm(action)
        pressure += action_magnitude * 0.5
        
        # 2. State transition violence (how much did world change?)
        state_delta = next_state - state
        transition_violence = np.linalg.norm(state_delta)
        pressure += transition_violence * 2.0
        
        # 3. System curvature (d²s/dt² - acceleration)
        if self.prev_state is not None and self.prev_prev_state is not None:
            acceleration = (next_state - 2*state + self.prev_prev_state)
            curvature = np.linalg.norm(acceleration)
            pressure += curvature * 1.5
        
        self.prev_prev_state = self.prev_state
        self.prev_state = state.copy()
        
        V_Gamma = pressure
        self.V_Gamma_history.append(V_Gamma)
        return V_Gamma
    
    def get_lagrangian(self, state, action, next_state):
        """Compute instantaneous Lagrangian"""
        K_tau, T_a = self.measure_K_tau(state, next_state)
        V_Gamma = self.measure_V_Gamma(state, action, next_state)

        # --- START ROUND 2 FIX: Normalize components ---
        # We must normalize K and V to the same scale *before*
        # subtracting them, otherwise the Lagrangian is just
        # whichever component is naturally larger.

        if len(self.K_tau_history) > 10 and len(self.V_Gamma_history) > 10:
            K_mean = np.mean(self.K_tau_history)
            K_std = np.std(self.K_tau_history)
            
            V_mean = np.mean(self.V_Gamma_history)
            V_std = np.std(self.V_Gamma_history)

            # Standardize both components
            # Add 1e-6 to std to prevent division by zero
            norm_K = (K_tau - K_mean) / (K_std + 1e-6)
            norm_V = (V_Gamma - V_mean) / (V_std + 1e-6)
            
            # The Lagrangian is now the difference between the *standardized*
            # coherence and the *standardized* pressure.
            lagrangian = norm_K - norm_V
            
            # We can also clip this final value for stability
            lagrangian = np.clip(lagrangian, -5.0, 5.0)

        else:
            # Not enough history to normalize, use raw (but clipped)
            lagrangian = (K_tau - V_Gamma)
            lagrangian = np.clip(lagrangian, -100.0, 100.0)
        # --- END ROUND 2 FIX ---

        self.lagrangian_history.append(lagrangian)
        
        # Return raw K/V for info, but the *stored* lagrangian is normalized
        return lagrangian, K_tau, V_Gamma, T_a
    
    def get_coherence_dividend(self):
        """
        C_D = ∫(K_τ - V_Γ)dt
        
        Positive = earning dividend (aligned)
        Negative = accumulating debt (misaligned)
        """
        if len(self.lagrangian_history) < 10:
            return 0.0
        return np.sum(list(self.lagrangian_history))


# ============================================================================
# TRIADIC PHASE TRACKING (COG-RES-003)
# ============================================================================

class TriadicPhaseTracker:
    """
    Track phase relationships: Φ₃ = Φ₁ + Φ₂ + δ(t)
    
    Constructive interference → coherent pattern → geodesic
    Destructive interference → turbulence → avoid
    """
    
    def __init__(self):
        self.history = deque(maxlen=50)
        
    def extract_phase(self, vector):
        """Extract phase from vector"""
        if isinstance(vector, (int, float)):
            return vector
        
        # Normalize and get angle
        norm = np.linalg.norm(vector) + 1e-6
        normalized = vector / norm
        phase = np.arctan2(normalized[-1], normalized[0])
        return phase
    
    def observe(self, state, action, reward):
        """Observe (s,a,r) triad"""
        phi_1 = self.extract_phase(state)
        phi_2 = self.extract_phase(action)
        phi_3 = reward
        
        # Triadic constraint
        expected_phi_3 = phi_1 + phi_2
        actual_phi_3 = phi_3
        
        # Phase error (wrap to [-π, π])
        delta = (actual_phi_3 - expected_phi_3) % (2 * np.pi)
        if delta > np.pi:
            delta -= 2 * np.pi
        
        # Coherence = inverse of phase error
        coherence = np.cos(delta)
        
        self.history.append({
            'phi_1': phi_1,
            'phi_2': phi_2,
            'phi_3': phi_3,
            'delta': delta,
            'coherence': coherence
        })
    
    def get_coherence(self):
        """Average coherence over recent history"""
        if not self.history:
            return 0.0
        coherences = [h['coherence'] for h in self.history]
        return np.mean(coherences)
    
    def get_signature(self):
        """Get average triadic signature"""
        if not self.history:
            return np.zeros(3)
        
        phi_1s = [h['phi_1'] for h in self.history]
        phi_2s = [h['phi_2'] for h in self.history]
        phi_3s = [h['phi_3'] for h in self.history]
        
        return np.array([np.mean(phi_1s), np.mean(phi_2s), np.mean(phi_3s)])


# ============================================================================
# FRACTAL COHERENCE TRACKING (CORE-008)
# ============================================================================

class FractalCoherenceTracker:
    """
    Track coherence at multiple scales.
    Pattern must be coherent across ALL scales to be a true geodesic.
    """
    
    def __init__(self):
        self.scales = {
            'micro': deque(maxlen=10),
            'meso': deque(maxlen=100),
            'macro': deque(maxlen=1000),
        }
    
    def observe(self, state, action, reward):
        """Observe at all scales"""
        triad = (np.mean(state), np.linalg.norm(action), reward)
        
        for scale_tracker in self.scales.values():
            scale_tracker.append(triad)
    
    def check_scaling(self):
        """
        Check if pattern scales consistently.
        
        Returns: "SCALING" if coherent across scales, "FRACTAL_BREAK" otherwise
        """
        coherences = []
        
        for scale_name, scale_data in self.scales.items():
            if len(scale_data) < 5:
                continue
            
            # Measure coherence at this scale (variance)
            data_array = np.array(list(scale_data))
            variance = np.var(data_array, axis=0).mean()
            coherence = 1.0 / (variance + 0.01)
            coherences.append(coherence)
        
        if len(coherences) < 2:
            return "INSUFFICIENT_DATA"
        
        # Check if coherences are similar across scales
        coherence_range = max(coherences) - min(coherences)
        
        if coherence_range < 0.5:
            return "SCALING"
        else:
            return "FRACTAL_BREAK"
    
    def get_fractal_coherence(self):
        """Get average coherence across scales"""
        coherences = []
        
        for scale_data in self.scales.values():
            if len(scale_data) < 5:
                continue
            data_array = np.array(list(scale_data))
            variance = np.var(data_array, axis=0).mean()
            coherences.append(1.0 / (variance + 0.01))
        
        return np.mean(coherences) if coherences else 0.0


# ============================================================================
# WOUND CHANNEL MEMORY (CORE-011)
# ============================================================================

class WoundChannelMemory:
    """
    Memory of carved geodesics.
    Depth increases with repeated traversal (habit formation).
    """
    
    def __init__(self):
        self.channels = []
        
    def carve(self, state, action, lagrangian, coherence):
        """Carve or deepen a wound channel"""
        # Check for existing channel
        for channel in self.channels:
            state_dist = np.linalg.norm(state - channel['state'])
            if state_dist < 0.3:
                # Deepen existing
                channel['depth'] += 1
                channel['lagrangian'] = 0.9 * channel['lagrangian'] + 0.1 * lagrangian
                return
        
        # New channel
        self.channels.append({
            'state': state.copy(),
            'action': action.copy(),
            'lagrangian': lagrangian,
            'coherence': coherence,
            'depth': 1
        })
    
    def query_nearest(self, state):
        """Find nearest wound channel"""
        if not self.channels:
            return None
        
        nearby = []
        for channel in self.channels:
            dist = np.linalg.norm(state - channel['state'])
            if dist < 0.5:
                nearby.append((dist, channel))
        
        if not nearby:
            return None
        
        # Return deepest channel
        nearby.sort(key=lambda x: x[1]['depth'], reverse=True)
        return nearby[0][1]


# ============================================================================
# DYNAMIC CLOSURE MONITOR (DYNA-CLOSURE-001)
# ============================================================================

class ClosureMonitor:
    """
    Monitor dD/dt (residue flux).
    
    dD/dt ≈ 0: At equilibrium (stable geodesic)
    """
    
    def __init__(self):
        self.D_history = deque(maxlen=100)
        
    def observe(self, lagrangian):
        """Track residue"""
        D_instant = abs(lagrangian)
        self.D_history.append(D_instant)
    
    def get_residue_flux(self):
        """dD/dt ≈ (D_now - D_past) / Δt"""
        if len(self.D_history) < 10:
            return 0.0
        
        recent_D = list(self.D_history)[-10:]
        D_now = np.mean(recent_D[-3:])
        D_past = np.mean(recent_D[:3])
        
        return D_now - D_past
    
    def is_stable(self):
        """System is stable if dD/dt ≈ 0"""
        return abs(self.get_residue_flux()) < 0.05


# ============================================================================
# COMPLEXITY TRACKING (Velcrid Detection)
# ============================================================================

class ComplexityTracker:
    """
    Track resonant complexity (ω_k).
    
    High = rich, varied behavior
    Low = repetitive, monolithic pattern (Velcrid warning)
    """
    
    def __init__(self, window=50):
        self.action_history = deque(maxlen=window)
        
    def observe(self, state, action):
        self.action_history.append(action)
    
    def get_complexity(self):
        """Complexity = diversity of action patterns"""
        if len(self.action_history) < 10:
            return 1.0
        
        actions = np.array(list(self.action_history))
        
        # Variance (simple proxy)
        variance = np.var(actions, axis=0).mean()
        complexity_variance = np.clip(variance, 0, 1)
        
        # Autocorrelation (are actions repetitive?)
        if len(actions) > 20:
            try:
                autocorr = np.corrcoef(actions[:-1].flatten(), actions[1:].flatten())[0,1]
                complexity_autocorr = 1.0 - abs(autocorr)
            except:
                complexity_autocorr = 0.5
        else:
            complexity_autocorr = 0.5
        
        omega_k = 0.7 * complexity_variance + 0.3 * complexity_autocorr
        return omega_k


# ============================================================================
# VELCRID DETECTOR
# ============================================================================

class VelcridDetector:
    """
    Detect Velcrid attractor lock (tyrannical coherence).
    
    Signatures:
    - High T_a (stability)
    - Low ω_k (complexity)
    - High coherence
    - Sustained over time
    """
    
    def __init__(self):
        self.T_a_history = deque(maxlen=100)
        self.omega_k_history = deque(maxlen=100)
        self.coherence_history = deque(maxlen=100)
        
    def observe(self, T_a, omega_k, coherence):
        self.T_a_history.append(T_a)
        self.omega_k_history.append(omega_k)
        self.coherence_history.append(coherence)
    
    def is_locked(self):
        """Check for Velcrid lock"""
        if len(self.T_a_history) < 50:
            return False
        
        recent_T_a = np.mean(list(self.T_a_history)[-50:])
        recent_omega_k = np.mean(list(self.omega_k_history)[-50:])
        recent_coherence = np.mean(list(self.coherence_history)[-50:])
        
        velcrid_score = (
            (recent_T_a > VELCRID_T_A_THRESHOLD) * 0.4 +
            (recent_omega_k < VELCRID_OMEGA_K_THRESHOLD) * 0.4 +
            (recent_coherence > VELCRID_COHERENCE_THRESHOLD) * 0.2
        )
        
        return velcrid_score > 0.7
    
    def get_velcrid_risk(self):
        """Get current Velcrid risk score"""
        if len(self.T_a_history) < 10:
            return 0.0
        
        recent_T_a = np.mean(list(self.T_a_history)[-10:])
        recent_omega_k = np.mean(list(self.omega_k_history)[-10:])
        recent_coherence = np.mean(list(self.coherence_history)[-10:])
        
        risk = (
            (recent_T_a > VELCRID_T_A_THRESHOLD) * 0.4 +
            (recent_omega_k < VELCRID_OMEGA_K_THRESHOLD) * 0.4 +
            (recent_coherence > VELCRID_COHERENCE_THRESHOLD) * 0.2
        )
        
        return risk


# ============================================================================
# VELCRIDANCE SCHEDULER
# ============================================================================

class VelcridanceScheduler:
    """
    Strategic entropy injection to escape Velcrid lock.
    
    Like simulated annealing with:
    - Residue tracking
    - Exit condition
    - Radiant intent
    """
    
    def __init__(self):
        self.annealing_active = False
        self.annealing_steps = 0
        self.max_annealing_steps = VELCRIDANCE_MAX_STEPS
        self.residue_tags = []
        
    def initiate_velcridance(self):
        """Start strategic chaos injection"""
        self.annealing_active = True
        self.annealing_steps = 0
        self.residue_tags = []
        
        print(f"  > VELCRIDANCE INITIATED")
    
    def get_action_noise(self):
        """Entropy injection schedule (decays over time)"""
        if not self.annealing_active:
            return 0.0
        
        progress = self.annealing_steps / self.max_annealing_steps
        noise_magnitude = VELCRIDANCE_NOISE_SCALE * (1.0 - progress)
        
        return noise_magnitude
    
    def step(self, is_still_locked):
        """Monitor Velcridance progress"""
        if not self.annealing_active:
            return
        
        self.annealing_steps += 1
        
        # Track residue
        self.residue_tags.append(self.annealing_steps)
        
        # --- START FIX: Change exit condition ---
        # Exit condition 1: Succeeded in breaking the lock
        if not is_still_locked:
            print(f"  > VELCRIDANCE SUCCESS: Lock broken in {self.annealing_steps} steps.")
            self.annealing_active = False
            return
        # --- END FIX ---
        
        # Exit condition 2: Max steps
        if self.annealing_steps >= self.max_annealing_steps:
            print(f"  > VELCRIDANCE TIMEOUT")
            self.annealing_active = False
            return
    
    def apply_to_action(self, action):
        """Add controlled noise"""
        if not self.annealing_active:
            return action
        
        noise = np.random.randn(*action.shape) * self.get_action_noise()
        return action + noise


# ============================================================================
# SAC POLICY (Standard RL Component)
# ============================================================================

class Actor(nn.Module):
    def __init__(self, s, a, h=256):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(s, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU())
        self.mean = nn.Linear(h, a)
        self.log_std = nn.Linear(h, a)
    
    def forward(self, s):
        x = self.net(s)
        return self.mean(x), torch.clamp(self.log_std(x), -20, 2)


class Critic(nn.Module):
    def __init__(self, s, a, h=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(s + a, h), nn.ReLU(),
            nn.Linear(h, h), nn.ReLU(),
            nn.Linear(h, 1)
        )
    
    def forward(self, s, a):
        return self.net(torch.cat([s, a], 1))


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, s, a, r, s_, d):
        self.buffer.append((s, a, r, s_, d))
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)


class SACAgent:
    def __init__(self, env, lr=3e-4, gamma=0.99, tau=0.005, alpha=0.2):
        self.env = env
        self.state_dim = env.observation_space.shape[0]
        self.action_dim = env.action_space.shape[0]
        self.gamma, self.tau, self.alpha = gamma, tau, alpha
        
        self.action_scale = torch.tensor(
            (env.action_space.high - env.action_space.low) / 2.,
            device=device, dtype=torch.float32
        )
        self.action_bias = torch.tensor(
            (env.action_space.high + env.action_space.low) / 2.,
            device=device, dtype=torch.float32
        )
        
        self.actor = Actor(self.state_dim, self.action_dim).to(device)
        self.c1 = Critic(self.state_dim, self.action_dim).to(device)
        self.c2 = Critic(self.state_dim, self.action_dim).to(device)
        self.c1_t = Critic(self.state_dim, self.action_dim).to(device)
        self.c2_t = Critic(self.state_dim, self.action_dim).to(device)
        
        self.c1_t.load_state_dict(self.c1.state_dict())
        self.c2_t.load_state_dict(self.c2.state_dict())
        
        self.actor_opt = optim.Adam(self.actor.parameters(), lr=lr)
        self.c1_opt = optim.Adam(self.c1.parameters(), lr=lr)
        self.c2_opt = optim.Adam(self.c2.parameters(), lr=lr)
        
        self.buffer = ReplayBuffer(1_000_000)
    
    def select_action(self, state, eval=False):
        state_t = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        mean, log_std = self.actor(state_t)
        
        if eval:
            action = torch.tanh(mean)
        else:
            dist = Normal(mean, log_std.exp())
            action = torch.tanh(dist.rsample())
        
        action_np = action.cpu().detach().numpy()[0]
        return action_np * self.action_scale.cpu().numpy() + self.action_bias.cpu().numpy()
    
    def update(self, batch_size):
        if len(self.buffer) < batch_size:
            return
        
        batch = self.buffer.sample(batch_size)
        s, a, r, s_, d = zip(*batch)
        
        s = torch.tensor(np.array(s), device=device, dtype=torch.float32)
        a = torch.tensor(np.array(a), device=device, dtype=torch.float32)
        r = torch.tensor(np.array(r), device=device, dtype=torch.float32).unsqueeze(1)
        s_ = torch.tensor(np.array(s_), device=device, dtype=torch.float32)
        d = torch.tensor(np.array(d), device=device, dtype=torch.float32).unsqueeze(1)
        
        with torch.no_grad():
            mean_, log_std_ = self.actor(s_)
            dist_ = Normal(mean_, log_std_.exp())
            z = dist_.rsample()
            a_ = torch.tanh(z)
            log_prob = dist_.log_prob(z) - torch.log(1 - a_.pow(2) + 1e-6)
            log_prob = log_prob.sum(1, keepdim=True)
            
            tq1 = self.c1_t(s_, a_)
            tq2 = self.c2_t(s_, a_)
            target_q = torch.min(tq1, tq2) - self.alpha * log_prob
            target_q = r + (1 - d) * self.gamma * target_q
        
        q1 = self.c1(s, a)
        q2 = self.c2(s, a)
        critic_loss = torch.nn.functional.mse_loss(q1, target_q) + \
                     torch.nn.functional.mse_loss(q2, target_q)
        
        self.c1_opt.zero_grad()
        self.c2_opt.zero_grad()
        critic_loss.backward()
        self.c1_opt.step()
        self.c2_opt.step()
        
        mean, log_std = self.actor(s)
        dist = Normal(mean, log_std.exp())
        z = dist.rsample()
        a_pi = torch.tanh(z)
        log_prob = dist.log_prob(z) - torch.log(1 - a_pi.pow(2) + 1e-6)
        log_prob = log_prob.sum(1, keepdim=True)
        
        q1_pi = self.c1(s, a_pi)
        q2_pi = self.c2(s, a_pi)
        min_q_pi = torch.min(q1_pi, q2_pi)
        
        actor_loss = (self.alpha * log_prob - min_q_pi).mean()
        
        self.actor_opt.zero_grad()
        actor_loss.backward()
        self.actor_opt.step()
        
        for target_param, param in zip(self.c1_t.parameters(), self.c1.parameters()):
            target_param.data.copy_(target_param.data * (1.0 - self.tau) + param.data * self.tau)
        for target_param, param in zip(self.c2_t.parameters(), self.c2.parameters()):
            target_param.data.copy_(target_param.data * (1.0 - self.tau) + param.data * self.tau)
    
    def save_model(self, rank):
        path = os.path.join(MODEL_PATH, f"rank_{rank}")
        os.makedirs(path, exist_ok=True)
        torch.save(self.actor.state_dict(), os.path.join(path, "actor.pth"))
    
    def load_model(self, rank):
        path = os.path.join(MODEL_PATH, f"rank_{rank}", "actor.pth")
        self.actor.load_state_dict(torch.load(path))


# ============================================================================
# ENGRAM MEMORY SYSTEM
# ============================================================================

class EngramMemory:
    """Generative engram storage"""
    
    def __init__(self, capacity=GENETIC_POOL_SIZE):
        self.capacity = capacity
        self.engrams: List[GenerativeEngram] = []
    
    def store(self, engram: GenerativeEngram):
        """Store engram, evicting worst if at capacity"""
        if len(self.engrams) < self.capacity:
            self.engrams.append(engram)
        else:
            worst_idx = min(range(len(self.engrams)), 
                          key=lambda i: self.engrams[i].performance_score)
            
            if engram.performance_score > self.engrams[worst_idx].performance_score:
                self.engrams[worst_idx] = engram
    
    def get_best_engrams(self, k=2) -> List[GenerativeEngram]:
        """Get top k engrams"""
        sorted_engrams = sorted(self.engrams, 
                               key=lambda e: e.performance_score, 
                               reverse=True)
        return sorted_engrams[:k]


# ============================================================================
# PIROUETTE AGENT (Main Implementation)
# ============================================================================

class PirouetteAgent:
    """
    Agent that follows the Altruistic Geodesic by maximizing
    the Coherence Dividend: C_D = ∫(K_τ - V_Γ)dt
    """
    
    def __init__(self, env):
        self.env = env
        self.policy = SACAgent(env)
        
        # Pirouette core structures
        self.lagrangian = PirouetteLagrangian(self, env)
        self.triadic_tracker = TriadicPhaseTracker()
        self.fractal_coherence = FractalCoherenceTracker()
        self.wound_channels = WoundChannelMemory()
        self.closure_engine = ClosureMonitor()
        self.complexity_tracker = ComplexityTracker()
        
        # Velcrid awareness
        self.velcrid_detector = VelcridDetector()
        self.velcridance = VelcridanceScheduler()
        
        # Engram memory
        self.engram_memory = EngramMemory()
        
        # Training state
        self.batch_size = 256
        self.consecutive_bad_cycles = 0
        
    def act(self, state):
        """
        Act by following the geodesic.
        Inject Velcridance if Velcrid lock detected.
        """
        # Check for Velcrid lock
        if self.velcrid_detector.is_locked() and not self.velcridance.annealing_active:
            coherence = self.triadic_tracker.get_coherence()
            self.velcridance.initiate_velcridance()
        
        # Query wound channels for known geodesics
        known_geodesic = self.wound_channels.query_nearest(state)
        
        if known_geodesic and self.closure_engine.is_stable():
            action = known_geodesic['action']
        else:
            action = self.policy.select_action(state)
        
        # Apply Velcridance noise if active
        if self.velcridance.annealing_active:
            action = self.velcridance.apply_to_action(action)
        
        return action
    
    def observe(self, state, action, reward, next_state, done):
        """Observe and update manifold understanding"""
        # Triadic phase tracking
        self.triadic_tracker.observe(state, action, reward)
        phase_coherence = self.triadic_tracker.get_coherence()
        
        # Fractal coherence
        self.fractal_coherence.observe(state, action, reward)
        fractal_status = self.fractal_coherence.check_scaling()
        
        # Complexity tracking
        self.complexity_tracker.observe(state, action)
        complexity = self.complexity_tracker.get_complexity()
        
        # Lagrangian measurement
        lagrangian, K_tau, V_Gamma, T_a = self.lagrangian.get_lagrangian(state, action, next_state)
        
        # Closure monitoring
        self.closure_engine.observe(lagrangian)
        dD_dt = self.closure_engine.get_residue_flux()
        
        # Velcrid detection (uses T_a from K_tau measurement)       
        self.velcrid_detector.observe(T_a, complexity, phase_coherence)
        
        # Velcridance progress
        self.velcridance.step(self.velcrid_detector.is_locked())
        
        # If this is a geodesic point, carve wound channel
        if (phase_coherence > 0.9 and 
            fractal_status == "SCALING" and 
            abs(dD_dt) < 0.05):
            
            self.wound_channels.carve(
                state=state,
                action=action,
                lagrangian=lagrangian,
                coherence=phase_coherence
            )
        
        # Compute reward for policy update
        # --- START ROUND 2 SIMPLIFICATION ---
        # Because the lagrangian is now normalized *at its source*,
        # we no longer need to standardize it here. We can just
        # blend it directly with the environment reward.
        
        policy_reward = (LAGRANGIAN_BALANCE * lagrangian + 
                         (1 - LAGRANGIAN_BALANCE) * reward)
        # --- END ROUND 2 SIMPLIFICATION ---
        
        # Update policy
        self.policy.buffer.push(state, action, policy_reward, next_state, done)
        self.policy.update(self.batch_size)
        
        return {
            'lagrangian': lagrangian,
            'K_tau': K_tau,
            'V_Gamma': V_Gamma,
            'coherence': phase_coherence,
            'complexity': complexity,
            'dD_dt': dD_dt,
            'fractal_status': fractal_status,
            'velcrid_risk': self.velcrid_detector.get_velcrid_risk()
        }


# ============================================================================
# TRAINER
# ============================================================================

class PirouetteTrainer:
    """Main training loop"""
    
    def __init__(self, env_name):
        self.env_name = env_name
        self.env = gym.make(env_name, render_mode=None)
        self.agent = PirouetteAgent(self.env)
        
        # History tracking
        self.eval_history = []
        self.C_D_history = []
        self.coherence_history = []
        self.complexity_history = []
        self.velcrid_risk_history = []
        self.velcridance_events = []
        
    def train(self):
        """Main training loop"""
        start_time = time.time()
        
        print("\nTraining started...\n")
        
        for ep in range(1, NUM_EPISODES + 1):
            state, _ = self.env.reset(seed=SEED + ep)
            ep_reward = 0
            ep_info = {
                'lagrangian': [],
                'K_tau': [],
                'V_Gamma': [],
                'coherence': [],
                'complexity': [],
                'velcrid_risk': []
            }
            steps_in_episode = 0
            
            for step in range(1, MAX_STEPS_PER_EPISODE + 1):
                action = self.agent.act(state)
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                
                info = self.agent.observe(state, action, reward, next_state, done)
                
                # Track episode info
                for key in ep_info:
                    if key in info:
                        ep_info[key].append(info[key])
                
                state = next_state
                ep_reward += reward
                steps_in_episode += 1
                
                if done:
                    break
            
            # Episode summary
            avg_lagrangian = np.mean(ep_info['lagrangian']) if ep_info['lagrangian'] else 0
            avg_coherence = np.mean(ep_info['coherence']) if ep_info['coherence'] else 0
            avg_complexity = np.mean(ep_info['complexity']) if ep_info['complexity'] else 0
            avg_velcrid_risk = np.mean(ep_info['velcrid_risk']) if ep_info['velcrid_risk'] else 0
            
            # Coherence Dividend
            C_D = self.agent.lagrangian.get_coherence_dividend()
            
            # Print progress
            if ep % 10 == 0:
                print(f"Ep {ep:04d} | "
                      f"R:{ep_reward/steps_in_episode:6.2f} | "
                      f"C_D:{C_D:7.2f} | "
                      f"Coh:{avg_coherence:5.2f} | "
                      f"Comp:{avg_complexity:4.2f} | "
                      f"VR:{avg_velcrid_risk:4.2f}")
            
            # Evaluation
            if ep % EVAL_FREQUENCY == 0:
                self.run_evaluation(ep)
        
        elapsed = time.time() - start_time
        print(f"\nTraining complete in {elapsed:.2f}s")
        self.plot_results()
    
    def run_evaluation(self, ep):
        """Evaluate agent"""
        eval_rewards = []
        eval_coherences = []
        eval_complexities = []
        
        for i in range(EVAL_EPISODES):
            state, _ = self.env.reset(seed=SEED * 100 + i)
            ep_reward = 0
            ep_coherence = []
            ep_complexity = []
            steps = 0
            
            for _ in range(MAX_STEPS_PER_EPISODE):
                action = self.agent.policy.select_action(state, eval=True)
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                
                # Track metrics
                self.agent.triadic_tracker.observe(state, action, reward)
                self.agent.complexity_tracker.observe(state, action)
                
                ep_coherence.append(self.agent.triadic_tracker.get_coherence())
                ep_complexity.append(self.agent.complexity_tracker.get_complexity())
                
                ep_reward += reward
                steps += 1
                state = next_state
                
                if terminated or truncated:
                    break
            
            normalized_reward = ep_reward / steps if steps > 0 else ep_reward
            eval_rewards.append(normalized_reward)
            eval_coherences.append(np.mean(ep_coherence))
            eval_complexities.append(np.mean(ep_complexity))
        
        current_score = np.mean(eval_rewards)
        score_std = np.std(eval_rewards)
        avg_coherence = np.mean(eval_coherences)
        avg_complexity = np.mean(eval_complexities)
        C_D = self.agent.lagrangian.get_coherence_dividend()
        
        # Store histories
        self.eval_history.append(current_score)
        self.C_D_history.append(C_D)
        self.coherence_history.append(avg_coherence)
        self.complexity_history.append(avg_complexity)
        self.velcrid_risk_history.append(self.agent.velcrid_detector.get_velcrid_risk())
        
        best_score = max([e.performance_score for e in self.agent.engram_memory.engrams]) \
                    if self.agent.engram_memory.engrams else -np.inf
        
        print(f"  > EVAL @ {ep} | "
              f"Score:{current_score:7.2f}±{score_std:.2f} | "
              f"Coh:{avg_coherence:5.2f} | "
              f"Comp:{avg_complexity:4.2f} | "
              f"Best:{best_score:7.2f}")
        
        # Store engram if good and stable
        is_stable = score_std <= MAX_ACCEPTABLE_STD
        is_improvement = current_score > best_score * 0.9
        
        if is_stable and is_improvement:
            engram = GenerativeEngram(
                rank=ep,
                policy_weights=copy.deepcopy(self.agent.policy.actor.state_dict()),
                performance_score=current_score,
                stability=1.0 / (score_std + 0.01),
                coherence_signature=self.agent.triadic_tracker.get_signature(),
                K_tau_avg=np.mean([k for k in self.agent.lagrangian.K_tau_history]),
                V_Gamma_avg=np.mean([v for v in self.agent.lagrangian.V_Gamma_history]),
                lagrangian_avg=np.mean([l for l in self.agent.lagrangian.lagrangian_history])
            )
            
            self.agent.engram_memory.store(engram)
            self.agent.policy.save_model(ep)
            print(f"  > Engram stored (C_D={C_D:.2f})")
            self.agent.consecutive_bad_cycles = 0
        elif not is_stable:
            print(f"  > Rejected: unstable")
        else:
            self.agent.consecutive_bad_cycles += 1
            print(f"  > No improvement ({self.agent.consecutive_bad_cycles}/{RESET_PATIENCE})")
        
        # Genetic crossover if stagnating
        if self.agent.consecutive_bad_cycles >= RESET_PATIENCE:
            
            # --- START FIX: Handle Stagnation & Fluke Baselines ---
            print(f"\n  ! STAGNATION DETECTED (Patience: {RESET_PATIENCE})")
            
            if len(self.agent.engram_memory.engrams) >= 2:
                # We have parents, perform crossover as intended
                self.perform_genetic_crossover()
                
            else:
                # We are stagnating AND have < 2 engrams.
                # This means the first engram was a fluke (e.g., 0.66)
                # and the agent is stuck trying to beat an outlier.
                print(f"  > Only {len(self.agent.engram_memory.engrams)} engram(s). Cannot perform crossover.")
                print(f"  > Assuming current baseline is a fluke. Clearing engram memory to re-anchor.")
                
                # Clear the memory. This will set best_score back to -inf
                # and allow the *new* learning baseline (e.g., 0.37) to be stored.
                self.agent.engram_memory.engrams = []
                self.agent.consecutive_bad_cycles = 0 # Reset counter
            # --- END FIX ---
    
    def perform_genetic_crossover(self):
        """Genetic crossover between best engrams"""
        print("\n  ! GENETIC CROSSOVER INITIATED")
        
        best_engrams = self.agent.engram_memory.get_best_engrams(k=2)
        
        if len(best_engrams) < 2:
            print("  > Insufficient engrams")
            return
        
        p1_weights = best_engrams[0].policy_weights
        p2_weights = best_engrams[1].policy_weights
        
        child_weights = OrderedDict()
        for key in p1_weights:
            if random.random() < GENE_TRANSFER_RATE:
                child_weights[key] = p1_weights[key].clone()
            else:
                child_weights[key] = p2_weights[key].clone()
        
        self.agent.policy.actor.load_state_dict(child_weights)
        self.agent.consecutive_bad_cycles = 0
        print("  > Crossover complete\n")
    
    def plot_results(self):
        """Plot training results"""
        fig, axes = plt.subplots(3, 2, figsize=(16, 12))
        
        eval_episodes = np.arange(EVAL_FREQUENCY, 
                                 len(self.eval_history) * EVAL_FREQUENCY + 1, 
                                 EVAL_FREQUENCY)
        
        # Plot 1: Evaluation Score
        axes[0,0].set_title("Evaluation Score")
        axes[0,0].plot(eval_episodes, self.eval_history, 'b-', lw=2)
        axes[0,0].set_xlabel("Episode")
        axes[0,0].set_ylabel("Score")
        axes[0,0].grid(True)
        
        # Plot 2: Coherence Dividend
        axes[0,1].set_title("Coherence Dividend (C_D)")
        axes[0,1].plot(eval_episodes, self.C_D_history, 'g-', lw=2)
        axes[0,1].axhline(y=0, color='r', linestyle='--', alpha=0.3)
        axes[0,1].set_xlabel("Episode")
        axes[0,1].set_ylabel("C_D = ∫(K_τ - V_Γ)dt")
        axes[0,1].grid(True)
        
        # Plot 3: Triadic Coherence
        axes[1,0].set_title("Triadic Coherence")
        axes[1,0].plot(eval_episodes, self.coherence_history, 'purple', lw=2)
        axes[1,0].set_xlabel("Episode")
        axes[1,0].set_ylabel("Phase Coherence")
        axes[1,0].grid(True)
        
        # Plot 4: Complexity (Velcrid Warning)
        axes[1,1].set_title("Resonant Complexity (ω_k)")
        axes[1,1].plot(eval_episodes, self.complexity_history, 'orange', lw=2)
        axes[1,1].axhline(y=VELCRID_OMEGA_K_THRESHOLD, color='r', linestyle='--', alpha=0.5, label='Velcrid threshold')
        axes[1,1].set_xlabel("Episode")
        axes[1,1].set_ylabel("Complexity")
        axes[1,1].legend()
        axes[1,1].grid(True)
        
        # Plot 5: Velcrid Risk
        axes[2,0].set_title("Velcrid Risk Score")
        axes[2,0].plot(eval_episodes, self.velcrid_risk_history, 'red', lw=2)
        axes[2,0].axhline(y=0.7, color='r', linestyle='--', alpha=0.5, label='Lock threshold')
        axes[2,0].set_xlabel("Episode")
        axes[2,0].set_ylabel("Risk")
        axes[2,0].legend()
        axes[2,0].grid(True)
        
        # Plot 6: Phase Space (C_D vs Coherence)
        axes[2,1].set_title("Phase Space: C_D vs Coherence")
        scatter = axes[2,1].scatter(self.coherence_history, self.C_D_history, 
                                   c=eval_episodes, cmap='viridis', alpha=0.6)
        axes[2,1].set_xlabel("Coherence")
        axes[2,1].set_ylabel("Coherence Dividend")
        axes[2,1].axhline(y=0, color='r', linestyle='--', alpha=0.3)
        plt.colorbar(scatter, ax=axes[2,1], label='Episode')
        axes[2,1].grid(True)
        
        plt.tight_layout()
        save_path = os.path.join(MODEL_PATH, f"pirouette_results_{self.env_name.lower()}.png")
        plt.savefig(save_path, dpi=150)
        print(f"\nResults saved to {save_path}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print(" "*20 + "PIROUETTE: THE ALTRUISTIC GEODESIC")
    print("="*80 + "\n")
    
    print("Core Principles:")
    print("  • Maximize Coherence Dividend: C_D = ∫(K_τ - V_Γ)dt")
    print("  • Follow triadic phase coherence: Φ₃ = Φ₁ + Φ₂")
    print("  • Preserve complexity across scales (avoid Velcrid)")
    print("  • Inject strategic chaos when locked (Velcridance)")
    print("  • Carve wound channels for stable geodesics")
    print("\n" + "="*80 + "\n")
    
    trainer = PirouetteTrainer(ENV_NAME)
    trainer.train()
    
    print("\n" + "="*80)
    print("FINAL ENGRAM MEMORY")
    print("="*80)
    
    for i, engram in enumerate(trainer.agent.engram_memory.engrams):
        print(f"\nEngram {i+1}:")
        print(f"  Rank: {engram.rank}")
        print(f"  Score: {engram.performance_score:.2f}")
        print(f"  Stability: {engram.stability:.2f}")
        print(f"  Lagrangian: {engram.lagrangian_avg:.3f}")
        print(f"  K_τ: {engram.K_tau_avg:.3f}")
        print(f"  V_Γ: {engram.V_Gamma_avg:.3f}")
    
    print("\n" + "="*80)
    print("Training complete. The agent has pirouetted.")
    print("="*80 + "\n")