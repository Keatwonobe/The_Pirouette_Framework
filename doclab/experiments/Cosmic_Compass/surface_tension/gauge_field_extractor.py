import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# --- Physics Engine ---
def potential(x, y, lam):
    return 0.5 * (x**2 + y**2) + lam * (x**2 * y - (1/3) * y**3)

def force_field(x, y, lam):
    """Returns the force vector (Fx, Fy) at position (x, y)"""
    Fx = -x - 2 * lam * x * y
    Fy = -y - lam * (x**2 - y**2)
    return Fx, Fy

# --- GAUGE FIELD EXTRACTOR ---
class GaugeFieldAnalyzer:
    """
    Extracts the emergent gauge field structure from the classical dynamics.
    
    Key idea: The Hamiltonian flow generates a velocity field v(x,y).
    The "gauge potential" A is defined such that:
        v = ∇ × A    (in appropriate formulation)
    
    The field strength F = dA is related to the curvature of the flow.
    """
    
    def __init__(self, lam=1.0):
        self.lam = lam
    
    def compute_velocity_field(self, x_range, y_range, resolution=50, E=0.18):
        """
        Computes the velocity field at fixed energy E across a grid.
        
        For each point, we compute the velocity that a particle with
        energy E would have at that point.
        """
        
        xs = np.linspace(*x_range, resolution)
        ys = np.linspace(*y_range, resolution)
        
        X, Y = np.meshgrid(xs, ys)
        
        # At each point, velocity is determined by energy conservation
        # E = ½(vx² + vy²) + V(x,y)
        # So ½|v|² = E - V(x,y)
        
        V = potential(X, Y, self.lam)
        
        # Kinetic energy available
        KE = E - V
        
        # Where KE < 0, region is classically forbidden
        forbidden = KE < 0
        
        # Velocity magnitude
        v_mag = np.sqrt(2 * np.maximum(KE, 0))
        
        # Velocity direction: tangent to equipotential or along force?
        # Actually, velocity direction is given by the equations of motion
        # v = p/m, and p is determined by energy and force direction
        
        # For now, use force direction (this is approximate)
        Fx, Fy = force_field(X, Y, self.lam)
        F_mag = np.sqrt(Fx**2 + Fy**2)
        F_mag[F_mag == 0] = 1.0  # Avoid division by zero
        
        # Velocity in direction of force (motion follows gradients)
        # Actually we want perpendicular for orbital motion
        # Let's use: v points tangent to constant energy surfaces
        
        # Gradient of potential = normal to surface
        # So velocity should be perpendicular to gradient
        grad_Vx = X + 2 * self.lam * X * Y
        grad_Vy = Y + self.lam * (X**2 - Y**2)
        
        # Perpendicular direction (rotate 90 degrees)
        vx = -grad_Vy
        vy = grad_Vx
        
        # Normalize and scale by available kinetic energy
        v_norm = np.sqrt(vx**2 + vy**2)
        v_norm[v_norm == 0] = 1.0
        
        vx = (vx / v_norm) * v_mag
        vy = (vy / v_norm) * v_mag
        
        # Mask forbidden region
        vx[forbidden] = 0
        vy[forbidden] = 0
        
        return X, Y, vx, vy, forbidden
    
    def compute_gauge_potential(self, X, Y, vx, vy):
        """
        Computes gauge potential A such that v ≈ related to curl(A).
        
        In 2D, we can define:
        - A = (Ax, Ay) such that the vorticity ω = ∇×v relates to field strength
        - Or use stream function: ψ such that v = (∂ψ/∂y, -∂ψ/∂x)
        
        We'll compute both.
        """
        
        # Method 1: Stream function (scalar potential for incompressible flow)
        # ∇·v = 0 for Hamiltonian flow (Liouville's theorem in reduced form)
        
        # Check divergence
        div_v = np.gradient(vx, axis=1) + np.gradient(vy, axis=0)
        
        # Method 2: Vector potential (for solenoidal part)
        # In 2D: A = (0, 0, Az) and v = ∇×A = (∂Az/∂y, -∂Az/∂x, 0)
        # So Az is like the stream function
        
        # We'll compute Az by integrating: ∂Az/∂x = -vy, ∂Az/∂y = vx
        # Using cumulative integration (approximate)
        
        dx = X[0, 1] - X[0, 0]
        dy = Y[1, 0] - Y[0, 0]
        
        # Integrate vx in y direction to get Az contribution
        Az_from_vx = np.cumsum(vx * dy, axis=0)
        
        # Integrate -vy in x direction to get Az contribution  
        Az_from_vy = -np.cumsum(vy * dx, axis=1)
        
        # Average the two (they should agree if v is exact curl of A)
        Az = 0.5 * (Az_from_vx + Az_from_vy)
        
        return Az, div_v
    
    def compute_field_strength(self, X, Y, Az):
        """
        Computes field strength tensor F = dA.
        
        In 2D with A = (0, 0, Az):
        F_xy = ∂_x A_y - ∂_y A_x = 0 (since Ax=Ay=0)
        
        The relevant quantity is the "magnetic field":
        B = ∇×A = (∂Az/∂y, -∂Az/∂x, curvature)
        
        The curvature (scalar B field) is:
        B_z = ∂Ay/∂x - ∂Ax/∂y = ∂²Az/∂x² + ∂²Az/∂y² = ∇²Az
        """
        
        # Compute second derivatives (Laplacian)
        dx = X[0, 1] - X[0, 0]
        dy = Y[1, 0] - Y[0, 0]
        
        # Second derivative in x
        d2Az_dx2 = (Az[:, 2:] - 2*Az[:, 1:-1] + Az[:, :-2]) / dx**2
        
        # Second derivative in y
        d2Az_dy2 = (Az[2:, :] - 2*Az[1:-1, :] + Az[:-2, :]) / dy**2
        
        # Laplacian (trim to common size)
        min_i = min(d2Az_dx2.shape[0], d2Az_dy2.shape[0])
        min_j = min(d2Az_dx2.shape[1], d2Az_dy2.shape[1])
        
        Bz = d2Az_dx2[:min_i, :min_j] + d2Az_dy2[:min_i, :min_j]
        
        return Bz
    
    def find_monopole_charges(self, X, Y, Bz, threshold=0.1):
        """
        Looks for localized regions of high field strength - potential
        "magnetic monopoles" or gauge charge density.
        
        In Yang-Mills theory, these would be instantons or magnetic monopoles.
        """
        
        # Find local maxima/minima of |Bz|
        Bz_abs = np.abs(Bz)
        
        # Simple peak finding: point higher than all neighbors
        charges = []
        
        for i in range(1, Bz.shape[0]-1):
            for j in range(1, Bz.shape[1]-1):
                val = Bz_abs[i, j]
                
                if val < threshold:
                    continue
                
                # Check if local maximum
                neighbors = Bz_abs[i-1:i+2, j-1:j+2]
                if val >= np.max(neighbors):
                    charges.append({
                        'x': X[i, j],
                        'y': Y[i, j],
                        'strength': Bz[i, j],
                        'i': i,
                        'j': j
                    })
        
        return charges

