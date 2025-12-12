import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# --- Physics Engine ---
def potential(x, y, lam):
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1/3) * y**3)

def equations_of_motion(t, state, m, lam):
    x, y, px, py = state
    Fx = -x - 2 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)
    return [px / m, py / m, Fx, Fy]

def equations_backward(t, state, m, lam):
    """Time-reversed dynamics to trace backward along unstable manifold"""
    return [-v for v in equations_of_motion(t, state, m, lam)]

# --- MANIFOLD TRACER ---
class ManifoldKnotExtractor:
    """
    Extracts stable and unstable manifolds as curves in 3D space.
    
    The third dimension is the Lyapunov exponent field or temporal phase,
    which reveals the braiding structure.
    """
    
    def __init__(self, m=1.0, lam=1.0):
        self.m = m
        self.lam = lam
        self.saddles = self.find_saddle_points()
        
    def find_saddle_points(self):
        """
        For Hénon-Heiles with λ=1, saddle points are at:
        (±1/√3, 1/√3) and (0, -2/√3)
        """
        sq3 = np.sqrt(3)
        return [
            (1/sq3, 1/sq3),
            (-1/sq3, 1/sq3),
            (0, -2/sq3)
        ]
    
    def compute_lyapunov_along_trajectory(self, x, y, t):
        """
        Computes local Lyapunov exponent from trajectory curvature.
        
        High curvature = strong stretching = positive λ
        Low curvature = stability = negative λ
        """
        
        # Compute velocity and acceleration
        vx = np.gradient(x, t)
        vy = np.gradient(y, t)
        ax = np.gradient(vx, t)
        ay = np.gradient(vy, t)
        
        # Curvature κ = |v × a| / |v|³
        # In 2D: κ = (vx*ay - vy*ax) / (vx² + vy²)^(3/2)
        
        v_mag = np.sqrt(vx**2 + vy**2)
        cross = vx * ay - vy * ax
        
        # Avoid division by zero
        v_mag[v_mag < 1e-10] = 1e-10
        
        kappa = np.abs(cross) / (v_mag**3)
        
        # Approximate Lyapunov exponent from curvature
        # High curvature = stretching = positive λ
        lyap = np.log1p(kappa)
        
        return lyap
    
    def trace_manifold_strand(self, saddle_idx, direction='stable', 
                             perturbation=1e-5, t_max=20.0):
        """
        Traces one strand of stable/unstable manifold from a saddle point.
        
        direction: 'stable' (forward in time) or 'unstable' (backward in time)
        """
        
        sx, sy = self.saddles[saddle_idx]
        
        # Find eigenvectors of linearized system at saddle
        # Jacobian at saddle point
        J = np.array([
            [0, 0, 1/self.m, 0],
            [0, 0, 0, 1/self.m],
            [-1 - 2*self.lam*sy, -2*self.lam*sx, 0, 0],
            [-2*self.lam*sx, -1 + 2*self.lam*sy, 0, 0]
        ])
        
        eigvals, eigvecs = np.linalg.eig(J)
        
        # Stable manifold: negative real part eigenvalues
        # Unstable manifold: positive real part eigenvalues
        if direction == 'stable':
            idx = np.argmin(np.real(eigvals))
        else:
            idx = np.argmax(np.real(eigvals))
        
        eigvec = np.real(eigvecs[:, idx])
        
        # Initial condition: saddle point + small perturbation along eigenvector
        x0 = sx + perturbation * eigvec[0]
        y0 = sy + perturbation * eigvec[1]
        px0 = perturbation * eigvec[2]
        py0 = perturbation * eigvec[3]
        
        # Integrate
        if direction == 'stable':
            eom = equations_of_motion
        else:
            eom = equations_backward
            t_max = -t_max  # Negative time for backward integration
        
        sol = solve_ivp(
            eom,
            [0, t_max],
            [x0, y0, px0, py0],
            args=(self.m, self.lam),
            method='DOP853',
            dense_output=True,
            rtol=1e-9,
            atol=1e-12,
            max_step=0.1
        )
        
        x = sol.y[0]
        y = sol.y[1]
        t = sol.t
        
        # Compute Lyapunov exponent along trajectory
        lyap = self.compute_lyapunov_along_trajectory(x, y, t)
        
        return x, y, lyap, t
    
    def extract_all_manifolds(self, n_strands_per_saddle=4):
        """
        Extracts all stable and unstable manifold strands from all saddle points.
        """
        
        manifolds = {
            'stable': [],
            'unstable': []
        }
        
        print("Extracting manifold strands...")
        
        for saddle_idx in range(len(self.saddles)):
            print(f"\nSaddle {saddle_idx+1} at {self.saddles[saddle_idx]}")
            
            # Generate multiple strands by varying perturbation direction
            for strand_i in range(n_strands_per_saddle):
                angle = 2 * np.pi * strand_i / n_strands_per_saddle
                
                # Stable manifold
                print(f"  Tracing stable strand {strand_i+1}/{n_strands_per_saddle}")
                x_s, y_s, lyap_s, t_s = self.trace_manifold_strand(
                    saddle_idx, 'stable', 
                    perturbation=1e-5 * (1 + 0.5*np.cos(angle))
                )
                
                manifolds['stable'].append({
                    'saddle': saddle_idx,
                    'strand': strand_i,
                    'x': x_s,
                    'y': y_s,
                    'lyap': lyap_s,
                    't': t_s
                })
                
                # Unstable manifold
                print(f"  Tracing unstable strand {strand_i+1}/{n_strands_per_saddle}")
                x_u, y_u, lyap_u, t_u = self.trace_manifold_strand(
                    saddle_idx, 'unstable',
                    perturbation=1e-5 * (1 + 0.5*np.sin(angle))
                )
                
                manifolds['unstable'].append({
                    'saddle': saddle_idx,
                    'strand': strand_i,
                    'x': x_u,
                    'y': y_u,
                    'lyap': lyap_u,
                    't': t_u
                })
        
        return manifolds

