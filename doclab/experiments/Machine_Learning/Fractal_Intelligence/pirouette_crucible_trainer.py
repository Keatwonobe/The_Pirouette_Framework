# pirouette_crucible_trainer.py
# Augmentation of advanced_ant_trainer_9.py to test for Intelligence Flux.

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Normal
import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
from collections import deque, OrderedDict
import random
import time
import math
import os
import shutil

# --- Configuration ---
ENV_NAME = 'Ant-v5'
NUM_EPISODES = 2000 # Increased episodes for more complex learning
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 20 # Evaluate less frequently as Prophet quiz is expensive
EVAL_EPISODES = 5
SEED = 42
MODEL_PATH = "./pirouette_crucible_models/"

# --- Original Hyperparameters ---
MANIFOLD_BONUS_COEFF = 0.02
MANIFOLD_TEAR_COEFF = 0.05
RESET_THRESHOLD = 0.7
RESET_PATIENCE = 10 # More patience for the harder task
INVERSION_THRESHOLD = -1000
GENETIC_POOL_SIZE = 10
GENE_TRANSFER_RATE = 0.6

# --- NEW: Intelligence Flux Hyperparameters ---
FLUX_REWARD_WEIGHT = 0.5 # Weight for the intelligence flux bonus
PROPHET_QUIZ_INTERVAL = 10 # Episodes between Prophet quizzes
PROPHET_PREDICTION_HORIZON = 50 # How many steps into the future to predict

# Set device and seeds
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
if os.path.exists(MODEL_PATH):
    shutil.rmtree(MODEL_PATH)
os.makedirs(MODEL_PATH, exist_ok=True)
print(f"Using device: {device}")
print(f"Crucible models will be saved in: {MODEL_PATH}")

### --- NEW: Crucible Environment with Hidden Physics --- ###
class CrucibleAntEnv:
    """A wrapper for the Ant environment that introduces hidden, learnable physics."""
    def __init__(self, env_name, max_steps):
        print("Initializing Crucible Environment...")
        self.env = gym.make(env_name, render_mode=None)
        self.max_steps_per_episode = max_steps
        self.current_step = 0
        
        # Hidden Physics Parameters: Oscillating Gravity
        self.gravity_period = self.max_steps_per_episode * 2 # Long period makes it non-obvious
        self.gravity_amplitude = -9.8 # Base gravity
        self.gravity_oscillation_amplitude = 4.0 # How much gravity fluctuates
        
        self.observation_space = self.env.observation_space
        self.action_space = self.env.action_space

    def reset(self, seed=None):
        self.current_step = 0
        self.update_gravity() # Set initial gravity
        return self.env.reset(seed=seed)

    def step(self, action):
        self.current_step += 1
        self.update_gravity()
        return self.env.step(action)

    def update_gravity(self):
        """Applies the oscillating gravity to the underlying simulation."""
        phase = (2 * np.pi * self.current_step) / self.gravity_period
        current_gravity = self.gravity_amplitude + self.gravity_oscillation_amplitude * np.sin(phase)
        self.env.unwrapped.model.opt.gravity[2] = current_gravity
    
    def get_future_gravity(self, future_steps):
        """Predicts the gravity for N future steps. Used by the Prophet."""
        future_gravities = []
        for i in range(1, future_steps + 1):
            future_step = self.current_step + i
            phase = (2 * np.pi * future_step) / self.gravity_period
            g = self.gravity_amplitude + self.gravity_oscillation_amplitude * np.sin(phase)
            future_gravities.append(g)
        return np.array(future_gravities)

