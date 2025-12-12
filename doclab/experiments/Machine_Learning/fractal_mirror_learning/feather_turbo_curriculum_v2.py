#!/usr/bin/env python3
"""
Feather-Turbo Curriculum (v2, tuned)
- Fixes CartPole collapse by using safer DQN hyperparams.
- Gates geodesic override until the agent shows basic competence (avg ep len).
- Keeps the A->B->C curriculum and geodesic transfer.
"""

import os, json, numpy as np
from dataclasses import dataclass, field
from typing import Dict, Optional

import gymnasium as gym
from stable_baselines3 import DQN, SAC
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.evaluation import evaluate_policy


# ------------- Dark Residue -------------
def dr_cartpole(s: np.ndarray) -> float:
    x, xdot, th, thdot = s
    return 0.4*abs(x) + 0.2*abs(xdot) + 1.5*abs(th) + 0.3*abs(thdot)

def dr_pendulum(s: np.ndarray) -> float:
    th = ((s[0] + np.pi) % (2*np.pi)) - np.pi
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


# ------------- Geodesic -------------
@dataclass
class ActionStats:
    count: int = 0
    mean_dr: float = 1e9

@dataclass
class GeoEntry:
    actions: Dict[int, ActionStats] = field(default_factory=dict)

class GeodesicMap:
    def __init__(self, discretizer: float = 5.0):
        self.table: Dict[int, GeoEntry] = {}
        self.discretizer = discretizer

    def _hash(self, s: np.ndarray) -> int:
        disc = tuple((s * self.discretizer).astype(int).tolist())
        return hash(disc)

    def update(self, s: np.ndarray, a_idx: int, dr: float):
        h = self._hash(s)
        entry = self.table.setdefault(h, GeoEntry())
        stats = entry.actions.get(a_idx, ActionStats(0, dr))
        c = stats.count + 1
        m = stats.mean_dr + (dr - stats.mean_dr) / c
        entry.actions[a_idx] = ActionStats(c, m)

    def best_action(self, s: np.ndarray) -> Optional[int]:
        h = self._hash(s)
        if h not in self.table or not self.table[h].actions:
            return None
        return min(self.table[h].actions.items(), key=lambda kv: kv[1].mean_dr)[0]

    def seen(self, s: np.ndarray, min_count: int = 5) -> bool:
        h = self._hash(s)
        if h not in self.table: return False
        return any(st.count >= min_count for st in self.table[h].actions.values())


class CompetenceGate:
    """Tracks recent episode lengths; opens when mean >= threshold."""
    def __init__(self, window=100, threshold=50):
        self.window = window
        self.threshold = threshold
        self.buf = []

    def push(self, ep_len: int):
        self.buf.append(ep_len)
        if len(self.buf) > self.window:
            self.buf.pop(0)

    def open(self) -> bool:
        if not self.buf: return False
        return (sum(self.buf)/len(self.buf)) >= self.threshold


class GeodesicWrapper(gym.ActionWrapper):
    def __init__(self, env, geo: GeodesicMap, dr_fn, influence=0.5, mastered=0.8, gate: Optional[CompetenceGate]=None):
        super().__init__(env)
        self.geo, self.dr_fn = geo, dr_fn
        self.influence, self.mastered = influence, mastered
        self._last_obs = None
        self.is_discrete = isinstance(env.action_space, gym.spaces.Discrete)
        self.gate = gate

    def action(self, action):
        if self._last_obs is None or not self.is_discrete:
            return action
        if self.gate is not None and not self.gate.open():
            return action  # don't override until basic competence
        best = self.geo.best_action(self._last_obs)
        if best is None: return action
        use_geo = np.random.rand() < (self.mastered if self.geo.seen(self._last_obs, min_count=5) else self.influence)
        return int(best) if use_geo else action

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        if self._last_obs is not None and self.is_discrete:
            self.geo.update(self._last_obs, int(action), float(self.dr_fn(obs)))
        self._last_obs = obs.copy()
        if terminated or truncated:
            if self.gate is not None:
                ep_len = info.get("episode", {}).get("l")  # Monitor fills episode info; sometimes absent
                if ep_len is None and hasattr(self.env, "episode_rewards"):
                    pass
            # Gymnasium's Monitor does not always include "episode" dict; we rely on external logging if absent.
        return obs, reward, terminated, truncated, info

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self._last_obs = obs.copy()
        return obs, info


class GeodesicContinuousWrapper(gym.ActionWrapper):
    def __init__(self, env, geo: GeodesicMap, dr_fn, influence=0.55, mastered=0.8):
        super().__init__(env)
        self.geo, self.dr_fn = geo, dr_fn
        self.influence, self.mastered = influence, mastered
        self._last_obs = None
        assert isinstance(env.action_space, gym.spaces.Box)

    def action(self, action):
        if self._last_obs is None:
            return action
        best = self.geo.best_action(self._last_obs)
        if best is None:
            return action
        sign = -1.0 if best == 0 else 1.0
        alpha = self.mastered if self.geo.seen(self._last_obs, min_count=5) else self.influence
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


# ------------- Callbacks -------------
class MeanEpLenLogger(BaseCallback):
    def __init__(self, gate: CompetenceGate, verbose=0):
        super().__init__(verbose)
        self.gate = gate
        self._ep_len = 0

    def _on_step(self) -> bool:
        # SB3 logger does not expose ep len directly each step; we approximate via infos
        infos = self.locals.get("infos", [])
        for info in infos:
            if "episode" in info:
                l = info["episode"].get("l", None)
                if l is not None:
                    self.gate.push(int(l))
        return True