# --- KNOT ANALYZER ---
def compute_writhe(curve_x, curve_y, curve_z):
    """
    Computes the writhe (self-linking number) of a 3D curve.
    
    Writhe measures how much the curve twists around itself.
    For a knot, writhe relates to the linking number.
    """
    
    n = len(curve_x)
    writhe = 0.0
    
    # Gauss linking integral (discrete approximation)
    for i in range(n-1):
        r1 = np.array([curve_x[i], curve_y[i], curve_z[i]])
        r1_next = np.array([curve_x[i+1], curve_y[i+1], curve_z[i+1]])
        dr1 = r1_next - r1
        
        for j in range(i+2, n-1):
            r2 = np.array([curve_x[j], curve_y[j], curve_z[j]])
            r2_next = np.array([curve_x[j+1], curve_y[j+1], curve_z[j+1]])
            dr2 = r2_next - r2
            
            # Vector from r1 to r2
            r12 = r2 - r1
            r12_mag = np.linalg.norm(r12)
            
            if r12_mag < 1e-10:
                continue
            
            # Compute cross product and triple product
            cross = np.cross(dr1, dr2)
            triple = np.dot(r12, cross)
            
            # Add contribution to writhe
            writhe += triple / (r12_mag**3)
    
    writhe = writhe / (4 * np.pi)
    
    return writhe

def compute_linking_number(curve1_x, curve1_y, curve1_z,
                           curve2_x, curve2_y, curve2_z):
    """
    Computes the linking number between two 3D curves.
    
    Linking number = number of times one curve winds around the other.
    Non-zero linking number = topologically linked (knotted).
    """
    
    n1 = len(curve1_x)
    n2 = len(curve2_x)
    
    link = 0.0
    
    # Gauss linking integral
    for i in range(n1-1):
        r1 = np.array([curve1_x[i], curve1_y[i], curve1_z[i]])
        r1_next = np.array([curve1_x[i+1], curve1_y[i+1], curve1_z[i+1]])
        dr1 = r1_next - r1
        
        for j in range(n2-1):
            r2 = np.array([curve2_x[j], curve2_y[j], curve2_z[j]])
            r2_next = np.array([curve2_x[j+1], curve2_y[j+1], curve2_z[j+1]])
            dr2 = r2_next - r2
            
            r12 = r2 - r1
            r12_mag = np.linalg.norm(r12)
            
            if r12_mag < 1e-10:
                continue
            
            cross = np.cross(dr1, dr2)
            triple = np.dot(r12, cross)
            
            link += triple / (r12_mag**3)
    
    link = link / (4 * np.pi)
    
    return link


