#!/usr/bin/env python3
"""
Wendigo-Minimalist v7: Pirouette SAC Agent with Shadow + Manifold
-----------------------------------------------------------------
An agent learning from a multi-objective reward signal that balances:
1. A drive to survive (Duration Bonus)
2. An aversion to instability (Dissonance Penalty)
3. A drive for active correction (Coherence Gain)
4. A drive for contrast & escape from shadow basins (ShadowContrastEngine)
5. A FIT-style manifold analyzer that records the reward geometry of the task.
"""

import gymnasium as gym
import numpy as np
from stable_baselines3 import SAC
# Note: 'configure' was imported but never used.
# from stable_baselines3.common.logger import configure
import matplotlib.pyplot as plt
# Note: 'defaultdict' was imported but never used.
# from collections import defaultdict
from typing import Dict, Callable, Tuple  # <-- ADDED

# ---------------------------------------------------------------------------
# Global Shaping Constants
# ---------------------------------------------------------------------------
gamma_coherence = 1.5     # <-- ADDED: Reward for reducing DR
delta_dissonance = 1.0   # <-- ADDED: Penalty for existing DR

# ---------------------------------------------------------------------------
# Reward programs: each is a function that maps metric dict -> scalar reward
# Metrics keys:
#   env_reward, coherence_gain, contrast_bonus, dissonance_penalty, shadow_penalty
# ---------------------------------------------------------------------------

def rp_env_only(m):
    return m["env_reward"]

def rp_env_plus_coherence(m):
    return m["env_reward"] + 0.4 * m["coherence_gain"]

def rp_contrast_hunter(m):
    # Strongly chase contrast, keep an eye on coherence, penalize dissonance
    return (
        m["env_reward"]
        + 0.2 * m["coherence_gain"]
        + 0.8 * m["contrast_bonus"]
        - 0.2 * m["dissonance_penalty"]
    )

def rp_shadow_avoidant(m):
    # Try to keep the system "smooth" and avoid shadow penalties
    return (
        m["env_reward"]
        + 0.2 * m["coherence_gain"]
        - 0.4 * m["dissonance_penalty"]
        - 0.8 * m["shadow_penalty"]
    )

def rp_explorer(m):
    # Very exploratory, values contrast and even a bit of dissonance to escape minima
    return (
        m["env_reward"]
        + 0.1 * m["coherence_gain"]
        + 1.0 * m["contrast_bonus"]
        + 0.2 * m["dissonance_penalty"]
        - 0.2 * m["shadow_penalty"]
    )

REWARD_PROGRAMS = {
    "env_only": rp_env_only,
    "env_plus_coherence": rp_env_plus_coherence,
    "contrast_hunter": rp_contrast_hunter,
    "shadow_avoidant": rp_shadow_avoidant,
    "explorer": rp_explorer,
}

# --------------------------------------------------------------------
# Manifold Analyzer (FIT-style, adapted for Wendigo)
# --------------------------------------------------------------------

