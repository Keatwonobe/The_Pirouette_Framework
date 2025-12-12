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
# Standard Prism-Folded Wada Generation

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
    pdf[boundaries] = 8.0 
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
# 2. THE THERMOGRAPHER (Frustration Calc)
# ==========================================

class FrustrationCinema:
    def __init__(self, points, adj_list, temp=2.6):
        self.points = points
        self.adj = adj_list
        self.n = len(points)
        self.temp = temp
        self.spins = np.random.choice([-1, 1], size=self.n)
        
        # We need a colormap for energy
        self.cmap = plt.cm.inferno
        
    def update_physics(self, frames=1):
        for _ in range(frames):
            indices = np.random.randint(0, self.n, size=self.n)
            for idx in indices:
                s = self.spins[idx]
                h = sum(self.spins[n] for n in self.adj[idx])
                dE = 2 * s * h
                if dE <= 0 or np.random.rand() < np.exp(-dE / self.temp):
                    self.spins[idx] *= -1

    def get_energy_colors(self):
        # Calculate Local Energy per node
        # E = -s * sum(neighbors)
        # If aligned (Happy): E is negative.
        # If anti-aligned (Frustrated): E is positive.
        
        energies = np.zeros(self.n)
        for i in range(self.n):
            h = sum(self.spins[n] for n in self.adj[i])
            energies[i] = -1 * self.spins[i] * h
            
        # Normalize for visualization
        # Typical range for hexagonal lattice is -6 to +6
        # We want High Energy (positive) to be bright
        
        norm_e = (energies + 6) / 12.0 # Map -6..6 to 0..1 roughly
        norm_e = np.clip(norm_e, 0, 1)
        
        return self.cmap(norm_e)

# ==========================================
# 3. ACTION!
# ==========================================

RES = 800
ZOOM = 2.0
N_POINTS = 5000
TEMP = 2.6 # The Critical "Resurrection" Temp

print(f"[-] Building Set...")
oracle = generate_oracle_map(RES, ZOOM)
pts, adj = get_wada_graph(N_POINTS, oracle, ZOOM)

print(f"[-] Initializing Thermal Camera (T={TEMP})...")
cinema = FrustrationCinema(pts, adj, temp=TEMP)

fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.set_facecolor('black')
ax.axis('off')
ax.set_xlim(-ZOOM, ZOOM)
ax.set_ylim(-ZOOM, ZOOM)

# Background: Faint Oracle
ax.imshow(oracle, origin='lower', extent=[-ZOOM, ZOOM, -ZOOM, ZOOM], cmap='twilight', alpha=0.3)

# Foreground: The Energy
scatter = ax.scatter(pts[:,0], pts[:,1], s=6, c=cinema.get_energy_colors())

title_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')
stat_text = ax.text(0.02, 0.92, "", transform=ax.transAxes, color='orange', fontsize=10, fontfamily='monospace')

def animate(i):
    cinema.update_physics(frames=1)
    
    # Update Colors based on Energy
    colors = cinema.get_energy_colors()
    scatter.set_color(colors)
    
    title_text.set_text(f"Frustration Dynamics (Energy Flow)")
    stat_text.set_text(f"Temp: {TEMP} | Frame: {i}")
    
    if i % 10 == 0: print(f"Rendering frame {i}...")
    return scatter, title_text, stat_text

print(f"[-] Filming Heatmap...")
anim = animation.FuncAnimation(fig, animate, frames=100, interval=50, blit=True)
anim.save('wada_frustration_flow.gif', writer=PillowWriter(fps=15))
print("[+] MRI Complete. Saved to 'wada_frustration_flow.gif'")