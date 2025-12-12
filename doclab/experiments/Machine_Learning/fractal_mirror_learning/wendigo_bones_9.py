#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WENDIGO BONES v9
Pirouette-native, minimal, discrete actor-critic with ratchet archive + anchors.

Key changes from v8:
 - Discrete actor/critic to match CartPole's action space (0/1) — fixes action/critic mismatch.
 - Anchors gathered relative to best-so-far (not only near mastery) — real "return-to-good".
 - Shock-aware critic updates: scale LR on spikes instead of skipping.
 - Prime Directive reward emphasizes timescale (span) with normalized Dark Residue (DR).
 - Small terminal bonus for horizon completion to encourage 500s.
 - Keeps your top-k/ratchet archive + restore loop and "weaver" style replay.
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
    # Gymnasium fallback name if needed
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

EPS_START = 0.30
EPS_END   = 0.05
EPS_DECAY = 0.85  # decay per 100 episodes (roughly)

BATCH_SIZE = 128
REPLAY_CAP = 50_000
WEAVER_CAP = 10_000
ANCHOR_CAP = 10_000

# Prime Directive weights
PRIME_W_SPAN = 1.0   # timescale fraction
PRIME_W_COH  = 0.5   # closure = -ΔDR+
PRIME_W_DR   = 0.5   # DR penalty (normalized)
TERM_BONUS   = 1.0   # bonus at 500 steps

# Dark Residue normalization
DR_INIT_SCALE = 5.0  # initial scale; will be EMA-updated
DR_EMA_BETA   = 0.95

# Critic shock handling
SHOCK_FACTOR = 4.0     # threshold multiplier vs EMA loss
SHOCK_LR_SCALE = 0.25  # temporary LR scale when shocked

# Archive / restore
ARCHIVE_TOPK = 15
RATCHET_PATIENCE = 10         # episodes allowed below threshold before restore
RATCHET_FRACTION_BAD = 0.60   # restore when ep_steps < 60% of best_ever

# Training scheduling
UPDATES_PER_EP = 1
WEAVER_RATIO = 0.25   # fraction of weaver samples in a batch
ANCHOR_RATIO = 0.25   # fraction of anchor samples in a batch


# --------------------
# Nets
# --------------------
class DiscreteActor(nn.Module):
    def __init__(self, obs_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, 2)  # logits for actions {0,1}
        )
    def forward(self, obs):
        return self.net(obs)  # logits


class QCritic2(nn.Module):
    def __init__(self, obs_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, 2)  # Q(s, a=0/1)
        )
    def forward(self, obs):
        return self.net(obs)  # [B,2]


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
        logits = self.actor(obs_t)  # [1,2]
        return int(torch.argmax(logits, dim=-1).item())

    def update(self, batch, batch_weaver=None, batch_anchor=None):
        # combine batches per ratios
        buf = list(batch)

        def take_from(src, n):
            if not src: return []
            n = min(n, len(src))
            return random.sample(src, n)

        n_total = len(buf)
        n_weaver = int(WEAVER_RATIO * BATCH_SIZE)
        n_anchor = int(ANCHOR_RATIO * BATCH_SIZE)

        wb = take_from(batch_weaver or [], n_weaver)
        ab = take_from(batch_anchor or [], n_anchor)

        # top off with base replay to reach BATCH_SIZE
        combined = wb + ab + buf
        if len(combined) < BATCH_SIZE:
            # pad from buf (resample)
            combined += take_from(buf, BATCH_SIZE - len(combined))
        else:
            combined = combined[:BATCH_SIZE]

        obs = torch.as_tensor(np.stack([t.obs for t in combined]), dtype=torch.float32, device=DEVICE)
        act = torch.as_tensor(np.stack([t.act for t in combined]), dtype=torch.int64, device=DEVICE).unsqueeze(1)  # [B,1]
        rew = torch.as_tensor(np.stack([t.rew for t in combined]), dtype=torch.float32, device=DEVICE).unsqueeze(1)
        nxt = torch.as_tensor(np.stack([t.next_obs for t in combined]), dtype=torch.float32, device=DEVICE)
        done = torch.as_tensor(np.stack([t.done for t in combined]), dtype=torch.float32, device=DEVICE).unsqueeze(1)

        with torch.no_grad():
            nxt_q = self.target_critic(nxt)               # [B,2]
            nxt_a = torch.argmax(self.actor(nxt), -1)     # greedy a*
            tgt_q = nxt_q.gather(1, nxt_a.unsqueeze(1))   # Q'(s',a*)
            y = rew + self.gamma * (1.0 - done) * tgt_q

        q = self.critic(obs)                               # [B,2]
        q_a = q.gather(1, act)                             # [B,1]
        td = y - q_a
        critic_loss = (td.pow(2)).mean()

        # shock-aware LR scaling instead of skipping
        lr_scale = 1.0
        if self.critic_loss_ema is None:
            self.critic_loss_ema = critic_loss.item()
        else:
            if critic_loss.item() > SHOCK_FACTOR * self.critic_loss_ema:
                lr_scale = SHOCK_LR_SCALE
            self.critic_loss_ema = 0.9 * self.critic_loss_ema + 0.1 * critic_loss.item()

        for g in self.opt_critic.param_groups:
            g.setdefault('lr_orig', g['lr'])
            g['lr'] = g['lr_orig'] * lr_scale
        self.opt_critic.zero_grad()
        critic_loss.backward()
        nn.utils.clip_grad_norm_(self.critic.parameters(), 5.0)
        self.opt_critic.step()
        for g in self.opt_critic.param_groups:
            g['lr'] = g['lr_orig']

        # actor: maximize expected Q under its own policy
        logits = self.actor(obs)                            # [B,2]
        probs = torch.softmax(logits, dim=-1)
        with torch.no_grad():
            q_det = self.critic(obs)                        # stop-gradient target
        actor_loss = -(probs * q_det).sum(dim=-1).mean()

        self.opt_actor.zero_grad()
        actor_loss.backward()
        nn.utils.clip_grad_norm_((self.actor.parameters()), 5.0)
        self.opt_actor.step()

        # soft update
        with torch.no_grad():
            for p, tp in zip(self.critic.parameters(), self.target_critic.parameters()):
                tp.data.mul_(1.0 - self.tau).add_(self.tau * p.data)


