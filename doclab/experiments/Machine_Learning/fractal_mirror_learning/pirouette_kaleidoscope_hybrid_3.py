import gymnasium as gym
import numpy as np
import time
from stable_baselines3 import SAC
from stable_baselines3.common.buffers import ReplayBuffer
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.logger import configure
import torch as th
import collections

# --- SDE DEVICE HOTFIX (SB3) ---
# This is a common issue with SB3 and SDE on CUDA. This patch
# ensures the SDE noise matrix is moved to the correct device.
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
# --- END SDE HOTFIX ---


# --- Part 1: The Kaleidoscope (Vigor) ---
# This is our "solver table" for proven, coherent engrams.

class KaleidoscopeMemory:
    """
    This is the "Vigor" engine.
    It stores and retrieves "Generative Engrams" (proven solutions).
    """
    def __init__(self):
        # The "graph of engrams" or "solver table."
        # Stores: key -> (action, score, source)
        self.kaleidoscope = {}
        
        # "Engram Simplification" Bins
        self.pos_bins = np.linspace(-2.4, 2.4, 10)
        self.vel_bins = np.linspace(-4, 4, 10)
        self.angle_bins = np.linspace(-0.209, 0.209, 10)
        self.angle_vel_bins = np.linspace(-4, 4, 10)
        
        # Metadata to track our engrams
        self.genetic_lineage = collections.defaultdict(int)

    def discretize_state(self, obs):
        """ The "Engram Simplification" function. """
        cart_pos, cart_vel, pole_angle, pole_vel = obs
        
        pos_idx = np.digitize(cart_pos, self.pos_bins)
        vel_idx = np.digitize(cart_vel, self.vel_bins)
        angle_idx = np.digitize(pole_angle, self.angle_bins)
        angle_vel_idx = np.digitize(pole_vel, self.angle_vel_bins)
        
        return (pos_idx, vel_idx, angle_idx, angle_vel_idx)

    def get_engram(self, obs):
        """ Retrieves a proven action from the "solver table". """
        engram_key = self.discretize_state(obs)
        return self.kaleidoscope.get(engram_key)

    def learn_from_history(self, episode_history):
        """
        Performs "Formular Induction."
        Weaves a successful, coherent run into the Kaleidoscope.
        """
        count = 0
        
        # The history is (obs, action) pairs.
        # We also have the final score of this run.
        run_score = len(episode_history) 
        
        for (obs, action) in episode_history:
            engram_key = self.discretize_state(obs)
            
            # Check if this engram is already known
            existing_engram = self.kaleidoscope.get(engram_key)
            
            # Only add/overwrite if this new run is *better*
            # than the one we have in memory.
            if existing_engram is None or run_score > existing_engram[1]:
                self.kaleidoscope[engram_key] = (action, run_score, self.genetic_lineage[run_score])
                count += 1
        return count

    def record_genetic_run(self, score, source="unknown"):
        """ Records the 'parentage' of a successful run """
        self.genetic_lineage[score] += 1

# --- Part 2: The Dark Residue Metric ---
# We are not using this for the reward, but we can still print it.
def calculate_dark_residue(obs):
    """
    Calculates the "cost" or "risk" of a given state.
    A simple proxy for the Pirouette Framework's D metric.
    """
    cart_pos, cart_vel, pole_angle, pole_vel = obs
    
    # Cost 1: Risk of falling (pole angle)
    # Scaled: 0 is good, 1 is max angle
    angle_cost = (abs(pole_angle) / 0.209) ** 2
    
    # Cost 2: Wasted energy / instability (velocities)
    # Scaled: 0 is still, 1 is max velocity
    cart_vel_cost = (abs(cart_vel) / 4.0)
    pole_vel_cost = (abs(pole_vel) / 4.0)
    
    # Cost 3: Risk of going out of bounds
    pos_cost = (abs(cart_pos) / 2.4) ** 2
    
    # Combine costs. We weight angle cost most heavily.
    residue = (0.6 * angle_cost + 
               0.1 * cart_vel_cost + 
               0.1 * pole_vel_cost + 
               0.2 * pos_cost)
    
    return residue / 4.0 # Normalize to [0, 1] range (roughly)