# --- VISUALIZATION ---
def plot_gauge_field_structure(analyzer, x_range, y_range, E=0.18, resolution=80):
    """
    Master visualization of the gauge field extraction.
    """
    
    print(f"Computing gauge field at E={E:.4f}...")
    
    X, Y, vx, vy, forbidden = analyzer.compute_velocity_field(
        x_range, y_range, resolution=resolution, E=E
    )
    
    print("Extracting gauge potential...")
    Az, div_v = analyzer.compute_gauge_potential(X, Y, vx, vy)
    
    print("Computing field strength...")
    Bz = analyzer.compute_field_strength(X, Y, Az)
    
    print("Searching for monopole charges...")
    charges = analyzer.find_monopole_charges(X, Y, Bz, threshold=np.max(np.abs(Bz))*0.5)
    
    print(f"Found {len(charges)} charge concentrations")
    
    # Create visualization
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # 1. Velocity field (streamplot)
    ax1 = fig.add_subplot(gs[0, 0])
    
    # Mask forbidden region
    vx_plot = np.ma.masked_where(forbidden, vx)
    vy_plot = np.ma.masked_where(forbidden, vy)
    
    # Plot potential background
    V_plot = potential(X, Y, analyzer.lam)
    ax1.contourf(X, Y, V_plot, levels=20, cmap='gray', alpha=0.3)
    ax1.contour(X, Y, V_plot, levels=[E], colors='yellow', linewidths=3)
    
    # Velocity streamlines
    ax1.streamplot(X, Y, vx_plot, vy_plot, color='blue', density=1.5, 
                  linewidth=1, arrowsize=1.5)
    
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title(f'Velocity Field at E={E:.4f}\n(Yellow = Energy Surface)')
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.2)
    
    # 2. Gauge potential Az
    ax2 = fig.add_subplot(gs[0, 1])
    
    Az_plot = np.ma.masked_where(forbidden, Az)
    im2 = ax2.contourf(X, Y, Az_plot, levels=30, cmap='RdBu_r')
    ax2.contour(X, Y, Az_plot, levels=15, colors='black', linewidths=0.5, alpha=0.3)
    
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_title('Gauge Potential A_z\n(Contours = Gauge Field Lines)')
    ax2.set_aspect('equal')
    plt.colorbar(im2, ax=ax2, label='A_z')
    ax2.grid(True, alpha=0.2)
    
    # 3. Field strength (curvature)
    ax3 = fig.add_subplot(gs[0, 2])
    
    # Trim X, Y to match Bz size
    X_trim = X[1:-1, 1:-1]
    Y_trim = Y[1:-1, 1:-1]
    
    im3 = ax3.contourf(X_trim, Y_trim, Bz, levels=30, cmap='seismic')
    ax3.contour(X_trim, Y_trim, Bz, levels=[0], colors='black', linewidths=2)
    
    # Mark charges
    for charge in charges:
        color = 'red' if charge['strength'] > 0 else 'blue'
        ax3.scatter([charge['x']], [charge['y']], s=200, c=color, 
                   marker='*', edgecolors='black', linewidths=2, zorder=10)
    
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_title(f'Field Strength F = dA (∇²A_z)\n{len(charges)} Charge Centers')
    ax3.set_aspect('equal')
    plt.colorbar(im3, ax=ax3, label='B_z = ∇²A_z')
    ax3.grid(True, alpha=0.2)
    
    # 4. Divergence check (should be ~0 for Hamiltonian flow)
    ax4 = fig.add_subplot(gs[1, 0])
    
    div_plot = np.ma.masked_where(forbidden, div_v)
    im4 = ax4.contourf(X, Y, div_plot, levels=30, cmap='PRGn')
    
    ax4.set_xlabel('x')
    ax4.set_ylabel('y')
    ax4.set_title('Divergence ∇·v\n(Should be ≈0 for Hamiltonian)')
    ax4.set_aspect('equal')
    plt.colorbar(im4, ax=ax4, label='∇·v')
    ax4.grid(True, alpha=0.2)
    
    # 5. Vorticity field
    ax5 = fig.add_subplot(gs[1, 1])
    
    # Compute curl of velocity (vorticity)
    omega = np.gradient(vy, axis=1) - np.gradient(vx, axis=0)
    omega_plot = np.ma.masked_where(forbidden, omega)
    
    im5 = ax5.contourf(X, Y, omega_plot, levels=30, cmap='twilight')
    
    ax5.set_xlabel('x')
    ax5.set_ylabel('y')
    ax5.set_title('Vorticity ω = ∇×v\n(Rotation of flow)')
    ax5.set_aspect('equal')
    plt.colorbar(im5, ax=ax5, label='ω')
    ax5.grid(True, alpha=0.2)
    
    # 6. Charge distribution
    ax6 = fig.add_subplot(gs[1, 2])
    
    if len(charges) > 0:
        charge_strengths = [c['strength'] for c in charges]
        charge_x = [c['x'] for c in charges]
        charge_y = [c['y'] for c in charges]
        
        scatter = ax6.scatter(charge_x, charge_y, s=300, 
                            c=charge_strengths, cmap='seismic',
                            edgecolors='black', linewidths=2,
                            vmin=-np.max(np.abs(charge_strengths)),
                            vmax=np.max(np.abs(charge_strengths)))
        
        plt.colorbar(scatter, ax=ax6, label='Charge Strength')
        
        ax6.set_xlabel('x')
        ax6.set_ylabel('y')
        ax6.set_title('Gauge Charge Distribution\n(Red = +, Blue = -)')
        ax6.set_aspect('equal')
        ax6.grid(True, alpha=0.2)
        
        # Print charge info
        print("\nCharge locations:")
        for i, c in enumerate(charges):
            print(f"  Charge {i+1}: ({c['x']:.3f}, {c['y']:.3f}), Q = {c['strength']:.4f}")
    else:
        ax6.text(0.5, 0.5, 'No charges found', ha='center', va='center', 
                transform=ax6.transAxes, fontsize=16)
        ax6.set_xlim(x_range)
        ax6.set_ylim(y_range)
    
    plt.suptitle(f'Emergent Gauge Field Structure at E={E:.4f}', 
                fontsize=16, fontweight='bold')
    
    plt.show()
    
    return charges

