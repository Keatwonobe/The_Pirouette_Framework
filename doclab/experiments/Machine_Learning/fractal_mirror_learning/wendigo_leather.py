#!/usr/bin/env python3
"""
wendigo_geodesic_universal.py
------------------------------
Universal Geodesic Navigation with Reverse Pareto Analysis.

Scales from CartPole → Pendulum → Ant → Humanoid

Key adaptations for continuous/complex tasks:
- State discretization with adaptive resolution
- Action clustering for continuous action spaces
- Multi-scale geodesic maps (coarse → fine)
- Dynamic RPA threshold based on task complexity
- Curriculum learning: start simple, auto-advance on mastery
"""
import gymnasium as gym
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional
import json
import os
import time
import hashlib

# --------------------------------------------------------------------------- #
# TASK CURRICULUM
# --------------------------------------------------------------------------- #

TASK_CURRICULUM = [
    {
        'name': 'CartPole',
        'env_id': 'CartPole-v1',
        'is_discrete': True,
        'mastery_threshold': 495,
        'mastery_episodes': 15,
        'max_episodes': 200,
        'state_discretization': 10,
        'gamma_coherence': 1.5,
        'beta_duration': 0.05,
        'delta_dissonance': 1.0,
    },
    {
        'name': 'Pendulum',
        'env_id': 'Pendulum-v1',
        'is_discrete': False,
        'mastery_threshold': -150,  # Pendulum uses negative rewards
        'mastery_episodes': 15,
        'max_episodes': 300,
        'state_discretization': 5,
        'action_clusters': 7,
        'gamma_coherence': 2.0,
        'beta_duration': 0.1,
        'delta_dissonance': 0.5,
    },
    {
        'name': 'Ant',
        'env_id': 'Ant-v5',
        'is_discrete': False,
        'mastery_threshold': 5000,
        'mastery_episodes': 10,
        'max_episodes': 1000,
        'state_discretization': 3,
        'action_clusters': 5,
        'gamma_coherence': 1.0,
        'beta_duration': 0.5,
        'delta_dissonance': 0.2,
    },
    {
        'name': 'Humanoid',
        'env_id': 'Humanoid-v5',
        'is_discrete': False,
        'mastery_threshold': 8000,
        'mastery_episodes': 5,
        'max_episodes': 2000,
        'state_discretization': 2,
        'action_clusters': 3,
        'gamma_coherence': 0.8,
        'beta_duration': 1.0,
        'delta_dissonance': 0.1,
    }
]

GALLERY_DIR = "gallery_geodesic_curriculum"
os.makedirs(GALLERY_DIR, exist_ok=True)

# --------------------------------------------------------------------------- #
# UNIVERSAL DARK RESIDUE
# --------------------------------------------------------------------------- #

class DarkResidueCalculator:
    """
    Task-agnostic DR calculation.
    
    Measures:
    1. State deviation from origin (normalized)
    2. State velocity (rate of change)
    3. Action jank (L2 distance from previous)
    """
    
    def __init__(self, obs_space, action_space):
        self.obs_dim = obs_space.shape[0] if hasattr(obs_space, 'shape') else 1
        self.action_dim = action_space.shape[0] if hasattr(action_space, 'shape') else 1
        
        # Adaptive normalization
        self.obs_scale = np.ones(self.obs_dim)
        self.action_scale = 1.0
        
        # Running statistics
        self.obs_history = deque(maxlen=1000)
        self.action_history = deque(maxlen=1000)
    
    def update_scales(self):
        """Update normalization scales from history."""
        if len(self.obs_history) > 10:
            obs_array = np.array(list(self.obs_history))
            self.obs_scale = np.std(obs_array, axis=0) + 1e-6
        
        if len(self.action_history) > 10:
            action_array = np.array(list(self.action_history))
            self.action_scale = np.std(action_array) + 1e-6
    
    def calculate(self, obs: np.ndarray, prev_obs: Optional[np.ndarray] = None,
                  action: Optional[np.ndarray] = None, prev_action: Optional[np.ndarray] = None) -> float:
        """
        Universal DR calculation.
        """
        self.obs_history.append(obs)
        if action is not None:
            self.action_history.append(action)
        
        # Periodically update scales
        if len(self.obs_history) % 100 == 0:
            self.update_scales()
        
        dr = 0.0
        
        # 1. State deviation (distance from stable region)
        state_deviation = np.sum(np.abs(obs / self.obs_scale))
        dr += 0.3 * state_deviation / self.obs_dim
        
        # 2. State velocity (if we have previous observation)
        if prev_obs is not None:
            velocity = np.linalg.norm((obs - prev_obs) / self.obs_scale)
            dr += 0.3 * velocity
        
        # 3. Action jank (if we have previous action)
        if action is not None and prev_action is not None:
            action_flat = np.array(action).flatten()
            prev_action_flat = np.array(prev_action).flatten()
            jank = np.linalg.norm(action_flat - prev_action_flat) / self.action_scale
            dr += 0.4 * jank
        
        return max(0.01, dr)  # Keep floor


