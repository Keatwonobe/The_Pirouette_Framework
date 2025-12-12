#!/usr/bin/env python3
import gymnasium as gym
import numpy as np
import copy
import torch
import os, time, collections
from collections import deque
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure
from stable_baselines3.common.buffers import ReplayBuffer

# =========================================================
# 1. TASK CONFIG – Pendulum warmup, then Ant
# =========================================================
TASKS = [
    {
        "name": "Pendulum",
        "env_id": "Pendulum-v1",
        "is_discrete": False,
        "max_episodes": 80,
        "pendulum_mastery": -40.0,
        # pirouette weights
        "gamma_coherence": 1.2,
        "beta_duration": 0.1,
        "delta_dissonance": 0.25,
        # mirage
        "mirage_base": 0.03,
        "mirage_gain": 0.6,
        "mirage_max": 0.35,
        "horizon": 8,
        "span_threshold": 3,
        # reward blend
        "env_reward_weight": 0.15,
        "pirouette_reward_weight": 0.85,
    },
    {
        "name": "Ant",
        "env_id": "Ant-v5",
        "is_discrete": False,
        "max_episodes": 1200,
        # pirouette weights for locomotion
        "gamma_coherence": 1.0,
        "beta_duration": 0.5,
        "delta_dissonance": 0.15,
        # mirage
        "mirage_base": 0.05,
        "mirage_gain": 0.4,
        "mirage_max": 0.35,
        "horizon": 12,
        "span_threshold": 4,
        # reward blend
        "env_reward_weight": 0.35,
        "pirouette_reward_weight": 0.55,  # leave a bit more room for forward
        "forward_gain": 3.0,
    },
    # Humanoid can be added here later
]

# =========================================================
# 2. Universal DR
# =========================================================
class UniversalDR:
    def __init__(self, obs_dim: int, hist_len: int = 1500):
        self.obs_dim = obs_dim
        self.hist = deque(maxlen=hist_len)
        self.scale = np.ones(obs_dim, dtype=np.float32)

    def update_scale(self):
        if len(self.hist) < 50:
            return
        arr = np.array(self.hist, dtype=np.float32)
        self.scale = np.std(arr, axis=0) + 1e-6

    def calculate(self, obs: np.ndarray, prev: np.ndarray | None = None) -> float:
        self.hist.append(obs)
        if len(self.hist) % 100 == 0:
            self.update_scale()

        base = 0.3 * np.sum(np.abs(obs / self.scale)) / self.obs_dim
        if prev is not None:
            vel = np.linalg.norm((obs - prev) / self.scale)
        else:
            vel = 0.0

        dr = base + 0.7 * vel
        return max(0.01, float(dr))

# =========================================================
# 3. Pirouette Lagrangian
# =========================================================
def pirouette_lagrangian(dr, dr_d, gamma, beta, delta):
    coh = gamma * max(0.0, -dr_d)
    press = delta * dr
    L = coh + beta - press
    return float(np.clip(L, -20.0, 20.0))

# =========================================================
# 4. Span-aware SAC wrapper (now: configurable buffer per env)
# =========================================================
class SpanAwareSAC:
    def __init__(
        self,
        env,
        span_threshold: int = 4,
        buffer_size: int = 50_000,
        learning_starts: int = 5_000,
        
    ):
        self.env = env
        self.degrade_streak = 0

        self.agent = SAC(
            "MlpPolicy",
            env,
            verbose=0,
            train_freq=(1, "step"),
            buffer_size=buffer_size,
            learning_starts=learning_starts,
        )
        self.span_threshold = span_threshold
        self.base_lr = 3e-4
        self.last_span = 0
        self.recent_rewards = deque(maxlen=50)
        self.checkpoints = []

        # NEW: anchor for “that one good run”
        self.anchor_score = -1e9
        self.anchor_dr = 999.0
        self.anchor_span = 0
        self.anchor_ep = -1
        self.anchor_state = None

    def save_anchor(self, score, dr, span, ep):
        self.anchor_score = float(score)
        self.anchor_dr = float(dr)
        self.anchor_span = int(span)
        self.anchor_ep = int(ep)
        self.anchor_state = copy.deepcopy(self.agent.policy.actor.state_dict())
        print(f"  [anchor] latched ep={ep}, score={score:.1f}, DR={dr:.3f}, span={span}")

    def restore_anchor(self):
        if self.anchor_state is not None:
            self.agent.policy.actor.load_state_dict(self.anchor_state)
            print(f"  [anchor] restored → score≈{self.anchor_score:.1f}")
        else:
            print("  [anchor] restore requested but no anchor saved")

    def train_step(self, span: int):
        act_opt = self.agent.policy.actor.optimizer
        crt_opt = self.agent.policy.critic.optimizer
        act_lr_old = act_opt.param_groups[0]["lr"]
        crt_lr_old = crt_opt.param_groups[0]["lr"]

        if span < self.span_threshold:
            scale = max(0.1, span / self.span_threshold)
            for g in act_opt.param_groups:
                g["lr"] = self.base_lr * scale
            for g in crt_opt.param_groups:
                g["lr"] = self.base_lr * scale

        self.agent.train(gradient_steps=1)

        for g in act_opt.param_groups:
            g["lr"] = act_lr_old
        for g in crt_opt.param_groups:
            g["lr"] = crt_lr_old

    def checkpoint(self, ep: int, span: int):
        self.checkpoints.append(
            (ep, span, copy.deepcopy(self.agent.policy.actor.state_dict()))
        )
        if len(self.checkpoints) > 5:
            self.checkpoints.pop(0)

    def rollback_if_needed(self, span: int):
        if span == 0 and self.checkpoints:
            best = max(self.checkpoints, key=lambda x: x[1])
            ep, sp, st = best
            print(f"  ! rollback → episode {ep} (span={sp})")
            self.agent.policy.actor.load_state_dict(st)

