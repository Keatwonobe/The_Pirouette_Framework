# pirouette_triumvirate_trainer_v2.py
# This script implements the three-expert architecture (Ki, Ta, Gamma)
# to test the "fractal sensing" and "robotics bootstrapping" concepts.
# Version 2: Corrects the replay buffer sampling bug.

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Normal
import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
from collections import deque
import time
import os
import shutil
import random # <-- Added missing import

# --- Configuration ---
ENV_NAME = 'Ant-v5'
NUM_EPISODES = 2000
MAX_STEPS_PER_EPISODE = 1000
EVAL_FREQUENCY = 20
EVAL_EPISODES = 5
SEED = 42
MODEL_PATH = "./pirouette_triumvirate_models/"

# --- NEW: Triumvirate & Crucible Hyperparameters ---
FLUX_REWARD_WEIGHT = 0.5
PROPHET_QUIZ_INTERVAL = 10
PROPHET_PREDICTION_HORIZON = 50
LIDAR_RAYS = 16 # Number of rays for the Gamma-Prophet's sensor
CRUCIBLE_NOISE_LEVEL = 0.1 # Noise added to the Ki-signal for the Ta-Prophet to detect

# Set device and seeds
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
np.random.seed(SEED); torch.manual_seed(SEED); random.seed(SEED) # <-- Added random seed
if os.path.exists(MODEL_PATH): shutil.rmtree(MODEL_PATH)
os.makedirs(MODEL_PATH, exist_ok=True)
print(f"Using device: {device}")
print(f"Triumvirate models will be saved in: {MODEL_PATH}")


### --- Crucible Environment with LIDAR and Noise --- ###
class CrucibleAntEnv:
    """A wrapper for the Ant environment with hidden physics (Ki), virtual LIDAR (Gamma), and signal noise (Ta)."""
    def __init__(self, env_name, max_steps):
        print("Initializing Triumvirate Crucible Environment...")
        self.env = gym.make(env_name, render_mode=None)
        self.max_steps_per_episode = max_steps
        self.current_step = 0
        
        # Ki-Signal Parameters (Oscillating Gravity)
        self.gravity_period = self.max_steps_per_episode * 2
        self.gravity_base = -9.8
        self.gravity_amp = 4.0
        self.noise_level = CRUCIBLE_NOISE_LEVEL

        # The observation space is now a dictionary
        self.observation_space = gym.spaces.Dict({
            'state': self.env.observation_space,
            'lidar': gym.spaces.Box(low=0, high=1, shape=(LIDAR_RAYS,), dtype=np.float32)
        })
        self.action_space = self.env.action_space

    def reset(self, seed=None):
        self.current_step = 0
        self.update_gravity()
        obs, info = self.env.reset(seed=seed)
        lidar_scan = self._perform_lidar_scan()
        return {'state': obs, 'lidar': lidar_scan}, info

    def step(self, action):
        self.current_step += 1
        self.update_gravity()
        obs, reward, term, trunc, info = self.env.step(action)
        lidar_scan = self._perform_lidar_scan()
        return {'state': obs, 'lidar': lidar_scan}, reward, term, trunc, info

    def update_gravity(self):
        phase = (2 * np.pi * self.current_step) / self.gravity_period
        clean_gravity = self.gravity_base + self.gravity_amp * np.sin(phase)
        noise = np.random.normal(0, self.noise_level)
        self.env.unwrapped.model.opt.gravity[2] = clean_gravity + noise
        self.last_clean_gravity = clean_gravity # Store for Ta-Prophet's training

    def _perform_lidar_scan(self):
        # This is a simplified LIDAR. A real implementation would use mujoco's raycasting.
        # Here, we simulate it by measuring distance from center to a virtual boundary.
        qpos = self.env.unwrapped.data.qpos
        agent_pos = qpos[:2]
        
        # Define a virtual circular boundary for demonstration
        boundary_radius = 10.0
        distances = np.ones(LIDAR_RAYS) * boundary_radius # Default to max distance
        
        # This is a placeholder; a real implementation would be more complex
        # For now, let's return a simple vector based on agent's position
        for i in range(LIDAR_RAYS):
            angle = (2 * np.pi * i) / LIDAR_RAYS
            ray_vector = np.array([np.cos(angle), np.sin(angle)])
            # Simulate a simple wall at x=5
            if ray_vector[0] > 0 and agent_pos[0] < 5:
                 t = (5 - agent_pos[0]) / ray_vector[0]
                 if t > 0: distances[i] = min(distances[i], t)

        return np.clip(distances / boundary_radius, 0, 1).astype(np.float32)


    def get_future_clean_gravity(self, future_steps):
        """Predicts the clean gravity signal, used for training the Ki and Ta prophets."""
        future_gravities = []
        for i in range(1, future_steps + 1):
            future_step = self.current_step + i
            phase = (2 * np.pi * future_step) / self.gravity_period
            g = self.gravity_base + self.gravity_amp * np.sin(phase)
            future_gravities.append(g)
        return np.array(future_gravities)