class MetaRewardOrgan:
    """
    Autopoietic 'organ' that:
      - Starts with an ablation-style bootstrap over reward programs
      - Periodically re-evaluates them
      - Uses curiosity so it doesn't get stuck on a single profile
    """

    def __init__(
        self,
        programs: Dict[str, Callable],
        initial_program: str = "env_only",
        meta_interval: int = 30,
        eval_episodes: int = 3,
        dr_weight: float = 0.1,
        curiosity_coef: float = 5.0,
    ):
        self.programs = programs
        self.current_name = initial_program
        self.meta_interval = meta_interval
        self.eval_episodes = eval_episodes
        self.dr_weight = dr_weight
        self.curiosity_coef = curiosity_coef

        self.episode_counter = 0
        self.global_best_score = -np.inf

        # Track usage and performance per program
        self.stats = {
            name: {
                "n": 0,
                "mean_env": 0.0,
                "mean_dr": 0.0,
                "last_score": -np.inf,
            }
            for name in programs.keys()
        }
        self.program_usage = {name: 0 for name in programs.keys()}

        self._bootstrapped = False

    # --- main interface used by the training loop ---

    def compute_reward(self, metrics: Dict[str, float]) -> float:
        """Apply the current reward program."""
        return self.programs[self.current_name](metrics)

    def on_episode_end(self, env_return: float, avg_dr: float):
        """Called at the end of every episode."""
        self.episode_counter += 1

        st = self.stats[self.current_name]
        st["n"] += 1
        # online update for means
        st["mean_env"] += (env_return - st["mean_env"]) / st["n"]
        st["mean_dr"] += (avg_dr - st["mean_dr"]) / st["n"]

        self.program_usage[self.current_name] += 1

    def should_meta_update(self) -> bool:
        # First time: run bootstrap as soon as we have some steps
        if not self._bootstrapped and self.episode_counter >= self.meta_interval:
            return True
        # After that: periodic meta updates
        return self.episode_counter > 0 and self.episode_counter % self.meta_interval == 0

    def run_meta_update(self, agent: SAC, make_eval_env: Callable[[], gym.Env]):
        """
        Meta-step:
          - If first time: ablation bootstrap (3 runs per program)
          - Thereafter: re-evaluate all programs, combining env_return & DR & curiosity
        """
        print("[MetaOrgan] Running meta-update...")
        if not self._bootstrapped:
            self._bootstrap_via_ablation(agent, make_eval_env)
            self._bootstrapped = True
        else:
            self._reevaluate_programs(agent, make_eval_env)

        print(f"[MetaOrgan] Active program: {self.current_name}")

    # --- internals ---

    def _bootstrap_via_ablation(self, agent: SAC, make_eval_env: Callable[[], gym.Env]):
        """
        Do an initial ablation: each reward program gets eval_episodes runs from the
        same unmodified agent. We pick the one with the best env-return - dr_weight * DR
        plus a curiosity bonus for underused programs.
        """
        best_name = self.current_name
        best_score = -np.inf

        for name in self.programs.keys():
            env_mean, dr_mean = self._evaluate_program(agent, make_eval_env, name)
            score = env_mean - self.dr_weight * dr_mean
            self.stats[name]["last_score"] = score

            # curiosity: prefer programs we've used less
            curiosity = self.curiosity_coef / np.sqrt(1.0 + self.program_usage[name])
            total_score = score + curiosity

            print(
                f"[MetaOrgan][Bootstrap] {name}: env={env_mean:.2f}, DR={dr_mean:.3f}, "
                f"score={score:.2f}, curiosity={curiosity:.2f}, total={total_score:.2f}"
            )

            if total_score > best_score:
                best_score = total_score
                best_name = name

        self.current_name = best_name
        self.global_best_score = best_score
        print(
            f"[MetaOrgan][Bootstrap] Selected program '{best_name}' "
            f"with score={best_score:.2f}"
        )

    def _reevaluate_programs(self, agent: SAC, make_eval_env: Callable[[], gym.Env]):
        best_name = self.current_name
        best_score = self.global_best_score

        for name in self.programs.keys():
            env_mean, dr_mean = self._evaluate_program(agent, make_eval_env, name)
            score = env_mean - self.dr_weight * dr_mean
            self.stats[name]["last_score"] = score

            curiosity = self.curiosity_coef / np.sqrt(1.0 + self.program_usage[name])
            total_score = score + curiosity

            print(
                f"[MetaOrgan][Reeval] {name}: env={env_mean:.2f}, DR={dr_mean:.3f}, "
                f"score={score:.2f}, curiosity={curiosity:.2f}, total={total_score:.2f}"
            )

            # Only change programs if we beat global best: avoid overwriting a good regime
            if total_score > best_score:
                best_score = total_score
                best_name = name

        if best_name != self.current_name:
            print(
                f"[MetaOrgan] Switching program {self.current_name} -> {best_name} "
                f"(score improved from {self.global_best_score:.2f} to {best_score:.2f})"
            )
            self.current_name = best_name
            self.global_best_score = best_score
        else:
            print(
                f"[MetaOrgan] No better program found; staying with {self.current_name}. "
                f"(global_best={self.global_best_score:.2f})"
            )

    def _evaluate_program(
        self, agent: SAC, make_eval_env: Callable[[], gym.Env], program_name: str
    ) -> Tuple[float, float]:
        """
        Short eval: run eval_episodes episodes with the given reward program
        (NO training) and report mean env_return and mean DR.
        """
        env_returns = []
        dr_means = []
        beta_duration = 0.05

        program = self.programs[program_name]
        # <-- ADDED: Must instantiate the engine
        sc_engine = ShadowContrastEngine() 

        for _ in range(self.eval_episodes):
            env = make_eval_env()
            obs, _ = env.reset()
            done = False
            trunc = False

            ep_env_return = 0.0
            dr_sum = 0.0
            steps = 0

            last_dr = calculate_dark_residue(obs)

            while not (done or trunc):
                action, _ = agent.predict(obs, deterministic=True)
                obs_next, env_r, done, trunc, info = env.step(action)

                current_dr = calculate_dark_residue(obs_next)
                delta_dr = current_dr - last_dr

                # re-derive shaping components
                coh = -gamma_coherence * delta_dr  # reward coherence if DR goes down
                
                # <-- FIXED: Call instance method with (last_dr, current_dr)
                contrast_bonus, shadow_penalty, sc_info = sc_engine.compute(
                    last_dr, current_dr
                )
                disson_penalty = delta_dissonance * current_dr

                metrics = {
                    "env_reward": beta_duration,
                    "coherence_gain": float(coh),
                    "contrast_bonus": float(contrast_bonus),
                    "dissonance_penalty": float(disson_penalty),
                    "shadow_penalty": float(shadow_penalty),
                }

                _ = program(metrics)  # we don't need the shaped reward, only env+DR
                ep_env_return += env_r
                dr_sum += current_dr
                steps += 1

                obs = obs_next
                last_dr = current_dr # <-- ADDED: Update last_dr for next step

            env_returns.append(ep_env_return)
            dr_means.append(dr_sum / max(1, steps))

        return float(np.mean(env_returns)), float(np.mean(dr_means))


