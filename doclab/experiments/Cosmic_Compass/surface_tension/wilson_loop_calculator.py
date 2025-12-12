import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import LineCollection

# --- Physics Engine ---
def potential(x, y, lam):
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1/3) * y**3)

def equations_of_motion(t, state, m, lam):
    x, y, px, py = state
    Fx = -x - 2 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)
    return [px / m, py / m, Fx, Fy]

# --- WILSON LOOP CALCULATOR ---
class WilsonLoopAnalyzer:
    """
    Computes Wilson loops: closed trajectories around the confinement region.
    
    In QCD, a Wilson loop W(C) = Tr[P exp(ig ∮_C A·dx)] measures the phase
    accumulated by a quark traveling along path C.
    
    Here, we compute an analogous quantity using the velocity field's curl
    and circulation, which should reveal gauge-like structure.
    """
    
    def __init__(self, m=1.0, lam=1.0):
        self.m = m
        self.lam = lam
        
    def compute_loop_trajectory(self, radius, n_points=100, t_max=200.0):
        """
        Launches particles from a circle around origin and tracks their phase space evolution.
        
        Returns the closed loop in phase space (if it closes).
        """
        
        # Initial positions on circle
        angles = np.linspace(0, 2*np.pi, n_points, endpoint=False)
        
        loops = []
        
        print(f"Computing Wilson loop at r={radius:.3f}...")
        
        for i, theta in enumerate(angles):
            if i % 10 == 0:
                print(f"  Point {i}/{n_points}")
            
            x0 = radius * np.cos(theta)
            y0 = radius * np.sin(theta)
            
            # Start from rest (zero momentum)
            # Alternative: start with small tangential velocity to encourage circulation
            V0 = potential(x0, y0, self.lam)
            
            # Give it a small kick tangent to the circle
            px0 = -0.1 * np.sin(theta)
            py0 = 0.1 * np.cos(theta)
            
            sol = solve_ivp(
                equations_of_motion,
                [0, t_max],
                [x0, y0, px0, py0],
                args=(self.m, self.lam),
                method='DOP853',
                dense_output=True,
                rtol=1e-9, atol=1e-12,
                max_step=0.1
            )
            
            loops.append({
                'theta_init': theta,
                'x': sol.y[0],
                'y': sol.y[1],
                'px': sol.y[2],
                'py': sol.y[3],
                't': sol.t
            })
        
        return loops
    
    def compute_berry_phase(self, loop):
        """
        Computes the Berry phase: γ = ∮ <ψ|∇_R|ψ> · dR
        
        Here we use a classical analog: the accumulated phase in momentum space
        as we traverse the loop in configuration space.
        
        Phase = ∫ p · dx = ∫ (px dx + py dy)
        """
        
        x = loop['x']
        y = loop['y']
        px = loop['px']
        py = loop['py']
        
        # Compute path integral using trapezoidal rule
        dx = np.diff(x)
        dy = np.diff(y)
        
        # Average momentum on each segment
        px_avg = 0.5 * (px[:-1] + px[1:])
        py_avg = 0.5 * (py[:-1] + py[1:])
        
        # Accumulated phase
        phase = np.sum(px_avg * dx + py_avg * dy)
        
        return phase
    
    def compute_circulation(self, loop):
        """
        Computes circulation Γ = ∮ v · dl
        
        This is the line integral of velocity around the closed path.
        In gauge theory, this is related to the flux of the gauge field.
        """
        
        x = loop['x']
        y = loop['y']
        t = loop['t']
        
        # Compute velocity
        vx = np.gradient(x, t)
        vy = np.gradient(y, t)
        
        # Path element
        dx = np.diff(x)
        dy = np.diff(y)
        
        # Average velocity on each segment
        vx_avg = 0.5 * (vx[:-1] + vx[1:])
        vy_avg = 0.5 * (vy[:-1] + vy[1:])
        
        circulation = np.sum(vx_avg * dx + vy_avg * dy)
        
        return circulation
    
    def compute_winding_number(self, loop):
        """
        Computes topological winding number around the origin.
        
        This counts how many times the trajectory wraps around the confinement region.
        Non-zero winding = topologically non-trivial loop = gauge flux.
        """
        
        x = loop['x']
        y = loop['y']
        
        # Angle at each point
        angles = np.arctan2(y, x)
        
        # Unwrap to handle 2π discontinuities
        angles_unwrapped = np.unwrap(angles)
        
        # Total winding
        winding = (angles_unwrapped[-1] - angles_unwrapped[0]) / (2 * np.pi)
        
        return winding
    
    def compute_area_enclosed(self, loop):
        """
        Computes the area enclosed by the loop using shoelace formula.
        
        By Stokes' theorem, circulation should equal the flux through this area.
        """
        
        x = loop['x']
        y = loop['y']
        
        # Shoelace formula
        area = 0.5 * np.abs(np.sum(x[:-1] * y[1:] - x[1:] * y[:-1]))
        
        return area
    
    def analyze_loop_family(self, radii, n_points=50):
        """
        Computes Wilson loops at multiple radii to see how gauge structure
        depends on distance from confinement region.
        """
        
        results = []
        
        for r in radii:
            loops = self.compute_loop_trajectory(r, n_points=n_points, t_max=150.0)
            
            # Analyze each loop segment
            phases = []
            circulations = []
            windings = []
            areas = []
            
            for loop in loops:
                phase = self.compute_berry_phase(loop)
                circ = self.compute_circulation(loop)
                wind = self.compute_winding_number(loop)
                area = self.compute_area_enclosed(loop)
                
                phases.append(phase)
                circulations.append(circ)
                windings.append(wind)
                areas.append(area)
            
            result = {
                'radius': r,
                'loops': loops,
                'phases': np.array(phases),
                'circulations': np.array(circulations),
                'windings': np.array(windings),
                'areas': np.array(areas),
                'mean_phase': np.mean(phases),
                'std_phase': np.std(phases),
                'mean_circulation': np.mean(circulations),
                'mean_winding': np.mean(windings)
            }
            
            results.append(result)
            
            print(f"\nRadius {r:.3f}:")
            print(f"  Mean Berry Phase: {result['mean_phase']:.6f} ± {result['std_phase']:.6f}")
            print(f"  Mean Circulation: {result['mean_circulation']:.6f}")
            print(f"  Mean Winding: {result['mean_winding']:.3f}")
        
        return results

