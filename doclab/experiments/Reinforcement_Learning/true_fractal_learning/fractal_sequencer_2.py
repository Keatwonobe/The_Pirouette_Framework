import gymnasium as gym
import numpy as np
import time

# --- 1. THE FRACTAL ENGINE (Reused) ---
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def generate_weights(self, m, lam):
        weights = []
        p_m, p_l = 0.0, 0.0
        sigma, dt = 1.0, 0.1
        curr_m, curr_l = m, lam
        ESCAPE = 10.0
        
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
        return np.array(weights[:self.output_dim], dtype=np.float32)

# --- 2. THE DNA EXTRACTOR ---
class FractalGaiter:
    """
    Takes the specific 'genes' found in your previous run and loops them.
    """
    def __init__(self, env_name):
        self.env = gym.make(env_name)
        obs_dim = self.env.observation_space.shape[0]
        act_dim = self.env.action_space.shape[0]
        
        self.hypernet = FractalHypernet(obs_dim * act_dim)
        
        # THE DNA FROM YOUR LOG
        # We define the 'Keyframes' of the walk cycle
        self.keyframes = [
            {'name': 'PREP (Teal)', 'coords': (0.25, -0.14)},
            {'name': 'KICK (Red)',  'coords': (-0.35, -0.03)},
            {'name': 'CATCH (Teal)', 'coords': (0.50, -0.50)}, # From step 8
            {'name': 'REST (Gold)', 'coords': (0.00, 0.00)}
        ]
        
        # Pre-compile the weights for speed
        print("Compiling Fractal DNA...")
        for kf in self.keyframes:
            m, l = kf['coords']
            w_flat = self.hypernet.generate_weights(m, l)
            kf['weights'] = w_flat.reshape(act_dim, obs_dim)

    def get_action(self, obs, phase_idx):
        """
        Phase Index determines which fractal keyframe is active.
        """
        kf = self.keyframes[phase_idx]
        # Linear Policy: Action = W * Obs
        # We use tanh to keep it in valid motor range
        return np.tanh(kf['weights'] @ obs)

# --- 3. THE RHYTHM SEARCH (Evolutionary Strategy) ---
class RhythmSearch:
    def __init__(self):
        self.gaiter = FractalGaiter("BipedalWalker-v3")
        
    def evaluate_rhythm(self, timings):
        """
        Timings: A list of integers [t1, t2, t3, t4]
        Each integer is how many frames to hold that keyframe.
        """
        # Create env inside loop for safety
        env = gym.make("BipedalWalker-v3")
        obs, _ = env.reset()
        
        total_reward = 0
        steps = 0
        
        # We loop the cycle 10 times (attempting continuous walking)
        for _ in range(10): 
            for kf_idx, hold_time in enumerate(timings):
                # Hold this fractal state for 'hold_time' frames
                for _ in range(int(hold_time)):
                    action = self.gaiter.get_action(obs, kf_idx)
                    obs, r, term, trunc, _ = env.step(action)
                    total_reward += r
                    steps += 1
                    
                    if term or trunc:
                        env.close()
                        # Penalty for falling early, but keep the points gained
                        return total_reward if steps > 50 else -100
            
            if total_reward < -50: break # Fail fast
            
        env.close()
        return total_reward

    def optimize(self):
        print("🥁 TUNING THE FRACTAL RHYTHM...")
        print("   We have the Notes (Fractal Coordinates). We need the Tempo.")
        
        # Initial guess: [Prep, Kick, Catch, Rest] duration in frames
        # Walker steps are usually ~20-30 frames total
        population = np.random.randint(2, 15, size=(20, 4)) 
        
        best_r = -float('inf')
        best_rhythm = None
        
        start_time = time.time()
        
        for gen in range(10): # Quick Generations
            scores = []
            for indiv in population:
                score = self.evaluate_rhythm(indiv)
                scores.append(score)
                
                if score > best_r:
                    best_r = score
                    best_rhythm = indiv
                    print(f"   > New Rhythm Found: {indiv} (Score: {score:.1f})")
            
            # Selection & Mutation
            # Keep top 5
            top_indices = np.argsort(scores)[-5:]
            parents = population[top_indices]
            
            # Repopulate
            new_pop = []
            for _ in range(20):
                p = parents[np.random.randint(len(parents))]
                # Mutate: shift timing by +/- 2 frames
                mutation = np.random.randint(-2, 3, size=4)
                child = np.clip(p + mutation, 1, 20) # Keep frames between 1 and 20
                new_pop.append(child)
            population = np.array(new_pop)
            
            if best_r > 50: # If it's walking well, stop
                print("   > Walker is viable!")
                break
                
        print(f"\n✨ RHYTHM LOCKED in {time.time()-start_time:.1f}s")
        print(f"   Best Sequence Durations: {best_rhythm}")
        return best_rhythm

    def visualize(self, rhythm):
        print("\n🎥 Playing the Loop...")
        env = gym.make("BipedalWalker-v3", render_mode="human")
        obs, _ = env.reset()
        
        total = 0
        while True:
            for kf_idx, hold_time in enumerate(rhythm):
                # Print current phase
                name = self.gaiter.keyframes[kf_idx]['name']
                # print(f"Phase: {name}")
                
                for _ in range(int(hold_time)):
                    action = self.gaiter.get_action(obs, kf_idx)
                    obs, r, term, trunc, _ = env.step(action)
                    total += r
                    if term or trunc: break
                if term or trunc: break
            if term or trunc: break
            
        print(f"Final Run Score: {total:.1f}")
        env.close()

if __name__ == "__main__":
    try:
        tuner = RhythmSearch()
        best_beat = tuner.optimize()
        tuner.visualize(best_beat)
    except Exception as e:
        print(f"Error: {e}")