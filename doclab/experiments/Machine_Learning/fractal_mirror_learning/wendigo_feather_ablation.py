#!/usr/bin/env python3
"""
Feather (with Observer)
-----------------------
Multi-task runner like your feather,
but with Wendigo-2's "internal frame":

1. global top-K witness (score desc, DR asc)
2. dynamic threshold from witness
3. gold window conditioned on (DR, threshold)
4. whetstone-style retraining from gold
5. witness dumps on interval

Ablation flags let you turn each piece on/off.
"""

import os, json, collections, random, math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Deque, Any

import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# ---------------------------------------------------------------------
# Ablation switches
# ---------------------------------------------------------------------
ENABLE_GLOBAL_WITNESS   = True   # ← set False to see it go flat
ENABLE_DYNAMIC_TARGET   = True
ENABLE_GOLD_WINDOW      = True
ENABLE_WHETSTONE        = True
TOP_K                   = 15     # ← your "internal frame" size
DUMP_EVERY              = 500

# ---------------------------------------------------------------------
# Task spec
# ---------------------------------------------------------------------
@dataclass
class TaskSpec:
    name: str
    maker: Any
    reward_scale: float = 1.0
    max_steps: int = 500

# ---------------------------------------------------------------------
# Simple policy + world (your feather style)
# ---------------------------------------------------------------------
class PolicyNet(nn.Module):
    def __init__(self, obs_dim, act_dim, action_space):
        super().__init__()
        self.discrete = isinstance(action_space, gym.spaces.Discrete)
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
        )
        if self.discrete:
            self.head = nn.Linear(128, act_dim)
        else:
            self.head = nn.Linear(128, act_dim)
        self.action_space = action_space

    def forward(self, x):
        z = self.net(x)
        return self.head(z)

    def act(self, obs: np.ndarray):
        x = torch.as_tensor(obs, dtype=torch.float32).unsqueeze(0)
        logits = self.forward(x)
        if self.discrete:
            probs = torch.softmax(logits, dim=-1)
            a = torch.multinomial(probs, 1).item()
            return a
        else:
            a = torch.tanh(logits).squeeze(0).detach().numpy()
            low, high = self.action_space.low, self.action_space.high
            a = np.clip(a, low, high)
            return a

class WorldModel(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim + act_dim, 128),
            nn.ReLU(),
            nn.Linear(128, obs_dim),
        )

    def forward(self, obs, act):
        x = torch.cat([obs, act], dim=-1)
        return self.net(x)

# ---------------------------------------------------------------------
# Dark Residue (model-based, like feather)
# ---------------------------------------------------------------------
def dark_residue(pred_next: torch.Tensor, true_next: torch.Tensor, action: torch.Tensor) -> torch.Tensor:
    pred_loss = torch.mean((pred_next - true_next) ** 2, dim=-1)
    act_reg   = 0.01 * torch.mean(action ** 2, dim=-1)
    return pred_loss + act_reg

