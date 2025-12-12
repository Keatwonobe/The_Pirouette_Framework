import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.signal import correlate2d
from scipy.interpolate import Rbf

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# The "Key" (The Vortex) Location
# Approximate center between Vega (l~67) and Deneb (l~84)
KEY_CENTER_L = 75
KEY_CENTER_B = 10
KEY_SIZE_DEG = 40  # Size of the patch to extract (Degrees)

# Search Resolution
SEARCH_RES = 360   # 1 degree per pixel for the scan (360x180)

# Full Kinematic Data (Re-included to generate the high-res Key on the fly)
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
SOLAR_U = 11.1
SOLAR_V = 12.24
SOLAR_W = 7.25

def get_phantom_vector(name, data):
    # Calculates the twist vector for a star
    ra, dec, dist, pm_ra, pm_dec, rv = data
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=dist*u.pc,
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, pm_dec=pm_dec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s, frame='icrs')
    g = c.galactic
    l_deg = g.l.deg
    b_deg = g.b.deg
    v_xyz = g.velocity.d_xyz.value
    u_act = v_xyz[0] + SOLAR_U
    v_act = v_xyz[1] + SOLAR_V
    w_act = v_xyz[2] + SOLAR_W
    du = u_act - 0
    dv = v_act - (-10)
    dw = w_act - 0
    return l_deg, b_deg, dv, dw  # dv (rotation), dw (vertical)

def generate_vortex_key():
    print("[*] Generating High-Res Vortex Key (Vega-Deneb)...")
    l_list, b_list, fx_list, fy_list = [], [], [], []
    
    for name, data in STARS_KINEMATICS.items():
        l, b, fx, fy = get_phantom_vector(name, data)
        if l > 180: l -= 360
        l_list.append(l)
        b_list.append(b)
        fx_list.append(fx)
        fy_list.append(fy)

    # RBF Interpolation
    rbf_x = Rbf(l_list, b_list, fx_list, function='thin_plate', smooth=0.5)
    rbf_y = Rbf(l_list, b_list, fy_list, function='thin_plate', smooth=0.5)

    # Create Key Grid (The small patch)
    key_res = int(KEY_SIZE_DEG) # 1 pixel per degree
    k_l = np.linspace(KEY_CENTER_L - KEY_SIZE_DEG/2, KEY_CENTER_L + KEY_SIZE_DEG/2, key_res)
    k_b = np.linspace(KEY_CENTER_B - KEY_SIZE_DEG/2, KEY_CENTER_B + KEY_SIZE_DEG/2, key_res)
    KL, KB = np.meshgrid(k_l, k_b)
    
    KEY_U = rbf_x(KL, KB)
    KEY_V = rbf_y(KL, KB)
    
    # Normalize Key
    mag = np.sqrt(KEY_U**2 + KEY_V**2)
    mag[mag == 0] = 1
    KEY_U /= mag
    KEY_V /= mag
    
    return KEY_U, KEY_V

