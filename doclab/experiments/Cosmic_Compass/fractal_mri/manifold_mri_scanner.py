import numpy as np
import h5py
import time
import os
from scipy.ndimage import laplace

class ManifoldMRIScanner:
    def __init__(self, resolution=500, max_steps=1000, bounds=2.0, filename="wada_manifold_mri.h5"):
        """
        THE MANIFOLD MRI SCANNER
        Generates a volumetric dataset of the Fractal's 'Nervous System'.
        
        resolution: Grid density (e.g., 500x500)
        max_steps:  The depth of the MRI (Z-axis)
        bounds:     Spatial zoom level
        """
        self.res = resolution
        self.steps = max_steps
        self.bounds = bounds
        self.filename = filename
        
        # Physics Constants (Hénon-Heiles)
        self.dt = 0.1
        self.epsilon = 1e-5  # The Shadow separation distance
        
    def _initialize_grid(self):
        """Creates the vectorized grid for Reality and Shadow."""
        print(f"[-] Initializing Quantum Grid ({self.res}x{self.res})...")
        
        # 1. Reality Grid
        m = np.linspace(-self.bounds, self.bounds, self.res)
        l = np.linspace(-self.bounds, self.bounds, self.res)
        M, L = np.meshgrid(m, l)
        
        # State vectors: [m, l, pm, pl]
        self.state_r = np.stack([M, L, np.zeros_like(M), np.zeros_like(L)], axis=0)
        
        # 2. Shadow Grid (Displaced by epsilon)
        # We displace slightly in both M and L to measure isotropic stretching
        dist_m = M + self.epsilon
        dist_l = L + self.epsilon
        self.state_s = np.stack([dist_m, dist_l, np.zeros_like(M), np.zeros_like(L)], axis=0)
        
        # Tracking arrays
        self.active_mask = np.ones((self.res, self.res), dtype=bool)
        
    def _step_physics(self, state):
        """Vectorized Leapfrog Integrator for the Hénon-Heiles potential."""
        m, l, pm, pl = state[0], state[1], state[2], state[3]
        
        # Half-step momentum
        # Gradient V: dV/dm = m + 2ml, dV/dl = l + m^2 - l^2
        pm -= 0.5 * self.dt * (m + 2*m*l)
        pl -= 0.5 * self.dt * (l + m**2 - l**2)
        
        # Full-step position
        m += self.dt * pm
        l += self.dt * pl
        
        # Half-step momentum (at new position)
        pm -= 0.5 * self.dt * (m + 2*m*l)
        pl -= 0.5 * self.dt * (l + m**2 - l**2)
        
        return state

    def run_scan(self):
        self._initialize_grid()
        
        print(f"[-] Opening CloudConnect Storage: {self.filename}")
        with h5py.File(self.filename, 'w') as f:
            # Create Datasets
            # We store the "Delta" (Spatial Gradient of Divergence) and raw Divergence
            dset_div   = f.create_dataset("divergence", (self.steps, self.res, self.res), dtype='float32')
            dset_delta = f.create_dataset("delta_gradient", (self.steps, self.res, self.res), dtype='float32')
            
            # Attributes for reproducibility
            f.attrs['resolution'] = self.res
            f.attrs['bounds'] = self.bounds
            f.attrs['dt'] = self.dt
            
            t0 = time.time()
            
            for t in range(self.steps):
                # PROGRESS BAR FIX: 
                # Only calculate rate if t > 0 to avoid division by zero on the first frame
                if t % 10 == 0 and t > 0:
                    elapsed = time.time() - t0
                    # Safety against super-fast execution
                    if elapsed == 0: elapsed = 0.001 
                    
                    rate = (t) / elapsed
                    rem = (self.steps - t) / rate
                    print(f"\r[Slice {t}/{self.steps}] MRI Scanning... {rate:.1f} slices/s (ETA: {rem:.0f}s)", end='')

                # 1. Evolve Reality and Shadow
                self.state_r = self._step_physics(self.state_r)
                self.state_s = self._step_physics(self.state_s)
                
                # 2. Calculate Divergence (The Lyapunov Stretch)
                # Euclidean distance between Reality and Shadow
                diff = self.state_r[:2] - self.state_s[:2] # shape (2, res, res)
                dist = np.sqrt(diff[0]**2 + diff[1]**2)
                
                # Log Divergence (Lyapunov estimate)
                # We perform a safe log
                log_div = np.log(dist / self.epsilon + 1e-9)
                
                # 3. Calculate THE DELTA (Spatial Gradient)
                # This is what you asked for: The delta moving from geodesic to geodesic.
                # High values here indicate you are on a "Ridge" of the potential.
                # We use a Laplacian filter to find edges in the chaos field.
                delta_map = np.abs(laplace(log_div))
                
                # 4. Filter Escaped Particles (Optional: clamp values for visual consistency)
                # Check escape condition (r^2 > 20)
                r2 = self.state_r[0]**2 + self.state_r[1]**2
                escaped = r2 > 20.0
                
                # Once escaped, the physics is meaningless, so we freeze the last known delta
                # (Logic handled implicitly by not zeroing out 'escaped' but letting them drift)
                # Just clamp the log_div to avoid infinities
                log_div[escaped] = 10.0 # Max saturation
                
                # 5. Write Slice to Disk
                dset_div[t, :, :] = log_div.astype('float32')
                dset_delta[t, :, :] = delta_map.astype('float32')
                
            print(f"\n[+] Scan Complete. Data locked in {self.filename}")
            if os.path.exists(self.filename):
                print(f"[+] Volumetric Size: {os.path.getsize(self.filename) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    # WARNING: This will generate data. 
    # 500x500x500 slices is approx 1GB of raw floats.
    # Defaulting to 400x400x400 for your test run
    scanner = ManifoldMRIScanner(resolution=400, max_steps=400, bounds=2.0)
    scanner.run_scan()