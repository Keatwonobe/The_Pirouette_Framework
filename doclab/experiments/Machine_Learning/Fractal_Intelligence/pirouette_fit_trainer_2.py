# pirouette_fit_trainer.py
# This script combines the robust genetic framework from advanced_ant_trainer_9.py
# with the Fractal Intelligence Transfer (FIT) concepts from PPS-069.
# Version 2: Corrects the critic update logic in the SAC agent.

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Normal
import numpy as np
import gymnasium as gym
from gymnasium.vector import AsyncVectorEnv
import matplotlib.pyplot as plt
from collections import deque, OrderedDict
import random
import time
import math
import os
import shutil

# --- Configuration ---
ENV_NAME = 'Ant-v5'
NUM_EPISODES = 4000
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 10 
EVAL_EPISODES = 5
SEED = 2700
MODEL_PATH = "./pirouette_fit_models/"

# --- Hyperparameters from Advanced Trainer ---
MANIFOLD_BONUS_COEFF = 0.02
MANIFOLD_TEAR_COEFF = 0.05
RESET_THRESHOLD = 0.7
RESET_PATIENCE = 10 
INVERSION_THRESHOLD = -1000
GENETIC_POOL_SIZE = 10
GENE_TRANSFER_RATE = 0.6
RISK_REWARD_MULTIPLIER = 0.1
ACTION_MAGNITUDE_THRESHOLD = 0.1
MAX_ACCEPTABLE_STD = 200

# --- MERGED: Hyperparameters from FIT/Crucible Protocol ---
FLUX_REWARD_WEIGHT = 0.5
PROPHET_QUIZ_INTERVAL = 10
PROPHET_PREDICTION_HORIZON = 50

# Set device and seeds
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
if os.path.exists(MODEL_PATH):
    shutil.rmtree(MODEL_PATH)
os.makedirs(MODEL_PATH, exist_ok=True)
print(f"Using device: {device}")
print(f"FIT models will be saved in: {MODEL_PATH}")

# --- MERGED: Crucible Environment from PPS-069 ---
class CrucibleAntEnv:
    """A wrapper for the Ant environment that introduces hidden, learnable physics (Ki-Modulated Field)."""
    def __init__(self, env_name, max_steps):
        print("Initializing Crucible Environment...")
        self.env = gym.make(env_name, render_mode=None)
        self.max_steps_per_episode = max_steps
        self.current_step = 0
        
        self.gravity_period = self.max_steps_per_episode * 2 
        self.gravity_amplitude = -9.8
        self.gravity_oscillation_amplitude = 4.0
        
        self.observation_space = self.env.observation_space
        self.action_space = self.env.action_space
        # Ensure API compliance for vectorization
        self.metadata = self.env.metadata
        self.render_mode = self.env.render_mode

    def reset(self, seed=None, options=None):
        self.current_step = 0
        self.update_gravity()
        return self.env.reset(seed=seed)

    def step(self, action):
        self.current_step += 1
        self.update_gravity()
        return self.env.step(action)

    def update_gravity(self):
        phase = (2 * np.pi * self.current_step) / self.gravity_period
        current_gravity = self.gravity_amplitude + self.gravity_oscillation_amplitude * np.sin(phase)
        self.env.unwrapped.model.opt.gravity[2] = current_gravity
    
    def get_future_gravity(self, future_steps):
        future_gravities = []
        for i in range(1, future_steps + 1):
            future_step = self.current_step + i
            phase = (2 * np.pi * future_step) / self.gravity_period
            g = self.gravity_amplitude + self.gravity_oscillation_amplitude * np.sin(phase)
            future_gravities.append(g)
        return np.array(future_gravities)
    def close(self):
        """Closes the underlying environment."""
        self.env.close()

# --- MERGED: Prophet Module from PPS-069 ---
class Prophet:
    def __init__(self, state_dim, horizon):
        self.horizon = horizon
        self.model = nn.Sequential(
            nn.Linear(state_dim, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, horizon)
        ).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        self.loss_fn = nn.MSELoss()
        self.predictive_span = 0

    def train(self, state, future_gravities):
        state_t = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        true_gravities_t = torch.tensor(future_gravities, device=device, dtype=torch.float32).unsqueeze(0)
        self.optimizer.zero_grad()
        predicted_gravities = self.model(state_t)
        loss = self.loss_fn(predicted_gravities, true_gravities_t)
        loss.backward()
        self.optimizer.step()

    def measure_predictive_span(self, state, true_future_gravities, accuracy_threshold=0.1):
        state_t = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            predictions = self.model(state_t).cpu().numpy().flatten()
        errors = np.abs(predictions - true_future_gravities) / (np.abs(true_future_gravities) + 1e-6)
        for i in range(self.horizon):
            if errors[i] > accuracy_threshold:
                self.predictive_span = i
                return self.predictive_span
        self.predictive_span = self.horizon
        return self.predictive_span

