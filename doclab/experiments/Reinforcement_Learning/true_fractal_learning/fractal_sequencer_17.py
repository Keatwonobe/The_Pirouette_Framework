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
        
        # Basin Identity (Used for SLIP vs Pendulum classification)
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
# 2. THE HILDEBRAND OSCILLATOR (The Math Layer)
# ============================================================
class HildebrandOscillator:
    """
    Implements the coupled oscillator math:
    - Duty Factor (beta): Stance vs Swing time
    - Relative Phase (phi): Lag between legs
    """
    def __init__(self):
        self.phase_counter = 0.0
        
    def get_target_angles(self, t_step, freq, beta, phi):
        """
        Returns target angles for Hip1 and Hip2 based on symmetry.
        """
        # 1. Fundamental Clock (T)
        # 50 FPS assumption. Freq is in Hz.
        self.phase_counter += (0.02 * freq)
        self.phase_counter %= 1.0 # Normalize to [0, 1] cycle
        
        # 2. Leg Phases
        # Leg 1 is reference (0.0)
        # Leg 2 is shifted by phi
        phase1 = self.phase_counter
        phase2 = (self.phase_counter + phi) % 1.0
        
        # 3. Waveform Generator (Respecting Duty Factor beta)
        # If phase < beta: Stance (Push back)
        # If phase > beta: Swing (Recover forward)
        def waveform(p, b):
            if p < b:
                # Stance: Linear interpolation from +Range to -Range
                # We normalize 0..b to 0..1 then map to Angle
                progress = p / b
                return 1.0 - (2.0 * progress) # Result: 1.0 -> -1.0
            else:
                # Swing: Fast reset from -Range to +Range
                progress = (p - b) / (1.0 - b)
                return -1.0 + (2.0 * progress) # Result: -1.0 -> 1.0

        angle1 = waveform(phase1, beta)
        angle2 = waveform(phase2, beta)
        
        return angle1, angle2

# ============================================================
# 3. SYMMETRY AGENT (The Driver)
# ============================================================
class SymmetryAgent:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.act_dim = dummy.action_space.shape[0]
        self.obs_dim = dummy.observation_space.shape[0]
        # We need weights for Stiffness (k) and Damping (d) for SLIP model
        self.hypernet = FractalHypernet(8) # 4 joints * 2 params (k, d)
        dummy.close()
        
        self.oscillator = HildebrandOscillator()

    def get_action_data(self, obs, t_step):
        cm, cl, rm, rl, tilt, freq, phase_start = self.gene
        
        # 1. Fractal Orbit Logic (To determine Gait Parameters)
        orbit_angle = phase_start + (t_step * 0.02 * 0.5 * 2 * np.pi) # Slow orbit
        cos_a, sin_a = np.cos(orbit_angle), np.sin(orbit_angle)
        cos_t, sin_t = np.cos(tilt), np.sin(tilt)
        
        m = cm + (rm * cos_a * cos_t - rl * sin_a * sin_t)
        lam = cl + (rm * cos_a * sin_t + rl * sin_a * cos_t)
        
        # 2. Map Fractal to Hildebrand Variables
        # m -> Duty Factor (Beta). Map [-1, 1] to [0.3, 0.8]
        # High m = Walk (High Beta), Low m = Run (Low Beta)
        beta = np.clip(0.55 + (m * 0.25), 0.3, 0.9)
        
        # lam -> Relative Phase (Phi). Map [-1, 1] to [0.0, 1.0]
        # 0.5 = Anti-phase (Trot/Walk), 0.0 = In-phase (Pronk)
        phi = (lam + 1.0) / 2.0 % 1.0
        
        # 3. Get Target Kinematics from Oscillator
        target_hip1, target_hip2 = self.oscillator.get_target_angles(t_step, freq, beta, phi)
        
        # 4. Generate Stiffness/Damping from Fractal (SLIP Dynamics)
        # The fractal determines HOW rigid the leg is (Spring constant)
        weights, color = self.hypernet.generate_weights(m, lam)
        # Map weights to positive gains (0 to 10)
        gains = (weights + 1.0) * 2.0 
        
        # 5. PD Controller (The Nervous System)
        # Torque = k * (Target - Current) - d * Velocity
        # Obs mapping: [4]=Hip1, [9]=Hip2
        
        actions = np.zeros(4)
        
        # Leg 1 Hip
        k1, d1 = gains[0], gains[1]
        err1 = target_hip1 - obs[4]
        actions[0] = (k1 * err1) - (d1 * obs[6]) # obs[6] is hip velocity approx
        
        # Leg 2 Hip
        k2, d2 = gains[2], gains[3]
        err2 = target_hip2 - obs[9]
        actions[2] = (k2 * err2) - (d2 * obs[11])
        
        # Knees (Slave to Hips with fractal offset or simple damping)
        # We let the fractal drive knees purely responsively
        actions[1] = -0.1 * obs[7] # Simple damping
        actions[3] = -0.1 * obs[12]
        
        return np.tanh(actions), color, beta, phi

