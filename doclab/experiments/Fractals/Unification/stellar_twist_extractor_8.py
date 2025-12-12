import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.interpolate import Rbf

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Target: The Cold Spot Basin (Rank #3)
TARGET_L = -155.9 
TARGET_B = -63.9
ZOOM = 20    # Degrees wide
RES = 60     # Resolution (Keep relatively low for clean 3D wireframe)

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
    "Capella":       (79.17, 45.99, 12.9, 75.5, -427.1, 30.2),
    "Pollux":        (116.32, 28.02, 10.3, -626.5, -45.8, 3.2),
    "Deneb":         (310.35, 45.28, 802.0, 1.56, 1.55, -4.5),
    "Regulus":       (152.09, 11.96, 23.8, -248.5, 6.0, 5.9),
    "Castor":        (113.65, 31.88, 15.6, -192.4, -146.7, 14.4),
    "Spica":         (201.29, -11.16, 77.0, -42.5, -31.7, 1.0)
}
SOLAR_U, SOLAR_V, SOLAR_W = 11.1, 12.24, 7.25

def get_phantom_vector(name, data):
    ra, dec, dist, pm_ra, pm_dec, rv = data
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=dist*u.pc,
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, pm_dec=pm_dec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s, frame='icrs')
    g = c.galactic
    v_xyz = g.velocity.d_xyz.value
    dv = (v_xyz[1] + SOLAR_V) - (-10) # Rotation Lag
    dw = (v_xyz[2] + SOLAR_W) - 0     # Vertical Bob
    return g.l.deg, g.b.deg, dv, dw

def generate_stellar_field():
    l_list, b_list, fx_list, fy_list = [], [], [], []
    for name, data in STARS_KINEMATICS.items():
        l, b, fx, fy = get_phantom_vector(name, data)
        if l > 180: l -= 360
        l_list.append(l)
        b_list.append(b)
        fx_list.append(fx)
        fy_list.append(fy)
    
    rbf_x = Rbf(l_list, b_list, fx_list, function='thin_plate', smooth=0.5)
    rbf_y = Rbf(l_list, b_list, fy_list, function='thin_plate', smooth=0.5)
    
    # Target Grid
    grid_l = np.linspace(TARGET_L - ZOOM/2, TARGET_L + ZOOM/2, RES)
    grid_b = np.linspace(TARGET_B - ZOOM/2, TARGET_B + ZOOM/2, RES)
    L, B = np.meshgrid(grid_l, grid_b)
    
    FX = rbf_x(L, B)
    FY = rbf_y(L, B)
    
    return L, B, FX, FY

def extract_cmb_surface(fits_path):
    data = fits.getdata(fits_path)
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    grid_l = np.linspace(TARGET_L - ZOOM/2, TARGET_L + ZOOM/2, RES)
    grid_b = np.linspace(TARGET_B - ZOOM/2, TARGET_B + ZOOM/2, RES)
    L, B = np.meshgrid(grid_l, grid_b)
    
    coords = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    
    # Extract Temp (K)
    # We invert it for the plot: Deep Cold = Deep Hole
    T = cmb[ipix]
    return L, B, T

def main():
    print(f"[*] Visualizing the Maw in 3D (l={TARGET_L}, b={TARGET_B})...")
    
    # 1. Get Data
    L, B, T = extract_cmb_surface(FITS_PATH)
    _, _, FX, FY = generate_stellar_field()
    
    # 2. Normalize for 3D scaling
    # We want the temperature to look like terrain
    T_norm = (T - np.mean(T)) / np.std(T)
    # Invert so Cold = Down
    T_vis = -T_norm 
    
    # 3. Visualization
    fig = plt.figure(figsize=(12, 10), facecolor='#050505')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#050505')
    
    # Plot Surface (CMB Topology)
    surf = ax.plot_surface(L, B, T_vis, cmap='magma', edgecolor='none', alpha=0.8, rstride=1, cstride=1)
    
    # Plot Wireframe (for structure)
    ax.plot_wireframe(L, B, T_vis, color='black', alpha=0.2, rstride=5, cstride=5)
    
    # Plot Quiver (Stellar Forces)
    # We check stride to avoid cluttering the plot
    skip = 4
    
    # We place the vectors slightly above the surface
    Z_offset = T_vis + 0.5 
    
    # Vector scaling
    mag = np.sqrt(FX**2 + FY**2)
    FX_n = FX / np.max(mag)
    FY_n = FY / np.max(mag)
    
    # Quiver Key:
    # X direction = Longitude flow
    # Y direction = Latitude flow
    # Z direction = 0 (We assume the force is tangential to the sky plane)
    ax.quiver(L[::skip, ::skip], B[::skip, ::skip], Z_offset[::skip, ::skip], 
              FX_n[::skip, ::skip], FY_n[::skip, ::skip], 0, 
              color='cyan', length=1.0, normalize=True, linewidth=1.5, arrow_length_ratio=0.3)
    
    # Labels
    ax.set_title("The Maw Hypothesis: 3D Topology Inspector", color='white', fontsize=14)
    ax.set_xlabel("Longitude (l)", color='white')
    ax.set_ylabel("Latitude (b)", color='white')
    ax.set_zlabel("Cold Depth (Inverse Temp)", color='white')
    
    # Axis styling
    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')
    ax.tick_params(axis='z', colors='gray')
    ax.xaxis.set_pane_color((0.1, 0.1, 0.1, 1.0))
    ax.yaxis.set_pane_color((0.1, 0.1, 0.1, 1.0))
    ax.zaxis.set_pane_color((0.1, 0.1, 0.1, 1.0))
    
    # Initial Camera Angle
    ax.view_init(elev=45, azim=-135)
    
    plt.savefig("cmb_maw_3d.png")
    print("✅ 3D Render Saved: cmb_maw_3d.png")
    print("\n INTERPRETATION KEY:")
    print(" 1. The Terrain is the CMB Temperature (Lower = Colder/Deeper).")
    print(" 2. The Cyan Arrows are the Stellar Twist Vectors.")
    print(" 3. LOOK FOR: Do the arrows flow INTO the hole (Sink) or ALONG the channel (River)?")

if __name__ == "__main__":
    main()