import numpy as np
import h5py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
from scipy.ndimage import laplace
import os
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("RENDERER")

# --- PART 1: THE SCANNER (Generating the Data) ---
class ManifoldMRIScanner:
    def __init__(self, resolution=200, max_steps=100, bounds=2.0, filename="wada_deep_mri.h5"):
        self.res = resolution
        self.steps = max_steps
        self.bounds = bounds
        self.filename = filename
        self.dt = 0.1
        self.epsilon = 1e-5 
        
    def _initialize_grid(self):
        # Reality Grid
        m = np.linspace(-self.bounds, self.bounds, self.res)
        l = np.linspace(-self.bounds, self.bounds, self.res)
        M, L = np.meshgrid(m, l)
        self.state_r = np.stack([M, L, np.zeros_like(M), np.zeros_like(L)], axis=0)
        
        # Shadow Grid
        dist_m = M + self.epsilon
        dist_l = L + self.epsilon
        self.state_s = np.stack([dist_m, dist_l, np.zeros_like(M), np.zeros_like(L)], axis=0)
        
    def _step_physics(self, state):
        m, l, pm, pl = state[0], state[1], state[2], state[3]
        pm -= 0.5 * self.dt * (m + 2*m*l)
        pl -= 0.5 * self.dt * (l + m**2 - l**2)
        m += self.dt * pm
        l += self.dt * pl
        pm -= 0.5 * self.dt * (m + 2*m*l)
        pl -= 0.5 * self.dt * (l + m**2 - l**2)
        return state

    def run_scan(self):
        self._initialize_grid()
        with h5py.File(self.filename, 'w') as f:
            dset_div = f.create_dataset("divergence", (self.steps, self.res, self.res), dtype='float32')
            dset_delta = f.create_dataset("delta_gradient", (self.steps, self.res, self.res), dtype='float32')
            f.attrs['resolution'] = self.res
            f.attrs['bounds'] = self.bounds
            
            for t in range(self.steps):
                self.state_r = self._step_physics(self.state_r)
                self.state_s = self._step_physics(self.state_s)
                
                diff = self.state_r[:2] - self.state_s[:2]
                dist = np.sqrt(diff[0]**2 + diff[1]**2)
                log_div = np.log(dist / self.epsilon + 1e-9)
                delta_map = np.abs(laplace(log_div))
                
                r2 = self.state_r[0]**2 + self.state_r[1]**2
                escaped = r2 > 20.0
                log_div[escaped] = 10.0
                
                dset_div[t, :, :] = log_div.astype('float32')
                dset_delta[t, :, :] = delta_map.astype('float32')

# --- PART 2: THE RENDERER (Making the GIF) ---
class ManifoldRenderer:
    def __init__(self, filename="wada_manifold_mri.h5"):
        self.filename = filename
        self.f = h5py.File(filename, 'r')
        self.res = self.f.attrs['resolution']
        self.bounds = self.f.attrs['bounds']
        self.steps = self.f['delta_gradient'].shape[0]

    def animate_mri_scan(self, save_file=None):
        fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor='#0f0f0f')
        
        div_0 = self.f['divergence'][0]
        delta_0 = self.f['delta_gradient'][0]
        
        # Calculate dynamic limits based on the middle of the simulation for better contrast
        div_vmax = np.percentile(self.f['divergence'][self.steps//2], 99)
        delta_vmax = np.percentile(self.f['delta_gradient'][self.steps//2], 98)

        extent = [-self.bounds, self.bounds, -self.bounds, self.bounds]
        
        # Left Plot: Divergence
        img_div = axes[0].imshow(div_0, cmap='magma', origin='lower', extent=extent, vmin=0, vmax=div_vmax)
        axes[0].set_title("Raw Lyapunov Divergence", color='white')
        axes[0].axis('off')
        
        # Right Plot: Delta
        img_delta = axes[1].imshow(delta_0, cmap='viridis_r', origin='lower', extent=extent, vmin=0, vmax=delta_vmax)
        c_map = mcolors.LinearSegmentedColormap.from_list("viridis_r", ["black", "cyan", "white"])
        img_delta.set_cmap(c_map)
        axes[1].set_title("The Delta (Structure)", color='white')
        axes[1].axis('off')

        title_text = fig.suptitle(f"Z-Slice: 0 / {self.steps}", color='white', fontsize=16)

        def update(frame):
            d = self.f['divergence'][frame]
            g = self.f['delta_gradient'][frame]
            img_div.set_data(d)
            img_delta.set_data(g)
            title_text.set_text(f"Z-Slice: {frame}")
            return img_div, img_delta, title_text

        # Animate
        ani = animation.FuncAnimation(fig, update, frames=range(0, self.steps, 1), blit=True, interval=50)
        
        if save_file:
            print(f"Rendering GIF to {save_file}...")
            # Use PillowWriter for GIF support
            ani.save(save_file, writer='pillow', fps=20)
            print("Render Complete.")
        
        self.f.close()

# --- EXECUTION ---
# 1. Run the Physics Simulation
print("Initializing Scanner...")
# Using 200 resolution and 80 steps for a balance of speed and quality
scanner = ManifoldMRIScanner(resolution=200, max_steps=80, bounds=2.0)
scanner.run_scan()

# 2. Render the GIF
print("Initializing Renderer...")
renderer = ManifoldRenderer()
renderer.animate_mri_scan(save_file="manifold_chaos.gif")