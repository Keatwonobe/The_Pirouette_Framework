import gymnasium as gym
import numpy as np
import time
from collections import deque

# ============================================================
# 1. FRACTAL PHYSICS CORE
# ============================================================
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt, ESCAPE = 1.0, 0.1, 10.0
        
        # Basin Identity (The "Sand State")
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"     # Damping / Sampler
        elif abs(theta) > 2.5: color = "Red"     # Chaos / Navigator
        else:                  color = "Gold"    # Stability / Integrator
        
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
# 2. DELTA ORBIT AGENT
# ============================================================
class OrbitAgent:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.act_dim = dummy.action_space.shape[0]
        self.obs_dim = dummy.observation_space.shape[0]
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        dummy.close()

    def get_action_data(self, obs, t_step):
        # Unpack Gene: [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        cm, cl, rm, rl, tilt, freq, phase = self.gene
        
        angle = phase + (t_step * 0.02 * freq * 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(tilt), np.sin(tilt)
        
        m = cm + (rm * cos_a * cos_t - rl * sin_a * sin_t)
        lam = cl + (rm * cos_a * sin_t + rl * sin_a * cos_t)
        
        weights, color = self.hypernet.generate_weights(m, lam)
        W = weights.reshape(self.act_dim, self.obs_dim)
        
        return np.tanh(W @ obs), color

# ============================================================
# 3. THE DELTA SCOREKEEPER
# ============================================================
class DeltaScorekeeper:
    def __init__(self, alpha=0.05):
        self.baseline = 0.0
        self.alpha = alpha # Learning rate for the baseline
        
    def get_delta_score(self, raw_score):
        # The Delta: How much better is this than usual?
        delta = raw_score - self.baseline
        
        # Update Baseline (Slowly adapt to the new normal)
        # If delta is positive, baseline rises (making it harder next time)
        # If delta is negative, baseline drops (giving a chance to recover)
        self.baseline = (1 - self.alpha) * self.baseline + self.alpha * raw_score
        
        return delta

# ============================================================
# 4. DELTA-KI TRAINER (Sand-Aware Evolution)
# ============================================================
class DeltaKiTrainer:
    def __init__(self, env_name, n_heads=6):
        self.env_name = env_name
        self.heads = [{'gene': self.random_gene(), 'scorekeeper': DeltaScorekeeper()} for _ in range(n_heads)]
        self.global_best_dist = 0.0
        self.global_best_gene = None

    def random_gene(self):
        # [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        return np.array([
            np.random.normal(0, 0.3), np.random.normal(0, 0.3),
            np.random.uniform(0.5, 1.2), np.random.uniform(0.5, 1.2), # Forced Large Radius
            np.random.uniform(0, np.pi), np.random.uniform(0.5, 1.5),
            np.random.uniform(0, 2*np.pi)
        ])

    def evaluate(self, gene, scorekeeper, render=False):
        agent = OrbitAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        max_dist = 0
        basin_counts = {"Gold": 0, "Red": 0, "Teal": 0}
        steps = 0
        
        while steps < 600:
            action, color = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            
            # Track Basin Usage (The "Sand" State)
            basin_counts[color] += 1
            
            # Metric: Pure Distance
            curr_x = env.unwrapped.hull.position.x
            dist = curr_x - start_x
            max_dist = max(max_dist, dist)
            
            steps += 1
            if term or trunc: break
        env.close()
        
        # Calculate Delta
        delta = scorekeeper.get_delta_score(max_dist)
        
        # Determine Dominant Basin (for Mutation Logic)
        dominant_basin = max(basin_counts, key=basin_counts.get)
        
        return delta, max_dist, dominant_basin

    def run(self, generations=20):
        print(f"🌊 DELTA-KI TRAINER: {self.env_name}")
        print("   Reward = (Distance - Moving_Average). No points for stagnation.")
        print("   Mutation controlled by Fractal Basin (Sand Logic).")
        
        for g in range(generations):
            print(f"\n--- Generation {g} ---")
            
            for i, head in enumerate(self.heads):
                # 1. Evaluate
                delta, raw_dist, basin = self.evaluate(head['gene'], head['scorekeeper'])
                
                # 2. Check Global Record
                if raw_dist > self.global_best_dist:
                    self.global_best_dist = raw_dist
                    self.global_best_gene = head['gene'].copy()
                    print(f"   🏆 NEW RECORD: {raw_dist:.1f}m (Head {i})")
                
                # 3. Sand Logic: Adjust Mutation based on Basin
                # "Ki" implies rhythm: We need different behaviors in different phases
                if basin == "Gold":
                    mutation_scale = 0.02 # Stable: Fine-tune
                    strategy = "Refining"
                elif basin == "Teal":
                    mutation_scale = 0.10 # Damping: Moderate search
                    strategy = "Exploring"
                else: # Red
                    mutation_scale = 0.25 # Chaos: High Variance / Scramble
                    strategy = "Scrambling"
                
                print(f"   Head {i}: Dist {raw_dist:.1f}m | Delta {delta:+.2f} | Basin: {basin} ({strategy})")
                
                # 4. Evolution Step
                # If Delta is positive, we keep this gene and mutate slightly
                # If Delta is negative, we revert to parent (or keep current) and mutate harder
                
                if delta > 0:
                    # Success! Keep this gene, burn it into memory
                    # (In this simple version, 'gene' is effectively the parent)
                    pass 
                else:
                    # Failure relative to baseline.
                    # If we are stuck (negative delta for a while), we need to change.
                    # Since we don't store a separate parent here, we just mutate the current one.
                    # The 'mutation_scale' handles the magnitude.
                    pass
                
                # Mutate
                noise = np.random.normal(0, mutation_scale, size=7)
                head['gene'] += noise
                
                # Constraints
                head['gene'][2] = max(0.5, head['gene'][2]) # Radius M
                head['gene'][3] = max(0.5, head['gene'][3]) # Radius L

            if self.global_best_dist > 50.0:
                print("   > Goal Reached.")
                break
                
        return self.global_best_gene

if __name__ == "__main__":
    try:
        trainer = DeltaKiTrainer("BipedalWalker-v3", n_heads=6)
        best_gene = trainer.run(generations=15)
        
        if best_gene is not None:
            print("\nVisualizing the Delta Walker...")
            # Create a temp scorekeeper for viz
            dummy_sk = DeltaScorekeeper()
            trainer.evaluate(best_gene, dummy_sk, render=True)
    except Exception as e:
        print(f"Error: {e}")