# wendigo_autopoietic_ant.py
import gymnasium as gym
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import DummyVecEnv

# ---------------------------------------------------------
# 1) Dark Residue for Ant
#    We're going to treat DR as "how off you are from a nice,
#    upright, forward-moving ant".
# ---------------------------------------------------------
def ant_dark_residue(obs: np.ndarray) -> float:
    """
    Ant obs (mujoco) usually starts with:
    [qpos(15) w/out 2 dims?, qvel(14), ... ]
    We'll make a cheap DR:
      - penalize pitch/roll (orientation)
      - reward torso height near target
      - penalize high joint velocities
    """
    # be defensive about length
    # typical Ant-v4/v5 obs is ~111; first 13-ish are qpos
    torso_height_target = 0.6

    # height is usually at index 0 or 2 depending on wrapper
    # in gymnasium Ant, obs[0] = x_pos, obs[1] = y_pos, obs[2] = z (height)
    if len(obs) > 2:
        height = obs[2]
    else:
        height = torso_height_target

    # rough velocity energy
    vel_energy = np.sum(np.abs(obs[-10:]))

    height_err = abs(height - torso_height_target)

    # DR should be small when height good and not flailing
    dr = 1.5 * height_err + 0.05 * vel_energy
    return float(dr)


# ---------------------------------------------------------
# 2) Autopoietic reward mixer
#    We gently mix env reward with DR penalty.
#    Later you can let this mutate itself like your CartPole version.
# ---------------------------------------------------------
class AutopoieticAntWrapper(gym.Wrapper):
    def __init__(self, env, dr_weight=0.2):
        super().__init__(env)
        self.dr_weight = dr_weight
        self.current_mode = "Train"

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        dr = ant_dark_residue(obs)
        # autopoietic blend: keep main task but bias to low DR
        mixed_reward = reward - self.dr_weight * dr
        info["dark_residue"] = dr
        info["mode"] = self.current_mode
        return obs, mixed_reward, terminated, truncated, info

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self.current_mode = "Train"
        return obs, info


# ---------------------------------------------------------
# 3) Optional: callback to watch DR during training
# ---------------------------------------------------------
class DRLoggerCallback(BaseCallback):
    def __init__(self, verbose=1):
        super().__init__(verbose)

    def _on_step(self) -> bool:
        # env is VecEnv; grab first
        infos = self.locals.get("infos", [])
        if len(infos) > 0 and "dark_residue" in infos[0]:
            dr = infos[0]["dark_residue"]
            if self.verbose > 0 and self.n_calls % 1000 == 0:
                print(f"[DR] step={self.num_timesteps} dr={dr:.4f}")
        return True


def make_ant_env(dr_weight=0.2):
    def _init():
        # pick the one you have installed; many setups use "Ant-v4"
        env = gym.make("Ant-v5")
        env = AutopoieticAntWrapper(env, dr_weight=dr_weight)
        env = Monitor(env)
        return env
    return _init


if __name__ == "__main__":
    # -----------------------------------------------------
    # 4) Build vec env
    # -----------------------------------------------------
    env = DummyVecEnv([make_ant_env(dr_weight=0.15)])

    # -----------------------------------------------------
    # 5) SAC for Ant — standard-ish config
    #     (tweak net_arch to your taste)
    # -----------------------------------------------------
    model = SAC(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        buffer_size=1_000_000,
        batch_size=256,
        gamma=0.99,
        tau=0.02,
        train_freq=1,
        gradient_steps=1,
        policy_kwargs=dict(net_arch=[256, 256]),
    )

    model.learn(
        total_timesteps=1_000_000,
        callback=DRLoggerCallback(verbose=1),
        log_interval=10,
    )

    model.save("autopoietic_ant_sac.zip")
