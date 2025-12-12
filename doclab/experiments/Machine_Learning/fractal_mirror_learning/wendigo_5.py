#!/usr/bin/env python3
"""
Wendigo Multitask
- 1 SAC
- 2 tasks: CartPole-v1 (discrete→Box) + Pendulum-v1
- shared teacher/actor: teacher sees task_id, actor chases detached L
- autopoietic ring replays clean transitions for both tasks
"""

import os, sys, json, logging
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
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
    # angle from upright (0, 1) ~ (cos=1, sin=0):
    angle_err = np.arctan2(sin_th, cos_th)  # -pi..pi
    # action is in [-1, 1] *after* we rescale
    dr = (
        0.8 * abs(angle_err)    # care about upright
        + 0.15 * abs(thdot)     # care about smooth motion
        + 0.05 * abs(action)    # care about energy spent
    )
    return float(dr)


# ---------------------------------------------------------------------
# multi-task env
# ---------------------------------------------------------------------
class MultiTaskWendigoEnv(gym.Env):
    """
    One env that randomly picks among several underlying envs at reset.
    - action_space: Box([-1,1], shape=(1,))
    - observation_space: Box([-inf, inf], shape=(6,))
      last value = task_id_norm
    """

    metadata = {"render_modes": []}

    def __init__(self):
        super().__init__()
        # build actual gym envs
        self.tasks: List[Dict[str, Any]] = []

        # Task 0: CartPole
        cart = gym.make("CartPole-v1")
        self.tasks.append({
            "id": 0,
            "name": "cartpole",
            "env": cart,
            "type": "discrete",   # we will map [-1,1] -> {0,1}
        })

        # Task 1: Pendulum
        pend = gym.make("Pendulum-v1")
        self.tasks.append({
            "id": 1,
            "name": "pendulum",
            "env": pend,
            "type": "continuous",  # we will scale [-1,1] -> env.action_space
        })

        self.num_tasks = len(self.tasks)
        self.current_task = None
        self.current_env = None

        # unified action space
        self.action_space = gym.spaces.Box(
            low=np.array([-1.0], dtype=np.float32),
            high=np.array([1.0], dtype=np.float32),
            dtype=np.float32,
        )

        # unified obs space (6-dim)
        high = np.array([np.inf] * 6, dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=-high, high=high, dtype=np.float32)

    def _select_task(self):
        self.current_task = np.random.randint(0, self.num_tasks)
        self.current_env = self.tasks[self.current_task]["env"]

    def _obs_to_6(self, obs: np.ndarray, task_id: int) -> np.ndarray:
        # pad/truncate to 5, then append task_id_norm
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
        return obs6, {"task_id": self.current_task, "inner_info": info}

    def step(self, action: np.ndarray):
        # map action to underlying env
        task = self.tasks[self.current_task]
        if task["type"] == "discrete":
            # cartpole: map to 0/1
            a = float(action[0])
            disc = 0 if a < 0.0 else 1
            obs, rew, term, trunc, info = task["env"].step(disc)
            # we'll shape later
            obs6 = self._obs_to_6(obs, self.current_task)
            return obs6, rew, term, trunc, {"task_id": self.current_task, **info}
        else:
            # pendulum: env expects [-2,2], we have [-1,1]
            a = float(action[0])
            low, high = -2.0, 2.0
            pend_a = np.array([a * 2.0], dtype=np.float32)  # scale
            obs, rew, term, trunc, info = task["env"].step(pend_a)
            obs6 = self._obs_to_6(obs, self.current_task)
            return obs6, rew, term, trunc, {"task_id": self.current_task, "raw_action": float(pend_a[0]), **info}


# ---------------------------------------------------------------------
# Coherence + Predictive heads (same as before, just +task_id)
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
    score: float
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
        self.sac.set_logger(configure("./wendigo_logs_multi", ["stdout"]))

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
        x = th.tensor([[mean_dr, vigor_ratio, ep_len_norm, task_id_norm]], dtype=th.float32, device=device)
        y = th.tensor([[true_score]], dtype=th.float32, device=device)
        pred = self.coherence_head(x)
        loss = ((pred - y) ** 2).mean()
        self.coherence_opt.zero_grad()
        loss.backward()
        self.coherence_opt.step()
        return float(loss.item())

    def predict_coherence_score(self, mean_dr, vigor_ratio, ep_len_norm, task_id_norm):
        with th.no_grad():
            x = th.tensor([[mean_dr, vigor_ratio, ep_len_norm, task_id_norm]], dtype=th.float32, device=device)
            pred = self.coherence_head(x)
            return float(pred.item())

    def train_predictive_head(
        self,
        mean_dr: float,
        vigor_ratio: float,
        ep_len_norm: float,
        dyn_threshold_norm: float,
        coh_pred_norm: float,
        score: float,
        task_id_norm: float,
        episode_idx: int,
    ):
        score_norm = min(1.0, score / 500.0)
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


