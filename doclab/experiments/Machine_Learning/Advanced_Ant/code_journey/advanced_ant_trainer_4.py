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
import pywt # You may need to run: pip install PyWavelets

# --- Configuration ---
ENV_NAME = 'Ant-v5'
NUM_EPISODES = 300
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 15 # Evaluate and sync every 15 episodes
EVAL_EPISODES = 5   # Number of episodes to run for evaluation
SEED = 42

# --- Hyperparameters ---
RHYTHM_BONUS_COEFF = 0.05 

# Set device and seeds
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)

# --- UTILS (HFD, Analytics, Shadow Detector) ---
def calculate_hfd(series):
    L, x, N = [], [], len(series)
    if N < 20: return 1.0
    for k in range(1, 10):
        Lk = sum(np.sum(np.abs(np.diff(series[m::k])))*(N-1)/((len(series[m::k])-1)*k) for m in range(k) if len(series[m::k])>1)
        if Lk > 0: L.append(np.log(Lk/k)); x.append(np.log(1.0/k))
    return np.polyfit(x, L, 1)[0] if L else 1.0

class ContinuousPirouetteAnalytics:
    def __init__(self): self.Ki_rest, self.Ki_motion = 4.14159, 4.18879
    def temporal_coherence_spectrum(self, data):
        if len(data) < 20: return None
        scales = np.arange(1, min(len(data)//4, 128))
        coeffs, _ = pywt.cwt(data, scales, 'cmor1.0-1.0')
        return np.abs(np.mean(np.exp(1j*np.angle(coeffs)), axis=1))

class ContinuousShadowRegionDetector:
    def __init__(self, analytics): self.analytics = analytics
    def analyze_and_suggest(self, data):
        if data is None or len(data) < 50: return {}
        coherence = self.analytics.temporal_coherence_spectrum((data-np.mean(data))/(np.std(data)+1e-6))
        if coherence is None: return {}
        suggestions, mean_coherence = {}, np.mean(coherence)
        print(f"  [Shadow] Coherence: {mean_coherence:.4f}.", end=" ")
        if mean_coherence < 0.15: print("Mode: Stability"); suggestions.update({'critic_lr':1e-4,'actor_lr':1e-4,'batch_size':1024,'alpha':0.05})
        elif mean_coherence < 0.4: print("Mode: Exploration"); suggestions.update({'critic_lr':self.analytics.Ki_rest/10000,'actor_lr':self.analytics.Ki_rest/15000,'batch_size':512,'alpha':0.2})
        else: print("Mode: Fine-tuning"); suggestions.update({'critic_lr':5e-5,'actor_lr':5e-5,'batch_size':256,'alpha':0.1})
        return suggestions

# --- SAC Agent (Unchanged) ---
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
    def select_action(self,s,eval=False):s=torch.tensor(s,device=device,dtype=torch.float32).unsqueeze(0);m,ls=self.actor(s);d=Normal(m,ls.exp());a=torch.tanh(m) if eval else torch.tanh(d.rsample());return(a.cpu().detach().numpy()[0]*self.action_scale.cpu().numpy())+self.action_bias.cpu().numpy()
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
        if'critic_lr'in sg:new=sg['critic_lr'];[g.update(lr=new) for g in [self.c1_opt.param_groups[0],self.c2_opt.param_groups[0]]]
        if'actor_lr'in sg:self.a_opt.param_groups[0].update(lr=sg['actor_lr'])
        if'alpha'in sg:self.alpha=sg['alpha']

# --- Hydra Trainer ---
class HydraTrainer:
    def __init__(self, env_name, num_episodes, max_steps, eval_freq):
        self.env_name = env_name
        self.num_episodes = num_episodes
        self.max_steps = max_steps
        self.eval_freq = eval_freq
        self.batch_size = 256
        self.reward_history = { 'shadow': [], 'pirouette': [], 'rhythmic': [], 'hydra_avg': [] }
        self.state_history = { 'shadow': deque(maxlen=5000), 'pirouette': deque(maxlen=5000), 'rhythmic': deque(maxlen=5000) }

        # Create the three specialized agents
        env = gym.make(env_name)
        self.agents = { name: SACAgent(env) for name in self.reward_history.keys() if name != 'hydra_avg' }
        
        # Setup analytics tools
        self.analytics = ContinuousPirouetteAnalytics()
        self.shadow_detector = ContinuousShadowRegionDetector(self.analytics)
        self.agent_types = list(self.agents.keys())

    def train(self):
        start_time, agent_idx = time.time(), 0
        for ep in range(self.num_episodes):
            agent_name = self.agent_types[agent_idx]
            agent = self.agents[agent_name]
            
            s, _ = agent.env.reset(seed=SEED + ep)
            ep_r, ep_s = 0, []
            
            for step in range(self.max_steps):
                a = agent.select_action(s)
                s_, r, term, trunc, _ = agent.env.step(a)
                done = term or trunc
                
                shaped_r = self.shape_reward(r, a, step, agent_name)
                agent.buffer.push(s, a, shaped_r, s_, done)
                agent.update(self.batch_size)
                
                s = s_; ep_r += r; ep_s.append(s)
                if done: break

            self.reward_history[agent_name].append(ep_r)
            self.state_history[agent_name].extend(ep_s)
            
            avg_all = np.mean([r for sublist in self.reward_history.values() for r in sublist[-20:] if sublist])
            self.reward_history['hydra_avg'].append(avg_all)
            print(f"Ep:{ep+1:03d} [Trained: {agent_name:<9}] Rw:{ep_r:7.1f} AvgRw:{avg_all:7.1f}")
            
            if (ep + 1) % self.eval_freq == 0:
                self.run_competitive_evaluation()

            agent_idx = (agent_idx + 1) % len(self.agent_types)
        
        print(f"\nTraining finished in {time.time()-start_time:.2f}s.")
        self.plot_rewards()

    def shape_reward(self, r, a, step, agent_name):
        if agent_name == 'rhythmic':
            action_mag = np.linalg.norm(a)
            pulse = (math.cos(2 * math.pi * step / self.analytics.Ki_motion) + 1) / 2
            return r + (RHYTHM_BONUS_COEFF * action_mag * pulse)
        return r

    def run_competitive_evaluation(self):
        print("\n" + "="*20 + " COMPETITIVE EVALUATION " + "="*20)
        eval_scores = {}
        for name, agent in self.agents.items():
            print(f"  > Evaluating {name} agent...")
            
            # Run individual analysis before evaluation
            self.run_agent_analysis(name, agent)
            
            total_rewards = []
            for i in range(EVAL_EPISODES):
                s, _ = agent.env.reset(seed=SEED * 100 + i)
                ep_r, done = 0, False
                for _ in range(self.max_steps):
                    a = agent.select_action(s, evaluate=True)
                    s, r, term, trunc, _ = agent.env.step(a)
                    done = term or trunc
                    ep_r += r
                    if done: break
                total_rewards.append(ep_r)
            eval_scores[name] = np.mean(total_rewards)
            print(f"    ...Avg Score: {eval_scores[name]:.2f}")

        winner_name = max(eval_scores, key=eval_scores.get)
        print(f"\n  WINNER: {winner_name.upper()} (Score: {eval_scores[winner_name]:.2f})\n")
        
        # --- Strategy Transfer ---
        winner_agent = self.agents[winner_name]
        for name, agent in self.agents.items():
            if name != winner_name:
                print(f"  > Syncing {winner_name}'s strategy -> {name}")
                agent.actor.load_state_dict(winner_agent.actor.state_dict())
                agent.c1.load_state_dict(winner_agent.c1.state_dict())
                agent.c2.load_state_dict(winner_agent.c2.state_dict())
                agent.c1_t.load_state_dict(winner_agent.c1_t.state_dict())
                agent.c2_t.load_state_dict(winner_agent.c2_t.state_dict())
        print("="*64 + "\n")

    def run_agent_analysis(self, name, agent):
        if name == 'shadow':
            suggestions = self.shadow_detector.analyze_and_suggest(np.array(agent.td_errors))
            agent.apply_suggestions(suggestions)
        elif name == 'pirouette':
            hfd = calculate_hfd(np.linalg.norm(np.array(self.state_history[name]), axis=1))
            print(f"  [Pirouette] HFD: {hfd:.4f}.", end=" ")
            s, ravg = {}, np.mean(self.reward_history[name][-self.eval_freq:] or [0])
            if hfd > 1.8: print("Mode: Stability"); s.update({'critic_lr':5e-5,'actor_lr':5e-5,'alpha':0.05})
            elif hfd < 1.5 and ravg < 200: print("Mode: Exploration"); s.update({'critic_lr':3e-4,'actor_lr':3e-4,'alpha':0.3})
            elif hfd < 1.5: print("Mode: Fine-tuning"); s.update({'critic_lr':1e-5,'actor_lr':1e-5,'alpha':0.1})
            else: print("Mode: Standard"); s.update({'critic_lr':3e-4,'actor_lr':3e-4,'alpha':0.2})
            agent.apply_suggestions(s)

    def plot_rewards(self):
        plt.figure(figsize=(15,8)); plt.title("Hydra Trainer Reward Progress")
        colors = {'shadow': 'r', 'pirouette': 'g', 'rhythmic': 'b', 'hydra_avg': 'k'}
        for name, history in self.reward_history.items():
            if not history: continue
            if name == 'hydra_avg':
                plt.plot(history, color=colors[name], lw=2.5, label='Overall Average')
            else:
                # Plot individual episode rewards as scattered points
                x_vals = np.arange(len(self.reward_history['hydra_avg']))[::len(self.agents)] + list(self.agents.keys()).index(name)
                plt.scatter(x_vals[:len(history)], history, c=colors[name], alpha=0.3, s=15, label=f'{name} points')

        plt.xlabel("Episode"); plt.ylabel("Total Reward"); plt.legend(); plt.grid(True)
        plt.savefig("hydra_trainer_rewards.png"); print(f"\nPlot saved to hydra_trainer_rewards.png")

# --- Main Execution ---
if __name__ == "__main__":
    trainer = HydraTrainer(ENV_NAME, NUM_EPISODES, MAX_STEPS_PER_EPISODE, EVAL_FREQUENCY)
    trainer.train()