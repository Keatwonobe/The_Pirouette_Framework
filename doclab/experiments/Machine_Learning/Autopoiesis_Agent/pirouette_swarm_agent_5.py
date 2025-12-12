#!/usr/bin/env python3
"""
Saclet v4: PARALLELIZED Predictive Coherence with Helical Variational Structure

NEW: Multi-threaded execution using ProcessPoolExecutor
Runs N Saclets in parallel for massive speedup!

Integrates:
- World model for K_τ as predictive accuracy (self-knowledge)
- Variational path integration (proper action over trajectories)
- Helical calculus (κ-coupling for rotational memory)
- Multi-scale + swarm coupling framework
- PARALLEL EXECUTION for speed
"""

import copy
import time
import random
from dataclasses import dataclass
from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

import gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ============================================================================
# WORLD MODEL (for predictive K_τ)
# ============================================================================

class WorldModel(nn.Module):
    """
    Learns to predict next_state from (state, action).
    
    K_τ becomes: "How well do I predict my own effects?"
    High K_τ = low prediction error = self-knowledge
    """
    def __init__(self, state_dim, action_dim, hidden=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, state_dim)
        )
        
    def forward(self, state, action):
        x = torch.cat([state, action], dim=-1)
        return self.net(x)
    
    def predict(self, state, action):
        """Predict next state"""
        with torch.no_grad():
            state_t = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
            action_t = torch.tensor(action, dtype=torch.float32, device=device).unsqueeze(0)
            pred = self.forward(state_t, action_t)
            return pred.cpu().numpy()[0]


# ============================================================================
# SAC COMPONENTS
# ============================================================================

class Actor(nn.Module):
    def __init__(self, s, a, h=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(s, h),
            nn.ReLU(),
            nn.Linear(h, h),
            nn.ReLU(),
        )
        self.mean = nn.Linear(h, a)
        self.log_std = nn.Linear(h, a)

    def forward(self, x):
        x = self.net(x)
        mean = self.mean(x)
        log_std = self.log_std(x).clamp(-20, 2)
        return mean, log_std


class Critic(nn.Module):
    def __init__(self, s, a, h=256):
        super().__init__()
        self.q = nn.Sequential(
            nn.Linear(s + a, h),
            nn.ReLU(),
            nn.Linear(h, h),
            nn.ReLU(),
            nn.Linear(h, 1)
        )

    def forward(self, s, a):
        return self.q(torch.cat([s, a], dim=-1))


class ReplayBuffer:
    def __init__(self, size=100_000):
        self.size = size
        self.ptr = 0
        self.full = False
        self.states = None
        self.actions = None
        self.rewards = None
        self.next_states = None
        self.dones = None

    def init_arrays(self, state_dim, action_dim):
        self.states = np.zeros((self.size, state_dim), dtype=np.float32)
        self.actions = np.zeros((self.size, action_dim), dtype=np.float32)
        self.rewards = np.zeros((self.size, 1), dtype=np.float32)
        self.next_states = np.zeros((self.size, state_dim), dtype=np.float32)
        self.dones = np.zeros((self.size, 1), dtype=np.float32)

    def store(self, s, a, r, ns, d):
        if self.states is None:
            self.init_arrays(len(s), len(a))
        self.states[self.ptr] = s
        self.actions[self.ptr] = a
        self.rewards[self.ptr] = r
        self.next_states[self.ptr] = ns
        self.dones[self.ptr] = d
        self.ptr = (self.ptr + 1) % self.size
        if self.ptr == 0:
            self.full = True

    def sample(self, batch_size=256):
        max_idx = self.size if self.full else self.ptr
        idx = np.random.randint(0, max_idx, size=batch_size)
        return (
            torch.tensor(self.states[idx], device=device),
            torch.tensor(self.actions[idx], device=device),
            torch.tensor(self.rewards[idx], device=device),
            torch.tensor(self.next_states[idx], device=device),
            torch.tensor(self.dones[idx], device=device),
        )


