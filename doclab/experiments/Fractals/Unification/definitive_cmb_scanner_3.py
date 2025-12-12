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
LMAX = 60                   # Total Bandwidth to compute
N_RES = 250                 # Grid Resolution
FRAMES = 60                 # Animation Frames
K_RANGE = np.linspace(0.899999, 1.100001, FRAMES) # Twist Range (0 to 2 covers the k=0.5 case)
GIF_NAME = "cmb_decomposition_scanner.gif"

# ======================
# 1. DATA & DECOMPOSITION
# ======================
def get_alms_and_grid(fits_path, lmax, n_res):
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # High Res Grid for ALM Extraction
    n_theta_alm = lmax * 3
    n_phi_alm = lmax * 4
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
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    # Synthesis Grid
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    return alms, TH_GRID, PH_GRID

# ======================
# 2. FAST MODE BUILDERS
# ======================
def build_mode_map_single_L(alms, target_l, TH, PH):
    """ Compiles a Mode Map for a SINGLE L (e.g. L=10) """
    modes = {}
    l = target_l
    print(f"   -> Building Mode Map for L={l}...")
    for m in range(-l, l + 1):
        alm = alms.get((l, m), 0j)
        if alm == 0j: continue
        Y_lm = sph_harm(m, l, PH, TH)
        modes[m] = modes.get(m, np.zeros_like(TH, dtype=np.complex128)) + alm * Y_lm
    return modes

def build_mode_map_substrate(alms, lmax, exclude_range, TH, PH):
    """ Compiles a Mode Map for everything OUTSIDE exclude_range """
    modes = {}
    l_start, l_end = exclude_range
    print(f"   -> Building Substrate Mode Map (Excluding L{l_start}-{l_end})...")
    
    for l in range(lmax + 1):
        if l_start <= l <= l_end: continue # Skip the Skeleton
        
        for m in range(-l, l + 1):
            alm = alms.get((l, m), 0j)
            if alm == 0j: continue
            
            Y_lm = sph_harm(m, l, PH, TH)
            modes[m] = modes.get(m, np.zeros_like(TH, dtype=np.complex128)) + alm * Y_lm
    return modes

def synthesize_fast(modes, k, PH):
    """ Apply twist k to pre-computed modes """
    out = np.zeros_like(PH, dtype=np.complex128)
    twist_factor = k - 1.0
    for m, mode_data in modes.items():
        if twist_factor == 0:
            out += mode_data
        else:
            out += mode_data * np.exp(1j * m * twist_factor * PH)
    return out.real

# ======================
# 3. ANIMATION LOOP
# ======================
def run_decomposition_scanner():
    alms, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    
    print("[*] Pre-computing Component Maps...")
    modes_L10 = build_mode_map_single_L(alms, 10, TH, PH)
    modes_L20 = build_mode_map_single_L(alms, 20, TH, PH)
    modes_L30 = build_mode_map_single_L(alms, 30, TH, PH)
    modes_L40 = build_mode_map_single_L(alms, 40, TH, PH)
    modes_Sub = build_mode_map_substrate(alms, LMAX, (10, 40), TH, PH)
    
    print(f"[*] Starting Render ({FRAMES} frames)...")
    frames = []

    # Helper for Plotting
    def plot_panel(ax, data, title, cmap, contour=True):
        ax.imshow(data, origin='lower', extent=[-180,180,-90,90], cmap=cmap)
        if contour:
            # Subtle contours for the "Pure L" look
            ax.contour(data, levels=10, colors='black', alpha=0.3, linewidths=0.5, extent=[-180,180,-90,90], origin='lower')
        ax.set_title(title, fontsize=9, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])

    for i, k in enumerate(K_RANGE):
        if i % 5 == 0: sys.stdout.write(f"\r[>] Frame {i+1}/{FRAMES} (k={k:.3f})")
        
        # Synthesize
        m10 = synthesize_fast(modes_L10, k, PH)
        m20 = synthesize_fast(modes_L20, k, PH)
        m30 = synthesize_fast(modes_L30, k, PH)
        m40 = synthesize_fast(modes_L40, k, PH)
        mSub = synthesize_fast(modes_Sub, k, PH)
        
        # Manifold Magnitude (approximated by abs of complex reconstruction, 
        # but since synthesize returns real, we re-calculate full complex for mag if needed.
        # Here we approximate visual style with abs(real)**0.45 for contrast)
        mManifold = np.abs(mSub)**0.45

        # Plot
        fig = plt.figure(figsize=(16, 10))
        gs = gridspec.GridSpec(3, 2, wspace=0.05, hspace=0.2)
        
        plot_panel(plt.subplot(gs[0,0]), m10, f"Pure L=10 | k={k:.3f}", 'RdBu_r')
        plot_panel(plt.subplot(gs[0,1]), m20, f"Pure L=20 | k={k:.3f}", 'RdBu_r')
        plot_panel(plt.subplot(gs[1,0]), m30, f"Pure L=30 | k={k:.3f}", 'RdBu_r')
        plot_panel(plt.subplot(gs[1,1]), m40, f"Pure L=40 | k={k:.3f}", 'RdBu_r')
        plot_panel(plt.subplot(gs[2,0]), mSub, f"Substrate (L10-40 Removed) | k={k:.3f}", 'RdBu_r')
        
        # The Manifold view (Magnitude/Energy)
        ax_man = plt.subplot(gs[2,1])
        im_man = ax_man.imshow(mManifold, origin='lower', extent=[-180,180,-90,90], cmap='inferno')
        ax_man.set_title(f"Substrate Manifold (Energy) | k={k:.3f}", fontsize=9, fontweight='bold')
        ax_man.set_xticks([])
        ax_man.set_yticks([])
        
        fig.suptitle(f"CMB HARMONIC DECOMPOSITION SCANNER", fontsize=16, y=0.95)
        
        fname = f"_decomp_{i:03d}.png"
        plt.savefig(fname, dpi=80, bbox_inches='tight')
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames.append(img.copy())
        os.remove(fname)

    print(f"\n[*] Saving GIF: {GIF_NAME}")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=80, loop=0)
    print("✅ Done.")

if __name__ == "__main__":
    run_decomposition_scanner()