import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from astropy.coordinates import SkyCoord
import astropy.units as u
from PIL import Image
import os

# ======================================================
# CONFIG
# ======================================================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60                      # compute full alms
REMOVE_RANGE = (10, 40)        # strip L10-40
N_RES = 300
FRAMES = 120
DURATION = 80

K_MIN = -10
K_MAX = 100
K_SCAN = np.linspace(K_MIN, K_MAX, FRAMES)

ALMS = None
YLM = None
TH = None
PH = None

# ======================================================
# LOAD CMB & COMPUTE FULL ALMS
# ======================================================
def load_alm_grid():
    global ALMS, YLM, TH, PH

    print("[*] Loading FITS...")
    data = fits.getdata(FITS_PATH)
    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    # Patch NaN
    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hp = HEALPix(nside=nside, frame="galactic", order="ring")

    # Grid for alm extraction
    t = np.linspace(0, np.pi, LMAX * 4)
    p = np.linspace(-np.pi, np.pi, LMAX * 8, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t, p, indexing="ij")

    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hp.lonlat_to_healpix(coords.l, coords.b)
    T_s = cmb[ipix]

    dtheta = t[1]-t[0]
    dphi = p[1]-p[0]
    wts = np.sin(TH_ALM) * dtheta * dphi

    print("[*] Computing a_lm...")
    ALMS = {}
    for l in range(LMAX + 1):
        for m in range(-l, l+1):
            Y = sph_harm(m, l, PH_ALM, TH_ALM)
            ALMS[(l,m)] = np.sum(T_s * np.conjugate(Y) * wts)

    # Remove the stiffness band
    L1, L2 = REMOVE_RANGE
    for l in range(L1, L2+1):
        for m in range(-l, l+1):
            ALMS[(l,m)] = 0j

    # Prepare synthesis grid
    tt = np.linspace(0, np.pi, N_RES)
    pp = np.linspace(-np.pi, np.pi, N_RES)
    TH, PH = np.meshgrid(tt, pp, indexing="ij")

    print("[*] Precomputing Y_lm grid...")
    YLM = {}
    for l in range(LMAX+1):
        for m in range(-l, l+1):
            YLM[(l,m)] = sph_harm(m, l, PH, TH)

# ======================================================
# SYNTHESIS WITH TWIST
# ======================================================
def synthesize_twist(k):
    out = np.zeros_like(TH, dtype=np.complex128)
    phase = (k - 1.0) * PH

    for l in range(LMAX+1):
        for m in range(-l, l+1):
            alm = ALMS[(l,m)]
            if alm == 0j:
                continue
            Y = YLM[(l,m)]
            out += alm * Y * np.exp(1j * m * phase)

    return out.real

# ======================================================
# ANIMATION DRIVER
# ======================================================
def run():
    load_alm_grid()

    frames = []
    print("[*] Rendering frames...")

    for i, k in enumerate(K_SCAN):
        print(f"  Frame {i+1}/{FRAMES} | k={k:.3f}")

        Tmap = synthesize_twist(k)
        vis = np.power(np.abs(Tmap), 0.45)
        vmin, vmax = vis.min(), vis.max()

        fig, ax = plt.subplots(figsize=(10,6))
        im = ax.imshow(vis, extent=(-180,180,-90,90),
                       cmap='inferno',
                       norm=colors.Normalize(vmin=vmin, vmax=vmax),
                       origin='lower')
        ax.set_title(f"L10–40 Removed | Twist k = {k:.3f}")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        plt.colorbar(im, ax=ax, fraction=0.05)

        fname = f"temp_substrate_{i:03d}.png"
        plt.savefig(fname, dpi=100, bbox_inches='tight')
        plt.close(fig)

        with Image.open(fname) as img:
            frames.append(img.copy())

        os.remove(fname)

    outname = "cmb_substrate_twist_l10-40_removed.gif"
    frames[0].save(outname,
                   save_all=True,
                   append_images=frames[1:],
                   duration=DURATION,
                   loop=0)

    print(f"\n✅ Saved: {outname}")

if __name__ == "__main__":
    run()
