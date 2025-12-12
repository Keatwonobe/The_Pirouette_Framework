#!/usr/bin/env python3
"""
Wendigo Momentum Climber: Pareto-Style Hill Exploration
--------------------------------------------------------
When the agent finds a breakthrough, it enters "momentum mode" where
each successful improvement extends exploration by 1 episode.

This captures growth sequences like: 88 → 185 → 155 → 309 → 196 → 149
The agent rides the wave of discovery instead of prematurely cutting it short.

Key Innovation: Dynamic window that grows with success, shrinks with plateau.
"""
import gymnasium as gym
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure
from collections import deque
from dataclasses import dataclass, field
from typing import Optional, List, Dict
import os
import copy

# --------------------------------------------------------------------------- #
# CONFIGURATION
# --------------------------------------------------------------------------- #

GALLERY_DIR = "gallery_momentum_climber"
os.makedirs(GALLERY_DIR, exist_ok=True)

# Pirouette reward parameters
GAMMA_COHERENCE = 1.5
BETA_DURATION = 0.05
DELTA_DISSONANCE = 1.0

# Momentum climbing parameters
BREAKTHROUGH_MULTIPLIER = 1.3  # Lower threshold - we want to catch growth early
BREAKTHROUGH_ABSOLUTE = 30  # Minimum absolute improvement
INITIAL_CLIMB_WINDOW = 5  # Start with smaller window
MOMENTUM_EXTENSION = 1  # Extend by 1 episode per improvement
MAX_CLIMB_WINDOW = 25  # Cap to prevent infinite climbing
PLATEAU_TOLERANCE = 3  # Episodes without improvement before giving up

SCORE_WINDOW = 20


# --------------------------------------------------------------------------- #
# DARK RESIDUE CALCULATION
# --------------------------------------------------------------------------- #

def calculate_dark_residue_cartpole(obs: np.ndarray) -> float:
    """CartPole-specific DR."""
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    return (0.4 * abs(cart_pos) + 
            0.2 * abs(cart_vel) + 
            1.5 * abs(pole_angle) + 
            0.3 * abs(pole_vel))


def calculate_dark_residue_ant(obs: np.ndarray) -> float:
    """Ant-specific DR: focus on torso orientation and velocity control."""
    if len(obs) < 13:
        return 0.0
    
    z_pos = obs[0]
    orientations = obs[1:5]
    joint_angles = obs[5:13]
    velocities = obs[13:] if len(obs) > 13 else np.zeros(14)
    
    z_penalty = max(0, 0.3 - z_pos) * 10
    orientation_penalty = np.sum(np.abs(orientations - [1, 0, 0, 0])) * 2
    joint_penalty = np.sum(np.abs(joint_angles)) * 0.1
    velocity_chaos = np.sum(np.abs(velocities)) * 0.01
    
    return z_penalty + orientation_penalty + joint_penalty + velocity_chaos


# --------------------------------------------------------------------------- #
# ACTION WRAPPER
# --------------------------------------------------------------------------- #

class DiscreteToBoxActionWrapper(gym.ActionWrapper):
    """Converts discrete action space to continuous for SAC."""
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

    def action(self, action: np.ndarray) -> int:
        return 0 if action[0] < 0.0 else 1


# --------------------------------------------------------------------------- #
# MOMENTUM CLIMBER
# --------------------------------------------------------------------------- #

@dataclass
class MomentumRun:
    """Tracks a sequence of improving episodes."""
    start_episode: int
    start_score: int
    scores: List[int] = field(default_factory=list)
    best_score: int = 0
    episodes_since_improvement: int = 0
    total_extensions: int = 0
    
    def add_score(self, score: int) -> bool:
        """
        Add score to run. Returns True if this improves the best.
        """
        self.scores.append(score)
        
        if score > self.best_score:
            self.best_score = score
            self.episodes_since_improvement = 0
            return True
        else:
            self.episodes_since_improvement += 1
            return False
    
    def should_continue(self, max_window: int, tolerance: int) -> bool:
        """Should we keep climbing?"""
        if len(self.scores) >= max_window:
            return False
        if self.episodes_since_improvement >= tolerance:
            return False
        return True
    
    def get_summary(self) -> Dict:
        """Summary statistics."""
        return {
            'duration': len(self.scores),
            'start_score': self.start_score,
            'best_score': self.best_score,
            'final_score': self.scores[-1] if self.scores else 0,
            'improvements': sum(1 for i in range(1, len(self.scores)) 
                              if self.scores[i] > max(self.scores[:i])),
            'extensions': self.total_extensions,
        }


