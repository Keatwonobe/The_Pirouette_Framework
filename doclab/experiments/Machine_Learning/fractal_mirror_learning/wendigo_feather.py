#!/usr/bin/env python3
"""
wendigo_geodesic_sac.py
-----------------------
The Pirouette SAC Agent with Geodesic Navigation and Reverse Pareto Analysis.

Core Innovation:
- Multi-objective reward (coherence gain, duration, dissonance penalty)
- Geodesic Map: learns state -> action -> expected_DR mappings
- Reverse Pareto Analysis: identifies critical 20% of moments causing 80% of DR
- Witness-First: every episode is catalogued and analyzed
- Phase-Aware: switches between exploration and exploitation based on geodesic proximity

This combines your proven SAC approach with the geodesic navigation framework.
"""
import gymnasium as gym
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any
import json
import os
import time

# --------------------------------------------------------------------------- #
# CONFIGURATION
# --------------------------------------------------------------------------- #

GALLERY_DIR = "gallery_geodesic_sac"
os.makedirs(GALLERY_DIR, exist_ok=True)

# Pirouette reward hyperparameters
GAMMA_COHERENCE = 1.5   # Weight for coherence gain
BETA_DURATION = 0.05    # Small constant reward per step
DELTA_DISSONANCE = 1.0  # Weight for dissonance penalty

# Geodesic parameters
GEODESIC_INFLUENCE = 0.3  # How much geodesic map influences action selection
EXPLORATION_DECAY = 0.995  # Per-episode decay of exploration rate
MIN_EXPLORATION = 0.1

# RPA parameters
RPA_THRESHOLD = 0.8  # Identify moments causing 80% of DR

# --------------------------------------------------------------------------- #
# DARK RESIDUE CALCULATION
# --------------------------------------------------------------------------- #

def calculate_dark_residue(obs: np.ndarray) -> float:
    """CartPole-specific DR: weighted sum of state deviations."""
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    return (0.4 * abs(cart_pos) + 
            0.2 * abs(cart_vel) + 
            1.5 * abs(pole_angle) + 
            0.3 * abs(pole_vel))

# --------------------------------------------------------------------------- #
# DATA STRUCTURES
# --------------------------------------------------------------------------- #

@dataclass
class Transition:
    """A single step with residue tracking."""
    state: np.ndarray
    action: np.ndarray
    reward: float
    next_state: np.ndarray
    done: bool
    
    # Residue components
    dark_residue: float = 0.0
    dr_derivative: float = 0.0  # Change in DR
    coherence_gain: float = 0.0  # Negative dr_derivative (good)
    
    def state_hash(self) -> int:
        """Hash for geodesic map indexing."""
        # Discretize state for hashing
        discretized = (self.state * 10).astype(int)
        return hash(tuple(discretized))


