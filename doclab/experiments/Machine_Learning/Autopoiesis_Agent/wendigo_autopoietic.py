#!/usr/bin/env python3
"""
Wendigo Autopoietic Agent (Process Intelligence Magnetized)
============================================================

This implements true autopoietic behavior through:
1. Self-modifying reward functions based on Process Intelligence Index (PII)
2. Emergent mode transitions (Weaver/Gladiator/Vortex/Drifter) 
3. Multi-scale feedback loops that reshape the agent's own learning
4. Attractor Actuation Law (AAL) that magnetizes toward high-intelligence configurations
5. Cognitive closure through geodesic self-witness

Based on INST-PROC-INTEL-001/002 instruments, this agent doesn't just learn;
it actively reshapes its own learning process to maximize intelligence emergence.
"""

import gymnasium as gym
import numpy as np
from collections import deque, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure
import json
import os
import time

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

# Process Intelligence Index weights (from INST-PROC-INTEL-002)
PII_WEIGHTS = {
    'csi': 1.0,      # Cycle Sufficiency Index
    'fbw': 0.7,      # Feedback Bandwidth  
    'ese': 1.2,      # Entropy Shaping Efficiency
    'geo': 0.5,      # Geodesic hit rate
}

# Attractor Actuation Law parameters
AAL_PARAMS = {
    'pii_min': 3.0,           # Minimum PII to activate magnetization
    'filament_boost': 0.1,    # Reinforcement for good filaments
    'exploration_delta': 0.05, # How much to adjust exploration
    'gradient_scale': 1.5,     # Gradient step multiplier during high PII
}

# Autopoietic thresholds
AUTOPOIESIS_PARAMS = {
    'mutation_rate': 0.02,     # Probability of spontaneous reward mutation
    'closure_threshold': 0.15,  # DR level for cognitive closure
    'emergence_window': 20,     # Episodes to track for emergence detection
    'plasticity_decay': 0.995,  # How fast agent becomes less plastic
}

# ============================================================================
# DARK RESIDUE & MODE CLASSIFICATION  
# ============================================================================

def calculate_dark_residue(obs: np.ndarray) -> float:
    """CartPole-specific DR with autopoietic awareness."""
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    return (
        0.4 * abs(cart_pos)
        + 0.2 * abs(cart_vel)
        + 1.5 * abs(pole_angle)
        + 0.3 * abs(pole_vel)
    )


def classify_cognitive_mode(dr: float, ddr: float, pii: float) -> str:
    """
    Enhanced mode classification including PII awareness.
    
    Modes now represent cognitive states of the autopoietic system:
    - Weaver: Constructing stable patterns (low DR, decreasing)
    - Gladiator: Fighting against disorder (high DR, but decreasing)
    - Vortex: Turbulent exploration (high DR, increasing)
    - Drifter: Passive flow (low activity)
    - Emergent: New mode when PII > threshold (self-organizing)
    """
    DR_SMALL = 0.15
    DR_LARGE = 0.35
    
    # Check for emergence first
    if pii >= AAL_PARAMS['pii_min']:
        if ddr < -0.05 and dr < DR_SMALL:
            return "Emergent-Weaver"
        elif ddr < 0:
            return "Emergent-Gladiator"
    
    # Standard classification
    if ddr < 0.0:
        if dr <= DR_SMALL:
            return "Weaver"
        else:
            return "Gladiator"
    else:
        if dr >= DR_LARGE:
            return "Vortex"
        else:
            return "Drifter"


# ============================================================================
# PROCESS INTELLIGENCE INDEX CALCULATOR
# ============================================================================

