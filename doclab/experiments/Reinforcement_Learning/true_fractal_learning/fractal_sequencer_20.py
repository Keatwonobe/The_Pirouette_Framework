import gymnasium as gym
import numpy as np
import time
from collections import deque

# ============================================================
# 1. FRACTAL PHYSICS (Robust)
# ============================================================
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt, ESCAPE = 1.0, 0.1, 10.0
        
        # Basin Identity (Sand State)
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"     # Damping / Exploring
        elif abs(theta) > 2.5: color = "Red"     # Chaos / Scrambling
        else:                  color = "Gold"    # Stability / Refining
        
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
# 2. HILDEBRAND OSCILLATOR (With Stance Detection)
# ============================================================
class HildebrandOscillator:
    def __init__(self):
        self.phase_counter = 0.0
        
    def get_phase_targets(self, t_step, freq, beta, phi):
        """
        Returns (Hip_Target, Knee_Target, Is_Stance) for both legs.
        """
        self.phase_counter += (0.02 * freq)
        self.phase_counter %= 1.0 
        
        phase1 = self.phase_counter
        phase2 = (self.phase_counter + phi) % 1.0
        
        def get_leg_state(p, b):
            # STANCE (Foot on ground)
            if p < b: 
                # Hip drives BACK (-1.0) to push body forward
                # Knee locks STRAIGHT (0.0) to support weight
                prog = p / b
                hip_t = 1.0 - (2.0 * prog) 
                knee_t = 0.0 
                return hip_t, knee_t, True
            
            # SWING (Foot in air)
            else: 
                # Hip drives FORWARD (+1.0) to catch step
                # Knee BENDS (-1.5) to clear ground
                prog = (p - b) / (1.0 - b)
                hip_t = -1.0 + (2.0 * prog)
                
                # Knee Flexion Wave (Bend then Straighten)
                if prog < 0.5: knee_t = -1.5 # Lift
                else:          knee_t = 0.0  # Prepare for impact
                
                return hip_t, knee_t, False

        h1, k1, s1 = get_leg_state(phase1, beta)
        h2, k2, s2 = get_leg_state(phase2, beta)
        
        return (h1, k1, s1), (h2, k2, s2)

