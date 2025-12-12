import numpy as np
import matplotlib.pyplot as plt
import logging
import time

# Configure Logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("CHRONOS")

class ChronosScope:
    def __init__(self, width=1920, height=1080):
        """
        THE CHRONOS SCOPE
        Visualizes the 'Twin' attractors by overlaying Forward Time (+t)
        against Reverse Time (-t).
        """
        self.w = width
        self.h = height
        self.filename = "chronos_symmetry_test.png"
        
        # Target the Nozzle Throat (same as previous scan)
        self.center_m = 0.0
        self.center_l = 1.0
        self.scale = 1.2
        self.aspect = self.w / self.h
        
        # Physics Params
        # Note: We keep the same energy level
        self.max_steps = 2000 
        
    def gradient(self, m, l):
        # Standard Hénon-Heiles
        dm = m + 2 * m * l
        dl = l + (m**2 - l**2)
        return dm, dl

    def scan_manifold(self, direction=1):
        """
        direction: 1 for Future (Exhaust), -1 for Past (Intake)
        """
        logger.info(f"[-] Scanning Time Vector: {'FUTURE (+t)' if direction==1 else 'PAST (-t)'}...")
        
        # Create Grid
        m_space = np.linspace(self.center_m - self.scale/2, self.center_m + self.scale/2, self.w)
        l_span = (self.scale / self.aspect)
        l_space = np.linspace(self.center_l - l_span/2, self.center_l + l_span/2, self.h)
        
        # We process in chunks to save memory
        final_map = np.zeros((self.h, self.w), dtype=np.float32)
        
        chunk_size = 128
        
        start_time = time.time()
        
        for y in range(0, self.h, chunk_size):
            y_end = min(y + chunk_size, self.h)
            for x in range(0, self.w, chunk_size):
                x_end = min(x + chunk_size, self.w)
                
                # Grid chunk
                M, L = np.meshgrid(m_space[x:x_end], l_space[y:y_end])
                
                # Init Physics
                m_curr, l_curr = M.copy(), L.copy()
                pm, pl = np.zeros_like(m_curr), np.zeros_like(l_curr)
                
                active = np.ones_like(m_curr, dtype=bool)
                stability = np.zeros_like(m_curr, dtype=np.float32) + self.max_steps
                
                # Dynamic Time Step (Negative for reverse time)
                dt = 0.05 * direction 
                
                # Integration Loop
                for t in range(0, self.max_steps, 20):
                    if not np.any(active): break
                    
                    # Burst integration
                    for _ in range(20):
                        # Symplectic Leapfrog
                        dm, dl = m_curr + 2*m_curr*l_curr, l_curr + m_curr**2 - l_curr**2
                        pm[active] -= 0.5 * dt * dm[active]
                        pl[active] -= 0.5 * dt * dl[active]
                        m_curr[active] += dt * pm[active]
                        l_curr[active] += dt * pl[active]
                        
                        dm, dl = m_curr + 2*m_curr*l_curr, l_curr + m_curr**2 - l_curr**2
                        pm[active] -= 0.5 * dt * dm[active]
                        pl[active] -= 0.5 * dt * dl[active]

                    # Check Escape
                    r2 = m_curr**2 + l_curr**2
                    escaped = (r2 > 20.0) & active
                    
                    if np.any(escaped):
                        stability[escaped] = t
                        active[escaped] = False
                
                final_map[y:y_end, x:x_end] = stability
        
        logger.info(f"    Scan complete ({time.time() - start_time:.2f}s)")
        return final_map

    def render_composite(self):
        # 1. Scan Future (Red)
        future_map = self.scan_manifold(direction=1)
        
        # 2. Scan Past (Cyan)
        past_map = self.scan_manifold(direction=-1)
        
        logger.info("[-] Compositing Temporal Interlock...")
        
        # Normalize (Log scale for detail)
        f_norm = np.log1p(future_map)
        f_norm = f_norm / np.max(f_norm)
        
        p_norm = np.log1p(past_map)
        p_norm = p_norm / np.max(p_norm)
        
        # Create Composite Image (R, G, B)
        # Red Channel = Future
        # Blue/Green Channel = Past
        
        img = np.zeros((self.h, self.w, 3), dtype=np.float32)
        
        img[:,:,0] = f_norm  # Red
        img[:,:,1] = p_norm * 0.8 # Green (dimmed slightly for cyan look)
        img[:,:,2] = p_norm  # Blue
        
        # Enhance Contrast
        img = np.clip(img * 1.5, 0, 1)
        
        # Add Nozzle Walls overlay
        m_space = np.linspace(self.center_m - self.scale/2, self.center_m + self.scale/2, self.w)
        l_span = (self.scale / self.aspect)
        l_space = np.linspace(self.center_l - l_span/2, self.center_l + l_span/2, self.h)
        M, L = np.meshgrid(m_space, l_space)
        V = 0.5*(M**2 + L**2) + (M**2*L - L**3/3.0)
        boundary_mask = np.abs(V - 1.0/6.0) < 0.002
        img[boundary_mask] = [1, 1, 1] # White walls
        
        plt.imsave(self.filename, img)
        logger.info(f"[+] TWIN DETECTED. Saved to {self.filename}")
        
        # Preview
        plt.figure(figsize=(12, 8))
        plt.imshow(img, origin='lower')
        plt.title("TEMPORAL SYMMETRY TEST: Future (Red) vs Past (Cyan)", color='black')
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    scope = ChronosScope()
    scope.render_composite()