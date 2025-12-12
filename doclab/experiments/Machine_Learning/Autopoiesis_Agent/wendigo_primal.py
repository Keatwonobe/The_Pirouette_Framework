"""
pirouette_ant_autopoietic.py
Version: 0.1.0
Purpose: Train an Ant agent with Pirouette-style autopoiesis:
    - dark residue minimization (annealed)
    - manifold well shaping
    - span coherence reward
    - tiny prophet (next-state predictor) that pays for improved predictability
"""

import math
from collections import deque

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from stable_baselines3 import SAC
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback


# =========================================================
# 1. Dark Residue
# =========================================================
def ant_dark_residue(obs: np.ndarray) -> float:
    """
    Cheap coherence penalty for Ant.
    - stabilizes torso height around ~0.6
    - discourages wild velocity in the tail of obs
    """
    target_height = 0.6
    height = obs[2] if len(obs) > 2 else target_height
    vel_energy = np.sum(np.abs(obs[-10:]))
    height_err = abs(height - target_height)
    return 1.5 * height_err + 0.05 * vel_energy


# =========================================================
# 2. Manifold Well (gives the agent something smooth to touch)
# =========================================================
class ManifoldWell:
    def __init__(self, action_dim: int, max_steps: int = 2000,
                 bonus_coeff: float = 0.5, tear_coeff: float = 0.1):
        self.action_dim = action_dim
        self.max_steps = max_steps
        self.bonus_coeff = bonus_coeff
        self.tear_coeff = tear_coeff

        self.center = np.zeros(action_dim, dtype=np.float32)
        self.phase = np.random.uniform(0, 2 * np.pi, size=action_dim)
        self.frequency = np.random.uniform(0.5, 1.5, size=action_dim)
        self.amplitude = np.random.uniform(0.4, 0.8, size=action_dim)

    def step(self, t: int):
        # move the manifold center slowly over training
        time_factor = (2 * np.pi * t) / self.max_steps
        self.center = (
            self.amplitude * np.sin(self.frequency * time_factor + self.phase)
        ).astype(np.float32)

    def reward(self, action: np.ndarray) -> tuple[float, float]:
        dist = np.linalg.norm(action - self.center)
        align = self.bonus_coeff * math.exp(-2.0 * dist)
        tear = -self.tear_coeff * max(0.0, dist - 1.0)
        return align + tear, dist


