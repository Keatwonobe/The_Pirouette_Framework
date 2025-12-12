import gymnasium as gym
import numpy as np
import time

# ============================================================
# 1. ROBUST FRACTAL PHYSICS
# ============================================================
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

# ============================================================
# 2. ADAPTIVE AGENT
# ============================================================
class AdaptiveOrbitAgent:
    def __init__(self, env_name, gene):
        self.env_name = env_name
        # Gene: [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        self.gene = gene
        
        dummy = gym.make(env_name)
        self.obs_dim = dummy.observation_space.shape[0]
        self.act_dim = dummy.action_space.shape[0]
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        dummy.close()

    def get_action_data(self, obs, t_step):
        cm, cl, rm, rl, tilt, freq, phase = self.gene
        
        angle = phase + (t_step * 0.02 * freq * 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(tilt), np.sin(tilt)
        
        m = cm + (rm * cos_a * cos_t - rl * sin_a * sin_t)
        lam = cl + (rm * cos_a * sin_t + rl * sin_a * cos_t)
        
        weights, color = self.hypernet.generate_weights(m, lam)
        W = weights.reshape(self.act_dim, self.obs_dim)
        
        return np.tanh(W @ obs), color, (m, lam)

# ============================================================
# 3. ADAPTIVE SEARCH HEAD
# ============================================================
class AdaptiveSearchHead:
    """
    Manages a search window with variable zoom.
    """
    def __init__(self, id_num):
        self.id = id_num
        self.best_score = -float('inf')
        self.best_gene = None
        self.stagnation = 0
        
        # Initial Center
        self.center = np.array([
            np.random.normal(0, 0.2), np.random.normal(0, 0.2), 
            np.random.uniform(0.6, 1.2), np.random.uniform(0.6, 1.2),
            np.random.uniform(0, np.pi), np.random.uniform(0.5, 1.5),
            np.random.uniform(0, 2*np.pi)
        ])
        
        # Initial Scale (Zoom Level) - Starts Coarse
        self.scale = np.array([0.3, 0.3, 0.3, 0.3, 0.5, 0.3, 1.0])

    def sample(self):
        # Sample around center using current scale
        noise = np.random.normal(0, self.scale)
        candidate = self.center + noise
        
        # Anti-Collapse
        candidate[2] = max(0.5, candidate[2]) 
        candidate[3] = max(0.5, candidate[3])
        return candidate

    def update(self, candidate, score):
        """
        The Adaptive Logic:
        - If score improves: Zoom IN (Refine)
        - If score stagnates: Zoom OUT (Look around)
        """
        if score > self.best_score:
            self.best_score = score
            self.best_gene = candidate.copy()
            self.center = candidate.copy() # Move to better spot
            
            # Zoom In (Refine)
            # We decay the scale to sharpen focus
            self.scale *= 0.85 
            self.stagnation = 0
            return "Refining"
            
        else:
            self.stagnation += 1
            if self.stagnation > 2:
                # Zoom Out (Expand search radius)
                self.scale *= 1.2
                # Cap max scale to avoid searching outer space
                self.scale = np.minimum(self.scale, 0.5)
                return "Expanding"
            return "Holding"

    def respawn(self):
        # Hard Reset if totally lost
        self.center = np.random.normal(0, 1.0, size=7)
        self.scale = np.array([0.5]*7)
        self.best_score = -float('inf')
        self.stagnation = 0

# ============================================================
# 4. ADAPTIVE OPTIMIZER
# ============================================================
class AdaptiveFractalOptimizer:
    def __init__(self, env_name, n_heads=5):
        self.env_name = env_name
        self.heads = [AdaptiveSearchHead(i) for i in range(n_heads)]
        self.global_best_score = -float('inf')
        self.global_best_gene = None

    def evaluate(self, gene, render=False):
        agent = AdaptiveOrbitAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        total_r = 0
        steps = 0
        basin_crossings = 0
        last_color = ""
        
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

    def run(self, generations=15):
        print(f"🔭 ADAPTIVE FRACTAL SEARCH: {self.env_name}")
        print("   heads will Zoom IN on success and Zoom OUT on failure.")
        
        for g in range(generations):
            print(f"\n--- Generation {g} ---")
            
            for head in self.heads:
                # 1. Scout
                candidate = head.sample()
                fit, raw = self.evaluate(candidate)
                
                # 2. Update Head State
                action = head.update(candidate, fit)
                
                # 3. Global Record
                if raw > self.global_best_score:
                    self.global_best_score = raw
                    self.global_best_gene = candidate.copy()
                    print(f"   🏆 NEW RECORD: {raw:.1f} (Head {head.id})")
                
                print(f"   Head {head.id}: Best {head.best_score:.0f} | Action: {action} | Scale: {np.mean(head.scale):.3f}")
                
                # 4. Respawn check
                if head.stagnation > 5:
                    print(f"   > Head {head.id} lost. Respawning.")
                    head.respawn()
            
            if self.global_best_score > 300:
                print("   > Solved.")
                break
        
        return self.global_best_gene

if __name__ == "__main__":
    try:
        opt = AdaptiveFractalOptimizer("BipedalWalker-v3", n_heads=6)
        best_gene = opt.run(generations=20)
        
        print("\nVisualizing Adaptive Solution...")
        opt.evaluate(best_gene, render=True)
    except Exception as e:
        print(f"Error: {e}")