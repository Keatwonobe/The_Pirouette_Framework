import gymnasium as gym
import numpy as np
import time

# --- 1. THE FRACTAL CORE & ORCHESTRA (Reused) ---
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
    def generate_weights(self, m, lam):
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt, ESCAPE = 1.0, 0.1, 10.0
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
        return np.array(weights[:self.output_dim], dtype=np.float32)

class PolicyOrchestra:
    def __init__(self, env_name, size=50):
        self.env_name = env_name
        dummy = gym.make(env_name)
        self.obs_dim = dummy.observation_space.shape[0]
        self.act_dim = dummy.action_space.shape[0]
        dummy.close()
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        self.models = []
        print(f"🎻 TUNING ORCHESTRA: Generating {size} Fractal Models...")
        for i in range(size):
            radius = np.sqrt(i / size) * 1.5
            angle = np.pi * (3 - np.sqrt(5)) * i * 10.0
            m, l = radius * np.cos(angle), radius * np.sin(angle)
            W = self.hypernet.generate_weights(m, l).reshape(self.act_dim, self.obs_dim)
            self.models.append({'id': i, 'coords': np.array([m, l]), 'W': W})
    def get_nearest_model(self, m, l):
        query = np.array([m, l])
        best_dist = float('inf')
        best_model = None
        for model in self.models:
            dist = np.linalg.norm(model['coords'] - query)
            if dist < best_dist: best_dist = dist; best_model = model
        return best_model

