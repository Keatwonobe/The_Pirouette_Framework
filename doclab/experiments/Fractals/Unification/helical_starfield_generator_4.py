import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
W_RESONANCE = 1.0047
LOCKED_TURNS = 30.00   # The integer resonance we found
ANCHOR_STAR = "Galactic Center"

# Expanded Star List (Name, RA, Dec)
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
    Returns the Phase Angle (0 to 2pi) relative to the ideal helix.
    """
    # 1. Coordinate Setup
    phi = np.deg2rad(l)
    theta = np.deg2rad(90 - b)
    z = np.cos(theta)
    h_idx = (z + 1) / 2.0
    
    # 2. Ideal Helix Phase
    # The angle the helix WOUL be at if it started at 0
    ideal_phi = (h_idx * turns * 2 * np.pi * w) % (2 * np.pi)
    
    # 3. The Difference (Raw Offset)
    # We don't take abs() here because we want to know Direction (Lead vs Lag)
    delta = (phi - ideal_phi) % (2 * np.pi)
    
    return h_idx, delta

def main():
    names, l, b = get_data()
    
    # 1. Establish the Anchor Offset
    # We need to rotate the whole system so Galactic Center is exactly at 0 degrees
    # Find GC index
    try:
        gc_idx = names.index(ANCHOR_STAR)
        _, gc_raw_phase = calculate_phase_angle(l[gc_idx], b[gc_idx], LOCKED_TURNS, W_RESONANCE)
        SYSTEM_OFFSET = gc_raw_phase
        print(f"[*] Anchor '{ANCHOR_STAR}' found. Rotating system by {-np.degrees(SYSTEM_OFFSET):.2f} degrees.")
    except ValueError:
        SYSTEM_OFFSET = 0
        print("[!] Anchor not found. Using raw phase.")

    # 2. Calculate Final Phases for all stars
    helical_heights = []
    final_phases = []
    
    for i in range(len(names)):
        h, raw_phase = calculate_phase_angle(l[i], b[i], LOCKED_TURNS, W_RESONANCE)
        
        # Apply the anchor rotation
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
    ax.set_theta_zero_location("N") # 0 degrees at top
    ax.set_theta_direction(-1)      # Clockwise
    
    # Plot Stars
    # Theta = Phase Angle
    # R = Helical Height (Center = South Pole, Edge = North Pole)
    
    # Custom Colors based on "Groove Proximity"
    # Green = Main Groove (0 deg), Cyan = Shadow Groove (180 deg), Orange = Minor (Other)
    colors = []
    sizes = []
    
    for phase in final_phases:
        # Distance from 0 deg (Main Groove)
        d0 = min(phase, 2*np.pi - phase)
        # Distance from 180 deg (Shadow Groove)
        d180 = abs(phase - np.pi)
        
        if d0 < 0.1: # Close to Main
            colors.append('lime')
            sizes.append(150)
        elif d180 < 0.1: # Close to Shadow
            colors.append('cyan')
            sizes.append(120)
        else:
            colors.append('orange')
            sizes.append(80)

    ax.scatter(final_phases, helical_heights, c=colors, s=sizes, alpha=0.8, edgecolors='white', linewidth=0.5)
    
    # Labels
    for i, name in enumerate(names):
        # Push label slightly outward
        ax.annotate(name, (final_phases[i], helical_heights[i]), 
                   xytext=(5, 5), textcoords='offset points', 
                   color='white', fontsize=8, alpha=0.7)
        
    # Draw Groove Lines
    ax.plot([0, 0], [0, 1], color='lime', linestyle='--', alpha=0.5, label='Major Groove (0°)')
    ax.plot([np.pi, np.pi], [0, 1], color='cyan', linestyle='--', alpha=0.5, label='Shadow Groove (180°)')
    
    # Grid Styling
    ax.grid(True, color='#333333', linestyle=':')
    ax.set_rlabel_position(90)
    plt.yticks([0.25, 0.5, 0.75, 1.0], ['0.25', '0.50', '0.75', '1.0'], color='gray', size=8)
    plt.title(f"The Pirouette Phase Clock\n(Turns={LOCKED_TURNS}, Anchor={ANCHOR_STAR})", color='white', y=1.08)
    
    # Add a footer with the "Green Band" stats
    # Filter stars in the "Green Band" (approx 0.3 rad)
    band_stars = [names[i] for i, p in enumerate(final_phases) if 0.2 < p < 0.4]
    band_txt = f"Green Band (approx 17°): {', '.join(band_stars)}"
    plt.figtext(0.5, 0.02, band_txt, ha='center', color='orange', fontsize=9)

    plt.legend(loc='lower right', frameon=False, labelcolor='white')
    plt.savefig("helical_phase_clock.png", dpi=150)
    print("✅ Phase Clock Generated: helical_phase_clock.png")

if __name__ == "__main__":
    main()