### --- NEW: Prophet Module for Measuring Predictive Span (σ) --- ###
class Prophet:
    def __init__(self, state_dim, horizon):
        self.horizon = horizon
        # The Prophet is a simple feed-forward network that learns to predict physics
        self.model = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, horizon) # Predicts 'horizon' steps ahead
        ).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        self.loss_fn = nn.MSELoss()
        self.predictive_span = 0 # σ value

    def train(self, state, future_gravities):
        """Train the Prophet model on a single data point."""
        state_t = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        true_gravities_t = torch.tensor(future_gravities, device=device, dtype=torch.float32).unsqueeze(0)
        
        self.optimizer.zero_grad()
        predicted_gravities = self.model(state_t)
        loss = self.loss_fn(predicted_gravities, true_gravities_t)
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def measure_predictive_span(self, state, true_future_gravities, accuracy_threshold=0.1):
        """Quiz the agent's internal model and return its predictive span (σ)."""
        state_t = torch.tensor(state, device=device, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            predictions = self.model(state_t).cpu().numpy().flatten()
        
        errors = np.abs(predictions - true_future_gravities) / np.abs(true_future_gravities)
        
        # Find the first point where the prediction is wrong
        for i in range(self.horizon):
            if errors[i] > accuracy_threshold:
                self.predictive_span = i
                return self.predictive_span
        
        self.predictive_span = self.horizon # Perfect prediction
        return self.predictive_span

# --- Existing SAC Agent (Unchanged) ---
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
        self.action_scale=torch.tensor((e.action_space.high-e.action_space.low)/2.,device=device,dtype=torch.float32)
        self.action_bias=torch.tensor((e.action_space.high+e.action_space.low)/2.,device=device,dtype=torch.float32)
        self.actor=Actor(self.state_dim,self.action_dim,h).to(device);self.c1,self.c2=Critic(self.state_dim,self.action_dim,h).to(device),Critic(self.state_dim,self.action_dim,h).to(device)
        self.c1_t,self.c2_t=Critic(self.state_dim,self.action_dim,h).to(device),Critic(self.state_dim,self.action_dim,h).to(device)
        self.c1_t.load_state_dict(self.c1.state_dict());self.c2_t.load_state_dict(self.c2.state_dict())
        self.a_opt,self.c1_opt,self.c2_opt=optim.Adam(self.actor.parameters(),lr=lr),optim.Adam(self.c1.parameters(),lr=lr),optim.Adam(self.c2.parameters(),lr=lr)
        self.buffer=ReplayBuffer(1_000_000);self.td_errors=deque(maxlen=5000)
    def select_action(self,s,eval=False):
        s=torch.tensor(s,device=device,dtype=torch.float32).unsqueeze(0)
        m,ls=self.actor(s)
        a=torch.tanh(m) if eval else torch.tanh(Normal(m,ls.exp()).rsample())
        return(a.cpu().detach().numpy()[0]*self.action_scale.cpu().numpy())+self.action_bias.cpu().numpy()
    def update(self,B):
        if len(self.buffer)<B:return
        s,a,r,s_,d=zip(*self.buffer.sample(B));s,a,r,s_,d=torch.tensor(np.array(s),device=device,dtype=torch.float32),torch.tensor(np.array(a),device=device,dtype=torch.float32),torch.tensor(np.array(r),device=device,dtype=torch.float32).unsqueeze(1),torch.tensor(np.array(s_),device=device,dtype=torch.float32),torch.tensor(np.array(d),device=device,dtype=torch.float32).unsqueeze(1)
        with torch.no_grad():
            m_,ls_=self.actor(s_);d_=Normal(m_,ls_.exp());z=d_.rsample();a_=torch.tanh(z);lp=d_.log_prob(z)-torch.log(1-a_.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
            tq1,tq2=self.c1_t(s_,a_),self.c2_t(s_,a_);tq=torch.min(tq1,tq2)-self.alpha*lp;tq=r+(1-d)*self.gamma*tq
        cq1,cq2=self.c1(s,a),self.c2(s,a);self.td_errors.append((F.mse_loss(cq1,tq)+F.mse_loss(cq2,tq)).detach().cpu().item());c1l,c2l=F.mse_loss(cq1,tq),F.mse_loss(cq2,tq)
        self.c1_opt.zero_grad();c1l.backward();self.c1_opt.step();self.c2_opt.zero_grad();c2l.backward();self.c2_opt.step()
        m,ls=self.actor(s);d=Normal(m,ls.exp());z=d.rsample();a_pi=torch.tanh(z);lp=d.log_prob(z)-torch.log(1-a_pi.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
        q1_pi,q2_pi=self.c1(s,a_pi),self.c2(s,a_pi);min_q_pi=torch.min(q1_pi,q2_pi);al=(self.alpha*lp-min_q_pi).mean();self.a_opt.zero_grad();al.backward();self.a_opt.step()
        for t,s_p in zip(self.c1_t.parameters(),self.c1.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s_p.data*self.tau)
        for t,s_p in zip(self.c2_t.parameters(),self.c2.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s_p.data*self.tau)
    def save_model(self, rank):
        path = os.path.join(MODEL_PATH, f"rank_{rank}"); os.makedirs(path, exist_ok=True)
        torch.save(self.actor.state_dict(), os.path.join(path, "actor.pth"))
    def genetic_crossover(self, high_scores_data):
        print("  > Performing genetic crossover...")
        sorted_scores = sorted(high_scores_data.items(), key=lambda item: item[0], reverse=True)
        parent_ranks = [data['rank'] for _, data in sorted_scores[:2]]
        if len(parent_ranks) < 2: print("  > Not enough parents."); return
        p1_actor = torch.load(os.path.join(MODEL_PATH, f"rank_{parent_ranks[0]}", "actor.pth"))
        p2_actor = torch.load(os.path.join(MODEL_PATH, f"rank_{parent_ranks[1]}", "actor.pth"))
        child_dict = OrderedDict()
        for key in p1_actor:
            if random.random() < GENE_TRANSFER_RATE: child_dict[key] = p1_actor[key].clone()
            else: child_dict[key] = (p1_actor[key].clone() * 0.5 + p2_actor[key].clone() * 0.5)
        self.actor.load_state_dict(child_dict)
        print("  > Crossover complete.")

# --- Trainer, now with Flux-seeking behavior ---
class PirouetteCrucibleTrainer:
    def __init__(self, env_name, num_episodes, max_steps):
        self.env = CrucibleAntEnv(env_name, max_steps)
        self.agent = SACAgent(self.env, lr=3e-4, a=0.2)
        self.prophet = Prophet(self.agent.state_dim, PROPHET_PREDICTION_HORIZON)
        
        self.num_episodes, self.max_steps, self.batch_size = num_episodes, max_steps, 256
        self.reward_history, self.eval_history, self.sigma_history = [], [], []
        
        self.high_scores = {} 
        self.consecutive_bad_cycles = 0
        self.last_sigma = 0

    def train(self):
        start_time = time.time()
        for ep in range(1, self.num_episodes + 1):
            s, _ = self.env.reset(seed=SEED + ep)
            ep_r_env, ep_actions_taken = 0, 0
            
            for step in range(1, self.max_steps + 1):
                a = self.agent.select_action(s)
                s_, r_env, term, trunc, info = self.env.step(a) 
                done = term or trunc
                
                # --- NEW: Flux Reward Calculation ---
                # 1. Train the Prophet's model on the current state
                future_g = self.env.get_future_gravity(PROPHET_PREDICTION_HORIZON)
                self.prophet.train(s, future_g)

                # 2. Calculate the Flux Reward
                delta_sigma = self.prophet.predictive_span - self.last_sigma
                # Energy cost is simplified to action magnitude
                energy_cost = np.linalg.norm(a) + 1e-6 
                # Intelligence Flux (Phi)
                flux = delta_sigma / energy_cost 
                flux_reward = FLUX_REWARD_WEIGHT * flux
                
                total_reward = r_env + flux_reward
                
                self.agent.buffer.push(s, a, total_reward, s_, done)
                self.agent.update(self.batch_size)
                
                s = s_; ep_r_env += r_env; ep_actions_taken += 1
                if done: break
            
            self.reward_history.append(ep_r_env)

            if ep % PROPHET_QUIZ_INTERVAL == 0:
                # --- NEW: Periodically measure predictive span ---
                current_sigma = self.prophet.measure_predictive_span(s, self.env.get_future_gravity(PROPHET_PREDICTION_HORIZON))
                self.sigma_history.append(current_sigma)
                print(f"Ep:{ep:04d} | Env Reward:{ep_r_env:8.2f} | Predictive Span (σ): {current_sigma:02d}/{PROPHET_PREDICTION_HORIZON}")
                self.last_sigma = current_sigma

            if ep % EVAL_FREQUENCY == 0:
                self.run_evaluation(ep)

        print(f"\nTraining finished in {time.time()-start_time:.2f}s.")
        self.plot_results()

    def run_evaluation(self, ep):
        eval_rewards = []
        for i in range(EVAL_EPISODES):
            s, _ = self.env.reset(seed=SEED * 100 + i)
            ep_r = 0
            for _ in range(self.max_steps):
                a = self.agent.select_action(s, eval=True)
                s, r, term, trunc, _ = self.env.step(a)
                ep_r += r
                if term or trunc: break
            eval_rewards.append(ep_r)
        
        avg_eval_score = np.mean(eval_rewards)
        self.eval_history.append(avg_eval_score)
        
        # Genetic pool management
        if len(self.high_scores) < GENETIC_POOL_SIZE or avg_eval_score > min(self.high_scores.keys()):
            if len(self.high_scores) == GENETIC_POOL_SIZE:
                worst_score = min(self.high_scores.keys())
                del self.high_scores[worst_score]
            
            rank = len(self.high_scores) + 1
            self.high_scores[avg_eval_score] = {'rank': rank}
            self.agent.save_model(rank)
            print(f"  > New high score added to pool. Rank {rank} | Score: {avg_eval_score:.2f}")

        # Check for performance degradation and trigger crossover
        best_known_score = max(self.high_scores.keys()) if self.high_scores else 0
        if avg_eval_score < best_known_score * RESET_THRESHOLD:
            self.consecutive_bad_cycles += 1
        else:
            self.consecutive_bad_cycles = 0

        if self.consecutive_bad_cycles >= RESET_PATIENCE:
            print("\n  ! PERFORMANCE DEGRADED. INITIATING GENETIC TRANSFER !")
            self.agent.genetic_crossover(self.high_scores)
            self.consecutive_bad_cycles = 0

    def plot_results(self):
        fig, ax1 = plt.subplots(figsize=(15, 7))
        ax1.set_title("Crucible Training: Task Reward vs. Predictive Span (σ)")
        ax1.set_xlabel("Episode")
        
        # Plot Rewards
        ax1.set_ylabel("Evaluation Reward", color='tab:blue')
        eval_episodes = np.arange(EVAL_FREQUENCY, self.num_episodes + 1, EVAL_FREQUENCY)
        ax1.plot(eval_episodes, self.eval_history, color='tab:blue', lw=2, label='Evaluation Score')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        
        # Plot Predictive Span (σ)
        ax2 = ax1.twinx()
        ax2.set_ylabel("Predictive Span (σ)", color='tab:red')
        sigma_episodes = np.arange(PROPHET_QUIZ_INTERVAL, self.num_episodes + 1, PROPHET_QUIZ_INTERVAL)
        ax2.plot(sigma_episodes, self.sigma_history, color='tab:red', linestyle='--', marker='o', label='Predictive Span (σ)')
        ax2.tick_params(axis='y', labelcolor='tab:red')
        
        fig.tight_layout()
        plt.grid(True)
        save_path = "pirouette_crucible_results.png"
        plt.savefig(save_path)
        print(f"\nPlot saved to {save_path}")

# --- Main Execution ---
if __name__ == "__main__":
    trainer = PirouetteCrucibleTrainer(ENV_NAME, NUM_EPISODES, MAX_STEPS_PER_EPISODE)
    trainer.train()