import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord, Galactocentric, LSR
import astropy.units as u
import astropy.coordinates as coord

# ======================
# CONFIGURATION
# ======================
W_RESONANCE = 1.0047
LOCKED_TURNS = 30.00
ANCHOR_STAR = "Galactic Center"

# ======================
# PRECISE KINEMATIC DATA (J2000)
# Sources: Hipparcos, SIMBAD, Gaia DR2/3 (as found in search)
# Format: (RA_deg, Dec_deg, Dist_pc, pm_ra_mas_yr, pm_dec_mas_yr, rv_km_s)
# ======================
STARS_KINEMATICS = {
    "Sirius":        (101.28, -16.71, 2.64,  -546.0,  -1223.1, -5.5),
    "Betelgeuse":    (88.79,   7.40,  168.0, 26.4,    9.6,     21.9),
    "Aldebaran":     (68.98,   16.50, 20.4,  63.5,   -188.9,   54.3),
    "Vega":          (279.23,  38.78, 7.68,  200.9,   286.2,  -13.9),
    "Rigel":         (78.63,  -8.20,  260.0, 1.31,    0.50,    17.8),
    "Alpha Centauri":(219.90, -60.83, 1.33,  -3679.3, 473.7,  -21.4),
    "Antares":       (247.35, -26.43, 170.0, -12.1,  -23.3,   -3.4),
    "Arcturus":      (213.91,  19.18, 11.26, -1093.4, -1999.4, -5.2), # High proper motion check
    "Procyon":       (114.82,  5.22,  3.5,   -716.6,  -1034.6, -3.2),
    "Galactic Center":(266.41, -29.00, 8178, 0, 0, 0) # Anchor
}

# Add standard sun motion relative to LSR for correction
# (U, V, W) = (11.1, 12.24, 7.25) km/s (Schonrich et al. 2010)
SOLAR_MOTION = [11.1, 12.24, 7.25] * u.km / u.s

def calculate_helical_phase(ra, dec, turns, w, offset=0):
    """
    Calculates the Helical Phase Angle for the plot X-axis.
    """
    # Convert to Galactic first
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')
    g = c.galactic
    
    phi = g.l.rad
    theta = np.deg2rad(90 - g.b.deg)
    z = np.cos(theta)
    h_idx = (z + 1) / 2.0
    
    ideal_phi = (h_idx * turns * 2 * np.pi * w) % (2 * np.pi)
    phase = (phi - ideal_phi - offset) % (2 * np.pi)
    
    return np.degrees(phase)

def calculate_retrograde_velocity(name, data):
    """
    Calculates the V component (tangential to Galactic rotation) 
    relative to the Local Standard of Rest (LSR).
    Negative V = Lagging the rotation (Retrograde Drift).
    """
    ra, dec, dist, pm_ra, pm_dec, rv = data
    
    # Create SkyCoord with full kinematic data
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, 
                 distance=dist*u.pc, 
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, 
                 pm_dec=pm_dec*u.mas/u.yr, 
                 radial_velocity=rv*u.km/u.s, 
                 frame='icrs')
    
    # Transform to Galactic Frame
    g = c.galactic
    
    # Approximating UVW (U=Toward Center, V=Rotation Direction, W=North Pole)
    # This requires converting the proper motion vectors aligned to Galactic frame
    # Astropy 4.0+ handles this via differential coordinates
    
    # We want velocity relative to LSR. 
    # V_LSR = V_star + V_Sun_LSR
    # Note: Astropy's LSR frame is useful here.
    
    lsr_coord = c.transform_to(LSR())
    
    # Get velocity components in Cartesian representation (x,y,z) of LSR
    # However, standard UVW is usually defined at the Sun's position.
    # U = velocity toward Galactic Center (approx -X in Galactic, but let's be careful)
    # V = velocity in direction of rotation (Y in Galactic)
    # W = velocity toward North Galactic Pole (Z in Galactic)
    
    # Let's use simple Galactic uvw method if available or construct from cartesian
    v_cart = lsr_coord.velocity.d_xyz
    
    # In Galactic frame:
    # X points to Center (l=0), Y points to Rotation (l=90), Z points to North (b=90)
    # So U = v_x, V = v_y, W = v_z
    # But we need to account for the star's POSITION angle if it's far away?
    # For local stars (<1kpc), U,V,W are roughly aligned with X,Y,Z.
    
    # Actually, let's use the standard U, V, W definition:
    # U: Velocity towards Galactic Center
    # V: Velocity in direction of Galactic Rotation
    # W: Velocity towards North Galactic Pole
    
    # Calculate Galactic Proper Motions
    # We transform the *frame* of the coordinate including differentials
    c_gal = c.transform_to('galactic')
    
    # Extract velocities in Cartesian frame aligned with Galactic Center
    # v_x (towards center), v_y (rotation), v_z (north)
    v_xyz = c_gal.velocity.d_xyz
    
    # v_y is the component in direction of l=90 (Rotation)
    # This is the Heliocentric velocity. We need to add Solar Motion correction for LSR.
    # Solar V is 12.24 km/s (Sun moves faster than LSR).
    # So V_star_LSR = V_star_helio + V_sun
    
    v_rotation_drift = v_xyz[1].to(u.km/u.s).value + 12.24
    
    # RESULT:
    # Positive V = Moving FASTER than the average star (Super-Prograde)
    # Negative V = LAG (Retrograde Drift)
    # We want "Retrograde Potential", so let's invert it.
    # Retrograde Potential = -V_drift
    
    return -v_rotation_drift

