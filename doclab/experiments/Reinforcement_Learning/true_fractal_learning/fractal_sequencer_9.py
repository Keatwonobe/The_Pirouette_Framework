import gymnasium as gym
import numpy as np
import time

# --- 1. THE FRACTAL PHYSICS CORE (Robust & Fast) ---
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def generate_weights(self, m, lam):
        weights = []
        # Robust simulation parameters
        curr_m, curr_l = m, lam
        sigma, dt, ESCAPE = 1.0, 0.1, 10.0
        
        # Determine Basin Identity (The "Flavor" of physics)
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"     # Damping
        elif abs(theta) > 2.5: color = "Red"     # Chaos/Force
        else:                  color = "Gold"    # Stiffness
        
        while len(weights) < self.output_dim:
            # Manifold Clamp (The Space Folder)
            if abs(curr_m) > ESCAPE or abs(curr_l) > ESCAPE:
                curr_m = np.fmod(curr_m, 2.0)
                curr_l = np.fmod(curr_l, 2.0)
            
            try:
                # Symplectic Euler Step
                grad_m = curr_m + 2 * sigma * curr_m * curr_l
                grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
                curr_m += dt * (curr_m + 2 * sigma * curr_m * curr_l) # Simplified for speed
                curr_l += dt * (curr_l + sigma * (curr_m**2 - curr_l**2))
            except: 
                curr_m, curr_l = 0.0, 0.0
                
            weights.append(np.tanh(curr_m))
            weights.append(np.tanh(curr_l))
            
        return np.array(weights[:self.output_dim], dtype=np.float32), color

# --- 2. THE ORBIT KING AGENT ---
class OrbitKingAgent:
    """
    Directly maps Orbit Parameters -> Fractal Weights -> Motor Torques.
    No intermediate static policies.
    """
    def __init__(self, env_name, params):
        self.env_name = env_name
        
        # The Royal Decree (Orbit Parameters)
        self.center_m = params[0]
        self.center_l = params[1]
        self.radius_m = params[2] # Must be large to prevent collapse
        self.radius_l = params[3]
        self.tilt     = params[4]
        self.freq     = params[5]
        self.phase    = params[6]
        
        # Engine Setup
        dummy = gym.make(env_name)
        self.obs_dim = dummy.observation_space.shape[0]
        self.act_dim = dummy.action_space.shape[0]
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        dummy.close()

    def get_action_data(self, obs, t_step):
        # 1. Calculate Phase (The Heartbeat)
        # t_step is frames (approx 0.02s)
        angle = self.phase + (t_step * 0.02 * self.freq * 2 * np.pi)
        
        # 2. Parametric Ellipse (The Geometry)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(self.tilt), np.sin(self.tilt)
        
        m = self.center_m + (self.radius_m * cos_a * cos_t - self.radius_l * sin_a * sin_t)
        lam = self.center_l + (self.radius_m * cos_a * sin_t + self.radius_l * sin_a * cos_t)
        
        # 3. Generate Physics (The Real-Time Fractal)
        weights, color = self.hypernet.generate_weights(m, lam)
        W = weights.reshape(self.act_dim, self.obs_dim)
        
        # 4. Motor Output
        action = np.tanh(W @ obs)
        
        return action, color, (m, lam)

# --- 3. THE NOVELTY ARCHIVE (The Historian) ---
class NoveltyHistorian:
    def __init__(self):
        self.history = [] # Stores successful genes
        
    def get_novelty(self, gene):
        if not self.history: return 10.0
        
        # Compare current gene to history
        # We focus on Frequency and Radius (The "Vibe" of the orbit)
        diffs = []
        for past_gene in self.history:
            # Distance in parameter space
            d = np.linalg.norm(gene - past_gene)
            diffs.append(d)
        
        return min(diffs) # Distance to nearest neighbor
        
    def record(self, gene, score):
        # Only record decent runs to avoid filling history with trash
        if score > -50:
            self.history.append(gene.copy())
            # Keep history manageable
            if len(self.history) > 100:
                self.history.pop(0)

