import gymnasium as gym
import numpy as np
from collections import deque

# ============================================================
# 1. KINESTHETIC HYPERNET (The Brain)
# ============================================================
class KinestheticHypernet:
    """
    Combines v11's Henon-Heiles Potential with v19's robustness.
    """
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def get_potential_energy(self, x, y):
        # From v11: The Chaos Metric
        return 0.5 * (x**2 + y**2) + (x**2 * y - (1.0/3.0) * y**3)

    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt = 1.0, 0.1
        
        # v19 Basin Coloring
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"     # Stable Basin
        elif abs(theta) > 2.5: color = "Red"     # Chaos Basin
        else:                  color = "Gold"    # Transition Basin

        for _ in range(self.output_dim // 2 + 1):
            # The Fractal Iteration
            grad_m = curr_m + 2 * sigma * curr_m * curr_l
            grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
            curr_m += dt * grad_m
            curr_l += dt * grad_l
            weights.extend([np.tanh(curr_m), np.tanh(curr_l)])
            
        return np.array(weights[:self.output_dim], dtype=np.float32), color

# ============================================================
# 2. HILDEBRAND OSCILLATOR (The Rhythm - v17)
# ============================================================
class HildebrandOscillator:
    def __init__(self):
        self.phase_counter = 0.0
        
    def get_target_angles(self, t_step, freq, beta, phi):
        self.phase_counter = (self.phase_counter + (0.02 * freq)) % 1.0
        
        p1 = self.phase_counter
        p2 = (self.phase_counter + phi) % 1.0
        
        def waveform(p, b):
            # v17 Waveform Logic
            if p < b: return 1.0 - (2.0 * (p / b))      # Stance
            else:     return -1.0 + (2.0 * (p-b)/(1-b)) # Swing
            
        return waveform(p1, beta), waveform(p2, beta)

# ============================================================
# 3. DYNAMIC BALLAST (The Body - v19 + v11 Logic)
# ============================================================
class DynamicBallast:
    def __init__(self):
        self.static_mass = 5.0
        self.dynamic_gain = 3.0
        
    def get_torque(self, hull_angle, velocity, knottedness):
        """
        KEY INNOVATION: 
        We use 'Knottedness' (Chaos) to overdrive the Ballast.
        If the agent is doing something crazy (High K), we stiffen the core.
        """
        # 1. Base Physical Stabilization (v19)
        lean_torque = -self.static_mass * np.cos(hull_angle)
        run_torque  = -np.clip(velocity, 0, 2.0) * self.dynamic_gain * np.cos(hull_angle)
        
        base_torque = lean_torque + run_torque
        
        # 2. The "Core Brace" (Kinesthetic Injection)
        # If Knottedness is high, we multiply the stabilizing force.
        # This allows the agent to "lean into" the chaos without falling.
        stability_multiplier = 1.0 + (knottedness * 0.5) 
        
        return base_torque * stability_multiplier

# ============================================================
# 4. CHIMERA AGENT
# ============================================================
class ChimeraAgent:
    def __init__(self, env_name, gene):
        self.gene = gene # [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        
        dummy = gym.make(env_name)
        self.hypernet = KinestheticHypernet(8) # 4 joints * 2 (Gain, Offset)
        dummy.close()
        
        self.oscillator = HildebrandOscillator()
        self.ballast = DynamicBallast()
        self.history = deque(maxlen=5) # For Knottedness calc

    def calculate_knottedness(self, m, lam):
        # v11: The Soul Calculation
        self.history.append(np.array([m, lam]))
        if len(self.history) < 3: return 0.0
        
        # Curvature Calculation
        r_curr, r_prev, r_prev2 = self.history[-1], self.history[-2], self.history[-3]
        v = r_curr - r_prev
        a = (r_curr - r_prev) - (r_prev - r_prev2)
        
        cross_prod = abs(v[0]*a[1] - v[1]*a[0])
        curvature = cross_prod / (np.linalg.norm(v)**3 + 1e-9)
        
        # Potential Energy Weighting
        V = abs(self.hypernet.get_potential_energy(m, lam))
        return min(V * curvature, 10.0)

    def get_action_data(self, obs, t_step):
        cm, cl, rm, rl, tilt, freq, phase = self.gene
        
        # --- 1. THE FRACTAL ORBIT ---
        # The source of the movement pattern
        angle = phase + (t_step * 0.02 * 0.5 * 2 * np.pi)
        m = cm + (rm * np.cos(angle) * np.cos(tilt) - rl * np.sin(angle) * np.sin(tilt))
        lam = cl + (rm * np.cos(angle) * np.sin(tilt) + rl * np.sin(angle) * np.cos(tilt))
        
        # --- 2. KNOTTEDNESS (The Metric of Soul) ---
        k_val = self.calculate_knottedness(m, lam)
        
        # --- 3. HILDEBRAND GAIT (The Rhythm) ---
        # We Map Fractal -> Gait Params
        beta = np.clip(0.55 + (m * 0.2), 0.4, 0.8) # Duty Factor
        phi = (lam + 1.0) / 2.0 % 1.0              # Relative Phase
        
        t_hip1, t_hip2 = self.oscillator.get_target_angles(t_step, freq, beta, phi)
        
        # --- 4. DYNAMIC BALLAST (The Stability) ---
        # Note we pass k_val (Chaos) into the Ballast!
        ballast_torque = self.ballast.get_torque(obs[0], obs[2], k_val)
        
        # --- 5. SYNTHESIS ---
        weights, color = self.hypernet.generate_weights(m, lam)
        gains = (weights + 1.0) * 4.0 # Dynamic muscle stiffness
        
        # Hip Control: Oscillator + Ballast + Reflex
        # We inject the Ballast Torque directly into the Hips
        act_h1 = (gains[0] * (t_hip1 - obs[4])) + ballast_torque
        act_h2 = (gains[2] * (t_hip2 - obs[9])) + ballast_torque
        
        # Knee Control: Damping
        act_k1 = -0.1 * obs[7]
        act_k2 = -0.1 * obs[12]
        
        actions = np.array([act_h1, act_k1, act_h2, act_k2])
        return np.tanh(actions), k_val, ballast_torque

# ============================================================
# 5. KINESTHETIC TRAINER
# ============================================================
class KinestheticTrainer:
    def __init__(self, env_name):
        self.env_name = env_name
        
    def evaluate(self, gene, render=False):
        agent = ChimeraAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        total_dist = 0
        total_knot = 0 # Accumulate creativity
        steps = 0
        start_x = env.unwrapped.hull.position.x
        
        while steps < 600:
            action, k_val, ballast = agent.get_action_data(obs, steps)
            obs, r, term, trunc, _ = env.step(action)
            
            total_knot += k_val
            steps += 1
            if term or trunc: break
            
        final_x = env.unwrapped.hull.position.x
        dist = final_x - start_x
        
        # FITNESS FUNCTION: The Key to restoring "Soul"
        # We reward Distance (Competence) AND Knottedness (Creativity)
        # But we only reward Knottedness IF they walked a decent distance.
        if dist > 20.0:
            fitness = dist + (total_knot * 0.2) 
        else:
            fitness = dist # Don't reward seizures on the starting line
            
        return fitness, dist, total_knot

    def run(self, generations=10):
        print(f"🧬 CHIMERA PROTOCOL: Fusing v11 Soul + v19 Body")
        population = [np.random.normal(0,1,7) for _ in range(10)]
        
        best_gene = None
        best_fit = -999
        
        for g in range(generations):
            for i, gene in enumerate(population):
                fit, dist, knot = self.evaluate(gene)
                if fit > best_fit:
                    best_fit = fit
                    best_gene = gene.copy()
                    print(f"   Gen {g} New Best: Fit {fit:.1f} (Dist {dist:.1f}m + Knot {knot:.1f})")
            
            # Simple Mutation
            population = [best_gene + np.random.normal(0, 0.1, 7) for _ in range(10)]
            
        return best_gene

if __name__ == "__main__":
    trainer = KinestheticTrainer("BipedalWalker-v3")
    best_gn = trainer.run(generations=5)
    print("Visualizing Chimera...")
    trainer.evaluate(best_gn, render=True)