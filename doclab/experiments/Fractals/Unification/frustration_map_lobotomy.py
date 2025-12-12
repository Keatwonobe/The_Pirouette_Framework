import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from numba import njit, prange
import time

# ==========================================
# THE LOBOTOMY KERNEL
# ==========================================

def perform_lobotomy(points, adj_list, oracle_map, zoom, cut_threshold=0.1):
    """
    Removes nodes that sit on the fractal boundaries.
    """
    res = oracle_map.shape[0]
    scale = (2.0 * zoom) / res
    cx, cy = res/2, res/2
    
    # 1. Identify "Bad" Nodes (Boundary Dwellers)
    # We map points back to the Oracle to check if they are near an edge
    valid_indices = []
    
    # Simple edge detection on map
    grad_x = np.abs(np.diff(oracle_map, axis=1, append=oracle_map[:, -1:]))
    grad_y = np.abs(np.diff(oracle_map, axis=0, append=oracle_map[-1:, :]))
    edges = (grad_x + grad_y) > 0
    
    kept_count = 0
    
    # Map from Old Index -> New Index
    remap = {}
    
    for i, pt in enumerate(points):
        # Convert physical x,y back to map row,col
        px_idx = int((pt[0] / scale) + cx)
        py_idx = int((pt[1] / scale) + cy)
        
        # Clamp
        px_idx = np.clip(px_idx, 0, res-1)
        py_idx = np.clip(py_idx, 0, res-1)
        
        # Check if this pixel is an edge (or neighbor is edge)
        # We look at a 3x3 window around the point
        is_fractal = False
        w = 2
        r_min, r_max = max(0, py_idx-w), min(res, py_idx+w)
        c_min, c_max = max(0, px_idx-w), min(res, px_idx+w)
        
        if np.any(edges[r_min:r_max, c_min:c_max]):
            is_fractal = True
            
        if not is_fractal:
            remap[i] = kept_count
            valid_indices.append(i)
            kept_count += 1
            
    # 2. Rebuild Graph
    new_points = points[valid_indices]
    new_adj = [[] for _ in range(kept_count)]
    
    for old_u in valid_indices:
        new_u = remap[old_u]
        for old_v in adj_list[old_u]:
            if old_v in remap: # Only keep connection if both survived
                new_v = remap[old_v]
                new_adj[new_u].append(new_v)
                
    return new_points, new_adj

# ==========================================
# 1. THE PRISM SOLVER (The Oracle)
# ==========================================
# This precomputes the "Truth Map" efficiently

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
    # Generates the Master Lookup Table
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
            
            # Symmetry Folding
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
            
            # Solve
            basin = get_basin_single(eff_px, eff_py)
            
            # Unfold
            if basin != 0:
                basin = (basin - 1 + rot) % 3 + 1
            out_map[y, x] = basin
            
    return out_map

# ==========================================
# 2. THE LOOKUP MECHANISM
# ==========================================

def get_wada_graph_from_oracle(n_points, oracle_map, zoom):
    """
    Generates a graph using the Oracle Map as a lookup table.
    No integration happens here. It is instant.
    """
    res = oracle_map.shape[0]
    
    # 1. Create Probability Density Function (PDF) based on Boundaries
    # We find edges by looking for pixel differences
    # Simple gradient approximation
    grad_x = np.abs(np.diff(oracle_map, axis=1, append=oracle_map[:, -1:]))
    grad_y = np.abs(np.diff(oracle_map, axis=0, append=oracle_map[-1:, :]))
    boundaries = (grad_x + grad_y) > 0
    
    # PDF: High prob on boundaries, low in bulk
    pdf = np.ones_like(oracle_map, dtype=float) * 0.05
    pdf[boundaries] = 5.0
    pdf /= pdf.sum()
    
    # 2. Sample Points from the PDF
    indices = np.arange(pdf.size)
    chosen_indices = np.random.choice(indices, size=n_points, replace=False, p=pdf.flatten())
    py_idx, px_idx = np.unravel_index(chosen_indices, oracle_map.shape)
    
    # 3. Convert Index to Coordinate (Physical Space)
    # Map index [0, res] to [-zoom, zoom]
    scale = (2.0 * zoom) / res
    cx, cy = res/2, res/2
    
    # Jitter the points slightly to avoid grid-lock artifacts
    jitter = np.random.uniform(-0.5, 0.5, size=n_points) * scale
    
    pts_x = (px_idx - cx) * scale + jitter
    pts_y = (py_idx - cy) * scale + jitter
    points = np.column_stack((pts_x, pts_y))
    
    # 4. LOOKUP BASIN (The Instant Solve)
    # Since we picked these points FROM the map, we already know where they are.
    # But for robustness (due to jitter), we can just peek at the map index again.
    basin_ids = oracle_map[py_idx, px_idx]
    
    # 5. Triangulate
    tri = Delaunay(points)
    
    # 6. Build Adjacency
    adj_list = [set() for _ in range(n_points)]
    for simplex in tri.simplices:
        for i in range(3):
            u, v = simplex[i], simplex[(i+1)%3]
            # Standard graph connection
            adj_list[u].add(v)
            adj_list[v].add(u)
            
    # Convert sets to lists
    adj_final = [list(s) for s in adj_list]
    
    return points, adj_final, basin_ids

