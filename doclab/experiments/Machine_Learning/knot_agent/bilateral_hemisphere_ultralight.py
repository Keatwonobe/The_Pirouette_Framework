"""
Bilateral Hemisphere Agent - ULTRA LIGHTWEIGHT
===============================================
- Tiny population (32 agents)
- Minimal rollouts (512 steps)
- Aggressive memory cleanup
- Checkpoint after EVERY cycle
- 4 workers max (safe for any PC)
- CPU-only PyTorch to avoid VRAM issues
"""

import gymnasium as gym
import numpy as np
from collections import deque
from multiprocessing import Pool
import pickle
import os
import gc

# ============================================================================
# CONFIG
# ============================================================================
OBS_DIM = 105  # Ant-v4 has 27, v5 has 105 - check your version!
ACT_DIM = 8
H1 = 32  # Smaller network = less memory
H2 = 16

MAX_WORKERS = 4  # Very conservative
POP_SIZE = 32    # Tiny population
ROLLOUT_SIZE = 512  # Smaller rollouts

PARAM_DIM = (H1 * OBS_DIM + H1) + (H2 * H1 + H2) + (ACT_DIM * H2 + ACT_DIM)
CHECKPOINT_FILE = "bilateral_ultralight.pkl"

print(f"Network size: {PARAM_DIM} parameters")

# ============================================================================
# LEFT HEMISPHERE: NUMPY WORKERS
# ============================================================================
_worker_env = None

def worker_init():
    global _worker_env
    import warnings
    warnings.filterwarnings("ignore")
    try:
        _worker_env = gym.make("Ant-v5", terminate_when_unhealthy=True, render_mode=None)
        _worker_env.reset()
    except Exception as e:
        print(f"Worker init failed: {e}")

def worker_eval(args):
    static_vec, seed = args
    global _worker_env
    
    if _worker_env is None:
        return -1000.0, 0
    
    # Unpack
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
    def __init__(self, pop_size=POP_SIZE):
        self.dim = PARAM_DIM
        self.pop_size = pop_size
        self.pop = self._init_population()
        self.gen = 0
        self.all_time_best_fitness = -np.inf
        self.all_time_best_params = None
        self.pool = None
        
    def _init_population(self):
        return np.random.randn(self.pop_size, self.dim).astype(np.float32) * 0.1
    
    def start_workers(self):
        if self.pool is None:
            print(f"[LEFT] Starting {MAX_WORKERS} workers...")
            self.pool = Pool(processes=MAX_WORKERS, initializer=worker_init, maxtasksperchild=5)
            
    def stop_workers(self):
        if self.pool is not None:
            print("[LEFT] Stopping workers...")
            self.pool.terminate()
            self.pool.join()
            self.pool = None
            gc.collect()  # Force garbage collection
    
    def step(self):
        self.gen += 1
        self.start_workers()
        
        # Adaptive sigma
        sigma = 0.15 if self.gen < 10 else 0.05
        if self.all_time_best_fitness < 0:
            sigma = 0.2
        
        # Evaluate
        seeds = [self.gen * self.pop_size + i for i in range(self.pop_size)]
        args = [(self.pop[i], seeds[i]) for i in range(self.pop_size)]
        results = self.pool.map(worker_eval, args)
        
        fits = np.array([r[0] for r in results])
        steps = np.array([r[1] for r in results])
        
        # Update best
        best_idx = np.argmax(fits)
        if fits[best_idx] > self.all_time_best_fitness:
            self.all_time_best_fitness = fits[best_idx]
            self.all_time_best_params = self.pop[best_idx].copy()
        
        # Evolution
        n_elites = max(3, int(self.pop_size * 0.15))
        elite_indices = np.argsort(fits)[-n_elites:]
        elites = self.pop[elite_indices]
        
        new_pop = []
        if self.all_time_best_params is not None:
            new_pop.append(self.all_time_best_params)
        
        while len(new_pop) < self.pop_size:
            p1 = elites[np.random.randint(len(elites))]
            p2 = elites[np.random.randint(len(elites))]
            mask = np.random.rand(self.dim) > 0.5
            child = np.where(mask, p1, p2) + np.random.randn(self.dim).astype(np.float32) * sigma
            new_pop.append(child)
        
        self.pop = np.stack(new_pop)
        
        return {
            'best': np.max(fits),
            'mean': np.mean(fits),
            'steps': np.mean(steps)
        }
    
    def inject(self, params):
        self.pop[0] = params.astype(np.float32)
    
    def get_best(self):
        return self.all_time_best_params
    
    def get_state(self):
        return {
            'pop': self.pop,
            'gen': self.gen,
            'best_fit': self.all_time_best_fitness,
            'best_params': self.all_time_best_params
        }
    
    def set_state(self, state):
        self.pop = state['pop']
        self.gen = state['gen']
        self.all_time_best_fitness = state['best_fit']
        self.all_time_best_params = state['best_params']