# --- Manifold Well (from advanced_ant_trainer) ---
class ManifoldWell:
    def __init__(self, action_dim, max_steps):
        self.action_dim = action_dim; self.max_steps = max_steps
        self.center = np.zeros(action_dim)
        self.phase = np.random.uniform(0, 2*np.pi, size=action_dim)
        self.frequency = np.random.uniform(0.5, 1.5, size=action_dim)
        self.amplitude = np.random.uniform(0.4, 0.8, size=action_dim)
    def step(self, t):
        time_factor = (2*np.pi*t)/self.max_steps
        self.center = self.amplitude * np.sin(self.frequency*time_factor + self.phase)
    def get_reward(self, action):
        distance = np.linalg.norm(action - self.center)
        alignment_bonus = MANIFOLD_BONUS_COEFF * math.exp(-2.0 * distance)
        tear_penalty = -MANIFOLD_TEAR_COEFF * max(0, distance - 1.0)
        return alignment_bonus + tear_penalty

# --- SAC Agent & Replay Buffer ---
class ReplayBuffer:
    def __init__(self,c):self.b=deque(maxlen=c)
    def push(self,s,a,r,s_,d):self.b.append((s,a,r,s_,d))
    def sample(self,B):return random.sample(self.b,B)
    def __len__(self):return len(self.b)
