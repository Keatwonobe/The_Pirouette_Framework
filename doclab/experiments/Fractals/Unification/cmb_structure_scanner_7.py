import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord
from PIL import Image
import os
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
L_MIN = 20
L_MAX = 60
FRAMES = 60

# ZOOM WINDOW (The Microscope Target)
# Looking at a dense region near the galactic plane
LAT_MIN, LAT_MAX = -30, 30
LON_MIN, LON_MAX = 20, 80
N_RES = 512                 # 512x512 pixels for just this window

# MOTION SETTINGS
K_START = 0.9
K_END = 1.1
FOCUS_START = 30            # Start at "Blob" scale
FOCUS_END = 55              # End at "Filament" scale
PARALLAX_FACTOR = 0.2       # Exaggerated depth for the microscope

GIF_NAME = "cmb_triangular_microscope.gif"

# ======================
# 1. LOCALIZED ENGINE
# ======================

def get_alms_and_local_grid(fits_path, l_max_scan, lat_bounds, lon_bounds, n_res):
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

    # ALM Extraction Grid (Global)
    n_theta_alm = l_max_scan * 3
    n_phi_alm = l_max_scan * 4
    t_alm = np.linspace(0, np.pi, n_theta_alm)
    p_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')

    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    print("[*] Extracting ALMs...")
    alms = {}
    for l in range(l_max_scan + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    # SYNTHESIS GRID (LOCAL ZOOM)
    print(f"[*] Generating Microscope Grid ({lat_bounds} deg lat, {lon_bounds} deg lon)...")
    
    # Convert deg to rad for synthesis
    # Latitude: 90 is 0 rad, -90 is pi rad
    theta_min = np.deg2rad(90 - lat_bounds[1])
    theta_max = np.deg2rad(90 - lat_bounds[0])
    
    # Longitude: -180 to 180 is -pi to pi
    # We need to handle wrapping if bounds cross 180, but let's assume simple crop first
    phi_min = np.deg2rad(lon_bounds[0])
    phi_max = np.deg2rad(lon_bounds[1])
    
    theta_vec = np.linspace(theta_min, theta_max, n_res)
    phi_vec = np.linspace(phi_min, phi_max, n_res)
    
    TH_ZOOM, PH_ZOOM = np.meshgrid(theta_vec, phi_vec, indexing='ij')
    
    return alms, TH_ZOOM, PH_ZOOM

def precompute_zoom_modes(alms, l_min, l_max, TH, PH):
    print(f"[*] Pre-computing Local Harmonics for L={l_min}-{l_max}...")
    modes_by_l = {}
    for l in range(l_min, l_max + 1):
        modes_by_l[l] = {}
        for m in range(-l, l + 1):
            if (l,m) not in alms: continue
            # Compute Y_lm only on the zoom patch
            modes_by_l[l][m] = alms[(l,m)] * sph_harm(m, l, PH, TH)
    return modes_by_l

def synthesize_microscope(modes_by_l, k_base, center_l, PH):
    total_field = np.zeros_like(PH, dtype=np.complex128)
    
    # Wide focus for the "Tunnel" effect
    focus_width = 8.0 
    
    for l, m_dict in modes_by_l.items():
        # Focus Weight
        weight = np.exp(-0.5 * ((l - center_l) / focus_width) ** 2)
        if weight < 0.05: continue 

        # Parallax Twist
        l_norm = (l - L_MIN) / (L_MAX - L_MIN)
        local_k = k_base + (PARALLAX_FACTOR * l_norm * (k_base - 1.0))
        twist_factor = local_k - 1.0

        layer_sum = np.zeros_like(PH, dtype=np.complex128)
        for m, mode_data in m_dict.items():
            if twist_factor == 0:
                layer_sum += mode_data
            else:
                layer_sum += mode_data * np.exp(1j * m * twist_factor * PH)
        
        total_field += layer_sum * weight

    return total_field.real

# ======================
# 2. RENDER LOOP
# ======================
def run_microscope():
    alms, TH, PH = get_alms_and_local_grid(FITS_PATH, L_MAX, (LAT_MIN, LAT_MAX), (LON_MIN, LON_MAX), N_RES)
    modes_data = precompute_zoom_modes(alms, L_MIN, L_MAX, TH, PH)
    
    frames = []
    
    # Motion Vectors: "Rushing Away"
    # We sweep K and Focus together to simulate movement Z-axis
    k_vals = np.concatenate([np.linspace(K_START, K_END, FRAMES//2), np.linspace(K_END, K_START, FRAMES//2)])
    f_vals = np.concatenate([np.linspace(FOCUS_START, FOCUS_END, FRAMES//2), np.linspace(FOCUS_END, FOCUS_START, FRAMES//2)])
    
    print(f"[*] Rendering Microscope View...")
    
    for i in range(FRAMES):
        k = k_vals[i]
        foc = f_vals[i]
        
        sys.stdout.write(f"\r[>] Frame {i+1}/{FRAMES} | Twist={k:.3f} | Depth L={foc:.1f}")
        sys.stdout.flush()
        
        # 1. Synthesize
        img = synthesize_microscope(modes_data, k, foc, PH)
        
        # 2. Add "Flow" Lines (Gradient)
        gy, gx = np.gradient(img)
        flow = np.sqrt(gx**2 + gy**2)
        
        # 3. Plot
        fig = plt.figure(figsize=(10, 10), facecolor='black')
        ax = plt.gca()
        
        # Composite: Structure + Flow
        # Use a diverging map to see the "Triangles" forming
        im = ax.imshow(img, origin='lower', cmap='twilight_shifted', extent=[LON_MIN, LON_MAX, LAT_MIN, LAT_MAX])
        
        # Overlay subtle flow lines to emphasize motion
        ax.contour(flow, levels=8, colors='white', alpha=0.2, linewidths=0.5, origin='lower', extent=[LON_MIN, LON_MAX, LAT_MIN, LAT_MAX])
        
        ax.set_title(f"CMB MICROSCOPE: Galactic Sector [{LON_MIN}:{LON_MAX}, {LAT_MIN}:{LAT_MAX}]\nTwist k={k:.3f} | Focus Depth L={foc:.1f}", 
                     color='white', fontsize=12)
        ax.axis('off')
        
        fname = f"_micro_{i:03d}.png"
        plt.savefig(fname, dpi=80, bbox_inches='tight', facecolor='black')
        plt.close(fig)
        
        with Image.open(fname) as pim:
            frames.append(pim.copy())
        os.remove(fname)

    print(f"\n[*] Saving GIF: {GIF_NAME}")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=50, loop=0)
    print("✅ Microscope Scan Complete.")

if __name__ == "__main__":
    run_microscope()