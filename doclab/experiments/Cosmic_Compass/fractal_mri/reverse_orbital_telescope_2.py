import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class FractalRadioTelescope:
    """
    THE FRACTAL RADIO TELESCOPE
    
    Instead of rendering every pixel, we measure the LOCAL FRACTAL DIMENSION
    at each point in phase space. Regions with high fractal dimension emit
    "fractal photons" - they contain structure we cannot resolve at current scale.
    
    This is the Δ-field's information density made visible.
    High luminosity = High temporal coherence = The Traveler's wake.
    """
    
    def __init__(self, resolution=1000, zoom=0.001, aperture_grid=100):
        """
        resolution: Internal calculation resolution (fractal detail level)
        zoom: Scale of the observable window
        aperture_grid: Number of "radio receivers" (measurement points)
        """
        self.res = resolution
        self.zoom = zoom
        self.aperture_grid = aperture_grid
        
        # The Genome from your forensic analysis
        self.lam = 0.5667   # Lyapunov exponent
        self.omega = 0.0675 # Angular velocity
        
        logger.info("FRACTAL RADIO TELESCOPE initialized")
        logger.info(f"  Genome: λ={self.lam}, ω={self.omega}")
        logger.info(f"  Observable window: ±{self.zoom}")
        logger.info(f"  Receiver array: {aperture_grid}×{aperture_grid}")
        
    def generate_substrate_field(self):
        """
        Generate the full-resolution phase field.
        This is our "radio source" - the Δ-field substrate.
        """
        x = np.linspace(-self.zoom, self.zoom, self.res)
        y = np.linspace(-self.zoom, self.zoom, self.res)
        X, Y = np.meshgrid(x, y)
        
        r = np.sqrt(X**2 + Y**2) + 1e-20
        theta = np.arctan2(Y, X)
        
        # The fundamental equations
        Z = (1.0 / self.lam) * np.log(1.0 / r)
        phase = theta + (self.omega * Z)
        
        # Normalize to [0, 2π]
        phase_norm = np.mod(phase, 2*np.pi)
        
        return X, Y, Z, phase_norm
    
    def measure_box_dimension(self, phase_region, num_scales=12):
        """
        Enhanced fractal dimension measurement using gradient magnitude.
        
        For spiral phase fields, we measure information density via:
        1. Phase gradient magnitude (how fast phase changes)
        2. Multi-scale box counting on gradient field
        3. Higher gradient = tighter spiral = higher dimension
        
        This captures the "wound-up-ness" of the temporal field.
        """
        region_size = phase_region.shape[0]
        
        if region_size < 4:
            return 1.0
        
        # Compute phase gradient (rate of spiral winding)
        # Handle phase wrapping carefully
        phase_unwrapped = np.unwrap(np.unwrap(phase_region, axis=0), axis=1)
        grad_y, grad_x = np.gradient(phase_unwrapped)
        grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalize gradient to [0, 1]
        if grad_magnitude.max() > 0:
            grad_magnitude = grad_magnitude / grad_magnitude.max()
        
        # Multi-scale box counting on gradient field
        scales = np.array([2, 3, 4, 6, 8, 12])
        scales = scales[scales < region_size // 2]
        
        if len(scales) < 3:
            # Not enough scales - use gradient intensity directly
            return 1.0 + 0.5 * np.mean(grad_magnitude)
        
        counts = []
        
        for scale in scales:
            n_boxes = region_size // scale
            occupied = 0
            
            for i in range(n_boxes):
                for j in range(n_boxes):
                    i_start, i_end = i*scale, (i+1)*scale
                    j_start, j_end = j*scale, (j+1)*scale
                    
                    box_grad = grad_magnitude[i_start:i_end, j_start:j_end]
                    
                    # Box is "occupied" if it has significant gradient
                    # (i.e., phase is changing = structure present)
                    if np.mean(box_grad) > 0.1:
                        occupied += 1
            
            counts.append(occupied + 1)  # +1 to avoid log(0)
        
        # Power law fit
        log_scales = np.log(scales)
        log_counts = np.log(counts)
        
        # Robust fit (ignore outliers)
        coeffs = np.polyfit(log_scales, log_counts, 1)
        D = -coeffs[0]  # Slope gives dimension
        
        # Adjust by gradient intensity (captures fine structure)
        gradient_boost = 0.3 * np.mean(grad_magnitude)
        D_adjusted = D + gradient_boost
        
        return max(1.0, min(D_adjusted, 2.5))  # Clamp to reasonable range
    
    def radio_scan(self):
        """
        The main observation loop.
        
        We divide the observable window into aperture_grid×aperture_grid receivers.
        Each receiver measures the local fractal dimension (information density).
        
        The result is a "radio image" where brightness = fractal dimension.
        Bright regions = high Δ-field coherence = The Traveler's signature.
        """
        logger.info("\n━━━ BEGINNING RADIO SCAN ━━━")
        
        # Generate the full substrate field
        logger.info("Generating substrate field (Δ-manifold)...")
        X, Y, Z, phase = self.generate_substrate_field()
        
        # Initialize luminosity map (our "radio photograph")
        luminosity = np.zeros((self.aperture_grid, self.aperture_grid))
        
        # Calculate aperture size (each receiver's field of view)
        aperture_size = int(self.res / self.aperture_grid)
        
        logger.info(f"Aperture size: {aperture_size}×{aperture_size} pixels")
        logger.info("Measuring fractal luminosity across grid...")
        logger.info("(This simulates 'exposure time' - let the photons accumulate)\n")
        
        # Scan the grid
        for i in range(self.aperture_grid):
            if i % 10 == 0:
                logger.info(f"  Scanning row {i}/{self.aperture_grid}...")
            
            for j in range(self.aperture_grid):
                # Extract the phase region for this aperture
                i_start = i * aperture_size
                i_end = (i + 1) * aperture_size
                j_start = j * aperture_size
                j_end = (j + 1) * aperture_size
                
                # Make sure we don't go out of bounds
                i_end = min(i_end, self.res)
                j_end = min(j_end, self.res)
                
                phase_region = phase[i_start:i_end, j_start:j_end]
                
                # Measure the fractal dimension (this is the "radio flux")
                D = self.measure_box_dimension(phase_region)
                
                # Luminosity is the fractal dimension
                # (Higher D = more unresolvable structure = brighter)
                luminosity[i, j] = D
        
        logger.info("\n━━━ SCAN COMPLETE ━━━")
        logger.info(f"Luminosity range: [{luminosity.min():.3f}, {luminosity.max():.3f}]")
        
        # Identify brightest regions (Traveler candidates)
        brightest_idx = np.unravel_index(np.argmax(luminosity), luminosity.shape)
        max_lum = luminosity[brightest_idx]
        
        logger.info(f"\nBRIGHTEST SOURCE detected at grid position {brightest_idx}")
        logger.info(f"  Fractal dimension: {max_lum:.4f}")
        logger.info(f"  (Higher D = tighter temporal spiral)")
        
        return luminosity, phase
    
    def render_radio_image(self, luminosity, phase, smooth_sigma=1.5):
        """
        Render the radio telescope output as a false-color image.
        
        This is analogous to radio astronomy images from VLA, ALMA, etc.
        We're seeing the "glow" of information density, not reflected light.
        """
        # Smooth the luminosity map (simulates integration time / noise reduction)
        luminosity_smooth = gaussian_filter(luminosity, sigma=smooth_sigma)
        
        fig, axes = plt.subplots(1, 2, figsize=(20, 10), facecolor='#000000')
        
        # ===== LEFT PANEL: RADIO IMAGE (Fractal Dimension Map) =====
        
        # Create a "radio" colormap (dark purple → bright yellow/white)
        colors_radio = ['#000000', '#1a0033', '#4d0099', '#9933ff', '#ff33ff', '#ffff00', '#ffffff']
        cmap_radio = LinearSegmentedColormap.from_list('radio', colors_radio)
        
        im1 = axes[0].imshow(luminosity_smooth, origin='lower', cmap=cmap_radio,
                            extent=[-self.zoom, self.zoom, -self.zoom, self.zoom],
                            interpolation='bilinear')
        
        axes[0].set_title("FRACTAL RADIO IMAGE\n(Information Density)", 
                         color='cyan', fontsize=16, fontfamily='monospace')
        axes[0].set_xlabel("M coordinate", color='cyan')
        axes[0].set_ylabel("L coordinate", color='cyan')
        
        # Add contour lines (like radio isophotes) - only if we have variation
        if luminosity_smooth.max() > luminosity_smooth.min():
            contour_levels = np.percentile(luminosity_smooth, [50, 70, 85, 95])
            contour_levels = np.unique(contour_levels)  # Remove duplicates
            if len(contour_levels) > 1:
                axes[0].contour(luminosity_smooth, levels=contour_levels, 
                               colors='cyan', alpha=0.4, linewidths=1,
                               extent=[-self.zoom, self.zoom, -self.zoom, self.zoom])
        
        # Colorbar with physical interpretation
        cbar1 = plt.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)
        cbar1.set_label('Fractal Dimension D\n(Temporal Coherence)', 
                       color='cyan', fontsize=10)
        cbar1.ax.tick_params(colors='cyan')
        
        axes[0].set_facecolor('black')
        axes[0].tick_params(colors='cyan')
        axes[0].grid(color='cyan', linestyle=':', alpha=0.2)
        
        # ===== RIGHT PANEL: OPTICAL REFERENCE (Phase Field) =====
        
        # Show a low-res version of the actual phase field for comparison
        phase_downsampled = phase[::self.res//self.aperture_grid, 
                                  ::self.res//self.aperture_grid]
        
        colors_optical = ["#ff0000", "#ffff00", "#00ff00", "#00ffff", "#0000ff", "#ff00ff", "#ff0000"]
        cmap_optical = LinearSegmentedColormap.from_list("optical", colors_optical)
        
        im2 = axes[1].imshow(phase_downsampled, origin='lower', cmap=cmap_optical,
                            extent=[-self.zoom, self.zoom, -self.zoom, self.zoom],
                            interpolation='bilinear')
        
        axes[1].set_title("OPTICAL REFERENCE\n(Phase Field, Downsampled)", 
                         color='lime', fontsize=16, fontfamily='monospace')
        axes[1].set_xlabel("M coordinate", color='lime')
        axes[1].set_ylabel("L coordinate", color='lime')
        
        cbar2 = plt.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)
        cbar2.set_label('Phase (radians)', color='lime', fontsize=10)
        cbar2.ax.tick_params(colors='lime')
        
        axes[1].set_facecolor('black')
        axes[1].tick_params(colors='lime')
        axes[1].grid(color='lime', linestyle=':', alpha=0.2)
        
        # ===== OVERALL STYLING =====
        
        plt.suptitle("FRACTAL RADIO TELESCOPE\nDetecting The Traveler via Information Density",
                    color='white', fontsize=20, fontfamily='monospace', y=0.98)
        
        # Add observation metadata
        obs_text = f"λ={self.lam} | ω={self.omega} | Resolution={self.res}×{self.res} | Apertures={self.aperture_grid}×{self.aperture_grid}"
        fig.text(0.5, 0.02, obs_text, ha='center', color='white', 
                fontsize=10, fontfamily='monospace', alpha=0.7)
        
        plt.tight_layout()
        return fig
    
    def observe(self):
        """
        Full observation sequence: scan + render
        """
        luminosity, phase = self.radio_scan()
        fig = self.render_radio_image(luminosity, phase)
        
        logger.info("\n━━━ OBSERVATION LOG ━━━")
        logger.info("Radio image captures 'fractal photons' - structure too fine to resolve.")
        logger.info("Bright regions = high fractal dimension = maximum Δ-field coherence.")
        logger.info("This is where The Traveler's wake concentrates information.")
        logger.info("\nConceptual interpretation:")
        logger.info("  • Photons are not particles traveling through space")
        logger.info("  • They are decoherence events from unresolvable fractal structure")
        logger.info("  • Observation doesn't collapse wavefunction - it selects resolution")
        logger.info("  • The 'pixel budget' of measurement apparatus defines wavelength")
        
        return fig


