#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WENDIGO BONES v9.1 (Corrected)
This version fixes the reward signal and learning frequency to enable effective training.
"""

import os
import math
import random
from collections import deque, namedtuple
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

try:
    import gym
except Exception:
    import gymnasium as gym

Transition = namedtuple("Transition", "obs act rew next_obs done mode")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --------------------
# Config (tweakables)
# --------------------
ENV_ID = "CartPole-v1"
TOTAL_EPISODES = 800
MAX_STEPS = 500
GAMMA = 0.99
TAU = 0.01
LR = 3e-4

EPS_START = 0.50  # <<< FIX: Increased initial exploration
EPS_END   = 0.05
EPS_DECAY = 0.90  # <<< FIX: Slightly faster decay to balance wider exploration

BATCH_SIZE = 128
REPLAY_CAP = 50_000
WEAVER_CAP = 10_000
ANCHOR_CAP = 10_000

# Prime Directive weights
PRIME_W_SPAN = 1.0
PRIME_W_COH  = 1.0   # <<< FIX: Increased weight for the now-functional closure term
PRIME_W_DR   = 0.5
TERM_BONUS   = 1.0

# Dark Residue normalization
DR_INIT_SCALE = 5.0
DR_EMA_BETA   = 0.95

# Critic shock handling
SHOCK_FACTOR = 4.0
SHOCK_LR_SCALE = 0.25

# Archive / restore
ARCHIVE_TOPK = 15
RATCHET_PATIENCE = 10
RATCHET_FRACTION_BAD = 0.60

# Training scheduling
# UPDATES_PER_EP is now dynamic, see main loop
WEAVER_RATIO = 0.25
ANCHOR_RATIO = 0.25


# --------------------
# Nets
# --------------------
class DiscreteActor(nn.Module):
    def __init__(self, obs_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, 2)
        )
    def forward(self, obs):
        return self.net(obs)

class QCritic2(nn.Module):
    def __init__(self, obs_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, 2)
        )
    def forward(self, obs):
        return self.net(obs)

class PirouetteAC:
    def __init__(self, obs_dim, lr=LR, gamma=GAMMA, tau=TAU):
        self.actor = DiscreteActor(obs_dim).to(DEVICE)
        self.critic = QCritic2(obs_dim).to(DEVICE)
        self.target_critic = QCritic2(obs_dim).to(DEVICE)
        self.target_critic.load_state_dict(self.critic.state_dict())

        self.opt_actor = optim.Adam(self.actor.parameters(), lr=lr)
        self.opt_critic = optim.Adam(self.critic.parameters(), lr=lr)
        self.gamma = gamma
        self.tau = tau
        self.critic_loss_ema = None

    @torch.no_grad()
    def choose_action(self, obs, eps=0.1):
        obs_t = torch.as_tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        if np.random.rand() < eps:
            return np.random.randint(0, 2)
        logits = self.actor(obs_t)
        return int(torch.argmax(logits, dim=-1).item())

    def update(self, batch, batch_weaver=None, batch_anchor=None):
        buf = list(batch)
        def take_from(src, n):
            if not src: return []
            return random.sample(src, min(n, len(src)))

        n_weaver = int(WEAVER_RATIO * BATCH_SIZE)
        n_anchor = int(ANCHOR_RATIO * BATCH_SIZE)
        wb = take_from(batch_weaver or [], n_weaver)
        ab = take_from(batch_anchor or [], n_anchor)
        
        combined = wb + ab
        remaining_size = BATCH_SIZE - len(combined)
        if remaining_size > 0:
            combined += take_from(buf, remaining_size)
        combined = combined[:BATCH_SIZE]

        obs = torch.as_tensor(np.stack([t.obs for t in combined]), dtype=torch.float32, device=DEVICE)
        act = torch.as_tensor(np.stack([t.act for t in combined]), dtype=torch.int64, device=DEVICE).unsqueeze(1)
        rew = torch.as_tensor(np.stack([t.rew for t in combined]), dtype=torch.float32, device=DEVICE).unsqueeze(1)
        nxt = torch.as_tensor(np.stack([t.next_obs for t in combined]), dtype=torch.float32, device=DEVICE)
        done = torch.as_tensor(np.stack([t.done for t in combined]), dtype=torch.float32, device=DEVICE).unsqueeze(1)

        with torch.no_grad():
            nxt_q = self.target_critic(nxt)
            nxt_a = torch.argmax(self.actor(nxt), -1)
            tgt_q = nxt_q.gather(1, nxt_a.unsqueeze(1))
            y = rew + self.gamma * (1.0 - done) * tgt_q

        q = self.critic(obs)
        q_a = q.gather(1, act)
        critic_loss = (y - q_a).pow(2).mean()

        lr_scale = 1.0
        if self.critic_loss_ema is None: self.critic_loss_ema = critic_loss.item()
        else:
            if critic_loss.item() > SHOCK_FACTOR * self.critic_loss_ema: lr_scale = SHOCK_LR_SCALE
            self.critic_loss_ema = 0.9 * self.critic_loss_ema + 0.1 * critic_loss.item()

        for g in self.opt_critic.param_groups:
            g.setdefault('lr_orig', g['lr']); g['lr'] = g['lr_orig'] * lr_scale
        self.opt_critic.zero_grad(); critic_loss.backward(); nn.utils.clip_grad_norm_(self.critic.parameters(), 5.0); self.opt_critic.step()
        for g in self.opt_critic.param_groups: g['lr'] = g['lr_orig']

        logits = self.actor(obs)
        probs = torch.softmax(logits, dim=-1)
        with torch.no_grad(): q_det = self.critic(obs)
        actor_loss = -(probs * q_det).sum(dim=-1).mean()

        self.opt_actor.zero_grad(); actor_loss.backward(); nn.utils.clip_grad_norm_((self.actor.parameters()), 5.0); self.opt_actor.step()

        with torch.no_grad():
            for p, tp in zip(self.critic.parameters(), self.target_critic.parameters()):
                tp.data.mul_(1.0 - self.tau).add_(self.tau * p.data)


# --------------------
# Utils
# --------------------
class RatchetPolicyArchive:
    def __init__(self, topk=ARCHIVE_TOPK):
        self.entries = []
        self.best_ever = 0
        self.topk = topk

    def store(self, steps, actor, critic):
        sd_a = {k: v.cpu().clone() for k, v in actor.state_dict().items()}
        sd_c = {k: v.cpu().clone() for k, v in critic.state_dict().items()}
        self.entries.append((steps, sd_a, sd_c))
        self.entries.sort(key=lambda x: x[0], reverse=True)
        self.entries = self.entries[:self.topk]
        self.best_ever = max(self.best_ever, steps)

    def restore_best(self, agent):
        if not self.entries: return False
        best = self.entries[0]
        agent.actor.load_state_dict(best[1]); agent.critic.load_state_dict(best[2])
        return True

def eps_for_episode(ep):
    k = (ep // 100); return max(EPS_END, EPS_START * (EPS_DECAY ** k))

def compute_dark_residue(prev_logits, cur_logits):
    if prev_logits is None or cur_logits is None: return 0.0
    with torch.no_grad():
        p0 = torch.softmax(prev_logits, dim=-1); p1 = torch.softmax(cur_logits, dim=-1)
        kl = (p0 * (torch.log(p0 + 1e-8) - torch.log(p1 + 1e-8))).sum(dim=-1).mean().item()
    return float(max(0.0, kl))

class DRNormalizer:
    def __init__(self, init_scale=DR_INIT_SCALE, beta=DR_EMA_BETA):
        self.scale = init_scale; self.beta = beta; self.initialized = False
    def norm(self, x):
        val = abs(x)
        if not self.initialized: self.scale = max(1e-3, val); self.initialized = True
        else: self.scale = self.beta * self.scale + (1 - self.beta) * max(1e-3, val)
        return x / max(self.scale, 1e-6)

def prime_directive_reward(cur_dr_norm, ddr_norm, step_idx, max_steps=MAX_STEPS, hit_max=False):
    span = step_idx / float(max_steps)
    closure = max(0.0, -ddr_norm)
    term_bonus = TERM_BONUS if hit_max else 0.0
    r = (PRIME_W_SPAN * span + PRIME_W_COH * closure - PRIME_W_DR * max(0.0, cur_dr_norm) + term_bonus)
    return r, span, closure


# --------------------
# Main training
# --------------------
def main():
    env = gym.make(ENV_ID)
    obs_dim = env.observation_space.shape[0]
    agent = PirouetteAC(obs_dim)
    replay, weaver, anchors = deque(maxlen=REPLAY_CAP), deque(maxlen=WEAVER_CAP), deque(maxlen=ANCHOR_CAP)
    archive = RatchetPolicyArchive(topk=ARCHIVE_TOPK)

    bad_run_counter = 0
    dr_norm = DRNormalizer()
    next_threshold = 8 # Start with a low bar
    top15 = deque(maxlen=15)

    for ep in range(1, TOTAL_EPISODES + 1):
        obs, _ = env.reset()
        eps = eps_for_episode(ep)
        ep_trans, ep_steps, ep_reward_sum = [], 0, 0.0
        prev_logits, prev_dr_n = None, 0.0

        for t in range(1, MAX_STEPS + 1):
            obs_t = torch.as_tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            cur_logits = agent.actor(obs_t)
            
            dr = compute_dark_residue(prev_logits, cur_logits)
            dr_n = dr_norm.norm(dr)
            ddr_n = dr_n - prev_dr_n  # <<< FIX: Correct ddr calculation

            a = agent.choose_action(obs, eps=eps)
            next_obs, _, terminated, truncated, _ = env.step(a)
            done = terminated or truncated
            hit_max = (t == MAX_STEPS and not terminated)

            r, span, closure = prime_directive_reward(dr_n, ddr_n, t, MAX_STEPS, hit_max=hit_max)
            ep_trans.append(Transition(obs, a, r, next_obs, float(done), "Weaver"))
            ep_steps = t

            prev_logits, prev_dr_n = cur_logits, dr_n # <<< FIX: Track previous normalized DR
            obs = next_obs
            if done: break

        top15.append(ep_steps)
        replay.extend(ep_trans)
        weaver.extend(ep_trans)

        if ep_steps > next_threshold:
            archive.store(ep_steps, agent.actor, agent.critic)
            # <<< FIX: More responsive threshold update
            next_threshold = int(max(ep_steps + 1, math.ceil(ep_steps * 1.10)))
            print(f"[ARCHIVE] Stored policy at {ep_steps} steps. Next threshold is > {next_threshold}.")
        
        if ep_steps >= max(200, int(0.8 * archive.best_ever)):
            anchors.extend(ep_trans[-min(ep_steps, 200):])

        if archive.best_ever > 0 and ep_steps < int(RATCHET_FRACTION_BAD * archive.best_ever):
            bad_run_counter += 1
            if bad_run_counter >= RATCHET_PATIENCE and archive.restore_best(agent):
                print(f"[ARCHIVE] Restored best policy ({archive.best_ever} steps)")
                bad_run_counter = 0
        else:
            bad_run_counter = 0

        if len(replay) >= BATCH_SIZE:
            # <<< FIX: More updates for longer episodes
            updates_per_ep = max(1, ep_steps // 4)
            for _ in range(updates_per_ep):
                batch = random.sample(replay, BATCH_SIZE)
                agent.update(batch, list(weaver), list(anchors))

        avg_top = np.mean(top15) if top15 else 0.0
        print(f"Ep {ep:03d} | steps={ep_steps:4d} | top15={avg_top:6.2f} | threshold={next_threshold:4d} | "
              f"archive={len(archive.entries)} | anchor={len(anchors):4d}")

    env.close()

if __name__ == "__main__":
    main()