# ============================================================
# 4. HILDEBRAND TRAINER
# ============================================================
class DeltaScorekeeper:
    def __init__(self, alpha=0.05):
        self.baseline = 0.0
        self.alpha = alpha
    def get_delta_score(self, raw_score):
        delta = raw_score - self.baseline
        self.baseline = (1 - self.alpha) * self.baseline + self.alpha * raw_score
        return delta

class HildebrandTrainer:
    def __init__(self, env_name, n_heads=6):
        self.env_name = env_name
        self.heads = [{'gene': self.random_gene(), 'scorekeeper': DeltaScorekeeper()} for _ in range(n_heads)]
        self.global_best_score = 0.0
        self.global_best_gene = None

    def random_gene(self):
        # [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        return np.array([
            np.random.normal(0, 0.2), np.random.normal(0, 0.2),
            np.random.uniform(0.5, 1.0), np.random.uniform(0.5, 1.0),
            np.random.uniform(0, np.pi), np.random.uniform(0.8, 2.5), # Higher freq for gaits
            np.random.uniform(0, 2*np.pi)
        ])

    def evaluate(self, gene, scorekeeper, render=False):
        agent = SymmetryAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        max_dist = 0
        steps = 0
        
        # Analytics
        gait_types = {"Run": 0, "Walk": 0}
        
        while steps < 600:
            action, color, beta, phi = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            
            curr_x = env.unwrapped.hull.position.x
            dist = curr_x - start_x
            max_dist = max(max_dist, dist)
            
            # Classify Gait
            if beta < 0.5: gait_types["Run"] += 1
            else:          gait_types["Walk"] += 1
            
            # Print Gait info during Render
            if render and steps % 50 == 0:
                gait_name = "WALK" if beta > 0.5 else "RUN/SLIP"
                # print(f"   t={steps} | {color} Basin | Beta={beta:.2f} ({gait_name}) | Phi={phi:.2f}")
            
            steps += 1
            if term or trunc: break
        env.close()
        
        delta = scorekeeper.get_delta_score(max_dist)
        dominant_gait = "Walk" if gait_types["Walk"] > gait_types["Run"] else "Run"
        
        return delta, max_dist, dominant_gait

    def run(self, generations=20):
        print(f"🐎 HILDEBRAND SYMMETRY TRAINER: {self.env_name}")
        print(f"   Searching the Topology of Gaits (Beta vs Phi)...")
        
        for g in range(generations):
            print(f"\n--- Generation {g} ---")
            
            for i, head in enumerate(self.heads):
                delta, dist, gait = self.evaluate(head['gene'], head['scorekeeper'])
                
                if dist > self.global_best_score:
                    self.global_best_score = dist
                    self.global_best_gene = head['gene'].copy()
                    print(f"   🏆 NEW RECORD: {dist:.1f}m ({gait} Symmetry)")
                
                # Feedback
                print(f"   Head {i}: {dist:.1f}m | Delta {delta:+.2f} | Mode: {gait}")
                
                # Mutation Strategy (Gradient Ascent on Symmetry)
                # If Delta > 0, we refine the current Phase/Duty relationship.
                # If Delta < 0, we shift the Orbit center to find a new Gait Mode.
                
                noise_scale = 0.05 if delta > 0 else 0.2
                noise = np.random.normal(0, noise_scale, size=7)
                head['gene'] += noise
                
                # Constraints (Keep Freq reasonable)
                head['gene'][5] = np.clip(head['gene'][5], 0.5, 3.0)

            if self.global_best_score > 60.0:
                print("   > Stable Limit Cycle Established.")
                break
                
        return self.global_best_gene

if __name__ == "__main__":
    try:
        trainer = HildebrandTrainer("BipedalWalker-v3", n_heads=6)
        best_gene = trainer.run(generations=15)
        
        print("\nVisualizing the Symmetry Group...")
        dummy_sk = DeltaScorekeeper()
        trainer.evaluate(best_gene, dummy_sk, render=True)
    except Exception as e:
        print(f"Error: {e}")