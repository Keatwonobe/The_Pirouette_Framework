import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.stats import linregress
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys
import time

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 512                 # High res for accurate box counting
PATCH_SIZE = 32             # Size of the "Focus" blocks for the camera
THRESHOLD_PERCENTILE = 80   # Defines the "Skeleton" for the global check

# ======================
# 1. OPTIMIZED SYNTHESIS ENGINE
# ======================

def get_alms_and_coords(fits_path, lmax, n_res):
    print(f"[*] Loading CMB Data from {fits_path}...")
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
    print("[*] Extracting Spherical Harmonics (ALMs)...")
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

    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    # Synthesis Coords
    theta_vec = np.linspace(0, np.pi, n_res)
    phi_vec = np.linspace(-np.pi, np.pi, n_res)
    
    return alms, theta_vec, phi_vec

def precompute_m_profiles(alms, lmax, theta_vec):
    """
    OPTIMIZATION: Sums Legendre polynomials for each m into a single profile.
    """
    print(f"[*] Pre-computing Latitudinal Profiles (Matrix Optimization)...")
    
    m_range = np.arange(-lmax, lmax + 1)
    n_m = len(m_range)
    n_theta = len(theta_vec)
    
    profiles = np.zeros((n_m, n_theta), dtype=np.complex128)
    zeros_phi = np.zeros_like(theta_vec)
    
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) in alms:
                # We assume phi=0 to get the theta dependence (P_lm)
                Y_lm_theta = sph_harm(m, l, zeros_phi, theta_vec)
                profiles[i, :] += alms[(l, m)] * Y_lm_theta
                
    return profiles, m_range

def fast_synthesize_gradient(profiles, m_range, phi_vec):
    """
    Synthesizes the field using Matrix Multiplication, then computes Gradient.
    """
    print("[*] Synthesizing Field via Matrix Multiplication...")
    # 1. Matrix Mult for Field
    m_col = m_range[:, np.newaxis]
    phi_row = phi_vec[np.newaxis, :]
    
    # Phase Matrix (k=1.0 for Reality)
    phase_matrix = np.exp(1j * m_col * phi_row) 
    
    # Field = Profiles.T @ Phase
    field_complex = profiles.T @ phase_matrix
    field = field_complex.real
    
    # 2. Gradient (Chaos)
    print("[*] Calculating Gradient Magnitude...")
    grad_y, grad_x = np.gradient(field)
    chaos = np.sqrt(grad_x**2 + grad_y**2)
    
    # Normalize
    chaos = (chaos - chaos.min()) / (chaos.max() - chaos.min())
    return chaos

# ======================
# 2. FRACTAL ENGINE
# ======================

def box_count(img, threshold=0.5):
    binary = img > threshold
    pixels = np.array(binary, dtype=int)
    scales = []
    counts = []
    
    s = min(pixels.shape)
    while s > 1:
        # Fast block reduction
        h = (pixels.shape[0] // s) * s
        w = (pixels.shape[1] // s) * s
        trimmed = pixels[:h, :w]
        blocks = trimmed.reshape(h//s, s, w//s, s)
        max_blocks = blocks.max(axis=(1, 3))
        
        count = np.sum(max_blocks)
        if count > 0:
            scales.append(s)
            counts.append(count)
        s //= 2
        
    return np.array(scales), np.array(counts)

def get_fractal_dimension_map(chaos_map, patch_size):
    h, w = chaos_map.shape
    d_map = np.zeros((h // patch_size, w // patch_size))
    
    print(f"[*] Scanning Local Fractal Dimension (Grid {d_map.shape})...")
    
    # Iterate patches
    count = 0
    total = d_map.size
    
    for i in range(d_map.shape[0]):
        for j in range(d_map.shape[1]):
            y = i * patch_size
            x = j * patch_size
            patch = chaos_map[y:y+patch_size, x:x+patch_size]
            
            thresh = np.mean(patch) # Local adaptive threshold
            
            scales, counts = box_count(patch, thresh)
            
            if len(scales) > 2:
                # Negative slope = Dimension
                slope, _, _, _, _ = linregress(np.log(1.0/scales), np.log(counts))
                d_map[i, j] = slope 
            else:
                d_map[i, j] = 0
            
            count += 1
            if count % 50 == 0:
                sys.stdout.write(f"\r    -> Progress: {count}/{total} blocks")
                sys.stdout.flush()
                
    print("\n")
    return d_map

# ======================
# 3. EXECUTION
# ======================

def run_fractal_camera_optimized():
    start_t = time.time()
    
    # A. Optimized Synthesis
    alms, theta_vec, phi_vec = get_alms_and_coords(FITS_PATH, LMAX, N_RES)
    profiles, m_range = precompute_m_profiles(alms, LMAX, theta_vec)
    chaos = fast_synthesize_gradient(profiles, m_range, phi_vec)
    
    # B. Global Check
    print("[*] Performing Global Box-Counting Check...")
    thresh_val = np.percentile(chaos, THRESHOLD_PERCENTILE)
    scales, counts = box_count(chaos, thresh_val)
    
    log_inv_s = np.log(1.0 / scales)
    log_N = np.log(counts)
    slope, intercept, r_value, _, _ = linregress(log_inv_s, log_N)
    global_D = slope
    
    # C. The Camera Scan
    d_map = get_fractal_dimension_map(chaos, PATCH_SIZE)
    
    # D. Plotting
    fig = plt.figure(figsize=(14, 10), facecolor='#111')
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])
    
    # 1. Raw Chaos
    ax1 = plt.subplot(gs[0, 0])
    ax1.imshow(chaos, cmap='inferno', origin='lower')
    ax1.set_title("1. Raw Chaos Field (Gradient Energy)", color='white')
    ax1.axis('off')
    
    # 2. Fractal Verification
    ax2 = plt.subplot(gs[0, 1])
    ax2.set_facecolor('#222')
    ax2.plot(log_inv_s, log_N, 'o', color='cyan', label='CMB Structure')
    ax2.plot(log_inv_s, slope * log_inv_s + intercept, 'r--', label=f'Fit (D={global_D:.3f})')
    ax2.set_title(f"2. Fractal Verification (R²={r_value**2:.4f})", color='white')
    ax2.set_xlabel("log(1/scale)", color='gray')
    ax2.set_ylabel("log(Count)", color='gray')
    ax2.legend()
    ax2.grid(True, color='#444')
    ax2.tick_params(colors='gray')
    
    # 3. The Fractal Camera
    ax3 = plt.subplot(gs[1, :])
    im = ax3.imshow(d_map, cmap='magma', origin='lower', extent=[0, N_RES, 0, N_RES], interpolation='bicubic')
    ax3.set_title(f"3. THE FRACTAL CAMERA: Local Dimensionality Map (Block {PATCH_SIZE})", color='white')
    ax3.axis('off')
    
    cbar = plt.colorbar(im, ax=ax3, orientation='horizontal', pad=0.05, fraction=0.05)
    cbar.set_label("Local Fractal Dimension (Complexity)", color='gray')
    cbar.ax.xaxis.set_tick_params(color='gray')
    plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'), color='gray')
    
    plt.tight_layout()
    plt.savefig("cmb_fractal_camera_optimized.png", dpi=100, facecolor='#111')
    
    end_t = time.time()
    print(f"✅ Analysis Complete in {end_t - start_t:.2f}s. Global D={global_D:.4f}")

if __name__ == "__main__":
    run_fractal_camera_optimized()