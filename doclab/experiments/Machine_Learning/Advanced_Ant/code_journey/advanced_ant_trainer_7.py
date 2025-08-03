# pirouette_genetic_trainer.py

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
NUM_EPISODES = 500
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 20
EVAL_EPISODES = 10
SEED = 42
MODEL_PATH = "./pirouette_genetic_models/"

# --- Hyperparameters ---
MANIFOLD_BONUS_COEFF = 0.02
MANIFOLD_TEAR_COEFF = 0.05
RESET_THRESHOLD = 0.7
RESET_PATIENCE = 3
INVERSION_THRESHOLD = -1000 # Invert actions if episode score is this low
GENETIC_POOL_SIZE = 3 # Keep top 3 models for crossover

# Set device and seeds
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
if os.path.exists(MODEL_PATH):
    shutil.rmtree(MODEL_PATH) # Clean slate for new model pool
os.makedirs(MODEL_PATH, exist_ok=True)
print(f"Using device: {device}")
print(f"Top {GENETIC_POOL_SIZE} models will be saved in: {MODEL_PATH}")

# --- UTILS (Shadow Detector is now simplified) ---
class ShadowStabilityDetector:
    def analyze_and_suggest(self, td_errors):
        if not td_errors: return {}
        suggestions = {}
        avg_td_error = np.mean(td_errors)
        print(f"  [Shadow Analysis] Avg TD-Error: {avg_td_error:.4f}", end=" ")
        
        # Simple heuristic: if errors are high, be more conservative. If low, explore more.
        if avg_td_error > 1.0:
            print("Mode: Unstable -> Reducing learning rate")
            suggestions.update({'critic_lr': 5e-5, 'actor_lr': 5e-5, 'alpha': 0.1})
        else:
            print("Mode: Stable -> Standard learning rate")
            suggestions.update({'critic_lr': 3e-4, 'actor_lr': 3e-4, 'alpha': 0.2})
        return suggestions

# --- Manifold Well (The "Hot Spot" Problem) ---
class ManifoldWell:
    def __init__(self, action_dim, max_steps):
        self.action_dim = action_dim
        self.max_steps = max_steps
        self.center = np.zeros(action_dim)
        self.phase = np.random.uniform(0, 2 * np.pi, size=action_dim)
        self.frequency = np.random.uniform(0.5, 1.5, size=action_dim)
        self.amplitude = np.random.uniform(0.4, 0.8, size=action_dim)

    def step(self, t):
        time_factor = (2 * np.pi * t) / self.max_steps
        self.center = self.amplitude * np.sin(self.frequency * time_factor + self.phase)

    def get_reward(self, action):
        distance = np.linalg.norm(action - self.center)
        alignment_bonus = MANIFOLD_BONUS_COEFF * math.exp(-2.0 * distance)
        tear_penalty = -MANIFOLD_TEAR_COEFF * max(0, distance - 1.0)
        return alignment_bonus + tear_penalty

