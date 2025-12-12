import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from numba import njit, prange
import time

# ==========================================
# 0. OPTIMIZED NUMBA KERNEL (Must be defined first)
# ==========================================

@njit(parallel=True, fastmath=True)
def integrate_henon_heiles_optimized(m_flat, l_flat, t_max=50.0, dt=0.05, sigma=1.0):
    """
    Optimized integrator using Numba.
    1. Parallel execution across CPU cores.
    2. Lower escape threshold (r > 4.0 is usually sufficient past saddle points).
    3. Compiled machine code loops.
    """
    n = len(m_flat)
    out_m = np.empty(n, dtype=np.float64)
    out_l = np.empty(n, dtype=np.float64)
    
    # Escape threshold: Saddle points are at r=1/sigma. 
    # Once r > 4.0, the particle is ballistically escaping.
    escape_r2 = 16.0  
    steps = int(t_max / dt)

    for i in prange(n):
        m = m_flat[i]
        l = l_flat[i]
        pm = 0.0
        pl = 0.0
        
        active = True
        
        for _ in range(steps):
            # Symplectic Velocity Verlet
            # 1. Half-step momentum
            fm = -(m + 2*sigma*m*l)
            fl = -(l + sigma*(m**2 - l**2))
            
            pm += 0.5 * dt * fm
            pl += 0.5 * dt * fl
            
            # 2. Full-step position
            m += dt * pm
            l += dt * pl
            
            # 3. New Forces
            fm_new = -(m + 2*sigma*m*l)
            fl_new = -(l + sigma*(m**2 - l**2))
            
            # 4. Half-step momentum
            pm += 0.5 * dt * fm_new
            pl += 0.5 * dt * fl_new
            
            # Check escape
            if m*m + l*l > escape_r2:
                active = False
                break
        
        out_m[i] = m
        out_l[i] = l
        
    return out_m, out_l

# ==========================================
# 1. MESH GENERATION (Wada & Regular)
# ==========================================

def integrate_henon_heiles_batch(m_grid, l_grid, t_max=50.0, dt=0.1, sigma=1.0):
    # Flatten inputs for the Numba function
    shape = m_grid.shape
    m_flat = m_grid.flatten()
    l_flat = l_grid.flatten()
    
    # Run optimized kernel
    # Note: First run will include compilation time (~1-2s), subsequent runs are instant
    m_out, l_out = integrate_henon_heiles_optimized(m_flat, l_flat, t_max, dt, sigma)
    
    return m_out.reshape(shape), l_out.reshape(shape)

def get_wada_graph(n_points):
    # 1. Generate Basin Map
    res = 200 # INCREASED RES because Numba is fast now!
    x = np.linspace(-2, 2, res)
    y = np.linspace(-2, 2, res)
    X, Y = np.meshgrid(x, y)
    
    # This calls the optimized batch integrator
    m_final, l_final = integrate_henon_heiles_batch(X, Y)
    
    angle = np.arctan2(l_final, m_final)
    basins = np.zeros_like(angle, dtype=int)
    mask_teal = (angle > np.pi/3) & (angle < np.pi)
    mask_gold = (angle > -np.pi/3) & (angle < np.pi/3)
    basins[mask_teal] = 1
    basins[mask_gold] = 3
    basins[~mask_teal & ~mask_gold] = 2
    
    # 2. PDF (Boundary Detection)
    grad_x = np.abs(np.diff(basins, axis=1, append=basins[:, -1:]))
    grad_y = np.abs(np.diff(basins, axis=0, append=basins[-1:, :]))
    boundaries = (grad_x + grad_y) > 0
    
    pdf = np.ones_like(basins, dtype=float) * 0.1
    pdf[boundaries] = 5.0
    pdf /= pdf.sum()
    
    # 3. Sample Points
    indices = np.arange(pdf.size)
    chosen = np.random.choice(indices, size=n_points, replace=False, p=pdf.flatten())
    py, px = np.unravel_index(chosen, pdf.shape)
    
    # Map to -2, 2
    dx = 4.0 / res
    pts_x = -2 + px * dx + np.random.uniform(-dx/2, dx/2, n_points)
    pts_y = -2 + py * dx + np.random.uniform(-dx/2, dx/2, n_points)
    points = np.column_stack((pts_x, pts_y))
    
    # 4. Triangulate
    tri = Delaunay(points)
    
    # 5. Adjacency
    adj = {i: set() for i in range(n_points)}
    for simplex in tri.simplices:
        for i in range(3):
            u, v = simplex[i], simplex[(i+1)%3]
            adj[u].add(v)
            adj[v].add(u)
    
    return points, [list(adj[i]) for i in range(n_points)]

