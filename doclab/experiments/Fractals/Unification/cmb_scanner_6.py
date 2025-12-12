import numpy as np
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb 

# ======================
# CONFIG
# ======================

# IMPORTANT: This FITS file must be in the same directory to run!
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits" 
TWIST_CONST = 1.0072973525643
TWIST_MODE = "untwist"     # "twist" or "untwist"

# grid resolution
N_THETA = 1024
N_PHI   = 2048


# ======================
# ANALYSIS FUNCTIONS
# ======================

def compute_correlation_for_k(cmb, hpix, TH, PH, k, mode="untwist"):
    """Return (r, rms_diff, rms_lap) for given twist k."""
    # Original (only once per script run ideally, but recompute for clarity)
    cmb_orig = healpix_sample(cmb, hpix, TH, PH)

    # Twisted
    PH_src = twist_phi(PH, k, mode=mode)
    cmb_twisted = healpix_sample(cmb, hpix, TH, PH_src)

    mask = np.isfinite(cmb_orig) & np.isfinite(cmb_twisted)
    x = cmb_orig[mask] - cmb_orig[mask].mean()
    y = cmb_twisted[mask] - cmb_twisted[mask].mean()

    r = np.dot(x, y) / np.sqrt(np.dot(x, x) * np.dot(y, y))

    diff = cmb_orig[mask] - cmb_twisted[mask]
    rms_diff = np.sqrt(np.mean(diff**2))

    # Laplacian rms as a “Lyapunov texture” measure
    cmb_twisted_valid = cmb_twisted.copy()
    cmb_twisted_valid[~mask] = np.nanmedian(cmb_twisted[mask])
    lap = calculate_laplacian(cmb_twisted_valid)
    lap_mask = np.isfinite(lap)
    rms_lap = np.sqrt(np.mean(lap[lap_mask]**2))

    return r, rms_diff, rms_lap

def calculate_laplacian(image):
    """
    Computes the 2D Laplacian (nabla^2) of the image using np.gradient.
    Proxy for structural/non-linear comparison (Lyapunov comparison).
    """
    grad_y, grad_x = np.gradient(image)
    laplacian = np.gradient(grad_x, axis=1) + np.gradient(grad_y, axis=0)
    return laplacian


def render_helicity_view(T, PH):
    """
    Converts Temperature (Amplitude) and Longitude (Phase) into an 
    HSV-based Topographic Phase Map (Helicity view).
    T: CMB Temperature map (Amplitude)
    PH: Longitude map (Phase) in radians [-pi, pi)
    """
    # Phase (Hue): Map PH [-pi, pi) to [0, 1] range for Hue
    hue = (PH + np.pi) / (2 * np.pi)
    
    # Normalize T
    T_clean = T.copy()
    T_median = np.nanmedian(T)
    T_clean[np.isnan(T_clean)] = T_median
    
    # Logarithmic Compression
    log_amp = np.log1p(np.abs(T_clean - T_clean.mean())) 
    
    # Iso-Contour Generation
    contour_freq = 30.0 
    structure = np.sin(log_amp * contour_freq)
    
    # Normalize structure for Value
    val = 0.6 + 0.4 * structure
    
    # Saturation
    sat = np.ones_like(hue) * 0.95
    
    # Stack HSV and convert
    hsv = np.dstack((hue, sat, val))
    rgb = hsv_to_rgb(hsv)
    
    # Mask out NaNs
    rgb[np.isnan(T), :] = 0.0
    
    return rgb


# ======================
# CORE CMBSCANNER FUNCTIONS
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

