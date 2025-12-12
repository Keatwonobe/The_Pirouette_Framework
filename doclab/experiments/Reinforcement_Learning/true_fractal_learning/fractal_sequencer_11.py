import gymnasium as gym
import numpy as np
import time
from collections import deque

# ============================================================
# 1. TOPOLOGICAL PHYSICS ENGINE
# ============================================================

class TopologicalHypernet:
    """
    The Fractal Core, enhanced with Hénon-Heiles Potential awareness.
    """
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def get_potential_energy(self, x, y):
        """
        The Hénon-Heiles Potential V(x,y).
        Used to weight the importance of the twist.
        """
        # We fix the internal lambda parameter to 1.0 for the manifold landscape
        lam_param = 1.0 
        return 0.5 * (x**2 + y**2) + lam_param * (x**2 * y - (1.0/3.0) * y**3)

    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt, ESCAPE = 1.0, 0.1, 10.0
        
        # Basin Coloring for viz
        theta = np.arctan2(lam, m)
        if 0.5 < theta < 2.5: color = "Teal"
        elif abs(theta) > 2.5: color = "Red"
        else:                  color = "Gold"

        while len(weights) < self.output_dim:
            if abs(curr_m) > ESCAPE or abs(curr_l) > ESCAPE:
                curr_m = np.fmod(curr_m, 2.0); curr_l = np.fmod(curr_l, 2.0)
            try:
                grad_m = curr_m + 2 * sigma * curr_m * curr_l
                grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
                curr_m += dt * (curr_m + 2 * sigma * curr_m * curr_l)
                curr_l += dt * (curr_l + sigma * (curr_m**2 - curr_l**2))
            except: curr_m, curr_l = 0.0, 0.0
            weights.append(np.tanh(curr_m)); weights.append(np.tanh(curr_l))
            
        return np.array(weights[:self.output_dim], dtype=np.float32), color

# ============================================================
# 2. THE KNOTTED AGENT
# ============================================================

