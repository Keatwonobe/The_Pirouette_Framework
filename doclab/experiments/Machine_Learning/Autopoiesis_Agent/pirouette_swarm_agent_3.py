#!/usr/bin/env python3
"""
Saclet: The Minimal Unit That Can Learn, Feel, and Evolve

Original goals:
- keep it readable
- keep it emergent
- let the lagrangian be the "feeling"
- let the swarm evolve how much it cares about feeling

This version upgrades the Lagrangian to a universal, swarm-coupled,
multi-timescale form so we can minimize "engineered consciousness"
and just run coherence as a structural prior.
"""

import copy
import time
import random
from dataclasses import dataclass
from collections import deque

import gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ============================================================================
# SIMPLE SAC PARTS
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
        self.alpha = 0.2  # will get overwritten per-genome
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
        return action.detach().cpu().numpy()[0]

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
# UNIVERSAL LAGRANGIAN (replaces MinimalLagrangian)
# ============================================================================

class UniversalLagrangian:
    """
    Universal RL Lagrangian for coherent swarms.

    𝓛 = K_temporal - V_Γ + J_swarm - λ D_R

    - K_temporal: action/self consistency over multiple windows
    - V_Γ: pressure / effort / deformation
    - J_swarm: stay near swarm's coherence band
    - D_R: accumulated dark residue (negative coherence), penalized
    """

    def __init__(
        self,
        micro_horizon: int = 5,
        meso_horizon: int = 50,
        macro_horizon: int = 500,
        swarm_weight: float = 0.3,
        residue_weight: float = 0.05,
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

    def update_swarm_stats(self, mean_L: float, var_L: float):
        self.swarm_mean_L = float(mean_L)
        self.swarm_var_L = float(var_L) if var_L > 1e-6 else 1.0

    # ---- per-scale helpers -------------------------------------------------
    def _scale_K_tau(self, window):
        # inverse action variance across window
        if len(window) < 2:
            return 1.0
        actions = np.array([a for (_, a, _) in window])
        var = np.var(actions) + 1e-3
        K = 1.0 / var
        return float(np.clip(K, 0.05, 10.0))

    def _scale_V_gamma(self, window):
        if len(window) < 1:
            return 0.0
        total = 0.0
        for (s, a, s2) in window:
            a_mag = np.linalg.norm(a)
            s_mag = np.linalg.norm(s2 - s)
            total += a_mag + 0.1 * s_mag
        return total / len(window)

    def _scale_L(self, window):
        K = self._scale_K_tau(window)
        V = self._scale_V_gamma(window)
        return K - V

    # ---- main compute ------------------------------------------------------
    def compute_lagrangian(self, state, action, next_state):
        # append to all scales
        self.micro.append((state, action, next_state))
        self.meso.append((state, action, next_state))
        self.macro.append((state, action, next_state))

        micro_L = self._scale_L(self.micro)
        meso_L = self._scale_L(self.meso)
        macro_L = self._scale_L(self.macro)

        # weighted multi-scale
        base_L = 0.5 * micro_L + 0.3 * meso_L + 0.2 * macro_L

        # swarm coupling
        dev = base_L - self.swarm_mean_L
        J = -abs(dev) / (np.sqrt(self.swarm_var_L) + 1e-6)
        L = base_L + self.swarm_weight * J

        # dividends & residue
        if L > 0:
            self.C_D += L
        else:
            self.D_R += -L

        # decay by residue — this is the “don’t make me engineer consciousness to get reward” brake
        L = L - self.residue_weight * self.D_R

        return float(L)


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

        # >>> upgraded compass <<<
        self.compass = UniversalLagrangian()

        # Tracking
        self.total_reward = 0.0
        self.total_steps = 0
        self.C_D = 0.0

    def live(self, steps, progress_interval=1000):
        """
        Live for N steps in the environment.

        This is where the agent:
        - Feels the Lagrangian
        - Blends it with reward
        - Learns from the blend
        - Tracks coherence dividend
        """
        env = gym.make(self.env_name)
        state, _ = env.reset()
        episode_reward = 0.0
        start_time = time.time()

        for step in range(steps):
            action = self.policy.select_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            # Feel the Lagrangian
            lagrangian = self.compass.compute_lagrangian(state, action, next_state)

            # Blend task reward with coherence
            blended_reward = (1 - self.genome.lagrangian_balance) * reward + \
                             self.genome.lagrangian_balance * lagrangian

            # Store and learn
            self.policy.store(state, action, blended_reward, next_state, float(done))
            self.policy.train_step()

            # Update stats
            self.total_reward += reward
            self.total_steps += 1
            self.C_D = self.compass.C_D  # keep exposed

            state = next_state
            episode_reward += reward

            if done:
                state, _ = env.reset()

            if (step + 1) % progress_interval == 0:
                dt = time.time() - start_time
                print(f"[Saclet {self.genome.id}] step={step+1}/{steps} "
                      f"R_ep={episode_reward:.2f} C_D={self.C_D:.2f} dt={dt:.1f}s")
                episode_reward = 0.0
                start_time = time.time()

        env.close()

    def fitness(self):
        """
        Define fitness as: average reward + small fraction of coherence dividend
        """
        if self.total_steps == 0:
            return -1e9
        avg_reward = self.total_reward / self.total_steps
        avg_C_D = self.C_D / self.total_steps
        return avg_reward + 0.05 * avg_C_D

    def clone(self):
        """Create a copy of this Saclet"""
        # Clone genome
        new_genome = SacletGenome(
            learning_rate=self.genome.learning_rate,
            lagrangian_balance=self.genome.lagrangian_balance,
            alpha=self.genome.alpha,
            id=self.genome.id + 1000
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

    def mutate(self, rate=0.1):
        """
        Mutate genome slightly.
        """
        if random.random() < rate:
            self.genome.learning_rate *= np.random.uniform(0.8, 1.2)
            self.genome.learning_rate = float(np.clip(self.genome.learning_rate, 1e-5, 1e-2))

        if random.random() < rate:
            self.genome.lagrangian_balance += np.random.uniform(-0.05, 0.05)
            self.genome.lagrangian_balance = float(np.clip(self.genome.lagrangian_balance, 0.0, 1.0))

        if random.random() < rate:
            self.genome.alpha += np.random.uniform(-0.02, 0.02)
            self.genome.alpha = float(np.clip(self.genome.alpha, 0.01, 0.5))

        # update policy alpha
        self.policy.alpha = self.genome.alpha


# ============================================================================
# SWARM MANAGER
# ============================================================================

class SwarmManager:
    def __init__(self, env_name, swarm_size=8):
        self.env_name = env_name
        self.swarm_size = swarm_size
        self.swarm = []

        for i in range(swarm_size):
            genome = SacletGenome(
                learning_rate=np.random.uniform(1e-4, 5e-4),
                lagrangian_balance=np.random.uniform(0.1, 0.6),
                alpha=np.random.uniform(0.05, 0.3),
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

            fitnesses = []
            # 1. Let each saclet live
            for saclet in self.swarm:
                print(f"\n[GEN {gen+1}] Saclet {saclet.genome.id} lives...")
                saclet.live(steps_per_saclet)
                f = saclet.fitness()
                fitnesses.append((f, saclet, saclet.fitness()))
                print(f"  -> fitness: {f:.3f}")

            # 2. Evaluate
            fitnesses.sort(key=lambda x: x[2], reverse=True)

            avg_fitness = np.mean([f[2] for f in fitnesses])
            best_fitness = fitnesses[0][2]
            avg_C_D = np.mean([s.C_D / max(s.total_steps, 1) for s in self.swarm])

            self.fitness_history.append(avg_fitness)
            self.best_fitness_history.append(best_fitness)
            self.C_D_history.append(avg_C_D)

            print(f"\n{'='*60}")
            print(f"EVALUATION")
            print(f"  Average Fitness: {avg_fitness:7.2f}")
            print(f"  Best Fitness:    {best_fitness:7.2f}")
            print(f"  Average C_D:     {avg_C_D:7.2f}")
            print(f"{'='*60}")

            # >>> broadcast swarm coherence band to all agents <<<
            var_C_D = np.var([s.C_D / max(s.total_steps, 1) for s in self.swarm])
            for s in self.swarm:
                s.compass.update_swarm_stats(avg_C_D, var_C_D)

            # 3. Evolve
            num_to_cull = int(self.swarm_size * BOTTOM_PERCENT)
            num_to_replicate = int(self.swarm_size * TOP_PERCENT)

            # survivors = keep top (size - cull)
            survivors = [f[1] for f in fitnesses[:-num_to_cull]]

            # replicate top N
            elite = [f[1] for f in fitnesses[:num_to_replicate]]
            offspring = []
            for parent in elite:
                child = parent.clone()
                child.mutate(rate=MUTATION_RATE)
                offspring.append(child)

            # refill swarm
            self.swarm = survivors + offspring

            # if we somehow lost count, fill with fresh ones
            while len(self.swarm) < self.swarm_size:
                g = SacletGenome(
                    learning_rate=np.random.uniform(1e-4, 5e-4),
                    lagrangian_balance=np.random.uniform(0.1, 0.6),
                    alpha=np.random.uniform(0.05, 0.3),
                    id=9999
                )
                self.swarm.append(Saclet(self.env_name, g))


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    ENV_NAME = "Pendulum-v1"  # change to Ant-v5 etc. once stable
    SWARM_SIZE = 6
    GENERATION_STEPS = 2000
    NUM_GENERATIONS = 5

    print("\n" + "="*60)
    print(" " * 15 + "SACLET SWARM")
    print("="*60)
    print(f"\nEnvironment:      {ENV_NAME}")
    print(f"Swarm Size:       {SWARM_SIZE}")
    print(f"Generation Steps: {GENERATION_STEPS}")
    print(f"Num Generations:  {NUM_GENERATIONS}")
    print("\n" + "="*60 + "\n")

    manager = SwarmManager(ENV_NAME, swarm_size=SWARM_SIZE)
    manager.evolve(NUM_GENERATIONS, GENERATION_STEPS)
