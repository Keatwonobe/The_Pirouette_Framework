import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# --- 1. The Physics (The Arena) ---
def potential(x, y, lam):
    """Hénon-Heiles Potential Energy Surface."""
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1/3) * y**3)

def equations_of_motion(t, state, m, lam):
    x, y, px, py = state
    # Forces are negative gradient of potential
    Fx = -x - 2 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)
    return [px / m, py / m, Fx, Fy]

# --- 2. The Oracle (Determines Fate) ---
def get_exit_from_rest(x0, y0, m, lam, t_max=2000.0, r_esc_sq=36.0):
    """
    Drops a particle from (x0, y0) with ZERO initial momentum.
    Returns the Exit ID (1, 2, 3) or 0 if trapped.
    """
    # Define Escape Event (using squared radius for speed)
    def escape(t, state, *args):
        return (state[0]**2 + state[1]**2) - r_esc_sq
    escape.terminal = True
    escape.direction = 1

    # Integrate from rest (px=0, py=0)
    # Add minuscule noise to break perfect symmetry on separatrix lines
    x0_p = x0 + np.random.uniform(-1e-9, 1e-9)
    y0_p = y0 + np.random.uniform(-1e-9, 1e-9)

    sol = solve_ivp(
        equations_of_motion,
        [0, t_max],
        [x0_p, y0_p, 0.0, 0.0], 
        args=(m, lam),
        events=escape,
        rtol=1e-5, atol=1e-7 # Good balance for a large map
    )

    # Check if it escaped
    if not sol.t_events[0].size:
        return 0 # Trapped

    # Classify Exit based on final angle
    x_end, y_end = sol.y[0][-1], sol.y[1][-1]
    angle = np.arctan2(y_end, x_end) % (2 * np.pi)
    # Map 3 sectors to IDs 1, 2, 3
    exit_id = int(angle // (2 * np.pi / 3)) + 1
    return exit_id

# --- 3. The Map Maker (The Loop) ---
def generate_basin_map(m, lam, xy_limits, resolution):
    print(f"Starting map generation ({resolution}x{resolution} pixels)...")
    print("This will take a moment. Watch the progress.")
    
    xs = np.linspace(xy_limits[0], xy_limits[1], resolution)
    ys = np.linspace(xy_limits[2], xy_limits[3], resolution)
    
    # The image array. Rows are y, Cols are x.
    basin_img = np.zeros((resolution, resolution), dtype=int)
    
    total_pixels = resolution * resolution
    count = 0
    
    for i in range(resolution): # Loop over y (rows)
        y = ys[i]
        for j in range(resolution): # Loop over x (cols)
            x = xs[j]
            
            # Get the fate of this pixel
            exit_id = get_exit_from_rest(x, y, m, lam)
            
            # Fill image array (invert y index for image coordinates)
            basin_img[resolution - 1 - i, j] = exit_id
            
            count += 1
            if count % (total_pixels // 10) == 0:
                print(f"Progress: {count / total_pixels * 100:.0f}%")
                
    return basin_img

# --- 4. Execution and Visualization ---
if __name__ == "__main__":
    # Parameters
    MASS = 1.0
    LAMBDA = 1.0
    RES = 400  # Resolution (e.g., 400x400). Higher = slower but prettier.
    LIMITS = [-2.0, 2.0, -2.0, 2.0] # [x_min, x_max, y_min, y_max]
    
    # 1. Generate the Map
    img_data = generate_basin_map(MASS, LAMBDA, LIMITS, RES)
    
    # 2. Plotting
    plt.figure(figsize=(10, 10), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')

    # Define our cosmic colormap
    # 0=Black, 1=Red, 2=Green, 3=Blue
    cmap = ListedColormap(['black', 'red', 'green', 'blue'])
    
    plt.imshow(img_data, extent=LIMITS, origin='lower', cmap=cmap, interpolation='nearest')
    
    # Overlay potential contours for context
    X, Y = np.meshgrid(np.linspace(*LIMITS[:2], 200), np.linspace(*LIMITS[2:], 200))
    Z = potential(X, Y, LAMBDA)
    E_saddle = 1.0 / (6.0 * LAMBDA**2)
    # Draw the "coastline" of the saddle energy
    plt.contour(X, Y, Z, levels=[E_saddle], colors='white', linewidths=1, linestyles='--', alpha=0.7)
    
    # Styling
    plt.title(f"The Mirror Universe: Hénon-Heiles Basins ($\lambda$={LAMBDA})", color='white', fontsize=16)
    plt.xlabel("x position", color='white')
    plt.ylabel("y position", color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    
    # Custom Legend
    legend_elements = [
        Patch(facecolor='black', edgecolor='w', label='Trapped/High Ground'),
        Patch(facecolor='red', edgecolor='w', label='Exit 1 Basin'),
        Patch(facecolor='green', edgecolor='w', label='Exit 2 Basin'),
        Patch(facecolor='blue', edgecolor='w', label='Exit 3 Basin'),
        plt.Line2D([0], [0], color='white', linestyle='--', label='Saddle Energy Limit')
    ]
    plt.legend(handles=legend_elements, loc='upper right', facecolor='black', edgecolor='white', labelcolor='white')
    
    plt.tight_layout()
    print("Rendering image...")
    plt.show()