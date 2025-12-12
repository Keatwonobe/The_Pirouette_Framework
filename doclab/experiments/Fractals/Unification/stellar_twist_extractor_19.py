import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
# The Suspected Object (Cold Spot Core)
TARGET_L = -155.9 
TARGET_B = -63.9
FOV_DEG = 60.0 # Wide Field of View to catch surrounding stars

# Augmented Kinematics (Adding Southern Neighbors)
# Data: [RA, Dec, Dist, pmRA, pmDec, RV]
STARS_KINEMATICS = {
    # The Usual Suspects
    "Sirius":        (101.28, -16.71, 2.64,  -546.0,  -1223.1, -5.5),
    "Rigel":         (78.63,  -8.20,  260.0, 1.31,    0.50,    17.8),
    "Alpha Centauri":(219.90, -60.83, 1.33,  -3679.3, 473.7,  -21.4),
    "Procyon":       (114.82,  5.22,  3.5,   -716.6,  -1034.6, -3.2),
    "Canopus":       (95.99,  -52.70, 94.0,  19.9,    23.2,    20.5), # New
    "Achernar":      (24.43,  -57.24, 42.7,  88.0,    -40.0,   16.0), # New (Very close!)
    "Fomalhaut":     (344.41, -29.62, 7.7,   329.2,   -164.2,  6.5),  # New
    "Peacock":       (306.41, -56.74, 56.0,  18.2,    -105.4,  2.0),  # New
    "Beta Ceti":     (12.27,  -17.99, 29.5,  232.0,   32.0,    13.0), # New (Diphda)
    "Ankaa":         (6.57,   -42.31, 23.8,  237.0,   -178.0,  -11.0) # New
}

SOLAR_U, SOLAR_V, SOLAR_W = 11.1, 12.24, 7.25

def get_tangent_plane_vectors(name, data):
    # 1. Load Star
    ra, dec, dist, pm_ra, pm_dec, rv = data
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=dist*u.pc,
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, pm_dec=pm_dec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s, frame='icrs')
    
    # 2. Convert to Galactic
    g = c.galactic
    l = g.l.deg
    b = g.b.deg
    
    # Fix Longitude wrap for plotting
    if l > 180: l -= 360
    
    # Check if in Field of View
    # Simple distance check in deg
    dist_deg = np.sqrt((l - TARGET_L)**2 + (b - TARGET_B)**2)
    if dist_deg > FOV_DEG/2 + 10: # Slight buffer
        return None
    
    # 3. Calculate 3D Velocity (LSR Corrected)
    v_xyz = g.velocity.d_xyz.value
    u_lsr = v_xyz[0] + SOLAR_U
    v_lsr = v_xyz[1] + SOLAR_V
    w_lsr = v_xyz[2] + SOLAR_W
    
    # 4. Project onto Tangent Plane (Relative to Cold Spot)
    # Relative Position
    rel_l = l - TARGET_L
    rel_b = b - TARGET_B
    
    # Phantom Vector (Deviation from Quiet Flow)
    # "Quiet" = V~-10 (Rotation), U~0 (Radial), W~0 (Vertical)
    du = u_lsr - 0
    dv = v_lsr - (-10)
    dw = w_lsr - 0
    
    # Vector Projection:
    # X-axis on plot = Longitude flow (driven by Rotation dv)
    # Y-axis on plot = Latitude flow (driven by Vertical dw)
    vec_x = dv
    vec_y = dw
    
    return rel_l, rel_b, vec_x, vec_y, dist, name

def main():
    print(f"[*] Tracking Stellar Prey around the Maw (l={TARGET_L}, b={TARGET_B})...")
    
    stars_x, stars_y = [], []
    vecs_x, vecs_y = [], []
    names, dists = [], []
    
    for name, data in STARS_KINEMATICS.items():
        res = get_tangent_plane_vectors(name, data)
        if res:
            x, y, vx, vy, d, n = res
            stars_x.append(x)
            stars_y.append(y)
            vecs_x.append(vx)
            vecs_y.append(vy)
            dists.append(d)
            names.append(n)
            
    # VISUALIZATION
    fig = plt.figure(figsize=(10, 10), facecolor='#050505')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#050505')
    
    # 1. Plot the "Maw" (Target Center)
    circle1 = plt.Circle((0, 0), 2, color='lime', alpha=0.2)
    circle2 = plt.Circle((0, 0), 5, color='lime', fill=False, linestyle='--')
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.text(0, 0, " INVISIBLE OBJECT\n(Cold Spot Core)", color='lime', ha='center', va='center', fontweight='bold')
    
    # 2. Plot the Stars (Prey)
    # Color by Distance (pc) - Brighter = Closer
    sc = ax.scatter(stars_x, stars_y, c=dists, cmap='cool', s=100, zorder=10)
    
    # 3. Plot the Flow Vectors
    # Invert X if looking "out"? No, standard map view.
    # L decreases to the right usually, but let's stick to Cartesian x=l
    ax.quiver(stars_x, stars_y, vecs_x, vecs_y, color='white', scale=100, width=0.005)
    
    # Labels
    for i, txt in enumerate(names):
        ax.text(stars_x[i]+1, stars_y[i]+1, txt, color='cyan', fontsize=9)
        
    ax.set_title("Gun-Barrel View: Stellar Motion relative to the Cold Spot", color='white', fontsize=14)
    ax.set_xlabel("Relative Longitude (deg)", color='gray')
    ax.set_ylabel("Relative Latitude (deg)", color='gray')
    ax.grid(True, color='#222222', linestyle=':')
    
    # Center lines
    ax.axhline(0, color='gray', alpha=0.3)
    ax.axvline(0, color='gray', alpha=0.3)
    
    # Set Limits
    ax.set_xlim(FOV_DEG/2, -FOV_DEG/2) # Astronomers prefer East (Left) positive
    ax.set_ylim(-FOV_DEG/2, FOV_DEG/2)
    
    plt.savefig("stellar_maw_tracker.png")
    print("✅ Tracker Map Saved: stellar_maw_tracker.png")
    
    # Calculate Flow Pattern
    # Simple heuristic: Do vectors point IN or OUT?
    radial_flow = 0
    tangential_flow = 0
    count = 0
    
    for i in range(len(stars_x)):
        # Radius vector
        rx, ry = stars_x[i], stars_y[i]
        r_mag = np.sqrt(rx**2 + ry**2)
        rx/=r_mag; ry/=r_mag
        
        # Velocity vector
        vx, vy = vecs_x[i], vecs_y[i]
        
        # Dot product (Radial)
        radial_flow += (vx*rx + vy*ry)
        
        # Cross product (Tangential/Swirl)
        tangential_flow += (vx*ry - vy*rx)
        count += 1
        
    avg_rad = radial_flow / count
    avg_tan = tangential_flow / count
    
    print("\n" + "="*50)
    print("KINEMATIC DIAGNOSIS:")
    print(f"Radial Flow:     {avg_rad:.2f} (Positive=Explosion, Negative=Implosion)")
    print(f"Tangential Flow: {avg_tan:.2f} (Positive=CCW Swirl, Negative=CW Swirl)")
    
    if avg_rad < -5:
        print("⚡ DETECTED: Convergent Flow (Implosion/Sink). Stars are falling in.")
    elif abs(avg_tan) > 5:
        print("⚡ DETECTED: Vortex Flow. Stars are swirling around the axis.")
    elif avg_rad > 5:
        print("RESULT: Divergent Flow (Wake). Stars are moving away/around.")
    else:
        print("RESULT: No coherent pattern detected yet.")

if __name__ == "__main__":
    main()