def main():
    names = list(STARS_KINEMATICS.keys())
    
    # 1. Calculate Anchor Offset (GC Phase)
    gc_data = STARS_KINEMATICS["Galactic Center"] # (ra, dec, ...)
    # Galactic center has phase 0 by definition in our previous plot, but let's recalc
    raw_gc_phase = calculate_helical_phase(gc_data[0], gc_data[1], LOCKED_TURNS, W_RESONANCE)
    OFFSET = np.deg2rad(raw_gc_phase)
    
    phases = []
    retro_potentials = []
    colors = []
    sizes = []

    print(f"[*] Calculating Retrograde Drift for {len(names)} stars...")
    print(f"{'Star':<15} | {'Phase':<10} | {'Retro Drift (km/s)':<20}")
    print("-" * 50)
    
    for name in names:
        data = STARS_KINEMATICS[name]
        
        # Phase
        p_deg = calculate_helical_phase(data[0], data[1], LOCKED_TURNS, W_RESONANCE, OFFSET)
        phases.append(p_deg)
        
        # Retrograde Potential (Lag velocity)
        if name == "Galactic Center":
            r_pot = 0 # Reference
        else:
            r_pot = calculate_retrograde_velocity(name, data)
            
        retro_potentials.append(r_pot)
        
        print(f"{name:<15} | {p_deg:<10.1f} | {r_pot:<20.1f}")
        
        # Color Logic
        if name in ["Aldebaran", "Betelgeuse", "Arcturus"]:
            colors.append('red') # Suspected Outliers
            sizes.append(150)
        elif name in ["Rigel", "Sirius", "Alpha Centauri"]:
            colors.append('lime') # Channel Dwellers
            sizes.append(150)
        else:
            colors.append('white')
            sizes.append(100)

    # ======================
    # PLOT
    # ======================
    plt.figure(figsize=(12, 8), facecolor='#111111')
    ax = plt.gca()
    ax.set_facecolor('#111111')
    
    # Zero Line (LSR)
    plt.axhline(0, color='gray', linestyle='--', alpha=0.5, label='Local Standard of Rest (Co-Rotation)')
    
    # Scatter
    plt.scatter(phases, retro_potentials, c=colors, s=sizes, edgecolors='white', alpha=0.9, zorder=10)
    
    # Labels
    for i, txt in enumerate(names):
        plt.text(phases[i] + 5, retro_potentials[i], txt, color=colors[i], fontsize=10, fontweight='bold')
        
    # Vertical Canyons (from previous map)
    plt.axvline(360, color='lime', linestyle='-', alpha=0.3)
    plt.axvline(0, color='lime', linestyle='-', alpha=0.3, label='Major Groove (0°)')
    plt.axvspan(12, 24, color='cyan', alpha=0.2, label='Minor Groove (18°)')

    plt.title("Retrograde Potential Test: Do Outliers Lag the Rotation?", color='white', fontsize=14)
    plt.xlabel("Helical Phase Angle (Degrees)", color='gray')
    plt.ylabel("Retrograde Drift (km/s)\n(Positive = Dragging/Lagging | Negative = Moving Fast)", color='gray')
    
    plt.grid(True, color='#222222', linestyle=':')
    ax.tick_params(colors='gray')
    plt.legend(loc='upper right')
    
    plt.xlim(-20, 380)
    
    plt.savefig("helical_retrograde_test.png")
    print("✅ Analysis Complete. Saved to helical_retrograde_test.png")

if __name__ == "__main__":
    main()