import numpy as np
import gymnasium as gym
import time

class FractalPolicyGenerator:
    """
    The Brain: Now scaling to multi-dimensional control.
    """
    def compute_basin_features(self, m, lam, max_steps=100):
        # --- The Pirouette Dynamics (Same as before) ---
        p_m, p_l = 0.0, 0.0
        sigma = 1.0
        dt = 0.1
        
        trajectory_m = [m]
        trajectory_l = [lam]
        
        for _ in range(max_steps):
            grad_m = m + 2 * sigma * m * lam
            grad_l = lam + sigma * (m**2 - lam**2)
            
            p_m_half = p_m - (dt / 2) * grad_m
            p_l_half = p_l - (dt / 2) * grad_l
            
            m = m + dt * p_m_half
            lam = lam + dt * p_l_half
            
            grad_m_new = m + 2 * sigma * m * lam
            grad_l_new = lam + sigma * (m**2 - lam**2)
            
            p_m = p_m_half - (dt / 2) * grad_m_new
            p_l = p_l_half - (dt / 2) * grad_l_new
            
            trajectory_m.append(m)
            trajectory_l.append(lam)
            
            if m**2 + lam**2 > 20: break
            
        return {
            'coherence': 2 * trajectory_m[0],   # The "Stiffness" / P-Gain
            'coupling': trajectory_l[0],        # The "Damping" / D-Gain
            'interaction': trajectory_m[0] * trajectory_l[0], # Cross-term
            'bias': np.arctan2(lam, m)          # Directional Preference
        }
    
    def get_policy(self, m, lam, env_name):
        features = self.compute_basin_features(m, lam)
        
        if 'LunarLander' in env_name:
            def policy_fn(state):
                # State: [x, y, vx, vy, angle, v_angle, leg1, leg2]
                
                # 1. Vertical Control (Main Engine)
                # We want vy to be positive (up) if we are low, but negative (down) to land.
                # Heuristic: Hover if dropping too fast.
                vertical_target = -0.5 # Target descent speed
                v_error = vertical_target - state[3]
                
                # Coherence drives main thrust based on descent speed
                main_engine_signal = features['coherence'] * v_error + features['bias']
                
                # 2. Horizontal/Angle Control (Side Engines)
                # Coupling drives stabilization of angle and horizontal speed
                angle_stabilize = features['coupling'] * (state[4] + state[5])
                horizontal_stabilize = features['interaction'] * state[2]
                
                side_engine_signal = angle_stabilize + horizontal_stabilize
                
                # Discrete Action Map for LunarLander-v3
                # 0: Do nothing, 1: Main, 2: Left, 3: Right
                if main_engine_signal > 0.5:
                    return 1 # Fire Main
                elif side_engine_signal > 0.3:
                    return 2 # Fire Left (Push Right)
                elif side_engine_signal < -0.3:
                    return 3 # Fire Right (Push Left)
                else:
                    return 0
            return policy_fn

        elif 'BipedalWalker' in env_name:
            def policy_fn(state):
                # State: 24 dimensions.
                # 0: Hull Angle, 2: vx, 3: vy
                # 4-8: Leg 1 (Hip angle, Knee angle...)
                # 9-13: Leg 2 (Hip angle, Knee angle...)
                
                hull_angle = state[0]
                vx = state[2]
                
                # We create a "Reactive Walker"
                # It doesn't plan; it reflexes based on Fractal Gains.
                
                # Gain A: Keep Hull Flat (P-Control on Hull)
                hull_restore = -features['coherence'] * hull_angle
                
                # Gain B: Move Forward (Bias on Hips)
                forward_drive = features['bias'] * 0.5
                
                # Gain C: Leg Damping (D-Control on Joints)
                # We apply the 'Coupling' term to the joint speeds to stop jitter
                
                actions = np.zeros(4)
                
                # Simple Sine-based Gait approximation driven by Fractal
                # This is a "Neuro- Oscillator" approach
                # We use the hull angle to drive the legs anti-symmetrically
                
                # Hip 1 & 2 (Opposite phases)
                actions[0] = hull_restore + forward_drive + (features['interaction'] * state[4])
                actions[2] = hull_restore + forward_drive - (features['interaction'] * state[9])
                
                # Knees 1 & 2 (Stabilization)
                actions[1] = features['coupling'] * state[6] # Damping Knee 1
                actions[3] = features['coupling'] * state[11] # Damping Knee 2
                
                return np.tanh(actions) # Clip to -1, 1
                
            return policy_fn
        
        else:
            raise ValueError("Unknown Environment")