class Actor(nn.Module):
    def __init__(self,s,a,h=256):super().__init__();self.n=nn.Sequential(nn.Linear(s,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU());self.m=nn.Linear(h,a);self.ls=nn.Linear(h,a)
    def forward(self,s):x=self.n(s);return self.m(x),torch.clamp(self.ls(x),-20,2)
class Critic(nn.Module):
    def __init__(self,s,a,h=256):super().__init__();self.n=nn.Sequential(nn.Linear(s+a,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU(),nn.Linear(h,1))
    def forward(self,s,a):return self.n(torch.cat([s,a],1))

class SACAgent:
    def __init__(self,e,h=256,lr=3e-4,g=0.99,t=0.005,a=0.2):
        self.env=e;self.state_dim,self.action_dim=e.observation_space.shape[0],e.action_space.shape[0];self.gamma,self.tau,self.alpha=g,t,a
        self.action_scale=torch.tensor((e.action_space.high-e.action_space.low)/2.,device=device,dtype=torch.float32);self.action_bias=torch.tensor((e.action_space.high+e.action_space.low)/2.,device=device,dtype=torch.float32)
        self.actor=Actor(self.state_dim,self.action_dim,h).to(device);self.c1,self.c2=Critic(self.state_dim,self.action_dim,h).to(device),Critic(self.state_dim,self.action_dim,h).to(device)
        self.c1_t,self.c2_t=Critic(self.state_dim,self.action_dim,h).to(device),Critic(self.state_dim,self.action_dim,h).to(device);self.c1_t.load_state_dict(self.c1.state_dict());self.c2_t.load_state_dict(self.c2.state_dict())
        self.a_opt,self.c1_opt,self.c2_opt=optim.Adam(self.actor.parameters(),lr=lr),optim.Adam(self.c1.parameters(),lr=lr),optim.Adam(self.c2.parameters(),lr=lr)
        self.buffer=ReplayBuffer(1_000_000)

    # In the SACAgent class

    def select_action(self, s, eval=False):
        state_t = torch.tensor(s, device=device, dtype=torch.float32)
    
        # Add a batch dimension if the input is a single state
        is_single = state_t.dim() == 1
        if is_single:
            state_t = state_t.unsqueeze(0)

        mean, log_std = self.actor(state_t)
    
        if eval:
            action = torch.tanh(mean)
        else:
            dist = Normal(mean, log_std.exp())
            action = torch.tanh(dist.rsample())
        
        # Squeeze the batch dimension back out if the input was a single state
        if is_single:
            action = action.squeeze(0)
        
        return (action.cpu().detach().numpy() * self.action_scale.cpu().numpy()) + self.action_bias.cpu().numpy()

    def update(self,B):
        if len(self.buffer)<B:return
        s,a,r,s_,d=zip(*self.buffer.sample(B));s,a,r,s_,d=torch.tensor(np.array(s),device=device,dtype=torch.float32),torch.tensor(np.array(a),device=device,dtype=torch.float32),torch.tensor(np.array(r),device=device,dtype=torch.float32).unsqueeze(1),torch.tensor(np.array(s_),device=device,dtype=torch.float32),torch.tensor(np.array(d),device=device,dtype=torch.float32).unsqueeze(1)
        with torch.no_grad():
            m_,ls_=self.actor(s_);d_=Normal(m_,ls_.exp());z=d_.rsample();a_=torch.tanh(z);lp=d_.log_prob(z)-torch.log(1-a_.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
            tq1,tq2=self.c1_t(s_,a_),self.c2_t(s_,a_);tq=torch.min(tq1,tq2)-self.alpha*lp;tq=r+(1-d)*self.gamma*tq
        
        # --- BUG FIX: Critic update logic refactored for clarity and stability ---
        # 1. Calculate the loss for both critics
        cq1 = self.c1(s, a)
        cq2 = self.c2(s, a)
        critic_loss = F.mse_loss(cq1, tq) + F.mse_loss(cq2, tq)

        # 2. Optimize the critics
        self.c1_opt.zero_grad()
        self.c2_opt.zero_grad()
        critic_loss.backward()
        self.c1_opt.step()
        self.c2_opt.step()
        # --- End of fix ---

        m,ls=self.actor(s);d=Normal(m,ls.exp());z=d.rsample();a_pi=torch.tanh(z);lp=d.log_prob(z)-torch.log(1-a_pi.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
        q1_pi,q2_pi=self.c1(s,a_pi),self.c2(s,a_pi);min_q_pi=torch.min(q1_pi,q2_pi);al=(self.alpha*lp-min_q_pi).mean();self.a_opt.zero_grad();al.backward();self.a_opt.step()
        
        for t,s_p in zip(self.c1_t.parameters(),self.c1.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s_p.data*self.tau)
        for t,s_p in zip(self.c2_t.parameters(),self.c2.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s_p.data*self.tau)
        
    def save_model(self, rank):
        path = os.path.join(MODEL_PATH, f"rank_{rank}");os.makedirs(path, exist_ok=True)
        torch.save(self.actor.state_dict(), os.path.join(path, "actor.pth"))
        
    def genetic_crossover(self, high_scores_data):
        print("  > Performing genetic crossover...")
        sorted_scores = sorted(high_scores_data.items(), key=lambda item: item[0], reverse=True)
        parent_ranks = [data['rank'] for _, data in sorted_scores[:2]]
        if len(parent_ranks) < 2: print("  > Not enough parents for crossover."); return
        p1_weights = torch.load(os.path.join(MODEL_PATH, f"rank_{parent_ranks[0]}", "actor.pth"))
        p2_weights = torch.load(os.path.join(MODEL_PATH, f"rank_{parent_ranks[1]}", "actor.pth"))
        child_weights = OrderedDict()
        for key in p1_weights:
            if random.random() < GENE_TRANSFER_RATE: child_weights[key] = p1_weights[key].clone()
            else: child_weights[key] = (p1_weights[key] * 0.5 + p2_weights[key] * 0.5)
        self.actor.load_state_dict(child_weights)
        print("  > Crossover complete. New generation initiated.")

# --- The Hybrid FIT Trainer ---
class PirouetteFITTrainer:
    def __init__(self, env_name, num_episodes, max_steps):
        # --- Parallel Environment Setup ---
        def make_env(seed):
            def _init():
                env = CrucibleAntEnv(env_name, max_steps)
                env.reset(seed=seed)
                return env
            return _init

        num_cpu_cores = os.cpu_count() or 1
        self.num_envs = max(1, num_cpu_cores - 2)
        print(f"🚀 Creating {self.num_envs} parallel environments...")
        self.env = AsyncVectorEnv([make_env(SEED + i) for i in range(self.num_envs)])
        # --- End of Setup ---

        self.agent = SACAgent(self.env, lr=3e-4, a=0.2)
        self.prophet = Prophet(self.agent.state_dim, PROPHET_PREDICTION_HORIZON)
        
        # Create a list of components, one for each parallel environment
        self.manifold_wells = [ManifoldWell(self.agent.action_dim, max_steps) for _ in range(self.num_envs)]
        self.inversion_modes = [False] * self.num_envs

        self.num_episodes, self.max_steps = num_episodes, max_steps
        self.total_training_steps = num_episodes * max_steps
        self.batch_size = 256
        
        self.reward_history, self.eval_history, self.sigma_history = [], [], []
        self.high_scores, self.consecutive_bad_cycles = {}, 0
        self.last_sigma = 0
        self.current_delta_sigma = 0

    def train(self):
        start_time = time.time()
        s, _ = self.env.reset()
        
        global_step = 0
        while global_step * self.num_envs < self.total_training_steps:
            global_step += 1
            current_total_steps = global_step * self.num_envs

            # Select actions (now batched) and apply inversion if needed
            base_action = self.agent.select_action(s)
            action = base_action.copy()
            for i in range(self.num_envs):
                if self.inversion_modes[i]:
                    action[i] = -action[i]
            
            s_next, r_env, term, trunc, infos = self.env.step(action)
            
            # Get future physics states for the whole batch
            future_g_batch = np.array(self.env.call('get_future_gravity', PROPHET_PREDICTION_HORIZON))

            # Process results for each environment in the batch
            for i in range(self.num_envs):
                done = term[i] or trunc[i]
                
                self.prophet.train(s[i], future_g_batch[i])
                
                # Reward shaping from original script
                energy_cost = np.linalg.norm(action[i]) + 1e-6 
                flux_reward = FLUX_REWARD_WEIGHT * (self.current_delta_sigma / energy_cost)
                
                self.manifold_wells[i].step(global_step)
                r_manifold = self.manifold_wells[i].get_reward(action[i])
                
                action_magnitude = np.linalg.norm(action[i])
                risk_bonus = (action_magnitude - ACTION_MAGNITUDE_THRESHOLD) * RISK_REWARD_MULTIPLIER if action_magnitude > ACTION_MAGNITUDE_THRESHOLD else 0
                
                total_reward = r_env[i] + flux_reward + r_manifold + risk_bonus
                
                self.agent.buffer.push(s[i], action[i], total_reward, s_next[i], done)
                self.agent.update(self.batch_size)

                # Check for finished episodes to update inversion state
                if "_final_info" in infos and infos["_final_info"][i]:
                    ep_info = infos["final_info"][i]
                    ep_r_env = ep_info['episode']['r'][0]
                    steps_in_episode = ep_info['episode']['l'][0]
                    ep_r_env_normalized = ep_r_env / steps_in_episode if steps_in_episode > 0 else ep_r_env
                    self.inversion_modes[i] = True if ep_r_env_normalized < INVERSION_THRESHOLD and not self.inversion_modes[i] else False

            s = s_next

            # --- Evaluation and Management ---
            eval_step_trigger = EVAL_FREQUENCY * self.max_steps
            if current_total_steps % eval_step_trigger < self.num_envs:
                print(f"\n--- EVALUATION @ Step ~{current_total_steps // 1000}k ---")
                self.run_evaluation_and_manage_pool(current_total_steps // 1000)

                # Quiz the prophet and update delta_sigma for the next training segment
                current_sigma = self.prophet.measure_predictive_span(s_next[0], future_g_batch[0])
                self.sigma_history.append(current_sigma)
                print(f"  > Predictive Span (σ): {current_sigma:02d}/{PROPHET_PREDICTION_HORIZON}")
                self.current_delta_sigma = current_sigma - self.last_sigma
                self.last_sigma = current_sigma
        
        self.env.close()
        print(f"\nTraining finished in {time.time()-start_time:.2f}s.")
        self.plot_results()

    def run_evaluation_and_manage_pool(self, current_step_k):
        # Create a single, non-parallel environment for clean evaluation.
        eval_env = CrucibleAntEnv(ENV_NAME, self.max_steps)
        
        total_rewards, episode_lengths = [], []
        for i in range(EVAL_EPISODES):
            s_eval, _ = eval_env.reset(seed=SEED * 100 + i)
            ep_r, steps_taken = 0, 0
            for _ in range(self.max_steps):
                # Use the agent to select an action in evaluation mode.
                a = self.agent.select_action(s_eval, eval=True)
                s_eval, r, term, trunc, _ = eval_env.step(a)
                ep_r += r
                steps_taken += 1
                if term or trunc:
                    break
            # Normalize reward by steps taken, same as the original script.
            total_rewards.append(ep_r / steps_taken if steps_taken > 0 else ep_r)
            episode_lengths.append(steps_taken)
        
        current_eval_score = np.mean(total_rewards)
        eval_reward_std = np.std(total_rewards)
        self.eval_history.append(current_eval_score)
        
        best_pool_score = max(self.high_scores.keys()) if self.high_scores else -np.inf
        print(f"  > Eval Avg Score:{current_eval_score:8.2f} | Best in Pool:{best_pool_score:8.2f} | Std Dev:{eval_reward_std:.2f}")

        # --- Genetic Pool Management Logic (largely unchanged) ---
        is_stable = eval_reward_std <= MAX_ACCEPTABLE_STD
        if (len(self.high_scores) < GENETIC_POOL_SIZE or current_eval_score > min(self.high_scores.keys())) and is_stable:
            if len(self.high_scores) == GENETIC_POOL_SIZE:
                worst_score = min(self.high_scores.keys())
                worst_rank = self.high_scores.pop(worst_score)['rank']
                shutil.rmtree(os.path.join(MODEL_PATH, f"rank_{worst_rank}"), ignore_errors=True)
            
            used_ranks = {data['rank'] for data in self.high_scores.values()}
            new_rank = next(rank for rank in range(1, GENETIC_POOL_SIZE + 2) if rank not in used_ranks)
            self.high_scores[current_eval_score] = {'rank': new_rank}
            self.agent.save_model(new_rank)
            print(f"  > New stable model added to pool at rank {new_rank} with score {current_eval_score:.2f}")
        elif not is_stable:
            print(f"  > Score rejected due to instability (Std: {eval_reward_std:.2f})")

        # --- Crossover Trigger Logic (unchanged) ---
        if current_eval_score < best_pool_score * RESET_THRESHOLD:
            self.consecutive_bad_cycles += 1
            print(f"  > Performance below threshold. Bad cycles: {self.consecutive_bad_cycles}/{RESET_PATIENCE}")
        else:
            self.consecutive_bad_cycles = 0

        if self.consecutive_bad_cycles >= RESET_PATIENCE:
            print("\n  ! PERFORMANCE DEGRADED. INITIATING GENETIC TRANSFER !")
            self.agent.genetic_crossover(self.high_scores)
            self.consecutive_bad_cycles = 0

        # Close the temporary evaluation environment to release its resources.
        eval_env.close()

    def plot_results(self):
        fig, ax1 = plt.subplots(figsize=(15, 7))
        ax1.set_title("FIT Training: Task Reward vs. Predictive Span (σ)")
        ax1.set_xlabel("Episode")
        
        ax1.set_ylabel("Evaluation Score (Normalized)", color='tab:blue')
        eval_episodes = np.arange(EVAL_FREQUENCY, len(self.eval_history) * EVAL_FREQUENCY + 1, EVAL_FREQUENCY)
        ax1.plot(eval_episodes, self.eval_history, color='tab:blue', lw=2, label='Evaluation Score')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        
        ax2 = ax1.twinx()
        ax2.set_ylabel("Predictive Span (σ)", color='tab:red')
        sigma_episodes = np.arange(PROPHET_QUIZ_INTERVAL, len(self.sigma_history) * PROPHET_QUIZ_INTERVAL + 1, PROPHET_QUIZ_INTERVAL)
        ax2.plot(sigma_episodes, self.sigma_history, color='tab:red', linestyle='--', marker='o', label='Predictive Span (σ)')
        ax2.tick_params(axis='y', labelcolor='tab:red')
        
        fig.tight_layout(); plt.grid(True)
        save_path = "pirouette_fit_results.png"; plt.savefig(save_path)
        print(f"\nPlot saved to {save_path}")

# --- Main Execution ---
if __name__ == "__main__":
    trainer = PirouetteFITTrainer(ENV_NAME, NUM_EPISODES, MAX_STEPS_PER_EPISODE)
    trainer.train()