import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.ndimage import sobel, gaussian_filter
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 512
HEADING_L = 51.8
HEADING_B = -72.9

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
    except FileNotFoundError:
        print("[!] File not found.")
        sys.exit(1)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    n_theta_alm = lmax * 3; n_phi_alm = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta_alm)
    p_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
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
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, TH_GRID, PH_GRID

def synthesize_structure(alms, TH, PH):
    field = np.zeros_like(TH, dtype=np.complex128)
    for l in range(LMAX + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            Y_lm = sph_harm(m, l, PH, TH)
            field += alms[(l, m)] * Y_lm
            
    gy, gx = np.gradient(field.real)
    return np.sqrt(gx**2 + gy**2)

def rotate_to_heading(structure_map, heading_l, heading_b):
    n_res = structure_map.shape[0]
    theta_t = np.linspace(0, np.pi, n_res)
    phi_t = np.linspace(-np.pi, np.pi, n_res)
    TH_T, PH_T = np.meshgrid(theta_t, phi_t, indexing='ij')
    
    x_t = np.sin(TH_T) * np.cos(PH_T)
    y_t = np.sin(TH_T) * np.sin(PH_T)
    z_t = np.cos(TH_T)
    
    th_h = np.deg2rad(90 - heading_b)
    ph_h = np.deg2rad(heading_l)
    
    hx = np.sin(th_h) * np.cos(ph_h)
    hy = np.sin(th_h) * np.sin(ph_h)
    hz = np.cos(th_h)
    
    z_new = np.array([hx, hy, hz])
    x_new = np.cross(np.array([0,1,0]), z_new)
    if np.linalg.norm(x_new) < 0.01: x_new = np.array([1,0,0]) 
    x_new /= np.linalg.norm(x_new)
    y_new = np.cross(z_new, x_new)
    
    R = np.column_stack((x_new, y_new, z_new))
    P_target = np.vstack((x_t.flatten(), y_t.flatten(), z_t.flatten()))
    P_orig = R @ P_target
    
    x_o, y_o, z_o = P_orig
    theta_o = np.arccos(np.clip(z_o, -1, 1))
    phi_o = np.arctan2(y_o, x_o)
    
    r_idx = (theta_o / np.pi) * (n_res - 1)
    c_idx = ((phi_o + np.pi) / (2*np.pi)) * (n_res - 1)
    r_idx = np.clip(np.round(r_idx), 0, n_res-1).astype(int)
    c_idx = np.clip(np.round(c_idx), 0, n_res-1).astype(int)
    
    return structure_map[r_idx, c_idx].reshape(n_res, n_res)

# ======================
# 2. HULL DETECTOR
# ======================

def detect_hull_boundary(rotated_map):
    print(f"[*] Mapping the Hull Boundary...")
    
    # Smooth slightly to remove noise
    smooth = gaussian_filter(rotated_map, sigma=2)
    
    # Calculate "Turbulence Gradient"
    # We want to find where the Chaos Intensity jumps the fastest
    # This is the derivative of the structure map itself
    grad_y = sobel(smooth, axis=0) # Gradient along latitude (North-South)
    
    # We are looking for positive gradients (Low -> High)
    # The "Wall" is the ring of max gradient
    wall_map = np.clip(grad_y, 0, None)
    
    return wall_map

# ======================
# 3. MAIN
# ======================

def run_hull_mapper():
    alms, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    structure = synthesize_structure(alms, TH, PH)
    
    # Normalize
    structure = (structure - structure.min()) / (structure.max() - structure.min())
    
    # Rotate to Nose-Up
    hull_view = rotate_to_heading(structure, HEADING_L, HEADING_B)
    
    # Detect the Wall
    boundary_layer = detect_hull_boundary(hull_view)
    
    # --- PLOTTING ---
    fig = plt.figure(figsize=(10, 12), facecolor='#050505')
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    
    # 1. The Hull Skin (Unwrapped)
    ax_map = plt.subplot(gs[0])
    
    # Composite: Blue=Laminar Nose, Red=Turbulent Body, White=The Wall
    # We create a custom RGB image
    h, w = hull_view.shape
    rgb = np.zeros((h, w, 3))
    
    # Laminar Zone (Top) - Blueish
    rgb[:, :, 2] = np.clip(1.0 - hull_view, 0, 1) * 0.8
    # Turbulent Zone - Reddish/Chaos
    rgb[:, :, 0] = hull_view
    
    # The Wall - White Hot
    wall_norm = (boundary_layer - boundary_layer.min()) / (boundary_layer.max() - boundary_layer.min())
    mask = wall_norm > 0.4 # Threshold for the wall
    rgb[mask] = [1, 1, 1] # White lines
    
    ax_map.imshow(rgb, extent=[-180, 180, 180, 0], aspect='auto')
    
    # Overlay the 60-degree marker
    ax_map.axhline(60, color='yellow', linestyle='--', linewidth=1, label='60° Theoretical Boundary')
    
    ax_map.set_title("THE COSMIC HULL | Boundary Layer Separation", color='white', fontsize=14)
    ax_map.set_ylabel("Degrees from Nose", color='gray')
    ax_map.set_xlabel("Azimuth (Spin Angle)", color='gray')
    ax_map.legend(loc='upper right')
    
    # 2. The Polar Projection (Looking down the Nose)
    ax_polar = plt.subplot(gs[1], projection='polar')
    ax_polar.set_facecolor('#000000')
    
    # Project the "Wall Map" into polar
    # Radius = Angle from Nose (0 to 90 degrees only, to zoom in on the cap)
    # Theta = Azimuth
    
    # Extract the top 90 degrees
    cap_map = boundary_layer[:N_RES//2, :]
    
    # Create polar grid
    r = np.linspace(0, 90, N_RES//2)
    t = np.linspace(0, 2*np.pi, N_RES)
    R, T = np.meshgrid(r, t, indexing='ij')
    
    # Plot
    # We transpose cap_map to match meshgrid (R, T)
    ax_polar.pcolormesh(T, R, cap_map, cmap='inferno', shading='auto')
    
    ax_polar.set_title("NOSE CONE GEOMETRY (Polar View)", color='white', fontsize=10, pad=20)
    ax_polar.grid(color='#333', linestyle=':')
    ax_polar.set_yticks([30, 60, 90])
    ax_polar.set_yticklabels(['30°', '60°', '90°'], color='gray')
    ax_polar.tick_params(axis='x', colors='gray')
    
    plt.tight_layout()
    plt.savefig("cmb_hull_mapper.png", dpi=120, facecolor='#050505')
    print("✅ Hull Mapped. Saved to cmb_hull_mapper.png")

if __name__ == "__main__":
    run_hull_mapper()