class FractalConductor:
    def __init__(self, orchestra, params):
        self.orchestra = orchestra
        self.center_m, self.center_l = params[0], params[1]
        self.radius_m, self.radius_l = params[2], params[3]
        self.tilt, self.freq, self.phase = params[4], params[5], params[6]
    def get_action(self, obs, t_step):
        angle = self.phase + (t_step * 0.02 * self.freq * 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(self.tilt), np.sin(self.tilt)
        curr_m = self.center_m + (self.radius_m * cos_a * cos_t - self.radius_l * sin_a * sin_t)
        curr_l = self.center_l + (self.radius_m * cos_a * sin_t + self.radius_l * sin_a * cos_t)
        model = self.orchestra.get_nearest_model(curr_m, curr_l)
        return np.tanh(model['W'] @ obs), model['id'], (curr_m, curr_l)

# --- 2. THE NOVELTY ARCHIVE (The Memory) ---
class NoveltyArchive:
    """
    Stores the history of orbits to determine 'Newness'.
    Manages the 'Trimming' of the beard.
    """
    def __init__(self, max_size=50):
        self.archive = [] # List of {'gene': np.array, 'score': float}
        self.max_size = max_size
        
    def calculate_novelty(self, gene):
        """
        Returns the distance to the NEAREST neighbor in the archive.
        High distance = Very Novel (Crowd Cheers!)
        Low distance = Heard it before (Boring)
        """
        if len(self.archive) == 0:
            return 10.0 # First song is always novel
            
        distances = []
        for entry in self.archive:
            # gene is 7D, so we look at Euclidean distance in Gene Space
            d = np.linalg.norm(entry['gene'] - gene)
            distances.append(d)
        
        # We only care about how close we are to the *nearest* known song
        nearest_dist = min(distances)
        return nearest_dist

    def add_to_archive(self, gene, score):
        self.archive.append({'gene': gene.copy(), 'score': score})
        
        # TRIM THE BEARD
        # If too big, remove the one that is 'Least Valuable'
        # (Low Score AND Low Novelty compared to others)
        if len(self.archive) > self.max_size:
            # Sort by Score (Keep the Hits)
            self.archive.sort(key=lambda x: x['score'], reverse=True)
            # Remove the worst performing track
            removed = self.archive.pop()
            # return True

# --- 3. THE EXPLORER DJ (The Agent) ---
class FractalExplorerDJ:
    def __init__(self, env_name):
        self.env_name = env_name
        self.orchestra = PolicyOrchestra(env_name, size=50)
        self.archive = NoveltyArchive(max_size=30)
        self.hall_of_fame_best = -float('inf')
        self.best_gene = None

    def evaluate_track(self, gene, render=False):
        conductor = FractalConductor(self.orchestra, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        total_reward = 0
        steps = 0
        
        while steps < 500:
            action, _, _ = conductor.get_action(obs, steps)
            obs, r, term, trunc, _ = env.step(action)
            total_reward += r
            steps += 1
            if term or trunc:
                if steps < 50: total_reward = -100
                break
        env.close()
        return total_reward

    def spin_records(self):
        print(f"\n🎧 FRACTAL EXPLORER: {self.env_name}")
        print("   Incentivizing: Survival (Score) + Originality (Novelty)")
        
        # Init Population
        population = []
        for _ in range(20):
            gene = np.array([
                np.random.normal(0, 0.2), np.random.normal(0, 0.2), # Center
                np.random.uniform(0.5, 1.2), np.random.uniform(0.5, 1.2), # Radius
                np.random.uniform(0, np.pi), np.random.uniform(0.2, 1.5), # Tilt/Freq
                np.random.uniform(0, 2*np.pi)
            ])
            population.append(gene)
        population = np.array(population)

        # Main Loop
        for session in range(20):
            print(f"\n--- Session {session+1}: Mixing New Tracks ---")
            
            evaluated_pop = []
            
            for gene in population:
                # 1. Check the Vibe (Reward)
                raw_score = self.evaluate_track(gene)
                
                # 2. Check the Crowd (Novelty)
                novelty_bonus = self.archive.calculate_novelty(gene) * 20.0 # Scale factor
                
                # 3. Total Appeal
                # We blend them. A terrible song (score -100) needs MASSIVE novelty to survive.
                total_fitness = raw_score + novelty_bonus
                
                evaluated_pop.append({
                    'gene': gene,
                    'raw': raw_score,
                    'novelty': novelty_bonus,
                    'fit': total_fitness
                })
                
                # 4. Update Hall of Fame (Pure Meritocracy)
                if raw_score > self.hall_of_fame_best:
                    self.hall_of_fame_best = raw_score
                    self.best_gene = gene.copy()
                    print(f"   🏆 NEW HIGH SCORE: {raw_score:.1f} (Novelty: {novelty_bonus:.1f})")

            # Sort by Fitness (Score + Novelty)
            evaluated_pop.sort(key=lambda x: x['fit'], reverse=True)
            
            # Print the Top of the Charts
            top = evaluated_pop[0]
            print(f"   Chart Topper: Score {top['raw']:.0f} + Novelty {top['novelty']:.1f} = {top['fit']:.1f}")
            if top['novelty'] > 15.0:
                print("   > The crowd goes wild! A brand new sound!")
            
            # Update Archive with the winners of this generation
            for i in range(5):
                winner = evaluated_pop[i]
                # Only archive if it's somewhat viable (-50 cutoff)
                if winner['raw'] > -50:
                    self.archive.add_to_archive(winner['gene'], winner['raw'])
            
            # Evolution (Selection + Mutation)
            new_pop = []
            # Elitism: Keep Top 3
            for i in range(3):
                new_pop.append(evaluated_pop[i]['gene'])
                
            # Crossover/Mutation from Archive (Experience) + Current Elites
            while len(new_pop) < 20:
                # 50% chance to remix a classic hit from the archive
                if len(self.archive.archive) > 0 and np.random.rand() < 0.5:
                    parent_idx = np.random.randint(len(self.archive.archive))
                    parent = self.archive.archive[parent_idx]['gene'].copy()
                else:
                    # 50% chance to remix a current hit
                    parent = evaluated_pop[np.random.randint(5)]['gene'].copy()
                
                # Mutate
                noise = np.random.normal(0, 0.1, size=7)
                child = parent + noise
                new_pop.append(child)
                
            population = np.array(new_pop)
            
            if self.hall_of_fame_best > 300:
                print("   > Platinum Record Achieved.")
                break

        print(f"✨ SESSION COMPLETE. Best Raw Score: {self.hall_of_fame_best:.1f}")
        return self.best_gene

if __name__ == "__main__":
    try:
        dj = FractalExplorerDJ("BipedalWalker-v3")
        best_track = dj.spin_records()
        
        print("\nVisualizing the Platinum Hit...")
        dj.evaluate_track(best_track, render=True)
    except Exception as e:
        print(f"Error: {e}")