# --- Part 3: The Hybrid Agent (Rigor + Vigor) ---

class HybridPirouetteAgent:
    """
    Combines a "Rigor" engine (SAC) with a "Vigor" engine (Kaleidoscope).
    """
    def __init__(self, env, device):
        self.env = env
        self.device = device
        
        # 1. The "Vigor" Engine
        self.kaleidoscope = KaleidoscopeMemory()
        
        
        # 3. The "Rigor" Engine
        policy_kwargs = dict(
            use_sde=True, # State-Dependent Exploration (SDE)
            log_std_init=-2.0, # Initial exploration noise
            net_arch=[64, 64] # Smaller network
        )
        
        # SAC Model - This is the "Rigor" engine
        self.sac_agent = SAC(
            "MlpPolicy",
            env,
            policy_kwargs=policy_kwargs,
            verbose=0,
            learning_starts=5000, # "Dragster Tuning": Give SAC time to learn
            use_sde=True,
            tensorboard_log="./sac_pirouette_log/",
            device=self.device, # Pass the device
            # --- KEY FIX 1: Tell SAC to use OUR buffer ---
        )
        
        self.replay_buffer = self.sac_agent.replay_buffer

        # --- FIX FOR THE _logger ATTRIBUTE ERROR ---
        # Explicitly create and set the logger for the SAC agent
        # as you identified.
        new_logger = configure(self.sac_agent.tensorboard_log, ["stdout", "tensorboard"])
        self.sac_agent.set_logger(new_logger)
        # --- END FIX ---
        
        # 4. The Replay Buffer is now shared.
        # self.replay_buffer now points to the same object
        # as self.sac_agent.replay_buffer.
        
        self.total_steps = 0
        self.batch_size = 256

    def choose_action(self, obs):
        """
        The core of the framework.
        1. Try to use "Vigor" (memory).
        2. If no memory, use "Rigor" (propose a new solution).
        """
        
        # 1. Try "Vigor"
        # Is there a proven, coherent engram for this state?
        engram = self.kaleidoscope.get_engram(obs)
        if engram is not None:
            # Vigor success! Use the "solver table."
            continuous_action = engram[0] # Get the stored action
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

    def learn(self, obs, action, next_obs, reward, done, info):
        """
        This is the "Rigor" learning step.
        The SAC agent learns from every single step.
        """
        self.total_steps += 1
        
        # Add the experience to the SAC agent's "mind"
        # We MUST pass the `info` dictionary inside a list
        # because the buffer expects a list of infos (one for each env).
        self.replay_buffer.add(obs, next_obs, action, reward, done, [info])
        
        # Train the SAC agent if it's ready
        if self.total_steps > self.sac_agent.learning_starts:
            if self.total_steps % 32 == 0: # Train every 32 steps
                # --- KEY FIX 2: Call train() correctly ---
                # We are passing gradient_steps (an int), not the buffer.
                # We do 32 gradient steps since we only call this every 32 env steps.
                self.sac_agent.train(gradient_steps=32, batch_size=self.batch_size)


# --- Wrapper for Continuous -> Discrete Action ---
# SAC outputs a continuous action (e.g., -0.8 to 0.8), but CartPole
# in the standard model takes a discrete action (0 or 1).
# We'll use a continuous environment, but this wrapper shows how to adapt.
# *** UPDATE: We are using the *continuous* CartPole env, but
#     we still need a wrapper to handle the action *format*. ***
class ContinuousActionWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        # The SAC agent will output a continuous value in range [-1, 1]
        # We need to map this to the env's force range
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

    def step(self, action):
        # action is a numpy array like [-0.3] from the SAC agent
        # We convert this continuous action to the discrete 0 or 1
        # that the underlying CartPole-v1 environment expects.
        discrete_action = 1 if action[0] > 0 else 0
        
        # We pass the *discrete* action to the underlying env
        obs, reward, terminated, truncated, info = self.env.step(discrete_action)
        
        return obs, reward, terminated, truncated, info


