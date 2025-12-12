import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy.interpolate import griddata
from numba import njit, prange
import time

# ==========================================
# 1. THE PRISM SOLVER (The Oracle) - REUSED
# ==========================================

@njit(fastmath=True)
def get_basin_single(m, l, t_max=60.0, dt=0.05, escape_r2=16.0):
    pm, pl = 0.0, 0.0
    steps = int(t_max / dt)
    sigma = 1.0
    for _ in range(steps):
        fm = -(m + 2*sigma*m*l)
        fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm
        pl += 0.5 * dt * fl
        m += dt * pm
        l += dt * pl
        
        fm = -(m + 2*sigma*m*l)
        fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm
        pl += 0.5 * dt * fl
        
        if m*m + l*l > escape_r2:
            angle = np.arctan2(l, m)
            if angle > 0.5 and angle < 2.6: return 1
            elif angle <= -2.6 or angle >= 2.6: return 2
            else: return 3
    return 0

@njit(parallel=True, fastmath=True)
def generate_oracle_map(res, zoom):
    out_map = np.zeros((res, res), dtype=np.int8)
    cx = (res - 1) / 2.0
    cy = (res - 1) / 2.0
    scale = (2.0 * zoom) / res
    deg120 = 2.094395
    deg240 = 4.188790
    
    for y in prange(res):
        for x in range(res):
            px = (x - cx) * scale
            py = (y - cy) * scale
            r = np.sqrt(px*px + py*py)
            theta = np.arctan2(py, px)
            if theta < 0: theta += 2*np.pi
            
            rot = 0
            eff_theta = theta
            if theta >= deg240:
                eff_theta -= deg240
                rot = 2
            elif theta >= deg120:
                eff_theta -= deg120
                rot = 1
                
            eff_px = r * np.cos(eff_theta)
            eff_py = r * np.sin(eff_theta)
            
            basin = get_basin_single(eff_px, eff_py)
            
            if basin != 0:
                basin = (basin - 1 + rot) % 3 + 1
            out_map[y, x] = basin
            
    return out_map

# ==========================================
# 2. GRAPH GENERATION
# ==========================================

def get_wada_graph_from_oracle(n_points, oracle_map, zoom):
    res = oracle_map.shape[0]
    grad_x = np.abs(np.diff(oracle_map, axis=1, append=oracle_map[:, -1:]))
    grad_y = np.abs(np.diff(oracle_map, axis=0, append=oracle_map[-1:, :]))
    boundaries = (grad_x + grad_y) > 0
    
    pdf = np.ones_like(oracle_map, dtype=float) * 0.05
    pdf[boundaries] = 5.0
    pdf /= pdf.sum()
    
    indices = np.arange(pdf.size)
    chosen_indices = np.random.choice(indices, size=n_points, replace=False, p=pdf.flatten())
    py_idx, px_idx = np.unravel_index(chosen_indices, oracle_map.shape)
    
    scale = (2.0 * zoom) / res
    cx, cy = res/2, res/2
    jitter = np.random.uniform(-0.5, 0.5, size=n_points) * scale
    
    pts_x = (px_idx - cx) * scale + jitter
    pts_y = (py_idx - cy) * scale + jitter
    points = np.column_stack((pts_x, pts_y))
    
    tri = Delaunay(points)
    adj_list = [[] for _ in range(n_points)]
    for simplex in tri.simplices:
        for i in range(3):
            u, v = simplex[i], simplex[(i+1)%3]
            adj_list[u].append(v)
            adj_list[v].append(u) # Simple list append, we'll dedup later if needed but Ising is robust
            
    return points, adj_list

# ==========================================
# 3. ISING ACTIVITY MONITOR
# ==========================================