def main():
    print("[*] Loading FITS...")
    try:
        # Check for FITS file
        data = fits.getdata(FITS_PATH)
    except FileNotFoundError:
        print(f"[!] ERROR: FITS file not found: {FITS_PATH}. Please upload it to run the analysis.")
        return
        
    # Data loading (rest of the original script)
    # ...
    print("[*] FITS columns:", data.dtype.names)
    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
        print("[*] Using column 'I' as CMB temperature")
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
        print("[*] Using column 'INP_CMB' as CMB temperature")
    else:
        raise ValueError("No usable CMB temperature field found!")
        
    npix = cmb.size
    nside = int(np.sqrt(npix / 12))
    print(f"[*] nside inferred from map: {nside} (npix={npix})")

    print("[*] Initializing HEALPix object...")
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    print("[*] Building angular grid...")
    TH, PH = build_equatorial_grid(N_THETA, N_PHI) 

    print("[*] Sampling original CMB onto grid...")
    cmb_orig = healpix_sample(cmb, hpix, TH, PH)

    print(f"[*] Applying twist (mode={TWIST_MODE}, k={TWIST_CONST})...")
    PH_src = twist_phi(PH, TWIST_CONST, mode=TWIST_MODE)
    cmb_twisted = healpix_sample(cmb, hpix, TH, PH_src)

    # Simple sanity correlation (original)
    mask = np.isfinite(cmb_orig) & np.isfinite(cmb_twisted)
    x = cmb_orig[mask] - cmb_orig[mask].mean()
    y = cmb_twisted[mask] - cmb_twisted[mask].mean()
    r = np.dot(x, y) / np.sqrt(np.dot(x, x) * np.dot(y, y))
    print(f"[+] Correlation (orig vs twisted): r = {r:.4f}")
    
    # ======================
    # NEW ANALYSIS COMPUTATION
    # ======================
    print("[*] Computing new analysis fields (Mask, Helicity, Laplacian)...")
    
    # 1. Correlation Mask (Absolute Difference)
    cmb_mask = np.abs(cmb_orig - cmb_twisted)
    
    # 2. Helicity View (Original and Twisted)
    cmb_helicity_orig = render_helicity_view(cmb_orig, PH)
    cmb_helicity_twisted = render_helicity_view(cmb_twisted, PH) 
    
    # 3. Laplacian (Lyapunov Comparison Proxy)
    cmb_orig_valid = cmb_orig.copy()
    cmb_orig_valid[~mask] = np.nanmedian(cmb_orig[mask])
    cmb_twisted_valid = cmb_twisted.copy()
    cmb_twisted_valid[~mask] = np.nanmedian(cmb_twisted[mask])
    
    cmb_laplacian_orig = calculate_laplacian(cmb_orig_valid)
    cmb_laplacian_twisted = calculate_laplacian(cmb_twisted_valid)
    cmb_laplacian_orig[~mask] = np.nan 
    cmb_laplacian_twisted[~mask] = np.nan 

    # ======================
    # PARAMETRIC TWIST SCAN
    # ======================
    # print("[*] Scanning correlation as a function of k...")

    # k_values = np.linspace(0.5, 5.0, 80)  # adjust range/resolution as you like
    # r_vals = []
    # rms_vals = []
    # rms_lap_vals = []

    # for k in k_values:
    #     r_k, rms_k, rms_lap_k = compute_correlation_for_k(
    #         cmb, hpix, TH, PH, k, mode=TWIST_MODE
    #     )
    #     r_vals.append(r_k)
    #     rms_vals.append(rms_k)
    #     rms_lap_vals.append(rms_lap_k)

    # r_vals = np.array(r_vals)
    # rms_vals = np.array(rms_vals)
    # rms_lap_vals = np.array(rms_lap_vals)

    # Plot twist spectrum
    # fig_k, ax_k = plt.subplots(2, 1, figsize=(8, 8), sharex=True, constrained_layout=True)

    # ax_k[0].plot(k_values, r_vals)
    # ax_k[0].axvline(TWIST_CONST, color="k", linestyle="--", label=f"k = {TWIST_CONST}")
    # ax_k[0].set_ylabel("Pearson r(orig, twisted)")
    # ax_k[0].legend()

    # ax_k[1].plot(k_values, rms_vals, label="RMS |ΔT|")
    # ax_k[1].plot(k_values, rms_lap_vals, label="RMS ∇²T_twisted", alpha=0.7)
    # ax_k[1].axvline(TWIST_CONST, color="k", linestyle="--")
    # ax_k[1].set_xlabel("Twist constant k")
    # ax_k[1].set_ylabel("RMS")
    # ax_k[1].legend()

    # plt.savefig("cmb_twist_spectrum.png")
    # plt.close(fig_k)
    # print("[*] Twist spectrum saved as cmb_twist_spectrum.png")


    # ======================
    # PLOTS
    # ======================
    print("[*] Plotting combined results...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), constrained_layout=True)
    extent = (-180, 180, -90, 90)
    
    # --- ROW 1: Standard Maps and Mask ---
    
    # P1: Original CMB Temperature
    im0 = axes[0, 0].imshow(cmb_orig, origin="lower", aspect="auto", extent=extent, cmap="coolwarm")
    axes[0, 0].set_title("1. Original CMB Temperature")
    fig.colorbar(im0, ax=axes[0, 0], fraction=0.046, pad=0.04)

    # P2: Twisted CMB Temperature
    im1 = axes[0, 1].imshow(cmb_twisted, origin="lower", aspect="auto", extent=extent, cmap="coolwarm")
    axes[0, 1].set_title(f"2. CMB $\\varphi$ {TWIST_MODE} (k={TWIST_CONST})")
    fig.colorbar(im1, ax=axes[0, 1], fraction=0.046, pad=0.04)

    # P3: Correlation Mask (Absolute Difference)
    im2 = axes[0, 2].imshow(cmb_mask, origin="lower", aspect="auto", extent=extent, cmap="plasma")
    axes[0, 2].set_title("3. Correlation Mask (Absolute Difference)")
    fig.colorbar(im2, ax=axes[0, 2], fraction=0.046, pad=0.04, label="$|T_{\\text{orig}} - T_{\\text{twist}}|$")
    
    # --- ROW 2: Helicity and Laplacian Comparison ---

    # P4: Original Helicity View (Topographic Phase Map)
    axes[1, 0].imshow(cmb_helicity_orig, origin="lower", aspect="auto", extent=extent)
    axes[1, 0].set_title("4. Original 'Helicity' View (T as Amplitude)")
    
    # P5: Twisted Helicity View
    axes[1, 1].imshow(cmb_helicity_twisted, origin="lower", aspect="auto", extent=extent)
    axes[1, 1].set_title(f"5. Twisted 'Helicity' View (k={TWIST_CONST})")

    # P6: Laplacian Comparison (Twisted) - Proxy for Lyapunov Structure
    im5 = axes[1, 2].imshow(cmb_laplacian_twisted, origin="lower", aspect="auto", extent=extent, cmap="bwr")
    axes[1, 2].set_title(f"6. Laplacian $\\nabla^2 T_{TWIST_MODE}$ ('Lyapunov' Proxy)")
    fig.colorbar(im5, ax=axes[1, 2], fraction=0.046, pad=0.04, label="$\\nabla^2 T$ (Filtered Texture)")
    
    # Set common labels
    for ax in axes.flat:
        ax.set_xlabel("Longitude (deg)")
        ax.set_ylabel("Latitude (deg)")

    plt.savefig("cmb_correlation_analysis.png")
    plt.close(fig)
    print("[*] Plot saved as cmb_correlation_analysis.png")

if __name__ == "__main__":
    main()