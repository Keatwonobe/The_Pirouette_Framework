import numpy as np
import matplotlib.pyplot as plt
from numba import njit
import time

# ==========================================
# 1. CONFIGURATION
# ==========================================
SAMPLES_PER_ITER = 5000 # Number of random points to test per iteration
ITERS = 50              # Number of refinement steps
KEEP_FRACTION = 0.05    # Keep top 5% of points (based on low T) for next iteration
DT = 0.05               # Time step
T_MAX_HYPER = 5.0       # MAX simulation time (VERY low for 'success fast')
ESCAPE_R2 = 25.0        # Escape horizon (kept from original)

# 3D Search Space Configuration (m, l, sigma)
ML_CENTER = np.array([0.0, 0.0])
ML_RANGE_INIT = 0.5
SIGMA_CENTER_INIT = 1.0
SIGMA_RANGE_INIT = 0.5


# ==========================================
# 2. PHYSICS KERNEL (JIT COMPILED)
# ==========================================
@njit(fastmath=True)
def get_data(m, l, sigma):
    """
    Simulates a single particle in the potential V(m, l; sigma)
    and returns:
    1. Basin (0=Trapped, 1,2,3=Escaped)
    2. Frustration (Accumulated Force Stress)
    3. Escape Time (Steps taken)
    """
    pm, pl = 0.0, 0.0 # Start from rest
    steps = 0
    stress = 0.0
    max_steps = int(T_MAX_HYPER / DT)

    for _ in range(max_steps):
        # 1. Force Calculation (F = -grad V)
        fm = -(m + 2*sigma*m*l)
        fl = -(l + sigma*(m**2 - l**2))

        # Frustration Accumulation
        force_mag = np.sqrt(fm*fm + fl*fl)
        stress += force_mag * DT

        # 2. Symplectic Integration (Velocity Verlet structure)
        # Half-step velocity
        pm += 0.5 * DT * fm
        pl += 0.5 * DT * fl
        
        # Full-step position
        m += DT * pm
        l += DT * pl

        # Recalc force for second half-step
        fm = -(m + 2*sigma*m*l)
        fl = -(l + sigma*(m**2 - l**2))
        
        # Second half-step velocity
        pm += 0.5 * DT * fm
        pl += 0.5 * DT * fl

        steps += 1

        # 3. Escape Condition
        if m*m + l*l > ESCAPE_R2:
            # Basin assignment based on exit angle (for consistency, though we ignore basin in this search)
            angle = np.arctan2(l, m)
            if angle > 0.5 and angle < 2.6: return 1, stress, steps
            elif angle <= -2.6 or angle >= 2.6: return 2, stress, steps
            else: return 3, stress, steps

    return 0, stress, steps # Trapped


