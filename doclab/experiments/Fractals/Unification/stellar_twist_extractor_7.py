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

# Target: The Cold Spot Basin (Your Rank #3)
TARGET_L = -155.9 
TARGET_B = -63.9
ZOOM = 30 # Degrees wide

# Stellar Kinematics (To regenerate the Key)
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
    # Twist Deviation vector
    dv = (v_xyz[1] + SOLAR_V) - (-10) # Rotation Lag
    dw = (v_xyz[2] + SOLAR_W) - 0     # Vertical Bob
    return g.l.deg, g.b.deg, dv, dw

def generate_scalar_twist_field(res=100):
    # We convert the vector field (U,V) into a scalar field (Magnitude)
    # This represents the "Energy" of the twist we want to subtract
    l_list, b_list, mag_list = [], [], []
    for name, data in STARS_KINEMATICS.items():
        l, b, dv, dw = get_phantom_vector(name, data)
        if l > 180: l -= 360
        mag = np.sqrt(dv**2 + dw**2)
        l_list.append(l)
        b_list.append(b)
        mag_list.append(mag)
        
    rbf = Rbf(l_list, b_list, mag_list, function='thin_plate', smooth=0.5)
    
    # Generate field over the target window
    grid_l = np.linspace(TARGET_L - ZOOM/2, TARGET_L + ZOOM/2, res)
    grid_b = np.linspace(TARGET_B - ZOOM/2, TARGET_B + ZOOM/2, res)
    L, B = np.meshgrid(grid_l, grid_b)
    
    # We evaluate RBF at the VEGA-DENEB Key location (l=75, b=10) 
    # to get the pure "Shape" of the twist, independent of local coordinate
    # But we map it to the target window dimensions
    # Actually, we want to subtract the LOCALLY detected resonance pattern.
    # Let's use the local stellar RBF field "projected" to the target.
    
    # Simple approach: Generate the pattern at the Key location (Vega)
    # This assumes the Cold Spot is a "Stamp" of the Vega Vortex.
    TWIST_SHAPE = rbf(L + (75 - TARGET_L), B + (10 - TARGET_B))
    
    # Normalize (0 to 1)
    TWIST_SHAPE = (TWIST_SHAPE - np.min(TWIST_SHAPE)) / (np.max(TWIST_SHAPE) - np.min(TWIST_SHAPE))
    
    return TWIST_SHAPE, L, B

def extract_cmb_patch(fits_path, res=100):
    data = fits.getdata(fits_path)
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    grid_l = np.linspace(TARGET_L - ZOOM/2, TARGET_L + ZOOM/2, res)
    grid_b = np.linspace(TARGET_B - ZOOM/2, TARGET_B + ZOOM/2, res)
    L, B = np.meshgrid(grid_l, grid_b)
    
    coords = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    return cmb[ipix]

def main():
    print(f"[*] The Eraser Test: Can we subtract the Twist from the Cold Spot?")
    print(f"    Target: l={TARGET_L}, b={TARGET_B} (Cold Spot Basin)")
    
    # 1. Get the Raw CMB (The Territory)
    cmb_patch = extract_cmb_patch(FITS_PATH)
    
    # 2. Get the Twist Key (The Map)
    twist_key, L, B = generate_scalar_twist_field()
    
    # 3. Optimize Subtraction (Find best scaling factor)
    # We want to minimize the variance of (CMB - alpha * Twist)
    # This finds the "depth" of the twist in the CMB data
    from scipy.optimize import minimize_scalar
    
    def variance_after_subtraction(alpha):
        residual = cmb_patch - (alpha * twist_key * np.std(cmb_patch))
        return np.var(residual)
    
    res = minimize_scalar(variance_after_subtraction)
    best_alpha = res.x
    
    residual = cmb_patch - (best_alpha * twist_key * np.std(cmb_patch))
    variance_reduction = 100 * (1 - np.var(residual) / np.var(cmb_patch))
    
    print(f"    Optimal subtraction amplitude: {best_alpha:.4f}")
    print(f"    Variance Reduction: {variance_reduction:.2f}%")
    
    # 4. Visualization
    fig = plt.figure(figsize=(15, 5), facecolor='#0a0a0a')
    
    # A. Original Cold Spot
    ax1 = fig.add_subplot(131)
    im1 = ax1.imshow(cmb_patch, origin='lower', cmap='RdBu_r')
    ax1.set_title("1. Original CMB (Cold Spot)", color='white')
    ax1.axis('off')
    
    # B. The Twist Key (Stellar Data)
    ax2 = fig.add_subplot(132)
    im2 = ax2.imshow(twist_key, origin='lower', cmap='inferno')
    ax2.set_title("2. Stellar Twist Key (Vega Vortex)", color='white')
    ax2.axis('off')
    
    # C. The Residual (Healed Map)
    ax3 = fig.add_subplot(133)
    im3 = ax3.imshow(residual, origin='lower', cmap='RdBu_r')
    ax3.set_title(f"3. Residual (Eraser Result)\n-{variance_reduction:.1f}% Variance", color='white')
    ax3.axis('off')
    
    plt.savefig("cmb_twist_subtraction.png")
    print("✅ Experiment Complete. Saved: cmb_twist_subtraction.png")
    
    if variance_reduction > 10:
        print("\nSUCCESS: Significant anomaly reduction detected.")
        print("The Twist Key successfully 'healed' part of the Cold Spot.")
    else:
        print("\nRESULT: No significant reduction.")
        print("The Twist Key shape does not mathematically match the Cold Spot depth.")

if __name__ == "__main__":
    main()