# ============================================================================
# RIGHT HEMISPHERE: PYTORCH (LAZY IMPORT)
# ============================================================================
def lazy_torch():
    import torch
    # Force CPU only to avoid VRAM issues
    torch.set_num_threads(2)  # Limit CPU threads
    import torch.nn as nn
    import torch.optim as optim
    return torch, nn, optim

class RightHemisphere:
    def __init__(self):
        torch, nn, optim = lazy_torch()
        self.torch = torch
        
        # Build tiny networks
        self.policy = nn.Sequential(
            nn.Linear(OBS_DIM, H1), nn.Tanh(),
            nn.Linear(H1, H2), nn.Tanh(),
            nn.Linear(H2, ACT_DIM), nn.Tanh()
        )
        
        self.value_net = nn.Sequential(
            nn.Linear(OBS_DIM, H1), nn.Tanh(),
            nn.Linear(H1, H2), nn.Tanh(),
            nn.Linear(H2, 1)
        )
        
        self.policy_opt = optim.Adam(self.policy.parameters(), lr=3e-4)
        self.value_opt = optim.Adam(self.value_net.parameters(), lr=3e-4)
        self.rewards = deque(maxlen=5)
        
    def get_params(self):
        with self.torch.no_grad():
            params = []
            for p in self.policy.parameters():
                params.append(p.cpu().numpy().flatten())
            return np.concatenate(params).astype(np.float32)
    
    def set_params(self, flat):
        params = self.torch.from_numpy(flat).float()
        offset = 0
        with self.torch.no_grad():
            for p in self.policy.parameters():
                numel = p.numel()
                p.copy_(params[offset:offset+numel].view_as(p))
                offset += numel
    
    def load_from_left(self, params):
        self.set_params(params)
        # Reset optimizer
        self.policy_opt = self.torch.optim.Adam(self.policy.parameters(), lr=3e-4)
        
    def collect(self, env, n_steps=ROLLOUT_SIZE):
        """Tiny rollout to save memory"""
        states, actions, rewards, values, dones = [], [], [], [], []
        
        obs, _ = env.reset()
        ep_rew = 0
        
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
            ep_rew += reward
            
            rewards.append(reward)
            dones.append(terminated or truncated)
            
            if terminated or truncated:
                self.rewards.append(ep_rew)
                obs, _ = env.reset()
                ep_rew = 0
        
        return {
            'states': np.array(states),
            'actions': np.array(actions),
            'rewards': np.array(rewards),
            'values': np.array(values),
            'dones': np.array(dones)
        }
    
    def compute_gae(self, rewards, values, dones):
        advantages = np.zeros_like(rewards)
        last_gae = 0
        for t in reversed(range(len(rewards))):
            next_val = 0 if t == len(rewards)-1 else values[t+1]
            delta = rewards[t] + 0.99 * next_val * (1-dones[t]) - values[t]
            advantages[t] = last_gae = delta + 0.99 * 0.95 * (1-dones[t]) * last_gae
        return advantages, advantages + values
    
    def update(self, rollout):
        states = self.torch.FloatTensor(rollout['states'])
        actions = self.torch.FloatTensor(rollout['actions'])
        
        advantages, returns = self.compute_gae(
            rollout['rewards'], rollout['values'], rollout['dones']
        )
        
        advantages = self.torch.FloatTensor(advantages)
        returns = self.torch.FloatTensor(returns)
        
        if advantages.std() > 1e-8:
            advantages = (advantages - advantages.mean()) / advantages.std()
        
        # Single epoch to save memory
        for _ in range(3):
            action_pred = self.policy(states)
            values_pred = self.value_net(states).squeeze()
            
            log_probs = -0.5 * ((action_pred - actions) ** 2).sum(dim=1)
            policy_loss = -(log_probs * advantages).mean()
            value_loss = ((values_pred - returns) ** 2).mean()
            
            self.policy_opt.zero_grad()
            policy_loss.backward()
            self.torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
            self.policy_opt.step()
            
            self.value_opt.zero_grad()
            value_loss.backward()
            self.torch.nn.utils.clip_grad_norm_(self.value_net.parameters(), 0.5)
            self.value_opt.step()
    
    def step(self, env):
        """Single rollout to save memory"""
        rollout = self.collect(env)
        self.update(rollout)
        return np.mean(self.rewards) if self.rewards else 0
    
    def get_state(self):
        return {
            'policy': self.policy.state_dict(),
            'value': self.value_net.state_dict()
        }
    
    def set_state(self, state):
        self.policy.load_state_dict(state['policy'])
        self.value_net.load_state_dict(state['value'])

