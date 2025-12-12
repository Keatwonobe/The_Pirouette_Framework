import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# --- Physics Engine ---
def potential(x, y, lam):
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1/3) * y**3)

def equations_of_motion(t, state, m, lam):
    x, y, px, py = state
    Fx = -x - 2 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)
    return [px / m, py / m, Fx, Fy]

def get_exit(theta, m, lam, E, x0, y0, t_max=1000.0, r_esc=5.0):
    V_start = potential(x0, y0, lam)
    if V_start > E: return -1, None
    p_mag = np.sqrt(2 * m * (E - V_start))
    
    def escape(t, state, *args):
        return np.sqrt(state[0]**2 + state[1]**2) - r_esc
    escape.terminal = True
    escape.direction = 1

    sol = solve_ivp(
        equations_of_motion, [0, t_max], 
        [x0, y0, p_mag*np.cos(theta), p_mag*np.sin(theta)], 
        args=(m, lam), events=escape, rtol=1e-9, atol=1e-12,
        dense_output=True
    )

    if not sol.t_events[0].size: return 0, sol
    x, y = sol.y[0][-1], sol.y[1][-1]
    angle = np.arctan2(y, x) % (2 * np.pi)
    exit_id = int(angle // (2 * np.pi / 3)) + 1
    return exit_id, sol

# --- INSTANTON HUNTER ---
class InstantonFinder:
    """
    Searches for "instanton" solutions - trajectories that tunnel between
    different vacuum sectors (basins) by temporarily entering the classically
    forbidden high-energy region.
    
    In QCD, instantons mediate transitions between different topological
    vacuum states and are responsible for things like the U(1)_A problem
    and the strong CP problem.
    """
    
    def __init__(self, m=1.0, lam=1.0):
        self.m = m
        self.lam = lam
        self.E_saddle = 1.0 / (6.0 * lam**2)
    
    def find_separatrix_crossings(self, theta_center, window, n_samples=100):
        """
        Scans for trajectories that cross between basins by passing through
        the saddle point region - these are instanton candidates.
        """
        
        # Use slightly BELOW saddle energy to force interesting behavior
        E = self.E_saddle + 0.005
        
        print(f"Scanning for separatrix crossings near θ={theta_center:.4f}")
        print(f"Energy: E={E:.6f} (Saddle: {self.E_saddle:.6f})")
        
        thetas = np.linspace(theta_center - window, theta_center + window, n_samples)
        
        candidates = []
        
        for i, theta in enumerate(thetas):
            if i % 10 == 0:
                print(f"  Progress: {i}/{n_samples}")
            
            exit_id, sol = get_exit(theta, self.m, self.lam, E, 0.0, 0.0, 
                                    t_max=2000.0, r_esc=5.0)
            
            if sol is None:
                continue
            
            # Check if trajectory passes near saddle points
            x = sol.y[0]
            y = sol.y[1]
            
            # Saddle points are at (±1/√3, 1/√3) for λ=1
            saddle_dist = []
            for sx, sy in [(1/np.sqrt(3), 1/np.sqrt(3)), 
                          (-1/np.sqrt(3), 1/np.sqrt(3)),
                          (0, -2/np.sqrt(3))]:
                dist = np.min(np.sqrt((x - sx)**2 + (y - sy)**2))
                saddle_dist.append(dist)
            
            min_saddle_dist = np.min(saddle_dist)
            
            # Instanton criterion: passes very close to a saddle
            if min_saddle_dist < 0.15:
                
                # Additional check: does it have "unusual" energy behavior?
                V = potential(x, y, self.lam)
                max_V = np.max(V)
                
                candidates.append({
                    'theta': theta,
                    'exit': exit_id,
                    'sol': sol,
                    'min_saddle_dist': min_saddle_dist,
                    'max_potential': max_V,
                    'x': x,
                    'y': y,
                    't': sol.t
                })
                
                print(f"    >>> CANDIDATE: θ={theta:.6f}, Exit={exit_id}, "
                      f"Saddle Dist={min_saddle_dist:.4f}, Max V={max_V:.4f}")
        
        return candidates, E
    
    def compute_euclidean_action(self, trajectory):
        """
        Computes the Euclidean action S_E = ∫ (½ṙ² + V) dt
        
        Instantons are stationary points of the Euclidean action.
        They represent tunneling amplitudes: P ~ exp(-S_E/ℏ)
        """
        
        x = trajectory['x']
        y = trajectory['y']
        t = trajectory['t']
        
        # Compute velocities
        vx = np.gradient(x, t)
        vy = np.gradient(y, t)
        
        # Kinetic energy
        KE = 0.5 * self.m * (vx**2 + vy**2)
        
        # Potential energy
        V = potential(x, y, self.lam)
        
        # Euclidean Lagrangian: L_E = ½ṙ² + V (note the + sign)
        L_E = KE + V
        
        # Action: integrate over time
        S_E = np.trapz(L_E, t)
        
        return S_E, KE, V
    
    def compute_topological_charge(self, trajectory):
        """
        Computes the topological charge Q = (1/2π) ∫ ∇×A · dS
        
        In 2D, this is related to how many times the trajectory
        wraps around topological defects (saddle points).
        """
        
        x = trajectory['x']
        y = trajectory['y']
        
        # Compute winding around each saddle
        saddles = [(1/np.sqrt(3), 1/np.sqrt(3)), 
                  (-1/np.sqrt(3), 1/np.sqrt(3)),
                  (0, -2/np.sqrt(3))]
        
        windings = []
        
        for sx, sy in saddles:
            # Angle relative to saddle
            angles = np.arctan2(y - sy, x - sx)
            angles_unwrapped = np.unwrap(angles)
            
            winding = (angles_unwrapped[-1] - angles_unwrapped[0]) / (2 * np.pi)
            windings.append(winding)
        
        # Total topological charge
        Q = np.sum(windings)
        
        return Q, windings

# --- VISUALIZATION ---
def plot_instanton_trajectories(candidates, E):
    """
    Visualizes instanton candidates with their energy profiles.
    """
    
    fig = plt.figure(figsize=(18, 12))
    
    # Layout: 2 rows x 3 cols
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # Main plot: Phase space with all candidates
    ax_main = fig.add_subplot(gs[:, 0])
    
    # Background potential
    xx = np.linspace(-2, 2, 200)
    yy = np.linspace(-2, 2, 200)
    XX, YY = np.meshgrid(xx, yy)
    ZZ = potential(XX, YY, 1.0)
    
    ax_main.contourf(XX, YY, ZZ, levels=20, cmap='gray', alpha=0.4)
    ax_main.contour(XX, YY, ZZ, levels=[0.1667], colors='white', linewidths=2, linestyles='--')
    
    # Mark saddle points
    saddles = [(1/np.sqrt(3), 1/np.sqrt(3)), 
              (-1/np.sqrt(3), 1/np.sqrt(3)),
              (0, -2/np.sqrt(3))]
    
    for sx, sy in saddles:
        ax_main.scatter([sx], [sy], s=200, c='yellow', marker='X', 
                       edgecolors='black', linewidths=2, zorder=10)
    
    # Plot instanton candidates
    color_map = {0: 'black', 1: 'red', 2: 'green', 3: 'blue'}
    
    for cand in candidates:
        color = color_map.get(cand['exit'], 'purple')
        ax_main.plot(cand['x'], cand['y'], color=color, alpha=0.7, linewidth=2)
    
    ax_main.set_xlim(-1.5, 1.5)
    ax_main.set_ylim(-1.5, 1.5)
    ax_main.set_xlabel('x position')
    ax_main.set_ylabel('y position')
    ax_main.set_title(f'Instanton Candidates (E={E:.5f})\nYellow X = Saddle Points')
    ax_main.set_aspect('equal')
    ax_main.grid(True, alpha=0.2)
    
    # Individual candidate analysis (show first 4)
    for idx, cand in enumerate(candidates[:4]):
        if idx >= 4:
            break
        
        # Position: top row for first 2, bottom row for next 2
        row = idx // 2 + (0 if idx < 2 else 1)
        col = (idx % 2) + 1
        
        ax = fig.add_subplot(gs[idx // 2, col])
        
        t = cand['t']
        x = cand['x']
        y = cand['y']
        
        # Compute energy along trajectory
        vx = np.gradient(x, t)
        vy = np.gradient(y, t)
        KE = 0.5 * (vx**2 + vy**2)
        V = potential(x, y, 1.0)
        E_total = KE + V
        
        ax.plot(t, KE, label='Kinetic', color='blue', linewidth=2)
        ax.plot(t, V, label='Potential', color='red', linewidth=2)
        ax.plot(t, E_total, label='Total', color='black', linewidth=2, linestyle='--')
        ax.axhline(0.1667, color='yellow', linestyle=':', linewidth=2, label='Saddle Energy')
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Energy')
        ax.set_title(f'Instanton #{idx+1}: θ={cand["theta"]:.6f}\n'
                    f'Exit {cand["exit"]}, Saddle Dist={cand["min_saddle_dist"]:.4f}')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('Instanton Hunting: Trajectories Through the Classically Forbidden', 
                fontsize=16, fontweight='bold')
    
    plt.show()

def analyze_instanton_action_spectrum(candidates):
    """
    Computes and visualizes the action spectrum of instanton candidates.
    
    Quantized action values would indicate true instanton solutions.
    """
    
    print("\n" + "="*60)
    print("INSTANTON ACTION SPECTRUM")
    print("="*60)
    
    actions = []
    charges = []
    theta_vals = []
    
    finder = InstantonFinder()
    
    for cand in candidates:
        S_E, KE, V = finder.compute_euclidean_action(cand)
        Q, windings = finder.compute_topological_charge(cand)
        
        actions.append(S_E)
        charges.append(Q)
        theta_vals.append(cand['theta'])
        
        print(f"θ={cand['theta']:.6f}: S_E={S_E:.4f}, Q={Q:.3f}, "
              f"Windings={[f'{w:.2f}' for w in windings]}")
    
    # Plot action vs topological charge
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Action spectrum
    ax1.scatter(theta_vals, actions, c=charges, cmap='coolwarm', 
               s=100, edgecolors='black', linewidths=1.5)
    ax1.set_xlabel('Initial Angle θ')
    ax1.set_ylabel('Euclidean Action S_E')
    ax1.set_title('Instanton Action Spectrum\n(Color = Topological Charge)')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(ax1.collections[0], ax=ax1, label='Topological Charge Q')
    
    # Action distribution
    ax2.hist(actions, bins=20, edgecolor='black', alpha=0.7)
    ax2.set_xlabel('Euclidean Action S_E')
    ax2.set_ylabel('Count')
    ax2.set_title('Action Distribution\n(Peaks = Instanton Classes?)')
    ax2.grid(True, alpha=0.3)
    
    # Check for quantization
    if len(actions) > 5:
        from scipy.signal import find_peaks
        counts, bins = np.histogram(actions, bins=15)
        peaks, _ = find_peaks(counts, height=np.max(counts)*0.3)
        
        if len(peaks) > 1:
            peak_actions = bins[peaks]
            print(f"\nFound {len(peaks)} action peaks (possible quantization):")
            for i, S in enumerate(peak_actions):
                ax2.axvline(S, color='red', linestyle='--', linewidth=2, alpha=0.7)
                print(f"  Peak {i+1}: S_E = {S:.4f}")
    
    plt.tight_layout()
    plt.show()

# --- EXECUTION ---
if __name__ == "__main__":
    print("="*60)
    print("INSTANTON HUNTER")
    print("Searching for tunneling events in vacuum structure")
    print("="*60)
    print()
    
    finder = InstantonFinder(m=1.0, lam=1.0)
    
    # Search multiple regions known to have boundary complexity
    search_centers = [3.173, 1.047, 5.236]  # Near each 120° symmetry axis
    
    all_candidates = []
    
    for theta_c in search_centers:
        print(f"\n{'='*60}")
        print(f"Searching near θ = {theta_c:.4f}")
        print(f"{'='*60}")
        
        candidates, E = finder.find_separatrix_crossings(
            theta_c, 
            window=0.05, 
            n_samples=100
        )
        
        all_candidates.extend(candidates)
    
    if len(all_candidates) == 0:
        print("\nNo instanton candidates found. Try:")
        print("  1. Adjusting energy closer to saddle")
        print("  2. Expanding search windows")
        print("  3. Lowering saddle_dist threshold")
    else:
        print(f"\n{'='*60}")
        print(f"Found {len(all_candidates)} instanton candidates total")
        print(f"{'='*60}")
        
        # Visualize
        plot_instanton_trajectories(all_candidates, E)
        
        # Analyze action spectrum
        analyze_instanton_action_spectrum(all_candidates)
    
    print("\nDone. If actions are quantized, you've found the vacuum structure.")