# ==========================================
# 3. MAIN EXECUTION (CHAOS HYPERSEEKER)
# ==========================================
if __name__ == "__main__":
    start_time = time.time()
    
    # --- Initial Search Volume ---
    ml_center = ML_CENTER
    ml_range = ML_RANGE_INIT
    sigma_center = SIGMA_CENTER_INIT
    sigma_range = SIGMA_RANGE_INIT
    
    # List to store (m, l, sigma, steps) of all best points found
    best_points = [] 

    print(f"[*] Starting Chaos Hyperseek in 3D (m, l, sigma)...")
    print(f"[*] Target: Fastest escapes ($T \\le {T_MAX_HYPER:.2f}$s)")

    for i in range(ITERS):
        # 1. GENERATE POINTS: Define the search space for this iteration
        m_pts = np.random.uniform(ml_center[0] - ml_range, ml_center[0] + ml_range, SAMPLES_PER_ITER)
        l_pts = np.random.uniform(ml_center[1] - ml_range, ml_center[1] + ml_range, SAMPLES_PER_ITER)
        s_pts = np.random.uniform(sigma_center - sigma_range, sigma_center + sigma_range, SAMPLES_PER_ITER)

        # 2. RUN SIMULATIONS & FILTER: Run the JIT-compiled kernel on all points
        escaped_points_data = []
        for m, l, s in zip(m_pts, l_pts, s_pts):
            # Only run the kernel if sigma is within a reasonable non-negative range
            if s > 0:
                basin, stress, steps = get_data(m, l, s)
                if basin != 0: # Only keep points that escaped
                    escaped_points_data.append((m, l, s, steps))
        
        if not escaped_points_data:
            # If no points escaped in the search area, slightly expand the search
            ml_range *= 1.2
            sigma_range *= 1.2
            print(f"   [!] Iter {i+1}/{ITERS}: No escapes found. Expanding search range.")
            continue

        # Convert to numpy array for efficient sorting and mean calculation
        escaped_points = np.array(escaped_points_data)
        
        # 3. RANK CHAOS: Sort by minimum escape time (steps)
        # Note: We sort by the last column (steps)
        escaped_points = escaped_points[escaped_points[:, 3].argsort()]
        
        # 4. REFINE: Select the most chaotic points (lowest T) and update centers
        num_keep = max(10, int(len(escaped_points) * KEEP_FRACTION))
        top_points = escaped_points[:num_keep]
        best_points.extend(top_points.tolist()) # Store for final plot

        # Calculate new center and range for next iteration
        ml_center = top_points[:, :2].mean(axis=0)
        sigma_center = top_points[:, 2].mean()
        
        # Range reduction: Zoom in on the new center
        ml_range *= 0.75
        sigma_range *= 0.75

        # Ensure range doesn't get too small or sigma range is non-negative
        ml_range = max(ml_range, 1e-6)
        sigma_range = max(sigma_range, 1e-6)
        
        print(f"   [+] Iter {i+1}/{ITERS}: Found {len(escaped_points)} escapes. New center (m,l,sigma) = ({ml_center[0]:.4f}, {ml_center[1]:.4f}, {sigma_center:.4f}). Range: {ml_range:.4f}")

    elapsed = time.time() - start_time
    print(f"[+] Hyperseek Complete in {elapsed:.2f}s. Total points found: {len(best_points)}")

    # ==========================================
    # 4. VISUALIZATION (3D Scatter)
    # ==========================================
    if not best_points:
        print("[!] No highly chaotic points found to plot.")
    else:
        final_points = np.array(best_points)
        m, l, s, steps = final_points.T

        # Chaos Metric: Inverse Time (Higher value = Higher Chaos)
        # T_escape = steps * DT
        chaos_metric = 1.0 / (steps * DT)

        fig = plt.figure(figsize=(10, 10))
        # Use a high DPI for better resolution in 3D
        ax = fig.add_subplot(projection='3d')

        # Scatter plot: m, l, sigma (colored by chaos)
        scatter = ax.scatter(m, l, s, c=chaos_metric, cmap='plasma', s=3, alpha=0.7)

        # Labels
        ax.set_xlabel('Initial Position $m$')
        ax.set_ylabel('Initial Position $l$')
        ax.set_zlabel('Potential Parameter $\\sigma$')
        ax.set_title('Chaos Hyperseeker: High-Frequency Manifold in 3D $(m, l, \\sigma)$', color='white')

        # Style
        ax.set_facecolor('black')
        ax.xaxis.pane.fill = ax.yaxis.pane.fill = ax.zaxis.pane.fill = False # Make background transparent
        ax.xaxis.pane.edgecolor = ax.yaxis.pane.edgecolor = ax.zaxis.pane.edgecolor = '#222222' # Subtle grid lines
        
        # Colorbar for the Chaos Metric
        cbar = fig.colorbar(scatter, ax=ax, shrink=0.7, aspect=20, pad=0.1)
        cbar.set_label('Chaos Frequency ($1/T_{escape}$)', color='white')
        cbar.ax.tick_params(colors='white')
        
        # Tick colors
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.tick_params(axis='z', colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.zaxis.label.set_color('white')
        
        plt.savefig('chaos_hyperseeker_3d_manifold.png')
        plt.close(fig)
        print("[+] 3D Chaos Hyperseek Visualization Saved to 'chaos_hyperseeker_3d_manifold.png'")