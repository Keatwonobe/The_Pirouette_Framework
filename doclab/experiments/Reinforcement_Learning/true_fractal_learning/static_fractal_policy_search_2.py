import gymnasium as gym
import numpy as np
import time

# --- 1. THE FRACTAL ENGINE (ROBUST) ---
class FractalHypernet:
    """
    The 'Left Brain': Generates the physics weights from coordinates.
    Includes the 'Manifold Clamp' to prevent explosions.
    """
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def generate_weights(self, m, lam):
        weights = []
        p_m, p_l = 0.0, 0.0
        sigma, dt = 1.0, 0.1
        curr_m, curr_l = m, lam
        ESCAPE = 10.0
        
        while len(weights) < self.output_dim:
            # Manifold Clamp
            if abs(curr_m) > ESCAPE or abs(curr_l) > ESCAPE:
                curr_m = np.fmod(curr_m, 2.0)
                curr_l = np.fmod(curr_l, 2.0)
                p_m *= 0.1; p_l *= 0.1
            
            try:
                # Symplectic Dynamics
                grad_m = curr_m + 2 * sigma * curr_m * curr_l
                grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
                p_m -= (dt/2) * grad_m
                p_l -= (dt/2) * grad_l
                curr_m += dt * p_m
                curr_l += dt * p_l
                # NaN Guard
                if np.isnan(curr_m): curr_m = 0.0
            except:
                curr_m, curr_l = 0.0, 0.0
                
            weights.append(np.tanh(curr_m))
            weights.append(np.tanh(curr_l))
            
        return np.array(weights[:self.output_dim], dtype=np.float32)

# --- 2. THE RL SELECTOR (RIGHT BRAIN) ---
class RLSelector:
    """
    The 'Right Brain': A simple Policy Gradient agent that selects
    which Fractal Tile to use based on the current state.
    """
    def __init__(self, state_dim, n_tiles, learning_rate=0.01):
        self.n_tiles = n_tiles
        # Simple MLP: State -> Hidden -> Softmax(Tiles)
        self.W1 = np.random.randn(state_dim, 64) * 0.1
        self.b1 = np.zeros(64)
        self.W2 = np.random.randn(64, n_tiles) * 0.1
        self.b2 = np.zeros(n_tiles)
        self.lr = learning_rate
        
        # Memory
        self.saved_log_probs = []
        self.rewards = []

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    def select_tile(self, state):
        # Forward Pass
        h = np.tanh(state @ self.W1 + self.b1)
        logits = h @ self.W2 + self.b2
        probs = self.softmax(logits)
        
        # Sample Action (Tile Index)
        tile_idx = np.random.choice(self.n_tiles, p=probs)
        
        # Save gradients for backprop later
        # (Simplified manual backprop storage)
        d_softmax = probs.copy()
        d_softmax[tile_idx] -= 1 # Gradient of -log(p)
        self.saved_grads = (state, h, d_softmax)
        
        return tile_idx

    def update(self, episode_reward):
        # Very simple REINFORCE-like update (Vanilla Policy Gradient)
        # pushing the weights towards the tiles chosen in a successful run
        state, h, d_softmax = self.saved_grads
        
        # If reward is bad, push AWAY from these choices. If good, push TOWARD.
        # Normalize reward proxy
        signal = np.clip(episode_reward, -10, 10) 
        
        # Backprop (Manual for Numpy speed/compatibility)
        grad_W2 = np.outer(h, d_softmax) * signal
        grad_b2 = d_softmax * signal
        
        grad_h = d_softmax @ self.W2.T * (1 - h**2) # tanh derivative
        grad_W1 = np.outer(state, grad_h) * signal
        grad_b1 = grad_h * signal
        
        # Ascent
        self.W2 -= self.lr * grad_W2
        self.b2 -= self.lr * grad_b2
        self.W1 -= self.lr * grad_W1
        self.b1 -= self.lr * grad_b1

