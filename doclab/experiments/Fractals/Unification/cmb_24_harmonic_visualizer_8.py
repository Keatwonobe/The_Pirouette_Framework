import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.special import sph_harm
from PIL import Image
import os
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 100                 # Mesh resolution (lower for smooth 3D plot)
K_REALITY = 1.0
GIF_NAME = "cmb_particle_portrait.gif"
FRAMES = 60

# Physics Parameters from previous findings
HEADING_L = 51.8
HEADING_B = -72.9
BOW_SHOCK_ANGLE = 60.0      # Degrees

# ======================
# 1. ENGINE
# ======================

def get_alms_and_grid(fits_path, lmax, n_res):
    print(f"[*] Loading CMB Data...")
    try:
        data = fits.getdata(fits_path)
        if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else: cmb = data.astype(np.float64)
        cmb[np.isnan(cmb)] = np.nanmean(cmb)
    except:
        # Fallback for offline testing
        cmb = np.random.randn(12*512**2)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    n_theta = lmax * 3; n_phi = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta)
    p_alm = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')
    
    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            try:
                Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            except: # Scipy < 1.15 fallback
                from scipy.special import sph_harm as sh
                Y_lm = sh(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    # Mesh Grid for 3D Plot
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, TH_GRID, PH_GRID

def synthesize_fields(alms, TH, PH):
    # 1. Structure (for Deformation)
    field = np.zeros_like(TH, dtype=np.complex128)
    for l in range(LMAX + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            try: Y_lm = sph_harm(m, l, PH, TH)
            except: from scipy.special import sph_harm as sh; Y_lm = sh(m, l, PH, TH)
            field += alms[(l, m)] * Y_lm
            
    # Gradient Energy (Chaos)
    gy, gx = np.gradient(field.real)
    chaos = np.sqrt(gx**2 + gy**2)
    
    # Structure (Raw Field)
    structure = field.real
    
    return structure, chaos

# ======================
# 2. 3D BUILDER
# ======================

def run_particle_portrait():
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    
    alms, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    structure, chaos = synthesize_fields(alms, TH, PH)
    
    # Normalize for 3D mapping
    s_norm = (structure - structure.min()) / (structure.max() - structure.min())
    c_norm = (chaos - chaos.min()) / (chaos.max() - chaos.min())
    
    # 1. Deform the Sphere
    # Radius = Base + Amplitude * Structure
    R_BASE = 1.0
    R_AMP = 0.3
    R = R_BASE + R_AMP * s_norm
    
    # Convert to Cartesian
    # Note: TH is 0..pi (Colatitude), PH is -pi..pi
    # We want standard physics convention
    x = R * np.sin(TH) * np.cos(PH)
    y = R * np.sin(TH) * np.sin(PH)
    z = R * np.cos(TH)
    
    # 2. Motion Vector (Heading)
    # Convert Galactic (l, b) to Cartesian direction
    # heading_b is latitude, so theta = 90 - b
    th_h = np.deg2rad(90 - HEADING_B)
    ph_h = np.deg2rad(HEADING_L)
    
    vx = np.sin(th_h) * np.cos(ph_h) * 2.5 # Length of arrow
    vy = np.sin(th_h) * np.sin(ph_h) * 2.5
    vz = np.cos(th_h) * 2.5
    
    print(f"[*] Rendering 3D Particle Portrait...")
    frames = []
    
    # Rotation Loop
    angles = np.linspace(0, 360, FRAMES, endpoint=False)
    
    for i, angle in enumerate(angles):
        sys.stdout.write(f"\r[>] Frame {i+1}/{FRAMES}")
        sys.stdout.flush()
        
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('black')
        
        # Plot Surface
        # Color by Chaos (Red=High Friction, Blue=Low Friction)
        surf = ax.plot_surface(x, y, z, facecolors=plt.cm.inferno(c_norm), 
                               rstride=1, cstride=1, shade=True, alpha=0.9, antialiased=True)
        
        # Plot Motion Arrow (The "Spine")
        ax.quiver(0, 0, 0, vx, vy, vz, color='cyan', linewidth=3, arrow_length_ratio=0.1)
        
        # Plot Bow Shock Ring (Approximate)
        # It's a circle perpendicular to V at distance R
        # Simplified: Just a wireframe sphere to show the "Ideal" shape vs "Real" shape
        # ax.plot_wireframe(np.sin(TH)*np.cos(PH), np.sin(TH)*np.sin(PH), np.cos(TH), 
        #                   color='gray', alpha=0.1, linewidth=0.5)

        # Labels
        ax.text(vx, vy, vz, "  Motion Vector", color='cyan', fontsize=12)
        
        # Camera
        ax.view_init(elev=20, azim=angle)
        ax.set_axis_off()
        ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_zlim(-1.5, 1.5)
        ax.set_title("THE UNIVERSE PARTICLE\n(Structure Deformation + Chaos Skin)", color='white', fontsize=16)
        
        fname = f"_part_{i:03d}.png"
        plt.savefig(fname, dpi=80, bbox_inches='tight', facecolor='black')
        plt.close(fig)
        
        with Image.open(fname) as pim:
            frames.append(pim.copy())
        os.remove(fname)

    print(f"\n[*] Saving GIF: {GIF_NAME}")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=60, loop=0)
    print("✅ Portrait Complete.")

if __name__ == "__main__":
    run_particle_portrait()