class FractalTrainer:
    def __init__(self, env_name):
        self.env_name = env_name
        self.generator = FractalPolicyGenerator()
        
    def evaluate(self, m, lam, episodes=1, max_steps=500):
        policy = self.generator.get_policy(m, lam, self.env_name)
        
        # Capture errors for environments that might not be installed
        try:
            env = gym.make(self.env_name)
        except gym.error.DependencyNotInstalled:
            print(f"Error: {self.env_name} requires Box2D. 'pip install gymnasium[box2d]'")
            return -9999

        total_reward = 0
        for _ in range(episodes):
            obs, _ = env.reset()
            ep_reward = 0
            steps = 0
            terminated = False
            truncated = False
            
            while not (terminated or truncated) and steps < max_steps:
                action = policy(obs)
                obs, reward, terminated, truncated, _ = env.step(action)
                ep_reward += reward
                steps += 1
                
                # EARLY STOPPING FOR EFFICIENCY
                # If Walker falls effectively (very low reward), abort early to save time
                if 'Walker' in self.env_name and ep_reward < -100:
                    break
                    
            total_reward += ep_reward
        env.close()
        return total_reward / episodes

    def train(self):
        print(f"🌀 FRACTAL TRAINING: {self.env_name}")
        start_time = time.time()
        
        # --- PHASE 1: GRID SCAN ---
        # Expanded range for complex dynamics
        m_vals = np.linspace(-1.5, 1.5, 12)
        l_vals = np.linspace(-1.5, 1.5, 12)
        
        best_reward = -float('inf')
        best_coord = (0,0)
        
        print("Scanning Basin Coordinates...")
        count = 0
        total = len(m_vals) * len(l_vals)
        
        for m in m_vals:
            for lam in l_vals:
                r = self.evaluate(m, lam, episodes=1, max_steps=400)
                
                if r > best_reward:
                    best_reward = r
                    best_coord = (m, lam)
                    # print(f"  New Best: {best_reward:.1f} at ({m:.2f}, {lam:.2f})")
                
                count += 1
                if count % 20 == 0:
                    print(f"  Progress: {count}/{total} | Top: {best_reward:.1f}")

        # --- PHASE 2: LOCAL ZOOM ---
        print(f"\nZooming in on ({best_coord[0]:.2f}, {best_coord[1]:.2f})...")
        center_m, center_l = best_coord
        radius = 0.2
        
        m_fine = np.linspace(center_m - radius, center_m + radius, 8)
        l_fine = np.linspace(center_l - radius, center_l + radius, 8)
        
        for m in m_fine:
            for lam in l_fine:
                r = self.evaluate(m, lam, episodes=3, max_steps=600) # More robust check
                if r > best_reward:
                    best_reward = r
                    best_coord = (m, lam)

        duration = time.time() - start_time
        print(f"✨ COMPLETE in {duration:.1f}s.")
        print(f"🏆 Best Reward: {best_reward:.1f} at m={best_coord[0]:.3f}, λ={best_coord[1]:.3f}")
        return best_coord

    def visualize(self, coord):
        print(f"\nVisualizing {self.env_name}...")
        env = gym.make(self.env_name, render_mode="human")
        policy = self.generator.get_policy(coord[0], coord[1], self.env_name)
        
        obs, _ = env.reset()
        total_reward = 0
        while True:
            action = policy(obs)
            obs, reward, terminated, truncated, _ = env.step(action)
            total_reward += reward
            if terminated or truncated:
                print(f"Episode Reward: {total_reward:.1f}")
                break
        env.close()

if __name__ == "__main__":
    
    # 1. LUNAR LANDER
    # This usually learns a very aggressive "Hoverslam" strategy
    try:
        lander = FractalTrainer("LunarLander-v3")
        best_lander_coords = lander.train()
        lander.visualize(best_lander_coords)
    except Exception as e:
        print(f"Skipping LunarLander: {e}")

    print("\n" + "="*50 + "\n")

    # 2. BIPEDAL WALKER
    # This is the 'Hail Mary'. If this walks, the fractal theory is magic.
    try:
        walker = FractalTrainer("BipedalWalker-v3")
        best_walker_coords = walker.train()
        walker.visualize(best_walker_coords)
    except Exception as e:
        print(f"Skipping BipedalWalker: {e}")