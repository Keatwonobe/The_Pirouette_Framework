import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time

class PirouetteLattice:
    def __init__(self, L=16, m_sq=0.1, lambda_4=1.0):
        """
        Initialize the 4D lattice for the Delta field.
        Paper Ref: Appendix A.1 [cite: 607-610]
        L: Lattice size (L^4)
        m_sq: Mass squared parameter (m_Delta^2)
        lambda_4: Quartic coupling
        """
        self.L = L
        self.m_sq = m_sq
        self.lambda_4 = lambda_4
        
        # Initialize field with cold start (all zeros) or hot start (random)
        # Using small random noise to break symmetry
        self.phi = np.random.normal(0, 0.1, (L, L, L, L))
        
        # Pre-calculate checkerboard masks for vectorized updates
        self.mask_even = self._make_checkerboard(0)
        self.mask_odd = self._make_checkerboard(1)

    def _make_checkerboard(self, offset):
        """Creates a boolean mask for checkerboard updates."""
        coords = np.indices(self.phi.shape)
        return (np.sum(coords, axis=0) % 2) == offset

    def action_local(self, phi_val, neighbors_sum):
        """
        Calculate the local action at a site.
        Paper Ref: Eq 79 [cite: 609]
        S = 0.5 * (d_mu phi)^2 + 0.5 * m^2 * phi^2 + (lambda/24) * phi^4
        
        On the lattice, the kinetic term sum(phi_{x+mu} - phi_x)^2 expands.
        We only care about the parts depending on phi_x for the update delta.
        """
        # Kinetic part contribution: -phi_x * sum(neighbors) + 4*phi_x^2 (in 4D usually 8 neighbors? 
        # Actually in 4D Euclidean, coordination number is 8 (2*D).
        # We assume unit lattice spacing a=1.
        
        kinetic = -phi_val * neighbors_sum + 4.0 * (phi_val**2) # Simplified effective local part
        potential = 0.5 * self.m_sq * (phi_val**2) + (self.lambda_4 / 24.0) * (phi_val**4)
        return kinetic + potential

    def update(self, steps=1):
        """
        Metropolis-Hastings update step (Vectorized).
        Paper Ref: Appendix A.2 [cite: 613]
        """
        for _ in range(steps):
            for mask in [self.mask_even, self.mask_odd]:
                # Get current values
                phi_old = self.phi[mask]
                
                # Calculate sum of neighbors (Periodic Boundary Conditions)
                # Roll array in all 4 directions (+/-) for all 4 dimensions
                neighbors = np.zeros_like(self.phi)
                for d in range(4):
                    neighbors += np.roll(self.phi, 1, axis=d) + np.roll(self.phi, -1, axis=d)
                
                neigh_sum = neighbors[mask]
                
                # Propose new values (Gaussian step)
                delta = np.random.normal(0, 0.5, size=phi_old.shape)
                phi_new = phi_old + delta
                
                # Calculate change in action
                # Note: We implement a simplified change check for speed
                # dS = S_new - S_old
                # Standard Kinetic term on lattice: 0.5 * sum((phi_x - phi_y)^2)
                # Change at x depends on: 0.5 * sum_mu [ (phi'_x - phi_{x+mu})^2 - (phi_x - phi_{x+mu})^2 + ... ]
                # This effectively simplifies to dS = (phi'_x - phi_x) * (4*D*phi_x - sum_neighbors) + ...
                # Let's use the exact local action difference for accuracy:
                
                # Kinetic difference:
                # The term sum(phi_x - phi_neigh)^2 expands to phi_x^2 - 2*phi_x*phi_neigh + ...
                # D = 4 dimensions -> 8 neighbors
                # dS_kin = 4.0 * (phi_new**2 - phi_old**2) - (phi_new - phi_old) * neigh_sum
                
                dS_kin = 4.0 * (phi_new**2 - phi_old**2) - (phi_new - phi_old) * neigh_sum
                dS_mass = 0.5 * self.m_sq * (phi_new**2 - phi_old**2)
                dS_int = (self.lambda_4 / 24.0) * (phi_new**4 - phi_old**4)
                
                dS = dS_kin + dS_mass + dS_int
                
                # Metropolis Accept/Reject
                # If dS < 0 accept. If dS > 0 accept with exp(-dS)
                prob = np.exp(-dS)
                accept_mask = (np.random.rand(*dS.shape) < prob)
                
                # Update grid
                self.phi[mask] = np.where(accept_mask, phi_new, phi_old)

    def measure_correlation(self):
        """
        Measure two-point correlation C(r) along the x-axis.
        Paper Ref: Eq 81 [cite: 620]
        """
        # Average over y, z, t and all x-starts
        corrs = []
        # Center the field (subtract mean)
        phi_centered = self.phi - np.mean(self.phi)
        
        # Use FFT for fast correlation or simple spatial average
        # We'll use simple spatial average along axis 0 (x)
        for r in range(self.L // 2):
            c_r = np.mean(phi_centered * np.roll(phi_centered, -r, axis=0))
            corrs.append(c_r)
        
        # Normalize
        if corrs[0] != 0:
            corrs = np.array(corrs) / corrs[0]
        return corrs

def fit_stiffness(corrs):
    """Fit C(r) ~ A * exp(-r/xi) to extract stiffness xi."""
    r_vals = np.arange(len(corrs))
    
    def exponential_decay(r, xi, A):
        return A * np.exp(-r / xi)
    
    try:
        # Initial guess: xi = 2.0, A = 1.0
        popt, _ = curve_fit(exponential_decay, r_vals, corrs, p0=[2.0, 1.0], bounds=(0, [100, 10]))
        return popt[0] # Returns xi
    except:
        return 0.0

# --- The "Bigger Scan" Manager ---

def run_pirouette_scan(grid_size=5):
    """
    Scans the (m^2, lambda) phase space.
    Paper Ref: 4.2 Lattice Extraction [cite: 216]
    """
    print(f"--- Starting Pirouette Stiffness Scan ({grid_size}x{grid_size}) ---")
    print("Mapping stiffness xi over parameter space...")
    
    # Define parameter ranges (Paper implies searching for solitonic phase)
    # We scan m^2 from negative (broken symmetry) to positive
    m_sq_range = np.linspace(-1.0, 0.5, grid_size)
    lambda_range = np.linspace(0.1, 5.0, grid_size)
    
    results = np.zeros((grid_size, grid_size))
    
    for i, m in enumerate(m_sq_range):
        for j, lam in enumerate(lambda_range):
            print(f"  > Simulating: m^2={m:.2f}, lambda={lam:.2f}...", end="")
            
            # Setup Lattice
            # Paper uses L=16. Reduced here to L=8 for demo speed.
            # Change L=16 for "Bigger Scan" accuracy.
            lat = PirouetteLattice(L=8, m_sq=m, lambda_4=lam) 
            
            # Thermalize 
            lat.update(steps=200) 
            
            # Measure
            xi_samples = []
            for _ in range(10): # 10 Measurements
                lat.update(steps=10) # Decorrelation steps
                c_r = lat.measure_correlation()
                xi = fit_stiffness(c_r)
                xi_samples.append(xi)
            
            avg_xi = np.mean(xi_samples)
            results[i, j] = avg_xi
            print(f" Stiffness xi = {avg_xi:.4f}")
            
    return m_sq_range, lambda_range, results

# --- Execution ---

if __name__ == "__main__":
    # Run the scan
    ms, ls, stiffness_map = run_pirouette_scan(grid_size=6)

    # Visualization
    plt.figure(figsize=(8, 6))
    plt.imshow(stiffness_map, origin='lower', extent=[ls.min(), ls.max(), ms.min(), ms.max()], aspect='auto', cmap='viridis')
    plt.colorbar(label='Stiffness (Correlation Length) $\\xi$')
    plt.xlabel('Coupling $\\lambda_4$')
    plt.ylabel('Mass Squared $m_\\Delta^2$')
    plt.title('Pirouette Field Stiffness Map')
    plt.show()

    # Data Dump for analysis
    print("\nScan Complete.")
    print("Use this map to find regions where ratios match 1 : 22 : 23")