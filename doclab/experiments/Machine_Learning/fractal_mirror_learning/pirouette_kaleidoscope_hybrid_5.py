import numpy as np
import gym
from gym import spaces
import torch as th
from stable_baselines3 import SAC
from stable_baselines3.common.logger import configure

# -----------------------------
# 1) Dark Residue (vectorized)
# -----------------------------
def calculate_dark_residue(obs):
    """
    Accepts either 4-dim cartpole obs or our 8-dim augmented obs.
    We always evaluate residue on the first 4 dims.
    """
    cart_pos, cart_vel, pole_angle, pole_vel = obs[:4]
    # keep angle heavy so we reward "upright"
    angle_term = abs(pole_angle)
    angle_vel_term = 0.5 * abs(pole_vel)
    cart_vel_term = 0.1 * abs(cart_vel)
    cart_pos_term = 0.05 * abs(cart_pos)
    residue = angle_term + angle_vel_term + cart_vel_term + cart_pos_term
    return residue, angle_term, angle_vel_term, cart_vel_term, cart_pos_term


# ----------------------------------------
# 2) Observation wrapper: feed more info
# ----------------------------------------
class DarkResidueObsWrapper(gym.ObservationWrapper):
    """
    Extends CartPole obs (4) -> (8):
        [cart_pos, cart_vel, pole_angle, pole_vel,
         |pole_angle|, |pole_vel|, |cart_vel|, dark_residue]
    This gives the SAC policy direct access to the thing we care about.
    """
    def __init__(self, env):
        super().__init__(env)
        low = np.full((8,), -np.inf, dtype=np.float32)
        high = np.full((8,), np.inf, dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

    def observation(self, obs):
        residue, a1, a2, a3, a4 = calculate_dark_residue(obs)
        cart_pos, cart_vel, pole_angle, pole_vel = obs
        aug = np.array([
            cart_pos,
            cart_vel,
            pole_angle,
            pole_vel,
            abs(pole_angle),
            abs(pole_vel),
            abs(cart_vel),
            residue
        ], dtype=np.float32)
        return aug


# -----------------------------------------------------
# 3) Action wrapper (same idea as your original file)
# -----------------------------------------------------
class ContinuousActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

    def action(self, action):
        # map continuous → discrete for CartPole
        return 0 if action[0] < 0 else 1


# -----------------------------------------------------
# 4) Kaleidoscope memory that cares about residue
# -----------------------------------------------------
class KaleidoscopeMemory:
    """
    New rule: every state bin keeps the *best* (i.e. lowest-residue, coherent-preferred)
    action we've ever seen for that bin.

    That means dissonant-but-clean episodes can still upgrade the memory.
    """

    def __init__(self):
        # keep bins similar to original, but these can be tuned
        self.pos_bins = np.linspace(-2.4, 2.4, 5)
        self.vel_bins = np.linspace(-3.0, 3.0, 5)
        self.angle_bins = np.linspace(-0.209, 0.209, 7)
        self.angle_vel_bins = np.linspace(-3.5, 3.5, 5)

        # key -> dict(action, residue, score, coherent_flag)
        self.kaleidoscope = {}

    def discretize_state(self, obs_4):
        cart_pos, cart_vel, pole_angle, pole_vel = obs_4
        pos_idx = np.digitize(cart_pos, self.pos_bins)
        vel_idx = np.digitize(cart_vel, self.vel_bins)
        angle_idx = np.digitize(pole_angle, self.angle_bins)
        angle_vel_idx = np.digitize(pole_vel, self.angle_vel_bins)
        return (pos_idx, vel_idx, angle_idx, angle_vel_idx)

    def get_known_action(self, obs_4):
        key = self.discretize_state(obs_4)
        entry = self.kaleidoscope.get(key, None)
        if entry is None:
            return None
        return entry["action"]

    def learn_from_history(self, episode_history, episode_score, episode_avg_dark, coherent_flag):
        """
        episode_history: list of (obs_8, action_array, step_dark)
        We will down-project obs_8[:4] for binning.
        We keep:
            - coherent wins over dissonant
            - within same flag, lower residue wins
            - tie-breaker: higher episode_score wins
        """
        updates = 0
        for obs_aug, action_arr, step_dark in episode_history:
            obs_4 = obs_aug[:4]
            key = self.discretize_state(obs_4)
            discrete_action = 0 if action_arr[0] < 0 else 1

            candidate = {
                "action": discrete_action,
                "residue": step_dark,
                "score": episode_score,
                "coherent": coherent_flag
            }

            if key not in self.kaleidoscope:
                self.kaleidoscope[key] = candidate
                updates += 1
            else:
                stored = self.kaleidoscope[key]
                # coherent beats non-coherent
                if coherent_flag and not stored["coherent"]:
                    self.kaleidoscope[key] = candidate
                    updates += 1
                else:
                    # both coherent or both not → pick cleaner
                    if step_dark < stored["residue"] - 1e-6:
                        self.kaleidoscope[key] = candidate
                        updates += 1
                    elif abs(step_dark - stored["residue"]) < 1e-6:
                        # same residue → take better score
                        if episode_score > stored["score"]:
                            self.kaleidoscope[key] = candidate
                            updates += 1
        return updates


# -----------------------------------------------------
# 5) Hybrid agent (Vigor first, Rigor second)
# -----------------------------------------------------
class HybridPirouetteAgent:
    def __init__(self, env, device):
        self.env = env
        self.device = device

        # Vigor
        self.kaleidoscope = KaleidoscopeMemory()

        # Rigor (SAC) – make it see augmented obs
        policy_kwargs = dict(net_arch=[64, 64])
        self.sac_agent = SAC(
            "MlpPolicy",
            env,
            policy_kwargs=policy_kwargs,
            verbose=0,
            learning_starts=600,     # start a little earlier than original
            use_sde=False,
            tensorboard_log="./sac_pirouette_log/",
            device=self.device,
        )
        self.replay_buffer = self.sac_agent.replay_buffer
        self.total_steps = 0
        self.batch_size = 512

    def choose_action(self, obs_aug):
        """
        obs_aug is 8-dim. Vigor bins on obs_aug[:4].
        """
        raw_obs = obs_aug[:4]
        known = self.kaleidoscope.get_known_action(raw_obs)
        if known is not None:
            # map discrete → continuous
            return (np.array([-1.0]) if known == 0 else np.array([1.0])), "Vigor"

        # Rigor
        obs_batched = obs_aug.reshape(1, -1)
        action_batched, _ = self.sac_agent.predict(obs_batched, deterministic=False)
        return action_batched[0], "Rigor"

    def learn(self, obs_aug, action, next_obs_aug, reward, done):
        self.total_steps += 1

        # stash transition
        self.replay_buffer.add(obs_aug, next_obs_aug, action, reward, done, [{}])

        # train more often to break out of plateaus
        if (
            self.total_steps > self.sac_agent.learning_starts
            and self.replay_buffer.size() > self.batch_size
            and self.total_steps % 15 == 0    # was 20 → 15 to be more aggressive
        ):
            if not hasattr(self.sac_agent, "_logger") or self.sac_agent._logger is None:
                self.sac_agent._setup_model()
                if not hasattr(self.sac_agent, "_logger") or self.sac_agent._logger is None:
                    self.sac_agent._logger = configure("./sac_pirouette_log/", [])
            self.sac_agent.train(gradient_steps=3, batch_size=self.batch_size)


# -----------------------------------------------------
# 6) Main training loop (destroyer version)
# -----------------------------------------------------
def main():
    device_name = "cuda" if th.cuda.is_available() else "cpu"
    device = th.device(device_name)
    print("Initializing Pirouette DESTROYER (SAC + Kaleidoscope).")
    print(f"Using device: {device_name}")

    base_env = gym.make("CartPole-v1")
    env = ContinuousActionWrapper(base_env)
    env = DarkResidueObsWrapper(env)

    agent = HybridPirouetteAgent(env, device)

    num_episodes = 500
    top_k = 15
    top_scores = []
    base_margin = 2

    print("Starting Hybrid 'Formular Induction' (Destroyer mode).")

    for ep in range(num_episodes):
        obs_aug, info = env.reset()
        episode_history = []
        total_score = 0
        total_dark = 0.0
        max_dark = 0.0
        vigor_ct = 0
        rigor_ct = 0

        terminated = False
        truncated = False
        step_idx = 0

        while not terminated and not truncated:
            action, mode = agent.choose_action(obs_aug)
            if mode == "Vigor":
                vigor_ct += 1
            else:
                rigor_ct += 1

            next_obs_aug, env_reward, terminated, truncated, info = env.step(action)

            # dark on NEXT obs (post action)
            dark, d1, d2, d3, d4 = calculate_dark_residue(next_obs_aug)
            max_dark = max(max_dark, dark)

            # stronger shaping: really penalize messy pole
            shaped_reward = env_reward - 0.08 * dark

            agent.learn(obs_aug, action, next_obs_aug, shaped_reward, terminated or truncated)

            # store with per-step dark so memory can pick the clean ones
            episode_history.append((obs_aug, action, dark))

            obs_aug = next_obs_aug
            total_score += env_reward
            total_dark += dark
            step_idx += 1

        # leaderboard stats BEFORE we insert
        if len(top_scores) > 0:
            avg_top = sum(top_scores) / len(top_scores)
            max_top = top_scores[0]
        else:
            avg_top = 0.0
            max_top = 0.0

        # adaptive coherence threshold:
        # - never lower than 90 (so small wins still count)
        # - 75% of best run, so we keep pushing up
        dyn_threshold = max(90, int(0.75 * max_top)) if max_top > 0 else 90

        # three ways to call it coherent
        is_hard = total_score >= dyn_threshold
        is_avg = (total_score >= avg_top + base_margin) and total_score >= 10
        is_near_best = (len(top_scores) >= 3) and (total_score >= 0.9 * max_top)

        # update leaderboard
        top_scores.append(int(total_score))
        top_scores = sorted(top_scores, reverse=True)[:top_k]

        # episode-level dark metrics
        avg_dark = total_dark / max(total_score, 1)

        # rigor level 0–3, like you wanted
        total_actions = vigor_ct + rigor_ct
        if rigor_ct == 0:
            rigor_level = 0
        else:
            rigor_ratio = rigor_ct / max(total_actions, 1)
            if rigor_ratio < 0.20:
                rigor_level = 1
            elif rigor_ratio < 0.50:
                rigor_level = 2
            else:
                rigor_level = 3

        if is_hard or is_avg or is_near_best:
            updates = agent.kaleidoscope.learn_from_history(
                episode_history,
                episode_score=total_score,
                episode_avg_dark=avg_dark,
                coherent_flag=True
            )
            print(f"Episode {ep+1}: Coherent run. Score: {total_score:.0f}. (KS updates: {updates})")
        else:
            # still try to learn from *clean* dissonant runs
            # i.e. only store states whose step_dark < episode avg
            clean_history = [(o, a, d) for (o, a, d) in episode_history if d <= avg_dark]
            if len(clean_history) > 0:
                updates = agent.kaleidoscope.learn_from_history(
                    clean_history,
                    episode_score=total_score,
                    episode_avg_dark=avg_dark,
                    coherent_flag=False
                )
            else:
                updates = 0
            print(f"Episode {ep+1}: Dissonant run. Score: {total_score:.0f}. Harvested: {updates} low-residue states.")

        print(
            f"    Avg Dark Residue: {avg_dark:.2f} (max {max_dark:.2f}) | "
            f"Vigor/Rigor: {vigor_ct}/{rigor_level}"
        )
        print(
            f"    Top-{len(top_scores)} scores: {top_scores} | avg={avg_top:.2f} | dyn_threshold={dyn_threshold}"
        )

    print("Training complete.")
    agent.sac_agent.save("pirouette_sac_model_destroyer")
    env.close()


if __name__ == "__main__":
    main()