@dataclass 
class Episode:
    """A witnessed episode with full trajectory."""
    episode_num: int
    transitions: List[Transition] = field(default_factory=list)
    
    # Aggregate metrics
    total_reward: float = 0.0
    total_score: int = 0
    mean_dr: float = 0.0
    total_coherence_gain: float = 0.0
    
    # Critical moments (from RPA)
    critical_indices: List[int] = field(default_factory=list)
    critical_states: List[int] = field(default_factory=list)  # state hashes
    
    timestamp: float = field(default_factory=time.time)
    
    def compute_metrics(self):
        """Aggregate statistics from transitions."""
        if not self.transitions:
            return
        
        self.total_score = len(self.transitions)
        self.total_reward = sum(t.reward for t in self.transitions)
        self.mean_dr = np.mean([t.dark_residue for t in self.transitions])
        self.total_coherence_gain = sum(t.coherence_gain for t in self.transitions)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize for gallery."""
        return {
            'episode_num': self.episode_num,
            'total_score': self.total_score,
            'total_reward': float(self.total_reward),
            'mean_dr': float(self.mean_dr),
            'total_coherence_gain': float(self.total_coherence_gain),
            'critical_moment_count': len(self.critical_indices),
            'timestamp': self.timestamp,
        }


# --------------------------------------------------------------------------- #
# REVERSE PARETO ANALYSIS
# --------------------------------------------------------------------------- #

class ReversePareto:
    """
    Identifies the critical few transitions responsible for most Dark Residue.
    """
    
    @staticmethod
    def analyze(episode: Episode, threshold: float = RPA_THRESHOLD) -> List[Tuple[int, int, float]]:
        """
        Find transitions accounting for `threshold` of total DR.
        
        Returns: List of (step_idx, state_hash, dr_contribution)
        """
        if not episode.transitions:
            return []
        
        # Score each transition by its DR
        impacts = []
        for i, trans in enumerate(episode.transitions):
            impacts.append({
                'idx': i,
                'state_hash': trans.state_hash(),
                'dr': trans.dark_residue,
            })
        
        # Sort by DR (descending)
        impacts.sort(key=lambda x: x['dr'], reverse=True)
        
        # Find critical few
        total_dr = sum(x['dr'] for x in impacts)
        if total_dr == 0:
            return []
        
        critical = []
        cumulative = 0.0
        
        for item in impacts:
            cumulative += item['dr']
            fraction = cumulative / total_dr
            
            critical.append((
                item['idx'],
                item['state_hash'],
                item['dr']
            ))
            
            if fraction >= threshold:
                break
        
        return critical


# --------------------------------------------------------------------------- #
# GEODESIC MAP
# --------------------------------------------------------------------------- #

class GeodesicMap:
    """
    Learns state -> action -> expected_DR mappings.
    
    This is the "chart of low-resistance paths" through state-space.
    """
    
    def __init__(self):
        # state_hash -> {action_idx -> (avg_dr, count)}
        self.map: Dict[int, Dict[int, Tuple[float, int]]] = defaultdict(lambda: {})
        
        # Track which states we've seen
        self.known_states: set = set()
        
    def update(self, state_hash: int, action: np.ndarray, dr: float):
        """Record observed DR for this state-action pair."""
        # Discretize continuous action to index
        action_idx = 0 if action[0] < 0 else 1
        
        self.known_states.add(state_hash)
        
        if action_idx not in self.map[state_hash]:
            self.map[state_hash][action_idx] = (dr, 1)
        else:
            old_avg, count = self.map[state_hash][action_idx]
            new_avg = (old_avg * count + dr) / (count + 1)
            self.map[state_hash][action_idx] = (new_avg, count + 1)
    
    def get_best_action(self, state_hash: int) -> int:
        """
        Return action with lowest expected DR for this state.
        Returns -1 if state unknown.
        """
        if state_hash not in self.map:
            return -1
        
        action_drs = self.map[state_hash]
        if not action_drs:
            return -1
        
        # Return action with minimum expected DR
        best_action = min(action_drs.keys(), key=lambda a: action_drs[a][0])
        return best_action
    
    def is_known(self, state_hash: int) -> bool:
        """Check if we've seen this state before."""
        return state_hash in self.known_states
    
    def get_expected_dr(self, state_hash: int, action_idx: int) -> float:
        """Get expected DR for state-action pair, or high value if unknown."""
        if state_hash in self.map and action_idx in self.map[state_hash]:
            return self.map[state_hash][action_idx][0]
        return 999.0  # High DR for unknown pairs


# --------------------------------------------------------------------------- #
# WITNESS (gallery + geodesic learning)
# --------------------------------------------------------------------------- #

