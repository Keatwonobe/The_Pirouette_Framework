import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d import Axes3D
from time import time
from numba import jit, prange

# --------------------------------------------------
# PIROUETTE 3D TOPOGRAPHY: THE RIPPLE SCAN
# --------------------------------------------------
# GOAL: Visualize the "interference fringes" as 
# physical 3D terrain to see the wave structure.
# --------------------------------------------------

# Configuration
RANGE = 18.0
RES = 400            # 400x400 grid (160k polygons - decent for Matplotlib)
STEPS = 500          # Integration depth
DT = 0.015           # Slightly larger step for contrast
GAMMA = 0.02
TWIST = 2.83814

# --- JIT Physics (Standard Float is fine for this scale) ---
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
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    def w_calc(a, t):
        d = np.abs(a - t)
        if d > 180: d = 360 - d
        return np.exp(-(d/80.0)**2)
    
    w_gold = w_calc(angle, 30.0)
    w_teal = w_calc(angle, 150.0)
    w_red = w_calc(angle, 270.0)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

@jit(nopython=True, parallel=True)
def generate_height_map(res, rng):
    grid = np.zeros((res, res))
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
            
            # Height = Log Displacement
            dist = np.sqrt((m - m_start)**2 + (lam - lam_start)**2)
            grid[i, j] = np.log1p(dist) # Log scale smoothes the peaks
            
    return grid

# --- Main Render ---
if __name__ == "__main__":
    print("Simulating 3D Terrain...")
    Z = generate_height_map(RES, RANGE)
    
    print("Rendering 3D Surface...")
    
    # Setup Grid
    x = np.linspace(-RANGE, RANGE, RES)
    y = np.linspace(-RANGE, RANGE, RES)
    X, Y = np.meshgrid(x, y)
    
    # Setup Plot
    fig = plt.figure(figsize=(16, 12), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Lighting (Essential for seeing ripples)
    ls = LightSource(azdeg=315, altdeg=45)
    
    # The Color Map
    # inferno is good: Black valleys, Fire peaks
    rgb = ls.shade(Z, cmap=cm.inferno, vert_exag=0.1, blend_mode='soft')
    
    # Plot Surface
    # rstride/cstride controls downsampling for display speed
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=rgb,
                           linewidth=0, antialiased=False, shade=False)
    
    # Remove pane backgrounds for that "floating in void" look
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    
    # Remove grid lines and ticks for clean art style
    ax.grid(False)
    ax.axis('off')
    
    # Camera Angle
    # Elev=60 looks down at an angle (good for ripples)
    # Azim=-45 aligns with the diagonal symmetry
    ax.view_init(elev=55, azim=-45)
    
    plt.tight_layout()
    filename = f"pirouette_3d_ripples_{RANGE}.png"
    plt.savefig(filename, dpi=100) # 100 DPI is faster for 3D
    print(f"Saved to {filename}")
    plt.show()