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
        # Symplectic Euler (modified velocity Verlet) for the complex map
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
    # Boundary detection
    grad_x = np.abs(np.diff(oracle_map, axis=1, append=oracle_map[:, -1:]))
    grad_y = np.abs(np.diff(oracle_map, axis=0, append=oracle_map[-1:, :]))
    boundaries = (grad_x + grad_y) > 0
    # Create PDF biased towards boundaries
    pdf = np.ones_like(oracle_map, dtype=float) * 0.05
    pdf[boundaries] = 6.0 # Focus on the fractal edges
    pdf /= pdf.sum()
    
    # Sample points
    indices = np.arange(pdf.size)
    # Using 'replace=False' ensures unique points
    chosen = np.random.choice(indices, size=n_points, replace=False, p=pdf.flatten())
    py, px = np.unravel_index(chosen, oracle_map.shape)
    
    # Convert pixel coords to simulation coords
    scale = (2.0 * zoom) / res; cx, cy = res/2, res/2
    # Add minor noise to avoid collinearity/aliasing issues
    pts_x = (px - cx) * scale + np.random.uniform(-0.5, 0.5, n_points)*scale*0.1
    pts_y = (py - cy) * scale + np.random.uniform(-0.5, 0.5, n_points)*scale*0.1
    points = np.column_stack((pts_x, pts_y))
    
    # Delaunay triangulation and adjacency list for the Ising model
    tri = Delaunay(points)
    adj = [[] for _ in range(n_points)]
    for simplex in tri.simplices:
        for i in range(3):
            u, v = simplex[i], simplex[(i+1)%3]
            adj[u].append(v); adj[v].append(u)
            
    # Remove duplicates from adjacency lists (triangulation can produce duplicates)
    for i in range(n_points):
        adj[i] = list(set(adj[i]))
        
    return points, adj, tri

# ==========================================
# 2. THE THERMODYNAMIC SIMULATOR
# ==========================================

class HeatmapEngine:
    def __init__(self, points, adj_list, temp=2.6):
        self.points = points
        self.adj = adj_list
        self.n = len(points)
        self.temp = temp
        # Initial state: random spins
        self.spins = np.random.choice([-1, 1], size=self.n)
        
    def step(self, frames=1):
        """Metropolis Monte Carlo step for the Ising Model."""
        for _ in range(frames):
            # Select N random sites to flip (one full sweep)
            indices = np.random.randint(0, self.n, size=self.n)
            for idx in indices:
                s = self.spins[idx]
                # Calculate local magnetic field (sum of neighbor spins)
                h = sum(self.spins[n] for n in self.adj[idx])
                # Energy difference if spin is flipped
                dE = 2 * s * h
                
                # Metropolis criteria: Accept flip if dE <= 0 or with Boltzmann probability
                if dE <= 0 or np.random.rand() < np.exp(-dE / self.temp):
                    self.spins[idx] *= -1

    def get_frustration(self):
        """Calculate Local Frustration (Energy) for visualization."""
        # E_i = -s_i * H_i, where H_i is the local magnetic field
        # High E_i (positive) = High Frustration (spin is opposite to most neighbors)
        # Low E_i (negative) = Low Frustration (spin is aligned with most neighbors)
        energies = np.zeros(self.n)
        for i in range(self.n):
            h = sum(self.spins[n] for n in self.adj[i])
            energies[i] = -1 * self.spins[i] * h
        return energies

# ==========================================
# 3. INTERPOLATION OPTIMIZATION
# ==========================================

def precalculate_interpolation_weights(tri, grid_x, grid_y):
    """
    Pre-calculates all necessary data for fast linear interpolation on a fixed grid.
    
    Returns:
        indices (array): Indices of the three vertices for each grid point.
        weights (array): Barycentric coordinates (weights) for each grid point.
        valid_mask (array): Boolean mask indicating which grid points are inside the hull.
    """
    # Create the grid points array
    grid_points = np.column_stack((grid_x.flatten(), grid_y.flatten()))
    
    # Find the simplex (triangle) each grid point falls into
    simplex_indices = tri.find_simplex(grid_points)
    
    # Mask for points outside the convex hull (-1 index)
    valid_mask = simplex_indices != -1
    valid_indices = np.where(valid_mask)[0]
    
    # Get the vertex indices (p0, p1, p2) for the valid points
    vertex_indices = tri.simplices[simplex_indices[valid_mask]]
    
    # Get the vertices' coordinates
    points_p0 = tri.points[vertex_indices[:, 0]]
    points_p1 = tri.points[vertex_indices[:, 1]]
    points_p2 = tri.points[vertex_indices[:, 2]]
    
    # Calculate Barycentric Coordinates (weights)
    P = grid_points[valid_mask]
    
    # Helper for 2D area calculation (cross product determinant)
    def area_det(p1, p2, p3):
        return (p2[:, 0] - p1[:, 0]) * (p3[:, 1] - p1[:, 1]) - (p3[:, 0] - p1[:, 0]) * (p2[:, 1] - p1[:, 1])

    # Total area (twice the area of the triangle P0P1P2)
    Area = area_det(points_p0, points_p1, points_p2)

    # Weights (lambda_0, lambda_1, lambda_2)
    w0 = area_det(P, points_p1, points_p2) / Area
    w1 = area_det(P, points_p2, points_p0) / Area
    w2 = area_det(P, points_p0, points_p1) / Area

    # Store all weights and indices in a dense structure to match grid size
    all_weights = np.zeros((grid_points.shape[0], 3))
    all_weights[valid_mask] = np.column_stack((w0, w1, w2))
    
    all_indices = np.zeros((grid_points.shape[0], 3), dtype=int)
    all_indices[valid_mask] = vertex_indices
    
    # The interpolation should only happen for valid points.
    # We return the data needed for the fast update.
    return all_indices, all_weights, valid_mask, grid_x.shape