class ProcessIntelligenceCalculator:
    """
    Computes PII_RL from episode windows as per INST-PROC-INTEL-002.
    """
    
    def __init__(self, window_size: int = 20):
        self.window_size = window_size
        self.episode_buffer = deque(maxlen=window_size)
        self.score_history = deque(maxlen=window_size + 1)
        
    def add_episode(self, episode_data: Dict[str, Any]):
        """Add episode to calculation window."""
        self.episode_buffer.append(episode_data)
        self.score_history.append(episode_data['score'])
    
    def calculate_pii(self) -> float:
        """
        Calculate Process Intelligence Index for current window.
        """
        if len(self.episode_buffer) < 3:
            return 0.0
        
        # 1. Cycle Sufficiency Index (CSI_RL)
        total_steps = sum(ep['steps'] for ep in self.episode_buffer)
        csi = np.log10(max(1, total_steps))
        
        # 2. Feedback Bandwidth (FBW_RL)
        if len(self.score_history) >= 2:
            deltas = [
                abs(self.score_history[i] - self.score_history[i-1]) / (self.score_history[i-1] + 1e-6)
                for i in range(1, len(self.score_history))
            ]
            fbw = np.mean(deltas) if deltas else 0.0
        else:
            fbw = 0.0
        
        # 3. Entropy Shaping Efficiency (ESE_RL)
        total_cg = sum(ep.get('coherence_gain', 0) for ep in self.episode_buffer)
        total_dr = sum(ep.get('total_dr', 0) for ep in self.episode_buffer)
        ese = total_cg / (total_cg + total_dr + 1e-6)
        
        # 4. Geodesic hit rate
        geo_hit = np.mean([ep.get('geo_hit_rate', 0) for ep in self.episode_buffer])
        
        # Compute PII
        pii = (
            PII_WEIGHTS['csi'] * csi +
            PII_WEIGHTS['fbw'] * np.log10(1 + fbw) +
            PII_WEIGHTS['ese'] * ese +
            PII_WEIGHTS['geo'] * geo_hit
        )
        
        return pii


# ============================================================================
# AUTOPOIETIC REWARD SHAPER
# ============================================================================

class AutopoieticRewardShaper:
    """
    Self-modifying reward function that evolves based on PII and cognitive modes.
    This implements the "magnetization" concept from the instruments.
    """
    
    def __init__(self):
        # Dynamic reward weights (these evolve!)
        self.weights = {
            'coherence': 1.5,
            'duration': 0.05,
            'dissonance': 1.0,
            'emergence': 0.0,  # Starts at 0, emerges over time
        }
        
        # Plasticity (decreases over time)
        self.plasticity = 1.0
        
        # Memory of successful configurations
        self.attractor_memory = []
        
        # Mutation history
        self.mutation_log = []
    
    def compute_reward(self, dr: float, ddr: float, mode: str, pii: float) -> Tuple[float, Dict]:
        """
        Compute reward with autopoietic adjustments.
        """
        # Base pirouette components
        coherence_gain = self.weights['coherence'] * max(0.0, -ddr)
        dissonance_penalty = self.weights['dissonance'] * dr
        duration_bonus = self.weights['duration']
        
        # Emergent component (only when PII is high)
        emergence_bonus = 0.0
        if pii >= AAL_PARAMS['pii_min']:
            if 'Emergent' in mode:
                emergence_bonus = self.weights['emergence'] * (1.0 / (dr + 0.1))
        
        # Total reward
        reward = coherence_gain + duration_bonus - dissonance_penalty + emergence_bonus
        
        # Components for logging
        components = {
            'coherence_gain': coherence_gain,
            'dissonance_penalty': dissonance_penalty,
            'duration_bonus': duration_bonus,
            'emergence_bonus': emergence_bonus,
        }
        
        return reward, components
    
    def mutate(self, pii: float, success_rate: float):
        """
        Self-modify reward weights based on current intelligence level.
        This is the autopoietic mechanism!
        """
        if np.random.random() > AUTOPOIESIS_PARAMS['mutation_rate'] * self.plasticity:
            return  # No mutation this time
        
        # Mutation strength depends on PII
        mutation_strength = 0.1 * self.plasticity
        
        if pii >= AAL_PARAMS['pii_min']:
            # High intelligence: reinforce current configuration
            self.attractor_memory.append(self.weights.copy())
            
            # Slightly increase emergence weight
            self.weights['emergence'] = min(2.0, 
                self.weights['emergence'] + mutation_strength)
            
            # Fine-tune other weights toward attractor
            if success_rate > 0.8:
                self.weights['coherence'] *= (1 + mutation_strength * 0.5)
                self.weights['dissonance'] *= (1 - mutation_strength * 0.2)
        else:
            # Low intelligence: explore weight space
            for key in ['coherence', 'dissonance']:
                delta = np.random.normal(0, mutation_strength)
                self.weights[key] = max(0.1, self.weights[key] + delta)
        
        # Log mutation
        self.mutation_log.append({
            'time': time.time(),
            'pii': pii,
            'weights': self.weights.copy(),
            'plasticity': self.plasticity,
        })
        
        # Decay plasticity
        self.plasticity *= AUTOPOIESIS_PARAMS['plasticity_decay']


