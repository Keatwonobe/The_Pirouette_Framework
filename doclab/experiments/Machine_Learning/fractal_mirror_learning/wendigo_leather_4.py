#!/usr/bin/env python3
import gymnasium as gym
import numpy as np
import copy
import torch
import os, time
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure

# =========================================================
# 1. TASK CONFIG – Ant-first, Pendulum as warmup
# =========================================================
TASKS = [
    {
        "name": "Pendulum",
        "env_id": "Pendulum-v1",
        "is_discrete": False,
        "max_episodes": 80,
        # pendulum "mastery" in your terms = return <= -40
        "pendulum_mastery": -40.0,
        # pirouette weights (heavier pressure -> faster centering)
        "gamma_coherence": 1.2,
        "beta_duration": 0.1,
        "delta_dissonance": 0.25,
        # mirage
        "mirage_base": 0.03,
        "mirage_gain": 0.6,
        "mirage_max": 0.35,
        "horizon": 8,
        "span_threshold": 3,
        # blend: pendulum doesn’t really need env reward
        "env_reward_weight": 0.15,
        "pirouette_reward_weight": 0.85,
    },
    {
        "name": "Ant",
        "env_id": "Ant-v5",
        "is_discrete": False,
        "max_episodes": 1200,
        # pirouette weights for locomotion
        # lower delta_dissonance so DR doesn’t kill forward motion
        "gamma_coherence": 1.0,
        "beta_duration": 0.5,
        "delta_dissonance": 0.15,
        # mirage tuned lower gain -> Ant DR will be bigger
        "mirage_base": 0.05,
        "mirage_gain": 0.4,
        "mirage_max": 0.35,
        "horizon": 12,
        "span_threshold": 4,
        # KEY: we let Ant’s native reward speak
        "env_reward_weight": 0.35,
        "pirouette_reward_weight": 0.65,
    },
    # you can add Humanoid here after Ant
]

# =========================================================
# 2. Universal DR (same idea as leather_3)
# =========================================================
from collections import deque
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

        # normalize deviation
        base = 0.3 * np.sum(np.abs(obs / self.scale)) / self.obs_dim

        if prev is not None:
            vel = np.linalg.norm((obs - prev) / self.scale)
        else:
            vel = 0.0

        dr = base + 0.7 * vel
        return max(0.01, float(dr))

# =========================================================
# 3. Pirouette Lagrangian (same math)
# =========================================================
def pirouette_lagrangian(dr, dr_d, gamma, beta, delta):
    coh = gamma * max(0.0, -dr_d)   # reward for reducing DR
    press = delta * dr              # penalty for being in DR
    L = coh + beta - press
    return float(np.clip(L, -20.0, 20.0))

# =========================================================
# 4. Span-aware SAC wrapper (simplified from leather_3)
# =========================================================
from collections import deque
import copy

class SpanAwareSAC:
    def __init__(self, env, span_threshold: int = 4):
        self.env = env
        self.agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))
        self.span_threshold = span_threshold
        self.base_lr = 3e-4
        self.last_span = 0
        self.recent_rewards = deque(maxlen=50)
        self.checkpoints = []

    def train_step(self, span: int):
        # modulate learning rate when blind
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

        # restore
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
        # simple rule: span collapses to 0 → rollback
        if span == 0 and self.checkpoints:
            best = max(self.checkpoints, key=lambda x: x[1])
            ep, sp, st = best
            print(f"  ! rollback → episode {ep} (span={sp})")
            self.agent.policy.actor.load_state_dict(st)

