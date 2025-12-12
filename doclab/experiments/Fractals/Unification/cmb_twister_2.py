import numpy as np
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt
from scipy.special import sph_harm

# ======================
# CONFIG (No Change)
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
TWIST_MODE = "untwist"   # "twist" or "untwist"
N_THETA = 320
N_PHI   = 640
LMAX   = 40
K_VALUES = np.linspace(1.05, 1.08, 410)
K_SPECIAL = 1.0072973525643

# ======================
# TWIST & SAMPLING HELPERS (No Change)
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
    # Corrected latitude calculation for Astropy SkyCoord (Galactic)
    # 0.5*pi - TH is colatitude, converted to latitude
    lat_deg = np.rad2deg(0.5*np.pi - TH) 
    # Note: Astropy SkyCoord takes l, b (longitude, latitude)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    return cmb[ipix]


# ======================
# SPHERICAL HARMONICS (Refactored for speed)
# ======================

def compute_alm_fast(T, TH, PH, lmax):
    """
    Compute a_lm up to lmax using vectorized numpy operations.
    T, TH, PH shapes: (N_THETA, N_PHI)
    Returns alms as array alm[l, m + lmax].
    """
    theta_1d = TH[:, 0]
    phi_1d   = PH[0, :]
    dtheta = theta_1d[1] - theta_1d[0]
    dphi   = phi_1d[1] - phi_1d[0]

    # Pre-calculate weights and flatten arrays
    sinTH = np.sin(TH)
    weight = (sinTH * dtheta * dphi).ravel()
    
    T_flat   = T.ravel()
    PH_flat  = PH.ravel()
    TH_flat  = TH.ravel()
    N_GRID   = T_flat.size

    alms = np.zeros((lmax+1, 2*lmax+1), dtype=np.complex128)

    # Pre-calculate all Y_lm on the grid in a vectorized way
    # This loop is slow but runs only ONCE. The original code's loop was 
    # INSIDE the K_VALUES loop, which was the main performance killer.
    # The new structure keeps this calc separate from the K-loop.
    print(f"        -> Generating {lmax+1}*{(2*lmax+1)} = {lmax*(lmax+2)+1} spherical harmonics... (One-time cost)")
    
    # Store all Y_lm in a single array (lmax+1, 2*lmax+1, N_GRID)
    Y_lms = np.zeros((lmax+1, 2*lmax+1, N_GRID), dtype=np.complex128)
    
    for l in range(lmax+1):
        for m in range(-l, l+1):
            # sph_harm is vectorized and calculates all N_GRID points at once
            Y_lms[l, m + lmax] = sph_harm(m, l, PH_flat, TH_flat)

    # Compute a_lm using vectorized dot product
    # a_lm = sum(T * Y_lm_conj * weight)
    print("        -> Computing a_lm via vectorized dot product...")
    
    # Calculate the complex conjugate of Y_lm * weight, and reshape 
    # to (N_GRID, total_alm_count) for a single dot product.
    # We transpose later to get the desired (lmax+1, 2*lmax+1) output.
    Y_lm_conj_weighted = np.conjugate(Y_lms).reshape(-1, N_GRID) * weight
    
    # The dot product (T_flat) * (Y_lm_conj_weighted) is faster than repeated loops
    # result shape is (total_alm_count,)
    alms_flat = np.dot(T_flat, Y_lm_conj_weighted.T) 
    
    # Reshape back to the original l, m layout
    alms = alms_flat.reshape(lmax+1, 2*lmax+1)

    return alms


def alm_correlation(alm0, alm1, lmax):
    """
    Compute overall complex correlation between two alm sets. (No Change)
    """
    num = 0 + 0j
    den0 = 0.0
    den1 = 0.0
    for l in range(lmax+1):
        for m in range(-l, l+1):
            # The indices are based on a fixed storage size (2*LMAX+1), not 2*l+1
            a0 = alm0[l, m + LMAX] # Use LMAX for index shift
            a1 = alm1[l, m + LMAX] # Use LMAX for index shift
            num  += a0 * np.conjugate(a1)
            den0 += np.abs(a0)**2
            den1 += np.abs(a1)**2
    if den0 == 0 or den1 == 0:
        return 0.0
    return num / np.sqrt(den0 * den1)


def alm_correlation_per_l(alm0, alm1, lmax):
    """
    Per-l correlation C_l between two alm sets. (No Change)
    """
    C_l = np.zeros(lmax+1, dtype=np.complex128)
    for l in range(lmax+1):
        num = 0 + 0j
        den0 = 0.0
        den1 = 0.0
        for m in range(-l, l+1):
            a0 = alm0[l, m + LMAX] # Use LMAX for index shift
            a1 = alm1[l, m + LMAX] # Use LMAX for index shift
            num  += a0 * np.conjugate(a1)
            den0 += np.abs(a0)**2
            den1 += np.abs(a1)**2
        if den0 == 0 or den1 == 0:
            C_l[l] = 0.0
        else:
            C_l[l] = num / np.sqrt(den0 * den1)
    return C_l


# ======================
# MAIN
# ======================

# Store the pre-calculated Y_lm/weight for reuse (major optimization)
Y_LM_CONJ_WEIGHTED = None

