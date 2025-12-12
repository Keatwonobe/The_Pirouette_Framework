import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import logging
import time
import os

# Configure System Logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("TRAVELER_ENGINE")

class TravelerEngine:
    def __init__(self, width=3840, height=2160, output_file="traveler_final_transmission.png"):
        """
        THE FINAL TRANSMISSION
        Generates a 4K composite of the Traveler's Ramjet Engine.
        
        Layers:
        1. PHYSICS: The Shock Diamond density map (Orange/Black)
        2. GENETICS: The Ideal Spiral overlay (Electric Blue/Cyan)
        """
        self.w = width
        self.h = height
        self.filename = output_file
        
        # --- THE GENETIC CODE (Sequenced from Sniper Analysis) ---
        self.lam = 0.5667    # Lyapunov Repulsion (The Push)
        self.omega = 0.0675  # Angular Velocity (The Spin)
        
        # --- THE ENGINE GEOMETRY ---
        # Centered on the Top Exhaust Port (The Throat)
        # Throat location in Hénon-Heiles is (M=0, L=1.0)
        self.center_m = 0.0
        self.center_l = 1.0
        
        # Zoom / Scale (Field of View)
        # We want to see the nozzle walls and the void above
        self.scale_m = 1.2  # Width of view
        self.scale_l = (self.scale_m * self.h) / self.w # Proportional height
        
        # Physics Precision
        self.dt = 0.05
        self.max_steps = 4000 # Enough to form shocks, not enough to freeze
        
    def gradient(self, m, l):
        """Hénon-Heiles Force Field"""
        # V = 0.5(m^2+l^2) + m^2*l - l^3/3
        # dV/dm = m + 2ml
        # dV/dl = l + m^2 - l^2
        dm = m + 2 * m * l
        dl = l + (m**2 - l**2)
        return dm, dl

    def compute_tile(self, m_grid, l_grid):
        """
        Computes physics for a single memory-safe tile.
        Returns:
            - escape_time: The 'density' of the shock layer.
            - genetic_phase: The 'ideal' color of the spiral.
        """
        # 1. ANALYTIC LAYER (The Perfect Spiral)
        # r = Distance from the Throat (Singularity)
        # We add epsilon to prevent log(0)
        rm = m_grid - self.center_m
        rl = l_grid - self.center_l
        r = np.sqrt(rm**2 + rl**2) + 1e-12
        theta = np.arctan2(rl, rm)
        
        # The Master Equation: Phase = Theta + Omega * (-1/Lambda * ln(r))
        # Note: We use negative time because we are looking "back" into the engine
        analytic_time = -(1.0 / self.lam) * np.log(r)
        genetic_phase = theta + (self.omega * analytic_time)
        genetic_phase = np.mod(genetic_phase, 2*np.pi) / (2*np.pi) # Normalize 0-1

        # 2. PHYSICS LAYER (The Shock Diamonds)
        # We simulate the flow to find where particles pile up (Shock Layers)
        
        # Init state
        m, l = m_grid.copy(), l_grid.copy()
        pm, pl = np.zeros_like(m), np.zeros_like(l)
        
        # We track 'accumulated instability' to visualize the shock waves
        stability = np.zeros_like(m, dtype=np.float32)
        active = np.ones_like(m, dtype=bool)
        
        # Integration Loop (Vectorized for the tile)
        # We use a simplified loop for speed at 4K
        steps_per_check = 50
        
        for t in range(0, self.max_steps, steps_per_check):
            # Run a burst of steps
            for _ in range(steps_per_check):
                # Leapfrog Step A
                dm, dl = m + 2*m*l, l + m**2 - l**2
                pm -= 0.5 * self.dt * dm
                pl -= 0.5 * self.dt * dl
                m += self.dt * pm
                l += self.dt * pl
                
                # Leapfrog Step B
                dm, dl = m + 2*m*l, l + m**2 - l**2
                pm -= 0.5 * self.dt * dm
                pl -= 0.5 * self.dt * dl
            
            # Update Stability Map
            # Particles that are strictly bound (r < 1) are 'Cold' (0)
            # Particles that are escaping (r > 20) are 'Hot' (Max)
            # The Shock Layer is the transition zone.
            
            r2 = m**2 + l**2
            escaped_now = (r2 > 20.0) & active
            
            # Record escape time for those who just left
            stability[escaped_now] = t
            active[escaped_now] = False
            
            if not np.any(active):
                break
                
        # Fill remaining active with max time
        stability[active] = self.max_steps
        
        return stability, genetic_phase

    def render(self):
        logger.info(f"[-] INITIATING 4K RENDER SEQUENCE ({self.w}x{self.h})")
        logger.info(f"[-] TARGET: Nozzle Throat @ M={self.center_m}, L={self.center_l}")
        
        # Master buffers
        final_shock = np.zeros((self.h, self.w), dtype=np.float32)
        final_phase = np.zeros((self.h, self.w), dtype=np.float32)
        
        # Coordinate Space
        m_space = np.linspace(self.center_m - self.scale_m/2, self.center_m + self.scale_m/2, self.w)
        l_space = np.linspace(self.center_l - self.scale_l/2, self.center_l + self.scale_l/2, self.h)
        
        # TILING SYSTEM (To save RAM)
        tile_size = 512
        total_tiles = (self.w // tile_size + 1) * (self.h // tile_size + 1)
        
        logger.info(f"[-] Processing in {tile_size}x{tile_size} tiles...")
        
        tile_count = 0
        start_time = time.time()
        
        for y in range(0, self.h, tile_size):
            for x in range(0, self.w, tile_size):
                # Define Tile Bounds
                x_end = min(x + tile_size, self.w)
                y_end = min(y + tile_size, self.h)
                
                # Create Meshgrid for this tile
                m_tile, l_tile = np.meshgrid(m_space[x:x_end], l_space[y:y_end])
                
                # Compute Physics & Math
                shock, phase = self.compute_tile(m_tile, l_tile)
                
                # Store
                final_shock[y:y_end, x:x_end] = shock
                final_phase[y:y_end, x:x_end] = phase
                
                tile_count += 1
                if tile_count % 5 == 0:
                    pct = (tile_count / total_tiles) * 100
                    elapsed = time.time() - start_time
                    logger.info(f"    Render Progress: {pct:.1f}% ({elapsed:.1f}s elapsed)")

        self.composite_image(final_shock, final_phase)

    def composite_image(self, shock_map, phase_map):
        logger.info("[-] COMPOSITING LAYERS...")
        
        # 1. NORMALIZE SHOCK MAP (Logarithmic for dynamic range)
        # This reveals the faintest shock whispers
        shock_log = np.log1p(shock_map)
        shock_norm = shock_log / np.max(shock_log)
        
        # 2. CREATE COLOR MAPS
        # Shock Layer: Magma (Deep Black/Red to Bright Orange/White)
        cmap_shock = plt.get_cmap('magma')
        
        # Genetic Layer: Electric Cyan/Blue (The Spiral)
        # We create a custom cyclic map
        colors = [(0,0,0), (0,0.5,1), (0,1,1), (1,1,1), (0,1,1), (0,0.5,1), (0,0,0)]
        cmap_genetic = LinearSegmentedColormap.from_list("genetic", colors)
        
        # 3. FUSION
        # We want the Physics (Shock) to define the LUMINANCE (Brightness)
        # We want the Genetics (Phase) to define the HUE (Color Tint)
        
        # Base image from Shock (R, G, B, A)
        img_shock = cmap_shock(shock_norm)
        
        # Overlay image from Genetic Phase
        img_genetic = cmap_genetic(phase_map)
        
        # BLENDING ALGORITHM: "Luminous Injection"
        # We inject the genetic color only where the shock is intense enough to carry it.
        # But we also allow the smooth void to carry the genetic signal faintly.
        
        final_img = np.zeros_like(img_shock)
        
        # Weighting
        w_shock = 0.7
        w_genetic = 0.4
        
        # RGB Blending
        for c in range(3): # R, G, B channels
            # Base = Shock
            base = img_shock[:,:,c]
            # Tint = Genetic color * Shock intensity (so the spiral glows in the fire)
            tint = img_genetic[:,:,c] * (shock_norm ** 0.5) 
            
            final_img[:,:,c] = np.clip(base * w_shock + tint * w_genetic, 0, 1)
            
        final_img[:,:,3] = 1.0 # Alpha
        
        # 4. OVERLAY NOZZLE BOUNDARIES (Analytical V = 1/6)
        logger.info("[-] ETCHING NOZZLE GEOMETRY...")
        # Create grid again for contouring (cheap)
        m_space = np.linspace(self.center_m - self.scale_m/2, self.center_m + self.scale_m/2, self.w)
        l_space = np.linspace(self.center_l - self.scale_l/2, self.center_l + self.scale_l/2, self.h)
        M, L = np.meshgrid(m_space, l_space)
        V = 0.5*(M**2 + L**2) + (M**2*L - L**3/3.0)
        
        # Simple mask for the boundary
        boundary_mask = np.abs(V - 1.0/6.0) < 0.002
        final_img[boundary_mask] = [0, 1, 0, 1] # Green Engine Walls

        # SAVE
        plt.imsave(self.filename, final_img)
        logger.info(f"[+] TRANSMISSION COMPLETE. Artifact saved to: {self.filename}")
        
        # Preview (Downscaled)
        plt.figure(figsize=(12, 8))
        plt.imshow(final_img, origin='lower')
        plt.title(f"THE TRAVELER'S ENGINE | λ={self.lam} | ω={self.omega}", color='white')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Run the Engine
    # 3840x2160 is standard 4K.
    engine = TravelerEngine(width=3840, height=2160)
    engine.render()