import gymnasium as gym
import numpy as np
import logging
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("FRACTAL_RHYTHM")

# ============================================================
# 1. THE FRACTAL CORE (With Unsolvable Detection)
# ============================================================
class FractalCore:
    def __init__(self, horizon=40, particles=64):
        self.horizon = horizon 
        self.n_particles = particles
        
    def hunt_loops(self, m_start, l_start, sigma):
        # 1. CLAMP (Initial Safety)
        m_start = np.clip(m_start, -2.0, 2.0)
        l_start = np.clip(l_start, -2.0, 2.0)
        
        # 2. Particle Cloud
        noise = np.random.normal(0, 0.15, (self.n_particles, 2))
        curr_m = np.full(self.n_particles, m_start) + noise[:, 0]
        curr_l = np.full(self.n_particles, l_start) + noise[:, 1]
        
        trajectories = np.zeros((self.horizon, self.n_particles, 2))
        dt = 0.2
        
        # 3. Physics Evolution
        for t in range(self.horizon):
            trajectories[t, :, 0] = curr_m
            trajectories[t, :, 1] = curr_l
            
            # Wada Force
            # We catch overflows here to detect "The Unsolvable"
            try:
                term1 = 2 * sigma * curr_m * curr_l
                term2 = sigma * (curr_m**2 - curr_l**2)
                fm = -(curr_m + term1)
                fl = -(curr_l + term2)
                
                curr_m += dt * fm
                curr_l += dt * fl
                
                # Check for "The Unsolvable" (Explosion)
                if np.any(np.abs(curr_m) > 10.0) or np.any(np.isnan(curr_m)):
                    return None, "UNSOLVABLE"
                    
            except RuntimeWarning:
                return None, "UNSOLVABLE"

        # 4. Loop Detection
        start = trajectories[0]
        errors = np.zeros((self.horizon, self.n_particles))
        
        for t in range(4, self.horizon): # Minimum loop size 4
            d = np.linalg.norm(trajectories[t] - start, axis=1)
            errors[t] = d
            
        # Find best loop
        valid_errors = errors[4:, :]
        min_err_idx = np.unravel_index(np.argmin(valid_errors), valid_errors.shape)
        
        best_t = min_err_idx[0] + 4 
        best_p = min_err_idx[1]
        
        best_error = valid_errors[min_err_idx]
        
        if best_error > 0.5: # No good loop found
            return None, "CHAOS"
            
        loop_traj = trajectories[:best_t, best_p, :]
        return loop_traj, "STABLE"

