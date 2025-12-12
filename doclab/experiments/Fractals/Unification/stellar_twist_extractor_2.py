import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.signal import find_peaks
from astropy.coordinates import SkyCoord
import astropy.units as u
import json

# ======================
# CONFIGURATION
# ======================
# Known kinematic anomalies (Twist Anchors)
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

# ======================
# ASTROPY KINEMATICS
# ======================
def get_galactic_kinematics(name, data):
    """
    Uses Astropy to get precise Galactic coordinates and velocities.
    """
    ra, dec, dist, pm_ra, pm_dec, rv = data
    
    # Create coordinate object
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=dist*u.pc,
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, pm_dec=pm_dec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s, frame='icrs')
    
    c_gal = c.galactic
    l = c_gal.l.deg
    b = c_gal.b.deg
    
    # Get Galactic Cartesian velocities (U, V, W)
    # astropy returns U towards center, V rotation, W North Pole
    # We use the standard definition relative to LSR later
    v_xyz = c_gal.velocity.d_xyz.value
    u_helio, v_helio, w_helio = v_xyz[0], v_xyz[1], v_xyz[2]
    
    # LSR Correction
    u_act = u_helio + SOLAR_U
    v_act = v_helio + SOLAR_V
    w_act = w_helio + SOLAR_W
    
    # Ideal "Quiet Hull" Motion (The background we subtract to find the Twist)
    # V ~ -220 is galactic rotation, but local stars vary.
    # We look for "Phantom Force" deviations: u=0, v=0 relative to local flow, w=0
    
    # Twist Deviation = Total Velocity perpendicular to plane + Radial expansion
    # We treat tangential rotation (V) as 'normal' and look for U/W anomalies
    du = u_act 
    dv = 0 # Ignore rotation speed diffs for now, focus on "Twist" (radial/vertical)
    dw = w_act 
    
    return l, b, u_act, v_act, w_act, du, dv, dw

# ======================
# ROBUST PATTERN EXTRACTION
# ======================
def extract_robust_signature(positions, deviations, center_lon, center_lat, radius=90):
    """
    Determines the dominant geometric angles of the twist.
    """
    lons = np.array([p[0] for p in positions])
    lats = np.array([p[1] for p in positions])
    dus = np.array([d[0] for d in deviations]) # Using U (radial)
    dws = np.array([d[1] for d in deviations]) # Using W (vertical)
    
    # Normalize longitude wrap
    dlons = lons - center_lon
    dlons = np.where(dlons > 180, dlons - 360, dlons)
    dlons = np.where(dlons < -180, dlons + 360, dlons)
    dlats = lats - center_lat
    
    distances = np.sqrt(dlons**2 + dlats**2)
    mask = distances < radius
    
    if np.sum(mask) < 3: return None
    
    local_lons = dlons[mask]
    local_lats = dlats[mask]
    local_dus = dus[mask]
    local_dws = dws[mask]
    
    # Magnitude of the "Phantom Force"
    twist_mag = np.sqrt(local_dus**2 + local_dws**2)
    
    # Position Angle on the Sky (The "Spoke" direction)
    spoke_angles = np.degrees(np.arctan2(local_lats, local_lons)) % 360
    
    # We sort by magnitude to find the "Strongest Anchors"
    # The twist is defined by where the force is strongest
    sorted_indices = np.argsort(twist_mag)[::-1] # Descending
    
    # Take top 5 strongest twist stars
    top_indices = sorted_indices[:5]
    top_angles = spoke_angles[top_indices]
    top_angles.sort()
    
    # Calculate Relative Angles (The Key)
    # e.g. difference between Star A and Star B
    rel_angles = np.diff(top_angles)
    wrap_angle = (360 - top_angles[-1] + top_angles[0])
    rel_angles = np.append(rel_angles, wrap_angle)
    
    return {
        'anchor_angles': top_angles,
        'relative_angles': rel_angles,
        'strength': np.mean(twist_mag[top_indices])
    }

# ======================
# MAIN EXECUTION
# ======================
def main():
    print("="*60)
    print("STELLAR TWIST EXTRACTOR: GEOMETRIC KEY GEN")
    print("="*60)
    
    positions = []
    deviations = []
    
    print("[1] Processing Kinematics...")
    for name, data in STARS_KINEMATICS.items():
        if name == "Galactic Center": continue
        l, b, u_act, v_act, w_act, du, dv, dw = get_galactic_kinematics(name, data)
        positions.append((l, b))
        # We use U (Radial) and W (Vertical) as the "Twist" components
        deviations.append((du, dw)) 
        print(f"  {name:15} | l={l:5.1f} b={b:5.1f} | Twist Force: {np.sqrt(du**2 + dw**2):5.1f} km/s")

    print("\n[2] Generating Geometric Key from Galactic Center...")
    # We look at the pattern of stars *around* the GC
    gc_key = extract_robust_signature(positions, deviations, 266.41, -29.00)
    
    if gc_key:
        print("\n  >>> GALACTIC CENTER KEY FOUND <<<")
        print(f"  Anchor Angles (Absolute): {np.round(gc_key['anchor_angles'], 1)}")
        print(f"  Relative Intervals (THE PATTERN): {np.round(gc_key['relative_angles'], 1)}")
        print(f"  Twist Strength: {gc_key['strength']:.1f}")
        
        # Visualize
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='polar')
        
        # Plot Anchors
        theta = np.deg2rad(gc_key['anchor_angles'])
        radii = np.ones_like(theta) * gc_key['strength']
        
        ax.scatter(theta, radii, c='red', s=100, label='Twist Anchors', zorder=10)
        
        # Draw Spokes
        for t in theta:
            ax.plot([0, t], [0, gc_key['strength']], 'r--', alpha=0.5)
            
        ax.set_title("The Stellar Key: Geometric Structure of the Twist", pad=20)
        plt.savefig("stellar_geometric_key.png")
        print("  Saved visualization: stellar_geometric_key.png")
        
        # EXPORT KEY
        with open("twist_key.json", "w") as f:
            json.dump({
                "type": "stellar_twist_key",
                "relative_angles": gc_key['relative_angles'].tolist(),
                "tolerance": 15.0 # Degrees +/- matching tolerance
            }, f, indent=2)
        print("  Saved Key: twist_key.json")
        
    else:
        print("Failed to generate key.")

if __name__ == "__main__":
    main()