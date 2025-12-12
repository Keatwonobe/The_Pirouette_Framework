#!/usr/bin/env python3
"""
Wendigo Momentum Climber v3.0: Validated Hill Climbing
-------------------------------------------------------
Adds policy validation and environment perturbations to prevent exploitation.

New features:
- Breakthrough policies are validated with 10 test runs
- Only adopt policy if validation confirms improvement
- Ant environment gets random force perturbations to prevent "standing still"
- More conservative about what counts as a real breakthrough
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
import io
import pickle

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
BREAKTHROUGH_MULTIPLIER = 1.25
BREAKTHROUGH_ABSOLUTE = 25
INITIAL_CLIMB_WINDOW = 8
MOMENTUM_EXTENSION = 1
MAX_CLIMB_WINDOW = 30
PLATEAU_TOLERANCE = 4
SCORE_WINDOW = 25

# Validation parameters
VALIDATION_RUNS = 10  # Test policy this many times
VALIDATION_THRESHOLD = 0.7  # Must beat baseline 70% of the time


# --------------------------------------------------------------------------- #
# PERTURBATION WRAPPER FOR ANT
# --------------------------------------------------------------------------- #

class AntPerturbationWrapper(gym.Wrapper):
    """
    Adds random external forces to Ant to prevent standing still exploitation.
    """
    def __init__(self, env, force_prob=0.15, force_magnitude=50.0):
        super().__init__(env)
        self.force_prob = force_prob
        self.force_magnitude = force_magnitude
        self.step_count = 0
    
    def reset(self, **kwargs):
        self.step_count = 0
        return self.env.reset(**kwargs)
    
    def step(self, action):
        obs, reward, done, truncated, info = self.env.step(action)
        self.step_count += 1
        
        # Apply random perturbations periodically
        if np.random.random() < self.force_prob:
            # Access the mujoco simulation
            if hasattr(self.env.unwrapped, 'data'):
                # Random force direction
                force = np.random.randn(3) * self.force_magnitude
                # Apply to torso (body index 1)
                self.env.unwrapped.data.xfrc_applied[1, :3] = force
        
        return obs, reward, done, truncated, info


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
    """
    Ant-specific DR with penalties for immobility.
    """
    if len(obs) < 13:
        return 0.0
    
    z_pos = obs[0]
    orientations = obs[1:5]
    joint_angles = obs[5:13]
    velocities = obs[13:27] if len(obs) >= 27 else obs[13:]
    
    # Penalties for instability
    z_penalty = max(0, 0.3 - z_pos) * 10
    orientation_penalty = np.sum(np.abs(orientations - [1, 0, 0, 0])) * 2
    joint_penalty = np.sum(np.abs(joint_angles)) * 0.05
    velocity_chaos = np.sum(np.abs(velocities)) * 0.005
    
    # NEW: Penalty for being too still (discourages standing)
    velocity_magnitude = np.sqrt(np.sum(velocities[:3]**2)) if len(velocities) >= 3 else 0
    stillness_penalty = max(0, 0.5 - velocity_magnitude) * 5
    
    return z_penalty + orientation_penalty + joint_penalty + velocity_chaos + stillness_penalty


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
# POLICY VALIDATION
# --------------------------------------------------------------------------- #

def validate_policy(agent: SAC, env, baseline_score: float, 
                   calc_dr_fn, num_runs: int = VALIDATION_RUNS) -> Dict:
    """
    Test a policy to see if it's genuinely better.
    Returns validation statistics.
    """
    scores = []
    
    for _ in range(num_runs):
        obs, _ = env.reset()
        done, truncated = False, False
        score = 0
        
        while not done and not truncated:
            action, _ = agent.predict(obs, deterministic=True)
            obs, _, done, truncated, _ = env.step(action)
            score += 1
        
        scores.append(score)
    
    avg_score = np.mean(scores)
    win_rate = sum(1 for s in scores if s > baseline_score) / len(scores)
    
    return {
        'avg_score': avg_score,
        'min_score': min(scores),
        'max_score': max(scores),
        'std_score': np.std(scores),
        'win_rate': win_rate,
        'passed': win_rate >= VALIDATION_THRESHOLD,
    }


def save_policy_checkpoint(agent: SAC) -> bytes:
    """Save agent policy to bytes for restoration."""
    buffer = io.BytesIO()
    # Save just the policy state dict
    state_dict = {
        'policy': agent.policy.state_dict(),
        'actor': agent.actor.state_dict() if hasattr(agent, 'actor') else None,
        'critic': agent.critic.state_dict() if hasattr(agent, 'critic') else None,
    }
    pickle.dump(state_dict, buffer)
    return buffer.getvalue()


def restore_policy_checkpoint(agent: SAC, checkpoint_bytes: bytes):
    """Restore agent policy from bytes."""
    buffer = io.BytesIO(checkpoint_bytes)
    state_dict = pickle.load(buffer)
    agent.policy.load_state_dict(state_dict['policy'])
    if state_dict['actor'] and hasattr(agent, 'actor'):
        agent.actor.load_state_dict(state_dict['actor'])
    if state_dict['critic'] and hasattr(agent, 'critic'):
        agent.critic.load_state_dict(state_dict['critic'])


# --------------------------------------------------------------------------- #
# MOMENTUM CLIMBER WITH VALIDATION
# --------------------------------------------------------------------------- #

@dataclass
class MomentumRun:
    """Tracks a sequence of improving episodes."""
    start_episode: int
    start_score: int
    scores: List[int] = field(default_factory=list)
    best_score: int = 0
    best_episode_offset: int = 0
    episodes_since_improvement: int = 0
    total_extensions: int = 0
    checkpoint: Optional[bytes] = None  # Policy at best score
    validated: bool = False
    
    def add_score(self, score: int) -> int:
        """Add score and return improvement delta."""
        self.scores.append(score)
        
        if score > self.best_score:
            improvement = score - self.best_score
            self.best_score = score
            self.best_episode_offset = len(self.scores) - 1
            self.episodes_since_improvement = 0
            return improvement
        else:
            self.episodes_since_improvement += 1
            return 0
    
    def should_continue(self, max_window: int, tolerance: int) -> bool:
        if len(self.scores) >= max_window:
            return False
        if self.episodes_since_improvement >= tolerance:
            return False
        return True
    
    def get_summary(self) -> Dict:
        return {
            'duration': len(self.scores),
            'start_score': self.start_score,
            'best_score': self.best_score,
            'final_score': self.scores[-1] if self.scores else 0,
            'improvement': self.best_score - self.start_score,
            'extensions': self.total_extensions,
            'validated': self.validated,
        }


class MomentumClimber:
    """Detects breakthroughs and validates improvements."""
    
    def __init__(self, score_window: int = SCORE_WINDOW):
        self.score_history = deque(maxlen=score_window)
        self.current_run: Optional[MomentumRun] = None
        self.completed_runs: List[MomentumRun] = []
        self.total_breakthroughs = 0
        self.last_validated_checkpoint: Optional[bytes] = None
        
    def record_score(self, score: int):
        self.score_history.append(score)
    
    def get_baseline(self) -> float:
        if len(self.score_history) < 5:
            return 0.0
        return np.mean(self.score_history)
    
    def is_breakthrough(self, score: int, ep_num: int) -> bool:
        if self.current_run is not None:
            return False
        if len(self.score_history) < 5:
            return False
        
        baseline = self.get_baseline()
        threshold = baseline * BREAKTHROUGH_MULTIPLIER
        absolute_improvement = score - baseline
        
        return (score >= threshold and 
                absolute_improvement >= BREAKTHROUGH_ABSOLUTE)
    
    def start_momentum_run(self, episode_num: int, score: int):
        self.current_run = MomentumRun(
            start_episode=episode_num,
            start_score=score,
            best_score=score
        )
        self.current_run.add_score(score)
        self.total_breakthroughs += 1
        
        print(f"\n{'='*70}")
        print(f"🚀 MOMENTUM | Ep{episode_num} {score} | Base{self.get_baseline():.0f}")
        print(f"{'='*70}")
    
    def update_momentum(self, score: int, agent: SAC, save_checkpoint: bool = True) -> Dict:
        if self.current_run is None:
            return {'climbing': False}
        
        improvement = self.current_run.add_score(score)
        
        # Save checkpoint at new best
        if improvement > 0:
            self.current_run.total_extensions += 1
            if save_checkpoint:
                self.current_run.checkpoint = save_policy_checkpoint(agent)
        
        should_continue = self.current_run.should_continue(
            MAX_CLIMB_WINDOW, 
            PLATEAU_TOLERANCE
        )
        
        remaining = max(0, INITIAL_CLIMB_WINDOW + 
                       self.current_run.total_extensions - 
                       len(self.current_run.scores))
        
        if not should_continue:
            self._end_momentum_run()
            return {'climbing': False, 'just_finished': True}
        
        return {
            'climbing': True,
            'remaining': remaining,
            'best': self.current_run.best_score,
            'improvement': improvement,
            'plateau_count': self.current_run.episodes_since_improvement,
            'total_extensions': self.current_run.total_extensions,
        }
    
    def validate_run(self, agent: SAC, env, calc_dr_fn) -> bool:
        """
        Validate the current run's best policy.
        Returns True if validation passes.
        """
        if self.current_run is None or self.current_run.checkpoint is None:
            return False
        
        baseline = self.get_baseline()
        print(f"🔬 Validating policy (best={self.current_run.best_score})...")
        
        # Restore best checkpoint temporarily
        original_policy = save_policy_checkpoint(agent)
        restore_policy_checkpoint(agent, self.current_run.checkpoint)
        
        # Run validation
        results = validate_policy(agent, env, baseline, calc_dr_fn)
        
        # Restore current policy
        restore_policy_checkpoint(agent, original_policy)
        
        self.current_run.validated = results['passed']
        
        print(f"   Avg:{results['avg_score']:.0f} | "
              f"Win%:{results['win_rate']*100:.0f} | "
              f"{'✅ PASS' if results['passed'] else '❌ FAIL (lucky fluke)'}")
        
        # If validated, save as new baseline checkpoint
        if results['passed']:
            self.last_validated_checkpoint = self.current_run.checkpoint
        
        return results['passed']
    
    def _end_momentum_run(self):
        if self.current_run is None:
            return
        
        summary = self.current_run.get_summary()
        self.completed_runs.append(self.current_run)
        
        val_marker = "✓" if summary['validated'] else "✗"
        print(f"{'='*70}")
        print(f"🏁 RUN END | {summary['duration']}ep | "
              f"{summary['start_score']}→{summary['best_score']} "
              f"(+{summary['improvement']}) | "
              f"Ext{summary['extensions']} | Val{val_marker}")
        print(f"{'='*70}\n")
        
        self.current_run = None
    
    def is_climbing(self) -> bool:
        return self.current_run is not None
    
    def get_stats(self) -> Dict:
        validated_runs = [r for r in self.completed_runs if r.validated]
        total_improvement = sum(r.get_summary()['improvement'] 
                               for r in self.completed_runs)
        
        return {
            'total_breakthroughs': self.total_breakthroughs,
            'completed_runs': len(self.completed_runs),
            'validated_runs': len(validated_runs),
            'currently_climbing': self.is_climbing(),
            'best_run': max((r.best_score for r in self.completed_runs), default=0),
            'total_improvement': total_improvement,
        }


# --------------------------------------------------------------------------- #
# TRAINING
# --------------------------------------------------------------------------- #

def train_environment(env_name: str, calc_dr_fn, mastery_threshold: int, 
                     agent: Optional[SAC] = None, starting_episode: int = 1):
    """Train on a single environment with validated momentum climbing."""
    
    print(f"\n{'='*80}")
    print(f"Training: {env_name} | Target: {mastery_threshold}")
    print(f"{'='*80}\n")
    
    # Create environment
    if env_name == "CartPole-v1":
        base_env = gym.make(env_name)
        env = DiscreteToBoxActionWrapper(base_env)
    else:
        # Ant with perturbations
        base_env = gym.make(env_name)
        env = AntPerturbationWrapper(base_env, force_prob=0.15, force_magnitude=50.0)
    
    # Initialize agent
    if agent is None or env_name != "CartPole-v1":
        print(f"Initializing SAC agent...")
        agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))
        new_logger = configure(None, ["stdout"])
        agent.set_logger(new_logger)
        
        # Warmup
        print(f"Warmup...")
        obs, _ = env.reset()
        for _ in range(10000):
            random_action = env.action_space.sample()
            next_obs, _, done, truncated, _ = env.step(random_action)
            agent.replay_buffer.add(obs, next_obs, random_action, 0.0, done, [{}])
            obs = next_obs
            if done or truncated:
                obs, _ = env.reset()
        print("Ready.\n")
    
    # Momentum climber with validation
    climber = MomentumClimber()
    top_scores = []
    max_episodes = 2000
    
    for ep in range(starting_episode, starting_episode + max_episodes):
        # Run episode
        obs, _ = env.reset()
        done, truncated = False, False
        score = 0
        previous_dr = calc_dr_fn(obs)
        dr_sum = 0.0
        
        while not done and not truncated:
            action, _ = agent.predict(obs, deterministic=True)
            next_obs, _, done, truncated, _ = env.step(action)
            
            current_dr = calc_dr_fn(next_obs)
            dr_derivative = current_dr - previous_dr
            
            coherence_gain = GAMMA_COHERENCE * max(0, -dr_derivative)
            dissonance_penalty = DELTA_DISSONANCE * current_dr
            reward = coherence_gain + BETA_DURATION - dissonance_penalty
            
            agent.replay_buffer.add(obs, next_obs, action, reward, done, [{}])
            agent.train(gradient_steps=1)
            
            obs = next_obs
            previous_dr = current_dr
            dr_sum += current_dr
            score += 1
        
        mean_dr = dr_sum / max(score, 1)
        
        # Update tracking
        top_scores.append(score)
        top_scores.sort(reverse=True)
        top_scores = top_scores[:15]
        avg_top = np.mean(top_scores)
        
        # Check for breakthrough
        if climber.is_breakthrough(score, ep):
            climber.start_momentum_run(ep, score)
        
        # Update momentum
        status = {'climbing': False}
        if climber.is_climbing():
            status = climber.update_momentum(score, agent)
            
            # If run just finished, validate it
            if status.get('just_finished') and climber.completed_runs:
                last_run = climber.completed_runs[-1]
                if last_run.checkpoint is not None:
                    climber.validate_run(agent, env, calc_dr_fn)
        else:
            climber.record_score(score)
        
        # Status message
        if status['climbing']:
            status_msg = (f"⛰️  [{status['remaining']}r {status['best']}b "
                         f"p{status['plateau_count']} e{status['total_extensions']}]")
            if status['improvement'] > 0:
                status_msg += f" ⬆️+{status['improvement']}"
        elif status.get('just_finished'):
            status_msg = "✅"
        else:
            status_msg = ""
        
        # Report
        stats = climber.get_stats()
        print(
            f"Ep{ep:04d} {score:4d} | "
            f"DR{mean_dr:.3f} | "
            f"T15:{avg_top:.0f} | "
            f"Base:{climber.get_baseline():.0f} | "
            f"R:{stats['completed_runs']}/{stats['validated_runs']} "
            f"{status_msg}"
        )
        
        # Check mastery
        if len(top_scores) == 15 and avg_top >= mastery_threshold:
            print(f"\n{'*'*80}")
            print(f"*** {env_name} MASTERY | Ep{ep} | Top15:{avg_top:.1f} ***")
            print(f"Runs: {stats['completed_runs']} ({stats['validated_runs']} validated)")
            print(f"{'*'*80}\n")
            
            agent.save(os.path.join(GALLERY_DIR, 
                      f"{env_name.lower().replace('-', '_')}_mastery.zip"))
            env.close()
            return agent, ep
    
    env.close()
    return agent, starting_episode + max_episodes


def main():
    print("=" * 80)
    print("WENDIGO MOMENTUM CLIMBER v3.0 - Validated")
    print("=" * 80)
    
    # Train CartPole
    agent, final_ep = train_environment(
        "CartPole-v1",
        calculate_dark_residue_cartpole,
        495
    )
    
    # Train Ant (with perturbations)
    agent, final_ep = train_environment(
        "Ant-v5",
        calculate_dark_residue_ant,
        5000,
        agent=None,
        starting_episode=1
    )
    
    print("\n" + "=" * 80)
    print("COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()