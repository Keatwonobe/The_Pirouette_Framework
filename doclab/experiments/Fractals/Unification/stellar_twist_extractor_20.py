import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from astropy.coordinates import SkyCoord
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
# The Invisible Axis (Cold Spot Core)
AXIS_L = -155.9
AXIS_B = -63.9

# The "Swirl Squad" (Stars near the axis)
STARS_KINEMATICS = {
    "Achernar":      (24.43,  -57.24, 42.7,  88.0,    -40.0,   16.0), # The Guardian
    "Canopus":       (95.99,  -52.70, 94.0,  19.9,    23.2,    20.5),
    "Alpha Centauri":(219.90, -60.83, 1.33,  -3679.3, 473.7,  -21.4),
    "Peacock":       (306.41, -56.74, 56.0,  18.2,    -105.4,  2.0),
    "Ankaa":         (6.57,   -42.31, 23.8,  237.0,   -178.0,  -11.0),
    "Alnair":        (332.06, -46.96, 31.0,  108.0,   -137.0,  11.0),
    "Fomalhaut":     (344.41, -29.62, 7.7,   329.2,   -164.2,  6.5),
    "Beta Ceti":     (12.27,  -17.99, 29.5,  232.0,   32.0,    13.0),
    "Sirius":        (101.28, -16.71, 2.64,  -546.0,  -1223.1, -5.5), # Reference
    "Rigel":         (78.63,  -8.20,  260.0, 1.31,    0.50,    17.8)  # Reference
}

SOLAR_U, SOLAR_V, SOLAR_W = 11.1, 12.24, 7.25

def get_3d_kinematics(name, data):
    ra, dec, dist, pm_ra, pm_dec, rv = data
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=dist*u.pc,
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, pm_dec=pm_dec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s, frame='icrs')
    
    # 1. 3D Position (XYZ) relative to Sun
    # Astropy Cartesian representation: x points to Galactic Center
    g = c.galactic
    xyz = g.cartesian
    x, y, z = xyz.x.value, xyz.y.value, xyz.z.value
    
    # 2. 3D Velocity (UVW)
    uvw = g.velocity.d_xyz.value
    u_vel = uvw[0] + SOLAR_U
    v_vel = uvw[1] + SOLAR_V
    w_vel = uvw[2] + SOLAR_W
    
    return x, y, z, u_vel, v_vel, w_vel

def get_axis_vector():
    # Convert Axis (l,b) to a Unit Vector in 3D
    c = SkyCoord(l=AXIS_L*u.deg, b=AXIS_B*u.deg, frame='galactic')
    xyz = c.cartesian
    return np.array([xyz.x.value, xyz.y.value, xyz.z.value])

def main():
    print(f"[*] Visualizing the Vortex Tunnel in 3D...")
    
    fig = plt.figure(figsize=(12, 10), facecolor='#050505')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#050505')
    
    # 1. Draw the Maw Axis (The Invisible Core)
    axis_vec = get_axis_vector() * 100 # Length 100 pc
    ax.plot([0, axis_vec[0]], [0, axis_vec[1]], [0, axis_vec[2]], 
            color='lime', linestyle='--', linewidth=2, label='Maw Axis (Cold Spot)')
    
    # 2. Plot Stars
    for name, data in STARS_KINEMATICS.items():
        x, y, z, u_v, v_v, w_v = get_3d_kinematics(name, data)
        
        # Calculate Tangential Velocity relative to Axis
        # V_tan = V - (V . Axis) * Axis
        v_vec = np.array([u_v, v_v, w_v])
        axis_unit = axis_vec / np.linalg.norm(axis_vec)
        v_proj = np.dot(v_vec, axis_unit) * axis_unit
        v_tan = v_vec - v_proj
        
        # Color by Swirl Intensity
        swirl_mag = np.linalg.norm(v_tan)
        c = plt.cm.cool(min(swirl_mag/50, 1.0))
        
        # Plot Star
        ax.scatter(x, y, z, color=c, s=100, edgecolors='white')
        ax.text(x+2, y+2, z+2, name, color='white', fontsize=8)
        
        # Draw Velocity Vector
        # We exaggerate length for visibility
        scale = 2.0
        ax.quiver(x, y, z, u_v*scale, v_v*scale, w_v*scale, color=c, alpha=0.6, length=1)
        
        # Draw "Tether" to Axis (to visualize the spiral)
        # Find closest point on axis line
        star_vec = np.array([x, y, z])
        proj_on_axis = np.dot(star_vec, axis_unit) * axis_unit
        ax.plot([x, proj_on_axis[0]], [y, proj_on_axis[1]], [z, proj_on_axis[2]], 
                color='gray', linestyle=':', alpha=0.3)

    # Styling
    ax.set_xlabel('X (Toward GC)', color='gray')
    ax.set_ylabel('Y (Rotation)', color='gray')
    ax.set_zlabel('Z (North)', color='gray')
    
    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')
    ax.tick_params(axis='z', colors='gray')
    
    # Remove pane fills
    ax.xaxis.set_pane_color((0, 0, 0, 0))
    ax.yaxis.set_pane_color((0, 0, 0, 0))
    ax.zaxis.set_pane_color((0, 0, 0, 0))
    
    # Camera
    ax.view_init(elev=20, azim=-60)
    
    plt.savefig("stellar_maw_3d.png")
    print("✅ 3D Vortex Model Saved: stellar_maw_3d.png")
    print("\nINTERPRETATION:")
    print(" 1. Lime Line = The Invisible Axis pointing to the Cold Spot.")
    print(" 2. Cyan/Pink Vectors = Stellar Motion.")
    print(" 3. LOOK FOR: A 'Corkscrew' pattern where stars spiral around the Lime Line.")

if __name__ == "__main__":
    main()