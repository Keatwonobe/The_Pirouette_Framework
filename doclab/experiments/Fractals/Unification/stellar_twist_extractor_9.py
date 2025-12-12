import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.interpolate import Rbf
from scipy.signal import correlate2d
from skimage.transform import resize

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# Target: The Cold Spot Basin
TARGET_L = -155.9
TARGET_B = -63.9
SEARCH_SIZE = 40  # Degrees
RES = 100         # Pixel resolution of the search map

# Scales to test (The "Redshift" factor)
# 1.0 = Original Stellar Scale
# >1.0 = Redshifted (Stretched)
# <1.0 = Blueshifted (Compressed)
SCALES = np.linspace(0.5, 2.5, 20) 

# Re-include Kinematics for Key Gen
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

def generate_base_key(size_pixels=20):
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
    
    k_range = np.linspace(-10, 10, size_pixels) # 20 degree generic patch
    KL, KB = np.meshgrid(k_range, k_range)
    
    # Eval at Vega-Deneb Center (l=75, b=10)
    KU = rbf_x(KL + 75, KB + 10)
    KV = rbf_y(KL + 75, KB + 10)
    
    mag = np.sqrt(KU**2 + KV**2)
    mag[mag == 0] = 1
    return KU/mag, KV/mag

def load_cmb_gradients(fits_path):
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
    patch = cmb[ipix]
    
    grad_y, grad_x = np.gradient(patch)
    mag = np.sqrt(grad_x**2 + grad_y**2)
    mag[mag == 0] = 1
    
    return grad_x/mag, grad_y/mag, patch

def scan_redshift(cmb_u, cmb_v, base_key_u, base_key_v):
    print("[*] Scanning Manifold Redshift (Multi-Scale Correlation)...")
    
    best_scale_map = np.zeros_like(cmb_u)
    max_score_map = np.zeros_like(cmb_u) - 999
    
    for scale in SCALES:
        # Resize Key
        new_size = int(base_key_u.shape[0] * scale)
        if new_size < 3: continue
        
        # Resize preserving vector nature
        key_u_sc = resize(base_key_u, (new_size, new_size))
        key_v_sc = resize(base_key_v, (new_size, new_size))
        
        # Convolve
        score = correlate2d(cmb_u, key_u_sc, mode='same') + correlate2d(cmb_v, key_v_sc, mode='same')
        
        # Update Best Maps
        mask = score > max_score_map
        max_score_map[mask] = score[mask]
        best_scale_map[mask] = scale
        
    return best_scale_map, max_score_map

def main():
    # 1. Load Data
    cmb_u, cmb_v, cmb_temp = load_cmb_gradients(FITS_PATH)
    key_u, key_v = generate_base_key(size_pixels=20) # Base size ~20% of map
    
    # 2. Run Redshift Scan
    scale_map, score_map = scan_redshift(cmb_u, cmb_v, key_u, key_v)
    
    # 3. Visualize
    fig = plt.figure(figsize=(18, 6), facecolor='#0a0a0a')
    
    # A. CMB Temperature (Reference)
    ax1 = fig.add_subplot(131)
    im1 = ax1.imshow(cmb_temp, cmap='magma', origin='lower')
    ax1.set_title("1. The Cold Spot (Depth)", color='white')
    ax1.axis('off')
    
    # B. Match Strength (Where is the twist?)
    ax2 = fig.add_subplot(132)
    # Only show significant matches
    masked_score = np.ma.masked_where(score_map < np.mean(score_map) + 0.5*np.std(score_map), score_map)
    im2 = ax2.imshow(masked_score, cmap='inferno', origin='lower')
    ax2.set_title("2. Twist Pattern Strength", color='white')
    ax2.axis('off')
    
    # C. REDSHIFT MAP (The Manifold Stretch)
    ax3 = fig.add_subplot(133)
    # Mask low confidence areas to see the scale of the *signal* only
    masked_scale = np.ma.masked_where(score_map < np.mean(score_map) + 0.5*np.std(score_map), scale_map)
    
    im3 = ax3.imshow(masked_scale, cmap='seismic', origin='lower', vmin=0.5, vmax=2.5)
    ax3.set_title("3. MANIFOLD REDSHIFT MAP\n(Blue=Compressed, Red=Stretched)", color='white')
    ax3.axis('off')
    
    cbar = plt.colorbar(im3, ax=ax3)
    cbar.set_label("Scale Factor (1.0 = Local Star Scale)", color='white')
    cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
    
    plt.savefig("cmb_manifold_redshift.png")
    print("✅ Redshift Analysis Saved: cmb_manifold_redshift.png")
    
    # Analyze the Center vs Rim
    center_y, center_x = RES//2, RES//2
    center_scale = scale_map[center_y, center_x]
    
    # Rim is roughly 25% out
    rim_slice = scale_map[RES//4:3*RES//4, RES//4:3*RES//4]
    avg_rim_scale = np.mean(rim_slice)
    
    print("\n" + "="*50)
    print("MANIFOLD METRIC ANALYSIS:")
    print(f"Center Scale Factor: {center_scale:.2f}x")
    print(f"Ambient/Rim Scale:   {avg_rim_scale:.2f}x")
    
    if center_scale > avg_rim_scale:
        print("\n⚡ RESULT: REDSHIFT DETECTED.")
        print("The Twist Pattern is STRETCHED at the center of the Cold Spot.")
        print("This supports the 'Maw' (Gravity Well) hypothesis.")
    elif center_scale < avg_rim_scale:
        print("\n⚡ RESULT: BLUESHIFT DETECTED.")
        print("The Twist Pattern is COMPRESSED at the center.")
        print("This suggests a 'Fountain' or excessive pressure node.")
    else:
        print("\nRESULT: Flat Metric. No scale distortion observed.")

if __name__ == "__main__":
    main()