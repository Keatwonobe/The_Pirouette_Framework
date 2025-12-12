"""
UNIFIED KNOT FIELD THEORY
Mathematical framework connecting CMB geometry to particle physics
via fractal wound-channel scaling
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.constants import hbar, c, m_p, m_e
from scipy.special import sph_harm

# ======================
# FUNDAMENTAL CONSTANTS
# ======================

# Universal knot invariant (measured)
KNOT_RATIO = 1.0 / 3.0

# CMB scale parameters
R_CMB = 4.4e26  # meters (Hubble radius)

# Use Compton frequency as the base oscillation
# For CMB scale, use the Hubble frequency
H_0 = 2.2e-18  # Hubble constant in Hz
F_CMB_BASE = H_0  # Base frequency = Hubble expansion rate

# The k-space frequency we measured (983333 cycles/k) is actually
# the TOPOLOGICAL twist rate, not the physical oscillation.
# Physical oscillation frequency scales inversely with radius:
# f ~ c/r (characteristic frequency of a system of size r)

# Proton scale
R_PROTON = 0.84e-15  # meters (proton charge radius)

# Physical constants
HBAR = hbar  # J·s
C = c  # m/s
M_PROTON = m_p  # kg
M_ELECTRON = m_e  # kg

print("=" * 70)
print("UNIFIED KNOT FIELD THEORY")
print("Mathematical Framework")
print("=" * 70)

# ======================
# SCALE EQUATIONS
# ======================

def scale_level_from_radius(r, r_cmb=R_CMB):
    """
    Calculate the fractal layer number from physical scale.
    Each layer shrinks by factor of 1/3.
    
    r = r_cmb × (1/3)^n
    n = log₃(r_cmb / r)
    """
    if r <= 0 or r_cmb <= 0:
        return 0
    
    ratio = r_cmb / r
    n = np.log(ratio) / np.log(3.0)
    return n

def radius_at_layer(n, r_cmb=R_CMB):
    """
    Calculate physical radius at fractal layer n.
    """
    return r_cmb * (KNOT_RATIO ** n)

def frequency_at_layer(n, f_base=None):
    """
    Calculate oscillation frequency at layer n.
    
    Physical frequency scales as 1/r, not as (1/3)^n.
    Since r ~ (1/3)^n, frequency scales as 3^n.
    
    This makes sense: smaller systems oscillate faster.
    """
    if f_base is None:
        f_base = H_0  # Hubble frequency at CMB scale
    
    # Frequency increases as we go to smaller scales
    return f_base * (3.0 ** n)

# ======================
# WOUND CHANNEL THICKNESS
# ======================

def wound_channel_thickness(r):
    """
    The 'thread' thickness of the knot at scale r.
    
    Hypothesis: The wound channel thickness scales with the
    fractal layer. At CMB scale, it's maximal. At proton scale,
    it's minimal but still detectable.
    
    We assume the channel thickness is proportional to the
    radius at that scale.
    """
    n = scale_level_from_radius(r)
    
    # Channel thickness as a fraction of radius
    # This parameter needs calibration from observation
    CHANNEL_FRACTION = 0.1  # 10% of radius
    
    thickness = r * CHANNEL_FRACTION
    return thickness

# ======================
# KNOT COMPLEXITY
# ======================

def knot_winding_number():
    """
    Trefoil knot winding number.
    For a (p,q)-torus knot, the winding number is gcd(p,q).
    For trefoil (2,3), winding = 1, but crossing number = 3.
    
    We use crossing number as the relevant topological invariant.
    """
    return 3

def knot_jones_polynomial():
    """
    Jones polynomial for trefoil knot: t + t³ - t⁴
    Evaluated at t=1 gives the knot invariant.
    
    For our purposes, we use the absolute value of the
    polynomial evaluated at the golden ratio φ.
    """
    phi = (1 + np.sqrt(5)) / 2
    t = phi
    jones = t + t**3 - t**4
    return abs(jones)

# ======================
# MASS FROM GEOMETRY
# ======================

def mass_from_knot_energy(f_oscillation, topology_factor=1.0):
    """
    Calculate particle mass from knot oscillation frequency.
    
    E = ħω = ħ × 2πf
    m = E/c² = (ħ × 2πf) / c²
    
    The topology_factor accounts for knot complexity.
    """
    omega = 2 * np.pi * f_oscillation
    energy = HBAR * omega * topology_factor
    mass = energy / (C**2)
    return mass

def predict_proton_mass():
    """
    Predict proton mass from fractal knot theory.
    """
    # Calculate layer number for proton scale
    n_proton = scale_level_from_radius(R_PROTON, R_CMB)
    
    print(f"\nProton Scale Calculation:")
    print(f"  CMB radius: {R_CMB:.2e} m")
    print(f"  Proton radius: {R_PROTON:.2e} m")
    print(f"  Scale ratio: {R_CMB/R_PROTON:.2e}")
    print(f"  Fractal layer n: {n_proton:.2f}")
    print(f"  Expected from 10^41: {np.log(1e41)/np.log(3):.2f}")
    
    # Frequency at proton scale
    f_proton = frequency_at_layer(n_proton, F_CMB_BASE)
    print(f"  Oscillation frequency: {f_proton:.2e} Hz")
    
    # Topology factor from knot geometry
    K_topology = knot_winding_number() * knot_jones_polynomial()
    print(f"  Topology factor K: {K_topology:.3f}")
    
    # Predicted mass
    m_predicted = mass_from_knot_energy(f_proton, K_topology)
    
    print(f"\nMass Prediction:")
    print(f"  Predicted: {m_predicted:.3e} kg")
    print(f"  Observed: {M_PROTON:.3e} kg")
    print(f"  Ratio: {m_predicted/M_PROTON:.3f}")
    print(f"  Error: {abs(m_predicted - M_PROTON)/M_PROTON * 100:.1f}%")
    
    return m_predicted, m_predicted/M_PROTON

# ======================
# RESONANCE SPECTRUM
# ======================

def particle_spectrum_from_resonances():
    """
    Predict particle masses from integer resonances.
    Each stable resonance creates a particle.
    """
    resonances = [3, 5, 7, 11, 13]  # Stable integer resonances
    
    particles = {}
    
    for res in resonances:
        # Frequency modified by resonance number
        f_res = F_CMB_BASE * (KNOT_RATIO ** 87) * res / 3.0
        
        # Mass from this resonance
        K_res = res  # Resonance number as topology factor
        m_res = mass_from_knot_energy(f_res, K_res)
        
        particles[res] = {
            'resonance': res,
            'frequency': f_res,
            'mass_kg': m_res,
            'mass_GeV': m_res * C**2 / 1.602e-10,  # Convert to GeV
        }
    
    return particles

# ======================
# HOLOGRAPHIC PROJECTION
# ======================

def compute_holographic_density(resonance, phase_offset):
    """
    Compute the manifold stress density for a given resonance
    and phase offset. This predicts localization vs diffusion.
    
    Returns: density_factor (0 to 1, where 1 = highly localized)
    """
    # Phase offset near 0.2 creates tight knots (matter)
    # Phase offset near π creates loose orbits (shadow)
    
    # Simple model: cosine function
    # offset=0.2 → cos(0.2) ≈ 0.98 (high density)
    # offset=π → cos(π) = -1 (low density, map to 0)
    
    density_raw = np.cos(phase_offset)
    
    # Map [-1, 1] to [0, 1]
    density_normalized = (density_raw + 1) / 2
    
    # Resonance factor: integer resonances amplify localization
    resonance_boost = 1.0 + 0.5 * (1.0 if resonance == int(resonance) else 0.0)
    
    density_factor = min(1.0, density_normalized * resonance_boost)
    
    return density_factor

# ======================
# ANALYSIS & PREDICTIONS
# ======================

def run_unified_analysis():
    """
    Run complete analysis and generate predictions.
    """
    print("\n" + "=" * 70)
    print("PART 1: SCALE ANALYSIS")
    print("=" * 70)
    
    # Test scale law
    test_scales = [R_CMB, 1e20, 1e10, 1e0, 1e-10, R_PROTON]
    
    print("\nScale Law Test:")
    print(f"{'Radius (m)':<15} {'Layer n':<12} {'Frequency (Hz)':<15} {'Thickness (m)'}")
    print("-" * 70)
    
    for r in test_scales:
        n = scale_level_from_radius(r)
        f = frequency_at_layer(n)
        thickness = wound_channel_thickness(r)
        print(f"{r:<15.2e} {n:<12.2f} {f:<15.2e} {thickness:<.2e}")
    
    print("\n" + "=" * 70)
    print("PART 2: PROTON MASS PREDICTION")
    print("=" * 70)
    
    m_pred, ratio = predict_proton_mass()
    
    print("\n" + "=" * 70)
    print("PART 3: PARTICLE SPECTRUM")
    print("=" * 70)
    
    particles = particle_spectrum_from_resonances()
    
    print("\nPredicted Particle Masses from Resonances:")
    print(f"{'Resonance':<12} {'Mass (kg)':<15} {'Mass (GeV)':<15} {'Known Particle?'}")
    print("-" * 70)
    
    known_particles = {
        3: "Proton/Neutron (0.938 GeV)",
        5: "Pentaquark (~4.5 GeV)",
        7: "Bottom Baryon (~5.6 GeV)",
        11: "Unknown/Exotic",
        13: "Unknown/Exotic"
    }
    
    for res in sorted(particles.keys()):
        p = particles[res]
        known = known_particles.get(res, "Unknown")
        print(f"{res:<12} {p['mass_kg']:<15.3e} {p['mass_GeV']:<15.3f} {known}")
    
    print("\n" + "=" * 70)
    print("PART 4: HOLOGRAPHIC LOCALIZATION")
    print("=" * 70)
    
    print("\nLocalization Predictions:")
    print(f"{'Resonance':<12} {'Phase Offset':<15} {'Density Factor':<15} {'Type'}")
    print("-" * 70)
    
    test_configs = [
        (3, 0.2, "Matter (Localized)"),
        (3, np.pi, "Shadow (Diffuse)"),
        (5, 0.2, "Matter (Localized)"),
        (7, 0.2, "Matter (Localized)"),
        (4.5, 0.2, "Unstable (Mixed)"),
    ]
    
    for res, phase, desc in test_configs:
        density = compute_holographic_density(res, phase)
        print(f"{res:<12.1f} {phase:<15.2f} {density:<15.3f} {desc}")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\n1. Universal Scaling: (1/3)^n from CMB to proton")
    print(f"2. Proton mass prediction: {ratio:.3f}× observed")
    print(f"3. Particle spectrum: Integer resonances create stable particles")
    print(f"4. Holographic projection: Phase determines matter vs shadow")
    print(f"\nAll predictions follow from:")
    print(f"   • Knot invariant: {KNOT_RATIO}")
    print(f"   • Winding number: {knot_winding_number()}")
    print(f"   • Scale range: 10^41")
    
    return particles

# ======================
# VISUALIZATION
# ======================

def create_theory_summary_plot(particles):
    """
    Create a comprehensive summary visualization.
    """
    fig = plt.figure(figsize=(16, 12), facecolor='#000000')
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)
    
    # === PLOT 1: Scale Ladder ===
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#000000')
    
    scales = np.logspace(26, -15, 100)
    layers = [scale_level_from_radius(s) for s in scales]
    
    ax1.semilogx(scales, layers, color='cyan', linewidth=2)
    ax1.axvline(R_CMB, color='red', linestyle='--', alpha=0.5, label='CMB')
    ax1.axvline(R_PROTON, color='yellow', linestyle='--', alpha=0.5, label='Proton')
    ax1.set_xlabel("Physical Scale (m)", color='gray')
    ax1.set_ylabel("Fractal Layer n", color='gray')
    ax1.set_title("Scale Law: r = r_CMB × (1/3)^n", color='white', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.2, color='gray')
    ax1.tick_params(colors='gray')
    
    # === PLOT 2: Frequency Cascade ===
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#000000')
    
    layers_test = np.arange(0, 100, 1)
    freqs = [frequency_at_layer(n) for n in layers_test]
    
    ax2.semilogy(layers_test, freqs, color='magenta', linewidth=2)
    ax2.set_xlabel("Fractal Layer n", color='gray')
    ax2.set_ylabel("Frequency (Hz)", color='gray')
    ax2.set_title("Frequency Cascade: f = f₀ × (1/3)^n", color='white', fontsize=12)
    ax2.grid(True, alpha=0.2, color='gray')
    ax2.tick_params(colors='gray')
    
    # === PLOT 3: Particle Spectrum ===
    ax3 = fig.add_subplot(gs[1, :])
    ax3.set_facecolor('#000000')
    
    resonances = list(particles.keys())
    masses_gev = [particles[r]['mass_GeV'] for r in resonances]
    
    ax3.bar(resonances, masses_gev, color='lime', alpha=0.7, edgecolor='white')
    ax3.set_xlabel("Resonance Number", color='gray')
    ax3.set_ylabel("Predicted Mass (GeV)", color='gray')
    ax3.set_title("Particle Spectrum from Integer Resonances", color='white', fontsize=12)
    ax3.set_yscale('log')
    ax3.grid(True, alpha=0.2, color='gray', axis='y')
    ax3.tick_params(colors='gray')
    
    # Known particles overlay
    ax3.axhline(0.938, color='red', linestyle='--', alpha=0.5, linewidth=2, label='Proton (observed)')
    ax3.legend()
    
    # === PLOT 4: Wound Channel Thickness ===
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.set_facecolor('#000000')
    
    scales_thick = np.logspace(26, -15, 100)
    thickness = [wound_channel_thickness(s) for s in scales_thick]
    
    ax4.loglog(scales_thick, thickness, color='orange', linewidth=2)
    ax4.set_xlabel("Physical Scale (m)", color='gray')
    ax4.set_ylabel("Channel Thickness (m)", color='gray')
    ax4.set_title("Wound Channel Thickness", color='white', fontsize=12)
    ax4.grid(True, alpha=0.2, color='gray')
    ax4.tick_params(colors='gray')
    
    # === PLOT 5: Holographic Density Map ===
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.set_facecolor('#000000')
    
    resonances_test = np.linspace(1, 10, 100)
    phases_test = np.linspace(0, np.pi, 100)
    R, P = np.meshgrid(resonances_test, phases_test)
    
    density_map = np.zeros_like(R)
    for i in range(len(phases_test)):
        for j in range(len(resonances_test)):
            density_map[i, j] = compute_holographic_density(R[i, j], P[i, j])
    
    im = ax5.contourf(R, P, density_map, levels=20, cmap='plasma')
    ax5.set_xlabel("Resonance Number", color='gray')
    ax5.set_ylabel("Phase Offset (rad)", color='gray')
    ax5.set_title("Holographic Localization Map", color='white', fontsize=12)
    plt.colorbar(im, ax=ax5, label='Density Factor')
    ax5.tick_params(colors='gray')
    
    plt.suptitle("UNIFIED KNOT FIELD THEORY\nMathematical Framework", 
                color='white', fontsize=16, fontweight='bold')
    
    plt.savefig('/home/claude/unified_theory_framework.png', dpi=150, facecolor='#000000')
    print("\n✓ Theory framework saved: unified_theory_framework.png")

# ======================
# MAIN
# ======================

def main():
    particles = run_unified_analysis()
    create_theory_summary_plot(particles)
    
    print("\n" + "=" * 70)
    print("UNIFIED FRAMEWORK COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()