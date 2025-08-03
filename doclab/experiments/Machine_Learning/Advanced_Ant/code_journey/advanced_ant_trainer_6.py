# pirouette_manifold_trainer.py

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Normal
import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
from collections import deque
import random
import time
import math
import os
import pywt # PyWavelets dependency

# --- Configuration ---
ENV_NAME = 'Ant-v5'
NUM_EPISODES = 500
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 20 # Evaluate and analyze every 20 episodes
EVAL_EPISODES = 10  # Number of episodes to run for formal evaluation
SEED = 42
MODEL_PATH = "./pirouette_models/"

# --- Hyperparameters ---
MANIFOLD_BONUS_COEFF = 0.02 # Reward for aligning with the well
MANIFOLD_TEAR_COEFF = 0.05  # Penalty for tearing the manifold (straying far)
RESET_THRESHOLD = 0.7       # Reset if performance drops below 70% of peak
RESET_PATIENCE = 3          # Number of bad eval cycles before resetting

# Set device and seeds
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
os.makedirs(MODEL_PATH, exist_ok=True)
print(f"Using device: {device}")
print(f"Models will be saved in: {MODEL_PATH}")

# --- UTILS (HFD, Analytics, Shadow Detector) ---
def calculate_hfd(series):
    L, x, N = [], [], len(series)
    if N < 20: return 1.0
    for k in range(1, 10):
        Lk = sum(np.sum(np.abs(np.diff(series[m::k])))*(N-1)/((len(series[m::k])-1)*k) for m in range(k) if len(series[m::k])>1)
        if Lk > 0: L.append(np.log(Lk/k)); x.append(np.log(1.0/k))
    return np.polyfit(x, L, 1)[0] if L else 1.0

class ContinuousShadowRegionDetector:
    def analyze_and_suggest(self, td_errors):
        if td_errors is None or len(td_errors) < 50: return {}
        
        # Using HFD of TD-errors as a proxy for learning stability
        hfd = calculate_hfd(td_errors)
        suggestions, mean_error = {}, np.mean(td_errors)
        
        print(f"  [Shadow Analysis] TD-Error HFD: {hfd:.4f}, Avg Error: {mean_error:.4f}", end=" ")
        
        if hfd > 1.9:
            print("Mode: Unstable Learning -> Increasing Stability")
            suggestions.update({'critic_lr': 1e-5, 'actor_lr': 1e-5, 'alpha': 0.05})
        elif hfd < 1.6 and mean_error > 0.5:
            print("Mode: Stagnant Learning -> Encouraging Exploration")
            suggestions.update({'critic_lr': 3e-4, 'actor_lr': 3e-4, 'alpha': 0.3})
        else:
            print("Mode: Stable Learning -> Standard Update")
            suggestions.update({'critic_lr': 5e-5, 'actor_lr': 5e-5, 'alpha': 0.1})
            
        return suggestions

# --- Manifold Well (The "Hot Spot" Problem) ---
class ManifoldWell:
    def __init__(self, action_dim, max_steps):
        self.action_dim = action_dim
        self.max_steps = max_steps
        self.center = np.zeros(action_dim)
        # Parameters to make the well move smoothly but unpredictably
        self.phase = np.random.uniform(0, 2 * np.pi, size=action_dim)
        self.frequency = np.random.uniform(0.5, 1.5, size=action_dim)
        self.amplitude = np.random.uniform(0.4, 0.8, size=action_dim)

    def step(self, t):
        """Updates the well's center for the current timestep t."""
        time_factor = (2 * np.pi * t) / self.max_steps
        self.center = self.amplitude * np.sin(self.frequency * time_factor + self.phase)

    def get_reward(self, action):
        """Calculates bonus/penalty based on action's proximity to the well center."""
        distance = np.linalg.norm(action - self.center)
        
        # Reward for being close to the center (aligning the manifold)
        alignment_bonus = MANIFOLD_BONUS_COEFF * math.exp(-2.0 * distance)
        
        # Penalty for being too far (tearing the manifold)
        tear_threshold = 1.0 # Actions further than this distance are penalized
        tear_penalty = -MANIFOLD_TEAR_COEFF * max(0, distance - tear_threshold)
        
        return alignment_bonus + tear_penalty

