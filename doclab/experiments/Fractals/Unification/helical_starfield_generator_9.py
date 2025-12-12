import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
W_RESONANCE = 1.0047
LOCKED_TURNS = 30.00
ANCHOR_STAR = "Galactic Center"

# Full Kinematic Dataset
STARS_KINEMATICS = {
    "Sirius":        (101.28, -16.71, 2.64,  -546.0,  -1223.1, -5.5),
    "Betelgeuse":    (88.79,   7.40,  168.0, 26.4,    9.6,     21.9),
    "Aldebaran":     (68.98,   16.50, 20.4,  63.5,   -188.9,   54.3),
    "Vega":          (279.23,  38.78, 7.68,  200.9,   286.2,  -13.9),
    "Rigel":         (78.63,  -8.20,  260.0, 1.31,    0.50,    17.8),
    "Alpha Centauri":(219.90, -60.83, 1.33,  -3679.3, 473.7,  -21.4),
    "Antares":       (247.35, -26.43, 170.0, -12.1,  -23.3,   -3.4),
    "Arcturus":      (213.91,  19.18, 11.26, -1093.4, -1999.4, -5.2),
    "Procyon":       (114.82,  5.22,  3.5,   -716.6,  -1034.6, -3.2),
    "Galactic Center":(266.41, -29.00, 8178, 0, 0, 0),
    "Capella":       (79.17, 45.99, 12.9, 75.5, -427.1, 30.2),
    "Pollux":        (116.32, 28.02, 10.3, -626.5, -45.8, 3.2),
    "Deneb":         (310.35, 45.28, 802.0, 1.56, 1.55, -4.5),
    "Regulus":       (152.09, 11.96, 23.8, -248.5, 6.0, 5.9),
    "Castor":        (113.65, 31.88, 15.6, -192.4, -146.7, 14.4),
    "Spica":         (201.29, -11.16, 77.0, -42.5, -31.7, 1.0)
}

# Solar Motion for LSR correction (U,V,W) in km/s
SOLAR_U = 11.1
SOLAR_V = 12.24
SOLAR_W = 7.25

def get_radial_velocity_u(name, data):
    ra, dec, dist, pm_ra, pm_dec, rv = data
    
    # Create SkyCoord
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=dist*u.pc,
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, pm_dec=pm_dec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s, frame='icrs')
    
    # Transform to Galactic to get U, V, W
    g = c.galactic
    v_xyz = g.velocity.d_xyz.value
    
    # U is the velocity towards the Galactic Center.
    # In the Cartesian frame (x,y,z):
    # x is towards Center (l=0)
    # y is towards Rotation (l=90)
    # z is towards North (b=90)
    
    # Correct for Solar Motion relative to LSR
    u_lsr = v_xyz[0] + SOLAR_U
    
    # Interpretation:
    # Positive U (+): Moving TOWARD Galactic Center (Falling In)
    # Negative U (-): Moving AWAY from Galactic Center (Moving Out)
    # Note: Astropy convention for d_x is usually towards the center from the sun.
    # Let's verify standard U definition: U is often defined positive towards center.
    
    return g.l.deg, g.b.deg, u_lsr

def calculate_helical_height(b):
    theta = np.deg2rad(90 - b)
    z = np.cos(theta)
    h_idx = (z + 1) / 2.0
    return h_idx

def main():
    print(f"[*] Analyzing Radial Dynamics (U-Velocity)...")
    
    plt.figure(figsize=(12, 8), facecolor='#111111')
    ax = plt.gca()
    ax.set_facecolor('#111111')
    
    # Plot "Stable Orbit" Zone
    plt.axhspan(-10, 10, color='lime', alpha=0.1, label='Stable Radial Orbit')
    plt.axhline(0, color='lime', linestyle='--', alpha=0.5)

    u_velocities = []
    heights = []
    names = []
    colors = []
    
    for name, data in STARS_KINEMATICS.items():
        if name == "Galactic Center": continue
        
        l, b, u_vel = get_radial_velocity_u(name, data)
        h = calculate_helical_height(b)
        
        u_velocities.append(u_vel)
        heights.append(h)
        names.append(name)
        
        # Color Logic
        if abs(u_vel) < 10:
            c = 'lime' # Stable
        elif u_vel > 10:
            c = 'cyan' # Falling In (Compression)
        else:
            c = 'salmon' # Moving Out (Expansion)
            
        colors.append(c)
        
        # Plot Star
        plt.scatter(h, u_vel, color=c, s=150, edgecolors='white', zorder=10)
        plt.text(h + 0.01, u_vel, name, color='white', fontsize=9, alpha=0.9)

    plt.title("Helical Radial Dynamics: The 'Breath' of the Manifold", color='white')
    plt.xlabel("Helical Height (z) [0=South, 1=North]", color='gray')
    plt.ylabel("Radial Velocity U (km/s)\n[+ Falling In | - Moving Out]", color='gray')
    
    # Annotations for "Spring" Physics
    plt.text(0.1, 40, "COMPRESSION ZONE\n(Falling In)", color='cyan', alpha=0.5, fontsize=10, fontweight='bold')
    plt.text(0.1, -40, "EXPANSION ZONE\n(Moving Out)", color='salmon', alpha=0.5, fontsize=10, fontweight='bold')
    
    plt.grid(True, color='#222222', linestyle=':')
    ax.tick_params(colors='gray')
    plt.legend(loc='upper right')
    
    plt.savefig("helical_radial_dynamics.png")
    print("✅ Radial Map Saved: helical_radial_dynamics.png")

if __name__ == "__main__":
    main()