import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("SLIPPAGE_REACTOR")

class SlippageReactor:
    def __init__(self):
        self.dt = 0.005
        self.steps = 5000
        
        # --- PHYSICS PARAMETERS ---
        self.coupling_strength = 8.0   # How deep is the "Wound Channel" Red carves?
        self.forward_inertia = 0.95    # Forward momentum conservation
        self.quadrupole_range = 1.5    # Radius where 4-lobe structure dominates
        
    def get_manifold_gradient(self, x, y, time_step):
        """
        The Background Potential.
        Outer: Cardioid/Dipole (2-Lobe).
        Inner: Quadrupole (4-Lobe) - The Fractal Bifurcation.
        """
        r = np.sqrt(x**2 + y**2) + 1e-6
        theta = np.arctan2(y, x)
        
        # 1. Base Potential (The "Manifold Pressure")
        # Retro seeks High P, Forward seeks Low P.
        # We model "Pressure" as density.
        
        # Outer: Dipole (Cardioid-ish)
        # P ~ r * cos(theta)
        p_outer = r * np.cos(theta)
        
        # Inner: Quadrupole (The 4-Lobe Bifurcation)
        # P ~ cos(4 * theta)
        # We blend them based on radius.
        blend = np.exp(-r / self.quadrupole_range)
        p_inner = 3.0 * np.cos(4 * theta + time_step * 0.05) # Rotate slowly
        
        pressure = (1 - blend) * p_outer + blend * p_inner
        
        # Numerical Gradient
        eps = 0.01
        dp_dx = (self.get_pressure_at(x + eps, y, time_step) - self.get_pressure_at(x - eps, y, time_step)) / (2 * eps)
        dp_dy = (self.get_pressure_at(x, y + eps, time_step) - self.get_pressure_at(x, y - eps, time_step)) / (2 * eps)
        
        return dp_dx, dp_dy, pressure

    def get_pressure_at(self, x, y, t):
        r = np.sqrt(x**2 + y**2) + 1e-6
        theta = np.arctan2(y, x)
        blend = np.exp(-r / self.quadrupole_range)
        p_outer = r * np.cos(theta)
        p_inner = 3.0 * np.cos(4 * theta + t * 0.05)
        return (1 - blend) * p_outer + blend * p_inner

    def run_simulation(self):
        logger.info("[-] INITIATING SEQUENTIAL POTENTIAL SOLVER...")
        
        # Arrays for history
        retro_path = []
        fwd_path = []
        slippage_cloud = [] 
        
        # --- NEW HISTORY ARRAYS ---
        gap_history = []
        pressure_history = [] 
        fwd_force_history = []
        # --- END NEW ARRAYS ---
        
        # [Initial Conditions]
        rx, ry = -8.0, 2.0  # Retro (Architect)
        fx, fy = -8.2, 1.8  # Forward (Occupant)
        
        rvx, rvy = 0.5, -0.2
        fvx, fvy = 0.5, -0.2
        
        t = 0
        
        for s in range(self.steps):
            # [Logging]

            # 1. RETRO DYNAMICS
            g_rx, g_ry, r_pressure = self.get_manifold_gradient(rx, ry, t) # <--- GET PRESSURE
            # [Rest of Retro Dynamics]
            
            # 2. FORWARD DYNAMICS
            # [Distance vector to Retro]
            dx = rx - fx
            dy = ry - fy
            dist = np.sqrt(dx**2 + dy**2)
            
            # [Channel Force]
            f_chan_x = self.coupling_strength * dx
            f_chan_y = self.coupling_strength * dy
            
            # [Manifold Force]
            g_fx, g_fy, f_pressure = self.get_manifold_gradient(fx, fy, t) # <--- GET PRESSURE
            f_man_x = -g_fx # Descend
            f_man_y = -g_fy
            
            # Total Force on Forward
            ff_x = f_chan_x + f_man_x * 0.2
            ff_y = f_chan_y + f_man_y * 0.2
            
            # --- RECORD DYNAMICS ---
            gap_history.append(dist)
            pressure_history.append(r_pressure - f_pressure) # Record Pressure Differential
            fwd_force_history.append(np.linalg.norm([ff_x, ff_y]))
            # --- END RECORD ---
            
            # [Update Forward]
            # [Slippage Calculation]
            # [Termination]
            
            t += self.dt
            
        return np.array(retro_path), np.array(fwd_path), np.array(slippage_cloud), np.array(gap_history), np.array(pressure_history), np.array(fwd_force_history)

    def render(self):
        r_path, f_path, electrons, gap_hist, press_diff, fwd_force = self.run_simulation()
        
        logger.info("[-] Visualizing Slippage & Bifurcation...")
        
        # CHANGE: Create a multi-subplot figure (2 rows, 2 columns)
        fig = plt.figure(figsize=(16, 16), facecolor='#080808')
        
        # --- PANEL 1: TRAJECTORY & MANIFOLD (Top-Left) ---
        ax1 = fig.add_subplot(2, 2, 1, facecolor='#080808')
        
        # [Manifold Background Contour]
        grid_range = 8
        gx = np.linspace(-grid_range, grid_range, 200)
        gy = np.linspace(-grid_range, grid_range, 200)
        GX, GY = np.meshgrid(gx, gy)
        
        # Vectorized pressure calc (for background at t=0)
        R = np.sqrt(GX**2 + GY**2) + 1e-6
        TH = np.arctan2(GY, GX)
        BLEND = np.exp(-R / self.quadrupole_range)
        P = (1-BLEND)*(R*np.cos(TH)) + BLEND*(3.0*np.cos(4*TH))
        
        ax1.contourf(GX, GY, P, levels=40, cmap='magma', alpha=0.2)
        ax1.contour(GX, GY, P, levels=10, colors='white', linewidths=0.2, alpha=0.1) # Add lines for structure
        
        # 2. RETROGRADE PATH (Red)
        ax1.plot(r_path[:,0], r_path[:,1], color='#ff0000', linewidth=1.5, linestyle='-', alpha=0.7, label='Architect (Retrograde)')
        
        # 3. FORWARD PATH (Cyan) - Use a gradient for 'energy' or 'slippage'
        if len(f_path) > 1:
            points_f = f_path.reshape(-1, 1, 2)
            segments_f = np.concatenate([points_f[:-1], points_f[1:]], axis=1)
            lc_f = LineCollection(segments_f, cmap='cyan', norm=plt.Normalize(0, 1))
            lc_f.set_array(fwd_force/fwd_force.max()) # Color by force magnitude (Excitation)
            lc_f.set_linewidth(2.0)
            lc_f.set_alpha(1.0)
            ax1.add_collection(lc_f)
        
        # 4. ELECTRON SLIPPAGE (Scatter)
        # [Existing scatter code for electrons]
        if len(electrons) > 0:
            ex, ey, edist = electrons[:,0], electrons[:,1], electrons[:,2]
            norm_dist = np.clip(edist / edist.max(), 0, 1)
            ax1.scatter(ex, ey, s=norm_dist*50, c=norm_dist, cmap='hot', alpha=0.4 + norm_dist*0.4, edgecolors='none', label='Electron (Slippage)')

        # 5. ANNOTATIONS
        bifurcation_circle = plt.Circle((0,0), self.quadrupole_range, color='white', fill=False, linestyle=':', alpha=0.5)
        ax1.add_artist(bifurcation_circle)
        ax1.set_title("SLIPPAGE TRAJECTORY: KNOTTING & DECOHERENCE", color='white', fontsize=12)
        ax1.set_xlim(-grid_range, grid_range)
        ax1.set_ylim(-grid_range, grid_range)
        ax1.set_aspect('equal')
        ax1.axis('off')
        ax1.legend(loc='upper right', facecolor='black', edgecolor='white', labelcolor='white')
        
        
        # --- PANEL 2: GAP DISTANCE (Top-Right) ---
        ax2 = fig.add_subplot(2, 2, 2, facecolor='#080808')
        steps_array = np.arange(len(gap_hist))
        ax2.plot(steps_array, gap_hist, color='lime', linewidth=1.5)
        ax2.set_title("COUPLING DYNAMICS: GAP DISTANCE", color='white', fontsize=12)
        ax2.set_xlabel("Time Step", color='white')
        ax2.set_ylabel("Distance $|r_{Retro} - r_{Fwd}|$", color='white')
        ax2.tick_params(colors='white')
        ax2.grid(True, alpha=0.3)
        
        # --- PANEL 3: PRESSURE DIFFERENTIAL (Bottom-Left) ---
        ax3 = fig.add_subplot(2, 2, 3, facecolor='#080808')
        ax3.plot(steps_array, press_diff, color='magenta', linewidth=1.5)
        ax3.set_title("MANIFOLD DIFFERENTIAL: $\\Delta P$", color='white', fontsize=12)
        ax3.set_xlabel("Time Step", color='white')
        ax3.set_ylabel("Pressure Difference", color='white')
        ax3.tick_params(colors='white')
        ax3.grid(True, alpha=0.3)

        # --- PANEL 4: FORWARD FORCE (Bottom-Right) ---
        ax4 = fig.add_subplot(2, 2, 4, facecolor='#080808')
        ax4.plot(steps_array, fwd_force, color='yellow', linewidth=1.5)
        ax4.set_title("FORWARD FORCE: CHANNEL LOCK-IN $\\rightarrow$ KNOT INTENSITY", color='white', fontsize=12)
        ax4.set_xlabel("Time Step", color='white')
        ax4.set_ylabel("Force Magnitude $|F_{Fwd}|$", color='white')
        ax4.tick_params(colors='white')
        ax4.grid(True, alpha=0.3)

        plt.suptitle("THE SLIPPAGE REACTOR: ELECTRON GENESIS & LOCK-IN ANALYSIS", color='white', fontsize=16)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig("slippage_reactor_analysis_multiplot.png", dpi=150)
        logger.info("[+] Render Saved: 'slippage_reactor_analysis_multiplot.png'")
        # plt.show() # Disabled for production

if __name__ == "__main__":
    reactor = SlippageReactor()
    reactor.render()