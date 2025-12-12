import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

# ==========================================
# 1. BASIN PHYSICS (Henon-Heiles)
# ==========================================
def integrate_henon_heiles_batch(m_grid, l_grid, t_max=100.0, dt=0.05, sigma=1.0):
    """
    Integrates the system for a grid of initial conditions.
    Returns final positions to determine basin escape.
    """
    shape = m_grid.shape
    m = m_grid.flatten()
    l = l_grid.flatten()
    pm = np.zeros_like(m)
    pl = np.zeros_like(l)
    
    # Track active particles (r < escape_radius)
    active = np.ones_like(m, dtype=bool)
    escape_radius = 20.0
    steps = int(t_max / dt)
    
    for _ in range(steps):
        if not np.any(active): break
        
        # Vectorized Leapfrog Integration
        m_act, l_act = m[active], l[active]
        pm_act, pl_act = pm[active], pl[active]
        
        # Forces: dV/dm, dV/dl
        fm = -(m_act + 2*sigma*m_act*l_act)
        fl = -(l_act + sigma*(m_act**2 - l_act**2))
        
        pm_half = pm_act + 0.5 * dt * fm
        pl_half = pl_act + 0.5 * dt * fl
        
        m_next = m_act + dt * pm_half
        l_next = l_act + dt * pl_half
        
        fm_next = -(m_next + 2*sigma*m_next*l_next)
        fl_next = -(l_next + sigma*(m_next**2 - l_next**2))
        
        pm_next = pm_half + 0.5 * dt * fm_next
        pl_next = pl_half + 0.5 * dt * fl_next
        
        m[active], l[active] = m_next, l_next
        pm[active], pl[active] = pm_next, pl_next
        
        # Check for escape
        r2 = m[active]**2 + l[active]**2
        escaped_now = r2 > escape_radius**2
        
        # Update active mask (only deactivate newly escaped)
        active_indices = np.where(active)[0]
        active[active_indices[escaped_now]] = False
            
    return m.reshape(shape), l.reshape(shape)

def get_basin_map(resolution=200, x_lim=(-2, 2), y_lim=(-2, 2)):
    """Generates the Red/Gold/Teal basin map."""
    x = np.linspace(x_lim[0], x_lim[1], resolution)
    y = np.linspace(y_lim[0], y_lim[1], resolution)
    X, Y = np.meshgrid(x, y)
    
    m_final, l_final = integrate_henon_heiles_batch(X, Y)
    
    r = np.sqrt(m_final**2 + l_final**2)
    angle = np.arctan2(l_final, m_final)
    
    basins = np.zeros_like(r, dtype=int)
    
    # Classification Logic (Appendix A.1)
    mask_trapped = r < 10.0
    mask_teal = (angle > np.pi/3) & (angle < np.pi)
    mask_gold = (angle > -np.pi/3) & (angle < np.pi/3)
    
    basins[mask_teal] = 1 # Teal
    basins[mask_gold] = 3 # Gold
    basins[~mask_teal & ~mask_gold] = 2 # Red
    basins[mask_trapped] = 0 # Stability Island
    
    return X, Y, basins

# ==========================================
# 2. MESH GENERATION (The "Mesher")
# ==========================================
def generate_fractal_mesh(resolution=300, n_points=2000):
    print("Scanning basins...")
    X, Y, basins = get_basin_map(resolution=resolution)
    
    print("Calculating gradients...")
    # Find edges using simple gradient
    grad_x = np.abs(np.diff(basins, axis=1, append=basins[:, -1:]))
    grad_y = np.abs(np.diff(basins, axis=0, append=basins[-1:, :]))
    boundaries = (grad_x + grad_y) > 0
    
    # Create Probability Density Function (PDF) for node placement
    pdf = np.ones_like(basins, dtype=float) * 0.05 # Low background density
    pdf[boundaries] = 5.0                          # High boundary density
    pdf[basins == 0] = 1.0                         # Medium density in island
    pdf /= pdf.sum()
    
    print(f"Sampling {n_points} nodes...")
    indices = np.arange(pdf.size)
    chosen_indices = np.random.choice(indices, size=n_points, replace=False, p=pdf.flatten())
    
    py, px = np.unravel_index(chosen_indices, pdf.shape)
    
    # Add jitter to avoid grid artifacts
    x_min, x_max = X.min(), X.max()
    y_min, y_max = Y.min(), Y.max()
    dx = (x_max - x_min) / resolution
    dy = (y_max - y_min) / resolution
    
    points_x = X[py, px] + np.random.uniform(-dx/2, dx/2, size=n_points)
    points_y = Y[py, px] + np.random.uniform(-dy/2, dy/2, size=n_points)
    points = np.column_stack((points_x, points_y))
    
    print("Triangulating...")
    tri = Delaunay(points)
    
    return points, tri

# ==========================================
# 3. EXPORT HELPERS
# ==========================================
def get_adjacency_list(tri):
    """Converts Delaunay triangulation to adjacency list for Physics Solver"""
    indptr, indices = tri.vertex_neighbor_vertices
    adjacency = {}
    for i in range(len(tri.points)):
        neighbors = indices[indptr[i]:indptr[i+1]]
        adjacency[i] = neighbors.tolist()
    return adjacency

if __name__ == "__main__":
    # Generate Mesh
    points, tri = generate_fractal_mesh(resolution=400, n_points=2500)
    
    # Get Graph for Physics
    graph = get_adjacency_list(tri)
    print(f"Graph generated: {len(graph)} nodes")
    print(f"Node 0 is connected to: {graph[0]}")
    
    # Visualize
    plt.figure(figsize=(10, 10))
    plt.triplot(points[:,0], points[:,1], tri.simplices, color='black', lw=0.5)
    plt.plot(points[:,0], points[:,1], 'o', markersize=2, color='red')
    plt.title("Wada Fractal Mesh")
    plt.show()