class ManifoldAnalyzer:
    """
    Aggregates per-step metrics into a 2D task manifold.

    - rows: named channels (e.g. env, coherence, contrast, dissonance, shadow, total)
    - cols: time steps in episode [0, max_steps)
    - stores running sums + counts so you get an average manifold
      over all episodes without keeping every episode in memory.
    """
    def __init__(self, max_steps, channel_names):
        self.max_steps = max_steps
        self.channel_names = channel_names
        self.n_channels = len(channel_names)

        # running sums and counts
        self.sums = np.zeros((self.n_channels, self.max_steps), dtype=np.float32)
        self.counts = np.zeros(self.max_steps, dtype=np.int32)

    def log_step(self, t, metrics_dict):
        """
        t: integer time index in [0, max_steps)
        metrics_dict: {channel_name: value}
        """
        if t < 0 or t >= self.max_steps:
            return  # ignore overflow just in case

        for i, name in enumerate(self.channel_names):
            v = metrics_dict.get(name, None)
            if v is not None:
                self.sums[i, t] += float(v)

        # we treat 'time t was visited' as one sample
        self.counts[t] += 1

    def get_manifold(self):
        # avoid division by zero
        counts_safe = np.maximum(self.counts, 1)
        manifold = self.sums / counts_safe[None, :]
        return manifold

    def save_engram(self, npy_path="wendigo_task_manifold.npy"):
        manifold = self.get_manifold()
        np.save(npy_path, manifold)
        return npy_path

    def plot_heatmap(self, png_path="wendigo_task_manifold.png",
                     title="Wendigo Task Manifold"):
        manifold = self.get_manifold()

        fig, ax = plt.subplots(figsize=(10, 6))
        im = ax.imshow(
            manifold,
            aspect='auto',
            origin='lower',
            interpolation='nearest'
        )
        ax.set_title(title)
        ax.set_xlabel("Time step in episode")
        ax.set_yticks(np.arange(self.n_channels))
        ax.set_yticklabels(self.channel_names)
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label("Average value")

        fig.tight_layout()
        plt.savefig(png_path, dpi=150)
        plt.close(fig)
        return png_path


# --------------------------------------------------------------------
# Shadow Contrast Engine (from previous step)
# --------------------------------------------------------------------

