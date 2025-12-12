import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm
import matplotlib.colors as mcolors
import os

# ======================
# CONFIGURATION
# ======================

# USER DATA HOOK: Set this to the path of your .npy file
# If None, the system generates a high-fidelity Planck-like simulation
CMB_FILE_PATH = None 

# PHYSICS CONSTANTS
KNOT_RATIO = 1.0 / 3.0    # The fundamental scaling law
ZOOM_SPEED = 0.05         # Speed of the camera flight
FRAMES = 240              # Total animation length
FPS = 24                  # Cinematic framerate

# SCALES (The Journey)
SCALES = [
    ("CMB HORIZON", 4.4e26, "Cosmic Surface Tension"),
    ("SUPERCLUSTER", 1e23, "Filamentary Web"),
    ("GALAXY", 1e21, "Galactic Rotation Curves"),
    ("SOLAR SYSTEM", 1e11, "Planetary Resonance"),
    ("HUMAN", 1.7, "Observer Scale"),
    ("CELLULAR", 1e-5, "Biological Machinery"),
    ("ATOMIC", 1e-10, "Electron Shells"),
    ("PROTON", 8.4e-16, "The Fractal Core")
]

print("=" * 70)
print("P I R O U E T T E   E N G I N E   v 4")
print("Tier 4: Dynamic Flight & Data Integration")
print("=" * 70)

# ======================
# DATA ENGINE
# ======================

def load_or_generate_cmb():
    """
    Loads real user data if available, otherwise generates 
    a high-fidelity spherical harmonic simulation of the CMB.
    """
    if CMB_FILE_PATH and os.path.exists(CMB_FILE_PATH):
        print(f"[*] Loading real data from {CMB_FILE_PATH}...")
        try:
            data = np.load(CMB_FILE_PATH)
            # Normalize to -1..1
            data = (data - np.min(data)) / (np.max(data) - np.min(data)) * 2 - 1
            print("[✓] Data loaded successfully.")
            return data
        except Exception as e:
            print(f"[!] Error loading data: {e}. Reverting to simulation.")
    
    print("[*] Generating Planck-like CMB simulation (Spherical Harmonics)...")
    theta = np.linspace(0, np.pi, 100)
    phi = np.linspace(0, 2*np.pi, 200)
    THETA, PHI = np.meshgrid(theta, phi)
    
    # Generate multipoles (l=2 to l=8 for large scale structure)
    # This mimics the "mottled" look of real Planck data
    cmb_map = np.zeros_like(THETA)
    
    # Dipole (motion)
    cmb_map += 0.5 * np.real(sph_harm(0, 1, PHI, THETA))
    # Quadrupole (anisotropy)
    cmb_map += 0.3 * np.real(sph_harm(0, 2, PHI, THETA))
    # Octupole (the "Axis of Evil" alignment hint)
    cmb_map += 0.2 * np.real(sph_harm(0, 3, PHI, THETA))
    
    # Add scale-invariant noise (small scale fluctuations)
    noise = np.random.randn(*THETA.shape) * 0.1
    
    return THETA, PHI, cmb_map + noise

# ======================
# GEOMETRY ENGINE
# ======================

def generate_trefoil(t, scale=1.0):
    """Generates the Trefoil Knot geometry."""
    x = scale * (np.sin(t) + 2 * np.sin(2*t))
    y = scale * (np.cos(t) - 2 * np.cos(2*t))
    z = scale * (-np.sin(3*t))
    return x, y, z

def generate_starfield(n_stars=200):
    """Generates a background starfield for parallax."""
    phi = np.random.uniform(0, 2*np.pi, n_stars)
    theta = np.random.uniform(0, np.pi, n_stars)
    r = np.random.uniform(10, 20, n_stars) # Distant background
    
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

# ======================
# VISUALIZATION
# ======================