# ============================================================================
# COORDINATOR
# ============================================================================
def save_checkpoint(cycle, left, right):
    data = {
        'cycle': cycle,
        'left': left.get_state(),
        'right': right.get_state() if right else None
    }
    temp = CHECKPOINT_FILE + ".tmp"
    with open(temp, 'wb') as f:
        pickle.dump(data, f)
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
    os.rename(temp, CHECKPOINT_FILE)
    print(f"✓ Checkpoint saved (cycle {cycle})")

def load_checkpoint():
    if not os.path.exists(CHECKPOINT_FILE):
        return None
    with open(CHECKPOINT_FILE, 'rb') as f:
        return pickle.load(f)

def run_training(cycles=100, left_gens=5, right_updates=2):
    print("=" * 60)
    print("BILATERAL AGENT - ULTRA LIGHTWEIGHT")
    print(f"Pop: {POP_SIZE} | Workers: {MAX_WORKERS} | Net: {H1}-{H2}")
    print("=" * 60)
    
    # Initialize
    left = LeftHemisphere()
    env = gym.make("Ant-v4", terminate_when_unhealthy=True)
    right = None
    
    # Load checkpoint
    start_cycle = 1
    ckpt = load_checkpoint()
    if ckpt:
        print(f"\nFound checkpoint at cycle {ckpt['cycle']}")
        resume = input("Resume? (y/n): ").lower().strip()
        if resume == 'y':
            left.set_state(ckpt['left'])
            start_cycle = ckpt['cycle'] + 1
            print(f"Resumed from cycle {ckpt['cycle']}")
    
    try:
        for cycle in range(start_cycle, cycles + 1):
            print(f"\n{'='*60}")
            print(f"CYCLE {cycle}/{cycles}")
            print(f"{'='*60}")
            
            # LEFT: Evolution
            print(f"\n[LEFT] Evolving {left_gens} generations...")
            for g in range(left_gens):
                res = left.step()
                print(f"  Gen {left.gen:3d}: Best={res['best']:6.1f} | "
                      f"Mean={res['mean']:6.1f} | Steps={res['steps']:4.0f}")
            
            # CRITICAL: Stop workers before PyTorch
            left.stop_workers()
            
            # RIGHT: PPO (lazy init)
            if right is None:
                print("\n[System] Loading PyTorch...")
                right = RightHemisphere()
                if ckpt and ckpt['right']:
                    right.set_state(ckpt['right'])
                    ckpt = None  # Clear after use
            
            # Transfer L→R
            best = left.get_best()
            if best is not None:
                print(f"\n[→] Left → Right (Fit: {left.all_time_best_fitness:.1f})")
                right.load_from_left(best)
            
            # RIGHT: Refine
            print(f"\n[RIGHT] Refining {right_updates} updates...")
            mean_rew = 0
            for u in range(right_updates):
                mean_rew = right.step(env)
                print(f"  Update {u+1}: Reward={mean_rew:6.1f}")
            
            # Transfer R→L
            print(f"\n[←] Right → Left (Rew: {mean_rew:.1f})")
            left.inject(right.get_params())
            
            # SAVE EVERY CYCLE
            save_checkpoint(cycle, left, right)
            
            # Aggressive cleanup
            gc.collect()
    
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted - saving...")
        save_checkpoint(cycle, left, right)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        save_checkpoint(cycle, left, right)
    finally:
        left.stop_workers()
        env.close()
        print("\n✓ Cleanup complete")

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method('spawn', force=True)
    
    run_training(
        cycles=200,      # Many short cycles
        left_gens=5,     # Just 5 gens per cycle
        right_updates=2  # Just 2 updates per cycle
    )