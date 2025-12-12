#!/usr/bin/env python3
"""
Feather-Turbo Curriculum
------------------------
A geodesic-augmented curriculum runner that accelerates learning (Bones-style horsepower)
and transfers Feather's geodesic across tasks: CartPole -> Pendulum -> Acrobot.

Dependencies:
  pip install gymnasium stable-baselines3

Usage:
  python feather_turbo_curriculum.py
"""

import os
import sys
import math
import time
import json
import random
from dataclasses import dataclass, field
from typing import Dict, Tuple, Any, List, Optional

import numpy as np

try:
    import gymnasium as gym
except Exception as e:
    raise RuntimeError("This script requires gymnasium. Please `pip install gymnasium`") from e

try:
    from stable_baselines3 import DQN, SAC
    from stable_baselines3.common.monitor import Monitor
    from stable_baselines3.common.noise import NormalActionNoise
    from stable_baselines3.common.callbacks import BaseCallback
    from stable_baselines3.common.evaluation import evaluate_policy
except Exception as e:
    raise RuntimeError("This script requires stable-baselines3. Please `pip install stable-baselines3`") from e


# =============================
# Dark Residue (per environment)
# =============================

def dr_cartpole(s: np.ndarray) -> float:
    x, xdot, th, thdot = s
    return 0.4*abs(x) + 0.2*abs(xdot) + 1.5*abs(th) + 0.3*abs(thdot)

def dr_pendulum(s: np.ndarray) -> float:
    th = ((s[0] + np.pi) % (2*np.pi)) - np.pi  # wrap angle
    thdot = s[1]
    return 0.5*abs(th) + 0.2*abs(thdot)

def dr_acrobot(s: np.ndarray) -> float:
    th1, th2, th1dot, th2dot = s
    return 0.4*(abs(th1) + 0.6*abs(th2)) + 0.15*(abs(th1dot) + abs(th2dot))

def get_dr_fn(env_id: str):
    if "CartPole" in env_id: return dr_cartpole
    if "Pendulum" in env_id: return dr_pendulum
    if "Acrobot"  in env_id: return dr_acrobot
    return dr_cartpole


# =====================
# Geodesic Map & Witness
# =====================

@dataclass
class ActionStats:
    count: int = 0
    mean_dr: float = 1e9  # lower is better

@dataclass
class GeoEntry:
    actions: Dict[int, ActionStats] = field(default_factory=dict)

class GeodesicMap:
    def __init__(self, discretizer: float = 5.0):
        self.table: Dict[int, GeoEntry] = {}
        self.discretizer = discretizer

    def _hash_state(self, s: np.ndarray) -> int:
        disc = tuple((s * self.discretizer).astype(int).tolist())
        return hash(disc)

    def update(self, s: np.ndarray, a_idx: int, dr: float):
        h = self._hash_state(s)
        if h not in self.table:
            self.table[h] = GeoEntry()
        stats = self.table[h].actions.get(a_idx, ActionStats(0, dr))
        new_count = stats.count + 1
        new_mean = stats.mean_dr + (dr - stats.mean_dr) / new_count
        self.table[h].actions[a_idx] = ActionStats(new_count, new_mean)

    def best_action(self, s: np.ndarray) -> Optional[int]:
        h = self._hash_state(s)
        if h not in self.table or not self.table[h].actions:
            return None
        return min(self.table[h].actions.items(), key=lambda kv: kv[1].mean_dr)[0]

    def seen(self, s: np.ndarray) -> bool:
        return self._hash_state(s) in self.table


