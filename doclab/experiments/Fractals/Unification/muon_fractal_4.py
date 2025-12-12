import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("FLUX_SCANNER")

class MuonFluxScanner:
    def __init__(self, resolution=1000, zoom=2.0):
        """
        THE FLUX SCANNER (FIXED)
        Maps the energy exchange rate of the manifold.
        """
        self.res = resolution
        self.zoom = zoom
        self.friction = 0.04
        self.retro_pressure = 0.12
        self.initial_kick = 2.0 
        self.max_radius = 10.0 # New boundary condition
        self.steps = 100
        self.dt = 0.05

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
        # Note: Potential gradient (d_pot) is dV/dr, Force is -dV/dr
        fm = -d_pot_m + f_drag_m + f_exp_m
        fl = -d_pot_l + f_drag_l + f_exp_l
        
        return fm, fl

    def run_scan(self):
        logger.info(f"[-] Charging Flux Capacitors ({self.res}x{self.res})...")
        
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
        
        # Active particle mask
        active = np.ones_like(m, dtype=bool) 
        
        logger.info("[-] Dropping particles...")
        
        for t in range(self.steps):
            if not np.any(active): 
                logger.info("    All particles stabilized or escaped.")
                break
            
            # 1. Integration on active particles
            m_act, l_act, vm_act, vl_act = m[active], l[active], vm[active], vl[active]
            
            # --- Verlet Step ---
            fm, fl = self.get_forces(m_act, l_act, vm_act, vl_act)
            
            # Update velocity
            vm[active] += fm * self.dt
            vl[active] += fl * self.dt
            
            # Update position
            m[active] += vm[active] * self.dt
            l[active] += vl[active] * self.dt
            
            # 2. Check for freezing/deactivation (Stability/Robustness Fix)
            r_sq = m[active]**2 + l[active]**2
            
            # Identify particles that should be deactivated (escaped OR exploded)
            escaped_or_exploded = (r_sq > self.max_radius**2) | (~np.isfinite(r_sq))
            
            # Get the global indices of the particles to be deactivated
            global_indices = np.where(active)
            
            # Use the subset filter to find which global indices to set to False
            m_to_deactivate = global_indices[0][escaped_or_exploded]
            l_to_deactivate = global_indices[1][escaped_or_exploded]

            # Update the main active mask
            active[m_to_deactivate, l_to_deactivate] = False

        # 3. Calculate Final Flux
        # We need to calculate final KE for all particles, including those that exploded.
        # However, we must ensure KE is finite for the calculation.
        
        # We cap the kinetic energy to prevent overflow issues during final KE calculation
        # This will still result in high delta_energy but will be finite.
        v_sq = vm**2 + vl**2
        v_sq = np.nan_to_num(v_sq, nan=self.initial_kick**2, posinf=1e6, neginf=1e6)
        
        final_ke = 0.5 * v_sq
        delta_energy = final_ke - initial_ke
        
        # Crucial step: Mask non-finite results (which should be handled by nan_to_num but safer to re-check)
        delta_energy[~np.isfinite(delta_energy)] = np.nan 

        return delta_energy

    def render(self):
        flux_map = self.run_scan()
        
        logger.info("[-] Visualizing Thermodynamics...")
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='#0b0b0b')
        
        # 1. Calculate max_val safely, ignoring NaNs (Robustness Fix)
        # We calculate the max using nanmax
        max_val = np.nanmax(np.abs(flux_map))
        
        # 2. Handle map failure gracefully
        if not np.isfinite(max_val) or max_val == 0.0:
            logger.error("Map is entirely non-finite or zero. Cannot normalize.")
            ax.set_title("MUON FLUX MANIFOLD (ERROR: NO VALID DATA)", color='red')
            plt.tight_layout()
            plt.savefig("muon_flux_map_error.png", dpi=150)
            return

        # COLORMAP: "Thermodynamic War"
        colors = ["#001133", "#004488", "#000000", "#cc4400", "#ffcc00"]
        nodes = [0.0, 0.45, 0.5, 0.55, 1.0]
        cmap_flux = LinearSegmentedColormap.from_list("flux_war", list(zip(nodes, colors)))
        
        # Apply normalization, centered at 0
        norm = TwoSlopeNorm(vmin=-max_val, vcenter=0, vmax=max_val)
        
        # Use np.ma.masked_invalid to mask out the NaNs for plotting (Robustness Fix)
        plot_data = np.ma.masked_invalid(flux_map)

        im = ax.imshow(plot_data, origin='lower', cmap=cmap_flux, norm=norm,
                       extent=[-self.zoom, self.zoom, -self.zoom, self.zoom])
        
        # Add a colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Net Energy Flux ($\Delta E$)', color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
        
        # Add contours to show the "Zero Flux" boundary (The Event Horizon)
        ax.contour(plot_data, levels=[0], colors='white', linewidths=0.5, alpha=0.3,
                   extent=[-self.zoom, self.zoom, -self.zoom, self.zoom])
        
        ax.set_title("MUON FLUX MANIFOLD\nBlue = Energy Sink (Stability) | Gold = Energy Source (Decay)", 
                     color='white', fontsize=14)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig("muon_flux_map_fixed.png", dpi=150)
        logger.info("[+] Map generated: 'muon_flux_map_fixed.png'")

if __name__ == "__main__":
    scanner = MuonFluxScanner(resolution=1000, zoom=1150)
    scanner.render()