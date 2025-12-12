import numpy as np
import gymnasium as gym
import time
import heapq

class FractalDynamics:
    """
    The Physics Engine of the Manifold.
    Maps coordinates (m, λ) -> Control Gains (P, D, Phase).
    """
    @staticmethod
    def compute_properties(m, lam, steps=50):
        # Symplectic evolution to find the "texture" of the coordinate
        p_m, p_l = 0.0, 0.0
        sigma = 1.0 # The scaling factor
        dt = 0.1
        
        traj_m = []
        traj_l = []
        
        # Integrate the Pirouette Basin
        curr_m, curr_l = m, lam
        for _ in range(steps):
            # Symplectic Euler steps
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
            
            traj_m.append(curr_m)
            traj_l.append(curr_l)
            
            if curr_m**2 + curr_l**2 > 50: break

        # Extract manifold properties from the trajectory
        # These map to: Stiffness, Damping, and Rhythmic Bias
        return {
            'stiffness': 2.0 * traj_m[0],       # Proportional Gain
            'damping': traj_l[0],               # Derivative Gain
            'resonance': np.mean(traj_m),       # Integral/Bias
            'phase_offset': np.arctan2(lam, m), # For cyclic gaits
            'stability': len(traj_m) / steps    # How stable the coordinate is
        }

class ManifoldPolicy:
    """
    The Agent that lives on the Manifold.
    """
    def __init__(self, m, lam, env_type):
        self.props = FractalDynamics.compute_properties(m, lam)
        self.env_type = env_type
        
    def act(self, state):
        p = self.props
        
        if self.env_type == 'LunarLander':
            # State: [x, y, vx, vy, ang, ang_v, l1, l2]
            
            # Vertical Logic (Hover vs Drop)
            # Use 'resonance' to define a comfortable hover height
            target_descent = -0.3 # safe speed
            
            # PD Controller derived from Manifold
            vert_force = (p['stiffness'] * (target_descent - state[3]) + 
                          p['resonance'] * 0.5)
            
            # Horizontal Logic (Stabilization)
            # Use 'damping' to kill angular velocity
            tilt_force = (p['damping'] * state[5] + 
                          p['stiffness'] * state[4])
            
            # Mixer
            if vert_force > 0.5: return 1 # Main
            if tilt_force > 0.2: return 2 # Left engine (push right)
            if tilt_force < -0.2: return 3 # Right engine (push left)
            return 0

        elif self.env_type == 'BipedalWalker':
            # State: 24 dims. Hull(0-3), Joints(4-13), Lidar(14-23)
            # We treat the walker as a rhythmic oscillator coupled to the fractal
            
            hull_angle = state[0]
            hull_ang_vel = state[1]
            vx = state[2]
            
            # The "Spike" in the fractal provides the exact stiffness 
            # needed to keep the hull upright.
            balance_torque = (-p['stiffness'] * hull_angle 
                              -p['damping'] * hull_ang_vel)
            
            # forward drive
            target_vx = 0.5 # Walk, don't run
            drive = p['resonance'] * (target_vx - vx)
            
            actions = np.zeros(4)
            
            # Leg 1 (Hip, Knee)
            # We use the phase_offset to create asymmetry (walking gait)
            actions[0] = balance_torque + drive + np.sin(p['phase_offset'])
            actions[1] = -0.1 * state[6] # Simple knee damping
            
            # Leg 2 (Hip, Knee) - Antiphase
            actions[2] = balance_torque + drive + np.sin(p['phase_offset'] + np.pi)
            actions[3] = -0.1 * state[11]
            
            return np.tanh(actions)
            
        return 0

