import gymnasium as gym
import numpy as np
import time

# ============================================================
# 1. FRACTAL PHYSICS (The Engine)
# ============================================================
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

# ============================================================
# 2. THE AGENT (The Driver)
# ============================================================
class GoalAgent:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.act_dim = dummy.action_space.shape[0]
        self.obs_dim = dummy.observation_space.shape[0]
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        dummy.close()

    def get_action(self, obs, t_step):
        # Unpack Gene: [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        cm, cl, rm, rl, tilt, freq, phase = self.gene
        
        angle = phase + (t_step * 0.02 * freq * 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(tilt), np.sin(tilt)
        
        m = cm + (rm * cos_a * cos_t - rl * sin_a * sin_t)
        lam = cl + (rm * cos_a * sin_t + rl * sin_a * cos_t)
        
        W = self.hypernet.generate_weights(m, lam).reshape(self.act_dim, self.obs_dim)
        return np.tanh(W @ obs)

# ============================================================
# 3. THE GOAL EVALUATOR (The Judge)
# ============================================================
class GoalEvaluator:
    def __init__(self, env_name):
        self.env_name = env_name
        
    def measure_performance(self, gene, render=False):
        agent = GoalAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        max_distance = 0
        steps = 0
        
        while steps < 800: # Give it time to walk far
            action = agent.get_action(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            
            # PURE METRIC: Distance Traveled
            # We ignore the game's "Reward" completely.
            current_x = env.unwrapped.hull.position.x
            dist = current_x - start_x
            max_distance = max(max_distance, dist)
            
            steps += 1
            if term or trunc: break
            
        env.close()
        
        # FITNESS = DISTANCE
        # If it fell immediately, Distance is small (~0.5).
        # If it knelt, Distance is 0.
        # If it walked, Distance is > 10.
        return max_distance

# ============================================================
# 4. ADAPTIVE SEARCH (The Optimizer)
# ============================================================
class GoalSearchHead:
    def __init__(self, id_num):
        self.id = id_num
        self.best_dist = 0.0
        self.best_gene = None
        self.stagnation = 0
        # Initialize Random Search Window
        self.center = np.random.normal(0, 0.5, size=7)
        self.scale = np.array([0.3]*7)

    def sample(self):
        cand = self.center + np.random.normal(0, self.scale)
        cand[2] = max(0.5, cand[2]) # Force Radius > 0.5 (Movement Mandate)
        cand[3] = max(0.5, cand[3])
        return cand

    def update(self, candidate, dist):
        if dist > self.best_dist:
            self.best_dist = dist
            self.best_gene = candidate.copy()
            self.center = candidate.copy()
            self.scale *= 0.9 # Focus
            self.stagnation = 0
            return "New Record"
        else:
            self.stagnation += 1
            if self.stagnation > 3:
                self.scale *= 1.2 # Expand
                return "Expanding"
            return "Holding"

class FractalGoalSearch:
    def __init__(self, env_name, n_heads=6):
        self.evaluator = GoalEvaluator(env_name)
        self.heads = [GoalSearchHead(i) for i in range(n_heads)]
        self.global_best_dist = 0.0
        self.global_best_gene = None

    def run(self, generations=15):
        print(f"🎯 FRACTAL GOAL SEEKER: {self.evaluator.env_name}")
        print("   Goal: MAXIMIZE DISTANCE (Pure Velocity). No Safety Nets.")
        
        for g in range(generations):
            print(f"\n--- Generation {g} ---")
            
            for head in self.heads:
                # 1. Sample & Test
                gene = head.sample()
                dist = self.evaluator.measure_performance(gene)
                
                # 2. Update Head
                status = head.update(gene, dist)
                
                # 3. Global Check
                if dist > self.global_best_dist:
                    self.global_best_dist = dist
                    self.global_best_gene = gene.copy()
                    print(f"   🏆 NEW DISTANCE RECORD: {dist:.1f} meters (Head {head.id})")
                
                print(f"   Head {head.id}: {dist:.1f}m (Best: {head.best_dist:.1f}m) | {status}")
                
                # 4. Reset if stuck at 0 (Kneeling/Falling)
                if head.stagnation > 5 and head.best_dist < 2.0:
                    print(f"   > Head {head.id} is stuck at start line. Respawning.")
                    head.__init__(head.id) # Hard Reset

            if self.global_best_dist > 50.0:
                print("   > Goal Reached (End of Track).")
                break
                
        return self.global_best_gene

if __name__ == "__main__":
    try:
        # We assume BipedalWalker-v3 is the target
        searcher = FractalGoalSearch("BipedalWalker-v3", n_heads=8)
        best_gene = searcher.run(generations=20)
        
        if best_gene is not None:
            print("\nVisualizing the Sprinter...")
            searcher.evaluator.measure_performance(best_gene, render=True)
        else:
            print("No viable walker found.")
    except Exception as e:
        print(f"Error: {e}")