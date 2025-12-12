import gymnasium as gym
import numpy as np
import time
from stable_baselines3 import SAC
from stable_baselines3.common.buffers import ReplayBuffer
from stable_baselines3.common.noise import NormalActionNoise
import torch as th

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
        
        # "Engram Simplification" Bins
        self.pos_bins = np.linspace(-2.4, 2.4, 10)
        self.vel_bins = np.linspace(-4, 4, 10)
        self.angle_bins = np.linspace(-0.209, 0.209, 10)
        self.angle_vel_bins = np.linspace(-4, 4, 10)
        
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
    with the "Vigor" of the Kaleidoscope's proven memory."""
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
            use_sde=True, # State-dependent exploration
            tensorboard_log="./sac_pirouette_log/",
            device=self.device # <-- FIX: Tell SAC which device to use
        )
        
        # 3. The Replay Buffer for continuous learning
        self.replay_buffer = ReplayBuffer(
            buffer_size=100_000,
            observation_space=self.env.observation_space,
            action_space=self.env.action_space,
            device=self.device, # <-- FIX: Tell the buffer which device to use
            n_envs=1
        )
        
        self.total_steps = 0
        self.batch_size = 256

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
        action, _states = self.sac_agent.predict(obs, deterministic=False)
        return action, "Rigor"

    def learn(self, obs, action, next_obs, reward, done):
        """
        This is the continuous learning step.
        The SAC agent learns from *every* experience.
        """
        self.total_steps += 1
        
        # Store the experience in the replay buffer
        self.replay_buffer.add(obs, next_obs, action, reward, done, [{}])
        
        # Train the SAC ("Rigor") agent if we have enough samples
        if self.total_steps > self.sac_agent.learning_starts and self.total_steps % 50 == 0:
            if self.replay_buffer.size() > self.batch_size:
                data = self.replay_buffer.sample(self.batch_size)
                self.sac_agent.train(data)

# --- Main Training Loop ---

def main():
    # --- FIX: Device Detection ---
    # We add this block to detect the GPU and set the device
    device_name = "cuda" if th.cuda.is_available() else "cpu"
    device = th.device(device_name)
    print(f"Initializing Pirouette Hybrid (SAC + Kaleidoscope) Agent...")
    print(f"Using device: {device_name}")
    # -----------------------------
    
    # We MUST use a continuous action space for SAC.
    # We create the CartPole env, but *tell it* we want a continuous action space.
    env = gym.make("CartPole-v1", render_mode="human")
    
    # We need to wrap the environment to handle continuous actions
    # The default CartPole-v1 has a *discrete* action space (0 or 1).
    # SAC performs best with *continuous* actions (force from -1.0 to 1.0).
    # This is a common step in real RL. We will create a wrapper.
    
    class ContinuousActionWrapper(gym.Wrapper):
        def __init__(self, env):
            super().__init__(env)
            # We change the action space to be continuous
            self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)

        def step(self, action):
            # The original env wants 0 (left) or 1 (right).
            # We map our continuous action to this.
            discrete_action = 0 if action[0] < 0 else 1
            # We also scale the force based on the action's magnitude
            # (This is a more realistic physics model)
            # self.env.force_mag = 10.0 * abs(action[0]) # Uncomment for variable force
            
            obs, reward, terminated, truncated, info = self.env.step(discrete_action)
            return obs, reward, terminated, truncated, info

    env = ContinuousActionWrapper(env)
    agent = HybridPirouetteAgent(env, device=device) # <-- Pass device to agent
    
    num_episodes = 500
    coherence_threshold = 400 # We're raising the bar for coherence
    
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
            # 1. Agent chooses hybrid action
            action, mode = agent.choose_action(obs)
            if mode == "Vigor":
                vigor_actions += 1
            else:
                rigor_actions += 1
            
            # 2. Environment responds
            next_obs, reward, terminated, truncated, info = env.step(action)
            
            # 3. Calculate "Dark Residue" (D)
            dark_residue = calculate_dark_residue(next_obs)
            
            # 4. Define the Reward for the SAC agent
            # The reward is the *negative* of the Dark Residue
            # This trains the SAC agent to *minimize* D.
            sac_reward = -dark_residue
            
            # 5. Continuous Learning (Rigor)
            # The SAC agent learns from this step
            agent.learn(obs, action, next_obs, sac_reward, terminated or truncated)
            
            # 6. Record history for Kaleidoscope (Vigor)
            episode_history.append((obs, action))
            
            total_score += reward # Standard score
            total_dark_residue += dark_residue
            obs = next_obs

        # --- Episodic Learning Step (Vigor) ---
        if total_score > coherence_threshold:
            print(f"Episode {i+1}: *** Coherent Engram Found! *** Score: {total_score:.0f}")
            new_engrams = agent.kaleidoscope.learn_from_history(episode_history)
            print(f"    Inducing formula... Wove {new_engrams} new states into Kaleidoscope.")
            print(f"    Kaleidoscope size: {len(agent.kaleidoscope.kaleidoscope)}")
        else:
            print(f"Episode {i+1}: Dissonant run. Score: {total_score:.0f}. Discarding history.")
            
        print(f"    Avg Dark Residue: {total_dark_residue / total_score:.2f} | Vigor/Rigor: {vigor_actions}/{rigor_actions}")
            
    print("Training complete.")
    agent.sac_agent.save("pirouette_sac_model")
    env.close()

if __name__ == "__main__":
    main()

