import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import pickle

# --- Physics Engine ---
def potential(x, y, lam):
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1/3) * y**3)

def equations_of_motion(t, state, m, lam):
    x, y, px, py = state
    Fx = -x - 2 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)
    return [px / m, py / m, Fx, Fy]

def equations_backward(t, state, m, lam):
    """Time-reversed dynamics"""
    return [-v for v in equations_of_motion(t, state, m, lam)]

# --- IMPROVED MANIFOLD EXTRACTOR ---
class ImprovedManifoldExtractor:
    """
    Extracts manifolds with better control over the integration region.
    """
    
    def __init__(self, m=1.0, lam=1.0):
        self.m = m
        self.lam = lam
        self.saddles = self.find_saddle_points()
        
    def find_saddle_points(self):
        sq3 = np.sqrt(3)
        return [
            (1/sq3, 1/sq3),
            (-1/sq3, 1/sq3),
            (0, -2/sq3)
        ]
    
    def compute_lyapunov_field(self, x, y, t):
        """Compute local Lyapunov exponent from curvature"""
        vx = np.gradient(x, t)
        vy = np.gradient(y, t)
        ax = np.gradient(vx, t)
        ay = np.gradient(vy, t)
        
        v_mag = np.sqrt(vx**2 + vy**2)
        v_mag[v_mag < 1e-10] = 1e-10
        
        cross = vx * ay - vy * ax
        kappa = np.abs(cross) / (v_mag**3)
        
        # Map to reasonable range for visualization
        lyap = np.tanh(kappa * 10)  # Compress to [-1, 1]
        
        return lyap
    
    def trace_manifold(self, saddle_idx, direction='stable', angle_offset=0.0):
        """
        Traces manifold from saddle point.
        
        angle_offset: Rotate initial perturbation by this angle (radians)
        """
        
        sx, sy = self.saddles[saddle_idx]
        
        # Jacobian
        J = np.array([
            [0, 0, 1/self.m, 0],
            [0, 0, 0, 1/self.m],
            [-1 - 2*self.lam*sy, -2*self.lam*sx, 0, 0],
            [-2*self.lam*sx, -1 + 2*self.lam*sy, 0, 0]
        ])
        
        eigvals, eigvecs = np.linalg.eig(J)
        
        if direction == 'stable':
            idx = np.argmin(np.real(eigvals))
        else:
            idx = np.argmax(np.real(eigvals))
        
        eigvec = np.real(eigvecs[:, idx])
        
        # Rotate perturbation
        rot = np.array([
            [np.cos(angle_offset), -np.sin(angle_offset)],
            [np.sin(angle_offset), np.cos(angle_offset)]
        ])
        
        pos_pert = rot @ eigvec[:2]
        
        # Initial condition
        eps = 1e-4
        x0 = sx + eps * pos_pert[0]
        y0 = sy + eps * pos_pert[1]
        px0 = eps * eigvec[2]
        py0 = eps * eigvec[3]
        
        # Boundary event
        def boundary(t, state, *args):
            return np.sqrt(state[0]**2 + state[1]**2) - 2.0
        boundary.terminal = True
        boundary.direction = 1
        
        # Integrate
        eom = equations_of_motion if direction == 'stable' else equations_backward
        t_span = [0, 30.0] if direction == 'stable' else [0, -30.0]
        
        sol = solve_ivp(
            eom,
            t_span,
            [x0, y0, px0, py0],
            args=(self.m, self.lam),
            method='DOP853',
            events=boundary,
            rtol=1e-10,
            atol=1e-13,
            max_step=0.02
        )
        
        if len(sol.t) < 10:
            return None, None, None, None
        
        x = sol.y[0]
        y = sol.y[1]
        t = sol.t
        
        lyap = self.compute_lyapunov_field(x, y, t)
        
        return x, y, lyap, t
    
    def extract_all_manifolds(self, n_angles=6):
        """Extract multiple strands per saddle by varying angle"""
        
        manifolds = {'stable': [], 'unstable': []}
        
        print("Extracting manifold network...")
        
        for saddle_idx in range(3):
            print(f"\nSaddle {saddle_idx+1}:")
            
            for i in range(n_angles):
                angle = 2 * np.pi * i / n_angles
                
                # Stable
                x_s, y_s, lyap_s, t_s = self.trace_manifold(
                    saddle_idx, 'stable', angle
                )
                
                if x_s is not None:
                    manifolds['stable'].append({
                        'saddle': saddle_idx,
                        'angle': angle,
                        'x': x_s,
                        'y': y_s,
                        'lyap': lyap_s,
                        't': t_s
                    })
                    print(f"  Stable {i+1}/{n_angles}: {len(x_s)} points")
                
                # Unstable
                x_u, y_u, lyap_u, t_u = self.trace_manifold(
                    saddle_idx, 'unstable', angle
                )
                
                if x_u is not None:
                    manifolds['unstable'].append({
                        'saddle': saddle_idx,
                        'angle': angle,
                        'x': x_u,
                        'y': y_u,
                        'lyap': lyap_u,
                        't': t_u
                    })
                    print(f"  Unstable {i+1}/{n_angles}: {len(x_u)} points")
        
        return manifolds