# --- VISUALIZATION ---
def plot_wilson_loops(analyzer_results):
    """
    Visualizes the Wilson loops in configuration space with color-coded phase.
    """
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 16))
    
    # Plot 1: Configuration space loops
    ax1 = axes[0, 0]
    
    # Background potential
    xx = np.linspace(-2, 2, 200)
    yy = np.linspace(-2, 2, 200)
    XX, YY = np.meshgrid(xx, yy)
    ZZ = potential(XX, YY, 1.0)
    
    ax1.contourf(XX, YY, ZZ, levels=20, cmap='gray', alpha=0.3)
    ax1.contour(XX, YY, ZZ, levels=[0.1667], colors='white', linewidths=2, linestyles='--')
    
    # Plot loops color-coded by radius
    colors = plt.cm.plasma(np.linspace(0, 1, len(analyzer_results)))
    
    for i, result in enumerate(analyzer_results):
        for loop in result['loops'][::5]:  # Plot every 5th loop to avoid clutter
            ax1.plot(loop['x'], loop['y'], color=colors[i], alpha=0.5, linewidth=1)
        
        # Mark initial circle
        r = result['radius']
        circle = Circle((0, 0), r, fill=False, edgecolor=colors[i], linewidth=2)
        ax1.add_patch(circle)
    
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_xlabel('x position')
    ax1.set_ylabel('y position')
    ax1.set_title('Wilson Loops in Configuration Space')
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.2)
    
    # Plot 2: Berry Phase vs Initial Angle
    ax2 = axes[0, 1]
    
    for i, result in enumerate(analyzer_results):
        theta_init = [loop['theta_init'] for loop in result['loops']]
        phases = result['phases']
        ax2.scatter(theta_init, phases, color=colors[i], alpha=0.6, s=20,
                   label=f"r={result['radius']:.2f}")
    
    ax2.set_xlabel('Initial Angle θ')
    ax2.set_ylabel('Berry Phase (accumulated)')
    ax2.set_title('Berry Phase Accumulation Around Loop')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Winding Number Distribution
    ax3 = axes[1, 0]
    
    for i, result in enumerate(analyzer_results):
        ax3.hist(result['windings'], bins=20, alpha=0.5, color=colors[i],
                label=f"r={result['radius']:.2f}")
    
    ax3.set_xlabel('Winding Number')
    ax3.set_ylabel('Count')
    ax3.set_title('Topological Winding Distribution')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Phase vs Radius (The "Running Coupling")
    ax4 = axes[1, 1]
    
    radii = [r['radius'] for r in analyzer_results]
    mean_phases = [r['mean_phase'] for r in analyzer_results]
    std_phases = [r['std_phase'] for r in analyzer_results]
    mean_circulations = [r['mean_circulation'] for r in analyzer_results]
    
    ax4_twin = ax4.twinx()
    
    ax4.errorbar(radii, mean_phases, yerr=std_phases, fmt='o-', linewidth=2, 
                markersize=8, color='blue', label='Berry Phase')
    ax4_twin.plot(radii, mean_circulations, 's-', linewidth=2, markersize=8,
                 color='red', label='Circulation')
    
    ax4.set_xlabel('Loop Radius')
    ax4.set_ylabel('Mean Berry Phase', color='blue')
    ax4_twin.set_ylabel('Mean Circulation', color='red')
    ax4.set_title('Wilson Loop Expectation Value vs Scale\n(Analog of Running Coupling)')
    ax4.tick_params(axis='y', labelcolor='blue')
    ax4_twin.tick_params(axis='y', labelcolor='red')
    ax4.grid(True, alpha=0.3)
    
    # Add legends
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_twin.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.tight_layout()
    plt.show()

