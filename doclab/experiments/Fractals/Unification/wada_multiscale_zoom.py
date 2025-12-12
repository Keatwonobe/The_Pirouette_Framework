import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from scipy.spatial import Delaunay
from scipy.interpolate import LinearNDInterpolator
from numba import njit, prange

# ==========================================
# 1. THE PRISM SOLVER (Scale-Invariant Physics)
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
    # This generates the "Truth" at any specific zoom level
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
    pdf[boundaries] = 8.0 # High bias to catch the "strands" at every scale
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
    return points, adj

# ==========================================
# 2. THE FRUSTRATION ENGINE
# ==========================================

@njit(fastmath=True)
def calculate_frustration_fast(spins, adj_indices, adj_indptr):
    # JIT-compiled energy calculation for speed
    n = len(spins)
    energy = np.zeros(n)
    for i in range(n):
        start = adj_indptr[i]
        end = adj_indptr[i+1]
        h = 0.0
        for k in range(start, end):
            neighbor = adj_indices[k]
            h += spins[neighbor]
        energy[i] = -1 * spins[i] * h
    return energy

class LayerScanner:
    def __init__(self, points, adj_list, temp=2.8):
        self.n = len(points)
        self.temp = temp
        self.spins = np.random.choice([-1, 1], size=self.n)
        
        # Convert List of Lists to CSR-like structure for Numba
        # (Flattened array + pointers)
        self.adj_indices = []
        self.adj_indptr = [0]
        for neighbors in adj_list:
            self.adj_indices.extend(neighbors)
            self.adj_indptr.append(len(self.adj_indices))
        
        self.adj_indices = np.array(self.adj_indices, dtype=np.int32)
        self.adj_indptr = np.array(self.adj_indptr, dtype=np.int32)

    def relax(self, steps=100):
        # Quick Metropolis burn-in to find the "Strands"
        # We do this in Python because passing the ragged structure to JIT is complex
        # but for 100 steps it's fine.
        for _ in range(steps):
            indices = np.random.randint(0, self.n, size=self.n // 2)
            for idx in indices:
                s = self.spins[idx]
                # Re-calculate local H (slow path, but robust)
                start, end = self.adj_indptr[idx], self.adj_indptr[idx+1]
                h = np.sum(self.spins[self.adj_indices[start:end]])
                dE = 2 * s * h
                if dE <= 0 or np.random.rand() < np.exp(-dE / self.temp):
                    self.spins[idx] *= -1
                    
    def get_energy(self):
        return calculate_frustration_fast(self.spins, self.adj_indices, self.adj_indptr)

# ==========================================
# 3. THE COSMIC ZOOM
# ==========================================

RES = 600
N_POINTS = 12000 # Enough to define strands, light enough to re-mesh 60 times
TEMP = 2.8 
FRAMES = 60

# Zoom Sequence: Logarithmic pull-back
# From Microscopic (0.1) to Macroscopic (3.0)
ZOOMS = np.logspace(np.log10(8.0), np.log10(5.0), FRAMES)

fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.set_facecolor('black')
ax.axis('off')

# Init image
im = ax.imshow(np.zeros((RES, RES)), origin='lower', cmap='inferno', vmin=-4, vmax=4)
title_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

def animate(i):
    current_zoom = ZOOMS[i]
    
    # 1. GENERATE LAYER (The Oracle)
    # We re-calculate the map at this specific scale
    oracle = generate_oracle_map(RES, current_zoom)
    
    # 2. GENERATE NODES (The Mesh)
    pts, adj = get_wada_graph(N_POINTS, oracle, current_zoom)
    
    # 3. FIND FRUSTRATION (The Physics)
    scanner = LayerScanner(pts, adj, temp=TEMP)
    scanner.relax(steps=60) # Fast burn-in to let strands form
    energy = scanner.get_energy()
    
    # 4. RENDER (The Interpolation)
    grid_x, grid_y = np.mgrid[-current_zoom:current_zoom:600j, -current_zoom:current_zoom:600j]
    interp = LinearNDInterpolator(pts, energy)
    heatmap = interp(grid_x, grid_y)
    
    # Update Plot
    im.set_data(heatmap.T)
    im.set_extent([-current_zoom, current_zoom, -current_zoom, current_zoom])
    
    # Update Axis limits to match zoom (creates the zoom effect)
    ax.set_xlim(-current_zoom, current_zoom)
    ax.set_ylim(-current_zoom, current_zoom)
    
    title_text.set_text(f"Scale: {current_zoom:.4f} | Frustration Strands")
    print(f"Rendering Layer {i+1}/{FRAMES} (Zoom={current_zoom:.2f})...")
    
    return im, title_text

print(f"[-] Starting Multiscale Scan...")
anim = animation.FuncAnimation(fig, animate, frames=FRAMES, interval=80, blit=False)
anim.save('wada_multiscale_zoom.gif', writer=PillowWriter(fps=12))
print("[+] Scan Complete. Saved to 'wada_multiscale_zoom.gif'")