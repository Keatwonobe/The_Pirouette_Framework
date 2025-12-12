"""
Bilateral Hemisphere Agent - Windows Safe & Bomb-Proof
====================================================
- OBS_DIM fixed to 105 (Ant-v5 standard).
- Checkpointing: Saves state every cycle. Resumes automatically.
- Anti-Hang: Uses map_async to ensure Ctrl+C works on Windows.
"""

import gymnasium as gym
import numpy as np
from collections import deque
from multiprocessing import Pool, cpu_count
import pickle
import os
import signal
import sys
import time

# ============================================================================
# ARCHITECTURE CONFIG
# ============================================================================
# FIXED: Ant-v5 usually outputs 105 dims (27 physics + 78 contact forces)
OBS_DIM = 105 
ACT_DIM = 8
H1 = 64
H2 = 32

# Calculate total parameter count
PARAM_DIM = (H1 * OBS_DIM + H1) + (H2 * H1 + H2) + (ACT_DIM * H2 + ACT_DIM)
CHECKPOINT_FILE = "bilateral_checkpoint.pkl"

# ============================================================================
# GRACEFUL KILLER (Handle Ctrl+C)
# ============================================================================
class GracefulKiller:
    """Captures Ctrl+C to allow saving before exit"""
    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print("\n\n[!] TEMINATION SIGNAL RECEIVED. FINISHING WORKER THEN SAVING...")
        self.kill_now = True

# ============================================================================
# LEFT HEMISPHERE: PURE NUMPY WORKERS
# ============================================================================
_worker_env = None

def worker_init():
    """Initialize worker - NO PYTORCH IMPORTS"""
    global _worker_env
    import warnings
    warnings.filterwarnings("ignore")
    try:
        # Create env with same settings
        _worker_env = gym.make("Ant-v5", terminate_when_unhealthy=True, render_mode=None)
        _worker_env.reset()
    except Exception as e:
        print(f"Worker init failed: {e}")

def worker_eval(args):
    """Evaluate using pure numpy - NO PYTORCH"""
    static_vec, seed = args
    global _worker_env
    
    if _worker_env is None:
        return -1000.0, 0
    
    # Unpack weights
    idx = 0
    w1 = static_vec[idx:idx + H1*OBS_DIM].reshape(H1, OBS_DIM)
    idx += H1 * OBS_DIM
    b1 = static_vec[idx:idx + H1]
    idx += H1
    w2 = static_vec[idx:idx + H2*H1].reshape(H2, H1)
    idx += H2 * H1
    b2 = static_vec[idx:idx + H2]
    idx += H2
    w3 = static_vec[idx:idx + ACT_DIM*H2].reshape(ACT_DIM, H2)
    idx += ACT_DIM * H2
    b3 = static_vec[idx:]
    
    try:
        obs, _ = _worker_env.reset(seed=seed)
        total_reward = 0.0
        steps = 0
        
        for _ in range(1000):
            obs = np.asarray(obs, dtype=np.float32)
            
            # Check dimension safety
            if obs.shape[0] != OBS_DIM:
                # Fail gracefully if env mismatch persists
                return -9999.0, 0

            # Numpy forward pass
            z1 = np.tanh(w1 @ obs + b1)
            z2 = np.tanh(w2 @ z1 + b2)
            action = np.tanh(w3 @ z2 + b3)
            
            obs, reward, terminated, truncated, _ = _worker_env.step(action)
            total_reward += reward
            steps += 1
            
            if terminated or truncated:
                break
        
        fitness = total_reward + (steps * 0.1)
        if steps < 50:
            fitness = -500.0
            
        return fitness, steps
        
    except Exception:
        return -1000.0, 0

