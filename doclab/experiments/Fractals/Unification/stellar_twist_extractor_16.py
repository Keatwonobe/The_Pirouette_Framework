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

# Target: The Soliton Core
TARGET_L = -155.9
TARGET_B = -63.9
ZOOM_DEG = 20.0     
RES = 300           

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

def calculate_caustics(fits_path):
    print("[*] Generating Caustic Map (Divergence of Delta)...")
    
    # 1. Re-Generate Fields (Stars vs CMB)
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
    
    su = rbf_x(L, B)
    sv = rbf_y(L, B)
    # Norm
    smag = np.sqrt(su**2 + sv**2); smag[smag==0]=1
    su/=smag; sv/=smag

    # CMB
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
    cmag = np.sqrt(gx**2 + gy**2); cmag[cmag==0]=1
    cu = gx/cmag; cv = gy/cmag
    
    # 2. Delta Field
    du = cu - su
    dv = cv - sv
    
    # 3. Divergence (The Caustic Finder)
    # Div = d(du)/dx + d(dv)/dy
    # Note: np.gradient returns (d_y, d_x)
    dy_du, dx_du = np.gradient(du)
    dy_dv, dx_dv = np.gradient(dv)
    
    divergence = dx_du + dy_dv
    
    # 4. Curl (The Spin) for reference
    curl = dx_dv - dy_du
    
    return divergence, curl, patch

def main():
    div, curl, temp = calculate_caustics(FITS_PATH)
    
    fig = plt.figure(figsize=(18, 6), facecolor='#0a0a0a')
    
    # A. Divergence Map (The Folds)
    ax1 = fig.add_subplot(131)
    # Negative Div (Blue) = Sink/Compression (Caustic)
    # Positive Div (Red) = Source/Expansion
    vmax = np.std(div) * 2.5
    im1 = ax1.imshow(div, cmap='RdBu', origin='lower', vmin=-vmax, vmax=vmax)
    ax1.set_title("1. CAUSTIC MAP (Divergence)", color='white')
    ax1.axis('off')
    plt.colorbar(im1, ax=ax1, label="Compression (Blue) vs Expansion (Red)")
    
    # B. Curl Map (The Spin)
    ax2 = fig.add_subplot(132)
    vmax_c = np.std(curl) * 2.5
    im2 = ax2.imshow(curl, cmap='PRGn', origin='lower', vmin=-vmax_c, vmax=vmax_c)
    ax2.set_title("2. SPIN MAP (Curl)", color='white')
    ax2.axis('off')
    
    # C. Composite Anatomy
    ax3 = fig.add_subplot(133)
    ax3.set_facecolor('#000000')
    
    # Background: Temperature (The Hole)
    ax3.imshow(temp, cmap='gray', origin='lower', alpha=0.5)
    
    # Overlay: Caustics (Blue lines = Folds)
    # We create a mask for strong negative divergence
    caustic_mask = np.ma.masked_where(div > -np.std(div), div)
    ax3.imshow(caustic_mask, cmap='winter', origin='lower', alpha=0.9) # Bright Blue/Cyan
    
    # Overlay: Vortex Cores (Purple/Green blobs)
    # Mask for strong curl
    curl_mask = np.ma.masked_where(np.abs(curl) < np.std(curl), curl)
    ax3.imshow(curl_mask, cmap='PRGn', origin='lower', alpha=0.6)
    
    ax3.set_title("3. MANIFOLD ANATOMY", color='white')
    ax3.text(10, 20, "Blue = Fold Lines (Sinks)", color='cyan', fontweight='bold')
    ax3.text(10, 10, "Purple/Green = Vortices", color='lime', fontweight='bold')
    ax3.axis('off')
    
    plt.savefig("cmb_manifold_caustics.png")
    print("✅ Caustic Analysis Saved: cmb_manifold_caustics.png")
    
    # Interpretation Helper
    min_div = np.min(div)
    max_div = np.max(div)
    
    print("\n" + "="*50)
    print("TOPOLOGY REPORT:")
    if abs(min_div) > abs(max_div):
        print("Type: DOMINANT SINK (Compression)")
        print("The manifold is folding inward (Negative Divergence wins).")
        print("Look for sharp Blue lines in Plot 3 - these are the 'Creases'.")
    else:
        print("Type: DOMINANT SOURCE (Expansion)")
        print("The manifold is bubbling outward.")

if __name__ == "__main__":
    main()