def get_regular_graph(n_points, zoom):
    side = int(np.sqrt(n_points))
    x = np.linspace(-zoom, zoom, side)
    y = np.linspace(-zoom, zoom, side)
    X, Y = np.meshgrid(x, y)
    points = np.column_stack((X.flatten(), Y.flatten()))
    
    adj_list = [[] for _ in range(len(points))]
    for i in range(side):
        for j in range(side):
            idx = i * side + j
            if i > 0: adj_list[idx].append((i-1)*side + j)
            if i < side-1: adj_list[idx].append((i+1)*side + j)
            if j > 0: adj_list[idx].append(i*side + j - 1)
            if j < side-1: adj_list[idx].append(i*side + j + 1)
            
    return points, adj_list

# ==========================================
# 3. ISING SIMULATION (Optimized Python)
# ==========================================

def run_ising_fast(adj_list, temps, mc_steps=800):
    n_spins = len(adj_list)
    magnetizations = []
    
    # Pre-convert adj_list to jagged array for faster access? 
    # For now, list of lists is fine for N=4000.
    
    for T in temps:
        spins = np.random.choice([-1, 1], size=n_spins)
        M_accum = 0.0
        
        for step in range(mc_steps):
            # Monte Carlo Sweep (Approximate)
            # Pick random nodes
            indices = np.random.randint(0, n_spins, size=n_spins)
            
            for idx in indices:
                s = spins[idx]
                # Sum neighbors
                h = 0
                for nbr in adj_list[idx]:
                    h += spins[nbr]
                
                dE = 2 * s * h
                
                if dE <= 0 or np.random.rand() < np.exp(-dE / T):
                    spins[idx] *= -1
            
            if step > mc_steps // 2:
                M_accum += np.abs(np.sum(spins))
                
        magnetizations.append(M_accum / (mc_steps/2 * n_spins))
        
    return np.array(magnetizations)

# ==========================================
# EXECUTION
# ==========================================

MAP_RES = 1000
ZOOM = 2.0
N_POINTS = 5000 

print(f"[-] Generating Oracle...")
oracle_map = generate_oracle_map(MAP_RES, ZOOM)

print(f"[-] Building Full Wada Graph...")
pts_full, adj_full, _ = get_wada_graph_from_oracle(N_POINTS, oracle_map, ZOOM)

print(f"[-] Performing Lobotomy (Removing Fractal Skeleton)...")
pts_cut, adj_cut = perform_lobotomy(pts_full, adj_full, oracle_map, ZOOM)
print(f"    Nodes Reduced: {len(pts_full)} -> {len(pts_cut)}")

print(f"[-] Running Ising Race (Full vs Lobotomized)...")
TEMPS = np.linspace(1.0, 4.0, 15)

# Run Full
mag_full = run_ising_fast(adj_full, TEMPS) # Re-use previous function
# Run Cut
mag_cut = run_ising_fast(adj_cut, TEMPS)

# Plot
plt.figure(figsize=(10, 6), facecolor='#111111')
plt.plot(TEMPS, mag_full, 'o-', color='#00ffff', label='Full Wada (With Skeleton)')
plt.plot(TEMPS, mag_cut, 'x--', color='#ffff00', label='Lobotomized (Basins Only)')
plt.title("The Lobotomy Test: Removing the Chaos", color='white')
plt.xlabel("Temperature", color='white')
plt.ylabel("Magnetization", color='white')
plt.legend()
plt.grid(color='#333333')
plt.tick_params(colors='white')
plt.savefig('wada_lobotomy_test.png')
plt.show()