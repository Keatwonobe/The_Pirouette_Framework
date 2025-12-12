import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import logging

# Configure logging to look like a system boot
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("RENDERER")

class ManifoldRenderer:
    def __init__(self, filename="wada_deep_mri.h5"):
        logger.info(f"Mounting Data Volume: {filename}")
        self.filename = filename
        try:
            self.f = h5py.File(filename, 'r')
        except FileNotFoundError:
            logger.error("Volume not found. Run the Scanner first.")
            raise

        # Load Metadata
        self.res = self.f.attrs['resolution']
        self.bounds = self.f.attrs['bounds']
        self.steps = self.f['delta_gradient'].shape[0]
        
        logger.info(f"Volume Metrics: {self.res}x{self.res} Grid | {self.steps} Time Slices")

    def animate_mri_scan(self, save_file=None):
        """
        Creates a side-by-side animation:
        Left: The Raw Divergence (The Chaos)
        Right: The Delta Gradient (The Information Structure)
        """
        logger.info("Initializing MRI Cine-Loop...")
        
        # Setup Figure
        fig, axes = plt.subplots(1, 2, figsize=(16, 8), facecolor='#0f0f0f')
        
        # Pre-load first frame to set limits
        div_0 = self.f['divergence'][0]
        delta_0 = self.f['delta_gradient'][0]
        
        # Color limits (fixed so they don't flicker)
        div_vmax = np.percentile(self.f['divergence'][self.steps//2], 99)
        delta_vmax = np.percentile(self.f['delta_gradient'][self.steps//2], 98)

        # Plot Config
        extent = [-self.bounds, self.bounds, -self.bounds, self.bounds]
        
        img_div = axes[0].imshow(div_0, cmap='magma', origin='lower', extent=extent, vmin=0, vmax=div_vmax)
        axes[0].set_title("Raw Lyapunov Divergence", color='white')
        axes[0].axis('off')
        
        img_delta = axes[1].imshow(delta_0, cmap='viridis_r', origin='lower', extent=extent, vmin=0, vmax=delta_vmax)
        # Custom colormap for delta: Black to Cyan
        import matplotlib.colors as mcolors
        c_map = mcolors.LinearSegmentedColormap.from_list("viridis_r", ["black", "cyan", "white"])
        img_delta.set_cmap(c_map)
        
        axes[1].set_title("The Delta (Information Ridge)", color='white')
        axes[1].axis('off')

        title_text = fig.suptitle(f"Z-Slice: 0 / {self.steps}", color='white', fontsize=16)

        def update(frame):
            # Read data from HDF5
            d = self.f['divergence'][frame]
            g = self.f['delta_gradient'][frame]
            
            img_div.set_data(d)
            img_delta.set_data(g)
            title_text.set_text(f"Z-Slice: {frame} / {self.steps} (Evolution of Chaos)")
            return img_div, img_delta, title_text

        ani = animation.FuncAnimation(fig, update, frames=range(0, self.steps, 2), blit=False, interval=30)
        
        if save_file:
            logger.info(f"Rendering to video: {save_file}")
            ani.save(save_file, fps=30, extra_args=['-vcodec', 'libx264'])
            logger.info("Render Complete.")
        else:
            plt.show()

    def render_3d_nervous_system(self, threshold_percentile=95, stride=4):
        """
        Extracts the high-delta points and plots them in 3D.
        This reveals the 'Skeleton' of the fractal.
        
        stride: Skips pixels to prevent crashing matplotlib (Higher = Faster/Lower Res)
        """
        logger.info("Extracting Volumetric Isosurfaces...")
        
        # 1. Load the volume (downsampled for RAM safety)
        # We slice [::stride, ::stride, ::stride]
        vol_delta = self.f['delta_gradient'][::stride, ::stride, ::stride]
        
        # 2. Thresholding
        # We only want to see the "Ridges" (High Delta)
        thresh_val = np.percentile(vol_delta, threshold_percentile)
        logger.info(f"Thresholding at Delta > {thresh_val:.4f} (Top {100-threshold_percentile}%)")
        
        z_idx, y_idx, x_idx = np.where(vol_delta > thresh_val)
        values = vol_delta[z_idx, y_idx, x_idx]
        
        logger.info(f"Rendering {len(values)} points...")
        
        # 3. Plotting
        fig = plt.figure(figsize=(12, 10), facecolor='#0f0f0f')
        ax = fig.add_subplot(111, projection='3d', facecolor='#0f0f0f')
        
        # Map indices back to physical space
        # Z is time (0 to steps)
        # X, Y are space (-bounds to bounds)
        
        # Normalize coords for plotting
        z_plot = z_idx 
        y_plot = y_idx 
        x_plot = x_idx 

        p = ax.scatter(x_plot, y_plot, z_plot, c=values, cmap='cool', s=0.5, alpha=0.3)
        
        ax.set_xlabel("M Axis", color='white')
        ax.set_ylabel("L Axis", color='white')
        ax.set_zlabel("Time (Z)", color='white')
        
        # Make axes panes transparent
        ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        
        # Colorbar
        cbar = plt.colorbar(p, ax=ax, shrink=0.5, pad=0.1)
        cbar.set_label("Delta Intensity", color='white')
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
        
        ax.tick_params(colors='white')
        ax.view_init(elev=30, azim=45)
        
        plt.title(f"The Fractal Nervous System (Top {100-threshold_percentile}% Activity)", color='white')
        plt.show()

if __name__ == "__main__":
    renderer = ManifoldRenderer()
    
    # MODE 1: View the MRI Animation
    # Close the window to proceed to the next mode
    renderer.animate_mri_scan() 
    
    # MODE 2: View the 3D Ghost Structure
    # stride=5 is safe. Decrease to 2 or 1 for High Quality (Warning: Heavy)
    renderer.render_3d_nervous_system(threshold_percentile=97, stride=5)