class SnailProbeTool:
    """
    Wendigo 'poke-and-go' weight explorer.

    - decides how BIG the change is (fraction of params, noise scale)
    - applies it to ACTOR only
    - evaluates
    - reverts if it did bad
    """
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
        self.sacw = sac_wrapper  # SpanAwareSAC
        self.max_frac = max_frac
        self.min_frac = min_frac
        self.base_noise = base_noise
        self.max_noise = max_noise
        self.probe_steps = probe_steps
        self.score_slack = score_slack  # allow small score drops if DR is nicer

        # where we park the actor when we poke
        self._saved_actor_state = None

    def _pick_probe_size(self, span: int, max_span: int, mean_dr: float):
        """
        span low + dr high  -> big move
        span high + dr low  -> small move
        """
        span_ratio = 0.0 if max_span == 0 else min(1.0, span / max_span)
        # DR is unbounded-ish, just squash
        dr_ratio = 1.0 - np.exp(-3.0 * float(mean_dr))  # 0 -> 1

        # more unstable -> larger fraction
        frac = (
            self.min_frac
            + (self.max_frac - self.min_frac) * (1.0 - 0.5 * span_ratio + 0.5 * dr_ratio)
        )
        frac = float(np.clip(frac, self.min_frac, self.max_frac))

        # noise stronger when DR is stronger
        noise = self.base_noise + (self.max_noise - self.base_noise) * dr_ratio
        return frac, float(noise)

    def _get_actor_params(self):
        return list(self.sacw.agent.policy.actor.parameters())

    def _select_param_indices(self, params, fraction: float):
        # flatten into a list of (tensor, idx_tuple)
        flat = []
        for p in params:
            if not p.requires_grad:
                continue
            flat.append(p)
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
        span: int,
        max_span: int,
        base_score: float,
        base_mean_dr: float,
        dr_calc,
    ):
        """
        do 1 poke:
        - save
        - perturb subset
        - evaluate
        - accept/reject
        """
        self._save_actor()

        frac, noise = self._pick_probe_size(span, max_span, base_mean_dr)

        params = self._get_actor_params()
        chosen = self._select_param_indices(params, frac)
        self._apply_noise(chosen, noise)

        probe_score, probe_mean_dr = evaluate_policy_once(
            env,
            self.sacw.agent,
            dr_calc,
            max_steps=self.probe_steps,
        )

        # acceptance: better score OR (not much worse + better DR)
        score_ok = probe_score >= base_score * (1.0 - self.score_slack)
        dr_ok = probe_mean_dr <= base_mean_dr * 0.95

        if score_ok or dr_ok:
            # keep probe
            print(
                f"  [snail] accepted probe: frac={frac:.3f}, noise={noise:.3f}, "
                f"score={probe_score:.1f} (base={base_score:.1f}), "
                f"DR={probe_mean_dr:.3f} (base={base_mean_dr:.3f})"
            )
            self._saved_actor_state = None
        else:
            # rollback
            print(
                f"  [snail] rejected probe: frac={frac:.3f}, noise={noise:.3f}, "
                f"score={probe_score:.1f} < base={base_score:.1f}"
            )
            self._restore_actor()

def evaluate_policy_once(env, agent, dr_calc, max_steps=800):
    obs, _ = env.reset()
    done = False
    truncated = False
    steps = 0
    total_reward = 0.0
    dr_vals = []
    prev_obs = None
    while not done and not truncated and steps < max_steps:
        act, _ = agent.predict(obs, deterministic=True)
        nxt, env_r, done, truncated, _ = env.step(act)
        dr = dr_calc.calculate(nxt, prev_obs)
        dr_vals.append(dr)
        total_reward += env_r
        prev_obs = obs
        obs = nxt
        steps += 1
    mean_dr = float(np.mean(dr_vals)) if dr_vals else 1.0
    return total_reward, mean_dr


# =========================================================
# 5. Lagrangian “prophet” stub (for now we can treat span as len(ep))
#    You can plug your real prophet from leather_3 if you want 1:1 parity.
# =========================================================
def estimate_span_from_episode(lag_list: list[float], horizon: int) -> int:
    # cheap stand-in: how many future steps stay within ±0.25 of last val
    if not lag_list:
        return 0
    base = lag_list[-1]
    span = 0
    for v in lag_list[-horizon:]:
        if abs(v - base) < 0.25 * (abs(base) + 1e-3):
            span += 1
    return min(span, horizon)