class MomentumClimber:
    """
    Detects breakthroughs and manages momentum-based exploration.
    
    The key insight: extend exploration dynamically based on continued success.
    Each improvement adds 1 more episode to explore. Stop after 3 episodes
    without improvement or hitting max window.
    """
    
    def __init__(self, score_window: int = SCORE_WINDOW):
        self.score_history = deque(maxlen=score_window)
        self.current_run: Optional[MomentumRun] = None
        self.completed_runs: List[MomentumRun] = []
        self.total_breakthroughs = 0
        
    def record_score(self, score: int):
        """Add score to history."""
        self.score_history.append(score)
    
    def get_baseline(self) -> float:
        """Current performance baseline."""
        if len(self.score_history) < 5:
            return 0.0
        return np.mean(self.score_history)
    
    def is_breakthrough(self, score: int, ep_num: int) -> bool:
        """
        Check if this score represents a breakthrough.
        Only triggers if we're NOT already in a momentum run.
        """
        if self.current_run is not None:
            return False  # Already climbing
        
        if len(self.score_history) < 5:
            return False
        
        baseline = self.get_baseline()
        threshold = baseline * BREAKTHROUGH_MULTIPLIER
        absolute_improvement = score - baseline
        
        return (score >= threshold and 
                absolute_improvement >= BREAKTHROUGH_ABSOLUTE)
    
    def start_momentum_run(self, episode_num: int, score: int):
        """Begin a new momentum exploration run."""
        self.current_run = MomentumRun(
            start_episode=episode_num,
            start_score=score,
            best_score=score
        )
        self.current_run.add_score(score)
        self.total_breakthroughs += 1
        
        print(f"\n{'='*70}")
        print(f"🚀 MOMENTUM MODE ACTIVATED")
        print(f"   Episode {episode_num}: Score {score}")
        print(f"   Baseline: {self.get_baseline():.1f}")
        print(f"   Initial window: {INITIAL_CLIMB_WINDOW} episodes")
        print(f"   Will extend +1 episode per improvement (max {MAX_CLIMB_WINDOW})")
        print(f"{'='*70}\n")
    
    def update_momentum(self, score: int) -> Dict:
        """
        Update current momentum run with new score.
        Returns status dict.
        """
        if self.current_run is None:
            return {'climbing': False}
        
        improved = self.current_run.add_score(score)
        
        if improved:
            # Extend the window!
            self.current_run.total_extensions += 1
            extension_msg = f"✨ +{score-self.current_run.best_score} improvement! Window extended."
        else:
            extension_msg = ""
        
        # Check if we should continue
        should_continue = self.current_run.should_continue(
            MAX_CLIMB_WINDOW, 
            PLATEAU_TOLERANCE
        )
        
        remaining = max(0, INITIAL_CLIMB_WINDOW + 
                       self.current_run.total_extensions - 
                       len(self.current_run.scores))
        
        if not should_continue:
            self._end_momentum_run()
            return {
                'climbing': False,
                'just_finished': True,
                'extension_msg': extension_msg
            }
        
        return {
            'climbing': True,
            'remaining': remaining,
            'best': self.current_run.best_score,
            'improved': improved,
            'extension_msg': extension_msg,
            'plateau_count': self.current_run.episodes_since_improvement,
            'total_extensions': self.current_run.total_extensions,
        }
    
    def _end_momentum_run(self):
        """Complete the current momentum run."""
        if self.current_run is None:
            return
        
        summary = self.current_run.get_summary()
        self.completed_runs.append(self.current_run)
        
        print(f"\n{'='*70}")
        print(f"🏁 MOMENTUM RUN COMPLETE")
        print(f"   Duration: {summary['duration']} episodes")
        print(f"   Start → Best: {summary['start_score']} → {summary['best_score']}")
        print(f"   Improvements found: {summary['improvements']}")
        print(f"   Extensions earned: {summary['extensions']}")
        print(f"   {'Plateau reached' if summary['best_score'] == summary['final_score'] else 'Ended on decline'}")
        print(f"{'='*70}\n")
        
        self.current_run = None
    
    def is_climbing(self) -> bool:
        """Are we currently in momentum mode?"""
        return self.current_run is not None
    
    def get_stats(self) -> Dict:
        """Overall statistics."""
        return {
            'total_breakthroughs': self.total_breakthroughs,
            'completed_runs': len(self.completed_runs),
            'currently_climbing': self.is_climbing(),
            'best_run': max((r.best_score for r in self.completed_runs), default=0),
        }


# --------------------------------------------------------------------------- #
# TRAINING
# --------------------------------------------------------------------------- #

