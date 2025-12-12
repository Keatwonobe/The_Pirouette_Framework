import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("CHANNEL_SOLVER")

class ChannelTopologySolver:
    def __init__(self, lobes=3, cycles=1):
        self.lobes = lobes
        self.cycles = cycles
        self.dt = 0.005
        
        # --- GEOMETRY ---
        self.r_singularity = 0.2  # The Switch Point
        self.r_boundary = 12.0    # The Edge of the System
        
        # --- POTENTIAL PARAMETERS ---
        # The "Depth" of the channels
        self.channel_strength = 2.5 
        
        # Dissipation (Friction) for the Proton to settle into the groove
        self.friction_in = 0.04  
        
        # "Negative Pressure" (Acceleration) for the Muon to blast out
        self.pressure_out = 0.02 

    def get_forces(self, m, l, phase):
        """
        Calculates forces based on a Split-Topology:
        - Radial Force (Attract vs Repel)
        - Angular Force (Always Confine)
        """
        r_sq = m**2 + l**2
        r = np.sqrt(r_sq)
        if r < 1e-6: r = 1e-6
        
        theta = np.arctan2(l, m)
        
        # --- 1. ANGULAR CONFINEMENT (The Channel Walls) ---
        # We want distinct valleys at angles 2*pi*k / lobes.
        # Potential V_ang ~ -cos(n * theta)
        # Force F_theta ~ -dV/dtheta ~ -sin(n * theta)
        
        # Calculate torque to push particle towards the nearest valley center
        # The valley is where cos(n*theta) is MAX (1).
        # We want a restoring force towards these angles.
        torque = -self.channel_strength * np.sin(self.lobes * theta)
        
        # Convert Torque to Cartesian Forces
        # F_tangential = torque / r
        # Fx = -F_tan * sin(theta)
        # Fy = F_tan * cos(theta)
        f_tan = torque / r
        fx_channel = -f_tan * np.sin(theta)
        fy_channel = f_tan * np.cos(theta)
        
        # --- 2. RADIAL DYNAMICS (The Gravity/Railgun) ---
        if phase == "PROTON":
            # Attractive Core (Gravity)
            # F_r = -r
            fr = -r
            
        elif phase == "MUON":
            # Repulsive Core (Dark Energy / Railgun)
            # F_r = +r (Exponential expansion)
            # We want it to accelerate out.
            fr = 1.5 * r 
            
        fx_radial = fr * np.cos(theta)
        fy_radial = fr * np.sin(theta)
        
        # Combine
        fx = fx_radial + fx_channel
        fy = fy_radial + fy_channel
        
        return fx, fy

    def solve_trajectory(self):
        logger.info(f"[-] SOLVING CHANNEL TOPOLOGY ({self.lobes}-Fold Symmetry)...")
        
        # We simulate ONE distinct event: In -> Switch -> Out
        
        # HISTORY ARRAYS
        proton_path = []
        muon_path = []
        
        # --- PHASE 1: PROTON (The Carver) ---
        # Start at the boundary, slightly off-axis to force it to "find" a channel
        start_angle = 0.5  # Offset to ensure it spirals in
        m = self.r_boundary * np.cos(start_angle)
        l = self.r_boundary * np.sin(start_angle)
        vm, vl = 0.0, 0.0
        
        phase = "PROTON"
        step = 0
        max_steps = 100000
        
        logger.info("    [1/2] Proton Phase: Carving the Wound...")
        while step < max_steps:
            r = np.sqrt(m**2 + l**2)
            
            # Record
            if step % 5 == 0:
                proton_path.append([m, l])
            
            # Switch Condition: Hit the Singularity
            if r < self.r_singularity:
                logger.info("          <Singularity Reached>")
                break
            
            # Physics
            fx, fy = self.get_forces(m, l, phase)
            
            # Friction (Drag) is essential for the Proton to "fall"
            fx -= self.friction_in * vm
            fy -= self.friction_in * vl
            
            # Integrate
            vm += fx * self.dt
            vl += fy * self.dt
            m += vm * self.dt
            l += vl * self.dt
            step += 1
            
        # --- PHASE 2: MUON (The Exiter) ---
        # We start exactly where the Proton died.
        # But we enter "Negative Potential Mode" (Repulsive Radial, Attractive Angular)
        phase = "MUON"
        step = 0
        
        # Nudge it slightly outward to prevent getting stuck in the exact center 0,0
        m *= 1.1
        l *= 1.1
        
        # Reset velocity? 
        # Option A: Keep Proton momentum (Flyby). 
        # Option B: Stop and explode (Big Bang). 
        # Let's preserve a fraction of momentum to show continuity ("The Loop").
        vm *= 0.5
        vl *= 0.5
        
        logger.info("    [2/2] Muon Phase: Exiting via Wound Channel...")
        while step < max_steps:
            r = np.sqrt(m**2 + l**2)
            
            if step % 5 == 0:
                muon_path.append([m, l])
            
            # Exit Condition: Left the system
            if r > self.r_boundary * 1.2:
                break
                
            # Physics
            fx, fy = self.get_forces(m, l, phase)
            
            # No Friction for Muon? Or "Negative Friction" (Acceleration)?
            # Let's add slight drag to keep the railgun from calculating NaNs (Inf speed)
            # But mostly we let the Radial Force drive it.
            fx -= 0.01 * vm 
            fy -= 0.01 * vl
            
            vm += fx * self.dt
            vl += fy * self.dt
            m += vm * self.dt
            l += vl * self.dt
            step += 1

        return np.array(proton_path), np.array(muon_path)

    def render(self):
        p_path, m_path = self.solve_trajectory()
        
        logger.info("[-] Rendering Geometric Solution...")
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='#050505')
        
        # 1. VISUALIZE THE POTENTIAL FIELD (Background)
        grid_limit = self.r_boundary * 1.1
        x = np.linspace(-grid_limit, grid_limit, 200)
        y = np.linspace(-grid_limit, grid_limit, 200)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        THETA = np.arctan2(Y, X)
        
        # Visualize the "Channels" (where angular potential is low)
        # V_ang ~ -cos(n*theta)
        # We plot the "Valley Depth"
        Z = -np.cos(self.lobes * THETA)
        
        # Contour: Faint guidelines
        ax.contourf(X, Y, Z, levels=20, cmap='gray', alpha=0.15)
        
        # 2. PLOT PROTON (The Wound Carver) - CYAN
        # Fade it out as it gets to the center (Time passing)
        if len(p_path) > 1:
            points_p = p_path.reshape(-1, 1, 2)
            segments_p = np.concatenate([points_p[:-1], points_p[1:]], axis=1)
            
            # Gradient: Bright entering, Dark ending
            cmap_p = LinearSegmentedColormap.from_list("proton", ["#00ffff", "#004444"])
            lc_p = LineCollection(segments_p, cmap=cmap_p, norm=plt.Normalize(0, len(p_path)))
            lc_p.set_array(np.arange(len(p_path))) # Color by time
            lc_p.set_linewidth(1.5)
            lc_p.set_alpha(0.8)
            ax.add_collection(lc_p)

        # 3. PLOT MUON (The Channel Exit) - MAGENTA/RED
        # Bright exploding from center, fading out
        if len(m_path) > 1:
            points_m = m_path.reshape(-1, 1, 2)
            segments_m = np.concatenate([points_m[:-1], points_m[1:]], axis=1)
            
            # Gradient: White/Hot center -> Magenta edge
            cmap_m = LinearSegmentedColormap.from_list("muon", ["#ffffff", "#ff00ff", "#550055"])
            lc_m = LineCollection(segments_m, cmap=cmap_m, norm=plt.Normalize(0, len(m_path)))
            lc_m.set_array(np.arange(len(m_path)))
            lc_m.set_linewidth(2.0) # Thicker (High Energy)
            lc_m.set_alpha(0.9)
            ax.add_collection(lc_m)

        ax.set_xlim(-grid_limit, grid_limit)
        ax.set_ylim(-grid_limit, grid_limit)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Annotations
        ax.set_title(f"GEOMETRIC SOLVER: CHANNEL EXIT\nSymmetry: {self.lobes} | In (Cyan) -> Singularity -> Out (Magenta)", 
                     color='white', fontsize=14)
        
        plt.tight_layout()
        plt.savefig("muon_channel_solution.png", dpi=150)
        logger.info("[+] Solution Saved: 'muon_channel_solution.png'")
        plt.show()

if __name__ == "__main__":
    # 3-Fold Symmetry (Triangle Channels)
    solver = ChannelTopologySolver(lobes=3)
    solver.render()