class ManifoldSurfer:
    """
    The Search Algorithm.
    Recursive Spatial Partitioning to find 'Spikes' in the basin.
    """
    def __init__(self, env_name, generations=3):
        self.env_name = env_name
        self.generations = generations
        self.env_type = 'LunarLander' if 'Lunar' in env_name else 'BipedalWalker'
        self.top_spikes = [] # Stores (reward, m, lam, depth)

    def evaluate_coord(self, m, lam, episodes=1, max_steps=400):
        # We average multiple runs to filter out "Lucky" runs (noise on the manifold)
        total_r = 0
        
        # Critical: Catch errors if Box2D isn't playing nice
        try:
            env = gym.make(self.env_name)
        except:
            return -999
            
        agent = ManifoldPolicy(m, lam, self.env_type)
        
        for _ in range(episodes):
            obs, _ = env.reset()
            ep_r = 0
            steps = 0
            terminated = False
            truncated = False
            
            while not (terminated or truncated) and steps < max_steps:
                action = agent.act(obs)
                obs, r, terminated, truncated, _ = env.step(action)
                ep_r += r
                steps += 1
                
                # Walker 'Fall' check to save time
                if self.env_type == 'BipedalWalker' and ep_r < -80: break
                # Lander 'Crash' check
                if self.env_type == 'LunarLander' and ep_r < -200: break
            
            total_r += ep_r
        
        env.close()
        return total_r / episodes

    def scan_region(self, center_m, center_l, radius, density, depth):
        """
        Scans a specific patch of the fractal.
        Returns the top candidates from this patch.
        """
        # Create grid
        m_vals = np.linspace(center_m - radius, center_m + radius, density)
        l_vals = np.linspace(center_l - radius, center_l + radius, density)
        
        candidates = []
        
        # 2D Scan
        for m in m_vals:
            for lam in l_vals:
                # Fast evaluation (1 episode)
                reward = self.evaluate_coord(m, lam, episodes=1)
                candidates.append((reward, m, lam))
        
        # Sort and return top 3 'Spikes'
        candidates.sort(reverse=True, key=lambda x: x[0])
        return candidates[:3]

    def surf(self):
        print(f"🌊 SURFING THE MANIFOLD: {self.env_name}")
        start_time = time.time()
        
        # --- Gen 0: Global Scan ---
        print("\n[Depth 0] Global Satellite Scan...")
        # Broad search to find continents
        top_seeds = self.scan_region(0, 0, 1.5, density=10, depth=0)
        
        current_best = top_seeds[0]
        print(f"  Found potential basin at: m={current_best[1]:.2f}, λ={current_best[2]:.2f} (R: {current_best[0]:.1f})")

        # --- Recursive Zoom ---
        active_spikes = top_seeds
        
        for gen in range(1, self.generations + 1):
            print(f"\n[Depth {gen}] Zooming into {len(active_spikes)} Spikes...")
            new_spikes = []
            
            radius = 1.5 / (4 ** gen) # Shrink search radius exponentially
            
            for rank, (r, m, lam) in enumerate(active_spikes):
                print(f"  > Investigating Spike #{rank+1} at ({m:.3f}, {lam:.3f})...", end="")
                
                # Scan local area
                local_bests = self.scan_region(m, lam, radius, density=6, depth=gen)
                
                # Verify stability (Re-eval top candidate with more episodes)
                best_local = local_bests[0]
                verified_score = self.evaluate_coord(best_local[1], best_local[2], episodes=5)
                
                print(f" Refined to {verified_score:.1f}")
                new_spikes.append((verified_score, best_local[1], best_local[2]))
            
            # Keep only the absolute best for the next generation to save compute
            new_spikes.sort(reverse=True, key=lambda x: x[0])
            active_spikes = new_spikes[:3] # Keep top 3 lineages
            
            current_best = active_spikes[0]

        duration = time.time() - start_time
        print("\n" + "="*50)
        print(f"🏁 FRACTAL SOLUTION FOUND in {duration:.1f}s")
        print(f"📍 Coordinate: m={current_best[1]:.5f}, λ={current_best[2]:.5f}")
        print(f"🏆 Verified Reward: {current_best[0]:.2f}")
        print("="*50)
        
        return current_best[1], current_best[2]

    def visualize(self, m, lam):
        print("\n🎥 Running Final Simulation...")
        env = gym.make(self.env_name, render_mode="human")
        agent = ManifoldPolicy(m, lam, self.env_type)
        
        obs, _ = env.reset()
        total_r = 0
        while True:
            action = agent.act(obs)
            obs, r, term, trunc, _ = env.step(action)
            total_r += r
            if term or trunc: break
        
        print(f"Final Run Score: {total_r:.2f}")
        env.close()

if __name__ == "__main__":
    
    # 1. Lunar Lander (The 3D Plateau)
    try:
        surfer = ManifoldSurfer("LunarLander-v3", generations=2)
        m, lam = surfer.surf()
        surfer.visualize(m, lam)
    except Exception as e:
        print(f"Lander Error: {e}")

    print("\n\n")

    # 2. BipedalWalker (The Needle in the Haystack)
    try:
        surfer = ManifoldSurfer("BipedalWalker-v3", generations=3)
        m, lam = surfer.surf()
        surfer.visualize(m, lam)
    except Exception as e:
        print(f"Walker Error: {e}")