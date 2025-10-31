import torch
import gymnasium as gym
import numpy as np
import imageio
from PIL import Image # You need to install this: pip install Pillow

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
# Update this path to your best model
MODEL_TO_LOAD = "./pirouette_fit_models_seed_42/rank_10/actor.pth" 
ENV_NAME = 'Ant-v5'
GIF_FILENAME = "ant_performance_optimized.gif"
MAX_STEPS = 1000
RESIZE_FACTOR = 0.5 # Resize to 50% of original resolution
FRAME_SKIP = 2 # Save every 2nd frame

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
    exit()
actor.eval()

# --- Create Rendered Environment ---
env = gym.make(ENV_NAME, render_mode='rgb_array')
s, _ = env.reset()

frames = []
print("Running episode to generate optimized frames...")

# --- Run episode and record optimized frames ---
for step in range(MAX_STEPS):
    # --- OPTIMIZATION HAPPENS HERE ---
    if step % FRAME_SKIP == 0:
        frame = env.render()
        pil_img = Image.fromarray(frame)
        new_size = (int(pil_img.width * RESIZE_FACTOR), int(pil_img.height * RESIZE_FACTOR))
        resized_img = pil_img.resize(new_size, Image.Resampling.LANCZOS)
        frames.append(np.array(resized_img))

    s_tensor = torch.tensor(s, dtype=torch.float32, device=device).unsqueeze(0)
    
    with torch.no_grad():
        mean, _ = actor(s_tensor)
        action = torch.tanh(mean).cpu().numpy().flatten()
    
    s, _, term, trunc, _ = env.step(action)

    if term or trunc:
        break
# We still need to call render() every step to keep the display buffer updated, even if we don't save the frame.
    else:
        env.render()


env.close()

# --- Save frames as a GIF ---
print(f"Saving {len(frames)} optimized frames to {GIF_FILENAME}...")
imageio.mimsave(GIF_FILENAME, frames, fps=30)
print("Optimized GIF creation complete.")