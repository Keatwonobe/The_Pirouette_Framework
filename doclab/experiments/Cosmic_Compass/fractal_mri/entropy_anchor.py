import numpy as np
import matplotlib.pyplot as plt
import logging
from matplotlib.colors import LinearSegmentedColormap

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("ANCHOR")

class EntropyAnchor:
    def __init__(self, resolution=1000, damping=0.015):
        """
        THE ENTROPY ANCHOR
        Maps the 'Cold' structure of the fractal by robbing particles of energy.
        
        damping: The friction coefficient (The rate of energy theft).
        """
        self.res = resolution
        self.gamma = damping # Friction
        self.dt = 0.05
        self.max_steps = 3000
        self.bounds = 1.5 # Viewing the central well
        
    def gradient(self, m, l):
        # Hénon-Heiles Potential Gradient
        dm = m + 2 * m * l
        dl = l + (m**2 - l**2)
        return dm, dl

    def run_sedimentation(self):
        logger.info(f"[-] FREEZING THE CHAOS ({self.res}x{self.res})...")
        logger.info(f"[-] Friction Coefficient: {self.gamma}")
        
        # 1. Initialize Grid (High Energy Start)
        m_vals = np.linspace(-self.bounds, self.bounds, self.res)
        l_vals = np.linspace(-self.bounds, self.bounds, self.res)
        M, L = np.meshgrid(m_vals, l_vals)
        
        # Velocity starts at zero, but Potential Energy is high at the edges
        m, l = M.copy(), L.copy()
        vm = np.zeros_like(m)
        vl = np.zeros_like(l)
        
        # Metric: ORBITAL LIFETIME
        # We count how much distance they cover before stopping.
        # High distance = Stable Orbit (Resonance)
        # Low distance = Immediate Crash
        orbit_length = np.zeros_like(m, dtype=np.float32)
        active = np.ones_like(m, dtype=bool)
        
        # Integration Loop (Dissipative)
        for t in range(self.max_steps):
            if t % 500 == 0:
                active_count = np.sum(active)
                logger.info(f"    Step {t}/{self.max_steps} | Active Orbiters: {active_count}")
                if active_count == 0: break
            
            # 1. Calculate Force
            grad_m, grad_l = self.gradient(m, l)
            
            # 2. Update Velocity with DAMPING
            # v_new = v_old + (Force - Friction*v_old) * dt
            vm[active] += (-grad_m[active] - self.gamma * vm[active]) * self.dt
            vl[active] += (-grad_l[active] - self.gamma * vl[active]) * self.dt
            
            # 3. Update Position
            m[active] += vm[active] * self.dt
            l[active] += vl[active] * self.dt
            
            # 4. Measure "Life" (Distance Traveled this step)
            # This captures the "Swirl"
            speed = np.sqrt(vm[active]**2 + vl[active]**2)
            orbit_length[active] += speed
            
            # 5. Check "Death" (Stop condition)
            # If speed is near zero, they have settled (frozen)
            # OR if they escaped the bounds (drifted away)
            stopped = (speed < 0.01)
            escaped = (m[active]**2 + l[active]**2 > 10.0)
            
            # Mark inactive
            done_indices = np.where(active)[0] # Flattened trickery required for rigorous vectorization
            # Simplified boolean mask update:
            
            current_active_mask = stopped | escaped
            
            # If we wanted to be perfectly precise we'd index properly, 
            # but for 2D grids, masking is easier:
            # Update the main active mask based on the subset
            active[active] = ~current_active_mask

        return orbit_length

    def render(self):
        data = self.run_sedimentation()
        
        logger.info("[-] Developing Sediment Map...")
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='#050510')
        
        # Log scale to see the faint outer orbits
        plot_data = np.log1p(data)
        
        # Custom "Ice & Bone" Colormap
        # Dark Blue -> Cyan -> White (High stability)
        colors = ["#000000", "#1a0b2e", "#4b276b", "#3b7d85", "#83d8d3", "#ffffff"]
        cmap_bone = LinearSegmentedColormap.from_list("ice_bone", colors)
        
        im = ax.imshow(plot_data, origin='lower', cmap=cmap_bone,
                       extent=[-self.bounds, self.bounds, -self.bounds, self.bounds])
        
        # Overlay the Theoretical Stability Triangle
        m_tri = np.linspace(-self.bounds, self.bounds, 500)
        l_tri = np.linspace(-self.bounds, self.bounds, 500)
        Mt, Lt = np.meshgrid(m_tri, l_tri)
        V = 0.5*(Mt**2 + Lt**2) + (Mt**2*Lt - Lt**3/3.0)
        ax.contour(Mt, Lt, V, levels=[1.0/6.0], colors='white', linewidths=0.8, alpha=0.3)
        
        ax.set_title("THE ENTROPY ANCHOR (Dissipative Structure)", color='#83d8d3', fontsize=16)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig("entropy_anchor.png")
        logger.info("[+] Anchor dropped. Map saved to 'entropy_anchor.png'")
        plt.show()

if __name__ == "__main__":
    # Friction 0.015 is the "Sweet Spot" 
    # Too high = everything stops instantly. 
    # Too low = everything orbits forever.
    anchor = EntropyAnchor(resolution=1000, damping=0.015)
    anchor.render()