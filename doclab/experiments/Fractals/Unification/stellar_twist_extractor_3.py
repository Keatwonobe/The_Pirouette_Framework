import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
from astropy.coordinates import SkyCoord
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
RESOLUTION = 100  # Grid resolution for flow map
SMOOTHING = 0.5   # RBF smoothing factor

# Full Kinematic Data
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

def get_phantom_vector(name, data):
    ra, dec, dist, pm_ra, pm_dec, rv = data
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=dist*u.pc,
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, pm_dec=pm_dec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s, frame='icrs')
    g = c.galactic
    l_deg = g.l.deg
    b_deg = g.b.deg
    
    # Velocities
    v_xyz = g.velocity.d_xyz.value
    u_act = v_xyz[0] + SOLAR_U
    v_act = v_xyz[1] + SOLAR_V # Rotation direction
    w_act = v_xyz[2] + SOLAR_W
    
    # PHANTOM VECTOR: Deviation from ideal quiet orbit
    du = u_act - 0
    dv = v_act - (-10)
    dw = w_act - 0
    
    l_rad = np.deg2rad(l_deg)
    
    # Simplified projection for visualization:
    # Flow X (along longitude) ~ dv (Rotation)
    # Flow Y (along latitude) ~ dw (Vertical)
    flow_x = dv 
    flow_y = dw 
    
    return l_deg, b_deg, flow_x, flow_y, np.sqrt(du**2 + dv**2 + dw**2)

def main():
    print("Generating Stellar Flow Map...")
    
    l_list, b_list = [], []
    fx_list, fy_list = [], []
    mag_list = []
    names_list = []  # <--- Added to keep track of names synced with data
    
    for name, data in STARS_KINEMATICS.items():
        if name == "Galactic Center": continue 
        l, b, fx, fy, mag = get_phantom_vector(name, data)
        
        # Aitoff/Map Projection Handling: Shift l to [-180, 180]
        if l > 180: l -= 360
        
        l_list.append(l)
        b_list.append(b)
        fx_list.append(fx)
        fy_list.append(fy)
        mag_list.append(mag)
        names_list.append(name) # <--- Store name here

    # 1. Create Interpolation Grid
    grid_l = np.linspace(-180, 180, RESOLUTION)
    grid_b = np.linspace(-90, 90, RESOLUTION)
    L_GRID, B_GRID = np.meshgrid(grid_l, grid_b)
    
    # 2. RBF Interpolation
    print("Interpolating Vector Field (RBF)...")
    rbf_x = Rbf(l_list, b_list, fx_list, function='thin_plate', smooth=SMOOTHING)
    rbf_y = Rbf(l_list, b_list, fy_list, function='thin_plate', smooth=SMOOTHING)
    rbf_m = Rbf(l_list, b_list, mag_list, function='thin_plate', smooth=SMOOTHING)
    
    FLOW_X = rbf_x(L_GRID, B_GRID)
    FLOW_Y = rbf_y(L_GRID, B_GRID)
    MAG_GRID = rbf_m(L_GRID, B_GRID)
    
    # 3. Visualization
    fig = plt.figure(figsize=(16, 9), facecolor='#050505')
    
    # Using standard rectangular plot to avoid projection artifacts in streamplot
    ax = fig.add_subplot(111)
    ax.set_facecolor('#050505')
    
    # Background Density (Force Magnitude)
    strm = ax.streamplot(grid_l, grid_b, FLOW_X, FLOW_Y, 
                         color=np.sqrt(FLOW_X**2 + FLOW_Y**2), 
                         cmap='plasma', 
                         density=2.0, 
                         linewidth=1, 
                         arrowsize=1.5)
    
    # Overlay Stars
    ax.scatter(l_list, b_list, c='white', s=50, zorder=10)
    
    # Fix for IndexError: Iterate over the synced names_list
    for i, txt in enumerate(names_list):
        ax.text(l_list[i]+2, b_list[i]+2, txt, color='white', fontsize=8)

    ax.set_title("The Stellar Flow Map: Interpolated Twist Currents", color='white', fontsize=16)
    ax.set_xlabel("Galactic Longitude (l)", color='gray')
    ax.set_ylabel("Galactic Latitude (b)", color='gray')
    
    cbar = plt.colorbar(strm.lines)
    cbar.set_label("Phantom Force Magnitude (km/s)", color='gray')
    cbar.ax.yaxis.set_tick_params(color='gray', labelcolor='gray')
    
    ax.grid(True, color='#333333', linestyle=':')
    ax.set_xlim(180, -180) # Astronomical convention
    ax.set_ylim(-90, 90)
    
    plt.savefig("stellar_flow_map.png")
    print("✅ Flow Map Saved: stellar_flow_map.png")
    
    np.savez("twist_flow_field.npz", L=L_GRID, B=B_GRID, U=FLOW_X, V=FLOW_Y)
    print("✅ Field Data Saved: twist_flow_field.npz")

if __name__ == "__main__":
    main()