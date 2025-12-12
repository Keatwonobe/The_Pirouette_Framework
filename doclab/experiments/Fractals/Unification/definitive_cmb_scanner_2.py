#!/usr/bin/env python
"""
cmb_substrate_decomp_6view.py

Decompose the CMB into:
  - pure L=10 shell
  - pure L=20 shell
  - pure L=30 shell
  - pure L=40 shell
  - substrate (L10–40 removed) at a given k
  - substrate manifold / distortion view (|T|^0.45) at another k

Outputs a single 3×2 PNG figure.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
import os

# -----------------------------
# SciPy spherical harmonics wrapper
# -----------------------------
try:
    from scipy.special import sph_harm_y

    def my_sph_harm(m, l, phi_az, theta_pol):
        """
        Wrapper giving the same calling convention we like:
            my_sph_harm(m, l, phi, theta)

        New SciPy: sph_harm_y(l, m, theta_pol, phi_az)
        """
        return sph_harm_y(l, m, theta_pol, phi_az)

except ImportError:
    from scipy.special import sph_harm as _sph_harm

    def my_sph_harm(m, l, phi_az, theta_pol):
        # Old SciPy signature: sph_harm(m, l, theta_az, phi_pol)
        return _sph_harm(m, l, phi_az, theta_pol)


# ======================================================
# CONFIG
# ======================================================
FITS_PATH    = "COM_CompMap_CMB-smica_2048_R1.20.fits"

LMAX         = 60          # compute full a_lm up to here
REMOVE_RANGE = (10, 40)    # define substrate band to strip

N_RES        = 300         # synthesis map resolution

# k-values for the views
K_SHELL      = 0.5         # twist for the pure shells + substrate map
K_MANIFOLD   = -1.5        # twist for the manifold/distortion view

# Globals filled by load_alm_grid()
ALMS_FULL = None   # all alms
ALMS_SUB  = None   # with L in REMOVE_RANGE stripped
YLM       = None
TH        = None
PH        = None


# ======================================================
# LOAD CMB & COMPUTE FULL a_lm, PRECOMPUTE Y_lm GRID
# ======================================================
def load_alm_grid():
    global ALMS_FULL, ALMS_SUB, YLM, TH, PH

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
    t_alm = np.linspace(0, np.pi, LMAX * 4)
    p_alm = np.linspace(-np.pi, np.pi, LMAX * 8, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing="ij")

    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hp.lonlat_to_healpix(coords.l, coords.b)
    T_s = cmb[ipix]

    dtheta = t_alm[1] - t_alm[0]
    dphi   = p_alm[1] - p_alm[0]
    wts    = np.sin(TH_ALM) * dtheta * dphi

    print("[*] Computing a_lm...")
    ALMS_FULL = {}
    for l in range(LMAX + 1):
        for m in range(-l, l+1):
            Y = my_sph_harm(m, l, PH_ALM, TH_ALM)
            ALMS_FULL[(l, m)] = np.sum(T_s * np.conjugate(Y) * wts)

    # Substrate alms: copy, then zero out the stiffness band
    ALMS_SUB = ALMS_FULL.copy()
    L1, L2 = REMOVE_RANGE
    for l in range(L1, L2 + 1):
        for m in range(-l, l+1):
            ALMS_SUB[(l, m)] = 0j

    # Prepare synthesis grid
    tt = np.linspace(0, np.pi, N_RES)
    pp = np.linspace(-np.pi, np.pi, N_RES)
    TH_, PH_ = np.meshgrid(tt, pp, indexing="ij")
    TH = TH_
    PH = PH_

    print("[*] Precomputing Y_lm grid...")
    YLM = {}
    for l in range(LMAX + 1):
        for m in range(-l, l+1):
            YLM[(l, m)] = my_sph_harm(m, l, PH, TH)

    # Store globals
    globals()["ALMS_FULL"] = ALMS_FULL
    globals()["ALMS_SUB"]  = ALMS_SUB
    globals()["YLM"]       = YLM
    globals()["TH"]        = TH
    globals()["PH"]        = PH


# ======================================================
# SYNTHESIS HELPERS
# ======================================================
def synthesize_twist(k, alms_dict):
    """
    Synthesize T(theta,phi;k) = sum_{l,m} a_lm * Y_lm(theta,phi) * e^{i m (k-1) phi}.
    """
    out = np.zeros_like(TH, dtype=np.complex128)
    phase = (k - 1.0) * PH

    for l in range(LMAX + 1):
        for m in range(-l, l+1):
            alm = alms_dict.get((l, m), 0j)
            if alm == 0j:
                continue
            Y = YLM[(l, m)]
            out += alm * Y * np.exp(1j * m * phase)

    return out.real


def synthesize_single_L(l0, k):
    """
    Pure L-shell map: only use a_{l0,m}, zero everything else.
    """
    shell_alms = {}
    for m in range(-l0, l0 + 1):
        shell_alms[(l0, m)] = ALMS_FULL.get((l0, m), 0j)
    return synthesize_twist(k, shell_alms)


# ======================================================
# PLOTTING HELPERS
# ======================================================
def plot_shell(ax, Tmap, title, add_contours=True):
    """
    Plot a real-valued Tmap on a Mollweide-like lat/lon grid using imshow+contours.
    """
    # latitude/longitude extents
    extent = (-180, 180, -90, 90)

    im = ax.imshow(Tmap,
                   extent=extent,
                   origin='lower',
                   cmap='RdBu_r')
    if add_contours:
        nlat, nlon = Tmap.shape
        lons = np.linspace(-180, 180, nlon)
        lats = np.linspace(-90,  90,  nlat)
        Lon, Lat = np.meshgrid(lons, lats)
        ax.contour(Lon, Lat, Tmap,
                   levels=20,
                   colors='k',
                   linewidths=0.6,
                   alpha=0.9)

    ax.set_title(title)
    ax.set_xlabel("Galactic Longitude (deg)")
    ax.set_ylabel("Galactic Latitude (deg)")
    return im


def plot_manifold(ax, Tmap, title):
    """
    Plot the manifold/distortion view: |T|^0.45 with inferno colormap.
    """
    vis = np.power(np.abs(Tmap), 0.45)
    extent = (-180, 180, -90, 90)

    vmin, vmax = vis.min(), vis.max()
    im = ax.imshow(vis,
                   extent=extent,
                   origin='lower',
                   cmap='inferno',
                   norm=colors.Normalize(vmin=vmin, vmax=vmax))
    # Optional: central meridian line
    ax.axvline(0.0, color='k', linestyle=':', alpha=0.5)

    ax.set_title(title)
    ax.set_xlabel("Galactic Longitude (deg)")
    ax.set_ylabel("Galactic Latitude (deg)")
    return im


# ======================================================
# MAIN: 6-VIEW DECOMPOSITION
# ======================================================
def run_decomposition():
    if any(g is None for g in [ALMS_FULL, ALMS_SUB, YLM, TH, PH]):
        load_alm_grid()

    # 1) Pure shells at K_SHELL
    print("[*] Synthesizing pure L shells...")
    T_L10 = synthesize_single_L(10, K_SHELL)
    T_L20 = synthesize_single_L(20, K_SHELL)
    T_L30 = synthesize_single_L(30, K_SHELL)
    T_L40 = synthesize_single_L(40, K_SHELL)

    # 2) Substrate map (L10–40 removed) at K_SHELL
    print("[*] Synthesizing substrate map...")
    T_sub_shell = synthesize_twist(K_SHELL, ALMS_SUB)

    # 3) Substrate manifold view at K_MANIFOLD
    print("[*] Synthesizing substrate manifold view...")
    T_sub_manifold = synthesize_twist(K_MANIFOLD, ALMS_SUB)

    # 4) Build 3×2 panel
    print("[*] Building 6-panel decomposition figure...")
    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    ax10, ax20 = axes[0]
    ax30, ax40 = axes[1]
    ax_sub, ax_man = axes[2]

    plot_shell(ax10, T_L10, f"Pure L=10 | k={K_SHELL:.3f}")
    plot_shell(ax20, T_L20, f"Pure L=20 | k={K_SHELL:.3f}")
    plot_shell(ax30, T_L30, f"Pure L=30 | k={K_SHELL:.3f}")
    plot_shell(ax40, T_L40, f"Pure L=40 | k={K_SHELL:.3f}")

    plot_shell(ax_sub, T_sub_shell,
               f"Substrate (L10–40 removed) | k={K_SHELL:.3f}",
               add_contours=True)

    im_man = plot_manifold(ax_man, T_sub_manifold,
                           f"Substrate Manifold | k={K_MANIFOLD:.3f}")

    # Colorbar for the manifold panel
    cbar = fig.colorbar(im_man, ax=ax_man, fraction=0.046, pad=0.02)
    cbar.set_label("|T|^0.45")

    fig.tight_layout()
    outname = "cmb_substrate_decomposition_6view.png"
    plt.savefig(outname, dpi=150, bbox_inches='tight')
    plt.close(fig)

    print(f"✅ Saved 6-view decomposition to: {outname}")


if __name__ == "__main__":
    run_decomposition()