def create_flight_animation():
    
    # 1. Setup Data
    THETA, PHI, CMB_DATA = load_or_generate_cmb()
    stars_x, stars_y, stars_z = generate_starfield()
    t_knot = np.linspace(0, 2*np.pi, 1000)
    
    # 2. Setup Figure
    fig = plt.figure(figsize=(20, 12), facecolor='#050505')
    gs = GridSpec(3, 4, figure=fig, width_ratios=[1, 1, 0.4, 0.4])
    
    # MAIN VIEWPORT (The Flight) - Spans 2x3 blocks
    ax_main = fig.add_subplot(gs[:, :2], projection='3d')
    ax_main.set_facecolor('#000000')
    ax_main.axis('off')
    
    # HUD: SCALE LADDER
    ax_ladder = fig.add_subplot(gs[:, 2])
    ax_ladder.set_facecolor('#080808')
    
    # HUD: CMB DATA
    ax_cmb = fig.add_subplot(gs[0, 3], projection='polar')
    ax_cmb.set_facecolor('#080808')
    
    # HUD: METRICS
    ax_metrics = fig.add_subplot(gs[1:, 3])
    ax_metrics.set_facecolor('#080808')
    ax_metrics.axis('off')

    # 3. Animation Update
    def update(frame):
        ax_main.clear()
        ax_ladder.clear()
        ax_metrics.clear()
        ax_metrics.axis('off')
        
        # --- PHYSICS CALCS ---
        # Continuous scale factor
        # We cycle through 3 orders of magnitude then loop to create infinite zoom
        loop_progress = (frame % (FRAMES // 3)) / (FRAMES // 3)
        zoom_level = 3.0 ** loop_progress # Scales from 1x to 3x
        
        # Global absolute scale (logarithmic descent)
        total_progress = frame / FRAMES
        current_log_scale = np.log10(SCALES[0][1]) - total_progress * (np.log10(SCALES[0][1]/SCALES[-1][1]))
        current_scale_m = 10**current_log_scale
        
        # --- MAIN VIEWPORT: INFINITE ZOOM ---
        
        # Layer 1: The knot we are inside (Large)
        # It expands from Scale 1 -> 3, eventually flying past camera
        s1 = zoom_level * 3.0
        x1, y1, z1 = generate_trefoil(t_knot, scale=s1)
        ax_main.plot(x1, y1, z1, color='cyan', alpha=max(0, 1.0 - loop_progress), linewidth=2)
        
        # Layer 2: The knot in focus (Medium)
        # It expands from Scale 0.33 -> 1
        s2 = zoom_level
        x2, y2, z2 = generate_trefoil(t_knot, scale=s2)
        # Color shifts from Blue (distant) to Cyan (close)
        ax_main.plot(x2, y2, z2, color='white', alpha=0.9, linewidth=3)
        
        # Layer 3: The knot emerging (Small)
        # It expands from Scale 0.11 -> 0.33
        s3 = zoom_level * 0.333
        x3, y3, z3 = generate_trefoil(t_knot, scale=s3)
        ax_main.plot(x3, y3, z3, color='magenta', alpha=loop_progress, linewidth=1)
        
        # Starfield (Parallax)
        # Stars rotate slowly to simulate orbit
        azimuth = frame * 0.5
        ax_main.scatter(stars_x, stars_y, stars_z, c='white', s=1, alpha=0.4)
        
        # Camera
        ax_main.set_xlim(-4, 4)
        ax_main.set_ylim(-4, 4)
        ax_main.set_zlim(-4, 4)
        # Orbiting camera
        ax_main.view_init(elev=30, azim=azimuth)
        
        # --- HUD: SCALE LADDER ---
        
        y_pos = np.arange(len(SCALES))
        names = [s[0] for s in SCALES]
        vals = [np.log10(s[1]) for s in SCALES]
        
        # Draw the static ladder
        ax_ladder.vlines(0, 0, len(SCALES)-1, colors='gray', alpha=0.3)
        ax_ladder.scatter(np.zeros_like(y_pos), y_pos, c='gray', s=30)
        
        # Highlight current position
        # Find where we are relative to the discrete scales
        # Map current_log_scale to y_pos coordinates
        log_max = np.log10(SCALES[0][1])
        log_min = np.log10(SCALES[-1][1])
        norm_pos = (log_max - current_log_scale) / (log_max - log_min) * (len(SCALES)-1)
        
        ax_ladder.scatter([0], [norm_pos], c='lime', s=150, edgecolors='white', zorder=10)
        ax_ladder.text(0.1, norm_pos, f"{current_scale_m:.1e} m", color='lime', fontsize=12, fontweight='bold', va='center')
        
        # Labels
        for i, (name, val, desc) in enumerate(SCALES):
            color = 'white' if abs(i - norm_pos) < 0.5 else 'gray'
            alpha = 1.0 if abs(i - norm_pos) < 0.5 else 0.5
            ax_ladder.text(-0.2, i, name, color=color, alpha=alpha, ha='right', fontsize=10)
            if abs(i - norm_pos) < 0.5:
                ax_ladder.text(0.5, i, desc, color='cyan', fontsize=8, ha='left')
        
        ax_ladder.set_xlim(-1, 1)
        ax_ladder.set_ylim(len(SCALES), -1) # Inverted Y for top-down list
        ax_ladder.axis('off')
        
        # --- HUD: CMB DATA ---
        if frame == 0: # Draw once for performance optimization in MP4, but GIF needs redraw
            ax_cmb.clear()
            # Wrap simulation to polar
            # Simple visualization of the loaded data
            mesh = ax_cmb.pcolormesh(PHI, THETA, CMB_DATA, cmap='inferno', shading='gouraud')
            ax_cmb.grid(False)
            ax_cmb.set_xticks([])
            ax_cmb.set_yticks([])
            ax_cmb.set_title("CMB POLARIZATION", color='orange', fontsize=8, pad=2)

        # --- HUD: METRICS ---
        
        freq = 3e8 / current_scale_m
        layer_n = np.log(SCALES[0][1] / current_scale_m) / np.log(3.0)
        
        metrics_text = f"""
        FLIGHT COMPUTER
        ----------------
        LAYER:   n = {layer_n:.2f}
        
        FREQ:    {freq:.2e} Hz
        PERIOD:  {1/freq:.2e} s
        
        INVARIANT: 1/3
        TOPOLOGY:  Trefoil (3_1)
        
        STATUS:    {SCALES[int(norm_pos)][0]}
        """
        ax_metrics.text(0.1, 0.9, metrics_text, color='lime', family='monospace', fontsize=10, va='top')
        
        # Overlay grid on metrics for "tech" feel
        ax_metrics.hlines([0.2, 0.4, 0.6, 0.8], 0, 1, colors='green', alpha=0.1)

        return ax_main, ax_ladder, ax_cmb, ax_metrics

    # 4. Render
    print("[*] Engaging Pirouette Engine...")
    print(f"    Frames: {FRAMES} | Res: 2000x1200")
    anim = FuncAnimation(fig, update, frames=FRAMES, interval=40, blit=False)
    
    save_path = 'pirouette_tier4_flight.gif'
    print(f"[*] Rendering flight path to {save_path}...")
    anim.save(save_path, writer=PillowWriter(fps=FPS))
    print("[✓] Flight complete.")

if __name__ == "__main__":
    create_flight_animation()