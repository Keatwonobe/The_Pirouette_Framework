import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# --- 1. The Physics (The Basin) ---

def potential(x, y, lam):
    """Standard Henon-Heiles Potential."""
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1/3) * y**3)

def forces(x, y, lam):
    """Negative gradient of potential: Fx = -dV/dx, Fy = -dV/dy."""
    Fx = -x - 2 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)
    return Fx, Fy

def equations_of_motion(t, state, m, lam):
    x, y, px, py = state
    Fx, Fy = forces(x, y, lam)
    # x_dot = p/m, p_dot = Force
    return [px / m, py / m, Fx, Fy]

# --- 2. The Measurer (Integration) ---

def get_trajectory_outcome(theta, m, lam, E, x0, y0, t_max=1000.0, r_esc=5.0):
    """
    Launches a particle and returns (exit_id, dwell_time).
    """
    # 1. Initialize Momentum based on Energy
    V_start = potential(x0, y0, lam)
    
    # Safety check: Is start point valid?
    if V_start > E:
        return -1, 0.0 # Tunneling required (forbidden)

    # Kinetic Energy T = E - V = p^2 / 2m => p = sqrt(2m(E-V))
    p_mag = np.sqrt(2 * m * (E - V_start))
    px0 = p_mag * np.cos(theta)
    py0 = p_mag * np.sin(theta)

    # 2. Define Escape Event
    # FIXED: Added *args to accept m and lam (even though we don't use them here)
    def escape_condition(t, state, *args):
        x, y, _, _ = state
        return np.sqrt(x**2 + y**2) - r_esc
        
    escape_condition.terminal = True
    escape_condition.direction = 1 # Trigger only when crossing outwards

    # 3. Integrate
    sol = solve_ivp(
        equations_of_motion, 
        [0, t_max], 
        [x0, y0, px0, py0], 
        args=(m, lam),
        events=escape_condition,
        rtol=1e-6, atol=1e-9 # High precision for chaos
    )

    # 4. Classify Outcome
    if not sol.t_events or not sol.t_events[0].size: 
        # Did not escape
        return 0, t_max
    
    # Escaped
    t_escape = sol.t_events[0][0]
    x_end, y_end = sol.y[0][-1], sol.y[1][-1]
    
    # Classify Exit (angles 0 to 2pi)
    angle_esc = np.arctan2(y_end, x_end) % (2 * np.pi)
    
    # Hénon-Heiles usually has 3 exits separated by 120 degrees (2pi/3)
    # We map angle to exits 1, 2, 3
    exit_id = int(angle_esc // (2 * np.pi / 3)) + 1
    
    return exit_id, t_escape

# --- 3. The Scanner (Coarse Search) ---

def scan_angles(m, lam, E, x0, y0, n_samples=360, t_max=500.0):
    """
    Scans the horizon to find 'sticky' regions.
    """
    thetas = np.linspace(0, 2*np.pi, n_samples)
    results = []
    
    print(f"Scanning {n_samples} angles...")
    for theta in thetas:
        exit_id, T = get_trajectory_outcome(theta, m, lam, E, x0, y0, t_max)
        results.append((theta, exit_id, T))
        
    dtype = [('theta', float), ('exit', int), ('T', float)]
    return np.array(results, dtype=dtype)

# --- 4. The Pinpoint (Surface Tension Finder) ---

def find_surface_tension_angle(m, lam, E, x0, y0, scan_data, t_refine=2000.0):
    """
    Takes scan data, finds the highest dwell time peak, 
    and zooms in to find the critical angle theta_star.
    """
    # 1. Identify the Bracket around the highest peak
    # We look for a local maximum in dwell time T
    Ts = scan_data['T']
    idx_max = np.argmax(Ts)
    
    # Initial bracket: the neighboring points in the coarse scan
    # Handle wrap-around indices
    n = len(scan_data)
    theta_L = scan_data['theta'][(idx_max - 1) % n]
    theta_R = scan_data['theta'][(idx_max + 1) % n]
    
    print(f"Bracketing peak near {scan_data['theta'][idx_max]:.3f} rad...")

    # 2. Greedy Bisection (Hill Climbing on Dwell Time)
    # We assume the singularity (infinity) is between L and R.
    # We narrow the window by keeping the side with higher T.
    
    current_L, current_R = theta_L, theta_R
    best_theta = scan_data['theta'][idx_max]
    max_dwell_found = Ts[idx_max]
    
    for i in range(20): # 20 iterations is huge precision zoom
        mid = (current_L + current_R) / 2
        
        # Test slightly to the left and right of mid to find gradient direction
        # (Since the peak might be infinitely sharp, simple midpoint check isn't enough)
        delta = (current_R - current_L) * 0.1
        
        # Ensure we don't collapse too fast
        if delta < 1e-12: delta = 1e-12

        _, T_left = get_trajectory_outcome(mid - delta, m, lam, E, x0, y0, t_refine)
        _, T_right = get_trajectory_outcome(mid + delta, m, lam, E, x0, y0, t_refine)
        
        # Update best found
        if T_left > max_dwell_found: 
            max_dwell_found = T_left
            best_theta = mid - delta
        if T_right > max_dwell_found: 
            max_dwell_found = T_right
            best_theta = mid + delta

        # Squeeze the bracket towards the higher ground
        if T_left > T_right:
            current_R = mid # Peak is likely in the left half
        else:
            current_L = mid # Peak is likely in the right half
            
        # Stopping condition: Bracket is tiny
        if abs(current_R - current_L) < 1e-7:
            break
            
    return best_theta, max_dwell_found

# --- 5. Execution ---

if __name__ == "__main__":
    # Parameters
    MASS = 1.0
    LAMBDA = 1.0
    # Dynamic Energy Calculation: Slightly above the saddle
    E_SADDLE = 1.0 / (6.0 * LAMBDA**2)
    ENERGY = E_SADDLE + 0.01  # +0.01 ensures we can escape
    
    print(f"Saddle Energy: {E_SADDLE:.5f}")
    print(f"Particle Energy: {ENERGY:.5f}")

    X_START, Y_START = 0.0, 0.0 

    # --- 1. The Panoramic Scan (Color Coded) ---
    print("Running Panoramic Scan...")
    # Increase resolution to see the "fuzz"
    data = scan_angles(MASS, LAMBDA, ENERGY, X_START, Y_START, n_samples=1000, t_max=500.0)

    # Separate data by exit for coloring
    # Exit 0 = Stuck (Black)
    # Exit 1 = Top Right (Red)
    # Exit 2 = Top Left (Green)
    # Exit 3 = Bottom (Blue)
    
    colors = ['k', 'r', 'g', 'b']
    labels = ['Stuck/Slow', 'Exit 1', 'Exit 2', 'Exit 3']
    
    plt.figure(figsize=(12, 6))
    
    for exit_code in [1, 2, 3, 0]:
        mask = (data['exit'] == exit_code)
        if np.any(mask):
            plt.scatter(data['theta'][mask], data['T'][mask], 
                        c=colors[exit_code], s=10, label=labels[exit_code], alpha=0.6)

    # --- 2. The Zoom (Investigating the 3.17 Spike) ---
    print("Zooming in on the spike at 3.17...")
    theta_center = 3.17
    window = 0.05 # +/- 0.05 radians
    
    # Generate high-res scan just for the spike
    thetas_zoom = np.linspace(theta_center - window, theta_center + window, 200)
    T_zoom = []
    
    for th in thetas_zoom:
        # Use higher t_max here to see the top of the mountain
        _, T = get_trajectory_outcome(th, MASS, LAMBDA, ENERGY, X_START, Y_START, t_max=1500.0)
        T_zoom.append(T)
        
    # Plot the zoom as a faint overlay line to show the "True Shape"
    plt.plot(thetas_zoom, T_zoom, 'k-', alpha=0.3, linewidth=1, label='Deep Zoom Scan')

    plt.axvline(3.17, color='k', linestyle='--', alpha=0.3)
    plt.title(f"Fractal Scattering: Exit Channels & Dwell Time\nE={ENERGY:.4f}")
    plt.xlabel("Launch Angle (rad)")
    plt.ylabel("Dwell Time (Pirouettes)")
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.2)
    plt.show()