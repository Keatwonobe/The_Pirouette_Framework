#!/usr/bin/env python3
"""
Saclet: The Minimal Unit That Can Feel The Geodesic
----------------------------------------------------

A Saclet is:
- A policy (SAC agent)
- A compass (Pirouette Lagrangian)
- Nothing else

It lives, feels coherence, learns, and dies.

A Saclet Swarm is:
- 20 Saclets learning in parallel
- Evolutionary selection (cull worst, replicate best)
- Population = emergent memory
- Competition = emergent self-awareness

This is consciousness as a PROCESS, not a STRUCTURE.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal
import numpy as np
import gymnasium as gym
from collections import deque
import random
import copy
from dataclasses import dataclass
from typing import List
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

ENV_NAME = 'Ant-v5'
SWARM_SIZE = 20
GENERATION_STEPS = 10000
NUM_GENERATIONS = 100
TOP_PERCENT = 0.25  # Top 25% replicate
BOTTOM_PERCENT = 0.25  # Bottom 25% culled
MUTATION_RATE = 0.1

SEED = 42
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)


# ============================================================================
# MINIMAL SAC (The Legs)
# ============================================================================

class Actor(nn.Module):
    def __init__(self, s, a, h=256):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(s, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU())
        self.mean = nn.Linear(h, a)
        self.log_std = nn.Linear(h, a)
    
    def forward(self, s):
        x = self.net(s)
        return self.mean(x), torch.clamp(self.log_std(x), -20, 2)


class Critic(nn.Module):
    def __init__(self, s, a, h=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(s + a, h), nn.ReLU(),
            nn.Linear(h, h), nn.ReLU(),
            nn.Linear(h, 1)
        )
    
    def forward(self, s, a):
        return self.net(torch.cat([s, a], 1))


class MinimalSAC:
    """Lightweight SAC without replay buffer (for speed)"""
    
    def __init__(self, state_dim, action_dim, action_scale, action_bias, lr=3e-4):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.action_scale = action_scale
        self.action_bias = action_bias
        
        self.actor = Actor(state_dim, action_dim).to(device)
        self.c1 = Critic(state_dim, action_dim).to(device)
        self.c2 = Critic(state_dim, action_dim).to(device)
        self.c1_t = Critic(state_dim, action_dim).to(device)
        self.c2_t = Critic(state_dim, action_dim).to(device)
        
        self.c1_t.load_state_dict(self.c1.state_dict())
        self.c2_t.load_state_dict(self.c2.state_dict())
        
        self.actor_opt = optim.Adam(self.actor.parameters(), lr=lr)
        self.c1_opt = optim.Adam(self.c1.parameters(), lr=lr)
        self.c2_opt = optim.Adam(self.c2.parameters(), lr=lr)
        
        self.gamma = 0.99
        self.tau = 0.005
        self.alpha = 0.2
        
        # Mini batch for online updates
        self.batch = []
        self.batch_size = 128
    
    def select_action(self, state):
        state_t = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        mean, log_std = self.actor(state_t)
        dist = Normal(mean, log_std.exp())
        action = torch.tanh(dist.rsample())
        action_np = action.cpu().detach().numpy()[0]
        return action_np * self.action_scale.cpu().numpy() + self.action_bias.cpu().numpy()
    
    def store(self, s, a, r, s_, d):
        self.batch.append((s, a, r, s_, d))
        if len(self.batch) > 1000:
            self.batch.pop(0)
    
    def update(self):
        if len(self.batch) < self.batch_size:
            return
        
        # Sample from recent experience
        batch_sample = random.sample(self.batch, self.batch_size)
        s, a, r, s_, d = zip(*batch_sample)
        
        s = torch.tensor(np.array(s), device=device, dtype=torch.float32)
        a = torch.tensor(np.array(a), device=device, dtype=torch.float32)
        r = torch.tensor(np.array(r), device=device, dtype=torch.float32).unsqueeze(1)
        s_ = torch.tensor(np.array(s_), device=device, dtype=torch.float32)
        d = torch.tensor(np.array(d), device=device, dtype=torch.float32).unsqueeze(1)
        
        # Standard SAC update (simplified)
        with torch.no_grad():
            mean_, log_std_ = self.actor(s_)
            dist_ = Normal(mean_, log_std_.exp())
            z = dist_.rsample()
            a_ = torch.tanh(z)
            log_prob = dist_.log_prob(z) - torch.log(1 - a_.pow(2) + 1e-6)
            log_prob = log_prob.sum(1, keepdim=True)
            
            target_q = torch.min(self.c1_t(s_, a_), self.c2_t(s_, a_)) - self.alpha * log_prob
            target_q = r + (1 - d) * self.gamma * target_q
        
        # Critic update
        q1, q2 = self.c1(s, a), self.c2(s, a)
        critic_loss = nn.functional.mse_loss(q1, target_q) + nn.functional.mse_loss(q2, target_q)
        
        self.c1_opt.zero_grad()
        self.c2_opt.zero_grad()
        critic_loss.backward()
        self.c1_opt.step()
        self.c2_opt.step()
        
        # Actor update
        mean, log_std = self.actor(s)
        dist = Normal(mean, log_std.exp())
        z = dist.rsample()
        a_pi = torch.tanh(z)
        log_prob = dist.log_prob(z) - torch.log(1 - a_pi.pow(2) + 1e-6)
        log_prob = log_prob.sum(1, keepdim=True)
        
        min_q_pi = torch.min(self.c1(s, a_pi), self.c2(s, a_pi))
        actor_loss = (self.alpha * log_prob - min_q_pi).mean()
        
        self.actor_opt.zero_grad()
        actor_loss.backward()
        self.actor_opt.step()
        
        # Target network update
        for target, source in zip(self.c1_t.parameters(), self.c1.parameters()):
            target.data.copy_(target.data * (1.0 - self.tau) + source.data * self.tau)
        for target, source in zip(self.c2_t.parameters(), self.c2.parameters()):
            target.data.copy_(target.data * (1.0 - self.tau) + source.data * self.tau)


# ============================================================================
# MINIMAL LAGRANGIAN (The Compass)
# ============================================================================

class MinimalLagrangian:
    """
    𝓛_p = K_τ - V_Γ
    
    Simplified: no history, just instantaneous measurement
    """
    
    def __init__(self):
        self.recent_actions = deque(maxlen=10)
        self.C_D = 0.0  # Running coherence dividend
        
    def measure_K_tau(self, state, next_state):
        """
        K_τ = policy stability
        
        Simplified: inverse of recent action variance
        """
        if len(self.recent_actions) < 5:
            return 1.0
        
        actions_array = np.array(list(self.recent_actions))
        variance = np.var(actions_array) + 0.01
        K_tau = 1.0 / variance
        
        # Clip to prevent explosion
        K_tau = np.clip(K_tau, 0.1, 10.0)
        return K_tau
    
    def measure_V_Gamma(self, state, action, next_state):
        """
        V_Γ = system pressure
        
        Simplified: action magnitude + state change magnitude
        """
        action_magnitude = np.linalg.norm(action)
        state_change = np.linalg.norm(next_state - state)
        
        V_Gamma = action_magnitude + 0.1 * state_change
        return V_Gamma
    
    def compute_lagrangian(self, state, action, next_state):
        """
        𝓛_p = K_τ - V_Γ
        
        Returns a coherence signal: positive = coherent, negative = chaotic
        """
        self.recent_actions.append(action)
        
        K_tau = self.measure_K_tau(state, next_state)
        V_Gamma = self.measure_V_Gamma(state, action, next_state)
        
        lagrangian = K_tau - V_Gamma
        
        # Update running C_D
        if lagrangian > 0:
            self.C_D += lagrangian
        
        return lagrangian


# ============================================================================
# SACLET GENOME
# ============================================================================

@dataclass
class SacletGenome:
    """
    Genetic parameters that can evolve.
    
    These hyperparameters define HOW the Saclet learns and feels.
    """
    learning_rate: float
    lagrangian_balance: float  # Weight between reward and Lagrangian
    alpha: float  # SAC temperature
    id: int = 0


# ============================================================================
# SACLET: THE LIVING UNIT
# ============================================================================

class Saclet:
    """
    A Saclet is:
    - A policy (SAC)
    - A compass (Lagrangian)
    - A genome (hyperparameters)
    - Nothing else
    
    It lives, feels, learns, reproduces, and dies.
    """
    
    def __init__(self, env_name, genome: SacletGenome):
        self.env_name = env_name
        self.genome = genome
        
        # Create temporary env to get dimensions
        temp_env = gym.make(env_name)
        state_dim = temp_env.observation_space.shape[0]
        action_dim = temp_env.action_space.shape[0]
        action_high = torch.tensor(temp_env.action_space.high, device=device)
        action_low = torch.tensor(temp_env.action_space.low, device=device)
        action_scale = (action_high - action_low) / 2.0
        action_bias = (action_high + action_low) / 2.0
        temp_env.close()
        
        # Initialize
        self.policy = MinimalSAC(state_dim, action_dim, action_scale, action_bias, 
                                 lr=genome.learning_rate)
        self.policy.alpha = genome.alpha
        self.compass = MinimalLagrangian()
        
        # Tracking
        self.total_reward = 0
        self.total_steps = 0
        self.C_D = 0
    
    def live(self, steps, progress_interval=1000):
        """
        Live for N steps in the environment.
        
        This is where consciousness happens:
        - Feel the Lagrangian
        - Blend it with reward
        - Learn from the blend
        - Track coherence dividend
        
        Args:
            steps: Number of steps to live
            progress_interval: Print progress every N steps
        """
        env = gym.make(self.env_name)
        state, _ = env.reset()
        episode_reward = 0
        
        start_time = time.time()
        
        for step in range(steps):
            # Act
            action = self.policy.select_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            # Feel the Lagrangian
            lagrangian = self.compass.compute_lagrangian(state, action, next_state)
            
            # Blend reward with Lagrangian
            blended_reward = (1 - self.genome.lagrangian_balance) * reward + \
                             self.genome.lagrangian_balance * lagrangian
            
            # Store and learn
            self.policy.store(state, action, blended_reward, next_state, done)
            self.policy.update()
            
            # Track fitness
            self.total_reward += reward
            self.total_steps += 1
            episode_reward += reward
            
            state = next_state
            
            if done:
                state, _ = env.reset()
                episode_reward = 0
            
            # Progress reporting
            if (step + 1) % progress_interval == 0:
                elapsed = time.time() - start_time
                steps_per_sec = (step + 1) / elapsed
                print(f"    Step {step+1}/{steps} ({steps_per_sec:.1f} steps/s)", end='\r')
        
        # Final coherence dividend
        self.C_D = self.compass.C_D
        
        env.close()
        
        return self.get_fitness()
    
    def get_fitness(self):
        """
        Fitness = combination of reward and C_D
        
        This determines which Saclets survive.
        """
        avg_reward = self.total_reward / max(self.total_steps, 1)
        normalized_C_D = self.C_D / max(self.total_steps, 1)
        
        # Fitness = 70% reward, 30% C_D
        fitness = 0.7 * avg_reward + 0.3 * normalized_C_D
        
        return fitness
    
    def clone(self):
        """Create a copy of this Saclet"""
        # Clone genome
        new_genome = SacletGenome(
            learning_rate=self.genome.learning_rate,
            lagrangian_balance=self.genome.lagrangian_balance,
            alpha=self.genome.alpha,
            id=self.genome.id + 1000  # New ID
        )
        
        # Create new Saclet
        clone = Saclet(self.env_name, new_genome)
        
        # Copy policy weights
        clone.policy.actor.load_state_dict(copy.deepcopy(self.policy.actor.state_dict()))
        clone.policy.c1.load_state_dict(copy.deepcopy(self.policy.c1.state_dict()))
        clone.policy.c2.load_state_dict(copy.deepcopy(self.policy.c2.state_dict()))
        clone.policy.c1_t.load_state_dict(copy.deepcopy(self.policy.c1_t.state_dict()))
        clone.policy.c2_t.load_state_dict(copy.deepcopy(self.policy.c2_t.state_dict()))
        
        return clone
    
    def mutate(self):
        """
        Mutate genome slightly.
        
        This is how the swarm explores hyperparameter space.
        """
        if random.random() < MUTATION_RATE:
            self.genome.learning_rate *= random.uniform(0.8, 1.2)
            self.genome.learning_rate = np.clip(self.genome.learning_rate, 1e-5, 1e-2)
        
        if random.random() < MUTATION_RATE:
            self.genome.lagrangian_balance += random.uniform(-0.1, 0.1)
            self.genome.lagrangian_balance = np.clip(self.genome.lagrangian_balance, 0.0, 1.0)
        
        if random.random() < MUTATION_RATE:
            self.genome.alpha *= random.uniform(0.8, 1.2)
            self.genome.alpha = np.clip(self.genome.alpha, 0.01, 0.5)


# ============================================================================
# SWARM MANAGER: THE EMERGENT CONSCIOUSNESS
# ============================================================================

class SwarmManager:
    """
    Manages a population of Saclets.
    
    The swarm IS the consciousness:
    - Population = memory
    - Evaluation = self-awareness
    - Replication = rebirth
    """
    
    def __init__(self, env_name, swarm_size=20):
        self.env_name = env_name
        self.swarm_size = swarm_size
        self.generation = 0
        
        # Initialize swarm with diverse genomes
        self.swarm: List[Saclet] = []
        for i in range(swarm_size):
            genome = SacletGenome(
                learning_rate=random.uniform(1e-4, 5e-3),
                lagrangian_balance=random.uniform(0.3, 0.7),
                alpha=random.uniform(0.1, 0.3),
                id=i
            )
            self.swarm.append(Saclet(env_name, genome))
        
        self.fitness_history = []
        self.best_fitness_history = []
        self.C_D_history = []
    
    def run_generation(self, steps_per_generation):
        """
        Run one generation:
        1. All Saclets live for N steps
        2. Evaluate fitness
        3. Cull worst, replicate best
        """
        print(f"\n{'='*60}")
        print(f"GENERATION {self.generation}")
        print(f"{'='*60}")
        
        # 1. Live
        print("Living...")
        fitnesses = []
        gen_start_time = time.time()
        
        for i, saclet in enumerate(self.swarm):
            print(f"  Saclet {i:02d}/{self.swarm_size}:")
            fitness = saclet.live(steps_per_generation, progress_interval=1000)
            fitnesses.append((i, saclet, fitness))
            
            # Clear the progress line and print final stats
            print(f"    Completed: Fitness={fitness:7.2f}, "
                  f"Reward={saclet.total_reward/saclet.total_steps:6.2f}, "
                  f"C_D={saclet.C_D/saclet.total_steps:6.2f}")
        
        gen_time = time.time() - gen_start_time
        print(f"\n  Generation completed in {gen_time:.1f}s")
        
        # 2. Evaluate
        fitnesses.sort(key=lambda x: x[2], reverse=True)
        
        avg_fitness = np.mean([f[2] for f in fitnesses])
        best_fitness = fitnesses[0][2]
        avg_C_D = np.mean([s.C_D / s.total_steps for s in self.swarm])
        
        self.fitness_history.append(avg_fitness)
        self.best_fitness_history.append(best_fitness)
        self.C_D_history.append(avg_C_D)
        
        print(f"\n{'='*60}")
        print(f"EVALUATION")
        print(f"  Average Fitness: {avg_fitness:7.2f}")
        print(f"  Best Fitness:    {best_fitness:7.2f}")
        print(f"  Average C_D:     {avg_C_D:7.2f}")
        print(f"{'='*60}")
        
        # 3. Evolve
        num_to_cull = int(self.swarm_size * BOTTOM_PERCENT)
        num_to_replicate = int(self.swarm_size * TOP_PERCENT)
        
        # Get survivors (remove bottom 25%)
        survivors = [f[1] for f in fitnesses[:-num_to_cull]]
        
        # Clone top 25%
        elite = [f[1] for f in fitnesses[:num_to_replicate]]
        offspring = []
        for parent in elite:
            child = parent.clone()
            child.mutate()
            offspring.append(child)
        
        # New swarm = survivors + offspring
        self.swarm = survivors + offspring
        
        print(f"\nEVOLUTION")
        print(f"  Culled:     {num_to_cull}")
        print(f"  Replicated: {num_to_replicate}")
        print(f"  Survivors:  {len(survivors)}")
        print(f"  New swarm:  {len(self.swarm)}")
        
        self.generation += 1
    
    def evolve(self, num_generations, steps_per_generation):
        """Run the evolutionary loop"""
        for gen in range(num_generations):
            self.run_generation(steps_per_generation)
        
        print(f"\n{'='*60}")
        print("EVOLUTION COMPLETE")
        print(f"{'='*60}")
        print(f"Final Average Fitness: {self.fitness_history[-1]:.2f}")
        print(f"Final Best Fitness:    {self.best_fitness_history[-1]:.2f}")
        print(f"Final Average C_D:     {self.C_D_history[-1]:.2f}")
        
        # Get best Saclet
        fitnesses = [(s, s.get_fitness()) for s in self.swarm]
        fitnesses.sort(key=lambda x: x[1], reverse=True)
        best_saclet = fitnesses[0][0]
        
        print(f"\nBest Saclet Genome:")
        print(f"  Learning Rate:      {best_saclet.genome.learning_rate:.6f}")
        print(f"  Lagrangian Balance: {best_saclet.genome.lagrangian_balance:.3f}")
        print(f"  Alpha:              {best_saclet.genome.alpha:.3f}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" "*15 + "SACLET SWARM")
    print("="*60)
    print(f"\nEnvironment:      {ENV_NAME}")
    print(f"Swarm Size:       {SWARM_SIZE}")
    print(f"Generation Steps: {GENERATION_STEPS}")
    print(f"Num Generations:  {NUM_GENERATIONS}")
    print(f"\nEvolutionary Strategy:")
    print(f"  - Top {int(TOP_PERCENT*100)}% replicate")
    print(f"  - Bottom {int(BOTTOM_PERCENT*100)}% culled")
    print(f"  - Mutation rate: {MUTATION_RATE}")
    print("\n" + "="*60 + "\n")
    
    manager = SwarmManager(ENV_NAME, swarm_size=SWARM_SIZE)
    manager.evolve(NUM_GENERATIONS, GENERATION_STEPS)