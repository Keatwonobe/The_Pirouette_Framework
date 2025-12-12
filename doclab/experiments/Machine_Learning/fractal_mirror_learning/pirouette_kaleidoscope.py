import gymnasium as gym
import numpy as np
import time

class KaleidoscopeAgent:
    """
    This agent learns by building a "Data Kaleidoscope" (a "solver table") 
    of "Generative Engrams" based on the Pirouette Framework.
    
    It does not use backpropagation or gradient descent.
    It learns by "Formular Induction" from successful, coherent episodes.
    """
    def __init__(self, observation_space, action_space):
        self.action_space = action_space
        
        # --- The Data Kaleidoscope ---
        # This is our "graph of engrams" or "solver table."
        # It maps a simplified "engram_key" (a state) to a successful "solution" (an action).
        # We are "weaving" a graph of solutions.
        self.kaleidoscope = {}
        # -----------------------------

        # --- "Engram Simplification" Bins ---
        # We need to simplify the continuous state [pos, vel, angle, angle_vel]
        # into a discrete "engram_key". We define bins for each observation.
        # This is a form of "deduplication" and "simplification".
        self.pos_bins = np.linspace(-2.4, 2.4, 10)
        self.vel_bins = np.linspace(-4, 4, 10) # Capping velocity for simplicity
        self.angle_bins = np.linspace(-0.209, 0.209, 10) # ~12 degrees
        self.angle_vel_bins = np.linspace(-4, 4, 10) # Capping angular velocity

    def discretize_state(self, obs):
        """
        This is the "Engram Simplification" function.
        It turns a complex, continuous observation into a simple, hashable
        "engram_key" that can be stored in our Kaleidoscope.
        """
        cart_pos, cart_vel, pole_angle, pole_vel = obs
        
        pos_idx = np.digitize(cart_pos, self.pos_bins)
        vel_idx = np.digitize(cart_vel, self.vel_bins)
        angle_idx = np.digitize(pole_angle, self.angle_bins)
        angle_vel_idx = np.digitize(pole_vel, self.angle_vel_bins)
        
        # The tuple is our "simplified engram" key.
        return (pos_idx, vel_idx, angle_idx, angle_vel_idx)

    def choose_action(self, obs):
        """
        This is the "Heartbeat" of the agent.
        It checks for a "resonant loop" (a known engram) or explores.
        """
        engram_key = self.discretize_state(obs)
        
        if engram_key in self.kaleidoscope:
            # --- "Vigor" (Use Existing Engram) ---
            # A "resonant loop" is found! We know the solution for this state.
            # We play back the action from our "solver table."
            return self.kaleidoscope[engram_key]
        else:
            # --- "Rigor" (Explore to Create New Engram) ---
            # No engram found. We must "weave a new construct" by
            # exploring the environment.
            return self.action_space.sample()

    def learn_from_history(self, episode_history):
        """
        This is "Formular Induction."
        After a *successful* episode, we treat its history as a
        "Coherent Engram" and "weave" it into our Kaleidoscope.
        """
        # We iterate over the successful (obs, action) pairs
        for obs, action in episode_history:
            
            # 1. Simplify the observation into its engram key
            engram_key = self.discretize_state(obs)
            
            # 2. "Weave" the solution into the graph.
            # We store this action as the *correct solution* for this state.
            # This builds our "solver table."
            if engram_key not in self.kaleidoscope:
                self.kaleidoscope[engram_key] = action
                

# --- Main Training Loop ---

def main():
    print("Initializing Pirouette Agent for Gymnasium...")
    # Render_mode="human" lets us watch the agent learn
    env = gym.make("CartPole-v1", render_mode="human")
    
    agent = KaleidoscopeAgent(env.observation_space, env.action_space)
    
    num_episodes = 10000
    # We define a "coherent" episode as one that scores over 150
    coherence_threshold = 80 
    
    print("Starting 'Formular Induction' (Learning)...")
    
    for i in range(num_episodes):
        obs, info = env.reset()
        
        episode_history = []
        total_reward = 0
        terminated = False
        truncated = False
        
        while not terminated and not truncated:
            # 1. Agent chooses action based on its Kaleidoscope
            action = agent.choose_action(obs)
            
            # 2. Environment responds
            next_obs, reward, terminated, truncated, info = env.step(action)
            
            # 3. Record what happened
            episode_history.append((obs, action))
            total_reward += reward
            
            obs = next_obs
            
            # Optional: slow down rendering to watch
            # time.sleep(0.01)

        # --- "Rigor" / Learning Step ---
        # After the episode, check if it was "coherent"
        if total_reward > coherence_threshold:
            print(f"Episode {i+1}: *** Coherent Engram Found! *** Score: {total_reward}")
            print(f"    Inducing formula... Weaving {len(episode_history)} new states into Kaleidoscope.")
            agent.learn_from_history(episode_history)
            print(f"    Kaleidoscope size is now: {len(agent.kaleidoscope)}")
        else:
            print(f"Episode {i+1}: Dissonant run. Score: {total_reward}. Discarding history.")
            
    print("Training complete.")
    env.close()

if __name__ == "__main__":
    main()
