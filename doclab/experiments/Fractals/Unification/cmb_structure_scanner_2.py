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
N_RES = 300                 # Resolution per panel
FRAMES = 60                 # Animation duration
K_START = 0.8
K_END = 1.2
CHAOS_DAMPING = 5.0         # The "Cooling" Factor (Removes the Magma)
GIF_NAME = "cmb_spectral_structure_scan.gif"

# ======================
# 1. SPECTRAL OPTIMIZATION ENGINE
# ======================

def get_alms_and_coords(fits_path, lmax, n_res):
    print(f"[*] Loading CMB Data from {fits_path}...")
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

def precompute_spectral_profiles(alms, lmax, theta_vec):
    """
    Separates the harmonics into 6 distinct matrix profiles for fast synthesis.
    """
    print(f"[*] Pre-computing Spectral Channels (L10, L20, L30, L40, Sub, Rem)...")
    
    m_range = np.arange(-lmax, lmax + 1)
    n_m = len(m_range); n_theta = len(theta_vec)
    zeros_phi = np.zeros_like(theta_vec)
    
    # Initialize dictionary of matrices
    keys = ['L10', 'L20', 'L30', 'L40', 'Substrate', 'Remainder']
    profiles = {k: np.zeros((n_m, n_theta), dtype=np.complex128) for k in keys}
    
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) not in alms: continue
            
            # The Legendre Component
            Y_lm_theta = sph_harm(m, l, zeros_phi, theta_vec)
            term = alms[(l, m)] * Y_lm_theta
            
            # Sort into buckets
            if l == 10: profiles['L10'][i, :] += term
            elif l == 20: profiles['L20'][i, :] += term
            elif l == 30: profiles['L30'][i, :] += term
            elif l == 40: profiles['L40'][i, :] += term
            elif l < 10: profiles['Substrate'][i, :] += term
            elif l > 40: profiles['Remainder'][i, :] += term
            
    return profiles, m_range

def synthesize_and_filter(profile_matrix, m_range, phi_vec, k, damp):
    """
    1. Synthesize Field
    2. Compute Chaos (Gradient)
    3. Apply Stability Mask
    """
    # Matrix Synthesis
    m_col = m_range[:, np.newaxis]
    phi_row = phi_vec[np.newaxis, :]
    phase_matrix = np.exp(1j * m_col * k * phi_row)
    
    field_complex = profile_matrix.T @ phase_matrix
    field = field_complex.real
    
    # Chaos Calculation
    grad_y, grad_x = np.gradient(field)
    chaos = np.sqrt(grad_x**2 + grad_y**2)
    
    # Normalize Chaos (Local to this band)
    c_min, c_max = np.percentile(chaos, [1, 99])
    if c_max > c_min:
        chaos_norm = np.clip((chaos - c_min) / (c_max - c_min), 0, 1)
    else:
        chaos_norm = np.zeros_like(chaos)
        
    # The Filter
    stability_mask = np.exp(-damp * chaos_norm)
    clean_structure = field * stability_mask
    
    return clean_structure

# ======================
# 2. SPECTRAL SCANNER LOOP
# ======================

def run_spectral_scanner():
    alms, theta_vec, phi_vec = get_alms_and_coords(FITS_PATH, LMAX, N_RES)
    profiles_dict, m_range = precompute_spectral_profiles(alms, LMAX, theta_vec)
    
    K_RANGE = np.linspace(K_START, K_END, FRAMES)
    frames = []
    
    print(f"[-] Scanning Spectral Structure (k={K_START}->{K_END})...")
    
    for i, k in enumerate(K_RANGE):
        sys.stdout.write(f"\r[>] Frame {i+1}/{FRAMES} | k={k:.3f}")
        sys.stdout.flush()
        
        # Prepare Plot
        fig = plt.figure(figsize=(15, 10), facecolor='#050505')
        gs = gridspec.GridSpec(2, 3, wspace=0.1, hspace=0.2)
        
        panels = [
            ('Substrate (L<10)', profiles_dict['Substrate'], gs[0, 0]),
            ('L=10 (Bass)', profiles_dict['L10'], gs[0, 1]),
            ('L=20 (Tenor)', profiles_dict['L20'], gs[0, 2]),
            ('L=30 (Alto)', profiles_dict['L30'], gs[1, 0]),
            ('L=40 (Soprano)', profiles_dict['L40'], gs[1, 1]),
            ('Remainder (L>40)', profiles_dict['Remainder'], gs[1, 2])
        ]
        
        for title, matrix, grid_loc in panels:
            # Generate the "Clean" view for this band
            img = synthesize_and_filter(matrix, m_range, phi_vec, k, CHAOS_DAMPING)
            
            ax = plt.subplot(grid_loc)
            ax.imshow(img, origin='lower', cmap='twilight', extent=[-180, 180, -90, 90])
            ax.set_title(f"{title}", color='white', fontsize=10)
            ax.axis('off')
            
            # Reality Marker
            if abs(k - 1.0) < 0.01:
                ax.text(0.05, 0.9, "★ LOCKED", transform=ax.transAxes, color='yellow', fontsize=8)

        fig.suptitle(f"CMB SPECTRAL STRUCTURE SCAN | Twist k={k:.3f}\n(Chaos Filtered: Magma Removed)", 
                     color='cyan', fontsize=14, y=0.95)
        
        fname = f"_spec_{i:03d}.png"
        plt.savefig(fname, dpi=70, bbox_inches='tight', facecolor='#050505')
        plt.close(fig)
        
        with Image.open(fname) as pim:
            frames.append(pim.copy())
        os.remove(fname)

    print(f"\n[*] Saving GIF: {GIF_NAME}")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=80, loop=0)
    print("✅ Spectral Scan Complete.")

if __name__ == "__main__":
    run_spectral_scanner()