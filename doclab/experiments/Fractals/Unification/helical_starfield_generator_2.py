import numpy as np
import matplotlib.pyplot as plt

# ======================
# CONFIGURATION
# ======================
W_RESONANCE = 1.0047  # The "Squaring the Circle" Resonance
HELIX_TURNS = 10      # Lower turns for clearer visualization of individual stars

# ======================
# REAL STAR DATA (Right Ascension, Declination)
# ======================
# Top 25 Brightest Stars + Notable Objects
# (Name, RA in Deg, Dec in Deg, Color for plot)
STARS = [
    ("Sirius", 101.28, -16.71, 'cyan'),
    ("Canopus", 95.98, -52.69, 'white'),
    ("Arcturus", 213.91, 19.18, 'orange'),
    ("Alpha Centauri", 219.90, -60.83, 'yellow'),
    ("Vega", 279.23, 38.78, 'cyan'),
    ("Rigel", 78.63, -8.20, 'blue'),
    ("Procyon", 114.82, 5.22, 'white'),
    ("Achernar", 24.42, -57.23, 'blue'),
    ("Betelgeuse", 88.79, 7.40, 'red'),
    ("Hadar", 210.80, -60.37, 'blue'),
    ("Capella", 79.17, 45.99, 'yellow'),
    ("Altair", 297.69, 8.86, 'white'),
    ("Aldebaran", 68.98, 16.50, 'orange'),
    ("Spica", 201.29, -11.16, 'blue'),
    ("Antares", 247.35, -26.43, 'red'),
    ("Pollux", 116.32, 28.02, 'orange'),
    ("Fomalhaut", 344.41, -29.62, 'white'),
    ("Deneb", 310.35, 45.28, 'white'),
    ("Mimosa", 191.93, -59.69, 'blue'),
    ("Regulus", 152.09, 11.96, 'blue'),
    ("Adhara", 104.65, -28.97, 'blue'),
    ("Castor", 113.65, 31.88, 'white'),
    ("Gacrux", 187.79, -57.11, 'red'),
    ("Shaula", 263.40, -37.10, 'blue'),
    # Significant Coordinate Points
    ("Galactic Center", 266.41, -29.00, 'magenta'),
    ("North Pole", 0.0, 90.0, 'green'),
]

# ======================
# HELICAL MATH
# ======================
def celestial_to_helical(ra, dec, w, turns):
    """
    Converts RA/Dec to Helical Index (h, phase_error).
    """
    # Convert RA/Dec (Equatorial) to Radians
    # Note: For strict physics we usually convert to Galactic (l,b) first, 
    # but let's see if the Equatorial frame resonates first.
    
    phi = np.deg2rad(ra)
    theta = np.deg2rad(90 - dec)
    
    # z projection (-1 to 1)
    z = np.cos(theta)
    
    # Helical Height Index (0 to 1)
    h_idx = (z + 1) / 2.0
    
    # Ideal Helical Phase
    ideal_phi = (h_idx * turns * 2 * np.pi * w) % (2 * np.pi)
    
    # Phase Drift (The "Error")
    phase_error = np.abs(phi - ideal_phi)
    phase_error = np.minimum(phase_error, 2*np.pi - phase_error)
    
    return h_idx, phase_error

# ======================
# MAIN
# ======================
def main():
    print(f"[*] Scanning {len(STARS)} Known Stars...")
    
    plt.figure(figsize=(12, 8), facecolor='#111111')
    ax = plt.gca()
    ax.set_facecolor('#111111')
    
    for name, ra, dec, color in STARS:
        h_idx, drift = celestial_to_helical(ra, dec, W_RESONANCE, HELIX_TURNS)
        
        # Plot
        # X-Axis = Helical Height (z)
        # Y-Axis = Phase Drift (How far "off wire" they are)
        plt.scatter(h_idx, drift, color=color, s=100, edgecolors='white', alpha=0.8)
        
        # Label with offset to avoid clutter
        plt.text(h_idx + 0.01, drift, name, color=color, fontsize=9, alpha=0.9)

    plt.title(f"Helical Indexing of Bright Stars\n(W={W_RESONANCE}, Turns={HELIX_TURNS})", color='white')
    plt.xlabel("Helical Height Index (0=South, 1=North)", color='gray')
    plt.ylabel("Phase Drift (Resonance Error)", color='gray')
    
    # Draw "Resonance Lines" (Zero Drift)
    plt.axhline(0, color='lime', linestyle='--', alpha=0.3, label='Perfect Resonance')
    plt.legend(loc='upper right')
    
    ax.tick_params(colors='gray')
    plt.grid(True, color='#333333', linestyle='--')
    
    plt.savefig("helical_bright_stars.png")
    print("✅ Scan complete. Saved to helical_bright_stars.png")

if __name__ == "__main__":
    main()