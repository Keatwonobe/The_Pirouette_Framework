import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.special import sph_harm, sph_harm_y
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX      = 40

# grid for a_lm extraction
N_TH_ALM  = LMAX * 4
N_PH_ALM  = LMAX * 8

# grid for synthesis / correlations
N_TH_SYN  = 180
N_PH_SYN  = 360

K_MIN, K_MAX = -1.5, 4.0
N_K = 121
K_SCAN = np.linspace(K_MIN, K_MAX, N_K)

# ---------------------- helpers ----------------------
def get_ylm(m, l, phi, theta):
    """Handle SciPy's sph_harm vs sph_harm_y."""
    try:
        return sph_harm_y(l, m, phi, theta)
    except TypeError:
        return sph_harm(m, l, phi, theta)

def load_cmb_and_alms():
    """Load SMICA map and compute a_lm up to LMAX using quadrature."""
    data = fits.getdata(FITS_PATH)
    if isinstance(data, np.ndarray) and data.dtype.fields:
        if "I" in data.dtype.names:
            cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names:
            cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else:
            cmb = np.array(data[data.dtype.names[0]], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size/12))
    hp    = HEALPix(nside=nside, order="ring", frame="galactic")

    theta = np.linspace(0, np.pi, N_TH_ALM)
    phi   = np.linspace(-np.pi, np.pi, N_PH_ALM, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")

    lon = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix   = hp.lonlat_to_healpix(coords.l, coords.b)
    T_s    = cmb[ipix]

    dtheta = theta[1]-theta[0]
    dphi   = phi[1]-phi[0]
    wts    = np.sin(TH) * dtheta * dphi

    alms = {}
    for l in range(LMAX+1):
        for m in range(-l, l+1):
            Y = get_ylm(m, l, PH, TH)
            alms[(l, m)] = np.sum(T_s * np.conjugate(Y) * wts)

    return cmb, alms

def build_mode_maps(alms, remove_band=None):
    """
    Precompute per-m mode maps on a synthesis grid:
      M_m(θ,φ) = sum_l a_lm Y_lm(θ,φ)
    Optionally zero out a band L1≤l≤L2.
    """
    theta = np.linspace(0, np.pi, N_TH_SYN)
    phi   = np.linspace(-np.pi, np.pi, N_PH_SYN, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")

    mode_maps = {m: np.zeros_like(TH, dtype=np.complex128)
                 for m in range(-LMAX, LMAX+1)}

    for l in range(LMAX+1):
        if remove_band is not None:
            L1, L2 = remove_band
            if L1 <= l <= L2:
                continue

        for m in range(-l, l+1):
            alm = alms.get((l, m), 0j)
            if alm == 0j:
                continue
            Y = get_ylm(m, l, PH, TH)
            mode_maps[m] += alm * Y

    return mode_maps, TH, PH

def synthesize_from_modes(mode_maps, PH, k_twist):
    """
    Helical twist synthesis:
      T_k(θ,φ) = Re Σ_m M_m(θ,φ) e^{i m (k−1) φ}
    """
    twist = k_twist - 1.0
    out   = np.zeros_like(PH, dtype=np.complex128)

    if abs(twist) < 1e-15:
        for M in mode_maps.values():
            out += M
        return out.real

    phi = PH
    for m, M in mode_maps.items():
        if not np.any(M):
            continue
        phase = np.exp(1j * m * twist * phi)
        out  += M * phase

    return out.real

def map_corr(ref, other):
    """Pearson correlation between two sky maps."""
    a = ref.ravel() - ref.mean()
    b = other.ravel() - other.mean()
    denom = np.sqrt((a*a).sum() * (b*b).sum())
    if denom == 0:
        return 0.0
    return float((a*b).sum() / denom)

# ---------------------- main scan ----------------------
def main():
    print("[*] Loading CMB and computing a_lm...")
    cmb, alms = load_cmb_and_alms()

    print("[*] Building mode maps: full field...")
    modes_full, TH, PH = build_mode_maps(alms, remove_band=None)

    print("[*] Building mode maps: L10–40 removed...")
    modes_sub, _, _ = build_mode_maps(alms, remove_band=(10, 40))

    print("[*] Building mode maps: random-phase fake...")
    rng = np.random.default_rng(1234)
    alms_fake = {}
    for (l, m), val in alms.items():
        amp   = np.abs(val)
        phase = rng.uniform(0, 2*np.pi)
        alms_fake[(l, m)] = amp * np.exp(1j * phase)
    modes_fake, _, _ = build_mode_maps(alms_fake, remove_band=None)

    print("[*] Synthesizing reference maps at k=1 (no twist)...")
    Tref_full = synthesize_from_modes(modes_full, PH, k_twist=1.0)
    Tref_sub  = synthesize_from_modes(modes_sub,  PH, k_twist=1.0)
    Tref_fake = synthesize_from_modes(modes_fake, PH, k_twist=1.0)

    corr_full, corr_sub, corr_fake = [], [], []

    print("[*] Scanning k and computing correlations...")
    for k in K_SCAN:
        Tk_full = synthesize_from_modes(modes_full, PH, k)
        Tk_sub  = synthesize_from_modes(modes_sub,  PH, k)
        Tk_fake = synthesize_from_modes(modes_fake, PH, k)

        corr_full.append(map_corr(Tref_full, Tk_full))
        corr_sub.append(map_corr(Tref_sub,   Tk_sub))
        corr_fake.append(map_corr(Tref_fake, Tk_fake))

    corr_full = np.array(corr_full)
    corr_sub  = np.array(corr_sub)
    corr_fake = np.array(corr_fake)

    np.savez("twist_correlations.npz",
             k=K_SCAN,
             corr_full=corr_full,
             corr_sub=corr_sub,
             corr_fake=corr_fake)

    print("[*] Plotting...")
    plt.figure(figsize=(10, 6))
    plt.plot(K_SCAN, corr_full, label="Real CMB (full L≤40)", linewidth=2)
    plt.plot(K_SCAN, corr_sub,  label="Real CMB with L10–40 removed", linewidth=2)
    plt.plot(K_SCAN, corr_fake, label="Random-phase fake (full L≤40)", linestyle="--")

    plt.axvline(0.9,  color="gray",  linestyle=":", label="Traveler ~0.9")
    plt.axvline(np.pi, color="green", linestyle=":", label="π")

    plt.xlabel("Twist index k")
    plt.ylabel("Correlation with k=1 map")
    plt.title("Helical Twist Correlation vs k (LMAX=40)")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("twist_correlation_scan_helical.png", dpi=150)
    print("✅ Saved twist_correlation_scan_helical.png")

if __name__ == "__main__":
    main()
