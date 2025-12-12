import numpy as np
import matplotlib.pyplot as plt
import logging
from scipy.optimize import curve_fit

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def henon_heiles_grad(m, l):
    """Gradient of the Hénon–Heiles potential."""
    dV_dm = m + 2*m*l
    dV_dl = l + (m**2 - l**2)
    return np.array([dV_dm, dV_dl])

class ForceLawBiopsy:
    def __init__(self, steps_per_ray=200, max_sim_steps=300):
        self.steps_per_ray = steps_per_ray
        self.max_sim_steps = max_sim_steps
        self.dt = 0.05
        self.kick = 1e-5
        
        # The Three Force Vectors (Normalized directions to saddles)
        # 1. Top (Weak/Red) -> Angle 90 deg
        # 2. Bottom-Right (EM/Gold) -> Angle 330 deg (-30)
        # 3. Bottom-Left (Strong/Teal) -> Angle 210 deg
        
        # Note: Saddles are at distance 1.0 from origin
        self.rays = [
            {"label": "Weak Force (Top/Red)",   "angle": np.pi/2,       "color": "#ff3333"},
            {"label": "EM Force (Right/Gold)",  "angle": -np.pi/6,      "color": "#ffaa00"},
            {"label": "Strong Force (Left/Teal)", "angle": 7*np.pi/6,   "color": "#00cccc"}
        ]

    def measure_tension_at_point(self, m0, l0):
        """
        Releases a 'Reality' and 'Shadow' particle at (m0, l0) and measures divergence.
        """
        # Reality
        ma, la = m0, l0
        pma, pla = 0.0, 0.0
        
        # Shadow
        mb, lb = m0 + self.kick, l0 + self.kick
        pmb, plb = 0.0, 0.0
        
        max_div = 0.0
        
        for _ in range(self.max_sim_steps):
            # Leapfrog A
            ga = henon_heiles_grad(ma, la)
            pma -= 0.5 * self.dt * ga[0]
            pla -= 0.5 * self.dt * ga[1]
            ma += self.dt * pma
            la += self.dt * pla
            ga = henon_heiles_grad(ma, la)
            pma -= 0.5 * self.dt * ga[0]
            pla -= 0.5 * self.dt * ga[1]
            
            # Leapfrog B
            gb = henon_heiles_grad(mb, lb)
            pmb -= 0.5 * self.dt * gb[0]
            plb -= 0.5 * self.dt * gb[1]
            mb += self.dt * pmb
            lb += self.dt * plb
            gb = henon_heiles_grad(mb, lb)
            pmb -= 0.5 * self.dt * gb[0]
            plb -= 0.5 * self.dt * gb[1]
            
            # Measure separation
            dist = np.sqrt((ma-mb)**2 + (la-lb)**2)
            if dist > max_div:
                max_div = dist
                
            # Stop if escaped
            if (ma**2 + la**2) > 20.0:
                break
                
        return np.log(max_div + self.kick)

    def scan_ray(self, ray_data):
        angle = ray_data["angle"]
        # Scan from center (0) almost to the saddle (1.0)
        # We stop at 0.95 to avoid the singularity of the saddle itself
        r_values = np.linspace(0.01, 0.95, self.steps_per_ray)
        tension_values = []
        
        logger.info(f"Scanning {ray_data['label']}...")
        
        for r in r_values:
            m = r * np.cos(angle)
            l = r * np.sin(angle)
            t = self.measure_tension_at_point(m, l)
            tension_values.append(t)
            
        return r_values, np.array(tension_values)

    def run_analysis(self):
        plt.style.use('dark_background')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        results = []

        for ray in self.rays:
            r, tension = self.scan_ray(ray)
            results.append((ray, r, tension))
            
            # Plot raw profile
            ax1.plot(r, tension, color=ray["color"], label=ray["label"], linewidth=2)
            
        # AXIS 1: The Raw Force Profile
        ax1.set_title("The Force Profiles: Tension vs Distance", fontsize=14, color='white')
        ax1.set_xlabel("Distance from Center (r/R_saddle)", fontsize=12)
        ax1.set_ylabel("Manifold Tension (Log Divergence)", fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.2)
        
        # AXIS 2: The Derivative (The Effective 'Force')
        # If Tension is Potential, Derivative is Force. 
        # Or if Tension is Force, this is Impulse. Let's look at the gradient of tension.
        ax2.set_title("Gradient of Instability (The 'Pull')", fontsize=14, color='white')
        
        for ray, r, tension in results:
            # Calculate gradient
            grad = np.gradient(tension, r)
            # Smooth it slightly for visualization
            grad_smooth = np.convolve(grad, np.ones(5)/5, mode='same')
            
            ax2.plot(r, grad_smooth, color=ray["color"], linestyle="--", linewidth=1.5)
            
        ax2.set_xlabel("Distance from Center", fontsize=12)
        ax2.set_ylabel("Change in Tension (d/dr)", fontsize=12)
        ax2.grid(True, alpha=0.2)

        plt.suptitle("Geometric Origin of Forces: Ray Scanning the Three Jets", fontsize=16)
        plt.savefig("force_law_biopsy.png", dpi=150)
        logger.info("Biopsy complete. Saved to 'force_law_biopsy.png'")
        plt.show()

if __name__ == "__main__":
    biopsy = ForceLawBiopsy()
    biopsy.run_analysis()