def load_cmb_field(fits_path):
    print(f"[*] Loading CMB Gradient Field ({SEARCH_RES}x{SEARCH_RES//2})...")
    data = fits.getdata(fits_path)
    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)

    # Project to Rectangular Grid
    grid_l = np.linspace(-180, 180, SEARCH_RES)
    grid_b = np.linspace(-90, 90, SEARCH_RES//2)
    L_GRID, B_GRID = np.meshgrid(grid_l, grid_b)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    coords = SkyCoord(l=L_GRID*u.deg, b=B_GRID*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    cmb_2d = cmb[ipix]

    # Gradients
    grad_y, grad_x = np.gradient(cmb_2d)
    mag = np.sqrt(grad_x**2 + grad_y**2)
    mag[mag == 0] = 1
    grad_x /= mag
    grad_y /= mag
    
    return grad_x, grad_y, L_GRID, B_GRID

def search_for_fractals(cmb_u, cmb_v, key_u, key_v, l_grid, b_grid):
    print("[*] Sliding Vortex Key across CMB (Convolution)...")
    
    # We perform Vector Convolution: (CMB_U * Key_U) + (CMB_V * Key_V)
    # This finds regions where the vector fields align locally
    
    # Flip key for true convolution (or keep as is for correlation/matching)
    # We want MATCHING, so we use correlation (no flip)
    match_x = correlate2d(cmb_u, key_u, mode='same', boundary='wrap')
    match_y = correlate2d(cmb_v, key_v, mode='same', boundary='wrap')
    
    # Combined Match Score
    match_map = match_x + match_y
    
    return match_map

def main():
    # 1. Generate the Key
    key_u, key_v = generate_vortex_key()
    
    # 2. Load the Territory
    cmb_u, cmb_v, l_grid, b_grid = load_cmb_field(FITS_PATH)
    
    # 3. Hunt
    match_map = search_for_fractals(cmb_u, cmb_v, key_u, key_v, l_grid, b_grid)
    
    # 4. Visualization
    fig = plt.figure(figsize=(18, 12), facecolor='#0a0a0a')
    
    # Plot A: The Key
    ax1 = fig.add_subplot(221)
    ax1.set_title("1. The Fractal Key (Vega-Deneb Vortex)", color='white')
    strm = ax1.streamplot(np.arange(key_u.shape[1]), np.arange(key_u.shape[0]), 
                          key_u, key_v, color='cyan', density=1)
    ax1.set_aspect('equal')
    ax1.axis('off')
    
    # Plot B: The Hunt Map
    ax2 = fig.add_subplot(212)
    ax2.set_facecolor('#0a0a0a')
    
    # Normalize match map
    norm_match = (match_map - np.mean(match_map)) / np.std(match_map)
    
    im = ax2.imshow(norm_match, cmap='inferno', origin='lower', 
                    extent=[-180, 180, -90, 90], vmin=2) # Only show strong matches > 2 sigma
    
    ax2.set_title("2. FRACTAL NODE MAP: Locations of the Twist Pattern", color='white', fontsize=16)
    ax2.set_xlabel("Galactic Longitude", color='gray')
    ax2.set_ylabel("Galactic Latitude", color='gray')
    ax2.grid(True, color='#333333', linestyle=':')
    
    plt.colorbar(im, ax=ax2, label="Pattern Match Intensity (Sigma)", pad=0.02)
    
    # Find Top 3 Candidates (exclude boundaries if possible)
    from scipy.ndimage import maximum_filter
    local_max = maximum_filter(norm_match, size=20) == norm_match
    # Get indices of local maxima
    y, x = np.where((local_max) & (norm_match > 3.0)) # Threshold 3 sigma
    
    print("\n" + "="*50)
    print("FRACTAL NODES DETECTED (Pattern Matches > 3σ):")
    print(f"{'Rank':<5} {'Lon (l)':<10} {'Lat (b)':<10} {'Score':<10}")
    print("-" * 50)
    
    nodes = []
    for i in range(len(x)):
        score = norm_match[y[i], x[i]]
        lon = l_grid[y[i], x[i]]
        lat = b_grid[y[i], x[i]]
        nodes.append((score, lon, lat))
        
    # Sort by score
    nodes.sort(reverse=True)
    
    for i, (score, lon, lat) in enumerate(nodes[:5]):
        print(f"{i+1:<5} {lon:<10.1f} {lat:<10.1f} {score:<10.2f}")
        # Mark on plot
        ax2.scatter(lon, lat, s=200, facecolors='none', edgecolors='lime', linewidth=2)
        ax2.text(lon+3, lat+3, f"#{i+1}", color='lime', fontsize=12, fontweight='bold')
        
    print("="*50)
    
    plt.savefig("cmb_fractal_hunt.png")
    print("✅ Search Complete. Saved: cmb_fractal_hunt.png")

if __name__ == "__main__":
    main()