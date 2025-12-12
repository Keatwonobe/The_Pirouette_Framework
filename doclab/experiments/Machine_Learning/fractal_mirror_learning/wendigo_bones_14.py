#!/usr/bin/env python3
"""
wendigo_bones_gold.py

This version integrates a "Gold Window" to give the agent a persistent sense of
its ideal self, preventing catastrophic forgetting and stabilizing performance
at high levels. It complements the RatchetPolicyArchive.
"""

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque, namedtuple
from dataclasses import dataclass, field
import random
import math

Transition = namedtuple("Transition", "obs act rew next_obs done mode dark")

# ---------------------------------------------------------
# Dataclasses for Gold Window (New)
# ---------------------------------------------------------
@dataclass
class GoldEpisode:
    """Stores a full, high-quality episode trajectory."""
    score: int
    mean_dr: float
    transitions: list[Transition] = field(default_factory=list)

class GoldWindow:
    """A buffer of the agent's best-ever episodes to act as a 'sense of self'."""
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.buffer: list[GoldEpisode] = []

    def add(self, episode: GoldEpisode):
        """Adds an episode, maintaining a sorted list of the best."""
        self.buffer.append(episode)
        # Sort by score (high is good) then by mean_dr (low is good)
        self.buffer.sort(key=lambda e: (e.score, -e.mean_dr), reverse=True)
        if len(self.buffer) > self.capacity:
            self.buffer = self.buffer[:self.capacity]

    def sample_clean_transitions(self, k: int) -> list[Transition]:
        """Samples the k cleanest transitions from all episodes in the window."""
        if not self.buffer:
            return []
        
        all_transitions = [t for ep in self.buffer for t in ep.transitions]
        # Sort all available transitions by their dark residue (lower is better)
        all_transitions.sort(key=lambda t: t.dark)
        
        return all_transitions[:k]

# ---------------------------------------------------------
# Dark Residue + Classifier
# ---------------------------------------------------------
def dark_residue(obs: np.ndarray) -> float:
    x, xdot, theta, thetadot = obs
    return (0.4 * abs(x) + 0.2 * abs(xdot) + 1.5 * abs(theta) + 0.3 * abs(thetadot))

def classify_mode(dr: float, ddr: float) -> str:
    DR_SMALL, DR_LARGE = 0.15, 0.35
    if ddr < 0.0: return "Weaver" if dr <= DR_SMALL else "Gladiator"
    else: return "Vortex" if dr >= DR_LARGE else "Drifter"

# ---------------------------------------------------------
# MLP and RatchetPolicyArchive (Unchanged)
# ---------------------------------------------------------
class MLP(nn.Module):
    def __init__(self, inp, out, act=nn.ReLU):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(inp, 128), act(),
            nn.Linear(128, 128), act(),
            nn.Linear(128, out),
        )
    def forward(self, x): return self.net(x)

class RatchetPolicyArchive:
    def __init__(self, capacity=5, patience=6):
        self.capacity, self.patience = capacity, patience
        self.snapshots, self.bad_streak, self.best_ever, self.ratchet_threshold = [], 0, 0, 0

    def maybe_store(self, steps, actor, critic, target_critic):
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
        self.snapshots = self.snapshots[:self.capacity]
        self.ratchet_threshold = steps

    def get_teacher_state_dict(self):
        return random.choice(self.snapshots)["actor"] if self.snapshots else None

    def report_and_should_restore(self, steps):
        if not self.snapshots or self.best_ever == 0: return False
        if steps < self.best_ever * 0.6: self.bad_streak += 1
        else: self.bad_streak = 0
        return self.bad_streak >= self.patience

    def restore_best(self, actor, critic, target_critic):
        if not self.snapshots: return
        best_snapshot = self.snapshots[0]
        actor.load_state_dict(best_snapshot["actor"])
        critic.load_state_dict(best_snapshot["critic"])
        target_critic.load_state_dict(best_snapshot["target"])
        self.bad_streak = 0
        print(f"[ARCHIVE] Restored best policy ({best_snapshot['steps']} steps)")

# ---------------------------------------------------------
# AC (Modified to accept Gold Batch)
# ---------------------------------------------------------
class PirouetteAC:
    def __init__(self, obs_dim, act_dim, lr=3e-4, gamma=0.99, tau=0.01):
        self.actor = MLP(obs_dim, act_dim)
        self.critic = MLP(obs_dim + act_dim, 1)
        self.target_critic = MLP(obs_dim + act_dim, 1)
        self.target_critic.load_state_dict(self.critic.state_dict())
        self.opt_actor = optim.Adam(self.actor.parameters(), lr=lr)
        self.opt_critic = optim.Adam(self.critic.parameters(), lr=lr)
        self.gamma, self.tau = gamma, tau
        self.critic_loss_ema = None

    @torch.no_grad()
    def act(self, obs, noise_std=0.1):
        obs_t = torch.as_tensor(obs, dtype=torch.float32).unsqueeze(0)
        a = self.actor(obs_t) + noise_std * torch.randn_like(self.actor(obs_t))
        return a.squeeze(0).clamp(-1.0, 1.0).numpy()

    def update(self, batch, batch_weaver=None, batch_anchor=None, batch_gold=None, shock_factor=4.0): # <<< MODIFIED
        # Critic trains on a general sample of all experiences
        obs, act, rew, nxt, done = map(torch.as_tensor, (
            np.stack([b.obs for b in batch]),
            np.stack([b.act for b in batch]),
            np.stack([b.rew for b in batch]).reshape(-1, 1),
            np.stack([b.next_obs for b in batch]),
            np.stack([b.done for b in batch]).reshape(-1, 1)
        ))
        obs, act, rew, nxt, done = obs.float(), act.float(), rew.float(), nxt.float(), done.float()
        
        with torch.no_grad():
            nxt_act = self.actor(nxt)
            tgt_q = self.target_critic(torch.cat([nxt, nxt_act], dim=-1))
            y = rew + self.gamma * (1.0 - done) * tgt_q

        q = self.critic(torch.cat([obs, act], dim=-1))
        critic_loss = nn.functional.mse_loss(q, y)

        do_critic = self.critic_loss_ema is None or critic_loss.item() <= shock_factor * self.critic_loss_ema
        if self.critic_loss_ema is None: self.critic_loss_ema = critic_loss.item()
        else: self.critic_loss_ema = 0.9 * self.critic_loss_ema + 0.1 * critic_loss.item()

        if do_critic:
            self.opt_critic.zero_grad(); critic_loss.backward(); self.opt_critic.step()

        # <<< MODIFIED: Actor trains on a mix biased towards HIGH-QUALITY transitions
        actor_batch = (batch_weaver or []) + (batch_anchor or []) + (batch_gold or [])
        if not actor_batch:
            actor_batch = batch # Fallback
        
        obs_actor = torch.as_tensor(np.stack([b.obs for b in actor_batch]), dtype=torch.float32)
        act_pred = self.actor(obs_actor)
        q_for_act = self.critic(torch.cat([obs_actor, act_pred], dim=-1))
        actor_loss = -q_for_act.mean()

        self.opt_actor.zero_grad(); actor_loss.backward(); self.opt_actor.step()

        with torch.no_grad():
            for p, tp in zip(self.critic.parameters(), self.target_critic.parameters()):
                tp.data.mul_(1 - self.tau).add_(self.tau * p.data)

