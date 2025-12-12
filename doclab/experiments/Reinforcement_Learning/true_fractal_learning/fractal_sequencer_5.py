import gymnasium as gym
import numpy as np
import time

# --- 1. THE FRACTAL CORE (Robust) ---
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def generate_weights(self, m, lam):
        weights = []
        p_m, p_l = 0.0, 0.0
        sigma, dt = 1.0, 0.1
        curr_m, curr_l = m, lam
        ESCAPE = 10.0
        
        # Color Detector
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"
        elif abs(theta) > 2.5: color = "Red"
        else:                  color = "Gold"

        while len(weights) < self.output_dim:
            if abs(curr_m) > ESCAPE or abs(curr_l) > ESCAPE:
                curr_m = np.fmod(curr_m, 2.0); curr_l = np.fmod(curr_l, 2.0)
                p_m *= 0.1; p_l *= 0.1
            try:
                grad_m = curr_m + 2 * sigma * curr_m * curr_l
                grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
                p_m -= (dt/2) * grad_m; p_l -= (dt/2) * grad_l
                curr_m += dt * p_m; curr_l += dt * p_l
                if np.isnan(curr_m): curr_m = 0.0
            except: curr_m, curr_l = 0.0, 0.0
            weights.append(np.tanh(curr_m)); weights.append(np.tanh(curr_l))
        return np.array(weights[:self.output_dim], dtype=np.float32), color

# --- 2. THE RIPPLE GAIT ---
class RippleGait:
    def __init__(self, env_name, params):
        self.env_name = env_name
        # Unpack Genes
        self.center_m = params[0]
        self.center_l = params[1]
        self.radius_m = params[2] 
        self.radius_l = params[3] 
        self.tilt     = params[4] 
        self.freq     = params[5] 
        self.phase    = params[6] 
        
        # Motors: 0:Hip1, 1:Knee1, 2:Hip2, 3:Knee2
        self.motor_names = ["R.Hip", "R.Knee", "L.Hip", "L.Knee"]
        
        # Engine
        dummy = gym.make(env_name)
        self.obs_dim = dummy.observation_space.shape[0]
        self.act_dim = dummy.action_space.shape[0]
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        dummy.close()
        
    def get_body_mask(self, angle):
        """
        Creates a rolling wave of activation across the 4 motors.
        The angle (0 to 2pi) determines which part is 'hot'.
        """
        # Normalize angle to 0-1 cycle
        cycle = (angle % (2 * np.pi)) / (2 * np.pi)
        
        # We define 4 windows (Gaussian bumps) for the 4 motors
        # Motor 0 (R.Hip) peaks at 0.0
        # Motor 1 (R.Knee) peaks at 0.125 (slightly after hip)
        # Motor 2 (L.Hip) peaks at 0.5 (Anti-phase)
        # Motor 3 (L.Knee) peaks at 0.625
        
        centers = np.array([0.0, 0.15, 0.5, 0.65]) 
        width = 0.15 # Sharpness of the activation
        
        # Distance calculation handling the wrap-around (0 == 1)
        dist = np.abs(cycle - centers)
        dist = np.minimum(dist, 1.0 - dist)
        
        # Gaussian Activation: exp(-dist^2 / width)
        activation = np.exp(-(dist**2) / (2 * width**2))
        
        # Identify dominant part for display
        dominant_idx = np.argmax(activation)
        return activation, self.motor_names[dominant_idx]

    def get_action(self, obs, t_step):
        # 1. The Clock
        angle = self.phase + (t_step * 0.02 * self.freq * 2 * np.pi)
        
        # 2. The Geometry (Orbit)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(self.tilt), np.sin(self.tilt)
        
        m = self.center_m + (self.radius_m * cos_a * cos_t - self.radius_l * sin_a * sin_t)
        lam = self.center_l + (self.radius_m * cos_a * sin_t + self.radius_l * sin_a * cos_t)
        
        # 3. The Fractal (Physics)
        weights, color = self.hypernet.generate_weights(m, lam)
        W = weights.reshape(self.act_dim, self.obs_dim)
        
        # 4. The Ripple (Body Sequence)
        mask, active_part = self.get_body_mask(angle)
        
        # 5. Combine: Action = (Fractal_Policy * Obs) * Body_Mask
        raw_action = np.tanh(W @ obs)
        masked_action = raw_action * mask
        
        return masked_action, color, active_part

# --- 3. THE OPTIMIZER ---
class RippleSearch:
    def __init__(self, env_name):
        self.env_name = env_name
        
    def evaluate_gait(self, params, render=False):
        agent = RippleGait(self.env_name, params)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        total_reward = 0
        forward_velocity_bonus = 0
        steps = 0
        
        last_part = ""
        
        while steps < 500:
            action, color, part = agent.get_action(obs, steps)
            obs, r, term, trunc, _ = env.step(action)
            
            total_reward += r
            forward_velocity_bonus += obs[2]
            
            # Visual feedback on the sequence
            if render and part != last_part:
                # print(f"   Frame {steps}: Activating {part} ({color} Basin)")
                last_part = part
            
            steps += 1
            if term or trunc:
                if steps < 50: total_reward = -100
                break
        
        env.close()
        return total_reward + (forward_velocity_bonus * 8.0) # High velocity incentive

    def optimize(self):
        print(f"🌊 FRACTAL RIPPLE SEARCH: {self.env_name}")
        print("   Synchronizing Manifold Physics with Body Sequence...")
        
        # Gene: [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        # Init around Triple Point
        population = []
        for _ in range(30):
            gene = [
                np.random.normal(-0.2, 0.1), # Center M
                np.random.normal(-0.2, 0.1), # Center L
                np.random.uniform(0.5, 0.9), # Radius (Large for big steps)
                np.random.uniform(0.5, 0.9),
                np.random.uniform(0, np.pi),
                np.random.uniform(0.8, 1.8), # Slightly faster freq for walking
                np.random.uniform(0, 2*np.pi)
            ]
            population.append(gene)
        population = np.array(population)
            
        best_fit = -float('inf')
        best_gene = None
        
        for gen in range(15):
            scores = []
            for i, gene in enumerate(population):
                fit = self.evaluate_gait(gene)
                scores.append(fit)
                
                if fit > best_fit:
                    best_fit = fit
                    best_gene = gene.copy()
                    print(f"   [Gen {gen}] New Ripple: Vel Bonus={fit:.1f} | Freq={gene[5]:.2f}Hz")
            
            # Selection
            elites = population[np.argsort(scores)[-5:]]
            
            # Mutation
            new_pop = []
            for _ in range(30):
                parent = elites[np.random.randint(len(elites))].copy()
                noise = np.random.normal(0, 0.05, size=7)
                child = parent + noise
                # Enforce minimum stride size
                child[2] = max(0.4, child[2])
                child[3] = max(0.4, child[3])
                new_pop.append(child)
            population = np.array(new_pop)
            
            if best_fit > 350:
                print("   > Dominant Gait Found.")
                break

        print(f"✨ RIPPLE LOCKED. Best Fitness: {best_fit:.1f}")
        return best_gene

if __name__ == "__main__":
    try:
        searcher = RippleSearch("BipedalWalker-v3")
        best_ripple = searcher.optimize()
        
        print("\nVisualizing the Sequential Gait...")
        searcher.evaluate_gait(best_ripple, render=True)
    except Exception as e:
        print(f"Error: {e}")