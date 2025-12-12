#!/usr/bin/env python3
"""
Wendigo Multitask (Refactored w/ Targeted Training)
- 1 SAC
- 3 tasks: CartPole, Pendulum, MountainCarContinuous
- Per-task score normalization and mastery tracking.
- TaskLibrary now implements a "targeted" curriculum:
    - 90% focus on unmastered tasks.
    - 10% "reassessment" of mastered tasks.
- Scoring logic is generalized to handle step-based (CartPole) 
  and reward-based (MountainCar) scores.
"""

import os, sys, json, logging
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any
from collections import deque, defaultdict
import numpy as np

import gymnasium as gym
import torch as th
import torch.nn as nn
import torch.optim as optim

from stable_baselines3 import SAC
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.logger import configure

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("wendigo-multi")

device = th.device("cuda") if th.cuda.is_available() else th.device("cpu")


# ---------------------------------------------------------------------
# task-specific dark residue
# ---------------------------------------------------------------------
def dark_residue_cartpole(obs: np.ndarray) -> float:
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    dr = (
        0.4 * abs(cart_pos)
        + 0.2 * abs(cart_vel)
        + 1.5 * abs(pole_angle)
        + 0.3 * abs(pole_vel)
    )
    return float(dr)


def dark_residue_pendulum(obs: np.ndarray, action: float) -> float:
    # obs = [cos θ, sin θ, θdot]
    cos_th, sin_th, thdot = obs
    angle_err = np.arctan2(sin_th, cos_th)  # -pi..pi
    dr = (
        0.8 * abs(angle_err)
        + 0.15 * abs(thdot)
        + 0.05 * abs(action)
    )
    return float(dr)

def dark_residue_mountaincar(obs: np.ndarray, action: float) -> float:
    # obs = [position, velocity]
    pos, vel = obs
    # Goal is pos 0.5
    dist_to_goal = abs(0.5 - pos)
    # Penalize being at the bottom (-0.5) with no velocity
    low_vel_penalty = max(0, 0.02 - abs(vel)) * 20.0 * (1.0 - abs(pos))
    dr = (
        0.6 * dist_to_goal 
        + 0.3 * low_vel_penalty 
        + 0.1 * abs(action)
    )
    return float(dr)


# ---------------------------------------------------------------------
# NEW: Task Normalization & Library (Upgraded)
# ---------------------------------------------------------------------

@dataclass
class TaskSpec:
    """Holds normalization info and score history for a single task."""
    name: str
    reward_min: float
    reward_max: float
    solve_threshold_norm: float
    score_metric: str = "steps" # "steps" or "reward"
    step_cap: int = 500
    window: int = 25
    scores: deque = field(default_factory=lambda: deque(maxlen=25))
    # NEW: Per-task DR normalization values
    dr_min: float = 0.0
    dr_max: float = 3.0

    def update(self, raw_score: float):
        """Add a new raw score to the history."""
        self.scores.append(raw_score)

    def normalize_single_score(self, raw_score: float) -> float:
        """Normalize a single score to [0, 1] based on task min/max."""
        if self.reward_max == self.reward_min:
            return 0.0
        clamped = max(self.reward_min, min(self.reward_max, raw_score))
        return (clamped - self.reward_min) / (self.reward_max - self.reward_min)

    # NEW: DR Normalization method
    def normalize_dr(self, dr: float) -> float:
        """Normalize a single DR value to [0, 1]."""
        clamped = max(self.dr_min, min(self.dr_max, dr))
        return (clamped - self.dr_min) / (self.dr_max - self.dr_min)

    def normalized_scores(self) -> List[float]:
        """Return the recent history, normalized to [0, 1]."""
        return [self.normalize_single_score(s) for s in self.scores]

    def mastery(self) -> Tuple[bool, float]:
        """
        Check if the task is mastered.
        NEW: Requires a full window and checks for score variance to avoid flatlines.
        """
        if len(self.scores) < self.window:  # Require a full window of scores
            return False, 0.0
        
        ns = self.normalized_scores()
        avg = float(np.mean(ns))
        score_variance = float(np.var(ns))
        
        # Mastery requires meeting the threshold AND showing some score variance (not flatlined)
        is_mastered = avg >= self.solve_threshold_norm and score_variance > 1e-4
        return is_mastered, avg