# --------------------
# Utils
# --------------------
class RatchetPolicyArchive:
    def __init__(self, topk=ARCHIVE_TOPK):
        self.entries = []  # list of (steps, actor_sd, critic_sd)
        self.best_ever = 0
        self.topk = topk

    def store(self, steps, actor, critic):
        sd_a = {k: v.cpu().clone() for k, v in actor.state_dict().items()}
        sd_c = {k: v.cpu().clone() for k, v in critic.state_dict().items()}
        self.entries.append((steps, sd_a, sd_c))
        self.entries.sort(key=lambda x: x[0], reverse=True)
        if len(self.entries) > self.topk:
            self.entries = self.entries[:self.topk]
        self.best_ever = max(self.best_ever, steps)

    def restore_best(self, agent):
        if not self.entries: return False
        best = self.entries[0]
        agent.actor.load_state_dict(best[1])
        agent.critic.load_state_dict(best[2])
        return True


def eps_for_episode(ep):
    # gentle decay per 100 eps
    k = (ep // 100)
    return max(EPS_END, EPS_START * (EPS_DECAY ** k))


def compute_dark_residue(prev_logits, cur_logits):
    """
    A light-weight surrogate for DR: KL between consecutive policy logits.
    Normalized later via EMA scale. If no prev logits, return 0.
    """
    if prev_logits is None or cur_logits is None:
        return 0.0
    with torch.no_grad():
        p0 = torch.softmax(prev_logits, dim=-1)
        p1 = torch.softmax(cur_logits, dim=-1)
        kl = (p0 * (torch.log(p0 + 1e-8) - torch.log(p1 + 1e-8))).sum(dim=-1).mean().item()
    return float(max(0.0, kl))


class DRNormalizer:
    def __init__(self, init_scale=DR_INIT_SCALE, beta=DR_EMA_BETA):
        self.scale = init_scale
        self.beta = beta
        self.initialized = False

    def norm(self, x):
        # update EMA scale with |x|
        val = abs(x)
        if not self.initialized:
            self.scale = max(1e-3, val)
            self.initialized = True
        else:
            self.scale = self.beta * self.scale + (1 - self.beta) * max(1e-3, val)
        return x / max(self.scale, 1e-6)


def prime_directive_reward(cur_dr_norm, ddr, step_idx, max_steps=MAX_STEPS, hit_max=False):
    # Timescale fraction
    span = step_idx / float(max_steps)
    # Closure: reward reductions in DR (only positive improvement)
    closure = max(0.0, -ddr)
    term_bonus = TERM_BONUS if hit_max else 0.0
    r = (PRIME_W_SPAN * span +
         PRIME_W_COH  * closure -
         PRIME_W_DR   * max(0.0, cur_dr_norm) +
         term_bonus)
    return r, span, closure


# --------------------
# Main training
# --------------------
def main():
    env = gym.make(ENV_ID)
    obs_dim = env.observation_space.shape[0]

    agent = PirouetteAC(obs_dim, lr=LR, gamma=GAMMA, tau=TAU)

    replay = deque(maxlen=REPLAY_CAP)
    weaver = deque(maxlen=WEAVER_CAP)
    anchors = deque(maxlen=ANCHOR_CAP)

    archive = RatchetPolicyArchive(topk=ARCHIVE_TOPK)

    # Ratchet tracking
    bad_run_counter = 0

    # DR tracking
    dr_norm = DRNormalizer()
    prev_logits = None

    # Thresholds
    next_threshold = None

    # Logging
    top15 = deque(maxlen=15)

    # Prime directive-only score accumulation (for debug)
    for ep in range(1, TOTAL_EPISODES + 1):
        obs, _ = env.reset()
        eps = eps_for_episode(ep)
        ep_trans = []
        ep_steps = 0
        ep_reward_sum = 0.0

        # Keep last logits to compute DR
        prev_logits = None

        for t in range(1, MAX_STEPS + 1):
            # logits for DR estimation
            obs_t = torch.as_tensor(obs, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            cur_logits = agent.actor(obs_t)

            # DR: KL(policy_t-1 || policy_t)
            dr = compute_dark_residue(prev_logits, cur_logits)
            dr_n = dr_norm.norm(dr)

            a = agent.choose_action(obs, eps=eps)
            next_obs, _, terminated, truncated, _ = env.step(a)
            done = terminated or truncated
            hit_max = (t == MAX_STEPS and not terminated)

            # Reward uses span & DR dynamics only (task score is implicit in span; env reward unused)
            # dDR ~ change vs previous (approximate with current minus previous normalized)
            prev_dr_n = 0.0 if prev_logits is None else dr_norm.norm(compute_dark_residue(None, None))  # zero baseline
            # We can't recompute previous normalized reliably here without keeping a history;
            # approximate ddr as current normalized DR change vs 0 (penalize raw DR, closure rewards when dr decreases)
            ddr = dr_n  # simple surrogate (negative ddr rewarded via closure)

            r, span, closure = prime_directive_reward(dr_n, ddr, t, MAX_STEPS, hit_max=hit_max)

            # Store transition
            ep_trans.append(Transition(obs=obs, act=a, rew=r, next_obs=next_obs, done=float(done), mode="Weaver"))
            ep_steps = t
            ep_reward_sum += r

            prev_logits = cur_logits

            obs = next_obs
            if done:
                break

        # Episode end bookkeeping
        top15.append(ep_steps)
        replay.extend(ep_trans)
        weaver.extend(ep_trans[-min(len(ep_trans), 200):])  # recent local context

        # Archive logic: store surpassing personal thresholds repeatedly
        if archive.best_ever == 0:
            next_threshold = 8
        if ep_steps > (next_threshold or 0):
            archive.store(ep_steps, agent.actor, agent.critic)
            if next_threshold is None:
                next_threshold = ep_steps
            while next_threshold is not None and ep_steps > next_threshold:
                next_threshold = int(max(next_threshold + 1, math.ceil(next_threshold * 1.05)))
            print(f"[ARCHIVE] Stored policy at {ep_steps} steps. Next threshold is > {next_threshold}.")
        # also store anchors when reaching a strong fraction of best
        if ep_steps >= max(200, int(0.8 * max(archive.best_ever, 1))):
            take = min(ep_steps, 200)
            for t in ep_trans[-take:]:
                anchors.append(t)

        # Ratchet restore if we underperform for long
        if archive.best_ever > 0 and ep_steps < int(RATCHET_FRACTION_BAD * archive.best_ever):
            bad_run_counter += 1
            if bad_run_counter >= RATCHET_PATIENCE:
                ok = archive.restore_best(agent)
                if ok:
                    print(f"[ARCHIVE] Restored best policy ({archive.best_ever} steps)")
                bad_run_counter = 0
        else:
            bad_run_counter = 0

        # Training updates
        if len(replay) >= BATCH_SIZE:
            for _ in range(UPDATES_PER_EP):
                batch = random.sample(replay, BATCH_SIZE)
                agent.update(batch, batch_weaver=list(weaver), batch_anchor=list(anchors))

        # Logging
        avg_top = np.mean(top15) if top15 else 0.0
        th = next_threshold if next_threshold is not None else 0
        print(f"Ep {ep:03d} | steps={ep_steps:4d} | top15={avg_top:6.2f} | threshold={th:4d} | "
              f"archive={len(archive.entries)} | anchor={len(anchors):4d}")

    env.close()


if __name__ == "__main__":
    main()