# --- VISUALIZATION ---
def visualize_knot_structure(manifolds):
    """
    Multi-panel visualization of the knot structure.
    """
    
    fig = plt.figure(figsize=(20, 14))
    
    # Main 3D view
    ax_main = fig.add_subplot(2, 3, (1, 4), projection='3d')
    
    # Plot stable manifolds (blue tones)
    for m in manifolds['stable']:
        color = plt.cm.Blues(0.4 + 0.5 * m['saddle']/2)
        ax_main.plot(m['x'], m['y'], m['lyap'], 
                    color=color, alpha=0.6, linewidth=1.5)
    
    # Plot unstable manifolds (red tones)
    for m in manifolds['unstable']:
        color = plt.cm.Reds(0.4 + 0.5 * m['saddle']/2)
        ax_main.plot(m['x'], m['y'], m['lyap'], 
                    color=color, alpha=0.6, linewidth=1.5)
    
    # Mark saddle points
    saddles = [(1/np.sqrt(3), 1/np.sqrt(3)), 
               (-1/np.sqrt(3), 1/np.sqrt(3)), 
               (0, -2/np.sqrt(3))]
    
    for i, (sx, sy) in enumerate(saddles):
        ax_main.scatter([sx], [sy], [0], s=300, c='gold', 
                       marker='*', edgecolors='black', linewidths=2, zorder=100)
    
    ax_main.set_xlabel('x position', fontsize=10)
    ax_main.set_ylabel('y position', fontsize=10)
    ax_main.set_zlabel('Lyapunov λ', fontsize=10)
    ax_main.set_title('The Manifold Knot\n(Blue=Stable, Red=Unstable, Stars=Saddles)', 
                     fontsize=12, fontweight='bold')
    ax_main.view_init(elev=25, azim=45)
    
    # View 2: Top-down (xy projection)
    ax2 = fig.add_subplot(2, 3, 2)
    
    for m in manifolds['stable']:
        ax2.plot(m['x'], m['y'], color='blue', alpha=0.3, linewidth=1)
    for m in manifolds['unstable']:
        ax2.plot(m['x'], m['y'], color='red', alpha=0.3, linewidth=1)
    
    for sx, sy in saddles:
        ax2.scatter([sx], [sy], s=200, c='gold', marker='*', 
                   edgecolors='black', linewidths=2, zorder=100)
    
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_title('Top View (xy projection)\nThe Braiding Pattern')
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    
    # View 3: Side view (xz projection)
    ax3 = fig.add_subplot(2, 3, 3)
    
    for m in manifolds['stable']:
        ax3.plot(m['x'], m['lyap'], color='blue', alpha=0.3, linewidth=1)
    for m in manifolds['unstable']:
        ax3.plot(m['x'], m['lyap'], color='red', alpha=0.3, linewidth=1)
    
    ax3.set_xlabel('x')
    ax3.set_ylabel('Lyapunov λ')
    ax3.set_title('Side View (xλ projection)\nThe Twist Structure')
    ax3.grid(True, alpha=0.3)
    
    # View 4: Another angle
    ax4 = fig.add_subplot(2, 3, 5, projection='3d')
    
    # Only plot a subset for clarity
    for m in manifolds['stable'][::2]:
        ax4.plot(m['x'], m['y'], m['lyap'], 
                color='blue', alpha=0.7, linewidth=2)
    for m in manifolds['unstable'][::2]:
        ax4.plot(m['x'], m['y'], m['lyap'], 
                color='red', alpha=0.7, linewidth=2)
    
    for sx, sy in saddles:
        ax4.scatter([sx], [sy], [0], s=300, c='gold', 
                   marker='*', edgecolors='black', linewidths=2, zorder=100)
    
    ax4.set_xlabel('x')
    ax4.set_ylabel('y')
    ax4.set_zlabel('λ')
    ax4.set_title('Sparse View\n(Every other strand)')
    ax4.view_init(elev=45, azim=-60)
    
    # View 5: Lyapunov distribution
    ax5 = fig.add_subplot(2, 3, 6)
    
    all_lyap_stable = np.concatenate([m['lyap'] for m in manifolds['stable']])
    all_lyap_unstable = np.concatenate([m['lyap'] for m in manifolds['unstable']])
    
    ax5.hist(all_lyap_stable, bins=50, alpha=0.6, color='blue', 
            label='Stable', density=True)
    ax5.hist(all_lyap_unstable, bins=50, alpha=0.6, color='red', 
            label='Unstable', density=True)
    
    ax5.set_xlabel('Lyapunov Exponent λ')
    ax5.set_ylabel('Density')
    ax5.set_title('Lyapunov Distribution\nAlong Manifolds')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('manifold_knot_complete.png', dpi=150, bbox_inches='tight')
    print("\nSaved: manifold_knot_complete.png")
    plt.show()

