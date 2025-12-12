#!/usr/bin/env python3
"""
Wendigo-Minimalist (Pirouette Closure Edition)

Goal:
- keep your pirouette reward (coherence gain + duration - dissonance)
- classify each transition into Weaver / Gladiator / Vortex / Drifter
- bias learning toward Weaver/Gladiator transitions
- optional closure-style exploration pattern

Refactored with "Advanced Pirouette Agent" concepts:
- Decoupled environment reward and shaped reward.
- Normalized, scale-insensitive Dark Residue (log1p + EMA).
- Relative classifier to prevent buffer flooding.
"""

import gymnasium as gym
import numpy as np
from collections import deque
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure

ENV_ID = "LunarLanderContinuous-v3"

# ---------------------------------------------------------------------
# 1. New Pirouette Reward & Classification Components
# ---------------------------------------------------------------------

class RunningStat:
    """Helper class for Exponential Moving Average (EMA)"""
    def __init__(self, beta=0.01, eps=1e-6):
        self.beta = beta
        self.value = None
        self.eps = eps

    def update(self, x: float) -> float:
        if self.value is None:
            self.value = float(x)
        else:
            self.value = (1 - self.beta) * self.value + self.beta * float(x)
        return self.value

    def get(self) -> float:
        return self.value if self.value is not None else 1.0

def dark_residue_generic(obs: np.ndarray) -> float:
    """Scale-insensitive dark residue using log(1+|x|)"""
    obs = np.asarray(obs, dtype=np.float32)
    # scale-insensitive: log(1+|x|)
    x = np.log1p(np.abs(obs))
    # emphasize early dims a bit
    w = np.linspace(1.2, 0.8, num=obs.shape[0], dtype=np.float32)
    return float(np.sum(x * w) / obs.shape[0])

class PirouetteRewardShaper:
    """
    Calculates a blended reward from env reward, closure gain (coherence),
    and a normalized residue (dissonance) tax.
    """
    def __init__(self, w_env=1.0, w_closure=0.8, w_residue=0.5):
        self.w_env = w_env
        self.w_closure = w_closure
        self.w_residue = w_residue
        self.dr_stat = RunningStat(beta=0.01) # EMA for Dark Residue

    def shape(self, env_reward: float, obs: np.ndarray, next_obs: np.ndarray) -> tuple[float, float, float, float]:
        dr_cur = dark_residue_generic(next_obs)
        # Update EMA and get the reference (typical) DR
        dr_ref = self.dr_stat.update(dr_cur)
        # Normalize current DR against the typical value
        dr_norm = dr_cur / (dr_ref + 1e-6)

        dr_prev = dark_residue_generic(obs)
        delta_dr = dr_cur - dr_prev  # + = worse (more residue), - = better

        # Closure gain is from *improving* coherence (reducing residue)
        closure_gain = max(0.0, -delta_dr)
        # Normalize closure gain to keep it bounded
        closure_gain = np.tanh(closure_gain)

        shaped = (
            self.w_env * env_reward            # 1. Task reward
            + self.w_closure * closure_gain   # 2. Coherence bonus
            - self.w_residue * dr_norm        # 3. Dissonance tax
        )
        return shaped, dr_norm, delta_dr, dr_ref

class PirouetteModeClassifier:
    """Classifies transitions based on *relative* DR and *relative* dDR."""
    def __init__(self):
        # EMA for the *magnitude* of delta_dr
        self.ddr_stat = RunningStat(beta=0.01)

    def classify(self, dr_norm: float, delta_dr: float) -> str:
        # Normalize delta_dr by its typical magnitude
        dref = self.ddr_stat.update(abs(delta_dr))
        if dref < 1e-6:
            dref = 1e-6
        rel_ddr = delta_dr / dref # relative change in residue

        # Thresholds are now based on relative, normalized values
        # small dr_norm means we're in a good coherent pocket
        if rel_ddr < -0.8 and dr_norm < 1.1:
            return "Weaver" # Big improvement, already in good state
        if rel_ddr < -0.4 and dr_norm < 1.3:
            return "Gladiator" # Good improvement
        if rel_ddr > 1.0 and dr_norm > 1.4:
            return "Vortex" # Getting much worse, in a bad state
        return "Drifter"


