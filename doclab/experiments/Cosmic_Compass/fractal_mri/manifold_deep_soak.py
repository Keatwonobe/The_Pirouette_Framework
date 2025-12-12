import numpy as np
import h5py
import time
import os
from scipy.ndimage import laplace

class DeepManifoldScanner:
    def __init__(self, resolution=500, max_steps=4000, bounds=2.0, filename="wada_deep_mri.h5"):
        self.res = resolution
        self.steps = max_steps
        self.bounds = bounds
        self.filename = filename
        self.dt = 0.1
        self.epsilon = 1e-5 
        
    def run_scan(self):
        print(f"[-] Initializing Deep Soak Grid ({self.res}x{self.res})...")
        
        # 1. Setup Grids
        m = np.linspace(-self.bounds, self.bounds, self.res)
        l = np.linspace(-self.bounds, self.bounds, self.res)
        M, L = np.meshgrid(m, l)
        
        # State: Reality (r) and Shadow (s)
        # [M, L, pM, pL]
        state_r = np.stack([M, L, np.zeros_like(M), np.zeros_like(L)], axis=0)
        state_s = np.stack([M+self.epsilon, L+self.epsilon, np.zeros_like(M), np.zeros_like(L)], axis=0)
        
        # MASKING SYSTEM:
        # We track who has escaped. If escaped, we stop updating them.
        # This lets the middle "soak" for thousands of steps.
        escaped_mask = np.zeros((self.res, self.res), dtype=bool)
        
        # Storage for the 'Frozen' divergence values
        final_log_div = np.zeros((self.res, self.res), dtype=np.float32)

        print(f"[-] Opening Storage: {self.filename}")
        with h5py.File(self.filename, 'w') as f:
            # We store the SIGNED Laplacian (Directional Delta)
            dset_signed_delta = f.create_dataset("signed_delta", (self.steps, self.res, self.res), dtype='float32')
            
            f.attrs['resolution'] = self.res
            f.attrs['bounds'] = self.bounds
            
            t0 = time.time()
            
            for t in range(self.steps):
                # Progress
                if t % 10 == 0 and t > 0:
                    elapsed = time.time() - t0
                    if elapsed == 0: elapsed = 0.001
                    rate = t / elapsed
                    rem = (self.steps - t) / rate
                    active_count = np.sum(~escaped_mask)
                    print(f"\r[T={t}/{self.steps}] Active Particles: {active_count} | {rate:.1f} slices/s | ETA: {rem:.0f}s", end='')

                # --- PHYSICS ENGINE (Vectorized & Masked) ---
                # Only update points that have NOT escaped (~escaped_mask)
                # This prevents NaNs and saves computation (conceptually)
                
                # We flatten for boolean indexing, then reshape back
                # (Note: In pure numpy, masking like this can be slower than full matrix ops due to overhead, 
                # but it prevents floating point overflow on escaped particles).
                
                # Actually, for speed, we perform physics on ALL, but we maintain the logic:
                
                # 1. Leapfrog Step
                for state in [state_r, state_s]:
                    m_curr, l_curr, pm, pl = state
                    
                    # Half-kick
                    pm -= 0.5 * self.dt * (m_curr + 2*m_curr*l_curr)
                    pl -= 0.5 * self.dt * (l_curr + m_curr**2 - l_curr**2)
                    
                    # Drift
                    m_curr += self.dt * pm
                    l_curr += self.dt * pl
                    
                    # Half-kick
                    pm -= 0.5 * self.dt * (m_curr + 2*m_curr*l_curr)
                    pl -= 0.5 * self.dt * (l_curr + m_curr**2 - l_curr**2)
                    
                    state[:] = [m_curr, l_curr, pm, pl]

                # 2. Check Escape
                r2 = state_r[0]**2 + state_r[1]**2
                new_escapes = (r2 > 20.0) & (~escaped_mask)
                escaped_mask = escaped_mask | new_escapes
                
                # 3. Calculate Divergence
                diff = state_r[:2] - state_s[:2]
                dist = np.sqrt(diff[0]**2 + diff[1]**2)
                
                # Safe Log
                current_log_div = np.log(dist / self.epsilon + 1e-12)
                
                # Update the "Final" map with current values.
                # If a point is already escaped, its value in 'current_log_div' might be garbage 
                # (super high), so we only update the non-escaped ones?
                # Actually, strictly speaking, we want to snapshot the divergence *as* it evolves.
                
                # 4. Calculate SIGNED Laplacian (The Directional Delta)
                # Positive = Convex (Bowl), Negative = Concave (Ridge)
                # We compute this on the entire field to see the waves moving through the escaping particles too.
                # To prevent garbage from distant particles ruining the gradient, we clamp the input.
                
                clamped_div = np.clip(current_log_div, -5, 15) 
                
                # standard Laplace is sum of second derivatives
                signed_delta = laplace(clamped_div)
                
                # 5. Write
                dset_signed_delta[t, :, :] = signed_delta.astype('float32')
                
            print(f"\n[+] Scan Complete. Deep Soak finished.")

if __name__ == "__main__":
    # Running 1500 steps to really let the center settle
    scanner = DeepManifoldScanner(resolution=500, max_steps=4000, bounds=2.0)
    scanner.run_scan()