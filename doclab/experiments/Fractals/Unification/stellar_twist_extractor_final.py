import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.interpolate import Rbf
from matplotlib.patches import FancyArrowPatch

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# The Maw (Cold Spot Core)
TARGET_L = -155.9
TARGET_B = -63.9
ZOOM_DEG = 50.0   # Wide Field to capture the whole Corkscrew
RES = 400         # High Resolution

# EXPANDED STELLAR CATALOG (The "Swirl Squad" + Reinforcements)
# [RA, Dec, Dist, pmRA, pmDec, RV]
STARS_KINEMATICS = {
    # The Inner Ring (The Guardian)
    "Achernar":      (24.43,  -57.24, 42.7,  88.0,    -40.0,   16.0),
    "Canopus":       (95.99,  -52.70, 94.0,  19.9,    23.2,    20.5),
    "Alpha Centauri":(219.90, -60.83, 1.33,  -3679.3, 473.7,  -21.4),
    "Peacock":       (306.41, -56.74, 56.0,  18.2,    -105.4,  2.0),
    "Ankaa":         (6.57,   -42.31, 23.8,  237.0,   -178.0,  -11.0),
    "Alnair":        (332.06, -46.96, 31.0,  108.0,   -137.0,  11.0),
    
    # The Outer Ring (The Funnel)
    "Fomalhaut":     (344.41, -29.62, 7.7,   329.2,   -164.2,  6.5),
    "Beta Ceti":     (12.27,  -17.99, 29.5,  232.0,   32.0,    13.0),
    "Acamar":        (40.07,  -40.30, 49.4,  58.0,    -14.0,   12.0),
    "Zaurak":        (59.56,  -13.51, 60.0,  -2.0,    -56.0,   57.0),
    "Rigel":         (78.63,  -8.20,  260.0, 1.31,    0.50,    17.8),
    "Sirius":        (101.28, -16.71, 2.64,  -546.0,  -1223.1, -5.5),
    "Adhara":        (104.66, -28.97, 123.0, 2.0,     -3.0,    27.0),
    
    # Deep Field Anchors (Phoenix/Fornax region)
    "Phoenicis":     (10.50,  -46.00, 30.0,  200.0,   -100.0,  10.0), # Approx/Proxy
    "Beta Hydri":    (4.10,   -77.25, 7.5,   2240.0,  -320.0,  23.0),
    "Gamma Grus":    (338.0,  -37.0,  30.0,  150.0,   -150.0,  -10.0) # Approx/Proxy
}

SOLAR_U, SOLAR_V, SOLAR_W = 11.1, 12.24, 7.25

def get_phantom_vector(name, data):
    ra, dec, dist, pm_ra, pm_dec, rv = data
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=dist*u.pc,
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, pm_dec=pm_dec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s, frame='icrs')
    g = c.galactic
    l, b = g.l.deg, g.b.deg
    
    # 3D Velocity
    v_xyz = g.velocity.d_xyz.value
    # Twist Deviation (Phantom Vector)
    dv = (v_xyz[1] + SOLAR_V) - (-10) # Rotation Lag
    dw = (v_xyz[2] + SOLAR_W) - 0     # Vertical Bob
    
    return l, b, dv, dw

def generate_grand_fields(fits_path):
    print("[*] Generating the Grand Fields (CMB + Stellar Flow)...")
    
    # 1. Stellar Flow Field (Interpolated)
    l_list, b_list, fx_list, fy_list = [], [], [], []
    
    for name, data in STARS_KINEMATICS.items():
        l, b, fx, fy = get_phantom_vector(name, data)
        # Shift l to center on Target (handle -180/180 wrap)
        # Target is -155. So -180 is close to -155. 180 is far.
        # We want everything in [-180, 180] relative to target?
        # Let's just normalize to -180..180
        if l > 180: l -= 360
        
        l_list.append(l)
        b_list.append(b)
        fx_list.append(fx)
        fy_list.append(fy)
        
    # RBF Interpolation
    rbf_x = Rbf(l_list, b_list, fx_list, function='thin_plate', smooth=0.5)
    rbf_y = Rbf(l_list, b_list, fy_list, function='thin_plate', smooth=0.5)
    
    grid_l = np.linspace(TARGET_L - ZOOM_DEG/2, TARGET_L + ZOOM_DEG/2, RES)
    grid_b = np.linspace(TARGET_B - ZOOM_DEG/2, TARGET_B + ZOOM_DEG/2, RES)
    L, B = np.meshgrid(grid_l, grid_b)
    
    FLOW_U = rbf_x(L, B)
    FLOW_V = rbf_y(L, B)
    
    # 2. CMB Background
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
    TEMP_MAP = cmb[ipix]
    
    return TEMP_MAP, FLOW_U, FLOW_V, L, B, l_list, b_list

