import gymnasium as gym
import numpy as np
from collections import deque
import math

# ============================================================
# 1. KINESTHETIC HYPERNET (The Brain)
# ============================================================
class KinestheticHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def get_potential_energy(self, x, y):
        # Henon-Heiles Potential
        return 0.5 * (x**2 + y**2) + (x**2 * y - (1.0/3.0) * y**3)

    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt = 1.0, 0.1
        
        # Basin Visualization
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"     # Stable
        elif abs(theta) > 2.5: color = "Red"     # Chaos
        else:                  color = "Gold"    # Transition

        # Fractal Iteration
        for _ in range(self.output_dim // 2 + 1):
            grad_m = curr_m + 2 * sigma * curr_m * curr_l
            grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
            curr_m += dt * grad_m
            curr_l += dt * grad_l
            weights.extend([np.tanh(curr_m), np.tanh(curr_l)])
            
        return np.array(weights[:self.output_dim], dtype=np.float32), color

# ============================================================
# 2. HILDEBRAND OSCILLATOR (The Clock)
# ============================================================
class HildebrandOscillator:
    def __init__(self):
        self.phase_counter = 0.0
        
    def get_phase_targets(self, t_step, freq, beta, phi):
        self.phase_counter = (self.phase_counter + (0.02 * freq)) % 1.0
        
        p1 = self.phase_counter
        p2 = (self.phase_counter + phi) % 1.0
        
        def get_leg_state(p, b):
            # STANCE
            if p < b: 
                prog = p / b
                return 1.0 - (2.0 * prog), 0.0, True
            # SWING
            else: 
                prog = (p - b) / (1.0 - b)
                return -1.0 + (2.0 * prog), (-1.0 if prog < 0.5 else 0.0), False

        return get_leg_state(p1, beta), get_leg_state(p2, beta)

# ============================================================
# 3. REFLEXIVE BALLAST (The Body)
# ============================================================
class ReflexiveBallast:
    def __init__(self):
        self.static_mass = 5.0
        self.dynamic_gain = 3.0
        
    def get_stabilization(self, hull_angle, velocity, knottedness):
        # 1. Torque
        lean_torque = -self.static_mass * np.cos(hull_angle)
        run_torque  = -np.clip(velocity, 0, 2.0) * self.dynamic_gain * np.cos(hull_angle)
        
        # "Brace for Chaos"
        knot_brace = 1.0 + (knottedness * 0.5)
        total_torque = (lean_torque + run_torque) * knot_brace
        
        # 2. Tension (Buckle Reflex)
        tension = 1.0 + (abs(hull_angle) * 5.0) if hull_angle < 0 else 1.0
            
        return total_torque, tension

# ============================================================
# 4. CHIMERA AGENT v21 (Unchanged Physics)
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
        
        v = self.history[-1] - self.history[-2]
        a = v - (self.history[-2] - self.history[-3])
        cross = abs(v[0]*a[1] - v[1]*a[0])
        curve = cross / (np.linalg.norm(v)**3 + 1e-9)
        
        V = abs(self.hypernet.get_potential_energy(m, lam))
        return min(V * curve, 10.0)

    def get_action_data(self, obs, t_step):
        cm, cl, rm, rl, tilt, freq, phase = self.gene
        
        angle = phase + (t_step * 0.02 * freq * 2 * np.pi)
        m = cm + (rm * np.cos(angle) * np.cos(tilt) - rl * np.sin(angle) * np.sin(tilt))
        lam = cl + (rm * np.cos(angle) * np.sin(tilt) + rl * np.sin(angle) * np.cos(tilt))
        
        k_val = self.calculate_knottedness(m, lam)
        weights, color = self.hypernet.generate_weights(m, lam)
        
        beta = np.clip(0.55 + (m * 0.2), 0.4, 0.8)
        phi = (lam + 1.0) / 2.0 % 1.0
        (h1_t, k1_t, s1), (h2_t, k2_t, s2) = self.oscillator.get_phase_targets(t_step, freq, beta, phi)
            
        bal_torque, bal_tension = self.ballast.get_stabilization(obs[0], obs[2], k_val)
        
        gains = (weights + 1.0) * 4.0 
        actions = np.zeros(4)
        
        # Leg 1
        actions[0] = (gains[0] * (h1_t - obs[4])) + bal_torque
        k_stiff1 = gains[1] * (bal_tension if s1 else 0.2)
        actions[1] = (k_stiff1 * (k1_t - obs[6])) - (gains[1] * (0.5 if s1 else 0.1) * obs[7])
        
        # Leg 2
        actions[2] = (gains[2] * (h2_t - obs[9])) + bal_torque
        k_stiff2 = gains[3] * (bal_tension if s2 else 0.2)
        actions[3] = (k_stiff2 * (k2_t - obs[11])) - (gains[3] * (0.5 if s2 else 0.1) * obs[12])
        
        return np.tanh(actions), k_val, color

# ============================================================
# 5. BREATHING TRAINER (The New Logic)
# ============================================================
class BreathingTrainer:
    def __init__(self, env_name):
        self.env_name = env_name
        self.breath_cycle = 6 # Total generations in one breath (3 Inhale, 3 Exhale)
        
    def evaluate(self, gene, phase, render=False):
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
        
        # --- THE BREATHING LOGIC ---
        if phase == "INHALE":
            # REWARD CHAOS: We want new structures.
            # We pay the agent in Knots.
            fitness = dist + (total_knot * 0.2)
        else:
            # EXHALE (Consolidation):
            # PUNISH CHAOS: We want efficiency.
            # If two agents go the same distance, the one who did it smoother wins.
            fitness = dist - (total_knot * 0.05) 
            
        return fitness, dist, total_knot

    def run(self):
        print("🫁 IRON LUNG PROTOCOL: Pulsed Learning")
        print("   Inhale: Reward Complexity. Exhale: Punish Inefficiency.")
        
        # Seed with stable walker params
        population = []
        for _ in range(12):
            gene = np.array([0.0, 0.0, 0.8, 0.8, 0.5, 1.5, 0.0])
            population.append(gene + np.random.normal(0, 0.3, 7))

        best_gene = population[0]
        
        for g in range(30):
            # Determine Breath Phase
            cycle_pos = g % self.breath_cycle
            if cycle_pos < (self.breath_cycle // 2):
                phase = "INHALE"
                icon = "😤"
                mutation_scale = 0.2 # High Mutation during Inhale
            else:
                phase = "EXHALE"
                icon = "😮‍💨"
                mutation_scale = 0.05 # Fine-tuning during Exhale
                
            print(f"\n--- Gen {g} [{icon} {phase}] ---")
            
            gen_best_fit = -999
            
            for i, gene in enumerate(population):
                fit, dist, knot = self.evaluate(gene, phase)
                
                if fit > gen_best_fit:
                    gen_best_fit = fit
                    best_gene = gene.copy()
                    print(f"   ★ Record: {dist:.1f}m (Knot: {knot:.0f}) | Fit: {fit:.1f}")
            
            # Elitist Mutation
            # We keep the best, and mutate copies of it.
            # This 'ratchets' the progress.
            population = [best_gene.copy()] # Keep the king
            for _ in range(11):
                noise = np.random.normal(0, mutation_scale, 7)
                population.append(best_gene + noise)
            
        return best_gene

if __name__ == "__main__":
    trainer = BreathingTrainer("BipedalWalker-v3")
    best = trainer.run()
    print("\nFinal Result Verification...")
    trainer.evaluate(best, "EXHALE", render=True)