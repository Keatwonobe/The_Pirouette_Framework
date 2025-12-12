#!/usr/bin/env python3
"""
Wendigo-Minimalist v6: The Pirouette SAC Agent
------------------------------------------------
An agent learning from a multi-objective reward signal that balances:
1. A drive to survive (Duration Bonus)
2. An aversion to instability (Dissonance Penalty)
3. A drive for active correction (Coherence Gain)
"""
import gymnasium as gym
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure

class DiscreteToBoxActionWrapper(gym.ActionWrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

    def action(self, action: np.ndarray) -> int:
        return 0 if action[0] < 0.0 else 1

def calculate_dark_residue(obs: np.ndarray) -> float:
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    return 0.4 * abs(cart_pos) + 0.2 * abs(cart_vel) + 1.5 * abs(pole_angle) + 0.3 * abs(pole_vel)

def main():
    env = DiscreteToBoxActionWrapper(gym.make("CartPole-v1"))
    agent = SAC("MlpPolicy", env, verbose=0, train_freq=(1, "step"))

    new_logger = configure(None, ["stdout"])
    agent.set_logger(new_logger)

    # --- Hyperparameters for the Pirouette Reward System ---
    gamma_coherence = 1.5   # Weight for rewarding active stability improvements
    beta_duration = 0.05    # Small constant reward for each step survived
    delta_dissonance = 1.0  # Weight for penalizing the current unstable state
    REPLAY_WARMUP_STEPS = 10000
    # ------------------------------------------------------

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
        previous_dr = calculate_dark_residue(obs)

        while not done and not truncated:
            action, _ = agent.predict(obs, deterministic=True)
            next_obs, _, done, truncated, _ = env.step(action)

            # --- MULTI-OBJECTIVE PIROUETTE REWARD ---
            current_dr = calculate_dark_residue(next_obs)
            dr_derivative = current_dr - previous_dr
            
            # 1. Reward for actively increasing coherence (reducing DR)
            coherence_gain = gamma_coherence * max(0, -dr_derivative)
            
            # 2. Penalty for the current state of dissonance (current DR)
            dissonance_penalty = delta_dissonance * current_dr
            
            # 3. Final reward combines coherence, duration, and dissonance
            reward = coherence_gain + beta_duration - dissonance_penalty
            
            previous_dr = current_dr
            # ----------------------------------------

            agent.replay_buffer.add(obs, next_obs, action, reward, done, [{}])
            agent.train(gradient_steps=1)

            obs = next_obs
            score += 1

        top_scores.append(score)
        top_scores.sort(reverse=True)
        top_scores = top_scores[:15]
        avg_top = sum(top_scores) / len(top_scores)

        print(f"Episode {ep:03d}: Score={score} | Top-15 Avg={avg_top:.2f}")

        MASTERY_THRESHOLD = 495
        if len(top_scores) == 15 and avg_top >= MASTERY_THRESHOLD:
            print(f"\n*** MASTERY ACHIEVED ***\nTop-15 average score ({avg_top:.2f}) hit the target.")
            agent.save("wendigo_PirouetteSAC_mastery.zip")
            break

    env.close()
    print("--- Training Complete ---")

if __name__ == "__main__":
    main()