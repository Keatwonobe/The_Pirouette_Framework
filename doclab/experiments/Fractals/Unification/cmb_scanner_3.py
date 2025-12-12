import numpy as np
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt

# ======================
# CONFIG
# ======================

FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
TWIST_CONST = 2.83814
TWIST_MODE = "untwist"     # "twist" or "untwist"

# grid resolution
N_THETA = 1024
N_PHI   = 2048


def twist_phi(phi, k, mode="untwist"):
    """
    phi: radians in [-pi, pi)
    mode = "twist"   -> phi_src = k * phi
         = "untwist" -> phi_src = phi / k
    result wrapped back into [-pi, pi)
    """
    if mode == "twist":
        src = phi * k
    else:
        src = phi / k

    return (src + np.pi) % (2.0 * np.pi) - np.pi


def build_equatorial_grid(n_theta, n_phi):
    """
    theta in [0, pi], phi in [-pi, pi)
    """
    theta = np.linspace(0.0, np.pi, n_theta)
    phi   = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")
    return TH, PH


def healpix_sample(cmb, hpix, TH, PH):
    """
    Sample the HEALPix map 'cmb' at angles (TH, PH).
    TH: colatitude (0..pi), PH: longitude (-pi..pi)
    """
    # convert to Galactic lon/lat for HEALPix
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))  # [0, 360)
    lat_deg = np.rad2deg(0.5*np.pi - TH)              # [-90, 90]

    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)  # same shape as TH

    return cmb[ipix]


def main():
    print("[*] Loading FITS...")
    data = fits.getdata(FITS_PATH)
    print("[*] FITS columns:", data.dtype.names)

    # choose the temperature field
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

    # simple sanity correlation
    mask = np.isfinite(cmb_orig) & np.isfinite(cmb_twisted)
    x = cmb_orig[mask] - cmb_orig[mask].mean()
    y = cmb_twisted[mask] - cmb_twisted[mask].mean()
    r = np.dot(x, y) / np.sqrt(np.dot(x, x) * np.dot(y, y))
    print(f"[+] Correlation (orig vs twisted): r = {r:.4f}")

    # ======================
    # PLOTS
    # ======================
    print("[*] Plotting...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

    im0 = axes[0].imshow(
        cmb_orig,
        origin="lower",
        aspect="auto",
        extent=(-180, 180, -90, 90),
        cmap="coolwarm",
    )
    axes[0].set_title("Original CMB (equirectangular projection)")
    axes[0].set_xlabel("Longitude (deg)")
    axes[0].set_ylabel("Latitude (deg)")
    fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

    im1 = axes[1].imshow(
        cmb_twisted,
        origin="lower",
        aspect="auto",
        extent=(-180, 180, -90, 90),
        cmap="coolwarm",
    )
    axes[1].set_title(f"CMB with φ {TWIST_MODE} by k={TWIST_CONST}")
    axes[1].set_xlabel("Longitude (deg)")
    axes[1].set_ylabel("Latitude (deg)")
    fig.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

    plt.show()


if __name__ == "__main__":
    main()
