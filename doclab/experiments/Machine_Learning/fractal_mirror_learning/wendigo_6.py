#!/usr/bin/env python3
"""
Wendigo Multitask (Refactored)
- 1 SAC
- 2 tasks: CartPole-v1 (discrete→Box) + Pendulum-v1
- Per-task score normalization and mastery tracking.
- Global leaderboard based on normalized scores to prevent metric pollution.
- Gated curriculum logic (scaffolding) for adding new tasks.
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
# task-specific dark residue (Unchanged)
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


# ---------------------------------------------------------------------
# NEW: Task Normalization & Library
# ---------------------------------------------------------------------

@dataclass
class TaskSpec:
    """Holds normalization info and score history for a single task."""
    name: str
    reward_min: float          # known or assumed floor (using steps as score)
    reward_max: float          # known or assumed cap (using steps as score)
    solve_threshold_norm: float  # e.g. 0.90 means “90% of cap”
    window: int = 25
    # Factory needed to create a new deque for each instance
    scores: deque = field(default_factory=lambda: deque(maxlen=25))

    def update(self, raw_score: float):
        """Add a new raw score (steps) to the history."""
        self.scores.append(raw_score)

    def normalized_scores(self) -> List[float]:
        """Return the recent history, normalized to [0, 1]."""
        if self.reward_max == self.reward_min:
            return [0.0 for _ in self.scores]

        ns = []
        for s in self.scores:
            clamped = max(self.reward_min, min(self.reward_max, s))
            ns.append((clamped - self.reward_min) / (self.reward_max - self.reward_min))
        return ns

    def mastery(self) -> Tuple[bool, float]:
        """Check if the task is mastered based on the normalized average."""
        ns = self.normalized_scores()
        if len(ns) < self.window // 2:  # not enough data yet
            return False, 0.0
        
        avg = float(np.mean(ns))
        return avg >= self.solve_threshold_norm, avg

class TaskLibrary:
    """Manages all registered tasks and their specs."""
    def __init__(self):
        self.tasks: Dict[str, TaskSpec] = {}
        self.active_order: List[str] = []  # In case we want curriculum sampling

    def register(self, task_spec: TaskSpec):
        """Add a new task to the library."""
        if task_spec.name in self.tasks:
            logger.warning(f"Task {task_spec.name} is already registered. Overwriting.")
        self.tasks[task_spec.name] = task_spec
        if task_spec.name not in self.active_order:
            self.active_order.append(task_spec.name)
        logger.info(f"Registered task: {task_spec.name} (Min: {task_spec.reward_min}, Max: {task_spec.reward_max})")


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

    def ready_for_new_task(self, k_mastered: int = 2, min_norm: float = 0.85) -> bool:
        """Check if we've mastered enough tasks to add a new one."""
        mastered_count = 0
        for name, spec in self.tasks.items():
            mastered, avg = spec.mastery()
            if mastered and avg >= min_norm:
                mastered_count += 1
        return mastered_count >= k_mastered

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
        if spec.reward_max == spec.reward_min:
            norm = 0.0
        else:
            clamped = max(spec.reward_min, min(spec.reward_max, raw_score))
            norm = (clamped - spec.reward_min) / (spec.reward_max - spec.reward_min)
        
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

# (This class is from the prompt, but GoldWindow is used instead in the code)
class TopKPerTask:
    def __init__(self, k=15):
        self.k = k
        self.per_task = defaultdict(list)
    # ... (add, get methods) ...

