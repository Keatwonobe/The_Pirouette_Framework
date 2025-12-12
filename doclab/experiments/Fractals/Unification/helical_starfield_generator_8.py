import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord, LSR
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
W_RESONANCE = 1.0047
LOCKED_TURNS = 30.00
ANCHOR_STAR = "Galactic Center"

# Data from previous step (Name, RA, Dec, Dist, pmRA, pmDec, RV)
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
    "Deneb":         (310.35, 45.28, 802.0, 1.56, 1.55, -4.5)
}

# Solar Motion for LSR correction (U,V,W) in km/s
SOLAR_U = 11.1
SOLAR_V = 12.24
SOLAR_W = 7.25

def get_kinematics(name, data):
    ra, dec, dist, pm_ra, pm_dec, rv = data
    
    # 1. Create SkyCoord
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=dist*u.pc,
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, pm_dec=pm_dec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s, frame='icrs')
    
    # 2. Get Galactic Coordinates (l, b)
    g = c.galactic
    l_deg = g.l.deg
    b_deg = g.b.deg
    
    # 3. Get Velocity Vector (U, V, W)
    # Transform to Galactic frame to get Cartesian velocities
    # U = Towards Center, V = Rotation, W = North
    # Note: Astropy d_xyz in Galactic frame aligns with:
    # x -> Center (l=0), y -> Rotation (l=90), z -> North (b=90)
    v_xyz = g.velocity.d_xyz.value
    
    # Correct for Solar Motion to get LSR
    # U_lsr = U_star + U_sun
    u_vel = v_xyz[0] + SOLAR_U
    v_vel = v_xyz[1] + SOLAR_V
    w_vel = v_xyz[2] + SOLAR_W
    
    # Invert V so Positive = Prograde (Moving with rotation), Negative = Retrograde (Lag)
    # Wait, previous script used "Retrograde Drift" where Positive = Lag.
    # Let's stick to standard Physics for arrows:
    # V_lsr > 0 means moving faster than LSR?
    # Standard: V is positive towards l=90.
    # If Star V=230, LSR V=220. Star is +10 relative.
    # If Star V=210, LSR V=220. Star is -10 relative.
    # So "Lag" is negative V_lsr in this code.
    
    return l_deg, b_deg, u_vel, v_vel, w_vel

def calculate_helical_pos(l, b, turns, w, offset):
    phi = np.deg2rad(l)
    theta = np.deg2rad(90 - b)
    z = np.cos(theta)
    h_idx = (z + 1) / 2.0
    
    ideal_phi = (h_idx * turns * 2 * np.pi * w) % (2 * np.pi)
    phase = (phi - ideal_phi - offset) % (2 * np.pi)
    return h_idx, np.degrees(phase)

def main():
    # 1. Get Anchor Offset
    gc_data = STARS_KINEMATICS["Galactic Center"]
    _, _, _, _, _ = get_kinematics("GC", gc_data) # Just to warm up
    # We know GC is at 0,0 roughly, but let's calc offset
    l_gc, b_gc, _, _, _ = get_kinematics("Galactic Center", gc_data)
    
    # Calc raw phase of GC
    phi_gc = np.deg2rad(l_gc)
    theta_gc = np.deg2rad(90 - b_gc)
    z_gc = np.cos(theta_gc)
    h_gc = (z_gc + 1) / 2.0
    raw_ideal_gc = (h_gc * LOCKED_TURNS * 2 * np.pi * W_RESONANCE) % (2 * np.pi)
    # We want GC to be at Phase 0 (or 360)
    # So Phase = (phi - ideal - offset) = 0  => offset = phi - ideal
    OFFSET = (phi_gc - raw_ideal_gc)

    # 2. Process all stars
    print(f"[*] Generating Helical Flow Map...")
    
    plt.figure(figsize=(14, 8), facecolor='#111111')
    ax = plt.gca()
    ax.set_facecolor('#111111')
    
    # Draw Canyons
    canyons = [0, 18, 180, 360]
    for c in canyons:
        plt.axvline(c, color='#222222', linestyle='-', linewidth=15, alpha=0.5)
        plt.axvline(c, color='lime' if c%180==0 else 'cyan', linestyle=':', alpha=0.6)

    for name, data in STARS_KINEMATICS.items():
        if name == "Galactic Center": continue
        
        l, b, u_vel, v_vel, w_vel = get_kinematics(name, data)
        h, phase = calculate_helical_pos(l, b, LOCKED_TURNS, W_RESONANCE, OFFSET)
        
        # Scaling vectors for visualization
        # X-arrow: V velocity (Rotation drift)
        # Y-arrow: W velocity (Vertical motion)
        scale = 0.005
        
        # V_vel is km/s.
        # If V_vel is negative (Lag/Retrograde in my previous calc), it points LEFT.
        # Wait, previous script: Result = -v_rotation_drift.
        # So Positive Result (Lag) came from Negative V_drift.
        # Here v_vel is raw LSR velocity.
        # If v_vel > 0 (Prograde/Fast) -> Arrow RIGHT.
        # If v_vel < 0 (Retrograde/Lag) -> Arrow LEFT.
        
        dx = v_vel * scale * 2 # Exaggerate horizontal drift
        dy = w_vel * scale
        
        # Color based on vertical W velocity
        # Red = Moving North (Up), Blue = Moving South (Down)
        c = 'salmon' if w_vel > 0 else 'dodgerblue'
        
        # Plot Star
        plt.scatter(phase, h, color=c, s=100, zorder=5, edgecolors='white')
        
        # Plot Arrow
        plt.arrow(phase, h, dx, dy, color=c, head_width=0.015, alpha=0.8, zorder=6)
        
        # Label
        plt.text(phase + 3, h + 0.01, f"{name}\nW:{w_vel:.1f}", color='white', fontsize=8, alpha=0.7)

    plt.title("Helical Flow Map: Velocity Vectors (V_drift, W_vertical)", color='white')
    plt.xlabel("Helical Phase (Canyons at 0°, 18°, 180°)", color='gray')
    plt.ylabel("Helical Height (z)", color='gray')
    plt.xlim(-20, 380)
    plt.ylim(-0.1, 1.1)
    
    # Legend
    plt.arrow(330, 0.1, 20, 0, color='white', head_width=0.02)
    plt.text(330, 0.06, "Moving Fast (Prograde)", color='gray', fontsize=8)
    plt.arrow(330, 0.15, -20, 0, color='white', head_width=0.02)
    plt.text(330, 0.18, "Dragging (Retrograde)", color='gray', fontsize=8)
    
    plt.grid(True, color='#222222', linestyle=':')
    ax.tick_params(colors='gray')
    
    plt.savefig("helical_flow_map.png")
    print("✅ Flow Map Saved: helical_flow_map.png")

if __name__ == "__main__":
    main()