#!/usr/bin/env python3
"""
wendigo_bones_archived.py

Pirouette-only AC with:
- PRIME-DIRECTIVE reward (span + closure - DR)
- PolicyArchive to save a "mesh" of good policies.
- Teacher-guided exploration to prevent catastrophic forgetting.
- Anchor buffer and Shock clamp for stability.
"""

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque, namedtuple
import random

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
            nn.Linear(inp, 128),
            act(),
            nn.Linear(128, 128),
            act(),
            nn.Linear(128, out),
        )
    def forward(self, x):
        return self.net(x)

# ---------------------------------------------------------
# PolicyArchive (replaces PolicyVault)
# ---------------------------------------------------------
class PolicyArchive:
    def __init__(self, capacity=5, lock_steps=490, patience=5):
        self.capacity = capacity
        self.lock_steps = lock_steps
        self.patience = patience
        
        self.snapshots = []
        self.bad_streak = 0
        self.best_ever = 0

    def maybe_store(self, steps, actor, critic, target_critic):
        if steps < self.lock_steps:
            return

        self.best_ever = max(self.best_ever, steps)
        
        # Add the new policy snapshot
        snapshot = {
            "steps": steps,
            "actor": {k: v.cpu().clone() for k, v in actor.state_dict().items()},
            "critic": {k: v.cpu().clone() for k, v in critic.state_dict().items()},
            "target": {k: v.cpu().clone() for k, v in target_critic.state_dict().items()},
        }
        self.snapshots.append(snapshot)
        
        # Keep the archive sorted by performance
        self.snapshots.sort(key=lambda x: x["steps"], reverse=True)
        
        # Evict the worst policy if capacity is exceeded
        if len(self.snapshots) > self.capacity:
            self.snapshots.pop()

        print(f"[ARCHIVE] Stored policy at {steps} steps. Archive size: {len(self.snapshots)}")

    def get_teacher_state_dict(self):
        if not self.snapshots:
            return None
        # Return the state_dict of a random teacher's actor
        return random.choice(self.snapshots)["actor"]

    def report_and_should_restore(self, steps):
        if not self.snapshots:
            return False
        
        # If performance drops too far below our best ever, increment bad streak
        if steps < self.best_ever * 0.5: # e.g., if best is 500, trigger below 250
            self.bad_streak += 1
        else:
            self.bad_streak = 0
            
        return self.bad_streak >= self.patience

    def restore_best(self, actor, critic, target_critic):
        if not self.snapshots:
            return
        
        # The best policy is always at the top of our sorted list
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
    def act(self, obs, noise_std=0.1): # Slightly increased noise for exploration
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
# discrete wrapper
# ---------------------------------------------------------
class DiscreteToBox(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
    def action(self, act):
        return 0 if act[0] < 0 else 1

# ---------------------------------------------------------
# prime directive reward
# ---------------------------------------------------------
PRIME_W_SPAN = 1.0
PRIME_W_COH  = 1.5
PRIME_W_DR   = 1.0
MAX_STEPS    = 500

def prime_directive_reward(cur_dr, ddr, step_idx, max_steps=MAX_STEPS):
    span = step_idx / max_steps
    closure = max(0.0, -ddr)
    reward = (
        PRIME_W_SPAN * span
        + PRIME_W_COH * closure
        - PRIME_W_DR  * cur_dr
    )
    return reward, span, closure

# ---------------------------------------------------------
# training
# ---------------------------------------------------------
def train():
    env = DiscreteToBox(gym.make("CartPole-v1"))
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.shape[0]

    agent = PirouetteAC(obs_dim, act_dim)
    # This is a shell network to load teacher weights into
    teacher_actor = MLP(obs_dim, act_dim)

    general_buf = deque(maxlen=50_000)
    weaver_buf  = deque(maxlen=10_000)
    anchor_buf  = deque(maxlen=5_000) # Increased anchor buffer

    BATCH_GEN = 96
    BATCH_W   = 32
    BATCH_A   = 32

    archive = PolicyArchive(capacity=5, lock_steps=490, patience=6)

    obs, _ = env.reset()
    for _ in range(3_000):
        a = env.action_space.sample()
        nxt, _, done, trunc, _ = env.step(a)
        obs = nxt if not (done or trunc) else env.reset()[0]

    top15 = []
    total_eps = 600 # Train a bit longer

    for ep in range(1, total_eps + 1):
        obs, _ = env.reset()
        prev_dr = dark_residue(obs)
        done, trunc, steps, last_span = False, False, 0, 0.0

        # Teacher guidance probability decays over the run
        teacher_prob = 0.5 * (1 - ep / total_eps)

        while not (done or trunc):
            steps += 1
            a = None
            
            # --- Teacher-Guided Action Selection ---
            if len(archive.snapshots) > 0 and np.random.rand() < teacher_prob:
                with torch.no_grad():
                    teacher_dict = archive.get_teacher_state_dict()
                    teacher_actor.load_state_dict(teacher_dict)
                    obs_t = torch.as_tensor(obs, dtype=torch.float32).unsqueeze(0)
                    # Teacher action is decisive, no extra noise
                    a_t = teacher_actor(obs_t)
                    a = a_t.squeeze(0).clamp(-1.0, 1.0).numpy()
            else:
                # Agent explores on its own
                a = agent.act(obs)

            nxt, _, done, trunc, _ = env.step(a)

            cur_dr = dark_residue(nxt)
            ddr = cur_dr - prev_dr
            rew, span, coh = prime_directive_reward(cur_dr, ddr, steps, MAX_STEPS)
            last_span = span
            mode = classify_mode(cur_dr, ddr)

            tr = Transition(obs, a, rew, nxt, float(done), mode)
            general_buf.append(tr)
            if mode in ("Weaver", "Gladiator"):
                weaver_buf.append(tr)

            if len(general_buf) > BATCH_GEN:
                idxg = np.random.choice(len(general_buf), BATCH_GEN, replace=False)
                batch_gen = [general_buf[i] for i in idxg]
                
                batch_w = None
                if len(weaver_buf) > BATCH_W:
                    idxw = np.random.choice(len(weaver_buf), BATCH_W, replace=False)
                    batch_w = [weaver_buf[i] for i in idxw]

                batch_a = None
                if len(anchor_buf) > BATCH_A:
                    idxa = np.random.choice(len(anchor_buf), BATCH_A, replace=False)
                    batch_a = [anchor_buf[i] for i in idxa]

                agent.update(batch_gen, batch_weaver=batch_w, batch_anchor=batch_a)

            obs = nxt
            prev_dr = cur_dr

        # --- Episode End ---
        if steps >= 450:
            take_n = min(steps, 450)
            for i in range(1, take_n + 1):
                anchor_buf.append(general_buf[-i])

        archive.maybe_store(steps, agent.actor, agent.critic, agent.target_critic)

        top15.append(steps)
        top15 = sorted(top15, reverse=True)[:15]
        avg_top = sum(top15) / len(top15)

        print(
            f"Ep {ep:03d} | steps={steps:4d} | top15={avg_top:6.2f} | "
            f"teacher_p={teacher_prob:4.2f} | archive={len(archive.snapshots)} | "
            f"anchor={len(anchor_buf):4d}"
        )

        if archive.report_and_should_restore(steps):
            archive.restore_best(agent.actor, agent.critic, agent.target_critic)
            
        if len(top15) == 15 and avg_top >= 495:
             print("\n*** Stable Mastery Achieved ***")
             break

    env.close()

if __name__ == "__main__":
    train()