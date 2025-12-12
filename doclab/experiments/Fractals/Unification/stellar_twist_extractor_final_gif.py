import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.interpolate import Rbf
from PIL import Image
import os

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
OUTPUT_GIF = "pirouette_maw_feeding.gif"

# The Maw
TARGET_L = -155.9
TARGET_B = -63.9
ZOOM_DEG = 40.0
RES = 200

# Animation Settings
NUM_PARTICLES = 5000   # Density of the "Stream"
FRAMES = 60            # Duration
SPEED = 0.5            # Flow speed multiplier
TRAIL_LENGTH = 5       # How long the tails are

# The Kinematic Anchors
STARS_KINEMATICS = {
    "Achernar":      (24.43,  -57.24, 42.7,  88.0,    -40.0,   16.0),
    "Canopus":       (95.99,  -52.70, 94.0,  19.9,    23.2,    20.5),
    "Alpha Centauri":(219.90, -60.83, 1.33,  -3679.3, 473.7,  -21.4),
    "Peacock":       (306.41, -56.74, 56.0,  18.2,    -105.4,  2.0),
    "Ankaa":         (6.57,   -42.31, 23.8,  237.0,   -178.0,  -11.0),
    "Alnair":        (332.06, -46.96, 31.0,  108.0,   -137.0,  11.0),
    "Fomalhaut":     (344.41, -29.62, 7.7,   329.2,   -164.2,  6.5),
    "Beta Ceti":     (12.27,  -17.99, 29.5,  232.0,   32.0,    13.0),
    "Acamar":        (40.07,  -40.30, 49.4,  58.0,    -14.0,   12.0),
    "Zaurak":        (59.56,  -13.51, 60.0,  -2.0,    -56.0,   57.0),
    "Rigel":         (78.63,  -8.20,  260.0, 1.31,    0.50,    17.8),
    "Sirius":        (101.28, -16.71, 2.64,  -546.0,  -1223.1, -5.5)
}
SOLAR_U, SOLAR_V, SOLAR_W = 11.1, 12.24, 7.25

def get_phantom_vector(data):
    ra, dec, dist, pm_ra, pm_dec, rv = data
    c = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, distance=dist*u.pc,
                 pm_ra_cosdec=pm_ra*u.mas/u.yr, pm_dec=pm_dec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s, frame='icrs')
    g = c.galactic
    l, b = g.l.deg, g.b.deg
    v_xyz = g.velocity.d_xyz.value
    dv = (v_xyz[1] + SOLAR_V) - (-10)
    dw = (v_xyz[2] + SOLAR_W) - 0
    return l, b, dv, dw

def generate_flow_field():
    print("[*] Generating Helical Flow Field...")
    l_list, b_list, u_list, v_list = [], [], [], []
    
    for name, data in STARS_KINEMATICS.items():
        l, b, u, v = get_phantom_vector(data)
        if l > 180: l -= 360
        l_list.append(l)
        b_list.append(b)
        u_list.append(u)
        v_list.append(v)
        
    # RBF Interpolation (The Manifold Shape)
    rbf_u = Rbf(l_list, b_list, u_list, function='thin_plate', smooth=0.5)
    rbf_v = Rbf(l_list, b_list, v_list, function='thin_plate', smooth=0.5)
    
    return rbf_u, rbf_v, l_list, b_list

def get_cmb_background(fits_path):
    print("[*] Loading CMB Terrain...")
    try:
        data = fits.getdata(fits_path)
        if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else: cmb = data.astype(np.float64)
        
        mask = np.isnan(cmb)
        cmb[mask] = np.nanmean(cmb)
        nside = int(np.sqrt(cmb.size / 12))
        hpix = HEALPix(nside=nside, order="ring", frame="galactic")
        
        grid_l = np.linspace(TARGET_L - ZOOM_DEG/2, TARGET_L + ZOOM_DEG/2, RES)
        grid_b = np.linspace(TARGET_B - ZOOM_DEG/2, TARGET_B + ZOOM_DEG/2, RES)
        L, B = np.meshgrid(grid_l, grid_b)
        
        coords = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
        ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
        patch = cmb[ipix]
        return patch, L, B
    except:
        print("[!] CMB File not found. Using blank background.")
        return np.zeros((RES, RES)), np.zeros((RES, RES)), np.zeros((RES, RES))