# --- 4. THE CORONATION (Trainer) ---
class Coronation:
    def __init__(self, env_name):
        self.env_name = env_name
        self.historian = NoveltyHistorian()
        
    def evaluate_orbit(self, gene, render=False):
        agent = OrbitKingAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        total_reward = 0
        basin_crossings = 0
        last_color = ""
        steps = 0
        
        while steps < 500:
            action, color, coords = agent.get_action_data(obs, steps)
            obs, r, term, trunc, _ = env.step(action)
            
            total_reward += r
            
            # The Mandate: You Must Travel
            if color != last_color and steps > 5:
                basin_crossings += 1
                if render: print(f"   Frame {steps}: Crossed into {color}")
            last_color = color
            
            steps += 1
            if term or trunc:
                if steps < 50: total_reward = -100 # Punish instant death
                break
        
        env.close()
        
        # FITNESS FUNCTION
        # Score + (Basin Crossings * 5) - (Collapse Penalty)
        
        # Check for collapse (Radius too small)
        radius_avg = (gene[2] + gene[3]) / 2
        collapse_penalty = 0
        if radius_avg < 0.3: collapse_penalty = 100
        
        fitness = total_reward + (basin_crossings * 5.0) - collapse_penalty
        return fitness, total_reward

    def evolve(self):
        print(f"👑 THE ORBIT KING: {self.env_name}")
        print("   Directly Evolving Parametric Fractal Orbits...")
        
        # Population Init
        # Gene: [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        population = []
        for _ in range(25):
            gene = np.array([
                np.random.normal(0, 0.2), np.random.normal(0, 0.2), # Center
                np.random.uniform(0.5, 1.0), np.random.uniform(0.5, 1.0), # Radius (Large!)
                np.random.uniform(0, np.pi), # Tilt
                np.random.uniform(0.5, 1.5), # Freq
                np.random.uniform(0, 2*np.pi) # Phase
            ])
            population.append(gene)
        population = np.array(population)
        
        best_ever_gene = None
        best_ever_score = -float('inf')
        
        for gen in range(15):
            print(f"\n--- Generation {gen+1} ---")
            
            scores = []
            novelties = []
            
            for i, gene in enumerate(population):
                # Force Radius (Anti-Collapse Mandate)
                gene[2] = max(0.4, gene[2])
                gene[3] = max(0.4, gene[3])
                
                # 1. Physics Eval
                fit, raw_score = self.evaluate_orbit(gene)
                
                # 2. Novelty Eval
                novelty = self.historian.get_novelty(gene)
                
                # 3. Combined Score
                # We prioritize fitness, but use novelty as a tie-breaker/booster
                final_score = fit + (novelty * 10.0)
                
                scores.append(final_score)
                novelties.append(novelty)
                
                if raw_score > best_ever_score:
                    best_ever_score = raw_score
                    best_ever_gene = gene.copy()
                    print(f"   🏆 NEW KING: Score {raw_score:.1f} | Freq {gene[5]:.2f}Hz")
            
            # Archive the winners
            # Sort by raw score to archive competent agents
            ranked_indices = np.argsort(scores)
            top_idx = ranked_indices[-1]
            self.historian.record(population[top_idx], scores[top_idx])
            
            # Selection & Mutation
            elites = population[ranked_indices[-5:]] # Top 5
            
            new_pop = []
            for _ in range(25):
                parent = elites[np.random.randint(len(elites))].copy()
                # Mutation
                noise = np.random.normal(0, 0.08, size=7)
                child = parent + noise
                new_pop.append(child)
            population = np.array(new_pop)
            
            if best_ever_score > 300:
                print("   > The King has ascended.")
                break
                
        print(f"✨ CORONATION COMPLETE. High Score: {best_ever_score:.1f}")
        return best_ever_gene

if __name__ == "__main__":
    try:
        kingdom = Coronation("BipedalWalker-v3")
        king_gene = kingdom.evolve()
        
        print("\nVisualizing the Reign of the Orbit King...")
        kingdom.evaluate_orbit(king_gene, render=True)
    except Exception as e:
        print(f"Error: {e}")