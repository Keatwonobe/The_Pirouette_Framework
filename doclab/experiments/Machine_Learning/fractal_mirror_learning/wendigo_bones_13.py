#!/usr/bin/env python3
"""
wendigo_bones_ratchet_mastery.py

Integrates the RatchetPolicyArchive for an ever-increasing performance standard
and implements a stricter mastery condition based on minimum performance over a
window, not just the average.
"""

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque, namedtuple
import random
import math

Transition = namedtuple("Transition", "obs act rew next_obs done mode")

# ---------------------------------------------------------
# dark residue + classifier
# ---------------------------------------------------------
def dark_residue(obs: np.ndarray) -> float:
    x, xdot, theta, thetadot = obs
    return (
        0.4 * abs(x)
        + 0.2 * abs(xdot)
        + 1.5 * abs(theta)
        + 0.3 * abs(thetadot)
    )

def classify_mode(dr: float, ddr: float) -> str:
    DR_SMALL = 0.15
    DR_LARGE = 0.35
    if ddr < 0.0:
        return "Weaver" if dr <= DR_SMALL else "Gladiator"
    else:
        return "Vortex" if dr >= DR_LARGE else "Drifter"

# ---------------------------------------------------------
# MLP
# ---------------------------------------------------------
class MLP(nn.Module):
    def __init__(self, inp, out, act=nn.ReLU):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(inp, 128), act(),
            nn.Linear(128, 128), act(),
            nn.Linear(128, out),
        )
    def forward(self, x):
        return self.net(x)

# ---------------------------------------------------------
# RatchetPolicyArchive (New Logic)
# ---------------------------------------------------------
class RatchetPolicyArchive:
    def __init__(self, capacity=5, patience=6):
        self.capacity = capacity
        self.patience = patience
        self.snapshots = []
        self.bad_streak = 0
        self.best_ever = 0
        # This threshold can ONLY ever increase.
        self.ratchet_threshold = 0

    def maybe_store(self, steps, actor, critic, target_critic):
        # A policy is only a candidate for storage if it beats the last-stored score.
        if steps > self.ratchet_threshold:
            self._store_policy(steps, actor, critic, target_critic)
            print(f"[ARCHIVE] Stored policy at {steps} steps. Next threshold is > {self.ratchet_threshold}.")

    def _store_policy(self, steps, actor, critic, target_critic):
        self.best_ever = max(self.best_ever, steps)
        snapshot = {
            "steps": steps,
            "actor": {k: v.cpu().clone() for k, v in actor.state_dict().items()},
            "critic": {k: v.cpu().clone() for k, v in critic.state_dict().items()},
            "target": {k: v.cpu().clone() for k, v in target_critic.state_dict().items()},
        }
        self.snapshots.append(snapshot)
        self.snapshots.sort(key=lambda x: x["steps"], reverse=True)
        if len(self.snapshots) > self.capacity:
            self.snapshots.pop()
        
        # === THE RATCHET MECHANISM ===
        # The new threshold is now the score of the policy we just stored.
        self.ratchet_threshold = steps

    def get_teacher_state_dict(self):
        if not self.snapshots:
            return None
        return random.choice(self.snapshots)["actor"]

    def report_and_should_restore(self, steps):
        if not self.snapshots or self.best_ever == 0:
            return False
        
        # Restore if performance is consistently poor relative to our best ever
        if steps < self.best_ever * 0.6: # Stricter restore condition
            self.bad_streak += 1
        else:
            self.bad_streak = 0
            
        return self.bad_streak >= self.patience

    def restore_best(self, actor, critic, target_critic):
        if not self.snapshots:
            return
        
        best_snapshot = self.snapshots[0]
        actor.load_state_dict(best_snapshot["actor"])
        critic.load_state_dict(best_snapshot["critic"])
        target_critic.load_state_dict(best_snapshot["target"])
        self.bad_streak = 0
        print(f"[ARCHIVE] Restored best policy ({best_snapshot['steps']} steps)")