class LeftHemisphere:
    """Static evolution - pure numpy"""
    def __init__(self, pop_size=128):
        self.dim = PARAM_DIM
        self.pop_size = pop_size
        self.pop = self._init_population()
        self.fitness_history = deque(maxlen=10)
        self.gen = 0
        self.all_time_best_fitness = -np.inf
        self.all_time_best_params = None
        
        n_workers = min(16, max(1, cpu_count() - 2))
        self.pool = Pool(processes=n_workers, initializer=worker_init, maxtasksperchild=20)
        print(f"Left Hemisphere: {n_workers} numpy-only workers")
        
    def _init_population(self):
        pop = []
        for _ in range(self.pop_size):
            params = np.random.randn(self.dim).astype(np.float32) * 0.1
            pop.append(params)
        return np.stack(pop)
    
    def step(self):
        self.gen += 1
        
        # Dynamic sigma
        if self.gen < 20: sigma = 0.15
        elif self.all_time_best_fitness < 0: sigma = 0.2
        else: sigma = 0.05
        
        seeds = [self.gen * self.pop_size + i for i in range(self.pop_size)]
        args = [(self.pop[i], seeds[i]) for i in range(self.pop_size)]
        
        # CRITICAL FOR WINDOWS: Use map_async with timeout to allow Ctrl+C
        res_async = self.pool.map_async(worker_eval, args)
        try:
            results = res_async.get(timeout=99999) # Long timeout allows interrupts
        except TimeoutError:
            print("Workers timed out!")
            return None
        
        fits = np.array([r[0] for r in results])
        steps = np.array([r[1] for r in results])
        
        # Check for crash codes
        if np.mean(fits) < -9000:
            print("CRITICAL: Dimension Mismatch detected in workers.")
            raise RuntimeError(f"Env OBS mismatch. Config: {OBS_DIM}")

        best_idx = np.argmax(fits)
        if fits[best_idx] > self.all_time_best_fitness:
            self.all_time_best_fitness = fits[best_idx]
            self.all_time_best_params = self.pop[best_idx].copy()
        
        self.fitness_history.append(np.max(fits))
        
        # Evolution (Elitism + Mutation)
        n_elites = max(4, int(self.pop_size * 0.15))
        elite_indices = np.argsort(fits)[-n_elites:]
        elites = self.pop[elite_indices]
        
        new_pop = []
        if self.all_time_best_params is not None:
            new_pop.append(self.all_time_best_params.copy())
        
        while len(new_pop) < self.pop_size:
            p1 = elites[np.random.randint(len(elites))]
            p2 = elites[np.random.randint(len(elites))]
            mask = np.random.rand(self.dim) > 0.5
            child = np.where(mask, p1, p2)
            child = child + np.random.randn(self.dim).astype(np.float32) * sigma
            new_pop.append(child)
        
        self.pop = np.stack(new_pop)
        
        return {
            'best_fitness': np.max(fits),
            'mean_fitness': np.mean(fits),
            'mean_steps': np.mean(steps),
            'all_time_best': self.all_time_best_fitness
        }
    
    def inject_genome(self, params):
        self.pop[0] = params.astype(np.float32)
    
    def get_best_policy(self):
        return self.all_time_best_params
    
    def get_state(self):
        """Serialize state for checkpoint"""
        return {
            'pop': self.pop,
            'gen': self.gen,
            'all_time_best_fitness': self.all_time_best_fitness,
            'all_time_best_params': self.all_time_best_params
        }

    def set_state(self, state):
        """Load state from checkpoint"""
        self.pop = state['pop']
        self.gen = state['gen']
        self.all_time_best_fitness = state['all_time_best_fitness']
        self.all_time_best_params = state['all_time_best_params']

    def cleanup(self):
        self.pool.terminate() # Force kill
        self.pool.join()

# ============================================================================
# RIGHT HEMISPHERE: PyTorch PPO
# ============================================================================
def lazy_import_torch():
    import torch
    import torch.nn as nn
    import torch.optim as optim
    return torch, nn, optim

