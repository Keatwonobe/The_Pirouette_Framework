import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
W_RESONANCE = 1.0047
LOCKED_TURNS = 30.00   # Fixed from previous optimization
ANCHOR_STAR = "Galactic Center"

# Expanded Star List (Name, RA, Dec) from helical_starfield_generator_2.py
STARS_DATA = [
    ("Galactic Center", 266.41, -29.00),
    ("Sirius", 101.28, -16.71),
    ("Canopus", 95.98, -52.69),
    ("Arcturus", 213.91, 19.18),
    ("Alpha Centauri", 219.90, -60.83),
    ("Vega", 279.23, 38.78),
    ("Rigel", 78.63, -8.20),
    ("Procyon", 114.82, 5.22),
    ("Betelgeuse", 88.79, 7.40),
    ("Achernar", 24.42, -57.23),
    ("Hadar", 210.80, -60.37),
    ("Capella", 79.17, 45.99),
    ("Altair", 297.69, 8.86),
    ("Aldebaran", 68.98, 16.50),
    ("Spica", 201.29, -11.16),
    ("Antares", 247.35, -26.43),
    ("Pollux", 116.32, 28.02),
    ("Fomalhaut", 344.41, -29.62),
    ("Deneb", 310.35, 45.28),
    ("Mimosa", 191.93, -59.69),
    ("Regulus", 152.09, 11.96),
    ("Castor", 113.65, 31.88),
    ("Gacrux", 187.79, -57.11),
    ("Shaula", 263.40, -37.10),
    ("North Pole", 0.0, 90.0),
]

def get_data():
    names = []
    l_list = []
    b_list = []
    print("[*] Calculating Galactic Phases...")
    for name, ra, dec in STARS_DATA:
        c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
        g = c.galactic
        names.append(name)
        l_list.append(g.l.degree)
        b_list.append(g.b.degree)
    return names, np.array(l_list), np.array(b_list)

def calculate_phase_angle(l, b, turns, w):
    """
    Returns the Raw Phase Angle (0 to 2pi) relative to the ideal helix.
    """
    phi = np.deg2rad(l)
    theta = np.deg2rad(90 - b)
    z = np.cos(theta)
    h_idx = (z + 1) / 2.0
    
    # Ideal Helix Phase (before offset)
    ideal_phi = (h_idx * turns * 2 * np.pi * w) % (2 * np.pi)
    
    # Raw Phase Difference (0 to 2pi) - Direction matters now!
    delta = (phi - ideal_phi) % (2 * np.pi)
    
    return h_idx, delta

def main():
    names, l, b = get_data()
    
    # 1. Establish the Anchor Offset (Rotate the system so GC is at 0)
    try:
        gc_idx = names.index(ANCHOR_STAR)
        _, gc_raw_phase = calculate_phase_angle(l[gc_idx], b[gc_idx], LOCKED_TURNS, W_RESONANCE)
        SYSTEM_OFFSET = gc_raw_phase
    except ValueError:
        SYSTEM_OFFSET = 0
    
    # 2. Calculate Final Phases for all stars
    helical_heights = []
    final_phases = []
    
    for i in range(len(names)):
        h, raw_phase = calculate_phase_angle(l[i], b[i], LOCKED_TURNS, W_RESONANCE)
        corrected_phase = (raw_phase - SYSTEM_OFFSET) % (2 * np.pi)
        
        helical_heights.append(h)
        final_phases.append(corrected_phase)

    # ======================
    # VISUALIZATION: The Phase Clock
    # ======================
    plt.figure(figsize=(10, 10), facecolor='#050505')
    ax = plt.subplot(111, projection='polar')
    ax.set_facecolor('#050505')
    
    # Plot Settings
    ax.set_theta_zero_location("N") # 0 degrees (Major Groove) at the top
    ax.set_theta_direction(-1)      # Clockwise
    
    # Draw Harmonic Lines (Potential Grooves)
    potential_grooves = [0, np.pi/20, np.pi/10, np.pi/4, np.pi/2, np.pi] # 0, 9, 18, 45, 90, 180 degrees
    for angle in potential_grooves:
        if angle != 0:
            # Draw the line and its mirror image
            ax.plot([angle, angle], [0, 1], color='red' if angle == np.pi/10 else '#333333', linestyle=':', alpha=0.5)
            ax.plot([2*np.pi - angle, 2*np.pi - angle], [0, 1], color='red' if angle == np.pi/10 else '#333333', linestyle=':', alpha=0.5)
    
    # Plot Stars
    for i, h in enumerate(helical_heights):
        phase = final_phases[i]
        
        # Color based on position relative to the helix cylinder:
        if np.abs(phase - 0) < 0.1 or np.abs(phase - 2*np.pi) < 0.1:
             color = 'lime' # Major Groove
        elif np.abs(phase - np.pi) < 0.1:
             color = 'cyan' # Shadow Groove (180 deg)
        elif 0.2 < phase < 0.4: # Our identified Green Band
             color = 'yellow' # Minor Groove Candidate
        else:
             color = 'orange'
             
        # Star size based on the square root of the height to make pole stars small
        size = 150 * (np.sqrt(h) + 0.1) 
             
        ax.scatter(phase, h, c=color, s=size, alpha=0.8, edgecolors='white', linewidth=0.5)
        
        # Label the most important stars for clarity
        if names[i] in ["Galactic Center", "Rigel", "Sirius", "Aldebaran", "Vega"]:
            ax.annotate(names[i], (phase, h), xytext=(5, 5), textcoords='offset points', color='white', fontsize=9, alpha=0.9)

    # Draw Resonance Lines
    ax.plot([0, 0], [0, 1], color='lime', linestyle='-', alpha=0.7, linewidth=2, label='Major Groove (0°)')
    ax.plot([np.pi, np.pi], [0, 1], color='cyan', linestyle='-', alpha=0.7, linewidth=2, label='Shadow Groove (180°)')
    
    # Final styling
    ax.grid(True, color='#333333', linestyle=':')
    ax.set_rlabel_position(90)
    plt.yticks([0.25, 0.5, 0.75, 1.0], ['0.25', '0.50', '0.75', '1.0 (N.Gal.Pole)'], color='gray', size=8)
    plt.title(f"The Helical Phase Clock: 30-Turn Resonance", color='white', y=1.08)
    plt.legend(loc='lower right', frameon=False, labelcolor='white')
    
    plt.savefig("helical_phase_clock_grooves.png", dpi=150)
    print("✅ Phase Clock Generated: helical_phase_clock_grooves.png")

if __name__ == "__main__":
    main()