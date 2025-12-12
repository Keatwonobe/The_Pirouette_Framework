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

# The Nodes you found (Rank 1-5)
NODES = [
    {"rank": 1, "l": 2.5,    "b": -62.8, "name": "Southern Ring A"},
    {"rank": 2, "l": 70.7,   "b": -67.9, "name": "Southern Ring B"},
    {"rank": 3, "l": -155.9, "b": -63.9, "name": "Cold Spot Basin"}, # l=204.1
    {"rank": 4, "l": 118.8,  "b": 88.0,  "name": "North Galactic Pole"},
    {"rank": 5, "l": -164.0, "b": -30.7, "name": "Eridanus Anomaly"}
]

# Size of the zoom window (Degrees)
ZOOM_SIZE = 20 
RES = 50 # Pixel resolution of the zoom

# Re-include Key Generation for comparison overlay
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
    u_act = v_xyz[0] + SOLAR_U
    v_act = v_xyz[1] + SOLAR_V
    w_act = v_xyz[2] + SOLAR_W
    du = u_act - 0
    dv = v_act - (-10)
    dw = w_act - 0
    return g.l.deg, g.b.deg, dv, dw

def generate_key_overlay():
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
    
    # Generate a generic 20x20 grid centered at 0,0 for overlay
    k_l = np.linspace(-ZOOM_SIZE/2, ZOOM_SIZE/2, RES)
    k_b = np.linspace(-ZOOM_SIZE/2, ZOOM_SIZE/2, RES)
    KL, KB = np.meshgrid(k_l, k_b)
    
    # Eval at the VEGA-DENEB Key location (l=75, b=10)
    # This generates the pattern we matched against
    KU = rbf_x(KL + 75, KB + 10)
    KV = rbf_y(KL + 75, KB + 10)
    
    # Normalize
    mag = np.sqrt(KU**2 + KV**2)
    mag[mag == 0] = 1
    KU /= mag
    KV /= mag
    
    return KU, KV

def extract_cmb_patch(fits_path, center_l, center_b):
    try:
        data = fits.getdata(fits_path)
        if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else: cmb = data.astype(np.float64)
        mask = np.isnan(cmb)
        cmb[mask] = np.nanmean(cmb)
        
        nside = int(np.sqrt(cmb.size / 12))
        hpix = HEALPix(nside=nside, order="ring", frame="galactic")
        
        # Create Grid
        grid_l = np.linspace(center_l - ZOOM_SIZE/2, center_l + ZOOM_SIZE/2, RES)
        grid_b = np.linspace(center_b - ZOOM_SIZE/2, center_b + ZOOM_SIZE/2, RES)
        L_GRID, B_GRID = np.meshgrid(grid_l, grid_b)
        
        coords = SkyCoord(l=L_GRID*u.deg, b=B_GRID*u.deg, frame='galactic')
        ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
        patch = cmb[ipix]
        
        # Gradients
        grad_y, grad_x = np.gradient(patch)
        mag = np.sqrt(grad_x**2 + grad_y**2)
        mag[mag == 0] = 1
        grad_x /= mag
        grad_y /= mag
        
        return grad_x, grad_y, patch
    except Exception as e:
        print(f"[!] Error extracting patch: {e}")
        return None, None, None

def main():
    print("[*] Generating Visual Inspections for Fractal Nodes...")
    
    key_u, key_v = generate_key_overlay()
    
    fig = plt.figure(figsize=(20, 10), facecolor='#0a0a0a')
    
    for i, node in enumerate(NODES):
        print(f"  > Inspecting #{node['rank']}: {node['name']}...")
        
        gx, gy, temp = extract_cmb_patch(FITS_PATH, node['l'], node['b'])
        
        if gx is None: continue
        
        # Subplot layout: Row 1 = CMB Temp, Row 2 = Gradients + Key
        # We'll just do one complex plot per node in a row
        
        ax = fig.add_subplot(2, 3, i+1)
        ax.set_facecolor('#0a0a0a')
        
        # Background: CMB Temperature
        im = ax.imshow(temp, origin='lower', cmap='magma', extent=[-ZOOM_SIZE/2, ZOOM_SIZE/2, -ZOOM_SIZE/2, ZOOM_SIZE/2])
        
        # Foreground: CMB Gradients (White Arrows)
        # We skip pixels to make it readable
        skip = 4
        X, Y = np.meshgrid(np.linspace(-ZOOM_SIZE/2, ZOOM_SIZE/2, RES), np.linspace(-ZOOM_SIZE/2, ZOOM_SIZE/2, RES))
        
        ax.quiver(X[::skip, ::skip], Y[::skip, ::skip], 
                  gx[::skip, ::skip], gy[::skip, ::skip], 
                  color='white', alpha=0.6, scale=25, label='CMB Flow')
        
        # Overlay: The Stellar Key (Cyan Streamlines)
        # We overlay the key to see if it fits the flow
        ax.streamplot(np.linspace(-ZOOM_SIZE/2, ZOOM_SIZE/2, RES), 
                      np.linspace(-ZOOM_SIZE/2, ZOOM_SIZE/2, RES), 
                      key_u, key_v, color='cyan', density=0.8, linewidth=1.5, arrowsize=1.5)
        
        ax.set_title(f"#{node['rank']} {node['name']}\n(l={node['l']:.1f}, b={node['b']:.1f})", color='white', fontsize=10)
        ax.axis('off')

    # Add a legend/key in the 6th slot
    ax_leg = fig.add_subplot(2, 3, 6)
    ax_leg.axis('off')
    ax_leg.text(0.1, 0.7, "LEGEND", color='white', fontsize=14, fontweight='bold')
    ax_leg.text(0.1, 0.6, "Background: CMB Temp (Magma)", color='gray')
    ax_leg.text(0.1, 0.5, "→ White Arrows: CMB Gradient Flow", color='white')
    ax_leg.text(0.1, 0.4, "〰 Cyan Lines: Stellar Vortex Key", color='cyan')
    ax_leg.text(0.1, 0.2, "Match Condition:", color='white', fontweight='bold')
    ax_leg.text(0.1, 0.1, "White Arrows should align with Cyan Lines", color='gray')
    
    plt.tight_layout()
    plt.savefig("cmb_node_inspection.png")
    print("✅ Inspection Complete. Saved: cmb_node_inspection.png")

if __name__ == "__main__":
    main()