class RightHemisphere:
    def __init__(self):
        torch, nn, optim = lazy_import_torch()
        self.torch = torch
        self.nn = nn
        self.optim = optim
        
        self.policy = self._build_policy()
        self.value_net = self._build_value_net()
        
        self.policy_optimizer = optim.Adam(self.policy.parameters(), lr=3e-4)
        self.value_optimizer = optim.Adam(self.value_net.parameters(), lr=3e-4)
        self.reward_history = deque(maxlen=10)
        
    def _build_policy(self):
        return self.nn.Sequential(
            self.nn.Linear(OBS_DIM, H1),
            self.nn.Tanh(),
            self.nn.Linear(H1, H2),
            self.nn.Tanh(),
            self.nn.Linear(H2, ACT_DIM),
            self.nn.Tanh()
        )
    
    def _build_value_net(self):
        return self.nn.Sequential(
            self.nn.Linear(OBS_DIM, 64),
            self.nn.Tanh(),
            self.nn.Linear(64, 32),
            self.nn.Tanh(),
            self.nn.Linear(32, 1)
        )
    
    def get_flat_params(self):
        with self.torch.no_grad():
            params = []
            for p in self.policy.parameters():
                params.append(p.cpu().numpy().flatten())
            return np.concatenate(params).astype(np.float32)
    
    def set_flat_params(self, flat_params):
        params = self.torch.from_numpy(flat_params).float()
        offset = 0
        with self.torch.no_grad():
            for p in self.policy.parameters():
                numel = p.numel()
                p.copy_(params[offset:offset+numel].view_as(p))
                offset += numel
    
    def load_from_static(self, static_params):
        self.set_flat_params(static_params)
        # Reset optimizer to allow new exploration
        self.policy_optimizer = self.optim.Adam(self.policy.parameters(), lr=3e-4)
        
    def collect_rollout(self, env, n_steps=2048):
        states, actions, rewards, values, dones = [], [], [], [], []
        obs, _ = env.reset()
        ep_reward = 0
        
        for _ in range(n_steps):
            state_t = self.torch.FloatTensor(obs).unsqueeze(0)
            with self.torch.no_grad():
                action = self.policy(state_t)
                value = self.value_net(state_t)
                action = action + self.torch.randn_like(action) * 0.1
                action = self.torch.clamp(action, -1, 1)
            
            states.append(obs)
            actions.append(action.squeeze().numpy())
            values.append(value.item())
            
            obs, reward, terminated, truncated, _ = env.step(action.squeeze().numpy())
            ep_reward += reward
            rewards.append(reward)
            dones.append(terminated or truncated)
            
            if terminated or truncated:
                self.reward_history.append(ep_reward)
                obs, _ = env.reset()
                ep_reward = 0
        
        return {
            'states': np.array(states), 'actions': np.array(actions),
            'rewards': np.array(rewards), 'values': np.array(values),
            'dones': np.array(dones)
        }
    
    def compute_gae(self, rewards, values, dones, gamma=0.99, lam=0.95):
        advantages = np.zeros_like(rewards)
        last_gae = 0
        for t in reversed(range(len(rewards))):
            next_value = 0 if t == len(rewards)-1 else values[t+1]
            delta = rewards[t] + gamma * next_value * (1-dones[t]) - values[t]
            advantages[t] = last_gae = delta + gamma * lam * (1-dones[t]) * last_gae
        return advantages, advantages + values
    
    def update(self, rollout, epochs=4):
        states = self.torch.FloatTensor(rollout['states'])
        actions = self.torch.FloatTensor(rollout['actions'])
        advantages, returns = self.compute_gae(rollout['rewards'], rollout['values'], rollout['dones'])
        
        advantages = self.torch.FloatTensor(advantages)
        returns = self.torch.FloatTensor(returns)
        if advantages.std() > 1e-8:
            advantages = (advantages - advantages.mean()) / advantages.std()
        
        for _ in range(epochs):
            action_pred = self.policy(states)
            values_pred = self.value_net(states).squeeze()
            
            log_probs = -0.5 * ((action_pred - actions) ** 2).sum(dim=1)
            policy_loss = -(log_probs * advantages).mean()
            value_loss = ((values_pred - returns) ** 2).mean()
            
            self.policy_optimizer.zero_grad()
            policy_loss.backward()
            self.torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
            self.policy_optimizer.step()
            
            self.value_optimizer.zero_grad()
            value_loss.backward()
            self.torch.nn.utils.clip_grad_norm_(self.value_net.parameters(), 0.5)
            self.value_optimizer.step()
    
    def step(self, env, n_rollouts=2):
        for _ in range(n_rollouts):
            rollout = self.collect_rollout(env, n_steps=1024)
            self.update(rollout)
        return {'mean_reward': np.mean(self.reward_history) if self.reward_history else 0}
    
    def get_policy_params(self):
        return self.get_flat_params()

    def get_state(self):
        return {
            'policy': self.policy.state_dict(),
            'value': self.value_net.state_dict(),
            'p_opt': self.policy_optimizer.state_dict(),
            'v_opt': self.value_optimizer.state_dict()
        }

    def set_state(self, state):
        self.policy.load_state_dict(state['policy'])
        self.value_net.load_state_dict(state['value'])
        self.policy_optimizer.load_state_dict(state['p_opt'])
        self.value_optimizer.load_state_dict(state['v_opt'])

