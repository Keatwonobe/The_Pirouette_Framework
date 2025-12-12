import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from numba import njit, prange
import json

# =========================================================
#  COMPLETE PROTON MODEL WITH 24 Hz HARMONIC STRUCTURE
# =========================================================

# --- FUNDAMENTAL CONSTANTS ---
FUNDAMENTAL_FREQUENCY = 24.0  # Hz - The universal harmonic
CYCLES_PER_ANIMATION = 1      # Complete 24 Hz cycles to show

# Physical Parameters
PROTON_MASS_MEV = 938.272      # MeV/c²
HBAR_C = 197.327               # MeV·fm (ℏc)
PROTON_RADIUS_FM = 0.8414      # Measured charge radius (fm)
QCD_SCALE_FM = 1.0             # Confinement scale

# Quark Sources (3-fold symmetry in M-L plane)
QUARK_POSITIONS = np.array([
    [0.6, 0.0, 0.0],      # Quark 1 (up)
    [-0.3, 0.52, 0.0],    # Quark 2 (up)  
    [-0.3, -0.52, 0.0]    # Quark 3 (down)
]) * PROTON_RADIUS_FM / 0.6  # Scale to proton size

# Animation
TOTAL_FRAMES = 120            # 10 seconds at 24 fps
OUTPUT_FILE = "proton_complete_model.gif"

# Grid resolution
SPATIAL_RES = 150
Z_LAYERS = 50

# =========================================================
#  CORE PHYSICS: WAVE INTERFERENCE WITH 24 HARMONICS
# =========================================================

@njit(parallel=True)
def calculate_proton_field(x, y, z, quark_pos, time_phase, harmonics=24):
    """
    Calculate the quantum field at point (x,y,z) given quark sources.
    Uses 24 harmonic modes for the fundamental frequency structure.
    """
    field_real = 0.0
    field_imag = 0.0
    
    for q in range(3):  # Three quarks
        qx, qy, qz = quark_pos[q]
        
        # Distance from quark
        dx = x - qx
        dy = y - qy
        dz = z - qz
        r = np.sqrt(dx*dx + dy*dy + dz*dz)
        
        if r < 1e-9:
            r = 1e-9
        
        # Base wavelength from quark position
        k_base = 2 * np.pi / (r + 0.1)
        
        # Superposition of 24 harmonic modes
        for n in range(1, harmonics + 1):
            k_n = k_base * n
            phase_n = k_n * r - 2 * np.pi * n * time_phase
            amplitude = 1.0 / (r * np.sqrt(n))  # Amplitude falls with mode number
            
            field_real += amplitude * np.cos(phase_n)
            field_imag += amplitude * np.sin(phase_n)
    
    intensity = field_real**2 + field_imag**2
    return intensity, field_real, field_imag

@njit(parallel=True)
def render_proton_slice(z_val, quark_pos, time_phase, res, extent):
    """Render a 2D slice at height z."""
    x_vals = np.linspace(-extent, extent, res)
    y_vals = np.linspace(-extent, extent, res)
    
    field_map = np.zeros((res, res), dtype=np.float64)
    
    for i in prange(res):
        for j in range(res):
            intensity, _, _ = calculate_proton_field(
                x_vals[j], y_vals[i], z_val, 
                quark_pos, time_phase, 24
            )
            field_map[i, j] = intensity
    
    return field_map

# =========================================================
#  FRACTAL LOCK FINDER (from basin explorer)
# =========================================================

def find_fractal_locks_simple(quark_pos, time_phase, n_samples=36):
    """
    Quick scan for fractal lock points at a given time phase.
    Returns positions and intensities.
    """
    locks = []
    
    # Polar scan
    radii = np.linspace(0.2, 1.5, 8)
    angles = np.linspace(0, 2*np.pi, n_samples, endpoint=False)
    
    for r in radii:
        for theta in angles:
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            
            # Check at z=0 plane
            intensity, _, _ = calculate_proton_field(x, y, 0.0, quark_pos, time_phase, 24)
            
            if intensity > 50:  # Threshold
                locks.append({
                    'x': x, 'y': y, 'z': 0.0,
                    'r': r, 'theta': theta,
                    'intensity': intensity
                })
    
    return locks

