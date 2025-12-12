"""
THE GRAND UNIFICATION GIF - TIER 2 ENHANCED RIGOR
Building on Tier 1, adds:
1. Ghost overlays showing 1/3 contraction visually
2. Curvature (κ) and torsion (τ) metrics
3. Narrative text synced to scale transitions
4. Phase-based breathing animation
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
from scipy.constants import hbar, c

# ======================
# UNIVERSAL CONSTANTS
# ======================

KNOT_RATIO = 1.0 / 3.0
CROSSING_NUMBER = 3

# Physical scales with narrative
SCALES = [
    ("CMB Core", 4.4e26, 
     "The wound in spacetime. Surface tension\nat cosmic scale defines dark energy."),
    
    ("Galaxy", 1e21,
     "Helical resonance organizes dark matter\ninto filaments. 1/3 scaling visible."),
    
    ("Solar System", 1e11,
     "Planetary orbits follow knot curvature\nminima. Stable resonances."),
    
    ("Human", 1e7,
     "Perception layer. We exist at the\ncurvature equilibrium scale."),
    
    ("Atom", 1e-10,
     "Quantum boundary. Knot transitions\nfrom diffuse to localized."),
    
    ("Proton", 8.4e-16,
     "The fractal core. 2276 locks form\nthree statistical 'quarks'.")
]

SCALE_CMB = SCALES[0][1]
SCALE_PROTON = SCALES[-1][1]

# Animation
N_FRAMES = 200  # Slightly longer for narrative timing
FPS = 20

# Constants
HBAR = hbar
C = c

print("=" * 70)
print("THE GRAND UNIFICATION - TIER 2 ENHANCED RIGOR")
print("=" * 70)
print("New features:")
print("  • Ghost overlays (show 1/3 scaling)")
print("  • Curvature κ and torsion τ plots")
print("  • Narrative text per scale")
print("  • Phase breathing animation")
print("=" * 70)

# ======================
# KNOT GEOMETRY (from Tier 1)
# ======================

def trefoil_knot_parametric(t, scale=1.0, phase=0.0, breathing=0.0):
    """
    Trefoil with optional breathing (phase modulation).
    breathing parameter makes the knot pulse with frequency.
    """
    # Base trefoil
    r = scale * (1.0 + breathing * np.sin(phase * 5))  # Pulse 5x per rotation
    
    x = r * (np.sin(t) + 2 * np.sin(2*t + phase))
    y = r * (np.cos(t) - 2 * np.cos(2*t + phase))
    z = r * (-np.sin(3*t + phase))
    
    return x, y, z

def trefoil_frenet_frame(t, scale=1.0, phase=0.0):
    """Compute Frenet frame for deterministic lock placement."""
    dt = 1e-6
    
    x, y, z = trefoil_knot_parametric(t, scale, phase)
    x_dt, y_dt, z_dt = trefoil_knot_parametric(t + dt, scale, phase)
    x_2dt, y_2dt, z_2dt = trefoil_knot_parametric(t + 2*dt, scale, phase)
    
    dx = (x_dt - x) / dt
    dy = (y_dt - y) / dt
    dz = (z_dt - z) / dt
    
    d2x = (x_2dt - 2*x_dt + x) / (dt**2)
    d2y = (y_2dt - 2*y_dt + y) / (dt**2)
    d2z = (z_2dt - 2*z_dt + z) / (dt**2)
    
    speed = np.sqrt(dx**2 + dy**2 + dz**2)
    if speed < 1e-10: speed = 1e-10
    T = np.array([dx, dy, dz]) / speed
    
    accel = np.array([d2x, d2y, d2z])
    accel_perp = accel - np.dot(accel, T) * T
    accel_mag = np.linalg.norm(accel_perp)
    if accel_mag < 1e-10: accel_mag = 1e-10
    N = accel_perp / accel_mag
    
    B = np.cross(T, N)
    
    return T, N, B

def compute_curvature_torsion(t, scale=1.0, phase=0.0):
    """
    Compute curvature κ and torsion τ at point t on the knot.
    
    κ = |r' × r''| / |r'|³  (curvature)
    τ = (r' × r'') · r''' / |r' × r''|²  (torsion)
    """
    dt = 1e-6
    
    # Position and derivatives
    r = np.array(trefoil_knot_parametric(t, scale, phase))
    r1 = np.array(trefoil_knot_parametric(t + dt, scale, phase))
    r2 = np.array(trefoil_knot_parametric(t + 2*dt, scale, phase))
    r3 = np.array(trefoil_knot_parametric(t + 3*dt, scale, phase))
    
    # First, second, third derivatives
    dr = (r1 - r) / dt
    d2r = (r2 - 2*r1 + r) / (dt**2)
    d3r = (r3 - 3*r2 + 3*r1 - r) / (dt**3)
    
    # Curvature
    cross = np.cross(dr, d2r)
    kappa = np.linalg.norm(cross) / (np.linalg.norm(dr)**3 + 1e-10)
    
    # Torsion
    cross_norm_sq = np.dot(cross, cross)
    if cross_norm_sq > 1e-10:
        tau = np.dot(cross, d3r) / cross_norm_sq
    else:
        tau = 0.0
    
    return kappa, tau

# ======================
# DETERMINISTIC LOCKS
# ======================

def generate_deterministic_locks(scale, n_layers=8, n_arms=24):
    """Generate locks from Frenet frame (Tier 1)."""
    locks = []
    t_samples = np.linspace(0, 2*np.pi, n_arms, endpoint=False)
    
    for t in t_samples:
        x0, y0, z0 = trefoil_knot_parametric(t, scale, 0.0)
        T, N, B = trefoil_frenet_frame(t, scale, 0.0)
        
        for layer in range(n_layers):
            r = scale * (KNOT_RATIO ** layer)
            
            # Locks along frame directions
            for direction in [N, -N, B, -B]:
                locks.append([
                    x0 + r * direction[0],
                    y0 + r * direction[1],
                    z0 + r * direction[2]
                ])
            
            # Diagonal combinations
            for sign_n in [-1, 1]:
                for sign_b in [-1, 1]:
                    r_diag = r / np.sqrt(2)
                    locks.append([
                        x0 + sign_n * r_diag * N[0] + sign_b * r_diag * B[0],
                        y0 + sign_n * r_diag * N[1] + sign_b * r_diag * B[1],
                        z0 + sign_n * r_diag * N[2] + sign_b * r_diag * B[2]
                    ])
    
    return np.array(locks)

# ======================
# PHYSICS
# ======================

def compute_continuous_scale(frame, n_frames):
    """Continuous zoom (Tier 1)."""
    progress = frame / n_frames
    n_max = np.log(SCALE_CMB / SCALE_PROTON) / np.log(3.0)
    n_current = progress * n_max
    scale = SCALE_CMB * (KNOT_RATIO ** n_current)
    return scale, n_current

def calculate_mass_from_knot(scale, frequency):
    """Mass from geometry (Tier 1)."""
    omega = 2 * np.pi * frequency
    r_wound = scale * 0.1
    K_torsion = CROSSING_NUMBER
    mass = (HBAR / (C**2)) * omega * K_torsion / r_wound
    return mass, r_wound

def calculate_frequency(scale):
    """Characteristic frequency."""
    return C / scale

def get_narrative_text(scale):
    """Get narrative text for current scale."""
    for name, s_val, narrative in SCALES:
        if abs(np.log10(scale/s_val)) < 0.3:  # Within 2x of scale
            return name, narrative
    return "Transition", "Scaling continuously by 1/3..."

# ======================
# VISUALIZATION
# ======================

def create_tier2_animation():
    """Create Tier 2 animation with enhanced rigor."""
    
    print("\n[*] Pre-computing deterministic locks...")
    reference_scale = 1.0
    reference_locks = generate_deterministic_locks(reference_scale)
    n_locks = len(reference_locks)
    print(f"[✓] Generated {n_locks} deterministic locks")
    
    print("\n[*] Pre-computing curvature/torsion profiles...")
    t_samples = np.linspace(0, 2*np.pi, 50)
    kappa_profile = []
    tau_profile = []
    for t in t_samples:
        k, tau = compute_curvature_torsion(t, 1.0, 0.0)
        kappa_profile.append(k)
        tau_profile.append(tau)
    kappa_profile = np.array(kappa_profile)
    tau_profile = np.array(tau_profile)
    print(f"[✓] Average κ = {np.mean(kappa_profile):.3f}, τ = {np.mean(tau_profile):.3f}")
    
    print("\n[*] Setting up visualization...")
    
    fig = plt.figure(figsize=(22, 12), facecolor='#000000')
    gs = GridSpec(3, 4, figure=fig, hspace=0.4, wspace=0.4,
                  left=0.04, right=0.96, top=0.92, bottom=0.05)
    
    # Main 3D view (spans 2 columns)
    ax_3d = fig.add_subplot(gs[:, :2], projection='3d')
    
    # Right column panels
    ax_narrative = fig.add_subplot(gs[0, 2:])  # Narrative text
    ax_curvature = fig.add_subplot(gs[1, 2])    # Curvature plot
    ax_torsion = fig.add_subplot(gs[1, 3])      # Torsion plot
    ax_mass = fig.add_subplot(gs[2, 2])         # Mass equation
    ax_scale = fig.add_subplot(gs[2, 3])        # Scale ladder
    
    # Pre-compute knot curve
    t_knot = np.linspace(0, 2*np.pi, 200)
    
    # Storage for ghost knots
    ghost_scales = [1.0, 1.0/3.0, 1.0/9.0]  # Current, -1 layer, -2 layers
    
    def update(frame):
        scale, layer_n = compute_continuous_scale(frame, N_FRAMES)
        freq = calculate_frequency(scale)
        mass, r_wound = calculate_mass_from_knot(scale, freq)
        
        # Phase for breathing and rotation
        phase = 2 * np.pi * frame / N_FRAMES
        breathing = 0.05  # 5% amplitude breathing
        
        # Get narrative
        scale_name, narrative = get_narrative_text(scale)
        
        # Clear axes
        ax_3d.clear()
        ax_narrative.clear()
        ax_curvature.clear()
        ax_torsion.clear()
        ax_mass.clear()
        ax_scale.clear()
        
        # Backgrounds
        ax_3d.set_facecolor('#000000')
        for ax in [ax_narrative, ax_curvature, ax_torsion, ax_mass, ax_scale]:
            ax.set_facecolor('#0a0a0a')
        
        # === 3D KNOT WITH GHOSTS ===
        
        vis_scale = 1.0
        
        # Draw GHOST knots (previous scales, faded)
        for i, ghost_ratio in enumerate(ghost_scales[1:]):
            ghost_scale = vis_scale * ghost_ratio
            x_g, y_g, z_g = trefoil_knot_parametric(t_knot, ghost_scale, phase * 0.3)
            
            alpha_ghost = 0.15 / (i + 1)  # Fade older ghosts more
            ax_3d.plot(x_g, y_g, z_g, 'cyan', linewidth=2, 
                      alpha=alpha_ghost, linestyle='--')
        
        # Draw MAIN knot (current scale) with breathing
        x, y, z = trefoil_knot_parametric(t_knot, vis_scale, phase * 0.3, breathing)
        
        colors = plt.cm.plasma(np.linspace(0, 1, len(x)))
        for i in range(len(x) - 1):
            ax_3d.plot(x[i:i+2], y[i:i+2], z[i:i+2],
                      color=colors[i], linewidth=5, alpha=0.95)
        
        # Locks (scaled with breathing)
        lock_scale = vis_scale * (1.0 + breathing * np.sin(phase * 5))
        scaled_locks = reference_locks * lock_scale
        ax_3d.scatter(scaled_locks[:, 0], scaled_locks[:, 1], scaled_locks[:, 2],
                     c='cyan', s=3, alpha=0.5, edgecolors='none')
        
        # Wound thickness bar
        thickness_vis = (r_wound / scale) * vis_scale
        ax_3d.plot([0, thickness_vis], [0, 0], [0, 0],
                  'r-', linewidth=10, alpha=0.9, 
                  label=f'r_wound = {r_wound:.2e} m')
        
        # Setup
        ax_3d.set_xlim(-4, 4)
        ax_3d.set_ylim(-4, 4)
        ax_3d.set_zlim(-2, 2)
        ax_3d.view_init(elev=20, azim=frame * 360 / N_FRAMES)
        
        ax_3d.xaxis.pane.fill = False
        ax_3d.yaxis.pane.fill = False
        ax_3d.zaxis.pane.fill = False
        ax_3d.grid(False)
        ax_3d.set_xticks([])
        ax_3d.set_yticks([])
        ax_3d.set_zticks([])
        
        ax_3d.text2D(0.5, 0.98, f"{scale_name}",
                    transform=ax_3d.transAxes, color='white',
                    fontsize=22, fontweight='bold', ha='center', va='top')
        
        ax_3d.legend(loc='upper left', fontsize=9, framealpha=0.7)
        
        # === NARRATIVE TEXT ===
        
        ax_narrative.axis('off')
        
        narrative_box = f"""
{scale_name.upper()}

{narrative}

Scale: {scale:.2e} m
Layer: n = {layer_n:.2f}
        """
        
        ax_narrative.text(0.5, 0.5, narrative_box.strip(),
                         transform=ax_narrative.transAxes,
                         fontsize=11, color='white',
                         ha='center', va='center',
                         bbox=dict(boxstyle='round', facecolor='#1a1a3a',
                                  edgecolor='cyan', linewidth=2, pad=15))
        
        # === CURVATURE PLOT ===
        
        ax_curvature.plot(t_samples, kappa_profile, 'lime', linewidth=2)
        ax_curvature.fill_between(t_samples, 0, kappa_profile, 
                                 alpha=0.3, color='lime')
        ax_curvature.set_xlabel('t (parameter)', color='gray', fontsize=9)
        ax_curvature.set_ylabel('Curvature κ', color='lime', fontsize=10)
        ax_curvature.set_title('Knot Curvature', color='white', fontsize=10)
        ax_curvature.tick_params(colors='gray', labelsize=8)
        ax_curvature.grid(True, alpha=0.2, color='gray')
        
        # Add mean line
        mean_k = np.mean(kappa_profile)
        ax_curvature.axhline(mean_k, color='yellow', linestyle='--', 
                            linewidth=1, alpha=0.6)
        ax_curvature.text(0.95, 0.95, f'⟨κ⟩ = {mean_k:.3f}',
                         transform=ax_curvature.transAxes,
                         color='yellow', fontsize=8, ha='right', va='top')
        
        # === TORSION PLOT ===
        
        ax_torsion.plot(t_samples, tau_profile, 'orange', linewidth=2)
        ax_torsion.fill_between(t_samples, 0, tau_profile,
                               alpha=0.3, color='orange')
        ax_torsion.set_xlabel('t (parameter)', color='gray', fontsize=9)
        ax_torsion.set_ylabel('Torsion τ', color='orange', fontsize=10)
        ax_torsion.set_title('Knot Torsion', color='white', fontsize=10)
        ax_torsion.tick_params(colors='gray', labelsize=8)
        ax_torsion.grid(True, alpha=0.2, color='gray')
        
        mean_tau = np.mean(tau_profile)
        ax_torsion.axhline(mean_tau, color='yellow', linestyle='--',
                          linewidth=1, alpha=0.6)
        ax_torsion.text(0.95, 0.95, f'⟨τ⟩ = {mean_tau:.3f}',
                       transform=ax_torsion.transAxes,
                       color='yellow', fontsize=8, ha='right', va='top')
        
        # === MASS EQUATION ===
        
        ax_mass.axis('off')
        
        mass_gev = mass * C**2 / 1.60218e-10
        
        mass_text = f"""
MASS FROM GEOMETRY

m = (ℏ/c²) × ω × K × (1/r_wound)

ω = {freq:.2e} rad/s
K = {CROSSING_NUMBER}
r_wound = {r_wound:.2e} m

m = {mass:.2e} kg
  = {mass_gev:.2e} GeV/c²
        """
        
        ax_mass.text(0.5, 0.5, mass_text.strip(),
                    transform=ax_mass.transAxes,
                    fontsize=8, family='monospace',
                    color='white', ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='#1a1a2a',
                             edgecolor='red', linewidth=1, pad=8))
        
        # === SCALE LADDER ===
        
        log_range = np.log10(SCALE_CMB / SCALE_PROTON)
        log_current = np.log10(scale / SCALE_PROTON)
        progress = log_current / log_range
        
        ax_scale.barh([0], [progress], height=0.6, color='lime', alpha=0.9)
        ax_scale.barh([0], [1], height=0.6, color='gray', alpha=0.15)
        
        # Mark scales
        for i, (s_name, s_val, _) in enumerate(SCALES):
            log_pos = np.log10(s_val / SCALE_PROTON) / log_range
            ax_scale.axvline(log_pos, color='yellow', linestyle='--',
                           alpha=0.4, linewidth=1)
        
        ax_scale.set_xlim(0, 1)
        ax_scale.set_ylim(-0.5, 1)
        ax_scale.set_yticks([])
        ax_scale.set_xlabel('Progress', color='gray', fontsize=9)
        ax_scale.set_title('Scale: CMB → Proton', color='white', fontsize=10)
        ax_scale.tick_params(colors='gray', labelsize=8)
        
        ax_scale.text(0.5, -0.2, f'n = {layer_n:.2f}',
                     transform=ax_scale.transAxes, color='cyan',
                     fontsize=9, ha='center')
        
        # Main title
        fig.suptitle('THE COSMIC KNOT: Unified Structure (Tier 2 - Enhanced Rigor)',
                    color='white', fontsize=18, fontweight='bold')
        
        if (frame + 1) % 20 == 0:
            print(f"  Frame {frame+1}/{N_FRAMES} | {scale_name}")
        
        return ax_3d, ax_narrative, ax_curvature, ax_torsion, ax_mass, ax_scale
    
    print("\n[*] Generating animation...")
    anim = FuncAnimation(fig, update, frames=N_FRAMES,
                        interval=1000//FPS, blit=False, repeat=True)
    
    output_file = "cosmic_knot_tier2_enhanced.gif"
    print(f"\n[*] Saving to {output_file}...")
    anim.save(output_file, writer=PillowWriter(fps=FPS), dpi=100)
    
    print(f"\n[✓] Tier 2 animation complete!")
    print("=" * 70)

# ======================
# MAIN
# ======================

def main():
    create_tier2_animation()
    
    print("\n" + "=" * 70)
    print("TIER 2 ENHANCED RIGOR COMPLETE")
    print("=" * 70)
    print("\nNew Features:")
    print("  ✓ Ghost overlays (1/3 scaling visible)")
    print("  ✓ Curvature κ and torsion τ metrics")
    print("  ✓ Narrative text synced to scales")
    print("  ✓ Phase breathing (5% amplitude)")
    print("\nNext: Tier 3 adds cinematic polish, real CMB data")
    print("=" * 70)

if __name__ == "__main__":
    main()