# --- SAC Agent ---
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
        if eval:
            a=torch.tanh(m)
        else:
            d=Normal(m,ls.exp());a=torch.tanh(d.rsample())
        return(a.cpu().detach().numpy()[0]*self.action_scale.cpu().numpy())+self.action_bias.cpu().numpy()

    def update(self,B):
        if len(self.buffer)<B:return
        s,a,r,s_,d=zip(*self.buffer.sample(B));s,a,r,s_,d=torch.tensor(np.array(s),device=device,dtype=torch.float32),torch.tensor(np.array(a),device=device,dtype=torch.float32),torch.tensor(np.array(r),device=device,dtype=torch.float32).unsqueeze(1),torch.tensor(np.array(s_),device=device,dtype=torch.float32),torch.tensor(np.array(d),device=device,dtype=torch.float32).unsqueeze(1)
        with torch.no_grad():
            m_,ls_=self.actor(s_);d_=Normal(m_,ls_.exp());z=d_.rsample();a_=torch.tanh(z);lp=d_.log_prob(z)-torch.log(1-a_.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
            tq1,tq2=self.c1_t(s_,a_),self.c2_t(s_,a_);tq=torch.min(tq1,tq2)-self.alpha*lp;tq=r+(1-d)*self.gamma*tq
        cq1,cq2=self.c1(s,a),self.c2(s,a);td_error_val=(F.mse_loss(cq1,tq)+F.mse_loss(cq2,tq)).detach().cpu().item();self.td_errors.append(td_error_val);c1l,c2l=F.mse_loss(cq1,tq),F.mse_loss(cq2,tq)
        self.c1_opt.zero_grad();c1l.backward();self.c1_opt.step();self.c2_opt.zero_grad();c2l.backward();self.c2_opt.step()
        m,ls=self.actor(s);d=Normal(m,ls.exp());z=d.rsample();a_pi=torch.tanh(z);lp=d.log_prob(z)-torch.log(1-a_pi.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
        q1_pi,q2_pi=self.c1(s,a_pi),self.c2(s,a_pi);min_q_pi=torch.min(q1_pi,q2_pi);al=(self.alpha*lp-min_q_pi).mean();self.a_opt.zero_grad();al.backward();self.a_opt.step()
        for t,s_p in zip(self.c1_t.parameters(),self.c1.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s_p.data*self.tau)
        for t,s_p in zip(self.c2_t.parameters(),self.c2.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s_p.data*self.tau)

    def apply_suggestions(self,sg):
        if not sg: return
        print(f"  > Applying suggestions...")
        if 'critic_lr' in sg:
            new_lr = sg['critic_lr']
            for g in self.c1_opt.param_groups: g['lr'] = new_lr
            for g in self.c2_opt.param_groups: g['lr'] = new_lr
        if 'actor_lr' in sg: self.a_opt.param_groups[0]['lr'] = sg['actor_lr']
        if 'alpha' in sg: self.alpha = sg['alpha']

    def save_models(self, path):
        torch.save(self.actor.state_dict(), os.path.join(path, "best_actor.pth"))
        torch.save(self.c1.state_dict(), os.path.join(path, "best_critic1.pth"))
        torch.save(self.c2.state_dict(), os.path.join(path, "best_critic2.pth"))
        print(f"  > Saved new best models to {path}")

    def load_models(self, path):
        self.actor.load_state_dict(torch.load(os.path.join(path, "best_actor.pth")))
        self.c1.load_state_dict(torch.load(os.path.join(path, "best_critic1.pth")))
        self.c2.load_state_dict(torch.load(os.path.join(path, "best_critic2.pth")))
        # It's crucial to also sync the target networks after loading
        self.c1_t.load_state_dict(self.c1.state_dict())
        self.c2_t.load_state_dict(self.c2.state_dict())
        print(f"  > Loaded high-water-mark models from {path}")


# --- Trainer with Manifold and High-Water-Mark Logic ---
class PirouetteTrainer:
    def __init__(self, env_name, num_episodes, max_steps):
        self.env = gym.make(env_name)
        self.agent = SACAgent(self.env, lr=5e-5, a=0.1) # Start with stable params
        self.shadow_detector = ContinuousShadowRegionDetector()
        self.manifold_well = ManifoldWell(self.agent.action_dim, max_steps)
        
        self.num_episodes = num_episodes
        self.max_steps = max_steps
        self.batch_size = 256
        self.reward_history = []
        
        # High-Water-Mark attributes
        self.best_eval_score = -np.inf
        self.eval_reward_buffer = deque(maxlen=RESET_PATIENCE)
        self.consecutive_bad_cycles = 0

    def train(self):
        start_time = time.time()
        for ep in range(self.num_episodes):
            s, _ = self.env.reset(seed=SEED + ep)
            ep_r_env, ep_r_manifold = 0, 0
            
            for step in range(self.max_steps):
                a = self.agent.select_action(s)
                s_, r_env, term, trunc, _ = self.env.step(a)
                done = term or trunc
                
                # Update manifold well and get structural reward
                self.manifold_well.step(step)
                r_manifold = self.manifold_well.get_reward(a)
                
                total_reward = r_env + r_manifold
                
                self.agent.buffer.push(s, a, total_reward, s_, done)
                self.agent.update(self.batch_size)
                
                s = s_
                ep_r_env += r_env
                ep_r_manifold += r_manifold
                if done: break

            self.reward_history.append(ep_r_env)
            print(f"Ep:{ep+1:03d} | Env Rw:{ep_r_env:7.1f} | Manifold Rw: {ep_r_manifold:6.2f} | Steps: {step+1}")
            
            if (ep + 1) % EVAL_FREQUENCY == 0:
                self.run_evaluation_and_analysis()

        print(f"\nTraining finished in {time.time()-start_time:.2f}s.")
        self.plot_rewards()

    def run_evaluation_and_analysis(self):
        print("\n" + "="*20 + " EVALUATION & ANALYSIS " + "="*20)
        total_rewards = []
        for i in range(EVAL_EPISODES):
            s, _ = self.env.reset(seed=SEED * 100 + i)
            ep_r, done = 0, False
            for _ in range(self.max_steps):
                a = self.agent.select_action(s, eval=True)
                s, r, term, trunc, _ = self.env.step(a)
                done = term or trunc
                ep_r += r
                if done: break
            total_rewards.append(ep_r)
        
        current_eval_score = np.mean(total_rewards)
        print(f"  > Evaluation Score: {current_eval_score:.2f} (Best: {self.best_eval_score:.2f})")

        # High-Water-Mark Check
        if current_eval_score > self.best_eval_score:
            self.best_eval_score = current_eval_score
            self.agent.save_models(MODEL_PATH)
            self.consecutive_bad_cycles = 0 # Reset patience on new best
        else:
            if current_eval_score < self.best_eval_score * RESET_THRESHOLD:
                self.consecutive_bad_cycles += 1
                print(f"  > Performance below threshold. Bad cycles: {self.consecutive_bad_cycles}/{RESET_PATIENCE}")
            else:
                self.consecutive_bad_cycles = 0 # Reset if performance recovers above threshold

        if self.consecutive_bad_cycles >= RESET_PATIENCE:
            print("\n  ! PERFORMANCE DEGRADED. RESETTING TO HIGH-WATER-MARK POLICY. !")
            self.agent.load_models(MODEL_PATH)
            self.consecutive_bad_cycles = 0 # Reset patience after loading

        # Run Shadow Analysis
        suggestions = self.shadow_detector.analyze_and_suggest(np.array(self.agent.td_errors))
        self.agent.apply_suggestions(suggestions)
        print("="*63 + "\n")

    def plot_rewards(self):
        plt.figure(figsize=(15, 7))
        plt.title("Agent Reward Progress (Environment Reward)")
        plt.plot(self.reward_history, label='Episodic Reward', alpha=0.8)
        
        # Add a moving average to see the trend
        if len(self.reward_history) >= 20:
            moving_avg = np.convolve(self.reward_history, np.ones(20)/20, mode='valid')
            plt.plot(np.arange(19, len(self.reward_history)), moving_avg, color='red', lw=2, label='20-episode SMA')
            
        plt.xlabel("Episode")
        plt.ylabel("Total Environment Reward")
        plt.legend()
        plt.grid(True)
        save_path = "pirouette_manifold_rewards.png"
        plt.savefig(save_path)
        print(f"\nPlot saved to {save_path}")

# --- Main Execution ---
if __name__ == "__main__":
    trainer = PirouetteTrainer(ENV_NAME, NUM_EPISODES, MAX_STEPS_PER_EPISODE)
    trainer.train()