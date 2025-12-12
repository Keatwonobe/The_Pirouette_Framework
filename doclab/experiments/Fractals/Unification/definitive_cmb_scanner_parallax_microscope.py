import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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
N_RES = 300                 # Higher res for filament detail
FRAMES = 80                 # Smooth animation
L_MIN = 25                  # Bottom of scan range (The "Background")
L_MAX = 55                  # Top of scan range (The "Fibrous Details")

# PARALLAX SETTINGS
K_START = 0.899999
K_END = 1.100002
PARALLAX_FACTOR = 0.15      # How much faster High-L rotates vs Low-L (Creates depth)
GIF_NAME = "cmb_filament_parallax.gif"

# ======================
# 1. DATA INGESTION
# ======================
def get_alms_and_grid(fits_path, l_max_scan, n_res):
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    # Handle various FITS column names
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # High Res Extraction Grid
    # We only need up to L_MAX for the ALM calculation
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
    # Only compute up to L_MAX, we don't need the rest
    for l in range(l_max_scan + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    # Synthesis Grid
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    return alms, TH_GRID, PH_GRID

# ======================
# 2. COMPONENT BUILDER
# ======================
def precompute_modes_range(alms, l_min, l_max, TH, PH):
    """ 
    Pre-computes spherical harmonics for the range.
    Returns a dictionary structured by L: { l: { m: grid } }
    This allows us to apply twist individually per L.
    """
    print(f"[*] Pre-computing modes for L={l_min} to {l_max}...")
    modes_by_l = {}
    
    for l in range(l_min, l_max + 1):
        modes_by_l[l] = {}
        for m in range(-l, l + 1):
            alm = alms.get((l, m), 0j)
            if alm == 0j: continue
            
            # Compute base harmonic
            Y_lm = sph_harm(m, l, PH, TH)
            modes_by_l[l][m] = alm * Y_lm
            
    return modes_by_l

def synthesize_parallax_scan(modes_by_l, k_base, center_l_focus, focus_width, PH):
    """ 
    Applies Differential Twist (Parallax) and Gaussian Frequency Focus 
    """
    total_field = np.zeros_like(PH, dtype=np.complex128)
    
    # Iterate through all pre-computed L layers
    for l, m_dict in modes_by_l.items():
        
        # 1. TOMOGRAPHY (Focus Weight)
        # Gaussian window centered on 'center_l_focus'
        # This fades layers in and out as we scan depth
        weight = np.exp(-0.5 * ((l - center_l_focus) / focus_width) ** 2)
        if weight < 0.01: continue 

        # 2. PARALLAX (Differential Twist)
        # Higher L twists slightly more than Lower L
        # This separates the "fibers" (High L) from the "bulk" (Low L)
        # Parallax Factor determines the "distance" between layers
        l_norm = (l - L_MIN) / (L_MAX - L_MIN)
        local_k = k_base + (PARALLAX_FACTOR * l_norm * (k_base - 1.0))
        
        twist_factor = local_k - 1.0

        layer_sum = np.zeros_like(PH, dtype=np.complex128)
        for m, mode_data in m_dict.items():
            if twist_factor == 0:
                layer_sum += mode_data
            else:
                # Apply phase shift
                layer_sum += mode_data * np.exp(1j * m * twist_factor * PH)
        
        total_field += layer_sum * weight

    return total_field.real

# ======================
# 3. RENDER LOOP
# ======================
def run_filament_scanner():
    alms, TH, PH = get_alms_and_grid(FITS_PATH, L_MAX, N_RES)
    
    # Pre-compute ONLY the region of interest (L25-55)
    modes_data = precompute_modes_range(alms, L_MIN, L_MAX, TH, PH)

    print(f"[*] Starting Parallax Scan Render ({FRAMES} frames)...")
    frames = []

    # Animation Vectors
    # Twist oscillates
    k_vals = np.concatenate([
        np.linspace(K_START, K_END, FRAMES // 2),
        np.linspace(K_END, K_START, FRAMES // 2)
    ])
    
    # Focus scans from L=30 (Blobs) to L=45 (Fibers) and back
    focus_vals = np.concatenate([
        np.linspace(30, 48, FRAMES // 2),
        np.linspace(48, 30, FRAMES // 2)
    ])

    for i in range(FRAMES):
        k = k_vals[i]
        foc = focus_vals[i]
        
        if i % 5 == 0: 
            sys.stdout.write(f"\r[>] Frame {i+1}/{FRAMES} | Twist={k:.3f} | Focus_L={foc:.1f}")

        # 1. Synthesize the "Focused" View (Scanning)
        # Width=4 means we see a slice roughly 8-L wide
        scan_map = synthesize_parallax_scan(modes_data, k, foc, 4.0, PH)

        # 2. Synthesize the "Deep Composite" View (All layers, but with parallax)
        # Width=100 means we see everything at once
        full_map = synthesize_parallax_scan(modes_data, k, 40, 100.0, PH)
        
        # Edge Detection / Gradient for the "Fibers"
        # Simple gradient magnitude to highlight the "strings"
        gy, gx = np.gradient(scan_map)
        gradient_mag = np.sqrt(gx**2 + gy**2)

        # PLOTTING
        fig = plt.figure(figsize=(12, 12))
        gs = gridspec.GridSpec(2, 2, height_ratios=[1.5, 1], hspace=0.15, wspace=0.1)

        # Main View: The Full Parallax Composite
        ax_main = plt.subplot(gs[0, :])
        im_main = ax_main.imshow(full_map, origin='lower', cmap='twilight_shifted', extent=[-180,180,-90,90])
        ax_main.set_title(f"PARALLAX COMPOSITE | Twist k={k:.3f} (Differential Phase)", fontsize=10, fontweight='bold', color='white', backgroundcolor='black')
        ax_main.contour(full_map, levels=12, colors='white', alpha=0.15, linewidths=0.5, origin='lower', extent=[-180,180,-90,90])
        ax_main.axis('off')

        # Sub View 1: The Tomographic Focus Scan
        ax_scan = plt.subplot(gs[1, 0])
        ax_scan.imshow(scan_map, origin='lower', cmap='RdBu_r', extent=[-180,180,-90,90])
        ax_scan.set_title(f"TOMOGRAPHIC SLICE | Center L={foc:.1f}", fontsize=9, fontweight='bold')
        ax_scan.axis('off')

        # Sub View 2: The "Filament" Detector (Gradient)
        ax_fil = plt.subplot(gs[1, 1])
        # Amplify the gradient for visibility
        ax_fil.imshow(gradient_mag, origin='lower', cmap='inferno', vmin=0, vmax=np.percentile(gradient_mag, 98), extent=[-180,180,-90,90])
        ax_fil.set_title("FILAMENT STRUCTURE (Gradient)", fontsize=9, fontweight='bold')
        ax_fil.axis('off')

        fig.suptitle(f"CMB FRACTAL TOMOGRAPHY\nL-Range [{L_MIN}-{L_MAX}]", fontsize=14, y=0.96)
        
        fname = f"_filscan_{i:03d}.png"
        plt.savefig(fname, dpi=90, bbox_inches='tight')
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames.append(img.copy())
        os.remove(fname)

    print(f"\n[*] Saving GIF: {GIF_NAME}")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=60, loop=0)
    print("✅ Done.")

if __name__ == "__main__":
    run_filament_scanner()