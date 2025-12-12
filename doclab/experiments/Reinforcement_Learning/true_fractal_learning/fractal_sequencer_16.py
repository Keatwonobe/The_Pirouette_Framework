import gymnasium as gym
import numpy as np
import time
from collections import deque

# ============================================================
# 1. FRACTAL PHYSICS (Robust Engine)
# ============================================================
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt, ESCAPE = 1.0, 0.1, 10.0
        
        # Basin Identity
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"     # Damping
        elif abs(theta) > 2.5: color = "Red"     # Chaos
        else:                  color = "Gold"    # Stability
        
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
# 2. ORBIT AGENT
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
# 3. ELLIPSE ANALYZER (Kinematics)
# ============================================================
class EllipseAnalyzer:
    """
    Calculates the 'Loopiness' of the gait using Forward Kinematics.
    We compute the area swept by the foot relative to the hip.
    """
    def __init__(self):
        self.prev_foot_1 = None
        self.prev_foot_2 = None
        self.total_area = 0.0
        
    def get_foot_pos(self, hip_angle, knee_angle):
        # Approximate leg lengths for BipedalWalker (Upper=34, Lower=34 approx units)
        # We normalize to 1.0 for shape calculation
        l1, l2 = 1.0, 1.0
        
        # FK relative to hip
        # Hip angle is obs[4] (Leg 1) or obs[9] (Leg 2)
        # Knee angle is obs[6] (Leg 1) or obs[11] (Leg 2)
        
        theta1 = hip_angle
        theta2 = hip_angle + knee_angle
        
        x = l1 * np.sin(theta1) + l2 * np.sin(theta2)
        y = -(l1 * np.cos(theta1) + l2 * np.cos(theta2))
        return np.array([x, y])

    def update(self, obs):
        # Leg 1 (Right)
        f1 = self.get_foot_pos(obs[4], obs[6])
        # Leg 2 (Left)
        f2 = self.get_foot_pos(obs[9], obs[11])
        
        # Calculate Shoelace Area (Green's Theorem discrete)
        # Area += 0.5 * |x1*y2 - x2*y1| (Cross product)
        if self.prev_foot_1 is not None:
            # Vector from prev to curr
            d1 = np.cross(self.prev_foot_1, f1) # Swept area relative to hip
            d2 = np.cross(self.prev_foot_2, f2)
            
            # We sum absolute swept area to reward "Activity"
            self.total_area += 0.5 * (abs(d1) + abs(d2))
            
        self.prev_foot_1 = f1
        self.prev_foot_2 = f2
        
        return self.total_area

# ============================================================
# 4. DELTA-KI TRAINER (With Ellipse Bonus)
# ============================================================
class DeltaScorekeeper:
    def __init__(self, alpha=0.05):
        self.baseline = 0.0
        self.alpha = alpha
    def get_delta_score(self, raw_score):
        delta = raw_score - self.baseline
        self.baseline = (1 - self.alpha) * self.baseline + self.alpha * raw_score
        return delta

class EllipticalTrainer:
    def __init__(self, env_name, n_heads=6):
        self.env_name = env_name
        self.heads = [{'gene': self.random_gene(), 'scorekeeper': DeltaScorekeeper()} for _ in range(n_heads)]
        self.global_best_score = 0.0
        self.global_best_gene = None
        
        # THE DYNAMIC KNOB
        # 0.0 = Pure Distance, 5.0 = Excessive High-Stepping
        self.ellipse_knob = 2.0 

    def random_gene(self):
        return np.array([
            np.random.normal(0, 0.3), np.random.normal(0, 0.3),
            np.random.uniform(0.5, 1.2), np.random.uniform(0.5, 1.2),
            np.random.uniform(0, np.pi), np.random.uniform(0.5, 1.5),
            np.random.uniform(0, 2*np.pi)
        ])

    def evaluate(self, gene, scorekeeper, render=False):
        agent = OrbitAgent(self.env_name, gene)
        analyzer = EllipseAnalyzer()
        
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        max_dist = 0
        basin_counts = {"Gold": 0, "Red": 0, "Teal": 0}
        steps = 0
        
        while steps < 600:
            action, color = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            
            # Update Metrics
            basin_counts[color] += 1
            curr_x = env.unwrapped.hull.position.x
            dist = curr_x - start_x
            max_dist = max(max_dist, dist)
            
            # Update Ellipse Tracker
            stride_area = analyzer.update(obs)
            
            steps += 1
            if term or trunc: break
        env.close()
        
        # --- THE REWARD FORMULA ---
        # Score = Distance + (Distance * Area * Knob)
        # We multiply by Distance so it only rewards ellipses THAT MOVE FORWARD.
        # Flailing in place gets 0 distance, so 0 score.
        
        # Normalize area (it accumulates every frame, so divide by steps)
        avg_loop_size = stride_area / (steps + 1) * 100.0 # Scale up for readability
        
        raw_score = max_dist * (1.0 + (avg_loop_size * self.ellipse_knob))
        
        delta = scorekeeper.get_delta_score(raw_score)
        dominant_basin = max(basin_counts, key=basin_counts.get)
        
        return delta, raw_score, max_dist, avg_loop_size, dominant_basin

    def run(self, generations=20):
        print(f"🦵 ELLIPTICAL STRIDE TRAINER: {self.env_name}")
        print(f"   Dynamic Knob: {self.ellipse_knob} (Rewarding Large Loops)")
        
        for g in range(generations):
            print(f"\n--- Generation {g} ---")
            
            for i, head in enumerate(self.heads):
                delta, score, dist, loop, basin = self.evaluate(head['gene'], head['scorekeeper'])
                
                if score > self.global_best_score:
                    self.global_best_score = score
                    self.global_best_gene = head['gene'].copy()
                    print(f"   🏆 NEW RECORD: Score {score:.1f} (Dist {dist:.1f}m | Loop {loop:.2f})")
                
                # Sand Logic Mutation
                if basin == "Gold":   scale = 0.02; strategy = "Refining"
                elif basin == "Teal": scale = 0.10; strategy = "Exploring"
                else:                 scale = 0.25; strategy = "Scrambling"
                
                print(f"   Head {i}: Dist {dist:.1f}m | Loop {loop:.2f} | Delta {delta:+.1f} ({strategy})")
                
                # Evolution
                noise = np.random.normal(0, scale, size=7)
                
                # If doing well (Positive Delta), keep direction
                if delta > 0:
                    head['gene'] += noise * 0.5 # Small adjustment
                else:
                    head['gene'] += noise # Big adjustment to escape
                
                # Constraints
                head['gene'][2] = max(0.5, head['gene'][2]) # Radius
                head['gene'][3] = max(0.5, head['gene'][3])

            if self.global_best_score > 300: # Arbitrary high score
                print("   > Elite Sprinter Found.")
                break
                
        return self.global_best_gene

if __name__ == "__main__":
    try:
        trainer = EllipticalTrainer("BipedalWalker-v3", n_heads=6)
        best_gene = trainer.run(generations=15)
        
        print("\nVisualizing the Running Man...")
        dummy_sk = DeltaScorekeeper()
        trainer.evaluate(best_gene, dummy_sk, render=True)
    except Exception as e:
        print(f"Error: {e}")