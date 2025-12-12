import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# --- Physics Engine (Inherited from your code) ---
def potential(x, y, lam):
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1/3) * y**3)

def equations_of_motion(t, state, m, lam):
    x, y, px, py = state
    Fx = -x - 2 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)
    return [px / m, py / m, Fx, Fy]

def get_exit(theta, m, lam, E, x0, y0, t_max=2000.0, r_esc=5.0):
    V_start = potential(x0, y0, lam)
    if V_start > E: return -1
    p_mag = np.sqrt(2 * m * (E - V_start))
    
    def escape(t, state, *args):
        return np.sqrt(state[0]**2 + state[1]**2) - r_esc
    escape.terminal = True
    escape.direction = 1

    sol = solve_ivp(
        equations_of_motion, [0, t_max], 
        [x0, y0, p_mag*np.cos(theta), p_mag*np.sin(theta)], 
        args=(m, lam), events=escape, rtol=1e-8, atol=1e-10
    )

    if not sol.t_events[0].size: return 0
    x, y = sol.y[0][-1], sol.y[1][-1]
    angle = np.arctan2(y, x) % (2 * np.pi)
    return int(angle // (2 * np.pi / 3)) + 1

# --- THE RECURSIVE DESCENT ---
def measure_boundary_dimension(theta_center, window_size, m, lam, E, x0, y0, 
                                max_depth=8, samples_per_level=100):
    """
    Recursively zooms into a boundary region and measures how the
    number of boundary crossings scales with resolution.
    
    Returns:
    - scales: Array of window sizes explored
    - counts: Number of basin transitions found at each scale
    - dimension_estimate: Box-counting fractal dimension
    """
    
    print(f"Measuring fractal dimension at θ={theta_center:.5f}, Δθ={window_size:.6f}")
    
    scales = []
    counts = []
    
    current_window = window_size
    
    for depth in range(max_depth):
        # Sample this scale
        thetas = np.linspace(theta_center - current_window/2, 
                            theta_center + current_window/2, 
                            samples_per_level)
        
        exits = []
        for th in thetas:
            exits.append(get_exit(th, m, lam, E, x0, y0, t_max=1500))
        
        exits = np.array(exits)
        
        # Count transitions (boundary crossings)
        transitions = np.sum(exits[:-1] != exits[1:])
        
        if transitions > 0:
            scales.append(current_window)
            counts.append(transitions)
            print(f"  Depth {depth}: Δθ={current_window:.2e}, Transitions={transitions}")
        else:
            print(f"  Depth {depth}: No transitions found, stopping.")
            break
            
        # Zoom in
        current_window *= 0.5
        
    scales = np.array(scales)
    counts = np.array(counts)
    
    # Fractal Dimension via Box Counting
    # N(ε) ~ ε^(-D) => log(N) ~ -D * log(ε)
    if len(scales) > 2:
        log_scales = np.log(scales)
        log_counts = np.log(counts)
        
        # Linear fit
        coeffs = np.polyfit(log_scales, log_counts, 1)
        dimension = -coeffs[0]
        
        print(f"\n>>> Estimated Fractal Dimension: D = {dimension:.4f}")
        return scales, counts, dimension
    else:
        print("\nInsufficient data for dimension estimate.")
        return scales, counts, None

# --- SPATIAL MAPPING OF DIMENSIONS ---
def map_fractal_landscape(m, lam, E, x_range, y_range, resolution=20):
    """
    Creates a 2D map where each pixel shows the local fractal dimension
    of the boundary structure at that starting position.
    """
    
    print(f"Generating {resolution}x{resolution} Fractal Dimension Map...")
    print("This will take significant time. Grab coffee.\n")
    
    xs = np.linspace(*x_range, resolution)
    ys = np.linspace(*y_range, resolution)
    
    dimension_map = np.zeros((resolution, resolution))
    valid_map = np.zeros((resolution, resolution), dtype=bool)
    
    total = resolution * resolution
    count = 0
    
    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            count += 1
            
            # Check if this position is even accessible
            V = potential(x, y, lam)
            if V > E:
                dimension_map[i, j] = np.nan
                continue
                
            print(f"[{count}/{total}] Position ({x:.2f}, {y:.2f})")
            
            # Find a boundary angle at this position
            # Quick scan to locate a transition
            test_thetas = np.linspace(0, 2*np.pi, 36)
            test_exits = []
            for th in test_thetas:
                test_exits.append(get_exit(th, m, lam, E, x, y, t_max=500))
            
            test_exits = np.array(test_exits)
            
            # Find first transition
            trans_idx = -1
            for k in range(len(test_exits)-1):
                if test_exits[k] != test_exits[k+1] and test_exits[k] != 0 and test_exits[k+1] != 0:
                    trans_idx = k
                    break
                    
            if trans_idx == -1:
                dimension_map[i, j] = np.nan
                continue
                
            # Found a boundary, now measure it
            boundary_theta = test_thetas[trans_idx]
            window = 2 * np.pi / 36  # Start with the coarse resolution
            
            _, _, dim = measure_boundary_dimension(
                boundary_theta, window, m, lam, E, x, y,
                max_depth=5, samples_per_level=50
            )
            
            if dim is not None:
                dimension_map[i, j] = dim
                valid_map[i, j] = True
            else:
                dimension_map[i, j] = np.nan
                
            print()
    
    return xs, ys, dimension_map, valid_map

# --- VISUALIZATION ---
def visualize_dimension_landscape(xs, ys, dim_map, valid_map):
    """
    Plots the fractal dimension map with contours.
    """
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # 1. The Dimension Map
    cmap = LinearSegmentedColormap.from_list('fractal', 
                                             ['black', 'purple', 'red', 'orange', 'yellow', 'white'])
    
    im1 = ax1.imshow(dim_map, extent=[xs[0], xs[-1], ys[0], ys[-1]], 
                     origin='lower', cmap=cmap, vmin=0, vmax=1.5, interpolation='bilinear')
    
    ax1.set_xlabel('x position')
    ax1.set_ylabel('y position')
    ax1.set_title('Fractal Dimension Landscape\n(Darkness = Lower Complexity)')
    fig.colorbar(im1, ax=ax1, label='Local Fractal Dimension')
    
    # 2. Validity Mask (Where we got good data)
    ax2.imshow(valid_map, extent=[xs[0], xs[-1], ys[0], ys[-1]], 
               origin='lower', cmap='gray', interpolation='nearest')
    ax2.set_xlabel('x position')
    ax2.set_ylabel('y position')
    ax2.set_title('Data Quality Map\n(White = Valid Measurement)')
    
    plt.tight_layout()
    plt.show()

# --- EXECUTION ---
if __name__ == "__main__":
    MASS = 1.0
    LAMBDA = 1.0
    E_SADDLE = 1.0 / (6.0 * LAMBDA**2)
    ENERGY = E_SADDLE + 0.01
    
    print("="*60)
    print("FRACTAL DIMENSION MAPPER")
    print("Studying the recursive structure of basin boundaries")
    print("="*60)
    print()
    
    # Option 1: Deep dive at a single point
    print("OPTION 1: Single Point Analysis")
    print("-" * 60)
    
    # You found the spike at 3.173, let's measure it
    scales, counts, dim = measure_boundary_dimension(
        theta_center=3.173,
        window_size=0.1,
        m=MASS, lam=LAMBDA, E=ENERGY, x0=0.0, y0=0.0,
        max_depth=10,
        samples_per_level=200
    )
    
    # Plot the scaling relation
    if dim is not None:
        plt.figure(figsize=(10, 6))
        plt.loglog(scales, counts, 'o-', linewidth=2, markersize=8)
        plt.xlabel('Window Size Δθ')
        plt.ylabel('Number of Basin Transitions')
        plt.title(f'Box-Counting Dimension at θ=3.173\nSlope = {-dim:.4f}')
        plt.grid(True, alpha=0.3)
        plt.show()
    
    print("\n" + "="*60)
    print("\nOPTION 2: Spatial Map (Commented out - very slow)")
    print("Uncomment below to generate full landscape")
    print("="*60)
    
    # Option 2: Map the entire space (WARNING: SLOW)
    # Uncomment to run:
    """
    xs, ys, dim_map, valid_map = map_fractal_landscape(
        m=MASS, lam=LAMBDA, E=ENERGY,
        x_range=[-1.5, 1.5],
        y_range=[-1.5, 1.5],
        resolution=15  # Start small!
    )
    
    visualize_dimension_landscape(xs, ys, dim_map, valid_map)
    """