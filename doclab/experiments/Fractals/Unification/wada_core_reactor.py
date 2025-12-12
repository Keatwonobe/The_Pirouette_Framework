import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from scipy.spatial import Delaunay
from numba import njit, prange
import time

# ==========================================
# 1. THE GEOMETRY ENGINE (High Precision)
# ==========================================

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
    
    # Extreme bias towards the "Skeleton" to capture the crackle
    pdf = np.ones_like(oracle_map, dtype=float) * 0.01
    pdf[boundaries] = 15.0 
    pdf /= pdf.sum()
    
    indices = np.arange(pdf.size)
    chosen = np.random.choice(indices, size=n_points, replace=False, p=pdf.flatten())
    py, px = np.unravel_index(chosen, oracle_map.shape)
    
    scale = (2.0 * zoom) / res; cx, cy = res/2, res/2
    pts_x = (px - cx) * scale + np.random.uniform(-0.5, 0.5, n_points)*scale*0.1
    pts_y = (py - cy) * scale + np.random.uniform(-0.5, 0.5, n_points)*scale*0.1
    points = np.column_stack((pts_x, pts_y))
    
    tri = Delaunay(points)
    adj = [[] for _ in range(n_points)]
    for simplex in tri.simplices:
        for i in range(3):
            u, v = simplex[i], simplex[(i+1)%3]
            adj[u].append(v); adj[v].append(u)
    return points, adj, tri

# ==========================================
# 2. OPTIMIZED INTERPOLATION (The Speedup)
# ==========================================

def precalculate_interpolation_weights(tri, grid_x, grid_y):
    # This pre-bakes the barycentric coordinates so we can render 40k points instantly
    grid_points = np.column_stack((grid_x.flatten(), grid_y.flatten()))
    simplex_indices = tri.find_simplex(grid_points)
    valid_mask = simplex_indices != -1
    vertex_indices = tri.simplices[simplex_indices[valid_mask]]
    
    points_p0 = tri.points[vertex_indices[:, 0]]
    points_p1 = tri.points[vertex_indices[:, 1]]
    points_p2 = tri.points[vertex_indices[:, 2]]
    
    P = grid_points[valid_mask]
    def area_det(p1, p2, p3):
        return (p2[:, 0] - p1[:, 0]) * (p3[:, 1] - p1[:, 1]) - (p3[:, 0] - p1[:, 0]) * (p2[:, 1] - p1[:, 1])

    Area = area_det(points_p0, points_p1, points_p2)
    w0 = area_det(P, points_p1, points_p2) / Area
    w1 = area_det(P, points_p2, points_p0) / Area
    w2 = area_det(P, points_p0, points_p1) / Area

    all_weights = np.zeros((grid_points.shape[0], 3))
    all_weights[valid_mask] = np.column_stack((w0, w1, w2))
    all_indices = np.zeros((grid_points.shape[0], 3), dtype=int)
    all_indices[valid_mask] = vertex_indices
    return all_indices, all_weights, valid_mask, grid_x.shape

def fast_interp_update(point_values, indices, weights, valid_mask, output_shape):
    v0 = point_values[indices[valid_mask, 0]]
    v1 = point_values[indices[valid_mask, 1]]
    v2 = point_values[indices[valid_mask, 2]]
    interpolated = (weights[valid_mask, 0] * v0 + weights[valid_mask, 1] * v1 + weights[valid_mask, 2] * v2)
    full_grid = np.full(indices.shape[0], np.nan)
    full_grid[valid_mask] = interpolated
    return full_grid.reshape(output_shape)

# ==========================================
# 3. THE REACTOR CORE SIMULATION
# ==========================================