# ---------------------------------------------------------
# Wrapper & Reward (Unchanged)
# ---------------------------------------------------------
class DiscreteToBox(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
    def action(self, act): return 0 if act[0] < 0 else 1

PRIME_W_SPAN, PRIME_W_COH, PRIME_W_DR, MAX_STEPS = 1.0, 1.5, 1.0, 500

def prime_directive_reward(cur_dr, ddr, step_idx, max_steps=MAX_STEPS):
    span, closure = step_idx / max_steps, max(0.0, -ddr)
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
    
    gold_window = GoldWindow(capacity=10) # <<< NEW
    
    BATCH_GEN, BATCH_W, BATCH_A, BATCH_G = 64, 24, 24, 16 # <<< MODIFIED Batch sizes

    archive = RatchetPolicyArchive(capacity=5, patience=8)

    obs, _ = env.reset()
    for _ in range(3_000):
        obs, _, done, trunc, _ = env.step(env.action_space.sample())
        if done or trunc: obs, _ = env.reset()

    top15, total_eps = deque(maxlen=15), 600

    for ep in range(1, total_eps + 1):
        obs, _ = env.reset()
        prev_dr = dark_residue(obs)
        ep_trans, steps = [], 0
        teacher_prob = 0.5 * (1 - ep / total_eps)

        while True:
            steps += 1
            a = agent.act(obs)
            if archive.get_teacher_state_dict() and random.random() < teacher_prob:
                with torch.no_grad():
                    teacher_actor.load_state_dict(archive.get_teacher_state_dict())
                    a_t = teacher_actor(torch.as_tensor(obs, dtype=torch.float32).unsqueeze(0))
                    a = a_t.squeeze(0).clamp(-1.0, 1.0).numpy()

            nxt, _, done, trunc, _ = env.step(a)
            cur_dr = dark_residue(nxt)
            ddr = cur_dr - prev_dr
            rew, span, coh = prime_directive_reward(cur_dr, ddr, steps, MAX_STEPS)
            
            tr = Transition(obs, a, rew, nxt, float(done or trunc), classify_mode(cur_dr, ddr), cur_dr)
            ep_trans.append(tr); general_buf.append(tr)
            if tr.mode in ("Weaver", "Gladiator"): weaver_buf.append(tr)

            if len(general_buf) > BATCH_GEN:
                batch_gen = random.sample(general_buf, BATCH_GEN)
                batch_w = random.sample(weaver_buf, BATCH_W) if len(weaver_buf) > BATCH_W else None
                batch_a = random.sample(anchor_buf, BATCH_A) if len(anchor_buf) > BATCH_A else None
                batch_g = gold_window.sample_clean_transitions(BATCH_G) if gold_window.buffer else None # <<< NEW
                
                agent.update(batch_gen, batch_weaver=batch_w, batch_anchor=batch_a, batch_gold=batch_g)

            obs, prev_dr = nxt, cur_dr
            if done or trunc: break

        # --- Episode End ---
        if steps >= 480: # <<< NEW: Threshold for adding to Gold Window
            mean_ep_dr = sum(t.dark for t in ep_trans) / len(ep_trans)
            gold_window.add(GoldEpisode(score=steps, mean_dr=mean_ep_dr, transitions=ep_trans))

        if steps >= 450: anchor_buf.extend(ep_trans[-min(steps, 450):])
        
        archive.maybe_store(steps, agent.actor, agent.critic, agent.target_critic)
        
        top15.append(steps)
        avg_top = sum(top15) / len(top15)

        print(
            f"Ep {ep:03d} | steps={steps:4d} | top15_avg={avg_top:6.2f} | "
            f"threshold={archive.ratchet_threshold:4d} | gold_win={len(gold_window.buffer)} | "
            f"anchor={len(anchor_buf):4d}"
        )

        if archive.report_and_should_restore(steps):
            archive.restore_best(agent.actor, agent.critic, agent.target_critic)
            
        if len(top15) == 15 and min(top15) >= 490:
             print("\n*** Stable Mastery Achieved (min of last 15 runs >= 490) ***")
             break

    env.close()

if __name__ == "__main__":
    train()