class StopOnSolvedCallback(BaseCallback):
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


# ------------- Curriculum -------------
def run_cartpole(geo: GeodesicMap, total_timesteps=120_000, seed=42) -> DQN:
    env_id = "CartPole-v1"
    dr_fn = get_dr_fn(env_id)
    base_env = gym.make(env_id)
    base_env.reset(seed=seed)
    gate = CompetenceGate(window=100, threshold=50)  # open when avg ep_len >= 50
    env = GeodesicWrapper(Monitor(base_env), geo, dr_fn, influence=0.35, mastered=0.75, gate=gate)

    model = DQN(
        "MlpPolicy",
        env,
        learning_rate=5e-4,           # safer
        buffer_size=50_000,
        learning_starts=1_000,        # quicker start
        batch_size=64,                # standard
        tau=0.02,
        gamma=0.99,
        train_freq=1,                 # avoid over-updating early
        gradient_steps=1,
        target_update_interval=250,   # faster target sync
        exploration_fraction=0.10,    # cool quickly
        exploration_initial_eps=1.0,  # full exploration start
        exploration_final_eps=0.05,
        verbose=1,
        seed=seed,
    )

    cb_solved = StopOnSolvedCallback(env, threshold=495.0, check_freq=5000, n_eval_episodes=10, verbose=1)
    cb_gate = MeanEpLenLogger(gate)
    model.learn(total_timesteps=total_timesteps, callback=[cb_gate, cb_solved], progress_bar=True)
    return model

def run_pendulum(geo: GeodesicMap, total_timesteps=150_000, seed=43) -> SAC:
    env_id = "Pendulum-v1"
    dr_fn = get_dr_fn(env_id)
    base_env = gym.make(env_id)
    base_env.reset(seed=seed)
    env = GeodesicContinuousWrapper(Monitor(base_env), geo, dr_fn, influence=0.50, mastered=0.75)

    n_actions = env.action_space.shape[-1]
    action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.2*np.ones(n_actions))

    model = SAC(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        buffer_size=150_000,
        learning_starts=2_000,
        batch_size=256,
        tau=0.02,
        gamma=0.98,
        train_freq=(1, "step"),
        gradient_steps=2,           # slightly gentler
        ent_coef="auto_0.1",
        action_noise=action_noise,
        verbose=1,
        seed=seed,
    )
    model.learn(total_timesteps=total_timesteps, progress_bar=True)
    return model

def run_acrobot(geo: GeodesicMap, total_timesteps=180_000, seed=44) -> DQN:
    env_id = "Acrobot-v1"
    dr_fn = get_dr_fn(env_id)
    base_env = gym.make(env_id)
    base_env.reset(seed=seed)
    env = GeodesicWrapper(Monitor(base_env), geo, dr_fn, influence=0.40, mastered=0.75, gate=None)

    model = DQN(
        "MlpPolicy",
        env,
        learning_rate=5e-4,
        buffer_size=100_000,
        learning_starts=2_000,
        batch_size=128,
        tau=0.02,
        gamma=0.99,
        train_freq=1,
        gradient_steps=1,
        target_update_interval=500,
        exploration_fraction=0.20,
        exploration_initial_eps=1.0,
        exploration_final_eps=0.05,
        verbose=1,
        seed=seed,
    )
    model.learn(total_timesteps=total_timesteps, progress_bar=True)
    return model


def curriculum_run(
    out_dir: str = "./feather_turbo_runs_v2",
    seed: int = 42,
    cartpole_steps: int = 120_000,
    pendulum_steps: int = 150_000,
    acrobot_steps: int = 180_000,
    discretizer: float = 5.0,
):
    os.makedirs(out_dir, exist_ok=True)
    geo = GeodesicMap(discretizer=discretizer)

    print("\\n=== Phase A: CartPole ===")
    dqn_cart = run_cartpole(geo, total_timesteps=cartpole_steps, seed=seed)
    dqn_cart.save(os.path.join(out_dir, "cartpole_dqn.zip"))
    with open(os.path.join(out_dir, "geodesic_after_cartpole.json"), "w") as f:
        serial = {str(k): {str(a): st.__dict__ for a, st in e.actions.items()} for k, e in geo.table.items()}
        json.dump({"entries": len(geo.table), "table": serial}, f)

    print("\\n=== Phase B: Pendulum ===")
    sac_pend = run_pendulum(geo, total_timesteps=pendulum_steps, seed=seed+1)
    sac_pend.save(os.path.join(out_dir, "pendulum_sac.zip"))
    with open(os.path.join(out_dir, "geodesic_after_pendulum.json"), "w") as f:
        serial = {str(k): {str(a): st.__dict__ for a, st in e.actions.items()} for k, e in geo.table.items()}
        json.dump({"entries": len(geo.table), "table": serial}, f)

    print("\\n=== Phase C: Acrobot ===")
    dqn_acro = run_acrobot(geo, total_timesteps=acrobot_steps, seed=seed+2)
    dqn_acro.save(os.path.join(out_dir, "acrobot_dqn.zip"))
    with open(os.path.join(out_dir, "geodesic_after_acrobot.json"), "w") as f:
        serial = {str(k): {str(a): st.__dict__ for a, st in e.actions.items()} for k, e in geo.table.items()}
        json.dump({"entries": len(geo.table), "table": serial}, f)

    print("\\nDone ->", out_dir)
    return out_dir


if __name__ == "__main__":
    curriculum_run()