def calculate_friction_outline(temp, flow_u, flow_v):
    # Calculate gradients of CMB to find friction
    gy, gx = np.gradient(temp)
    # Normalize
    mag = np.sqrt(gx**2 + gy**2); mag[mag==0]=1
    cu, cv = gx/mag, gy/mag
    
    # Normalize flow
    fmag = np.sqrt(flow_u**2 + flow_v**2); fmag[fmag==0]=1
    fu, fv = flow_u/fmag, flow_v/fmag
    
    # Friction = Difference
    friction = np.sqrt((cu-fu)**2 + (cv-fv)**2)
    
    # Create Contour Mask (The Beast)
    # Smooth it for nice outline
    from scipy.ndimage import gaussian_filter
    friction_smooth = gaussian_filter(friction, sigma=3)
    
    return friction_smooth

def main():
    print(f"[*] Constructing the Pirouette Grand Map...")
    
    # 1. Get Data
    temp, flow_u, flow_v, L, B, star_l, star_b = generate_grand_fields(FITS_PATH)
    
    # 2. Get Friction (The Beast)
    friction = calculate_friction_outline(temp, flow_u, flow_v)
    
    # 3. Visualization
    fig = plt.figure(figsize=(16, 12), facecolor='#000500')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#000500')
    
    # LAYER 1: The Territory (CMB Depth)
    # Use 'magma' or 'bone' for deep space feel
    im = ax.imshow(temp, cmap='magma', origin='lower', 
                   extent=[L.min(), L.max(), B.min(), B.max()], alpha=0.8)
    
    # LAYER 2: The Beast (Friction Outline)
    # We use a contour to show the "Skin" of the Maw
    ax.contour(L, B, friction, levels=[1.2], colors='lime', linewidths=2, alpha=0.7)
    
    # LAYER 3: The Corkscrew (Averaged Trajectories)
    # Streamplot calculates the integrated path (trajectory)
    strm = ax.streamplot(np.linspace(L.min(), L.max(), RES), 
                         np.linspace(B.min(), B.max(), RES),
                         flow_u, flow_v, 
                         color='cyan', 
                         density=1.5,      # Density of lines
                         linewidth=0.8, 
                         arrowsize=1.0,
                         arrowstyle='->')
    
    # LAYER 4: The Buoys (Stars)
    # Plot stars
    ax.scatter(star_l, star_b, c='white', s=80, edgecolors='cyan', zorder=10)
    
    # Label key stars
    for i, name in enumerate(STARS_KINEMATICS.keys()):
        # Only label if in view
        if L.min() < star_l[i] < L.max() and B.min() < star_b[i] < B.max():
            ax.text(star_l[i]+1, star_b[i]+1, name, color='white', fontsize=9, fontweight='bold')

    # Annotations
    ax.set_title("THE PIROUETTE GRAND MAP: Soliton, Wake, and Corkscrew Flow", color='white', fontsize=18, pad=20)
    ax.set_xlabel("Galactic Longitude (l)", color='gray')
    ax.set_ylabel("Galactic Latitude (b)", color='gray')
    
    # Add a Target Reticle on the Core
    ax.scatter(TARGET_L, TARGET_B, marker='+', s=500, color='lime', linewidth=2)
    ax.text(TARGET_L, TARGET_B-3, "MAW CORE", color='lime', ha='center', fontweight='bold')
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='cyan', lw=1, label='Stellar Flow (Corkscrew)'),
        Line2D([0], [0], color='lime', lw=2, label='Friction Boundary (The Beast)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='w', markersize=8, label='Guardian Stars'),
        Line2D([0], [0], marker='+', color='lime', markersize=10, lw=0, label='Soliton Core')
    ]
    ax.legend(handles=legend_elements, loc='upper right', facecolor='#111111', labelcolor='white')
    
    ax.grid(True, color='#333333', linestyle=':')
    
    plt.savefig("pirouette_grand_map.png")
    print("✅ GRAND MAP SAVED: pirouette_grand_map.png")
    print("\nINTERPRETATION:")
    print(" 1. The BACKGROUND is the Ancient Universe (CMB).")
    print(" 2. The CYAN LINES are the averaged trajectories of the stars (The Corkscrew).")
    print(" 3. The LIME CONTOUR is where the two disagree (The Soliton/Predator).")
    print(" 4. Observe how the Cyan lines spiral AROUND the Lime center.")

if __name__ == "__main__":
    main()