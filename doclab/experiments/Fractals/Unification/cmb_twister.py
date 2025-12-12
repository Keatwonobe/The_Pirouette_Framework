import numpy as np
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt
from scipy.special import sph_harm

# ======================
# CONFIG
# ======================

FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

TWIST_MODE = "untwist"   # "twist" or "untwist"

# For multipole work, use a *reduced* grid to keep runtime reasonable.
# You can bump these once everything works.
N_THETA = 256
N_PHI   = 512

LMAX   = 40    # spherical harmonic cutoff
# k scan region around 1; refine as desired
K_VALUES = np.linspace(0.95, 1.05, 41)
K_SPECIAL = 1.0072973525643  # fine structure “1+alpha”


# ======================
# TWIST & SAMPLING HELPERS
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
# SPHERICAL HARMONICS
# ======================

def compute_alm(T, TH, PH, lmax):
    """
    Compute a_lm up to lmax using simple quadrature on the (TH, PH) grid.
    T, TH, PH shapes: (N_THETA, N_PHI)
    Returns alms as array alm[l, m+l] (so index m from -l..+l is shifted by +l).
    """
    # assume uniform sampling
    theta_1d = TH[:, 0]
    phi_1d   = PH[0, :]
    dtheta = theta_1d[1] - theta_1d[0]
    dphi   = phi_1d[1] - phi_1d[0]

    sinTH = np.sin(TH)

    alms = np.zeros((lmax+1, 2*lmax+1), dtype=np.complex128)

    # Flatten once to speed up dot products
    T_flat   = T.ravel()
    sin_flat = sinTH.ravel()
    PH_flat  = PH.ravel()
    TH_flat  = TH.ravel()

    weight = sin_flat * dtheta * dphi

    for l in range(lmax+1):
        for m in range(-l, l+1):
            Y_lm = sph_harm(m, l, PH_flat, TH_flat)  # (phi, theta) order
            integrand = T_flat * np.conjugate(Y_lm) * weight
            alm = np.sum(integrand)
            alms[l, m + lmax] = alm  # store shifted by +lmax so shape fixed

    return alms


def alm_correlation(alm0, alm1, lmax):
    """
    Compute overall complex correlation between two alm sets.
    """
    # restrict to physical region: for each l, m in [-l, +l]
    num = 0 + 0j
    den0 = 0.0
    den1 = 0.0
    for l in range(lmax+1):
        for m in range(-l, l+1):
            a0 = alm0[l, m + lmax]
            a1 = alm1[l, m + lmax]
            num  += a0 * np.conjugate(a1)
            den0 += np.abs(a0)**2
            den1 += np.abs(a1)**2
    if den0 == 0 or den1 == 0:
        return 0.0
    return num / np.sqrt(den0 * den1)


def alm_correlation_per_l(alm0, alm1, lmax):
    """
    Per-l correlation C_l between two alm sets.
    Returns array C_l (complex).
    """
    C_l = np.zeros(lmax+1, dtype=np.complex128)
    for l in range(lmax+1):
        num = 0 + 0j
        den0 = 0.0
        den1 = 0.0
        for m in range(-l, l+1):
            a0 = alm0[l, m + lmax]
            a1 = alm1[l, m + lmax]
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

def main():
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

    print("[*] Computing alm for original map...")
    alm_orig = compute_alm(cmb_orig, TH, PH, LMAX)

    # Scan over k
    C_values = []
    C_values_abs = []
    C_l_special = None

    for k in K_VALUES:
        print(f"    [-] k = {k:.6f}")
        PH_src = twist_phi(PH, k, mode=TWIST_MODE)
        cmb_tw = healpix_sample(cmb, hpix, TH, PH_src)
        alm_tw = compute_alm(cmb_tw, TH, PH, LMAX)

        Ck = alm_correlation(alm_orig, alm_tw, LMAX)
        C_values.append(Ck)
        C_values_abs.append(np.abs(Ck))

        # store per-l if this is our special k
        if np.isclose(k, K_SPECIAL, atol=1e-6):
            C_l_special = alm_correlation_per_l(alm_orig, alm_tw, LMAX)

    C_values = np.array(C_values)
    C_values_abs = np.array(C_values_abs)

    # ======================
    # PLOTS
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