class MinimalSAC:
    def __init__(self, state_dim, action_dim, action_scale, action_bias, lr=3e-4, gamma=0.99, tau=0.005):
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

        self.replay = ReplayBuffer()
        self.gamma = gamma
        self.tau = tau
        self.action_scale = action_scale
        self.action_bias = action_bias
        self.alpha = 0.2
        self.state_dim = state_dim
        self.action_dim = action_dim

    def select_action(self, state):
        state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        mean, log_std = self.actor(state)
        std = log_std.exp()
        normal = torch.distributions.Normal(mean, std)
        x_t = normal.rsample()
        y_t = torch.tanh(x_t)
        action = y_t * self.action_scale + self.action_bias
        
        # FIX: Explicitly cast to float64 to appease Box2D's strict type checking
        return action.detach().cpu().numpy()[0].astype(np.float64)

    def store(self, s, a, r, ns, d):
        self.replay.store(s, a, r, ns, d)

    def soft_update(self, source, target):
        for s_param, t_param in zip(source.parameters(), target.parameters()):
            t_param.data.copy_(t_param.data * (1.0 - self.tau) + s_param.data * self.tau)

    def train_step(self, batch_size=256):
        if self.replay.states is None or (not self.replay.full and self.replay.ptr < batch_size):
            return

        states, actions, rewards, next_states, dones = self.replay.sample(batch_size)

        # Critic update
        with torch.no_grad():
            nm, nlogstd = self.actor(next_states)
            nstd = nlogstd.exp()
            ndist = torch.distributions.Normal(nm, nstd)
            x_t = ndist.rsample()
            y_t = torch.tanh(x_t)
            next_actions = y_t * self.action_scale + self.action_bias
            log_prob = ndist.log_prob(x_t).sum(-1, keepdim=True) - torch.log(1 - y_t.pow(2) + 1e-7).sum(-1, keepdim=True)

            q1_t = self.c1_t(next_states, next_actions)
            q2_t = self.c2_t(next_states, next_actions)
            q_t = torch.min(q1_t, q2_t) - self.alpha * log_prob
            target_q = rewards + (1 - dones) * self.gamma * q_t

        q1 = self.c1(states, actions)
        q2 = self.c2(states, actions)
        c1_loss = ((q1 - target_q) ** 2).mean()
        c2_loss = ((q2 - target_q) ** 2).mean()

        self.c1_opt.zero_grad()
        c1_loss.backward()
        self.c1_opt.step()

        self.c2_opt.zero_grad()
        c2_loss.backward()
        self.c2_opt.step()

        # Actor update
        m, ls = self.actor(states)
        std = ls.exp()
        dist = torch.distributions.Normal(m, std)
        x_t = dist.rsample()
        y_t = torch.tanh(x_t)
        acts = y_t * self.action_scale + self.action_bias
        log_prob = dist.log_prob(x_t).sum(-1, keepdim=True) - torch.log(1 - y_t.pow(2) + 1e-7).sum(-1, keepdim=True)

        q1_pi = self.c1(states, acts)
        q2_pi = self.c2(states, acts)
        q_pi = torch.min(q1_pi, q2_pi)

        actor_loss = (self.alpha * log_prob - q_pi).mean()

        self.actor_opt.zero_grad()
        actor_loss.backward()
        self.actor_opt.step()

        # Target update
        self.soft_update(self.c1, self.c1_t)
        self.soft_update(self.c2, self.c2_t)


# ============================================================================
# HELICAL VARIATIONAL LAGRANGIAN
# ============================================================================

