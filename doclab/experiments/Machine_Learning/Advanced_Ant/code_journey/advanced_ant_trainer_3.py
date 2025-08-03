import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Normal
import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
from collections import deque, namedtuple
import random
import time
import os
import pywt # You may need to run: pip install PyWavelets

# --- Configuration ---
TRAINER_TYPE = 'PIROUETTE' # <-- CHOOSE YOUR TRAINER: 'SHADOW' or 'PIROUETTE'
ENV_NAME = 'Ant-v5'
NUM_EPISODES = 300
MAX_STEPS_PER_EPISODE = 1000
ANALYSIS_FREQUENCY = 50 # Analyze and adapt every 10 episodes
SEED = 42
COMPLEXITY_PENALTY_COEFF = 0.5 # For Pirouette trainer reward shaping

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Set random seeds for reproducibility
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

# --- NEW: Higuchi Fractal Dimension Calculator ---
def calculate_hfd(series):
    """Calculates the Higuchi Fractal Dimension of a time series."""
    L = []
    x = []
    N = len(series)
    if N < 20: return 1.0 # Not enough data, return neutral value

    for k in range(1, 10):
        Lk = 0
        for m in range(k):
            # Create a new series from the original with a stride of k
            sub_series = series[m::k]
            if len(sub_series) < 2: continue
            
            # Calculate the length of this new curve
            Lk += np.sum(np.abs(np.diff(sub_series))) * (N - 1) / ((len(sub_series) -1) * k)
        
        if Lk > 0:
            L.append(np.log(Lk / k))
            x.append(np.log(1.0 / k))

    if not L: return 1.0

    # Fit a line to the log-log plot to get the slope (the fractal dimension)
    (p, _) = np.polyfit(x, L, 1)
    return p

