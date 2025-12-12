import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
import pickle
import os
import signal
import sys
import gc

# --- CONFIGURATION (Based on Appendix A) ---
#  L=16 is the standard for the paper's results.
LATTICE_SIZE = 16 
#  Thermalization sweeps. Paper says 10^4. 
# WARNING: 10,000 takes a long time. Set to 1000 for a "Quick Scientific" run, 10000 for "Publication".
N_THERM = 1000  
#  Measurements. Paper says 100-1000.
N_MEAS = 100
# Decorrelation steps between measurements
N_DECORR = 10
# Grid resolution (Paper uses 25x25)
GRID_RES = 25
# Checkpoint filename
CHECKPOINT_FILE = "pirouette_checkpoint.pkl"

class PirouetteLattice:
    def __init__(self, L, m_sq, lambda_4):
        self.L = L
        self.m_sq = m_sq
        self.lambda_4 = lambda_4
        # CHANGE: Add .astype(np.float32)
        self.phi = np.random.normal(0, 0.5, (L, L, L, L)).astype(np.float32) 
        self.mask_even = self._make_checkerboard(0)
        self.mask_odd = self._make_checkerboard(1)

    def _make_checkerboard(self, offset):
        coords = np.indices(self.phi.shape)
        return (np.sum(coords, axis=0) % 2) == offset

    def update(self, steps=1):
        """Vectorized Metropolis-Hastings Update (Optimized)"""
        for _ in range(steps):
            for mask in [self.mask_even, self.mask_odd]:
                phi_old = self.phi[mask]
                
                # Optimized Neighbor Sum using in-place operations where possible
                # This prevents creating 8 full-size copies of the lattice
                neigh_sum = np.zeros_like(phi_old)
                for d in range(4):
                    neigh_sum += self.phi[np.roll(mask, 1, axis=d)] # Look forward
                    neigh_sum += self.phi[np.roll(mask, -1, axis=d)] # Look backward
                
                # Propose update
                # Reduce variance slightly for better acceptance in 4D
                delta = np.random.normal(0, 0.4, size=phi_old.shape).astype(np.float32)
                phi_new = phi_old + delta
                
                # Euclidean Action Change
                dS_kin = 4.0 * (phi_new**2 - phi_old**2) - (phi_new - phi_old) * neigh_sum
                dS_mass = 0.5 * self.m_sq * (phi_new**2 - phi_old**2)
                dS_int = (self.lambda_4 / 24.0) * (phi_new**4 - phi_old**4)
                
                dS = dS_kin + dS_mass + dS_int
                
                # Metropolis
                prob = np.exp(-dS)
                accept_mask = (np.random.rand(*dS.shape) < prob)
                self.phi[mask] = np.where(accept_mask, phi_new, phi_old)

    def measure_correlation_stiffness(self):
        """Extracts correlation length xi from the lattice."""
        # 1. Calculate C(r) averaged over spatial directions
        phi_bar = self.phi - np.mean(self.phi)
        corrs = []
        max_r = self.L // 2
        
        # Average correlation along 4 axes
        for r in range(max_r):
            c_sum = 0
            for d in range(4):
                c_sum += np.mean(phi_bar * np.roll(phi_bar, -r, axis=d))
            corrs.append(c_sum / 4.0)
            
        corrs = np.array(corrs)
        if corrs[0] != 0: corrs /= corrs[0] # Normalize
        
        # 2. Fit Exponential: C(r) ~ A * exp(-r/xi)
        def model(r, xi, A):
            return A * np.exp(-r / xi)
        
        try:
            # Bounds: xi must be positive, A usually close to 1
            popt, _ = curve_fit(model, np.arange(max_r), corrs, 
                                p0=[1.0, 1.0], bounds=([0.01, 0], [self.L, 5.0]))
            return popt[0] # Return xi
        except:
            return 0.0