# --------------------------------------------------------------------------- #
# UNIVERSAL STATE DISCRETIZATION
# --------------------------------------------------------------------------- #

class StateDiscretizer:
    """
    Adaptive state discretization for geodesic map indexing.
    
    Uses multi-resolution hashing: coarse for exploration, fine for exploitation.
    """
    
    def __init__(self, resolution: int = 10):
        self.resolution = resolution
        
    def discretize(self, state: np.ndarray, scale: int = 1) -> int:
        """
        Hash state at given resolution scale.
        scale=1: finest resolution
        scale=2: 2x coarser, etc.
        """
        effective_res = self.resolution // scale
        discretized = (state * effective_res).astype(int)
        
        # Use hashlib for consistent hashing across large state spaces
        state_bytes = discretized.tobytes()
        hash_obj = hashlib.md5(state_bytes)
        return int(hash_obj.hexdigest()[:8], 16)  # Use first 8 hex digits


# --------------------------------------------------------------------------- #
# ACTION CLUSTERING (for continuous action spaces)
# --------------------------------------------------------------------------- #

class ActionClusterer:
    """
    Clusters continuous actions into discrete representatives for geodesic map.
    """
    
    def __init__(self, action_dim: int, num_clusters: int = 7):
        self.action_dim = action_dim
        self.num_clusters = num_clusters
        
        # Initialize cluster centers uniformly in [-1, 1]^d
        self.centers = np.linspace(-1, 1, num_clusters)
        if action_dim > 1:
            # For multi-dimensional actions, use grid
            axes = [np.linspace(-1, 1, max(3, num_clusters // action_dim)) for _ in range(action_dim)]
            grid = np.meshgrid(*axes)
            self.centers = np.stack([g.flatten() for g in grid], axis=1)
            self.num_clusters = len(self.centers)
        else:
            self.centers = self.centers.reshape(-1, 1)
    
    def get_cluster(self, action: np.ndarray) -> int:
        """Return nearest cluster index."""
        action = np.array(action).flatten()
        distances = np.linalg.norm(self.centers - action, axis=1)
        return int(np.argmin(distances))
    
    def get_representative(self, cluster_idx: int) -> np.ndarray:
        """Get representative action for cluster."""
        return self.centers[cluster_idx]


# --------------------------------------------------------------------------- #
# DATA STRUCTURES (same as before, but more universal)
# --------------------------------------------------------------------------- #

@dataclass
class Transition:
    state: np.ndarray
    action: np.ndarray
    reward: float
    next_state: np.ndarray
    done: bool
    dark_residue: float = 0.0
    dr_derivative: float = 0.0
    coherence_gain: float = 0.0
    state_hash: int = 0
    action_cluster: int = 0


@dataclass 
class Episode:
    episode_num: int
    task_name: str
    transitions: List[Transition] = field(default_factory=list)
    total_reward: float = 0.0
    total_score: int = 0
    mean_dr: float = 0.0
    total_coherence_gain: float = 0.0
    critical_indices: List[int] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    
    def compute_metrics(self):
        if not self.transitions:
            return
        self.total_score = len(self.transitions)
        self.total_reward = sum(t.reward for t in self.transitions)
        self.mean_dr = np.mean([t.dark_residue for t in self.transitions])
        self.total_coherence_gain = sum(t.coherence_gain for t in self.transitions)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'episode_num': self.episode_num,
            'task_name': self.task_name,
            'total_score': self.total_score,
            'total_reward': float(self.total_reward),
            'mean_dr': float(self.mean_dr),
            'total_coherence_gain': float(self.total_coherence_gain),
            'critical_moment_count': len(self.critical_indices),
        }


# --------------------------------------------------------------------------- #
# REVERSE PARETO (unchanged logic)
# --------------------------------------------------------------------------- #

class ReversePareto:
    @staticmethod
    def analyze(episode: Episode, threshold: float = 0.8) -> List[Tuple[int, int, int, float]]:
        """Returns (step_idx, state_hash, action_cluster, dr_contribution)"""
        if not episode.transitions:
            return []
        
        impacts = [
            {
                'idx': i,
                'state_hash': t.state_hash,
                'action_cluster': t.action_cluster,
                'dr': t.dark_residue,
            }
            for i, t in enumerate(episode.transitions)
        ]
        
        impacts.sort(key=lambda x: x['dr'], reverse=True)
        
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
                item['action_cluster'],
                item['dr']
            ))
            if fraction >= threshold:
                break
        
        return critical


