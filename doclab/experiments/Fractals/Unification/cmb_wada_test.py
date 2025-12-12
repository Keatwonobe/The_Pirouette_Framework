import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy.interpolate import LinearNDInterpolator
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

def get_wada_graph(n_points, oracle_map, zoom):
    res = oracle_map.shape[0]
    grad_x = np.abs(np.diff(oracle_map, axis=1, append=oracle_map[:, -1:]))
    grad_y = np.abs(np.diff(oracle, axis=0, append=oracle[-1:, :]))
    boundaries = (grad_x + grad_y) > 0
    pdf = np.ones_like(oracle, dtype=float) * 0.05
    pdf[boundaries] = 8.0 
    pdf /= pdf.sum()
    indices = np.arange(pdf.size)
    chosen = np.random.choice(indices, size=n_points, replace=False, p=pdf.flatten())
    py, px = np.unravel_index(chosen, oracle.shape)
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
# 2. FRUSTRATION ENGINE
# ==========================================

class FrustrationScanner:
    def __init__(self, points, adj_list, temp=2.8):
        self.n = len(points)
        self.points = points
        self.adj = adj_list
        self.temp = temp
        self.spins = np.random.choice([-1, 1], size=self.n)

    def relax(self, steps=100):
        for _ in range(steps):
            indices = np.random.randint(0, self.n, size=self.n // 2)
            for idx in indices:
                s = self.spins[idx]
                h = sum(self.spins[n] for n in self.adj[idx])
                dE = 2 * s * h
                if dE <= 0 or np.random.rand() < np.exp(-dE / self.temp):
                    self.spins[idx] *= -1

    def get_energy(self):
        energies = np.zeros(self.n)
        for i in range(self.n):
            h = sum(self.spins[n] for n in self.adj[i])
            energies[i] = -1 * self.spins[i] * h
        return energies

# ==========================================
# 3. SPHERICAL PROJECTION
# ==========================================

RES = 800
ZOOM = 2.0
N_POINTS = 8000
TEMP = 3.0 # High energy to see the chaos

print("[-] Generating Wada Frustration Data...")
oracle = generate_oracle_map(RES, ZOOM)
pts, adj = get_wada_graph(N_POINTS, oracle, ZOOM)
scanner = FrustrationScanner(pts, adj, temp=TEMP)
scanner.relax(steps=200)
energy = scanner.get_energy()

print("[-] Interpolating to Grid...")
# Standard grid
grid_res = 800
gx = np.linspace(-ZOOM, ZOOM, grid_res)
gy = np.linspace(-ZOOM, ZOOM, grid_res)
GX, GY = np.meshgrid(gx, gy)
interp = LinearNDInterpolator(pts, energy)
heat_flat = interp(GX, GY)
# Fill nan
heat_flat[np.isnan(heat_flat)] = 0.0

print("[-] Projecting to Sphere (Mollweide)...")

# Mollweide coordinates
# Longitude: -pi to pi
# Latitude: -pi/2 to pi/2
n_lon = 800
n_lat = 400
lon = np.linspace(-np.pi, np.pi, n_lon)
lat = np.linspace(-np.pi/2, np.pi/2, n_lat)
LON, LAT = np.meshgrid(lon, lat)

# Mapping Logic:
# North Pole (Lat=pi/2) -> Wada Center (0,0)
# South Pole (Lat=-pi/2) -> Wada Edge (r=ZOOM)
# Longitude -> Wada Angle

# 1. Map Lat/Lon to Polar (r, theta)
# r = 0 at Lat=pi/2, r=ZOOM at Lat=-pi/2
# Linear mapping for now:
r_proj = ZOOM * (1.0 - (LAT + np.pi/2) / np.pi) 

# theta = Longitude
theta_proj = LON

# 2. Polar to Cartesian (Wada Coordinates)
wada_x = r_proj * np.cos(theta_proj)
wada_y = r_proj * np.sin(theta_proj)

# 3. Sample the Flat Heatmap at these coordinates
# We need to map wada_x, wada_y to indices in heat_flat
# wada_x is in [-ZOOM, ZOOM]
# Index = (val + ZOOM) / (2*ZOOM) * (grid_res-1)
x_idx = ((wada_x + ZOOM) / (2*ZOOM) * (grid_res - 1)).astype(int)
y_idx = ((wada_y + ZOOM) / (2*ZOOM) * (grid_res - 1)).astype(int)

# Clip
x_idx = np.clip(x_idx, 0, grid_res-1)
y_idx = np.clip(y_idx, 0, grid_res-1)

sphere_data = heat_flat[y_idx, x_idx]

# Plot
fig = plt.figure(figsize=(15, 8), facecolor='black')
ax = fig.add_subplot(111, projection='mollweide')
ax.set_facecolor('black')

# Plot Heatmap
im = ax.pcolormesh(lon, lat, sphere_data, cmap='inferno', shading='auto', vmin=-4, vmax=4)

ax.grid(color='cyan', alpha=0.3, linestyle='--')
ax.set_title("The Traveler's Impact (Wada Frustration on CMB Sphere)", color='white', fontsize=16)
ax.tick_params(colors='white')

# Add label for the "Green Spike" location
ax.text(0, np.pi/2 - 0.2, "THE TRAVELER (North Pole)", color='lime', ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('wada_cmb_projection.png', dpi=150)
print("[+] Projection Complete.")