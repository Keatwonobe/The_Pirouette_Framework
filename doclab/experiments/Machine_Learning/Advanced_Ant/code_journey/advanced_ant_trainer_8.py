# pirouette_genetic_trainer_v2.py

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
EVAL_FREQUENCY = 1 # <<< Evaluate every episode
EVAL_EPISODES = 5  # <<< Reduced for more frequent evaluations
SEED = 42
MODEL_PATH = "./pirouette_genetic_models_v2/"

# --- Hyperparameters ---
MANIFOLD_BONUS_COEFF = 0.02
MANIFOLD_TEAR_COEFF = 0.05
RESET_THRESHOLD = 0.7
RESET_PATIENCE = 5 # Increased patience to avoid overly frequent resets
INVERSION_THRESHOLD = -1000 # This threshold is now applied to normalized reward
GENETIC_POOL_SIZE = 10 # <<< Expanded to Top 10

# --- New Hyperparameters for Risk-Reward and Stability ---
RISK_REWARD_MULTIPLIER = 0.25 # How much extra reward per unit of action magnitude above threshold
ACTION_MAGNITUDE_THRESHOLD = 0.1 # Only apply risk bonus if actions are sufficiently large
STABILITY_PENALTY_WEIGHT = 0.5 # Not directly used in the score metric for storage, but conceptual
LENGTH_BONUS_WEIGHT = 0.01 # Small bonus for length in evaluation for display
MAX_ACCEPTABLE_STD = 200 # Maximum standard deviation in evaluation rewards to consider a run "stable" for high score board

# Set device and seeds
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
if os.path.exists(MODEL_PATH):
    shutil.rmtree(MODEL_PATH)
os.makedirs(MODEL_PATH, exist_ok=True)
print(f"Using device: {device}")
print(f"Top {GENETIC_POOL_SIZE} models will be saved in: {MODEL_PATH}")