# =========================================================
# 5. Snail-probe tool (now baseline = real episode return)
# =========================================================
class SnailProbeTool:
    def __init__(
        self,
        sac_wrapper,
        max_frac: float = 0.35,
        min_frac: float = 0.03,
        base_noise: float = 0.01,
        max_noise: float = 0.08,
        probe_steps: int = 800,
        score_slack: float = 0.03,
    ):
        self.sacw = sac_wrapper
        # "global" caps (used for small tasks)
        self.max_frac = max_frac
        self.min_frac = min_frac
        self.base_noise = base_noise
        self.max_noise = max_noise
        self.probe_steps = probe_steps
        self.score_slack = score_slack
        self._saved_actor_state = None
        self.best_seen_score = -1e9  # monotonic guard

    def _pick_probe_size(self, task, span: int, max_span: int, mean_dr: float):
        # task-aware caps
        if task is not None and task.get("name") == "Ant":
            task_max_frac = 0.12     # MUCH smaller than 0.35
            task_max_noise = 0.04
        else:
            task_max_frac = self.max_frac
            task_max_noise = self.max_noise

        span_ratio = 0.0 if max_span == 0 else min(1.0, span / max_span)
        dr_ratio = 1.0 - np.exp(-3.0 * float(mean_dr))

        frac = (
            self.min_frac
            + (task_max_frac - self.min_frac)
            * (1.0 - 0.5 * span_ratio + 0.5 * dr_ratio)
        )
        frac = float(np.clip(frac, self.min_frac, task_max_frac))
        noise = self.base_noise + (task_max_noise - self.base_noise) * dr_ratio
        return frac, float(noise)

    def _get_actor_params(self):
        return list(self.sacw.agent.policy.actor.parameters())

    def _select_param_indices(self, params, fraction: float):
        flat = [p for p in params if p.requires_grad]
        k = max(1, int(len(flat) * fraction))
        idxs = np.random.choice(len(flat), size=k, replace=False)
        return [flat[i] for i in idxs]

    def _apply_noise(self, tensors, noise_scale: float):
        for t in tensors:
            with torch.no_grad():
                t.add_(torch.randn_like(t) * noise_scale)

    def _save_actor(self):
        self._saved_actor_state = copy.deepcopy(self.sacw.agent.policy.actor.state_dict())

    def _restore_actor(self):
        if self._saved_actor_state is not None:
            self.sacw.agent.policy.actor.load_state_dict(self._saved_actor_state)
            self._saved_actor_state = None

    def probe(
        self,
        env,
        task,
        span: int,
        max_span: int,
        base_score: float,
        base_mean_dr: float,
        dr_calc,
    ):
        # 0) freeze once Ant is good – don't risk a fall
        if task is not None and task.get("name") == "Ant" and base_score > 500.0:
            print("  [snail] skipped: Ant ≥ 500, freezing actor")
            return

        # keep a monotonic baseline
        base_score = max(base_score, self.best_seen_score)

        # 1) save current actor
        self._save_actor()

        # 2) task-aware poke size
        frac, noise = self._pick_probe_size(task, span, max_span, base_mean_dr)

        # 3) perturb chosen params
        params = self._get_actor_params()
        chosen = self._select_param_indices(params, frac)
        self._apply_noise(chosen, noise)

        # 4) evaluate the probe under same rules
        probe_score, probe_mean_dr = evaluate_policy_once(
            env,
            self.sacw.agent,
            dr_calc,
            task=task,
            max_steps=self.probe_steps,
        )

        # 5) sign-aware acceptance
        if base_score <= 0.0:
            # fragile zone: must actually help coherence OR at least not crater score
            score_ok = probe_score >= (base_score - 10.0)
            dr_ok = probe_mean_dr <= (base_mean_dr * 0.75)
        else:
            # normal zone
            score_ok = probe_score >= base_score * (1.0 - self.score_slack)
            dr_ok = probe_mean_dr <= base_mean_dr * 0.95

        if score_ok or dr_ok:
            print(
                f"  [snail] accepted probe: frac={frac:.3f}, noise={noise:.3f}, "
                f"score={probe_score:.1f} (base={base_score:.1f}), "
                f"DR={probe_mean_dr:.3f} (base={base_mean_dr:.3f})"
            )
            self._saved_actor_state = None
            self.best_seen_score = max(self.best_seen_score, probe_score)
        else:
            print(
                f"  [snail] rejected probe: frac={frac:.3f}, noise={noise:.3f}, "
                f"score={probe_score:.1f} < base={base_score:.1f}"
            )
            self._restore_actor()


