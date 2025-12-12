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
# 2. THE VESTIBULAR REFLEX (The Balance System)
# ============================================================
class VestibularSystem:
    def __init__(self):
        # PID gains for the Hull Angle
        # These are "Reflex Strength" parameters
        self.kp = 10.0 # Stiffness (How hard to pull body upright)
        self.kd = 2.0  # Damping (Prevent oscillation)
        
    def get_balance_torque(self, current_angle, target_angle, angular_velocity):
        """
        Calculates the hip torque needed to maintain the Head (Hull)
        at the Target Angle.
        """
        error = target_angle - current_angle
        
        # PD Control Law
        # We want to minimize error while resisting velocity
        torque = (self.kp * error) - (self.kd * angular_velocity)
        
        return torque

# ============================================================
# 3. HILDEBRAND OSCILLATOR (The Gait System)
# ============================================================
class HildebrandOscillator:
    def __init__(self):
        self.phase_counter = 0.0
        
    def get_target_angles(self, t_step, freq, beta, phi):
        self.phase_counter += (0.02 * freq)
        self.phase_counter %= 1.0 
        
        phase1 = self.phase_counter
        phase2 = (self.phase_counter + phi) % 1.0
        
        def waveform(p, b):
            if p < b: # Stance
                prog = p / b
                return 1.0 - (2.0 * prog) 
            else: # Swing
                prog = (p - b) / (1.0 - b)
                return -1.0 + (2.0 * prog)

        return waveform(phase1, beta), waveform(phase2, beta)

# ============================================================
# 4. THE HYBRID AGENT
# ============================================================
class BalancedWalkerAgent:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.act_dim = dummy.action_space.shape[0]
        self.obs_dim = dummy.observation_space.shape[0]
        # Weights: [0-3] Leg Gains, [4] Lean Bias, [5] Balance Stiffness
        self.hypernet = FractalHypernet(6) 
        dummy.close()
        
        self.oscillator = HildebrandOscillator()
        self.vestibular = VestibularSystem()

    def get_action_data(self, obs, t_step):
        cm, cl, rm, rl, tilt, freq, phase_start = self.gene
        
        # --- 1. FRACTAL ORBIT ---
        angle = phase_start + (t_step * 0.02 * 0.5 * 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(tilt), np.sin(tilt)
        
        m = cm + (rm * cos_a * cos_t - rl * sin_a * sin_t)
        lam = cl + (rm * cos_a * sin_t + rl * sin_a * cos_t)
        
        # --- 2. GAIT PARAMETERS ---
        # Beta (Duty Factor): Walk (>0.5) vs Run (<0.5)
        beta = np.clip(0.55 + (m * 0.25), 0.35, 0.85)
        # Phi (Phase): Trot (0.5) vs Gallop/Pronk (0.0)
        phi = (lam + 1.0) / 2.0 % 1.0
        
        # --- 3. THE "SEMI-AUTOMATIC" CHOICE ---
        # The Fractal chooses the 'Attitude' (Lean)
        weights, color = self.hypernet.generate_weights(m, lam)
        
        # Weight[4] determines the Lean Target (-0.5 rad to +0.5 rad)
        # Red Basin (Chaos) -> Lean Forward (Attack)
        # Gold Basin (Stable) -> Lean Upright
        target_lean = weights[4] * 0.4 
        
        # --- 4. EXECUTION ---
        # A. Leg Targets (Hildebrand)
        t_hip1, t_hip2 = self.oscillator.get_target_angles(t_step, freq, beta, phi)
        
        # B. Leg Torques (Gait)
        gains = (weights[:4] + 1.0) * 3.0 # Stiffness
        
        # Leg 1
        gait_torque_1 = (gains[0] * (t_hip1 - obs[4])) - (gains[1] * obs[6])
        # Leg 2
        gait_torque_2 = (gains[2] * (t_hip2 - obs[9])) - (gains[3] * obs[11])
        
        # C. Balance Torque (Vestibular)
        # Calculates torque needed to keep Hull (obs[0]) at Target Lean
        balance_torque = self.vestibular.get_balance_torque(obs[0], target_lean, obs[1])
        
        # --- 5. THE MIXER ---
        # The Hip joints receive BOTH signals.
        # Note: To tilt torso forward (positive), you apply negative torque to hips relative to legs
        # We apply the balance torque equally to both hips to keep torso stable
        
        total_torque_1 = gait_torque_1 + balance_torque
        total_torque_2 = gait_torque_2 + balance_torque
        
        actions = np.array([
            total_torque_1, # Hip 1
            -0.1 * obs[7],  # Knee 1 (Simple damping)
            total_torque_2, # Hip 2
            -0.1 * obs[12]  # Knee 2
        ])
        
        return np.tanh(actions), color, beta, target_lean

# ============================================================
# 5. DELTA-KI TRAINER
# ============================================================
class DeltaScorekeeper:
    def __init__(self, alpha=0.05):
        self.baseline = 0.0
        self.alpha = alpha
    def get_delta_score(self, raw_score):
        delta = raw_score - self.baseline
        self.baseline = (1 - self.alpha) * self.baseline + self.alpha * raw_score
        return delta

class BalancedGaitTrainer:
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
            np.random.uniform(0, np.pi), np.random.uniform(0.8, 2.5),
            np.random.uniform(0, 2*np.pi)
        ])

    def evaluate(self, gene, scorekeeper, render=False):
        agent = BalancedWalkerAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        max_dist = 0
        steps = 0
        
        while steps < 600:
            action, color, beta, lean = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            
            curr_x = env.unwrapped.hull.position.x
            dist = curr_x - start_x
            max_dist = max(max_dist, dist)
            
            if render and steps % 50 == 0:
                # print(f"   Lean Target: {lean:.2f} rad | Beta: {beta:.2f}")
                pass

            steps += 1
            if term or trunc: break
        env.close()
        
        # Reward: Distance - (Head Instability Penalty)
        # We want it to walk far AND keep the head near the target
        # Actually, let's trust the Delta score. If it falls, distance stops.
        # No need to over-engineer the reward if the physics are robust.
        
        delta = scorekeeper.get_delta_score(max_dist)
        return delta, max_dist

    def run(self, generations=20):
        print(f"⚖️ BALANCED WALKER TRAINER: {self.env_name}")
        print(f"   Mixing Hildebrand Gait + Vestibular Reflex...")
        
        for g in range(generations):
            print(f"\n--- Generation {g} ---")
            
            for i, head in enumerate(self.heads):
                delta, dist = self.evaluate(head['gene'], head['scorekeeper'])
                
                if dist > self.global_best_score:
                    self.global_best_score = dist
                    self.global_best_gene = head['gene'].copy()
                    print(f"   🏆 NEW RECORD: {dist:.1f}m")
                
                print(f"   Head {i}: Dist {dist:.1f}m | Delta {delta:+.2f}")
                
                # Mutation
                scale = 0.05 if delta > 0 else 0.2
                head['gene'] += np.random.normal(0, scale, size=7)
                head['gene'][5] = np.clip(head['gene'][5], 0.5, 3.5) # Freq limits

            if self.global_best_score > 60.0:
                print("   > Balanced Gait Achieved.")
                break
                
        return self.global_best_gene

if __name__ == "__main__":
    try:
        trainer = BalancedGaitTrainer("BipedalWalker-v3", n_heads=6)
        best_gene = trainer.run(generations=15)
        
        print("\nVisualizing the Balanced Walker...")
        dummy_sk = DeltaScorekeeper()
        trainer.evaluate(best_gene, dummy_sk, render=True)
    except Exception as e:
        print(f"Error: {e}")