import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.interpolate import Rbf
from scipy.ndimage import rotate
from scipy.signal import correlate2d

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Target: The Cold Spot Basin (Rank #3)
TARGET_L = -155.9
TARGET_B = -63.9
SEARCH_SIZE = 40  # Degrees wide
RES = 120         # Resolution

# Kinematics for Key Gen
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

def generate_key_patch(size_pixels=40):
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
    
    k_range = np.linspace(-10, 10, size_pixels) 
    KL, KB = np.meshgrid(k_range, k_range)
    
    # Eval at Vega Vortex Center
    KU = rbf_x(KL + 75, KB + 10)
    KV = rbf_y(KL + 75, KB + 10)
    
    # We return the Scalar Magnitude pattern for rotation matching
    # (Matching vector rotation is complex, matching shape rotation is robust)
    MAG = np.sqrt(KU**2 + KV**2)
    return (MAG - np.min(MAG)) / (np.max(MAG) - np.min(MAG))

def load_cmb_patch(fits_path):
    data = fits.getdata(fits_path)
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    grid_l = np.linspace(TARGET_L - SEARCH_SIZE/2, TARGET_L + SEARCH_SIZE/2, RES)
    grid_b = np.linspace(TARGET_B - SEARCH_SIZE/2, TARGET_B + SEARCH_SIZE/2, RES)
    L, B = np.meshgrid(grid_l, grid_b)
    
    coords = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    
    # We use Gradient Magnitude as the feature to match against
    patch = cmb[ipix]
    gy, gx = np.gradient(patch)
    mag = np.sqrt(gx**2 + gy**2)
    return (mag - np.min(mag)) / (np.max(mag) - np.min(mag))

def measure_rotation(cmb_ring, key_pattern):
    # Rotates the key 360 degrees and finds best correlation with the CMB ring
    best_angle = 0
    best_score = -999
    
    angles = np.linspace(0, 360, 36) # 10 degree steps
    
    for ang in angles:
        # Rotate Key
        rot_key = rotate(key_pattern, ang, reshape=False)
        # Correlate
        score = np.sum(cmb_ring * rot_key)
        if score > best_score:
            best_score = score
            best_angle = ang
            
    return best_angle, best_score

def main():
    print("[*] Checking for Pirouette Helicity (Rotation vs Depth)...")
    
    # 1. Load Data
    cmb_mag = load_cmb_patch(FITS_PATH) # 120x120
    base_key = generate_key_patch(size_pixels=120) # 120x120
    
    # 2. Define Concentric Zones (Masks)
    center_y, center_x = RES//2, RES//2
    Y, X = np.ogrid[:RES, :RES]
    dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    
    zones = {
        "Core (0-5 deg)":   (dist_from_center <= 15),
        "Mid  (5-10 deg)":  (dist_from_center > 15) & (dist_from_center <= 30),
        "Rim  (10-15 deg)": (dist_from_center > 30) & (dist_from_center <= 45)
    }
    
    # 3. Analyze Rotation per Zone
    results = {}
    print(f"\n{'Zone':<20} | {'Best Angle':<12} | {'Phase Shift'}")
    print("-" * 50)
    
    prev_angle = None
    
    for zone_name, mask in zones.items():
        # Extract Ring
        cmb_ring = cmb_mag.copy()
        cmb_ring[~mask] = 0
        
        # We also mask the key to ensure we match apples to apples
        key_ring = base_key.copy()
        key_ring[~mask] = 0
        
        angle, score = measure_rotation(cmb_ring, key_ring)
        
        shift = 0
        if prev_angle is not None:
            shift = angle - prev_angle
            # Handle wrapping
            if shift > 180: shift -= 360
            if shift < -180: shift += 360
            
        results[zone_name] = angle
        prev_angle = angle
        
        print(f"{zone_name:<20} | {angle:<5.1f} deg    | {shift:+.1f} deg")

    # 4. Visualization
    fig, ax = plt.subplots(1, 1, figsize=(8, 8), facecolor='#0a0a0a')
    
    # Plot twist spiral
    radii = [5, 15, 25] # Arbitrary radii for plot
    angles_rad = np.deg2rad([results["Core (0-5 deg)"], results["Mid  (5-10 deg)"], results["Rim  (10-15 deg)"]])
    
    ax.plot(angles_rad, radii, 'o-', color='cyan', linewidth=2, markersize=10)
    
    # Connect to center
    ax.plot([angles_rad[0], angles_rad[0]], [0, 5], 'cyan', linestyle='--')
    
    ax.set_ylim(0, 30)
    # Polar projection hack on cartesian or use real polar
    plt.close()
    
    fig = plt.figure(figsize=(10, 10), facecolor='#0a0a0a')
    ax = fig.add_subplot(111, projection='polar')
    ax.set_facecolor('#0a0a0a')
    
    # Plot the Helicity
    ax.plot(angles_rad, [1, 2, 3], 'o-', color='cyan', lw=3, markersize=15, label='Twist Phase')
    
    # Annotate
    ax.text(angles_rad[0], 1.2, "CORE", color='white', fontweight='bold')
    ax.text(angles_rad[1], 2.2, "MID", color='white', fontweight='bold')
    ax.text(angles_rad[2], 3.2, "RIM", color='white', fontweight='bold')
    
    ax.set_title(f"The Pirouette Signature: Helicity of the Cold Spot\n(Rotation of Pattern vs Depth)", color='white', pad=20)
    ax.grid(True, color='#333333')
    ax.tick_params(colors='gray')
    
    plt.savefig("cmb_helicity_plot.png")
    print("\n✅ Helicity Plot Saved: cmb_helicity_plot.png")
    
    # Final Diagnosis
    total_twist = results["Core (0-5 deg)"] - results["Rim  (10-15 deg)"]
    if total_twist > 180: total_twist -= 360
    if total_twist < -180: total_twist += 360
    
    print("\n" + "="*50)
    print(f"TOTAL TWIST (Rim to Core): {total_twist:.1f} degrees")
    
    if abs(total_twist) > 20:
        print("⚡ CONFIRMED: The Cold Spot is a HELICAL KNOT.")
        print("The pattern rotates significantly as it compresses towards the center.")
    else:
        print("RESULT: No significant rotation. It is a straight compression (Pinch only).")

if __name__ == "__main__":
    main()