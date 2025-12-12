import gymnasium as gym
import numpy as np
import time

# --- 1. THE FRACTAL CORE (Standard) ---
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def generate_weights(self, m, lam):
        weights = []
        p_m, p_l = 0.0, 0.0
        sigma, dt = 1.0, 0.1
        curr_m, curr_l = m, lam
        ESCAPE = 10.0
        
        # Determine Basin Color (For user feedback)
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"     # Damping
        elif abs(theta) > 2.5: color = "Red"     # Chaos/Kick
        else:                  color = "Gold"    # Stability
        
        while len(weights) < self.output_dim:
            if abs(curr_m) > ESCAPE or abs(curr_l) > ESCAPE:
                curr_m = np.fmod(curr_m, 2.0); curr_l = np.fmod(curr_l, 2.0)
                p_m *= 0.1; p_l *= 0.1
            try:
                grad_m = curr_m + 2 * sigma * curr_m * curr_l
                grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
                p_m -= (dt/2) * grad_m; p_l -= (dt/2) * grad_l
                curr_m += dt * p_m; curr_l += dt * p_l
                if np.isnan(curr_m): curr_m = 0.0
            except: curr_m, curr_l = 0.0, 0.0
            weights.append(np.tanh(curr_m)); weights.append(np.tanh(curr_l))
            
        return np.array(weights[:self.output_dim], dtype=np.float32), color

# --- 2. THE ORBITAL CONTROLLER ---
class OrbitalPolicy:
    """
    Instead of a fixed point, the policy is defined by an ORBIT.
    (m, lambda) = Center + Radius * [cos(wt), sin(wt)]
    """
    def __init__(self, env_name, center_m, center_l, radius, frequency, phase_offset=0.0):
        self.env_name = env_name
        self.center_m = center_m
        self.center_l = center_l
        self.radius = radius
        self.freq = frequency
        self.phase = phase_offset
        
        # Build the engine
        dummy_env = gym.make(env_name)
        self.obs_dim = dummy_env.observation_space.shape[0]
        self.act_dim = dummy_env.action_space.shape[0]
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        dummy_env.close()
        
    def get_action_and_color(self, obs, t_step):
        # 1. Calculate the 'Delta' (Current Phase Angle)
        # 2*pi * freq * (time_in_seconds)
        # Assuming 50FPS
        current_angle = self.phase + (t_step * 0.02 * self.freq * 2 * np.pi)
        
        # 2. Map to Coordinate (The Orbit)
        m = self.center_m + self.radius * np.cos(current_angle)
        lam = self.center_l + self.radius * np.sin(current_angle)
        
        # 3. Generate Weights on the fly (The Flow)
        weights, color = self.hypernet.generate_weights(m, lam)
        W = weights.reshape(self.act_dim, self.obs_dim)
        
        # 4. Act
        action = np.tanh(W @ obs)
        return action, color, (m, lam)

# --- 3. THE ORBITAL SEARCH (Finding the Flow) ---
class OrbitalSearch:
    def __init__(self, env_name):
        self.env_name = env_name
        
    def evaluate_orbit(self, params, render=False):
        """
        Params: [Center_M, Center_L, Radius, Frequency]
        """
        cm, cl, rad, freq = params
        agent = OrbitalPolicy(self.env_name, cm, cl, rad, freq)
        
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        total_reward = 0
        steps = 0
        last_color = "None"
        
        if render: print(f"🚀 Launching Orbit: Center({cm:.2f},{cl:.2f}) R={rad:.2f} Freq={freq:.2f}")
        
        while steps < 400:
            action, color, coords = agent.get_action_and_color(obs, steps)
            
            # [LOGIC CHECK] The 'No Doubles' Rule
            # If render is on, we print transitions to prove the flow
            if render and color != last_color:
                print(f"   Frame {steps}: Transition -> {color} ({coords[0]:.2f}, {coords[1]:.2f})")
                last_color = color
                
            obs, r, term, trunc, _ = env.step(action)
            total_reward += r
            steps += 1
            
            if term or trunc:
                # Big penalty for crashing early
                if steps < 50: total_reward = -100
                break
                
        env.close()
        return total_reward

    def optimize(self):
        print(f"🪐 ORBITAL SEARCH: {self.env_name}")
        print("   Searching for the Heartbeat (Frequency) and Flow (Orbit)...")
        
        # Search Space:
        # Center M/L: Small deviations from 0 (The singularity)
        # Radius: How 'extreme' the physics changes are (0.1 to 1.5)
        # Frequency: The tempo (0.2 Hz to 2.0 Hz)
        
        best_score = -float('inf')
        best_params = None
        
        # Evolutionary Strategy (ES)
        pop_size = 20
        # Initialize near the "Genesect" (0,0) with moderate radius
        population = []
        for _ in range(pop_size):
            population.append([
                np.random.uniform(-0.5, 0.5), # Center M
                np.random.uniform(-0.5, 0.5), # Center L
                np.random.uniform(0.2, 1.0),  # Radius
                np.random.uniform(0.3, 1.5)   # Frequency
            ])
        population = np.array(population)
        
        for gen in range(100): # Fast search
            scores = []
            for indiv in population:
                score = self.evaluate_orbit(indiv)
                scores.append(score)
                
                if score > best_score:
                    best_score = score
                    best_params = indiv
                    print(f"   [Gen {gen}] New Best Orbit: R={indiv[2]:.2f} Freq={indiv[3]:.2f} | Score: {score:.1f}")
            
            # Selection
            top_indices = np.argsort(scores)[-5:]
            parents = population[top_indices]
            
            # Mutation
            new_pop = []
            for _ in range(pop_size):
                p = parents[np.random.randint(len(parents))].copy()
                # Mutate
                p += np.random.normal(0, 0.1, size=4)
                # Bounds check
                p[2] = np.clip(p[2], 0.1, 1.5) # Radius must be positive
                p[3] = np.clip(p[3], 0.1, 3.0) # Freq must be reasonable
                new_pop.append(p)
            population = np.array(new_pop)
            
            if best_score > 100:
                print("   > Stable Orbit Established.")
                break
                
        print(f"🏆 SEARCH COMPLETE. Best Score: {best_score:.1f}")
        return best_params

if __name__ == "__main__":
    try:
        searcher = OrbitalSearch("BipedalWalker-v3")
        best_orbit = searcher.optimize()
        
        # Visualize the Flow
        print("\nVisualizing the Infinite Cycle...")
        # We run it for a long time to see the loop
        searcher.evaluate_orbit(best_orbit, render=True)
        
    except Exception as e:
        print(f"Orbit Error: {e}")