# =========================================================
# 6. Policy evaluator (now knows about Ant forward)
# =========================================================
ANT_TORSO = "torso"

def evaluate_policy_once(env, agent, dr_calc, task=None, max_steps=800):
    obs, _ = env.reset()
    done = False
    truncated = False
    steps = 0
    total_reward = 0.0
    dr_vals = []
    prev_obs = None
    last_xpos = None

    while not done and not truncated and steps < max_steps:
        act, _ = agent.predict(obs, deterministic=True)
        nxt, env_r, done, truncated, _ = env.step(act)

        forward_reward = 0.0
        if task is not None and task["name"] == "Ant":
            xpos = float(env.unwrapped.get_body_com(ANT_TORSO)[0])
            if last_xpos is None:
                last_xpos = xpos
            dx = xpos - last_xpos
            last_xpos = xpos
            if dx > 0:
                forward_reward = task.get("forward_gain", 3.0) * dx

        dr = dr_calc.calculate(nxt, prev_obs)
        dr_vals.append(dr)

        reward = (
            task["env_reward_weight"] * env_r if task else env_r
        ) + (
            forward_reward
        )
        total_reward += reward

        prev_obs = obs
        obs = nxt
        steps += 1

    mean_dr = float(np.mean(dr_vals)) if dr_vals else 1.0
    return total_reward, mean_dr

# =========================================================
# 7. Span estimator
# =========================================================
def estimate_span_from_episode(lag_list: list[float], horizon: int) -> int:
    if not lag_list:
        return 0
    base = lag_list[-1]
    span = 0
    for v in lag_list[-horizon:]:
        if abs(v - base) < 0.25 * (abs(base) + 1e-3):
            span += 1
    return min(span, horizon)