# --- SAC Agent with Genetic Crossover ---
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

    def apply_suggestions(self,sg):
        if not sg: return
        print(f"  > Applying suggestions...")
        if 'critic_lr' in sg:
            new_lr = sg['critic_lr']; [g.update(lr=new_lr) for g in self.c1_opt.param_groups]; [g.update(lr=new_lr) for g in self.c2_opt.param_groups]
        if 'actor_lr' in sg: self.a_opt.param_groups[0]['lr'] = sg['actor_lr']
        if 'alpha' in sg: self.alpha = sg['alpha']

    def save_model(self, rank):
        path = os.path.join(MODEL_PATH, f"rank_{rank}")
        os.makedirs(path, exist_ok=True)
        torch.save(self.actor.state_dict(), os.path.join(path, "actor.pth"))
        torch.save(self.c1.state_dict(), os.path.join(path, "critic1.pth"))

    def load_model(self, rank):
        path = os.path.join(MODEL_PATH, f"rank_{rank}")
        self.actor.load_state_dict(torch.load(os.path.join(path, "actor.pth")))
        self.c1.load_state_dict(torch.load(os.path.join(path, "critic1.pth")))
        # It's crucial to also sync the other networks after loading
        self.c2.load_state_dict(self.c1.state_dict())
        self.c1_t.load_state_dict(self.c1.state_dict())
        self.c2_t.load_state_dict(self.c2.state_dict())

    def genetic_crossover(self, high_scores):
        print("  > Performing genetic crossover...")
        parent_models = {'actor': [], 'critic1': []}
        parent_scores = []

        # Load parent models and their scores
        for score, rank in high_scores.items():
            path = os.path.join(MODEL_PATH, f"rank_{rank}")
            if os.path.exists(path):
                parent_scores.append(score)
                parent_models['actor'].append(torch.load(os.path.join(path, "actor.pth")))
                parent_models['critic1'].append(torch.load(os.path.join(path, "critic1.pth")))
        
        if not parent_scores:
            print("  > No parent models found for crossover. Skipping.")
            return

        # Perform weighted average of weights
        for model_name in ['actor', 'critic1']:
            avg_state_dict = OrderedDict()
            total_score = sum(parent_scores)
            weights = [s / total_score for s in parent_scores]

            for i, state_dict in enumerate(parent_models[model_name]):
                for key, value in state_dict.items():
                    if i == 0:
                        avg_state_dict[key] = value.clone() * weights[i]
                    else:
                        avg_state_dict[key] += value.clone() * weights[i]
            
            # Load the new "child" state dict
            getattr(self, model_name).load_state_dict(avg_state_dict)

        # Sync all other networks from the new child
        self.c2.load_state_dict(self.c1.state_dict())
        self.c1_t.load_state_dict(self.c1.state_dict())
        self.c2_t.load_state_dict(self.c2.state_dict())
        print("  > Crossover complete. Agent now has combined genetics.")