# =========================================================
#  VISUALIZATION
# =========================================================

def create_proton_animation():
    print("=" * 70)
    print("COMPLETE PROTON MODEL - 24 Hz HARMONIC STRUCTURE")
    print("=" * 70)
    
    # Time array
    time_phases = np.linspace(0, CYCLES_PER_ANIMATION, TOTAL_FRAMES)
    
    # Setup figure
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Main 3D view
    ax_3d = fig.add_subplot(gs[:2, :2], projection='3d')
    
    # Side panels
    ax_xy = fig.add_subplot(gs[0, 2])  # XY slice
    ax_time = fig.add_subplot(gs[1, 2])  # Time evolution
    ax_spectrum = fig.add_subplot(gs[2, :])  # Frequency spectrum
    
    # Storage for time series
    lock_count_history = []
    energy_history = []
    
    def update(frame):
        time_phase = time_phases[frame]
        
        # Clear all axes
        ax_3d.clear()
        ax_xy.clear()
        ax_time.clear()
        ax_spectrum.clear()
        
        # === 1. 3D FIELD STRUCTURE ===
        extent = 1.5
        
        # Render multiple Z slices
        z_levels = np.linspace(-0.3, 0.3, 5)
        
        for z_val in z_levels:
            field_slice = render_proton_slice(z_val, QUARK_POSITIONS, time_phase, 80, extent)
            
            # Create mesh for this slice
            x = np.linspace(-extent, extent, 80)
            y = np.linspace(-extent, extent, 80)
            X, Y = np.meshgrid(x, y)
            Z = np.ones_like(X) * z_val
            
            # Threshold for visibility
            mask = field_slice > 20
            
            if np.any(mask):
                field_slice[~mask] = np.nan
                max_val = np.nanmax(field_slice)
                if max_val > 0:
                    # Plot surface
                    ax_3d.plot_surface(X, Y, Z, facecolors=plt.cm.hot(field_slice / max_val),
                                     alpha=0.6, antialiased=True, linewidth=0)
        
        # Find and plot fractal locks
        locks = find_fractal_locks_simple(QUARK_POSITIONS, time_phase)
        if locks:
            lock_x = [l['x'] for l in locks]
            lock_y = [l['y'] for l in locks]
            lock_z = [l['z'] for l in locks]
            ax_3d.scatter(lock_x, lock_y, lock_z, c='cyan', s=20, alpha=0.8, 
                         label=f'{len(locks)} locks')
        
        # Plot quark positions
        ax_3d.scatter(QUARK_POSITIONS[:, 0], QUARK_POSITIONS[:, 1], 
                     QUARK_POSITIONS[:, 2], c='yellow', s=200, marker='*',
                     edgecolors='red', linewidth=2, label='Quarks', zorder=10)
        
        ax_3d.set_xlabel('X (fm)')
        ax_3d.set_ylabel('Y (fm)')
        ax_3d.set_zlabel('Z (fm)')
        ax_3d.set_xlim(-extent, extent)
        ax_3d.set_ylim(-extent, extent)
        ax_3d.set_zlim(-0.5, 0.5)
        ax_3d.view_init(elev=25, azim=frame * 360 / TOTAL_FRAMES)
        ax_3d.legend(loc='upper right', fontsize=8)
        ax_3d.set_title(f'Proton Structure (t = {time_phase:.2f} cycles)', fontsize=12)
        
        # === 2. XY SLICE AT Z=0 ===
        field_xy = render_proton_slice(0.0, QUARK_POSITIONS, time_phase, 100, extent)
        
        im = ax_xy.imshow(field_xy, extent=[-extent, extent, -extent, extent],
                         origin='lower', cmap='hot', vmax=np.percentile(field_xy, 99))
        ax_xy.scatter(QUARK_POSITIONS[:, 0], QUARK_POSITIONS[:, 1], 
                     c='cyan', s=100, marker='*', edgecolors='white', linewidth=1)
        ax_xy.set_title('XY Slice (z=0)', fontsize=10)
        ax_xy.set_xlabel('X (fm)')
        ax_xy.set_ylabel('Y (fm)')
        
        # === 3. TIME EVOLUTION ===
        lock_count_history.append(len(locks) if locks else 0)
        energy_history.append(np.sum(field_xy))
        
        ax_time.plot(lock_count_history, 'c-', linewidth=2, label='Lock Count')
        ax_time.set_xlim(0, TOTAL_FRAMES)
        ax_time.set_ylabel('Fractal Locks', color='c')
        ax_time.tick_params(axis='y', labelcolor='c')
        ax_time.grid(True, alpha=0.3)
        
        ax_time2 = ax_time.twinx()
        ax_time2.plot(energy_history, 'r-', linewidth=2, alpha=0.6, label='Field Energy')
        ax_time2.set_ylabel('Energy', color='r')
        ax_time2.tick_params(axis='y', labelcolor='r')
        
        ax_time.set_title('Time Evolution', fontsize=10)
        ax_time.set_xlabel('Frame')
        
        # === 4. FREQUENCY SPECTRUM ===
        # FFT of lock count to show 24 Hz dominance
        if len(lock_count_history) > 10:
            fft = np.fft.fft(lock_count_history)
            freqs = np.fft.fftfreq(len(lock_count_history), d=1.0/FUNDAMENTAL_FREQUENCY)
            power = np.abs(fft)**2
            
            # Plot positive frequencies only
            positive = freqs > 0
            ax_spectrum.plot(freqs[positive], power[positive], 'b-', linewidth=2)
            ax_spectrum.axvline(FUNDAMENTAL_FREQUENCY, color='r', linestyle='--', 
                              linewidth=2, label=f'{FUNDAMENTAL_FREQUENCY} Hz')
            ax_spectrum.set_xlim(0, 100)
            ax_spectrum.set_xlabel('Frequency (Hz)')
            ax_spectrum.set_ylabel('Power')
            ax_spectrum.set_title('Frequency Spectrum - 24 Hz Fundamental', fontsize=10)
            ax_spectrum.legend()
            ax_spectrum.grid(True, alpha=0.3)
        
        if frame % 20 == 0:
            print(f"  Rendering frame {frame+1}/{TOTAL_FRAMES} | {len(locks) if locks else 0} locks")
        
        return ax_3d, ax_xy, ax_time, ax_spectrum
    
    # Create animation
    print("\n🎬 Generating animation...")
    ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=42, blit=False, repeat=True)
    
    # Save
    ani.save(OUTPUT_FILE, writer='pillow', fps=24)
    
    print(f"\n✅ Animation saved: {OUTPUT_FILE}")
    print(f"   Total frames: {TOTAL_FRAMES}")
    print(f"   Fundamental frequency: {FUNDAMENTAL_FREQUENCY} Hz")
    print(f"   Duration: {TOTAL_FRAMES/24:.1f} seconds")

