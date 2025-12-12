#!/usr/bin/env python3
"""
Wendigo (discrete-wrapped) v3 — teacher/actor aligned
- predictive head becomes the *teacher* for a Pirouette-style L
- SAC stays the *actor* and is rewarded with the detached teacher signal
- autopoietic cycle replays low-DR steps but now on the *same* coordinate system
- annealing: early = hunt hard, late = hunt clean
"""

import os
import sys
import math
import time
import logging
import json
from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple

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
logger = logging.getLogger("wendigo")

device = th.device("cuda") if th.cuda.is_available() else th.device("cpu")


# ---------------------------------------------------------------------
# Discrete → Continuous wrapper
# ---------------------------------------------------------------------
class DiscreteToBoxActionWrapper(gym.ActionWrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(
            low=np.array([-1.0], dtype=np.float32),
            high=np.array([1.0], dtype=np.float32),
            dtype=np.float32,
        )

    def action(self, action):
        if isinstance(action, np.ndarray):
            a = float(action[0])
        else:
            a = float(action)
        discrete = 0 if a < 0.0 else 1
        return discrete


# ---------------------------------------------------------------------
# Dark Residue
# ---------------------------------------------------------------------
def calculate_dark_residue(obs: np.ndarray) -> float:
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    dr = (
        0.4 * abs(cart_pos)
        + 0.2 * abs(cart_vel)
        + 1.5 * abs(pole_angle)
        + 0.3 * abs(pole_vel)
    )
    return float(dr)


# ---------------------------------------------------------------------
# Coherence-only critic
# ---------------------------------------------------------------------
class CoherenceHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, x: th.Tensor) -> th.Tensor:
        return self.net(x)


# ---------------------------------------------------------------------
# Predictive (teacher) head
# input: [mean_dr, vigor_ratio, ep_len_norm, dyn_threshold_norm, coh_pred_norm]
# output: [score_hat_norm, lag_hat_norm]
# ---------------------------------------------------------------------
class PredictiveHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(5, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 2),  # [score_norm, lag_norm]
        )

    def forward(self, x: th.Tensor) -> th.Tensor:
        return self.net(x)


# ---------------------------------------------------------------------
# Gold window
# ---------------------------------------------------------------------
@dataclass
class GoldEpisode:
    score: int
    mean_dr: float
    transitions: List[Tuple[np.ndarray, np.ndarray, np.ndarray, float, float, bool]]
    vigor: int
    rigor: int


class GoldWindow:
    def __init__(self, max_size: int = 48):
        self.max_size = max_size
        self.buffer: List[GoldEpisode] = []

    def maybe_add(self, ep: GoldEpisode):
        self.buffer.append(ep)
        self.buffer.sort(key=lambda e: e.score, reverse=True)
        if len(self.buffer) > self.max_size:
            self.buffer = self.buffer[: self.max_size]

    def sample_transitions(self, k: int = 16):
        if not self.buffer:
            return []
        ep = self.buffer[0]
        sorted_tr = sorted(ep.transitions, key=lambda t: t[-2])  # by dark
        return sorted_tr[: min(k, len(sorted_tr))]