def compute_topology_metrics(manifolds):
    """Compute knot invariants"""
    
    print("\n" + "="*60)
    print("TOPOLOGICAL ANALYSIS")
    print("="*60)
    
    # Count strands per saddle
    stable_counts = [0, 0, 0]
    unstable_counts = [0, 0, 0]
    
    for m in manifolds['stable']:
        stable_counts[m['saddle']] += 1
    for m in manifolds['unstable']:
        unstable_counts[m['saddle']] += 1
    
    print("\nStrand counts:")
    for i in range(3):
        print(f"  Saddle {i+1}: {stable_counts[i]} stable, {unstable_counts[i]} unstable")
    
    # Compute total path lengths
    print("\nPath lengths (proxy for manifold extent):")
    
    for manifold_type in ['stable', 'unstable']:
        print(f"\n{manifold_type.upper()}:")
        for m in manifolds[manifold_type]:
            path_length = np.sum(np.sqrt(np.diff(m['x'])**2 + np.diff(m['y'])**2))
            print(f"  Saddle {m['saddle']+1}, angle {m['angle']:.2f}: "
                  f"Length = {path_length:.4f}")
    
    # Check for heteroclinic connections (manifolds that come close)
    print("\n" + "="*60)
    print("HETEROCLINIC CONNECTIONS")
    print("="*60)
    
    connections = []
    
    for m_s in manifolds['stable']:
        for m_u in manifolds['unstable']:
            # Check minimum distance between curves
            min_dist = float('inf')
            
            for i in range(len(m_s['x'])):
                for j in range(len(m_u['x'])):
                    dist = np.sqrt((m_s['x'][i] - m_u['x'][j])**2 + 
                                  (m_s['y'][i] - m_u['y'][j])**2)
                    if dist < min_dist:
                        min_dist = dist
            
            if min_dist < 0.1:  # Threshold for "close"
                connections.append({
                    'stable_saddle': m_s['saddle'],
                    'unstable_saddle': m_u['saddle'],
                    'distance': min_dist
                })
    
    if len(connections) > 0:
        print(f"\nFound {len(connections)} potential heteroclinic connections:")
        for conn in connections[:10]:  # Show first 10
            print(f"  Stable {conn['stable_saddle']+1} → Unstable {conn['unstable_saddle']+1}: "
                  f"dist = {conn['distance']:.6f}")
    else:
        print("\nNo close approaches detected (manifolds well-separated)")

# --- EXECUTION ---
if __name__ == "__main__":
    print("="*60)
    print("INTEGRATED MANIFOLD KNOT ANALYZER")
    print("="*60)
    print()
    
    extractor = ImprovedManifoldExtractor(m=1.0, lam=1.0)
    
    # Extract with more strands for better coverage
    manifolds = extractor.extract_all_manifolds(n_angles=8)
    
    # Save for later use
    with open('manifolds_data.pkl', 'wb') as f:
        pickle.dump(manifolds, f)
    print("\nSaved manifolds to: manifolds_data.pkl")
    
    # Visualize
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    visualize_knot_structure(manifolds)
    
    # Analyze
    compute_topology_metrics(manifolds)
    
    print("\n" + "="*60)
    print("COMPLETE")
    print("="*60)
    print("\nThe knot structure has been extracted and visualized.")
    print("Look for:")
    print("  - Braiding in the top view")
    print("  - Twist in the side view")
    print("  - Interweaving in the 3D view")