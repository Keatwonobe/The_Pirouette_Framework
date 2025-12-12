#!/usr/bin/env python3
"""
wendigo_pirouette_ac.py

A pirouette-only alternative to SAC:
- environment: CartPole-v1 via gymnasium
- reward: dark-residue closure (same as minimalist_4)
- replay: dual-buffer (general + weaver/gladiator)
- learner: small actor-critic with target network
"""

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque, namedtuple

Transition = namedtuple("Transition", "obs act rew next_obs done mode")

# ---------------------------------------------------------------------
# 1. Dark Residue + mode classifier (same thresholds as before)
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
        if dr <= DR_SMALL:
            return "Weaver"
        else:
            return "Gladiator"
    else:
        if dr >= DR_LARGE:
            return "Vortex"
        else:
            return "Drifter"


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
# 3. Pirouette Actor-Critic
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
        """
        batch: list[Transition]
        batch_weaver: list[Transition] or None
        """
        # ----- critic update (general) -----
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

        self.opt_critic.zero_grad()
        critic_loss.backward()
        self.opt_critic.step()

        # ----- actor update (from weaver if available, else general) -----
        if batch_weaver is None or len(batch_weaver) == 0:
            batch_weaver = batch

        obs_w = torch.as_tensor(np.stack([b.obs for b in batch_weaver]), dtype=torch.float32)
        act_pred = self.actor(obs_w)
        q_for_act = self.critic(torch.cat([obs_w, act_pred], dim=-1))
        # maximize q  -> minimize -q
        actor_loss = -q_for_act.mean()

        self.opt_actor.zero_grad()
        actor_loss.backward()
        self.opt_actor.step()

        # ----- soft update -----
        with torch.no_grad():
            for p, tp in zip(self.critic.parameters(), self.target_critic.parameters()):
                tp.data.mul_(1 - self.tau).add_(self.tau * p.data)

# ---------------------------------------------------------------------
# 4. Discrete wrapper (same trick)
# ---------------------------------------------------------------------
class DiscreteToBox(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
    def action(self, act):
        return 0 if act[0] < 0 else 1

# ---------------------------------------------------------------------
# 5. Training
# ---------------------------------------------------------------------
def train():
    env = DiscreteToBox(gym.make("CartPole-v1"))
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.shape[0]

    agent = PirouetteAC(obs_dim, act_dim)

    general_buf = deque(maxlen=50_000)
    weaver_buf = deque(maxlen=10_000)

    BATCH = 128
    BATCH_W = 64

    # warmup
    obs, _ = env.reset()
    for _ in range(5_000):
        a = env.action_space.sample()
        nxt, _, done, trunc, _ = env.step(a)
        obs = nxt if not (done or trunc) else env.reset()[0]

    top15 = []

    gamma_coh = 1.5
    beta_dur = 0.05
    delta_dis = 1.0

    for ep in range(1, 301):
        obs, _ = env.reset()
        prev_dr = dark_residue(obs)
        done = False
        trunc = False
        ep_rew = 0
        steps = 0

        while not (done or trunc):
            a = agent.act(obs, noise_std=0.05)
            nxt, _, done, trunc, _ = env.step(a)

            cur_dr = dark_residue(nxt)
            ddr = cur_dr - prev_dr

            coh_gain = gamma_coh * max(0.0, -ddr)
            reward = coh_gain + beta_dur - delta_dis * cur_dr

            mode = classify_mode(cur_dr, ddr)

            tr = Transition(obs, a, reward, nxt, float(done), mode)
            general_buf.append(tr)
            if mode in ("Weaver", "Gladiator"):
                weaver_buf.append(tr)

            # learn every step once buffer big enough
            if len(general_buf) > BATCH:
                batch_idx = np.random.choice(len(general_buf), BATCH, replace=False)
                batch = [general_buf[i] for i in batch_idx]

                if len(weaver_buf) > BATCH_W:
                    w_idx = np.random.choice(len(weaver_buf), BATCH_W, replace=False)
                    batch_w = [weaver_buf[i] for i in w_idx]
                else:
                    batch_w = None

                agent.update(batch, batch_w)

            obs = nxt
            prev_dr = cur_dr
            ep_rew += reward
            steps += 1

        top15.append(steps)
        top15 = sorted(top15, reverse=True)[:15]
        avg_top = sum(top15) / len(top15)

        print(
            f"Ep {ep:03d} | steps={steps:4d} | top15={avg_top:6.2f} | "
            f"weaver={len(weaver_buf):5d} | general={len(general_buf):5d}"
        )

        if len(top15) == 15 and avg_top >= 450:
            print("*** PIR-AC mastery ***")
            break

    env.close()


if __name__ == "__main__":
    train()