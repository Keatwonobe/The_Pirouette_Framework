import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from scipy.spatial import Delaunay
from scipy.interpolate import LinearNDInterpolator
from numba import njit, prange

# ==========================================
# 1. THE GEOMETRY ENGINE (Oracle & Graph)
# ==========================================
# (Optimized Prism-Folded Wada Generation)

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
    pdf[boundaries] = 6.0 # Focus on the fractal edges
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
# 2. THE THERMODYNAMIC SIMULATOR
# ==========================================

class HeatmapEngine:
    def __init__(self, points, adj_list, temp=2.6):
        self.points = points
        self.adj = adj_list
        self.n = len(points)
        self.temp = temp
        self.spins = np.random.choice([-1, 1], size=self.n)
        
    def step(self, frames=1):
        for _ in range(frames):
            indices = np.random.randint(0, self.n, size=self.n)
            for idx in indices:
                s = self.spins[idx]
                h = sum(self.spins[n] for n in self.adj[idx])
                dE = 2 * s * h
                if dE <= 0 or np.random.rand() < np.exp(-dE / self.temp):
                    self.spins[idx] *= -1

    def get_frustration(self):
        # Calculate Local Frustration (Energy)
        # High positive value = High Frustration (Fighting neighbors)
        # Low negative value = Low Frustration (Happy)
        energies = np.zeros(self.n)
        for i in range(self.n):
            h = sum(self.spins[n] for n in self.adj[i])
            energies[i] = -1 * self.spins[i] * h
        return energies

# ==========================================
# 3. ANIMATION SETUP
# ==========================================

RES = 600 # Slightly lower res for smooth animation FPS
ZOOM = 2.0
N_POINTS = 5000
TEMP = 2.8 # Slightly hotter to ensure fluid movement

print(f"[-] Generating Map...")
oracle = generate_oracle_map(RES, ZOOM)
pts, adj = get_wada_graph(N_POINTS, oracle, ZOOM)

print(f"[-] Pre-calculating Interpolation Mesh...")
# We use LinearNDInterpolator to "bake" the triangulation
# This allows us to update the heatmap instantly every frame
grid_x, grid_y = np.mgrid[-ZOOM:ZOOM:600j, -ZOOM:ZOOM:600j]
interpolator = LinearNDInterpolator(pts, np.zeros(N_POINTS)) # Init with zeros

engine = HeatmapEngine(pts, adj, temp=TEMP)

fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.set_facecolor('black')
ax.axis('off')

# Initialize Image with dummy data
# Use 'inferno' for that spicy orange look
# vmin/vmax tuned to highlight the "Hot" spots (-6 is happy, +6 is angry)
im = ax.imshow(np.zeros((600, 600)), origin='lower', extent=[-ZOOM, ZOOM, -ZOOM, ZOOM], 
               cmap='inferno', vmin=-4, vmax=4, interpolation='bilinear')

# Overlay the basins faintly for context
ax.contour(oracle, levels=[0.5, 1.5, 2.5], extent=[-ZOOM, ZOOM, -ZOOM, ZOOM], colors='cyan', linewidths=0.5, alpha=0.3)

title_text = ax.text(0.02, 0.95, "Chaos Heatmap", transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

def animate(i):
    # Run physics
    engine.step(frames=1)
    
    # Get Energy
    energy = engine.get_frustration()
    
    # Interpolate
    interpolator.values[:] = energy # Update values in place if possible, or re-call
    # Actually LinearNDInterpolator holds the triangulation. We need to call it with new values.
    # But SciPy's LinearND doesn't support fast value updates easily.
    # Workaround: Re-instantiate is slow. 
    # FAST PATH: We simply call the interpolator on the grid. 
    # Note: If LinearND is too slow per frame, we fall back to 'nearest' or use a pre-computed weight matrix.
    # Let's try direct call, if slow we'll optimize.
    
    # Re-creating interpolator is actually often faster than one-by-one calls if N is small.
    # Let's use specific call:
    interp_update = LinearNDInterpolator(pts, energy)
    heatmap_data = interp_update(grid_x, grid_y)
    
    im.set_data(heatmap_data.T) # Transpose to match grid mgrid
    
    title_text.set_text(f"Frustration Flow (T={TEMP}) | Frame {i}")
    
    if i % 5 == 0: print(f"Rendering frame {i}...")
    return im, title_text

print(f"[-] Filming Heat Flow...")
anim = animation.FuncAnimation(fig, animate, frames=80, interval=60, blit=False)
anim.save('wada_heat_flow.gif', writer=PillowWriter(fps=15))
print("[+] Heatmap Generated. Saved to 'wada_heat_flow.gif'")