# ---------------------------------------------------------
# AC
# ---------------------------------------------------------
class PirouetteAC:
    def __init__(self, obs_dim, act_dim, lr=3e-4, gamma=0.99, tau=0.01):
        self.actor = MLP(obs_dim, act_dim)
        self.critic = MLP(obs_dim + act_dim, 1)
        self.target_critic = MLP(obs_dim + act_dim, 1)
        self.target_critic.load_state_dict(self.critic.state_dict())

        self.opt_actor = optim.Adam(self.actor.parameters(), lr=lr)
        self.opt_critic = optim.Adam(self.critic.parameters(), lr=lr)
        self.gamma = gamma
        self.tau = tau
        self.critic_loss_ema = None

    @torch.no_grad()
    def act(self, obs, noise_std=0.1):
        obs_t = torch.as_tensor(obs, dtype=torch.float32).unsqueeze(0)
        a = self.actor(obs_t)
        a = a + noise_std * torch.randn_like(a)
        return a.squeeze(0).clamp(-1.0, 1.0).numpy()

    def update(self, batch, batch_weaver=None, batch_anchor=None, shock_factor=4.0):
        obs = torch.as_tensor(np.stack([b.obs for b in batch]), dtype=torch.float32)
        act = torch.as_tensor(np.stack([b.act for b in batch]), dtype=torch.float32)
        rew = torch.as_tensor(np.stack([b.rew for b in batch]), dtype=torch.float32).unsqueeze(-1)
        nxt = torch.as_tensor(np.stack([b.next_obs for b in batch]), dtype=torch.float32)
        done = torch.as_tensor(np.stack([b.done for b in batch]), dtype=torch.float32).unsqueeze(-1)

        with torch.no_grad():
            nxt_act = self.actor(nxt)
            tgt_q = self.target_critic(torch.cat([nxt, nxt_act], dim=-1))
            y = rew + self.gamma * (1.0 - done) * tgt_q

        q = self.critic(torch.cat([obs, act], dim=-1))
        critic_loss = nn.functional.mse_loss(q, y)

        do_critic = True
        if self.critic_loss_ema is None:
            self.critic_loss_ema = critic_loss.item()
        else:
            if critic_loss.item() > shock_factor * self.critic_loss_ema:
                do_critic = False
            self.critic_loss_ema = 0.9 * self.critic_loss_ema + 0.1 * critic_loss.item()

        if do_critic:
            self.opt_critic.zero_grad()
            critic_loss.backward()
            self.opt_critic.step()

        batch_combined = batch_weaver if batch_weaver is not None else batch
        if batch_anchor is not None and len(batch_anchor) > 0:
            obs_w = np.stack([b.obs for b in batch_combined] + [b.obs for b in batch_anchor])
        else:
            obs_w = np.stack([b.obs for b in batch_combined])

        obs_w = torch.as_tensor(obs_w, dtype=torch.float32)
        act_pred = self.actor(obs_w)
        q_for_act = self.critic(torch.cat([obs_w, act_pred], dim=-1))
        actor_loss = -q_for_act.mean()

        self.opt_actor.zero_grad()
        actor_loss.backward()
        self.opt_actor.step()

        with torch.no_grad():
            for p, tp in zip(self.critic.parameters(), self.target_critic.parameters()):
                tp.data.mul_(1 - self.tau).add_(self.tau * p.data)