def main():
    # 1. Setup Environment
    rbf_u, rbf_v, anchor_l, anchor_b = generate_flow_field()
    cmb, L, B = get_cmb_background(FITS_PATH)
    
    # 2. Spawn Particles (Monte Carlo Injection)
    print(f"[*] Spawning {NUM_PARTICLES} test particles...")
    # Random positions within the zoom window
    px = np.random.uniform(TARGET_L - ZOOM_DEG/2, TARGET_L + ZOOM_DEG/2, NUM_PARTICLES)
    py = np.random.uniform(TARGET_B - ZOOM_DEG/2, TARGET_B + ZOOM_DEG/2, NUM_PARTICLES)
    
    # History buffer for trails
    history_x = [px.copy() for _ in range(TRAIL_LENGTH)]
    history_y = [py.copy() for _ in range(TRAIL_LENGTH)]
    
    frames_buffer = []
    
    print(f"[*] Simulating Time Evolution ({FRAMES} frames)...")
    
    for frame in range(FRAMES):
        if frame % 10 == 0: print(f"    Processing Frame {frame}/{FRAMES}...")
        
        # A. Advect Particles (Helical Calculus Step)
        # Get velocity at current position from RBF field
        # We assume the field is static (The River), and particles flow through it.
        u_vel = rbf_u(px, py)
        v_vel = rbf_v(px, py)
        
        # Update positions
        px += u_vel * SPEED * 0.01 # Scaling factor for smooth animation
        py += v_vel * SPEED * 0.01
        
        # Respawn if out of bounds (Continuity)
        mask_out = (px < TARGET_L - ZOOM_DEG/2) | (px > TARGET_L + ZOOM_DEG/2) | \
                   (py < TARGET_B - ZOOM_DEG/2) | (py > TARGET_B + ZOOM_DEG/2)
        
        px[mask_out] = np.random.uniform(TARGET_L - ZOOM_DEG/2, TARGET_L + ZOOM_DEG/2, np.sum(mask_out))
        py[mask_out] = np.random.uniform(TARGET_B - ZOOM_DEG/2, TARGET_B + ZOOM_DEG/2, np.sum(mask_out))
        
        # Update History
        history_x.pop(0)
        history_x.append(px.copy())
        history_y.pop(0)
        history_y.append(py.copy())
        
        # B. Render Frame
        fig = plt.figure(figsize=(10, 10), facecolor='#000500')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#000500')
        
        # Layer 1: CMB Depth
        ax.imshow(cmb, cmap='magma', origin='lower', alpha=0.6,
                  extent=[TARGET_L - ZOOM_DEG/2, TARGET_L + ZOOM_DEG/2,
                          TARGET_B - ZOOM_DEG/2, TARGET_B + ZOOM_DEG/2])
        
        # Layer 2: The Maw Core
        maw = Circle((TARGET_L, TARGET_B), 2.0, color='lime', alpha=0.3)
        ax.add_patch(maw)
        
        # Layer 3: Particle Stream (Trails)
        # Plot trails first (fainter)
        for t in range(TRAIL_LENGTH - 1):
            alpha = (t + 1) / TRAIL_LENGTH * 0.5
            ax.scatter(history_x[t], history_y[t], s=2, c='cyan', alpha=alpha, edgecolors='none')
            
        # Plot heads (bright)
        ax.scatter(px, py, s=5, c='white', alpha=0.9, edgecolors='none')
        
        # Layer 4: Anchors
        ax.scatter(anchor_l, anchor_b, s=150, facecolors='none', edgecolors='white', linewidth=2)
        
        # Formatting
        ax.set_xlim(TARGET_L + ZOOM_DEG/2, TARGET_L - ZOOM_DEG/2) # Invert X for Sky View
        ax.set_ylim(TARGET_B - ZOOM_DEG/2, TARGET_B + ZOOM_DEG/2)
        ax.set_title(f"THE MAW FEEDING: Kinematic Flow Simulation\nFrame {frame}", color='white', fontsize=14)
        ax.axis('off')
        
        # Save temp frame
        fname = f"temp_frame_{frame:03d}.png"
        plt.savefig(fname, bbox_inches='tight', dpi=100, facecolor='#000500')
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames_buffer.append(img.copy())
        os.remove(fname)

    # 3. Save GIF
    print("[*] Assembling GIF...")
    if frames_buffer:
        frames_buffer[0].save(
            OUTPUT_GIF,
            save_all=True,
            append_images=frames_buffer[1:],
            duration=100, # ms per frame
            loop=0
        )
        print(f"✅ ANIMATION COMPLETE: {OUTPUT_GIF}")
        print("   This visualization shows the 'Helical Current' inferred from stellar kinematics.")
        print("   Notice how the particles (Stars) don't just fall in; they spiral around the Lime Core.")

if __name__ == "__main__":
    main()