class TaskLibrary:
    """Manages all registered tasks and implements targeted curriculum."""
    def __init__(self):
        self.tasks: Dict[str, TaskSpec] = {}
        self.name_to_id: Dict[str, int] = {}
        self.id_to_name: Dict[int, str] = {}
        self.active_order: List[str] = []

    def register(self, task_id: int, task_spec: TaskSpec):
        """Add a new task to the library."""
        name = task_spec.name
        if name in self.tasks:
            logger.warning(f"Task {name} is already registered. Overwriting.")
        
        self.tasks[name] = task_spec
        self.name_to_id[name] = task_id
        self.id_to_name[task_id] = name
        
        if name not in self.active_order:
            self.active_order.append(name)
        logger.info(f"Registered task {task_id} ('{name}'): Score metric='{task_spec.score_metric}', Range=[{task_spec.reward_min}, {task_spec.reward_max}], StepCap={task_spec.step_cap}")

    def update_score(self, task_name: str, raw_score: float):
        """Update the score for a specific task."""
        if task_name in self.tasks:
            self.tasks[task_name].update(raw_score)
        else:
            logger.warning(f"Attempted to update score for unregistered task: {task_name}")

    def mastery_report(self) -> Dict[str, Dict[str, Any]]:
        """Get a report of mastery status for all tasks."""
        rep = {}
        for name, spec in self.tasks.items():
            mastered, avg = spec.mastery()
            rep[name] = {
                "mastered": mastered,
                "norm_avg": round(avg, 3),
                "raw_recent_avg": round(float(np.mean(spec.scores)), 1) if spec.scores else 0.0,
            }
        return rep

    def choose_task(self, reassessment_prob: float = 0.1) -> Tuple[int, str]:
        """
        Implement the "targeted" curriculum.
        Focuses on unmastered tasks, with occasional reassessment of mastered ones.
        """
        mastered_tasks = []
        unmastered_tasks = []
        for name, spec in self.tasks.items():
            mastered, _ = spec.mastery()
            if mastered:
                mastered_tasks.append(name)
            else:
                unmastered_tasks.append(name)

        chosen_name = ""
        if not unmastered_tasks:
            # All tasks are mastered, just pick one at random to maintain
            chosen_name = np.random.choice(self.active_order)
        
        elif mastered_tasks and np.random.rand() < reassessment_prob:
            # Time for a reassessment run on a mastered task
            chosen_name = np.random.choice(mastered_tasks)
        
        else:
            # Focus on an unmastered task
            chosen_name = np.random.choice(unmastered_tasks)
            
        return self.name_to_id[chosen_name], chosen_name


class GlobalTopKNorm:
    """Global leaderboard that stores *normalized* scores to be task-fair."""
    def __init__(self, k=15):
        self.k = k
        self.items: List[Tuple[float, str, float]] = []  # list of (norm_score, task_name, raw_score)

    def add(self, task_name: str, raw_score: float, task_lib: TaskLibrary):
        """Add a new score, normalizing it first."""
        if task_name not in task_lib.tasks:
            logger.warning(f"Task {task_name} not in library. Cannot add to leaderboard.")
            return

        spec = task_lib.tasks[task_name]
        norm = spec.normalize_single_score(raw_score)
        
        self.items.append((norm, task_name, raw_score))
        self.items.sort(key=lambda x: x[0], reverse=True) # Sort by norm_score
        if len(self.items) > self.k:
            self.items[:] = self.items[:self.k]

    def average_norm(self) -> float:
        """Get the average normalized score from the leaderboard."""
        if not self.items:
            return 0.0
        return float(np.mean([item[0] for item in self.items]))

def characterize_env(env) -> Dict[str, Any]:
    """Probe env metadata to log its properties."""
    info = {}
    spec = getattr(env, "spec", None)
    info["name"] = getattr(spec, "id", "unknown")
    info["max_steps"] = getattr(spec, "max_episode_steps", None)
    info["reward_threshold"] = getattr(spec, "reward_threshold", None)
    return info

class GlobalTransitionBank:
    """Stores and samples the globally cleanest transitions across all tasks."""
    def __init__(self, max_size=5000):
        self.max_size = max_size
        # Items are: (dr, task_id, transition_tuple)
        self.items: List[Tuple[float, int, Tuple]] = []

    def maybe_add(self, task_id: int, transition: Tuple, dr: float):
        """Add a transition and sort by DR, keeping the buffer trimmed."""
        self.items.append((dr, task_id, transition))
        self.items.sort(key=lambda x: x[0])  # Sort by lowest DR
        if len(self.items) > self.max_size:
            self.items = self.items[:self.max_size]

    def sample(self, k: int = 64) -> List[Tuple]:
        """Sample the top k cleanest transitions from the bank."""
        if not self.items:
            return []
        # Return the transition tuple itself
        return [x[2] for x in self.items[:min(k, len(self.items))]]

