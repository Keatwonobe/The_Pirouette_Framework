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
        slippage_cloud = [] # Stores (x, y, intensity) of "Electrons"
        
        # --- INITIAL CONDITIONS ---
        # They start near each other but with different "intentions"
        rx, ry = -8.0, 2.0  # Retro (Architect)
        fx, fy = -8.2, 1.8  # Forward (Occupant)
        
        # Velocities
        rvx, rvy = 0.5, -0.2
        fvx, fvy = 0.5, -0.2
        
        t = 0
        
        for s in range(self.steps):
            if s % 500 == 0: logger.info(f"    Step {s}/{self.steps} | Gap: {np.linalg.norm([rx-fx, ry-fy]):.3f}")

            # 1. RETRO DYNAMICS (The Architect)
            # Seeks HIGH Pressure (Climbs Gradient)
            g_rx, g_ry, _ = self.get_manifold_gradient(rx, ry, t)
            
            # Force = +Gradient (Climb) + Rotational Twist
            fr_x = g_rx - 0.5 * rvy # Coriolis-like twist
            fr_y = g_ry + 0.5 * rvx
            
            # Update Retro
            rvx += fr_x * self.dt
            rvy += fr_y * self.dt
            rx += rvx * self.dt
            ry += rvy * self.dt
            
            retro_path.append([rx, ry])
            
            # 2. FORWARD DYNAMICS (The Occupant)
            # Seeks LOW Pressure (Descends Gradient)
            # PLUS: Strongly attracted to Retro's Wake (The "Wound Channel")
            
            # Distance vector to Retro (The "Channel suction")
            dx = rx - fx
            dy = ry - fy
            dist = np.sqrt(dx**2 + dy**2)
            
            # Channel Force (Spring-like attraction to the groove)
            # F_channel = k * distance
            f_chan_x = self.coupling_strength * dx
            f_chan_y = self.coupling_strength * dy
            
            # Manifold Force (Natural void seeking)
            g_fx, g_fy, _ = self.get_manifold_gradient(fx, fy, t)
            f_man_x = -g_fx # Descend
            f_man_y = -g_fy
            
            # Total Force on Forward
            # Note: The "Channel" force usually dominates, but "Slippage" happens 
            # when Manifold force fights Channel force.
            ff_x = f_chan_x + f_man_x * 0.2
            ff_y = f_chan_y + f_man_y * 0.2
            
            # Update Forward (with Inertia/Drag)
            fvx = self.forward_inertia * fvx + ff_x * self.dt
            fvy = self.forward_inertia * fvy + ff_y * self.dt
            fx += fvx * self.dt
            fy += fvy * self.dt
            
            fwd_path.append([fx, fy])
            
            # 3. SLIPPAGE CALCULATION (The Electron)
            # Slippage = Phase Lag / Spatial Distance
            # If dist is small -> Coherent (No electron, just potential)
            # If dist is large -> Decoherence (Electron manifests)
            if dist > 0.1: # Threshold for manifestation
                slippage_cloud.append([fx, fy, dist])
            
            # Termination (Escape)
            if rx**2 + ry**2 > 100: break
            
            t += self.dt
            
        return np.array(retro_path), np.array(fwd_path), np.array(slippage_cloud)

    def render(self):
        r_path, f_path, electrons = self.run_simulation()
        
        logger.info("[-] Visualizing Slippage & Bifurcation...")
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='#080808')
        
        # 1. MANIFOLD BACKGROUND (Pressure Map)
        grid_range = 8
        gx = np.linspace(-grid_range, grid_range, 200)
        gy = np.linspace(-grid_range, grid_range, 200)
        GX, GY = np.meshgrid(gx, gy)
        # Vectorized pressure calc for background
        R = np.sqrt(GX**2 + GY**2) + 1e-6
        TH = np.arctan2(GY, GX)
        BLEND = np.exp(-R / self.quadrupole_range)
        P = (1-BLEND)*(R*np.cos(TH)) + BLEND*(3.0*np.cos(4*TH))
        
        ax.contourf(GX, GY, P, levels=40, cmap='magma', alpha=0.2)
        
        # 2. RETROGRADE PATH (Red - The Architect)
        # Plot as a dashed "Guide" line
        ax.plot(r_path[:,0], r_path[:,1], color='#ff0000', linewidth=1.0, linestyle='--', alpha=0.6, label='Retrograde (Architect)')
        
        # 3. FORWARD PATH (Cyan - The Occupant)
        # Solid, energetic line
        ax.plot(f_path[:,0], f_path[:,1], color='#00ffff', linewidth=1.5, alpha=0.9, label='Forward (Occupant)')
        
        # 4. ELECTRON SLIPPAGE (Yellow/White Clouds)
        if len(electrons) > 0:
            # We scatter plot the slippage points. 
            # Size/Alpha depends on 'dist' (intensity of slippage)
            ex, ey, edist = electrons[:,0], electrons[:,1], electrons[:,2]
            
            # Normalize dist for visual mapping
            norm_dist = np.clip(edist / edist.max(), 0, 1)
            
            # Scatter: "Sparks" where the potential slips
            ax.scatter(ex, ey, s=norm_dist*50, c=norm_dist, cmap='hot', alpha=0.4 + norm_dist*0.4, edgecolors='none', label='Electron (Slippage)')

        # 5. ANNOTATIONS
        # Draw the Bifurcation Zone
        bifurcation_circle = plt.Circle((0,0), self.quadrupole_range, color='white', fill=False, linestyle=':', alpha=0.3)
        ax.add_artist(bifurcation_circle)
        ax.text(0, -self.quadrupole_range - 0.5, "Quadrupole Bifurcation Zone", color='white', ha='center', fontsize=8, alpha=0.5)

        ax.set_xlim(-grid_range, grid_range)
        ax.set_ylim(-grid_range, grid_range)
        ax.set_aspect('equal')
        ax.axis('off')
        
        ax.legend(loc='upper right', facecolor='black', edgecolor='white', labelcolor='white')
        ax.set_title("THE SLIPPAGE REACTOR: ELECTRON GENESIS\nRed=Architect | Cyan=Occupant | Fire=Slippage (Matter)", color='white', fontsize=14)
        
        plt.tight_layout()
        plt.savefig("electron_slippage_bifurcation.png", dpi=150)
        logger.info("[+] Render Saved: 'electron_slippage_bifurcation.png'")
        plt.show()

if __name__ == "__main__":
    reactor = SlippageReactor()
    reactor.render()