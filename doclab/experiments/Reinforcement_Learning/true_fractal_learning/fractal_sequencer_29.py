import gymnasium as gym
import numpy as np
from collections import deque
import math

# ============================================================
# 1. THE FRACTAL CANVAS (Spatial Memory)
# ============================================================
class FractalCanvas:
    def __init__(self, resolution=64):
        self.res = resolution
        self.bounds = 2.5 # Range [-2.5, 2.5]
        # Stores: { (x,y): {'locked': bool, 'weights': vector, 'score': float} }
        self.grid = {} 
        self.locked_count = 0

    def _coords_to_key(self, m, lam):
        x = int(((m + self.bounds) / (2 * self.bounds)) * self.res)
        y = int(((lam + self.bounds) / (2 * self.bounds)) * self.res)
        x = max(0, min(self.res - 1, x))
        y = max(0, min(self.res - 1, y))
        return (x, y)

    def query(self, m, lam):
        key = self._coords_to_key(m, lam)
        if key in self.grid:
            cell = self.grid[key]
            if cell['locked']:
                return cell['weights'], True
        return None, False

    def update_pixel(self, m, lam, weights, velocity):
        key = self._coords_to_key(m, lam)
        # 1.2 m/s is the "Gold Standard" for efficient movement
        is_worthy = (velocity > 1.2)
        
        if key not in self.grid:
            self.grid[key] = {'locked': is_worthy, 'weights': weights, 'score': velocity}
            if is_worthy: self.locked_count += 1
        else:
            # Only update if this new move is FASTER than the old memory
            if velocity > self.grid[key]['score']:
                was_locked = self.grid[key]['locked']
                self.grid[key] = {'locked': is_worthy, 'weights': weights, 'score': velocity}
                if is_worthy and not was_locked:
                    self.locked_count += 1