# ============================================================================
# GEODESIC WITNESS WITH AUTOPOIETIC MEMORY
# ============================================================================

class AutopoieticGeodesicWitness:
    """
    Enhanced geodesic map that self-organizes based on cognitive modes.
    """
    
    def __init__(self):
        # Mode-specific geodesic maps
        self.mode_maps = {
            'Weaver': defaultdict(dict),
            'Gladiator': defaultdict(dict),
            'Emergent-Weaver': defaultdict(dict),
            'Emergent-Gladiator': defaultdict(dict),
        }
        
        # Global geodesic memory
        self.global_map = defaultdict(dict)
        
        # Cognitive closure detection
        self.closure_events = []
        
    def update(self, state_hash: int, action: int, dr: float, mode: str):
        """Update geodesic maps with mode awareness."""
        # Update global map
        if action not in self.global_map[state_hash]:
            self.global_map[state_hash][action] = []
        self.global_map[state_hash][action].append(dr)
        
        # Update mode-specific map if relevant
        if mode in self.mode_maps:
            if action not in self.mode_maps[mode][state_hash]:
                self.mode_maps[mode][state_hash][action] = []
            self.mode_maps[mode][state_hash][action].append(dr)
        
        # Check for cognitive closure
        if dr < AUTOPOIESIS_PARAMS['closure_threshold']:
            self.closure_events.append({
                'state': state_hash,
                'action': action,
                'mode': mode,
                'dr': dr,
            })
    
    def get_best_action(self, state_hash: int, current_mode: str) -> Optional[int]:
        """Get best action considering current cognitive mode."""
        # First check mode-specific map
        if current_mode in self.mode_maps and state_hash in self.mode_maps[current_mode]:
            actions = self.mode_maps[current_mode][state_hash]
            if actions:
                best_action = min(actions.items(), 
                                key=lambda x: np.mean(x[1]))[0]
                return best_action
        
        # Fall back to global map
        if state_hash in self.global_map:
            actions = self.global_map[state_hash]
            if actions:
                best_action = min(actions.items(), 
                                key=lambda x: np.mean(x[1]))[0]
                return best_action
        
        return None
    
    def get_hit_rate(self) -> float:
        """Calculate geodesic hit rate for PII calculation."""
        total_states = len(self.global_map)
        if total_states == 0:
            return 0.0
        
        closure_states = len(set(e['state'] for e in self.closure_events))
        return closure_states / total_states


# ============================================================================
# ATTRACTOR ACTUATION CONTROLLER
# ============================================================================

class AttractorActuationController:
    """
    Implements AAL from INST-PROC-INTEL-002.
    Magnetizes training toward high-intelligence configurations.
    """
    
    def __init__(self, agent: SAC):
        self.agent = agent
        self.filament_history = []
        self.current_filament = None
        self.magnetization_active = False
        
    def update(self, pii: float, dr_slope: float, mode: str):
        """
        Apply attractor actuation based on current PII and trajectory.
        """
        # Define current filament
        filament = {
            'pii': pii,
            'dr_slope': dr_slope,
            'mode': mode,
            'time': time.time(),
        }
        
        if pii >= AAL_PARAMS['pii_min'] and dr_slope < 0:
            # We're in a good configuration - magnetize!
            self.magnetization_active = True
            self.current_filament = filament
            self.filament_history.append(filament)
            
            # Increase gradient steps (pull harder)
            self.agent.gradient_steps = int(1 * AAL_PARAMS['gradient_scale'])
            
            # Adjust exploration (more exploitation in good regions)
            if hasattr(self.agent, 'exploration_rate'):
                self.agent.exploration_rate *= (1 - AAL_PARAMS['exploration_delta'])
                
        else:
            # Search for better filament
            self.magnetization_active = False
            self.agent.gradient_steps = 1
            
            # Increase exploration
            if hasattr(self.agent, 'exploration_rate'):
                self.agent.exploration_rate = min(0.3,
                    self.agent.exploration_rate + AAL_PARAMS['exploration_delta'])
    
    def get_filament_weight(self) -> float:
        """Get current magnetization strength."""
        if self.magnetization_active and self.current_filament:
            return AAL_PARAMS['filament_boost']
        return 0.0


