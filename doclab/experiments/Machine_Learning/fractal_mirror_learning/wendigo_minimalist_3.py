#!/usr/bin/env python3
"""
Wendigo-Minimalist v7: Pirouette SAC + Predictive Span
------------------------------------------------------
Adds a tiny "prophet" that tries to predict the next H Dark-Residue values
from the current observation. After every episode we train it on what the
episode actually did and log a predictive span σ in the same style as the
Pirouette FIT trainer.  (cf. Prophet.measure_predictive_span) :contentReference[oaicite:3]{index=3}
"""

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure

# -----------------------------------------------------------
# 1. Wendigo's DR, same as before
# -----------------------------------------------------------
def calculate_dark_residue(obs: np.ndarray) -> float:
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    return 0.4 * abs(cart_pos) + 0.2 * abs(cart_vel) + 1.5 * abs(pole_angle) + 0.3 * abs(pole_vel)

# -----------------------------------------------------------
# 2. Tiny DR-Prophet (predicts a *vector* of future DRs)
#    patterned after the Prophet in pirouette_fit_trainer_2.py :contentReference[oaicite:4]{index=4}
# -----------------------------------------------------------

def measure_hybrid_span(prophet, x, y, rel_err=0.25, abs_err=0.05):
    import numpy as np
    x_t = torch.tensor(x, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        pred = prophet.net(x_t).squeeze(0).numpy()
    span = 0
    for i in range(len(y)):
        e = abs(pred[i] - y[i])
        if e <= abs_err or e <= rel_err * (abs(y[i]) + 1e-6):
            span += 1
        else:
            break
    return span


class DRProphet(nn.Module):
    def __init__(self, obs_dim: int, horizon: int = 20, lr: float = 1e-3):
        super().__init__()
        self.horizon = horizon
        self.net = nn.Sequential(
            nn.Linear(obs_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, horizon),
        )
        self.opt = optim.Adam(self.parameters(), lr=lr)
        self.loss_fn = nn.L1Loss()  # robust to episode noise
        self.last_span = 0

    def train_step(self, x: np.ndarray, y: np.ndarray):
        """
        x: (obs_dim,)
        y: (horizon,)
        """
        x_t = torch.tensor(x, dtype=torch.float32).unsqueeze(0)
        y_t = torch.tensor(y, dtype=torch.float32).unsqueeze(0)
        pred = self.net(x_t)
        loss = self.loss_fn(pred, y_t)
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()

    def measure_predictive_span(self, x: np.ndarray, y: np.ndarray, rel_err_thresh: float = 0.1) -> int:
        """
        Return how many steps ahead we can predict before relative error blows up.
        Matches the spirit of measure_predictive_span(...) in the FIT trainer. :contentReference[oaicite:5]{index=5}
        """
        x_t = torch.tensor(x, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            pred = self.net(x_t).squeeze(0).numpy()

        # relative error per step
        eps = 1e-6
        rel_err = np.abs(pred - y) / (np.abs(y) + eps)

        span = 0
        for i in range(len(y)):
            if rel_err[i] <= rel_err_thresh:
                span += 1
            else:
                break

        self.last_span = span
        return span

# -----------------------------------------------------------
# 3. Discrete→Box wrapper for CartPole (same as your v6) :contentReference[oaicite:6]{index=6}
# -----------------------------------------------------------
class DiscreteToBoxActionWrapper(gym.ActionWrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

    def action(self, action: np.ndarray) -> int:
        return 0 if action[0] < 0.0 else 1

# -----------------------------------------------------------
# 4. Main Wendigo
# -----------------------------------------------------------
def main():
    env = DiscreteToBoxActionWrapper(gym.make("CartPole-v1"))
    agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))

    # logger
    new_logger = configure(None, ["stdout"])
    agent.set_logger(new_logger)

    # Pirouette reward weights
    gamma_coherence = 1.5   # reward for reducing DR
    beta_duration   = 0.05  # survival bonus
    delta_dissonance = 1.0  # penalty on current DR

    # Predictive span module
    obs_dim = env.observation_space.shape[0]
    SPAN_HORIZON = 20
    prophet = DRProphet(obs_dim, horizon=SPAN_HORIZON, lr=1e-3)

    REPLAY_WARMUP_STEPS = 10000
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
    last_sigma = 0  # to measure Δσ if we want to reward it

    for ep in range(1, num_episodes + 1):
        obs, _ = env.reset()
        done, truncated = False, False
        score = 0
        previous_dr = calculate_dark_residue(obs)

        # for prophet training
        ep_obs = []
        ep_dr = []

        while not done and not truncated:
            action, _ = agent.predict(obs, deterministic=True)
            next_obs, _, done, truncated, _ = env.step(action)

            current_dr = calculate_dark_residue(next_obs)
            DR_SCALE = 5.0  # makes tiny DR visible to prophet
            current_dr_scaled = current_dr * DR_SCALE
            dr_derivative = current_dr - previous_dr

            # 1. reward for active coherence
            coherence_gain = gamma_coherence * max(0, -dr_derivative)
            # 2. state penalty
            dissonance_penalty = delta_dissonance * current_dr
            # 3. base reward
            reward = coherence_gain + beta_duration - dissonance_penalty

            # (optional) reward for improving predictive span
            # reward += 0.0 * (last_sigma)  # leave off for now

            previous_dr = current_dr

            # store in replay
            agent.replay_buffer.add(obs, next_obs, action, reward, done, [{}])
            agent.train(gradient_steps=1)

            # store for prophet
            ep_obs.append(obs.copy())
            ep_dr.append(current_dr_scaled)

            obs = next_obs
            score += 1

        # ---------------------------------------------------
        # after episode: train prophet on this trajectory
        # ---------------------------------------------------
        SPH = SPAN_HORIZON
        MAX_CORRUPT = 0.55     # at worst 70% of the future is TV snow
        BASE_CORR   = 0.03    # even perfect balance gets a little snow
        GAIN_CORR   = 1.2     # how hard DR pumps noise

        epi_len = len(ep_obs)
        if epi_len > 2:
            # we only ever recorded one DR stream: ep_dr
            # treat that as the CLEAN stream
            ep_dr_clean = ep_dr  # <-- this is the missing line

            for t in range(epi_len - 1):
                x = ep_obs[t]

                # 1) build CLEAN future from ep_dr_clean
                future_clean = []
                for k in range(1, SPH + 1):
                    idx = t + k
                    if idx < len(ep_dr_clean):
                        future_clean.append(ep_dr_clean[idx])
                    else:
                        future_clean.append(ep_dr_clean[-1])
                future_clean = np.array(future_clean, dtype=np.float32)

                # 2) corruption prob tied to THIS step’s DR
                dr_here = ep_dr_clean[t]
                corr = BASE_CORR + GAIN_CORR * dr_here
                corr = float(min(MAX_CORRUPT, corr))

                # 3) literal static mask over the horizon
                mask = (np.random.rand(SPH) < corr).astype(np.float32)

                # 4) static shaped to the signal scale
                sig = np.std(future_clean) + 1e-3
                static = np.random.normal(loc=0.0, scale=sig, size=SPH).astype(np.float32)

                # 5) corrupted target = clean*(1-mask) + static*mask
                future_corrupted = future_clean * (1.0 - mask) + static * mask

                # 6) train prophet on the CORRUPTED target
                prophet.train_step(x, future_corrupted)

            # 7) measure span on CLEAN (this is the “can you see through the noise?” test)
            x0 = ep_obs[0]
            future_clean_0 = []
            for k in range(1, SPH + 1):
                if k < len(ep_dr_clean):
                    future_clean_0.append(ep_dr_clean[k])
                else:
                    future_clean_0.append(ep_dr_clean[-1])
            future_clean_0 = np.array(future_clean_0, dtype=np.float32)

            # looser because CartPole flattening makes relative errors big
            sigma = prophet.measure_predictive_span(x0, future_clean_0, rel_err_thresh=0.25)
        else:
            sigma = last_sigma
        # ---------------------------------------------------
        # score tracking (unchanged)
        # ---------------------------------------------------
        top_scores.append(score)
        top_scores.sort(reverse=True)
        top_scores = top_scores[:15]
        avg_top = sum(top_scores) / len(top_scores)

        print(
            f"Episode {ep:03d}: "
            f"Score={score:3d} | Top-15 Avg={avg_top:6.2f} | "
            f"Predictive Span (σ)={sigma:02d}/{SPAN_HORIZON}"
        )

        last_sigma = sigma

        MASTERY_THRESHOLD = 495
        if len(top_scores) == 15 and avg_top >= MASTERY_THRESHOLD:
            print(f"\n*** MASTERY ACHIEVED ***\nTop-15 average score ({avg_top:.2f}) hit the target.")
            agent.save("wendigo_PirouetteSAC_mastery.zip")
            break

    env.close()
    print("--- Training Complete ---")

if __name__ == "__main__":
    main()
