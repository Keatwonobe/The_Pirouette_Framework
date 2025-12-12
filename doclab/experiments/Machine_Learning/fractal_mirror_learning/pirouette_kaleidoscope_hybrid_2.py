import gymnasium as gym
import numpy as np
import time
from stable_baselines3 import SAC
from stable_baselines3.common.buffers import ReplayBuffer
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.logger import configure
import torch as th

# --- SDE DEVICE HOTFIX (SB3) ---
from stable_baselines3.common.distributions import StateDependentNoiseDistribution

_old_get_noise = StateDependentNoiseDistribution.get_noise

def _get_noise_on_same_device(self, latent_sde: th.Tensor) -> th.Tensor:
    # make sure exploration_mat lives where latent_sde lives
    if isinstance(self.exploration_mat, th.Tensor):
        if self.exploration_mat.device != latent_sde.device:
            self.exploration_mat = self.exploration_mat.to(latent_sde.device)
    # some SB3 versions keep a list of mats
    if hasattr(self, "exploration_matrices") and isinstance(self.exploration_matrices, list):
        new_mats = []
        for m in self.exploration_matrices:
            if isinstance(m, th.Tensor) and m.device != latent_sde.device:
                m = m.to(latent_sde.device)
            new_mats.append(m)
        self.exploration_matrices = new_mats
    return _old_get_noise(self, latent_sde)

StateDependentNoiseDistribution.get_noise = _get_noise_on_same_device
# --- END HOTFIX ---


# --- Part 1: The Kaleidoscope (Vigor) ---
# This is our "solver table" for proven, coherent engrams.
# We've adapted it from the previous file.

class KaleidoscopeMemory:
    """
    This is the "Vigor" engine.
    It stores and retrieves "Generative Engrams" (proven solutions).
    """
    def __init__(self):
        # The "graph of engrams" or "solver table."
        self.kaleidoscope = {}
        self.genetic_lineage = []
        
        # "Engram Simplification" Bins
        self.pos_bins = np.linspace(-2.4, 2.4, 10)
        self.vel_bins = np.linspace(-4, 4, 10)
        self.angle_bins = np.linspace(-0.209, 0.209, 10)
        self.angle_vel_bins = np.linspace(-4, 4, 10)
        
    def record_genetic_run(self, score, source="from-average"):
        self.genetic_lineage.append(
            {"score": score, "source": source, "timestamp": time.time()}
        )
        # keep it small
        if len(self.genetic_lineage) > 200:
            self.genetic_lineage = self.genetic_lineage[-200:]

    def discretize_state(self, obs):
        """ The "Engram Simplification" function. """
        cart_pos, cart_vel, pole_angle, pole_vel = obs
        
        pos_idx = np.digitize(cart_pos, self.pos_bins)
        vel_idx = np.digitize(cart_vel, self.vel_bins)
        angle_idx = np.digitize(pole_angle, self.angle_bins)
        angle_vel_idx = np.digitize(pole_vel, self.angle_vel_bins)
        
        return (pos_idx, vel_idx, angle_idx, angle_vel_idx)

    def get_known_action(self, obs):
        """
        Checks for a "resonant loop" (a known engram).
        Returns the action if found, else None.
        """
        engram_key = self.discretize_state(obs)
        return self.kaleidoscope.get(engram_key, None)

    def learn_from_history(self, episode_history):
        """
        "Formular Induction."
        Weaves a *successful* episode into the Kaleidoscope.
        """
        count = 0
        for obs, action in episode_history:
            engram_key = self.discretize_state(obs)
            
            # We must convert the SAC's continuous action [-1, 1] to a discrete one [0, 1]
            discrete_action = 0 if action[0] < 0 else 1
            
            if engram_key not in self.kaleidoscope:
                self.kaleidoscope[engram_key] = discrete_action
                count += 1
        return count

# --- Part 2: The Dark Residue Metric ---

def calculate_dark_residue(obs):
    """
    Calculates the "Dark Residue" (D) for a given state.
    This is our cost function, based on DARK_RESIDUE.md.
    We want to MINIMIZE this.
    """
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    
    # Define weights for the different components of "D"
    w_angle = 1.0  # Risk of falling
    w_pole_vel = 0.5 # Loss of control
    w_cart_vel = 0.1 # Wasted energy / "attention debt"
    
    # Calculate the Dark Residue
    residue = (
        w_angle * abs(pole_angle) +
        w_pole_vel * abs(pole_vel) +
        w_cart_vel * abs(cart_vel)
    )
    return residue