class HelicalVariationalLagrangian:
    """
    Enhanced Pirouette Lagrangian with:
    
    𝓛_p = K_τ(prediction) - V_Γ(pressure) + J_swarm - λD_R + κH_helix
    
    K_τ: Predictive coherence (self-knowledge via world model)
    V_Γ: Multi-scale pressure/effort
    J_swarm: Swarm coupling (communion principle)
    D_R: Dark residue penalty
    H_helix: Helical memory term (rotational phase tracking)
    """

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        micro_horizon: int = 5,
        meso_horizon: int = 50,
        macro_horizon: int = 500,
        swarm_weight: float = 0.3,
        residue_weight: float = 0.05,
        kappa: float = 0.2,
        world_model_lr: float = 1e-3,
    ):
        self.micro = deque(maxlen=micro_horizon)
        self.meso = deque(maxlen=meso_horizon)
        self.macro = deque(maxlen=macro_horizon)

        self.C_D = 0.0
        self.D_R = 0.0

        self.swarm_mean_L = 0.0
        self.swarm_var_L = 1.0

        self.swarm_weight = swarm_weight
        self.residue_weight = residue_weight
        self.kappa = kappa

        self.world_model = WorldModel(state_dim, action_dim).to(device)
        self.world_model_opt = optim.Adam(self.world_model.parameters(), lr=world_model_lr)
        
        self.phase_history = deque(maxlen=100)
        self.cumulative_phase = 0.0

    def update_swarm_stats(self, mean_L: float, var_L: float):
        self.swarm_mean_L = float(mean_L)
        self.swarm_var_L = float(var_L) if var_L > 1e-6 else 1.0

    def _compute_K_tau_predictive(self, state, action, next_state):
        """K_τ = self-knowledge = inverse prediction error"""
        predicted_next = self.world_model.predict(state, action)
        prediction_error = np.linalg.norm(predicted_next - next_state)
        K_tau = 1.0 / (prediction_error + 0.01)
        K_tau = np.clip(K_tau, 0.1, 10.0)
        return float(K_tau)

    def _compute_V_gamma_scale(self, window):
        """Temporal pressure at a given scale"""
        if len(window) < 1:
            return 0.0
        
        total = 0.0
        for (s, a, s2) in window:
            action_cost = np.linalg.norm(a)
            state_change = np.linalg.norm(s2 - s)
            total += action_cost + 0.1 * state_change
        
        return total / len(window)

    def _compute_helical_term(self, action):
        """κH_helix = rotational memory coupling"""
        if len(action) >= 2:
            phase = np.arctan2(action[1], action[0])
        else:
            phase = action[0]
        
        self.phase_history.append(phase)
        
        if len(self.phase_history) < 2:
            return 0.0
        
        phase_diffs = np.diff(list(self.phase_history))
        phase_diffs = np.arctan2(np.sin(phase_diffs), np.cos(phase_diffs))
        phase_variance = np.var(phase_diffs) + 0.01
        
        H_helix = 1.0 / phase_variance
        H_helix = np.clip(H_helix, 0.1, 5.0)
        
        self.cumulative_phase += phase_diffs[-1] if len(phase_diffs) > 0 else 0.0
        
        return float(H_helix)

    def _compute_path_action(self, window):
        """Compute action integral: S = ∫ 𝓛 dt over trajectory window"""
        if len(window) < 2:
            return 0.0
        
        path_action = 0.0
        for (s, a, s_next) in window:
            K_tau = self._compute_K_tau_predictive(s, a, s_next)
            V_gamma = np.linalg.norm(a) + 0.1 * np.linalg.norm(s_next - s)
            H_helix = self._compute_helical_term(a)
            L_instant = K_tau - V_gamma + self.kappa * H_helix
            path_action += L_instant
        
        return path_action / len(window)

    def compute_lagrangian(self, state, action, next_state):
        """Full Lagrangian with all terms"""
        self.micro.append((state, action, next_state))
        self.meso.append((state, action, next_state))
        self.macro.append((state, action, next_state))

        micro_action = self._compute_path_action(self.micro)
        meso_action = self._compute_path_action(self.meso)
        macro_action = self._compute_path_action(self.macro)

        base_L = 0.5 * micro_action + 0.3 * meso_action + 0.2 * macro_action

        deviation = base_L - self.swarm_mean_L
        J_swarm = -abs(deviation) / (np.sqrt(self.swarm_var_L) + 1e-6)
        
        L = base_L + self.swarm_weight * J_swarm

        if L > 0:
            self.C_D += L
        else:
            self.D_R += abs(L)

        L = L - self.residue_weight * self.D_R

        return float(L)

    def train_world_model(self, state, action, next_state):
        """Train world model to improve K_τ predictions"""
        state_t = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        action_t = torch.tensor(action, dtype=torch.float32, device=device).unsqueeze(0)
        next_state_t = torch.tensor(next_state, dtype=torch.float32, device=device).unsqueeze(0)

        pred = self.world_model(state_t, action_t)
        loss = ((pred - next_state_t) ** 2).mean()

        self.world_model_opt.zero_grad()
        loss.backward()
        self.world_model_opt.step()


# ============================================================================
# SACLET GENOME
# ============================================================================

@dataclass
class SacletGenome:
    learning_rate: float
    lagrangian_balance: float
    alpha: float
    kappa: float = 0.2
    id: int = 0


# ============================================================================
# SACLET
# ============================================================================

