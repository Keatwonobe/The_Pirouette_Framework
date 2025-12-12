import gymnasium as gym
import numpy as np
import time
import copy

# ---------------------------------------------------------------------------
# 1. THE FRACTAL PHYSICS ENGINE
# ---------------------------------------------------------------------------
class FractalHypernet:
    """
    Generates deterministic weights from a coordinate (m, λ).
    Includes 'Manifold Clamp' for safety.
    """
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def generate_weights(self, m, lam):
        weights = []
        p_m, p_l = 0.0, 0.0
        sigma, dt = 1.0, 0.1
        curr_m, curr_l = m, lam
        ESCAPE = 10.0
        
        # Identify Basin Color for the User
        theta = np.arctan2(lam, m)
        if 0.5 < abs(theta) < 2.5: color = "Teal"
        elif abs(theta) >= 2.5:    color = "Red"
        else:                      color = "Gold"
        
        # Generate Weights
        while len(weights) < self.output_dim:
            if abs(curr_m) > ESCAPE or abs(curr_l) > ESCAPE:
                curr_m = np.fmod(curr_m, 2.0)
                curr_l = np.fmod(curr_l, 2.0)
                p_m *= 0.1; p_l *= 0.1
            
            try:
                grad_m = curr_m + 2 * sigma * curr_m * curr_l
                grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
                p_m -= (dt/2) * grad_m
                p_l -= (dt/2) * grad_l
                curr_m += dt * p_m
                curr_l += dt * p_l
            except:
                curr_m, curr_l = 0.0, 0.0
                
            weights.append(np.tanh(curr_m))
            weights.append(np.tanh(curr_l))
            
        return np.array(weights[:self.output_dim], dtype=np.float32), color

class StaticPolicy:
    def __init__(self, weights, act_dim, obs_dim):
        self.W = weights.reshape(act_dim, obs_dim)
    
    def act(self, obs):
        return np.tanh(self.W @ obs)

# ---------------------------------------------------------------------------
# 2. THE CHAIN BUILDER
# ---------------------------------------------------------------------------
class FractalChainBuilder:
    def __init__(self, env_name, segment_length=30):
        self.env_name = env_name
        self.env = gym.make(env_name)
        self.obs_dim = self.env.observation_space.shape[0]
        self.act_dim = self.env.action_space.shape[0]
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        
        self.segment_length = segment_length # How many frames each "Pixel" controls
        self.chain = [] # List of (m, lam, weights, color) tuples
        
    def evaluate_sequence(self, candidate_m=None, candidate_l=None):
        """
        Runs the full history + the new candidate segment.
        Returns the total reward.
        """
        # Re-create env to ensure determinism (Box2D can be finicky with state setting)
        env = gym.make(self.env_name)
        obs, _ = env.reset(seed=42)
        
        total_reward = 0
        terminated = False
        truncated = False
        
        # 1. Replay History
        for i, (m, l, W, color) in enumerate(self.chain):
            policy = StaticPolicy(W, self.act_dim, self.obs_dim)
            
            # Run for segment_length frames
            for _ in range(self.segment_length):
                action = policy.act(obs)
                obs, r, term, trunc, _ = env.step(action)
                total_reward += r
                if term or trunc: 
                    env.close()
                    return -100 # Penalize early death in history
                    
        # 2. Test Candidate (if provided)
        if candidate_m is not None:
            weights, _ = self.hypernet.generate_weights(candidate_m, candidate_l)
            policy = StaticPolicy(weights, self.act_dim, self.obs_dim)
            
            segment_reward = 0
            for _ in range(self.segment_length):
                action = policy.act(obs)
                obs, r, term, trunc, _ = env.step(action)
                segment_reward += r
                total_reward += r
                
                # FAIL FAST: If we crash during the new segment
                if term or trunc:
                    if r == -100: # Crash penalty
                        return -500 
                    break
            
            # We return the Total Reward, but the search optimizes for the *Segment* contribution
            # combined with survival.
            
        env.close()
        return total_reward

    def find_next_link(self, n_samples=50):
        """
        Searches for the next best 'Fractal Pixel' to append to the chain.
        """
        best_r = -float('inf')
        best_coord = None
        best_color = "Unknown"
        
        # Search Strategy: Random Sampling across the basin
        # We look for "Gold" (Stability) and "Red" (Action) primarily
        m_vals = np.random.uniform(-1.5, 1.5, n_samples)
        l_vals = np.random.uniform(-1.5, 1.5, n_samples)
        
        # Add some specific "known good" regions to the search
        m_vals = np.concatenate([m_vals, [0.0, -0.5, 0.5]])
        l_vals = np.concatenate([l_vals, [0.0, 0.5, -0.5]])
        
        for m, l in zip(m_vals, l_vals):
            # Run the chain + this candidate
            r = self.evaluate_sequence(m, l)
            
            if r > best_r:
                best_r = r
                best_coord = (m, l)
                _, best_color = self.hypernet.generate_weights(m, l)
        
        return best_coord, best_color, best_r

    def build_chain(self, steps=10):
        print(f"🔗 BUILDING FRACTAL CHAIN: {self.env_name}")
        print(f"   Segment Length: {self.segment_length} frames")
        print(f"   Target: {steps} Linked Moves")
        
        start_time = time.time()
        
        for step in range(steps):
            print(f"\n[Step {step+1}/{steps}] Searching Manifold...")
            
            # Find best next move
            coord, color, score = self.find_next_link(n_samples=60)
            
            # Generate weights and lock it in
            m, l = coord
            W, _ = self.hypernet.generate_weights(m, l)
            self.chain.append((m, l, W, color))
            
            print(f"   > Locked Pixel: {color} Basin ({m:.2f}, {l:.2f})")
            print(f"   > Current Run Score: {score:.1f}")
            
            # Early Exit if solved
            if score > 280: # LunarLander/Walker solved
                print("   > Task Solved Early!")
                break
                
        duration = time.time() - start_time
        print(f"\n✨ CHAIN COMPLETE in {duration:.1f}s")
        print(f"   Sequence: {' -> '.join([c[3] for c in self.chain])}")
        
    def visualize(self):
        print("\n🎥 Playing Fractal Symphony...")
        env = gym.make(self.env_name, render_mode="human")
        obs, _ = env.reset(seed=42)
        
        total = 0
        
        try:
            for i, (m, l, W, color) in enumerate(self.chain):
                print(f"Frame {i*self.segment_length}: Switching to {color} ({m:.2f}, {l:.2f})")
                policy = StaticPolicy(W, self.act_dim, self.obs_dim)
                
                for _ in range(self.segment_length):
                    action = policy.act(obs)
                    obs, r, term, trunc, _ = env.step(action)
                    total += r
                    if term or trunc: break
                if term or trunc: break
        except Exception as e:
            print(e)
            
        print(f"Final Score: {total:.1f}")
        env.close()

if __name__ == "__main__":
    # Try BipedalWalker - The "Simon Says" of Physics
    # It needs to learn: Balance -> Lift -> Swing -> Land
    try:
        # Shorter segments (20 frames) for finer control
        builder = FractalChainBuilder("BipedalWalker-v3", segment_length=20)
        builder.build_chain(steps=15) # Build a 300-frame sequence
        builder.visualize()
    except Exception as e:
        print(f"Walker Error: {e}")