import gymnasium as gym
import numpy as np
import time
from gymnasium.spaces import Discrete, Box

# ---------------------------------------------------------------------------
# 1. THE GENERATOR: Fractal -> Static Weights
# ---------------------------------------------------------------------------
class FractalHypernet:
    """
    Stabilized Generator: Prevents infinite divergence with Space Folding.
    """
    def __init__(self, output_dim):
        self.output_dim = output_dim

    def generate_weights(self, m, lam):
        weights = []
        
        # Physics Constants
        p_m, p_l = 0.0, 0.0
        sigma = 1.0
        dt = 0.1
        curr_m, curr_l = m, lam
        
        # SAFETY VALVE: If values exceed this, we fold space.
        # tanh(10) is already 1.0, so going higher adds no info, only risk.
        ESCAPE_THRESHOLD = 10.0 
        
        while len(weights) < self.output_dim:
            # 1. Divergence Check
            if abs(curr_m) > ESCAPE_THRESHOLD or abs(curr_l) > ESCAPE_THRESHOLD:
                # "Space Folding": Wrap the coordinate back to the origin
                # This keeps the chaos but removes the infinity.
                curr_m = np.fmod(curr_m, 2.0)
                curr_l = np.fmod(curr_l, 2.0)
                # Dampen momentum to prevent immediate re-escape
                p_m *= 0.1
                p_l *= 0.1
            
            # 2. Safe Calculation Step
            try:
                # Symplectic Euler 
                grad_m = curr_m + 2 * sigma * curr_m * curr_l
                grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
                
                p_m_half = p_m - (dt/2) * grad_m
                p_l_half = p_l - (dt/2) * grad_l
                
                curr_m += dt * p_m_half
                curr_l += dt * p_l_half
                
                grad_m_new = curr_m + 2 * sigma * curr_m * curr_l
                grad_l_new = curr_l + sigma * (curr_m**2 - curr_l**2)
                
                p_m = p_m_half - (dt/2) * grad_m_new
                p_l = p_l_half - (dt/2) * grad_l_new
                
                # 3. NaN Guard (The Box2D Fix)
                if np.isnan(curr_m) or np.isnan(curr_l):
                    curr_m, curr_l = 0.0, 0.0 # Hard reset
                    
            except RuntimeWarning:
                # If an overflow happens during calculation, catch it
                curr_m, curr_l = 0.0, 0.0

            # 4. Map to Weight (Safe)
            # We use tanh to guarantee weights are in [-1, 1]
            weights.append(np.tanh(curr_m))
            weights.append(np.tanh(curr_l))
            
        return np.array(weights[:self.output_dim], dtype=np.float32)

# ---------------------------------------------------------------------------
# 2. THE AGENT: Static Reader (Adapted from your upload)
# ---------------------------------------------------------------------------
class StaticReader:
    def __init__(self, input_dim, output_dim, discrete=False):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.discrete = discrete
        self.W_size = input_dim * output_dim

    def act(self, W_flat, obs):
        # 1. Reshape the flat fractal weights into a matrix
        W = W_flat.reshape(self.output_dim, self.input_dim)
        
        # 2. Linear Pass
        # Simple policy: Action = W * Obs
        action = W @ obs
        
        # 3. Output Processing
        if self.discrete:
            return np.argmax(action)
        else:
            return np.tanh(action) # Continuous (Walker/Lander)