class Saclet:
    """
    A Saclet with predictive coherence and helical memory.
    """

    def __init__(self, env_name, genome: SacletGenome):
        self.env_name = env_name
        self.genome = genome

        # Get env dimensions
        temp_env = gym.make(env_name)
        state_dim = temp_env.observation_space.shape[0]
        action_dim = temp_env.action_space.shape[0]
        action_high = torch.tensor(temp_env.action_space.high, device=device)
        action_low = torch.tensor(temp_env.action_space.low, device=device)
        action_scale = (action_high - action_low) / 2.0
        action_bias = (action_high + action_low) / 2.0
        temp_env.close()

        self.policy = MinimalSAC(state_dim, action_dim, action_scale, action_bias,
                                 lr=genome.learning_rate)
        self.policy.alpha = genome.alpha

        self.compass = HelicalVariationalLagrangian(
            state_dim=state_dim,
            action_dim=action_dim,
            kappa=genome.kappa
        )

        self.total_reward = 0.0
        self.total_steps = 0
        self.C_D = 0.0

    def to_device(self, target_device):
        """Move all internal networks to specific device"""
        device_obj = torch.device(target_device)
        self.policy.actor.to(device_obj)
        self.policy.c1.to(device_obj)
        self.policy.c2.to(device_obj)
        self.policy.c1_t.to(device_obj)
        self.policy.c2_t.to(device_obj)
        self.compass.world_model.to(device_obj)

    def get_state_dict(self):
        """Extract weights to CPU to avoid CUDA pickling errors"""
        return {
            'actor': self.policy.actor.state_dict(),
            'c1': self.policy.c1.state_dict(),
            'c2': self.policy.c2.state_dict(),
            'c1_t': self.policy.c1_t.state_dict(),
            'c2_t': self.policy.c2_t.state_dict(),
            'world_model': self.compass.world_model.state_dict()
        }

    def load_state_dict(self, state_dict):
        """Load weights"""
        self.policy.actor.load_state_dict(state_dict['actor'])
        self.policy.c1.load_state_dict(state_dict['c1'])
        self.policy.c2.load_state_dict(state_dict['c2'])
        self.policy.c1_t.load_state_dict(state_dict['c1_t'])
        self.policy.c2_t.load_state_dict(state_dict['c2_t'])
        self.compass.world_model.load_state_dict(state_dict['world_model'])

    def live(self, steps, progress_interval=1000, verbose=False):
        """Live for N steps with predictive coherence"""
        env = gym.make(self.env_name)
        state, _ = env.reset()
        episode_reward = 0.0
        start_time = time.time()

        for step in range(steps):
            action = self.policy.select_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            lagrangian = self.compass.compute_lagrangian(state, action, next_state)
            self.compass.train_world_model(state, action, next_state)

            blended_reward = (1 - self.genome.lagrangian_balance) * reward + \
                             self.genome.lagrangian_balance * lagrangian

            self.policy.store(state, action, blended_reward, next_state, float(done))
            self.policy.train_step()

            self.total_reward += reward
            self.total_steps += 1
            self.C_D = self.compass.C_D

            state = next_state
            episode_reward += reward

            if done:
                state, _ = env.reset()

            if verbose and (step + 1) % progress_interval == 0:
                dt = time.time() - start_time
                print(f"    [Saclet {self.genome.id}] step={step+1}/{steps} "
                      f"R_ep={episode_reward:.2f} C_D={self.C_D:.2f} κ={self.genome.kappa:.2f} dt={dt:.1f}s")
                episode_reward = 0.0
                start_time = time.time()

        env.close()
        return self.fitness()

    def fitness(self):
        if self.total_steps == 0:
            return -1e9
        avg_reward = self.total_reward / self.total_steps
        avg_C_D = self.C_D / self.total_steps
        return avg_reward + 0.05 * avg_C_D

    def clone(self):
        new_genome = SacletGenome(
            learning_rate=self.genome.learning_rate,
            lagrangian_balance=self.genome.lagrangian_balance,
            alpha=self.genome.alpha,
            kappa=self.genome.kappa,
            id=self.genome.id + 1000
        )

        clone = Saclet(self.env_name, new_genome)
        clone.policy.actor.load_state_dict(copy.deepcopy(self.policy.actor.state_dict()))
        clone.policy.c1.load_state_dict(copy.deepcopy(self.policy.c1.state_dict()))
        clone.policy.c2.load_state_dict(copy.deepcopy(self.policy.c2.state_dict()))
        clone.policy.c1_t.load_state_dict(copy.deepcopy(self.policy.c1_t.state_dict()))
        clone.policy.c2_t.load_state_dict(copy.deepcopy(self.policy.c2_t.state_dict()))

        return clone

    def mutate(self, rate=0.1):
        if random.random() < rate:
            self.genome.learning_rate *= np.random.uniform(0.8, 1.2)
            self.genome.learning_rate = float(np.clip(self.genome.learning_rate, 1e-5, 1e-2))

        if random.random() < rate:
            self.genome.lagrangian_balance += np.random.uniform(-0.05, 0.05)
            self.genome.lagrangian_balance = float(np.clip(self.genome.lagrangian_balance, 0.0, 1.0))

        if random.random() < rate:
            self.genome.alpha += np.random.uniform(-0.02, 0.02)
            self.genome.alpha = float(np.clip(self.genome.alpha, 0.01, 0.5))
        
        if random.random() < rate:
            self.genome.kappa += np.random.uniform(-0.1, 0.1)
            self.genome.kappa = float(np.clip(self.genome.kappa, 0.0, 1.0))

        self.policy.alpha = self.genome.alpha
        self.compass.kappa = self.genome.kappa


