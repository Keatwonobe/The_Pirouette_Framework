import gymnasium as gym
import numpy as np
from collections import deque
import math

# ============================================================
# 1. CORE PHYSICS (v24 Ratchet Standard)
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
# 2. MOSAIC AGENT (The Splicer)
# ============================================================
class MosaicAgent:
    def __init__(self, env_name, mosaic_strip, slice_size=50):
        """
        mosaic_strip: List of Genes (one for each 50-step slice)
        """
        self.mosaic_strip = mosaic_strip
        self.slice_size = slice_size
        self.fade = 10 # Crossfade duration to prevent motor jerks
        
        dummy = gym.make(env_name)
        self.hypernet = KinestheticHypernet(8) 
        dummy.close()
        
        self.oscillator = HildebrandOscillator()
        self.ballast = ReflexiveBallast()
        self.history = deque(maxlen=5)

    def get_active_gene(self, t_step):
        # 1. Determine which "Frame" we are in
        frame_idx = min(t_step // self.slice_size, len(self.mosaic_strip) - 1)
        current_gene = self.mosaic_strip[frame_idx]
        
        # 2. Check for Transition (Crossfade)
        # If we are nearing the end of a frame, start blending with the next
        steps_into_frame = t_step % self.slice_size
        steps_left = self.slice_size - steps_into_frame
        
        if steps_left < self.fade and frame_idx < len(self.mosaic_strip) - 1:
            next_gene = self.mosaic_strip[frame_idx + 1]
            progress = (self.fade - steps_left) / self.fade
            # Linear Interpolation
            return ((1 - progress) * current_gene) + (progress * next_gene)
            
        return current_gene

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
# 3. MOSAIC TRAINER (Weaver Logic)
# ============================================================
class MosaicTrainer:
    def __init__(self, env_name):
        self.env_name = env_name
        self.total_steps = 800
        self.slice_size = 50
        self.num_frames = self.total_steps // self.slice_size
        self.breath_cycle = 4
        
        # THE ARCHIVE: A list of 16 genes, initially identical
        # [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        starter_gene = np.array([0.0, 0.0, 0.8, 0.8, 0.5, 1.5, 0.0])
        self.archive = [starter_gene.copy() for _ in range(self.num_frames)]
        
        self.global_best_dist = 0.0

    def evaluate(self, mosaic_strip, phase, render=False):
        agent = MosaicAgent(self.env_name, mosaic_strip, self.slice_size)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        total_knot = 0
        steps = 0
        
        while steps < self.total_steps:
            action, k_val, _ = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            total_knot += k_val
            steps += 1
            if term or trunc: break
        
        dist = env.unwrapped.hull.position.x - start_x
        env.close()
        
        # Inhale/Exhale Logic (v24)
        if phase == "INHALE":
            knot_bonus = math.log1p(total_knot) 
            fitness = dist * (1.0 + (knot_bonus * 0.1))
        else:
            fitness = dist 
            
        return fitness, dist, total_knot

    def run(self):
        print("🎞️ MOSAIC WEAVER: Temporal Splicing")
        print(f"   Stitching {self.num_frames} distinct timescales.")
        
        for g in range(300):
            # 1. Determine Phase
            if (g % self.breath_cycle) < 2:
                phase = "INHALE"; icon = "⚡"; mut_scale = 0.2
            else:
                phase = "EXHALE"; icon = "🛡️"; mut_scale = 0.05
            
            print(f"\n--- Gen {g} [{icon} {phase}] ---")
            
            # 2. Create Population based on Archive
            # Each candidate is the Archive, but with ONE or TWO frames Mutated.
            population = []
            
            # Candidate 0: The pure Archive (Control Group)
            population.append({'strip': [g.copy() for g in self.archive], 'mutations': []})
            
            for _ in range(12):
                # Copy the archive
                candidate_strip = [g.copy() for g in self.archive]
                
                # Pick 1 random frame to mutate
                idx1 = np.random.randint(0, self.num_frames)
                candidate_strip[idx1] += np.random.normal(0, mut_scale, 7)
                
                # In Inhale, maybe mutate a second frame too (more chaos)
                idx2 = -1
                if phase == "INHALE" and np.random.rand() > 0.5:
                    idx2 = np.random.randint(0, self.num_frames)
                    candidate_strip[idx2] += np.random.normal(0, mut_scale, 7)
                
                population.append({'strip': candidate_strip, 'mutations': [idx1, idx2]})

            # 3. Evaluate
            gen_best_fit = -999
            gen_best_dist = 0
            best_strip = None
            winning_indices = []
            
            for candidate in population:
                fit, dist, knot = self.evaluate(candidate['strip'], phase)
                
                if fit > gen_best_fit:
                    gen_best_fit = fit
                    gen_best_dist = dist
                    best_strip = candidate['strip']
                    winning_indices = candidate['mutations']

            print(f"   ★ Best: {gen_best_dist:.1f}m | Fit: {gen_best_fit:.1f}")
            
            # 4. UPDATE THE ARCHIVE
            # If the best strip beat our previous records, we bake the mutations into the Archive.
            # We trust the result: if changing Frame 3 made the whole run better, Frame 3 gets updated.
            if gen_best_dist >= self.global_best_dist * 0.95: # Allow slight dips if Fit is high (Inhale)
                if gen_best_dist > self.global_best_dist:
                    self.global_best_dist = gen_best_dist
                    print(f"   🏆 NEW RECORD. Archive Updated at frames {winning_indices}")
                
                # Commit the best strip to be the new Archive
                self.archive = [g.copy() for g in best_strip]
            else:
                print(f"   (Run rejected. Keeping previous Archive)")

        return self.archive

if __name__ == "__main__":
    trainer = MosaicTrainer("BipedalWalker-v3")
    final_strip = trainer.run()
    
    print("\nPlaying the Master Tape...")
    trainer.evaluate(final_strip, "EXHALE", render=True)