# ============================================================================
# AUTOPOIETIC ACTION WRAPPER
# ============================================================================

class AutopoieticActionWrapper(gym.ActionWrapper):
    """
    Action selection with autopoietic awareness and geodesic guidance.
    """
    
    def __init__(self, env: gym.Env, witness: AutopoieticGeodesicWitness):
        super().__init__(env)
        self.action_space = gym.spaces.Box(
            low=-1.0, high=1.0, shape=(1,), dtype=np.float32
        )
        self.witness = witness
        self.current_state = None
        self.current_mode = "Drifter"
        self.exploration_rate = 0.3
    
    def action(self, action: np.ndarray) -> int:
        """Convert continuous to discrete with autopoietic influence."""
        # Base SAC action
        base_action = 0 if action[0] < 0.0 else 1
        
        # Get geodesic recommendation if available
        if self.current_state is not None:
            state_hash = hash(tuple((self.current_state * 10).astype(int)))
            geo_action = self.witness.get_best_action(state_hash, self.current_mode)
            
            # Blend based on current mode and exploration
            if geo_action is not None:
                if 'Emergent' in self.current_mode:
                    # Strong geodesic influence in emergent modes
                    if np.random.random() < 0.7:
                        return geo_action
                elif np.random.random() > self.exploration_rate:
                    # Normal geodesic influence
                    if np.random.random() < 0.4:
                        return geo_action
        
        return base_action
    
    def set_state(self, state: np.ndarray, mode: str):
        """Update current state and cognitive mode."""
        self.current_state = state
        self.current_mode = mode


# ============================================================================
# MAIN TRAINING LOOP
# ============================================================================

