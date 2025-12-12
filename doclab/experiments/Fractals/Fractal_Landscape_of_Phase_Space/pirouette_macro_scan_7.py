import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d import Axes3D
from numba import jit, prange

# --------------------------------------------------
# PIROUETTE REALITY MAP: THE SPEED MANIFOLD
# --------------------------------------------------
# GOAL: Create a 3D surface where Height = Particle Speed.
# This visualizes the "Jets" as physical mountains of velocity.
# --------------------------------------------------

# Configuration
RANGE = 600000.0  # The scale where the jets live
RES = 400              # Resolution
STEPS = 500
DT = 0.05              # Matches the animation time step
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
    
    # Optimized weight calc
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

@jit(nopython=True, parallel=True)
def generate_speed_manifold(res, rng):
    speed_grid = np.zeros((res, res))
    
    x_vals = np.linspace(-rng, rng, res)
    y_vals = np.linspace(-rng, rng, res)
    
    for i in prange(res):
        lam_start = y_vals[i]
        for j in range(res):
            m_start = x_vals[j]
            
            m = m_start
            lam = lam_start
            pm = 0.0
            plam = 0.0
            
            # Run sim
            for _ in range(STEPS):
                Fm, Flam, w_red = get_force_fast(m, lam)
                drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
                pm = (pm + 0.5 * DT * Fm) * drag
                plam = (plam + 0.5 * DT * Flam) * drag
                m += DT * pm
                lam += DT * plam
            
            # Calculate Speed Magnitude
            speed = np.sqrt(pm**2 + plam**2)
            
            # Use Log scale to handle the massive difference between Zone 1 and Jets
            # Clamp to avoid overflow if things go crazy
            speed = min(speed, 1e20) 
            speed_grid[i, j] = np.log1p(speed)
            
    return speed_grid

if __name__ == "__main__":
    print(f"Generating Speed Manifold (Scale {RANGE})...")
    Z = generate_speed_manifold(RES, RANGE)
    
    # --- DEBUG: Check if physics actually ran ---
    print(f"Data Stats: Min={Z.min():.4f}, Max={Z.max():.4f}, Mean={Z.mean():.4f}")
    if np.isnan(Z).any():
        print("WARNING: Data contains NaNs. Replacing with 0.")
        Z = np.nan_to_num(Z)
    
    print("Rendering 3D Surface...")
    
    x = np.linspace(-RANGE, RANGE, RES)
    y = np.linspace(-RANGE, RANGE, RES)
    X, Y = np.meshgrid(x, y)
    
    fig = plt.figure(figsize=(16, 12), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Lighting Configuration
    ls = LightSource(azdeg=315, altdeg=45)
    
    # --- FIX 1: Normalize Z for the Color Shader ---
    # This ensures the colors map to the full range of the colormap
    # regardless of how small the log(speed) numbers are.
    z_min, z_max = Z.min(), Z.max()
    if z_max > z_min:
        Z_norm = (Z - z_min) / (z_max - z_min)
    else:
        Z_norm = Z # Avoid divide by zero if flat
    
    # --- FIX 2: Shade using the Normalized Data ---
    # We increase vert_exag significantly so the shader sees the terrain features
    rgb = ls.shade(Z_norm, cmap=cm.plasma, vert_exag=5.0, blend_mode='soft')
    
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=rgb,
                           linewidth=0, antialiased=False, shade=False)
    
    # Styling
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.grid(False)
    ax.axis('off')
    
    # View Angle
    ax.view_init(elev=60, azim=-45)
    
    plt.tight_layout()
    filename = f"pirouette_speed_manifold_{RANGE}.png"
    plt.savefig(filename, dpi=100)
    print(f"Saved to {filename}")
    plt.show()