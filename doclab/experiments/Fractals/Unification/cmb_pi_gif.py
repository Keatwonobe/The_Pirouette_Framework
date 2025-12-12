import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord
from PIL import Image
import os

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

LMAX = 40          # harmonic cutoff
N_RES = 300        # map resolution
GIF_FRAMES = 150
GIF_DURATION = 60  # ms per frame (smaller = faster)

# <<< TUNE THIS RANGE TO WHATEVER YOU WANT TO SCAN >>>
# Right now: a tight scan around k = 1.0
K_RANGE = np.linspace(0.999, 1.001, GIF_FRAMES, endpoint=True)

# ======================
# GLOBAL CACHE
# ======================
YLM_CACHE = None
ALMS_CACHE = None
TH_GRID = None
PH_GRID = None


# ======================
# 1. ALM + GRID SETUP
# ======================
def get_alm_and_grid(fits_path, lmax, n_res):
    """
    Loads the SMICA CMB map, computes a_lm up to lmax, and
    precomputes Y_lm(theta, phi) on an n_res x n_res synthesis grid.
    """
    global YLM_CACHE, ALMS_CACHE, TH_GRID, PH_GRID

    if ALMS_CACHE is not None:
        return  # already cached

    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {fits_path}")
        return

    # Extract CMB temperature component
    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    # Fill NaNs with map mean
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # Integration grid for a_lm
    n_theta_alm = lmax * 4
    n_phi_alm = lmax * 8

    theta_alm = np.linspace(0, np.pi, n_theta_alm)
    phi_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(theta_alm, phi_alm, indexing="ij")

    lon_deg = np.rad2deg((PH_ALM + 2 * np.pi) % (2 * np.pi))
    lat_deg = np.rad2deg(0.5 * np.pi - TH_ALM)

    coords = SkyCoord(l=lon_deg * u.deg, b=lat_deg * u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]

    dtheta = theta_alm[1] - theta_alm[0]
    dphi = phi_alm[1] - phi_alm[0]
    weights = np.sin(TH_ALM) * dtheta * dphi

    # Compute a_lm
    print(f"[*] Computing a_lm (lmax={lmax})...")
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)

    ALMS_CACHE = alms

    # Synthesis grid (for plotting maps)
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing="ij")

    # Cache Y_lm on synthesis grid
    print(f"[*] Caching Y_lm on {n_res}x{n_res} grid...")
    YLM_CACHE = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            YLM_CACHE[(l, m)] = sph_harm(m, l, PH_GRID, TH_GRID)


# ======================
# 2. FAST SYNTHESIS WITH TWIST
# ======================
def synthesize_twisted_universe_fast(k, lmax):
    """
    Re-synthesize the CMB map for a given twist k by
    applying a phase factor exp(i * m * (k-1) * phi).
    """
    if TH_GRID is None or ALMS_CACHE is None:
        return np.zeros((N_RES, N_RES))

    # delta_phi = (k - 1) * phi, so k=1 -> identity
    delta_phi_multiplier = (k - 1.0) * PH_GRID
    out = np.zeros_like(TH_GRID, dtype=np.complex128)

    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            alm = ALMS_CACHE.get((l, m), 0.0)
            Y_lm_untwisted = YLM_CACHE.get((l, m))
            if Y_lm_untwisted is None:
                continue

            phase = np.exp(1j * m * delta_phi_multiplier)
            out += alm * Y_lm_untwisted * phase

    return out.real


# ======================
# 3. MOTION-ONLY Δ-MAP GIF
# ======================
def run_motion_delta_gif():
    """
    Generates a GIF of |ΔI| between successive k slices, where
    I(k) = |T_ref - T_twist(k)|.
    This highlights only the parts of the sky where the interference
    pattern is CHANGING as you twist k.
    """
    get_alm_and_grid(FITS_PATH, LMAX, N_RES)
    if ALMS_CACHE is None:
        return

    print("\n[*] Starting motion-only ΔI(k) GIF generation...")
    print(f"    k-range: {K_RANGE[0]:.6f} -> {K_RANGE[-1]:.6f}")
    gamma = 0.5  # power-law to enhance faint structure

    # Reference map (k = 1) used for interference
    print("[*] Synthesizing T_ref (k = 1.0)...")
    T_ref = synthesize_twisted_universe_fast(1.0, LMAX)

    # -------- Pre-pass: find global max for normalization --------
    print("[*] Pre-pass to estimate ΔI dynamic range...")
    prev_I = None
    max_val = 0.0

    for k in K_RANGE:
        T_twist = synthesize_twisted_universe_fast(k, LMAX)
        I_map = np.abs(T_ref - T_twist)

        if prev_I is not None:
            dI = np.abs(I_map - prev_I)
            vis = np.power(dI, gamma)
            local_max = vis.max()
            if local_max > max_val:
                max_val = local_max

        prev_I = I_map

    if max_val <= 0:
        max_val = 1.0

    v_min, v_max = 0.0, max_val
    print(f"    ΔI vis range (after gamma): [{v_min:.4e}, {v_max:.4e}]")

    # -------- Second pass: build GIF frames --------
    frames = []
    prev_I = None

    for i, k in enumerate(K_RANGE):
        T_twist = synthesize_twisted_universe_fast(k, LMAX)
        I_map = np.abs(T_ref - T_twist)

        if prev_I is None:
            # First frame: no previous slice yet
            dI = np.zeros_like(I_map)
        else:
            dI = np.abs(I_map - prev_I)

        prev_I = I_map

        # Enhance and normalize
        vis = np.power(dI, gamma)

        fig, ax = plt.subplots(figsize=(10, 6.2))
        extent = (-180, 180, -90, 90)

        im = ax.imshow(
            vis,
            extent=extent,
            cmap="inferno",
            norm=colors.Normalize(vmin=v_min, vmax=v_max),
            origin="lower",
        )

        ax.set_title(
            r"Motion-only $\Delta I(k)$   (between successive k slices)"
            f"\nCurrent k = {k:.9f}",
            fontsize=14,
        )
        ax.set_xlabel("Galactic Longitude (deg)")
        ax.set_ylabel("Galactic Latitude (deg)")

        cb = plt.colorbar(
            im,
            ax=ax,
            fraction=0.046,
            pad=0.04,
            label=r"$|\Delta I|$ (enhanced)",
        )

        if (i + 1) % 15 == 0 or i == 0 or i == len(K_RANGE) - 1:
            print(f"  [-] Frame {i+1}/{len(K_RANGE)} at k={k:.9f}")

        # Save to temp PNG then into buffer
        tmp_name = f"temp_delta_frame_{i:03d}.png"
        plt.savefig(tmp_name, bbox_inches="tight", dpi=100)
        plt.close(fig)

        with Image.open(tmp_name) as img:
            frames.append(img.copy())
        os.remove(tmp_name)

    if frames:
        out_name = f"cmb_delta_motion_interference_lmax{LMAX}.gif"
        frames[0].save(
            out_name,
            save_all=True,
            append_images=frames[1:],
            duration=GIF_DURATION,
            loop=0,
        )
        print(f"\n✅ Motion-only ΔI GIF saved as: {out_name}")
    else:
        print("[!] No frames generated; something went wrong.")


if __name__ == "__main__":
    run_motion_delta_gif()