# ---------------------------------------------------------------------
# multi-task env (Upgraded for 3 tasks + targeted scheduling)
# ---------------------------------------------------------------------
class MultiTaskWendigoEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, task_lib: TaskLibrary):
        super().__init__()
        self.task_lib = task_lib # Store the library
        self.tasks: List[Dict[str, Any]] = []

        # Task 0: CartPole
        cart = gym.make("CartPole-v1")
        cart_info = characterize_env(cart)
        self.tasks.append({
            "id": 0,
            "name": "cartpole",
            "env": cart,
            "type": "discrete",
            "info": cart_info,
        })

        # Task 1: Pendulum
        pend = gym.make("Pendulum-v1")
        pend_info = characterize_env(pend)
        self.tasks.append({
            "id": 1,
            "name": "pendulum",
            "env": pend,
            "type": "continuous",
            "info": pend_info,
        })
        
        # Task 2: MountainCarContinuous
        mcc = gym.make("MountainCarContinuous-v0")
        mcc_info = characterize_env(mcc)
        self.tasks.append({
            "id": 2,
            "name": "mountaincar_cont",
            "env": mcc,
            "type": "continuous", # Action space is already [-1, 1]
            "info": mcc_info,
        })

        self.num_tasks = len(self.tasks)
        self.current_task_id = None
        self.current_task_name = None
        self.current_env = None

        self.action_space = gym.spaces.Box(
            low=np.array([-1.0], dtype=np.float32),
            high=np.array([1.0], dtype=np.float32),
            dtype=np.float32,
        )
        high = np.array([np.inf] * 6, dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=-high, high=high, dtype=np.float32)

    def _select_task(self):
        # NEW: Use the library's choice
        self.current_task_id, self.current_task_name = self.task_lib.choose_task()
        self.current_env = self.tasks[self.current_task_id]["env"]

    def _obs_to_6(self, obs: np.ndarray, task_id: int) -> np.ndarray:
        task_norm = task_id / max(1, self.num_tasks - 1)
        obs = np.array(obs, dtype=np.float32).flatten()
        if obs.shape[0] >= 5:
            base = obs[:5]
        else:
            base = np.zeros(5, dtype=np.float32)
            base[: obs.shape[0]] = obs
        full = np.concatenate([base, np.array([task_norm], dtype=np.float32)])
        return full

    def reset(self, *, seed: int | None = None, options: dict | None = None):
        super().reset(seed=seed)
        self._select_task()
        obs, info = self.current_env.reset(seed=seed)
        obs6 = self._obs_to_6(obs, self.current_task_id)
        return obs6, {"task_id": self.current_task_id, "task_name": self.current_task_name, "inner_info": info}

    def step(self, action: np.ndarray):
        task = self.tasks[self.current_task_id]
        task_name = task["name"]
        
        if task_name == "cartpole":
            a = float(action[0])
            disc = 0 if a < 0.0 else 1
            obs, rew, term, trunc, info = task["env"].step(disc)
            obs6 = self._obs_to_6(obs, self.current_task_id)
            return obs6, rew, term, trunc, {"task_id": self.current_task_id, "task_name": task_name, **info}
        
        elif task_name == "pendulum":
            a = float(action[0])
            pend_a = np.array([a * 2.0], dtype=np.float32) # scale to [-2, 2]
            obs, rew, term, trunc, info = task["env"].step(pend_a)
            obs6 = self._obs_to_6(obs, self.current_task_id)
            return obs6, rew, term, trunc, {"task_id": self.current_task_id, "task_name": task_name, "raw_action": float(pend_a[0]), **info}

        elif task_name == "mountaincar_cont":
            # Action space is already [-1, 1]
            a = np.array(action, dtype=np.float32) 
            obs, rew, term, trunc, info = task["env"].step(a)
            obs6 = self._obs_to_6(obs, self.current_task_id)
            return obs6, rew, term, trunc, {"task_id": self.current_task_id, "task_name": task_name, "raw_action": float(action[0]), **info}

        else:
            raise ValueError(f"Unknown task name in step: {task_name}")