def compute_and_cache_ylm(TH, PH, lmax):
    """Generates and caches the core integration factor (Y_lm* * weight)."""
    global Y_LM_CONJ_WEIGHTED
    if Y_LM_CONJ_WEIGHTED is not None:
        return

    theta_1d = TH[:, 0]
    phi_1d   = PH[0, :]
    dtheta = theta_1d[1] - theta_1d[0]
    dphi   = phi_1d[1] - phi_1d[0]
    
    sinTH = np.sin(TH)
    weight = (sinTH * dtheta * dphi).ravel()
    PH_flat  = PH.ravel()
    TH_flat  = TH.ravel()
    N_GRID   = TH_flat.size

    Y_lms = np.zeros((lmax+1, 2*lmax+1, N_GRID), dtype=np.complex128)
    
    print(f"        -> Generating {lmax*(lmax+2)+1} spherical harmonics...")
    for l in range(lmax+1):
        for m in range(-l, l+1):
            Y_lms[l, m + lmax] = sph_harm(m, l, PH_flat, TH_flat)

    # Pre-calculate the combined factor, shaped for a fast dot product
    Y_LM_CONJ_WEIGHTED = np.conjugate(Y_lms).reshape(-1, N_GRID) * weight
    print("        -> Y_lm factors cached.")

def compute_alm_final(T, TH, PH, lmax):
    """Uses the cached factors for ultra-fast a_lm computation."""
    compute_and_cache_ylm(TH, PH, lmax) # Ensure cache is populated
    
    T_flat = T.ravel()
    
    # Fast dot product using cached factor
    alms_flat = np.dot(T_flat, Y_LM_CONJ_WEIGHTED.T) 
    
    # Reshape back to the original l, m layout (lmax+1, 2*lmax+1)
    return alms_flat.reshape(lmax+1, 2*lmax+1)


def main():
    global LMAX # Need global for use in alm_correlation

    print("[*] Loading CMB FITS...")
    data = fits.getdata(FITS_PATH)
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
    print(f"[*] nside inferred: {nside}, npix={npix}")

    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    print("[*] Building angular grid...")
    TH, PH = build_equatorial_grid(N_THETA, N_PHI)

    print("[*] Sampling original map (k=1)...")
    cmb_orig = healpix_sample(cmb, hpix, TH, PH)

    print("[*] Computing alm for original map (uses cache warm-up)...")
    alm_orig = compute_alm_final(cmb_orig, TH, PH, LMAX)

    # Scan over k
    C_values = []
    C_values_abs = []
    C_l_special = None

    print(f"[*] Starting scan over {len(K_VALUES)} k values...")
    for i, k in enumerate(K_VALUES):
        # Only print every 5th or 10th iteration to reduce I/O overhead
        if i % 5 == 0:
             print(f"    [-] k = {k:.6f}") 
        
        # NOTE: PH_src changes, so healpix_sample *must* run inside the loop
        PH_src = twist_phi(PH, k, mode=TWIST_MODE)
        cmb_tw = healpix_sample(cmb, hpix, TH, PH_src)
        
        # This is now much faster due to the pre-calculated Y_lm factors
        alm_tw = compute_alm_final(cmb_tw, TH, PH, LMAX)

        Ck = alm_correlation(alm_orig, alm_tw, LMAX)
        C_values.append(Ck)
        C_values_abs.append(np.abs(Ck))

        # store per-l if this is our special k
        if np.isclose(k, K_SPECIAL, atol=1e-6):
            C_l_special = alm_correlation_per_l(alm_orig, alm_tw, LMAX)

    C_values = np.array(C_values)
    C_values_abs = np.array(C_values_abs)

    # ======================
    # PLOTS (No Change)
    # ======================

    fig, ax = plt.subplots(2, 1, figsize=(8, 8), sharex=True, constrained_layout=True)

    ax[0].plot(K_VALUES, C_values_abs, label="|C(k)| multipole correlation")
    ax[0].axvline(1.0, color="k", linestyle="--", label="k = 1 (identity)")
    ax[0].axvline(K_SPECIAL, color="r", linestyle=":", label=f"k_special = {K_SPECIAL:.6f}")
    ax[0].set_ylabel("|C(k)|")
    ax[0].legend()
    ax[0].set_title(f"Multipole correlation vs twist, l_max = {LMAX}")

    ax[1].plot(K_VALUES, C_values.real, label="Re C(k)")
    ax[1].plot(K_VALUES, C_values.imag, label="Im C(k)", linestyle="--")
    ax[1].set_xlabel("Twist constant k")
    ax[1].set_ylabel("C(k)")
    ax[1].legend()

    plt.savefig("cmb_multipole_twist_spectrum.png")
    plt.close(fig)
    print("[*] Saved cmb_multipole_twist_spectrum.png")

    if C_l_special is not None:
        fig2, ax2 = plt.subplots(figsize=(8,4), constrained_layout=True)
        ell = np.arange(LMAX+1)
        ax2.plot(ell, np.abs(C_l_special), marker="o")
        ax2.set_xlabel("l")
        ax2.set_ylabel(f"|C_l(k={K_SPECIAL:.6f})|")
        ax2.set_title("Per-l multipole correlation at special k")
        plt.savefig("cmb_multipole_per_l_special_k.png")
        plt.close(fig2)
        print("[*] Saved cmb_multipole_per_l_special_k.png")
    else:
        print("[!] Special k not exactly sampled; adjust K_VALUES to hit it exactly.")


if __name__ == "__main__":
    main()