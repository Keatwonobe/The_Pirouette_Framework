import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
import os
from PIL import Image
import sys

# ======================================================
# CONFIG
# ======================================================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

LMAX        = 40           # same low-L ceiling you used
REMOVE_L1   = 10           # strip L=10..40
REMOVE_L2   = 40

N_TH        = 240          # sky grid resolution (lat)
N_PH        = 480          # sky grid resolution (lon)

K_MIN       = -1.5
K_MAX       = 4.0
FRAMES      = 120
K_SCAN      = np.linspace(K_MIN, K_MAX, FRAMES)

GIF_NAME    = "cmb_substrate_twist_L10-40_removed_helical.gif"
FRAME_DUR   = 60  # ms per frame

# ======================================================
# SPHERICAL HARMONICS WRAPPER (your helical impl base)
# ======================================================
try:
    # SciPy >= 1.15
    from scipy.special import sph_harm_y

    def my_sph_harm(m, l, phi_az, theta_pol):
        # match your convention: (m, l, phi, theta)
        return sph_harm_y(l, m, phi_az, theta_pol)

except ImportError:
    # fallback: older SciPy
    from scipy.special import sph_harm as _sph_harm

    def my_sph_harm(m, l, phi_az, theta_pol):
        return _sph_harm(m, l, phi_az, theta_pol)

# ======================================================
# 1. EXTRACT a_lm ONCE (same idea as your scanners)
# ======================================================
def extract_alms(fits_path, lmax):
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # integration grid (coarser than nside; only for alms)
    n_theta = lmax * 4
    n_phi   = lmax * 8
    theta_grid = np.linspace(0.0, np.pi, n_theta)
    phi_grid   = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta_grid, phi_grid, indexing="ij")

    print("[*] Sampling CMB on integration grid...")
    lon_deg = np.rad2deg((PH + 2.0*np.pi) % (2.0*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords  = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix    = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_s     = cmb[ipix]

    dtheta = theta_grid[1] - theta_grid[0]
    dphi   = phi_grid[1]   - phi_grid[0]
    weights = np.sin(TH) * dtheta * dphi

    print(f"[*] Extracting a_lm up to LMAX={lmax}...")
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = my_sph_harm(m, l, PH, TH)
            val  = np.sum(T_s * np.conjugate(Y_lm) * weights)
            alms[(l, m)] = val

    return alms

# ======================================================
# 2. BUILD PER-m MODE MAPS (2D generalization of your
#    mode_lines helical compression)
# ======================================================
def build_mode_maps(alms, lmax, n_th, n_ph,
                    remove_l1=None, remove_l2=None):
    """
    mode_maps[m] = sum_{l >= |m|, l not in [remove_l1, remove_l2]}
                       a_lm Y_lm(theta, phi)
    """
    print("[*] Building mode maps on full sky grid...")
    theta = np.linspace(0.0, np.pi, n_th)
    phi   = np.linspace(-np.pi, np.pi, n_ph, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")  # TH,PH: (n_th, n_ph)

    mode_maps = {m: np.zeros((n_th, n_ph), dtype=np.complex128)
                 for m in range(-lmax, lmax + 1)}

    for l in range(lmax + 1):
        if remove_l1 is not None and remove_l2 is not None:
            if remove_l1 <= l <= remove_l2:
                continue  # strip L10–40 from the substrate

        for m in range(-l, l + 1):
            alm = alms.get((l, m), 0j)
            if alm == 0j:
                continue
            Y_lm = my_sph_harm(m, l, PH, TH)
            mode_maps[m] += alm * Y_lm

    return mode_maps, TH, PH

# ======================================================
# 3. FAST TWIST SYNTHESIS USING MODE MAPS
# ======================================================
def synthesize_map_from_modes(mode_maps, PH, k_twist=1.0):
    """
    T_k(theta,phi) = Re sum_m M_m(theta,phi) * exp(i m (k-1) phi)
    """
    twist = k_twist - 1.0
    signal = np.zeros_like(PH, dtype=np.complex128)

    if abs(twist) < 1e-15:
        # identity twist → just sum all mode maps
        for m, M in mode_maps.items():
            signal += M
        return signal.real

    phi = PH
    for m, M in mode_maps.items():
        if not np.any(M):
            continue
        phase = np.exp(1j * m * twist * phi)
        signal += M * phase

    return signal.real

# ======================================================
# 4. DRIVER: BUILD GIF OVER k
# ======================================================
def main():
    alms = extract_alms(FITS_PATH, LMAX)

    mode_maps, TH, PH = build_mode_maps(
        alms, LMAX, N_TH, N_PH,
        remove_l1=REMOVE_L1,
        remove_l2=REMOVE_L2
    )

    frames = []
    print(f"[*] Rendering {FRAMES} frames from k={K_MIN} to {K_MAX}...")

    # For consistent color scaling, sample a few k's
    sample_ks = np.linspace(K_MIN, K_MAX, 10)
    vals = []
    for k in sample_ks:
        Tk = synthesize_map_from_modes(mode_maps, PH, k_twist=k)
        vals.append(np.abs(Tk))
    vals = np.concatenate([v.ravel() for v in vals])
    vmin, vmax = np.percentile(vals, [1, 99])

    for i, k in enumerate(K_SCAN):
        print(f"  [>] Frame {i+1}/{FRAMES} | k={k:.3f}")
        Tk = synthesize_map_from_modes(mode_maps, PH, k_twist=k)
        vis = np.abs(Tk) ** 0.45  # contrast stretch

        fig, ax = plt.subplots(figsize=(10, 6))
        im = ax.imshow(
            vis,
            extent=(-180, 180, -90, 90),
            origin="lower",
            cmap="inferno",
            vmin=vmin, vmax=vmax,
            aspect="auto",
        )
        ax.set_title(f"Substrate Twist (L=0–9,>40 only) | k={k:.3f}")
        ax.set_xlabel("Galactic Longitude (deg)")
        ax.set_ylabel("Galactic Latitude (deg)")
        plt.colorbar(im, ax=ax, fraction=0.05)

        fname = f"_substrate_frame_{i:03d}.png"
        plt.savefig(fname, dpi=100, bbox_inches="tight")
        plt.close(fig)

        with Image.open(fname) as img:
            frames.append(img.copy())
        os.remove(fname)

    print(f"[*] Writing GIF: {GIF_NAME}")
    frames[0].save(
        GIF_NAME,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DUR,
        loop=0,
    )
    print("✅ Done.")

if __name__ == "__main__":
    main()