# --- Main Training Loop ---

def main():
    # --- Device Detection ---
    device_name = "cuda" if th.cuda.is_available() else "cpu"
    device = th.device(device_name)
    print(f"Initializing Pirouette Hybrid (SAC + Kaleidoscope) Agent...")
    print(f"Using device: {device_name}")
    # -----------------------------
    
    # 1. Create the base environment
    # We remove the failing 'continuous=True'
    base_env = gym.make("CartPole-v1", render_mode=None) # or "human"
    
    # 2. Wrap it to "lie" to SAC
    # This wrapper tells SAC the action space is continuous...
    # ...but secretly converts its continuous output to discrete 0/1.
    env = ContinuousActionWrapper(base_env)
    
    agent = HybridPirouetteAgent(env, device=device)
    
    num_episodes = 2000
    
    # --- "Dragster Tuning" ---
    # We make the Kaleidoscope *pickier*.
    # It only learns from "A+" runs.
    coherence_threshold = 300 # Only learn from scores > 300
    
    # We will also add a "genetic" coherence based on the
    # average of the best runs, so it can self-tune.
    top_k = 10
    top_scores = collections.deque(maxlen=top_k)
    avg_margin = 5 # How much better than avg to be "coherent"
    
    print("Starting Hybrid 'Formular Induction' (Learning)...")
    
    for i in range(num_episodes):
        obs, info = env.reset()
        done = False
        truncated = False
        
        episode_history = []
        total_score = 0
        total_dark_residue = 0
        vigor_actions = 0
        rigor_actions = 0

        while not done and not truncated:
            # 1. Choose action from Hybrid Agent
            action, mode = agent.choose_action(obs)
            
            if mode == "Vigor":
                vigor_actions += 1
            else:
                rigor_actions += 1
            
            # 2. Take action in environment
            # We pass the raw continuous action (e.g., [-0.3])
            # to our wrapper. The wrapper will handle conversion.
            next_obs, reward, terminated, truncated, info = env.step(action)
            
            # 3. Calculate Dark Residue
            dark_residue = calculate_dark_residue(obs)
            
            # 4. Define Reward for SAC agent ("Rigor" engine)
            # "Dragster Tuning": Give a *huge* penalty for failure.
            # This is the *real* "Dark Residue."
            sac_reward = 1.0 # "Living reward"
            if terminated:
                sac_reward = -100.0 # "Failure penalty"
            
            # 5. Continuous Learning (Rigor)
            # The SAC agent learns from this step
            # We must pass the `info` dict here.
            agent.learn(obs, action, next_obs, sac_reward, terminated or truncated, info)
            
            # 6. Record history for Kaleidoscope (Vigor)
            episode_history.append((obs, action))
            
            total_score += 1 # Score is just steps survived
            total_dark_residue += dark_residue
            obs = next_obs
            done = terminated

        # --- Episodic Learning Step (Vigor) ---
        
        # First, calculate the *current* coherence baseline
        if len(top_scores) > 0:
            avg_top = np.mean(top_scores)
        else:
            avg_top = 0

        # Check for coherence
        is_hard_coherent = total_score >= coherence_threshold
        is_avg_coherent = (total_score >= avg_top + avg_margin) and (total_score >= 10)

        # --- NOW update leaderboard with the current run ---
        if total_score > 0:
            top_scores.append(int(total_score))

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
            f"    Top-{top_k} scores: {sorted(list(top_scores), reverse=True)} | avg={np.mean(list(top_scores) + [0]):.2f} | margin={avg_margin}"
        )

    print("Training complete.")
    env.close()

if __name__ == "__main__":
    main()