# ---------------------------------------------------------------------
# Wendigo Agent
# ---------------------------------------------------------------------
class WendigoAgent:
    def __init__(self, env: gym.Env, seed: int = 42):
        self.env = env
        self.seed = seed
        self.env.reset(seed=seed)
        th.manual_seed(seed)
        np.random.seed(seed)
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
            buffer_size=200_000,
            batch_size=256,
            train_freq=(1, "step"),
            gradient_steps=1,
            gamma=0.99,
            action_noise=action_noise,
        )
        self.sac._setup_model()

        logger = configure("./wendigo_logs", ["stdout"])
        self.sac.set_logger(logger)

        self.coherence_head = CoherenceHead().to(device)
        self.coherence_opt = optim.Adam(self.coherence_head.parameters(), lr=1e-3)

        # teacher
        self.predictive_head = PredictiveHead().to(device)
        self.predictive_opt = optim.Adam(self.predictive_head.parameters(), lr=1e-3)

        # autopoiesis
        self.auto_ring = []
        self.auto_ring_max = 64
        self.temperature = 1.0  # cools over time

        # dark stats
        self.dark_running: List[float] = []
        self.max_dark_hist = 5_000

        # teacher/actor coupling params
        self.anneal_episodes = 300        # how long we stay in "hunt-first"
        self.alpha_residue = 0.8          # how strongly residue pulls L down
        self.lambda_pred = 1e-3           # how loud the teacher is overall
        self.beta_residue_actor = 0.25    # actor penalty per-step for dark in replay
        self.last_teacher_signal = 0.0    # detached teacher lag_norm, 0..1
        self.global_episode = 0

    # ---- dark stats --------------------------------------------------
    def register_dark(self, dr: float):
        self.dark_running.append(dr)
        if len(self.dark_running) > self.max_dark_hist:
            self.dark_running = self.dark_running[-self.max_dark_hist :]

    def current_dark_median(self) -> float:
        if not self.dark_running:
            return 0.4
        return float(np.median(self.dark_running))

    # ---- action ------------------------------------------------------
    def predict_action(self, obs: np.ndarray) -> Tuple[np.ndarray, str]:
        if np.random.rand() < 0.35:
            action, _ = self.sac.predict(obs, deterministic=False)
            return action, "Vigor"
        else:
            action, _ = self.sac.predict(obs, deterministic=True)
            return action, "Rigor"

    # ---- learning ----------------------------------------------------
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
        """
        Replay helper. This is where we make the *actor* chase the *teacher*.
        """
        if not transitions:
            return
        for (obs, action, next_obs, reward, dark, done) in transitions:
            # base extra: reward clean steps, scaled by temperature
            extra_reward = reward + self.temperature * (0.1 * max(0.0, 0.3 - dark))
            # actor penalty for dark residue — makes "tug" point the same direction
            extra_reward -= self.beta_residue_actor * dark
            # actor bonus: detached teacher signal
            extra_reward += 0.5 * self.last_teacher_signal  # teacher in charge

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
        self.sac.train(gradient_steps=min(8, len(transitions)))

    def train_coherence_head(self, mean_dr, vigor_ratio, ep_len_norm, true_score):
        x = th.tensor([[mean_dr, vigor_ratio, ep_len_norm]], dtype=th.float32, device=device)
        y = th.tensor([[true_score]], dtype=th.float32, device=device)
        pred = self.coherence_head(x)
        loss = ((pred - y) ** 2).mean()
        self.coherence_opt.zero_grad()
        loss.backward()
        self.coherence_opt.step()
        return float(loss.item())

    def predict_coherence_score(self, mean_dr, vigor_ratio, ep_len_norm):
        with th.no_grad():
            x = th.tensor([[mean_dr, vigor_ratio, ep_len_norm]], dtype=th.float32, device=device)
            pred = self.coherence_head(x)
            return float(pred.item())

    # >>> teacher: normalized Pirouette L
    def train_predictive_head(
        self,
        mean_dr: float,
        vigor_ratio: float,
        ep_len_norm: float,
        dyn_threshold_norm: float,
        coh_pred_norm: float,
        score: int,
        episode_idx: int,
    ):
        # normalize score to 0..1
        score_norm = min(1.0, score / 500.0)
        residue = mean_dr  # already small in cartpole

        # anneal: early = pure hunt, late = hunt clean
        a = max(0.1, 1.0 - episode_idx / float(self.anneal_episodes))

        # Pirouette target
        clean_component = score_norm - self.alpha_residue * residue
        lag_target = a * score_norm + (1.0 - a) * clean_component
        # clamp just in case
        lag_target = float(np.clip(lag_target, 0.0, 1.0))

        x = th.tensor(
            [[mean_dr, vigor_ratio, ep_len_norm, dyn_threshold_norm, coh_pred_norm]],
            dtype=th.float32,
            device=device,
        )
        y = th.tensor([[score_norm, lag_target]], dtype=th.float32, device=device)

        out = self.predictive_head(x)
        score_hat = out[0, 0]
        lag_hat = out[0, 1]

        # main: learn L-geometry
        lag_loss = ((lag_hat - y[0, 1]) ** 2).mean()
        # tiny: keep score roughly in line (optional)
        score_loss = ((score_hat - y[0, 0]) ** 2).mean()

        total_teacher_loss = lag_loss + 0.1 * score_loss

        self.predictive_opt.zero_grad()
        total_teacher_loss.backward()
        # scale so it doesn't sponge
        for p in self.predictive_head.parameters():
            if p.grad is not None:
                p.grad *= self.lambda_pred
        self.predictive_opt.step()

        # DETACH the teacher signal for the actor
        with th.no_grad():
            self.last_teacher_signal = float(lag_hat.clamp(0.0, 1.0).item())

        return float(total_teacher_loss.item()), float(score_hat.item()), float(lag_hat.item()), lag_target

    # >>> NEW: autopoietic digest
    def register_autopoietic_episode(self, snapshot: dict):
        self.auto_ring.append(snapshot)
        if len(self.auto_ring) > self.auto_ring_max:
            self.auto_ring = self.auto_ring[-self.auto_ring_max:]

    def run_autopoietic_cycle(self):
        if len(self.auto_ring) < 4:
            return
        # sort by predicted L desc, then DR asc
        ranked = sorted(
            self.auto_ring,
            key=lambda e: (-e["lag_pred_norm"], e["mean_dr"])
        )
        # take top 3 to digest
        for ep in ranked[:3]:
            tr = sorted(ep["transitions"], key=lambda t: t[4])[:12]
            self.sharpen_with_whetstones(tr)
        # cool a bit
        self.temperature = max(0.35, self.temperature * 0.997)


