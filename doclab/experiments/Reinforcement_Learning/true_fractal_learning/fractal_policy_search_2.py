import numpy as np
import gymnasium as gym
import time
import matplotlib.pyplot as plt

class FractalPolicyGenerator:
    """
    The Core Brain: Maps Fractal Coordinates (m, λ) to Control Physics.
    Adapted to handle both Discrete (CartPole) and Continuous (Pendulum) spaces.
    """
    def __init__(self):
        pass
        
    def compute_basin_features(self, m, lam, max_steps=100):
        """Evolve (m, λ) to extract dynamic features (Coherence, Coupling, Basin)."""
        p_m, p_l = 0.0, 0.0
        sigma = 1.0
        dt = 0.1
        
        trajectory_m = [m]
        trajectory_l = [lam]
        
        # Symplectic evolution (The Pirouette dynamics)
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
        
        theta_final = np.arctan2(lam, m)
        
        # Basin Classification (Teal/Gold/Red)
        if 0.5 < theta_final < 2.5: basin = 0    # Teal
        elif np.abs(theta_final) > 2.5: basin = 2 # Red
        else: basin = 1                           # Gold
        
        return {
            'basin': basin,
            'coherence': 2 * trajectory_m[0], # Acts as Proportional Gain
            'coupling': trajectory_l[0],      # Acts as Derivative Gain
            'interaction_strength': trajectory_m[0] * trajectory_l[0]
        }
    
    def get_policy(self, m, lam, mode='cartpole'):
        features = self.compute_basin_features(m, lam)
        
        def policy_fn(state):
            # 1. Standardize Inputs
            if mode == 'cartpole':
                # State: [x, x_dot, theta, theta_dot]
                pos = state[0]
                vel = state[1]
                angle = state[2]
                ang_vel = state[3]
                
                # Cross-Coupling Control Law (The "Pirouette" Strategy)
                # Mixing linear position with angular velocity
                val = (features['coherence'] * (pos + angle * 10.0) + 
                       features['coupling'] * (vel + ang_vel) + 
                       features['interaction_strength'] * (pos * ang_vel))
                
                # Discrete Action
                return 1 if val > 0 else 0

            elif mode == 'pendulum':
                # State: [cos(theta), sin(theta), theta_dot]
                # Convert back to angle for the fractal logic
                cos_th, sin_th, ang_vel = state
                current_angle = np.arctan2(sin_th, cos_th)
                
                # Continuous Control Law
                # We normalize the angle to encourage the swing up
                angle_error = ((current_angle + np.pi) % (2*np.pi)) - np.pi
                
                # Fractal PD Controller
                # Coherence -> Stiffness (P), Coupling -> Damping (D)
                torque = (-features['coherence'] * 5.0 * angle_error + 
                          -features['coupling'] * 2.0 * ang_vel)
                
                # Clip to env bounds (-2.0 to 2.0 usually)
                return np.clip([torque], -2.0, 2.0)
                
        return policy_fn

class FractalTrainer:
    def __init__(self, env_name):
        self.env_name = env_name
        self.mode = 'cartpole' if 'CartPole' in env_name else 'pendulum'
        self.generator = FractalPolicyGenerator()
        
    def evaluate(self, m, lam, episodes=3, render=False):
        """Runs a policy defined by (m, λ)"""
        policy = self.generator.get_policy(m, lam, self.mode)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        
        total_rewards = []
        for _ in range(episodes):
            obs, _ = env.reset()
            done = False
            ep_reward = 0
            steps = 0
            while not done:
                action = policy(obs)
                obs, reward, terminated, truncated, _ = env.step(action)
                ep_reward += reward
                steps += 1
                done = terminated or truncated
                if self.mode == 'pendulum' and steps >= 200: break # Speed up search
            total_rewards.append(ep_reward)
        
        env.close()
        return np.mean(total_rewards)

    def train(self):
        print(f"🌀 FRACTAL TRAINING STARTED: {self.env_name}")
        start_time = time.time()
        
        # --- PHASE 1: GLOBAL BASIN SCAN ---
        print("\n--- Phase 1: Scanning the Pirouette Basin (Coarse) ---")
        # Focusing on the "Gold" basin region seen in your heatmap
        m_vals = np.linspace(-1.0, 1.0, 15)
        l_vals = np.linspace(-1.0, 1.0, 15)
        
        best_reward = -float('inf')
        best_coord = (0,0)
        
        heatmap = np.zeros((15, 15))
        
        total_points = len(m_vals) * len(l_vals)
        for i, m in enumerate(m_vals):
            for j, lam in enumerate(l_vals):
                r = self.evaluate(m, lam, episodes=1)
                heatmap[j, i] = r # Visualize later if needed
                
                if r > best_reward:
                    best_reward = r
                    best_coord = (m, lam)
            
            # Simple progress bar
            prog = int((i / len(m_vals)) * 20)
            print(f"\rScanning: [{'='*prog}{' '*(20-prog)}] Best: {best_reward:.1f}", end="")

        print(f"\nPhase 1 Best: {best_reward:.1f} at (m={best_coord[0]:.2f}, λ={best_coord[1]:.2f})")

        # --- PHASE 2: FRACTAL ZOOM ---
        print("\n--- Phase 2: Fractal Zoom (Local Refinement) ---")
        # Zoom in 10x closer to the best point
        radius = 0.15
        center_m, center_l = best_coord
        
        m_fine = np.linspace(center_m - radius, center_m + radius, 10)
        l_fine = np.linspace(center_l - radius, center_l + radius, 10)
        
        for i, m in enumerate(m_fine):
            for j, lam in enumerate(l_fine):
                # Evaluate with more episodes for stability
                r = self.evaluate(m, lam, episodes=3)
                if r > best_reward:
                    best_reward = r
                    best_coord = (m, lam)
        
        duration = time.time() - start_time
        print(f"\n✨ TRAINING COMPLETE in {duration:.2f} seconds.")
        print(f"🏆 Ultimate Coordinate: m={best_coord[0]:.4f}, λ={best_coord[1]:.4f}")
        print(f"⭐️ Best Reward: {best_reward:.1f}")
        
        return best_coord

if __name__ == "__main__":
    # 1. Run CartPole
    print("="*60)
    trainer_cp = FractalTrainer("CartPole-v1")
    best_cp = trainer_cp.train()
    
    # Show off the winner
    print("\nVisualizing Best CartPole Agent...")
    trainer_cp.evaluate(best_cp[0], best_cp[1], episodes=2, render=True)

    # 2. Run Pendulum
    print("\n" + "="*60)
    trainer_p = FractalTrainer("Pendulum-v1")
    best_p = trainer_p.train()
    
    # Show off the winner
    print("\nVisualizing Best Pendulum Agent...")
    trainer_p.evaluate(best_p[0], best_p[1], episodes=2, render=True)