# ---------------------------------------------------------------------
# 2. Action wrapper (same as your minimalist)
# ---------------------------------------------------------------------
class DiscreteToBoxActionWrapper(gym.ActionWrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

    def action(self, action: np.ndarray) -> int:
        return 0 if action[0] < 0.0 else 1


# ---------------------------------------------------------------------
# 3. Optional closure-sig exploration
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
# 4. Main training loop (Refactored)
# ---------------------------------------------------------------------
def main():
    env = gym.make(ENV_ID)
    agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))
    agent.set_logger(configure(None, ["stdout"]))

    # --- Instantiate New Pirouette Components ---
    # Use suggested weights to balance task reward and closure reward
    shaper = PirouetteRewardShaper(
        w_env=1.0,      # Keep the task visible
        w_closure=0.6,  # Let closure help
        w_residue=0.3   # Residue is a tax, not a hammer
    )
    classifier = PirouetteModeClassifier()

    # --- Buffers ---
    weaver_buf = deque(maxlen=15_000) # Per your experiment
    general_buf = deque(maxlen=5_000) # Per your experiment

    explorer = ClosureExplorer(act_dim=env.action_space.shape[0])

    # --- Warm-up (Unchanged) ---
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
        
        # We track env_score for performance, shaped_score for interest
        ep_env_score = 0.0
        ep_shaped_score = 0.0
        # No more prev_dr needed here

        while not (done or truncated):
            base_action, _ = agent.predict(obs, deterministic=True)
            action = explorer.sample(base_action, eps=0.05)

            # --- Capture Environment Reward ---
            nxt, env_reward, done, truncated, info = env.step(action)

            # --- New Reward Shaping & Classification ---
            shaped_r, dr_norm, delta_dr, dr_ref = shaper.shape(env_reward, obs, nxt)
            mode = classifier.classify(dr_norm, delta_dr)

            # --- Agent Training (uses SHAPED reward) ---
            agent.replay_buffer.add(obs, nxt, action, shaped_r, done, [info])
            agent.train(gradient_steps=1)

            # --- Buffer Logic (uses SHAPED reward) ---
            transition = (obs.copy(), nxt.copy(), action.copy(), shaped_r, done)
            
            # Only stash "good-ish" stuff, preventing negative swamp
            simple_threshold = -5.0 
            
            if shaped_r > simple_threshold:
                general_buf.append(transition)

            if mode in ("Weaver", "Gladiator") and shaped_r > simple_threshold:
                weaver_buf.append(transition)
            
            # --- Oversampling Loop (Unchanged, uses SHAPED reward from buffer) ---
            if len(weaver_buf) > 16:
                for _ in range(2):
                    # 'r' here is the shaped_r we stored in the transition
                    o, no, a, r, d = weaver_buf[np.random.randint(0, len(weaver_buf))]
                    agent.replay_buffer.add(o, no, a, r, d, [{}])
                    agent.train(gradient_steps=1)

            # --- State Update & Score Tracking ---
            obs = nxt
            ep_env_score += env_reward      # Track true task score
            ep_shaped_score += shaped_r   # Track agent's perceived score
            
        # --- Logging (tracks ENV score) ---
        top_scores.append(ep_env_score) # Use env_score for "true" performance
        top_scores.sort(reverse=True)
        top_scores = top_scores[:15]
        avg_top = sum(top_scores) / len(top_scores)
        
        print(f"Episode {ep:03d}: EnvScore={ep_env_score:7.2f} | ShapedScore={ep_shaped_score:7.2f} | Top-15 Env={avg_top:7.2f} | WeaverBuf={len(weaver_buf):4d}")

    env.close()

if __name__ == "__main__":
    main()