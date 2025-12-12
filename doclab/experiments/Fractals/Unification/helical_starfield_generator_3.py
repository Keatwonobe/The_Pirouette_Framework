import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
W_RESONANCE = 1.0047
SCAN_RANGE = (1, 50)  # Check Turn counts from 1 to 50

# ======================
# DATA: Brightest Stars + Anchors
# ======================
# (Name, RA deg, Dec deg)
STARS_DATA = [
    ("Galactic Center", 266.41, -29.00), # The Anchor
    ("Sirius", 101.28, -16.71),
    ("Canopus", 95.98, -52.69),
    ("Arcturus", 213.91, 19.18),
    ("Alpha Centauri", 219.90, -60.83),
    ("Vega", 279.23, 38.78),
    ("Rigel", 78.63, -8.20),
    ("Betelgeuse", 88.79, 7.40),
    ("Aldebaran", 68.98, 16.50),
    ("Antares", 247.35, -26.43),
]

def get_galactic_coords(stars):
    """Converts Earth RA/Dec to Galactic l/b"""
    coords = []
    names = []
    
    print(f"[*] Converting {len(stars)} objects to Galactic Frame...")
    for name, ra, dec in stars:
        c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
        g = c.galactic
        coords.append((g.l.degree, g.b.degree))
        names.append(name)
    return names, coords

def calculate_drift(l, b, turns, w, phase_offset_rad=0):
    """
    Calculates distance from the perfect helix line.
    """
    phi = np.deg2rad(l)
    theta = np.deg2rad(90 - b)
    
    # Helical Height (0 to 1)
    z = np.cos(theta)
    h_idx = (z + 1) / 2.0
    
    # Ideal Phase at this height
    ideal_phi = (h_idx * turns * 2 * np.pi * w + phase_offset_rad) % (2 * np.pi)
    
    # Shortest distance around the circle
    diff = np.abs(phi - ideal_phi)
    drift = np.minimum(diff, 2*np.pi - diff)
    
    return h_idx, drift

def optimize_helix(names, coords):
    """
    Finds the Turn Count that minimizes total drift for the list.
    """
    best_score = float('inf')
    best_turns = 0
    best_offset = 0
    
    # Find index of Galactic Center for anchoring
    try:
        gc_idx = names.index("Galactic Center")
    except ValueError:
        gc_idx = -1

    print("[*] Scanning frequencies for resonance lock...")
    
    results = []

    # Sweep through Turn Counts
    for t in np.arange(SCAN_RANGE[0], SCAN_RANGE[1], 0.1):
        # 1. ANCHORING: Calculate Phase Offset required to zero-out Galactic Center
        # If GC is perfect, what is the offset?
        offset = 0
        if gc_idx != -1:
            l_gc, b_gc = coords[gc_idx]
            # Calculate what the phase WOULD be without offset
            phi_gc = np.deg2rad(l_gc)
            theta_gc = np.deg2rad(90 - b_gc)
            z_gc = np.cos(theta_gc)
            h_gc = (z_gc + 1) / 2.0
            raw_ideal = (h_gc * t * 2 * np.pi * W_RESONANCE) % (2 * np.pi)
            # Offset needed to make Ideal == Actual
            offset = phi_gc - raw_ideal

        # 2. SCORING: Sum the drift of all other stars using this T and Offset
        total_drift = 0
        for i, (l, b) in enumerate(coords):
            _, drift = calculate_drift(l, b, t, W_RESONANCE, offset)
            total_drift += drift  # Lower is better
            
        if total_drift < best_score:
            best_score = total_drift
            best_turns = t
            best_offset = offset
            
    print(f"✅ LOCK ACQUIRED: Best Turns={best_turns:.2f}, Offset={best_offset:.2f} rad")
    return best_turns, best_offset

# ======================
# MAIN
# ======================
def main():
    names, coords = get_galactic_coords(STARS_DATA)
    
    # Optimize
    best_t, best_off = optimize_helix(names, coords)
    
    # Plotting the "Locked" Solution
    plt.figure(figsize=(10, 6), facecolor='#111111')
    ax = plt.gca()
    ax.set_facecolor('#111111')
    
    for i, (l, b) in enumerate(coords):
        h, drift = calculate_drift(l, b, best_t, W_RESONANCE, best_off)
        
        # Color Logic: Red = Drift, Green = Locked
        color_score = 1 - (drift / np.pi) # 1 is perfect, 0 is bad
        c = plt.cm.RdYlGn(color_score**2) # Squaring emphasizes the "Lock"
        
        plt.scatter(h, drift, color=c, s=150, edgecolors='white')
        plt.text(h+0.01, drift, names[i], color='white', fontsize=9)
        
    plt.axhline(0, color='#00ff00', linestyle='--', alpha=0.5, label='Resonance Line')
    plt.title(f"Optimized Helical Targeting (Galactic Frame)\nBest Turns: {best_t:.2f} | Anchor: Galactic Center", color='white')
    plt.xlabel("Helical Height (0=S.Gal.Pole, 1=N.Gal.Pole)", color='gray')
    plt.ylabel("Phase Drift (Error)", color='gray')
    
    ax.tick_params(colors='gray')
    plt.grid(True, color='#333333', linestyle='--')
    plt.legend()
    
    plt.savefig("helical_optimized_target.png")
    plt.show()

if __name__ == "__main__":
    main()