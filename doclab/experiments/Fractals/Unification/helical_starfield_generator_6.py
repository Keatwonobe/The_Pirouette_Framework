import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.signal import find_peaks

# ======================
# CONFIGURATION
# ======================
W_RESONANCE = 1.0047
LOCKED_TURNS = 30.00
ANCHOR_STAR = "Galactic Center"
CANYON_SENSITIVITY = 30  # Number of bins for detecting grooves (360/30 = 12 deg width)

# Full Star List
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
    names, l_list, b_list = [], [], []
    for name, ra, dec in STARS_DATA:
        c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
        g = c.galactic
        names.append(name)
        l_list.append(g.l.degree)
        b_list.append(g.b.degree)
    return names, np.array(l_list), np.array(b_list)

def calculate_phase(l, b, turns, w, offset=0):
    phi = np.deg2rad(l)
    theta = np.deg2rad(90 - b)
    z = np.cos(theta)
    h_idx = (z + 1) / 2.0
    
    ideal_phi = (h_idx * turns * 2 * np.pi * w) % (2 * np.pi)
    phase = (phi - ideal_phi - offset) % (2 * np.pi)
    return h_idx, phase

def main():
    names, l, b = get_data()
    
    # 1. Determine Anchor Offset
    try:
        gc_idx = names.index(ANCHOR_STAR)
        _, raw_gc = calculate_phase(l[gc_idx], b[gc_idx], LOCKED_TURNS, W_RESONANCE, 0)
        SYSTEM_OFFSET = raw_gc
    except ValueError:
        SYSTEM_OFFSET = 0

    # 2. Calculate Phases
    heights = []
    phases = []
    phases_deg = []
    
    for i in range(len(names)):
        h, p = calculate_phase(l[i], b[i], LOCKED_TURNS, W_RESONANCE, SYSTEM_OFFSET)
        heights.append(h)
        phases.append(p)
        phases_deg.append(np.degrees(p))

    # ======================
    # CANYON DETECTION ALGORITHM
    # ======================
    # Create a histogram of phase angles to find "High Density" zones
    hist_y, hist_x = np.histogram(phases_deg, bins=CANYON_SENSITIVITY, range=(0, 360))
    
    # Identify "Canyon Centers" (Peaks in the histogram)
    peaks, _ = find_peaks(hist_y, height=2) # Must have at least 2 stars to be a "Canyon"
    
    canyon_centers = [(hist_x[p] + hist_x[p+1])/2 for p in peaks]
    print(f"[*] Detected {len(canyon_centers)} Canyons at degrees: {[int(c) for c in canyon_centers]}")

    # ======================
    # VISUALIZATION: The Unrolled Canyon Map
    # ======================
    plt.figure(figsize=(14, 8), facecolor='#111111')
    ax = plt.gca()
    ax.set_facecolor('#111111')
    
    # Plot the Detected Canyons (Vertical Bands)
    for center in canyon_centers:
        plt.axvspan(center - 6, center + 6, color='#222222', alpha=0.8) # 12-degree wide canyons
        plt.axvline(center, color='#333333', linestyle='--')
        plt.text(center, 1.02, f"{int(center)}°", color='gray', ha='center', fontsize=8)

    # Highlighting Specific Known Grooves
    # Major Groove (0 deg)
    plt.axvline(0, color='lime', linewidth=1, alpha=0.5)
    plt.axvline(360, color='lime', linewidth=1, alpha=0.5)
    
    # Plot Stars
    for i in range(len(names)):
        deg = phases_deg[i]
        h = heights[i]
        
        # Color Logic
        if deg > 355 or deg < 5: 
            c = 'lime'      # Major Groove
        elif 15 < deg < 25:
            c = 'cyan'      # The 18-degree "Speared" Cluster
        elif 175 < deg < 185:
            c = 'magenta'   # Shadow Groove (180)
        else:
            c = 'orange'    # Outliers
            
        plt.scatter(deg, h, color=c, s=100, edgecolors='white', zorder=10)
        plt.text(deg + 2, h, names[i], color='white', fontsize=9, alpha=0.8)

    plt.title(f"The Helical Canyon Map\n(Unrolled 30-Turn Cylinder | W={W_RESONANCE})", color='white')
    plt.xlabel("Helical Phase Angle (0° to 360°)", color='gray')
    plt.ylabel("Helical Height (0=South, 1=North)", color='gray')
    
    plt.xlim(-10, 370)
    plt.ylim(-0.05, 1.05)
    
    ax.tick_params(colors='gray')
    plt.grid(True, color='#222222', linestyle=':')
    
    # Save
    plt.savefig("helical_canyon_map.png")
    print("✅ Canyon Map Saved: helical_canyon_map.png")

if __name__ == "__main__":
    main()