# ============================================================
# 2. THE THOUGHT SEQUENCER (Rhythm & Regime)
# ============================================================
class RhythmAgent:
    def __init__(self, env_name, gene):
        self.gene = gene # [Bias_M, Bias_L, Sigma_Base, Aggression]
        dummy = gym.make(env_name)
        self.core = FractalCore(horizon=40, particles=80)
        dummy.close()
        
        # Mental State
        self.current_m = 0.1
        self.current_l = 0.1
        self.active_loop = None
        self.loop_phase = 0
        self.regime_sigma = gene[2] # Current Physics Regime
        self.unsolvable_counter = 0

    def get_action_data(self, obs):
        bias_m, bias_l, _, aggression = self.gene
        
        # 1. SEQUENCER CHECK
        # Do we need a new thought?
        # Yes if: No active loop OR Loop finished OR We hit Unsolvable recently
        need_new_thought = (self.active_loop is None) or \
                           (self.loop_phase >= len(self.active_loop))
                           
        if need_new_thought:
            # Seed the hunt with current Hull Angle (Context)
            hull_angle = obs[0]
            search_m = self.current_m + bias_m + (hull_angle * 0.5)
            search_l = self.current_l + bias_l
            
            # HUNT
            loop, status = self.core.hunt_loops(search_m, search_l, self.regime_sigma)
            
            if status == "STABLE":
                self.active_loop = loop
                self.loop_phase = 0
                self.unsolvable_counter = max(0, self.unsolvable_counter - 1)
                # logger.info(f"Found Loop (Len {len(loop)})")
                
            elif status == "CHAOS":
                # Mild failure: drift slightly and try again next step
                self.current_m += np.random.normal(0, 0.1)
                self.current_l += np.random.normal(0, 0.1)
                self.active_loop = None # Stumble for a frame
                
            elif status == "UNSOLVABLE":
                # CATASTROPHIC FAILURE -> REGIME SHIFT
                self.unsolvable_counter += 1
                
                # Push the agent into a new regime (Change Sigma)
                # If we were at 1.0, maybe 0.5 works? Or 1.5?
                shift = np.random.choice([-0.5, 0.5, 0.2, -0.2])
                self.regime_sigma = np.clip(self.regime_sigma + shift, 0.5, 2.0)
                
                # Teleport internal state to random safe spot
                self.current_m = np.random.uniform(-1, 1)
                self.current_l = np.random.uniform(-1, 1)
                
                # logger.info(f"💥 UNSOLVABLE! Regime Shift -> Sigma {self.regime_sigma:.2f}")
                self.active_loop = None

        # 2. EXECUTION (The Rhythm)
        actions = np.zeros(4)
        
        if self.active_loop is not None:
            # Surf the loop
            target = self.active_loop[self.loop_phase]
            
            # Smoothly interpolate
            self.current_m += (target[0] - self.current_m) * 0.5
            self.current_l += (target[1] - self.current_l) * 0.5
            
            self.loop_phase += 1
            
            # Map to motors
            drive_m = np.tanh(self.current_m * aggression)
            drive_l = np.tanh(self.current_l * aggression)
            
            # Symmetry mapping
            actions[0] = drive_m   # R Hip
            actions[1] = drive_l   # R Knee
            actions[2] = -drive_m  # L Hip
            actions[3] = -drive_l  # L Knee
            
        else:
            # STUMBLE MODE (No valid thought)
            # Apply "Recovery Reflex" (Stiff knees, slight hip correction)
            actions[1] = 0.5 # Knee extension
            actions[3] = 0.5
            actions[0] = -obs[0] # Simple balance
            actions[2] = -obs[0]

        return actions, self.regime_sigma

# ============================================================
# 3. TRAINER
# ============================================================
class RhythmTrainer:
    def evaluate(self, gene, render=False):
        try:
            agent = RhythmAgent("BipedalWalker-v3", gene)
            env = gym.make("BipedalWalker-v3", render_mode="human" if render else None)
            obs, _ = env.reset()
            
            start_x = env.unwrapped.hull.position.x
            regime_shifts = 0
            start_sigma = agent.regime_sigma
            
            for _ in range(800):
                action, current_sigma = agent.get_action_data(obs)
                obs, _, term, trunc, _ = env.step(action)
                
                if current_sigma != start_sigma:
                    regime_shifts += 1
                    start_sigma = current_sigma
                    
                if term or trunc: break
                
            dist = env.unwrapped.hull.position.x - start_x
            env.close()
            
            # Fitness: Distance + Bonus for surviving Regime Shifts
            return dist + (regime_shifts * 2.0), dist
            
        except Exception:
            return -100.0, 0.0

    def run(self):
        print("🥁 FRACTAL RHYTHM: The Thought Sequencer")
        # Gene: [Bias_M, Bias_L, Sigma_Base, Aggression]
        pop = [np.array([0.0, 0.0, 1.0, 2.0]) + np.random.normal(0, 0.2, 4) for _ in range(20)]
        best_gene = pop[0]
        best_dist = -999
        
        for g in range(20):
            scores = []
            for i, gene in enumerate(pop):
                fit, dist = self.evaluate(gene)
                scores.append(fit)
                if dist > best_dist:
                    best_dist = dist
                    best_gene = gene.copy()
                    print(f"   Gen {g} Record: {dist:.1f}m")
            
            # Mutate
            pop = [best_gene + np.random.normal(0, 0.1, 4) for _ in range(20)]
            
        return best_gene

if __name__ == "__main__":
    trainer = RhythmTrainer()
    best = trainer.run()
    trainer.evaluate(best, render=True)