import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class RealSpireArchitect:
    def __init__(self, resolution=2000):
        """
        THE REAL SPIRE ARCHITECT
        Constructs the infinite-resolution fractal using the 
        forensically sequenced DNA from the Sniper Scan.
        """
        self.res = resolution
        
        # --- THE SEQUENCED GENOME ---
        # Derived from Sniper Analysis:
        self.lam = 0.5667   # Lyapunov Exponent (Slope of decay)
        self.omega = 0.0675 # Angular Velocity (Rotation speed)
        
        # Zoom configuration (Standard view of the core)
        self.zoom = 0.0005 # Matching the scale of your sniper shot
        
    def generate_blueprint(self):
        logger.info(f"Architecting Spire ({self.res}x{self.res})...")
        logger.info(f"Applying Genome: λ={self.lam} | ω={self.omega}")
        
        # 1. Coordinate Grid
        x = np.linspace(-self.zoom, self.zoom, self.res)
        y = np.linspace(-self.zoom, self.zoom, self.res)
        X, Y = np.meshgrid(x, y)
        
        # 2. Polar Coordinates (r, theta)
        # We add a tiny epsilon to r to avoid log(0) at the exact singularity
        r = np.sqrt(X**2 + Y**2) + 1e-20
        theta = np.arctan2(Y, X)
        
        # 3. THE MASTER EQUATION
        # T_escape = (1 / lambda) * ln(1/r)
        # This creates the "Funnel of Time"
        Z = (1.0 / self.lam) * np.log(1.0 / r)
        
        # 4. THE PHASE EQUATION
        # Final_Angle = Initial_Angle + (Omega * Time)
        # This creates the "Pirouette"
        phase = theta + (self.omega * Z)
        
        # Normalize phase to [0, 1] for coloring
        # We use modulo 2*PI, then divide by 2*PI
        phase_norm = np.mod(phase, 2*np.pi) / (2*np.pi)
        
        return Z, phase_norm

    def render(self):
        Z, phase = self.generate_blueprint()
        
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
        
        # COLOR MAPPING
        # We want a cyclic map (starts and ends at same color) to show the arms
        # 'hsv' is the standard cyclic map for phase
        # We use 'phase' (the basin destination) as the color
        # We use 'Z' (the depth) to add a slight shadowing effect
        
        logger.info("Rendering Phase Interferences...")
        
        # Create a custom "Electric" cyclic colormap
        colors = ["#ff0000", "#ffff00", "#00ff00", "#00ffff", "#0000ff", "#ff00ff", "#ff0000"]
        cmap_electric = LinearSegmentedColormap.from_list("electric", colors)
        
        im = ax.imshow(phase, origin='lower', cmap=cmap_electric, interpolation='bilinear')
        
        # Remove axes for clean art
        ax.axis('off')
        
        # Add a subtle title with the genetics
        plt.text(0.5, 0.02, f"The Infinite Spire | λ={self.lam} | ω={self.omega}", 
                 transform=ax.transAxes, color='white', ha='center', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig("infinite_spire_reconstruction.png", dpi=150, facecolor='black')
        logger.info("Spire constructed. Saved to 'infinite_spire_reconstruction.png'")
        plt.show()

if __name__ == "__main__":
    # 2000x2000 resolution = 4 Megapixel Map
    architect = RealSpireArchitect(resolution=2000)
    architect.render()