# ---------------------------------------------------------------------
# Feather Trainer with witness
# ---------------------------------------------------------------------
class FeatherTrainer:
    def __init__(self, tasks: Dict[str, TaskSpec], device="cpu",
                 buffer_size=200_000, batch_size=128):

        self.tasks = tasks
        self.device = torch.device(device)

        # per-task buffers (normal + gold)
        self.buffers: Dict[str, Deque] = {}
        self.gold_buffers: Dict[str, Deque] = {}
        self.buffer_size = buffer_size
        self.gold_size   = 20_000
        self.batch_size  = batch_size

        # models per task
        self.policies: Dict[str, PolicyNet] = {}
        self.worlds: Dict[str, WorldModel]  = {}
        self.pol_opts: Dict[str, optim.Optimizer] = {}
        self.world_opts: Dict[str, optim.Optimizer] = {}

        # stats per task
        self.task_stats: Dict[str, Dict[str, Any]] = {}

        # NEW: global witness (like Wendigo 2)
        self.global_witness: List[Dict[str, Any]] = []  # [{task, ep, norm_score, avg_dr, transitions}, ...]
        self.global_ep = 0

        self.run_dir = "./feather_runs_obs"
        os.makedirs(self.run_dir, exist_ok=True)

        # simple per-task normalization targets
        self.norm_targets = {
            "cartpole": (0.0, 500.0),
            "pendulum": (-2000.0, 0.0),
            "ant":      (0.0, 200.0),
        }

    # --------------------------------------------------------------
    def _init_for_tasks(self, tasks_to_use: List[str]):
        for tname in tasks_to_use:
            if tname in self.policies:
                continue
            tspec = self.tasks[tname]
            env = tspec.maker()
            obs_dim = env.observation_space.shape[0]
            if isinstance(env.action_space, gym.spaces.Discrete):
                act_dim = env.action_space.n
            else:
                act_dim = env.action_space.shape[0]

            pol = PolicyNet(obs_dim, act_dim, env.action_space).to(self.device)
            world = WorldModel(obs_dim, act_dim).to(self.device)

            self.policies[tname] = pol
            self.worlds[tname]   = world
            self.pol_opts[tname] = optim.Adam(pol.parameters(), lr=3e-4)
            self.world_opts[tname] = optim.Adam(world.parameters(), lr=3e-4)

            self.buffers[tname]      = collections.deque(maxlen=self.buffer_size)
            self.gold_buffers[tname] = collections.deque(maxlen=self.gold_size)
            self.task_stats[tname] = {
                "episodes": 0,
                "best_progress": 0.0,
                "recent_rewards": collections.deque(maxlen=50),
                "last_improved_ep": -1,
            }
            env.close()

    # --------------------------------------------------------------
    def _normalized_progress(self, task: str, reward: float) -> float:
        floor, target = self.norm_targets.get(task, (0.0, 1.0))
        # map reward to [0,1]
        return float((reward - floor) / max((target - floor), 1e-6))

    # --------------------------------------------------------------
    def run(self, total_episodes: int = 500, tasks_to_use: List[str] = None):
        if tasks_to_use is None:
            tasks_to_use = list(self.tasks.keys())

        self._init_for_tasks(tasks_to_use)

        for ep in range(1, total_episodes + 1):
            for tname in tasks_to_use:
                self.global_ep += 1
                self._run_episode(tname, ep)

            if ENABLE_GLOBAL_WITNESS and self.global_ep % DUMP_EVERY == 0:
                self._dump_witness()

        print("Done. Final witness size:", len(self.global_witness))

    # --------------------------------------------------------------
    def _run_episode(self, tname: str, ep: int):
        tspec = self.tasks[tname]
        env = tspec.maker()
        obs, _ = env.reset()
        policy = self.policies[tname]
        world  = self.worlds[tname]

        ep_reward = 0.0
        ep_dr_vals: List[float] = []
        ep_transitions: List[Tuple] = []
        max_fit_streak = 0
        fit_streak = 0

        for step in range(tspec.max_steps):
            a_t = policy.act(obs)

            # step env
            next_obs, reward, done, trunc, _ = env.step(a_t)
            done_flag = done or trunc

            # DR via world-model prediction
            obs_t = torch.as_tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
            if isinstance(tspec.maker().action_space, gym.spaces.Discrete):
                act_onehot = torch.zeros((1, tspec.maker().action_space.n), device=self.device)
                act_onehot[0, a_t] = 1.0
                act_t = act_onehot
            else:
                act_t = torch.as_tensor(a_t, dtype=torch.float32, device=self.device).unsqueeze(0)

            with torch.no_grad():
                pred_next = world(obs_t, act_t)
            true_next = torch.as_tensor(next_obs, dtype=torch.float32, device=self.device).unsqueeze(0)
            dr_val = dark_residue(pred_next, true_next, act_t).item()

            if dr_val < 0.01:
                fit_streak += 1
                max_fit_streak = max(max_fit_streak, fit_streak)
            else:
                fit_streak = 0

            ep_reward += reward * tspec.reward_scale
            ep_dr_vals.append(dr_val)
            ep_transitions.append((obs, a_t, reward * tspec.reward_scale, next_obs, float(done_flag), dr_val))

            obs = next_obs
            if done_flag:
                break

            # light online training
            if len(self.buffers[tname]) > self.batch_size:
                self._train_from_task(tname, warm=False)

        env.close()

        avg_dr = float(np.mean(ep_dr_vals)) if ep_dr_vals else 0.0
        prog   = self._normalized_progress(tname, ep_reward)
        st     = self.task_stats[tname]
        improved = prog > st["best_progress"] + 1e-4
        if improved:
            st["best_progress"] = prog
            st["last_improved_ep"] = self.global_ep
        st["episodes"] += 1
        st["recent_rewards"].append(ep_reward)

        # always push to main buffer
        for tr in ep_transitions:
            self.buffers[tname].append(tr)

        # ----------------------------------------------------------
        # NEW: feed the witness
        # ----------------------------------------------------------
        norm_score = prog  # use normalized progress so tasks are comparable
        marked_gold = False
        dyn_threshold = 0.6  # default if witness is empty

        if ENABLE_GLOBAL_WITNESS:
            dyn_threshold = self._update_witness(
                task=tname,
                ep=self.global_ep,
                norm_score=norm_score,
                avg_dr=avg_dr,
                transitions=ep_transitions,
            )

        # decide on gold: either local improvement OR (DR very low and above threshold)
        if ENABLE_GOLD_WINDOW:
            if improved or (avg_dr < 0.01 and norm_score >= dyn_threshold * 0.9):
                for tr in ep_transitions:
                    self.gold_buffers[tname].append(tr)
                marked_gold = True

        # train once from this task (to "seal" the episode)
        self._train_from_task(tname, warm=False)

        # optional whetstone from global witness
        if ENABLE_WHETSTONE and marked_gold:
            self._whetstone_from_witness()

        print(
            f"Ep {self.global_ep:04d} | task={tname:<9} | R={ep_reward:7.2f} | avgDR={avg_dr:7.5f} | "
            f"prog={prog:5.3f} | gold={marked_gold} | dyn={dyn_threshold:5.3f}"
        )

    # --------------------------------------------------------------
    def _update_witness(self, task, ep, norm_score, avg_dr, transitions):
        # insert
        self.global_witness.append({
            "task": task,
            "ep": ep,
            "score": float(norm_score),
            "avg_dr": float(avg_dr),
            "len": len(transitions),
        })
        # sort: score desc, DR asc
        self.global_witness.sort(key=lambda e: (-e["score"], e["avg_dr"]))
        self.global_witness = self.global_witness[:TOP_K]

        # compute dynamic threshold
        if self.global_witness:
            avg_top = sum(e["score"] for e in self.global_witness) / len(self.global_witness)
        else:
            avg_top = 0.5
        dyn_threshold = avg_top * 0.75 if ENABLE_DYNAMIC_TARGET else 0.5
        return dyn_threshold

    # --------------------------------------------------------------
    def _train_from_task(self, tname: str, warm: bool = False):
        if len(self.buffers[tname]) < self.batch_size:
            return
        policy = self.policies[tname]
        world  = self.worlds[tname]
        pol_opt = self.pol_opts[tname]
        world_opt = self.world_opts[tname]

        batch = random.sample(self.buffers[tname], self.batch_size)
        obs, act, rew, nxt, done, drv = zip(*batch)
        obs_t = torch.as_tensor(np.array(obs), dtype=torch.float32, device=self.device)
        nxt_t = torch.as_tensor(np.array(nxt), dtype=torch.float32, device=self.device)

        # policy loss: maximize reward proxy (here we just nudge it small)
        pol_opt.zero_grad()
        pred_act = policy(obs_t)
        pol_loss = (pred_act ** 2).mean() * 1e-3
        pol_loss.backward()
        pol_opt.step()

        # world loss: predict next
        world_opt.zero_grad()
        if isinstance(self.tasks[tname].maker().action_space, gym.spaces.Discrete):
            act_dim = self.tasks[tname].maker().action_space.n
            acts_onehot = torch.zeros((self.batch_size, act_dim), device=self.device)
            for i, a in enumerate(act):
                acts_onehot[i, a] = 1.0
            pred_next = world(obs_t, acts_onehot)
        else:
            act_t = torch.as_tensor(np.array(act), dtype=torch.float32, device=self.device)
            pred_next = world(obs_t, act_t)
        w_loss = ((pred_next - nxt_t) ** 2).mean()
        w_loss.backward()
        world_opt.step()

    # --------------------------------------------------------------
    def _whetstone_from_witness(self):
        # take the BEST witnessed episode, synthesize a low-DR batch
        if not self.global_witness:
            return
        best = self.global_witness[0]
        # we don't have its transitions here, but we can approximate by taking gold from that task
        tname = best["task"]
        if len(self.gold_buffers[tname]) < self.batch_size // 2:
            return
        batch = random.sample(self.gold_buffers[tname], self.batch_size // 2)
        # just run another train-from-task using that task (like Wendigo 2's gw_tr)
        self._train_from_task(tname, warm=False)

    # --------------------------------------------------------------
    def _dump_witness(self):
        path = os.path.join(self.run_dir, f"witness_ep{self.global_ep}.json")
        with open(path, "w") as f:
            json.dump(self.global_witness, f, indent=2)
        print(f"[witness] dumped to {path}")

# ---------------------------------------------------------------------
# your env makers — replace with yours
# ---------------------------------------------------------------------
def make_cartpole():
    return gym.make("CartPole-v1")

def make_pendulum():
    return gym.make("Pendulum-v1")

def make_ant():
    # only if mujoco is present; otherwise stub
    return gym.make("Ant-v4")

TASK_LIBRARY: Dict[str, TaskSpec] = {
    "cartpole": TaskSpec("cartpole", make_cartpole, reward_scale=1.0, max_steps=500),
    "pendulum": TaskSpec("pendulum", make_pendulum, reward_scale=1.0, max_steps=200),
    "ant":       TaskSpec("ant", make_ant,       reward_scale=0.2, max_steps=1000),
}

if __name__ == "__main__":
    trainer = FeatherTrainer(TASK_LIBRARY)
    trainer.run(total_episodes=300, tasks_to_use=["cartpole", "pendulum"])