class GeodesicWitness:
    """
    Observes episodes, maintains galleries, and learns geodesic structure.
    """
    
    def __init__(self, top_k: int = 15):
        self.top_k = top_k
        
        # Episode storage
        self.all_episodes: List[Episode] = []
        self.top_episodes: List[Episode] = []
        
        # Geodesic learning
        self.geodesic_map = GeodesicMap()
        
        # Statistics
        self.exploration_rate = 1.0
        
    def observe(self, episode: Episode):
        """Witness an episode: store, analyze, learn."""
        # Compute metrics
        episode.compute_metrics()
        
        # Store
        self.all_episodes.append(episode)
        
        # Update top gallery
        self.top_episodes.append(episode)
        self.top_episodes.sort(key=lambda e: (e.total_score, -e.mean_dr), reverse=True)
        if len(self.top_episodes) > self.top_k:
            self.top_episodes = self.top_episodes[:self.top_k]
        
        # Reverse Pareto Analysis
        critical = ReversePareto.analyze(episode, RPA_THRESHOLD)
        episode.critical_indices = [idx for idx, _, _ in critical]
        episode.critical_states = [state_hash for _, state_hash, _ in critical]
        
        # Update geodesic map from ALL transitions (not just critical)
        # but weight critical moments more heavily in learning
        for trans in episode.transitions:
            state_hash = trans.state_hash()
            self.geodesic_map.update(state_hash, trans.action, trans.dark_residue)
        
        # Learn especially from critical moments
        for idx, state_hash, dr in critical:
            trans = episode.transitions[idx]
            # Double-weight critical moments
            self.geodesic_map.update(state_hash, trans.action, dr)
        
        # Adapt exploration
        self._update_exploration()
    
    def _update_exploration(self):
        """Decay exploration rate."""
        self.exploration_rate = max(MIN_EXPLORATION, 
                                   self.exploration_rate * EXPLORATION_DECAY)
    
    def should_explore(self) -> bool:
        """Decide if we should explore or exploit."""
        return np.random.random() < self.exploration_rate
    
    def get_geodesic_action(self, state: np.ndarray) -> int:
        """Get best action according to geodesic map."""
        discretized = (state * 10).astype(int)
        state_hash = hash(tuple(discretized))
        return self.geodesic_map.get_best_action(state_hash)
    
    def save_gallery(self, filename: str = "gallery.json"):
        """Persist witness state."""
        data = {
            'total_episodes': len(self.all_episodes),
            'geodesic_map_size': len(self.geodesic_map.known_states),
            'exploration_rate': self.exploration_rate,
            'top_episodes': [e.to_dict() for e in self.top_episodes],
        }
        
        path = os.path.join(GALLERY_DIR, filename)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)


# --------------------------------------------------------------------------- #
# GEODESIC-AWARE ACTION WRAPPER
# --------------------------------------------------------------------------- #

class GeodesicActionWrapper(gym.ActionWrapper):
    """
    Wraps discrete action space as continuous for SAC,
    but biases toward geodesic-recommended actions.
    """
    
    def __init__(self, env: gym.Env, witness: GeodesicWitness):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
        self.witness = witness
        self.current_state = None
    
    def action(self, action: np.ndarray) -> int:
        """
        Convert continuous action to discrete, with geodesic influence.
        """
        # Base SAC action
        sac_action = 0 if action[0] < 0.0 else 1
        
        # Should we explore?
        if self.witness.should_explore():
            return sac_action  # Trust SAC
        
        # Get geodesic recommendation
        if self.current_state is not None:
            geo_action = self.witness.get_geodesic_action(self.current_state)
            
            if geo_action >= 0:  # Valid recommendation
                # Blend: mostly trust geodesic, but allow SAC to override sometimes
                if np.random.random() < GEODESIC_INFLUENCE:
                    return geo_action
        
        return sac_action
    
    def set_state(self, state: np.ndarray):
        """Update current state for geodesic lookup."""
        self.current_state = state


# --------------------------------------------------------------------------- #
# MAIN TRAINING LOOP
# --------------------------------------------------------------------------- #