class SimulationManager:
    def __init__(self):
        self.m_range = np.linspace(-1.2, 0.0, GRID_RES) # Focus on broken phase
        self.l_range = np.linspace(1.0, 5.0, GRID_RES)
        self.results = np.zeros((GRID_RES, GRID_RES))
        self.completed_indices = set()
        self.start_time = time.time()
        self.total_points = GRID_RES * GRID_RES

    def load_checkpoint(self):
        if os.path.exists(CHECKPOINT_FILE):
            print(f"[System] Found checkpoint: {CHECKPOINT_FILE}")
            try:
                with open(CHECKPOINT_FILE, 'rb') as f:
                    data = pickle.load(f)
                    self.results = data['results']
                    self.completed_indices = data['completed']
                    # Restore params if you want, but we assume ranges are const
                print(f"[System] Resuming. {len(self.completed_indices)}/{self.total_points} points already calculated.")
            except Exception as e:
                print(f"[Error] Corrupt checkpoint: {e}. Starting fresh.")

    def save_checkpoint(self):
        with open(CHECKPOINT_FILE, 'wb') as f:
            pickle.dump({
                'results': self.results,
                'completed': self.completed_indices
            }, f)
        print(f"\n[System] Progress saved to {CHECKPOINT_FILE}")

    def run(self):
        print(f"--- PIROUETTE FIELD VALIDATION (L={LATTICE_SIZE}^4) ---")
        print(f"Parameters: Therm={N_THERM}, Meas={N_MEAS}, Grid={GRID_RES}x{GRID_RES}")
        
        try:
            for i, m_sq in enumerate(self.m_range):
                for j, lam in enumerate(self.l_range):
                    time.sleep(0.05) # Sleep 50ms between points to cool CPU
                    idx = (i, j)
                    if idx in self.completed_indices:
                        continue
                        
                    # --- THE PHYSICS ENGINE ---
                    lat = PirouetteLattice(L=LATTICE_SIZE, m_sq=m_sq, lambda_4=lam)
                    
                    # Thermalization (The heavy lifting)
                    # We break this loop to handle Ctrl+C gracefully if needed
                    lat.update(N_THERM)
                    
                    # Measurement Loop
                    xi_vals = []
                    for _ in range(N_MEAS):
                        lat.update(N_DECORR)
                        xi = lat.measure_correlation_stiffness()
                        if not np.isnan(xi) and xi > 0:
                            xi_vals.append(xi)
                    
                    # Store Result
                    if xi_vals:
                        avg_xi = np.mean(xi_vals)
                        self.results[i, j] = avg_xi
                    else:
                        self.results[i, j] = 0.0
                    
                    self.completed_indices.add(idx)
                    
                    # --- ADD THIS TO PREVENT MEMORY CRASHES ---
                    del lat       # Explicitly delete the lattice object
                    gc.collect()  # Force garbage collection
                    # ------------------------------------------

                    # Logging
                    count = len(self.completed_indices)
                    elapsed = time.time() - self.start_time
                    avg_time = elapsed / (count - len(self.completed_indices) + 1e-6) # rough est
                    # print(f"\rPoint ({i},{j}) [m^2={m_sq:.2f}, lam={lam:.2f}] -> xi={self.results[i,j]:.3f}", end="")
                    
                    # Auto-save every 5 points
                    if count % 5 == 0:
                        self.save_checkpoint()
                        
        except KeyboardInterrupt:
            print("\n[!] Interrupt detected. Saving state...")
            self.save_checkpoint()
            sys.exit(0)
            
        print("\n[System] Simulation Complete.")
        self.save_checkpoint()
        self.analyze_ratios()

    def analyze_ratios(self):
        """Finds the Standard Model candidates"""
        print("\n--- ANALYZING RATIOS (Target: 1 : 1.79 : 2.31) ---")
        # Flatten and filter
        data = []
        for i in range(GRID_RES):
            for j in range(GRID_RES):
                xi = self.results[i, j]
                if xi > 0.1:
                    data.append({'xi': xi, 'm': self.m_range[i], 'l': self.l_range[j]})
        
        data.sort(key=lambda x: x['xi'])
        
        candidates = []
        tolerance = 0.03 # Stricter 3% tolerance for "Scientific" run
        
        for base in data:
            xi_3 = base['xi'] # SU(3)
            
            # Find SU(2) match
            target_2 = xi_3 * 1.79
            matches_2 = [d for d in data if abs(d['xi'] - target_2)/target_2 < tolerance]
            
            # Find U(1) match
            target_1 = xi_3 * 2.31
            matches_1 = [d for d in data if abs(d['xi'] - target_1)/target_1 < tolerance]
            
            if matches_2 and matches_1:
                candidates.append({
                    'SU3': base,
                    'SU2': matches_2[0], # Closest
                    'U1': matches_1[0]
                })
        
        print(f"Found {len(candidates)} candidate geometries within {tolerance*100}% tolerance.")
        if candidates:
            # Sort by "completeness" or quality? Let's just show the first few.
            print("Top Candidate:")
            c = candidates[0]
            print(f"  SU(3): xi={c['SU3']['xi']:.4f} (m={c['SU3']['m']:.2f}, l={c['SU3']['l']:.2f})")
            print(f"  SU(2): xi={c['SU2']['xi']:.4f} (m={c['SU2']['m']:.2f}, l={c['SU2']['l']:.2f}) -> Ratio: {c['SU2']['xi']/c['SU3']['xi']:.3f}")
            print(f"  U(1):  xi={c['U1']['xi']:.4f}  (m={c['U1']['m']:.2f},  l={c['U1']['l']:.2f})  -> Ratio: {c['U1']['xi']/c['SU3']['xi']:.3f}")
            
            # Plot
            plt.figure(figsize=(8,6))
            plt.imshow(self.results, origin='lower', aspect='auto', 
                       extent=[self.l_range.min(), self.l_range.max(), self.m_range.min(), self.m_range.max()])
            plt.colorbar(label=r'Stiffness $\xi$')
            plt.scatter(c['SU3']['l'], c['SU3']['m'], c='red', marker='x', label='SU(3)')
            plt.scatter(c['SU2']['l'], c['SU2']['m'], c='orange', marker='x', label='SU(2)')
            plt.scatter(c['U1']['l'], c['U1']['m'], c='white', marker='x', label='U(1)')
            plt.legend()
            plt.title("Pirouette Stiffness Map with Candidate Points")
            plt.show()

if __name__ == "__main__":
    sim = SimulationManager()
    sim.load_checkpoint()
    sim.run()