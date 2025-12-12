import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
#  The Stability Scanner: Mapping the Forbidden Zones
# ==========================================================

# --- Configuration ---
LOBE_MIN, LOBE_MAX = 1.0, 10.0
LOBE_RES = 2000     # Resolution for Lobes (X-axis)

ANGLE_MIN, ANGLE_MAX = 0.0, 5
ANGLE_RES = 2000    # Resolution for Angles (Y-axis)

STEPS = 2000       # Steps per simulation (Fast scan)
DT = 0.005
DECAY = 0.9995     # Slight decay to test convergence

# --- Fast Physics Engine ---
def simulate_stability(lobes, angle_offset):
    """
    Runs a quick simulation for a specific Lobe/Angle configuration.
    Returns a 'Stability Score'.
    """
    t = np.linspace(0, 50 * np.pi, STEPS)
    
    # Base Radius (Decaying)
    r_base = np.power(DECAY, np.arange(STEPS)) * 5.0
    
    # Rotational Dynamics
    theta = 2.0 * t
    
    # Traveler 1 Trajectory
    x1 = r_base * np.cos(theta)
    y1 = r_base * np.sin(theta)
    
    # Traveler 2 Trajectory (Offset by Angle + Pi)
    # The 'angle_offset' changes the phase relationship between the two travelers
    x2 = r_base * np.cos(theta + np.pi + angle_offset)
    y2 = r_base * np.sin(theta + np.pi + angle_offset)
    
    # Manifold Interaction (Z-axis Tear)
    # This is where the Resonance (lobes) creates the shape
    z_amp = r_base * 1.5 * 0.5
    
    z1 = z_amp * np.sin(lobes * theta)
    z2 = z_amp * np.sin(lobes * theta + np.pi + angle_offset)
    
    # --- METRIC CALCULATION ---
    # We want to measure "Resonance" vs "Chaos".
    # Stable Particles (Knots) tend to have periodic interactions.
    # Unstable ones might drift or destructively interfere.
    
    # Let's measure the "Interaction Distance Variance".
    # If they lock into a knot, the distance between them should oscillate regularly.
    # If they are chaotic, the distance variance might be high or irregular.
    
    dist = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
    
    # "Score":
    # Low Variance relative to Mean = Stable Orbit (Circle/Torus)
    # High Variance = Lobe/Knot structure (The arms of the star)
    # We are looking for "Hot Valleys" -> High Structure.
    
    # We define "Stability" here as the AMPLITUDE of the interaction oscillation.
    # Integers (3, 4, 5) create large, distinct loops (High Amplitude).
    # Non-integers create a 'mush' (Low Amplitude / Noise).
    
    # Normalize by current radius to remove decay effect
    normalized_dist = dist / (r_base + 1e-9)
    score = np.std(normalized_dist) 
    
    return score

def run_scan():
    print(f"[*] Scanning Parameter Space ({LOBE_RES}x{ANGLE_RES})...")
    
    lobes = np.linspace(LOBE_MIN, LOBE_MAX, LOBE_RES)
    angles = np.linspace(ANGLE_MIN, ANGLE_MAX, ANGLE_RES)
    
    stability_map = np.zeros((ANGLE_RES, LOBE_RES))
    
    for i, ang in enumerate(angles):
        for j, lobe in enumerate(lobes):
            stability_map[i, j] = simulate_stability(lobe, ang)
            
    return lobes, angles, stability_map

def plot_stability_map(lobes, angles, stability_map):
    plt.figure(figsize=(14, 8))
    
    # Plot Heatmap
    # X-axis: Resonance (Lobes)
    # Y-axis: Offset (Initial Angle)
    # Color: Stability/Structure Score
    
    plt.imshow(stability_map, extent=[LOBE_MIN, LOBE_MAX, ANGLE_MIN, ANGLE_MAX], 
               origin='lower', aspect='auto', cmap='inferno')
    
    plt.colorbar(label="Structural Resonance (Knot Intensity)")
    
    plt.xlabel("Harmonic Resonance (Lobe Count)", fontsize=12)
    plt.ylabel("Phase Offset (Initial Angle)", fontsize=12)
    plt.title("The Map of Forbidden Zones: Stability Islands", fontsize=16)
    
    # Mark Integers for reference
    for k in range(int(LOBE_MIN), int(LOBE_MAX)+1):
        plt.axvline(k, color='cyan', linestyle='--', alpha=0.3)
        plt.text(k, ANGLE_MAX + 0.1, str(k), color='cyan', ha='center')

    plt.tight_layout()
    plt.savefig('stability_map.png', dpi=150)
    print("✅ Scan Complete. Map saved to 'stability_map.png'")

if __name__ == "__main__":
    l, a, m = run_scan()
    plot_stability_map(l, a, m)