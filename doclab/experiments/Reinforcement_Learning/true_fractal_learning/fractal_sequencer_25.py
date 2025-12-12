import gymnasium as gym
import numpy as np
from collections import deque
import math

# ============================================================
# 1. CORE PHYSICS (v24 Standard)
# ============================================================
class KinestheticHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
    
    def get_potential_energy(self, x, y):
        return 0.5 * (x**2 + y**2) + (x**2 * y - (1.0/3.0) * y**3)

    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt = 1.0, 0.1
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"
        elif abs(theta) > 2.5: color = "Red"
        else:                  color = "Gold"

        for _ in range(self.output_dim // 2 + 1):
            grad_m = curr_m + 2 * sigma * curr_m * curr_l
            grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
            curr_m += dt * grad_m
            curr_l += dt * grad_l
            weights.extend([np.tanh(curr_m), np.tanh(curr_l)])
        return np.array(weights[:self.output_dim], dtype=np.float32), color

class HildebrandOscillator:
    def __init__(self):
        self.phase_counter = 0.0
    
    def get_phase_targets(self, t_step, freq, beta, phi):
        self.phase_counter = (self.phase_counter + (0.02 * freq)) % 1.0
        p1 = self.phase_counter
        p2 = (self.phase_counter + phi) % 1.0
        
        def get_leg_state(p, b):
            if p < b: return 1.0 - (2.0 * p/b), 0.0, True
            else: 
                prog = (p - b) / (1.0 - b)
                return -1.0 + (2.0 * prog), (-1.0 if prog < 0.5 else 0.0), False
        return get_leg_state(p1, beta), get_leg_state(p2, beta)

class ReflexiveBallast:
    def __init__(self):
        self.static_mass = 5.0
        self.dynamic_gain = 3.0
    def get_stabilization(self, hull_angle, velocity, knottedness):
        lean_torque = -self.static_mass * np.cos(hull_angle)
        run_torque  = -np.clip(velocity, 0, 2.0) * self.dynamic_gain * np.cos(hull_angle)
        knot_brace = 1.0 + min(knottedness * 0.5, 5.0)
        total_torque = (lean_torque + run_torque) * knot_brace
        tension = 1.0 + (abs(hull_angle) * 5.0) if hull_angle < 0 else 1.0
        return total_torque, tension

# ============================================================
# 2. CHRONOS AGENT (The Time Stitcher)
# ============================================================
class ChronosAgent:
    def __init__(self, env_name, locked_timeline, candidate_gene, splice_time):
        """
        locked_timeline: List of genes [(time_0, gene_A), (time_50, gene_B)...]
        candidate_gene: The experimental gene we are testing NOW.
        splice_time: The step where we switch from History to Experiment.
        """
        self.locked_timeline = locked_timeline
        self.candidate_gene = candidate_gene
        self.splice_time = splice_time
        self.fade_window = 10 # Steps to smooth the transition
        
        dummy = gym.make(env_name)
        self.hypernet = KinestheticHypernet(8) 
        dummy.close()
        
        self.oscillator = HildebrandOscillator()
        self.ballast = ReflexiveBallast()
        self.history = deque(maxlen=5)

    def get_active_gene(self, t_step):
        # 1. PAST: If we are well before the splice, use the Locked Timeline
        if t_step < self.splice_time:
            # Find the gene responsible for this segment
            # (Simple implementation: Use the last locked gene)
            return self.locked_timeline[-1]
            
        # 2. FUTURE: If we are past the splice + fade, use Candidate
        elif t_step >= self.splice_time + self.fade_window:
            return self.candidate_gene
            
        # 3. TRANSITION: Cross-fade (Linear Interpolation)
        else:
            progress = (t_step - self.splice_time) / self.fade_window
            gene_past = self.locked_timeline[-1]
            gene_future = self.candidate_gene
            return (1 - progress) * gene_past + progress * gene_future

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
        # KEY: Get the spliced gene for this exact moment in time
        gene = self.get_active_gene(t_step)
        
        cm, cl, rm, rl, tilt, freq, phase = gene
        
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
        
        actions[0] = (gains[0] * (h1_t - obs[4])) + bal_torque
        k_stiff1 = gains[1] * (bal_tension if s1 else 0.2)
        actions[1] = (k_stiff1 * (k1_t - obs[6])) - (gains[1] * (0.5 if s1 else 0.1) * obs[7])
        
        actions[2] = (gains[2] * (h2_t - obs[9])) + bal_torque
        k_stiff2 = gains[3] * (bal_tension if s2 else 0.2)
        actions[3] = (k_stiff2 * (k2_t - obs[11])) - (gains[3] * (0.5 if s2 else 0.1) * obs[12])
        
        return np.tanh(actions), k_val, color

# ============================================================
# 3. CHRONOS TRAINER (The TAS Logic)
# ============================================================
class ChronosTrainer:
    def __init__(self, env_name):
        self.env_name = env_name
        # The Timeline: Starts with a generic gene at T=0
        self.locked_timeline = [np.array([0.0, 0.0, 0.8, 0.8, 0.5, 1.5, 0.0])]
        self.splice_time = 0
        self.segment_length = 50 # How many steps to conquer at a time
        
    def evaluate(self, candidate_gene, render=False):
        # We create the spliced agent
        agent = ChronosAgent(self.env_name, self.locked_timeline, candidate_gene, self.splice_time)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        total_knot = 0
        steps = 0
        
        # We run for PAST + SEGMENT + BUFFER
        max_steps = self.splice_time + self.segment_length + 20
        
        while steps < max_steps:
            action, k_val, _ = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            
            # Only count knots in the NEW territory (Experimental phase)
            if steps >= self.splice_time:
                total_knot += k_val
                
            steps += 1
            if term or trunc: break
        
        dist = env.unwrapped.hull.position.x - start_x
        env.close()
        
        # Fitness:
        # 1. MUST survive the splice duration
        if steps < self.splice_time + self.segment_length:
            return -100.0, dist, total_knot # Died too early
        
        # 2. If survived, maximize distance & complexity
        fitness = dist + (math.log1p(total_knot) * 0.5)
        return fitness, dist, total_knot

    def run(self):
        print("⏳ CHRONOS STITCHER: TAS Protocol")
        print(f"   Building a run in {self.segment_length}-step chunks.")
        
        current_best_gene = self.locked_timeline[0].copy()
        
        # We will stitch 10 segments (approx 500 steps)
        for segment in range(10):
            target_time = self.splice_time + self.segment_length
            print(f"\n--- Segment {segment+1}: Steps {self.splice_time} -> {target_time} ---")
            
            # Population seeded from the LAST WINNER
            # This ensures we start with a gene that works, and mutate from there.
            population = [current_best_gene.copy()] 
            for _ in range(11):
                population.append(current_best_gene + np.random.normal(0, 0.2, 7))
                
            segment_best_fit = -float('inf')
            segment_winner = None
            
            # Evolve for this specific time slice
            for gen in range(5): # Fast evolution per slice
                gen_best_fit = -float('inf')
                
                for i, gene in enumerate(population):
                    fit, dist, knot = self.evaluate(gene)
                    
                    if fit > gen_best_fit:
                        gen_best_fit = fit
                        best_in_gen = gene.copy()
                        
                    if fit > segment_best_fit:
                        segment_best_fit = fit
                        segment_winner = gene.copy()
                        # print(f"   ★ Splice Candidate: {dist:.1f}m (Fit {fit:.1f})")
                
                print(f"   Gen {gen}: Best Fit {gen_best_fit:.1f}")
                
                # Elitism for next gen
                population = [best_in_gen.copy()]
                for _ in range(11):
                    population.append(best_in_gen + np.random.normal(0, 0.1, 7))
            
            # --- LOCK THE SEGMENT ---
            if segment_winner is not None:
                print(f"🔒 SEGMENT LOCKED. Saving State at T={target_time}")
                # We update the timeline!
                # Note: We don't append to list, we just update the 'current_best' 
                # effectively saying "From here on out, use this gene as the base."
                # In a full stitcher, we would append to a list, but for simplicity 
                # here we are evolving a single evolving vector that gets "Checkpointed".
                self.locked_timeline.append(segment_winner)
                self.splice_time = target_time
                current_best_gene = segment_winner
            else:
                print("💀 SEGMENT FAILED. Retrying previous checkpoint.")
                # Don't advance splice_time, try again
                
        return current_best_gene

if __name__ == "__main__":
    trainer = ChronosTrainer("BipedalWalker-v3")
    best = trainer.run()
    
    print("\nVisualizing Full TAS Run...")
    # To view, we set splice time to infinity so it uses the accumulated timeline logic
    # (Simplified for viewing: just play the final result)
    # Ideally, we'd play the whole history list.
    trainer.splice_time = 0 # Reset for full run view using the final gene
    trainer.evaluate(best, render=True)