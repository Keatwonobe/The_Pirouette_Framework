"""
pirouette_pendulum.py

Pirouette-style contrast learner on Pendulum-v1:
- Phase 1: TRIAGE   -> build contrast manifold over (theta, theta_dot)
- Phase 2: ANALYZE  -> find hotspot cells with high average contrast
- Phase 3: LEARN    -> Q-learning with boosted learning rate in hotspot

Requires:
    pip install gymnasium[classic-control] numpy matplotlib
"""

import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


class PirouettePendulumAgent:
    def __init__(
        self,
        n_angle_bins=24,
        n_vel_bins=24,
        n_actions=7,
        triage_steps=10_000,
        learn_steps=50_000,
        hotspot_quantile=0.8,
        base_lr=0.1,
        hotspot_lr_factor=5.0,
        gamma=0.99,
        epsilon_start=1.0,
        epsilon_end=0.05,
    ):
        # Discretisation
        self.n_angle_bins = n_angle_bins
        self.n_vel_bins = n_vel_bins
        self.n_actions = n_actions

        # Time budgets
        self.triage_steps = triage_steps
        self.learn_steps = learn_steps

        # Hotspot detection
        self.hotspot_quantile = hotspot_quantile
        self.hotspot_lr_factor = hotspot_lr_factor

        # Q-learning hyperparams
        self.base_lr = base_lr
        self.gamma = gamma
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end

        # Will be set when we see env.action_space.high
        self.action_values = None  # np.linspace(-max_torque, max_torque, n_actions)

        # Contrast manifold: (angle_bin, vel_bin) -> [sum_contrast, count]
        self.manifold = defaultdict(lambda: [0.0, 0])
        self.max_contrast = 0.0
        self.hotspot_mask = np.zeros((n_angle_bins, n_vel_bins), dtype=bool)

        # Q-table: (angle_bin, vel_bin, action_idx)
        self.Q = np.zeros((n_angle_bins, n_vel_bins, n_actions), dtype=np.float32)

        self.phase = "IDLE"
        self.total_steps = 0
        self.last_reward = 0.0

        # Logging
        self.reward_trace = []

    # ---------- State & action helpers ----------

    def set_action_range_from_env(self, env):
        # Pendulum-v1 is Box([-2], [2])
        max_torque = float(env.action_space.high[0])
        self.action_values = np.linspace(-max_torque, max_torque, self.n_actions)

    def _decode_theta_and_vel(self, obs):
        # obs = [cos(theta), sin(theta), theta_dot]
        cos_t, sin_t, vel = obs
        theta = np.arctan2(sin_t, cos_t)  # -pi..pi
        return theta, vel

    def discretize_state(self, obs, env):
        theta, vel = self._decode_theta_and_vel(obs)

        # Angle bins over [-pi, pi]
        angle_idx = int((theta + np.pi) / (2 * np.pi) * self.n_angle_bins)
        angle_idx = np.clip(angle_idx, 0, self.n_angle_bins - 1)

        # Velocity bins: Pendulum default bound is around [-8, 8]
        max_speed = getattr(env.unwrapped, "max_speed", 8.0)
        vel_idx = int((vel + max_speed) / (2 * max_speed) * self.n_vel_bins)
        vel_idx = np.clip(vel_idx, 0, self.n_vel_bins - 1)

        return angle_idx, vel_idx

    def choose_action(self, s_idx, epsilon):
        angle_idx, vel_idx = s_idx

        if self.phase == "TRIAGE":
            # random during triage
            a_idx = np.random.randint(self.n_actions)
        else:
            if np.random.rand() < epsilon:
                a_idx = np.random.randint(self.n_actions)
            else:
                a_idx = np.argmax(self.Q[angle_idx, vel_idx, :])

        return a_idx

    # ---------- Phase 1: TRIAGE / contrast manifold ----------

    def triage_step(self, obs, reward, env):
        self.total_steps += 1

        # Contrast = |r_t - r_{t-1}| (pressure differential)
        contrast = abs(reward - self.last_reward)
        self.last_reward = reward

        s_idx = self.discretize_state(obs, env)
        key = s_idx

        data = self.manifold[key]
        data[0] += contrast
        data[1] += 1
        self.manifold[key] = data

        avg_contrast = data[0] / data[1]
        if avg_contrast > self.max_contrast:
            self.max_contrast = avg_contrast

        # Action: random during triage
        a_idx = self.choose_action(s_idx, epsilon=1.0)

        return a_idx

    def finalize_hotspot(self):
        # Build full contrast array
        contrast_grid = np.zeros((self.n_angle_bins, self.n_vel_bins), dtype=np.float32)

        for (a_idx, v_idx), (sum_c, count) in self.manifold.items():
            if count > 0:
                contrast_grid[a_idx, v_idx] = sum_c / count

        # Determine threshold using quantile among non-zero entries
        valid = contrast_grid[contrast_grid > 0]
        if len(valid) == 0:
            print("No contrast collected; hotspot remains empty.")
            return contrast_grid

        threshold = np.quantile(valid, self.hotspot_quantile)
        self.hotspot_mask = contrast_grid >= threshold

        print(
            f"[ANALYZE] Max contrast={contrast_grid.max():.4f}, "
            f"threshold (q={self.hotspot_quantile})={threshold:.4f}, "
            f"hotspot cells={self.hotspot_mask.sum()}"
        )
        return contrast_grid

    # ---------- Phase 3: LEARN (Q-learning with hotspot boost) ----------

    def learn_step(self, obs, reward, next_obs, done, env, step_in_learn):
        self.total_steps += 1

        # Linearly decay epsilon within learn phase
        frac = step_in_learn / max(1, self.learn_steps)
        epsilon = self.epsilon_start + frac * (self.epsilon_end - self.epsilon_start)
        epsilon = max(self.epsilon_end, epsilon)

        s_idx = self.discretize_state(obs, env)
        ns_idx = self.discretize_state(next_obs, env)

        a_idx = self.choose_action(s_idx, epsilon)

        # Q-learning update
        angle_idx, vel_idx = s_idx
        nangle_idx, nvel_idx = ns_idx

        max_next_q = np.max(self.Q[nangle_idx, nvel_idx, :])
        td_target = reward + (0.0 if done else self.gamma * max_next_q)
        td_error = td_target - self.Q[angle_idx, vel_idx, a_idx]

        # Boost learning rate if state is in hotspot
        lr = self.base_lr
        if self.hotspot_mask[angle_idx, vel_idx]:
            lr *= self.hotspot_lr_factor

        self.Q[angle_idx, vel_idx, a_idx] += lr * td_error

        return a_idx, epsilon

    # ---------- Running convenience ----------

    def action_from_index(self, a_idx):
        return np.array([self.action_values[a_idx]], dtype=np.float32)


