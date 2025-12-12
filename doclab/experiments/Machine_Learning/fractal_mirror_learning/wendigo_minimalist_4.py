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


# ---------------------------------------------------------------------
# 1. Dark Residue, as in your minimalist script
# ---------------------------------------------------------------------
def calculate_dark_residue(obs: np.ndarray) -> float:
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    return (
        0.4 * abs(cart_pos)
        + 0.2 * abs(cart_vel)
        + 1.5 * abs(pole_angle)
        + 0.3 * abs(pole_vel)
    )


# ---------------------------------------------------------------------
# 2. Pirouette 4-mode classifier (Gym version)
#    We approximate SoS logic with {DR, dDR} only.
# ---------------------------------------------------------------------
def classify_pirouette_mode(dr: float, ddr: float) -> str:
    """
    Weaver:     dDR < 0 and dr small         -> we're closing
    Gladiator:  dDR < 0 and dr large         -> closing under stress
    Vortex:     dDR > 0 and dr large         -> leaking / turbulence
    Drifter:    else
    thresholds tuned for CartPole scale
    """
    DR_SMALL = 0.15
    DR_LARGE = 0.35

    if ddr < 0.0:  # moving toward closure
        if dr <= DR_SMALL:
            return "Weaver"
        else:
            return "Gladiator"
    else:  # ddr >= 0, residue not decreasing
        if dr >= DR_LARGE:
            return "Vortex"
        else:
            return "Drifter"


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
    def __init__(self):
        self.step_idx = 0

    def sample(self, base_action: np.ndarray, eps: float = 0.15) -> np.ndarray:
        """
        every 4 steps we change the bias, but stay close to base_action
        """
        mode = self.step_idx % 4
        self.step_idx += 1

        a = float(base_action[0])

        if mode == 0:      # Weaver -> gentle toward center
            a = a * 0.5
        elif mode == 1:    # Gladiator -> push harder
            a = np.clip(a + 0.4, -1.0, 1.0)
        elif mode == 2:    # Vortex -> destabilize (flip sign slightly)
            a = np.clip(-a + 0.2, -1.0, 1.0)
        else:              # Drifter -> leave it
            a = a

        # small gaussian to make it not too obvious
        a = a + np.random.normal(0.0, eps)
        return np.array([np.clip(a, -1.0, 1.0)], dtype=np.float32)


# ---------------------------------------------------------------------
# 5. Main training loop
# ---------------------------------------------------------------------
def main():
    env = DiscreteToBoxActionWrapper(gym.make("CartPole-v1"))
    agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))

    new_logger = configure(None, ["stdout"])
    agent.set_logger(new_logger)

    # Pirouette reward hyperparams (same as your minimalist)
    gamma_coherence = 1.5
    beta_duration = 0.05
    delta_dissonance = 1.0

    # NEW: pirouette buffers
    weaver_buf = deque(maxlen=5_000)   # high-value transitions
    general_buf = deque(maxlen=20_000) # everything

    # NEW: closure-style explorer
    explorer = ClosureExplorer()

    REPLAY_WARMUP_STEPS = 10_000
    print(f"--- Pre-populating replay buffer with {REPLAY_WARMUP_STEPS} random steps... ---")
    obs, _ = env.reset()
    for _ in range(REPLAY_WARMUP_STEPS):
        random_action = env.action_space.sample()
        next_obs, _, done, truncated, _ = env.step(random_action)
        agent.replay_buffer.add(obs, next_obs, np.array([random_action]), 0.0, done, [{}])
        obs = next_obs
        if done or truncated:
            obs, _ = env.reset()
    print("--- Warm-up complete. Starting training. ---")

    top_scores = []
    num_episodes = 500

    for ep in range(1, num_episodes + 1):
        obs, _ = env.reset()
        done, truncated = False, False
        score = 0

        prev_dr = calculate_dark_residue(obs)

        while not done and not truncated:
            # --- policy action ---
            base_action, _ = agent.predict(obs, deterministic=True)

            # --- closure exploration (small) ---
            action = explorer.sample(base_action, eps=0.05)

            # --- env step ---
            next_obs, _, done, truncated, _ = env.step(action)

            # --- pirouette reward ---
            cur_dr = calculate_dark_residue(next_obs)
            ddr = cur_dr - prev_dr

            coherence_gain = gamma_coherence * max(0.0, -ddr)
            dissonance_penalty = delta_dissonance * cur_dr
            reward = coherence_gain + beta_duration - dissonance_penalty

            # --- classify mode (this is our "weaver finder") ---
            mode = classify_pirouette_mode(cur_dr, ddr)

            # --- standard SAC train step ---
            agent.replay_buffer.add(obs, next_obs, action, reward, done, [{}])
            agent.train(gradient_steps=1)

            # --- stash transition for pirouette replay ---
            transition = (obs.copy(), next_obs.copy(), action.copy(), reward, done)
            general_buf.append(transition)
            if mode in ("Weaver", "Gladiator"):
                weaver_buf.append(transition)

            # --- extra gradient steps from good stuff ---
            if len(weaver_buf) > 16:
                # train more from high-value windows
                for _ in range(2):  # small, but noticeable
                    o, no, a, r, d = weaver_buf[np.random.randint(0, len(weaver_buf))]
                    agent.replay_buffer.add(o, no, a, r, d, [{}])
                    agent.train(gradient_steps=1)

            obs = next_obs
            prev_dr = cur_dr
            score += 1

        # --- episode end ---
        top_scores.append(score)
        top_scores.sort(reverse=True)
        top_scores = top_scores[:15]
        avg_top = sum(top_scores) / len(top_scores)

        print(
            f"Episode {ep:03d}: "
            f"Score={score:3d} | "
            f"Top-15 Avg={avg_top:6.2f} | "
            f"WeaverBuf={len(weaver_buf):4d} | "
            f"GeneralBuf={len(general_buf):5d}"
        )

        MASTERY_THRESHOLD = 495
        if len(top_scores) == 15 and avg_top >= MASTERY_THRESHOLD:
            print("\n*** PIRouette-Only MASTERY ACHIEVED ***")
            agent.save("wendigo_pirouette_closure_mastery.zip")
            break

    env.close()
    print("--- Training Complete ---")


if __name__ == "__main__":
    main()