# ---------------------------------------------------------------------
# Coherence + Predictive heads (Unchanged architecture)
# ---------------------------------------------------------------------
class CoherenceHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1), # Outputs a normalized score
        )
    def forward(self, x: th.Tensor) -> th.Tensor:
        return self.net(x)

class PredictiveHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(6, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            # NEW: Output is now [score_norm, lag_norm, dr_norm]
            nn.Linear(32, 3),
        )
    def forward(self, x: th.Tensor) -> th.Tensor:
        return self.net(x)

@dataclass
class GoldEpisode:
    task_id: int
    task_name: str
    score: float # This is final_score (steps or reward)
    mean_dr: float
    transitions: List[Tuple]
    vigor: int
    rigor: int

class GoldWindow: # (Unchanged)
    def __init__(self, max_size: int = 64):
        self.max_size = max_size
        self.buffer: List[GoldEpisode] = []
    def maybe_add(self, ep: GoldEpisode):
        self.buffer.append(ep)
        self.buffer.sort(key=lambda e: (-e.score, e.mean_dr))
        if len(self.buffer) > self.max_size:
            self.buffer = self.buffer[: self.max_size]
    def sample_transitions(self, k: int = 16) -> List[Tuple]:
        if not self.buffer: return []
        ep = self.buffer[0]
        sorted_tr = sorted(ep.transitions, key=lambda t: t[4])  # by dark
        return sorted_tr[: min(k, len(sorted_tr))]


