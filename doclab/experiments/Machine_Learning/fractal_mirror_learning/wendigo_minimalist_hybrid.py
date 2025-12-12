#!/usr/bin/env python3
"""
Wendigo-Minimalist (Pirouette Closure Edition)

Goal:
- keep your pirouette reward (coherence gain + duration - dissonance)
- classify each transition into Weaver / Gladiator / Vortex / Drifter
- bias learning toward Weaver/Gladiator transitions
- optional closure-style exploration pattern

Based on:
- wendigo_geodesic_sac.py (gallery + RPA + geodesic)  <-- for the idea
- wendigo_minimalist.py (clean SAC + pirouette reward) <-- for the shape
"""

import gymnasium as gym
import numpy as np
from collections import deque
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure

ENV_ID = "LunarLanderContinuous-v3"

def calculate_dark_residue(obs: np.ndarray) -> float:
    """
    Generic dark residue:
    - punish large position/angle-ish values harder
    - punish velocity-ish values a bit
    Works for obs of length >= 1
    """
    obs = np.asarray(obs, dtype=np.float32)
    # heuristic: bigger magnitude → more residue
    # weight position-like dims a bit more
    base = np.abs(obs)

    # you can bias early dims (usually pos/angle) heavier
    weights = np.linspace(1.5, 0.5, num=base.shape[0])
    return float(np.sum(base * weights) / base.shape[0])


def classify_pirouette_mode(dr: float, ddr: float) -> str:
    DR_SMALL = 0.25 * max(1.0, dr)
    DR_LARGE = 0.6 * max(1.0, dr)
    if ddr < 0.0:
        return "Weaver" if dr <= DR_SMALL else "Gladiator"
    else:
        return "Vortex" if dr >= DR_LARGE else "Drifter"


# ---------------------------------------------------------------------
# 3. Action wrapper (same as your minimalist)
# ---------------------------------------------------------------------
class DiscreteToBoxActionWrapper(gym.ActionWrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

    def action(self, action: np.ndarray) -> int:
        return 0 if action[0] < 0.0 else 1


# ---------------------------------------------------------------------
# 4. Optional closure-sig exploration
#    tiny 4-step pattern: W->G->V->D in action-space
# ---------------------------------------------------------------------
class ClosureExplorer:
    def __init__(self, act_dim: int):
        self.step_idx = 0
        self.act_dim = act_dim

    def sample(self, base_action: np.ndarray, eps: float = 0.05) -> np.ndarray:
        mode = self.step_idx % 4
        self.step_idx += 1

        a = base_action.astype(np.float32).copy()
        if mode == 0:
            a *= 0.5
        elif mode == 1:
            a = np.clip(a + 0.4, -1.0, 1.0)
        elif mode == 2:
            a = np.clip(-a + 0.2, -1.0, 1.0)

        a = a + np.random.normal(0.0, eps, size=self.act_dim)
        return np.clip(a, -1.0, 1.0).astype(np.float32)


# ---------------------------------------------------------------------
# 5. Main training loop
# ---------------------------------------------------------------------
def main():
    env = gym.make(ENV_ID)
    agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))
    agent.set_logger(configure(None, ["stdout"]))

    gamma_coherence = 1.5
    beta_duration = 0.05
    delta_dissonance = 1.0

    weaver_buf = deque(maxlen=5_000)
    general_buf = deque(maxlen=20_000)

    explorer = ClosureExplorer(act_dim=env.action_space.shape[0])

    REPLAY_WARMUP_STEPS = 10_000
    obs, _ = env.reset()
    print(f"--- Pre-populating replay buffer with {REPLAY_WARMUP_STEPS} random steps... ---")
    for _ in range(REPLAY_WARMUP_STEPS):
        ra = env.action_space.sample()
        nxt, _, done, truncated, _ = env.step(ra)
        agent.replay_buffer.add(obs, nxt, ra, 0.0, done, [{}])
        obs = nxt
        if done or truncated:
            obs, _ = env.reset()
    print("--- Warm-up complete. Starting training. ---")

    top_scores = []
    num_episodes = 500

    for ep in range(1, num_episodes + 1):
        obs, _ = env.reset()
        done = truncated = False
        score = 0.0
        prev_dr = calculate_dark_residue(obs)

        while not (done or truncated):
            base_action, _ = agent.predict(obs, deterministic=True)
            action = explorer.sample(base_action, eps=0.05)

            nxt, _, done, truncated, info = env.step(action)

            cur_dr = calculate_dark_residue(nxt)
            ddr = cur_dr - prev_dr

            coherence_gain = gamma_coherence * max(0.0, -ddr)
            dissonance_penalty = delta_dissonance * cur_dr
            reward = coherence_gain + beta_duration - dissonance_penalty

            agent.replay_buffer.add(obs, nxt, action, reward, done, [info])
            agent.train(gradient_steps=1)

            transition = (obs.copy(), nxt.copy(), action.copy(), reward, done)
            general_buf.append(transition)
            mode = classify_pirouette_mode(cur_dr, ddr)
            if mode in ("Weaver", "Gladiator"):
                weaver_buf.append(transition)
            if len(weaver_buf) > 16:
                for _ in range(2):
                    o, no, a, r, d = weaver_buf[np.random.randint(0, len(weaver_buf))]
                    agent.replay_buffer.add(o, no, a, r, d, [{}])
                    agent.train(gradient_steps=1)

            obs = nxt
            prev_dr = cur_dr
            score += reward  # for Lunar this is more meaningful than steps

        top_scores.append(score)
        top_scores.sort(reverse=True)
        top_scores = top_scores[:15]
        avg_top = sum(top_scores) / len(top_scores)
        print(f"Episode {ep:03d}: Score={score:7.2f} | Top-15 Avg={avg_top:7.2f} | WeaverBuf={len(weaver_buf):4d} | GeneralBuf={len(general_buf):5d}")

    env.close()

if __name__ == "__main__":
    main()
