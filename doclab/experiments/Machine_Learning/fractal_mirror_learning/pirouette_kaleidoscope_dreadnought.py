import numpy as np
import gym
from gym import spaces
import torch as th
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure

# =========================================================
# 1) Dark Residue
# =========================================================
def calculate_dark_residue(obs):
    cart_pos, cart_vel, pole_angle, pole_vel = obs[:4]
    angle_term = abs(pole_angle)
    angle_vel_term = 0.5 * abs(pole_vel)
    cart_vel_term = 0.1 * abs(cart_vel)
    cart_pos_term = 0.05 * abs(cart_pos)
    residue = angle_term + angle_vel_term + cart_vel_term + cart_pos_term
    return residue, angle_term, angle_vel_term, cart_vel_term, cart_pos_term


# =========================================================
# 2) Obs wrapper (now 10-dim)
# =========================================================
class DarkResidueObsWrapper(gym.ObservationWrapper):
    """
    10-dim:
      0-3:   original cartpole
      4-7:   absolute helpers + residue
      8:     norm_target (filled from env via setter)
      9:     was_vigor_prev (0/1)
    """
    def __init__(self, env):
        super().__init__(env)
        low = np.full((10,), -np.inf, dtype=np.float32)
        high = np.full((10,), np.inf, dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        self._norm_target = 0.5
        self._was_vigor_prev = 0.0

    def set_dynamic_info(self, norm_target, was_vigor_prev):
        self._norm_target = float(norm_target)
        self._was_vigor_prev = float(was_vigor_prev)

    def observation(self, obs):
        residue, _, _, _, _ = calculate_dark_residue(obs)
        cart_pos, cart_vel, pole_angle, pole_vel = obs
        aug = np.array([
            cart_pos,
            cart_vel,
            pole_angle,
            pole_vel,
            abs(pole_angle),
            abs(pole_vel),
            abs(cart_vel),
            residue,
            self._norm_target,
            self._was_vigor_prev
        ], dtype=np.float32)
        return aug


# =========================================================
# 3) Continuous Action wrapper
# =========================================================
class ContinuousActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

    def action(self, action):
        return 0 if action[0] < 0 else 1


# =========================================================
# 4) Multi-slot Kaleidoscope
# =========================================================
class KaleidoscopeMemory:
    """
    Each key holds up to N candidates.
    We sort by:
        1) coherent desc
        2) residue asc
        3) score desc
    so we always have the "best 3" per region.
    """
    def __init__(self, max_per_key=3):
        self.pos_bins = np.linspace(-2.4, 2.4, 5)
        self.vel_bins = np.linspace(-3.0, 3.0, 5)
        self.angle_bins = np.linspace(-0.209, 0.209, 7)
        self.angle_vel_bins = np.linspace(-3.5, 3.5, 5)
        self.kaleidoscope = {}
        self.max_per_key = max_per_key

    def discretize_state(self, obs_4):
        cart_pos, cart_vel, pole_angle, pole_vel = obs_4
        pos_idx = np.digitize(cart_pos, self.pos_bins)
        vel_idx = np.digitize(cart_vel, self.vel_bins)
        angle_idx = np.digitize(pole_angle, self.angle_bins)
        angle_vel_idx = np.digitize(pole_vel, self.angle_vel_bins)
        return (pos_idx, vel_idx, angle_idx, angle_vel_idx)

    def get_best_for_state(self, obs_4):
        key = self.discretize_state(obs_4)
        arr = self.kaleidoscope.get(key, None)
        if not arr:
            return None
        return arr[0]  # already sorted

    def get_action_if_good(self, obs_4, current_residue, gate=0.30):
        """
        Return best Vigor action if we have one AND it's not clearly worse
        than what we're currently seeing.
        """
        best = self.get_best_for_state(obs_4)
        if best is None:
            return None
        # if KS's best residue is way better than what we see now, use it
        if best["residue"] < current_residue + gate:
            return best["action"]
        return None

    def _insert_candidate(self, key, candidate):
        arr = self.kaleidoscope.get(key, [])
        arr.append(candidate)
        # sort using our priority
        arr.sort(key=lambda c: (-1 if c["coherent"] else 0, c["residue"], -c["score"]))
        # keep top N
        arr = arr[:self.max_per_key]
        self.kaleidoscope[key] = arr

    def learn_from_history(self, episode_history, episode_score, coherent_flag):
        """
        episode_history: list of (obs_aug, action, step_dark)
        We allow up to max_per_key per bin.
        """
        updates = 0
        for obs_aug, action_arr, step_dark in episode_history:
            obs_4 = obs_aug[:4]
            key = self.discretize_state(obs_4)
            discrete_action = 0 if action_arr[0] < 0 else 1

            candidate = {
                "action": discrete_action,
                "residue": float(step_dark),
                "score": float(episode_score),
                "coherent": bool(coherent_flag)
            }

            before = self.kaleidoscope.get(key, [])
            self._insert_candidate(key, candidate)
            after = self.kaleidoscope.get(key, [])
            if len(after) > len(before) or after[0] is candidate:
                updates += 1
        return updates


# =========================================================
# 5) Hybrid Agent
# =========================================================
class HybridPirouetteAgent:
    def __init__(self, env, device):
        self.env = env
        self.device = device

        self.kaleidoscope = KaleidoscopeMemory(max_per_key=3)

        policy_kwargs = dict(net_arch=[64, 64])
        self.sac_agent = SAC(
            "MlpPolicy",
            env,
            policy_kwargs=policy_kwargs,
            verbose=0,
            learning_starts=800,
            tensorboard_log="./sac_pirouette_log_v2/",
            device=self.device,
        )
        self.replay_buffer = self.sac_agent.replay_buffer
        self.total_steps = 0
        self.batch_size = 512

    def choose_action(self, obs_aug, dyn_threshold, current_ep_score, force_eps=0.07):
        """
        obs_aug: 10-dim
        We may force SAC if:
          - random < eps
          - or we are under dyn_threshold by a lot
          - or KS entry is worse than current residue
        """
        raw_obs = obs_aug[:4]
        current_residue = obs_aug[7]

        # How far are we from the moving target?
        deficit = max(0.0, dyn_threshold - current_ep_score)

        # base exploration
        use_rigor = (np.random.rand() < force_eps)

        # more rigor if we're under target a lot
        if deficit > 80:
            if np.random.rand() < 0.25:
                use_rigor = True
        elif deficit > 40:
            if np.random.rand() < 0.15:
                use_rigor = True

        action_src = "Vigor"
        if not use_rigor:
            # try vigor, but only if it's not clearly worse
            vigor_action = self.kaleidoscope.get_action_if_good(raw_obs, current_residue)
            if vigor_action is not None:
                return np.array([-1.0]) if vigor_action == 0 else np.array([1.0]), action_src
            # otherwise fall through to rigor

        # rigor branch
        obs_batched = obs_aug.reshape(1, -1)
        action_batched, _ = self.sac_agent.predict(obs_batched, deterministic=False)
        return action_batched[0], "Rigor"

    def learn(self, obs_aug, action, next_obs_aug, reward, done, dark):
        self.total_steps += 1

        # oversample clean transitions
        self.replay_buffer.add(obs_aug, next_obs_aug, action, reward, done, [{}])
        if dark < 0.22:
            # add a second time to bias training toward clean
            self.replay_buffer.add(obs_aug, next_obs_aug, action, reward, done, [{}])

        if (
            self.total_steps > self.sac_agent.learning_starts
            and self.replay_buffer.size() > self.batch_size
            and self.total_steps % 15 == 0
        ):
            if not hasattr(self.sac_agent, "_logger") or self.sac_agent._logger is None:
                self.sac_agent._setup_model()
                if not hasattr(self.sac_agent, "_logger") or self.sac_agent._logger is None:
                    self.sac_agent._logger = configure("./sac_pirouette_log_v2/", [])
            self.sac_agent.train(gradient_steps=3, batch_size=self.batch_size)


# =========================================================
# 6) Main loop (v2)
# =========================================================
def main():
    device_name = "cuda" if th.cuda.is_available() else "cpu"
    device = th.device(device_name)
    print("Initializing Pirouette DESTROYER v2.")
    print(f"Using device: {device_name}")

    base_env = gym.make("CartPole-v1")
    env = ContinuousActionWrapper(base_env)
    obs_wrapper = DarkResidueObsWrapper(env)

    agent = HybridPirouetteAgent(obs_wrapper, device)

    num_episodes = 500
    top_k = 15
    top_scores = []
    base_margin = 2

    last_was_vigor = 0.0

    for ep in range(num_episodes):
        raw_obs, info = env.reset()
        # initial dyn info (will be updated below)
        obs_wrapper.set_dynamic_info(0.5, last_was_vigor)
        obs_aug = obs_wrapper.observation(raw_obs)

        episode_history = []
        total_score = 0
        total_dark = 0.0
        max_dark = 0.0
        vigor_ct = 0
        rigor_ct = 0

        terminated = False
        truncated = False

        while not terminated and not truncated:
            # dynamic threshold current estimate
            if len(top_scores) > 0:
                max_top = top_scores[0]
                dyn_threshold = max(120, int(0.75 * max_top))
            else:
                dyn_threshold = 120

            action, mode = agent.choose_action(
                obs_aug,
                dyn_threshold=dyn_threshold,
                current_ep_score=total_score
            )

            if mode == "Vigor":
                vigor_ct += 1
                last_was_vigor = 1.0
            else:
                rigor_ct += 1
                last_was_vigor = 0.0

            next_raw_obs, env_reward, terminated, truncated, info = env.step(action)
            dark, *_ = calculate_dark_residue(next_raw_obs)
            max_dark = max(max_dark, dark)

            shaped_reward = env_reward - 0.08 * dark

            # update dynamic fields for next obs
            norm_target = dyn_threshold / 500.0
            obs_wrapper.set_dynamic_info(norm_target, last_was_vigor)
            next_obs_aug = obs_wrapper.observation(next_raw_obs)

            agent.learn(obs_aug, action, next_obs_aug, shaped_reward, terminated or truncated, dark)

            episode_history.append((obs_aug, action, dark))

            obs_aug = next_obs_aug
            total_score += env_reward
            total_dark += dark

        # leaderboard
        if len(top_scores) > 0:
            avg_top = sum(top_scores) / len(top_scores)
            max_top = top_scores[0]
        else:
            avg_top = 0.0
            max_top = 0.0

        dyn_threshold = max(120, int(0.75 * max_top)) if max_top > 0 else 120

        top_scores.append(int(total_score))
        top_scores = sorted(top_scores, reverse=True)[:top_k]

        avg_dark = total_dark / max(total_score, 1)

        # rigor level
        total_actions = vigor_ct + rigor_ct
        if rigor_ct == 0:
            rigor_level = 0
        else:
            ratio = rigor_ct / max(total_actions, 1)
            if ratio < 0.20:
                rigor_level = 1
            elif ratio < 0.50:
                rigor_level = 2
            else:
                rigor_level = 3

        # --- New harvesting strategy ---
        # always keep the top-N cleanest steps
        HARVEST_TOP = 24
        episode_history_sorted = sorted(episode_history, key=lambda x: x[2])
        best_steps = episode_history_sorted[:HARVEST_TOP]

        is_coherent = (
            total_score >= dyn_threshold
            or (total_score >= avg_top + base_margin and total_score >= 10)
            or (len(top_scores) >= 3 and total_score >= 0.9 * max_top)
        )

        updates = agent.kaleidoscope.learn_from_history(
            best_steps,
            episode_score=total_score,
            coherent_flag=is_coherent
        )

        label = "Coherent run" if is_coherent else "Dissonant run"
        print(f"Episode {ep+1}: {label}. Score: {total_score:.0f}. (KS updates: {updates})")
        print(
            f"    Avg Dark Residue: {avg_dark:.2f} (max {max_dark:.2f}) | "
            f"Vigor/Rigor: {vigor_ct}/{rigor_level}"
        )
        print(
            f"    Top-{len(top_scores)} scores: {top_scores} | avg={avg_top:.2f} | dyn_threshold={dyn_threshold}"
        )

    print("Training complete.")
    agent.sac_agent.save("pirouette_sac_model_destroyer_v2")
    env.close()


if __name__ == "__main__":
    main()