# ============================================================================
# BILATERAL COORDINATOR
# ============================================================================
def save_checkpoint(cycle, left, right):
    data = {
        'cycle': cycle,
        'left_state': left.get_state(),
        'right_state': right.get_state()
    }
    with open(CHECKPOINT_FILE, 'wb') as f:
        pickle.dump(data, f)
    print(f"[Check] State saved to {CHECKPOINT_FILE}")

def load_checkpoint(left, right):
    if not os.path.exists(CHECKPOINT_FILE):
        return 1
    
    print(f"\nFound checkpoint: {CHECKPOINT_FILE}")
    print("Resume? (y/n): ", end="")
    try:
        # Set a simple timeout for input or default to yes if preferred
        # For now, we just assume input
        choice = input().lower().strip()
    except:
        choice = 'y' # Default to yes in weird shell environments

    if choice != 'y':
        return 1
        
    with open(CHECKPOINT_FILE, 'rb') as f:
        data = pickle.load(f)
    
    left.set_state(data['left_state'])
    right.set_state(data['right_state'])
    print(f"Resumed from Cycle {data['cycle']}")
    return data['cycle'] + 1

def run_bilateral_training(cycles=100, left_gens=10, right_updates=3):
    killer = GracefulKiller()
    
    print("=" * 60)
    print("BILATERAL HEMISPHERE - BOMB PROOF EDITION")
    print("=" * 60)
    
    left = LeftHemisphere(pop_size=128)
    right = RightHemisphere()
    
    # Attempt load
    start_cycle = load_checkpoint(left, right)
    env = gym.make("Ant-v5", terminate_when_unhealthy=True)
    
    try:
        for cycle in range(start_cycle, cycles + 1):
            # Check for kill signal before starting new cycle
            if killer.kill_now: break

            print(f"\n{'='*60}")
            print(f"CYCLE {cycle}/{cycles}")
            print(f"{'='*60}")
            
            # LEFT HEMISPHERE
            print(f"\n[LEFT] Running {left_gens} generations...")
            for g in range(left_gens):
                if killer.kill_now: break
                result = left.step()
                
                if (g+1) % 5 == 0 or g == left_gens-1:
                    print(f"  Gen {left.gen:3d}: Best={result['best_fitness']:6.1f} | "
                          f"Mean={result['mean_fitness']:6.1f} | "
                          f"Steps={result['mean_steps']:4.0f}")
            
            if killer.kill_now: break

            # Transfer
            best_static = left.get_best_policy()
            if best_static is not None:
                print(f"\n[TRANSFER] Left → Right (Fitness: {left.all_time_best_fitness:.1f})")
                right.load_from_static(best_static)
            
            # RIGHT HEMISPHERE
            print(f"\n[RIGHT] Running {right_updates} PPO updates...")
            mean_rew = 0
            for u in range(right_updates):
                if killer.kill_now: break
                result = right.step(env, n_rollouts=2)
                mean_rew = result['mean_reward']
                print(f"  Update {u+1:2d}: MeanReward={mean_rew:6.1f}")
            
            if killer.kill_now: break

            # Transfer Back
            refined = right.get_policy_params()
            print(f"[TRANSFER] Right → Left (Reward: {mean_rew:.1f})")
            left.inject_genome(refined)
            
            # CHECKPOINT
            save_checkpoint(cycle, left, right)
    
    except KeyboardInterrupt:
        print("\n[!] Manual interrupt detected via KeyboardInterrupt")
    except Exception as e:
        print(f"\n[!] Critical Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if killer.kill_now:
            print("\n[!] Saving checkpoint due to interrupt...")
            save_checkpoint(cycle, left, right)
        
        left.cleanup()
        env.close()
        print("\nCleanup complete.")

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method('spawn', force=True)
    
    run_bilateral_training(cycles=100, left_gens=10, right_updates=3)