class CoreReactor:
    def __init__(self, points, adj_list, temp=2.8):
        self.n = len(points)
        self.adj = adj_list
        self.temp = temp
        self.spins = np.random.choice([-1, 1], size=self.n)
        self.history = [] # To track total system energy (The Heartbeat)
        
    def step(self, frames=1):
        for _ in range(frames):
            indices = np.random.randint(0, self.n, size=self.n)
            for idx in indices:
                s = self.spins[idx]
                h = sum(self.spins[n] for n in self.adj[idx])
                dE = 2 * s * h
                if dE <= 0 or np.random.rand() < np.exp(-dE / self.temp):
                    self.spins[idx] *= -1
                    
        # Record Metric: Total Frustration of the System
        # Sum of all local energies (positive = bad)
        total_E = 0
        for i in range(self.n):
            h = sum(self.spins[n] for n in self.adj[i])
            total_E += -1 * self.spins[i] * h
        self.history.append(total_E / self.n) # Normalize
        if len(self.history) > 200: self.history.pop(0) # Keep window moving

    def get_frustration(self):
        energies = np.zeros(self.n)
        for i in range(self.n):
            h = sum(self.spins[n] for n in self.adj[i])
            energies[i] = -1 * self.spins[i] * h
        return energies

# ==========================================
# 4. EXECUTION
# ==========================================

RES = 1000 
ZOOM = 2400000000000000000 # THE CORE (Origin)
N_POINTS = 40000 # CRACKLING RESOLUTION
TEMP = 2.8 
FRAMES = 120

print(f"[-] Initializing Core Reactor ({N_POINTS} nodes)...")
oracle = generate_oracle_map(RES, ZOOM)
pts, adj, tri = get_wada_graph(N_POINTS, oracle, ZOOM)

print(f"[-] Pre-calculating 4K Mesh...")
grid_x, grid_y = np.mgrid[-ZOOM:ZOOM:800j, -ZOOM:ZOOM:800j]
indices, weights, valid_mask, out_shape = precalculate_interpolation_weights(tri, grid_x, grid_y)

reactor = CoreReactor(pts, adj, temp=TEMP)

# Setup Dual Plot (Map + Geiger Counter)
fig = plt.figure(figsize=(10, 12), facecolor='black')
gs = fig.add_gridspec(6, 1) # 5 rows map, 1 row graph

ax_map = fig.add_subplot(gs[0:5, 0])
ax_graph = fig.add_subplot(gs[5, 0])

ax_map.set_facecolor('black'); ax_map.axis('off')
ax_graph.set_facecolor('#111111'); ax_graph.grid(color='#333333')
ax_graph.set_title("Total System Frustration (The Heartbeat)", color='orange', fontsize=10)
ax_graph.tick_params(colors='white')

# Initial Data
im = ax_map.imshow(np.zeros((800, 800)), origin='lower', extent=[-ZOOM, ZOOM, -ZOOM, ZOOM], 
               cmap='inferno', vmin=-4, vmax=4)
ax_map.contour(oracle, levels=[0.5, 1.5, 2.5], extent=[-ZOOM, ZOOM, -ZOOM, ZOOM], colors='cyan', linewidths=0.3, alpha=0.3)

line, = ax_graph.plot([], [], color='cyan', linewidth=1.5)
ax_graph.set_xlim(0, 200)
ax_graph.set_ylim(-1, 2) # Adjust based on expected energy range

title_text = ax_map.text(0.02, 0.95, "Core Dynamics", transform=ax_map.transAxes, color='white', fontsize=14, fontfamily='monospace')

def animate(i):
    reactor.step(frames=2)
    
    # 1. Update Map
    energy = reactor.get_frustration()
    heatmap = fast_interp_update(energy, indices, weights, valid_mask, out_shape)
    im.set_data(heatmap.T)
    
    # 2. Update Graph
    y_data = reactor.history
    x_data = np.arange(len(y_data))
    line.set_data(x_data, y_data)
    if len(y_data) > 0:
        ax_graph.set_ylim(min(y_data)-0.1, max(y_data)+0.1)
    
    title_text.set_text(f"T={TEMP} | Particles={N_POINTS} | Frame {i}")
    if i % 10 == 0: print(f"Rendering frame {i}...")
    return im, line, title_text

print(f"[-] Igniting Reactor...")
anim = animation.FuncAnimation(fig, animate, frames=FRAMES, interval=50, blit=False)
anim.save('wada_core_reactor.gif', writer=PillowWriter(fps=20))
print("[+] Experiment Complete. Saved to 'wada_core_reactor.gif'")