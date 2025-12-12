import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from scipy.spatial import Delaunay
from numba import njit, prange
import time

# ==========================================
# 1. THE STAGE (Oracle & Graph)
# ==========================================
# Re-using your optimized pipeline for consistent geometry

@njit(fastmath=True)
def get_basin_single(m, l, t_max=60.0, dt=0.05, escape_r2=16.0):
    pm, pl = 0.0, 0.0
    steps = int(t_max / dt)
    sigma = 1.0
    for _ in range(steps):
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        m += dt * pm; l += dt * pl
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        if m*m + l*l > escape_r2:
            angle = np.arctan2(l, m)
            if angle > 0.5 and angle < 2.6: return 1
            elif angle <= -2.6 or angle >= 2.6: return 2
            else: return 3
    return 0

@njit(parallel=True, fastmath=True)
def generate_oracle_map(res, zoom):
    out_map = np.zeros((res, res), dtype=np.int8)
    cx = (res - 1) / 2.0; cy = (res - 1) / 2.0; scale = (2.0 * zoom) / res
    deg120 = 2.094395; deg240 = 4.188790
    for y in prange(res):
        for x in range(res):
            px = (x - cx) * scale; py = (y - cy) * scale
            r = np.sqrt(px*px + py*py); theta = np.arctan2(py, px)
            if theta < 0: theta += 2*np.pi
            rot = 0
            if theta >= deg240: theta -= deg240; rot = 2
            elif theta >= deg120: theta -= deg120; rot = 1
            eff_px = r * np.cos(theta); eff_py = r * np.sin(theta)
            basin = get_basin_single(eff_px, eff_py)
            if basin != 0: out_map[y, x] = (basin - 1 + rot) % 3 + 1
    return out_map

def get_wada_graph(n_points, oracle_map, zoom):
    res = oracle_map.shape[0]
    grad_x = np.abs(np.diff(oracle_map, axis=1, append=oracle_map[:, -1:]))
    grad_y = np.abs(np.diff(oracle_map, axis=0, append=oracle_map[-1:, :]))
    boundaries = (grad_x + grad_y) > 0
    pdf = np.ones_like(oracle_map, dtype=float) * 0.05
    pdf[boundaries] = 8.0 # High contrast for the animation
    pdf /= pdf.sum()
    indices = np.arange(pdf.size)
    chosen = np.random.choice(indices, size=n_points, replace=False, p=pdf.flatten())
    py, px = np.unravel_index(chosen, oracle_map.shape)
    scale = (2.0 * zoom) / res; cx, cy = res/2, res/2
    pts_x = (px - cx) * scale + np.random.uniform(-0.5, 0.5, n_points)*scale
    pts_y = (py - cy) * scale + np.random.uniform(-0.5, 0.5, n_points)*scale
    points = np.column_stack((pts_x, pts_y))
    tri = Delaunay(points)
    adj = [[] for _ in range(n_points)]
    for simplex in tri.simplices:
        for i in range(3):
            u, v = simplex[i], simplex[(i+1)%3]
            adj[u].append(v); adj[v].append(u)
    return points, adj

# ==========================================
# 2. THE CINEMATOGRAPHER
# ==========================================

class WadaCinema:
    def __init__(self, points, adj_list, temp=2.6):
        self.points = points
        self.adj = adj_list
        self.n = len(points)
        self.temp = temp
        self.spins = np.random.choice([-1, 1], size=self.n)
        
        # Color Palettes
        # Spin +1: Cyan (#00ffff)
        # Spin -1: Magenta (#ff00ff)
        self.colors = np.zeros((self.n, 4)) # RGBA
        
    def update_physics(self, frames=1):
        # Metropolis Step
        for _ in range(frames):
            # We do 1 Monte Carlo Sweep (try to flip N times)
            indices = np.random.randint(0, self.n, size=self.n)
            
            # Vectorized neighbor lookup is hard with ragged lists, 
            # so we use a fast Python loop (compiled via Numba would be better, but this is okay for visualization)
            for idx in indices:
                s = self.spins[idx]
                h = sum(self.spins[n] for n in self.adj[idx]) # Local Field
                dE = 2 * s * h
                if dE <= 0 or np.random.rand() < np.exp(-dE / self.temp):
                    self.spins[idx] *= -1

    def get_colors(self):
        # Map spins to colors
        # +1 -> Cyan (0, 1, 1, 1)
        # -1 -> Magenta (1, 0, 1, 1)
        c = np.zeros((self.n, 4))
        mask = (self.spins == 1)
        c[mask] = [0, 1, 1, 0.8]      # Cyan
        c[~mask] = [1, 0, 0.8, 0.8]   # Magenta
        return c

# ==========================================
# 3. ACTION!
# ==========================================

RES = 800
ZOOM = 2.0
N_POINTS = 4000
TEMP = 2.6 # The Resurrection Temperature

print(f"[-] Building Set ({RES}x{RES} Oracle)...")
oracle = generate_oracle_map(RES, ZOOM)

print(f"[-] Casting Actors ({N_POINTS} particles)...")
pts, adj = get_wada_graph(N_POINTS, oracle, ZOOM)

print(f"[-] Initializing Simulation (T={TEMP})...")
cinema = WadaCinema(pts, adj, temp=TEMP)

# Setup Plot
fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.set_facecolor('black')
ax.axis('off')
ax.set_xlim(-ZOOM, ZOOM)
ax.set_ylim(-ZOOM, ZOOM)

# Background: Faint Oracle Map
ax.imshow(oracle, origin='lower', extent=[-ZOOM, ZOOM, -ZOOM, ZOOM], cmap='twilight', alpha=0.3)

# Foreground: The Spins
scatter = ax.scatter(pts[:,0], pts[:,1], s=4, c=cinema.get_colors())

# Text Stats
title_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')
stat_text = ax.text(0.02, 0.92, "", transform=ax.transAxes, color='yellow', fontsize=10, fontfamily='monospace')

def animate(i):
    # Run physics
    cinema.update_physics(frames=1) # 1 Sweep per frame
    
    # Update Visuals
    scatter.set_color(cinema.get_colors())
    
    # Calculate Stats
    M = np.abs(np.sum(cinema.spins)) / N_POINTS
    
    title_text.set_text(f"Wada Spin Glass Dynamics (T={TEMP:.1f})")
    stat_text.set_text(f"Magnetization: {M:.3f} | Frame: {i}")
    
    if i % 10 == 0:
        print(f"Rendering frame {i}...")
        
    return scatter, title_text, stat_text

print(f"[-] filming...")
anim = animation.FuncAnimation(fig, animate, frames=120, interval=50, blit=True)

# Save
anim.save('wada_chaos_cinema.gif', writer=PillowWriter(fps=15))
print("[+] Cut! Print it. Saved to 'wada_chaos_cinema.gif'")