import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Arc
from matplotlib.path import Path
import matplotlib.patches as mpatches

# --- BRAID DIAGRAM GENERATOR ---
class BraidDiagramGenerator:
    """
    Converts the knotted manifold structure into a braid diagram.
    
    A braid diagram shows how strands cross over/under each other,
    revealing the twist structure and allowing classification of the knot type.
    """
    
    def __init__(self):
        self.crossings = []
        
    def detect_crossings(self, strands_3d, projection_axis='z'):
        """
        Projects 3D curves onto 2D and finds all crossing points.
        
        A crossing occurs when two projected curves intersect.
        The over/under relationship is determined by the unprojected coordinate.
        """
        
        crossings = []
        
        n_strands = len(strands_3d)
        
        print(f"Detecting crossings between {n_strands} strands...")
        
        for i in range(n_strands):
            for j in range(i+1, n_strands):
                strand_i = strands_3d[i]
                strand_j = strands_3d[j]
                
                # Project onto xy plane (ignore z for now)
                xi, yi, zi = strand_i['x'], strand_i['y'], strand_i['lyap']
                xj, yj, zj = strand_j['x'], strand_j['y'], strand_j['lyap']
                
                # Find intersections in the projected plane
                # This is approximate - we check pairwise segment intersections
                
                for k in range(len(xi)-1):
                    for l in range(len(xj)-1):
                        # Line segment 1: (xi[k], yi[k]) to (xi[k+1], yi[k+1])
                        # Line segment 2: (xj[l], yj[l]) to (xj[l+1], yj[l+1])
                        
                        cross_point = self._segment_intersection(
                            xi[k], yi[k], xi[k+1], yi[k+1],
                            xj[l], yj[l], xj[l+1], yj[l+1]
                        )
                        
                        if cross_point is not None:
                            cx, cy = cross_point
                            
                            # Determine over/under by comparing z values
                            # Interpolate z at the crossing point
                            t_i = self._interpolate_parameter(xi[k], yi[k], xi[k+1], yi[k+1], cx, cy)
                            t_j = self._interpolate_parameter(xj[l], yj[l], xj[l+1], yj[l+1], cx, cy)
                            
                            zi_cross = zi[k] + t_i * (zi[k+1] - zi[k])
                            zj_cross = zj[l] + t_j * (zj[l+1] - zj[l])
                            
                            # Record crossing
                            over_strand = i if zi_cross > zj_cross else j
                            under_strand = j if zi_cross > zj_cross else i
                            
                            crossings.append({
                                'x': cx,
                                'y': cy,
                                'over': over_strand,
                                'under': under_strand,
                                'over_z': max(zi_cross, zj_cross),
                                'under_z': min(zi_cross, zj_cross)
                            })
        
        print(f"Found {len(crossings)} crossings")
        
        self.crossings = crossings
        return crossings
    
    def _segment_intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        Finds intersection point of two line segments, if it exists.
        Returns (x, y) or None.
        """
        
        # Parametric form: P = P1 + t*(P2-P1), Q = P3 + s*(P4-P3)
        # Solve for t and s
        
        denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        
        if abs(denom) < 1e-10:
            return None  # Parallel
        
        t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / denom
        s = ((x1-x3)*(y1-y2) - (y1-y3)*(x1-x2)) / denom
        
        if 0 <= t <= 1 and 0 <= s <= 1:
            # Intersection exists
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
        else:
            return None
    
    def _interpolate_parameter(self, x1, y1, x2, y2, x, y):
        """
        Given a point (x,y) on segment from (x1,y1) to (x2,y2),
        find the parameter t such that (x,y) = (x1,y1) + t*((x2,y2)-(x1,y1))
        """
        
        dx = x2 - x1
        dy = y2 - y1
        
        if abs(dx) > abs(dy):
            t = (x - x1) / dx if dx != 0 else 0
        else:
            t = (y - y1) / dy if dy != 0 else 0
        
        return np.clip(t, 0, 1)
    
    def compute_braid_word(self, strands_3d):
        """
        Computes the braid word - a symbolic representation of the knot.
        
        Example: "σ1 σ2⁻¹ σ1" means:
        - Cross strand 1 over strand 2
        - Cross strand 2 under strand 3
        - Cross strand 1 over strand 2
        """
        
        # First detect all crossings
        crossings = self.detect_crossings(strands_3d)
        
        if len(crossings) == 0:
            return []
        
        # Sort crossings by some parameter (e.g., y-coordinate for horizontal braids)
        # This gives us the order in which crossings occur along the braid
        crossings_sorted = sorted(crossings, key=lambda c: c['y'])
        
        braid_word = []
        
        for cross in crossings_sorted:
            # Braid group generators: σ_i is a crossing between strand i and i+1
            # Positive = right crossing, Negative = left crossing
            
            i = min(cross['over'], cross['under'])
            j = max(cross['over'], cross['under'])
            
            # Determine chirality (positive or negative crossing)
            sign = 1 if cross['over'] < cross['under'] else -1
            
            braid_word.append({
                'generator': i,
                'sign': sign,
                'position': cross['y']
            })
        
        return braid_word
    
    def visualize_braid_diagram(self, strands_3d, show_lyapunov=False):
        """
        Draws a classical braid diagram showing all crossings.
        """
        
        crossings = self.detect_crossings(strands_3d)
        
        if len(crossings) == 0:
            print("No crossings found. Cannot draw braid diagram.")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # Plot 1: Projected curves with crossing markers
        ax1.set_aspect('equal')
        ax1.set_title('Projected Manifolds with Crossings', fontsize=14, fontweight='bold')
        ax1.set_xlabel('x position')
        ax1.set_ylabel('y position')
        
        # Draw all strands
        colors = plt.cm.tab10(np.linspace(0, 1, len(strands_3d)))
        
        for i, strand in enumerate(strands_3d):
            ax1.plot(strand['x'], strand['y'], color=colors[i], 
                    alpha=0.7, linewidth=2, label=f"Strand {i+1}")
        
        # Mark crossings with circles
        for cross in crossings:
            ax1.plot(cross['x'], cross['y'], 'ko', markersize=8, zorder=10)
            
            # Add over/under label
            label = f"{cross['over']+1}/{cross['under']+1}"
            ax1.text(cross['x'], cross['y'], label, fontsize=8, 
                    ha='center', va='center', color='white', 
                    bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
        
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Schematic braid diagram
        ax2.set_title('Braid Diagram (Schematic)', fontsize=14, fontweight='bold')
        ax2.set_xlim(-1, len(strands_3d) + 1)
        ax2.set_ylim(-1, len(crossings) + 2)
        ax2.set_xlabel('Strand Index')
        ax2.set_ylabel('Crossing Level')
        ax2.set_aspect('equal')
        
        # Draw vertical strand lines
        for i in range(len(strands_3d)):
            ax2.plot([i, i], [-1, len(crossings) + 1], 'k-', linewidth=2, alpha=0.3)
        
        # Sort crossings by y-coordinate (vertical position in braid)
        crossings_sorted = sorted(crossings, key=lambda c: c['y'])
        
        # Draw each crossing
        for level, cross in enumerate(crossings_sorted):
            over = cross['over']
            under = cross['under']
            
            # Draw crossing
            self._draw_crossing(ax2, over, under, level, positive=(over < under))
        
        # Label strands at top and bottom
        for i in range(len(strands_3d)):
            ax2.text(i, len(crossings) + 1.5, f"S{i+1}", ha='center', fontsize=12, fontweight='bold')
            ax2.text(i, -0.5, f"S{i+1}", ha='center', fontsize=12, fontweight='bold')
        
        ax2.grid(False)
        ax2.set_xticks([])
        ax2.set_yticks([])
        
        plt.tight_layout()
        plt.show()
        
        # Compute braid word
        braid_word = self.compute_braid_word(strands_3d)
        
        print("\n" + "="*60)
        print("BRAID WORD")
        print("="*60)
        
        if len(braid_word) > 0:
            word_str = ""
            for b in braid_word:
                sign_str = "" if b['sign'] > 0 else "⁻¹"
                word_str += f"σ{b['generator']+1}{sign_str} "
            
            print(f"\nBraid: {word_str}")
            print(f"\nThis knot has {len(braid_word)} crossings")
            
            # Count positive and negative crossings
            n_pos = sum(1 for b in braid_word if b['sign'] > 0)
            n_neg = sum(1 for b in braid_word if b['sign'] < 0)
            
            print(f"  Positive crossings: {n_pos}")
            print(f"  Negative crossings: {n_neg}")
            print(f"  Writhe: {n_pos - n_neg}")
    
    def _draw_crossing(self, ax, i, j, level, positive=True):
        """
        Draws a single crossing in the braid diagram.
        """
        
        # Crossing is between strands i and j at vertical level 'level'
        y = level
        
        # Over strand (continuous)
        if positive:
            # i goes over j
            ax.plot([i, j], [y-0.3, y+0.3], 'b-', linewidth=3, solid_capstyle='round')
            # Under strand (broken)
            ax.plot([j, i+0.3*(j-i)], [y-0.3, y-0.1], 'r-', linewidth=3, solid_capstyle='round')
            ax.plot([i+0.7*(j-i), j], [y+0.1, y+0.3], 'r-', linewidth=3, solid_capstyle='round')
        else:
            # j goes over i
            ax.plot([j, i], [y-0.3, y+0.3], 'b-', linewidth=3, solid_capstyle='round')
            # Under strand (broken)
            ax.plot([i, j-0.3*(j-i)], [y-0.3, y-0.1], 'r-', linewidth=3, solid_capstyle='round')
            ax.plot([j-0.7*(j-i), i], [y+0.1, y+0.3], 'r-', linewidth=3, solid_capstyle='round')

# --- LOAD MANIFOLD DATA ---
def load_manifolds_from_simulation():
    """
    Quick simulation to generate manifold data for visualization.
    This is a simplified version - in practice you'd load from the knot_extractor.py output.
    """
    
    from scipy.integrate import solve_ivp
    
    def potential(x, y, lam):
        return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1/3) * y**3)
    
    def equations_of_motion(t, state, m, lam):
        x, y, px, py = state
        Fx = -x - 2 * lam * x * y
        Fy = -y - lam * (x**2 - y**2)
        return [px / m, py / m, Fx, Fy]
    
    # Generate a few test trajectories around the three basins
    strands = []
    
    # Initial conditions near the three saddle points
    init_conditions = [
        (0.5, 0.5, 0.01, 0.01),
        (-0.5, 0.5, -0.01, 0.01),
        (0.0, -0.8, 0.0, -0.01)
    ]
    
    for ic in init_conditions:
        sol = solve_ivp(
            equations_of_motion,
            [0, 15.0],
            ic,
            args=(1.0, 1.0),
            method='DOP853',
            dense_output=True,
            rtol=1e-8,
            max_step=0.1
        )
        
        x = sol.y[0]
        y = sol.y[1]
        
        # Compute Lyapunov from curvature
        vx = np.gradient(x, sol.t)
        vy = np.gradient(y, sol.t)
        ax = np.gradient(vx, sol.t)
        ay = np.gradient(vy, sol.t)
        
        v_mag = np.sqrt(vx**2 + vy**2)
        v_mag[v_mag < 1e-10] = 1e-10
        
        cross = vx * ay - vy * ax
        kappa = np.abs(cross) / (v_mag**3)
        lyap = np.log1p(kappa)
        
        strands.append({
            'x': x,
            'y': y,
            'lyap': lyap,
            't': sol.t
        })
    
    return strands

# --- EXECUTION ---
if __name__ == "__main__":
    print("="*60)
    print("BRAID DIAGRAM GENERATOR")
    print("Visualizing the twist structure of the manifold knot")
    print("="*60)
    print()
    
    # Generate or load manifold data
    print("Generating test manifold data...")
    strands = load_manifolds_from_simulation()
    
    # Create braid diagram
    generator = BraidDiagramGenerator()
    
    print("\nGenerating braid diagram...")
    generator.visualize_braid_diagram(strands)
    
    print("\nDone. The braid has been diagrammed.")
    print("\nTo use with full manifold data:")
    print("1. Run knot_extractor.py first")
    print("2. Pass manifolds['stable'] or manifolds['unstable'] to this script")