# ============================================================
# 3. STANCE-LOCKED AGENT
# ============================================================
class StanceLockedAgent:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.act_dim = dummy.action_space.shape[0]
        self.obs_dim = dummy.observation_space.shape[0]
        # Weights for Gains: [Hip_K, Hip_D, Knee_K, Knee_D, Lean_Ref]
        self.hypernet = FractalHypernet(5) 
        dummy.close()
        
        self.oscillator = HildebrandOscillator()

    def get_action_data(self, obs, t_step):
        cm, cl, rm, rl, tilt, freq, phase_start = self.gene
        
        # --- 1. FRACTAL ORBIT ---
        angle = phase_start + (t_step * 0.02 * freq * 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(tilt), np.sin(tilt)
        
        m = cm + (rm * cos_a * cos_t - rl * sin_a * sin_t)
        lam = cl + (rm * cos_a * sin_t + rl * sin_a * cos_t)
        
        # --- 2. GAIT PARAMETERS ---
        # Beta: 0.55 is a fast walk / slow run.
        beta = np.clip(0.55 + (m * 0.25), 0.4, 0.8) 
        phi = (lam + 1.0) / 2.0 % 1.0
        
        # --- 3. DYNAMICS ---
        weights, color = self.hypernet.generate_weights(m, lam)
        gains = (weights[:4] + 1.0) * 4.0 # Base Gains (0 to 8)
        
        # --- 4. KINEMATICS (The Fix) ---
        (h1_t, k1_t, stance1), (h2_t, k2_t, stance2) = \
            self.oscillator.get_phase_targets(t_step, freq, beta, phi)
            
        # --- 5. CONTROL MIXER ---
        actions = np.zeros(4)
        
        # LEG 1 (Right)
        # Hip
        actions[0] = (gains[0] * (h1_t - obs[4])) - (gains[1] * obs[6])
        # Knee (CRITICAL FIX)
        # If Stance: High Stiffness to hold weight.
        # If Swing: Lower Stiffness to allow motion.
        knee_k = gains[2] * (2.0 if stance1 else 0.5) 
        actions[1] = (knee_k * (k1_t - obs[6])) - (gains[3] * obs[7])
        
        # LEG 2 (Left)
        actions[2] = (gains[0] * (h2_t - obs[9])) - (gains[1] * obs[11])
        knee_k2 = gains[2] * (2.0 if stance2 else 0.5)
        actions[3] = (knee_k2 * (k2_t - obs[11])) - (gains[3] * obs[12])
        
        # VIRTUAL BALLAST (The Forward Fall)
        # We apply a slight forward bias to hips to "lean" into the run
        lean_bias = weights[4] * 0.5
        actions[0] -= lean_bias
        actions[2] -= lean_bias
        
        return np.tanh(actions), color, beta, phi

# ============================================================
# 4. DELTA-KI TRAINER
# ============================================================
class DeltaScorekeeper:
    def __init__(self, alpha=0.05):
        self.baseline = 0.0
        self.alpha = alpha
    def get_delta_score(self, raw_score):
        # The Delta: Pure improvement over the average
        delta = raw_score - self.baseline
        # Update baseline slowly
        self.baseline = (1 - self.alpha) * self.baseline + self.alpha * raw_score
        return delta

class StanceLockedTrainer:
    def __init__(self, env_name, n_heads=6):
        self.env_name = env_name
        self.heads = [{'gene': self.random_gene(), 'scorekeeper': DeltaScorekeeper()} for _ in range(n_heads)]
        self.global_best_dist = 0.0
        self.global_best_gene = None

    def random_gene(self):
        return np.array([
            np.random.normal(0, 0.2), np.random.normal(0, 0.2),
            np.random.uniform(0.5, 1.0), np.random.uniform(0.5, 1.0),
            np.random.uniform(0, np.pi), np.random.uniform(0.8, 2.5),
            np.random.uniform(0, 2*np.pi)
        ])

    def evaluate(self, gene, scorekeeper, render=False):
        agent = StanceLockedAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        max_dist = 0.0
        steps = 0
        basin_counts = {"Gold":0, "Red":0, "Teal":0}
        
        while steps < 600:
            action, color, _, _ = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            
            curr_x = env.unwrapped.hull.position.x
            dist = curr_x - start_x
            max_dist = max(max_dist, dist)
            basin_counts[color] += 1
            
            steps += 1
            if term or trunc: break
        env.close()
        
        # Pure Delta Reward
        delta = scorekeeper.get_delta_score(max_dist)
        dom_basin = max(basin_counts, key=basin_counts.get)
        
        return delta, max_dist, dom_basin

    def run(self, generations=20):
        print(f"🔒 STANCE-LOCKED TRAINER: {self.env_name}")
        print("   Feature: Active Knee Locking during Stance Phase.")
        print("   Metric: Pure Delta (Distance - Baseline).")
        
        for g in range(generations):
            print(f"\n--- Generation {g} ---")
            
            for i, head in enumerate(self.heads):
                delta, dist, basin = self.evaluate(head['gene'], head['scorekeeper'])
                
                if dist > self.global_best_dist:
                    self.global_best_dist = dist
                    self.global_best_gene = head['gene'].copy()
                    print(f"   🏆 NEW RECORD: {dist:.1f}m (Head {i})")
                
                # Sand Logic (Ki)
                if basin == "Gold":   scale = 0.03; mode = "Refining"
                elif basin == "Teal": scale = 0.10; mode = "Exploring"
                else:                 scale = 0.25; mode = "Scrambling"
                
                print(f"   Head {i}: {dist:.1f}m | Delta {delta:+.2f} | {mode} ({basin})")
                
                # Mutation
                # If Delta is negative, we need to change significantly
                noise_scale = scale if delta > 0 else scale * 1.5
                head['gene'] += np.random.normal(0, noise_scale, size=7)
                
                # Constraints
                head['gene'][5] = np.clip(head['gene'][5], 0.5, 3.5) # Freq limits

            if self.global_best_dist > 80.0:
                print("   > Sprinter Found.")
                break
                
        return self.global_best_gene

if __name__ == "__main__":
    try:
        trainer = StanceLockedTrainer("BipedalWalker-v3", n_heads=6)
        best_gene = trainer.run(generations=15)
        
        print("\nVisualizing the Stance-Locked Walker...")
        dummy_sk = DeltaScorekeeper()
        trainer.evaluate(best_gene, dummy_sk, render=True)
    except Exception as e:
        print(f"Error: {e}")