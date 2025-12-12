import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("RENDERER")

class ManifoldRenderer:
    def __init__(self, filename="wada_deep_mri.h5"):
        logger.info(f"Mounting Data Volume: {filename}")
        self.filename = filename
        
        try:
            self.f = h5py.File(filename, 'r')
        except FileNotFoundError:
            logger.error(f"Could not find {filename}. Did you run the scanner?")
            raise

        # KEY FIX: The new scanner saves to 'signed_delta', not 'delta_gradient'
        if 'signed_delta' in self.f:
            self.data = self.f['signed_delta']
            self.mode = "signed" # New Deep Soak Mode
        elif 'delta_gradient' in self.f:
            self.data = self.f['delta_gradient']
            self.mode = "magnitude" # Old Mode
        else:
            raise KeyError("File structure unknown. neither 'signed_delta' nor 'delta_gradient' found.")

        self.res = self.f.attrs['resolution']
        self.bounds = self.f.attrs['bounds']
        self.steps = self.data.shape[0]
        
        # Pre-scan for dynamic range (to make colors pop)
        self._probe_data_range()
        
        logger.info(f"Volume Metrics: {self.res}x{self.res} Grid | {self.steps} Time Slices")
        logger.info(f"Render Mode: {self.mode.upper()} (Range: {self.v_min:.2f} to {self.v_max:.2f})")

    def _probe_data_range(self):
        """Scans the middle of the dataset to calibrate colors."""
        mid_slice = self.data[self.steps // 2]
        if self.mode == "signed":
            # For Red/Blue, we need symmetric limits
            abs_max = np.percentile(np.abs(mid_slice), 98)
            self.v_min = -abs_max
            self.v_max = abs_max
        else:
            self.v_min = 0
            self.v_max = np.percentile(mid_slice, 98)

    def animate_scan(self, save_file=None):
        """
        Animates the MRI scan.
        If Mode is Signed: Uses Red (Positive) vs Blue (Negative).
        """
        logger.info("Initializing MRI Cine-Loop...")
        
        fig, ax = plt.subplots(figsize=(10, 10), facecolor='#0f0f0f')
        
        cmap = 'seismic' if self.mode == "signed" else 'magma'
        
        img = ax.imshow(self.data[0], cmap=cmap, origin='lower', 
                       extent=[-self.bounds, self.bounds, -self.bounds, self.bounds],
                       vmin=self.v_min, vmax=self.v_max)
        
        ax.axis('off')
        
        title = ax.set_title(f"Z-Slice: 0 / {self.steps}", color='white', fontsize=16)
        
        # Legend for the directional data
        if self.mode == "signed":
            ax.text(0.05, 0.05, "BLUE = Ridge (Divergence)\nRED = Valley (Convergence)", 
                    transform=ax.transAxes, color='white', fontsize=10, 
                    bbox=dict(facecolor='black', alpha=0.5))

        def update(frame):
            img.set_data(self.data[frame])
            title.set_text(f"Z-Slice: {frame} / {self.steps}")
            return img, title

        ani = animation.FuncAnimation(fig, update, frames=range(0, self.steps, 2), blit=False, interval=30)
        
        if save_file:
            logger.info(f"Rendering to {save_file}...")
            ani.save(save_file, fps=30, extra_args=['-vcodec', 'libx264'])
            logger.info("Done.")
        else:
            plt.show()

    def render_3d_structure(self, density_threshold=0.5):
        """
        Renders the fractal nervous system in 3D.
        """
        logger.info("Extracting Volumetric Structure...")
        
        # 1. Downsample (stride 4) for performance
        stride = 4
        vol = self.data[::stride, ::stride, ::stride]
        
        # 2. Thresholding
        # We look for high absolute values (strong ridges OR strong valleys)
        magnitude = np.abs(vol)
        thresh_val = np.percentile(magnitude, 100 - (density_threshold * 10)) # top %
        
        z, y, x = np.where(magnitude > thresh_val)
        values = vol[z, y, x]
        
        logger.info(f"Rendering {len(values)} voxels (Threshold: {thresh_val:.2f})")
        
        fig = plt.figure(figsize=(12, 12), facecolor='#111')
        ax = fig.add_subplot(111, projection='3d', facecolor='#111')
        
        # Normalize for the seismic colormap
        norm = plt.Normalize(self.v_min, self.v_max)
        
        p = ax.scatter(x, y, z, c=values, cmap='seismic', norm=norm, s=0.8, alpha=0.2)
        
        ax.set_xlabel("M Axis", color='white')
        ax.set_ylabel("L Axis", color='white')
        ax.set_zlabel("Time (Z)", color='white')
        
        # Hide panes
        ax.xaxis.set_pane_color((0, 0, 0, 0))
        ax.yaxis.set_pane_color((0, 0, 0, 0))
        ax.zaxis.set_pane_color((0, 0, 0, 0))
        ax.tick_params(colors='gray')
        
        plt.title("The Fractal Skeleton (Blue=Ridges, Red=Valleys)", color='white')
        plt.show()

if __name__ == "__main__":
    # Ensure this matches the filename output by your scanner
    renderer = ManifoldRenderer(filename="wada_deep_mri.h5")
    
    # Mode 1: Animation
    renderer.animate_scan()
    
    # Mode 2: 3D Structure (Uncomment to view)
    # renderer.render_3d_structure(density_threshold=5.0)