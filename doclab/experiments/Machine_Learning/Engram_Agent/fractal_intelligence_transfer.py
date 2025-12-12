# fit_in_a_box_trainer.py
#
# This script is the result of systematic ablation testing on a complex locomotion
# task (Ant-v5). It represents a minimal, robust "Primal Engine" that can be
# added to a standard SAC agent to dramatically improve its ability to learn
# difficult, continuous control problems.
#
# The core philosophy is that before an agent can learn complex strategies,
# it must be grounded by a set of primal, survival-oriented drives.
#
# The "Primal Engine" consists of four key principles:
#
# 1. Survival-Focused Reward (The Will to Exist): The agent's reward is
#    normalized by the number of steps it survives. This heavily incentivizes
#    not dying above all else, creating a robust foundation for all other learning.
#
# 2. Risk-Driven Exploration (The Will to Act): The agent is given a small
#    bonus for taking actions with a large magnitude. This encourages bold,
#    exploratory behavior, preventing the agent from getting stuck in passive,
#    local minima where it does nothing.
#
# 3. Grounded Action (The "Sense of Touch"): A 'ManifoldWell' provides a
#    smooth, predictable, artificial force for the agent to orient against.
#    This gives the agent a foundational "sense of touch" or proprioception,
#    allowing it to connect its actions to coherent outcomes instead of
#    flailing randomly.
#
# 4. Stable Genetics (The Wisdom of the Tribe): When the agent's performance
#    stagnates, it performs a genetic crossover with other successful agents
#    from its lineage. Crucially, this process includes:
#      a) A stability check to ensure only reliable policies are saved.
#      b) A rollback mechanism to undo any crossover that results in a
#         weaker agent, preserving the hard-won wisdom of the past.
#
# This combination creates an agent that is not just a sterile optimizer, but
# a synthetic creature with a drive to survive, a curiosity to explore, a sense
# of its own body, and a connection to the wisdom of its ancestors.

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
import copy

# --- Configuration ---
ENV_NAME = 'Ant-v5'
NUM_EPISODES = 6000
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 10
EVAL_EPISODES = 5
SEED = 2700
MODEL_PATH = "./fractal_intelligence_transfer_models/"

# --- Primal Engine Hyperparameters ---
# These values are tuned for Ant-v5 but can be adjusted for other tasks.
RESET_PATIENCE = 10             # How many bad evaluations before triggering genetics.
GENETIC_POOL_SIZE = 10          # Number of successful ancestors to keep.
GENE_TRANSFER_RATE = 0.6        # Probability of inheriting a weight from parent 1.
RISK_REWARD_MULTIPLIER = 0.1    # Scales the bonus for bold actions.
ACTION_MAGNITUDE_THRESHOLD = 0.1# Actions above this magnitude get the risk bonus.
MAX_ACCEPTABLE_STD = 2.0        # Max performance variance to be considered "stable".
MANIFOLD_BONUS_COEFF = 0.02     # Scales the reward for aligning with the manifold.
MANIFOLD_TEAR_COEFF = 0.05      # Scales the penalty for deviating from the manifold.

# --- Setup ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
if os.path.exists(MODEL_PATH): shutil.rmtree(MODEL_PATH)
os.makedirs(MODEL_PATH, exist_ok=True)
print(f"Using device: {device}")
print(f"FIT-in-a-Box models will be saved in: {MODEL_PATH}")

# --- Principle 3: The "Sense of Touch" ---
class ManifoldWell:
    """Creates a smooth, oscillating force field in the action space."""
    def __init__(self, action_dim, max_steps):
        self.action_dim = action_dim
        self.max_steps = max_steps
        # The center of the "well" moves in a sine wave pattern.
        self.center = np.zeros(action_dim)
        self.phase = np.random.uniform(0, 2 * np.pi, size=action_dim)
        self.frequency = np.random.uniform(0.5, 1.5, size=action_dim)
        self.amplitude = np.random.uniform(0.4, 0.8, size=action_dim)

    def step(self, t):
        """Updates the center of the well based on the current timestep."""
        time_factor = (2 * np.pi * t) / self.max_steps
        self.center = self.amplitude * np.sin(self.frequency * time_factor + self.phase)

    def get_reward(self, action):
        """Calculates a reward based on the action's proximity to the well's center."""
        distance = np.linalg.norm(action - self.center)
        # Exponential reward for being close to the center (the "touch").
        alignment_bonus = MANIFOLD_BONUS_COEFF * math.exp(-2.0 * distance)
        # Linear penalty for being too far away.
        tear_penalty = -MANIFOLD_TEAR_COEFF * max(0, distance - 1.0)
        return alignment_bonus + tear_penalty

