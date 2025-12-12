import gymnasium as gym
import numpy as np
import time
from collections import deque
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("BICAMERAL_WALKER")

# --- PHYSICS CONSTANTS ---
TWIST = 3.8
NUM_PARTICLES = 3 
# Gene: [cx, cy, rx, ry, tilt, freq, phase] * 3 particles = 21 params
GENE_LEN = NUM_PARTICLES * 7 

# ============================================================
# 1. KAPPA-HYPERFILTER (The Resonator)
# ============================================================
# This calculates how "resonant" a given internal state is.
# High Score = Purple Zone (Calm). Low Score = Yellow Zone (Chaos).

class KappaHyperfilter:
    def get_fractal_force_vector(self, m, lam):
        # Wada/Basin Physics
        F_teal_m = -(m + 0.866) 
        F_teal_lam = -(lam - 0.5)
        F_red_m = -(m - 0.0)
        p_violation = TWIST * np.sin(m * 2.5) 
        F_red_lam = -(lam + 1.0) + p_violation
        sum_m = (F_teal_m + F_red_m)
        sum_lam = (F_teal_lam + F_red_lam)
        
        # Structure Tensor
        magnitude = np.sqrt(sum_m**2 + sum_lam**2)
        scaling_factor = np.sqrt(magnitude)
        F_gold_m = sum_m * scaling_factor
        F_gold_lam = sum_lam * scaling_factor
        
        # Angular Weights (The Basins)
        angle = np.degrees(np.arctan2(lam, m)) % 360
        def gaussian(x, mu, sig): return np.exp(-((x-mu)/sig)**2)
        
        # 3 Basins: 30, 150, 270 degrees
        w_gold = gaussian(min(abs(angle-30), 360-abs(angle-30)), 0, 80)
        w_teal = gaussian(min(abs(angle-150), 360-abs(angle-150)), 0, 80)
        w_red  = gaussian(min(abs(angle-270), 360-abs(angle-270)), 0, 80)
        
        tot = w_gold + w_teal + w_red + 1e-6
        return w_red/tot, w_teal/tot, w_gold/tot

    def sample_filters(self, m, lam):
        # Returns: Resonance Score (kP), Dominant Color
        nw_red, nw_teal, nw_gold = self.get_fractal_force_vector(m, lam)
        
        # Metrics derived from geometry
        coherence = (nw_teal + nw_gold) / (nw_red + 1e-6)
        
        # kP: The Kappa Potential. 
        # > 0.5: Stable/Resonant (Purple Zone)
        # < 0.0: Chaotic/Dissonant (Yellow Zone)
        kP = np.tanh(coherence - 1.0) 
        
        if nw_teal > nw_red and nw_teal > nw_gold: color = "Teal"
        elif nw_red > nw_teal and nw_red > nw_gold: color = "Red"
        else: color = "Gold"

        return kP, color

# ============================================================
# 2. FRACTAL HYPERNET (The Brain)
# ============================================================
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        self.filter = KappaHyperfilter()
        
    def generate_weights(self, m, lam):
        # Generates Neural Weights from Fractal Coordinates
        weights = []
        curr_m, curr_l = m, lam
        sigma, dt = 1.0, 0.1
        
        # Deterministic Chaos Expansion (The Hash Function of Reality)
        while len(weights) < self.output_dim:
            # Physics Step
            grad_m = curr_m + 2 * sigma * curr_m * curr_l
            grad_l = curr_l + sigma * (curr_m**2 - curr_l**2)
            curr_m += dt * grad_m
            curr_l += dt * grad_l
            
            # Map to [-1, 1] weight space
            weights.append(np.tanh(curr_m))
            weights.append(np.tanh(curr_l))
            
            # Containment
            if curr_m**2 + curr_l**2 > 16:
                curr_m *= 0.1; curr_l *= 0.1
                
        return np.array(weights[:self.output_dim], dtype=np.float32)