class KnottedOrbitAgent:
    def __init__(self, env_name, params):
        self.env_name = env_name
        # Gene: [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        self.params = params
        
        dummy = gym.make(env_name)
        self.obs_dim = dummy.observation_space.shape[0]
        self.act_dim = dummy.action_space.shape[0]
        self.hypernet = TopologicalHypernet(self.obs_dim * self.act_dim)
        dummy.close()
        
        # History buffer for calculating derivatives (Knottedness)
        # Stores (m, lambda) tuples
        self.history = deque(maxlen=5) 

    def calculate_instant_knottedness(self, m, lam):
        """
        Calculates the instantaneous Knottedness (K_inst) of the orbit.
        K ~ |V| * Curvature
        """
        self.history.append(np.array([m, lam]))
        
        if len(self.history) < 3:
            return 0.0
            
        # 1. Finite Difference Derivatives
        # Position vectors
        r_curr = self.history[-1]
        r_prev = self.history[-2]
        r_prev2 = self.history[-3]
        
        # Velocity (v) and Acceleration (a)
        v = r_curr - r_prev
        v_prev = r_prev - r_prev2
        a = v - v_prev
        
        # 2. Curvature (kappa)
        # k = |vx * ay - vy * ax| / |v|^3
        vx, vy = v[0], v[1]
        ax, ay = a[0], a[1]
        
        speed_sq = vx**2 + vy**2
        speed = np.sqrt(speed_sq) + 1e-9
        
        cross_prod = abs(vx * ay - vy * ax)
        curvature = cross_prod / (speed**3)
        
        # 3. Potential Weighting (The Delta Proxy)
        # Higher potential = closer to instability = more important twist
        V = abs(self.hypernet.get_potential_energy(m, lam))
        
        # 4. Knottedness
        K = V * curvature
        
        # Clamp artifacts
        return min(K, 100.0)

    def get_action_data(self, obs, t_step):
        cm, cl, rm, rl, tilt, freq, phase = self.params
        
        # Orbit Logic
        angle = phase + (t_step * 0.02 * freq * 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(tilt), np.sin(tilt)
        
        m = cm + (rm * cos_a * cos_t - rl * sin_a * sin_t)
        lam = cl + (rm * cos_a * sin_t + rl * sin_a * cos_t)
        
        # Compute K
        k_val = self.calculate_instant_knottedness(m, lam)
        
        # Generate Physics
        weights, color = self.hypernet.generate_weights(m, lam)
        W = weights.reshape(self.act_dim, self.obs_dim)
        
        return np.tanh(W @ obs), color, k_val, (m, lam)

# ============================================================
# 3. TOPOLOGICAL SEARCH
# ============================================================

class TopologicalSearch:
    def __init__(self, env_name):
        self.env_name = env_name
        
    def evaluate_topology(self, gene, render=False):
        agent = KnottedOrbitAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        total_reward = 0
        total_K = 0.0 # Accumulated Knottedness
        steps = 0
        
        while steps < 500:
            action, color, k_val, _ = agent.get_action_data(obs, steps)
            obs, r, term, trunc, _ = env.step(action)
            
            total_reward += r
            total_K += k_val
            
            # if render and k_val > 10.0:
            #     print(f"   Frame {steps}: HIGH KNOT ({k_val:.1f}) in {color} Basin")
            
            steps += 1
            if term or trunc:
                if steps < 50: total_reward = -100
                break
        env.close()
        
        # FITNESS FUNCTION
        # Survival + (Knottedness * Scale)
        # We explicitly reward the agent for taking a 'Twisted' path through phase space.
        fitness = total_reward + (total_K * 0.5)
        
        return fitness, total_reward, total_K

    def evolve(self):
        print(f"🌀 TOPOLOGICAL ORBIT SEARCH: {self.env_name}")
        print("   Seeking High-Knottedness Trajectories (The Braid)...")
        
        # Gene: [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        population = []
        for _ in range(30):
            gene = np.array([
                np.random.normal(0, 0.2), np.random.normal(0, 0.2), 
                np.random.uniform(0.5, 1.2), np.random.uniform(0.5, 1.2),
                np.random.uniform(0, np.pi), np.random.uniform(0.5, 1.5),
                np.random.uniform(0, 2*np.pi)
            ])
            population.append(gene)
        population = np.array(population)
        
        best_fit = -float('inf')
        best_gene = None
        
        for gen in range(15):
            scores = []
            
            for gene in population:
                # Anti-Collapse Constraint
                gene[2] = max(0.5, gene[2])
                gene[3] = max(0.5, gene[3])
                
                fit, raw, k_score = self.evaluate_topology(gene)
                scores.append(fit)
                
                if fit > best_fit:
                    best_fit = fit
                    best_gene = gene.copy()
                    print(f"   [Gen {gen}] New Topology: Fit={fit:.0f} (Raw={raw:.0f} + Knot={k_score:.0f})")
            
            # Selection
            elites = population[np.argsort(scores)[-5:]]
            
            # Mutation
            new_pop = []
            for _ in range(30):
                parent = elites[np.random.randint(len(elites))].copy()
                noise = np.random.normal(0, 0.05, size=7)
                child = parent + noise
                new_pop.append(child)
            population = np.array(new_pop)
            
            if best_fit > 1000: # High threshold because K adds up
                print("   > Highly Knotted Solution Found.")
                break
                
        print(f"✨ EVOLUTION COMPLETE. Best Fitness: {best_fit:.1f}")
        return best_gene

if __name__ == "__main__":
    try:
        searcher = TopologicalSearch("BipedalWalker-v3")
        best_knot = searcher.evolve()
        
        print("\nVisualizing the Braid...")
        searcher.evaluate_topology(best_knot, render=True)
    except Exception as e:
        print(f"Error: {e}")