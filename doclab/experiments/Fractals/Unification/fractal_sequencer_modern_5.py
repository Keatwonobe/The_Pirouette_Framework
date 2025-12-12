import gymnasium as gym
import numpy as np
import logging
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("FRACTAL_GIMBAL")

# ============================================================
# 1. THE FRACTAL GIMBAL (The Loop Hunter)
# ============================================================
class FractalGimbal:
    def __init__(self, horizon=20, particles=64):
        self.horizon = horizon 
        self.n_particles = particles
        
    def hunt_loops(self, m_start, l_start, sigma_offset):
        # 1. SAFETY CLAMP (Prevent hunting in deep chaos)
        m_start = np.clip(m_start, -2.0, 2.0)
        l_start = np.clip(l_start, -2.0, 2.0)
        
        # 2. Generate Cloud
        noise = np.random.normal(0, 0.1, (self.n_particles, 2))
        curr_m = np.full(self.n_particles, m_start) + noise[:, 0]
        curr_l = np.full(self.n_particles, l_start) + noise[:, 1]
        
        trajectories = np.zeros((self.horizon, self.n_particles, 2))
        
        sigma = 1.0 + sigma_offset 
        dt = 0.2
        
        # 3. Evolve Physics (With Explosion Guards)
        for t in range(self.horizon):
            trajectories[t, :, 0] = curr_m
            trajectories[t, :, 1] = curr_l
            
            # Wada Force
            # We use 'np.clip' inside the math to prevent overflow before it happens
            term1 = 2 * sigma * curr_m * curr_l
            term2 = sigma * (curr_m**2 - curr_l**2)
            
            fm = -(curr_m + np.clip(term1, -10, 10))
            fl = -(curr_l + np.clip(term2, -10, 10))
            
            curr_m += dt * fm
            curr_l += dt * fl
            
            # Hard Containment
            # If a particle escapes, we reset it to origin to kill the loop score
            escaped = (curr_m**2 + curr_l**2) > 9.0
            curr_m[escaped] = 0.0
            curr_l[escaped] = 0.0
            
            # NaN Check (The Box2D Saver)
            if np.any(np.isnan(curr_m)):
                curr_m = np.nan_to_num(curr_m)
                curr_l = np.nan_to_num(curr_l)

        # 4. Detect Loops
        start = trajectories[0]
        errors = np.zeros((self.horizon, self.n_particles))
        
        for t in range(1, self.horizon):
            d = np.linalg.norm(trajectories[t] - start, axis=1)
            errors[t] = d
            
        # Ignore first 4 steps (too short)
        valid_errors = errors[4:, :] 
        min_err_idx = np.unravel_index(np.argmin(valid_errors), valid_errors.shape)
        
        best_t = min_err_idx[0] + 4 
        best_p = min_err_idx[1]     
        
        loop_traj = trajectories[:best_t, best_p, :]
        quality = 1.0 / (valid_errors[min_err_idx] + 1e-3)
        
        return loop_traj, quality

# ============================================================
# 2. THE GIMBAL AGENT
# ============================================================
class GimbalAgent:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.gimbal = FractalGimbal(horizon=30, particles=50)
        dummy.close()
        
        self.current_m = 0.1
        self.current_l = 0.1
        self.target_loop = None
        self.loop_index = 0
        self.steps_on_loop = 0

    def get_action_data(self, obs):
        bias_m, bias_l, sigma_bias, speed_mult = self.gene
        
        # HUNT if needed
        if self.target_loop is None or self.steps_on_loop >= len(self.target_loop):
            hull_angle = obs[0] 
            # Clamp search start so we don't start the hunt in invalid space
            search_m = np.clip(self.current_m + bias_m + (hull_angle * 0.5), -2, 2)
            search_l = np.clip(self.current_l + bias_l, -2, 2)
            
            loop, quality = self.gimbal.hunt_loops(search_m, search_l, sigma_bias)
            
            self.target_loop = loop
            self.loop_index = 0
            self.steps_on_loop = 0

        # SURF
        target_state = self.target_loop[self.loop_index]
        
        # Lerp to target
        self.current_m += (target_state[0] - self.current_m) * 0.3 * speed_mult
        self.current_l += (target_state[1] - self.current_l) * 0.3 * speed_mult
        
        self.loop_index = (self.loop_index + 1) % len(self.target_loop)
        self.steps_on_loop += 1
        
        # MAP
        m_drive = np.tanh(self.current_m)
        l_drive = np.tanh(self.current_l)
        
        actions = np.zeros(4)
        actions[0] = m_drive       # Hip R
        actions[1] = l_drive       # Knee R
        actions[2] = -m_drive      # Hip L
        actions[3] = -l_drive      # Knee L
        
        # SAFETY FINALIZER: Ensure no NaNs ever reach Box2D
        actions = np.nan_to_num(actions, nan=0.0, posinf=1.0, neginf=-1.0)
        actions = np.clip(actions, -1.0, 1.0)
            
        return actions, len(self.target_loop)

# ============================================================
# 3. EVOLUTIONARY TRAINER
# ============================================================
class GimbalTrainer:
    def __init__(self, env_name):
        self.env_name = env_name
        
    def evaluate(self, gene, render=False):
        try:
            agent = GimbalAgent(self.env_name, gene)
            env = gym.make(self.env_name, render_mode="human" if render else None)
            obs, _ = env.reset()
            
            start_x = env.unwrapped.hull.position.x
            total_loops = 0
            steps = 0
            
            while steps < 800:
                action, loop_len = agent.get_action_data(obs)
                obs, reward, term, trunc, _ = env.step(action)
                
                if steps % loop_len == 0: total_loops += 1
                steps += 1
                if term or trunc: break
                
            dist = env.unwrapped.hull.position.x - start_x
            env.close()
            return dist + (total_loops * 0.5), dist
            
        except Exception as e:
            # If a run crashes, punish the gene heavily but don't stop the script
            # logger.error(f"Run Failed: {e}")
            try: env.close()
            except: pass
            return -100.0, 0.0

    def run(self):
        print("🌀 FRACTAL GIMBAL v2: Stabilized Loop Hunting")
        
        pop = [np.random.normal(0, 0.5, 4) for _ in range(20)]
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
                    print(f"   Gen {g} NEW RECORD: {dist:.1f}m")
            
            pop = [best_gene + np.random.normal(0, 0.1, 4) for _ in range(20)]
            
        return best_gene

if __name__ == "__main__":
    trainer = GimbalTrainer("BipedalWalker-v3")
    best = trainer.run()
    print("\n[-] Visualizing The Stabilized Gimbal...")
    trainer.evaluate(best, render=True)