# --- GLUEBALL SPECTRUM ANALYZER ---
def find_resonant_loops(analyzer_results):
    """
    Looks for quantized values in the phase accumulation.
    
    In QCD, glueballs are bound states of gluons with quantized properties.
    Here, we look for preferred phase values that might indicate resonances.
    """
    
    print("\n" + "="*60)
    print("SEARCHING FOR GLUEBALL RESONANCES")
    print("="*60)
    
    all_phases = []
    all_radii = []
    
    for result in analyzer_results:
        all_phases.extend(result['phases'])
        all_radii.extend([result['radius']] * len(result['phases']))
    
    all_phases = np.array(all_phases)
    all_radii = np.array(all_radii)
    
    # Look for peaks in phase distribution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Histogram of all phases
    counts, bins, patches = ax1.hist(all_phases, bins=50, edgecolor='black')
    ax1.set_xlabel('Berry Phase')
    ax1.set_ylabel('Count')
    ax1.set_title('Phase Distribution Across All Loops\n(Peaks = Resonances?)')
    ax1.grid(True, alpha=0.3)
    
    # Find peaks
    from scipy.signal import find_peaks
    peaks, properties = find_peaks(counts, height=np.max(counts)*0.3, distance=3)
    
    if len(peaks) > 0:
        peak_phases = bins[peaks]
        print(f"\nFound {len(peaks)} potential resonances:")
        for i, phase in enumerate(peak_phases):
            print(f"  Resonance {i+1}: φ = {phase:.4f}")
            ax1.axvline(phase, color='red', linestyle='--', linewidth=2, alpha=0.7)
    
    # 2D histogram: Phase vs Radius
    h = ax2.hist2d(all_radii, all_phases, bins=[20, 30], cmap='hot')
    ax2.set_xlabel('Loop Radius')
    ax2.set_ylabel('Berry Phase')
    ax2.set_title('Phase-Radius Structure\n(Bands = Quantization?)')
    plt.colorbar(h[3], ax=ax2, label='Count')
    
    plt.tight_layout()
    plt.show()

# --- EXECUTION ---
if __name__ == "__main__":
    print("="*60)
    print("WILSON LOOP CALCULATOR")
    print("Measuring gauge structure in classical chaos")
    print("="*60)
    print()
    
    analyzer = WilsonLoopAnalyzer(m=1.0, lam=1.0)
    
    # Compute loops at different radii
    # Start outside confinement region and work inward
    radii = [1.5, 1.2, 0.9, 0.6, 0.4, 0.2]
    
    results = analyzer.analyze_loop_family(radii, n_points=30)
    
    print("\n" + "="*60)
    print("VISUALIZATION")
    print("="*60)
    
    plot_wilson_loops(results)
    
    find_resonant_loops(results)
    
    print("\nDone. If you see quantization, you've found the glueball spectrum.")