"""
wendigo_feather_hybrid.py
- Witness-first (like feather)
- Reverse Pareto + galleries (like feather)
- BUT: reward shaping + gold-window replay (like wendigo_2)
- single-task by default (cartpole) so we can see the curve
"""

import os, json, time, random
from collections import deque, defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

import numpy as np
import gymnasium as gym

import torch as th
import torch.nn as nn
import torch.optim as optim

# -----------------------------------------------------------
# 1. tiny value net (parametric learner = the PUSH)
# -----------------------------------------------------------
class ValueNet(nn.Module):
    def __init__(self, obs_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def forward(self, x):
        return self.net(x)

# -----------------------------------------------------------
# 2. transition + episode (Feather-style)
# -----------------------------------------------------------
@dataclass
class Transition:
    state: np.ndarray
    action: int
    reward: float
    next_state: np.ndarray
    done: bool
    action_jank: float = 0.0
    reward_var: float = 0.0

@dataclass
class Episode:
    task: str
    transitions: List[Transition]
    total_reward: float = 0.0
    dark_residue: float = 0.0
    span: float = 0.0
    fit: float = 0.0

    def finalize(self, max_steps: int):
        self.total_reward = sum(t.reward for t in self.transitions)
        n = max(1, len(self.transitions))
        dr_sum = sum(t.action_jank + t.reward_var for t in self.transitions)
        self.dark_residue = dr_sum / n
        self.span = len(self.transitions) / max_steps
        self.fit = self.span / (1.0 + self.dark_residue)

# -----------------------------------------------------------
# 3. witness with galleries + gold replay
# -----------------------------------------------------------
class Witness:
    def __init__(self, max_top=24):
        self.top: List[Episode] = []
        self.worst: List[Episode] = []
        self.max_top = max_top

    def observe(self, ep: Episode):
        # top = high reward, low DR
        self.top.append(ep)
        self.top.sort(key=lambda e: (e.total_reward, -e.dark_residue), reverse=True)
        self.top = self.top[: self.max_top]

        # worst = low reward, high DR
        self.worst.append(ep)
        self.worst.sort(key=lambda e: (e.total_reward, -e.dark_residue))
        self.worst = self.worst[: 6]

    def sample_whetstones(self, k=32):
        if not self.top:
            return []
        best = self.top[0]
        # low-DR steps only
        trs = sorted(best.transitions, key=lambda t: (t.action_jank + t.reward_var))
        return trs[: min(k, len(trs))]

# -----------------------------------------------------------
# 4. main loop
# -----------------------------------------------------------
def main():
    env = gym.make("CartPole-v1")
    obs_dim = env.observation_space.shape[0]
    valnet = ValueNet(obs_dim)
    optim_v = optim.Adam(valnet.parameters(), lr=1e-3)

    replay = deque(maxlen=100_000)
    witness = Witness()

    max_episodes = 3000
    max_steps = 500
    epsilon = 0.2  # will anneal by witness later
    prev_action = 0

    for ep in range(1, max_episodes+1):
        obs, info = env.reset()
        episode_trs: List[Transition] = []
        reward_hist = deque(maxlen=10)
        prev_action = 0
        total_r = 0.0

        for step in range(max_steps):
            # geodesic-ish epsilon-greedy
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                with th.no_grad():
                    o = th.tensor(obs, dtype=th.float32).unsqueeze(0)
                    v = valnet(o).item()
                # cartpole 2 actions, pick best by probing
                # (cheapo since we don't have a policy net)
                vals = []
                for a in [0,1]:
                    vals.append((a, v))  # could be made action-aware
                action = max(vals, key=lambda x: x[1])[0]

            next_obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            # DR components
            action_jank = float(action != prev_action)
            reward_hist.append(reward)
            reward_var = float(np.std(reward_hist)) if len(reward_hist) > 1 else 0.0

            # SHAPED reward (this is the wendigo_2 move)
            cleanliness = max(0.0, 0.3 - (action_jank + reward_var))
            shaped_reward = reward + 0.25 * cleanliness - 0.05 * (action_jank + reward_var)

            # store
            tr = Transition(
                state=obs,
                action=action,
                reward=shaped_reward,
                next_state=next_obs,
                done=done,
                action_jank=action_jank,
                reward_var=reward_var,
            )
            episode_trs.append(tr)
            replay.append(tr)

            obs = next_obs
            prev_action = action
            total_r += reward

            # learn a bit
            if len(replay) > 1024:
                batch = random.sample(replay, 64)
                states = th.tensor(np.stack([b.state for b in batch]), dtype=th.float32)
                targets = th.tensor(np.array([b.reward for b in batch], dtype=np.float32)).unsqueeze(1)
                preds = valnet(states)
                loss = ((preds - targets)**2).mean()
                optim_v.zero_grad()
                loss.backward()
                optim_v.step()

            if done:
                break

        # finalize + witness
        ep_obj = Episode(task="cartpole", transitions=episode_trs)
        ep_obj.finalize(max_steps)
        witness.observe(ep_obj)

        # rehearse: add gold steps back in (whetstones)
        if ep % 5 == 0:
            ws = witness.sample_whetstones(k=32)
            for w in ws:
                replay.append(w)

        # adapt epsilon from witness (if we’re getting better, explore less)
        if len(witness.top) > 5:
            avg_top = sum(e.total_reward for e in witness.top[:5]) / 5
            if avg_top > 100:
                epsilon = max(0.05, epsilon * 0.98)

        print(f"Ep {ep:04d} | R={ep_obj.total_reward:5.1f} | DR={ep_obj.dark_residue:.3f} | FIT={ep_obj.fit:.3f} | eps={epsilon:.3f}")

    env.close()

if __name__ == "__main__":
    main()
