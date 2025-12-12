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
LMAX = 60
N_RES = 300
FRAMES = 80
K_START = 0.9
K_END = 1.1
GIF_NAME = "cmb_breathing_topology.gif"

# ======================
# 1. OPTIMIZED ENGINE
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
    return alms, theta, phi

def precompute_profiles(alms, lmax, theta_vec):
    m_range = np.arange(-lmax, lmax + 1)
    n_m = len(m_range); n_theta = len(theta_vec)
    zeros_phi = np.zeros_like(theta_vec)
    profiles = np.zeros((n_m, n_theta), dtype=np.complex128)
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) not in alms: continue
            Y_lm_theta = sph_harm(m, l, zeros_phi, theta_vec)
            profiles[i, :] += alms[(l, m)] * Y_lm_theta
    return profiles, m_range

def synthesize_field(profiles, m_range, phi_vec, k):
    m_col = m_range[:, np.newaxis]
    phi_row = phi_vec[np.newaxis, :]
    phase_matrix = np.exp(1j * m_col * k * phi_row)
    field = (profiles.T @ phase_matrix).real
    return field

# ======================
# 2. DIVERGENCE CALCULATION
# ======================

def calculate_divergence(field_k, field_next):
    # 1. Calculate Velocity Field (dField/dt)
    diff = field_next - field_k
    
    # 2. Calculate Gradient of Velocity (The Flow Vectors)
    vy, vx = np.gradient(diff)
    
    # 3. Calculate Divergence (div V = dVx/dx + dVy/dy)
    # This measures how much the flow is "spreading" or "condensing"
    dvx_dx = np.gradient(vx, axis=1)
    dvy_dy = np.gradient(vy, axis=0)
    
    divergence = dvx_dx + dvy_dy
    return divergence

# ======================
# 3. RENDER LOOP
# ======================

def run_breathing_topology():
    alms, theta_vec, phi_vec = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    profiles, m_range = precompute_profiles(alms, LMAX, theta_vec)
    
    k_vals = np.concatenate([np.linspace(K_START, K_END, FRAMES//2), np.linspace(K_END, K_START, FRAMES//2)])
    
    # Track the "Lung Capacity" (Total Net Divergence)
    lung_history = []
    
    frames = []
    print(f"[*] Mapping the Breathing Topology...")
    
    for i in range(FRAMES - 1):
        k_curr = k_vals[i]
        k_next = k_vals[i] + 0.001
        
        sys.stdout.write(f"\r[>] Frame {i+1}/{FRAMES} | Twist k={k_curr:.3f}")
        sys.stdout.flush()
        
        field_curr = synthesize_field(profiles, m_range, phi_vec, k_curr)
        field_next = synthesize_field(profiles, m_range, phi_vec, k_next)
        
        # Calculate Pressure (Divergence)
        div_map = calculate_divergence(field_curr, field_next)
        
        # Track global stats
        total_breath = np.sum(div_map)
        lung_history.append(total_breath)
        
        # Plot
        fig = plt.figure(figsize=(10, 12), facecolor='#050505')
        gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
        
        # 1. The Breathing Map
        ax_map = plt.subplot(gs[0])
        
        # Use a diverging colormap:
        # Red = Positive Divergence (Exhale/Expansion)
        # Blue = Negative Divergence (Inhale/Contraction/Condensation)
        limit = np.percentile(np.abs(div_map), 98)
        im = ax_map.imshow(div_map, origin='lower', cmap='seismic', 
                           extent=[-180, 180, -90, 90], vmin=-limit, vmax=limit)
        
        ax_map.set_title(f"THE BREATHING TOPOLOGY | Pressure Zones (k={k_curr:.3f})", color='white', fontsize=14)
        ax_map.axis('off')
        
        # 2. The Heartbeat Graph
        ax_graph = plt.subplot(gs[1])
        ax_graph.set_facecolor('#111')
        
        ax_graph.plot(lung_history, color='lime', linewidth=2)
        ax_graph.set_xlim(0, FRAMES)
        
        # Keep Y scale centered
        y_max = max(abs(min(lung_history) if lung_history else 0), abs(max(lung_history) if lung_history else 0))
        if y_max == 0: y_max = 1
        ax_graph.set_ylim(-y_max*1.1, y_max*1.1)
        
        ax_graph.axhline(0, color='gray', linestyle='--')
        ax_graph.set_title("NET COSMIC RESPIRATION (Total Divergence)", color='lime', fontsize=10)
        ax_graph.tick_params(colors='gray')
        
        plt.tight_layout()
        
        fname = f"_breath_{i:03d}.png"
        plt.savefig(fname, dpi=80, bbox_inches='tight', facecolor='#050505')
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames.append(img.copy())
        os.remove(fname)

    print(f"\n[*] Saving GIF: {GIF_NAME}")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=60, loop=0)
    print("✅ Breathing Topology Mapped.")

if __name__ == "__main__":
    run_breathing_topology()