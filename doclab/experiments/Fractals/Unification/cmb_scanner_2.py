import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

# ======================
# CONFIG
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
NSIDE = 2048
TWIST_CONST = 2.83814
TWIST_MODE = "untwist"   # "twist" or "untwist"

N_THETA = 1024
N_PHI   = 2048

# ===============================================================
# HEALPIX (RING SCHEME) ang2pix IMPLEMENTATION (NO healpy needed)
# ===============================================================

def ang2pix_ring(nside, theta, phi):
    """
    Pure-Python HEALPix ang2pix for RING ordering.
    theta: colatitude in radians [0, π]
    phi: longitude in radians [-π, π)
    """
    twothird = 2.0 / 3.0
    z = np.cos(theta)
    za = np.abs(z)

    # ring index
    ar = 1.5 + nside * z
    # number of pixels
    npix = 12 * nside * nside

    # north polar cap
    if z > twothird:
        iring = int(nside * np.sqrt(3*(1 - z)))
        iphi = int(phi * iring / (2*np.pi))
        ipix = 2 * iring * (iring - 1) + iphi
        return ipix

    # south polar cap
    if z < -twothird:
        iring = int(nside * np.sqrt(3*(1 + z)))
        iphi = int(phi * iring / (2*np.pi))
        ipix = npix - 2 * iring * (iring + 1) + iphi
        return ipix

    # equatorial region
    iring = int(nside * (2 - 1.5 * z))
    iphi = int(phi * nside / (2*np.pi) * 4)

    ipix = 2 * nside * (nside - 1) + (iring - 1) * 4*nside + iphi
    return ipix


# ===============================================================
# LONGITUDE TWIST
# ===============================================================

def twist_phi(phi, k=2.83814, mode="untwist"):
    if mode == "twist":
        src = phi * k
    else:  # untwist
        src = phi / k
    return (src + np.pi) % (2*np.pi) - np.pi


# ===============================================================
# MAIN
# ===============================================================

def main():
    print("[*] Loading FITS...")
    data = fits.getdata(FITS_PATH)

    # Print fields so we know what’s inside
    print("[*] FITS columns:", data.dtype.names)

    # Select the CMB temperature field
    if "I" in data.dtype.names:
        cmb = data["I"]
    elif "INP_CMB" in data.dtype.names:
        cmb = data["INP_CMB"]
    else:
        raise ValueError("No usable CMB temperature field found!")


    print("[*] Building grid...")
    theta = np.linspace(0, np.pi, N_THETA)
    phi   = np.linspace(-np.pi, np.pi, N_PHI)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")

    print("[*] Computing pixel indices for original CMB...")
    ipix_orig = np.vectorize(lambda t, p: ang2pix_ring(NSIDE, t, p))(TH, PH)
    cmb_orig = cmb[ipix_orig]

    print("[*] Applying twist...")
    PH_src = twist_phi(PH, TWIST_CONST, mode=TWIST_MODE)

    print("[*] Computing pixel indices for twisted CMB...")
    ipix_tw = np.vectorize(lambda t, p: ang2pix_ring(NSIDE, t, p))(TH, PH_src)
    cmb_tw = cmb[ipix_tw]

    # ====================
    # PLOT
    # ====================
    print("[*] Plotting...")
    fig, ax = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

    im0 = ax[0].imshow(
        cmb_orig,
        origin="lower",
        aspect="auto",
        extent=[-180, 180, -90, 90],
        cmap='coolwarm'
    )
    ax[0].set_title("Original CMB (Equirectangular)")
    ax[0].set_xlabel("Longitude (deg)")
    ax[0].set_ylabel("Latitude (deg)")
    plt.colorbar(im0, ax=ax[0])

    im1 = ax[1].imshow(
        cmb_tw,
        origin="lower",
        aspect="auto",
        extent=[-180, 180, -90, 90],
        cmap='coolwarm'
    )
    ax[1].set_title(f"CMB Twisted ({TWIST_MODE}, k={TWIST_CONST})")
    ax[1].set_xlabel("Longitude (deg)")
    ax[1].set_ylabel("Latitude (deg)")
    plt.colorbar(im1, ax=ax[1])

    plt.show()


if __name__ == "__main__":
    main()
