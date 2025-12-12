import numpy as np
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class ManifoldMesher:
    def __init__(self, resolution=1000, max_steps=1000, bounds_scale=2.5):
        self.res = resolution
        self.max_steps = max_steps
        self.scale = bounds_scale
        # Standard Henon-Heiles/Pirouette params
        self.sigma = 1.0 
        self.dt = 0.1
        
    def compute_grid(self):
        """
        Simulates the physics to get height (Z) and color (Basin).
        """
        logger.info(f"Initializing {self.res}x{self.res} Simulation Grid...")
        
        # 1. Create Coordinate Grid
        # Using a slightly wider aspect ratio to capture the 'wings'
        m_vals = np.linspace(-1.5 * self.scale, 1.5 * self.scale, self.res)
        l_vals = np.linspace(-1.2 * self.scale, 2.0 * self.scale, self.res)
        M, L = np.meshgrid(m_vals, l_vals)
        
        # 2. Dynamics Arrays
        p_m = np.zeros_like(M)
        p_l = np.zeros_like(L)
        active = np.ones_like(M, dtype=bool)
        escape_time = np.zeros_like(M, dtype=float) + self.max_steps
        basin_id = np.zeros_like(M, dtype=int)
        
        logger.info("Integrating Trajectories...")
        t0 = time.time()
        
        # 3. Integration Loop (Leapfrog)
        for step in range(1, self.max_steps + 1):
            if not np.any(active): break
            
            # Gradients
            # V = 1/2(m^2 + l^2) + sigma(m^2l - l^3/3)
            # dV/dm = m + 2*sigma*m*l
            # dV/dl = l + sigma(m^2 - l^2)
            
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
                # Classify Basin by Exit Angle
                theta = np.arctan2(L[escaped_now], M[escaped_now])
                
                # Teal: 0.5 < theta < 2.5
                # Red: |theta| > 2.5
                # Gold: Remaining
                b_now = np.zeros(np.sum(escaped_now), dtype=int)
                mask_teal = (theta > 0.5) & (theta < 2.5)
                mask_red = np.abs(theta) > 2.5
                # Gold is the default 0 in this temp array, but let's map it:
                # 1=Teal, 2=Gold, 3=Red
                b_now[:] = 2 # Default to Gold
                b_now[mask_teal] = 1
                b_now[mask_red] = 3
                
                basin_id[escaped_now] = b_now
                escape_time[escaped_now] = step
                active[escaped_now] = False
                
        logger.info(f"Simulation Complete ({time.time()-t0:.2f}s)")
        return m_vals, l_vals, escape_time, basin_id

    def export_ply(self, filename="pirouette_landscape.ply"):
        m_vals, l_vals, esc_time, basin_ids = self.compute_grid()
        
        logger.info("Generating Mesh Data...")
        
        # Flatten arrays for vertex writing
        rows, cols = self.res, self.res
        
        # Calculate Z (Height)
        # We use Log scale because the core is infinitely stable. 
        # Log compresses the spike so we can see the ridges.
        Z = np.log1p(esc_time)
        Z = Z / np.max(Z) * 2.0 # Scale height to roughly 2.0 units
        
        # Colors (RGB 0-255)
        # 0=Trapped (Black), 1=Teal, 2=Gold, 3=Red
        colors = np.zeros((rows, cols, 3), dtype=np.uint8)
        
        # Basin Colors
        c_black = [20, 20, 20]
        c_teal  = [0, 200, 200]
        c_gold  = [230, 180, 20]
        c_red   = [230, 60, 20]
        
        mask_0 = (basin_ids == 0)
        mask_1 = (basin_ids == 1)
        mask_2 = (basin_ids == 2)
        mask_3 = (basin_ids == 3)
        
        colors[mask_0] = c_black
        colors[mask_1] = c_teal
        colors[mask_2] = c_gold
        colors[mask_3] = c_red
        
        # Highlight Boundaries (High Z gradient)
        # This makes the "ridges" pop in white
        grads = np.gradient(Z)
        g_mag = np.sqrt(grads[0]**2 + grads[1]**2)
        edge_mask = g_mag > 0.15 # Threshold for "steepness"
        colors[edge_mask] = [255, 255, 255] # White ridges

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
            
            # 1. Write Vertices
            for i in range(rows):
                y = l_vals[i]
                for j in range(cols):
                    x = m_vals[j]
                    z = Z[i, j]
                    r, g, b = colors[i, j]
                    f.write(f"{x:.4f} {y:.4f} {z:.4f} {r} {g} {b}\n")
            
            # 2. Write Faces (Triangles connecting the grid)
            # Two triangles per grid square
            for i in range(rows - 1):
                for j in range(cols - 1):
                    # Indices in the flat list
                    # TL--TR
                    # | / |
                    # BL--BR
                    tl = i * cols + j
                    tr = tl + 1
                    bl = (i + 1) * cols + j
                    br = bl + 1
                    
                    # Triangle 1 (TL, BL, TR)
                    f.write(f"3 {tl} {bl} {tr}\n")
                    # Triangle 2 (TR, BL, BR)
                    f.write(f"3 {tr} {bl} {br}\n")

        logger.info("Done! Import the PLY file into Blender/MeshLab.")

if __name__ == "__main__":
    # Resolution 800 is a good balance for testing. 
    # For "Final Production", bump to 2000 (creates ~200MB file).
    mesher = ManifoldMesher(resolution=800, max_steps=600, bounds_scale=3.0)
    mesher.export_ply()