def train_environment(env_name: str, calc_dr_fn, mastery_threshold: int, 
                     agent: Optional[SAC] = None, starting_episode: int = 1):
    """Train on a single environment with momentum climbing."""
    
    print(f"\n{'='*80}")
    print(f"Training on {env_name}")
    print(f"Mastery Threshold: {mastery_threshold}")
    print(f"{'='*80}\n")
    
    # Create environment
    if env_name == "CartPole-v1":
        base_env = gym.make(env_name)
        env = DiscreteToBoxActionWrapper(base_env)
    else:
        env = gym.make(env_name)
    
    # Create or reuse agent
    if agent is None:
        agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))
        new_logger = configure(None, ["stdout"])
        agent.set_logger(new_logger)
        
        # Warmup
        print(f"Warming up replay buffer...")
        obs, _ = env.reset()
        for _ in range(10000):
            random_action = env.action_space.sample()
            next_obs, _, done, truncated, _ = env.step(random_action)
            agent.replay_buffer.add(obs, next_obs, random_action, 0.0, done, [{}])
            obs = next_obs
            if done or truncated:
                obs, _ = env.reset()
        print("Warmup complete.\n")
    
    # Momentum climbing manager
    climber = MomentumClimber()
    
    # Top scores tracking
    top_scores = []
    
    # Training loop
    max_episodes = 1000
    
    for ep in range(starting_episode, starting_episode + max_episodes):
        # Run episode
        obs, _ = env.reset()
        done, truncated = False, False
        score = 0
        previous_dr = calc_dr_fn(obs)
        dr_sum = 0.0
        
        while not done and not truncated:
            # Get action
            action, _ = agent.predict(obs, deterministic=True)
            next_obs, _, done, truncated, _ = env.step(action)
            
            # Compute Pirouette reward
            current_dr = calc_dr_fn(next_obs)
            dr_derivative = current_dr - previous_dr
            
            coherence_gain = GAMMA_COHERENCE * max(0, -dr_derivative)
            dissonance_penalty = DELTA_DISSONANCE * current_dr
            reward = coherence_gain + BETA_DURATION - dissonance_penalty
            
            # Train
            agent.replay_buffer.add(obs, next_obs, action, reward, done, [{}])
            agent.train(gradient_steps=1)
            
            obs = next_obs
            previous_dr = current_dr
            dr_sum += current_dr
            score += 1
        
        # Episode complete
        mean_dr = dr_sum / max(score, 1)
        
        # Update tracking
        top_scores.append(score)
        top_scores.sort(reverse=True)
        top_scores = top_scores[:15]
        avg_top = np.mean(top_scores)
        
        # Check for breakthrough (only if not already climbing)
        if climber.is_breakthrough(score, ep):
            climber.start_momentum_run(ep, score)
        
        # Update momentum state
        status = {'climbing': False}
        if climber.is_climbing():
            status = climber.update_momentum(score)
        else:
            # Not climbing, add to baseline
            climber.record_score(score)
        
        # Build status message
        if status['climbing']:
            ext_msg = f" {status['extension_msg']}" if status['extension_msg'] else ""
            status_msg = (f" [⛰️  Momentum: {status['remaining']} remaining, "
                         f"best={status['best']}, "
                         f"plateau={status['plateau_count']}, "
                         f"ext={status['total_extensions']}]{ext_msg}")
        elif status.get('just_finished'):
            status_msg = f" [✅ Momentum run ended]{' ' + status['extension_msg'] if status['extension_msg'] else ''}"
        else:
            status_msg = ""
        
        # Report
        stats = climber.get_stats()
        print(
            f"Ep {ep:04d}: Score={score:4d} | "
            f"MeanDR={mean_dr:.4f} | "
            f"Top15Avg={avg_top:.1f} | "
            f"Baseline={climber.get_baseline():.1f} | "
            f"Runs={stats['completed_runs']}"
            f"{status_msg}"
        )
        
        # Check mastery
        if len(top_scores) == 15 and avg_top >= mastery_threshold:
            print(f"\n{'*'*80}")
            print(f"*** {env_name} MASTERY ACHIEVED ***")
            print(f"Episode {ep}: Top-15 Average = {avg_top:.2f}")
            print(f"Total momentum runs: {stats['completed_runs']}")
            print(f"Best score in any run: {stats['best_run']}")
            print(f"{'*'*80}\n")
            
            agent.save(os.path.join(GALLERY_DIR, f"{env_name.lower().replace('-', '_')}_mastery.zip"))
            env.close()
            return agent, ep
    
    env.close()
    return agent, starting_episode + max_episodes


def main():
    print("=" * 80)
    print("WENDIGO MOMENTUM CLIMBER: Pareto-Style Dynamic Exploration")
    print("=" * 80)
    print()
    
    # Train CartPole first
    agent, final_ep = train_environment(
        "CartPole-v1",
        calculate_dark_residue_cartpole,
        495  # CartPole mastery
    )
    
    # Graduate to Ant
    agent, final_ep = train_environment(
        "Ant-v5",
        calculate_dark_residue_ant,
        5000,  # Ant mastery (adjust as needed)
        agent=agent,
        starting_episode=final_ep + 1
    )
    
    print("\n" + "=" * 80)
    print("MULTI-ENVIRONMENT TRAINING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()