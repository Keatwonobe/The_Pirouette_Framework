import gymnasium as gym
import numpy as np
from collections import deque
import math

# ============================================================
# 1. THE FRACTAL CANVAS (The Memory Bank)
# ============================================================
class FractalCanvas:
    def __init__(self, resolution=64):
        self.res = resolution
        self.bounds = 2.5 # Range [-2.5, 2.5] for m and lambda
        
        # The Grid stores: [Locked(bool), Weights(vec), Score(float)]
        # We use a dictionary for sparse storage to save memory/lookup time
        self.grid = {} 
        
        # Statistics
        self.locked_count = 0

    def _coords_to_key(self, m, lam):
        # Quantize continuous float space into discrete pixel coordinates
        # Map [-2.5, 2.5] -> [0, res]
        x = int(((m + self.bounds) / (2 * self.bounds)) * self.res)
        y = int(((lam + self.bounds) / (2 * self.bounds)) * self.res)
        # Clamp to avoid array errors
        x = max(0, min(self.res - 1, x))
        y = max(0, min(self.res - 1, y))
        return (x, y)

    def query(self, m, lam):
        """
        Returns: (Weights, Is_Locked)
        """
        key = self._coords_to_key(m, lam)
        if key in self.grid:
            cell = self.grid[key]
            if cell['locked']:
                return cell['weights'], True
        return None, False

    def update_pixel(self, m, lam, weights, velocity):
        """
        If this velocity is better than what we have seen at this pixel, save it.
        If it's VERY good, Lock it.
        """
        key = self._coords_to_key(m, lam)
        
        # Criteria for a "Gold Pixel"
        # 1.2 m/s is a solid jogging pace for BipedalWalker
        is_worthy = (velocity > 1.2)
        
        if key not in self.grid:
            self.grid[key] = {'locked': is_worthy, 'weights': weights, 'score': velocity}
            if is_worthy: self.locked_count += 1
        else:
            # Overwrite only if better
            if velocity > self.grid[key]['score']:
                was_locked = self.grid[key]['locked']
                self.grid[key] = {'locked': is_worthy, 'weights': weights, 'score': velocity}
                if is_worthy and not was_locked:
                    self.locked_count += 1

