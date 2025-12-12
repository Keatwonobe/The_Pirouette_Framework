import numpy as np
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class JetSlicer:
    def __init__(self, resolution=1000):
        """
        THE JET SLICER
        Zooms into the 'Throat' of the Top Exhaust Port (L=1.0).
        Looking for 'Shock Diamonds' and laminar layering.
        """
        self.res = resolution
        self.max_steps = 10000
        self.dt = 0.05
        
        # Focus Window: The Top Saddle Point
        # The saddle is exactly at (0, 1.0).
        # We scan a box around it to see the flow entering the nozzle.
        self.m_range = np.linspace(-0.5, 0.5, self.res)
        self.l_range = np.linspace(0.5, 1.5, self.res) # From inside (0.5) to outside (1.5)
        
    def compute_flow_dynamics(self):
        logger.info(f"[-] Slicing the Jet Plume ({self.res}x{self.res})...")
        
        M, L = np.meshgrid(self.m_range, self.l_range)
        
        # 1. Physics Engine
        # We track 'Time to Escape' to see the density layers
        escape_time = np.zeros_like(M)
        
        # We also track 'Velocity Magnitude' at the moment of crossing L=1.0
        # This helps visualize the kinetic energy of the jet
        # (Simplified: we map initial stability for now)
        
        m_curr = M.copy()
        l_curr = L.copy()
        pm = np.zeros_like(M)
        pl = np.zeros_like(L)
        active = np.ones_like(M, dtype=bool)
        
        # Run Simulation
        for step in range(self.max_steps):
            if step % 1000 == 0:
                logger.info(f"    Integration Step {step}/{self.max_steps}...")
                
            if not np.any(active): break
            
            # Gradients (Henon-Heiles)
            grad_m = m_curr + 2 * m_curr * l_curr
            grad_l = l_curr + (m_curr**2 - l_curr**2)
            
            # Leapfrog A
            pm[active] -= 0.5 * self.dt * grad_m[active]
            pl[active] -= 0.5 * self.dt * grad_l[active]
            
            # Drift
            m_curr[active] += self.dt * pm[active]
            l_curr[active] += self.dt * pl[active]
            
            # Leapfrog B
            grad_m = m_curr + 2 * m_curr * l_curr
            grad_l = l_curr + (m_curr**2 - l_curr**2)
            pm[active] -= 0.5 * self.dt * grad_m[active]
            pl[active] -= 0.5 * self.dt * grad_l[active]
            
            # ESCAPE CONDITION
            # If r > 20, they are gone.
            r2 = m_curr**2 + l_curr**2
            escaped_now = (r2 > 20.0) & active
            
            if np.any(escaped_now):
                escape_time[escaped_now] = step
                active[escaped_now] = False
        
        return escape_time

    def render_biopsy(self):
        data = self.compute_flow_dynamics()
        
        logger.info("[-] Rendering Flow Visualization...")
        
        fig, ax = plt.subplots(figsize=(10, 12), facecolor='#000510')
        
        # LOG SCALE to reveal the shock layers
        # The dynamic range between "instant escape" and "trapped" is huge
        plot_data = np.log1p(data)
        
        # Plot with a 'Fire' map to resemble engine exhaust
        im = ax.imshow(plot_data, origin='lower', cmap='inferno',
                       extent=[self.m_range[0], self.m_range[-1], self.l_range[0], self.l_range[-1]])
        
        # Overlay the Nozzle Geometry
        # The theoretical boundary is Energy = 1/6
        # V(m,l) = 1/6
        m_analytic = np.linspace(-0.5, 0.5, 200)
        l_analytic = np.linspace(0.5, 1.5, 200)
        Ma, La = np.meshgrid(m_analytic, l_analytic)
        V = 0.5*(Ma**2 + La**2) + (Ma**2*La - La**3/3.0)
        
        # Contour the "Walls" of the engine
        ax.contour(Ma, La, V, levels=[1.0/6.0], colors='cyan', linewidths=2, linestyles='--')
        ax.text(0, 1.02, "THROAT (L=1.0)", color='cyan', ha='center', fontsize=10, fontweight='bold')
        
        ax.set_title("JET BIOPSY: Top Exhaust Port", color='orange', fontsize=16)
        ax.set_xlabel("M Axis (Lateral)", color='white')
        ax.set_ylabel("L Axis (Axial)", color='white')
        
        # Add visual markers
        ax.axhline(1.0, color='white', alpha=0.3, linestyle=':')
        
        ax.tick_params(colors='white')
        
        plt.tight_layout()
        plt.savefig("jet_biopsy.png")
        logger.info("[+] Scan saved to 'jet_biopsy.png'")
        plt.show()

if __name__ == "__main__":
    slicer = JetSlicer(resolution=800)
    slicer.render_biopsy()