import numpy as np
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class DeepFieldMesher:
    def __init__(self, resolution=1200, max_steps=1200, zoom_level=4.5):
        self.res = resolution
        self.max_steps = max_steps
        self.zoom = zoom_level
        # Shift the view slightly Up (positive L) to capture the Blue channel better
        self.offset_l = 0.2 
        self.sigma = 1.0 
        self.dt = 0.1
        
    def compute_landscape(self):
        logger.info(f"Scanning Deep Field ({self.res}x{self.res})...")
        
        # 1. Setup the Grid (Zoomed Out & Shifted)
        # We increase the aspect ratio to capture the wide "wings" of Red/Gold
        m_span = 1.2 * self.zoom
        l_span = 1.2 * self.zoom
        
        m_vals = np.linspace(-m_span, m_span, self.res)
        l_vals = np.linspace(-l_span + self.offset_l, l_span + self.offset_l, self.res)
        
        M, L = np.meshgrid(m_vals, l_vals)
        
        # 2. Physics Engine (Vectorized)
        p_m = np.zeros_like(M)
        p_l = np.zeros_like(L)
        active = np.ones_like(M, dtype=bool)
        escape_time = np.zeros_like(M, dtype=float) + self.max_steps
        basin_id = np.zeros_like(M, dtype=int) # 0=Tower
        
        logger.info("integrating trajectories...")
        t0 = time.time()
        
        for step in range(1, self.max_steps + 1):
            if not np.any(active): break
            
            # 4th Order Symplectic Integration (Better stability for the 'Tower')
            # We stick to Leapfrog for speed, but with tighter checks
            
            # Kick 1
            grad_m = M + 2 * self.sigma * M * L
            grad_l = L + self.sigma * (M**2 - L**2)
            p_m[active] -= 0.5 * self.dt * grad_m[active]
            p_l[active] -= 0.5 * self.dt * grad_l[active]
            
            # Drift
            M[active] += self.dt * p_m[active]
            L[active] += self.dt * p_l[active]
            
            # Kick 2
            grad_m = M + 2 * self.sigma * M * L
            grad_l = L + self.sigma * (M**2 - L**2)
            p_m[active] -= 0.5 * self.dt * grad_m[active]
            p_l[active] -= 0.5 * self.dt * grad_l[active]
            
            # Escape Check
            r2 = M**2 + L**2
            # The 'Shelf' is roughly at r2 = 20, but we check farther out
            escaped_now = (r2 > 25.0) & active
            
            if np.any(escaped_now):
                theta = np.arctan2(L[escaped_now], M[escaped_now])
                
                # Assign Basins
                b_now = np.zeros(np.sum(escaped_now), dtype=int)
                mask_teal = (theta > 0.5) & (theta < 2.5) # The "Up" Channel
                mask_red  = (np.abs(theta) > 2.6)         # The "Left/Right" Wings
                # Gold is the remaining "Down" sectors
                
                b_now[:] = 2 # Gold
                b_now[mask_teal] = 1
                b_now[mask_red] = 3
                
                basin_id[escaped_now] = b_now
                escape_time[escaped_now] = step
                active[escaped_now] = False
                
        logger.info(f"Scan Complete ({time.time()-t0:.2f}s)")
        return m_vals, l_vals, escape_time, basin_id

    def generate_monolith_ply(self, filename="pirouette_monolith.ply"):
        m_vals, l_vals, esc_time, basin_ids = self.compute_landscape()
        
        logger.info("Constructing 3D Geometry...")
        rows, cols = self.res, self.res
        
        # --- Z-Axis Mapping (The "Tower" Logic) ---
        # We want the 'shelf' to be flat, and the 'tower' to rise sharply.
        # Log scale handles the chaos ridges well.
        Z = np.log1p(esc_time)
        
        # Maximize the height of the central tower (The Keep)
        # Any point that hit max_steps is "Infinite", so we boost it
        # to create a flat-topped monolith.
        max_z_val = np.max(Z)
        tower_mask = (esc_time >= self.max_steps * 0.95)
        Z[tower_mask] = max_z_val * 1.2 # Make the tower pop up above the ridges
        
        # Scale for visual export
        Z = Z / np.max(Z) * 3.0 
        
        # --- Color Mapping ---
        colors = np.zeros((rows, cols, 3), dtype=np.uint8)
        
        # 0: The Monolith (White/Silver)
        c_tower = [220, 220, 230] 
        # 1: Teal Basin
        c_teal  = [20, 180, 180]
        # 2: Gold Basin
        c_gold  = [210, 160, 40]
        # 3: Red Basin
        c_red   = [200, 50, 40]
        
        colors[basin_ids == 0] = c_tower
        colors[basin_ids == 1] = c_teal
        colors[basin_ids == 2] = c_gold
        colors[basin_ids == 3] = c_red
        
        # Highlight the "Shelf" Edge (The Aperture)
        # Calculate local slope
        grads = np.gradient(esc_time)
        slope = np.sqrt(grads[0]**2 + grads[1]**2)
        shelf_edge = (slope > 5.0) & (slope < 50.0) # Band of high change
        colors[shelf_edge] = [255, 255, 255] # White rim around the aperture

        # --- PLY Export ---
        logger.info(f"Writing {filename}...")
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
            for i in range(rows):
                y = l_vals[i]
                for j in range(cols):
                    x = m_vals[j]
                    z = Z[i, j]
                    r, g, b = colors[i, j]
                    f.write(f"{x:.4f} {y:.4f} {z:.4f} {r} {g} {b}\n")
            
            for i in range(rows - 1):
                for j in range(cols - 1):
                    tl = i * cols + j
                    tr = tl + 1
                    bl = (i + 1) * cols + j
                    br = bl + 1
                    f.write(f"3 {tl} {bl} {tr}\n")
                    f.write(f"3 {tr} {bl} {br}\n")

        logger.info("Done. The Monolith is ready.")

if __name__ == "__main__":
    # High Res, Wide Zoom
    mesher = DeepFieldMesher(resolution=1000, max_steps=1200, zoom_level=5.0)
    mesher.generate_monolith_ply()