def analyze_charge_quantization(energy_values, x_range, y_range):
    """
    Scans multiple energies to see if charge values are quantized.
    """
    
    print("\n" + "="*60)
    print("SCANNING CHARGE SPECTRUM ACROSS ENERGIES")
    print("="*60)
    
    analyzer = GaugeFieldAnalyzer(lam=1.0)
    
    all_charges = []
    
    for E in energy_values:
        print(f"\nE = {E:.5f}")
        X, Y, vx, vy, forbidden = analyzer.compute_velocity_field(
            x_range, y_range, resolution=60, E=E
        )
        Az, div_v = analyzer.compute_gauge_potential(X, Y, vx, vy)
        Bz = analyzer.compute_field_strength(X, Y, Az)
        charges = analyzer.find_monopole_charges(X, Y, Bz, 
                                                threshold=np.max(np.abs(Bz))*0.4)
        
        for c in charges:
            c['energy'] = E
            all_charges.append(c)
        
        print(f"  Found {len(charges)} charges")
    
    if len(all_charges) == 0:
        print("\nNo charges found across energy range.")
        return
    
    # Plot charge strength distribution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    strengths = [c['strength'] for c in all_charges]
    energies = [c['energy'] for c in all_charges]
    
    # Histogram of charge strengths
    ax1.hist(strengths, bins=30, edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Charge Strength')
    ax1.set_ylabel('Count')
    ax1.set_title('Charge Distribution Across All Energies\n(Quantization?)')
    ax1.grid(True, alpha=0.3)
    
    # Charge vs Energy
    ax2.scatter(energies, strengths, alpha=0.6, s=50, edgecolors='black')
    ax2.set_xlabel('Energy E')
    ax2.set_ylabel('Charge Strength')
    ax2.set_title('Charge Dependence on Energy\n(Bands = Quantization?)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# --- EXECUTION ---
if __name__ == "__main__":
    print("="*60)
    print("GAUGE FIELD EXTRACTOR")
    print("Revealing the Yang-Mills structure in Hamiltonian chaos")
    print("="*60)
    print()
    
    analyzer = GaugeFieldAnalyzer(lam=1.0)
    
    # Analyze at energy just above saddle
    E_saddle = 1.0 / 6.0
    E_test = E_saddle + 0.01
    
    x_range = [-1.5, 1.5]
    y_range = [-1.5, 1.5]
    
    charges = plot_gauge_field_structure(analyzer, x_range, y_range, 
                                        E=E_test, resolution=100)
    
    # Scan multiple energies for charge quantization
    print("\n" + "="*60)
    print("MULTI-ENERGY SCAN")
    print("="*60)
    
    E_scan = np.linspace(E_saddle + 0.005, E_saddle + 0.03, 8)
    analyze_charge_quantization(E_scan, x_range, y_range)
    
    print("\nDone. If charges are quantized and localized, you've found gauge bosons.")