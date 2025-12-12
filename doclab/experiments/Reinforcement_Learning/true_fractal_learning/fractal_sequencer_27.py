import gymnasium as gym
import numpy as np
from collections import deque
import math

# ============================================================
# 1. PHYSICS ENGINE (v24 Ratchet Standard)
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
        p1, p2 = self.phase_counter, (self.phase_counter + phi) % 1.0
        def get_leg(p, b):
            if p < b: return 1.0 - (2.0 * p/b), 0.0, True
            else: 
                prog = (p - b) / (1.0 - b)
                return -1.0 + (2.0 * prog), (-1.0 if prog < 0.5 else 0.0), False
        return get_leg(p1, beta), get_leg(p2, beta)

class ReflexiveBallast:
    def __init__(self):
        self.static_mass = 5.0
        self.dynamic_gain = 3.0
    def get_stabilization(self, hull_angle, velocity, knottedness):
        lean = -self.static_mass * np.cos(hull_angle)
        run  = -np.clip(velocity, 0, 2.0) * self.dynamic_gain * np.cos(hull_angle)
        brace = 1.0 + min(knottedness * 0.5, 5.0)
        tension = 1.0 + (abs(hull_angle) * 5.0) if hull_angle < 0 else 1.0
        return (lean + run) * brace, tension

# ============================================================
# 2. MOSAIC AGENT (The Splicer)
# ============================================================
class MosaicAgent:
    def __init__(self, env_name, mosaic_strip, slice_size=50):
        self.mosaic_strip = mosaic_strip
        self.slice_size = slice_size
        self.fade = 10 
        
        dummy = gym.make(env_name)
        self.hypernet = KinestheticHypernet(8) 
        dummy.close()
        self.oscillator = HildebrandOscillator()
        self.ballast = ReflexiveBallast()
        self.history = deque(maxlen=5)

    def get_active_gene(self, t_step):
        frame_idx = min(t_step // self.slice_size, len(self.mosaic_strip) - 1)
        current_gene = self.mosaic_strip[frame_idx]
        
        # Crossfade logic
        steps_into_frame = t_step % self.slice_size
        steps_left = self.slice_size - steps_into_frame
        
        if steps_left < self.fade and frame_idx < len(self.mosaic_strip) - 1:
            next_gene = self.mosaic_strip[frame_idx + 1]
            progress = (self.fade - steps_left) / self.fade
            return ((1 - progress) * current_gene) + (progress * next_gene)
        return current_gene

    def calculate_knottedness(self, m, lam):
        self.history.append(np.array([m, lam]))
        if len(self.history) < 3: return 0.0
        v = self.history[-1] - self.history[-2]
        a = v - (self.history[-2] - self.history[-3])
        cross = abs(v[0]*a[1] - v[1]*a[0])
        curve = cross / (np.linalg.norm(v)**3 + 1e-9)
        return min(abs(self.hypernet.get_potential_energy(m, lam)) * curve, 10.0)

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
# 3. CRYSTAL TRAINER (The Broken Pixel Logic)
# ============================================================
class CrystalTrainer:
    def __init__(self, env_name):
        self.env_name = env_name
        self.total_steps = 800
        self.slice_size = 50
        self.num_frames = self.total_steps // self.slice_size
        
        # The Archive: [Gene1, Gene2, ... Gene16]
        starter_gene = np.array([0.0, 0.0, 0.8, 0.8, 0.5, 1.5, 0.0])
        self.archive = [starter_gene.copy() for _ in range(self.num_frames)]
        
        # The Crystal Mask: True = "Broken/Locked", False = "Fluid"
        self.crystal_mask = [False] * self.num_frames
        
        # Performance Thresholds
        self.lock_threshold = 1.2 # Meters per 50 steps (approx 1.2m/s speed)
        
    def evaluate(self, mosaic_strip, render=False):
        agent = MosaicAgent(self.env_name, mosaic_strip, self.slice_size)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        segment_start_x = start_x
        
        segment_deltas = [] # How much distance gained in each slice?
        total_knot = 0
        steps = 0
        
        # Run loop
        while steps < self.total_steps:
            action, k_val, _ = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            total_knot += k_val
            
            # Check Segment Boundary
            if (steps + 1) % self.slice_size == 0:
                curr_x = env.unwrapped.hull.position.x
                delta = curr_x - segment_start_x
                segment_deltas.append(delta)
                segment_start_x = curr_x
            
            steps += 1
            if term or trunc: break
            
        # Fill remaining segments with 0.0 if we crashed early
        while len(segment_deltas) < self.num_frames:
            segment_deltas.append(0.0)
            
        final_dist = env.unwrapped.hull.position.x - start_x
        env.close()
        
        return final_dist, segment_deltas, total_knot

    def run(self):
        print("💎 FRACTAL CRYSTALLIZATION PROTOCOL")
        print(f"   Locking pixels that achieve > {self.lock_threshold}m per segment.")
        
        for g in range(40):
            # 1. Visualize the Crystal
            # ■ = Locked (Broken Pixel), □ = Fluid
            visual_map = ""
            locked_count = 0
            for is_locked in self.crystal_mask:
                if is_locked: 
                    visual_map += "■"
                    locked_count += 1
                else: 
                    visual_map += "□"
            
            print(f"\n--- Gen {g} [{visual_map}] ({locked_count}/{self.num_frames} Locked) ---")
            
            if locked_count == self.num_frames:
                print("   > CRYSTAL COMPLETE. FULLY OPTIMIZED.")
                break

            # 2. Create Population
            # We only mutate the □ (Fluid) frames.
            population = []
            
            # Control (The current Archive)
            population.append(self.archive) 
            
            for _ in range(12):
                candidate = [gene.copy() for gene in self.archive]
                
                # Mutate only Fluid frames
                for i in range(self.num_frames):
                    if not self.crystal_mask[i]:
                        # "Zoom In": High mutation because we need to fix this
                        mutation = np.random.normal(0, 0.2, 7)
                        candidate[i] += mutation
                
                population.append(candidate)

            # 3. Evaluate & Crystallize
            best_dist = -999
            best_strip = None
            best_deltas = []
            
            for strip in population:
                dist, deltas, _ = self.evaluate(strip)
                
                # Hybrid Fitness: Total Distance is king, but...
                if dist > best_dist:
                    best_dist = dist
                    best_strip = strip
                    best_deltas = deltas

            print(f"   ★ Run Distance: {best_dist:.1f}m")
            
            # 4. UPDATE ARCHIVE & LOCK PIXELS
            # We accept the best strip (Natural Selection)
            self.archive = [g.copy() for g in best_strip]
            
            # We check the Deltas of the Winner to see if any NEW pixels solidified
            new_locks = 0
            for i in range(self.num_frames):
                # If unlocked AND performance is good...
                if not self.crystal_mask[i] and best_deltas[i] > self.lock_threshold:
                    self.crystal_mask[i] = True # BREAK THE PIXEL (Lock it)
                    new_locks += 1
            
            if new_locks > 0:
                print(f"   > Crystallized {new_locks} new segments!")

        return self.archive

if __name__ == "__main__":
    trainer = CrystalTrainer("BipedalWalker-v3")
    final_crystal = trainer.run()
    
    print("\nVisualizing the Crystal...")
    trainer.evaluate(final_crystal, render=True)