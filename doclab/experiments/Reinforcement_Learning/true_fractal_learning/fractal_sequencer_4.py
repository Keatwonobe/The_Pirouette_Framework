import gymnasium as gym
import numpy as np
import time

# --- 1. THE FRACTAL ENGINE (Standard Robust) ---
class FractalHypernet:
    def __init__(self, output_dim):
        self.output_dim = output_dim
        
    def generate_weights(self, m, lam):
        weights = []
        p_m, p_l = 0.0, 0.0
        sigma, dt = 1.0, 0.1
        curr_m, curr_l = m, lam
        ESCAPE = 10.0
        
        # Color Detector for Visualization
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

# --- 2. THE SLINGSHOT TRAJECTORY ---
class EllipticalGait:
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
        
        # Engine
        dummy = gym.make(env_name)
        self.obs_dim = dummy.observation_space.shape[0]
        self.act_dim = dummy.action_space.shape[0]
        self.hypernet = FractalHypernet(self.obs_dim * self.act_dim)
        dummy.close()
        
    def get_action(self, obs, t_step):
        # 1. The Clock (Time -> Angle)
        # 50 FPS assumption
        angle = self.phase + (t_step * 0.02 * self.freq * 2 * np.pi)
        
        # 2. The Geometry (Angle -> Coordinate)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cos_t, sin_t = np.cos(self.tilt), np.sin(self.tilt)
        
        # Parametric Ellipse Rotation
        m = self.center_m + (self.radius_m * cos_a * cos_t - self.radius_l * sin_a * sin_t)
        lam = self.center_l + (self.radius_m * cos_a * sin_t + self.radius_l * sin_a * cos_t)
        
        # 3. The Fractal (Coordinate -> Weights)
        weights, color = self.hypernet.generate_weights(m, lam)
        W = weights.reshape(self.act_dim, self.obs_dim)
        
        # 4. The Action (Weights -> Motors)
        return np.tanh(W @ obs), color, (m, lam)

# --- 3. THE INDUCER (Fitness Function) ---
class GaitInducer:
    def __init__(self, env_name):
        self.env_name = env_name
        
    def evaluate_gait(self, params, render=False):
        agent = EllipticalGait(self.env_name, params)
        env = gym.make(self.env_name, render_mode="human" if render else None)
        obs, _ = env.reset()
        
        total_reward = 0
        forward_velocity_bonus = 0
        steps = 0
        
        last_color = ""
        basin_crossings = 0
        
        while steps < 450:
            action, color, coords = agent.get_action(obs, steps)
            obs, r, term, trunc, _ = env.step(action)
            
            # Behavior Shaping
            total_reward += r
            forward_velocity_bonus += obs[2] 
            
            if color != last_color and steps > 0:
                basin_crossings += 1
                if render: print(f"   Frame {steps}: Crossed into {color}")
            last_color = color
            
            steps += 1
            if term or trunc:
                if steps < 50: total_reward = -100 # Punish instant death
                break
        
        env.close()
        
        # Fitness: Survival + Speed + Complexity
        fitness = total_reward + (forward_velocity_bonus * 5.0) + (basin_crossings * 2.0)
        return fitness

    def optimize(self):
        print(f"📐 FRACTAL GAIT INDUCER: {self.env_name}")
        print("   Forcing Large-Scale Manifold Traversal...")
        
        # Gene Structure: [Cm, Cl, Rm, Rl, Tilt, Freq, Phase]
        population = []
        for _ in range(25):
            gene = [
                np.random.normal(-0.2, 0.1), # Center M
                np.random.normal(-0.2, 0.1), # Center L
                np.random.uniform(0.4, 0.8), # Radius M
                np.random.uniform(0.4, 0.8), # Radius L
                np.random.uniform(0, np.pi), # Tilt
                np.random.uniform(0.5, 1.5), # Freq
                np.random.uniform(0, 2*np.pi)# Phase
            ]
            population.append(gene)
            
        # FIX: Convert to numpy array BEFORE the loop starts
        population = np.array(population)
            
        best_fit = -float('inf')
        best_gene = None
        
        for gen in range(15):
            scores = []
            for i, gene in enumerate(population):
                # Clamp Radii
                gene[2] = max(0.4, gene[2]) 
                gene[3] = max(0.4, gene[3])
                
                fit = self.evaluate_gait(gene)
                scores.append(fit)
                
                if fit > best_fit:
                    best_fit = fit
                    best_gene = gene.copy()
                    print(f"   [Gen {gen}] New Gait: Vel Bonus={fit:.1f} | Freq={gene[5]:.2f}Hz")
            
            # Elite Selection (Now works because population is numpy array)
            elites = population[np.argsort(scores)[-5:]]
            
            # Mutation
            new_pop = []
            for _ in range(25):
                parent = elites[np.random.randint(len(elites))].copy()
                noise = np.random.normal(0, 0.05, size=7)
                child = parent + noise
                new_pop.append(child)
            population = np.array(new_pop)
            
            if best_fit > 300: 
                print("   > High Velocity Gait Achieved.")
                break

        print(f"✨ GAIT INDUCED. Best Fitness: {best_fit:.1f}")
        return best_gene

if __name__ == "__main__":
    try:
        inducer = GaitInducer("BipedalWalker-v3")
        best_gait = inducer.optimize()
        
        print("\nVisualizing the Induced Stride...")
        inducer.evaluate_gait(best_gait, render=True)
    except Exception as e:
        print(f"Error: {e}")