def main():
    print("=" * 80)
    print("WENDIGO GEODESIC SAC: Multi-Objective + Reverse Pareto + Geodesic Navigation")
    print("=" * 80)
    print()
    
    # Initialize
    witness = GeodesicWitness(top_k=15)
    base_env = gym.make("CartPole-v1")
    env = GeodesicActionWrapper(base_env, witness)
    
    agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))
    new_logger = configure(None, ["stdout"])
    agent.set_logger(new_logger)
    
    # Warmup replay buffer
    REPLAY_WARMUP_STEPS = 10000
    print(f"Warming up replay buffer with {REPLAY_WARMUP_STEPS} random steps...")
    obs, _ = env.reset()
    for _ in range(REPLAY_WARMUP_STEPS):
        random_action = env.action_space.sample()
        next_obs, _, done, truncated, _ = env.step(random_action)
        agent.replay_buffer.add(obs, next_obs, np.array([random_action]), 0.0, done, [{}])
        obs = next_obs
        if done or truncated:
            obs, _ = env.reset()
    print("Warmup complete. Starting training.\n")
    
    # Training
    num_episodes = 500
    MASTERY_THRESHOLD = 495
    
    for ep in range(1, num_episodes + 1):
        # Create episode witness object
        episode = Episode(episode_num=ep)
        
        obs, _ = env.reset()
        env.set_state(obs)  # For geodesic lookup
        
        done, truncated = False, False
        previous_dr = calculate_dark_residue(obs)
        
        while not done and not truncated:
            # SAC predicts action
            action, _ = agent.predict(obs, deterministic=True)
            
            # Step (action wrapper may modify based on geodesic)
            next_obs, _, done, truncated, _ = env.step(action)
            env.set_state(next_obs)
            
            # --- COMPUTE PIROUETTE REWARD ---
            current_dr = calculate_dark_residue(next_obs)
            dr_derivative = current_dr - previous_dr
            
            # 1. Coherence gain (negative derivative = good)
            coherence_gain = GAMMA_COHERENCE * max(0, -dr_derivative)
            
            # 2. Dissonance penalty
            dissonance_penalty = DELTA_DISSONANCE * current_dr
            
            # 3. Final reward
            reward = coherence_gain + BETA_DURATION - dissonance_penalty
            
            # --- WITNESS TRANSITION ---
            trans = Transition(
                state=obs.copy(),
                action=action,
                reward=reward,
                next_state=next_obs.copy(),
                done=done,
                dark_residue=current_dr,
                dr_derivative=dr_derivative,
                coherence_gain=coherence_gain,
            )
            episode.transitions.append(trans)
            
            # Train agent
            agent.replay_buffer.add(obs, next_obs, action, reward, done, [{}])
            agent.train(gradient_steps=1)
            
            obs = next_obs
            previous_dr = current_dr
        
        # Episode complete - WITNESS IT
        witness.observe(episode)
        
        # Report
        best_score = witness.top_episodes[0].total_score if witness.top_episodes else 0
        avg_top = np.mean([e.total_score for e in witness.top_episodes])
        
        print(
            f"Ep {ep:03d}: "
            f"Score={episode.total_score:3d} | "
            f"MeanDR={episode.mean_dr:.4f} | "
            f"CohGain={episode.total_coherence_gain:6.2f} | "
            f"Critical={len(episode.critical_indices):2d} | "
            f"GeoMap={len(witness.geodesic_map.known_states):4d} | "
            f"Explore={witness.exploration_rate:.3f} | "
            f"Top15Avg={avg_top:.1f} (best={best_score})"
        )
        
        # Check mastery
        if len(witness.top_episodes) == 15 and avg_top >= MASTERY_THRESHOLD:
            print(f"\n{'*' * 80}")
            print(f"*** MASTERY ACHIEVED at Episode {ep} ***")
            print(f"Top-15 Average: {avg_top:.2f}")
            print(f"Geodesic Map Size: {len(witness.geodesic_map.known_states)} states")
            print(f"{'*' * 80}\n")
            
            agent.save(os.path.join(GALLERY_DIR, "wendigo_geodesic_sac_mastery.zip"))
            witness.save_gallery("gallery_mastery.json")
            break
        
        # Periodic save
        if ep % 50 == 0:
            witness.save_gallery(f"gallery_ep{ep:03d}.json")
    
    # Final save
    witness.save_gallery("gallery_final.json")
    env.close()
    
    print("\n" + "=" * 80)
    print("TRAINING COMPLETE")
    print("=" * 80)
    print(f"\nFinal Statistics:")
    print(f"  Total Episodes: {len(witness.all_episodes)}")
    print(f"  Geodesic Map Size: {len(witness.geodesic_map.known_states)} states")
    print(f"  Final Exploration Rate: {witness.exploration_rate:.3f}")
    print(f"  Best Score: {witness.top_episodes[0].total_score if witness.top_episodes else 0}")


if __name__ == "__main__":
    main()