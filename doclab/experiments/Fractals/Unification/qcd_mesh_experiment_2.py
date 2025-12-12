import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import time

# ==========================================
# 1. MESH GENERATION (Wada & Regular)
# ==========================================

def integrate_henon_heiles_batch(m_grid, l_grid, t_max=50.0, dt=0.1, sigma=1.0):
    # Simplified integrator for speed in demo
    shape = m_grid.shape
    m = m_grid.flatten()
    l = l_grid.flatten()
    pm = np.zeros_like(m)
    pl = np.zeros_like(l)
    
    active = np.ones_like(m, dtype=bool)
    steps = int(t_max / dt)
    
    # We'll just do a few steps to get the "shape" roughly right for the demo
    # In a real run, use t_max=100, dt=0.05
    for _ in range(steps):
        if not np.any(active): break
        
        m_act, l_act = m[active], l[active]
        pm_act, pl_act = pm[active], pl[active]
        
        fm = -(m_act + 2*sigma*m_act*l_act)
        fl = -(l_act + sigma*(m_act**2 - l_act**2))
        
        m_next = m_act + dt * pm_act + 0.5 * dt**2 * fm
        l_next = l_act + dt * pl_act + 0.5 * dt**2 * fl
        
        # approximate new momentum
        fm_next = -(m_next + 2*sigma*m_next*l_next)
        fl_next = -(l_next + sigma*(m_next**2 - l_next**2))
        
        pm_next = pm_act + 0.5 * dt * (fm + fm_next)
        pl_next = pl_act + 0.5 * dt * (fl + fl_next)
        
        m[active], l[active] = m_next, l_next
        pm[active], pl[active] = pm_next, pl_next
        
        r2 = m[active]**2 + l[active]**2
        escaped_now = r2 > 100.0
        
        active_indices = np.where(active)[0]
        active[active_indices[escaped_now]] = False
            
    return m.reshape(shape), l.reshape(shape)

def get_wada_graph(n_points):
    # 1. Generate Basin Map (Low res for speed)
    res = 50
    x = np.linspace(-2, 2, res)
    y = np.linspace(-2, 2, res)
    X, Y = np.meshgrid(x, y)
    
    m_final, l_final = integrate_henon_heiles_batch(X, Y)
    
    angle = np.arctan2(l_final, m_final)
    basins = np.zeros_like(angle, dtype=int)
    mask_teal = (angle > np.pi/3) & (angle < np.pi)
    mask_gold = (angle > -np.pi/3) & (angle < np.pi/3)
    basins[mask_teal] = 1
    basins[mask_gold] = 3
    basins[~mask_teal & ~mask_gold] = 2
    
    # 2. PDF
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
    
    # Convert set to list
    adj_list = [list(adj[i]) for i in range(n_points)]
    return points, adj_list

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
            # Neighbors: up, down, left, right (Periodic BC usually, but let's do open to match Delaunay implicitly or closed?)
            # Delaunay is open boundary usually (convex hull). Let's stick to open for fairness or periodic?
            # Standard Ising is periodic. Wada Delaunay is open at edges.
            # Let's do Open for both to be structurally fair, or Periodic for Regular (standard) vs Open Wada.
            # Comparing "Standard Lattice QCD" (Periodic) vs "Wada" (likely Open/Dirichlet at boundary).
            # Let's use Open Grid for strict 1-to-1 comparison of "internal" connectivity.
            
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
    
    # Pre-compute neighbor indices for speed (list of arrays)
    # Actually, Python loops are slow. We'll do a simplified "random node update" loop.
    
    for T in temps:
        # Initialize Random Spins
        spins = np.random.choice([-1, 1], size=n_spins)
        
        M_accum = 0.0
        M2_accum = 0.0
        count = 0
        
        # Run MC Steps
        # One "Step" = N flip attempts (1 Monte Carlo Sweep)
        for step in range(mc_steps + burn_in):
            # Pick N random sites (vectorized-ish or just loop)
            # For pure python speed, we'll iterate N times per step
            # This is slow in Python. We will reduce N and steps for the demo.
            
            # FAST APPROXIMATION for DEMO:
            # Just do n_spins // 10 flips per 'step' to save time
            for _ in range(n_spins): 
                idx = np.random.randint(0, n_spins)
                s = spins[idx]
                
                # Calculate energy change
                # dE = 2 * s * sum(neighbors)
                neighbor_sum = sum(spins[n] for n in adj_list[idx])
                dE = 2 * s * neighbor_sum # J=1
                
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
        
        magnetizations.append(avg_M / n_spins) # Normalize per spin
        susceptibilities.append(chi / n_spins)
        
    return np.array(magnetizations), np.array(susceptibilities)

# ==========================================
# 3. THE RACE
# ==========================================

# Setup
N_POINTS = 400 # Small for speed
TEMPS = np.linspace(1.5, 3.5, 10) # Range covering Tc ~ 2.27
STEPS = 500 # Short run

print(f"Generating Wada Graph (N={N_POINTS})...")
pts_wada, adj_wada = get_wada_graph(N_POINTS)

print(f"Generating Regular Graph (N~{N_POINTS})...")
pts_reg, adj_reg = get_regular_graph(N_POINTS)
real_n_reg = len(adj_reg)

print(f"Running Wada Simulation...")
t0 = time.time()
mag_wada, chi_wada = run_ising_simulation(adj_wada, TEMPS, mc_steps=STEPS)
print(f"Wada done in {time.time()-t0:.2f}s")

print(f"Running Regular Simulation...")
t0 = time.time()
mag_reg, chi_reg = run_ising_simulation(adj_reg, TEMPS, mc_steps=STEPS)
print(f"Regular done in {time.time()-t0:.2f}s")

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