# =========================================================
# 8. Training loop (per-task, with fresh agent)
# =========================================================
def train_task(task):
    print("\n=== TASK:", task["name"], "(", task["env_id"], ") ===")
    env = gym.make(task["env_id"])
    obs_dim = env.observation_space.shape[0]
    dr_calc = UniversalDR(obs_dim)
    recent_scores = collections.deque(maxlen=12)
    recent_drs = collections.deque(maxlen=12)


    # IMPORTANT: fresh agent per task, with task-appropriate buffer
    if task["name"] == "Ant":
        agent = SpanAwareSAC(
            env,
            span_threshold=task["span_threshold"],
            buffer_size=200_000,
            learning_starts=10_000,
        )
    else:  # Pendulum
        agent = SpanAwareSAC(
            env,
            span_threshold=task["span_threshold"],
            buffer_size=50_000,
            learning_starts=5_000,
        )

    logger = configure(f'./logs_{task["name"]}/', ["stdout", "csv"])
    agent.agent.set_logger(logger)

    # SAFE warmup – only if the buffer is the real thing
    obs, _ = env.reset()
    for _ in range(5000):
        act = env.action_space.sample()
        nxt, _, d, tr, _ = env.step(act)
        if hasattr(agent.agent, "replay_buffer") and isinstance(
            agent.agent.replay_buffer, ReplayBuffer
        ):
            agent.agent.replay_buffer.add(obs, nxt, act, 0.0, d or tr, [{}])
        obs = nxt
        if d or tr:
            obs, _ = env.reset()

    top_scores = []
    snail = None

    for ep in range(1, task["max_episodes"] + 1):
        obs, _ = env.reset()
        done = False
        truncated = False
        prev_obs = None
        prev_dr = dr_calc.calculate(obs)
        ep_steps = 0
        ep_lags = []
        ep_env_return = 0.0
        last_xpos = None  # reset per episode for Ant

        while not done and not truncated:
            act, _ = agent.agent.predict(obs, deterministic=True)
            nxt, env_r, done, truncated, _ = env.step(act)

            # ---- forward progress (Ant) ----
            forward_reward = 0.0
            if task["name"] == "Ant":
                xpos = float(env.unwrapped.get_body_com(ANT_TORSO)[0])
                if last_xpos is None:
                    last_xpos = xpos
                dx = xpos - last_xpos
                last_xpos = xpos
                if dx > 0:
                    forward_reward = task.get("forward_gain", 3.0) * dx

            dr = dr_calc.calculate(nxt, prev_obs)
            dr_d = dr - prev_dr

            pir_r = pirouette_lagrangian(
                dr,
                dr_d,
                task["gamma_coherence"],
                task["beta_duration"],
                task["delta_dissonance"],
            )

            # MIRAGE
            corr_p = task["mirage_base"] + task["mirage_gain"] * dr
            corr_p = min(task["mirage_max"], corr_p)
            if np.random.rand() < corr_p:
                pir_r = np.random.normal(0.0, 0.5)

            reward = (
                task["env_reward_weight"] * env_r
                + task["pirouette_reward_weight"] * pir_r
                + forward_reward
            )

            agent.agent.replay_buffer.add(
                obs, nxt, act, reward, done or truncated, [{}]
            )

            ep_lags.append(pir_r)
            agent.train_step(span=agent.last_span)

            ep_env_return += env_r
            ep_steps += 1
            prev_obs = obs
            obs = nxt
            prev_dr = dr

        # -------------- END OF EPISODE --------------
        span = estimate_span_from_episode(ep_lags, task["horizon"])
        agent.last_span = span

        # basic stats
        base_score = ep_env_return
        base_mean_dr = float(np.mean(np.abs(ep_lags))) if ep_lags else 1.0

        # keep short windows for local growth detection
        recent_scores.append(base_score)
        recent_drs.append(base_mean_dr)

        # 1) detect a “burst” (wound-channel candidate)
        # rule: score must be clearly above local median/mean OR above current anchor
        local_ref = np.median(recent_scores) if len(recent_scores) >= 4 else base_score
        burst = (
            base_score > local_ref * 1.25  # 25% above local pattern
            or base_score > agent.anchor_score * 1.02  # or slightly better than old anchor
        )

        # 2) if it’s a *good* burst, anchor it immediately
        # (for Ant: only anchor positive scores, for Pendulum allow near-zero)
        if burst:
            if task["name"] == "Ant":
                if base_score > 0:  # only anchor genuine forward progress
                    agent.save_anchor(base_score, base_mean_dr, span, ep)
            else:
                # pendulum is often negative; anchor the “least bad” + low DR
                agent.save_anchor(base_score, base_mean_dr, span, ep)

        # 3) snail probing (kept from previous version)
        if snail is None:
            snail = SnailProbeTool(
                sac_wrapper=agent,
                probe_steps=400 if task["name"] == "Ant" else 200,
            )
        if ep % 5 == 0:
            snail.probe(
                env=env,
                task=task,
                span=span,
                max_span=task["horizon"],
                base_score=base_score,
                base_mean_dr=base_mean_dr,
                dr_calc=dr_calc,
            )

        # 4) AGGRESSIVE WOUND-CHANNEL GUARD
        # if we HAVE an anchor, and we’ve fallen way below it for a few episodes → roll back
        if agent.anchor_state is not None:
            far_below = (
                base_score < agent.anchor_score * 0.6
                or base_mean_dr > agent.anchor_dr * 1.35
            )

            if far_below:
                agent.degrade_streak += 1
            else:
                agent.degrade_streak = 0

            if agent.degrade_streak >= 2 and ep > agent.anchor_ep + 3:
                print(
                    f"  [anchor] episode {ep} degraded twice "
                    f"(score={base_score:.1f} vs anchor={agent.anchor_score:.1f}) → rollback"
                )
                agent.restore_anchor()
                agent.degrade_streak = 0

                # after restore, we can also trim replay a bit if you like
                # e.g. to prevent the bad episode from dominating:
                # agent.agent.replay_buffer.pos = max(0, agent.agent.replay_buffer.pos - 512)

        # 5) keep your existing agent rollback if you want:
        # agent.rollback_if_needed(span)

        # 6) TOP 15 by ENV REWARD (your earlier request)
        top_scores.append(base_score)
        top_scores.sort(reverse=True)
        top_scores = top_scores[:15]
        avg_top = sum(top_scores) / len(top_scores)

        print(
            f"Ep {ep:04d} | Steps={ep_steps:4d} | EnvR={base_score:8.1f} | "
            f"Span={span:2d}/{task['horizon']} | Top15={avg_top:7.1f}"
        )

        # 7) task-specific exit
        if task["name"] == "Pendulum" and base_score >= task["pendulum_mastery"]:
            print("Pendulum mastered → moving on.")
            break


    env.close()

# =========================================================
# 9. main
# =========================================================
if __name__ == "__main__":
    train_task(TASKS[0])  # Pendulum
    train_task(TASKS[1])  # Ant