# ---------------------------------------------------------------------
# Wendigo Agent (Refactored Heads)
# ---------------------------------------------------------------------
class WendigoMultiAgent:
    def __init__(self, env: gym.Env, seed: int = 42):
        self.env = env
        self.env.reset(seed=seed)
        np.random.seed(seed)
        th.manual_seed(seed)
        self.gold_dir = "./wendigo_gold"
        os.makedirs(self.gold_dir, exist_ok=True)

        n_actions = env.action_space.shape[0]
        action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

        self.sac = SAC(
            "MlpPolicy",
            env,
            verbose=0,
            device=device,
            learning_rate=3e-4,
            buffer_size=300_000,
            batch_size=256,
            train_freq=(1, "step"),
            gradient_steps=1,
            gamma=0.99,
            action_noise=action_noise,
        )
        self.sac._setup_model()
        self.sac.set_logger(configure("./wendigo_logs_multi_targeted", ["stdout"]))

        self.coherence_head = CoherenceHead().to(device)
        self.coherence_opt = optim.Adam(self.coherence_head.parameters(), lr=1e-3)

        self.predictive_head = PredictiveHead().to(device)
        self.predictive_opt = optim.Adam(self.predictive_head.parameters(), lr=1e-3)

        self.auto_ring = []
        self.auto_ring_max = 96
        self.temperature = 1.0
        self.dark_running: List[float] = []
        self.max_dark_hist = 8_000
        
        self.anneal_episodes = 350
        self.alpha_residue = 0.8
        self.lambda_pred = 1e-3
        self.beta_residue_actor = 0.25
        self.last_teacher_signal = 0.0
        self.global_episode = 0

    def register_dark(self, dr: float): # (Unchanged)
        self.dark_running.append(dr)
        if len(self.dark_running) > self.max_dark_hist:
            self.dark_running = self.dark_running[-self.max_dark_hist :]

    def current_dark_median(self) -> float: # (Unchanged)
        if not self.dark_running: return 0.4
        return float(np.median(self.dark_running))

    def predict_action(self, obs: np.ndarray) -> Tuple[np.ndarray, str]: # (Unchanged)
        if np.random.rand() < 0.35:
            a, _ = self.sac.predict(obs, deterministic=False)
            return a, "Vigor"
        else:
            a, _ = self.sac.predict(obs, deterministic=True)
            return a, "Rigor"

    def step_learn(self, obs, action, next_obs, reward, done): # (Unchanged)
        self.sac.replay_buffer.add(
            obs=obs, next_obs=next_obs, action=action, reward=reward, done=done,
            infos=[{"TimeLimit.truncated": False}],
        )
        self.sac.train(gradient_steps=1)

    def sharpen_with_whetstones(self, transitions: List[Tuple]): # (Unchanged)
        if not transitions: return
        for (obs, action, next_obs, reward, dark, done, task_id) in transitions:
            extra_reward = reward + self.temperature * (0.1 * max(0.0, 0.35 - dark))
            extra_reward -= self.beta_residue_actor * dark
            extra_reward += 0.5 * self.last_teacher_signal
            self.sac.replay_buffer.add(
                obs=obs, next_obs=next_obs, action=action, reward=extra_reward, done=done,
                infos=[{"TimeLimit.truncated": False}],
            )
            if self.sac.replay_buffer.size() < self.sac.batch_size: return
        self.sac.train(gradient_steps=min(10, len(transitions)))
        self.temperature = max(0.35, self.temperature * 0.997)

    def train_coherence_head(self, mean_dr, vigor_ratio, ep_len_norm, task_id_norm, true_score: float, task_spec: TaskSpec):
        # NEW: Train on the *normalized* score
        score_norm = task_spec.normalize_single_score(true_score)
        
        x = th.tensor([[mean_dr, vigor_ratio, ep_len_norm, task_id_norm]], dtype=th.float32, device=device)
        y = th.tensor([[score_norm]], dtype=th.float32, device=device)
        pred_norm = self.coherence_head(x)
        loss = ((pred_norm - y) ** 2).mean()
        self.coherence_opt.zero_grad()
        loss.backward()
        self.coherence_opt.step()
        return float(loss.item())

    def predict_coherence_score(self, mean_dr, vigor_ratio, ep_len_norm, task_id_norm) -> float:
        # NEW: Returns a normalized score
        with th.no_grad():
            x = th.tensor([[mean_dr, vigor_ratio, ep_len_norm, task_id_norm]], dtype=th.float32, device=device)
            pred_norm = self.coherence_head(x)
            return float(pred_norm.item())

    def train_predictive_head(
        self,
        mean_dr: float, # Raw mean DR for the episode
        vigor_ratio: float,
        ep_len_norm: float,
        dyn_threshold_norm: float,
        coh_pred_norm: float,
        score: float,
        task_id_norm: float,
        task_spec: TaskSpec,
        episode_idx: int,
    ):
        score_norm = task_spec.normalize_single_score(score)
        # NEW: Normalize the mean DR for this task
        mean_dr_norm = task_spec.normalize_dr(mean_dr)

        a = max(0.1, 1.0 - episode_idx / float(self.anneal_episodes))
        clean_component = score_norm - self.alpha_residue * mean_dr
        lag_target = float(np.clip(a * score_norm + (1.0 - a) * clean_component, 0.0, 1.0))

        x = th.tensor(
            [[mean_dr, vigor_ratio, ep_len_norm, dyn_threshold_norm, coh_pred_norm, task_id_norm]],
            dtype=th.float32, device=device,
        )
        # NEW: Target now includes the normalized DR
        y = th.tensor([[score_norm, lag_target, mean_dr_norm]], dtype=th.float32, device=device)

        out = self.predictive_head(x)
        # NEW: Unpack all three predictions
        score_hat_norm, lag_hat_norm, dr_hat_norm = out[0, 0], out[0, 1], out[0, 2]

        lag_loss = ((lag_hat_norm - y[0, 1]) ** 2).mean()
        score_loss = ((score_hat_norm - y[0, 0]) ** 2).mean()
        # NEW: Add DR loss
        dr_loss = ((dr_hat_norm - y[0, 2]) ** 2).mean()

        # NEW: Update total loss with DR component
        total_teacher_loss = score_loss + 0.5 * lag_loss + 0.5 * dr_loss

        self.predictive_opt.zero_grad()
        total_teacher_loss.backward()
        for p in self.predictive_head.parameters():
            if p.grad is not None:
                p.grad *= self.lambda_pred
        self.predictive_opt.step()

        with th.no_grad():
            self.last_teacher_signal = float(lag_hat_norm.clamp(0.0, 1.0).item())
        
        # NEW: Return the new prediction value for logging
        return float(total_teacher_loss.item()), float(score_hat_norm.item()), float(lag_hat_norm.item()), lag_target, float(dr_hat_norm.item())

    def register_autopoietic_episode(self, snap: dict): # (Unchanged)
        self.auto_ring.append(snap)
        if len(self.auto_ring) > self.auto_ring_max:
            self.auto_ring = self.auto_ring[-self.auto_ring_max :]

    def run_autopoietic_cycle(self): # (Unchanged)
        if len(self.auto_ring) < 5: return
        ranked = sorted(self.auto_ring, key=lambda e: (-e["lag_pred_norm"], e["mean_dr"]))
        for ep in ranked[:4]:
            tr = sorted(ep["transitions"], key=lambda t: t[4])[:14]
            self.sharpen_with_whetstones(tr)


