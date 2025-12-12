import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
#  The Phase Governance Spiral: Visualizing the Control Structure
# ==========================================================

# --- Configuration ---
LOBES = 3.0       # Focusing on the "Proton" (Triangle)
STEPS = 3000      # Simulation steps per angle
DECAY = 0.9995

# --- Stability Function (Same physics, new view) ---
def measure_structure(angle_offset):
    t = np.linspace(0, 50 * np.pi, STEPS)
    r_base = np.power(DECAY, np.arange(STEPS)) * 5.0
    theta = 2.0 * t
    
    # Traveler 1
    x1 = r_base * np.cos(theta)
    y1 = r_base * np.sin(theta)
    
    # Traveler 2 (Offset by Phase)
    x2 = r_base * np.cos(theta + np.pi + angle_offset)
    y2 = r_base * np.sin(theta + np.pi + angle_offset)
    
    # Z-Tear (Resonance)
    z_amp = r_base * 1.5 * 0.5
    z1 = z_amp * np.sin(LOBES * theta)
    z2 = z_amp * np.sin(LOBES * theta + np.pi + angle_offset)
    
    # Metric: High Standard Deviation = High Structure (Knot)
    # Low Standard Deviation = Low Structure (Slip/Orbit)
    dist = np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
    normalized_dist = dist / (r_base + 1e-9)
    return np.std(normalized_dist)

def plot_phase_spiral():
    print("[*] Calculating Phase Governance Topology...")
    
    # Scan full 360 degrees (0 to 2*Pi)
    angles = np.linspace(0, 2*np.pi, 360)
    stability_scores = []
    
    for ang in angles:
        stability_scores.append(measure_structure(ang))
        
    stability_scores = np.array(stability_scores)
    
    # Normalize for plotting
    stability_scores = (stability_scores - stability_scores.min()) / (stability_scores.max() - stability_scores.min())
    
    # --- The Polar Plot ---
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='polar')
    
    # Plot the "Structure Field"
    # r = Stability (Structure), theta = Phase Offset
    ax.plot(angles, stability_scores, color='crimson', lw=2, label='Structure Intensity')
    ax.fill(angles, stability_scores, color='crimson', alpha=0.1)
    
    # Highlight the Critical Zones
    # The Knot Side (Phase ~ 0.2)
    ax.scatter(0.2, stability_scores[int(0.2/(2*np.pi)*360)], color='gold', s=100, zorder=5, label='Knot Side (Matter)')
    
    # The Transition (Phase ~ Pi/2)
    ax.scatter(np.pi/2, stability_scores[int((np.pi/2)/(2*np.pi)*360)], color='black', s=100, zorder=5, label='Neutral Transition')
    
    # The Slip Side (Phase ~ Pi)
    ax.scatter(np.pi, stability_scores[int(np.pi/(2*np.pi)*360)], color='blue', s=100, zorder=5, label='Slip Side (Ghost)')

    ax.set_title(f"The Phase Governance Spiral\n(Resonance: {int(LOBES)})", fontsize=15, pad=20)
    ax.set_rticks([]) # Hide radial ticks for clarity
    ax.legend(loc='lower right', bbox_to_anchor=(1.1, 0.1))
    
    plt.tight_layout()
    plt.savefig('phase_governance_spiral.png', dpi=150)
    print("✅ Spiral Captured. Saved to 'phase_governance_spiral.png'")

if __name__ == "__main__":
    plot_phase_spiral()