# --- Part 3: The Hybrid Agent (Rigor + Vigor) ---

class HybridPirouetteAgent:
    """
    This agent combines the "Rigor" of an exploratory SAC agent
    with the "Vigor" of the Kaleidoscope's proven memory.
    """
    def __init__(self, env, device): # <-- Add device here
        self.env = env
        self.device = device # <-- Store device
        
        # 1. The "Vigor" Engine
        self.kaleidoscope = KaleidoscopeMemory()
        
        # 2. The "Rigor" Engine
        # SAC is designed for continuous actions (like force on the cart)
        # We'll use a continuous action space: Box(low=-1.0, high=1.0)
        policy_kwargs = dict(net_arch=[64, 64])
        self.sac_agent = SAC(
            "MlpPolicy",
            env,
            policy_kwargs=policy_kwargs,
            verbose=0,
            learning_starts=1000, # Start learning after 1000 steps
            use_sde=False, # State-dependent exploration
            tensorboard_log="./sac_pirouette_log/",
            device=self.device # <-- FIX: Tell SAC which device to use
        )
        

        # --- force SDE buffers onto the right device ---
        if getattr(self.sac_agent.policy, "use_sde", False):
            dist = self.sac_agent.policy.action_dist
            # main offender:
            dist.exploration_mat = dist.exploration_mat.to(self.device)
            # some SB3 versions also keep epsilon / log_std as tensors
            if hasattr(dist, "epsilon") and isinstance(dist.epsilon, th.Tensor):
                dist.epsilon = dist.epsilon.to(self.device)
            if hasattr(dist, "log_std") and isinstance(dist.log_std, th.Tensor):
                dist.log_std = dist.log_std.to(self.device)
        # ------------------------------------------------

        self.sac_agent._setup_model()

        # (2) HARD-SET a logger, because your SB3 isn’t giving you one
        if not hasattr(self.sac_agent, "_logger") or self.sac_agent._logger is None:
            # you can point this at a folder or leave it in-memory
            self.sac_agent._logger = configure(
             folder="./sac_pirouette_log/",
                format_strings=[],     # or ["stdout"] if you want prints
            )

        # 3. The Replay Buffer for continuous learning
        self.replay_buffer = ReplayBuffer(
            buffer_size=100_000,
            observation_space=self.env.observation_space,
            action_space=self.env.action_space,
            device=self.device, # <-- FIX: Tell the buffer which device to use
            n_envs=1
        )
        
        self.sac_agent.replay_buffer = self.replay_buffer

        self.total_steps = 0
        self.batch_size = 128

    def choose_action(self, obs):
        """
        The hybrid "heartbeat."
        Tries "Vigor" (Kaleidoscope) first, then "Rigor" (SAC).
        """
        # 1. Try "Vigor"
        known_action = self.kaleidoscope.get_known_action(obs)
        if known_action is not None:
            # A "coherent engram" was found!
            # Convert discrete action [0, 1] to continuous [-1, 1] for the env
            # This is a hack for this env; a real one would be more complex
            continuous_action = np.array([-1.0]) if known_action == 0 else np.array([1.0])
            return continuous_action, "Vigor"
            
        # 2. Try "Rigor"
        # No engram found. Ask the SAC agent to "propose" an action.

        # --- MANUAL BATCHING FIX ---
        # The `predict` function (esp. with SDE) is more robust
        # when it receives a batched observation.
        # We reshape the obs from (4,) to (1, 4).
        obs_batched = obs.reshape(1, -1)
        
        # Get the batched action
        action_batched, _states = self.sac_agent.predict(obs_batched, deterministic=False)
        
        # Unbatch the action from (1, 1) to (1,) for the env wrapper
        action_unbatched = action_batched[0]
        
        return action_unbatched, "Rigor"

    def learn(self, obs, action, next_obs, reward, done):
        self.total_steps += 1

        # 1) add transition to OUR buffer (SB3 is sharing it now)
        self.replay_buffer.add(
            obs,
            next_obs,
            action,
            reward,
            done,
            [{}],  # infos
        )

        # 2) only start training after warmup, and not every step
        if (
            self.total_steps > self.sac_agent.learning_starts
            and self.replay_buffer.size() > self.batch_size
            and self.total_steps % 50 == 0
        ):
            # make sure model is fully set up
            if not hasattr(self.sac_agent, "_logger") or self.sac_agent._logger is None:
                self.sac_agent._setup_model()
                if not hasattr(self.sac_agent, "_logger") or self.sac_agent._logger is None:
                    self.sac_agent._logger = configure(
                        folder="./sac_pirouette_log/",
                        format_strings=[],
                    )

        # 3) **this** is the correct call shape for your SB3:
        self.sac_agent.train(gradient_steps=1, batch_size=self.batch_size)