# =========================================================
# 6. Training loop (Ant-first)
# =========================================================
def train_task(task):
    print("\n=== TASK:", task["name"], "(", task["env_id"], ") ===")
    env = gym.make(task["env_id"])
    obs_dim = env.observation_space.shape[0]
    dr_calc = UniversalDR(obs_dim)
    agent = SpanAwareSAC(env, span_threshold=task["span_threshold"])

    logger = configure(f'./logs_{task["name"]}/', ["stdout", "csv"])
    agent.agent.set_logger(logger)

    # warmup
    obs, _ = env.reset()
    for _ in range(5000):
        act = env.action_space.sample()
        nxt, _, d, tr, _ = env.step(act)
        agent.agent.replay_buffer.add(obs, nxt, act, 0.0, d or tr, [{}])
        obs = nxt
        if d or tr:
            obs, _ = env.reset()

    top_scores = []
    for ep in range(1, task["max_episodes"] + 1):
        obs, _ = env.reset()
        done = False
        truncated = False
        prev_obs = None
        prev_dr = dr_calc.calculate(obs)
        ep_score = 0
        ep_lags = []
        ep_reward_true = 0.0

        while not done and not truncated:
            act, _ = agent.agent.predict(obs, deterministic=True)
            nxt, env_r, done, truncated, _ = env.step(act)

            dr = dr_calc.calculate(nxt, prev_obs)
            dr_d = dr - prev_dr

            pir_r = pirouette_lagrangian(
                dr,
                dr_d,
                task["gamma_coherence"],
                task["beta_duration"],
                task["delta_dissonance"],
            )

            # MIRAGE: corruption tied to DR
            corr_p = task["mirage_base"] + task["mirage_gain"] * dr
            if corr_p > task["mirage_max"]:
                corr_p = task["mirage_max"]
            if np.random.rand() < corr_p:
                pir_r = np.random.normal(0.0, 0.5)

            # blend env + pirouette (THIS is the Ant fix)
            reward = (
                task["env_reward_weight"] * env_r
                + task["pirouette_reward_weight"] * pir_r
            )

            agent.agent.replay_buffer.add(
                obs, nxt, act, reward, done or truncated, [{}]
            )
            ep_lags.append(pir_r)

            # span-aware train
            # span will be set after episode, but we can use last known for now
            agent.train_step(span=agent.last_span)

            ep_reward_true += env_r
            ep_score += 1
            prev_obs = obs
            obs = nxt
            prev_dr = dr

        # episode done → compute span on clean trail
        span = estimate_span_from_episode(ep_lags, task["horizon"])
        agent.last_span = span

        # measure baseline from THIS episode
        base_score = ep_score
        base_mean_dr = np.mean([abs(x) for x in ep_lags]) if ep_lags else 1.0

        # lazy-create tool (one per task)
        if ep == 1:
            snail = SnailProbeTool(
                sac_wrapper=agent,
                probe_steps=400 if task["name"] == "Ant" else 200,
            )

        # every few episodes, poke
        if ep % 5 == 0:
            snail.probe(
                env=env,
                span=span,
                max_span=task["horizon"],
                base_score=base_score,
                base_mean_dr=base_mean_dr,
                dr_calc=dr_calc,
            )

        agent.last_span = span

        # checkpoint every 10
        if ep % 10 == 0:
            agent.checkpoint(ep, span)

        # rollback if span collapsed
        agent.rollback_if_needed(span)

        top_scores.append(ep_score)
        top_scores.sort(reverse=True)
        top_scores = top_scores[:15]
        avg_top = sum(top_scores) / len(top_scores)

        print(
            f"Ep {ep:04d} | Steps={ep_score:4d} | EnvR={ep_reward_true:8.1f} | "
            f"Span={span:2d}/{task['horizon']} | Top15={avg_top:7.1f}"
        )

        # optional: your pendulum mastery check
        if task["name"] == "Pendulum" and ep_reward_true >= task["pendulum_mastery"]:
            print("Pendulum mastered → moving on.")
            break

    env.close()

if __name__ == "__main__":
    # warmup with Pendulum (since you said it solves in 3 encounters)
    train_task(TASKS[0])
    # then Ant
    train_task(TASKS[1])
