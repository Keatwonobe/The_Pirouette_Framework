#!/usr/bin/env python3
"""
Wendigo (discrete-wrapped)
--------------------------
Version that runs SAC on CartPole-v1 by wrapping the discrete action space
into a 1D continuous Box and mapping back.

Key pieces kept:
- logger
- cuda-safety
- dark residue shaping
- gold window
- whetstone replays
- coherence-only critic
"""

import os
import sys
import math
import time
import logging
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

# ---------------------------------------------------------------------
# logger
# ---------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("wendigo")


# ---------------------------------------------------------------------
# device safety
# ---------------------------------------------------------------------
device = th.device("cuda") if th.cuda.is_available() else th.device("cpu")


# ---------------------------------------------------------------------
# Discrete → Continuous wrapper
# SAC wants Box, CartPole gives Discrete(2)
# We'll expose Box([-1],[1]) and map back to {0,1}
# ---------------------------------------------------------------------
class DiscreteToBoxActionWrapper(gym.ActionWrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        # SAC likes float32 boxes
        self.action_space = gym.spaces.Box(
            low=np.array([-1.0], dtype=np.float32),
            high=np.array([1.0], dtype=np.float32),
            dtype=np.float32,
        )

    def action(self, action):
        """
        action: np.ndarray or float in [-1, 1]
        map to discrete 0/1
        """
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
    # obs = [cart_pos, cart_vel, pole_angle, pole_vel]
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
        # sort transitions by DR (t[-2])
        sorted_tr = sorted(ep.transitions, key=lambda t: t[-2])
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

        n_actions = env.action_space.shape[0]
        action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

        # SAC can now run because the env is Box
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

        # (optional but nice) give it a logger so .train() is happy
        logger = configure("./wendigo_logs", ["stdout"])
        self.sac.set_logger(logger)


        self.coherence_head = CoherenceHead().to(device)
        self.coherence_opt = optim.Adam(self.coherence_head.parameters(), lr=1e-3)

        self.dark_running: List[float] = []
        self.max_dark_hist = 5_000

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
        # vigor vs rigor
        if np.random.rand() < 0.35:
            action, _ = self.sac.predict(obs, deterministic=False)
            return action, "Vigor"
        else:
            action, _ = self.sac.predict(obs, deterministic=True)
            return action, "Rigor"

    # ---- learning ----------------------------------------------------
    def step_learn(self, obs, action, next_obs, reward, done):
        # action has shape (1,) because of our wrapper
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
        for (obs, action, next_obs, reward, dark, done) in transitions:
            extra_reward = reward + 0.1 * max(0.0, 0.3 - dark)
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


# ---------------------------------------------------------------------
# training loop
# ---------------------------------------------------------------------
def main():
    base_env = gym.make("CartPole-v1")
    env = DiscreteToBoxActionWrapper(base_env)  # <-- important fix

    agent = WendigoAgent(env)
    gold = GoldWindow(max_size=48)

    num_episodes = 500
    top_k = 15
    top_scores: List[int] = []

    for ep in range(1, num_episodes + 1):
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

            # env.step expects discrete, wrapper will convert our Box action → 0/1
            next_obs, env_reward, done, truncated, info = env.step(action)

            dark = calculate_dark_residue(next_obs)
            agent.register_dark(dark)

            dark_med = agent.current_dark_median()
            cleanliness = max(0.0, dark_med - dark)
            shaped_reward = env_reward + 0.25 * cleanliness - 0.05 * dark

            agent.step_learn(obs, action, next_obs, shaped_reward, done or truncated)

            ep_transitions.append((obs, action, next_obs, shaped_reward, dark, done or truncated))

            obs = next_obs
            score += 1
            ep_dark += dark
            steps += 1

        mean_dr = ep_dark / max(score, 1)
        vigor_ratio = vigor_ct / max((vigor_ct + rigor_ct), 1)
        ep_len_norm = min(1.0, score / 500.0)

        coh_loss = agent.train_coherence_head(mean_dr, vigor_ratio, ep_len_norm, score)
        coh_pred = agent.predict_coherence_score(mean_dr, vigor_ratio, ep_len_norm)

        # maintain top scores
        top_scores.append(score)
        top_scores = sorted(top_scores, reverse=True)[:top_k]
        avg_top = sum(top_scores) / len(top_scores)
        dyn_threshold = int(avg_top * 0.78)

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

            # whetstones from this episode
            this_low = sorted(ep_transitions, key=lambda t: t[4])[: max(5, len(ep_transitions) // 6)]
            agent.sharpen_with_whetstones(this_low)

            # periodic global whetstone
            if ep % 5 == 0:
                gw_tr = gold.sample_transitions(k=18)
                agent.sharpen_with_whetstones(gw_tr)

        # print like your runs
        run_type = "Coherent run." if mean_dr <= 0.22 else "Dissonant run."
        print(
            f"Episode {ep}: {run_type} Score: {score}. (Gold: {is_gold})"
        )
        print(
            f"    Avg Dark Residue: {mean_dr:.2f} | Vigor/Rigor: {vigor_ct}/{rigor_ct} "
            f"| CohHead: pred={coh_pred:.1f} loss={coh_loss:.3f}"
        )
        print(
            f"    Top-{len(top_scores)} scores: {top_scores} | avg={avg_top:.2f} | dyn_threshold={dyn_threshold}"
        )
        if gold.buffer:
            best_g = gold.buffer[0]
            print(
                f"    [GW] best={best_g.score} (DR={best_g.mean_dr:.2f}) | window={len(gold.buffer)}"
            )

    print("Training complete.")
    agent.sac.save("wendigo_sac_model")
    env.close()


if __name__ == "__main__":
    main()
