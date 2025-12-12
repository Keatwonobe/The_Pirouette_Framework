import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D
from numba import jit, prange

# --------------------------------------------------
# PIROUETTE HYDRODYNAMICS: 3D FLOW MAP
# --------------------------------------------------
# GOAL: Visualize the terrain (Stability) AND the 
# wind direction (Flow) simultaneously.
# --------------------------------------------------

# Configuration
# We use 6000 to ensure the ripples are real physics, not digital noise.
RANGE = 600000000.0   
RES = 400
STEPS = 500
DT = 0.015
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
def generate_hydro_data(res, rng):
    height_grid = np.zeros((res, res))
    flow_dir_grid = np.zeros((res, res)) # To store the angle of movement
    
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
            
            # 1. Calculate Height (Stability)
            # CLAMPING: We limit the distance to avoid "Infinity" errors
            dist = np.sqrt((m - m_start)**2 + (lam - lam_start)**2)
            dist = min(dist, 1000000.0) # Clamp ceiling
            height_grid[i, j] = np.log1p(dist)
            
            # 2. Calculate Flow Direction (The "Wind")
            # We compare where we ended up vs where we started
            delta_m = m - m_start
            delta_lam = lam - lam_start
            
            # Calculate angle in radians (from -pi to pi)
            angle = np.arctan2(delta_lam, delta_m)
            flow_dir_grid[i, j] = angle
            
    return height_grid, flow_dir_grid

if __name__ == "__main__":
    print(f"Simulating Hydrodynamics (Range +/- {RANGE})...")
    Z, Flow = generate_hydro_data(RES, RANGE)
    
    print("Rendering 3D Flow Map...")
    
    x = np.linspace(-RANGE, RANGE, RES)
    y = np.linspace(-RANGE, RANGE, RES)
    X, Y = np.meshgrid(x, y)
    
    fig = plt.figure(figsize=(16, 12), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # --- The Magic: Map Flow Angle to Color ---
    # Normalize flow angle (-pi to pi) to (0 to 1) for the colormap
    norm_flow = (Flow + np.pi) / (2 * np.pi)
    
    # Use 'hsv' colormap because it is circular (Red->Green->Blue->Red)
    # This represents direction perfectly (Compass Rose)
    color_map = cm.hsv(norm_flow)
    
    # Plot Surface
    surf = ax.plot_surface(X, Y, Z, 
                           facecolors=color_map, # Color by Wind Direction
                           rstride=1, cstride=1, 
                           linewidth=0, antialiased=False, shade=True)
    
    # Styling
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.grid(False)
    ax.axis('off')
    
    # Add a Color Compass Legend
    # We create a dummy scatter plot just to make the colorbar work
    m = cm.ScalarMappable(cmap=cm.hsv)
    m.set_array([])
    cbar = plt.colorbar(m, ax=ax, shrink=0.5, aspect=10, pad=0.0)
    cbar.set_label('Flow Direction (Cyclic)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    ax.set_title(f"Pirouette Hydrodynamics\nHeight = Instability | Color = Flow Direction", color='white')
    ax.view_init(elev=55, azim=-45)
    
    plt.tight_layout()
    filename = f"pirouette_hydro_flow{RANGE}.png"
    plt.savefig(filename, dpi=100)
    print(f"Saved to {filename}")
    plt.show()