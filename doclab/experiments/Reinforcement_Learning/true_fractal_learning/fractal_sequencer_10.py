import gymnasium as gym
import numpy as np
import time

# --- 1. THE FRACTAL PHYSICS CORE ---
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
    
    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt, ESCAPE = 1.0, 0.1, 10.0
        
        # Color Detector
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"
        elif abs(theta) > 2.5: color = "Red"
        else:                  color = "Gold"
        
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
        return np.array(weights[:self.output_dim], dtype=np.float32), color

# --- 2. THE ORBIT KING AGENT ---
class OrbitKingAgent:
    def __init__(self, env_name, params):
        self.env_name = env_name
        # Gene: [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        self.params = params
        
        dummy = gym.make(env_name)
        self.obs_dim = dummy.observation_space.shape[0]
        self.act_dim = dummy.action_space.shape[0]
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        dummy.close()

    def get_action_data(self, obs, t_step):
        # Unpack
        cm, cl, rm, rl, tilt, freq, phase = self.params
        
        # Clock
        angle = phase + (t_step * 0.02 * freq * 2 * np.pi)
        
        # Geometry
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(tilt), np.sin(tilt)
        
        m = cm + (rm * cos_a * cos_t - rl * sin_a * sin_t)
        lam = cl + (rm * cos_a * sin_t + rl * sin_a * cos_t)
        
        # Physics
        weights, color = self.hypernet.generate_weights(m, lam)
        W = weights.reshape(self.act_dim, self.obs_dim)
        
        return np.tanh(W @ obs), color, (m, lam)

# --- 3. THE SEARCH HEAD (The DJ) ---
class SearchHead:
    """
    A single 'DJ' that manages a Zoom Window in the 7D parameter space.
    """
    def __init__(self, id_num):
        self.id = id_num
        self.best_score = -float('inf')
        self.best_gene = None
        self.age = 0
        
        # Initialize a Search Window (Hypercube)
        # Center: Random point in viable space
        self.center = np.array([
            np.random.normal(0, 0.3), np.random.normal(0, 0.3), # Center
            np.random.uniform(0.5, 1.0), np.random.uniform(0.5, 1.0), # Radius
            np.random.uniform(0, np.pi), np.random.uniform(0.5, 1.5), # Tilt/Freq
            np.random.uniform(0, 2*np.pi) # Phase
        ])
        
        # Scale: How big the window is (Standard Deviation)
        self.scale = np.array([0.2, 0.2, 0.2, 0.2, 0.5, 0.2, 1.0])
        
    def sample(self, n_samples=5):
        """
        Generate 'n' candidates within the current window.
        """
        samples = []
        for _ in range(n_samples):
            noise = np.random.normal(0, self.scale)
            candidate = self.center + noise
            
            # Constraints (Anti-Collapse)
            candidate[2] = max(0.4, candidate[2]) # Rm
            candidate[3] = max(0.4, candidate[3]) # Rl
            
            samples.append(candidate)
        return samples

    def update(self, best_candidate, score):
        """
        Zoom In: Move center to best candidate and shrink scale.
        """
        self.age += 1
        
        if score > self.best_score:
            self.best_score = score
            self.best_gene = best_candidate
            
            # Move Center
            self.center = best_candidate
            
            # Zoom In (Shrink Scale)
            # We shrink faster on successful updates
            self.scale *= 0.8
        else:
            # If no improvement, slight expansion (explore local area)
            self.scale *= 1.1
            
    def is_stuck(self):
        # If scale gets too small or age is high with low score
        if np.mean(self.scale) < 0.01: return True
        if self.age > 5 and self.best_score < -50: return True
        return False

# --- 4. THE FRACTAL OPTIMIZER (The Manager) ---
class FractalOptimizer:
    def __init__(self, env_name, n_heads=5):
        self.env_name = env_name
        self.heads = [SearchHead(i) for i in range(n_heads)]
        self.global_best_score = -float('inf')
        self.global_best_gene = None

    def evaluate(self, gene, render=False):
        agent = OrbitKingAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        total_r = 0
        basin_crossings = 0
        last_color = ""
        steps = 0
        
        while steps < 500:
            action, color, _ = agent.get_action_data(obs, steps)
            obs, r, term, trunc, _ = env.step(action)
            total_r += r
            
            if color != last_color and steps > 5:
                basin_crossings += 1
            last_color = color
            
            steps += 1
            if term or trunc:
                if steps < 50: total_r = -100
                break
        env.close()
        
        # Fitness: Reward + Basin Crossing Bonus
        return total_r + (basin_crossings * 5.0), total_r

    def run_generation(self, gen_idx):
        print(f"\n--- Generation {gen_idx} ---")
        
        for head in self.heads:
            # 1. Head samples its window
            candidates = head.sample(n_samples=6)
            
            head_best_score = -float('inf')
            head_best_cand = None
            
            for cand in candidates:
                fit, raw = self.evaluate(cand)
                
                if fit > head_best_score:
                    head_best_score = fit
                    head_best_cand = cand
                
                # Check Global Best
                if raw > self.global_best_score:
                    self.global_best_score = raw
                    self.global_best_gene = cand.copy()
                    print(f"   🏆 NEW WORLD RECORD: {raw:.1f} (Head {head.id})")

            # 2. Head Zooms (Fractal Update)
            head.update(head_best_cand, head_best_score)
            
            print(f"   Head {head.id}: Best {head_best_score:.1f} | Window Size: {np.mean(head.scale):.3f}")
            
            # 3. Head Reset (Novelty Injection)
            if head.is_stuck():
                print(f"   > Head {head.id} is stuck. Respawning elsewhere...")
                self.heads[head.id] = SearchHead(head.id) # Re-roll

    def optimize(self, generations=10):
        print(f"🔍 FRACTAL ORBIT SEARCH: {self.env_name}")
        print(f"   Managing {len(self.heads)} Parallel Zoom Windows...")
        
        for g in range(generations):
            self.run_generation(g)
            
            if self.global_best_score > 300:
                print("   > Solution Found.")
                break
                
        print(f"✨ SEARCH COMPLETE. Best Score: {self.global_best_score:.1f}")
        return self.global_best_gene

if __name__ == "__main__":
    try:
        # Run the Multi-Headed Fractal Search
        opt = FractalOptimizer("BipedalWalker-v3", n_heads=6)
        best_orbit = opt.optimize(generations=15)
        
        print("\nVisualizing the Perfect Orbit...")
        opt.evaluate(best_orbit, render=True)
    except Exception as e:
        print(f"Error: {e}")