# ============================================================================
# PARALLEL EXECUTION HELPERS
# ============================================================================

def run_saclet_parallel(args):
    """
    Worker function. Reconstructs Saclet from DNA + Weights to avoid
    Windows CUDA pickling deadlocks.
    """
    genome, state_dict, steps, env_name, saclet_idx, total_saclets = args
    
    # Reconstruct the agent purely inside this process
    # This ensures the CUDA context is fresh for this worker
    worker_saclet = Saclet(env_name, genome)
    worker_saclet.load_state_dict(state_dict)
    
    # Now it's safe to move to GPU (if available)
    worker_saclet.to_device(device)
    
    if saclet_idx == 0:
        print(f"[Process {saclet_idx+1}/{total_saclets}] Saclet {genome.id} starting on {device}...")
    
    # Run
    fitness = worker_saclet.live(steps, verbose=False)
    
    # CRITICAL: Move back to CPU before returning results to main process
    worker_saclet.to_device('cpu')
    
    # Return the updated weights and the fitness
    return saclet_idx, fitness, worker_saclet.get_state_dict(), worker_saclet.C_D


# ============================================================================
# SWARM MANAGER WITH PARALLELIZATION
# ============================================================================

class ParallelSwarmManager:
    """
    Swarm manager with parallel execution of Saclets.
    
    Uses ProcessPoolExecutor to run multiple Saclets simultaneously.
    """
    
    def __init__(self, env_name, swarm_size=8, n_workers=None):
        self.env_name = env_name
        self.swarm_size = swarm_size
        
        # Default to using all CPU cores minus 1
        if n_workers is None:
            n_workers = max(1, mp.cpu_count() - 1)
        self.n_workers = n_workers
        
        self.swarm = []

        for i in range(swarm_size):
            genome = SacletGenome(
                learning_rate=np.random.uniform(1e-4, 5e-4),
                lagrangian_balance=np.random.uniform(0.1, 0.6),
                alpha=np.random.uniform(0.05, 0.3),
                kappa=np.random.uniform(0.0, 0.5),
                id=i
            )
            self.swarm.append(Saclet(env_name, genome))

        self.fitness_history = []
        self.best_fitness_history = []
        self.C_D_history = []

    def evolve(self, generations=10, steps_per_saclet=5000):
        TOP_PERCENT = 0.25
        BOTTOM_PERCENT = 0.25
        MUTATION_RATE = 0.25

        for gen in range(generations):
            print(f"\n{'='*60}")
            print(f"GENERATION {gen+1}/{generations}")
            print(f"{'='*60}")
            print(f"Running {self.swarm_size} Saclets in parallel with {self.n_workers} workers...")
            
            gen_start = time.time()
            
            # Prepare arguments: Send DATA (genome + weights), not OBJECTS
            # We must ensure weights are on CPU before packing
            args_list = []
            for i, saclet in enumerate(self.swarm):
                saclet.to_device('cpu') # Ensure main process doesn't lock GPU
                args_list.append((
                    saclet.genome, 
                    saclet.get_state_dict(), 
                    steps_per_saclet, 
                    self.env_name, 
                    i, 
                    self.swarm_size
                ))
            
            # Run in parallel
            results = []
            with ProcessPoolExecutor(max_workers=self.n_workers) as executor:
                futures = [executor.submit(run_saclet_parallel, args) for args in args_list]
                
                for future in as_completed(futures):
                    # Retrieve results: (index, fitness, new_weights, C_D)
                    idx, fit, new_weights, c_d = future.result()
                    
                    # Update the original saclet in the main process
                    self.swarm[idx].load_state_dict(new_weights)
                    self.swarm[idx].C_D = c_d
                    # Move back to GPU if you want (optional, but we move to CPU next loop anyway)
                    # self.swarm[idx].to_device(device) 
                    
                    results.append((fit, self.swarm[idx]))
                    print(f"  > Saclet {self.swarm[idx].genome.id} finished. Fitness: {fit:.2f}")
            
            gen_time = time.time() - gen_start
            
            # Sort by fitness (High is good)
            results.sort(key=lambda x: x[0], reverse=True)
            sorted_saclets = [r[1] for r in results]

            avg_fitness = np.mean([r[0] for r in results])
            best_fitness = results[0][0]
            
            # Just tracking C_D from the updated saclets
            avg_C_D = np.mean([s.C_D for s in sorted_saclets])

            self.fitness_history.append(avg_fitness)
            self.best_fitness_history.append(best_fitness)

            print(f"\n{'='*60}")
            print(f"EVALUATION (Generation completed in {gen_time:.1f}s)")
            print(f"  Average Fitness: {avg_fitness:7.2f}")
            print(f"  Best Fitness:    {best_fitness:7.2f}")
            print(f"  Average C_D:     {avg_C_D:7.2f}")
            print(f"{'='*60}")

            # Broadcast swarm stats
            var_C_D = np.var([s.C_D for s in sorted_saclets])
            for s in sorted_saclets:
                s.compass.update_swarm_stats(avg_C_D, var_C_D)

            # Evolve
            num_to_cull = int(self.swarm_size * BOTTOM_PERCENT)
            num_to_replicate = int(self.swarm_size * TOP_PERCENT)

            survivors = sorted_saclets[:-num_to_cull]
            elite = sorted_saclets[:num_to_replicate]
            
            offspring = []
            for parent in elite:
                child = parent.clone()
                child.mutate(rate=MUTATION_RATE)
                offspring.append(child)

            self.swarm = survivors + offspring

            # Fill any gaps
            while len(self.swarm) < self.swarm_size:
                g = SacletGenome(
                    learning_rate=np.random.uniform(1e-4, 5e-4),
                    lagrangian_balance=np.random.uniform(0.1, 0.6),
                    alpha=np.random.uniform(0.05, 0.3),
                    kappa=np.random.uniform(0.0, 0.5),
                    id=9999
                )
                self.swarm.append(Saclet(self.env_name, g))


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Prevent issues with multiprocessing on Windows
    mp.set_start_method('spawn', force=True)
    
    ENV_NAME = "LunarLanderContinuous-v2"
    SWARM_SIZE = 20  # Can now handle larger swarms!
    GENERATION_STEPS = 10000
    NUM_GENERATIONS = 10
    N_WORKERS = 4 # None = auto-detect (CPU count - 1)

    print("\n" + "="*60)
    print(" " * 5 + "⚡ PARALLEL HELICAL PREDICTIVE SACLET SWARM ⚡")
    print("="*60)
    print(f"\nEnvironment:      {ENV_NAME}")
    print(f"Swarm Size:       {SWARM_SIZE}")
    print(f"Generation Steps: {GENERATION_STEPS}")
    print(f"Num Generations:  {NUM_GENERATIONS}")
    print(f"Parallel Workers: {N_WORKERS if N_WORKERS else 'Auto (CPU-1)'}")
    print("\nEnhancements:")
    print("  ✓ World model for predictive K_τ")
    print("  ✓ Variational path integration")
    print("  ✓ Helical calculus (κ-coupling)")
    print("  ✓ Multi-scale coherence")
    print("  ✓ Swarm communion")
    print("  ⚡ PARALLEL EXECUTION")
    print("\n" + "="*60 + "\n")

    manager = ParallelSwarmManager(ENV_NAME, swarm_size=SWARM_SIZE, n_workers=N_WORKERS)
    manager.evolve(NUM_GENERATIONS, GENERATION_STEPS)
    
    print("\n" + "="*60)
    print("🌀 EVOLUTION COMPLETE 🌀")
    print("="*60)