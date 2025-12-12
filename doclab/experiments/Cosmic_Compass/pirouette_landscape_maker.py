import numpy as np
import logging
import time
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class DeepBoreMesher:
    def __init__(self, resolution=1000, max_steps=100000, bounds_scale=0.1):
        """
        DEEP BORE CONFIGURATION:
        - resolution: Grid density (1000x1000 = 1M points)
        - max_steps:  The 'Ceiling'. We raised this to 100,000 to see the needle.
        - bounds_scale: The 'Zoom'. 0.1 focuses tightly on the singularity.
        """
        self.res = resolution
        self.max_steps = max_steps
        self.scale = bounds_scale
        
        # Standard Henon-Heiles/Pirouette physics params (Must match original)
        self.sigma = 1.0 
        self.dt = 0.1
        
        # Visualization params
        self.height_scale = 10.0  # How tall the spikes look
        
    def compute_grid(self):
        """
        Simulates the physics to get height (Z) and color (Basin).
        """
        logger.info(f"Initializing {self.res}x{self.res} Deep Bore Grid...")
        logger.info(f"Zoom Level: {1.0/self.scale:.1f}x | Max Depth: {self.max_steps}")
        
        # 1. Create Coordinate Grid (Centered on the Singularity)
        m_vals = np.linspace(-1.5 * self.scale, 1.5 * self.scale, self.res)
        l_vals = np.linspace(-1.5 * self.scale, 1.5 * self.scale, self.res)
        M, L = np.meshgrid(m_vals, l_vals)
        
        # 2. Dynamics Arrays
        p_m = np.zeros_like(M)
        p_l = np.zeros_like(L)
        active = np.ones_like(M, dtype=bool)
        escape_time = np.zeros_like(M, dtype=float) + self.max_steps
        basin_id = np.zeros_like(M, dtype=int)
        
        logger.info("Integrating Trajectories (This may take a while)...")
        t0 = time.time()
        
        # 3. Integration Loop (Leapfrog)
        # We print progress because 100k steps is a lot.
        for step in range(1, self.max_steps + 1):
            if not np.any(active): 
                logger.info("All particles escaped early.")
                break
            
            if step % 5000 == 0:
                pct = (step / self.max_steps) * 100
                active_count = np.sum(active)
                sys.stdout.write(f"\rStep {step}/{self.max_steps} ({pct:.1f}%) | Active Particles: {active_count}   ")
                sys.stdout.flush()
            
            # --- PHYSICS ENGINE (Identical to Original) ---
            # Half-kick
            grad_m = M + 2 * self.sigma * M * L
            grad_l = L + self.sigma * (M**2 - L**2)
            p_m[active] -= 0.5 * self.dt * grad_m[active]
            p_l[active] -= 0.5 * self.dt * grad_l[active]
            
            # Drift
            M[active] += self.dt * p_m[active]
            L[active] += self.dt * p_l[active]
            
            # Half-kick (at new pos)
            grad_m = M + 2 * self.sigma * M * L
            grad_l = L + self.sigma * (M**2 - L**2)
            p_m[active] -= 0.5 * self.dt * grad_m[active]
            p_l[active] -= 0.5 * self.dt * grad_l[active]
            
            # Check Escape
            r2 = M**2 + L**2
            escaped_now = (r2 > 20.0) & active
            
            if np.any(escaped_now):
                theta = np.arctan2(L[escaped_now], M[escaped_now])
                b_now = np.zeros(np.sum(escaped_now), dtype=int)
                
                # Basin Classification
                mask_teal = (theta > 0.5) & (theta < 2.5)
                mask_red = np.abs(theta) > 2.5
                b_now[:] = 2 # Gold
                b_now[mask_teal] = 1
                b_now[mask_red] = 3
                
                basin_id[escaped_now] = b_now
                escape_time[escaped_now] = step
                active[escaped_now] = False
                
        print() # Newline after progress bar
        logger.info(f"Simulation Complete ({time.time()-t0:.2f}s)")
        return m_vals, l_vals, escape_time, basin_id

    def export_ply(self, filename="pirouette_deep_bore.ply"):
        m_vals, l_vals, esc_time, basin_ids = self.compute_grid()
        
        logger.info("Generating Mesh Data...")
        rows, cols = self.res, self.res
        
        # --- Z-AXIS CALCULATION (The Needle Logic) ---
        logger.info("Calculating Logarithmic Heights...")
        
        # 1. Log scale to compress the 100,000 range into viewable spikes
        Z = np.log1p(esc_time)
        
        # 2. Normalize based on the LOG max, not absolute max
        max_log_z = np.max(Z)
        if max_log_z == 0: max_log_z = 1.0
        
        # 3. Apply Height Scale (No clamping!)
        Z = Z / max_log_z * self.height_scale
        
        # --- COLORING ---
        colors = np.zeros((rows, cols, 3), dtype=np.uint8)
        
        # Basin Colors
        c_void  = [10, 10, 10]    # The Core (Did not escape)
        c_teal  = [0, 200, 200]
        c_gold  = [230, 180, 20]
        c_red   = [230, 60, 20]
        c_white = [255, 255, 255] # Rim
        
        # Apply Base Colors
        colors[basin_ids == 0] = c_void
        colors[basin_ids == 1] = c_teal
        colors[basin_ids == 2] = c_gold
        colors[basin_ids == 3] = c_red
        
        # Highlight Rims (Steep gradients)
        grads = np.gradient(esc_time)
        slope = np.sqrt(grads[0]**2 + grads[1]**2)
        # Adaptive rim threshold based on zoom
        rim_mask = (slope > 5.0) & (basin_ids != 0)
        colors[rim_mask] = c_white

        logger.info(f"Writing PLY to {filename}...")
        
        header = f"""ply
format ascii 1.0
element vertex {rows * cols}
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
element face {(rows-1) * (cols-1) * 2}
property list uchar int vertex_index
end_header
"""
        
        with open(filename, 'w') as f:
            f.write(header)
            
            # Vertices
            for i in range(rows):
                y = l_vals[i]
                for j in range(cols):
                    x = m_vals[j]
                    z = Z[i, j]
                    r, g, b = colors[i, j]
                    f.write(f"{x:.5f} {y:.5f} {z:.5f} {r} {g} {b}\n")
            
            # Faces
            for i in range(rows - 1):
                for j in range(cols - 1):
                    tl = i * cols + j
                    tr = tl + 1
                    bl = (i + 1) * cols + j
                    br = bl + 1
                    f.write(f"3 {tl} {bl} {tr}\n")
                    f.write(f"3 {tr} {bl} {br}\n")

        logger.info("Done! The Needle has been forged.")

if __name__ == "__main__":
    # 1000x1000 grid, 100,000 steps, 0.1 zoom (Targeting the core)
    mesher = DeepBoreMesher(resolution=1000, max_steps=100000, bounds_scale=0.1)
    mesher.export_ply()