# ============================================================
# 2. PHYSICS ENGINE (v24 Standard)
# ============================================================
class KinestheticHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
    def get_potential_energy(self, x, y):
        return 0.5 * (x**2 + y**2) + (x**2 * y - (1.0/3.0) * y**3)
    def generate_weights_raw(self, m, lam):
        # Standard generation without checking canvas
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
# 3. CANVAS AGENT (The Painter)
# ============================================================
class CanvasAgent:
    def __init__(self, env_name, gene, canvas):
        self.gene = gene
        self.canvas = canvas
        
        dummy = gym.make(env_name)
        self.hypernet = KinestheticHypernet(8) 
        dummy.close()
        self.oscillator = HildebrandOscillator()
        self.ballast = ReflexiveBallast()
        self.history = deque(maxlen=5)
        
        # Telemetry for updating the Canvas later
        # List of (m, lam, weights, velocity_at_t)
        self.trace_log = [] 

    def calculate_knottedness(self, m, lam):
        self.history.append(np.array([m, lam]))
        if len(self.history) < 3: return 0.0
        v = self.history[-1] - self.history[-2]
        a = v - (self.history[-2] - self.history[-3])
        cross = abs(v[0]*a[1] - v[1]*a[0])
        curve = cross / (np.linalg.norm(v)**3 + 1e-9)
        return min(abs(self.hypernet.get_potential_energy(m, lam)) * curve, 10.0)

    def get_action_data(self, obs, t_step):
        cm, cl, rm, rl, tilt, freq, phase = self.gene
        
        # 1. Orbit Position
        angle = phase + (t_step * 0.02 * freq * 2 * np.pi)
        m = cm + (rm * np.cos(angle) * np.cos(tilt) - rl * np.sin(angle) * np.sin(tilt))
        lam = cl + (rm * np.cos(angle) * np.sin(tilt) + rl * np.sin(angle) * np.cos(tilt))
        
        # 2. QUERY THE CANVAS
        weights, is_locked = self.canvas.query(m, lam)
        
        if weights is None:
            # UNLOCKED PIXEL: Generate fresh + Add Mutation (The Zoom)
            base_weights, color = self.hypernet.generate_weights_raw(m, lam)
            # Add significant noise to explore this unknown region
            mutation = np.random.normal(0, 0.3, size=base_weights.shape)
            weights = base_weights + mutation
            status_color = color # Standard basin color
        else:
            # LOCKED PIXEL: Use exact weights
            # We assign a special color to denote "Memory Read"
            status_color = "Crystal" 
            
        # Log this moment for potential crystallization
        # We store obs[2] (Hull Velocity) as the score metric
        self.trace_log.append({
            'm': m, 'lam': lam, 
            'weights': weights, 
            'vel': obs[2]
        })
        
        # 3. Standard Physics
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
# 4. CANVAS TRAINER
# ============================================================
class CanvasTrainer:
    def __init__(self, env_name):
        self.env_name = env_name
        self.canvas = FractalCanvas(resolution=64)
        
    def evaluate(self, gene, render=False):
        agent = CanvasAgent(self.env_name, gene, self.canvas)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        start_x = env.unwrapped.hull.position.x
        total_knot = 0
        steps = 0
        crystal_reads = 0
        
        while steps < 800:
            action, k_val, color = agent.get_action_data(obs, steps)
            obs, _, term, trunc, _ = env.step(action)
            total_knot += k_val
            
            if color == "Crystal":
                crystal_reads += 1
            
            steps += 1
            if term or trunc: break
            
        dist = env.unwrapped.hull.position.x - start_x
        env.close()
        
        # POST-RUN ANALYSIS: Update the Canvas
        # We "Develop" the film.
        if dist > 1.0: # Only learn from decent runs
            for frame in agent.trace_log:
                self.canvas.update_pixel(frame['m'], frame['lam'], frame['weights'], frame['vel'])
        
        return dist, crystal_reads

    def run(self):
        print("🎨 FRACTAL CANVAS v28")
        print("   Logic: Lock good pixels. Mutate the void.")
        
        # Initial Gene (Orbit parameters)
        # We don't need to mutate this much, the complexity is in the Weights now.
        best_gene = np.array([0.0, 0.0, 0.8, 0.8, 0.5, 1.5, 0.0])
        
        for g in range(50):
            print(f"\n--- Gen {g} ---")
            
            # 1. Run a batch of "Probes"
            # These agents have slightly different orbits to paint different parts of the canvas
            batch_best_dist = 0
            total_reads = 0
            
            for i in range(10):
                # Probe gene: Mutate orbit slightly to explore map
                probe = best_gene + np.random.normal(0, 0.1, 7)
                
                dist, reads = self.evaluate(probe)
                total_reads += reads
                
                if dist > batch_best_dist:
                    batch_best_dist = dist
                    best_gene = probe.copy() # Move the "Camera" to the interesting spot
            
            # 2. Visualize the Canvas State
            # Simple ASCII progress bar of filled pixels
            fill_pct = (len(self.canvas.grid) / (64*64)) * 100
            gold_pct = (self.canvas.locked_count / (64*64)) * 100
            
            print(f"   ★ Best Dist: {batch_best_dist:.1f}m")
            print(f"   Canvas: [Known: {fill_pct:.1f}%] [LOCKED: {gold_pct:.2f}%]")
            print(f"   Crystal Usage: {total_reads} frames read from cache.")
            
            if batch_best_dist > 150.0: # Arbitrary win
                print("   > MASTERPIECE COMPLETE.")
                break

        return best_gene

if __name__ == "__main__":
    trainer = CanvasTrainer("BipedalWalker-v3")
    best_gene = trainer.run()
    
    print("\nVisualizing the Fractal Surface...")
    trainer.evaluate(best_gene, render=True)