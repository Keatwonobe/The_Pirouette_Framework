#!/usr/bin/env python3
"""
wendigo_bones_pd.py

Pure-pirouette actor-critic (no SAC) with PRIME-DIRECTIVE reward.

Source principles:
- PDM-000 (Triune Law): act to minimize (H_i - H_total) and reduce Dark Residue,
  i.e. boost systemic longevity while keeping self-cost low. :contentReference[oaicite:4]{index=4}
- Pirouette closure reward from minimalist lineage (coherence = -ΔDR). :contentReference[oaicite:5]{index=5}

Environment: CartPole-v1 (500-step horizon)
"""

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque, namedtuple

Transition = namedtuple("Transition", "obs act rew next_obs done mode")

# ---------------------------------------------------------------------
# 1. Dark Residue + 4-mode classifier (same thresholds) 
# ---------------------------------------------------------------------
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

# ---------------------------------------------------------------------
# 2. Tiny MLPs
# ---------------------------------------------------------------------
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

# ---------------------------------------------------------------------
# 3. Pirouette Actor-Critic (same bones as your file) 
# ---------------------------------------------------------------------
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

    @torch.no_grad()
    def act(self, obs, noise_std=0.05):
        obs_t = torch.as_tensor(obs, dtype=torch.float32).unsqueeze(0)
        a = self.actor(obs_t)
        a = a + noise_std * torch.randn_like(a)
        return a.squeeze(0).numpy()

    def update(self, batch, batch_weaver=None):
        obs = torch.as_tensor(np.stack([b.obs for b in batch]), dtype=torch.float32)
        act = torch.as_tensor(np.stack([b.act for b in batch]), dtype=torch.float32)
        rew = torch.as_tensor(np.stack([b.rew for b in batch]), dtype=torch.float32).unsqueeze(-1)
        nxt = torch.as_tensor(np.stack([b.next_obs for b in batch]), dtype=torch.float32)
        done = torch.as_tensor(np.stack([b.done for b in batch]), dtype=torch.float32).unsqueeze(-1)

        # critic
        with torch.no_grad():
            nxt_act = self.actor(nxt)
            tgt_q = self.target_critic(torch.cat([nxt, nxt_act], dim=-1))
            y = rew + self.gamma * (1.0 - done) * tgt_q

        q = self.critic(torch.cat([obs, act], dim=-1))
        critic_loss = nn.functional.mse_loss(q, y)

        self.opt_critic.zero_grad()
        critic_loss.backward()
        self.opt_critic.step()

        # actor (prefer weaver/gladiator)
        if not batch_weaver:
            batch_weaver = batch

        obs_w = torch.as_tensor(np.stack([b.obs for b in batch_weaver]), dtype=torch.float32)
        act_pred = self.actor(obs_w)
        q_for_act = self.critic(torch.cat([obs_w, act_pred], dim=-1))
        actor_loss = -q_for_act.mean()

        self.opt_actor.zero_grad()
        actor_loss.backward()
        self.opt_actor.step()

        # soft target update
        with torch.no_grad():
            for p, tp in zip(self.critic.parameters(), self.target_critic.parameters()):
                tp.data.mul_(1 - self.tau).add_(self.tau * p.data)

# ---------------------------------------------------------------------
# 4. Discrete wrapper
# ---------------------------------------------------------------------
class DiscreteToBox(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
    def action(self, act):
        return 0 if act[0] < 0 else 1

# ---------------------------------------------------------------------
# 5. PRIME-DIRECTIVE reward
# ---------------------------------------------------------------------
# weights are clean + small on purpose; tune if you want a sharper closure bias
PRIME_W_SPAN = 1.0     # systemic / total enthalpy term
PRIME_W_COH  = 1.5     # closure term (same magnitude as bones) :contentReference[oaicite:6]{index=6}
PRIME_W_DR   = 1.0     # cost for self-residue

MAX_STEPS = 500        # CartPole-v1

def prime_directive_reward(cur_dr, ddr, step_idx, max_steps=MAX_STEPS):
    """
    Implements: r = w_span * span + w_coh * closure - w_dr * DR
    where span = step / max_steps
    """
    span = step_idx / max_steps
    closure = max(0.0, -ddr)          # only pay when DR is actually closing
    reward = (
        PRIME_W_SPAN * span
        + PRIME_W_COH * closure
        - PRIME_W_DR  * cur_dr
    )
    return reward, span, closure

# ---------------------------------------------------------------------
# 6. Training loop
# ---------------------------------------------------------------------
def train():
    env = DiscreteToBox(gym.make("CartPole-v1"))
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.shape[0]

    agent = PirouetteAC(obs_dim, act_dim)

    general_buf = deque(maxlen=50_000)
    weaver_buf = deque(maxlen=10_000)

    BATCH   = 128
    BATCH_W = 64

    # warmup (no learning)
    obs, _ = env.reset()
    for _ in range(5_000):
        a = env.action_space.sample()
        nxt, _, done, trunc, _ = env.step(a)
        obs = nxt if not (done or trunc) else env.reset()[0]

    top15 = []

    for ep in range(1, 401):
        obs, _ = env.reset()
        prev_dr = dark_residue(obs)
        done = False
        trunc = False
        steps = 0
        last_span = 0.0

        while not (done or trunc):
            steps += 1
            a = agent.act(obs, noise_std=0.05)
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

            # learn
            if len(general_buf) > BATCH:
                idx = np.random.choice(len(general_buf), BATCH, replace=False)
                batch = [general_buf[i] for i in idx]

                if len(weaver_buf) > BATCH_W:
                    widx = np.random.choice(len(weaver_buf), BATCH_W, replace=False)
                    batch_w = [weaver_buf[i] for i in widx]
                else:
                    batch_w = None

                agent.update(batch, batch_w)

            obs = nxt
            prev_dr = cur_dr

        # episode bookkeeping
        top15.append(steps)
        top15 = sorted(top15, reverse=True)[:15]
        avg_top = sum(top15) / len(top15)

        print(
            f"Ep {ep:03d} | steps={steps:4d} | span={last_span:5.3f} | "
            f"top15={avg_top:6.2f} | weaver={len(weaver_buf):5d} | general={len(general_buf):5d}"
        )

        # same spirit as your file, just lower threshold for demo
        if len(top15) == 15 and avg_top >= 450:
            print("*** PIR-AC (Prime Directive) mastery ***")
            break

    env.close()

if __name__ == "__main__":
    train()
