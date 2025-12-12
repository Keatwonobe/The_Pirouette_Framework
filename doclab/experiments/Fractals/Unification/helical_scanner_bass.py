import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm, sph_harm_y
import astropy.units as u
from astropy.coordinates import SkyCoord
from PIL import Image
import os
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
TARGET_L = 40              # The "Skeleton" Harmonic
N_RES = 300                # Resolution for visualization
FRAMES = 60                # Number of animation frames
K_START = 0.5
K_END = 1.5
GIF_NAME = "cmb_skeleton_dna_l40.gif"

# ======================
# UTILITIES
# ======================
def get_ylm(m, l, phi, theta):
    try:
        return sph_harm_y(l, m, phi, theta)
    except AttributeError:
        return sph_harm(m, l, phi, theta)

def extract_specific_mode(fits_path, target_l):
    """
    Extracts ONLY the alms for a specific L mode.
    All other L modes are ignored.
    """
    print(f"[*] Loading CMB and extracting ONLY L={target_l}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)
    
    # Infill
    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # Integration grid
    n_theta = target_l * 4
    n_phi = target_l * 8
    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')

    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]

    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]
    weights = np.sin(TH) * dtheta * dphi

    alms = {}
    # We only care about L = target_l
    l = target_l
    for m in range(-l, l + 1):
        Y_lm = get_ylm(m, l, PH, TH)
        val = np.sum(T_sample * np.conjugate(Y_lm) * weights)
        alms[(l, m)] = val
        
    return alms

def synthesize_skeleton(alms, target_l, n_res, k):
    """
    Synthesizes the twisted skeleton map.
    """
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    
    map_out = np.zeros_like(TH, dtype=np.complex128)
    
    l = target_l
    for m in range(-l, l + 1):
        if (l, m) not in alms: continue
        
        Y_lm = get_ylm(m, l, PH, TH)
        
        # The DNA Twist Phase
        twist_phase = np.exp(1j * m * (k - 1.0) * PH)
        
        map_out += alms[(l, m)] * Y_lm * twist_phase
            
    return map_out.real

# ======================
# MAIN
# ======================
def main():
    # 1. Get the Skeleton DNA
    skeleton_alms = extract_specific_mode(FITS_PATH, TARGET_L)
    
    # 2. Animate the Twist
    print(f"[*] Generating Skeleton Twist Animation (k={K_START} to {K_END})...")
    
    frames = []
    k_values = np.linspace(K_START, K_END, FRAMES)
    
    for i, k in enumerate(k_values):
        sys.stdout.write(f"\r[>] Rendering Frame {i+1}/{FRAMES} (k={k:.3f})")
        sys.stdout.flush()
        
        # Synthesize
        img = synthesize_skeleton(skeleton_alms, TARGET_L, N_RES, k)
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Heatmap
        im = ax.imshow(img.T, cmap='RdBu_r', extent=[-180, 180, -90, 90], origin='lower')
        
        # The "Bones" - Nodal Lines (Zero Crossings)
        # These show the topology clearly
        ax.contour(img.T, levels=[0], colors='black', linewidths=2.5, extent=[-180, 180, -90, 90], origin='lower')
        
        ax.set_title(f"Universal Skeleton (L={TARGET_L}) | Twist k={k:.3f}", fontsize=14)
        ax.set_xlabel("Galactic Longitude")
        ax.set_ylabel("Galactic Latitude")
        
        if abs(k - 1.0) < 0.02:
            ax.text(0, 95, "★ TRUE GEOMETRY ★", color='green', ha='center', fontsize=12, fontweight='bold')
        
        # Save frame
        fname = f"skel_frame_{i}.png"
        plt.savefig(fname, dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        with Image.open(fname) as pim:
            frames.append(pim.copy())
        os.remove(fname)

    print(f"\n[*] Saving DNA Animation to {GIF_NAME}...")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=60, loop=0)
    print("✅ Done. The Skeleton is revealed.")

if __name__ == "__main__":
    main()