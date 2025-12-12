import gymnasium as gym
import numpy as np
from stable_baselines3 import SAC

# --------------------------------------------------------------------
# 1) This wrapper matches what you used in the training scripts:
#    SAC outputs [-1, 1] -> we map sign to discrete 0/1.
# --------------------------------------------------------------------
class SACCartPoleWrapper(gym.ActionWrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        # SAC wants a Box action space
        self.action_space = gym.spaces.Box(
            low=-1.0, high=1.0, shape=(1,), dtype=np.float32
        )
        # optional: remember last state/mode if you want parity with autopoietic
        self.current_state = None
        self.current_mode = "Eval"

    def action(self, action: np.ndarray) -> int:
        # simplest: negative -> 0, positive -> 1
        return 0 if action[0] < 0 else 1

    def set_state(self, state: np.ndarray, mode: str = "Eval"):
        # kept for compatibility with the autopoietic script style
        self.current_state = state
        self.current_mode = mode

# --------------------------------------------------------------------
# 2) Your shared dark-residue metric (same as in training)
# --------------------------------------------------------------------
def calculate_dark_residue(obs: np.ndarray) -> float:
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    return (
        0.4 * abs(cart_pos)
        + 0.2 * abs(cart_vel)
        + 1.5 * abs(pole_angle)
        + 0.3 * abs(pole_vel)
    )

# --------------------------------------------------------------------
# 3) Evaluation loop, now using the wrapper
# --------------------------------------------------------------------
def eval_policy(model, episodes=20, noise_std=0.0, name="agent"):
    # use wrapped env so SAC outputs are valid
    env = SACCartPoleWrapper(gym.make("CartPole-v1"))

    totals = []
    avg_dr_per_ep = []

    for ep in range(episodes):
        obs, _ = env.reset()
        # optional start perturbation
        if noise_std > 0:
            obs = obs + np.random.normal(0, noise_std, size=obs.shape)

        done = False
        truncated = False
        ep_reward = 0.0
        ep_dr = 0.0
        steps = 0

        # we can also tell the wrapper our current state/mode
        env.set_state(obs, "Eval")

        while not done and not truncated:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, truncated, _ = env.step(action)

            ep_reward += reward
            ep_dr += calculate_dark_residue(obs)
            steps += 1

            env.set_state(obs, "Eval")

        totals.append(ep_reward)
        avg_dr_per_ep.append(ep_dr / max(1, steps))

    env.close()
    print(
        f"{name}: mean_return={np.mean(totals):.2f}, "
        f"std_return={np.std(totals):.2f}, "
        f"mean_DR={np.mean(avg_dr_per_ep):.4f}"
    )
    return {
        "returns": totals,
        "avg_dr": avg_dr_per_ep,
    }

# --------------------------------------------------------------------
# 4) Load both of your saved models and run both clean + noisy
#    (adjust paths to match wherever you actually saved them)
# --------------------------------------------------------------------
if __name__ == "__main__":
    minimalist = SAC.load("wendigo_PirouetteSAC_mastery.zip")
    autopoietic = SAC.load("autopoietic_gallery/evolved_agent.zip")

    print("=== clean eval (no noise) ===")
    res_min_clean = eval_policy(minimalist, name="minimalist")
    res_auto_clean = eval_policy(autopoietic, name="autopoietic")

    print("=== noisy eval (0.05) ===")
    res_min_noisy = eval_policy(minimalist, noise_std=0.05, name="minimalist+noise")
    res_auto_noisy = eval_policy(autopoietic, noise_std=0.05, name="autopoietic+noise")