# ---------------------------------------------------------------------
# multi-task env (Slightly modified to log info)
# ---------------------------------------------------------------------
class MultiTaskWendigoEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self):
        super().__init__()
        self.tasks: List[Dict[str, Any]] = []

        # Task 0: CartPole
        cart = gym.make("CartPole-v1")
        cart_info = characterize_env(cart)
        logger.info(f"Task 0 (cartpole) info: {cart_info}")
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
        logger.info(f"Task 1 (pendulum) info: {pend_info}")
        self.tasks.append({
            "id": 1,
            "name": "pendulum",
            "env": pend,
            "type": "continuous",
            "info": pend_info,
        })
        
        # This confirms the prompt's analysis:
        # Task 0 (CartPole-v1) max_steps: 500
        # Task 1 (Pendulum-v1) max_steps: 200
        # The "score = steps" logic means Pendulum is the 200-capped task.

        self.num_tasks = len(self.tasks)
        self.current_task = None
        self.current_env = None

        self.action_space = gym.spaces.Box(
            low=np.array([-1.0], dtype=np.float32),
            high=np.array([1.0], dtype=np.float32),
            dtype=np.float32,
        )
        high = np.array([np.inf] * 6, dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=-high, high=high, dtype=np.float32)

    def _select_task(self):
        self.current_task = np.random.randint(0, self.num_tasks)
        self.current_env = self.tasks[self.current_task]["env"]

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
        obs6 = self._obs_to_6(obs, self.current_task)
        return obs6, {"task_id": self.current_task, "inner_info": info, "task_name": self.tasks[self.current_task]["name"]}

    def step(self, action: np.ndarray):
        task = self.tasks[self.current_task]
        task_name = task["name"]
        if task["type"] == "discrete":
            a = float(action[0])
            disc = 0 if a < 0.0 else 1
            obs, rew, term, trunc, info = task["env"].step(disc)
            obs6 = self._obs_to_6(obs, self.current_task)
            return obs6, rew, term, trunc, {"task_id": self.current_task, "task_name": task_name, **info}
        else:
            a = float(action[0])
            low, high = -2.0, 2.0
            pend_a = np.array([a * 2.0], dtype=np.float32)
            obs, rew, term, trunc, info = task["env"].step(pend_a)
            obs6 = self._obs_to_6(obs, self.current_task)
            return obs6, rew, term, trunc, {"task_id": self.current_task, "task_name": task_name, "raw_action": float(pend_a[0]), **info}


# ---------------------------------------------------------------------
# Coherence + Predictive heads (Unchanged)
# ---------------------------------------------------------------------
class CoherenceHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, x: th.Tensor) -> th.Tensor:
        return self.net(x)


class PredictiveHead(nn.Module):
    def __init__(self):
        super().__init__()
        # inputs: [mean_dr, vigor_ratio, ep_len_norm, dyn_threshold_norm, coh_pred_norm, task_id_norm]
        self.net = nn.Sequential(
            nn.Linear(6, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 2),  # [score_norm, lag_norm]
        )

    def forward(self, x: th.Tensor) -> th.Tensor:
        return self.net(x)


@dataclass
class GoldEpisode:
    task_id: int
    task_name: str
    score: float # This is 'steps'
    mean_dr: float
    transitions: List[Tuple]
    vigor: int
    rigor: int


class GoldWindow:
    def __init__(self, max_size: int = 64):
        self.max_size = max_size
        self.buffer: List[GoldEpisode] = []

    def maybe_add(self, ep: GoldEpisode):
        self.buffer.append(ep)
        # sort by score then by low DR
        self.buffer.sort(key=lambda e: (-e.score, e.mean_dr))
        if len(self.buffer) > self.max_size:
            self.buffer = self.buffer[: self.max_size]

    def sample_transitions(self, k: int = 16) -> List[Tuple]:
        if not self.buffer:
            return []
        ep = self.buffer[0]
        sorted_tr = sorted(ep.transitions, key=lambda t: t[4])  # by dark
        return sorted_tr[: min(k, len(sorted_tr))]


