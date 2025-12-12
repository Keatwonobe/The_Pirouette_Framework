import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.special import sph_harm, sph_harm_y
from PIL import Image
import warnings
import os
import sys

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ============================================================
# CONFIG
# ============================================================
FITS_PATH   = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX        = 40

# Substrate = everything EXCEPT the stiff mid-band
REMOVE_BAND = (10, 40)   # (L1, L2)

# Synthesis grid
N_TH_SYN = 180
N_PH_SYN = 360

# Twist scan
K_MIN, K_MAX = -1.5, 4.0
N_K          = 121
K_VALUES     = np.linspace(K_MIN, K_MAX, N_K)

# Cache file for a_lm
ALM_CACHE = f"cmb_alms_lmax{LMAX}.npz"

# Output GIF
GIF_NAME  = "cmb_substrate_helical_scanner5.gif"


# ============================================================
# HELPER: spherical harmonic wrapper
# ============================================================
def get_ylm(m, l, phi, theta):
    """
    Wrapper that prefers sph_harm_y if present (faster / better behaved),
    otherwise falls back to sph_harm.
    NOTE SciPy's sph_harm convention is (m, l, phi, theta).
    """
    try:
        return sph_harm_y(l, m, phi, theta)
    except TypeError:
        return sph_harm(m, l, phi, theta)