def main():
    env = MultiTaskWendigoEnv()
    agent = WendigoMultiAgent(env)
    gold = GoldWindow(max_size=64)

    num_episodes = 500
    top_eps = []

    for ep in range(1, num_episodes + 1):
        agent.global_episode = ep
        obs, info = env.reset()
        task_id = info["task_id"]
        task_id_norm = task_id / max(1, env.num_tasks - 1)

        done = False
        truncated = False

        score = 0.0
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
            cur_task = step_info["task_id"]

            # pick DR by task
            if cur_task == 0:
                dark = dark_residue_cartpole(next_obs[:4])
            else:
                # for pendulum we want the raw action before we normalized
                raw_a = step_info.get("raw_action", float(action[0]))
                dark = dark_residue_pendulum(next_obs[:3], raw_a)

            agent.register_dark(dark)
            dark_med = agent.current_dark_median()
            cleanliness = max(0.0, dark_med - dark)

            # shape by task a bit
            if cur_task == 0:
                shaped_reward = env_reward + 0.25 * cleanliness - 0.05 * dark
            else:
                # pendulum reward is negative → lift it + DR
                shaped_reward = (env_reward / 10.0) + 0.25 * cleanliness - 0.05 * dark

            agent.step_learn(obs, action, next_obs, shaped_reward, done or truncated)

            ep_transitions.append(
                (obs, action, next_obs, shaped_reward, dark, done or truncated, cur_task)
            )

            obs = next_obs
            score += 1.0  # generic step score; for pendulum this is "duration"
            ep_dark += dark
            steps += 1

        mean_dr = ep_dark / max(score, 1.0)
        vigor_ratio = vigor_ct / max((vigor_ct + rigor_ct), 1)
        ep_len_norm = min(1.0, score / 500.0)

        coh_loss = agent.train_coherence_head(mean_dr, vigor_ratio, ep_len_norm, task_id_norm, score)
        coh_pred = agent.predict_coherence_score(mean_dr, vigor_ratio, ep_len_norm, task_id_norm)

        # leaderboard (global)
        top_eps.append({"score": score, "dark": mean_dr, "task": task_id})
        top_eps.sort(key=lambda e: (-e["score"], e["dark"]))
        top_eps = top_eps[:15]
        avg_top = sum(e["score"] for e in top_eps) / len(top_eps)
        dyn_threshold = int(avg_top * 0.75)
        dyn_threshold_norm = min(1.2, dyn_threshold / 500.0)
        coh_pred_norm = min(1.2, coh_pred / 500.0)

        ph_loss, score_hat_norm, lag_hat_norm, lag_target_norm = agent.train_predictive_head(
            mean_dr,
            vigor_ratio,
            ep_len_norm,
            dyn_threshold_norm,
            coh_pred_norm,
            score,
            task_id_norm,
            ep,
        )

        # gold: allow per-task
        is_gold = (
            (mean_dr <= 0.22 and score >= (dyn_threshold - 20))
            or (coh_pred >= (dyn_threshold - 10))
        )
        if is_gold:
            ge = GoldEpisode(
                task_id=task_id,
                score=score,
                mean_dr=mean_dr,
                transitions=ep_transitions,
                vigor=vigor_ct,
                rigor=rigor_ct,
            )
            gold.maybe_add(ge)
            this_low = sorted(ep_transitions, key=lambda t: t[4])[: max(6, len(ep_transitions) // 6)]
            agent.sharpen_with_whetstones(this_low)

        agent.register_autopoietic_episode(
            {
                "task_id": task_id,
                "score": score,
                "mean_dr": mean_dr,
                "vigor_ratio": vigor_ratio,
                "ep_len_norm": ep_len_norm,
                "dyn_threshold": dyn_threshold,
                "coh_pred": coh_pred,
                "lag_target_norm": lag_target_norm,
                "lag_pred_norm": lag_hat_norm,
                "transitions": ep_transitions,
            }
        )

        if ep % 4 == 0:
            agent.run_autopoietic_cycle()

        # print
        run_type = "Coherent run." if mean_dr <= 0.22 else "Dissonant run."
        print(
            f"Episode {ep}: {run_type} (task={task_id}) Score: {score:.0f}. (Gold: {is_gold})"
        )
        print(
            f"    Avg DR: {mean_dr:.2f} | V/R: {vigor_ct}/{rigor_ct} | CohHead: pred={coh_pred:.1f} loss={coh_loss:.3f} "
            f"| PredHead: scorê={score_hat_norm*500.0:.1f} L̂={lag_hat_norm:.3f} (target={lag_target_norm:.3f}, loss={ph_loss:.5f})"
        )
        if gold.buffer:
            best = gold.buffer[0]
            print(
                f"    [GW] best={best.score:.0f} (DR={best.mean_dr:.2f}, task={best.task_id}) | window={len(gold.buffer)}"
            )
        print(
            f"    Top-15: {[{'t':e['task'],'s':e['score']} for e in top_eps]} | avg={avg_top:.2f} | dyn_thr={dyn_threshold}"
        )

        if ep % 20 == 0:
            agent.sac.save(f"wendigo_multi_ep{ep}")
            with open(f"{agent.gold_dir}/wendigo_multi_gold.json", "w") as f:
                json.dump(
                    [
                        {
                            "task_id": g.task_id,
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

    print("Multitask training complete.")
    agent.sac.save("wendigo_multi_final")
    env.close()


if __name__ == "__main__":
    main()