### --- The Triumvirate Prophets --- ###
class Prophet(nn.Module):
    """Base class for a Prophet model."""
    def __init__(self, input_dim, output_dim, hidden_dim=128):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        self.loss_fn = nn.MSELoss()

    def train_step(self, input_data, target_data):
        input_t = torch.tensor(input_data, device=device, dtype=torch.float32).unsqueeze(0)
        target_t = torch.tensor(target_data, device=device, dtype=torch.float32).unsqueeze(0)
        self.optimizer.zero_grad()
        prediction = self.model(input_t)
        loss = self.loss_fn(prediction, target_t)
        loss.backward()
        self.optimizer.step()
        return loss.item()

# --- SAC Agent (Modified to handle Dict observations) ---
# Note: The core SAC logic is unchanged, only observation handling is adapted.
class Actor(nn.Module):
    def __init__(self,s,a,h=256):super().__init__();self.n=nn.Sequential(nn.Linear(s,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU());self.m=nn.Linear(h,a);self.ls=nn.Linear(h,a)
    def forward(self,s):x=self.n(s);return self.m(x),torch.clamp(self.ls(x),-20,2)
class Critic(nn.Module):
    def __init__(self,s,a,h=256):super().__init__();self.n=nn.Sequential(nn.Linear(s+a,h),nn.ReLU(),nn.Linear(h,h),nn.ReLU(),nn.Linear(h,1))
    def forward(self,s,a):return self.n(torch.cat([s,a],1))

class SACAgent:
    def __init__(self,e,h=256,lr=3e-4,g=0.99,t=0.005,a=0.2):
        self.env=e; self.state_dim,self.action_dim=e.observation_space['state'].shape[0],e.action_space.shape[0];self.gamma,self.tau,self.alpha=g,t,a
        self.action_scale=torch.tensor((e.action_space.high-e.action_space.low)/2.,device=device,dtype=torch.float32)
        self.action_bias=torch.tensor((e.action_space.high+e.action_space.low)/2.,device=device,dtype=torch.float32)
        self.actor=Actor(self.state_dim,self.action_dim,h).to(device);self.c1,self.c2=Critic(self.state_dim,self.action_dim,h).to(device),Critic(self.state_dim,self.action_dim,h).to(device)
        self.c1_t,self.c2_t=Critic(self.state_dim,self.action_dim,h).to(device),Critic(self.state_dim,self.action_dim,h).to(device)
        self.c1_t.load_state_dict(self.c1.state_dict());self.c2_t.load_state_dict(self.c2.state_dict())
        self.a_opt,self.c1_opt,self.c2_opt=optim.Adam(self.actor.parameters(),lr=lr),optim.Adam(self.c1.parameters(),lr=lr),optim.Adam(self.c2.parameters(),lr=lr)
        self.buffer=deque(maxlen=1_000_000)
    
    def select_action(self,s_dict,eval=False):
        s=torch.tensor(s_dict['state'],device=device,dtype=torch.float32).unsqueeze(0)
        m,ls=self.actor(s)
        a=torch.tanh(m) if eval else torch.tanh(Normal(m,ls.exp()).rsample())
        return(a.cpu().detach().numpy()[0]*self.action_scale.cpu().numpy())+self.action_bias.cpu().numpy()

    def push_to_buffer(self, s, a, r, s_, d):
        self.buffer.append((s['state'], a, r, s_['state'], d))

    def update(self,B):
        if len(self.buffer)<B:return
        # --- BUG FIX IS HERE ---
        s,a,r,s_,d=zip(*random.sample(self.buffer,B));s,a,r,s_,d=torch.tensor(np.array(s),device=device,dtype=torch.float32),torch.tensor(np.array(a),device=device,dtype=torch.float32),torch.tensor(np.array(r),device=device,dtype=torch.float32).unsqueeze(1),torch.tensor(np.array(s_),device=device,dtype=torch.float32),torch.tensor(np.array(d),device=device,dtype=torch.float32).unsqueeze(1)
        with torch.no_grad():
            m_,ls_=self.actor(s_);d_=Normal(m_,ls_.exp());z=d_.rsample();a_=torch.tanh(z);lp=d_.log_prob(z)-torch.log(1-a_.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
            tq1,tq2=self.c1_t(s_,a_),self.c2_t(s_,a_);tq=torch.min(tq1,tq2)-self.alpha*lp;tq=r+(1-d)*self.gamma*tq
        cq1,cq2=self.c1(s,a),self.c2(s,a);c1l,c2l=F.mse_loss(cq1,tq),F.mse_loss(cq2,tq)
        self.c1_opt.zero_grad();c1l.backward();self.c1_opt.step();self.c2_opt.zero_grad();c2l.backward();self.c2_opt.step()
        m,ls=self.actor(s);d=Normal(m,ls.exp());z=d.rsample();a_pi=torch.tanh(z);lp=d.log_prob(z)-torch.log(1-a_pi.pow(2)+1e-6);lp=lp.sum(1,keepdim=True)
        q1_pi,q2_pi=self.c1(s,a_pi),self.c2(s,a_pi);min_q_pi=torch.min(q1_pi,q2_pi);al=(self.alpha*lp-min_q_pi).mean();self.a_opt.zero_grad();al.backward();self.a_opt.step()
        for t,s_p in zip(self.c1_t.parameters(),self.c1.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s_p.data*self.tau)
        for t,s_p in zip(self.c2_t.parameters(),self.c2.parameters()):t.data.copy_(t.data*(1.0-self.tau)+s_p.data*self.tau)


# --- The Main Trainer ---
class PirouetteTriumvirateTrainer:
    def __init__(self):
        self.env = CrucibleAntEnv(ENV_NAME, MAX_STEPS_PER_EPISODE)
        self.agent = SACAgent(self.env)
        
        # Initialize the Triumvirate
        state_dim = self.env.observation_space['state'].shape[0]
        self.ki_prophet = Prophet(state_dim, PROPHET_PREDICTION_HORIZON) # Predicts rhythm
        self.gamma_prophet = Prophet(LIDAR_RAYS, 4) # Predicts spatial structure (e.g., classifies into 4 types)
        self.ta_prophet = Prophet(state_dim, 1) # Predicts noise/error level
        
        # History logs
        self.eval_history, self.sigma_history, self.ta_history, self.gamma_history = [], [], [], []
        self.last_sigma = 0

    def train(self):
        start_time = time.time()
        for ep in range(1, NUM_EPISODES + 1):
            s, _ = self.env.reset(seed=SEED + ep)
            ep_r, ep_steps = 0, 0
            
            for step in range(1, MAX_STEPS_PER_EPISODE + 1):
                a = self.agent.select_action(s)
                s_next, r, term, trunc, info = self.env.step(a)
                done = term or trunc
                
                # --- Train the Prophets ---
                # 1. Ki-Prophet learns the clean signal
                future_g_clean = self.env.get_future_clean_gravity(PROPHET_PREDICTION_HORIZON)
                self.ki_prophet.train_step(s['state'], future_g_clean)

                # 2. Gamma-Prophet learns spatial structure from LIDAR
                # (Here we use a dummy target, a real task would have spatial labels)
                dummy_gamma_target = np.random.rand(4) 
                self.gamma_prophet.train_step(s['lidar'], dummy_gamma_target)

                # 3. Ta-Prophet learns to predict the noise (error of Ki-Prophet)
                with torch.no_grad():
                    ki_pred = self.ki_prophet.model(torch.tensor(s['state'], device=device, dtype=torch.float32))
                actual_noisy_g = self.env.env.unwrapped.model.opt.gravity[2]
                prediction_error = np.abs(ki_pred[0].item() - actual_noisy_g)
                self.ta_prophet.train_step(s['state'], np.array([prediction_error]))

                # --- Calculate Reward and Update Agent ---
                delta_sigma = self.ki_prophet.predictive_span - self.last_sigma if hasattr(self.ki_prophet, 'predictive_span') else 0
                flux_reward = FLUX_REWARD_WEIGHT * (delta_sigma / (np.linalg.norm(a) + 1e-6))
                total_reward = r + flux_reward
                
                self.agent.push_to_buffer(s, a, total_reward, s_next, done)
                self.agent.update(256)
                
                s = s_next; ep_r += r; ep_steps += 1
                if done: break
            
            if ep % PROPHET_QUIZ_INTERVAL == 0:
                self.run_prophet_quiz(s, ep, ep_r)

            if ep % EVAL_FREQUENCY == 0:
                self.run_evaluation()

        print(f"\nTraining finished in {time.time()-start_time:.2f}s.")
        self.plot_results()

    def run_prophet_quiz(self, s, ep, ep_r):
        # Ki-Prophet Quiz
        with torch.no_grad():
            ki_preds = self.ki_prophet.model(torch.tensor(s['state'], device=device, dtype=torch.float32)).cpu().numpy()
        future_g_clean = self.env.get_future_clean_gravity(PROPHET_PREDICTION_HORIZON)
        errors = np.abs(ki_preds - future_g_clean) / (np.abs(future_g_clean) + 1e-6)
        current_sigma = np.argmax(errors > 0.15) if np.any(errors > 0.15) else PROPHET_PREDICTION_HORIZON
        self.ki_prophet.predictive_span = current_sigma
        self.sigma_history.append(current_sigma)
        
        # Ta-Prophet & Gamma-Prophet logging
        with torch.no_grad():
            ta_coherence = 1 - torch.sigmoid(self.ta_prophet.model(torch.tensor(s['state'], device=device, dtype=torch.float32))).item()
            gamma_output = self.gamma_prophet.model(torch.tensor(s['lidar'], device=device, dtype=torch.float32)).cpu().numpy()
        self.ta_history.append(ta_coherence)
        self.gamma_history.append(np.argmax(gamma_output)) # Log the classified 'space type'

        print(f"Ep:{ep:04d} | Reward:{ep_r:7.2f} | σ(Ki):{current_sigma:02d} | Tₐ(Coherence):{ta_coherence:5.3f} | Γ(Space Type):{np.argmax(gamma_output)}")
        self.last_sigma = current_sigma
        
    def run_evaluation(self):
        eval_rewards = []
        for _ in range(EVAL_EPISODES):
            s, _ = self.env.reset()
            ep_r = 0
            for _ in range(MAX_STEPS_PER_EPISODE):
                a = self.agent.select_action(s, eval=True)
                s, r, term, trunc, _ = self.env.step(a)
                ep_r += r
                if term or trunc: break
            eval_rewards.append(ep_r)
        self.eval_history.append(np.mean(eval_rewards))
        print(f"  > Eval Score: {np.mean(eval_rewards):.2f}")

    def plot_results(self):
        fig, axs = plt.subplots(4, 1, figsize=(15, 20), sharex=True)
        fig.suptitle("Triumvirate Sensorium Training Analysis", fontsize=16)
        
        x_eval = np.arange(1, len(self.eval_history) + 1) * EVAL_FREQUENCY
        x_quiz = np.arange(1, len(self.sigma_history) + 1) * PROPHET_QUIZ_INTERVAL
        
        axs[0].plot(x_eval, self.eval_history, 'b-', label='Evaluation Score')
        axs[0].set_ylabel("Score"); axs[0].legend(); axs[0].grid(True)
        
        axs[1].plot(x_quiz, self.sigma_history, 'r-o', label='σ (Ki Predictive Span)')
        axs[1].set_ylabel("Predictive Span (σ)"); axs[1].legend(); axs[1].grid(True)

        axs[2].plot(x_quiz, self.ta_history, 'g-', label='Tₐ (Coherence Score)')
        axs[2].set_ylabel("Coherence (Tₐ)"); axs[2].legend(); axs[2].grid(True)
        
        axs[3].plot(x_quiz, self.gamma_history, 'm.', label='Γ (Spatial Class)')
        axs[3].set_ylabel("Space Type (Γ)"); axs[3].legend(); axs[3].grid(True)
        
        plt.xlabel("Episode")
        plt.tight_layout(rect=[0, 0.03, 1, 0.96])
        save_path = "pirouette_triumvirate_results.png"
        plt.savefig(save_path)
        print(f"\nPlot saved to {save_path}")

# --- Main Execution ---
if __name__ == "__main__":
    trainer = PirouetteTriumvirateTrainer()
    trainer.train()