class GeodesicWrapper(gym.ActionWrapper):
    """
    Discrete envs: override action with geodesic's best with certain probability.
    """
    def __init__(self, env, geo: GeodesicMap, dr_fn, influence=0.65, mastered_override=0.85):
        super().__init__(env)
        self.geo = geo
        self.dr_fn = dr_fn
        self.influence = influence
        self.mastered = mastered_override
        self._last_obs = None
        self.is_discrete = isinstance(env.action_space, gym.spaces.Discrete)

    def action(self, action):
        if self._last_obs is None or not self.is_discrete:
            return action
        best = self.geo.best_action(self._last_obs)
        if best is not None:
            use_geo = np.random.rand() < (self.mastered if self.geo.seen(self._last_obs) else self.influence)
            if use_geo:
                return int(best)
        return action

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        if self._last_obs is not None and self.is_discrete:
            dr = float(self.dr_fn(obs))
            self.geo.update(self._last_obs, int(action), dr)
        self._last_obs = obs.copy()
        return obs, reward, terminated, truncated, info

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self._last_obs = obs.copy()
        return obs, info


class GeodesicContinuousWrapper(gym.ActionWrapper):
    """
    Continuous envs (Pendulum): use geodesic knowledge (from CartPole) as a mean-nudger.
    We interpret "best action index" {0,1} as torque sign hints {-1,+1}.
    """
    def __init__(self, env, geo: GeodesicMap, dr_fn, influence=0.65, master=0.85):
        super().__init__(env)
        self.geo = geo
        self.dr_fn = dr_fn
        self.influence = influence
        self.mastered = master
        self._last_obs = None
        assert isinstance(env.action_space, gym.spaces.Box)

    def action(self, action):
        if self._last_obs is None:
            return action
        best = self.geo.best_action(self._last_obs)
        if best is None:
            return action
        sign = -1.0 if best == 0 else 1.0
        alpha = self.mastered if self.geo.seen(self._last_obs) else self.influence
        nudged = 0.7*action + 0.3*np.array([sign], dtype=np.float32)
        return alpha*nudged + (1.0-alpha)*action

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        self._last_obs = obs.copy()
        return obs, reward, terminated, truncated, info

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self._last_obs = obs.copy()
        return obs, info


# =================
# Simple Callbacks
# =================

class StopOnSolvedCallback(BaseCallback):
    """
    Stop training when mean reward exceeds threshold for N eval episodes.
    """
    def __init__(self, env, threshold: float, check_freq: int = 5000, n_eval_episodes: int = 10, verbose: int = 0):
        super().__init__(verbose)
        self.env = env
        self.threshold = threshold
        self.check_freq = check_freq
        self.n_eval_episodes = n_eval_episodes

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq != 0:
            return True
        mean_r, _ = evaluate_policy(self.model, self.env, n_eval_episodes=self.n_eval_episodes, deterministic=True)
        if self.verbose:
            print(f"[eval] step={self.num_timesteps} meanR={mean_r:.2f}")
        return bool(mean_r < self.threshold)


# =================
# Curriculum Runner
# =================

def run_cartpole(geo: GeodesicMap, total_timesteps=150_000, seed=42) -> DQN:
    env_id = "CartPole-v1"
    dr_fn = get_dr_fn(env_id)
    base_env = gym.make(env_id)
    base_env.reset(seed=seed)
    env = GeodesicWrapper(Monitor(base_env), geo, dr_fn, influence=0.65, mastered_override=0.85)

    model = DQN(
        "MlpPolicy",
        env,
        learning_rate=1e-3,
        buffer_size=100_000,
        learning_starts=3_000,
        batch_size=128,
        tau=0.01,
        gamma=0.99,
        train_freq=4,
        gradient_steps=4,
        target_update_interval=1_000,
        exploration_fraction=0.2,
        exploration_initial_eps=0.6,
        exploration_final_eps=0.05,
        verbose=1,
        seed=seed,
    )
    cb = StopOnSolvedCallback(env, threshold=495.0, check_freq=5_000, n_eval_episodes=10, verbose=1)
    model.learn(total_timesteps=total_timesteps, callback=cb, progress_bar=True)
    return model