# ---------------------------------------------------------------------
# Wendigo Agent (Unchanged)
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
        self.sac.set_logger(configure("./wendigo_logs_multi_refactored", ["stdout"]))

        self.coherence_head = CoherenceHead().to(device)
        self.coherence_opt = optim.Adam(self.coherence_head.parameters(), lr=1e-3)

        self.predictive_head = PredictiveHead().to(device)
        self.predictive_opt = optim.Adam(self.predictive_head.parameters(), lr=1e-3)

        self.auto_ring = []
        self.auto_ring_max = 96
        self.temperature = 1.0

        self.dark_running: List[float] = []
        self.max_dark_hist = 8_000

        # teacher params
        self.anneal_episodes = 350
        self.alpha_residue = 0.8
        self.lambda_pred = 1e-3
        self.beta_residue_actor = 0.25
        self.last_teacher_signal = 0.0
        self.global_episode = 0

    # -------------------------
    def register_dark(self, dr: float):
        self.dark_running.append(dr)
        if len(self.dark_running) > self.max_dark_hist:
            self.dark_running = self.dark_running[-self.max_dark_hist :]

    def current_dark_median(self) -> float:
        if not self.dark_running:
            return 0.4
        return float(np.median(self.dark_running))

    # -------------------------
    def predict_action(self, obs: np.ndarray) -> Tuple[np.ndarray, str]:
        if np.random.rand() < 0.35:
            a, _ = self.sac.predict(obs, deterministic=False)
            return a, "Vigor"
        else:
            a, _ = self.sac.predict(obs, deterministic=True)
            return a, "Rigor"

    def step_learn(self, obs, action, next_obs, reward, done):
        self.sac.replay_buffer.add(
            obs=obs,
            next_obs=next_obs,
            action=action,
            reward=reward,
            done=done,
            infos=[{"TimeLimit.truncated": False}],
        )
        self.sac.train(gradient_steps=1)

    def sharpen_with_whetstones(self, transitions: List[Tuple]):
        if not transitions:
            return
        for (obs, action, next_obs, reward, dark, done, task_id) in transitions:
            extra_reward = reward + self.temperature * (0.1 * max(0.0, 0.35 - dark))
            extra_reward -= self.beta_residue_actor * dark
            extra_reward += 0.5 * self.last_teacher_signal
            self.sac.replay_buffer.add(
                obs=obs,
                next_obs=next_obs,
                action=action,
                reward=extra_reward,
                done=done,
                infos=[{"TimeLimit.truncated": False}],
            )
            if self.sac.replay_buffer.size() < self.sac.batch_size:
                return
        self.sac.train(gradient_steps=min(10, len(transitions)))
        self.temperature = max(0.35, self.temperature * 0.997)

    def train_coherence_head(self, mean_dr, vigor_ratio, ep_len_norm, task_id_norm, true_score):
        # Note: true_score is steps. We normalize it for the head.
        score_norm = min(1.0, true_score / 500.0) # Using 500 as a generic cap for the head
        x = th.tensor([[mean_dr, vigor_ratio, ep_len_norm, task_id_norm]], dtype=th.float32, device=device)
        y = th.tensor([[score_norm]], dtype=th.float32, device=device) # Train on normalized score
        pred = self.coherence_head(x)
        loss = ((pred - y) ** 2).mean()
        self.coherence_opt.zero_grad()
        loss.backward()
        self.coherence_opt.step()
        return float(loss.item())

    def predict_coherence_score(self, mean_dr, vigor_ratio, ep_len_norm, task_id_norm):
        with th.no_grad():
            x = th.tensor([[mean_dr, vigor_ratio, ep_len_norm, task_id_norm]], dtype=th.float32, device=device)
            pred_norm = self.coherence_head(x)
            return float(pred_norm.item()) * 500.0 # Return in raw-ish space for logging

    def train_predictive_head(
        self,
        mean_dr: float,
        vigor_ratio: float,
        ep_len_norm: float,
        dyn_threshold_norm: float, # <-- NOW NORMALIZED
        coh_pred_norm: float,
        score: float, # raw steps
        task_id_norm: float,
        episode_idx: int,
    ):
        score_norm = min(1.0, score / 500.0) # Generic 500-cap normalization
        residue = mean_dr

        a = max(0.1, 1.0 - episode_idx / float(self.anneal_episodes))
        clean_component = score_norm - self.alpha_residue * residue
        lag_target = a * score_norm + (1.0 - a) * clean_component
        lag_target = float(np.clip(lag_target, 0.0, 1.0))

        x = th.tensor(
            [[mean_dr, vigor_ratio, ep_len_norm, dyn_threshold_norm, coh_pred_norm, task_id_norm]],
            dtype=th.float32,
            device=device,
        )
        y = th.tensor([[score_norm, lag_target]], dtype=th.float32, device=device)

        out = self.predictive_head(x)
        score_hat = out[0, 0]
        lag_hat = out[0, 1]

        lag_loss = ((lag_hat - y[0, 1]) ** 2).mean()
        score_loss = ((score_hat - y[0, 0]) ** 2).mean()
        total_teacher_loss = lag_loss + 0.1 * score_loss

        self.predictive_opt.zero_grad()
        total_teacher_loss.backward()
        for p in self.predictive_head.parameters():
            if p.grad is not None:
                p.grad *= self.lambda_pred
        self.predictive_opt.step()

        with th.no_grad():
            self.last_teacher_signal = float(lag_hat.clamp(0.0, 1.0).item())

        return float(total_teacher_loss.item()), float(score_hat.item()), float(lag_hat.item()), lag_target

    def register_autopoietic_episode(self, snap: dict):
        self.auto_ring.append(snap)
        if len(self.auto_ring) > self.auto_ring_max:
            self.auto_ring = self.auto_ring[-self.auto_ring_max :]

    def run_autopoietic_cycle(self):
        if len(self.auto_ring) < 5:
            return
        ranked = sorted(self.auto_ring, key=lambda e: (-e["lag_pred_norm"], e["mean_dr"]))
        for ep in ranked[:4]:
            tr = sorted(ep["transitions"], key=lambda t: t[4])[:14]
            self.sharpen_with_whetstones(tr)