# --- UTILS (Shadow Detector is now simplified) ---
class ShadowStabilityDetector:
    def analyze_and_suggest(self, td_errors):
        if not td_errors: return {}
        suggestions = {}
        avg_td_error = np.mean(td_errors)
        
        if avg_td_error > 1.5:
            suggestions.update({'critic_lr': 5e-5, 'actor_lr': 5e-5, 'alpha': 0.1})
        else:
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
        if 'critic_lr' in sg:
            new_lr = sg['critic_lr']; [g.update(lr=new_lr) for g in self.c1_opt.param_groups]; [g.update(lr=new_lr) for g in self.c2_opt.param_groups]
        if 'actor_lr' in sg: self.a_opt.param_groups[0]['lr'] = sg['actor_lr']
        if 'alpha' in sg: self.alpha = sg['alpha']

    def save_model(self, rank):
        path = os.path.join(MODEL_PATH, f"rank_{rank}")
        os.makedirs(path, exist_ok=True)
        torch.save(self.actor.state_dict(), os.path.join(path, "actor.pth"))
        torch.save(self.c1.state_dict(), os.path.join(path, "critic1.pth"))

    def genetic_crossover(self, high_scores):
        print("  > Performing genetic crossover...")
        parent_models = {'actor': [], 'c1': []} 
        parent_scores = [score for score in high_scores.keys()]
        
        # Load parent models
        for rank in high_scores.values():
            path = os.path.join(MODEL_PATH, f"rank_{rank}")
            if os.path.exists(path):
                parent_models['actor'].append(torch.load(os.path.join(path, "actor.pth")))
                parent_models['c1'].append(torch.load(os.path.join(path, "critic1.pth")))
        
        if len(parent_scores) < 2:
            print("  > Not enough parent models for crossover. Skipping.")
            return

        # Perform weighted average of weights
        for model_name_str in ['actor', 'c1']: 
            avg_state_dict = OrderedDict()
            # Normalize scores to create weights. Add a small epsilon to handle negative scores.
            min_score = min(parent_scores)
            normalized_scores = [(s - min_score + 1e-5) for s in parent_scores]
            total_score = sum(normalized_scores)
            weights = [s / total_score for s in normalized_scores]

            for i, state_dict in enumerate(parent_models[model_name_str]):
                for key, value in state_dict.items():
                    if i == 0:
                        avg_state_dict[key] = value.clone() * weights[i]
                    else:
                        avg_state_dict[key] += value.clone() * weights[i]
            
            getattr(self, model_name_str).load_state_dict(avg_state_dict)

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
        self.eval_history = []
        
        self.high_scores = {}
        self.consecutive_bad_cycles = 0
        self.inversion_mode = False

    def train(self):
        start_time = time.time()
        for ep in range(1, self.num_episodes + 1):
            s, _ = self.env.reset(seed=SEED + ep)
            ep_r_env = 0
            steps_in_episode = 0 
            
            if self.inversion_mode:
                print(f"  -> Ep:{ep:03d} starts in ACTION INVERSION mode.")

            for step in range(1, self.max_steps + 1):
                a = self.agent.select_action(s)
                if self.inversion_mode: a = -a
                
                # Retrieve info from env.step for potential velocity/contact data
                s_, r_env, term, trunc, info = self.env.step(a) 
                done = term or trunc
                
                self.manifold_well.step(step)
                r_manifold = self.manifold_well.get_reward(a)
                
                # --- RISK-REWARD SCORING ---
                action_magnitude = np.linalg.norm(a)
                risk_bonus = 0
                if action_magnitude > ACTION_MAGNITUDE_THRESHOLD:
                    risk_bonus = (action_magnitude - ACTION_MAGNITUDE_THRESHOLD) * RISK_REWARD_MULTIPLIER
                
                total_reward = r_env + r_manifold + risk_bonus
                
                self.agent.buffer.push(s, a, total_reward, s_, done)
                self.agent.update(self.batch_size)
                
                s = s_; ep_r_env += r_env
                steps_in_episode += 1 
                if done: break
            
            # Normalize ep_r_env by steps_in_episode
            if steps_in_episode > 0:
                ep_r_env_normalized = ep_r_env / steps_in_episode
            else:
                ep_r_env_normalized = ep_r_env 
            
            self.reward_history.append(ep_r_env_normalized) 

            if ep_r_env_normalized < INVERSION_THRESHOLD and not self.inversion_mode: 
                self.inversion_mode = True
            else:
                self.inversion_mode = False

            if ep % EVAL_FREQUENCY == 0:
                self.run_evaluation_and_analysis(ep)

        print(f"\nTraining finished in {time.time()-start_time:.2f}s.")
        self.plot_rewards()

    def manage_high_scores(self, new_score, stability_std=0, average_length=0):
        # We'll use a combined metric for judging 'goodness'
        # Example: prioritize higher score, but penalize high standard deviation (instability)
        # and prefer longer runs. You might need to tune these weights.
        # This is a heuristic; tune these values!
        
        is_current_score_stable_enough = (stability_std <= MAX_ACCEPTABLE_STD) or (new_score > 1500) # For very high scores, allow more instability
        
        # If the pool is not full, or the new score is better than the worst, AND it's stable enough
        if (len(self.high_scores) < GENETIC_POOL_SIZE and is_current_score_stable_enough) or \
           (is_current_score_stable_enough and new_score > (min(self.high_scores.keys()) if self.high_scores else -np.inf)):
            
            # If the pool is full, we need to remove the worst *qualifying* score
            if len(self.high_scores) == GENETIC_POOL_SIZE:
                worst_score = min(self.high_scores.keys())
                worst_rank = self.high_scores.pop(worst_score)
                shutil.rmtree(os.path.join(MODEL_PATH, f"rank_{worst_rank}"), ignore_errors=True)
            
            new_rank = next(r for r in range(1, GENETIC_POOL_SIZE + 2) if r not in self.high_scores.values())
            
            self.high_scores[new_score] = new_rank 
            self.agent.save_model(new_rank)
            print(f"  > New good run (Score:{new_score:.2f}, Std:{stability_std:.2f}, AvgLen:{average_length:.0f}) added to Top-{GENETIC_POOL_SIZE} pool at rank {new_rank}.")
            return True
        elif not is_current_score_stable_enough:
            print(f"  > Score {new_score:.2f} (Std:{stability_std:.2f}) rejected due to instability.")
            return False
        return False


    def run_evaluation_and_analysis(self, current_episode):
        total_rewards = []
        episode_lengths = [] 
        for i in range(EVAL_EPISODES):
            s, _ = self.env.reset(seed=SEED * 100 + i)
            ep_r = 0
            steps_taken_eval = 0 
            for _ in range(self.max_steps):
                a = self.agent.select_action(s, eval=True)
                s, r, term, trunc, _ = self.env.step(a)
                ep_r += r
                steps_taken_eval += 1 
                if term or trunc: break
            
            if steps_taken_eval > 0: 
                total_rewards.append(ep_r / steps_taken_eval)
            else:
                total_rewards.append(ep_r) 
            episode_lengths.append(steps_taken_eval) 
        
        current_eval_score = np.mean(total_rewards)
        self.eval_history.append(current_eval_score)
        
        # Calculate stability metrics
        eval_reward_std = np.std(total_rewards)
        eval_length_mean = np.mean(episode_lengths)

        best_known_score = max(self.high_scores.keys()) if self.high_scores else -np.inf
        
        print(f"Ep:{current_episode:03d} | Eval Score:{current_eval_score:8.2f} | Best in Pool:{best_known_score:8.2f} | Std Dev:{eval_reward_std:.2f} | Avg Len:{eval_length_mean:.0f}")

        self.manage_high_scores(current_eval_score, eval_reward_std, eval_length_mean)

        if not self.manage_high_scores(current_eval_score, eval_reward_std, eval_length_mean) and current_eval_score < best_known_score * RESET_THRESHOLD: # Re-check manage_high_scores return
            self.consecutive_bad_cycles += 1
            print(f"  > Perf. below threshold. Bad cycles: {self.consecutive_bad_cycles}/{RESET_PATIENCE}")
        else:
            self.consecutive_bad_cycles = 0

        if self.consecutive_bad_cycles >= RESET_PATIENCE:
            print("\n  ! PERFORMANCE DEGRADED. INITIATING GENETIC TRANSFER CEREMONY !")
            self.agent.genetic_crossover(self.high_scores)
            self.consecutive_bad_cycles = 0
            self.agent.a_opt = optim.Adam(self.agent.actor.parameters(), lr=3e-4)
            self.agent.c1_opt = optim.Adam(self.agent.c1.parameters(), lr=3e-4)
            self.agent.c2_opt = optim.Adam(self.agent.c2.parameters(), lr=3e-4)

        suggestions = self.shadow_detector.analyze_and_suggest(list(self.agent.td_errors))
        self.agent.apply_suggestions(suggestions)

    def plot_rewards(self):
        plt.figure(figsize=(15, 7)); plt.title("Agent Reward Progress")
        plt.plot(self.reward_history, label='Episodic Reward (Normalized by Steps)', alpha=0.3)
        plt.plot(self.eval_history, color='red', lw=2, label=f'Evaluation Score (Normalized by Steps, every {EVAL_FREQUENCY} ep)')
        plt.xlabel("Episode"); plt.ylabel("Total Reward per Step"); plt.legend(); plt.grid(True)
        save_path = "pirouette_genetic_rewards_v2.png"; plt.savefig(save_path)
        print(f"\nPlot saved to {save_path}")

# --- Main Execution ---
if __name__ == "__main__":
    trainer = PirouetteTrainer(ENV_NAME, NUM_EPISODES, MAX_STEPS_PER_EPISODE)
    trainer.train()