# --- Trainer with Genetic Memory and Action Inversion ---
class PirouetteTrainer:
    def __init__(self, env_name, num_episodes, max_steps):
        self.env = gym.make(env_name)
        self.agent = SACAgent(self.env, lr=3e-4, a=0.2)
        self.shadow_detector = ShadowStabilityDetector()
        self.manifold_well = ManifoldWell(self.agent.action_dim, max_steps)
        self.num_episodes, self.max_steps, self.batch_size = num_episodes, max_steps, 256
        self.reward_history = []
        
        # High-Water-Mark & Genetic attributes
        self.high_scores = {} # {score: rank}
        self.consecutive_bad_cycles = 0
        self.inversion_mode = False

    def train(self):
        start_time = time.time()
        for ep in range(self.num_episodes):
            s, _ = self.env.reset(seed=SEED + ep)
            ep_r_env, ep_r_manifold = 0, 0
            
            if self.inversion_mode:
                print("  -> Episode in ACTION INVERSION mode.")

            for step in range(self.max_steps):
                a = self.agent.select_action(s)
                if self.inversion_mode:
                    a = -a # Invert the action
                
                s_, r_env, term, trunc, _ = self.env.step(a)
                done = term or trunc
                
                self.manifold_well.step(step)
                r_manifold = self.manifold_well.get_reward(a)
                total_reward = r_env + r_manifold
                
                self.agent.buffer.push(s, a, total_reward, s_, done)
                self.agent.update(self.batch_size)
                
                s = s_; ep_r_env += r_env; ep_r_manifold += r_manifold
                if done: break
            
            self.reward_history.append(ep_r_env)
            print(f"Ep:{ep+1:03d} | Env Rw:{ep_r_env:7.1f} | Manifold Rw: {ep_r_manifold:6.2f} | Steps: {step+1}")

            # Check for action inversion trigger
            if ep_r_env < INVERSION_THRESHOLD and not self.inversion_mode:
                self.inversion_mode = True
            else:
                self.inversion_mode = False

            if (ep + 1) % EVAL_FREQUENCY == 0:
                self.run_evaluation_and_analysis()

        print(f"\nTraining finished in {time.time()-start_time:.2f}s.")
        self.plot_rewards()

    def manage_high_scores(self, new_score):
        if len(self.high_scores) < GENETIC_POOL_SIZE or new_score > min(self.high_scores.keys()):
            # If the pool isn't full or the new score is better than the worst in the pool
            if len(self.high_scores) == GENETIC_POOL_SIZE:
                worst_score = min(self.high_scores.keys())
                worst_rank = self.high_scores.pop(worst_score)
                shutil.rmtree(os.path.join(MODEL_PATH, f"rank_{worst_rank}"), ignore_errors=True)
            
            # Find an available rank
            new_rank = 1
            while new_rank in self.high_scores.values():
                new_rank += 1
            
            self.high_scores[new_score] = new_rank
            self.agent.save_model(new_rank)
            print(f"  > New score {new_score:.2f} added to genetic pool at rank {new_rank}.")
            return True
        return False


    def run_evaluation_and_analysis(self):
        print("\n" + "="*20 + " EVALUATION & ANALYSIS " + "="*20)
        
        eval_episode_rewards = [] # To store the total reward for each evaluation episode
        for i in range(EVAL_EPISODES):
            s, _ = self.env.reset(seed=SEED * 100 + i) # Use unique seeds for evaluation episodes
            episode_reward = 0
            done = False
            steps_taken = 0
            while not done and steps_taken < self.max_steps:
                a = self.agent.select_action(s, eval=True) # Select action in evaluation mode
                s, r_env, term, trunc, _ = self.env.step(a)
                done = term or trunc
                episode_reward += r_env # Only consider environment reward for evaluation score
                steps_taken += 1
            eval_episode_rewards.append(episode_reward)

        current_eval_score = np.mean(eval_episode_rewards)
        
        best_known_score = max(self.high_scores.keys()) if self.high_scores else -np.inf
        print(f"  > Evaluation Score: {current_eval_score:.2f} (Best in Pool: {best_known_score:.2f})")

        is_new_best = self.manage_high_scores(current_eval_score)

        # Reset Check
        if not is_new_best and current_eval_score < best_known_score * RESET_THRESHOLD:
            self.consecutive_bad_cycles += 1
            print(f"  > Performance below threshold. Bad cycles: {self.consecutive_bad_cycles}/{RESET_PATIENCE}")
        else:
            self.consecutive_bad_cycles = 0

        if self.consecutive_bad_cycles >= RESET_PATIENCE:
            print("\n  ! PERFORMANCE DEGRADED. INITIATING GENETIC TRANSFER CEREMONY !")
            self.agent.genetic_crossover(self.high_scores)
            self.consecutive_bad_cycles = 0
            # We also reset the optimizers to give the new agent a clean start
            self.agent.a_opt = optim.Adam(self.agent.actor.parameters(), lr=3e-4)
            self.agent.c1_opt = optim.Adam(self.agent.c1.parameters(), lr=3e-4)
            self.agent.c2_opt = optim.Adam(self.agent.c2.parameters(), lr=3e-4)

        suggestions = self.shadow_detector.analyze_and_suggest(list(self.agent.td_errors))
        self.agent.apply_suggestions(suggestions)
        print("="*63 + "\n")

    def plot_rewards(self):
        plt.figure(figsize=(15, 7)); plt.title("Agent Reward Progress")
        plt.plot(self.reward_history, label='Episodic Reward', alpha=0.8)
        if len(self.reward_history) >= 20:
            moving_avg = np.convolve(self.reward_history, np.ones(20)/20, mode='valid')
            plt.plot(np.arange(19, len(self.reward_history)), moving_avg, color='red', lw=2, label='20-episode SMA')
        plt.xlabel("Episode"); plt.ylabel("Total Environment Reward"); plt.legend(); plt.grid(True)
        save_path = "pirouette_genetic_rewards.png"; plt.savefig(save_path)
        print(f"\nPlot saved to {save_path}")

# --- Main Execution ---
if __name__ == "__main__":
    trainer = PirouetteTrainer(ENV_NAME, NUM_EPISODES, MAX_STEPS_PER_EPISODE)
    trainer.train()