# ---------------------------------------------------------------------
# training loop
# ---------------------------------------------------------------------
def main():
    base_env = gym.make("CartPole-v1")
    env = DiscreteToBoxActionWrapper(base_env)

    agent = WendigoAgent(env)
    gold = GoldWindow(max_size=48)

    num_episodes = 500
    top_eps = []  # will be list of {"score":..., "dark":...}

    for ep in range(1, num_episodes + 1):
        agent.global_episode = ep
        obs, _ = env.reset()
        done = False
        truncated = False

        score = 0
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

            next_obs, env_reward, done, truncated, info = env.step(action)
            dark = calculate_dark_residue(next_obs)
            agent.register_dark(dark)

            dark_med = agent.current_dark_median()
            cleanliness = max(0.0, dark_med - dark)

            # base shape
            shaped_reward = env_reward + 0.25 * cleanliness - 0.05 * dark

            agent.step_learn(obs, action, next_obs, shaped_reward, done or truncated)

            ep_transitions.append((obs, action, next_obs, shaped_reward, dark, done or truncated))

            obs = next_obs
            score += 1
            ep_dark += dark
            steps += 1

        # -------- episode-level stats ----------
        mean_dr = ep_dark / max(score, 1)
        vigor_ratio = vigor_ct / max((vigor_ct + rigor_ct), 1)
        ep_len_norm = min(1.0, score / 500.0)

        coh_loss = agent.train_coherence_head(mean_dr, vigor_ratio, ep_len_norm, score)
        coh_pred = agent.predict_coherence_score(mean_dr, vigor_ratio, ep_len_norm)

        # --- leaderboard insert with prime-directive tie-break ---
        top_eps.append({"score": score, "dark": mean_dr})
        top_eps.sort(key=lambda e: (-e["score"], e["dark"]))
        top_eps = top_eps[:15]
        avg_top = sum(e["score"] for e in top_eps) / len(top_eps)
        dyn_threshold = int(avg_top * 0.75)

        # normalize for teacher
        dyn_threshold_norm = min(1.2, dyn_threshold / 500.0)
        coh_pred_norm = min(1.2, coh_pred / 500.0)

        # >>> train teacher on Pirouette target (detached for actor)
        ph_loss, score_hat_norm, lag_hat_norm, lag_target_norm = agent.train_predictive_head(
            mean_dr,
            vigor_ratio,
            ep_len_norm,
            dyn_threshold_norm,
            coh_pred_norm,
            score,
            ep,
        )

        # GOLD WINDOW
        is_gold = (mean_dr <= 0.20 and score >= (dyn_threshold - 20)) or (
            coh_pred >= (dyn_threshold - 10)
        )
        if is_gold:
            ge = GoldEpisode(
                score=score,
                mean_dr=mean_dr,
                transitions=ep_transitions,
                vigor=vigor_ct,
                rigor=rigor_ct,
            )
            gold.maybe_add(ge)

            # replay the cleanest steps
            this_low = sorted(ep_transitions, key=lambda t: t[4])[: max(5, len(ep_transitions) // 6)]
            agent.sharpen_with_whetstones(this_low)

            if ep % 5 == 0:
                gw_tr = gold.sample_transitions(k=18)
                agent.sharpen_with_whetstones(gw_tr)

            if ep % 10 == 0:
                agent.sac.save(f"wendigo_sac_ep{ep}")
                with open(f"{agent.gold_dir}/wendigo_gold_window.json", "w") as f:
                    json.dump(
                        [
                            {
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

        # register in auto ring
        agent.register_autopoietic_episode(
            {
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

        # ---- print
        run_type = "Coherent run." if mean_dr <= 0.22 else "Dissonant run."
        # denorm score pred for human
        ph_score_denorm = score_hat_norm * 500.0
        print(f"Episode {ep}: {run_type} Score: {score}. (Gold: {is_gold})")
        print(
            f"    Avg Dark Residue: {mean_dr:.2f} | Vigor/Rigor: {vigor_ct}/{rigor_ct} "
            f"| CohHead: pred={coh_pred:.1f} loss={coh_loss:.3f} "
            f"| PredHead: scorê={ph_score_denorm:.1f} L̂={lag_hat_norm:.3f} (target={lag_target_norm:.3f}, loss={ph_loss:.5f})"
        )
        if gold.buffer:
            best_g = gold.buffer[0]
            print(
                f"    [GW] best={best_g.score} (DR={best_g.mean_dr:.2f}) | window={len(gold.buffer)}"
            )
        print(
            f"    Top-15 scores: {[e['score'] for e in top_eps]} | avg={avg_top:.2f} | dyn_threshold={dyn_threshold}"
        )

    print("Training complete.")
    agent.sac.save("wendigo_sac_model")
    env.close()


if __name__ == "__main__":
    main()
