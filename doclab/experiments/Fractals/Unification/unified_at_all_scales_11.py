import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numba

# ======================
# CONFIGURATION
# ======================
RES = 1000              # High resolution for the zoom
MAX_STEPS = 5000        # Longer life to detect subtle captures
DT = 0.01               # Finer time step for precision

# FRACTAL ZOOM WINDOW
# We focus specifically on the "Edge" of the capture zone
IMPACT_MIN, IMPACT_MAX = 0.1, 8.0   # The "Coastline"
VEL_MIN, VEL_MAX = 0.4, 0.8         # The "Sweet Spot" for chaos

print("=" * 60)
print("F R A C T A L   D E E P   D I V E")
print(f"Zooming into Impact Zone: {IMPACT_MIN} to {IMPACT_MAX}")
print("=" * 60)

# ======================
# PHYSICS KERNEL
# ======================
@numba.jit(nopython=True)
def simulate_collision(impact_param, velocity):
    # Initial Conditions (Dipole Setup)
    # T1 (Compressor/Attractor)
    x1, y1 = -3.0, impact_param / 2.0
    vx1, vy1 = velocity, 0.0
    
    # T2 (Expander/Void)
    x2, y2 = 3.0, -impact_param / 2.0
    vx2, vy2 = -velocity, 0.0
    
    # Physics Tuning
    k_sub = 1.5      # Stronger Substrate (Sharper Chaos)
    g_int = 2.0      # Mutual Interaction
    
    for t in range(MAX_STEPS):
        # 1. Hénon-Heiles Substrate Forces (The "Triangle")
        # T1
        fx1_sub = -k_sub * (x1 + 2*x1*y1)
        fy1_sub = -k_sub * (y1 + x1**2 - y1**2)
        # T2
        fx2_sub = -k_sub * (x2 + 2*x2*y2)
        fy2_sub = -k_sub * (y2 + x2**2 - y2**2)
        
        # 2. Mutual Interaction (Dipole)
        dx = x2 - x1
        dy = y2 - y1
        dist_sq = dx*dx + dy*dy + 0.01
        dist = np.sqrt(dist_sq)
        f_mag = g_int / dist_sq
        
        nx, ny = dx/dist, dy/dist
        
        # T1 is pulled to T2
        vx1 += (fx1_sub + f_mag*nx) * DT
        vy1 += (fy1_sub + f_mag*ny) * DT
        
        # T2 is pulled to T1
        vx2 += (fx2_sub - f_mag*nx) * DT
        vy2 += (fy2_sub - f_mag*ny) * DT
        
        # Update
        x1 += vx1 * DT; y1 += vy1 * DT
        x2 += vx2 * DT; y2 += vy2 * DT
        
        # Check Escape (Scattering)
        r1_sq = x1*x1 + y1*y1
        if r1_sq > 25.0:
            angle = np.arctan2(y1, x1)
            # Map Angle to Basin Color
            if angle > 0.5 and angle < 2.5: return 1   # Top (Red)
            if angle > 2.5 or angle < -2.5: return 2   # Left (Teal)
            return 3                                   # Right (Gold)
            
    # Captured (The Knot)
    return 0

@numba.jit(nopython=True, parallel=True)
def run_zoom_grid(res):
    grid = np.zeros((res, res), dtype=np.int32)
    impacts = np.linspace(IMPACT_MIN, IMPACT_MAX, res)
    vels = np.linspace(VEL_MIN, VEL_MAX, res)
    
    for i in numba.prange(res):
        v = vels[i]
        for j in range(res):
            imp = impacts[j]
            grid[i, j] = simulate_collision(imp, v)
    return grid

# ======================
# MAIN EXECUTION
# ======================
def render_zoom():
    print(f"[*] Scanning {RES*RES} trajectories...")
    fate_map = run_zoom_grid(RES)
    print("[✓] Physics calculated.")
    
    plt.figure(figsize=(12, 10), facecolor='black')
    
    # The "Wada" Palette
    # Black = Knot, Red/Teal/Gold = Basins
    cmap = ListedColormap(['black', '#ff3333', '#00cccc', '#ffaa00'])
    
    plt.imshow(fate_map, origin='lower', 
               extent=[IMPACT_MIN, IMPACT_MAX, VEL_MIN, VEL_MAX],
               aspect='auto', cmap=cmap, interpolation='nearest')
    
    plt.xlabel("Impact Parameter (Zoomed)", color='white', fontsize=12)
    plt.ylabel("Velocity", color='white', fontsize=12)
    plt.title("The Coastline of Chaos: Searching for Wada", color='white', fontsize=16)
    
    plt.tick_params(colors='white')
    plt.tight_layout()
    plt.savefig('wada_fractal_zoom.png', dpi=200)
    print("[✓] Image saved to 'wada_fractal_zoom.png'")
    plt.show()

if __name__ == "__main__":
    render_zoom()