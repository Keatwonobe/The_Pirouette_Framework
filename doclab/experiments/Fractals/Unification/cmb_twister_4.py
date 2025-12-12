import numpy as np
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb 
from scipy.special import sph_harm
import os

# ======================
# CONFIG
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits" 
TWIST_MODE = "untwist"     # "twist" or "untwist"
LMAX = 40
N_THETA = 320 # Grid resolution for a_lm computation (lower for speed)
N_PHI = 640

# Scanning Parameters
K_RANGE_COARSE = np.linspace(0, 2, 600) # Coarse scan range
SPIKE_THRESHOLD = 0.005 # Minimum absolute drop in |C(k)| to flag a spike
SPIKE_WINDOW = 5        # Number of points before/after to check the drop

# ======================
# CORE CMBSCANNER FUNCTIONS (from cmb_scanner_6.py)
# ======================

def calculate_laplacian(image):
    """Computes the 2D Laplacian (nabla^2) of the image using np.gradient."""
    grad_y, grad_x = np.gradient(image)
    laplacian = np.gradient(grad_x, axis=1) + np.gradient(grad_y, axis=0)
    return laplacian

def render_helicity_view(T, PH):
    """Converts Temperature (Amplitude) and Longitude (Phase) into an HSV-based Topographic Phase Map."""
    hue = (PH + np.pi) / (2 * np.pi)
    T_clean = T.copy()
    T_clean[np.isnan(T_clean)] = np.nanmedian(T)
    
    log_amp = np.log1p(np.abs(T_clean - T_clean.mean())) 
    contour_freq = 30.0 
    structure = np.sin(log_amp * contour_freq)
    val = 0.6 + 0.4 * structure
    sat = np.ones_like(hue) * 0.95
    hsv = np.dstack((hue, sat, val))
    rgb = hsv_to_rgb(hsv)
    rgb[np.isnan(T), :] = 0.0
    return rgb