# ============================================================
# 2. PHYSICS ENGINE (v24 Ratchet)
# ============================================================
class KinestheticHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
    
    def get_potential_energy(self, x, y):
        return 0.5 * (x**2 + y**2) + (x**2 * y - (1.0/3.0) * y**3)

    def generate_weights_raw(self, m, lam):
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
# 3. HOLODECK AGENT (Mosaic + Canvas)
# ============================================================
class HolodeckAgent:
    def __init__(self, env_name, mosaic_strip, canvas, slice_size=50):
        self.mosaic_strip = mosaic_strip
        self.canvas = canvas
        self.slice_size = slice_size
        self.fade = 10 
        
        dummy = gym.make(env_name)
        self.hypernet = KinestheticHypernet(8) 
        dummy.close()
        
        self.oscillator = HildebrandOscillator()
        self.ballast = ReflexiveBallast()
        self.history = deque(maxlen=5)
        
        # Trace Log for learning: (m, lam, weights, velocity)
        self.trace = []

    def get_active_gene(self, t_step):
        # MOSAIC LOGIC: Temporal Splicing
        frame_idx = min(t_step // self.slice_size, len(self.mosaic_strip) - 1)
        current_gene = self.mosaic_strip[frame_idx]
        
        steps_into_frame = t_step % self.slice_size
        steps_left = self.slice_size - steps_into_frame
        
        if steps_left < self.fade and frame_idx < len(self.mosaic_strip) - 1:
            next_gene = self.mosaic_strip[frame_idx + 1]
            prog = (self.fade - steps_left) / self.fade
            return ((1 - prog) * current_gene) + (prog * next_gene)
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
        # 1. Get Trajectory from Mosaic
        gene = self.get_active_gene(t_step)
        cm, cl, rm, rl, tilt, freq, phase = gene
        
        angle = phase + (t_step * 0.02 * freq * 2 * np.pi)
        m = cm + (rm * np.cos(angle) * np.cos(tilt) - rl * np.sin(angle) * np.sin(tilt))
        lam = cl + (rm * np.cos(angle) * np.sin(tilt) + rl * np.sin(angle) * np.cos(tilt))
        
        # 2. Get Reaction from Canvas
        weights, is_locked = self.canvas.query(m, lam)
        
        if weights is None:
            # Unmapped territory: Improvise + Mutate
            base_w, color = self.hypernet.generate_weights_raw(m, lam)
            mutation = np.random.normal(0, 0.2, size=base_w.shape)
            weights = base_w + mutation
            status_color = color
        else:
            # Memory Recall: Use Locked Weights
            status_color = "Crystal" 
            
        # Log for updates
        self.trace.append({'m': m, 'lam': lam, 'weights': weights, 'vel': obs[2]})
        
        # 3. Physics & Control
        k_val = self.calculate_knottedness(m, lam)
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
        
        return np.tanh(actions), k_val, status_color

# ============================================================
# 4. HOLODECK TRAINER
# ============================================================
class HolodeckTrainer:
    def __init__(self, env_name):
        self.env_name = env_name
        self.total_steps = 800
        self.slice_size = 50
        self.num_frames = self.total_steps // self.slice_size
        self.breath_cycle = 4
        
        # 1. The Canvas (Shared Memory)
        self.canvas = FractalCanvas(resolution=64)
        
        # 2. The Archive (Mosaic Strip)
        starter_gene = np.array([0.0, 0.0, 0.8, 0.8, 0.5, 1.5, 0.0])
        self.archive = [starter_gene.copy() for _ in range(self.num_frames)]
        
        self.global_best_dist = 0.0

    def evaluate(self, mosaic_strip, phase, render=False):
        agent = HolodeckAgent(self.env_name, mosaic_strip, self.canvas, self.slice_size)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        total_knot = 0
        steps = 0
        crystal_reads = 0
        
        while steps < self.total_steps:
            action, k_val, color = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            total_knot += k_val
            if color == "Crystal": crystal_reads += 1
            steps += 1
            if term or trunc: break
        
        dist = env.unwrapped.hull.position.x - start_x
        env.close()
        
        # UPDATE CANVAS (If run was decent)
        # We assume if the run went > 2m, there were some good muscle movements in there.
        if dist > 2.0:
            for frame in agent.trace:
                self.canvas.update_pixel(frame['m'], frame['lam'], frame['weights'], frame['vel'])
        
        # Fitness Logic
        if phase == "INHALE":
            knot_bonus = math.log1p(total_knot) 
            fitness = dist * (1.0 + (knot_bonus * 0.1))
        else:
            fitness = dist 
            
        return fitness, dist, crystal_reads

    def run(self):
        print("🌌 HOLODECK PROTOCOL: Mosaic + Canvas")
        print("   Optimizing Time (Trajectory) AND Space (Muscle Memory).")
        
        for g in range(50):
            # Phase Logic
            if (g % self.breath_cycle) < 2:
                phase = "INHALE"; icon = "⚡"; mut_scale = 0.2
            else:
                phase = "EXHALE"; icon = "🛡️"; mut_scale = 0.05
            
            # Stats
            fill_pct = (len(self.canvas.grid) / (64*64)) * 100
            gold_pct = (self.canvas.locked_count / (64*64)) * 100
            print(f"\n--- Gen {g} [{icon} {phase}] Mem: {fill_pct:.1f}% (Locked: {gold_pct:.1f}%) ---")
            
            # Evolution Loop (Mosaic Logic)
            population = []
            population.append({'strip': [g.copy() for g in self.archive], 'mutations': []})
            
            for _ in range(12):
                strip = [g.copy() for g in self.archive]
                idx1 = np.random.randint(0, self.num_frames)
                strip[idx1] += np.random.normal(0, mut_scale, 7)
                
                idx2 = -1
                if phase == "INHALE" and np.random.rand() > 0.5:
                    idx2 = np.random.randint(0, self.num_frames)
                    strip[idx2] += np.random.normal(0, mut_scale, 7)
                    
                population.append({'strip': strip, 'mutations': [idx1, idx2]})

            best_fit = -999
            best_dist = 0
            best_strip = None
            best_reads = 0
            
            for candidate in population:
                fit, dist, reads = self.evaluate(candidate['strip'], phase)
                if fit > best_fit:
                    best_fit = fit
                    best_dist = dist
                    best_strip = candidate['strip']
                    best_reads = reads

            print(f"   ★ Best: {best_dist:.1f}m | Fit: {best_fit:.1f} | Reads: {best_reads}")
            
            # Archive Update
            if best_dist >= self.global_best_dist * 0.95:
                if best_dist > self.global_best_dist:
                    self.global_best_dist = best_dist
                    print(f"   🏆 NEW RECORD.")
                self.archive = [g.copy() for g in best_strip]

        return self.archive

if __name__ == "__main__":
    trainer = HolodeckTrainer("BipedalWalker-v3")
    final_strip = trainer.run()
    
    print("\nVisualizing the Holodeck...")
    trainer.evaluate(final_strip, "EXHALE", render=True)