import numpy as np
import matplotlib.pyplot as plt
import logging
from matplotlib.colors import LinearSegmentedColormap

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("HELICAL_ANCHOR")

class HelicalAnchor:
    def __init__(self, resolution=1000, damping=0.015):
        """
        THE HELICAL ANCHOR
        Maps the 'Helicity' structure of the fractal by tracking the total 
        angle of rotation (Winding Count) instead of distance traveled.
        
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
        logger.info(f"[-] ISOLATING ROTATIONAL MEMORY ({self.res}x{self.res})...")
        logger.info(f"[-] Friction Coefficient: {self.gamma}")
        
        # 1. Initialize Grid (High Energy Start)
        m_vals = np.linspace(-self.bounds, self.bounds, self.res)
        l_vals = np.linspace(-self.bounds, self.bounds, self.res)
        M, L = np.meshgrid(m_vals, l_vals)
        
        # Flatten for computation
        m, l = M.flatten(), L.flatten()
        vm = np.zeros_like(m)
        vl = np.zeros_like(l)
        
        # Metric: TOTAL ANGLE WINDING (Helicity)
        # We count the total absolute angle traversed before stopping.
        total_winding = np.zeros_like(m, dtype=np.float32)
        # Initial angle for all points
        prev_ang = np.arctan2(l, m) 
        active = np.ones_like(m, dtype=bool)
        
        # Integration Loop (Dissipative)
        for t in range(self.max_steps):
            if t % 500 == 0:
                active_count = np.sum(active)
                logger.info(f"    Step {t}/{self.max_steps} | Active Orbiters: {active_count}")
                if active_count == 0: break
            
            # --- Subset to active particles ---
            m_a, l_a, vm_a, vl_a = m[active], l[active], vm[active], vl[active]
            
            # 1. Calculate Force
            grad_m, grad_l = self.gradient(m_a, l_a)
            
            # 2. Update Velocity with DAMPING
            vm_a += (-grad_m - self.gamma * vm_a) * self.dt
            vl_a += (-grad_l - self.gamma * vl_a) * self.dt
            
            # 3. Update Position
            m_a += vm_a * self.dt
            l_a += vl_a * self.dt
            
            # 4. Measure "Life" (Total Angle Winding)
            curr_ang = np.arctan2(l_a, m_a)
            delta = curr_ang - prev_ang[active]
            
            # Vectorized Unwrap: Handles the jump from +pi to -pi (or vice-versa)
            delta = np.where(delta > np.pi, delta - 2*np.pi, delta)
            delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
            
            total_winding[active] += np.abs(delta)
            prev_ang[active] = curr_ang # Update previous angle for next step

            # --- Write back the updated values ---
            m[active], l[active], vm[active], vl[active] = m_a, l_a, vm_a, vl_a
            
            # 5. Check "Death" (Stop condition)
            # If speed is near zero, they have settled (frozen)
            speed = np.sqrt(vm_a**2 + vl_a**2)
            stopped = (speed < 0.01)
            escaped = (m_a**2 + l_a**2 > 10.0)
            
            current_active_mask = stopped | escaped
            active[active] = ~current_active_mask

        return total_winding.reshape(self.res, self.res)

    def render(self):
        data = self.run_sedimentation()
        
        logger.info("[-] Developing Helicity Map...")
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='#050510')
        
        # Log scale to visually enhance the structure of inner spirals
        plot_data = np.log1p(data / (2 * np.pi)) # Normalize to log(1 + Winding Counts)
        
        # Use a cyclic colormap (hsv) to emphasize phase/winding boundaries
        # Magma is also good for intensity, but let's try hsv to distinguish the spirals
        im = ax.imshow(plot_data, origin='lower', cmap='hsv',
                       extent=[-self.bounds, self.bounds, -self.bounds, self.bounds])
        
        # Overlay the Theoretical Stability Triangle
        m_tri = np.linspace(-self.bounds, self.bounds, 500)
        l_tri = np.linspace(-self.bounds, self.bounds, 500)
        Mt, Lt = np.meshgrid(m_tri, l_tri)
        V = 0.5*(Mt**2 + Lt**2) + (Mt**2*Lt - Lt**3/3.0)
        ax.contour(Mt, Lt, V, levels=[1.0/6.0], colors='white', linewidths=0.8, alpha=0.3)
        
        ax.set_title("THE HELICAL ANCHOR (Pure Rotational Memory)", color='cyan', fontsize=16)
        ax.set_xlabel('Mass Field (m)', color='white')
        ax.set_ylabel('Coupling Field (λ)', color='white')
        ax.tick_params(colors='white')
        ax.axis('on')
        
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('log(1 + Total Winding Count)', color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
        
        plt.tight_layout()
        plt.savefig("helical_entropy_anchor.png")
        logger.info("[+] Helicity map saved to 'helical_entropy_anchor.png'")
        plt.show()

if __name__ == "__main__":
    anchor = HelicalAnchor(resolution=1000, damping=0.015)
    anchor.render()