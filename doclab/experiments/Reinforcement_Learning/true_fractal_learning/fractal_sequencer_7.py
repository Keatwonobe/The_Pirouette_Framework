import gymnasium as gym
import numpy as np
import time

# --- 1. THE FRACTAL CORE ---
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt, ESCAPE = 1.0, 0.1, 10.0
        
        while len(weights) < self.output_dim:
            if abs(curr_m) > ESCAPE or abs(curr_l) > ESCAPE:
                curr_m = np.fmod(curr_m, 2.0); curr_l = np.fmod(curr_l, 2.0)
            try:
                grad_m = curr_m + 2 * sigma * curr_m * curr_l
                grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
                curr_m += dt * (curr_m + 2 * sigma * curr_m * curr_l)
                curr_l += dt * (curr_l + sigma * (curr_m**2 - curr_l**2))
            except: curr_m, curr_l = 0.0, 0.0
            weights.append(np.tanh(curr_m)); weights.append(np.tanh(curr_l))
        return np.array(weights[:self.output_dim], dtype=np.float32)

# --- 2. THE ORCHESTRA (Fractal A) ---
class PolicyOrchestra:
    """
    Generates 50 distinct static models scattered across the basin.
    """
    def __init__(self, env_name, size=50):
        self.env_name = env_name
        dummy = gym.make(env_name)
        self.obs_dim = dummy.observation_space.shape[0]
        self.act_dim = dummy.action_space.shape[0]
        dummy.close()
        
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        self.models = [] # List of {'coords': (m,l), 'W': matrix, 'id': int}
        
        print(f"🎻 TUNING ORCHESTRA: Generating {size} Fractal Models...")
        
        # We sample the basin using a Golden Spiral to ensure even coverage
        # without grid artifacts.
        for i in range(size):
            # Golden Angle distribution
            radius = np.sqrt(i / size) * 1.5 # Max radius 1.5
            angle = np.pi * (3 - np.sqrt(5)) * i * 10.0 # Golden angle
            
            m = radius * np.cos(angle)
            l = radius * np.sin(angle)
            
            # Generate Weights
            w_flat = self.hypernet.generate_weights(m, l)
            W = w_flat.reshape(self.act_dim, self.obs_dim)
            
            self.models.append({
                'id': i,
                'coords': np.array([m, l]),
                'W': W
            })
            
    def get_nearest_model(self, m, l):
        """
        Voronoi Selection: Find the model geometrically closest to (m, l)
        """
        query = np.array([m, l])
        best_dist = float('inf')
        best_model = None
        
        # Linear scan is fast enough for 50 items
        for model in self.models:
            dist = np.linalg.norm(model['coords'] - query)
            if dist < best_dist:
                best_dist = dist
                best_model = model
                
        return best_model

# --- 3. THE CONDUCTOR (Fractal B) ---
class FractalConductor:
    """
    An Orbit that sweeps through the Orchestra to play the music.
    """
    def __init__(self, orchestra, params):
        self.orchestra = orchestra
        # Orbit Parameters
        self.center_m = params[0]
        self.center_l = params[1]
        self.radius_m = params[2]
        self.radius_l = params[3]
        self.tilt     = params[4]
        self.freq     = params[5]
        self.phase    = params[6]
        
    def get_action(self, obs, t_step):
        # 1. Calculate Conductor Position
        angle = self.phase + (t_step * 0.02 * self.freq * 2 * np.pi)
        
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(self.tilt), np.sin(self.tilt)
        
        # The Cursor Position
        curr_m = self.center_m + (self.radius_m * cos_a * cos_t - self.radius_l * sin_a * sin_t)
        curr_l = self.center_l + (self.radius_m * cos_a * sin_t + self.radius_l * sin_a * cos_t)
        
        # 2. Select the Instrument (Nearest Neighbor)
        model = self.orchestra.get_nearest_model(curr_m, curr_l)
        
        # 3. Play Note
        action = np.tanh(model['W'] @ obs)
        
        return action, model['id'], (curr_m, curr_l)

# --- 4. THE COMPOSER (Search) ---
class DualFractalSearch:
    def __init__(self, env_name):
        self.env_name = env_name
        self.orchestra = PolicyOrchestra(env_name, size=50)
        
    def evaluate_composition(self, params, render=False):
        conductor = FractalConductor(self.orchestra, params)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        total_reward = 0
        steps = 0
        
        last_id = -1
        
        while steps < 500:
            action, model_id, coords = conductor.get_action(obs, steps)
            obs, r, term, trunc, _ = env.step(action)
            total_reward += r
            
            if render and model_id != last_id:
                # print(f"   Frame {steps}: Switching to Model #{model_id}")
                last_id = model_id
                
            steps += 1
            if term or trunc:
                if steps < 50: total_reward = -100
                break
        env.close()
        return total_reward

    def compose(self):
        print(f"\n🎼 DUAL FRACTAL SYNTHESIS: {self.env_name}")
        print("   Searching for the Melody that plays the 50 Models best...")
        
        # Gene: [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        population = []
        for _ in range(30):
            gene = [
                np.random.normal(0, 0.2), np.random.normal(0, 0.2), # Center
                np.random.uniform(0.5, 1.2), np.random.uniform(0.5, 1.2), # Radius
                np.random.uniform(0, np.pi), # Tilt
                np.random.uniform(0.2, 1.5), # Freq
                np.random.uniform(0, 2*np.pi)
            ]
            population.append(gene)
        population = np.array(population)
        
        best_score = -float('inf')
        best_gene = None
        
        for gen in range(15):
            scores = []
            for gene in population:
                score = self.evaluate_composition(gene)
                scores.append(score)
                
                if score > best_score:
                    best_score = score
                    best_gene = gene.copy()
                    print(f"   [Gen {gen}] New Melody: Score={score:.1f} | Freq={gene[5]:.2f}Hz")
            
            # Selection
            elites = population[np.argsort(scores)[-5:]]
            
            # Mutation
            new_pop = []
            for _ in range(30):
                parent = elites[np.random.randint(len(elites))].copy()
                child = parent + np.random.normal(0, 0.05, size=7)
                new_pop.append(child)
            population = np.array(new_pop)
            
            if best_score > 300: break
            
        print(f"✨ COMPOSITION COMPLETE. Best Score: {best_score:.1f}")
        return best_gene

if __name__ == "__main__":
    try:
        composer = DualFractalSearch("BipedalWalker-v3")
        best_song = composer.compose()
        
        print("\nVisualizing the Concert...")
        composer.evaluate_composition(best_song, render=True)
    except Exception as e:
        print(f"Error: {e}")