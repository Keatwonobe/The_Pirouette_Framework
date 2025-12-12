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

# Full Kinematic Data (RA, Dec, Dist, pmRA, pmDec, RV)
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

SOLAR_U = 11.1
SOLAR_V = 12.24
SOLAR_W = 7.25

def get_vectors(name, data):
    ra, dec, dist, pm_ra, pm_dec, rv = data
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=dist*u.pc,
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, pm_dec=pm_dec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s, frame='icrs')
    g = c.galactic
    l, b = g.l.deg, g.b.deg
    
    # 1. Actual Velocity (LSR Corrected)
    v_xyz = g.velocity.d_xyz.value
    u_act = v_xyz[0] + SOLAR_U
    v_act = v_xyz[1] + SOLAR_V
    w_act = v_xyz[2] + SOLAR_W
    
    # 2. Ideal Helical Velocity
    # A star in the "Canyon" has:
    # U (Radial) = 0 (Stable orbit)
    # V (Rotation) = -10 (The "Stream Speed" of Sirius/Rigel relative to LSR)
    # W (Vertical) = 0 (Stays on plane)
    u_ideal = 0
    v_ideal = -10
    w_ideal = 0
    
    # 3. The Phantom Vector (Difference)
    # This vector points to the "Disturber"
    du = u_act - u_ideal
    dv = v_act - v_ideal
    dw = w_act - w_ideal
    
    return l, b, du, dv, dw

def main():
    print(f"[*] Hunting for Dark Mass (Maws)...")
    
    plt.figure(figsize=(15, 8), facecolor='#050505')
    ax = plt.subplot(111, projection="aitoff")
    ax.set_facecolor('#050505')
    plt.grid(True, color='#222222', linestyle=':')
    
    for name, data in STARS_KINEMATICS.items():
        if name == "Galactic Center": continue
        
        l, b, du, dv, dw = get_vectors(name, data)
        
        # Convert l, b to Radians for Aitoff
        l_rad = np.deg2rad(l - 180) # Shift for Aitoff
        b_rad = np.deg2rad(b)
        
        # Project the 3D Phantom Vector onto the Sky Plane
        # We simplify by projecting dU (radial) and dV (tangential) onto l-axis
        # and dW (vertical) onto b-axis.
        # This is an approximation for visualization.
        
        # Magnitude of the Phantom Force
        mag = np.sqrt(du**2 + dv**2 + dw**2)
        
        # Vector Direction on Map
        # dL (Longitude push) ~ dV (Rotation) + dU (Radial) mixed
        # dB (Latitude push) ~ dW (Vertical)
        
        # Scaling for visibility
        scale = 0.005
        
        # Color based on "Thump" intensity (Magnitude)
        # Red = High Disturbance (Near a Maw?), Blue = Low
        c = plt.cm.magma(min(mag/100, 1.0))
        
        plt.scatter(l_rad, b_rad, color=c, s=50, zorder=10)
        
        # Draw the Phantom Vector
        # We use dV for horizontal shift (rotation lag) and dW for vertical shift
        # A star being pulled "Back" (Lag) has vector pointing left.
        # A star being pulled "Up" has vector pointing up.
        
        dx = dv * scale 
        dy = dw * scale
        
        # Invert dx for Aitoff view (l increases left)
        plt.arrow(l_rad, b_rad, -dx, dy, color=c, alpha=0.8, head_width=0.02, lw=1)
        
        # Label Outliers
        if mag > 30:
            plt.text(l_rad, b_rad + 0.05, f"{name}\nForce:{mag:.0f}", color='white', fontsize=8, ha='center')

    plt.title("The Dark Mass Hunter: Phantom Force Vectors\n(Arrows point to the source of disturbance)", color='white', y=1.05)
    plt.xlabel("Galactic Longitude (l)", color='gray')
    plt.ylabel("Galactic Latitude (b)", color='gray')
    
    # Add "Maw" Hypothesis Zones
    # If vectors converge, circle it!
    
    plt.savefig("helical_dark_mass_hunter.png")
    print("✅ Scan Complete. Saved to helical_dark_mass_hunter.png")

if __name__ == "__main__":
    main()