class ShadowContrastEngine:
    """
    Contrast = |ΔDR|         (how much the system changed)
    Shadow   = DR with low |ΔDR|
               (stuck in dissonant, low-gradient regions)

    We add:
      + lambda_contrast * |ΔDR|
      - lambda_shadow   * shadow_mask * DR
    to the reward.
    """

    def __init__(
        self,
        lambda_contrast: float = 0.5,
        lambda_shadow: float = 0.25,
        shadow_grad_eps: float = 1e-3,
        shadow_dr_threshold: float = 0.10,
    ):
        self.lambda_contrast = lambda_contrast
        self.lambda_shadow = lambda_shadow
        self.shadow_grad_eps = shadow_grad_eps
        self.shadow_dr_threshold = shadow_dr_threshold

    def compute(self, previous_dr: float, current_dr: float):
        """
        Returns (contrast_bonus, shadow_penalty, info_dict)
        """
        # Temporal contrast in dark residue
        dr_diff = current_dr - previous_dr
        contrast = abs(dr_diff)

        # "Shadow" = high DR but very small gradient
        in_shadow = (contrast < self.shadow_grad_eps) and (
            current_dr > self.shadow_dr_threshold
        )

        contrast_bonus = self.lambda_contrast * contrast
        shadow_penalty = self.lambda_shadow * current_dr if in_shadow else 0.0

        info = {
            "dr_diff": dr_diff,
            "contrast": contrast,
            "in_shadow": in_shadow,
            "shadow_penalty": shadow_penalty,
            "contrast_bonus": contrast_bonus,
        }
        return contrast_bonus, shadow_penalty, info


# --------------------------------------------------------------------
# Env wrapper + DR definition
# --------------------------------------------------------------------

