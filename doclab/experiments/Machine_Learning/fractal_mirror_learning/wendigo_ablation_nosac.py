#!/usr/bin/env python3
"""
Wendigo (discrete-wrapped) with Ablation Switches
-------------------------------------------------
Version that runs SAC on CartPole-v1 by wrapping the discrete action space
into a 1D continuous Box and mapping back.

Includes ablation switches to test the impact of each major component.
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

# ---------------------------------------------------------------------
# ABLATION SWITCHES
# Set these to True or False to test component contributions.
# ---------------------------------------------------------------------
ENABLE_REWARD_SHAPING = True   # Use Dark Residue to shape the reward signal?
ENABLE_COHERENCE_CRITIC = False   # Use the Coherence Head to predict scores and identify gold?
ENABLE_GOLD_WINDOW = False      # Store best episodes in the Gold Window?
ENABLE_WHETSTONE_REPLAYS = False  # Replay best transitions from the Gold Window?
# ---------------------------------------------------------------------

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
        self.gold_dir = "./wendigo_gold"
        os.makedirs(self.gold_dir, exist_ok=True)
        self.gold_buffer = []
        self.max_gold_buffer = 32

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

        if ENABLE_COHERENCE_CRITIC:
            self.coherence_head = CoherenceHead().to(device)
            self.coherence_opt = optim.Adam(self.coherence_head.parameters(), lr=1e-3)

        self.dark_running: List[float] = []
        self.max_dark_hist = 5_000

    def register_dark(self, dr: float):
        self.dark_running.append(dr)
        if len(self.dark_running) > self.max_dark_hist:
            self.dark_running = self.dark_running[-self.max_dark_hist :]

    def current_dark_median(self) -> float:
        if not self.dark_running:
            return 0.4
        return float(np.median(self.dark_running))

    def predict_action(self, obs: np.ndarray) -> Tuple[np.ndarray, str]:
        if np.random.rand() < 0.35:
            action, _ = self.sac.predict(obs, deterministic=False)
            return action, "Vigor"
        else:
            action, _ = self.sac.predict(obs, deterministic=True)
            return action, "Rigor"

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
        if not ENABLE_COHERENCE_CRITIC:
            return 0.0
        x = th.tensor([[mean_dr, vigor_ratio, ep_len_norm]], dtype=th.float32, device=device)
        y = th.tensor([[true_score]], dtype=th.float32, device=device)
        pred = self.coherence_head(x)
        loss = ((pred - y) ** 2).mean()
        self.coherence_opt.zero_grad()
        loss.backward()
        self.coherence_opt.step()
        return float(loss.item())

    def predict_coherence_score(self, mean_dr, vigor_ratio, ep_len_norm):
        if not ENABLE_COHERENCE_CRITIC:
            return 0.0
        with th.no_grad():
            x = th.tensor([[mean_dr, vigor_ratio, ep_len_norm]], dtype=th.float32, device=device)
            pred = self.coherence_head(x)
            return float(pred.item())

# ---------------------------------------------------------------------
# training loop
# ---------------------------------------------------------------------
def main():
    base_env = gym.make("CartPole-v1")
    env = DiscreteToBoxActionWrapper(base_env)

    agent = WendigoAgent(env)
    gold = GoldWindow(max_size=48)

    num_episodes = 300
    top_eps = []

    for ep in range(1, num_episodes + 1):
        obs, _ = env.reset()
        done, truncated = False, False
        score, vigor_ct, rigor_ct, ep_dark = 0, 0, 0, 0.0
        ep_transitions = []

        while not done and not truncated:
            action, mode = agent.predict_action(obs)
            if mode == "Vigor": vigor_ct += 1
            else: rigor_ct += 1

            next_obs, env_reward, done, truncated, info = env.step(action)
            dark = calculate_dark_residue(next_obs)
            agent.register_dark(dark)

            # --- ABLATION: REWARD SHAPING ---
            if ENABLE_REWARD_SHAPING:
                dark_med = agent.current_dark_median()
                cleanliness = max(0.0, dark_med - dark)
                shaped_reward = -dark
            else:
                shaped_reward = env_reward

            agent.step_learn(obs, action, next_obs, shaped_reward, done or truncated)
            ep_transitions.append((obs, action, next_obs, shaped_reward, dark, done or truncated))

            obs = next_obs
            score += 1
            ep_dark += dark

        mean_dr = ep_dark / max(score, 1)
        vigor_ratio = vigor_ct / max((vigor_ct + rigor_ct), 1)
        ep_len_norm = min(1.0, score / 500.0)

        # --- ABLATION: COHERENCE CRITIC ---
        coh_loss = agent.train_coherence_head(mean_dr, vigor_ratio, ep_len_norm, score)
        coh_pred = agent.predict_coherence_score(mean_dr, vigor_ratio, ep_len_norm)

        # --- Leaderboard logic ---
        top_eps.append({"score": score, "dark": mean_dr})
        top_eps.sort(key=lambda e: (-e["score"], e["dark"]))
        top_eps = top_eps[:15]
        avg_top = sum(e["score"] for e in top_eps) / len(top_eps)
        dyn_threshold = int(avg_top * 0.75)

        # --- ABLATION: GOLD WINDOW & WHETSTONES ---
        # Decide if this episode is "gold" based on enabled components
        is_gold_by_dr = (mean_dr <= 0.20 and score >= (dyn_threshold - 20))
        is_gold_by_coh = ENABLE_COHERENCE_CRITIC and (coh_pred >= (dyn_threshold - 10))
        is_gold = is_gold_by_dr or is_gold_by_coh

        if is_gold:
            if ENABLE_GOLD_WINDOW:
                ge = GoldEpisode(score, mean_dr, ep_transitions, vigor_ct, rigor_ct)
                gold.maybe_add(ge)

            if ENABLE_WHETSTONE_REPLAYS:
                # Whetstones from this episode's best moments
                this_low = sorted(ep_transitions, key=lambda t: t[4])[: max(5, len(ep_transitions) // 6)]
                agent.sharpen_with_whetstones(this_low)
                
                # Periodic global whetstone from the best gold episode
                if ep % 5 == 0 and ENABLE_GOLD_WINDOW:
                    gw_tr = gold.sample_transitions(k=18)
                    agent.sharpen_with_whetstones(gw_tr)
        
        # --- Periodic Housekeeping ---
        if ep % 10 == 0:
            agent.sac.save(f"wendigo_sac_ep{ep}")
            if ENABLE_GOLD_WINDOW:
                 with open(f"{agent.gold_dir}/wendigo_gold_window.json", "w") as f:
                    json.dump([{"score": g.score, "mean_dr": g.mean_dr, "vigor": g.vigor, "rigor": g.rigor, "len_transitions": len(g.transitions)} for g in gold.buffer], f, indent=2)

        # --- Logging ---
        run_type = "Coherent run." if mean_dr <= 0.22 else "Dissonant run."
        coh_str = f"| CohHead: pred={coh_pred:.1f} loss={coh_loss:.3f}" if ENABLE_COHERENCE_CRITIC else ""
        print(f"Episode {ep}: {run_type} Score: {score}. (Gold: {is_gold})")
        print(f"    Avg Dark Residue: {mean_dr:.2f} | Vigor/Rigor: {vigor_ct}/{rigor_ct} {coh_str}")

        if ENABLE_GOLD_WINDOW and gold.buffer:
            best_g = gold.buffer[0]
            print(f"    [GW] best={best_g.score} (DR={best_g.mean_dr:.2f}) | window={len(gold.buffer)}")
        
        print(f"    Top-15 scores: {[e['score'] for e in top_eps]} | avg={avg_top:.2f} | dyn_threshold={dyn_threshold}")

    print("Training complete.")
    agent.sac.save("wendigo_sac_model")
    env.close()


if __name__ == "__main__":
    main()