# =========================================================
# 3. Tiny Prophet (predict next_obs from obs, action)
# =========================================================
class TinyProphet(nn.Module):
    def __init__(self, obs_dim: int, act_dim: int, hidden: int = 128, lr: float = 1e-3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim + act_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, obs_dim),
        )
        self.opt = optim.Adam(self.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()

    @torch.no_grad()
    def predict_next(self, obs: torch.Tensor, act: torch.Tensor) -> torch.Tensor:
        x = torch.cat([obs, act], dim=-1)
        return self.net(x)

    def train_step(self, obs: torch.Tensor, act: torch.Tensor, next_obs: torch.Tensor) -> float:
        x = torch.cat([obs, act], dim=-1)
        pred = self.net(x)
        loss = self.loss_fn(pred, next_obs)
        self.opt.zero_grad()
        loss.backward()
        self.opt.step()
        return loss.item()


# =========================================================
# 4. Pirouette Ant Wrapper
#    Mixture: env_r - w_dr*DR + manifold_r + span_r + prophet_bonus
# =========================================================
class PirouetteAntWrapper(gym.Wrapper):
    def __init__(
        self,
        env: gym.Env,
        dr_weight_start: float = 0.2,
        dr_weight_end: float = 0.05,
        dr_anneal_steps: int = 300_000,
        span_threshold: float = 0.25,
        span_scale: float = 0.01,
    ):
        super().__init__(env)

        self.total_steps = 0
        self.dr_weight_start = dr_weight_start
        self.dr_weight_end = dr_weight_end
        self.dr_anneal_steps = dr_anneal_steps

        self.span_threshold = span_threshold
        self.span_scale = span_scale
        self.current_span = 0

        self.manifold = ManifoldWell(action_dim=env.action_space.shape[0])
        self.mode = "Train"

        # will be set by prophet callback
        self.prophet_bonus = 0.0
        self.last_obs = None

    def _current_dr_weight(self) -> float:
        if self.total_steps >= self.dr_anneal_steps:
            return self.dr_weight_end
        frac = self.total_steps / self.dr_anneal_steps
        return self.dr_weight_start + frac * (self.dr_weight_end - self.dr_weight_start)

    def reset(self, **kwargs):
        self.current_span = 0
        obs, info = self.env.reset(**kwargs)
        self.last_obs = obs
        return obs, info

    def step(self, action):
        # advance manifold
        self.manifold.step(self.total_steps)

        obs, reward, terminated, truncated, info = self.env.step(action)
        self.total_steps += 1

        # 1) autopoietic DR
        dr = ant_dark_residue(obs)
        dr_w = self._current_dr_weight()
        reward_autopoietic = reward - dr_w * dr

        # 2) manifold
        m_reward, dist = self.manifold.reward(action)

        # 3) span
        if dist < self.span_threshold:
            self.current_span += 1
        else:
            self.current_span = 0
        span_reward = self.current_span * self.span_scale

        # 4) prophet bonus (already set externally) and decay
        mixed_reward = reward_autopoietic + m_reward + span_reward + self.prophet_bonus
        self.prophet_bonus *= 0.5  # fade out

        # stash transition for prophet
        info["transition_obs"] = self.last_obs
        info["transition_act"] = action
        info["transition_next_obs"] = obs

        # log diagnostics
        info["dark_residue"] = dr
        info["dr_weight"] = dr_w
        info["manifold_reward"] = m_reward
        info["span"] = self.current_span
        info["span_reward"] = span_reward

        self.last_obs = obs
        return obs, mixed_reward, terminated, truncated, info


# =========================================================
# 5. Prophet Callback
#    Trains prophet online and sends bonus back into wrapper
# =========================================================
class ProphetCallback(BaseCallback):
    def __init__(
        self,
        vec_env,
        obs_dim: int,
        act_dim: int,
        bonus_scale: float = 0.02,
        buffer_size: int = 2048,
        verbose: int = 0,
    ):
        super().__init__(verbose)
        self.vec_env = vec_env
        self.prophet = TinyProphet(obs_dim, act_dim)
        self.bonus_scale = bonus_scale
        self.buffer = deque(maxlen=buffer_size)
        self.prev_loss = None

    def _on_step(self) -> bool:
        infos = self.locals.get("infos", [])
        # collect transitions
        for info in infos:
            o0 = info.get("transition_obs", None)
            a0 = info.get("transition_act", None)
            o1 = info.get("transition_next_obs", None)
            if o0 is not None and a0 is not None and o1 is not None:
                self.buffer.append((o0, a0, o1))

        # train prophet
        if len(self.buffer) >= 64:
            batch = list(self.buffer)[-64:]
            obs_batch = torch.tensor(np.stack([b[0] for b in batch]), dtype=torch.float32)
            act_batch = torch.tensor(np.stack([b[1] for b in batch]), dtype=torch.float32)
            nxt_batch = torch.tensor(np.stack([b[2] for b in batch]), dtype=torch.float32)

            loss = self.prophet.train_step(obs_batch, act_batch, nxt_batch)

            # compute improvement -> bonus
            if self.prev_loss is not None:
                improvement = max(0.0, self.prev_loss - loss)
                bonus = improvement * self.bonus_scale

                # write bonus into each underlying env
                try:
                    for env_idx in range(self.vec_env.num_envs):
                        env = self.vec_env.envs[env_idx]
                        if hasattr(env, "prophet_bonus"):
                            env.prophet_bonus += bonus
                except Exception:
                    pass

            self.prev_loss = loss

            if self.verbose > 0 and self.n_calls % 1000 == 0:
                print(f"[Prophet] step={self.num_timesteps} loss={loss:.6f}")

        return True


# =========================================================
# 6. Factory and main train
# =========================================================
def make_pirouette_ant_env():
    base = gym.make("Ant-v5")
    wrapped = PirouetteAntWrapper(base)
    return wrapped


def main():
    # build vec env
    env = DummyVecEnv([make_pirouette_ant_env])
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.shape[0]

    # build model
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
        policy_kwargs=dict(net_arch=[256, 256, 128]),
    )

    prophet_cb = ProphetCallback(
        env,
        obs_dim=obs_dim,
        act_dim=act_dim,
        bonus_scale=0.02,
        verbose=1,
    )

    # train
    model.learn(total_timesteps=1_000_000, callback=prophet_cb, log_interval=10)
    model.save("pirouette_ant_autopoietic_v1.zip")
    print("Training complete. Model saved to pirouette_ant_autopoietic_v1.zip")


if __name__ == "__main__":
    main()