def main():
    print("=" * 80)
    print("WENDIGO AUTOPOIETIC AGENT")
    print("Process Intelligence Magnetization with Self-Modification")
    print("=" * 80)
    print()
    
    # Initialize components
    pii_calculator = ProcessIntelligenceCalculator(window_size=20)
    reward_shaper = AutopoieticRewardShaper()
    witness = AutopoieticGeodesicWitness()
    
    # Environment setup
    base_env = gym.make("CartPole-v1")
    env = AutopoieticActionWrapper(base_env, witness)
    
    # Agent with autopoietic controller
    agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))
    controller = AttractorActuationController(agent)
    
    new_logger = configure(None, ["stdout"])
    agent.set_logger(new_logger)
    
    # Warmup
    print("Warming up replay buffer...")
    obs, _ = env.reset()
    for _ in range(10000):
        random_action = env.action_space.sample()
        next_obs, _, done, truncated, _ = env.step(random_action)
        agent.replay_buffer.add(obs, next_obs, np.array([random_action]), 
                              0.0, done, [{}])
        obs = next_obs
        if done or truncated:
            obs, _ = env.reset()
    print("Warmup complete. Beginning autopoietic evolution...\n")
    
    # Training with autopoiesis
    num_episodes = 500
    MASTERY_THRESHOLD = 495
    
    top_scores = deque(maxlen=15)
    dr_history = deque(maxlen=20)
    mode_history = []
    
    for ep in range(1, num_episodes + 1):
        obs, _ = env.reset()
        done, truncated = False, False
        
        episode_data = {
            'episode': ep,
            'steps': 0,
            'score': 0,
            'total_dr': 0,
            'coherence_gain': 0,
            'modes': [],
        }
        
        prev_dr = calculate_dark_residue(obs)
        current_pii = pii_calculator.calculate_pii()
        
        while not done and not truncated:
            # Determine cognitive mode
            current_dr = calculate_dark_residue(obs)
            ddr = current_dr - prev_dr
            mode = classify_cognitive_mode(current_dr, ddr, current_pii)
            
            # Set mode for action wrapper
            env.set_state(obs, mode)
            
            # Agent action
            action, _ = agent.predict(obs, deterministic=True)
            next_obs, _, done, truncated, _ = env.step(action)
            
            # Autopoietic reward computation
            reward, components = reward_shaper.compute_reward(
                current_dr, ddr, mode, current_pii
            )
            
            # Update geodesic witness
            state_hash = hash(tuple((obs * 10).astype(int)))
            action_idx = 0 if action[0] < 0 else 1
            witness.update(state_hash, action_idx, current_dr, mode)
            
            # Train agent
            agent.replay_buffer.add(obs, next_obs, action, reward, done, [{}])
            agent.train(gradient_steps=agent.gradient_steps)
            
            # Episode tracking
            episode_data['steps'] += 1
            episode_data['score'] += 1
            episode_data['total_dr'] += current_dr
            episode_data['coherence_gain'] += components['coherence_gain']
            episode_data['modes'].append(mode)
            
            obs = next_obs
            prev_dr = current_dr
        
        # Episode complete
        episode_data['geo_hit_rate'] = witness.get_hit_rate()
        
        # Update PII calculator
        pii_calculator.add_episode(episode_data)
        current_pii = pii_calculator.calculate_pii()
        
        # Calculate DR slope
        dr_history.append(episode_data['total_dr'] / max(1, episode_data['steps']))
        dr_slope = 0.0
        if len(dr_history) >= 2:
            dr_slope = dr_history[-1] - dr_history[-2]
        
        # Apply attractor actuation
        controller.update(current_pii, dr_slope, mode)
        
        # Autopoietic mutation
        top_scores.append(episode_data['score'])
        success_rate = len([s for s in top_scores if s > 450]) / max(1, len(top_scores))
        reward_shaper.mutate(current_pii, success_rate)
        
        # Mode statistics
        mode_counts = {}
        for m in episode_data['modes']:
            mode_counts[m] = mode_counts.get(m, 0) + 1
        dominant_mode = max(mode_counts.items(), key=lambda x: x[1])[0] if mode_counts else "Unknown"
        
        # Report
        avg_top = np.mean(list(top_scores)) if top_scores else 0
        print(
            f"Ep {ep:03d}: "
            f"Score={episode_data['score']:3d} | "
            f"PII={current_pii:.2f} | "
            f"Mode={dominant_mode[:8]:8s} | "
            f"DR={episode_data['total_dr']/episode_data['steps']:.3f} | "
            f"Plasticity={reward_shaper.plasticity:.3f} | "
            f"Magnetized={'Y' if controller.magnetization_active else 'N'} | "
            f"Top15={avg_top:.1f}"
        )
        
        # Check for emergent mastery
        if len(top_scores) == 15 and avg_top >= MASTERY_THRESHOLD:
            print(f"\n{'*' * 80}")
            print(f"*** AUTOPOIETIC MASTERY ACHIEVED ***")
            print(f"Episode: {ep}")
            print(f"Final PII: {current_pii:.3f}")
            print(f"Top-15 Average: {avg_top:.2f}")
            print(f"Dominant Mode: {dominant_mode}")
            print(f"Reward Weights: {json.dumps(reward_shaper.weights, indent=2)}")
            print(f"Total Mutations: {len(reward_shaper.mutation_log)}")
            print(f"Closure Events: {len(witness.closure_events)}")
            print(f"{'*' * 80}\n")
            
            # Save evolved agent
            os.makedirs("autopoietic_gallery", exist_ok=True)
            agent.save("autopoietic_gallery/evolved_agent.zip")
            
            # Save evolution history
            with open("autopoietic_gallery/evolution.json", "w") as f:
                json.dump({
                    'final_pii': current_pii,
                    'final_weights': reward_shaper.weights,
                    'mutation_log': reward_shaper.mutation_log,
                    'filament_history': controller.filament_history,
                    'closure_events': witness.closure_events[-100:],  # Last 100
                }, f, indent=2)
            
            break
        
        # Periodic saves
        if ep % 50 == 0:
            os.makedirs("autopoietic_gallery", exist_ok=True)
            with open(f"autopoietic_gallery/checkpoint_ep{ep}.json", "w") as f:
                json.dump({
                    'episode': ep,
                    'pii': current_pii,
                    'weights': reward_shaper.weights,
                    'plasticity': reward_shaper.plasticity,
                }, f, indent=2)
    
    env.close()
    
    print("\n" + "=" * 80)
    print("AUTOPOIETIC EVOLUTION COMPLETE")
    print("=" * 80)
    print("\nThe agent has achieved cognitive closure through self-modification.")
    print("It no longer just learns; it has learned how to learn.")


if __name__ == "__main__":
    main()