# ---------------------------------------------------------------------------
# 3. THE FILTER: Fail Fast & Zoom
# ---------------------------------------------------------------------------
class FractalFilterTrainer:
    def __init__(self, env_id):
        self.env_id = env_id
        self.env = gym.make(env_id)
        
        # Determine Dimensions
        self.obs_dim = self.env.observation_space.shape[0]
        if isinstance(self.env.action_space, Discrete):
            self.act_dim = self.env.action_space.n
            self.is_discrete = True
        else:
            self.act_dim = self.env.action_space.shape[0]
            self.is_discrete = False
            
        self.weight_count = self.obs_dim * self.act_dim
        self.hypernet = FractalHypernet(self.weight_count)
        self.agent = StaticReader(self.obs_dim, self.act_dim, self.is_discrete)
        
    def get_safety_status(self, obs, terminated, truncated):
        """
        The 'Fail Fast' Logic. Returns (is_safe, failure_penalty)
        """
        if 'BipedalWalker' in self.env_id:
            hull_angle = obs[0]
            # IF hull tilts too much (> 0.5 rad), it's a fail.
            if abs(hull_angle) > 0.8: return False, -10.0
            # IF body drops too low (y < 0.2), it's a fail.
            # (Assuming standard walker normalization)
            
        elif 'LunarLander' in self.env_id:
            # If tilting too much or falling too fast
            angle = obs[4]
            if abs(angle) > 1.0: return False, -10.0
            
        if terminated and not truncated: # Crashed/Fell
            return False, -100.0
            
        return True, 0.0

    def evaluate_coordinate(self, m, lam, fast_check=True):
        """
        1. Generate Weights from (m, λ).
        2. Run Simulation.
        3. Fail Fast if unstable.
        """
        # Generate the Static "Frame"
        weights = self.hypernet.generate_weights(m, lam)
        
        obs, _ = self.env.reset()
        total_reward = 0
        steps = 0
        
        # Fast Check limit (e.g., first 50 frames)
        limit = 60 if fast_check else 1000
        
        while steps < limit:
            action = self.agent.act(weights, obs)
            obs, reward, terminated, truncated, _ = self.env.step(action)
            
            total_reward += reward
            steps += 1
            
            # --- THE FILTER ---
            is_safe, penalty = self.get_safety_status(obs, terminated, truncated)
            if not is_safe:
                total_reward += penalty # Apply penalty
                break # FAIL FAST: Stop processing this frame immediately
            
            if terminated or truncated:
                break
                
        return total_reward

    def run_filter_sweep(self):
        print(f"🌊 FRACTAL FILTER ACTIVE: {self.env_id}")
        print(f"   Mapping 2D Chaos -> {self.weight_count}D Weight Matrix")
        
        # --- PHASE 1: COARSE SCAN (The Wide Lens) ---
        print("\n[Phase 1] Scanning Basin for Stable Frames...")
        m_vals = np.linspace(-1.5, 1.5, 20)
        l_vals = np.linspace(-1.5, 1.5, 20)
        
        candidates = []
        
        for m in m_vals:
            for lam in l_vals:
                # Run FAST check (only 60 steps)
                score = self.evaluate_coordinate(m, lam, fast_check=True)
                
                # If it survived the "Fail Fast" filter with decent score
                if score > -50: # Threshold depends on env
                    candidates.append((score, m, lam))
        
        # Sort by score
        candidates.sort(reverse=True, key=lambda x: x[0])
        top_candidates = candidates[:5]
        
        print(f"   Found {len(candidates)} survivors. Top seed: {top_candidates[0]}")
        
        # --- PHASE 2: ZOOM & VERIFY (The Microscope) ---
        print("\n[Phase 2] Zooming in on Stability Spikes...")
        
        best_overall = (-9999, 0, 0)
        
        for i, (score, seed_m, seed_l) in enumerate(top_candidates):
            print(f"   > Refining Seed {i+1}: ({seed_m:.2f}, {seed_l:.2f})")
            
            # Local grid around the seed
            radius = 0.1
            m_fine = np.linspace(seed_m - radius, seed_m + radius, 10)
            l_fine = np.linspace(seed_l - radius, seed_l + radius, 10)
            
            for mf in m_fine:
                for lf in l_fine:
                    # Run FULL check (max steps)
                    final_score = self.evaluate_coordinate(mf, lf, fast_check=False)
                    
                    if final_score > best_overall[0]:
                        best_overall = (final_score, mf, lf)
                        print(f"     Found New Best: {final_score:.1f} at ({mf:.3f}, {lf:.3f})")
                        
        print("\n" + "="*60)
        print(f"🏆 BEST FRAME FOUND: m={best_overall[1]:.4f}, λ={best_overall[2]:.4f}")
        print(f"   Score: {best_overall[0]:.1f}")
        print("="*60)
        
        return best_overall[1], best_overall[2]

    def visualize(self, m, lam):
        print("\n🎥 Visualizing the Frame...")
        env = gym.make(self.env_id, render_mode="human")
        weights = self.hypernet.generate_weights(m, lam)
        
        obs, _ = env.reset()
        cum_reward = 0
        while True:
            action = self.agent.act(weights, obs)
            obs, r, t, tr, _ = env.step(action)
            cum_reward += r
            if t or tr:
                print(f"Final Reward: {cum_reward:.1f}")
                break
        env.close()

if __name__ == "__main__":
    
    # 1. BipedalWalker-v3
    # The ultimate test. We need a frame that keeps balance.
    try:
        trainer = FractalFilterTrainer("BipedalWalker-v3")
        best_m, best_l = trainer.run_filter_sweep()
        trainer.visualize(best_m, best_l)
    except Exception as e:
        print(f"Walker Error: {e}")

    # 2. LunarLander-v3
    try:
         trainer = FractalFilterTrainer("LunarLander-v3")
         best_m, best_l = trainer.run_filter_sweep()
         trainer.visualize(best_m, best_l)
    except Exception as e:
         print(f"Lander Error: {e}")