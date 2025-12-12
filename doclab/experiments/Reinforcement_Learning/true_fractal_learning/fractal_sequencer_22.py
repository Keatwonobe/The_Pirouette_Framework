import gymnasium as gym
import numpy as np
from collections import deque

# ============================================================
# 1. KINESTHETIC HYPERNET (The Soul - v11)
# ============================================================
class KinestheticHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def get_potential_energy(self, x, y):
        # Henon-Heiles Potential (Chaos Metric)
        return 0.5 * (x**2 + y**2) + (x**2 * y - (1.0/3.0) * y**3)

    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt = 1.0, 0.1
        
        # v19 Basin Coloring
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"     # Stable
        elif abs(theta) > 2.5: color = "Red"     # Chaos
        else:                  color = "Gold"    # Transition

        # Fast Fractal Iteration
        for _ in range(self.output_dim // 2 + 1):
            grad_m = curr_m + 2 * sigma * curr_m * curr_l
            grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
            curr_m += dt * grad_m
            curr_l += dt * grad_l
            weights.extend([np.tanh(curr_m), np.tanh(curr_l)])
            
        return np.array(weights[:self.output_dim], dtype=np.float32), color

# ============================================================
# 2. HILDEBRAND OSCILLATOR (The Clock - v20)
# ============================================================
class HildebrandOscillator:
    def __init__(self):
        self.phase_counter = 0.0
        
    def get_phase_targets(self, t_step, freq, beta, phi):
        self.phase_counter = (self.phase_counter + (0.02 * freq)) % 1.0
        
        # Calculate Phase for both legs
        p1 = self.phase_counter
        p2 = (self.phase_counter + phi) % 1.0
        
        def get_leg_state(p, b):
            # STANCE (Foot on ground)
            if p < b: 
                prog = p / b
                # Hip drives BACK (-1.0) to push body
                hip_t = 1.0 - (2.0 * prog) 
                knee_t = 0.0 # Straight leg
                return hip_t, knee_t, True # True = Stance
            
            # SWING (Foot in air)
            else: 
                prog = (p - b) / (1.0 - b)
                # Hip drives FORWARD
                hip_t = -1.0 + (2.0 * prog)
                # Knee flexes to clear ground
                knee_t = -1.0 if prog < 0.5 else 0.0
                return hip_t, knee_t, False # False = Swing

        return get_leg_state(p1, beta), get_leg_state(p2, beta)

# ============================================================
# 3. REFLEXIVE BALLAST (The Body - v19 Upgraded)
# ============================================================
class ReflexiveBallast:
    def __init__(self):
        self.static_mass = 5.0
        self.dynamic_gain = 3.0
        
    def get_stabilization(self, hull_angle, velocity, knottedness):
        """
        Returns:
        1. Torque: To apply to hips (to pull hull back)
        2. Tension: To apply to KNEES (to prevent buckling)
        """
        # 1. Calculate Torque (v19 Logic)
        lean_torque = -self.static_mass * np.cos(hull_angle)
        
        # If running fast (velocity > 0), we need more lean compensation
        run_torque  = -np.clip(velocity, 0, 2.0) * self.dynamic_gain * np.cos(hull_angle)
        
        # If performing high-knot maneuver, brace the core
        knot_brace = 1.0 + (knottedness * 0.5)
        
        total_torque = (lean_torque + run_torque) * knot_brace
        
        # 2. Calculate "Buckle Tension" (The v21 Fix)
        # If the Hull is leaning forward (angle < 0), the knees are under load.
        # We return a tension multiplier.
        if hull_angle < 0:
            # The more we lean forward, the tighter the knees must be
            tension = 1.0 + (abs(hull_angle) * 5.0)
        else:
            tension = 1.0
            
        return total_torque, tension

# ============================================================
# 4. CHIMERA AGENT v21
# ============================================================
class ChimeraAgent:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.hypernet = KinestheticHypernet(8) 
        dummy.close()
        
        self.oscillator = HildebrandOscillator()
        self.ballast = ReflexiveBallast()
        self.history = deque(maxlen=5)

    def calculate_knottedness(self, m, lam):
        self.history.append(np.array([m, lam]))
        if len(self.history) < 3: return 0.0
        
        # Curvature Approximation
        v = self.history[-1] - self.history[-2]
        a = v - (self.history[-2] - self.history[-3])
        cross = abs(v[0]*a[1] - v[1]*a[0])
        curve = cross / (np.linalg.norm(v)**3 + 1e-9)
        
        V = abs(self.hypernet.get_potential_energy(m, lam))
        return min(V * curve, 10.0)

    def get_action_data(self, obs, t_step):
        cm, cl, rm, rl, tilt, freq, phase = self.gene
        
        # --- 1. FRACTAL HEART ---
        angle = phase + (t_step * 0.02 * freq * 2 * np.pi)
        m = cm + (rm * np.cos(angle) * np.cos(tilt) - rl * np.sin(angle) * np.sin(tilt))
        lam = cl + (rm * np.cos(angle) * np.sin(tilt) + rl * np.sin(angle) * np.cos(tilt))
        
        k_val = self.calculate_knottedness(m, lam)
        weights, color = self.hypernet.generate_weights(m, lam)
        
        # --- 2. HILDEBRAND GAIT ---
        beta = np.clip(0.55 + (m * 0.2), 0.4, 0.8)
        phi = (lam + 1.0) / 2.0 % 1.0
        (h1_t, k1_t, s1), (h2_t, k2_t, s2) = \
            self.oscillator.get_phase_targets(t_step, freq, beta, phi)
            
        # --- 3. REFLEXIVE BALLAST (The Buckle Fix) ---
        # We get Torque (for hips) AND Tension (for knees)
        bal_torque, bal_tension = self.ballast.get_stabilization(obs[0], obs[2], k_val)
        
        # --- 4. MOTOR CONTROL ---
        gains = (weights + 1.0) * 4.0 # Base stiffness
        
        actions = np.zeros(4)
        
        # LEG 1 (Right)
        # Hip: Drive + Ballast
        actions[0] = (gains[0] * (h1_t - obs[4])) + bal_torque
        
        # Knee: Stance Lock + Buckle Reflex
        # If Stance: Base stiff * Buckle Tension. If Swing: Low stiff.
        k_stiff1 = gains[1] * (bal_tension if s1 else 0.2)
        
        # Damping: If falling (High Tension), increase Damping to stop jitter
        k_damp1  = gains[1] * (0.5 if s1 else 0.1) 
        
        actions[1] = (k_stiff1 * (k1_t - obs[6])) - (k_damp1 * obs[7])
        
        # LEG 2 (Left)
        actions[2] = (gains[2] * (h2_t - obs[9])) + bal_torque
        
        k_stiff2 = gains[3] * (bal_tension if s2 else 0.2)
        k_damp2  = gains[3] * (0.5 if s2 else 0.1)
        
        actions[3] = (k_stiff2 * (k2_t - obs[11])) - (k_damp2 * obs[12])
        
        return np.tanh(actions), k_val, bal_torque

# ============================================================
# 5. TRAINER
# ============================================================
class ChimeraTrainer:
    def __init__(self, env_name):
        self.env_name = env_name
        
    def evaluate(self, gene, render=False):
        agent = ChimeraAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        total_knot = 0
        steps = 0
        
        while steps < 800:
            action, k_val, _ = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            
            total_knot += k_val
            steps += 1
            if term or trunc: break
        
        dist = env.unwrapped.hull.position.x - start_x
        env.close()
        
        # Fitness: Distance is King, Knot is the Queen.
        # If it falls (dist < 20), Knot score is zeroed to prevent seizing.
        fitness = dist + (total_knot * 0.1 if dist > 20 else 0)
        return fitness, dist, total_knot

    def run(self):
        print("👹 CHIMERA v21: 'The Buckle Reflex'")
        print("   Goal: Prevent face-plants using Dynamic Knee Tension.")
        
        # Seed with known good averages
        population = []
        for _ in range(10):
            gene = np.array([
                0.0, 0.0,    # Center
                0.8, 0.8,    # Radius
                0.5,         # Tilt
                1.5,         # Freq (Faster is actually more stable for dynamic walkers)
                0.0          # Phase
            ])
            population.append(gene + np.random.normal(0, 0.2, 7))

        best_gene = population[0]
        best_fit = -100
        
        for g in range(50):
            for i, gene in enumerate(population):
                fit, dist, knot = self.evaluate(gene)
                if fit > best_fit:
                    best_fit = fit
                    best_gene = gene.copy()
                    print(f"   Gen {g} Record: {dist:.1f}m (Knot: {knot:.0f})")
            
            # Elitist Mutation
            population = [best_gene + np.random.normal(0, 0.1, 7) for _ in range(100)]
            
        return best_gene

if __name__ == "__main__":
    trainer = ChimeraTrainer("BipedalWalker-v3")
    best = trainer.run()
    trainer.evaluate(best, render=True)