def run_pendulum(geo: GeodesicMap, total_timesteps=200_000, seed=43) -> SAC:
    env_id = "Pendulum-v1"
    dr_fn = get_dr_fn(env_id)
    base_env = gym.make(env_id)
    base_env.reset(seed=seed)
    env = GeodesicContinuousWrapper(Monitor(base_env), geo, dr_fn, influence=0.55, master=0.80)

    n_actions = env.action_space.shape[-1]
    action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.2*np.ones(n_actions))

    model = SAC(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        buffer_size=200_000,
        learning_starts=3_000,
        batch_size=256,
        tau=0.02,
        gamma=0.98,
        train_freq=(1, "step"),
        gradient_steps=4,
        ent_coef="auto_0.1",
        action_noise=action_noise,
        verbose=1,
        seed=seed,
    )
    model.learn(total_timesteps=total_timesteps, progress_bar=True)
    return model

def run_acrobot(geo: GeodesicMap, total_timesteps=250_000, seed=44) -> DQN:
    env_id = "Acrobot-v1"
    dr_fn = get_dr_fn(env_id)
    base_env = gym.make(env_id)
    base_env.reset(seed=seed)
    env = GeodesicWrapper(Monitor(base_env), geo, dr_fn, influence=0.60, mastered_override=0.85)

    model = DQN(
        "MlpPolicy",
        env,
        learning_rate=1e-3,
        buffer_size=150_000,
        learning_starts=5_000,
        batch_size=256,
        tau=0.02,
        gamma=0.99,
        train_freq=4,
        gradient_steps=4,
        target_update_interval=2_000,
        exploration_fraction=0.25,
        exploration_initial_eps=0.8,
        exploration_final_eps=0.05,
        verbose=1,
        seed=seed,
    )
    model.learn(total_timesteps=total_timesteps, progress_bar=True)
    return model


def curriculum_run(
    out_dir: str = "./feather_turbo_runs",
    seed: int = 42,
    cartpole_steps: int = 150_000,
    pendulum_steps: int = 200_000,
    acrobot_steps: int = 250_000,
    discretizer: float = 5.0,
):
    os.makedirs(out_dir, exist_ok=True)

    geo = GeodesicMap(discretizer=discretizer)

    print("\\n=== Phase A: CartPole (build geodesic & anchors) ===")
    dqn_cart = run_cartpole(geo, total_timesteps=cartpole_steps, seed=seed)
    dqn_cart.save(os.path.join(out_dir, "cartpole_dqn.zip"))
    with open(os.path.join(out_dir, "geodesic_after_cartpole.json"), "w") as f:
        serial = {str(k): {str(a): st.__dict__ for a, st in e.actions.items()} for k, e in geo.table.items()}
        json.dump({"entries": len(geo.table), "table": serial}, f)

    print("\\n=== Phase B: Pendulum (transfer geodesic as mean-nudger) ===")
    sac_pend = run_pendulum(geo, total_timesteps=pendulum_steps, seed=seed+1)
    sac_pend.save(os.path.join(out_dir, "pendulum_sac.zip"))
    with open(os.path.join(out_dir, "geodesic_after_pendulum.json"), "w") as f:
        serial = {str(k): {str(a): st.__dict__ for a, st in e.actions.items()} for k, e in geo.table.items()}
        json.dump({"entries": len(geo.table), "table": serial}, f)

    print("\\n=== Phase C: Acrobot (reuse discrete override) ===")
    dqn_acro = run_acrobot(geo, total_timesteps=acrobot_steps, seed=seed+2)
    dqn_acro.save(os.path.join(out_dir, "acrobot_dqn.zip"))
    with open(os.path.join(out_dir, "geodesic_after_acrobot.json"), "w") as f:
        serial = {str(k): {str(a): st.__dict__ for a, st in e.actions.items()} for k, e in geo.table.items()}
        json.dump({"entries": len(geo.table), "table": serial}, f)

    print("\\nDone. Models and geodesic snapshots saved to:", out_dir)
    return out_dir


if __name__ == "__main__":
    curriculum_run()