def fast_interp_update(point_values, indices, weights, valid_mask, output_shape):
    """
    Performs fast linear interpolation using pre-calculated weights and indices.
    """
    # Select the data only for the valid points
    valid_indices = indices[valid_mask]
    valid_weights = weights[valid_mask]
    
    # Get the spin/energy values for the corresponding vertices
    v0 = point_values[valid_indices[:, 0]]
    v1 = point_values[valid_indices[:, 1]]
    v2 = point_values[valid_indices[:, 2]]
    
    # Linear interpolation: V = w0*v0 + w1*v1 + w2*v2
    interpolated_values = (valid_weights[:, 0] * v0 + 
                           valid_weights[:, 1] * v1 + 
                           valid_weights[:, 2] * v2)
    
    # Reconstruct the full grid, filling invalid points (outside hull) with NaN
    full_grid_flat = np.full(indices.shape[0], np.nan)
    full_grid_flat[valid_mask] = interpolated_values
    
    # Reshape to the final 2D image
    return full_grid_flat.reshape(output_shape)


# ==========================================
# 4. ANIMATION SETUP
# ==========================================

RES = 1200 # Slightly lower res for smooth animation FPS
ZOOM = 24000000000000
N_POINTS = 25000
TEMP = 2.8 # Slightly hotter to ensure fluid movement
FRAMES = 80 # Number of frames to render

print(f"[-] Generating Map...")
oracle = generate_oracle_map(RES, ZOOM)
pts, adj, tri = get_wada_graph(N_POINTS, oracle, ZOOM)

print(f"[-] Pre-calculating Interpolation Weights (One-time cost)...")
# Define the interpolation grid
grid_x, grid_y = np.mgrid[-ZOOM:ZOOM:600j, -ZOOM:ZOOM:600j]

# Pre-calculate the required data for fast interpolation
indices, weights, valid_mask, output_shape = precalculate_interpolation_weights(tri, grid_x, grid_y)

# Initialize the physics engine
engine = HeatmapEngine(pts, adj, temp=TEMP)


# Setup Plot
fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.set_facecolor('black')
ax.axis('off')

# Initialize Image with dummy data
# vmin/vmax tuned to highlight the "Hot" spots (-4 is happy, +4 is angry)
im = ax.imshow(np.zeros((600, 600)), origin='lower', extent=[-ZOOM, ZOOM, -ZOOM, ZOOM], 
               cmap='inferno', vmin=-4, vmax=4, interpolation='bilinear')

# Overlay the basins faintly for context
ax.contour(oracle, levels=[0.5, 1.5, 2.5], extent=[-ZOOM, ZOOM, -ZOOM, ZOOM], colors='cyan', linewidths=0.5, alpha=0.3)

title_text = ax.text(0.02, 0.95, "Chaos Heatmap", transform=ax.transAxes, color='white', fontsize=14, fontfamily='monospace')

def animate(i):
    """
    The main animation loop. Runs the physics and updates the heatmap quickly.
    """
    # Run physics
    # Running 2 steps per frame helps the system evolve faster
    engine.step(frames=2) 
    
    # Get Energy (This is fast)
    energy = engine.get_frustration()
    
    # FAST Interpolation (This is the crucial speedup)
    heatmap_data = fast_interp_update(energy, indices, weights, valid_mask, output_shape)
    
    # Update the image data. Transpose is needed because mgrid is X,Y and imshow expects Y,X
    im.set_data(heatmap_data.T) 
    
    # Update title
    title_text.set_text(f"Frustration Flow (T={TEMP:.1f}) | Frame {i+1}/{FRAMES}")
    
    if (i+1) % 10 == 0: 
        print(f"Rendering frame {i+1}...")
        
    return im, title_text # Return the objects that were modified for blitting (even with blit=False)

print(f"[-] Filming Heat Flow... ({FRAMES} frames)")
# Set blit=False for safety since we are modifying text and contour is static
anim = animation.FuncAnimation(fig, animate, frames=FRAMES, interval=60, blit=False)
anim.save('wada_heat_flow.gif', writer=PillowWriter(fps=15))
print(f"[+] Heatmap Generated. Saved to 'wada_heat_flow.gif' ({FRAMES} frames @ 15 FPS)")

# Ensure the plot is closed after saving to prevent memory leaks in some environments
plt.close(fig)