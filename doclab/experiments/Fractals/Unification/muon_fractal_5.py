import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("HORIZON_PROFILER")

class ManifoldComparator:
    def __init__(self, samples=24000000):
        self.samples = samples
        self.max_radius = 24.0  # We scan out past the Muon's 24-unit limit
        
    def get_proton_flux(self, m, l, vm, vl):
        # PROTON: Standard Hénon-Heiles (Conservative + Friction)
        # Deep Gravity, No Retrograde Pressure
        friction = 0.02
        
        # Gradient
        dm = m + 2 * m * l
        dl = l + m**2 - l**2
        
        # Forces (Gravity + Drag)
        fm = -dm - friction * vm
        fl = -dl - friction * vl
        
        return fm, fl

    def get_muon_flux(self, m, l, vm, vl):
        # MUON: The "Critical Decay" Model
        # Gravity + Retrograde Pressure
        friction = 0.04
        retro_pressure = 0.12 # The expansion force
        
        # Gradient
        dm = m + 2 * m * l
        dl = l + m**2 - l**2
        
        # Forces (Gravity + Drag + Expansion)
        fm = -dm - friction * vm + (retro_pressure * m)
        fl = -dl - friction * vl + (retro_pressure * l)
        
        return fm, fl

    def run_profile(self, particle_type="proton"):
        logger.info(f"[-] Profiling {particle_type.upper()} Geometry...")
        
        # 1. Random Cloud of Probe Particles
        # We scatter them uniformly by area to get a good density reading
        r = np.sqrt(np.random.uniform(0, self.max_radius**2, self.samples))
        theta = np.random.uniform(0, 2*np.pi, self.samples)
        
        m = r * np.cos(theta)
        l = r * np.sin(theta)
        
        # 2. Initial Kick (High Energy Probe)
        kick = 2.0
        vm = kick * np.cos(theta)
        vl = kick * np.sin(theta)
        
        # Initial Kinetic Energy
        ke_start = 0.5 * (vm**2 + vl**2)
        
        # 3. Short Integration (Measure Instantaneous Flux)
        dt = 0.05
        steps = 50
        
        for t in range(steps):
            if particle_type == "proton":
                fm, fl = self.get_proton_flux(m, l, vm, vl)
            else:
                fm, fl = self.get_muon_flux(m, l, vm, vl)
                
            vm += fm * dt
            vl += fl * dt
            m += vm * dt
            l += vl * dt
            
        # 4. Final Energy & Radius
        ke_end = 0.5 * (vm**2 + vl**2)
        flux = ke_end - ke_start
        final_r = np.sqrt(m**2 + l**2)
        
        return final_r, flux

    def analyze(self):
        # Run Simulations
        r_p, flux_p = self.run_profile("proton")
        r_m, flux_m = self.run_profile("muon")
        
        logger.info("[-] Computing Radial Density Profiles...")
        
        # Binning the data by Radius
        bins = np.linspace(0, self.max_radius, 200)
        bin_centers = 0.5 * (bins[1:] + bins[:-1])
        
        # Calculate Mean Flux per Bin
        # We verify stability: Negative = Stable, Positive = Decaying
        mean_flux_p, _, _ = binned_statistic_safe(r_p, flux_p, bins)
        mean_flux_m, _, _ = binned_statistic_safe(r_m, flux_m, bins)
        
        # Smooth the lines for readability
        smooth_p = gaussian_filter1d(mean_flux_p, sigma=2)
        smooth_m = gaussian_filter1d(mean_flux_m, sigma=2)
        
        self.plot_comparison(bin_centers, smooth_p, smooth_m)

    def plot_comparison(self, r, p_flux, m_flux):
        fig, ax = plt.subplots(figsize=(14, 8), facecolor='#0b0b0b')
        ax.set_facecolor('#0b0b0b')
        
        # Zero Line (The Stability Horizon)
        ax.axhline(0, color='white', linestyle='--', linewidth=1, alpha=0.5)
        
        # PLOT 1: PROTON (The Anchor)
        ax.plot(r, p_flux, color='#00ccff', linewidth=3, label='Proton (Stable Core)')
        ax.fill_between(r, p_flux, 0, where=(p_flux < 0), color='#00ccff', alpha=0.1)
        
        # PLOT 2: MUON (The Decay)
        # We look for the "Crossover" where it goes from Blue (Stable) to Red (Unstable)
        ax.plot(r, m_flux, color='#ffaa00', linewidth=3, label='Muon (Retrograde Decay)')
        
        # Highlight the Positive Flux Zone (Decay Mode)
        ax.fill_between(r, m_flux, 0, where=(m_flux > 0), color='#ffaa00', alpha=0.3)
        ax.fill_between(r, m_flux, 0, where=(m_flux < 0), color='#004488', alpha=0.1)
        
        # Annotation: The 24-Unit Horizon
        ax.axvline(24, color='#ff0000', linestyle=':', linewidth=2)
        ax.text(24.5, max(m_flux)*0.8, "r=24 Units\n(Observed Muon Boundary)", color='#ff0000', fontsize=12)
        
        # Annotation: The 8-Unit Core
        ax.axvline(8, color='#00ccff', linestyle=':', linewidth=2)
        ax.text(8.5, min(p_flux)*0.8, "r=8 Units\n(Proton Core)", color='#00ccff', fontsize=12)

        ax.set_xlabel("Radius (Units)", color='white', fontsize=12)
        ax.set_ylabel("Net Energy Flux (Negative=Stable, Positive=Decay)", color='white', fontsize=12)
        ax.set_title("COMPARATIVE MANIFOLD STABILITY: PROTON vs MUON", color='white', fontsize=16)
        
        ax.tick_params(colors='white')
        ax.legend(facecolor='#111111', labelcolor='white')
        ax.grid(color='#333333', linestyle=':', linewidth=0.5)
        
        plt.tight_layout()
        plt.savefig("manifold_stability_profile.png", dpi=150)
        logger.info("[+] Comparison Saved: 'manifold_stability_profile.png'")
        plt.show()

# Helper for binning without scipy.stats dependency if needed, 
# but using numpy digitize is cleaner for custom averaging
def binned_statistic_safe(x, values, bins):
    # Digitize indices
    bin_indices = np.digitize(x, bins)
    
    bin_means = []
    for i in range(1, len(bins)):
        mask = (bin_indices == i)
        if np.any(mask):
            bin_means.append(np.mean(values[mask]))
        else:
            bin_means.append(0.0) # No data in bin
            
    return np.array(bin_means), bins, bin_indices

if __name__ == "__main__":
    comp = ManifoldComparator(samples=1000000)
    comp.analyze()