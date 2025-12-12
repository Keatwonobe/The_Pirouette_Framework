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
import time

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 400
FRAMES = 80
K_START = 0.8
K_END = 1.2
CHAOS_DAMPING = 6.0  # How aggressively to remove the chaos (Higher = Cleaner but darker)
GIF_NAME = "cmb_structure_reveal.gif"

# ======================
# 1. OPTIMIZED ENGINE (Reused)
# ======================

def get_alms_and_coords(fits_path, lmax, n_res):
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
    print("[*] Extracting Harmonics...")
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta_vec = np.linspace(0, np.pi, n_res)
    phi_vec = np.linspace(-np.pi, np.pi, n_res)
    return alms, theta_vec, phi_vec

def precompute_m_profiles(alms, lmax, theta_vec):
    m_range = np.arange(-lmax, lmax + 1)
    n_m = len(m_range); n_theta = len(theta_vec)
    profiles = np.zeros((n_m, n_theta), dtype=np.complex128)
    zeros_phi = np.zeros_like(theta_vec)
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) in alms:
                Y_lm_theta = sph_harm(m, l, zeros_phi, theta_vec)
                profiles[i, :] += alms[(l, m)] * Y_lm_theta
    return profiles, m_range

def fast_synthesize_structure(profiles, m_range, phi_vec, k):
    # 1. Synthesize Field (Temperature)
    m_col = m_range[:, np.newaxis]
    phi_row = phi_vec[np.newaxis, :]
    phase_matrix = np.exp(1j * m_col * k * phi_row)
    
    temp_complex = profiles.T @ phase_matrix
    temp = temp_complex.real
    
    # 2. Calculate Chaos (Gradient Magnitude)
    grad_y, grad_x = np.gradient(temp)
    chaos = np.sqrt(grad_x**2 + grad_y**2)
    
    # Normalize Chaos locally (0 to 1) for consistent filtering
    c_min, c_max = np.percentile(chaos, [1, 99])
    chaos_norm = np.clip((chaos - c_min) / (c_max - c_min), 0, 1)
    
    return temp, chaos_norm

# ======================
# 2. THE STRUCTURE SCANNER
# ======================

def run_structure_scanner():
    alms, theta_vec, phi_vec = get_alms_and_coords(FITS_PATH, LMAX, N_RES)
    profiles, m_range = precompute_m_profiles(alms, LMAX, theta_vec)
    
    K_RANGE = np.linspace(K_START, K_END, FRAMES)
    frames = []
    
    print(f"[-] Scanning Structure (Taking out the Chaos)...")
    
    for i, k in enumerate(K_RANGE):
        sys.stdout.write(f"\r[>] Processing Frame {i+1}/{FRAMES} | k={k:.3f}")
        sys.stdout.flush()
        
        # 1. Get Raw Data
        temp, chaos = fast_synthesize_structure(profiles, m_range, phi_vec, k)
        
        # 2. THE FILTER: Dampen regions where chaos is high
        # We use an exponential decay mask: Stability = exp(-damp * chaos)
        stability_mask = np.exp(-CHAOS_DAMPING * chaos)
        
        # 3. The Reveal
        structure = temp * stability_mask
        
        # --- Plotting ---
        fig = plt.figure(figsize=(12, 12), facecolor='#050505')
        gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 1], hspace=0.15)
        
        # Panel 1: The Raw Twist (Temperature)
        ax1 = plt.subplot(gs[0])
        ax1.imshow(temp, origin='lower', cmap='RdBu_r', extent=[-180, 180, -90, 90])
        ax1.set_title(f"1. RAW TEMPERATURE (k={k:.3f})", color='white', fontsize=10)
        ax1.axis('off')
        
        # Panel 2: The Chaos Mask (What we are removing)
        ax2 = plt.subplot(gs[1])
        # We plot the inverse mask to show "Where the Chaos Is"
        ax2.imshow(chaos, origin='lower', cmap='inferno', extent=[-180, 180, -90, 90])
        ax2.set_title(f"2. THE CHAOS BARRIER (Gradient Energy)", color='orange', fontsize=10)
        ax2.axis('off')
        
        # Panel 3: The Inner Picture (Structure)
        ax3 = plt.subplot(gs[2])
        # Use a distinctive map for the "Ghost" structure
        im = ax3.imshow(structure, origin='lower', cmap='twilight', extent=[-180, 180, -90, 90])
        ax3.set_title(f"3. THE INNER STRUCTURE (Stable Attractors)", color='cyan', fontsize=12, fontweight='bold')
        ax3.axis('off')
        
        # Add a visual indicator for K=1 (Reality)
        if abs(k - 1.0) < 0.01:
            ax3.text(0.02, 0.9, "★ REALITY LOCK", transform=ax3.transAxes, color='yellow', fontsize=12, fontweight='bold')
        
        fname = f"_struct_{i:03d}.png"
        plt.savefig(fname, dpi=70, bbox_inches='tight', facecolor='#050505')
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames.append(img.copy())
        os.remove(fname)

    print(f"\n[*] Saving GIF: {GIF_NAME}")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=60, loop=0)
    print("✅ Structure Scan Complete.")

if __name__ == "__main__":
    run_structure_scanner()