class DiscreteToBoxActionWrapper(gym.ActionWrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(
            low=-1.0, high=1.0, shape=(1,), dtype=np.float32
        )

    def action(self, action: np.ndarray) -> int:
        return 0 if action[0] < 0.0 else 1


def calculate_dark_residue(obs: np.ndarray) -> float:
    if obs is None or len(obs) < 4:
        return 0.0 # Handle potential edge case at reset
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    return (
        0.4 * abs(cart_pos)
        + 0.2 * abs(cart_vel)
        + 1.5 * abs(pole_angle)
        + 0.3 * abs(pole_vel)
    )


# --------------------------------------------------------------------
# Simple training curves plot
# --------------------------------------------------------------------

def plot_training(scores, manifold_analyzer: ManifoldAnalyzer):
    # Save & plot manifold first
    manifold_png = manifold_analyzer.plot_heatmap(
        png_path="wendigo_task_manifold.png",
        title="Wendigo Task Manifold (Avg over episodes)",
    )
    manifold_npy = manifold_analyzer.save_engram(
        npy_path="wendigo_task_manifold.npy"
    )
    print(f"\n[Manifold] Heatmap saved to: {manifold_png}")
    print(f"[Manifold] Engram saved to:  {manifold_npy}")

    # Then plot episode scores
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(np.arange(1, len(scores) + 1), scores, linewidth=2)
    ax.set_xlabel("Episode")
    ax.set_ylabel("Episode Score (steps survived)")
    ax.set_title("Wendigo Training Curve")
    ax.grid(True)
    score_png = "wendigo_training_scores.png"
    plt.tight_layout()
    plt.savefig(score_png, dpi=150)
    plt.close(fig)
    print(f"[Training] Score curve saved to: {score_png}")

def build_metrics(
    env_r: float,
    coherence_gain: float,
    contrast_bonus: float,
    dissonance_penalty: float,
    shadow_penalty: float,
) -> Dict[str, float]:
    return {
        "env_reward": float(env_r),
        "coherence_gain": float(coherence_gain),
        "contrast_bonus": float(contrast_bonus),
        "dissonance_penalty": float(dissonance_penalty),
        "shadow_penalty": float(shadow_penalty),
    }


# --------------------------------------------------------------------
# Main Wendigo training loop
# --------------------------------------------------------------------

def main():
    # --- env / agent setup ---
    env = DiscreteToBoxActionWrapper(gym.make("CartPole-v1"))
    agent = SAC(
        "MlpPolicy",
        env,
        verbose=0,
        train_freq=(1, "step"),
        buffer_size=50_000,
        learning_rate=3e-4,
        tau=0.02,
        gamma=0.99,
        batch_size=256,
        learning_starts=10000
    )

    def make_eval_env():
        return DiscreteToBoxActionWrapper(gym.make("CartPole-v1"))

    # --- autopoietic organ using reward programs ---
    organ = MetaRewardOrgan(
        programs=REWARD_PROGRAMS,
        initial_program="env_plus_coherence",
        meta_interval=30,      # episodes between meta-updates
        eval_episodes=3,       # your "3 runs per parameter"
        dr_weight=0.1,         # how strongly to penalize DR
        curiosity_coef=5.0,    # how aggressive curiosity is
    )

    # --- Manifold setup ---
    # <-- MOVED UP & FIXED
    num_episodes = 200
    max_steps = 500
    beta_duration = 0.05
    manifold_channels = [
        "env_reward",
        "coherence_gain",
        "contrast_bonus",
        "dissonance_penalty",
        "shadow_penalty",
        "shaped_reward", # <-- ADDED
    ]
    manifold = ManifoldAnalyzer(
        max_steps=max_steps, 
        channel_names=manifold_channels
    ) # <-- FIXED
    
    # --- Shadow Engine setup ---
    sc_engine = ShadowContrastEngine() # <-- ADDED

    scores = []

    for ep in range(1, num_episodes + 1):
        obs, _ = env.reset()
        done = False
        trunc = False

        last_dr = calculate_dark_residue(obs)
        ep_return = 0.0
        dr_sum = 0.0
        steps = 0

        for step in range(max_steps):
            if done or trunc:
                break

            action, _ = agent.predict(obs, deterministic=False)
            obs_next, env_r, done, trunc, info = env.step(action)

            current_dr = calculate_dark_residue(obs_next)
            delta_dr = current_dr - last_dr

            # shaping components
            coherence_gain = -gamma_coherence * delta_dr
            
            # <-- FIXED: Call instance method with (last_dr, current_dr)
            contrast_bonus, shadow_penalty, sc_info = sc_engine.compute(
                last_dr, current_dr
            )
            dissonance_penalty = delta_dissonance * current_dr

            metrics = build_metrics(
                beta_duration,
                coherence_gain,
                contrast_bonus,
                dissonance_penalty,
                shadow_penalty,
            )
            shaped_r = organ.compute_reward(metrics)

            # log manifold channels
            metrics["shaped_reward"] = shaped_r # <-- ADDED
            manifold.log_step(
                step, # <-- FIXED
                metrics # <-- FIXED
            )

            # train on shaped reward
            # Note: SB3 SAC expects rewards and dones as lists/arrays
            agent.replay_buffer.add(
                obs,
                obs_next,
                action,
                np.array([shaped_r], dtype=np.float32), # <-- Ensured array
                np.array([done], dtype=np.float32),     # <-- Ensured array
                [info],
            )
            # This logic is for SB3 < 2.0
            # For SB3 >= 2.0, use:
            # agent.replay_buffer.add(
            #     obs,
            #     obs_next,
            #     action,
            #     shaped_r,
            #     done,
            #     [info],
            # )

            # Check if buffer is full enough to train
            if agent.num_timesteps > agent.learning_starts:
                 agent.train(gradient_steps=agent.gradient_steps)

            ep_return += env_r
            dr_sum += current_dr
            steps += 1
            obs = obs_next
            last_dr = current_dr # <-- ADDED: Update last_dr for next step

        avg_dr = dr_sum / max(1, steps)
        scores.append(ep_return)
        organ.on_episode_end(ep_return, avg_dr)
        
        # Calculate mean of the last 15 scores
        last_15_mean = np.mean(scores[-15:])
        print(f"Episode {ep:03d}: Score={ep_return:.0f} | Avg-Top15={last_15_mean:.2f} | Program={organ.current_name}")


        if organ.should_meta_update():
            agent.save("wendigo_checkpoint") # Save agent before meta-update
            organ.run_meta_update(agent, make_eval_env)

    # finalize plots
    print("\nTraining complete. Generating final plots...")
    # <-- FIXED: Pass manifold object, not string. Removed redundant plot call.
    plot_training(scores, manifold) 
    agent.save("wendigo_final")
    print("Final model saved to wendigo_final.zip")


if __name__ == "__main__":
    main()