# ============================================================
# 3. BICAMERAL AGENT (The Walker)
# ============================================================
class BicameralAgent:
    def __init__(self, env_name, gene):
        self.gene = gene
        dummy = gym.make(env_name)
        self.act_dim = dummy.action_space.shape[0]
        self.obs_dim = dummy.observation_space.shape[0]
        self.hypernet = FractalHypernet(self.act_dim * self.obs_dim)
        dummy.close()
        
        # Internal State for the "Basin Spring"
        self.internal_clock = 0.0
        self.stress_accumulator = 0.0
        self.basin_jump_counter = 0
        
        # Dynamic Modifiers (The "Dream" Parameters)
        self.phase_offsets = np.zeros(NUM_PARTICLES)
        self.reality_warp = 1.0 # Standard physics

    def get_action_data(self, obs):
        # 1. Update Internal Clock based on Stress
        # If stress is high, we think FASTER (Time Dilation)
        # Low Stress (Calm) -> dt = 0.05
        # High Stress (Panic) -> dt = 0.20
        dt = 0.05 + (0.15 * np.clip(self.stress_accumulator, 0, 1))
        self.internal_clock += dt
        
        m_list, lam_list = [], []
        
        # 2. Evolve Particles
        for i in range(NUM_PARTICLES):
            g = self.gene[i*7 : (i+1)*7]
            cm, cl, rm, rl, tilt, freq, phase = g
            
            # Apply Phase Offsets (from previous Basin Jumps)
            eff_phase = phase + self.phase_offsets[i]
            
            # Calculate Orbit
            angle = eff_phase + (self.internal_clock * 0.1 * freq)
            
            # Apply Reality Warp (Dream Mode distorts space)
            rm_eff = rm * self.reality_warp
            rl_eff = rl * self.reality_warp
            
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            cos_t, sin_t = np.cos(tilt), np.sin(tilt)
            
            m = cm + (rm_eff * cos_a * cos_t - rl_eff * sin_a * sin_t)
            lam = cl + (rm_eff * cos_a * sin_t + rl_eff * sin_a * cos_t)
            
            m_list.append(m)
            lam_list.append(lam)

        # 3. Assess Resonance (The "Purple vs Yellow" check)
        # We check the resonance of the "Body" particle (P0)
        kP_body, basin_color = self.hypernet.filter.sample_filters(m_list[0], lam_list[0])
        
        # 4. The Bicameral Switch
        if kP_body > 0.3:
            # PURPLE ZONE: Logic Mode
            # Decay stress, stabilize reality
            self.stress_accumulator *= 0.95
            self.reality_warp = 1.0 + (1.0 - self.reality_warp) * 0.1 # Return to normal
            mode = "LOGIC"
            
        else:
            # YELLOW ZONE: Dream Mode
            # Accumulate stress
            self.stress_accumulator += 0.05
            mode = "DREAM"
            
            # THE BASIN SPRING: If stress gets too high, SNAP!
            if self.stress_accumulator > 1.0:
                # Trigger Basin Jump
                for i in range(NUM_PARTICLES):
                    # Randomly shift phase by PI/2 or PI
                    shift = np.random.choice([np.pi/2, np.pi, -np.pi/2])
                    self.phase_offsets[i] += shift
                
                # Warp Reality temporarily (Distort the orbit radii)
                self.reality_warp = np.random.uniform(0.5, 2.0)
                
                # Reset Stress
                self.stress_accumulator = 0.0
                self.basin_jump_counter += 1
                mode = "JUMP!"

        # 5. Generate Action
        # Composite point for weights
        m_comp = np.mean(m_list)
        lam_comp = np.mean(lam_list)
        
        weights = self.hypernet.generate_weights(m_comp, lam_comp)
        W = weights.reshape(self.act_dim, self.obs_dim)
        
        action = np.tanh(W @ obs)
        
        return action, mode, kP_body

# ============================================================
# 4. TRAINER
# ============================================================
class BicameralTrainer:
    def __init__(self, env_name, n_heads=4):
        self.env_name = env_name
        self.heads = [self.random_gene() for _ in range(n_heads)]
        self.best_gene = None
        self.best_score = -9999

    def random_gene(self):
        gene = []
        for _ in range(NUM_PARTICLES):
            gene.extend([
                np.random.normal(0, 0.3), np.random.normal(0, 0.3), # Center
                np.random.uniform(0.5, 1.5), np.random.uniform(0.5, 1.5), # Radii
                np.random.uniform(0, np.pi), # Tilt
                np.random.uniform(0.5, 2.0), # Freq
                np.random.uniform(0, 2*np.pi) # Phase
            ])
        return np.array(gene)

    def evaluate(self, gene, render=False):
        agent = BicameralAgent(self.env_name, gene)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        total_reward = 0
        steps = 0
        jumps = 0
        modes = {"LOGIC": 0, "DREAM": 0, "JUMP!": 0}
        
        while steps < 800:
            action, mode, kP = agent.get_action_data(obs)
            obs, reward, term, trunc, _ = env.step(action)
            total_reward += reward
            steps += 1
            
            modes[mode] += 1
            if mode == "JUMP!": jumps += 1
            
            if render:
                # Optional: Slow down render slightly to see movements
                # time.sleep(0.01)
                pass
                
            if term or trunc: break
            
        env.close()
        return total_reward, jumps, modes

    def run(self, generations=10):
        print(f"[-] Initializing Bicameral Trainer ({self.env_name})...")
        
        for g in range(generations):
            print(f"\nGeneration {g}:")
            gen_best_score = -9999
            
            for i, gene in enumerate(self.heads):
                score, jumps, modes = self.evaluate(gene)
                
                # Logging
                dream_ratio = modes['DREAM'] / (modes['LOGIC'] + modes['DREAM'] + 1)
                print(f"  Agent {i}: Score {score:6.1f} | Jumps {jumps} | Dream Ratio {dream_ratio:.2f}")
                
                if score > gen_best_score:
                    gen_best_score = score
                    # Elitism: Keep best
                    if score > self.best_score:
                        self.best_score = score
                        self.best_gene = gene.copy()
                        print(f"    >>> NEW RECORD: {self.best_score:.1f}")

                # Mutation (Evolution)
                # If the agent spent too much time dreaming (Chaos), mutate heavily
                mut_scale = 0.05 if dream_ratio < 0.3 else 0.2
                noise = np.random.normal(0, mut_scale, size=GENE_LEN)
                self.heads[i] = self.heads[i] * 0.9 + self.best_gene * 0.1 + noise # Pull to best + explore

        return self.best_gene

if __name__ == "__main__":
    trainer = BicameralTrainer("BipedalWalker-v3", n_heads=4)
    best_gene = trainer.run(generations=15)
    
    print("\n[-] Visualizing Best Bicameral Walker...")
    # Run visualization
    trainer.evaluate(best_gene, render=True)