def run_pirouette_pendulum(
    render=False,
    triage_steps=10_000,
    learn_steps=100_000,
    seed=0,
):
    env = gym.make("Pendulum-v1")
    env.reset(seed=seed)

    agent = PirouettePendulumAgent(
        triage_steps=triage_steps,
        learn_steps=learn_steps,
    )
    agent.set_action_range_from_env(env)

    # ---------------- Phase 1: TRIAGE ----------------
    agent.phase = "TRIAGE"
    obs, _ = env.reset()
    agent.last_reward = 0.0
    steps = 0

    print("[TRIAGE] Building contrast manifold...")
    while steps < agent.triage_steps:
        if render and steps % 5 == 0:
            env.render()

        a_idx = agent.triage_step(obs, reward=0.0, env=env)
        action = agent.action_from_index(a_idx)

        next_obs, reward, terminated, truncated, _ = env.step(action)
        # reward is only used for contrast; next loop uses it as last_reward
        agent.last_reward = reward

        obs = next_obs
        steps += 1
        if terminated or truncated:
            obs, _ = env.reset()

    # ---------------- Phase 2: ANALYZE ----------------
    print("[ANALYZE] Extracting hotspot from contrast manifold...")
    contrast_grid = agent.finalize_hotspot()

    # Optional: visualize manifold
    plt.figure(figsize=(6, 4))
    plt.imshow(
        contrast_grid.T,
        origin="lower",
        aspect="auto",
        cmap="magma",
        extent=[0, agent.n_angle_bins, 0, agent.n_vel_bins],
    )
    plt.colorbar(label="Average contrast")
    plt.title("Contrast manifold (angle x velocity)")
    plt.xlabel("Angle bin")
    plt.ylabel("Velocity bin")
    plt.tight_layout()
    plt.show(block=False)

    # ---------------- Phase 3: LEARN ----------------
    print("[LEARN] Q-learning with hotspot-boosted learning rate...")
    agent.phase = "LEARN"
    obs, _ = env.reset()
    step_in_learn = 0
    ep_return = 0.0
    ep = 0
    returns = []

    while step_in_learn < agent.learn_steps:
        if render:
            env.render()

        # Take a step & update Q
        action_idx, epsilon = agent.learn_step(
            obs=obs,
            reward=0.0,  # reward will be filled after env.step
            next_obs=obs,  # placeholder, replaced below
            done=False,
            env=env,
            step_in_learn=step_in_learn,
        )
        action = agent.action_from_index(action_idx)
        next_obs, reward, terminated, truncated, _ = env.step(action)

        # Now actually update with correct reward & next state
        # (small convenience: call learn_step again just for Q update,
        # but with epsilon ~ same; or do TD manually here.)
        s_idx = agent.discretize_state(obs, env)
        ns_idx = agent.discretize_state(next_obs, env)
        angle_idx, vel_idx = s_idx
        nangle_idx, nvel_idx = ns_idx
        max_next_q = np.max(agent.Q[nangle_idx, nvel_idx, :])
        td_target = reward + (0.0 if (terminated or truncated) else agent.gamma * max_next_q)
        td_error = td_target - agent.Q[angle_idx, vel_idx, action_idx]

        frac = step_in_learn / max(1, agent.learn_steps)
        epsilon = agent.epsilon_start + frac * (agent.epsilon_end - agent.epsilon_start)
        epsilon = max(agent.epsilon_end, epsilon)
        lr = agent.base_lr * (agent.hotspot_lr_factor if agent.hotspot_mask[angle_idx, vel_idx] else 1.0)
        agent.Q[angle_idx, vel_idx, action_idx] += lr * td_error

        ep_return += reward
        obs = next_obs
        step_in_learn += 1

        if terminated or truncated:
            returns.append(ep_return)
            agent.reward_trace.append(ep_return)
            ep += 1
            if ep % 10 == 0:
                print(
                    f"[LEARN] Episode {ep:4d} | "
                    f"steps={step_in_learn:6d}/{agent.learn_steps} | "
                    f"return={ep_return:7.2f} | eps={epsilon:.3f}"
                )
            ep_return = 0.0
            obs, _ = env.reset()

    env.close()
    print("[DONE] Training complete.")
    if returns:
        print(f"Average episodic return over last 10 episodes: {np.mean(returns[-10:]):.2f}")

    # Plot episode returns
    if returns:
        plt.figure(figsize=(6, 4))
        plt.plot(returns)
        plt.xlabel("Episode")
        plt.ylabel("Return")
        plt.title("Pendulum returns (pirouette contrast learner)")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    run_pirouette_pendulum(render=False)
