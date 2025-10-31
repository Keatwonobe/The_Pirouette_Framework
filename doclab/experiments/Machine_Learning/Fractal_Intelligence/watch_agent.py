import torch
import gymnasium as gym
import numpy as np
import time

# --- This is the same Actor class from your trainer ---
class Actor(torch.nn.Module):
    def __init__(self, s, a, h=256):
        super().__init__()
        self.n = torch.nn.Sequential(torch.nn.Linear(s, h), torch.nn.ReLU(), torch.nn.Linear(h, h), torch.nn.ReLU())
        self.m = torch.nn.Linear(h, a)
        self.ls = torch.nn.Linear(h, a)
    def forward(self, s):
        x = self.n(s)
        return self.m(x), torch.clamp(self.ls(x), -20, 2)

# --- Configuration ---
# IMPORTANT: Update this path to point to one of your best models from the 'pirouette_fit_models' directory.
# For example, if rank 5 was your best model.
MODEL_TO_LOAD = "./pirouette_fit_models/rank_5/actor.pth" 
ENV_NAME = 'Ant-v5'
MAX_STEPS = 1000

# --- Load the Model ---
device = torch.device("cpu")
env_temp = gym.make(ENV_NAME)
state_dim = env_temp.observation_space.shape[0]
action_dim = env_temp.action_space.shape[0]

actor = Actor(state_dim, action_dim).to(device)
try:
    actor.load_state_dict(torch.load(MODEL_TO_LOAD, map_location=device))
    print(f"Successfully loaded model from {MODEL_TO_LOAD}")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_TO_LOAD}")
    print("Please update the MODEL_TO_LOAD variable to a valid path.")
    exit()

actor.eval() # Set the model to evaluation mode

# --- Create Rendered Environment ---
# The 'human' render mode opens a live window
env = gym.make(ENV_NAME, render_mode='human')
s, _ = env.reset()

# --- Run one episode ---
for _ in range(MAX_STEPS):
    s_tensor = torch.tensor(s, dtype=torch.float32, device=device).unsqueeze(0)
    
    with torch.no_grad():
        mean, _ = actor(s_tensor)
        action = torch.tanh(mean).cpu().numpy().flatten()
    
    s, _, term, trunc, _ = env.step(action)
    time.sleep(0.01) # Slow down rendering to make it watchable

    if term or trunc:
        s, _ = env.reset()

env.close()