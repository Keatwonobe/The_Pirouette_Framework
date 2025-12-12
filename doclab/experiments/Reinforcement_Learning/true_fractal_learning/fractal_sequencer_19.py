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
# 2. VIRTUAL BALLAST (The "Front Weight")
# ============================================================
class VirtualBallast:
    """
    Simulates a heavy weight attached to the front of the Hull.
    Torque = Mass * Gravity * Lever_Arm * cos(Theta)
    """
    def __init__(self):
        self.static_mass = 5.0  # Base weight to counter back-heaviness
        self.dynamic_gain = 3.0 # How much to shift weight when moving
        
    def get_ballast_torque(self, hull_angle, velocity):
        # 1. Static Compensation (The "Nose Job")
        # We assume the 'Virtual Weight' is sticking straight out the front.
        # It generates negative torque (tipping forward).
        # Torque varies with angle (gravity vector).
        static_torque = -self.static_mass * np.cos(hull_angle)
        
        # 2. Dynamic Shift (The "Sprint Lean")
        # As we run faster (velocity > 0), we push the weight further out.
        # This increases the forward tipping moment.
        dynamic_lever = np.clip(velocity, 0, 2.0) * self.dynamic_gain
        dynamic_torque = -dynamic_lever * np.cos(hull_angle)
        
        return static_torque + dynamic_torque

# ============================================================
# 3. HILDEBRAND OSCILLATOR (Gait)
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
# 4. COUNTERWEIGHTED AGENT
# ============================================================
class CounterweightedAgent:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.act_dim = dummy.action_space.shape[0]
        self.obs_dim = dummy.observation_space.shape[0]
        self.hypernet = FractalHypernet(6) 
        dummy.close()
        
        self.oscillator = HildebrandOscillator()
        self.ballast = VirtualBallast()

    def get_action_data(self, obs, t_step):
        cm, cl, rm, rl, tilt, freq, phase_start = self.gene
        
        # --- 1. FRACTAL ORBIT ---
        angle = phase_start + (t_step * 0.02 * 0.5 * 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(tilt), np.sin(tilt)
        m = cm + (rm * cos_a * cos_t - rl * sin_a * sin_t)
        lam = cl + (rm * cos_a * sin_t + rl * sin_a * cos_t)
        
        # --- 2. GAIT ---
        beta = np.clip(0.55 + (m * 0.25), 0.35, 0.85)
        phi = (lam + 1.0) / 2.0 % 1.0
        
        # --- 3. VIRTUAL PHYSICS ---
        weights, color = self.hypernet.generate_weights(m, lam)
        
        # A. Calculate Ballast Torque (The Front Weight)
        # obs[0] = Hull Angle, obs[2] = Horizontal Velocity
        ballast_torque = self.ballast.get_ballast_torque(obs[0], obs[2])
        
        # B. Vestibular Reflex (Stiffness)
        # Still need this to stop it from falling over completely
        target_lean = -0.2 # Slight forward bias
        balance_error = target_lean - obs[0]
        reflex_torque = (10.0 * balance_error) - (2.0 * obs[1])
        
        # --- 4. MIXER ---
        # The Ballast is Feed-Forward (blind force)
        # The Reflex is Feed-Back (correction)
        total_balance_signal = ballast_torque + reflex_torque
        
        # --- 5. LEG CONTROL ---
        t_hip1, t_hip2 = self.oscillator.get_target_angles(t_step, freq, beta, phi)
        gains = (weights[:4] + 1.0) * 3.0
        
        # Apply Balance Signal to Hips
        # To tip hull forward, we torque legs backward (Action +)
        # Check signs: Box2D, torque on joint affects bodies oppositely.
        # Positive hip torque -> Legs Forward, Hull Backward.
        # We want Hull Forward (Negative Torque on Hull).
        # So we apply POSITIVE torque to Hips? No, Equal/Opposite.
        # Let's trust the PID sign: Error = Target(-0.2) - Curr(0.5) = -0.7.
        # Torque = 10 * -0.7 = -7.0.
        # Negative action usually moves legs back/body forward in standard setups.
        
        # Mixing Ballast into the Hip Drive
        act_1 = (gains[0] * (t_hip1 - obs[4])) - (gains[1] * obs[6]) + total_balance_signal
        act_2 = (gains[2] * (t_hip2 - obs[9])) - (gains[3] * obs[11]) + total_balance_signal
        
        actions = np.array([act_1, -0.1*obs[7], act_2, -0.1*obs[12]])
        return np.tanh(actions), color, beta, ballast_torque

# ============================================================
# 5. TRAINER
# ============================================================
class DeltaScorekeeper:
    def __init__(self, alpha=0.05):
        self.baseline = 0.0
        self.alpha = alpha
    def get_delta_score(self, raw_score):
        delta = raw_score - self.baseline
        self.baseline = (1 - self.alpha) * self.baseline + self.alpha * raw_score
        return delta

class CounterweightTrainer:
    def __init__(self, env_name, n_heads=6):
        self.env_name = env_name
        self.heads = [{'gene': self.random_gene(), 'scorekeeper': DeltaScorekeeper()} for _ in range(n_heads)]
        self.global_best_score = 0.0
        self.global_best_gene = None

    def random_gene(self):
        return np.array([
            np.random.normal(0, 0.2), np.random.normal(0, 0.2),
            np.random.uniform(0.5, 1.0), np.random.uniform(0.5, 1.0),
            np.random.uniform(0, np.pi), np.random.uniform(0.8, 2.5),
            np.random.uniform(0, 2*np.pi)
        ])

    def evaluate(self, gene, scorekeeper, render=False):
        agent = CounterweightedAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        max_dist = 0
        steps = 0
        
        while steps < 600:
            action, color, beta, ballast = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            
            curr_x = env.unwrapped.hull.position.x
            dist = curr_x - start_x
            max_dist = max(max_dist, dist)
            
            if render and steps % 50 == 0:
               pass # print(f"   Ballast Torque: {ballast:.2f} | Velocity: {obs[2]:.2f}")
            
            steps += 1
            if term or trunc: break
        env.close()
        
        delta = scorekeeper.get_delta_score(max_dist)
        return delta, max_dist

    def run(self, generations=20):
        print(f"🏗️ COUNTERWEIGHT TRAINER: {self.env_name}")
        print(f"   Simulating Virtual Front-Mass for Dynamic Balance...")
        
        for g in range(generations):
            print(f"\n--- Generation {g} ---")
            
            for i, head in enumerate(self.heads):
                delta, dist = self.evaluate(head['gene'], head['scorekeeper'])
                
                if dist > self.global_best_score:
                    self.global_best_score = dist
                    self.global_best_gene = head['gene'].copy()
                    print(f"   🏆 NEW RECORD: {dist:.1f}m")
                
                print(f"   Head {i}: Dist {dist:.1f}m | Delta {delta:+.2f}")
                
                scale = 0.05 if delta > 0 else 0.2
                head['gene'] += np.random.normal(0, scale, size=7)
                head['gene'][5] = np.clip(head['gene'][5], 0.5, 3.5)

            if self.global_best_score > 80.0:
                print("   > Heavy-Head Problem Solved.")
                break
                
        return self.global_best_gene

if __name__ == "__main__":
    try:
        trainer = CounterweightTrainer("BipedalWalker-v3", n_heads=6)
        best_gene = trainer.run(generations=15)
        
        print("\nVisualizing the Counterweighted Walker...")
        dummy_sk = DeltaScorekeeper()
        trainer.evaluate(best_gene, dummy_sk, render=True)
    except Exception as e:
        print(f"Error: {e}")