class ContinuousActionWrapper(gym.ActionWrapper):
    """
    Converts a discrete environment (like CartPole-v1)
    into a single continuous action dimension in [-1, 1].
    """
    def __init__(self, env):
        super().__init__(env)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

    def action(self, action):
        # Map continuous [-1, 1] → discrete action {0, 1}
        return 0 if action[0] < 0 else 1


# --- Main Training Loop ---

def main():
    device_name = "cuda" if th.cuda.is_available() else "cpu"
    device = th.device(device_name)
    print("Initializing Pirouette Hybrid (SAC + Kaleidoscope) Agent...")
    print(f"Using device: {device_name}")

    # env setup
    base_env = gym.make("CartPole-v1")
    env = ContinuousActionWrapper(base_env)

    agent = HybridPirouetteAgent(env, device)

    num_episodes = 800
    coherence_threshold = 150          # hard gate
    top_k = 10                         # keep top 10 runs
    top_scores = []                    # rolling leaderboard
    avg_margin = 5                     # “above average” margin in points

    print("Starting Hybrid 'Formular Induction' (Learning)...")

    for i in range(num_episodes):
        obs, info = env.reset()

        episode_history = []
        total_score = 0
        total_dark_residue = 0
        vigor_actions = 0
        rigor_actions = 0

        terminated = False
        truncated = False

        while not terminated and not truncated:
            action, mode = agent.choose_action(obs)
            if mode == "Vigor":
                vigor_actions += 1
            else:
                rigor_actions += 1

            next_obs, reward, terminated, truncated, info = env.step(action)

            # “dark residue” just for your printouts
            dark_residue = float(np.abs(reward - 1.0))
            total_dark_residue += dark_residue

            # store transition for SAC
            agent.learn(obs, action, next_obs, reward, terminated or truncated)

            # store for vigor
            episode_history.append((obs, action))

            obs = next_obs
            total_score += reward

        # --- NEW: compute current leaderboard average (before inserting current run) ---
        if len(top_scores) > 0:
            avg_top = sum(top_scores) / len(top_scores)
        else:
            avg_top = 0.0

        is_hard_coherent = total_score >= coherence_threshold
        is_avg_coherent = (total_score >= avg_top + avg_margin) and (total_score >= 10)

        # --- NOW update leaderboard with the current run ---
        top_scores.append(int(total_score))
        top_scores = sorted(top_scores, reverse=True)[:top_k]

        if is_hard_coherent or is_avg_coherent:
            agent.kaleidoscope.record_genetic_run(total_score, source="from-average")
            new_engrams = agent.kaleidoscope.learn_from_history(episode_history)
            mode_str = "threshold" if is_hard_coherent else "from-average"
            print(f"Episode {i+1}: Coherent run ({mode_str}). Score: {total_score:.0f}.")
            print(f"    Inducing formula... Wove {new_engrams} new states into Kaleidoscope.")
            print(f"    Kaleidoscope size: {len(agent.kaleidoscope.kaleidoscope)}")
        else:
            print(f"Episode {i+1}: Dissonant run. Score: {total_score:.0f}. Discarding history.")

        # always print the coherence baseline so you can watch it evolve
        print(
            f"    Avg Dark Residue: {total_dark_residue / max(total_score, 1):.2f} | "
            f"Vigor/Rigor: {vigor_actions}/{rigor_actions}"
        )
        print(
            f"    Top-{len(top_scores)} scores: {top_scores} | avg={avg_top:.2f} | margin={avg_margin}"
        )

    print("Training complete.")
    agent.sac_agent.save("pirouette_sac_model")
    env.close()


if __name__ == "__main__":
    main()