# --- Pirouette Analytics (For Shadow Trainer) ---
class ContinuousPirouetteAnalytics:
    def __init__(self):
        self.Ki_rest = 4.14159
    def temporal_coherence_spectrum(self, data, scales=None, wavelet='cmor1.0-1.0'):
        if len(data) < 20: return None, None, None
        if scales is None: scales = np.arange(1, min(len(data) // 4, 128))
        coeffs, _ = pywt.cwt(data, scales, wavelet)
        phase = np.angle(coeffs)
        time_adherence = np.abs(np.mean(np.exp(1j * phase), axis=1))
        return coeffs, scales, time_adherence

# --- Shadow Region Detection (For Shadow Trainer) ---
class ContinuousShadowRegionDetector:
    def __init__(self, analytics):
        self.analytics = analytics
        self.ki_rest = analytics.Ki_rest
    def analyze_and_suggest(self, data):
        if data is None or len(data) < 50: return {}
        data_norm = (data - np.mean(data)) / (np.std(data) + 1e-6)
        _, _, coherence, = self.analytics.temporal_coherence_spectrum(data_norm)
        if coherence is None: return {}
        suggestions = {}
        mean_coherence = np.mean(coherence)
        print(f"INFO: Mean coherence of TD error is {mean_coherence:.4f}.")
        if mean_coherence < 0.15:
            print("INFO: Deep shadow detected (chaos). Prioritizing stability.")
            suggestions.update({'critic_lr': 1e-4, 'actor_lr': 1e-4, 'batch_size': 1024, 'alpha': 0.05})
        elif mean_coherence < 0.4:
            print("INFO: Moderate shadow detected (struggling). Using Ki-based exploration.")
            suggestions.update({'critic_lr': self.ki_rest / 10000, 'actor_lr': self.ki_rest / 15000, 'batch_size': 512, 'alpha': 0.2})
        else:
            print("INFO: Shallow shadow or stable learning detected. Fine-tuning.")
            suggestions.update({'critic_lr': 5e-5, 'actor_lr': 5e-5, 'batch_size': 256, 'alpha': 0.1})
        return suggestions

# --- SAC Agent (The Learner) ---
# (Agent code remains the same as it's a generic SAC implementation)
class ReplayBuffer:
    def __init__(self, capacity): self.buffer = deque(maxlen=capacity)
    def push(self,s,a,r,s_,d): self.buffer.append((s,a,r,s_,d))
    def sample(self, B): return random.sample(self.buffer, B)
    def __len__(self): return len(self.buffer)

class Actor(nn.Module):
    def __init__(self,s_dim,a_dim,h_dim=256):
        super().__init__();self.net=nn.Sequential(nn.Linear(s_dim,h_dim),nn.ReLU(),nn.Linear(h_dim,h_dim),nn.ReLU());self.mean=nn.Linear(h_dim,a_dim);self.log_std=nn.Linear(h_dim,a_dim)
    def forward(self,s):x=self.net(s);m=self.mean(x);ls=self.log_std(x);return m,torch.clamp(ls,-20,2)

class Critic(nn.Module):
    def __init__(self,s_dim,a_dim,h_dim=256):
        super().__init__();self.net=nn.Sequential(nn.Linear(s_dim+a_dim,h_dim),nn.ReLU(),nn.Linear(h_dim,h_dim),nn.ReLU(),nn.Linear(h_dim,1))
    def forward(self,s,a):return self.net(torch.cat([s,a],1))

class SACAgent:
    def __init__(self,env,h_dim=256,lr=3e-4,gamma=0.99,tau=0.005,alpha=0.2):
        self.env=env;self.s_dim=env.observation_space.shape[0];self.a_dim=env.action_space.shape[0]
        self.a_scale=torch.tensor((env.action_space.high-env.action_space.low)/2.,device=device,dtype=torch.float32)
        self.a_bias=torch.tensor((env.action_space.high+env.action_space.low)/2.,device=device,dtype=torch.float32)
        self.gamma=gamma;self.tau=tau;self.alpha=alpha
        self.actor=Actor(self.s_dim,self.a_dim,h_dim).to(device)
        self.c1=Critic(self.s_dim,self.a_dim,h_dim).to(device);self.c2=Critic(self.s_dim,self.a_dim,h_dim).to(device)
        self.c1_t=Critic(self.s_dim,self.a_dim,h_dim).to(device);self.c2_t=Critic(self.s_dim,self.a_dim,h_dim).to(device)
        self.c1_t.load_state_dict(self.c1.state_dict());self.c2_t.load_state_dict(self.c2.state_dict())
        self.a_opt=optim.Adam(self.actor.parameters(),lr=lr);self.c1_opt=optim.Adam(self.c1.parameters(),lr=lr);self.c2_opt=optim.Adam(self.c2.parameters(),lr=lr)
        self.buffer=ReplayBuffer(1_000_000);self.td_errors=deque(maxlen=5000)
    def select_action(self,s,eval=False):
        s=torch.tensor(s,device=device,dtype=torch.float32).unsqueeze(0)
        m,ls=self.actor(s);dist=Normal(m,ls.exp());a=torch.tanh(m) if eval else torch.tanh(dist.rsample())
        return(a.cpu().detach().numpy()[0]*self.a_scale.cpu().numpy())+self.a_bias.cpu().numpy()
    def update(self,B):
        if len(self.buffer)<B:return
        s,a,r,s_,d=zip(*self.buffer.sample(B))
        s=torch.tensor(np.array(s),device=device,dtype=torch.float32);a=torch.tensor(np.array(a),device=device,dtype=torch.float32)
        r=torch.tensor(np.array(r),device=device,dtype=torch.float32).unsqueeze(1);s_=torch.tensor(np.array(s_),device=device,dtype=torch.float32)
        d=torch.tensor(np.array(d),device=device,dtype=torch.float32).unsqueeze(1)
        with torch.no_grad():
            m_,ls_=self.actor(s_);dist_=Normal(m_,ls_.exp());z=dist_.rsample();a_=torch.tanh(z)
            lp=dist_.log_prob(z)-torch.log(1-a_.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
            tq1=self.c1_t(s_,a_);tq2=self.c2_t(s_,a_);tq=torch.min(tq1,tq2)-self.alpha*lp;tq=r+(1-d)*self.gamma*tq
        cq1=self.c1(s,a);cq2=self.c2(s,a);self.td_errors.append((F.mse_loss(cq1,tq)+F.mse_loss(cq2,tq)).detach().cpu().item())
        c1l=F.mse_loss(cq1,tq);c2l=F.mse_loss(cq2,tq)
        self.c1_opt.zero_grad();c1l.backward();self.c1_opt.step();self.c2_opt.zero_grad();c2l.backward();self.c2_opt.step()
        m,ls=self.actor(s);dist=Normal(m,ls.exp());z=dist.rsample();a_pi=torch.tanh(z)
        lp=dist.log_prob(z)-torch.log(1-a_pi.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
        q1_pi=self.c1(s,a_pi);q2_pi=self.c2(s,a_pi);min_q_pi=torch.min(q1_pi,q2_pi)
        al=(self.alpha*lp-min_q_pi).mean();self.a_opt.zero_grad();al.backward();self.a_opt.step()
        for t,s in zip(self.c1_t.parameters(),self.c1.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s.data*self.tau)
        for t,s in zip(self.c2_t.parameters(),self.c2.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s.data*self.tau)
    def apply_suggestions(self,sg):
        if not sg:return
        print("--- Applying Suggestions ---")
        if'critic_lr'in sg:old=self.c1_opt.param_groups[0]['lr'];new=sg['critic_lr'];print(f"Critic LR: {old:.6f}->{new:.6f}");[g.update(lr=new)for g in[self.c1_opt.param_groups[0],self.c2_opt.param_groups[0]]]
        if'actor_lr'in sg:old=self.a_opt.param_groups[0]['lr'];new=sg['actor_lr'];print(f"Actor LR:  {old:.6f}->{new:.6f}");self.a_opt.param_groups[0]['lr']=new
        if'alpha'in sg:old=self.alpha;self.alpha=sg['alpha'];print(f"Alpha:     {old:.4f}->{self.alpha:.4f}")
        print("----------------------------")

# --- Trainer Base Class & Implementations ---
class BaseTrainer:
    def __init__(self, env_name, num_episodes, max_steps, analysis_freq):
        try:
            self.env = gym.make(env_name)
        except Exception as e:
            print(f"Error creating environment '{env_name}'. Is MuJoCo installed? Try: pip install gymnasium[mujoco]"); raise e
        self.agent = SACAgent(self.env)
        self.num_episodes = num_episodes
        self.max_steps = max_steps
        self.analysis_freq = analysis_freq
        self.batch_size = 256
        self.reward_history = []
        self.state_history = deque(maxlen=20000) # Store recent states for analysis
    def train(self):
        start_time = time.time()
        for episode in range(self.num_episodes):
            state, _ = self.env.reset(seed=SEED + episode)
            episode_reward, episode_states = 0, []
            for step in range(self.max_steps):
                action = self.agent.select_action(state)
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                self.agent.buffer.push(state, action, reward, next_state, done)
                self.agent.update(self.batch_size)
                state = next_state
                episode_reward += reward
                episode_states.append(state)
                if done: break
            self.reward_history.append(episode_reward)
            self.state_history.extend(episode_states)
            self.log_progress(episode, episode_reward)
            if episode > 0 and (episode + 1) % self.analysis_freq == 0:
                self.run_analysis()
        print(f"\nTraining finished in {time.time()-start_time:.2f} seconds.")
        self.plot_rewards()
        self.env.close()
    def log_progress(self, episode, reward):
        avg_reward = np.mean(self.reward_history[-100:])
        lr = self.agent.a_opt.param_groups[0]['lr']
        print(f"Ep: {episode+1}, Rw: {reward:.1f}, AvgRw: {avg_reward:.1f}, LR: {lr:.6f}, B: {self.batch_size}")
    def run_analysis(self): raise NotImplementedError
    def plot_rewards(self):
        plt.figure(figsize=(12,6));plt.plot(self.reward_history,alpha=0.6,label='Episode Reward')
        if len(self.reward_history)>=50:
            ma=np.convolve(self.reward_history,np.ones(50)/50,mode='valid')
            plt.plot(np.arange(49,len(self.reward_history)),ma,'r',linewidth=2,label='50-ep MA')
        plt.title(f"Training Rewards for {self.__class__.__name__}");plt.xlabel("Episode");plt.ylabel("Reward");plt.legend();plt.grid(True)
        plt.savefig(f"{self.__class__.__name__}_rewards.png");print(f"\nPlot saved to {self.__class__.__name__}_rewards.png")

class ShadowAwareTrainer(BaseTrainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.analytics = ContinuousPirouetteAnalytics()
        self.shadow_detector = ContinuousShadowRegionDetector(self.analytics)
    def run_analysis(self):
        print(f"\n--- Running Shadow Analysis ---")
        suggestions = self.shadow_detector.analyze_and_suggest(np.array(self.agent.td_errors))
        self.agent.apply_suggestions(suggestions)
        if 'batch_size' in suggestions:
            old = self.batch_size; self.batch_size = suggestions['batch_size']; print(f"Batch Size:{old}->{self.batch_size}")
        print("-----------------------------\n")

class PirouetteInformedTrainer(BaseTrainer):
    def run_analysis(self):
        print(f"\n--- Running Pirouette Analysis (Fractal Dimension) ---")
        # Use the norm of the state vectors to get a univariate time series
        state_norms = np.linalg.norm(np.array(self.state_history), axis=1)
        hfd = calculate_hfd(state_norms)
        print(f"INFO: State Trajectory HFD is {hfd:.4f}.")
        
        suggestions = {}
        # Get recent performance to decide how to react to complexity
        recent_avg_reward = np.mean(self.reward_history[-self.analysis_freq:])
        
        # High HFD (>1.8) -> Chaotic movement. Force stability.
        if hfd > 1.8:
            print("INFO: High complexity detected (chaotic). Forcing stability.")
            suggestions.update({'critic_lr': 5e-5, 'actor_lr': 5e-5, 'alpha': 0.05})
        # Low HFD (<1.5) -> Simple movement. Could be good or bad.
        elif hfd < 1.5:
            # If reward is low, agent is stuck. Break it out.
            if recent_avg_reward < 200:
                print("INFO: Low complexity and low reward (stuck). Encouraging exploration.")
                suggestions.update({'critic_lr': 3e-4, 'actor_lr': 3e-4, 'alpha': 0.3})
            # If reward is high, agent is efficient. Fine-tune.
            else:
                print("INFO: Low complexity and high reward (efficient). Fine-tuning.")
                suggestions.update({'critic_lr': 1e-5, 'actor_lr': 1e-5, 'alpha': 0.1})
        # Mid-range HFD -> Standard operation
        else:
            print("INFO: Healthy complexity detected. Standard parameters.")
            suggestions.update({'critic_lr': 3e-4, 'actor_lr': 3e-4, 'alpha': 0.2})
        
        self.agent.apply_suggestions(suggestions)
        print("------------------------------------------------------\n")

# --- Main Execution ---
if __name__ == "__main__":
    if TRAINER_TYPE == 'SHADOW':
        trainer = ShadowAwareTrainer(ENV_NAME, NUM_EPISODES, MAX_STEPS_PER_EPISODE, ANALYSIS_FREQUENCY)
    elif TRAINER_TYPE == 'PIROUETTE':
        trainer = PirouetteInformedTrainer(ENV_NAME, NUM_EPISODES, MAX_STEPS_PER_EPISODE, ANALYSIS_FREQUENCY)
    else:
        raise ValueError(f"Unknown trainer type: {TRAINER_TYPE}")
    
    trainer.train()