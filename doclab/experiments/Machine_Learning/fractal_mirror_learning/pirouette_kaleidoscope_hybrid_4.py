import numpy as np
import gym
import torch as th
from stable_baselines3 import SAC
from stable_baselines3.common.buffers import ReplayBuffer
from stable_baselines3.common.logger import configure
import collections

# --- Part 1: Kaleidoscope Memory (COARSER) ---
class KaleidoscopeMemory:
    def __init__(self):
        # coarser bins → more Vigor hits
        self.pos_bins = np.linspace(-2.4, 2.4, 5)       # was denser
        self.vel_bins = np.linspace(-3.0, 3.0, 5)
        self.angle_bins = np.linspace(-0.209, 0.209, 7)  # pole angle: make this one a bit finer
        self.angle_vel_bins = np.linspace(-3.5, 3.5, 5)

        self.kaleidoscope = {}

    def discretize_state(self, obs):
        cart_pos, cart_vel, pole_angle, pole_vel = obs
        pos_idx = np.digitize(cart_pos, self.pos_bins)
        vel_idx = np.digitize(cart_vel, self.vel_bins)
        angle_idx = np.digitize(pole_angle, self.angle_bins)
        angle_vel_idx = np.digitize(pole_vel, self.angle_vel_bins)
        return (pos_idx, vel_idx, angle_idx, angle_vel_idx)

    def get_known_action(self, obs):
        key = self.discretize_state(obs)
        return self.kaleidoscope.get(key, None)

    def learn_from_history(self, episode_history):
        count = 0
        for obs, action in episode_history:
            key = self.discretize_state(obs)
            discrete_action = 0 if action[0] < 0 else 1
            if key not in self.kaleidoscope:
                self.kaleidoscope[key] = discrete_action
                count += 1
        return count

# --- Part 2: Dark Residue (same as 2, but we can use it in reward) ---
def calculate_dark_residue(obs):
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    # keep angle heavy so we reward "upright"
    residue = (
        1.0 * abs(pole_angle) +
        0.5 * abs(pole_vel) +
        0.1 * abs(cart_vel)
    )
    return residue

# --- Part 3: Hybrid Agent ---
class HybridPirouetteAgent:
    def __init__(self, env, device):
        self.env = env
        self.device = device

        # Vigor
        self.kaleidoscope = KaleidoscopeMemory()

        # Rigor (SAC) – start earlier, train a bit more often
        policy_kwargs = dict(net_arch=[64, 64])
        self.sac_agent = SAC(
            "MlpPolicy",
            env,
            policy_kwargs=policy_kwargs,
            verbose=0,
            learning_starts=800,             # was 1000/5000 – learn sooner
            use_sde=False,
            tensorboard_log="./sac_pirouette_log/",
            device=self.device,
        )
        self.replay_buffer = self.sac_agent.replay_buffer
        self.total_steps = 0
        self.batch_size = 512

    def choose_action(self, obs):
        # 1) Vigor first
        known = self.kaleidoscope.get_known_action(obs)
        if known is not None:
            # map discrete → continuous
            return (np.array([-1.0]) if known == 0 else np.array([1.0])), "Vigor"

        # 2) Rigor
        obs_batched = obs.reshape(1, -1)
        action_batched, _ = self.sac_agent.predict(obs_batched, deterministic=False)
        return action_batched[0], "Rigor"

    def learn(self, obs, action, next_obs, reward, done):
        self.total_steps += 1

        # stash transition
        self.replay_buffer.add(obs, next_obs, action, reward, done, [{}])

        # train sooner + more often
        if (
            self.total_steps > self.sac_agent.learning_starts
            and self.replay_buffer.size() > self.batch_size
            and self.total_steps % 20 == 0   # was 50 – make it more responsive
        ):
            # make sure model is set up
            if not hasattr(self.sac_agent, "_logger") or self.sac_agent._logger is None:
                self.sac_agent._setup_model()
                if not hasattr(self.sac_agent, "_logger") or self.sac_agent._logger is None:
                    self.sac_agent._logger = configure("./sac_pirouette_log/", [])
            # small bursts
            self.sac_agent.train(gradient_steps=2, batch_size=self.batch_size)

# --- Continuous wrapper (same idea as before) ---
class ContinuousActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

    def action(self, action):
        return 0 if action[0] < 0 else 1

# --- Main ---
def main():
    device_name = "cuda" if th.cuda.is_available() else "cpu"
    device = th.device(device_name)
    print("Initializing Pirouette Hybrid (SAC + Kaleidoscope) Agent.")
    print(f"Using device: {device_name}")

    base_env = gym.make("CartPole-v1")
    env = ContinuousActionWrapper(base_env)

    agent = HybridPirouetteAgent(env, device)

    num_episodes = 500
    coherence_threshold = 110           # ↓ from 150/300/400
    top_k = 15
    top_scores = []
    avg_margin = 2                      # ↓ from 5 → easier to capture near-misses

    print("Starting Hybrid 'Formular Induction' (Learning).")

    for i in range(num_episodes):
        obs, info = env.reset()
        episode_history = []
        total_score = 0
        total_dark = 0.0
        vigor_ct = 0
        rigor_ct = 0

        terminated = False
        truncated = False

        while not terminated and not truncated:
            action, mode = agent.choose_action(obs)
            if mode == "Vigor":
                vigor_ct += 1
            else:
                rigor_ct += 1

            next_obs, env_reward, terminated, truncated, info = env.step(action)

            # tiny shaping: keep pole small
            dark = calculate_dark_residue(next_obs)
            shaped_reward = env_reward - 0.05 * dark    # env_reward=1 → 0.8..1.0 typically

            agent.learn(obs, action, next_obs, shaped_reward, terminated or truncated)

            episode_history.append((obs, action))

            obs = next_obs
            total_score += env_reward       # scoreboard stays env-pure
            total_dark += dark

        # --- leaderboard before insert ---
        if len(top_scores) > 0:
            avg_top = sum(top_scores) / len(top_scores)
            max_top = top_scores[0]
        else:
            avg_top = 0.0
            max_top = 0.0

        # three ways to call it coherent
        is_hard = total_score >= coherence_threshold
        is_avg = (total_score >= avg_top + avg_margin) and total_score >= 10
        is_near_best = (len(top_scores) >= 3) and (total_score >= 0.9 * max_top)

        # update leaderboard
        top_scores.append(int(total_score))
        top_scores = sorted(top_scores, reverse=True)[:top_k]

        if is_hard or is_avg or is_near_best:
            agent.kaleidoscope.learn_from_history(episode_history)
            print(f"Episode {i+1}: Coherent run. Score: {total_score:.0f}.")
        else:
            print(f"Episode {i+1}: Dissonant run. Score: {total_score:.0f}. Discarding history.")

        print(
            f"    Avg Dark Residue: {total_dark / max(total_score, 1):.2f} | "
            f"Vigor/Rigor: {vigor_ct}/{rigor_ct}"
        )
        print(
            f"    Top-{len(top_scores)} scores: {top_scores} | avg={avg_top:.2f} | margin={avg_margin}"
        )

    print("Training complete.")
    agent.sac_agent.save("pirouette_sac_model_tuned")
    env.close()

if __name__ == "__main__":
    main()
