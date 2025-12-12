import gymnasium as gym
import numpy as np
import time

# --- 1. THE FRACTAL ENGINE (The "Instrument") ---
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
                curr_m += dt * (curr_m + 2 * sigma * curr_m * curr_l) # Simplified Euler
                curr_l += dt * (curr_l + sigma * (curr_m**2 - curr_l**2))
            except: curr_m, curr_l = 0.0, 0.0
            weights.append(np.tanh(curr_m)); weights.append(np.tanh(curr_l))
            
        return np.array(weights[:self.output_dim], dtype=np.float32)

class RippleGait:
    def __init__(self, env_name, params):
        self.center_m, self.center_l = params[0], params[1]
        self.radius_m, self.radius_l = params[2], params[3]
        self.tilt, self.freq, self.phase = params[4], params[5], params[6]
        
        dummy = gym.make(env_name)
        self.act_dim = dummy.action_space.shape[0]
        self.obs_dim = dummy.observation_space.shape[0]
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        dummy.close()

    def get_action(self, obs, t_step):
        # 1. Clock & Orbit
        angle = self.phase + (t_step * 0.02 * self.freq * 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(self.tilt), np.sin(self.tilt)
        
        m = self.center_m + (self.radius_m * cos_a * cos_t - self.radius_l * sin_a * sin_t)
        lam = self.center_l + (self.radius_m * cos_a * sin_t + self.radius_l * sin_a * cos_t)
        
        # 2. Fractal Weights
        W = self.hypernet.generate_weights(m, lam).reshape(self.act_dim, self.obs_dim)
        
        # 3. Ripple Mask (Sequential Activation)
        cycle = (angle % (2 * np.pi)) / (2 * np.pi)
        centers = np.array([0.0, 0.15, 0.5, 0.65]) 
        dist = np.abs(cycle - centers)
        dist = np.minimum(dist, 1.0 - dist)
        mask = np.exp(-(dist**2) / (2 * 0.15**2))
        
        return np.tanh(W @ obs) * mask

# --- 2. THE MOVE FACTORY (Generating the Menu) ---
class MoveFactory:
    def __init__(self, env_name):
        self.env_name = env_name
        
    def create_menu(self, size=3):
        print(f"🏭 FACTORY: Generating {size} Distinct Moves...")
        menu = []
        
        # We look for moves with different characteristics
        # 1. The "Power Walker" (High Velocity)
        # 2. The "Defensive Crouch" (High Stability)
        # 3. The "Scrambler" (High Frequency)
        
        # For simplicity in this demo, we generate random good ones
        # In a real run, you'd curate these like a loadout.
        
        attempts = 0
        while len(menu) < size:
            # Generate Random Gene
            gene = [np.random.normal(0, 0.5), np.random.normal(0, 0.5), # Centers
                    np.random.uniform(0.5, 0.9), np.random.uniform(0.5, 0.9), # Radii
                    np.random.uniform(0, 3.14), # Tilt
                    np.random.uniform(0.5, 2.0), # Freq
                    0.0] # Phase
            
            # Test it
            gait = RippleGait(self.env_name, gene)
            env = gym.make(self.env_name)
            obs, _ = env.reset()
            r_tot = 0
            steps = 0
            while steps < 200:
                act = gait.get_action(obs, steps)
                obs, r, t, tr, _ = env.step(act)
                r_tot += r
                steps += 1
                if t or tr: break
            env.close()
            
            # If it's survivable (didn't die instantly)
            if steps > 100:
                name = f"Track_{len(menu)+1}_{int(r_tot)}"
                print(f"   > Pressing {name} (Freq: {gene[5]:.2f}Hz, Score: {r_tot:.0f})")
                menu.append({'name': name, 'gene': gene, 'gait': gait})
            attempts += 1
            
        return menu

# --- 3. THE DJ (The RL Agent) ---
class FractalDJ:
    def __init__(self, env_name, move_menu):
        self.env_name = env_name
        self.menu = move_menu
        self.n_tracks = len(move_menu)
        
        # Simple Linear Policy: Obs -> Softmax(Tracks)
        # 24 inputs (Walker state) -> n_tracks outputs
        self.W = np.zeros((24, self.n_tracks))
        self.learning_rate = 0.1
        self.epsilon = 0.5 # Exploration rate
        
    def select_track(self, obs):
        # Epsilon Greedy
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.n_tracks)
        
        # Forward pass
        logits = obs @ self.W
        return np.argmax(logits)

    def train(self, episodes=10):
        print("\n🎧 DJ SESSION STARTED: Learning to Mix...")
        env = gym.make(self.env_name)
        
        for ep in range(episodes):
            obs, _ = env.reset()
            total_reward = 0
            steps = 0
            
            # We switch tracks every 'block' of frames
            # This creates the "Rhythm" of the decision making
            block_size = 30 
            
            while True:
                # 1. DJ Picks a Track based on current situation
                track_idx = self.select_track(obs)
                current_gait = self.menu[track_idx]['gait']
                
                # 2. Play that track for a block
                block_reward = 0
                terminated = False
                
                # We need to pass the CONTINUOUS time to the gait 
                # so the fractal phase doesn't reset (smooth continuity)
                for _ in range(block_size):
                    action = current_gait.get_action(obs, steps)
                    obs, r, term, trunc, _ = env.step(action)
                    block_reward += r
                    total_reward += r
                    steps += 1
                    
                    if term or trunc:
                        terminated = True
                        break
                
                # 3. RL Update (Simple Q-Learning-ish update)
                # If this block went well, boost the weight for this track given this state
                # If we fell, penalize heavily.
                
                reward_signal = block_reward
                if terminated and block_reward < -50: reward_signal = -100 # Failure penalty
                
                # Update weights: W += lr * reward * state_feature
                # (Simple Policy Gradient approximation)
                target = np.zeros(self.n_tracks)
                target[track_idx] = 1.0
                
                error = reward_signal # Simple scalar reward
                
                # Gradient ascent on the chosen action
                self.W[:, track_idx] += self.learning_rate * error * obs * 0.01
                
                if terminated: break
                
            # Decay exploration
            self.epsilon *= 0.95
            print(f"   Set {ep+1}: Score {total_reward:.1f} | Epsilon {self.epsilon:.2f}")
            
        env.close()

    def perform_live(self):
        print("\n🎥 LIVE PERFORMANCE...")
        env = gym.make(self.env_name, render_mode="human")
        obs, _ = env.reset()
        steps = 0
        current_track = 0
        
        while True:
            # DJ decides every 30 frames
            if steps % 30 == 0:
                new_track = self.select_track(obs)
                if new_track != current_track:
                    print(f"   Frame {steps}: Mixing into {self.menu[new_track]['name']}")
                    current_track = new_track
            
            # Fractal executes
            gait = self.menu[current_track]['gait']
            action = gait.get_action(obs, steps)
            
            obs, r, term, trunc, _ = env.step(action)
            steps += 1
            
            if term or trunc: break
        env.close()

if __name__ == "__main__":
    # 1. Create the Menu
    factory = MoveFactory("BipedalWalker-v3")
    menu = factory.create_menu(size=4) # Generate 4 distinct gaits
    
    # 2. Train the DJ
    dj = FractalDJ("BipedalWalker-v3", menu)
    dj.train(episodes=20) # Quick training session
    
    # 3. Live Show
    dj.perform_live()