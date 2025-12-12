import numpy as np
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class AnalyticalSpireArchitect:
    def __init__(self, resolution=1000, zoom=0.001):
        """
        THE ANALYTICAL ARCHITECT
        Generates the Fractal Spire using "Reverse Orbital" laws 
        instead of brute-force integration.
        """
        self.res = resolution
        self.zoom = zoom
        
        # --- THE ORBITAL CONSTANTS ---
        # These define the "Personality" of the Pirouette.
        # Lambda: How fast it pushes you away (The "Reverse Gravity" strength)
        self.lyapunov_lambda = 0.5 
        
        # Omega: How fast it spins while pushing (The "Angular Momentum")
        self.angular_omega = 2.0   
        
    def calculate_spire(self):
        logger.info(f"Architecting Spire at {self.res}x{self.res} (Zoom: {self.zoom})")
        
        # 1. The Coordinate Grid (Centered on the Singularity)
        x = np.linspace(-self.zoom, self.zoom, self.res)
        y = np.linspace(-self.zoom, self.zoom, self.res)
        X, Y = np.meshgrid(x, y)
        
        # 2. Convert to Polar Coordinates (The natural language of orbits)
        # r = Distance from the "Perfect Spine"
        r = np.sqrt(X**2 + Y**2)
        theta = np.arctan2(Y, X)
        
        # 3. THE ANALYTICAL "REVERSE ORBIT" FORMULA
        # Instead of simulating, we solve for Time (Z-Level).
        
        # Formula: The closer you are to r=0, the longer you stay.
        # The relationship is logarithmic.
        # We add a small epsilon to r to avoid log(0)
        
        logger.info("Applying Logarithmic Decoherence Law...")
        
        # T_escape = (1 / lambda) * ln(1 / r)
        # This gives us the exact Z-level for every pixel instantly.
        escape_time = (1.0 / self.lyapunov_lambda) * np.log(1.0 / (r + 1e-20))
        
        # 4. Determine the Basin (The Color)
        # As the particle spirals out, its angle changes over time.
        # Final Angle = Initial Angle + (Rotation Speed * Time)
        final_theta = theta + (self.angular_omega * escape_time)
        
        # Normalize angle to 0-2PI for coloring
        phase = np.mod(final_theta, 2*np.pi)
        
        return escape_time, phase

    def render_blueprint(self):
        z_map, phase_map = self.calculate_spire()
        
        fig, axes = plt.subplots(1, 2, figsize=(20, 10), facecolor='#0f0f0f')
        
        # PLOT 1: The Time Topography (The Spire Height)
        # We mask the center where Z goes to infinity
        masked_z = np.ma.masked_where(z_map > np.percentile(z_map, 99.5), z_map)
        
        im1 = axes[0].imshow(masked_z, origin='lower', cmap='inferno')
        axes[0].set_title("Predicted Decoherence Time (Analytical Z)", color='white')
        axes[0].axis('off')
        
        # PLOT 2: The Phase Map (The Basins)
        # This shows the spiraling arms exactly as they mathematically exist
        im2 = axes[1].imshow(phase_map, origin='lower', cmap='hsv')
        axes[1].set_title("Projected Basin Destination (Phase)", color='white')
        axes[1].axis('off')
        
        plt.suptitle(f"The 'Reverse Orbital' Approximation (Zoom={self.zoom})", color='white', fontsize=16)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # We can zoom in insanely close because we aren't limited by step size.
    # Try zoom=1e-10 (Quantum scale) and it still works instantly.
    architect = AnalyticalSpireArchitect(resolution=1000, zoom=1e-5)
    architect.render_blueprint()