# ---------------------------------------------------------------------
# REFACTORED Main Loop
# ---------------------------------------------------------------------
def main():
    env = MultiTaskWendigoEnv()
    agent = WendigoMultiAgent(env)
    gold = GoldWindow(max_size=64)

    # --- NEW: Setup Task Library & Leaderboard ---
    task_lib = TaskLibrary()
    
    # Register Task 0 (CartPole)
    # We use steps as score, max_steps is 500
    task_lib.register(TaskSpec(
        name="cartpole",
        reward_min=0,
        reward_max=500, 
        solve_threshold_norm=0.95, # e.g. 475 steps
        window=25,
    ))
    
    # Register Task 1 (Pendulum)
    # We use steps as score, max_steps is 200
    task_lib.register(TaskSpec(
        name="pendulum",
        reward_min=0,
        reward_max=200,
        solve_threshold_norm=0.95, # e.g. 190 steps
        window=25,
    ))

    # This replaces the old `top_eps = []`
    global_leaderboard = GlobalTopKNorm(k=15)
    # ---------------------------------------------

    num_episodes = 500

    for ep in range(1, num_episodes + 1):
        agent.global_episode = ep
        obs, info = env.reset()
        task_id = info["task_id"]
        task_name = info["task_name"]
        task_id_norm = task_id / max(1, env.num_tasks - 1)

        done = False
        truncated = False

        score = 0.0 # This is steps
        vigor_ct = 0
        rigor_ct = 0
        ep_dark = 0.0
        ep_transitions = []
        steps = 0

        while not done and not truncated:
            action, mode = agent.predict_action(obs)
            if mode == "Vigor":
                vigor_ct += 1
            else:
                rigor_ct += 1

            next_obs, env_reward, done, truncated, step_info = env.step(action)
            cur_task_id = step_info["task_id"]

            if cur_task_id == 0: # cartpole
                dark = dark_residue_cartpole(next_obs[:4])
            else: # pendulum
                raw_a = step_info.get("raw_action", float(action[0]))
                dark = dark_residue_pendulum(next_obs[:3], raw_a)

            agent.register_dark(dark)
            dark_med = agent.current_dark_median()
            cleanliness = max(0.0, dark_med - dark)

            if cur_task_id == 0:
                shaped_reward = env_reward + 0.25 * cleanliness - 0.05 * dark
            else:
                shaped_reward = (env_reward / 10.0) + 0.25 * cleanliness - 0.05 * dark

            agent.step_learn(obs, action, next_obs, shaped_reward, done or truncated)

            ep_transitions.append(
                (obs, action, next_obs, shaped_reward, dark, done or truncated, cur_task_id)
            )

            obs = next_obs
            score += 1.0  # Use steps as the "score"
            ep_dark += dark
            steps += 1

        # --- REFACTORED: Post-Episode Logic ---
        
        mean_dr = ep_dark / max(score, 1.0)
        vigor_ratio = vigor_ct / max((vigor_ct + rigor_ct), 1)
        
        # Get task-specific max steps for ep_len_norm
        task_max_steps = task_lib.tasks[task_name].reward_max
        ep_len_norm = min(1.0, score / task_max_steps)

        # Update per-task history
        task_lib.update_score(task_name, score)
        
        # Update normalized global leaderboard
        global_leaderboard.add(task_name, score, task_lib)

        # Train coherence head
        # We pass the raw step-score; head normalizes it internally
        coh_loss = agent.train_coherence_head(mean_dr, vigor_ratio, ep_len_norm, task_id_norm, score)
        coh_pred = agent.predict_coherence_score(mean_dr, vigor_ratio, ep_len_norm, task_id_norm)
        coh_pred_norm = min(1.2, coh_pred / 500.0) # Generic norm for predictive head

        # NEW: Normalized dynamic threshold
        avg_top_norm = global_leaderboard.average_norm()
        dyn_threshold_norm = avg_top_norm * 0.75 # This is now [0, 1]
        
        # Train predictive head
        ph_loss, score_hat_norm, lag_hat_norm, lag_target_norm = agent.train_predictive_head(
            mean_dr,
            vigor_ratio,
            ep_len_norm,
            dyn_threshold_norm, # Pass the new normalized threshold
            coh_pred_norm,
            score, # Pass raw steps
            task_id_norm,
            ep,
        )

        # NEW: Mastery-based gold window logic
        mastered, norm_avg = task_lib.tasks[task_name].mastery()
        is_gold = (mastered and (mean_dr <= 0.22)) or \
                  (norm_avg > (task_lib.tasks[task_name].solve_threshold_norm * 0.8) and (mean_dr <= 0.25))

        if is_gold:
            ge = GoldEpisode(
                task_id=task_id,
                task_name=task_name,
                score=score,
                mean_dr=mean_dr,
                transitions=ep_transitions,
                vigor=vigor_ct,
                rigor=rigor_ct,
            )
            gold.maybe_add(ge)
            this_low = sorted(ep_transitions, key=lambda t: t[4])[: max(6, len(ep_transitions) // 6)]
            agent.sharpen_with_whetstones(this_low)

        # Autopoiesis (unchanged)
        agent.register_autopoietic_episode(
            {
                "task_id": task_id,
                "score": score,
                "mean_dr": mean_dr,
                "vigor_ratio": vigor_ratio,
                "ep_len_norm": ep_len_norm,
                "dyn_threshold": dyn_threshold_norm, # Store norm threshold
                "coh_pred": coh_pred,
                "lag_target_norm": lag_target_norm,
                "lag_pred_norm": lag_hat_norm,
                "transitions": ep_transitions,
            }
        )

        if ep % 4 == 0:
            agent.run_autopoietic_cycle()

        # --- REFACTORED: Logging ---
        run_type = "Coherent run." if mean_dr <= 0.22 else "Dissonant run."
        print(
            f"Episode {ep}: {run_type} (task={task_name}) Score: {score:.0f}. (Gold: {is_gold})"
        )
        print(
            f"    Avg DR: {mean_dr:.2f} | V/R: {vigor_ct}/{rigor_ct} | CohHead: pred={coh_pred:.1f} loss={coh_loss:.3f} "
            f"| PredHead: scorê={score_hat_norm*500.0:.1f} L̂={lag_hat_norm:.3f} (target={lag_target_norm:.3f}, loss={ph_loss:.5f})"
        )
        if gold.buffer:
            best = gold.buffer[0]
            print(
                f"    [GW] best={best.score:.0f} (DR={best.mean_dr:.2f}, task={best.task_name}) | window={len(gold.buffer)}"
            )
        
        # New Mastery Report
        mastery_rep = task_lib.mastery_report()
        print(f"    Mastery: {json.dumps(mastery_rep)}")
        
        # New Normalized Leaderboard Log
        leaderboard_log = [(round(n, 2), t, int(s)) for n, t, s in global_leaderboard.items]
        print(
            f"    Top-15 Norm: {leaderboard_log} | avg_norm={avg_top_norm:.2f} | dyn_thr_norm={dyn_threshold_norm:.2f}"
        )
        
        # --- NEW: Curriculum Gating ---
        if ep > 50 and ep % 10 == 0: # Check every 10 eps after a warmup
            if task_lib.ready_for_new_task(k_mastered=2, min_norm=0.90):
                logger.info(f"--- CURRICULUM: All {len(task_lib.tasks)} tasks mastered. Ready for new challenges! ---")
                # This is where you would add a new task:
                # e.g. task_lib.register(TaskSpec(name="mountaincar", ...))
                # And you would need to update/rebuild MultiTaskWendigoEnv
                # For now, we just log.
                pass

        if ep % 20 == 0:
            agent.sac.save(f"wendigo_multi_refactored_ep{ep}")
            with open(f"{agent.gold_dir}/wendigo_multi_refactored_gold.json", "w") as f:
                json.dump(
                    [
                        {
                            "task_id": g.task_id,
                            "task_name": g.task_name,
                            "score": g.score,
                            "mean_dr": g.mean_dr,
                            "vigor": g.vigor,
                            "rigor": g.rigor,
                            "len_transitions": len(g.transitions),
                        }
                        for g in gold.buffer
                    ],
                    f,
                    indent=2,
                )

    print("Refactored multitask training complete.")
    agent.sac.save("wendigo_multi_refactored_final")
    env.close()


if __name__ == "__main__":
    main()
