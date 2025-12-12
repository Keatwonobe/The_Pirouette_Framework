import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import Delaunay
from numba import njit, prange

# ==========================================
# 1. THE PHYSICS KERNEL
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

# ==========================================
# 2. THE SCANNER
# ==========================================

def extract_skeleton_layer(zoom, res=400, n_points=4000):
    # 1. Generate Map
    oracle = generate_oracle_map(res, zoom)
    
    # 2. Detect Boundaries (The Skeleton)
    grad_x = np.abs(np.diff(oracle, axis=1, append=oracle[:, -1:]))
    grad_y = np.abs(np.diff(oracle, axis=0, append=oracle[-1:, :]))
    boundaries = (grad_x + grad_y) > 0
    
    # 3. Extract Coordinates of the "Hot" pixels
    # We don't even need the Ising model here; we know the boundaries ARE the frustration.
    # This saves massive compute time for the 3D stack.
    y_idxs, x_idxs = np.where(boundaries)
    
    # Downsample if too dense
    if len(x_idxs) > n_points:
        choice = np.random.choice(len(x_idxs), n_points, replace=False)
        x_idxs = x_idxs[choice]
        y_idxs = y_idxs[choice]
        
    # Convert to physical coords
    scale = (2.0 * zoom) / res
    cx, cy = res/2, res/2
    
    phys_x = (x_idxs - cx) * scale
    phys_y = (y_idxs - cy) * scale
    
    return phys_x, phys_y

# ==========================================
# 3. BUILD THE CHUNK
# ==========================================

LAYERS = 600
ZOOM_START = 0.1
ZOOM_END = 300.0
POINTS_PER_LAYER = 3000

print(f"[-] Initializing Tomographic Scan ({LAYERS} layers)...")

all_x = []
all_y = []
all_z = [] # This will be log(zoom)

# Logarithmic spacing for zoom
zooms = np.logspace(np.log10(ZOOM_START), np.log10(ZOOM_END), LAYERS)

for i, z_level in enumerate(zooms):
    if i % 10 == 0: print(f"    Scanning Layer {i}/{LAYERS} (Zoom={z_level:.2f})...")
    
    # Extract the chaos skeleton
    xs, ys = extract_skeleton_layer(z_level, res=500, n_points=POINTS_PER_LAYER)
    
    # Store
    all_x.append(xs)
    all_y.append(ys)
    # We use -log(zoom) as the Z-axis so "Zooming In" looks like going "Down" into the funnel
    z_val = -np.log10(z_level) 
    all_z.append(np.full_like(xs, z_val))

# Flatten
X = np.concatenate(all_x)
Y = np.concatenate(all_y)
Z = np.concatenate(all_z)

# ==========================================
# 4. RENDER THE 3D MODEL
# ==========================================

print(f"[-] Rendering Point Cloud ({len(X)} points)...")

fig = plt.figure(figsize=(12, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

# Color by depth (Z)
# Deep inside (bottom) = Hot/White
# Outer rim (top) = Purple/Dark
p = ax.scatter(X, Y, Z, c=Z, cmap='magma', s=0.5, alpha=0.4, linewidth=0)

ax.set_axis_off() # Floating in void

# Set limits tightly
ax.set_xlim(-ZOOM_END, ZOOM_END)
ax.set_ylim(-ZOOM_END, ZOOM_END)
ax.set_zlim(-np.log10(ZOOM_END), -np.log10(ZOOM_START))

plt.title("The Chunk o' Chaos (Volumetric Reconstruction)", color='white', fontsize=15)
plt.tight_layout()
plt.savefig('wada_3d_chunk.png', dpi=150)
print("[+] Build Complete. Saved to 'wada_3d_chunk.png'")
plt.show()