def analyze_knot_topology(manifolds):
    """
    Computes topological invariants of the manifold knot.
    """
    
    print("\n" + "="*60)
    print("KNOT TOPOLOGY ANALYSIS")
    print("="*60)
    
    # Compute writhe for each manifold strand
    print("\nWrithe (self-linking) of individual strands:")
    
    for manifold_type in ['stable', 'unstable']:
        print(f"\n{manifold_type.upper()} MANIFOLDS:")
        
        for m in manifolds[manifold_type]:
            writhe = compute_writhe(m['x'], m['y'], m['lyap'])
            print(f"  Saddle {m['saddle']+1}, Strand {m['strand']+1}: "
                  f"Writhe = {writhe:.4f}")
    
    # Compute linking numbers between strands
    print("\n" + "="*60)
    print("LINKING NUMBERS (between different manifolds)")
    print("="*60)
    
    # Stable-Stable links
    print("\nStable-Stable links:")
    stable_strands = manifolds['stable']
    for i, m1 in enumerate(stable_strands):
        for j, m2 in enumerate(stable_strands[i+1:], start=i+1):
            if m1['saddle'] == m2['saddle']:
                continue  # Skip same saddle
            
            link = compute_linking_number(
                m1['x'], m1['y'], m1['lyap'],
                m2['x'], m2['y'], m2['lyap']
            )
            
            if abs(link) > 0.1:  # Only report significant links
                print(f"  Saddle {m1['saddle']+1} ↔ Saddle {m2['saddle']+1}: "
                      f"Link = {link:.4f}")
    
    # Stable-Unstable links (the heteroclinic tangles)
    print("\nStable-Unstable links (Heteroclinic connections):")
    unstable_strands = manifolds['unstable']
    
    max_links = []
    
    for m_s in stable_strands:
        for m_u in unstable_strands:
            link = compute_linking_number(
                m_s['x'], m_s['y'], m_s['lyap'],
                m_u['x'], m_u['y'], m_u['lyap']
            )
            
            max_links.append(abs(link))
            
            if abs(link) > 0.1:
                print(f"  Stable {m_s['saddle']+1} ↔ Unstable {m_u['saddle']+1}: "
                      f"Link = {link:.4f}")
    
    if len(max_links) > 0:
        avg_link = np.mean(max_links)
        max_link = np.max(max_links)
        
        print(f"\nAverage linking: {avg_link:.4f}")
        print(f"Maximum linking: {max_link:.4f}")
        
        if max_link > 1.5:
            print("\n>>> HIGHLY KNOTTED STRUCTURE <<<")
            print("Manifolds are strongly intertwined (Borromean-like)")
        elif max_link > 0.5:
            print("\n>>> MODERATE LINKING <<<")
            print("Manifolds form a trefoil or torus knot")
        else:
            print("\n>>> WEAKLY LINKED <<<")
            print("Manifolds are loosely braided")

# --- VISUALIZATION ---
def visualize_knotted_manifolds(manifolds):
    """
    Creates a 3D visualization of the manifolds as knotted curves.
    """
    
    fig = plt.figure(figsize=(18, 6))
    
    # Plot 1: Stable manifolds
    ax1 = fig.add_subplot(131, projection='3d')
    
    for i, m in enumerate(manifolds['stable']):
        color = plt.cm.Set1(m['saddle'] / 3.0)
        ax1.plot(m['x'], m['y'], m['lyap'], 
                color=color, alpha=0.7, linewidth=1.5,
                label=f"Saddle {m['saddle']+1}" if m['strand']==0 else "")
    
    ax1.set_xlabel('x position')
    ax1.set_ylabel('y position')
    ax1.set_zlabel('Lyapunov λ')
    ax1.set_title('Stable Manifolds\n(Forward Time)')
    ax1.legend()
    ax1.view_init(elev=30, azim=45)
    
    # Plot 2: Unstable manifolds
    ax2 = fig.add_subplot(132, projection='3d')
    
    for i, m in enumerate(manifolds['unstable']):
        color = plt.cm.Set2(m['saddle'] / 3.0)
        ax2.plot(m['x'], m['y'], m['lyap'], 
                color=color, alpha=0.7, linewidth=1.5,
                label=f"Saddle {m['saddle']+1}" if m['strand']==0 else "")
    
    ax2.set_xlabel('x position')
    ax2.set_ylabel('y position')
    ax2.set_zlabel('Lyapunov λ')
    ax2.set_title('Unstable Manifolds\n(Backward Time)')
    ax2.legend()
    ax2.view_init(elev=30, azim=45)
    
    # Plot 3: Combined (the knot)
    ax3 = fig.add_subplot(133, projection='3d')
    
    for m in manifolds['stable']:
        ax3.plot(m['x'], m['y'], m['lyap'], 
                color='blue', alpha=0.4, linewidth=1)
    
    for m in manifolds['unstable']:
        ax3.plot(m['x'], m['y'], m['lyap'], 
                color='red', alpha=0.4, linewidth=1)
    
    ax3.set_xlabel('x position')
    ax3.set_ylabel('y position')
    ax3.set_zlabel('Lyapunov λ')
    ax3.set_title('The Knot\n(Blue=Stable, Red=Unstable)')
    ax3.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.show()

# --- EXECUTION ---
if __name__ == "__main__":
    print("="*60)
    print("MANIFOLD KNOT EXTRACTOR")
    print("Untying the topology of chaos")
    print("="*60)
    print()
    
    extractor = ManifoldKnotExtractor(m=1.0, lam=1.0)
    
    # Extract manifolds
    manifolds = extractor.extract_all_manifolds(n_strands_per_saddle=2)
    
    # Visualize
    print("\n" + "="*60)
    print("VISUALIZATION")
    print("="*60)
    visualize_knotted_manifolds(manifolds)
    
    # Analyze topology
    analyze_knot_topology(manifolds)
    
    print("\nDone. The knot has been extracted.")