# ---------------------------------------------------------------------
# REFACTORED Main Loop (3 Tasks, Targeted, Generalized Scoring)
# ---------------------------------------------------------------------
def main():
    task_lib = TaskLibrary()

    # --- UPDATED: Task Registrations ---
    task_lib.register(0, TaskSpec(
        name="cartpole",
        reward_min=0, reward_max=500, 
        solve_threshold_norm=0.95,
        score_metric="steps", step_cap=500,
        window=25,
        dr_min=0.0, dr_max=2.0, # Adjusted DR range for CartPole
    ))
    # NEW: Pendulum is now reward-based with a proper range
    task_lib.register(1, TaskSpec(
        name="pendulum",
        reward_min=-1600.0, reward_max=0.0, # Realistic reward range
        solve_threshold_norm=0.8, # Threshold for high reward (e.g., > -320)
        score_metric="reward", step_cap=200,
        window=25,
        dr_min=0.0, dr_max=4.0, # Adjusted DR range for Pendulum
    ))
    task_lib.register(2, TaskSpec(
        name="mountaincar_cont",
        reward_min=-100, reward_max=100,
        solve_threshold_norm=0.95, # 95+ score is a solve
        score_metric="reward", step_cap=999,
        window=25,
        dr_min=0.0, dr_max=1.0, # Adjusted DR range for MountainCar
    ))
    
    env = MultiTaskWendigoEnv(task_lib)
    agent = WendigoMultiAgent(env)
    gold = GoldWindow(max_size=64)
    # NEW: Instantiate the global transition bank
    global_bank = GlobalTransitionBank(max_size=5000)

    global_leaderboard = GlobalTopKNorm(k=15)
    
    num_episodes = 750

    for ep in range(1, num_episodes + 1):
        agent.global_episode = ep
        obs, info = env.reset()
        task_id = info["task_id"]
        task_name = info["task_name"]
        task_id_norm = task_id / max(1, env.num_tasks - 1)
        task_spec = task_lib.tasks[task_name]

        done, truncated = False, False
        ep_reward, ep_steps, ep_dark = 0.0, 0.0, 0.0
        vigor_ct, rigor_ct = 0, 0
        ep_transitions = []
        dr_values = []

        while not done and not truncated:
            action, mode = agent.predict_action(obs)
            if mode == "Vigor": vigor_ct += 1
            else: rigor_ct += 1

            next_obs, env_reward, done, truncated, step_info = env.step(action)
            cur_task_id = step_info["task_id"]
            cur_task_name = step_info["task_name"]
            
            if cur_task_name == "cartpole":
                dark = dark_residue_cartpole(next_obs[:4])
                shaped_reward = env_reward + 0.1 * max(0.0, agent.current_dark_median() - dark) - 0.05 * dark
            elif cur_task_name == "pendulum":
                raw_a = step_info.get("raw_action", float(action[0]))
                dark = dark_residue_pendulum(next_obs[:3], raw_a)
                # NEW: Reward shaping for Pendulum
                shaped_reward = (env_reward / 8.0) - 0.15 * dark + 0.05 # Scale reward, penalize DR, add survival bonus
            elif cur_task_name == "mountaincar_cont":
                raw_a = step_info.get("raw_action", float(action[0]))
                dark = dark_residue_mountaincar(next_obs[:2], raw_a)
                shaped_reward = env_reward + 0.25 * max(0.0, agent.current_dark_median() - dark) - 0.05 * dark
            else:
                dark, shaped_reward = 0.0, env_reward
            
            agent.register_dark(dark)
            dr_values.append(dark)

            transition_tuple = (obs, action, next_obs, shaped_reward, dark, done or truncated, cur_task_id)
            ep_transitions.append(transition_tuple)
            # NEW: Add every transition to the global bank
            global_bank.maybe_add(cur_task_id, transition_tuple, dark)

            agent.step_learn(obs, action, next_obs, shaped_reward, done or truncated)

            obs = next_obs
            ep_reward += env_reward
            ep_steps += 1.0
            ep_dark += dark

        if task_spec.score_metric == "reward":
            final_score = ep_reward
        else:
            final_score = ep_steps

        mean_dr = ep_dark / max(ep_steps, 1.0)
        vigor_ratio = vigor_ct / max((vigor_ct + rigor_ct), 1)
        ep_len_norm = min(1.0, ep_steps / task_spec.step_cap)

        task_lib.update_score(task_name, final_score)
        global_leaderboard.add(task_name, final_score, task_lib)

        coh_loss = agent.train_coherence_head(mean_dr, vigor_ratio, ep_len_norm, task_id_norm, final_score, task_spec)
        coh_pred_norm = agent.predict_coherence_score(mean_dr, vigor_ratio, ep_len_norm, task_id_norm)
        
        avg_top_norm = global_leaderboard.average_norm()
        dyn_threshold_norm = avg_top_norm * 0.75
        
        # UPDATED: Call to the new predictive head trainer
        ph_loss, score_hat_norm, lag_hat_norm, lag_target, dr_hat_norm = agent.train_predictive_head(
            mean_dr, vigor_ratio, ep_len_norm, dyn_threshold_norm,
            coh_pred_norm, final_score, task_id_norm, task_spec, ep
        )

        mastered, norm_avg = task_spec.mastery()
        is_gold = (mastered and (mean_dr <= 0.22)) or (norm_avg > (task_spec.solve_threshold_norm * 0.8) and (mean_dr <= 0.25))

        if is_gold:
            ge = GoldEpisode(
                task_id=task_id, task_name=task_name, score=final_score,
                mean_dr=mean_dr, transitions=ep_transitions,
                vigor=vigor_ct, rigor=rigor_ct,
            )
            gold.maybe_add(ge)

        # NEW: Sharpening from the GLOBAL bank, not the gold window
        if ep > 20:
            clean_transitions = global_bank.sample(k=64)
            agent.sharpen_with_whetstones(clean_transitions)

        agent.register_autopoietic_episode({
            "transitions": ep_transitions, "mean_dr": mean_dr, "lag_pred_norm": lag_hat_norm
        })
        if ep % 4 == 0:
            agent.run_autopoietic_cycle()

        # --- UPDATED: Logging ---
        coh_pred_denorm = coh_pred_norm * (task_spec.reward_max - task_spec.reward_min) + task_spec.reward_min
        score_hat_denorm = score_hat_norm * (task_spec.reward_max - task_spec.reward_min) + task_spec.reward_min

        run_type = "Coherent run." if mean_dr <= 0.22 else "Dissonant run."
        print(f"Episode {ep}: {run_type} (task={task_name}) Score: {final_score:.1f}. (Gold: {is_gold})")
        
        # NEW: Extra logging for DR stats
        if dr_values:
            p10, p50, p90 = np.percentile(dr_values, [10, 50, 90])
            print(f"    DR (min/p10/p50/p90/max): {min(dr_values):.2f}/{p10:.2f}/{p50:.2f}/{p90:.2f}/{max(dr_values):.2f}")

        print(
            f"    V/R: {vigor_ct}/{rigor_ct} | CohHead: pred={coh_pred_denorm:.1f} loss={coh_loss:.3f} "
            f"| PredHead: scorê={score_hat_denorm:.1f} L̂={lag_hat_norm:.3f} (target={lag_target:.3f}, loss={ph_loss:.5f})"
        )
        if gold.buffer:
            best = gold.buffer[0]
            print(f"    [GW] best={best.score:.1f} (DR={best.mean_dr:.2f}, task={best.task_name}) | window={len(gold.buffer)}")
        
        mastery_rep = task_lib.mastery_report()
        print(f"    Mastery: {json.dumps(mastery_rep)}")
        
        # NEW: Print leaderboard only every 25 episodes
        if ep % 25 == 0:
            leaderboard_log = [(round(n, 2), t, int(s)) for n, t, s in global_leaderboard.items]
            print(
                f"    Top-15 Norm: {leaderboard_log} | avg_norm={avg_top_norm:.2f} | dyn_thr_norm={dyn_threshold_norm:.2f}"
            )

        if ep % 100 == 0: # Save less frequently
            agent.sac.save(f"wendigo_multi_targeted_ep{ep}")

    print("Targeted multitask training complete.")
    agent.sac.save("wendigo_multi_targeted_final")
    env.close()


if __name__ == "__main__":
    main()
