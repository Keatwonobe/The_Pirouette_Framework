import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.interpolate import Rbf

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Target: The Cold Spot Core
TARGET_L = -155.9
TARGET_B = -63.9
ZOOM_DEG = 20.0     # Wide enough to see the wake
RES = 200           # Resolution

# Kinematics
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
    dv = (v_xyz[1] + SOLAR_V) - (-10)
    dw = (v_xyz[2] + SOLAR_W) - 0
    return g.l.deg, g.b.deg, dv, dw

def generate_fields(fits_path):
    print("[*] Generating Flow Fields (Normal vs Actual)...")
    
    # 1. Stellar Field (The Normal)
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
    
    grid_l = np.linspace(TARGET_L - ZOOM_DEG/2, TARGET_L + ZOOM_DEG/2, RES)
    grid_b = np.linspace(TARGET_B - ZOOM_DEG/2, TARGET_B + ZOOM_DEG/2, RES)
    L, B = np.meshgrid(grid_l, grid_b)
    
    star_u = rbf_x(L, B)
    star_v = rbf_y(L, B)
    
    # Normalize
    s_mag = np.sqrt(star_u**2 + star_v**2)
    s_mag[s_mag==0] = 1
    star_u /= s_mag
    star_v /= s_mag

    # 2. CMB Field (The Actual)
    data = fits.getdata(fits_path)
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    coords = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    patch = cmb[ipix]
    
    gy, gx = np.gradient(patch)
    c_mag = np.sqrt(gx**2 + gy**2)
    c_mag[c_mag==0] = 1
    cmb_u = gx / c_mag
    cmb_v = gy / c_mag
    
    return star_u, star_v, cmb_u, cmb_v, patch, L, B

def calculate_delta_metrics(star_u, star_v, cmb_u, cmb_v):
    print("[*] Calculating Delta Metrics (Friction & Spin)...")
    
    # 1. Delta Vector (The Difference)
    # D = CMB - Star
    delta_u = cmb_u - star_u
    delta_v = cmb_v - star_v
    
    # Friction Magnitude (How much are they fighting?)
    friction = np.sqrt(delta_u**2 + delta_v**2)
    
    # 2. Delta Curl (The Spin from Normal)
    # Curl_2D = d(Dv)/dx - d(Du)/dy
    dy_du, dx_du = np.gradient(delta_u)
    dy_dv, dx_dv = np.gradient(delta_v)
    
    # Note: gradient returns (d/axis0, d/axis1). Axis0 is y (lat), Axis1 is x (lon)
    curl = dx_dv - dy_du
    
    return friction, curl, delta_u, delta_v

def main():
    # 1. Get Fields
    su, sv, cu, cv, temp, L, B = generate_fields(FITS_PATH)
    
    # 2. Calculate Physics
    friction, curl, du, dv = calculate_delta_metrics(su, sv, cu, cv)
    
    # 3. Visualize
    fig = plt.figure(figsize=(18, 6), facecolor='#0a0a0a')
    
    # A. Friction Map (Turbulence)
    ax1 = fig.add_subplot(131)
    # Friction ranges 0 (aligned) to 2 (opposed). 
    im1 = ax1.imshow(friction, cmap='inferno', origin='lower', vmin=0, vmax=2)
    ax1.set_title("1. Flow Friction (Drag)", color='white')
    ax1.axis('off')
    plt.colorbar(im1, ax=ax1, label="Vector Disagreement")
    
    # B. The Predator's Silhouette (Curl of Delta)
    ax2 = fig.add_subplot(132)
    # Diverging colormap: Red = Clockwise Spin, Blue = Counter-Clockwise
    # This highlights the EDGES of the wake
    vmax = np.std(curl) * 3
    im2 = ax2.imshow(curl, cmap='RdBu_r', origin='lower', vmin=-vmax, vmax=vmax)
    ax2.set_title("2. Delta Spin (Vorticity of the Wake)", color='white')
    ax2.axis('off')
    
    # C. Composite: The Beast in the Current
    ax3 = fig.add_subplot(133)
    ax3.set_facecolor('#000000')
    
    # Background: Temperature
    ax3.imshow(temp, cmap='gray', origin='lower', alpha=0.5)
    
    # Overlay: High Friction Zones (The Body)
    mask = friction > 1.2 # Significant disagreement
    ax3.imshow(mask, cmap='spring', origin='lower', alpha=0.6)
    
    # Overlay: Streamlines of the DELTA (The Turbulence Flow)
    # This shows how the fluid moves relative to the "Normal"
    ax3.streamplot(np.arange(RES), np.arange(RES), du, dv, color='cyan', density=1, linewidth=0.5, arrowsize=0.5)
    
    ax3.set_title("3. THE PREDATOR (Friction + Delta Flow)", color='white')
    ax3.axis('off')
    
    plt.savefig("cmb_flow_delta.png")
    print("✅ Delta Analysis Saved: cmb_flow_delta.png")
    
    print("\n" + "="*50)
    print("INTERPRETATION:")
    print(" 1. Friction Map: Bright spots are where the CMB violently disagrees with the Star Field.")
    print("    - A solid shape here is the 'Body' of the Soliton.")
    print(" 2. Delta Spin: Shows the rotational wake.")
    print("    - Look for paired Red/Blue lobes (Dipole) indicating flow around an object.")

if __name__ == "__main__":
    main()