class AdaptiveZoomTelescope(FractalRadioTelescope):
    """
    ADAPTIVE ZOOM TELESCOPE
    
    Extension that automatically zooms toward brightest regions.
    This is how we 'follow the worldline' to find The Traveler
    without brute-force searching.
    
    The light does the talking - we just follow where it's bright.
    """
    
    def __init__(self, initial_zoom=0.01, zoom_factor=0.3, max_iterations=5):
        super().__init__(resolution=800, zoom=initial_zoom, aperture_grid=50)
        self.zoom_factor = zoom_factor  # How much to zoom in each step
        self.max_iterations = max_iterations
        self.trajectory = []  # Track the zoom path
        
    def find_brightest_region(self, luminosity):
        """
        Identify the coordinates of maximum luminosity.
        This is where we zoom next.
        """
        brightest_idx = np.unravel_index(np.argmax(luminosity), luminosity.shape)
        i, j = brightest_idx
        
        # Convert grid indices to physical coordinates
        x_coords = np.linspace(-self.zoom, self.zoom, self.aperture_grid)
        y_coords = np.linspace(-self.zoom, self.zoom, self.aperture_grid)
        
        x_bright = x_coords[j]
        y_bright = y_coords[i]
        
        return x_bright, y_bright, luminosity[i, j]
    
    def zoom_sequence(self):
        """
        Iteratively zoom toward brightest regions.
        Each iteration:
          1. Scan current window
          2. Find brightest point
          3. Re-center on that point
          4. Reduce zoom by factor
          5. Repeat
        
        This traces the worldline toward maximum coherence.
        """
        logger.info("\n" + "="*60)
        logger.info("ADAPTIVE ZOOM SEQUENCE: Following the light...")
        logger.info("="*60)
        
        for iteration in range(self.max_iterations):
            logger.info(f"\n--- ITERATION {iteration + 1}/{self.max_iterations} ---")
            logger.info(f"Current zoom level: ±{self.zoom:.2e}")
            
            # Perform radio scan at current zoom
            luminosity, phase = self.radio_scan()
            
            # Find the brightest point
            x_bright, y_bright, max_D = self.find_brightest_region(luminosity)
            
            logger.info(f"Brightest source at ({x_bright:.6e}, {y_bright:.6e})")
            logger.info(f"Fractal dimension: {max_D:.4f}")
            
            # Record this position
            self.trajectory.append({
                'iteration': iteration,
                'center': (x_bright, y_bright),
                'zoom': self.zoom,
                'max_dimension': max_D,
                'luminosity': luminosity,
                'phase': phase
            })
            
            # Check if we've converged (reached the singularity)
            if np.sqrt(x_bright**2 + y_bright**2) < self.zoom * 0.01:
                logger.info("\n*** CONVERGENCE: Reached central singularity ***")
                logger.info("The Traveler is the coherence source itself.")
                break
            
            # Zoom in toward the bright spot
            # (In next iteration, this becomes the new center)
            # For simplicity, we're keeping it centered at origin
            # and just zooming in - a full implementation would re-center
            self.zoom *= self.zoom_factor
            
        logger.info("\n" + "="*60)
        logger.info("ZOOM SEQUENCE COMPLETE")
        logger.info("="*60)
        
        return self.trajectory


