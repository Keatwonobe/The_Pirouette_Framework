import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d import Axes3D
from numba import jit, prange

# --------------------------------------------------
# PIROUETTE SPEED MANIFOLD (VARIABLE RESOLUTION)
# --------------------------------------------------

# Configuration
RANGE = 600_000_000.0  # Massive Scale
RES = 500              # Resolution
STEPS = 500
DT = 0.05
GAMMA = 0.02
TWIST = 2.83814

@jit(nopython=True, fastmath=True)
def get_force_fast(m, lam):
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -m
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag = np.sqrt(sum_m**2 + sum_lam**2)
    scale = np.sqrt(mag)
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    # Weights
    angle_deg = (np.degrees(np.arctan2(lam, m))) % 360.0
    
    def get_w(target):
        d = np.abs(angle_deg - target)
        d = np.minimum(d, 360.0 - d)
        return np.exp(-(d/80.0)**2)

    w_gold = get_w(30.0)
    w_teal = get_w(150.0)
    w_red = get_w(270.0)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, w_red

# We pass the custom grids (x_grid, y_grid) instead of generating them inside
@jit(nopython=True, parallel=True)
def generate_speed_manifold_variable(x_vals, y_vals):
    res_x = len(x_vals)
    res_y = len(y_vals)
    speed_grid = np.zeros((res_y, res_x))
    
    for i in prange(res_y):
        lam_start = y_vals[i]
        for j in range(res_x):
            m_start = x_vals[j]
            
            m = m_start
            lam = lam_start
            pm = 0.0
            plam = 0.0
            
            for _ in range(STEPS):
                Fm, Flam, w_red = get_force_fast(m, lam)
                drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
                pm = (pm + 0.5 * DT * Fm) * drag
                plam = (plam + 0.5 * DT * Flam) * drag
                m += DT * pm
                lam += DT * plam
            
            speed = np.sqrt(pm**2 + plam**2)
            speed = min(speed, 1e20) 
            speed_grid[i, j] = np.log1p(speed)
            
    return speed_grid

if __name__ == "__main__":
    print(f"Generating Variable Resolution Grid (Max Scale {RANGE})...")
    
    # --- THE MAGIC TRICK: CUBIC DISTRIBUTION ---
    # We create a generic space from -1 to 1
    t = np.linspace(-1, 1, RES)
    
    # We cube it (t^3). This keeps -1 and 1 at the edges,
    # but flattens the curve near zero.
    # Result: Lots of points near 0, few points near max range.
    # We multiply by RANGE to scale it up.
    grid_distribution = (np.sign(t) * np.abs(t)**5) * RANGE
    
    # Create the 2D mesh based on this clustered grid
    X, Y = np.meshgrid(grid_distribution, grid_distribution)
    
    Z = generate_speed_manifold_variable(grid_distribution, grid_distribution)
    
    print("Rendering 3D Surface...")
    
    fig = plt.figure(figsize=(16, 12), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    ls = LightSource(azdeg=315, altdeg=45)
    
    # Normalize for color
    z_min, z_max = Z.min(), Z.max()
    Z_norm = (Z - z_min) / (z_max - z_min) if z_max > z_min else Z
    
    rgb = ls.shade(Z_norm, cmap=cm.plasma, vert_exag=5.0, blend_mode='soft')
    
    # Plot using the non-linear X and Y
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=rgb,
                           linewidth=0, antialiased=False, shade=False)
    
    ax.axis('off')
    
    # View Angle
    ax.view_init(elev=60, azim=-45)
    
    plt.tight_layout()
    filename = "pirouette_speed_fisheye.png"
    plt.savefig(filename, dpi=100)
    print(f"Saved to {filename}")
    plt.show()