# ============================================================
# STEP 1: Load CMB and compute a_lm (with caching)
# ============================================================
def load_cmb_and_alms(fits_path, lmax):
    """
    Compute a_lm up to lmax from the SMICA CMB map using quadrature
    on a HEALPix grid. Cache the result for future runs.
    """
    if os.path.exists(ALM_CACHE):
        print(f"[*] Loading cached a_lm from {ALM_CACHE}...")
        data = np.load(ALM_CACHE)
        alms = {}
        Ls   = data["L"]
        Ms   = data["M"]
        Re   = data["Re"]
        Im   = data["Im"]
        for L, M, r, im in zip(Ls, Ms, Re, Im):
            alms[(int(L), int(M))] = r + 1j * im
        return alms

    print(f"[*] Computing a_lm up to L={lmax} from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    # Handle SMICA column structure
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

    nside = int(np.sqrt(cmb.size / 12))
    hpix  = HEALPix(nside=nside, order="ring", frame="galactic")

    # Integration grid (quadrature)
    n_theta = lmax * 4
    n_phi   = lmax * 8
    theta   = np.linspace(0, np.pi, n_theta)
    phi     = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH  = np.meshgrid(theta, phi, indexing="ij")

    lon = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix   = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_s    = cmb[ipix]

    dtheta = theta[1] - theta[0]
    dphi   = phi[1]   - phi[0]
    weights = np.sin(TH) * dtheta * dphi

    alms = {}
    for l in range(lmax + 1):
        sum_alm_sq = 0.0
        for m in range(-l, l + 1):
            Y = get_ylm(m, l, PH, TH)
            val = np.sum(T_s * np.conjugate(Y) * weights)
            alms[(l, m)] = val
            sum_alm_sq += np.abs(val) ** 2
        # optional: could store C_l if you want
        # cl[l] = sum_alm_sq / (2*l + 1)

    # Cache to disk
    Ls, Ms, Re, Im = [], [], [], []
    for (l, m), v in alms.items():
        Ls.append(l); Ms.append(m)
        Re.append(v.real); Im.append(v.imag)
    np.savez(ALM_CACHE, L=np.array(Ls), M=np.array(Ms),
             Re=np.array(Re), Im=np.array(Im))
    print(f"[*] Saved a_lm cache to {ALM_CACHE}")

    return alms


# ============================================================
# STEP 2: Build helical mode maps (per-m pre-aggregation)
# ============================================================
def build_mode_maps(alms, lmax, remove_band=None):
    """
    Precompute M_m(θ,φ) = Σ_l a_lm Y_lm(θ,φ) on a synthesis grid.

    If remove_band = (L1, L2), modes in that band are excluded
    (used to isolate the substrate by removing L=10–40).
    """
    theta = np.linspace(0, np.pi, N_TH_SYN)
    phi   = np.linspace(-np.pi, np.pi, N_PH_SYN, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")

    mode_maps = {m: np.zeros_like(TH, dtype=np.complex128)
                 for m in range(-lmax, lmax + 1)}

    for l in range(lmax + 1):
        if remove_band is not None:
            L1, L2 = remove_band
            if L1 <= l <= L2:
                continue

        for m in range(-l, l + 1):
            alm = alms.get((l, m), 0j)
            if alm == 0j:
                continue
            Y = get_ylm(m, l, PH, TH)
            mode_maps[m] += alm * Y

    return mode_maps, TH, PH


# ============================================================
# STEP 3: Helical synthesis
# ============================================================
def synthesize_helical(mode_maps, PH, k_twist):
    """
    Helical twist synthesis:
        T_k(θ,φ) = Re Σ_m M_m(θ,φ) e^{i m (k−1) φ}
    where M_m are pre-aggregated per-m maps.
    """
    twist = k_twist - 1.0
    out   = np.zeros_like(PH, dtype=np.complex128)

    if abs(twist) < 1e-15:
        # Fast path for k=1
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


# ============================================================
# STEP 4: Frame normalization helper
# ============================================================
def normalize_frame(arr, vmin=None, vmax=None):
    """
    Normalize a frame to [0,1] using either fixed or percentile bounds.
    """
    a = arr.copy()
    if vmin is None or vmax is None:
        lo, hi = np.percentile(a, [2, 98])
    else:
        lo, hi = vmin, vmax
    a = np.clip(a, lo, hi)
    if hi > lo:
        a = (a - lo) / (hi - lo)
    else:
        a[:] = 0.0
    return a


# ============================================================
# MAIN SCANNER 5
# ============================================================
def main():
    print("=== Helical Scanner 5 : Substrate Twist Evolution ===")
    print(f"LMAX = {LMAX}, removing L={REMOVE_BAND[0]}–{REMOVE_BAND[1]} band.")

    # 1. Load / compute a_lm
    alms = load_cmb_and_alms(FITS_PATH, LMAX)

    # 2. Build substrate-only helical modes
    print("[*] Building substrate helical mode maps...")
    mode_maps, TH, PH = build_mode_maps(alms, LMAX, remove_band=REMOVE_BAND)

    # 3. Reference substrate map at k=1 (no twist)
    print("[*] Synthesizing reference substrate (k=1)...")
    T_ref = synthesize_helical(mode_maps, PH, k_twist=1.0)
    T_ref -= T_ref.mean()

    # 4. Generate frames over k
    frames = []
    lon = np.linspace(-180, 180, N_PH_SYN)
    lat = np.linspace(-90,  90, N_TH_SYN)
    extent = [lon.min(), lon.max(), lat.min(), lat.max()]

    print(f"[*] Scanning k from {K_MIN} to {K_MAX} ({N_K} steps)...")
    for i, k in enumerate(K_VALUES):
        sys.stdout.write(f"\r[>] k = {k:.3f}  ({i+1}/{N_K})")
        sys.stdout.flush()

        T_k = synthesize_helical(mode_maps, PH, k_twist=k)
        T_k -= T_k.mean()

        diff = np.abs(T_ref - T_k)
        diff_norm = normalize_frame(diff)

        # Plot to PNG
        fig, ax = plt.subplots(figsize=(10, 5))
        im = ax.imshow(diff_norm.T,
                       origin="lower",
                       extent=extent,
                       cmap="inferno",
                       aspect="auto")
        ax.set_title(f"L{REMOVE_BAND[0]}–{REMOVE_BAND[1]} Removed | "
                     f"Substrate | k = {k:.3f}")
        ax.set_xlabel("Galactic Longitude (deg)")
        ax.set_ylabel("Galactic Latitude (deg)")

        # optional vertical meridian line if you want it:
        ax.axvline(0, color="black", linewidth=0.5, alpha=0.5)

        plt.tight_layout()
        fname = f"scanner5_frame_{i:03d}.png"
        plt.savefig(fname, dpi=120)
        plt.close(fig)

        with Image.open(fname) as pim:
            frames.append(pim.convert("P", palette=Image.ADAPTIVE))
        os.remove(fname)

    print(f"\n[*] Saving GIF to {GIF_NAME}...")
    frames[0].save(
        GIF_NAME,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=80,   # ms per frame
        loop=0
    )
    print("✅ Done. Scanner 5 substrate evolution GIF written.")


if __name__ == "__main__":
    main()