# --------------------------------------------------------------------------- #
# MULTI-SCALE GEODESIC MAP
# --------------------------------------------------------------------------- #

class MultiScaleGeodesicMap:
    """
    Geodesic map with multiple resolution levels.
    Coarse maps for exploration, fine maps for exploitation.
    """
    
    def __init__(self, num_scales: int = 3):
        self.num_scales = num_scales
        # Scale 1 (finest) → Scale num_scales (coarsest)
        self.maps: List[Dict[Tuple[int, int], Tuple[float, int]]] = [
            defaultdict(lambda: (999.0, 0)) for _ in range(num_scales)
        ]
        self.known_states = set()
    
    def update(self, state_hash: int, action_cluster: int, dr: float, scale: int = 1):
        """Update map at given scale."""
        scale_idx = scale - 1
        key = (state_hash, action_cluster)
        
        old_dr, count = self.maps[scale_idx][key]
        new_dr = (old_dr * count + dr) / (count + 1) if count > 0 else dr
        self.maps[scale_idx][key] = (new_dr, count + 1)
        
        self.known_states.add(state_hash)
    
    def get_best_action(self, state_hash: int, scale: int = 1) -> int:
        """Get best action at given scale."""
        scale_idx = scale - 1
        
        # Find all actions tried in this state at this scale
        actions = [
            (action, dr, count)
            for (s, action), (dr, count) in self.maps[scale_idx].items()
            if s == state_hash
        ]
        
        if not actions:
            return -1
        
        # Return action with lowest DR (weighted by count for confidence)
        best_action = min(actions, key=lambda x: x[1])[0]
        return best_action
    
    def is_known(self, state_hash: int) -> bool:
        return state_hash in self.known_states


# --------------------------------------------------------------------------- #
# UNIVERSAL GEODESIC WITNESS
# --------------------------------------------------------------------------- #

class UniversalGeodesicWitness:
    """Task-agnostic witness with curriculum support."""
    
    def __init__(self, task_config: Dict[str, Any], top_k: int = 15):
        self.task_config = task_config
        self.task_name = task_config['name']
        self.top_k = top_k
        
        self.all_episodes: List[Episode] = []
        self.top_episodes: List[Episode] = []
        
        self.geodesic_map = MultiScaleGeodesicMap(num_scales=3)
        self.exploration_rate = 1.0
        self.exploration_decay = 0.995
        
        # Adaptive thresholds
        self.min_exploration = 0.1
        
    def observe(self, episode: Episode):
        episode.compute_metrics()
        self.all_episodes.append(episode)
        
        # Update top gallery
        self.top_episodes.append(episode)
        self.top_episodes.sort(key=lambda e: e.total_reward, reverse=True)
        if len(self.top_episodes) > self.top_k:
            self.top_episodes = self.top_episodes[:self.top_k]
        
        # RPA
        critical = ReversePareto.analyze(episode, threshold=0.8)
        episode.critical_indices = [idx for idx, _, _, _ in critical]
        
        # Update multi-scale geodesic map
        for trans in episode.transitions:
            # Update all scales
            for scale in range(1, 4):
                self.geodesic_map.update(
                    trans.state_hash // (scale * scale),  # Coarsen hash
                    trans.action_cluster,
                    trans.dark_residue,
                    scale
                )
        
        # Double-weight critical moments
        for idx, state_hash, action_cluster, dr in critical:
            for scale in range(1, 4):
                self.geodesic_map.update(
                    state_hash // (scale * scale),
                    action_cluster,
                    dr,
                    scale
                )
        
        self._update_exploration()
    
    def _update_exploration(self):
        self.exploration_rate = max(self.min_exploration, 
                                   self.exploration_rate * self.exploration_decay)
    
    def should_explore(self) -> bool:
        return np.random.random() < self.exploration_rate
    
    def get_geodesic_action(self, state_hash: int, available_actions: List[int]) -> int:
        """Get best action from geodesic map, trying coarse→fine."""
        # Try fine scale first, fall back to coarser if unknown
        for scale in range(1, 4):
            coarse_hash = state_hash // (scale * scale)
            action = self.geodesic_map.get_best_action(coarse_hash, scale)
            if action >= 0 and action in available_actions:
                return action
        return -1
    
    def check_mastery(self) -> bool:
        """Check if task is mastered."""
        if len(self.top_episodes) < self.task_config['mastery_episodes']:
            return False
        
        recent = self.top_episodes[:self.task_config['mastery_episodes']]
        avg_reward = np.mean([e.total_reward for e in recent])
        
        return avg_reward >= self.task_config['mastery_threshold']
    
    def save_gallery(self, filename: str):
        data = {
            'task_name': self.task_name,
            'total_episodes': len(self.all_episodes),
            'geodesic_map_size': len(self.geodesic_map.known_states),
            'exploration_rate': self.exploration_rate,
            'top_episodes': [e.to_dict() for e in self.top_episodes],
        }
        path = os.path.join(GALLERY_DIR, filename)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)


