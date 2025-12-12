import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
import cv2  # OpenCV for Optical Flow
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 512
K_BASE = 1.0
K_Twist = 1.01  # 1% Twist to induce flow

# ======================
# 1. HARMONIC ENGINE
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
    
    n_theta = lmax * 3; n_phi = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta)
    p_alm = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')
    
    # --- FIX: Attach Units for Astropy ---
    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi)) * u.deg
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM) * u.deg
    
    ipix = hpix.lonlat_to_healpix(lon_deg, lat_deg)
    # -------------------------------------

    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    alms = {}
    print("[*] Extracting Harmonics...")
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, theta, phi, TH_GRID, PH_GRID

def synthesize_field(alms, lmax, theta_vec, phi_vec, k):
    m_range = np.arange(-lmax, lmax + 1)
    n_theta = len(theta_vec)
    zeros_phi = np.zeros_like(theta_vec)
    
    # Fast Profile Pre-calc
    profiles = np.zeros((len(m_range), n_theta), dtype=np.complex128)
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) not in alms: continue
            profiles[i, :] += alms[(l, m)] * sph_harm(m, l, zeros_phi, theta_vec)
            
    phase_matrix = np.exp(1j * m_range[:, None] * k * phi_vec[None, :])
    field = (profiles.T @ phase_matrix).real
    return field

# ======================
# 2. HELICITY CALCULATOR (Optical Flow)
# ======================

def compute_optical_flow(img1, img2):
    # Normalize to 0-255 for OpenCV
    i1 = cv2.normalize(img1, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    i2 = cv2.normalize(img2, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Farneback Optical Flow (Dense)
    flow = cv2.calcOpticalFlowFarneback(i1, i2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    vx, vy = flow[..., 0], flow[..., 1]
    return vx, vy

def run_helicity_scan():
    alms, theta_vec, phi_vec, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    
    print(f"[*] Synthesizing Twist Response (k={K_BASE} -> {K_Twist})...")
    f0 = synthesize_field(alms, LMAX, theta_vec, phi_vec, K_BASE)
    f1 = synthesize_field(alms, LMAX, theta_vec, phi_vec, K_Twist)
    
    print(f"[*] Computing Optical Flow (Lucas-Kanade Dynamics)...")
    # Get true velocity field (detects rotation that gradient method misses)
    vx, vy = compute_optical_flow(f0, f1)
    
    print(f"[*] Analyzing Flow Topology (Div/Curl)...")
    # Divergence = dVx/dx + dVy/dy (Expansion)
    # Curl = dVy/dx - dVx/dy (Twist)
    dvx_dy, dvx_dx = np.gradient(vx)
    dvy_dy, dvy_dx = np.gradient(vy)
    
    divergence = dvx_dx + dvy_dy
    curl = dvy_dx - dvx_dy
    
    # HELICITY DENSITY (Screw Action)
    # H = Div * Curl
    chirality = divergence * curl
    
    # Global Index
    mean_chirality = np.mean(chirality)
    magnitude = np.mean(np.abs(chirality))
    index = mean_chirality / magnitude if magnitude > 0 else 0
    
    print(f"\n[*] RESULTS:")
    print(f"    Global Chirality Index: {index:+.5f}")
    if index > 0.005: print("    -> CONCLUSION: LEFT-HANDED (Levorotatory System)")
    elif index < -0.005: print("    -> CONCLUSION: RIGHT-HANDED (Dextrorotatory System)")
    else: print("    -> CONCLUSION: ACHIRAL (Parity Conserved)")
    
    # --- PLOTTING ---
    fig = plt.figure(figsize=(10, 14), facecolor='#050505')
    gs = gridspec.GridSpec(4, 1, height_ratios=[2, 1, 1, 1])
    
    # 1. Flow Field Visualization
    ax_flow = plt.subplot(gs[0])
    mag = np.sqrt(vx**2 + vy**2)
    ax_flow.imshow(mag, cmap='inferno', origin='lower', extent=[-180, 180, -90, 90])
    # Overlay streamlines
    stride = 20
    Y, X = np.mgrid[-90:90:N_RES*1j, -180:180:N_RES*1j]
    ax_flow.quiver(X[::stride, ::stride], Y[::stride, ::stride], 
                   vx[::stride, ::stride], vy[::stride, ::stride], 
                   color='cyan', scale=50, alpha=0.5)
    ax_flow.set_title("OPTICAL FLOW FIELD (Cosmic Wind)", color='white')
    ax_flow.axis('off')
    
    # 2. Chirality Map (The Screw)
    ax_chir = plt.subplot(gs[1])
    # Normalize for contrast
    c_norm = np.clip(chirality, -np.std(chirality)*2, np.std(chirality)*2)
    ax_chir.imshow(c_norm, cmap='seismic', origin='lower', extent=[-180, 180, -90, 90])
    ax_chir.set_title(f"CHIRALITY DENSITY MAP | Bias: {index:.4f}", color='white')
    ax_chir.axis('off')
    
    # 3. Zonal Chirality (Latitude Profile)
    ax_zonal = plt.subplot(gs[2])
    ax_zonal.set_facecolor('#111')
    zonal_c = np.mean(chirality, axis=1)
    lats = np.linspace(-90, 90, N_RES)
    ax_zonal.plot(lats, zonal_c, color='yellow')
    ax_zonal.fill_between(lats, 0, zonal_c, where=(zonal_c>0), color='cyan', alpha=0.3, label='Left (CCW)')
    ax_zonal.fill_between(lats, 0, zonal_c, where=(zonal_c<0), color='magenta', alpha=0.3, label='Right (CW)')
    ax_zonal.set_xlim(-90, 90)
    ax_zonal.axhline(0, color='gray', linestyle=':')
    ax_zonal.set_title("ZONAL CHIRALITY (Hemispheric Bias)", color='white', fontsize=10)
    ax_zonal.tick_params(colors='gray')
    ax_zonal.legend(loc='upper right')
    
    # 4. Correlation (The Coupling)
    ax_corr = plt.subplot(gs[3])
    ax_corr.set_facecolor('#111')
    sub = 100
    ax_corr.scatter(divergence.flatten()[::sub], curl.flatten()[::sub], c='white', s=1, alpha=0.2)
    # Fit
    m, b = np.polyfit(divergence.flatten(), curl.flatten(), 1)
    xx = np.linspace(divergence.min(), divergence.max(), 100)
    ax_corr.plot(xx, m*xx + b, color='lime', linestyle='--', label=f'Coupling: {m:.3f}')
    
    ax_corr.set_xlabel("Expansion (Div)", color='gray')
    ax_corr.set_ylabel("Twist (Curl)", color='gray')
    ax_corr.set_title("DIVERGENCE-CURL COUPLING", color='white', fontsize=10)
    ax_corr.tick_params(colors='gray')
    ax_corr.legend()
    
    plt.tight_layout()
    plt.savefig("cmb_helicity_scan.png", dpi=100, facecolor='#050505')
    print("✅ Scan Complete.")

if __name__ == "__main__":
    run_helicity_scan()