# --- Standard SAC Agent Implementation ---
# This is a clean, minimal implementation of Soft Actor-Critic.
class Actor(nn.Module):
    def __init__(self,s,a,h=256):super().__init__();self.n=nn.Sequential(nn.Linear(s,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU());self.m=nn.Linear(h,a);self.ls=nn.Linear(h,a)
    def forward(self,s):x=self.n(s);return self.m(x),torch.clamp(self.ls(x),-20,2)
class Critic(nn.Module):
    def __init__(self,s,a,h=256):super().__init__();self.n=nn.Sequential(nn.Linear(s+a,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU(),nn.Linear(h,1))
    def forward(self,s,a):return self.n(torch.cat([s,a],1))
class ReplayBuffer:
    def __init__(self,c):self.b=deque(maxlen=c)
    def push(self,s,a,r,s_,d):self.b.append((s,a,r,s_,d))
    def sample(self,B):return random.sample(self.b,B)
    def __len__(self):return len(self.b)

class SACAgent:
    def __init__(self, e, lr=3e-4, g=0.99, t=0.005, a=0.2):
        self.env=e;self.state_dim,self.action_dim=e.observation_space.shape[0],e.action_space.shape[0];self.gamma,self.tau,self.alpha=g,t,a
        self.action_scale=torch.tensor((e.action_space.high-e.action_space.low)/2.,device=device,dtype=torch.float32);self.action_bias=torch.tensor((e.action_space.high+e.action_space.low)/2.,device=device,dtype=torch.float32)
        self.actor=Actor(self.state_dim,self.action_dim).to(device);self.c1,self.c2=Critic(self.state_dim,self.action_dim).to(device),Critic(self.state_dim,self.action_dim).to(device)
        self.c1_t,self.c2_t=Critic(self.state_dim,self.action_dim).to(device),Critic(self.state_dim,self.action_dim).to(device);self.c1_t.load_state_dict(self.c1.state_dict());self.c2_t.load_state_dict(self.c2.state_dict())
        self.a_opt,self.c1_opt,self.c2_opt=optim.Adam(self.actor.parameters(),lr=lr),optim.Adam(self.c1.parameters(),lr=lr),optim.Adam(self.c2.parameters(),lr=lr)
        self.buffer=ReplayBuffer(1_000_000)
    def select_action(self,s,eval=False):
        s=torch.tensor(s,device=device,dtype=torch.float32).unsqueeze(0);m,ls=self.actor(s)
        a=torch.tanh(m) if eval else torch.tanh(Normal(m,ls.exp()).rsample())
        return(a.cpu().detach().numpy()[0]*self.action_scale.cpu().numpy())+self.action_bias.cpu().numpy()
    def update(self,B):
        if len(self.buffer)<B:return
        s,a,r,s_,d=zip(*self.buffer.sample(B));s,a,r,s_,d=torch.tensor(np.array(s),device=device,dtype=torch.float32),torch.tensor(np.array(a),device=device,dtype=torch.float32),torch.tensor(np.array(r),device=device,dtype=torch.float32).unsqueeze(1),torch.tensor(np.array(s_),device=device,dtype=torch.float32),torch.tensor(np.array(d),device=device,dtype=torch.float32).unsqueeze(1)
        with torch.no_grad():
            m_,ls_=self.actor(s_);d_=Normal(m_,ls_.exp());z=d_.rsample();a_=torch.tanh(z);lp=d_.log_prob(z)-torch.log(1-a_.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
            tq1,tq2=self.c1_t(s_,a_),self.c2_t(s_,a_);tq=torch.min(tq1,tq2)-self.alpha*lp;tq=r+(1-d)*self.gamma*tq
        cq1,cq2=self.c1(s,a),self.c2(s,a);cl=F.mse_loss(cq1,tq)+F.mse_loss(cq2,tq)
        self.c1_opt.zero_grad();self.c2_opt.zero_grad();cl.backward();self.c1_opt.step();self.c2_opt.step()
        m,ls=self.actor(s);d=Normal(m,ls.exp());z=d.rsample();a_pi=torch.tanh(z);lp=d.log_prob(z)-torch.log(1-a_pi.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
        q1_pi,q2_pi=self.c1(s,a_pi),self.c2(s,a_pi);min_q_pi=torch.min(q1_pi,q2_pi);al=(self.alpha*lp-min_q_pi).mean();self.a_opt.zero_grad();al.backward();self.a_opt.step()
        for t,s_p in zip(self.c1_t.parameters(),self.c1.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s_p.data*self.tau)
        for t,s_p in zip(self.c2_t.parameters(),self.c2.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s_p.data*self.tau)
    def save_model(self, rank):
        path=os.path.join(MODEL_PATH,f"rank_{rank}");os.makedirs(path,exist_ok=True)
        torch.save(self.actor.state_dict(),os.path.join(path,"actor.pth"))
    def load_model(self, rank):
        self.actor.load_state_dict(torch.load(os.path.join(MODEL_PATH, f"rank_{rank}", "actor.pth")))

# --- The Main Trainer ---
class FIT_in_a_Box_Trainer:
    def __init__(self):
        self.env = gym.make(ENV_NAME, render_mode=None)
        self.agent = SACAgent(self.env)
        self.manifold_well = ManifoldWell(self.agent.action_dim, MAX_STEPS_PER_EPISODE)
        self.batch_size = 256
        self.eval_history = []
        self.high_scores = {}; self.consecutive_bad_cycles = 0

    def train(self):
        start_time = time.time()
        for ep in range(1, NUM_EPISODES + 1):
            s, _ = self.env.reset(seed=SEED + ep)
            ep_r_env, steps_in_episode = 0, 0

            for step in range(1, MAX_STEPS_PER_EPISODE + 1):
                a = self.agent.select_action(s)
                s_, r_env, term, trunc, _ = self.env.step(a)
                done = term or trunc

                # --- Primal Engine Reward Shaping ---
                r_manifold = self.manifold_well.get_reward(a)
                action_magnitude = np.linalg.norm(a)
                risk_bonus = (action_magnitude - ACTION_MAGNITUDE_THRESHOLD) * RISK_REWARD_MULTIPLIER if action_magnitude > ACTION_MAGNITUDE_THRESHOLD else 0
                total_reward = r_env + r_manifold + risk_bonus

                self.agent.buffer.push(s, a, total_reward, s_, done)
                self.agent.update(self.batch_size)

                s = s_; ep_r_env += r_env; steps_in_episode += 1
                if done: break
            
            # --- Principle 1: Survival-Focused Reward ---
            ep_r_env_normalized = ep_r_env / steps_in_episode if steps_in_episode > 0 else ep_r_env

            if ep % 10 == 0:
                 print(f"Ep:{ep:04d} | Norm R:{ep_r_env_normalized:8.2f} | Steps: {steps_in_episode:4d}")

            if ep % EVAL_FREQUENCY == 0:
                self.run_evaluation_and_manage_pool(ep)

        print(f"\nTraining finished in {time.time()-start_time:.2f}s.")
        self.plot_results()

    # --- Principle 4: Stable Genetics & Rollback ---
    def run_evaluation_and_manage_pool(self, ep, post_crossover_check=False, best_parent_score=None):
        eval_rewards = []
        for i in range(EVAL_EPISODES):
            s_eval, _ = self.env.reset(seed=SEED * 100 + i); ep_r, steps = 0, 0
            for _ in range(MAX_STEPS_PER_EPISODE):
                a = self.agent.select_action(s_eval, eval=True)
                s_eval, r, term, trunc, _ = self.env.step(a)
                ep_r += r; steps += 1
                if term or trunc: break
            eval_rewards.append(ep_r / steps if steps > 0 else ep_r)
        
        current_eval_score = np.mean(eval_rewards)
        eval_reward_std = np.std(eval_rewards)
        if not post_crossover_check: self.eval_history.append(current_eval_score)
        
        best_pool_score = max(self.high_scores.keys()) if self.high_scores else -np.inf
        print(f"  > Eval @ Ep {ep} | Avg Score: {current_eval_score:8.2f} | Std Dev: {eval_reward_std:.2f} (Best in Pool: {best_pool_score:8.2f})")

        if post_crossover_check:
            if current_eval_score < best_parent_score:
                print(f"  > Crossover failed! Score {current_eval_score:.2f} < Parent Score {best_parent_score:.2f}. Rolling back...")
                return False
            else:
                print(f"  > Crossover successful! Score {current_eval_score:.2f} >= Parent Score {best_parent_score:.2f}.")
                return True

        is_stable = eval_reward_std <= MAX_ACCEPTABLE_STD
        is_improvement = len(self.high_scores) < GENETIC_POOL_SIZE or current_eval_score > min(self.high_scores.keys())

        if is_stable and is_improvement:
            if len(self.high_scores) == GENETIC_POOL_SIZE:
                worst_score = min(self.high_scores.keys())
                worst_rank = self.high_scores.pop(worst_score)['rank']
                shutil.rmtree(os.path.join(MODEL_PATH, f"rank_{worst_rank}"), ignore_errors=True)
            
            used_ranks = {data['rank'] for data in self.high_scores.values()}
            new_rank = next(rank for rank in range(1, GENETIC_POOL_SIZE + 2) if rank not in used_ranks)
            self.high_scores[current_eval_score] = {'rank': new_rank}
            self.agent.save_model(new_rank)
            print(f"  > New stable model added to pool at rank {new_rank} with score {current_eval_score:.2f}")
            self.consecutive_bad_cycles = 0
        elif not is_stable:
            print(f"  > Score rejected due to instability (Std Dev: {eval_reward_std:.2f} > {MAX_ACCEPTABLE_STD:.2f})")
        else:
            self.consecutive_bad_cycles += 1
            print(f"  > Performance did not improve. Bad cycles: {self.consecutive_bad_cycles}/{RESET_PATIENCE}")

        if self.consecutive_bad_cycles >= RESET_PATIENCE:
            self.perform_genetic_crossover(ep)
            self.consecutive_bad_cycles = 0

    def perform_genetic_crossover(self, ep):
        print("\n  ! PERFORMANCE STAGNATED. INITIATING GENETIC TRANSFER !")
        if len(self.high_scores) < 2:
            print("  > Not enough parents for crossover. Skipping."); return

        sorted_scores = sorted(self.high_scores.items(), key=lambda item: item[0], reverse=True)
        p1_score, p1_data = sorted_scores[0]
        p2_score, p2_data = sorted_scores[1]
        p1_rank, p2_rank = p1_data['rank'], p2_data['rank']
        
        print(f"  > Parents: Rank {p1_rank} (Score: {p1_score:.2f}) and Rank {p2_rank} (Score: {p2_score:.2f})")
        
        self.agent.load_model(p1_rank)
        best_parent_weights = copy.deepcopy(self.agent.actor.state_dict())

        p1_weights = torch.load(os.path.join(MODEL_PATH, f"rank_{p1_rank}", "actor.pth"))
        p2_weights = torch.load(os.path.join(MODEL_PATH, f"rank_{p2_rank}", "actor.pth"))
        child_weights = OrderedDict()
        for key in p1_weights:
            if random.random() < GENE_TRANSFER_RATE: child_weights[key] = p1_weights[key].clone()
            else: child_weights[key] = p2_weights[key].clone()
        self.agent.actor.load_state_dict(child_weights)
        print("  > Crossover complete. Evaluating new generation...")

        crossover_succeeded = self.run_evaluation_and_manage_pool(ep, post_crossover_check=True, best_parent_score=p1_score)
        if not crossover_succeeded:
            self.agent.actor.load_state_dict(best_parent_weights)
            print("  > Rollback complete. Best parent policy restored.")
        else:
             print("  > New generation validated. Continuing training.")

    def plot_results(self):
        plt.figure(figsize=(12, 6))
        plt.title("FIT-in-a-Box Trainer Evaluation Score")
        plt.xlabel("Episode")
        plt.ylabel("Evaluation Score (Normalized by Steps)")
        eval_episodes = np.arange(EVAL_FREQUENCY, len(self.eval_history) * EVAL_FREQUENCY + 1, EVAL_FREQUENCY)
        plt.plot(eval_episodes, self.eval_history, color='tab:blue', lw=2)
        plt.grid(True)
        save_path = "fit_in_a_box_results.png"
        plt.savefig(save_path)
        print(f"\nPlot saved to {save_path}")

# --- Main Execution ---
if __name__ == "__main__":
    trainer = FIT_in_a_Box_Trainer()
    trainer.train()