def plot_analysis_maps(cmb_orig, cmb_twisted, cmb_mask, cmb_helicity_orig, cmb_helicity_twisted, cmb_laplacian_twisted, k_val, file_suffix=""):
    """Generates the 6-panel analysis plot for a given twisted map."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), constrained_layout=True)
    extent = (-180, 180, -90, 90)
    
    # --- ROW 1: Standard Maps and Mask ---
    im0 = axes[0, 0].imshow(cmb_orig, origin="lower", aspect="auto", extent=extent, cmap="coolwarm")
    axes[0, 0].set_title("1. Original CMB Temperature")
    fig.colorbar(im0, ax=axes[0, 0], fraction=0.046, pad=0.04)

    im1 = axes[0, 1].imshow(cmb_twisted, origin="lower", aspect="auto", extent=extent, cmap="coolwarm")
    axes[0, 1].set_title(f"2. CMB $\\varphi$ {TWIST_MODE} (k={k_val:.8f})")
    fig.colorbar(im1, ax=axes[0, 1], fraction=0.046, pad=0.04)

    im2 = axes[0, 2].imshow(cmb_mask, origin="lower", aspect="auto", extent=extent, cmap="plasma")
    axes[0, 2].set_title("3. Correlation Mask (Absolute Difference)")
    fig.colorbar(im2, ax=axes[0, 2], fraction=0.046, pad=0.04, label="$|T_{\\text{orig}} - T_{\\text{twist}}|$")
    
    # --- ROW 2: Helicity and Laplacian Comparison ---
    axes[1, 0].imshow(cmb_helicity_orig, origin="lower", aspect="auto", extent=extent)
    axes[1, 0].set_title("4. Original 'Helicity' View (T as Amplitude)")
    
    axes[1, 1].imshow(cmb_helicity_twisted, origin="lower", aspect="auto", extent=extent)
    axes[1, 1].set_title(f"5. Twisted 'Helicity' View (k={k_val:.8f})")

    im5 = axes[1, 2].imshow(cmb_laplacian_twisted, origin="lower", aspect="auto", extent=extent, cmap="bwr")
    axes[1, 2].set_title(f"6. Laplacian $\\nabla^2 T_{TWIST_MODE}$ ('Lyapunov' Proxy)")
    fig.colorbar(im5, ax=axes[1, 2], fraction=0.046, pad=0.04, label="$\\nabla^2 T$ (Filtered Texture)")
    
    for ax in axes.flat:
        ax.set_xlabel("Longitude (deg)")
        ax.set_ylabel("Latitude (deg)")

    filename = f"cmb_analysis_k_{k_val:.8f}_{file_suffix}.png"
    plt.savefig(filename)
    plt.close(fig)
    print(f"[+] Analysis plot saved: {filename}")


# ======================
# TWIST & SAMPLING HELPERS (from cmb_twister_2.py)
# ======================
def twist_phi(phi, k, mode="untwist"):
    if mode == "twist":
        src = phi * k
    else:
        src = phi / k
    return (src + np.pi) % (2.0 * np.pi) - np.pi

def build_equatorial_grid(n_theta, n_phi):
    theta = np.linspace(0.0, np.pi, n_theta)
    phi   = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")
    return TH, PH

def healpix_sample(cmb, hpix, TH, PH):
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH) 
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    return cmb[ipix]

# ======================
# SPHERICAL HARMONICS (Optimized from cmb_twister_2.py)
# ======================
Y_LM_CONJ_WEIGHTED = None

def compute_and_cache_ylm(TH, PH, lmax):
    """Generates and caches the core integration factor (Y_lm* * weight)."""
    global Y_LM_CONJ_WEIGHTED
    if Y_LM_CONJ_WEIGHTED is not None:
        return

    # Grid setup and weight calculation
    theta_1d = TH[:, 0]
    phi_1d   = PH[0, :]
    dtheta = theta_1d[1] - theta_1d[0]
    dphi   = phi_1d[1] - phi_1d[0]
    sinTH = np.sin(TH)
    weight = (sinTH * dtheta * dphi).ravel()
    PH_flat  = PH.ravel()
    TH_flat  = TH.ravel()
    N_GRID   = TH_flat.size

    # Compute all Y_lm on the grid
    Y_lms = np.zeros((lmax+1, 2*lmax+1, N_GRID), dtype=np.complex128)
    print(f"        -> Generating {lmax*(lmax+2)+1} spherical harmonics... (One-time cost)")
    for l in range(lmax+1):
        for m in range(-l, l+1):
            Y_lms[l, m + lmax] = sph_harm(m, l, PH_flat, TH_flat)

    # Cache the combined factor
    Y_LM_CONJ_WEIGHTED = np.conjugate(Y_lms).reshape(-1, N_GRID) * weight
    print("        -> Y_lm factors cached.")

def compute_alm_final(T, TH, PH, lmax):
    """Uses the cached factors for ultra-fast a_lm computation."""
    compute_and_cache_ylm(TH, PH, lmax)
    T_flat = T.ravel()
    alms_flat = np.dot(T_flat, Y_LM_CONJ_WEIGHTED.T) 
    return alms_flat.reshape(lmax+1, 2*lmax+1)

def alm_correlation(alm0, alm1, lmax):
    """Compute overall complex correlation between two alm sets."""
    num = 0 + 0j
    den0 = 0.0
    den1 = 0.0
    for l in range(lmax+1):
        for m in range(-l, l+1):
            a0 = alm0[l, m + LMAX] # Use LMAX for index shift
            a1 = alm1[l, m + LMAX] # Use LMAX for index shift
            num  += a0 * np.conjugate(a1)
            den0 += np.abs(a0)**2
            den1 += np.abs(a1)**2
    if den0 == 0 or den1 == 0:
        return 0.0
    return num / np.sqrt(den0 * den1)


# ======================
# SPIKE DETECTION LOGIC
# ======================

def find_troughs(k_values, C_abs_values, threshold, window):
    """
    Identifies significant drops (troughs/spikes) in the correlation spectrum.
    A trough is detected if the value at point 'i' is lower than the average 
    of its surrounding 'window' points by more than 'threshold'.
    """
    trough_k = []
    
    # We ignore the edges to ensure a full window can be checked
    for i in range(window, len(C_abs_values) - window):
        C_i = C_abs_values[i]
        # Calculate the average of the surrounding window (excluding the center)
        C_before = C_abs_values[i - window : i]
        C_after  = C_abs_values[i + 1 : i + window + 1]
        
        # Check against the average of the surrounding points
        C_avg_surrounding = np.mean(np.concatenate((C_before, C_after)))
        
        if (C_avg_surrounding - C_i) > threshold:
            trough_k.append(k_values[i])

    # Remove near-duplicates by clustering (optional, but good for stability)
    trough_k.sort()
    final_troughs = []
    if trough_k:
        final_troughs.append(trough_k[0])
        for k in trough_k[1:]:
            # Check if the new k is sufficiently far from the last added k
            if np.abs(k - final_troughs[-1]) > (k_values[1] - k_values[0]) * 3:
                final_troughs.append(k)

    return final_troughs

# ======================
# MAIN EXECUTION
# ======================

def main_probe():
    global LMAX 

    print("[*] Loading CMB FITS...")
    try:
        data = fits.getdata(FITS_PATH)
    except FileNotFoundError:
        print(f"[!] ERROR: FITS file not found: {FITS_PATH}. Please upload it to run the analysis.")
        return

    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        raise ValueError("No usable CMB temperature field found!")

    npix = cmb.size
    nside = int(np.sqrt(npix / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    print(f"[*] Building angular grid ({N_THETA}x{N_PHI}) and sampling original map...")
    TH, PH = build_equatorial_grid(N_THETA, N_PHI)
    cmb_orig = healpix_sample(cmb, hpix, TH, PH)
    
    # Compute original a_lm (this also warms the Y_lm cache)
    print("[*] Computing alm for original map (cache warm-up)...")
    alm_orig = compute_alm_final(cmb_orig, TH, PH, LMAX)

    # --- 1. COARSE SCAN ---
    C_values_abs_coarse = []
    print(f"[*] Starting COARSE SCAN over {len(K_RANGE_COARSE)} k values...")
    for i, k in enumerate(K_RANGE_COARSE):
        if i % 10 == 0: print(f"    [-] Coarse k = {k:.6f}") 
        
        PH_src = twist_phi(PH, k, mode=TWIST_MODE)
        cmb_tw = healpix_sample(cmb, hpix, TH, PH_src)
        alm_tw = compute_alm_final(cmb_tw, TH, PH, LMAX)

        Ck = alm_correlation(alm_orig, alm_tw, LMAX)
        C_values_abs_coarse.append(np.abs(Ck))

    C_values_abs_coarse = np.array(C_values_abs_coarse)

    # --- 2. SPIKE DETECTION ---
    print("\n[*] Detecting significant troughs/spikes...")
    trough_k_values = find_troughs(K_RANGE_COARSE, C_values_abs_coarse, SPIKE_THRESHOLD, SPIKE_WINDOW)
    
    if not trough_k_values:
        print(f"[!] No significant troughs found with threshold={SPIKE_THRESHOLD}.")
        # Plot the coarse scan result anyway
        plot_correlation_spectrum(K_RANGE_COARSE, C_values_abs_coarse, trough_k_values, LMAX, "coarse_scan")
        return

    print(f"[+] Detected {len(trough_k_values)} potential special k-values:")
    for k in trough_k_values:
        print(f"    -> k_special = {k:.8f}")

    # Plot the coarse scan result with detected spikes
    plot_correlation_spectrum(K_RANGE_COARSE, C_values_abs_coarse, trough_k_values, LMAX, "coarse_scan")

    # --- 3. DETAIL ANALYSIS AND MAPPING ---
    print("\n[*] Generating detailed analysis maps for detected k-values...")
    
    # We add k=1 to the list for comparison if it's not already there
    k_to_analyze = trough_k_values.copy()
    if 1.0 not in k_to_analyze:
        k_to_analyze.append(1.0)
    k_to_analyze.sort()


    for k_val in k_to_analyze:
        print(f"\n    -> Processing k = {k_val:.8f}")
        
        # 1. Resample/Twist
        PH_src = twist_phi(PH, k_val, mode=TWIST_MODE)
        cmb_twisted = healpix_sample(cmb, hpix, TH, PH_src)
        
        # 2. Compute Analysis Fields
        mask = np.isfinite(cmb_orig) & np.isfinite(cmb_twisted)
        cmb_mask = np.abs(cmb_orig - cmb_twisted)
        cmb_helicity_orig = render_helicity_view(cmb_orig, PH)
        cmb_helicity_twisted = render_helicity_view(cmb_twisted, PH) 
        
        # Laplacian (needs valid data, using median fill for edge cases)
        cmb_orig_valid = cmb_orig.copy()
        cmb_orig_valid[~mask] = np.nanmedian(cmb_orig[mask])
        cmb_twisted_valid = cmb_twisted.copy()
        cmb_twisted_valid[~mask] = np.nanmedian(cmb_twisted[mask])
        
        # Calculate Laplacian on the filled map, then mask out the NaNs
        cmb_laplacian_twisted = calculate_laplacian(cmb_twisted_valid)
        cmb_laplacian_twisted[~mask] = np.nan 

        # 3. Plot
        plot_analysis_maps(
            cmb_orig, cmb_twisted, cmb_mask, 
            cmb_helicity_orig, cmb_helicity_twisted, 
            cmb_laplacian_twisted, k_val
        )

# ======================
# UTILITY PLOT FOR SPECTRUM
# ======================

def plot_correlation_spectrum(k_values, C_abs_values, special_k_list, LMAX, suffix=""):
    """Plots the overall correlation spectrum with marked special k-values."""
    fig, ax = plt.subplots(figsize=(8, 4), constrained_layout=True)

    ax.plot(k_values, C_abs_values, label="|C(k)| multipole correlation")
    ax.axvline(1.0, color="k", linestyle="--", label="k = 1 (identity)")
    
    # Mark the detected spikes
    for i, k_special in enumerate(special_k_list):
        label = f"k_probe {i+1} = {k_special:.8f}"
        ax.axvline(k_special, color="r", linestyle=":", label=label, alpha=0.7)
        # Add a point to mark the spot
        C_special = np.interp(k_special, k_values, C_abs_values)
        ax.plot(k_special, C_special, 'o', color='red', markersize=5)
        
    ax.set_ylabel("|C(k)|")
    ax.set_xlabel("Twist constant k")
    ax.set_title(f"Multipole correlation vs twist, l_max = {LMAX} ({suffix})")
    ax.legend(loc='lower left', fontsize='small')

    filename = f"cmb_multipole_twist_spectrum_{suffix}.png"
    plt.savefig(filename)
    plt.close(fig)
    print(f"[+] Spectrum plot saved as {filename}")


if __name__ == "__main__":
    main_probe()