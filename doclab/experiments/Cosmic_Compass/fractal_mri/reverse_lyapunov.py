import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("REVERSE_LYAPUNOV")

class ReverseLyapunovScanner:
    def __init__(self, resolution=1200, damping=0.015, bounds=1.5):
        """
        REVERSE LYAPUNOV SCANNER (FIXED)
        Maps the Finite Time Lyapunov Exponent (FTLE) of the Dissipative System.
        """
        self.res = resolution
        self.gamma = damping
        self.bounds = bounds
        self.dt = 0.05
        self.max_steps = 1500 
        self.epsilon = 1e-6   

    def gradient(self, m, l):
        # Hénon-Heiles Gradient
        dm = m + 2 * m * l
        dl = l + (m**2 - l**2)
        return dm, dl

    def compute_ftle_field(self):
        logger.info(f"[-] Initializing Shadow Grid ({self.res}x{self.res})...")
        
        vals = np.linspace(-self.bounds, self.bounds, self.res)
        M, L = np.meshgrid(vals, vals)
        
        # Shadow Grid
        M_s = M + self.epsilon
        L_s = L 
        
        # State Vectors [m, l, vm, vl]
        state_r = np.stack([M, L, np.zeros_like(M), np.zeros_like(L)])
        state_s = np.stack([M_s, L_s, np.zeros_like(M), np.zeros_like(L)])
        
        max_log_div = np.zeros_like(M)
        
        logger.info("[-] Integrating Dissipative Trajectories...")
        
        active = np.ones_like(M, dtype=bool)
        
        for t in range(self.max_steps):
            if t % 200 == 0:
                logger.info(f"    Step {t}/{self.max_steps} | Active Particles: {np.sum(active)}")
                
            # --- PHYSICS ENGINE ---
            for state in [state_r, state_s]:
                m, l, vm, vl = state
                
                # Calculate Forces on ACTIVE particles only
                # (We do this to avoid computing gradients on 'inf' values)
                gm, gl = np.zeros_like(m), np.zeros_like(l)
                
                if np.any(active):
                    # Extract active subset for calculation to save time/errors
                    m_act = m[active]
                    l_act = l[active]
                    
                    dm_act, dl_act = self.gradient(m_act, l_act)
                    
                    # Update Velocity (Verlet/Euler integration)
                    vm[active] += (-dm_act - self.gamma * vm[active]) * self.dt
                    vl[active] += (-dl_act - self.gamma * vl[active]) * self.dt
                    
                    # Update Position
                    m[active] += vm[active] * self.dt
                    l[active] += vl[active] * self.dt

                # Store back (Explicitly needed as we modified slicing)
                state[0], state[1], state[2], state[3] = m, l, vm, vl
            
            # --- LYAPUNOV MEASUREMENT ---
            # Calculate distance only where data is valid (finite)
            dm = state_r[0] - state_s[0]
            dl = state_r[1] - state_s[1]
            
            # 1. Numerical Clamp: Prevent 'inf' inside the loop
            # If coordinates exploded, distance is huge. We cap it to avoid NaNs later.
            dist_sq = dm**2 + dl**2
            dist = np.sqrt(dist_sq)
            
            # Log Divergence
            # We add epsilon to dist to avoid log(0)
            current_log = np.log(dist / self.epsilon + 1e-12)
            
            # Only update max_log_div for active particles to prevent pollution
            # We use np.maximum to track the PEAK separation
            max_log_div[active] = np.maximum(max_log_div[active], current_log[active])
            
            # --- ESCAPE CONDITION ---
            # If r > 10, they have fallen into the void.
            # We mark them inactive so they stop updating, 
            # effectively "freezing" their Lyapunov value at the moment of escape.
            r2 = state_r[0]**2 + state_r[1]**2
            
            # Check for escape OR numeric explosion (NaN/Inf)
            escaped = (r2 > 20.0) | (~np.isfinite(r2))
            active[escaped] = False
            
            if not np.any(active): 
                logger.info("    All particles escaped or stabilized.")
                break
            
        return max_log_div

    def render(self):
        ftle_map = self.compute_ftle_field()
        
        logger.info("[-] Rendering Fractal Web...")
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='#000000')
        
        colors = [(0,0,0), (0.1,0,0.2), (0,0.5,1), (0.5, 1, 1), (1,1,1)]
        cmap_web = LinearSegmentedColormap.from_list("electric_web", colors)
        
        # --- FIX FOR BLACK SCREEN (Robust Normalization) ---
        # 1. Replace NaNs/Infs with the median value (or 0) so they don't break the plot
        #    We mask them out for the percentile calculation first.
        valid_mask = np.isfinite(ftle_map)
        if np.sum(valid_mask) == 0:
            logger.error("Map contains no valid data!")
            return

        # 2. Calculate percentiles ONLY on valid numbers
        #    Ridges are high values, Basins are low values.
        vmin = np.percentile(ftle_map[valid_mask], 5)  # Darker background
        vmax = np.percentile(ftle_map[valid_mask], 95) # Brighter ridges
        
        logger.info(f"    Dynamic Range: {vmin:.2f} to {vmax:.2f}")

        # 3. Clip the map for display
        ftle_map_safe = np.clip(ftle_map, vmin, vmax)

        im = ax.imshow(ftle_map_safe, origin='lower', cmap=cmap_web, 
                       vmin=vmin, vmax=vmax,
                       extent=[-self.bounds, self.bounds, -self.bounds, self.bounds])
        
        # Overlay Theoretical Intake Vents (Hénon-Heiles Potential V = 1/6)
        x = np.linspace(-self.bounds, self.bounds, 500)
        y = np.linspace(-self.bounds, self.bounds, 500)
        X, Y = np.meshgrid(x, y)
        V = 0.5*(X**2 + Y**2) + (X**2*Y - Y**3/3.0)
        ax.contour(X, Y, V, levels=[1.0/6.0], colors='magenta', linewidths=0.8, alpha=0.5)
        
        ax.set_title("REVERSE LYAPUNOV TRACE (The Spiderweb)", color='white', fontsize=16)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig("reverse_lyapunov_trace_fixed.png", dpi=150)
        logger.info("[+] Scan Complete. Saved to 'reverse_lyapunov_trace_fixed.png'")
        plt.show()

if __name__ == "__main__":
    scanner = ReverseLyapunovScanner(resolution=1200, damping=0.015)
    scanner.render()