# --- 3. THE HYBRID MANAGER ---
class FractalHybridSystem:
    def __init__(self, env_name):
        self.env = gym.make(env_name)
        self.obs_dim = self.env.observation_space.shape[0]
        self.act_dim = self.env.action_space.shape[0]
        
        # Fractal Setup
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        
        # Grid Setup (4x4 = 16 Tiles)
        self.grid_size = 4
        self.n_tiles = self.grid_size * self.grid_size
        self.tiles = [] # Stores (m, lambda, WeightMatrix)
        
        # RL Agent
        self.agent = RLSelector(self.obs_dim, self.n_tiles)

    def generate_tile_grid(self, center_m, center_l, radius):
        """Creates the 'Deck' of static policies"""
        self.tiles = []
        m_vals = np.linspace(center_m - radius, center_m + radius, self.grid_size)
        l_vals = np.linspace(center_l - radius, center_l + radius, self.grid_size)
        
        print(f"   Generative Grid: {self.grid_size}x{self.grid_size} centered at ({center_m:.2f}, {center_l:.2f})")
        
        for m in m_vals:
            for lam in l_vals:
                # Generate the static weights for this coordinate
                raw_weights = self.hypernet.generate_weights(m, lam)
                W = raw_weights.reshape(self.act_dim, self.obs_dim)
                self.tiles.append({
                    'coords': (m, lam),
                    'weights': W,
                    'usage': 0,
                    'total_reward': 0
                })

    def run_training_round(self, episodes=5):
        """
        Runs a batch of episodes where RL chooses tiles dynamically.
        """
        round_reward = 0
        best_episode = -float('inf')
        
        for ep in range(episodes):
            obs, _ = self.env.reset()
            ep_reward = 0
            steps = 0
            
            # Episode Loop
            while steps < 500: # Max steps
                # 1. RL Selects a Tile
                tile_idx = self.agent.select_tile(obs)
                tile = self.tiles[tile_idx]
                
                # 2. Fractal Tile drives the motors
                # Action = Weights * Obs
                action = np.tanh(tile['weights'] @ obs)
                
                # 3. Step
                obs, reward, terminated, truncated, _ = self.env.step(action)
                ep_reward += reward
                steps += 1
                
                # Stats
                tile['usage'] += 1
                tile['total_reward'] += reward
                
                if terminated or truncated:
                    # RL Update (Per episode for simplicity here)
                    self.agent.update(ep_reward)
                    break
            
            round_reward += ep_reward
            best_episode = max(best_episode, ep_reward)
            
        return round_reward / episodes, best_episode

    def train_and_zoom(self, rounds=3):
        print(f"🧠 INITIALIZING HYBRID BRAIN: {self.env.spec.id}")
        
        # Initial Global Scan
        current_m, current_l = 0.0, 0.0
        current_radius = 1.5
        
        for r in range(rounds):
            print(f"\n--- Round {r+1}: The Zoom ---")
            
            # 1. Generate New Tiles (The Manifold Observation)
            self.generate_tile_grid(current_m, current_l, current_radius)
            
            # 2. Train RL on these Tiles (The Game)
            print("   RL Agent learning to play the tiles...")
            avg_score, best_score = self.run_training_round(episodes=10)
            
            print(f"   Performance: Avg {avg_score:.1f} | Best {best_score:.1f}")
            
            # 3. Analyze & Zoom
            # Find the tile that provided the most value
            best_tile = max(self.tiles, key=lambda t: t['total_reward'] / (t['usage'] + 1))
            
            new_m, new_l = best_tile['coords']
            print(f"   MVP Tile Found at ({new_m:.3f}, {new_l:.3f})")
            print(f"   > Zooming in...")
            
            # Update center and shrink radius
            current_m, current_l = new_m, new_l
            current_radius *= 0.4 # Zoom factor
            
            # (Optional) Reset RL weights? 
            # We keep them. The RL adapts to the new "finer" options.
            
        print("\n🏆 TRAINING COMPLETE")
        print(f"Final Focus: m={current_m:.4f}, λ={current_l:.4f}")
        return current_m, current_l

    def visualize(self, m, lam):
        print("\n🎥 Visualizing Final Manifold Point...")
        env = gym.make(self.env.spec.id, render_mode="human")
        
        # For viz, we just use the single best point found
        # (Or we could run the RL agent, but let's see the 'Center' performance)
        weights = self.hypernet.generate_weights(m, lam)
        W = weights.reshape(self.act_dim, self.obs_dim)
        
        obs, _ = env.reset()
        total = 0
        while True:
            action = np.tanh(W @ obs)
            obs, r, t, tr, _ = env.step(action)
            total += r
            if t or tr:
                print(f"Final Score: {total:.1f}")
                break
        env.close()

if __name__ == "__main__":
    # Run the Hybrid System on Walker
    try:
        system = FractalHybridSystem("BipedalWalker-v3")
        best_m, best_l = system.train_and_zoom(rounds=240)
        system.visualize(best_m, best_l)
    except Exception as e:
        print(f"Error: {e}")