def run_ising_heatmap(adj_list, temp, mc_steps=1000):
    n_spins = len(adj_list)
    spins = np.random.choice([-1, 1], size=n_spins)
    
    # We will track "Flip Count" per node (Volatility)
    flip_counts = np.zeros(n_spins, dtype=int)
    
    # We also track "Local Energy" (Frustration)
    # E_local = -Sum(s_i * s_j)
    # If aligned, E is negative (low). If anti-aligned, E is positive (high).
    avg_local_energy = np.zeros(n_spins, dtype=float)
    
    for step in range(mc_steps):
        indices = np.random.randint(0, n_spins, size=n_spins) # Approx 1 sweep
        
        for idx in indices:
            s = spins[idx]
            h = 0
            for nbr in adj_list[idx]:
                h += spins[nbr]
            
            dE = 2 * s * h # J=1
            
            if dE <= 0 or np.random.rand() < np.exp(-dE / temp):
                spins[idx] *= -1
                flip_counts[idx] += 1
        
        # Sample Energy periodically
        if step > mc_steps // 2 and step % 10 == 0:
            for i in range(n_spins):
                h = 0
                for nbr in adj_list[i]:
                    h += spins[nbr]
                # Local Energy: -0.5 * s * h (0.5 to not double count bonds? 
                # Actually local frustration is just -s*h. 
                # If s=1, h=4 (all aligned), E = -4 (Happy).
                # If s=1, h=-4 (all anti), E = +4 (Frustrated).
                avg_local_energy[i] += (-spins[i] * h)

    avg_local_energy /= (mc_steps / 2 / 10)
    return flip_counts, avg_local_energy

# ==========================================
# 4. EXECUTION
# ==========================================

MAP_RES = 1000
ZOOM = 2.0
N_POINTS = 6000 # Dense graph for good heatmap
TEMP_TARGET = 3.0 # The "Resurrection" Peak from previous plot

print(f"[-] Generating Oracle Map ({MAP_RES}x{MAP_RES})...")
oracle_map = generate_oracle_map(MAP_RES, ZOOM)

print(f"[-] Building Wada Graph (N={N_POINTS})...")
pts, adj, = get_wada_graph_from_oracle(N_POINTS, oracle_map, ZOOM)

print(f"[-] Running Ising Volatility Scan at T={TEMP_TARGET}...")
flips, energy = run_ising_heatmap(adj, TEMP_TARGET, mc_steps=2000)

# ==========================================
# 5. VISUALIZATION
# ==========================================

print(f"[-] Interpolating Heatmap...")
# We grid the "Energy" values back to the image
grid_x, grid_y = np.mgrid[-ZOOM:ZOOM:1000j, -ZOOM:ZOOM:1000j]
# Using 'linear' interpolation for smooth heat
heatmap_energy = griddata(pts, energy, (grid_x, grid_y), method='linear', fill_value=0)

fig, axes = plt.subplots(1, 2, figsize=(16, 8), facecolor='#050505')

# Plot 1: The Structure (Basin Map)
axes[0].imshow(oracle_map, origin='lower', extent=[-ZOOM, ZOOM, -ZOOM, ZOOM], cmap='twilight', alpha=0.8)
axes[0].set_title("The Underlying Structure (Wada Basins)", color='white', fontsize=16)
axes[0].axis('off')

# Plot 2: The Frustration (Heatmap)
# Overlay the heatmap on black
im = axes[1].imshow(heatmap_energy.T, origin='lower', extent=[-ZOOM, ZOOM, -ZOOM, ZOOM], cmap='inferno', vmin=np.percentile(energy, 5), vmax=np.percentile(energy, 95))
axes[1].set_title(f"Frustration Heatmap (T={TEMP_TARGET})", color='white', fontsize=16)
axes[1].axis('off')

# Add subtle contours of the map on the heatmap for context
axes[1].contour(oracle_map, levels=[0.5, 1.5, 2.5], extent=[-ZOOM, ZOOM, -ZOOM, ZOOM], colors='cyan', linewidths=0.3, alpha=0.3)

cb = plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)
cb.set_label('Local Energy (Frustration)', color='white')
cb.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color='white')

plt.suptitle("Thermal Resurrection Analysis: Where is the Energy Hiding?", color='white', fontsize=20)
plt.tight_layout()
plt.savefig('wada_frustration_heatmap.png')
plt.show()