# --------------------------------------------------------------------------- #
# UNIVERSAL ACTION WRAPPER
# --------------------------------------------------------------------------- #

class UniversalGeodesicWrapper(gym.Wrapper):
    """Universal wrapper for discrete and continuous action spaces."""
    
    def __init__(self, env, witness: UniversalGeodesicWitness, 
                 discretizer: StateDiscretizer, action_clusterer: Optional[ActionClusterer] = None):
        super().__init__(env)
        self.witness = witness
        self.discretizer = discretizer
        self.action_clusterer = action_clusterer
        self.current_state = None
        self.current_state_hash = None
        
        # Determine if we need Box wrapper for SAC
        if isinstance(env.action_space, gym.spaces.Discrete):
            self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
            self.is_discrete_base = True
        else:
            self.is_discrete_base = False
    
    def step(self, action):
        # Convert action if needed
        if self.is_discrete_base:
            actual_action = 0 if action[0] < 0.0 else 1
        else:
            actual_action = action
        
        # Get geodesic recommendation if not exploring
        if not self.witness.should_explore() and self.current_state_hash is not None:
            if self.action_clusterer:
                available = list(range(self.action_clusterer.num_clusters))
                geo_cluster = self.witness.get_geodesic_action(self.current_state_hash, available)
                
                if geo_cluster >= 0 and np.random.random() < 0.3:  # 30% geodesic influence
                    actual_action = self.action_clusterer.get_representative(geo_cluster)
            else:
                # Discrete case
                geo_action = self.witness.get_geodesic_action(self.current_state_hash, [0, 1])
                if geo_action >= 0 and np.random.random() < 0.3:
                    actual_action = geo_action
        
        return self.env.step(actual_action)
    
    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self.current_state = obs
        self.current_state_hash = self.discretizer.discretize(obs)
        return obs, info
    
    def set_state_hash(self, state: np.ndarray):
        self.current_state = state
        self.current_state_hash = self.discretizer.discretize(state)


# --------------------------------------------------------------------------- #
# CURRICULUM TRAINER
# --------------------------------------------------------------------------- #