# ---------------------------------------------------------
# discrete wrapper & reward
# ---------------------------------------------------------
class DiscreteToBox(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
    def action(self, act):
        return 0 if act[0] < 0 else 1

PRIME_W_SPAN, PRIME_W_COH, PRIME_W_DR, MAX_STEPS = 1.0, 1.5, 1.0, 500

def prime_directive_reward(cur_dr, ddr, step_idx, max_steps=MAX_STEPS):
    span = step_idx / max_steps
    closure = max(0.0, -ddr)
    return (PRIME_W_SPAN * span + PRIME_W_COH * closure - PRIME_W_DR * cur_dr), span, closure

# ---------------------------------------------------------
# training
# ---------------------------------------------------------
def train():
    env = DiscreteToBox(gym.make("CartPole-v1"))
    obs_dim, act_dim = env.observation_space.shape[0], env.action_space.shape[0]

    agent = PirouetteAC(obs_dim, act_dim)
    teacher_actor = MLP(obs_dim, act_dim)

    general_buf, weaver_buf, anchor_buf = deque(maxlen=50_000), deque(maxlen=10_000), deque(maxlen=5_000)
    
    BATCH_GEN, BATCH_W, BATCH_A = 96, 32, 32

    archive = RatchetPolicyArchive(capacity=5, patience=6)

    obs, _ = env.reset()
    for _ in range(3_000):
        a = env.action_space.sample()
        nxt, _, done, trunc, _ = env.step(a)
        obs = nxt if not (done or trunc) else env.reset()[0]

    top15 = deque(maxlen=15) # Use a deque for efficient rolling window
    total_eps = 600

    for ep in range(1, total_eps + 1):
        obs, _ = env.reset()
        prev_dr = dark_residue(obs)
        done, trunc, steps, last_span = False, False, 0, 0.0
        teacher_prob = 0.5 * (1 - ep / total_eps)

        while not (done or trunc):
            steps += 1
            a = agent.act(obs) # Default
            
            if len(archive.snapshots) > 0 and random.random() < teacher_prob:
                with torch.no_grad():
                    teacher_actor.load_state_dict(archive.get_teacher_state_dict())
                    a_t = teacher_actor(torch.as_tensor(obs, dtype=torch.float32).unsqueeze(0))
                    a = a_t.squeeze(0).clamp(-1.0, 1.0).numpy()

            nxt, _, done, trunc, _ = env.step(a)

            cur_dr = dark_residue(nxt)
            rew, span, coh = prime_directive_reward(cur_dr, cur_dr - prev_dr, steps, MAX_STEPS)
            
            tr = Transition(obs, a, rew, nxt, float(done), "N/A")
            general_buf.append(tr)
            if classify_mode(cur_dr, cur_dr-prev_dr) in ("Weaver", "Gladiator"):
                weaver_buf.append(tr)

            if len(general_buf) > BATCH_GEN:
                batch_gen = random.sample(general_buf, BATCH_GEN)
                batch_w = random.sample(weaver_buf, BATCH_W) if len(weaver_buf) > BATCH_W else None
                batch_a = random.sample(anchor_buf, BATCH_A) if len(anchor_buf) > BATCH_A else None
                agent.update(batch_gen, batch_weaver=batch_w, batch_anchor=batch_a)

            obs, prev_dr = nxt, cur_dr

        # --- Episode End ---
        if steps >= 450:
            for i in range(1, min(steps, 450) + 1):
                anchor_buf.append(general_buf[-i])
        
        archive.maybe_store(steps, agent.actor, agent.critic, agent.target_critic)
        
        top15.append(steps)
        avg_top = sum(top15) / len(top15)

        print(
            f"Ep {ep:03d} | steps={steps:4d} | top15_avg={avg_top:6.2f} | "
            f"threshold={archive.ratchet_threshold:4d} | archive={len(archive.snapshots)} | "
            f"anchor={len(anchor_buf):4d}"
        )

        if archive.report_and_should_restore(steps):
            archive.restore_best(agent.actor, agent.critic, agent.target_critic)
            
        # --- NEW MASTERY CONDITION ---
        # Exit only if the WORST of the last 15 runs is near-perfect.
        if len(top15) == 15 and min(top15) >= 490:
             print("\n*** Stable Mastery Achieved (min of last 15 runs >= 490) ***")
             break

    env.close()

if __name__ == "__main__":
    train()