# =========================================================
#  SCALE CALIBRATION REPORT
# =========================================================

def print_scale_report():
    print("\n" + "=" * 70)
    print("PROTON MODEL SCALE CALIBRATION")
    print("=" * 70)
    
    print(f"\nPhysical Constants:")
    print(f"  Proton mass: {PROTON_MASS_MEV:.3f} MeV/c²")
    print(f"  Proton radius: {PROTON_RADIUS_FM:.4f} fm")
    print(f"  QCD scale: {QCD_SCALE_FM:.1f} fm")
    print(f"  ℏc: {HBAR_C:.3f} MeV·fm")
    
    print(f"\nModel Parameters:")
    print(f"  Fundamental frequency: {FUNDAMENTAL_FREQUENCY} Hz")
    print(f"  Number of harmonics: 24")
    print(f"  Quark separation: ~{PROTON_RADIUS_FM:.2f} fm")
    
    # Period of oscillation
    period = 1.0 / FUNDAMENTAL_FREQUENCY
    print(f"  Oscillation period: {period*1e24:.2f} yoctoseconds (10⁻²⁴ s)")
    
    # Energy scale
    E_scale = HBAR_C / PROTON_RADIUS_FM  # Energy ~ ℏc/R
    print(f"  Characteristic energy: ~{E_scale:.0f} MeV")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    print_scale_report()
    create_proton_animation()