#!/usr/bin/env python3
"""
Wendigo-FIT with Generative Engrams: Meta-Learning Layer
---------------------------------------------------------
Inspired by Pirouette's COG-RES series, particularly:

COG-RES-004: Generative Engrams (memory as living generator)
COG-RES-003: Triadic Manifold (coherence topology)
COG-RES-001: Triadic Resonance (phase-locked patterns)

KEY INSIGHT FROM PIROUETTE:
Memory should not be "stored results" but "callable coherent dynamics"
- An engram is its own generator
- Retrieval = resonance activation, not lookup
- Patterns remain phase-coherent across delays

APPLICATION TO RL:
Instead of just storing policies in genetic pool, we store:
1. GENERATIVE ENGRAMS: Policy + context that generated it (Γ, T_p, K_i)
2. RESONANCE LOOKUP: Match new situations by "detuning metric"
3. TRIADIC COHERENCE: Track {state, action, outcome} phase relationships

This creates a meta-learning layer that:
- Learns WHEN to use which policy
- Adapts policies to similar-but-different contexts
- Maintains coherence across task variations
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
from typing import List, Tuple, Optional

# --- Configuration ---
ENV_NAME = 'Humanoid-v5'
NUM_EPISODES = 6000
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 10
EVAL_EPISODES = 5
SEED = 42
MODEL_PATH = "./wendigo_engrams/"

# Core hyperparameters
RESET_PATIENCE = 10
GENETIC_POOL_SIZE = 10
GENE_TRANSFER_RATE = 0.6
MAX_ACCEPTABLE_STD = 2.0

# Meta-learning hyperparameters
ENGRAM_RESONANCE_THRESHOLD = 0.3  # How similar must contexts be?
ENGRAM_BLEND_RATE = 0.2            # How fast to adapt retrieved engram
COHERENCE_MEMORY_LENGTH = 50       # Track recent triadic patterns

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

if os.path.exists(MODEL_PATH):
    shutil.rmtree(MODEL_PATH)
os.makedirs(MODEL_PATH, exist_ok=True)

print(f"Device: {device}")
print(f"Engram storage: {MODEL_PATH}")


# ============================================================================
# PIROUETTE-INSPIRED STRUCTURES
# ============================================================================

@dataclass
class EngramContext:
    """
    The 'generating parameters' for a policy engram.
    Corresponds to Pirouette's (Γ, T_p, K_i) triple.
    """
    gamma: float          # Temporal pressure / task difficulty (Γ)
    persistence: float    # How long policy was stable (T_p)
    identity: np.ndarray  # Characteristic state signature (K_i)
    
    def __repr__(self):
        return f"EngramContext(Γ={self.gamma:.3f}, T_p={self.persistence:.1f}, |K_i|={np.linalg.norm(self.identity):.2f})"


@dataclass
class GenerativeEngram:
    """
    COG-RES-004: A memory that is its own generator.
    
    Stores:
    - Policy weights (the 'attractor pattern')
    - Context that generated it (Γ, T_p, K_i)
    - Performance statistics
    - Coherence signature (triadic pattern)
    """
    rank: int
    policy_weights: OrderedDict
    context: EngramContext
    performance_score: float
    stability: float  # Inverse of std dev
    coherence_signature: np.ndarray  # Average {state, action, reward} triad
    
    def detuning_metric(self, query_context: EngramContext) -> float:
        """
        COG-RES-004 §6: Resonance test.
        How different is query context from this engram's context?
        """
        gamma_diff = abs(query_context.gamma - self.context.gamma)
        persistence_diff = abs(query_context.persistence - self.context.persistence)
        identity_diff = np.linalg.norm(query_context.identity - self.context.identity)
        
        # Weighted detuning (Γ matters most, then identity, then persistence)
        detuning = (1.0 * gamma_diff + 
                   0.5 * identity_diff / (np.linalg.norm(self.context.identity) + 1e-6) +
                   0.2 * persistence_diff / (self.context.persistence + 1e-6))
        
        return detuning


class TriadicCoherenceTracker:
    """
    COG-RES-003: Track phase relationships in {state, action, outcome} triads.
    
    In RL context:
    - State = observation vector
    - Action = policy output
    - Outcome = reward signal
    
    Coherence = how predictable the (s,a,r) relationship is
    """
    def __init__(self, max_length=50):
        self.history = deque(maxlen=max_length)
    
    def observe(self, state: np.ndarray, action: np.ndarray, reward: float):
        """Record a (state, action, reward) triad."""
        # Create normalized signatures
        state_sig = np.mean(state)  # Crude: just average (could use PCA)
        action_sig = np.linalg.norm(action)
        reward_sig = reward
        
        triad = np.array([state_sig, action_sig, reward_sig])
        self.history.append(triad)
    
    def get_signature(self) -> np.ndarray:
        """
        Return average triadic signature.
        This is the 'coherence pattern' - stable relationships between s, a, r.
        """
        if len(self.history) == 0:
            return np.zeros(3)
        return np.mean(list(self.history), axis=0)
    
    def get_coherence(self) -> float:
        """
        Measure coherence = inverse of variance.
        High coherence = predictable (s,a,r) relationships.
        """
        if len(self.history) < 10:
            return 0.0
        
        triads = np.array(list(self.history))
        variance = np.mean(np.var(triads, axis=0))
        coherence = 1.0 / (variance + 0.01)  # Higher = more coherent
        return coherence


# ============================================================================
# STANDARD RL COMPONENTS (from universal trainer)
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


# ============================================================================
# ENGRAM MEMORY SYSTEM
# ============================================================================

class EngramMemory:
    """
    COG-RES-004: The generative engram memory system.
    
    Stores policies not as dead weights, but as living generators
    with their generating context.
    """
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.engrams: List[GenerativeEngram] = []
    
    def store(self, engram: GenerativeEngram):
        """Store a new engram, evicting worst if at capacity."""
        if len(self.engrams) < self.capacity:
            self.engrams.append(engram)
        else:
            # Evict lowest performance
            worst_idx = min(range(len(self.engrams)), 
                          key=lambda i: self.engrams[i].performance_score)
            
            if engram.performance_score > self.engrams[worst_idx].performance_score:
                print(f"  > Evicting rank {self.engrams[worst_idx].rank} "
                      f"(score {self.engrams[worst_idx].performance_score:.2f})")
                self.engrams[worst_idx] = engram
    
    def resonance_query(self, query_context: EngramContext, 
                       threshold: float = 0.3) -> Optional[GenerativeEngram]:
        """
        COG-RES-004 §6: Query by resonance.
        
        Find engram whose context is most similar to query,
        if similarity exceeds threshold.
        """
        if not self.engrams:
            return None
        
        # Compute detuning for all engrams
        detunings = [(eng, eng.detuning_metric(query_context)) 
                    for eng in self.engrams]
        
        # Find best match
        best_eng, best_detuning = min(detunings, key=lambda x: x[1])
        
        if best_detuning < threshold:
            print(f"  > RESONANCE HIT: Rank {best_eng.rank}, "
                  f"detuning={best_detuning:.3f}, score={best_eng.performance_score:.2f}")
            return best_eng
        else:
            print(f"  > No resonance (best detuning={best_detuning:.3f} > {threshold})")
            return None
    
    def get_best_engrams(self, k=2) -> List[GenerativeEngram]:
        """Get top k engrams by performance."""
        sorted_engrams = sorted(self.engrams, 
                               key=lambda e: e.performance_score, 
                               reverse=True)
        return sorted_engrams[:k]


# ============================================================================
# META-LEARNING TRAINER
# ============================================================================

class MetaLearningTrainer:
    """
    Trainer that uses generative engrams for meta-learning.
    
    KEY ADDITIONS:
    1. Store policies with their generating context
    2. Query memory by resonance when performance drops
    3. Blend/adapt retrieved policies to current context
    4. Track triadic coherence to measure learning quality
    """
    def __init__(self, env_name):
        self.env_name = env_name
        self.env = gym.make(env_name, render_mode=None)
        self.agent = SACAgent(self.env)
        
        # Engram memory system
        self.engram_memory = EngramMemory(capacity=GENETIC_POOL_SIZE)
        
        # Triadic coherence tracking
        self.coherence_tracker = TriadicCoherenceTracker(
            max_length=COHERENCE_MEMORY_LENGTH
        )
        
        # Context tracking
        self.current_gamma = 0.0  # Temporal pressure (task difficulty)
        self.current_persistence = 0.0  # How long current policy stable
        self.current_identity = np.zeros(10)  # State signature
        
        self.batch_size = 256
        self.eval_history = []
        self.coherence_history = []
        self.resonance_events = []
        
        self.consecutive_bad_cycles = 0
        
        print(f"\n{'='*70}")
        print(f"META-LEARNING TRAINER WITH GENERATIVE ENGRAMS")
        print(f"Environment: {env_name}")
        print(f"Engram capacity: {GENETIC_POOL_SIZE}")
        print(f"Resonance threshold: {ENGRAM_RESONANCE_THRESHOLD}")
        print(f"{'='*70}\n")
    
    def estimate_current_context(self, recent_states: List[np.ndarray],
                                recent_rewards: List[float]) -> EngramContext:
        """
        Estimate current (Γ, T_p, K_i) context.
        
        Γ (gamma): Task difficulty = inverse of reward stability
        T_p (persistence): How many episodes current policy worked
        K_i (identity): Characteristic state distribution
        """
        # Gamma: high variance in rewards = high pressure
        if len(recent_rewards) > 5:
            reward_std = np.std(recent_rewards[-20:])
            gamma = reward_std + 0.1  # Higher std = higher pressure
        else:
            gamma = 1.0
        
        # Persistence: count stable episodes
        persistence = self.current_persistence
        
        # Identity: PCA-like signature of recent states
        if len(recent_states) > 10:
            states_array = np.array(recent_states[-50:])
            # Use mean and std of each dimension as crude signature
            mean_sig = np.mean(states_array, axis=0)[:5]
            std_sig = np.std(states_array, axis=0)[:5]
            identity = np.concatenate([mean_sig, std_sig])
        else:
            identity = np.zeros(10)
        
        return EngramContext(gamma=gamma, persistence=persistence, identity=identity)
    
    def blend_policies(self, current_weights: OrderedDict, 
                      engram_weights: OrderedDict, 
                      blend_rate: float) -> OrderedDict:
        """
        Adapt retrieved engram to current context.
        Like COG-RES-004's "re-bloom" - run the generator in new context.
        """
        blended = OrderedDict()
        for key in current_weights:
            blended[key] = (1 - blend_rate) * current_weights[key] + \
                          blend_rate * engram_weights[key]
        return blended
    
    def train(self):
        start_time = time.time()
        
        recent_states = []
        recent_rewards = []
        stable_episode_count = 0
        last_score = -np.inf
        
        for ep in range(1, NUM_EPISODES + 1):
            s, _ = self.env.reset(seed=SEED + ep)
            ep_reward = 0
            steps_in_episode = 0
            
            for step in range(1, MAX_STEPS_PER_EPISODE + 1):
                a = self.agent.select_action(s)
                s_, r_env, terminated, truncated, _ = self.env.step(a)
                done = terminated or truncated
                
                # Track triadic coherence
                self.coherence_tracker.observe(s, a, r_env)
                
                # Simple reward shaping (from FIT)
                action_magnitude = np.linalg.norm(a)
                risk_bonus = 0.15 * max(0, action_magnitude - 0.15)
                total_reward = r_env + risk_bonus
                
                self.agent.buffer.push(s, a, total_reward, s_, done)
                self.agent.update(self.batch_size)
                
                recent_states.append(s)
                s = s_
                ep_reward += r_env
                steps_in_episode += 1
                
                if done:
                    break
            
            # Process episode
            ep_reward_normalized = ep_reward / steps_in_episode if steps_in_episode > 0 else ep_reward
            recent_rewards.append(ep_reward_normalized)
            
            # Update persistence tracking
            if ep_reward_normalized > last_score * 0.9:  # Performance stable
                stable_episode_count += 1
            else:
                stable_episode_count = 0
            
            self.current_persistence = stable_episode_count
            last_score = ep_reward_normalized
            
            # Update gamma (temporal pressure)
            self.current_gamma = np.std(recent_rewards[-20:]) if len(recent_rewards) >= 20 else 1.0
            
            if ep % 10 == 0:
                coherence = self.coherence_tracker.get_coherence()
                print(f"Ep:{ep:04d} | R:{ep_reward_normalized:7.2f} | "
                      f"Steps:{steps_in_episode:4d} | "
                      f"Γ:{self.current_gamma:.2f} | "
                      f"T_p:{self.current_persistence} | "
                      f"Coherence:{coherence:.2f}")
            
            if ep % EVAL_FREQUENCY == 0:
                self.run_evaluation_and_manage_engrams(ep, recent_states, recent_rewards)
        
        elapsed = time.time() - start_time
        print(f"\nTraining finished in {elapsed:.2f}s.")
        self.plot_results()
    
    def run_evaluation_and_manage_engrams(self, ep, recent_states, recent_rewards):
        """Evaluate and manage engram memory with resonance query."""
        eval_rewards = []
        eval_coherences = []
        
        for i in range(EVAL_EPISODES):
            s, _ = self.env.reset(seed=SEED * 100 + i)
            ep_reward = 0
            steps = 0
            local_coherence = TriadicCoherenceTracker(max_length=20)
            
            for _ in range(MAX_STEPS_PER_EPISODE):
                a = self.agent.select_action(s, eval=True)
                s, r, terminated, truncated, _ = self.env.step(a)
                
                local_coherence.observe(s, a, r)
                ep_reward += r
                steps += 1
                
                if terminated or truncated:
                    break
            
            normalized = ep_reward / steps if steps > 0 else ep_reward
            eval_rewards.append(normalized)
            eval_coherences.append(local_coherence.get_coherence())
        
        current_score = np.mean(eval_rewards)
        score_std = np.std(eval_rewards)
        avg_coherence = np.mean(eval_coherences)
        
        self.eval_history.append(current_score)
        self.coherence_history.append(avg_coherence)
        
        best_score = max([e.performance_score for e in self.engram_memory.engrams]) if self.engram_memory.engrams else -np.inf
        
        print(f"  > Eval @ {ep} | Score:{current_score:7.2f} | Std:{score_std:.2f} | "
              f"Coherence:{avg_coherence:.2f} | Best:{best_score:7.2f}")
        
        # Store engram if stable and good
        is_stable = score_std <= MAX_ACCEPTABLE_STD
        is_improvement = current_score > best_score * 0.9
        
        if is_stable and is_improvement:
            context = self.estimate_current_context(recent_states, recent_rewards)
            coherence_sig = self.coherence_tracker.get_signature()
            
            engram = GenerativeEngram(
                rank=ep,
                policy_weights=copy.deepcopy(self.agent.actor.state_dict()),
                context=context,
                performance_score=current_score,
                stability=1.0 / (score_std + 0.01),
                coherence_signature=coherence_sig
            )
            
            self.engram_memory.store(engram)
            print(f"  > Stored engram: {context}")
            self.consecutive_bad_cycles = 0
            
        elif not is_stable:
            print(f"  > Rejected: unstable (Std: {score_std:.2f})")
        else:
            self.consecutive_bad_cycles += 1
            print(f"  > No improvement. Bad cycles: {self.consecutive_bad_cycles}/{RESET_PATIENCE}")
        
        # RESONANCE QUERY: If struggling, query memory
        if self.consecutive_bad_cycles >= RESET_PATIENCE:
            print("\n  ! PERFORMANCE DEGRADED. QUERYING ENGRAM MEMORY...")
            
            query_context = self.estimate_current_context(recent_states, recent_rewards)
            print(f"  > Query context: {query_context}")
            
            resonant_engram = self.engram_memory.resonance_query(
                query_context, 
                threshold=ENGRAM_RESONANCE_THRESHOLD
            )
            
            if resonant_engram:
                # BLEND: Adapt resonant engram to current context
                print(f"  > Blending resonant engram (rank {resonant_engram.rank}) with current policy...")
                
                current_weights = self.agent.actor.state_dict()
                blended_weights = self.blend_policies(
                    current_weights,
                    resonant_engram.policy_weights,
                    ENGRAM_BLEND_RATE
                )
                
                self.agent.actor.load_state_dict(blended_weights)
                self.resonance_events.append(ep)
                print(f"  > Blend complete. Resuming training.")
            else:
                # GENETIC: Fall back to traditional crossover
                print(f"  > No resonant match. Using genetic crossover...")
                best_engrams = self.engram_memory.get_best_engrams(k=2)
                
                if len(best_engrams) >= 2:
                    child_weights = OrderedDict()
                    for key in best_engrams[0].policy_weights:
                        if random.random() < GENE_TRANSFER_RATE:
                            child_weights[key] = best_engrams[0].policy_weights[key].clone()
                        else:
                            child_weights[key] = best_engrams[1].policy_weights[key].clone()
                    
                    self.agent.actor.load_state_dict(child_weights)
                    print(f"  > Genetic crossover complete.")
            
            self.consecutive_bad_cycles = 0
    
    def plot_results(self):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12))
        
        eval_episodes = np.arange(EVAL_FREQUENCY, 
                                 len(self.eval_history) * EVAL_FREQUENCY + 1, 
                                 EVAL_FREQUENCY)
        
        # Plot 1: Evaluation Score
        ax1.set_title(f"Meta-Learning with Engrams: {self.env_name}")
        ax1.set_xlabel("Episode")
        ax1.set_ylabel("Evaluation Score")
        ax1.plot(eval_episodes, self.eval_history, color='tab:blue', lw=2)
        
        # Mark resonance events
        for event_ep in self.resonance_events:
            ax1.axvline(x=event_ep, color='red', linestyle='--', alpha=0.3)
        ax1.legend(['Score', 'Resonance Event'])
        ax1.grid(True)
        
        # Plot 2: Triadic Coherence
        ax2.set_title("Triadic Coherence (Learning Quality)")
        ax2.set_xlabel("Episode")
        ax2.set_ylabel("Coherence")
        ax2.plot(eval_episodes, self.coherence_history, color='tab:green', lw=2)
        ax2.grid(True)
        
        # Plot 3: Engram Memory Evolution
        ax3.set_title("Engram Memory Pool")
        ax3.set_xlabel("Episode")
        ax3.set_ylabel("Number of Stored Engrams")
        
        # Track how memory fills over time
        memory_size = []
        for ep_idx in range(len(self.eval_history)):
            # Count engrams stored up to this episode
            ep_num = (ep_idx + 1) * EVAL_FREQUENCY
            count = sum(1 for e in self.engram_memory.engrams if e.rank <= ep_num)
            memory_size.append(count)
        
        ax3.plot(eval_episodes, memory_size, color='tab:purple', lw=2)
        ax3.axhline(y=GENETIC_POOL_SIZE, color='red', linestyle='--', alpha=0.5, label='Capacity')
        ax3.legend()
        ax3.grid(True)
        
        plt.tight_layout()
        save_path = f"meta_learning_engrams_{self.env_name.lower()}.png"
        plt.savefig(save_path)
        print(f"\nPlot saved to {save_path}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("WENDIGO-FIT WITH PIROUETTE GENERATIVE ENGRAMS")
    print("="*70 + "\n")
    
    trainer = MetaLearningTrainer(ENV_NAME)
    trainer.train()
    
    print("\n" + "="*70)
    print("ENGRAM MEMORY FINAL STATE")
    print("="*70)
    for i, engram in enumerate(trainer.engram_memory.engrams):
        print(f"\nEngram {i+1}:")
        print(f"  Rank: {engram.rank}")
        print(f"  Score: {engram.performance_score:.2f}")
        print(f"  Context: {engram.context}")
        print(f"  Coherence Sig: {engram.coherence_signature}")
    print("="*70 + "\n")