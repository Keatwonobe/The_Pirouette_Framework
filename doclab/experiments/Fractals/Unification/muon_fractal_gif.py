import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import matplotlib.animation as animation
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("MUON_ANIMATOR")

class MuonFluxAnimator:
    def __init__(self, resolution=600, zoom=0.0026, steps=100, frames=40):
        self.res = resolution
        self.zoom = zoom
        self.friction = 0.04
        self.retro_pressure = 0.12
        self.initial_kick = 2.0 
        self.max_radius = 60.0 # Ensure it covers the zoom area
        self.steps = steps
        self.frames = frames
        self.dt = 0.05
        
        # Frame capture interval
        self.capture_interval = max(1, self.steps // self.frames)

    def get_forces(self, m, l, vm, vl):
        # 1. Hénon-Heiles Conservative Gradient (Gravity)
        d_pot_m = m + 2 * m * l
        d_pot_l = l + m**2 - l**2
        
        # 2. Friction (Opposes Velocity) - The Sink
        f_drag_m = -self.friction * vm
        f_drag_l = -self.friction * vl
        
        # 3. Retrograde Expansion (Radial Repulsion) - The Source
        f_exp_m = self.retro_pressure * m
        f_exp_l = self.retro_pressure * l
        
        # Net Force
        fm = -d_pot_m + f_drag_m + f_exp_m
        fl = -d_pot_l + f_drag_l + f_exp_l
        
        return fm, fl

    def generate_animation(self):
        logger.info(f"[-] Initializing Animation Sequence ({self.res}x{self.res})...")
        
        # 1. Grid Setup
        x = np.linspace(-self.zoom, self.zoom, self.res)
        y = np.linspace(-self.zoom, self.zoom, self.res)
        M, L = np.meshgrid(x, y)
        
        # 2. High Energy Initialization
        angles = np.arctan2(L, M)
        vm = self.initial_kick * np.cos(angles)
        vl = self.initial_kick * np.sin(angles)
        
        m, l = M.copy(), L.copy()
        
        # Energy Tracking
        initial_ke = 0.5 * (vm**2 + vl**2)
        active = np.ones_like(m, dtype=bool) 
        
        # Setup Figure
        fig, ax = plt.subplots(figsize=(10, 10), facecolor='#0b0b0b')
        ax.axis('off')
        
        # Colormap
        colors = ["#001133", "#004488", "#000000", "#cc4400", "#ffcc00"]
        nodes = [0.0, 0.45, 0.5, 0.55, 1.0]
        cmap_flux = LinearSegmentedColormap.from_list("flux_war", list(zip(nodes, colors)))
        
        ims = []
        
        logger.info("[-] Simulating and Capturing Frames...")
        
        for t in range(self.steps):
            # Update Physics
            if np.any(active):
                m_act, l_act, vm_act, vl_act = m[active], l[active], vm[active], vl[active]
                fm, fl = self.get_forces(m_act, l_act, vm_act, vl_act)
                
                vm[active] += fm * self.dt
                vl[active] += fl * self.dt
                m[active] += vm[active] * self.dt
                l[active] += vl[active] * self.dt
                
                # Check bounds
                r_sq = m[active]**2 + l[active]**2
                escaped = (r_sq > self.max_radius**2) | (~np.isfinite(r_sq))
                
                # Deactivate escaped
                current_indices = np.where(active)
                m_esc = current_indices[0][escaped]
                l_esc = current_indices[1][escaped]
                active[m_esc, l_esc] = False
            
            # Capture Frame
            if t % self.capture_interval == 0 or t == self.steps - 1:
                # Calculate Flux
                v_sq = vm**2 + vl**2
                v_sq = np.nan_to_num(v_sq, nan=self.initial_kick**2, posinf=1e6, neginf=1e6)
                final_ke = 0.5 * v_sq
                flux_map = final_ke - initial_ke
                flux_map[~np.isfinite(flux_map)] = 0.0
                
                # Plot
                max_val = np.nanmax(np.abs(flux_map))
                if max_val < 0.1: max_val = 0.1 # Prevent div/0 for empty frames
                
                norm = TwoSlopeNorm(vmin=-max_val, vcenter=0, vmax=max_val)
                im = ax.imshow(flux_map, origin='lower', cmap=cmap_flux, norm=norm,
                               extent=[-self.zoom, self.zoom, -self.zoom, self.zoom], animated=True)
                
                # Add text annotation for step
                text = ax.text(0.02, 0.02, f"Time Step: {t}", transform=ax.transAxes, color='white')
                
                ims.append([im, text])
                
        # Create Animation
        logger.info(f"[-] Compiling {len(ims)} frames into GIF...")
        ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)
        
        ani.save('muon_genesis.gif', writer='pillow', fps=15)
        logger.info("[+] Animation Saved: 'muon_genesis.gif'")

if __name__ == "__main__":
    animator = MuonFluxAnimator(resolution=500, zoom=26.0, steps=120, frames=40)
    animator.generate_animation()