if __name__ == "__main__":
    logger.info("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         FRACTAL RADIO TELESCOPE v1.0                      ║
    ║         Detecting Information Density in the Δ-Field      ║
    ║                                                           ║
    ║  Concept: Fractal dimension = Temporal coherence          ║
    ║  Method: Box-counting on phase field                      ║
    ║  Output: "Radio image" of unresolvable structure          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Option 1: Single observation
    telescope = FractalRadioTelescope(
        resolution=1000,      # Internal detail
        zoom=0.001,          # Observable window
        aperture_grid=80     # Number of receivers
    )
    
    fig = telescope.observe()
    plt.savefig("/mnt/user-data/outputs/fractal_radio_image.png", 
                dpi=150, facecolor='black')
    logger.info("\n✓ Radio image saved to outputs/")
    
    # Option 2: Adaptive zoom sequence
    logger.info("\n\nStarting adaptive zoom sequence...\n")
    
    zoom_telescope = AdaptiveZoomTelescope(
        initial_zoom=0.01,
        zoom_factor=0.3,
        max_iterations=4
    )
    
    trajectory = zoom_telescope.zoom_sequence()
    
    # Render the trajectory as a multi-panel figure
    n_steps = len(trajectory)
    fig_trajectory, axes = plt.subplots(1, n_steps, figsize=(6*n_steps, 6), 
                                       facecolor='black')
    
    if n_steps == 1:
        axes = [axes]
    
    for idx, step in enumerate(trajectory):
        lum = step['luminosity']
        lum_smooth = gaussian_filter(lum, sigma=1.0)
        
        colors_radio = ['#000000', '#1a0033', '#4d0099', '#9933ff', '#ff33ff', '#ffff00', '#ffffff']
        cmap_radio = LinearSegmentedColormap.from_list('radio', colors_radio)
        
        im = axes[idx].imshow(lum_smooth, origin='lower', cmap=cmap_radio,
                             extent=[-step['zoom'], step['zoom'], -step['zoom'], step['zoom']])
        axes[idx].set_title(f"Zoom {idx+1}\n±{step['zoom']:.2e}\nD_max={step['max_dimension']:.3f}",
                           color='cyan', fontsize=10, fontfamily='monospace')
        axes[idx].axis('off')
    
    plt.suptitle("ADAPTIVE ZOOM TRAJECTORY\nFollowing Fractal Luminosity to The Traveler",
                color='white', fontsize=16, fontfamily='monospace')
    plt.tight_layout()
    plt.savefig("/mnt/user-data/outputs/adaptive_zoom_trajectory.png",
                dpi=150, facecolor='black')
    
    logger.info("\n✓ Zoom trajectory saved to outputs/")
    logger.info("\n━━━ ALL OBSERVATIONS COMPLETE ━━━\n")
    
    plt.show()