def train_task(task_config: Dict[str, Any], start_episode: int = 1):
    """Train on a single task until mastery or max episodes."""
    
    print("\n" + "=" * 80)
    print(f"TASK: {task_config['name']} ({task_config['env_id']})")
    print("=" * 80)
    
    # Setup
    base_env = gym.make(task_config['env_id'])
    discretizer = StateDiscretizer(resolution=task_config['state_discretization'])
    
    action_clusterer = None
    if not task_config['is_discrete']:
        action_dim = base_env.action_space.shape[0]
        action_clusterer = ActionClusterer(action_dim, task_config.get('action_clusters', 7))
    
    witness = UniversalGeodesicWitness(task_config)
    env = UniversalGeodesicWrapper(base_env, witness, discretizer, action_clusterer)
    
    # DR calculator
    dr_calc = DarkResidueCalculator(base_env.observation_space, base_env.action_space)
    
    # Agent
    agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))
    logger = configure(None, ["stdout"])
    agent.set_logger(logger)
    
    # Warmup
    print("Warming up replay buffer...")
    obs, _ = env.reset()
    for _ in range(5000):
        action = env.action_space.sample()
        next_obs, _, done, truncated, _ = env.step(action)
        agent.replay_buffer.add(obs, next_obs, action, 0.0, done or truncated, [{}])
        obs = next_obs
        if done or truncated:
            obs, _ = env.reset()
    print("Warmup complete.\n")
    
    # Training loop
    global_ep = start_episode
    for local_ep in range(1, task_config['max_episodes'] + 1):
        episode = Episode(episode_num=global_ep, task_name=task_config['name'])
        
        obs, _ = env.reset()
        env.set_state_hash(obs)
        done, truncated = False, False
        prev_obs = None
        prev_action = None
        
        while not done and not truncated:
            action, _ = agent.predict(obs, deterministic=True)
            next_obs, base_reward, done, truncated, _ = env.step(action)
            env.set_state_hash(next_obs)
            
            # Compute DR
            current_dr = dr_calc.calculate(next_obs, prev_obs, action, prev_action)
            prev_dr = dr_calc.calculate(obs, None, prev_action, None) if prev_obs is not None else current_dr
            dr_derivative = current_dr - prev_dr
            
            # Pirouette reward
            coherence_gain = task_config['gamma_coherence'] * max(0, -dr_derivative)
            dissonance_penalty = task_config['delta_dissonance'] * current_dr
            reward = coherence_gain + task_config['beta_duration'] - dissonance_penalty
            
            # Create transition
            state_hash = discretizer.discretize(obs)
            action_cluster = action_clusterer.get_cluster(action) if action_clusterer else (0 if action[0] < 0 else 1)
            
            trans = Transition(
                state=obs.copy(),
                action=action,
                reward=reward,
                next_state=next_obs.copy(),
                done=done,
                dark_residue=current_dr,
                dr_derivative=dr_derivative,
                coherence_gain=coherence_gain,
                state_hash=state_hash,
                action_cluster=action_cluster,
            )
            episode.transitions.append(trans)
            
            # Train
            agent.replay_buffer.add(obs, next_obs, action, reward, done or truncated, [{}])
            agent.train(gradient_steps=1)
            
            prev_obs = obs
            prev_action = action
            obs = next_obs
        
        # Witness
        witness.observe(episode)
        
        # Report
        best_reward = witness.top_episodes[0].total_reward if witness.top_episodes else 0
        avg_top = np.mean([e.total_reward for e in witness.top_episodes]) if witness.top_episodes else 0
        
        print(
            f"Ep {global_ep:04d} ({local_ep:03d}) | "
            f"R={episode.total_reward:7.1f} | "
            f"DR={episode.mean_dr:.4f} | "
            f"CohGain={episode.total_coherence_gain:6.1f} | "
            f"GeoMap={len(witness.geodesic_map.known_states):5d} | "
            f"Explore={witness.exploration_rate:.3f} | "
            f"Top{witness.top_k}Avg={avg_top:7.1f}"
        )
        
        global_ep += 1
        
        # Check mastery
        if witness.check_mastery():
            print(f"\n{'*' * 80}")
            print(f"*** MASTERY ACHIEVED for {task_config['name']} at episode {global_ep - 1} ***")
            print(f"Top-{witness.top_k} Average: {avg_top:.1f}")
            print(f"Geodesic Map Size: {len(witness.geodesic_map.known_states)} states")
            print(f"{'*' * 80}\n")
            
            witness.save_gallery(f"{task_config['name']}_mastery.json")
            agent.save(os.path.join(GALLERY_DIR, f"{task_config['name']}_mastery.zip"))
            break
        
        if local_ep % 50 == 0:
            witness.save_gallery(f"{task_config['name']}_ep{local_ep:04d}.json")
    
    env.close()
    return global_ep


# --------------------------------------------------------------------------- #
# MAIN: CURRICULUM LEARNING
# --------------------------------------------------------------------------- #

def main():
    print("=" * 80)
    print("WENDIGO GEODESIC CURRICULUM: CartPole → Pendulum → Ant → Humanoid")
    print("=" * 80)
    
    global_episode = 1
    
    for task_config in TASK_CURRICULUM:
        try:
            global_episode = train_task(task_config, global_episode)
        except KeyboardInterrupt:
            print("\n\nTraining interrupted by user.")
            break
        except Exception as e:
            print(f"\n\nError training {task_config['name']}: {e}")
            print("Continuing to next task...\n")
            continue
    
    print("\n" + "=" * 80)
    print("CURRICULUM COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()