def get_regular_graph(n_points):
    # Closest square
    side = int(np.sqrt(n_points))
    real_n = side * side
    
    x = np.linspace(-2, 2, side)
    y = np.linspace(-2, 2, side)
    X, Y = np.meshgrid(x, y)
    points = np.column_stack((X.flatten(), Y.flatten()))
    
    adj_list = [[] for _ in range(real_n)]
    
    for i in range(side):
        for j in range(side):
            idx = i * side + j
            if i > 0: adj_list[idx].append((i-1)*side + j)
            if i < side-1: adj_list[idx].append((i+1)*side + j)
            if j > 0: adj_list[idx].append(i*side + j - 1)
            if j < side-1: adj_list[idx].append(i*side + j + 1)
            
    return points, adj_list

# ==========================================
# 2. ISING SOLVER (Metropolis)
# ==========================================

def run_ising_simulation(adj_list, temps, mc_steps=1000, burn_in=200):
    n_spins = len(adj_list)
    magnetizations = []
    susceptibilities = []
    
    for T in temps:
        spins = np.random.choice([-1, 1], size=n_spins)
        M_accum = 0.0
        M2_accum = 0.0
        count = 0
        
        for step in range(mc_steps + burn_in):
            # DEMO SPEEDUP: Fewer flips per step
            for _ in range(n_spins // 2): 
                idx = np.random.randint(0, n_spins)
                s = spins[idx]
                neighbor_sum = sum(spins[n] for n in adj_list[idx])
                dE = 2 * s * neighbor_sum 
                
                if dE < 0 or np.random.rand() < np.exp(-dE / T):
                    spins[idx] *= -1
            
            if step >= burn_in:
                M = np.abs(np.sum(spins))
                M_accum += M
                M2_accum += M**2
                count += 1
        
        avg_M = M_accum / count
        avg_M2 = M2_accum / count
        chi = (avg_M2 - avg_M**2) / T
        
        magnetizations.append(avg_M / n_spins)
        susceptibilities.append(chi / n_spins)
        
    return np.array(magnetizations), np.array(susceptibilities)

# ==========================================
# 3. THE RACE
# ==========================================

# Setup
N_POINTS = 4000 
TEMPS = np.linspace(1.5, 3.5, 10)
STEPS = 500 

# ERROR FIXED HERE: calling get_wada_graph instead of the integrator
print(f"Generating Wada Graph (N={N_POINTS})...")
t0 = time.time()
pts_wada, adj_wada = get_wada_graph(N_POINTS)
print(f"Wada Graph Generation done in {time.time()-t0:.2f}s")

print(f"Generating Regular Graph (N~{N_POINTS})...")
pts_reg, adj_reg = get_regular_graph(N_POINTS)
real_n_reg = len(adj_reg)

print(f"Running Wada Simulation...")
t0 = time.time()
mag_wada, chi_wada = run_ising_simulation(adj_wada, TEMPS, mc_steps=STEPS)
print(f"Wada Simulation done in {time.time()-t0:.2f}s")

print(f"Running Regular Simulation...")
t0 = time.time()
mag_reg, chi_reg = run_ising_simulation(adj_reg, TEMPS, mc_steps=STEPS)
print(f"Regular Simulation done in {time.time()-t0:.2f}s")

# Plot
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.title("Magnetization vs Temperature")
plt.plot(TEMPS, mag_wada, 'o-', label=f'Wada (N={N_POINTS})', color='red')
plt.plot(TEMPS, mag_reg, 's--', label=f'Regular (N={real_n_reg})', color='blue')
plt.xlabel("Temperature (T)")
plt.ylabel("|M| / N")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.title("Susceptibility vs Temperature")
plt.plot(TEMPS, chi_wada, 'o-', label='Wada', color='red')
plt.plot(TEMPS, chi_reg, 's--', label='Regular', color='blue')
plt.xlabel("Temperature (T)")
plt.ylabel("Chi / N")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('ising_race_results.png')
print("Race complete.")