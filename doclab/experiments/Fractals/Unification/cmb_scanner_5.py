import numpy as np
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb 

# ======================
# CONFIG
# ======================

FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits" 
TWIST_CONST = 2.83814
TWIST_MODE = "untwist"     # Not used for this zoom, but maintained

# grid resolution (match previous script)
N_THETA = 1024
N_PHI   = 2048

# --- ZOOM CONFIGURATION ---
# Target the upper-right quadrant for enhancement:
ZOOM_LON_MIN, ZOOM_LON_MAX = 90.0, 180.0
ZOOM_LAT_MIN, ZOOM_LAT_MAX = 0.0, 90.0


# ======================
# ANALYSIS FUNCTIONS (Simplified for Zoom)
# ======================

def calculate_laplacian(image):
    # Computes the 2D Laplacian using np.gradient
    grad_y, grad_x = np.gradient(image)
    laplacian = np.gradient(grad_x, axis=1) + np.gradient(grad_y, axis=0)
    return laplacian


def render_helicity_view(T, PH):
    # Converts Temperature (Amplitude) and Longitude (Phase) to HSV
    hue = (PH + np.pi) / (2 * np.pi)
    
    T_clean = T.copy()
    T_clean[np.isnan(T_clean)] = np.nanmedian(T) # Fill NaNs for log
    
    # Logarithmic Compression
    log_amp = np.log1p(np.abs(T_clean - T_clean.mean())) 
    
    # Iso-Contour Generation
    contour_freq = 30.0 
    structure = np.sin(log_amp * contour_freq)
    
    val = 0.6 + 0.4 * structure
    sat = np.ones_like(hue) * 0.95
    
    hsv = np.dstack((hue, sat, val))
    rgb = hsv_to_rgb(hsv)
    rgb[np.isnan(T), :] = 0.0
    
    return rgb


# ======================
# CORE CMBSCANNER FUNCTIONS
# ======================

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


def main():
    print(f"[*] Loading FITS from {FITS_PATH}...")
    try:
        data = fits.getdata(FITS_PATH)
    except FileNotFoundError:
        print("[!] ERROR: FITS file not found. Please ensure it is present.")
        return
        
    # --- Setup ---
    cmb = np.array(data.get("I") or data.get("INP_CMB"), dtype=np.float64)
    npix = cmb.size
    nside = int(np.sqrt(npix / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Build Angular Grid (TH is colatitude, PH is longitude in radians)
    TH, PH = build_equatorial_grid(N_THETA, N_PHI) 
    
    # Calculate Latitudes and Longitudes in Degrees for indexing
    LAT_DEG = np.rad2deg(0.5*np.pi - TH) 
    LON_DEG = np.rad2deg(PH)
    
    # --- Zoom Indexing ---
    
    # Find indices for the zoom box
    lat_idx = np.where((LAT_DEG[:, 0] >= ZOOM_LAT_MIN) & (LAT_DEG[:, 0] <= ZOOM_LAT_MAX))[0]
    lon_idx = np.where((LON_DEG[0, :] >= ZOOM_LON_MIN) & (LON_DEG[0, :] <= ZOOM_LON_MAX))[0]
    
    if len(lat_idx) == 0 or len(lon_idx) == 0:
        print("[!] ERROR: Zoom indices empty. Check boundary conditions.")
        return
        
    lat_slice = slice(lat_idx.min(), lat_idx.max() + 1)
    lon_slice = slice(lon_idx.min(), lon_idx.max() + 1)
    
    # Cropped grids
    PH_zoom = PH[lat_slice, lon_slice]
    LAT_zoom = LAT_DEG[lat_slice, lon_slice]
    LON_zoom = LON_DEG[lat_slice, lon_slice]
    extent_zoom = (LON_zoom.min(), LON_zoom.max(), LAT_zoom.min(), LAT_zoom.max())

    # --- Sample & Analyze Zoomed Region ---
    print("[*] Sampling CMB onto Zoomed Grid...")
    cmb_zoom = healpix_sample(cmb, hpix, TH[lat_slice, lon_slice], PH_zoom)
    
    # Calculate Mask and Fill NaNs for Laplacian
    mask = np.isfinite(cmb_zoom)
    cmb_zoom_valid = cmb_zoom.copy()
    cmb_zoom_valid[~mask] = np.nanmedian(cmb_zoom[mask])

    print("[*] Applying Enhancement Filters...")
    cmb_helicity_zoom = render_helicity_view(cmb_zoom, PH_zoom)
    cmb_laplacian_zoom = calculate_laplacian(cmb_zoom_valid)
    cmb_laplacian_zoom[~mask] = np.nan # Apply mask back

    # --- PLOTS ---
    print("[*] Plotting Enhanced Zoom...")
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)
    
    # P1: Zoomed CMB Temperature
    im0 = axes[0].imshow(
        cmb_zoom, origin="lower", aspect="auto", extent=extent_zoom, cmap="coolwarm", 
        vmin=np.nanpercentile(cmb_zoom, 5), vmax=np.nanpercentile(cmb_zoom, 95) # Local Contrast
    )
    axes[0].set_title(f"1. Zoomed CMB Temperature ({ZOOM_LON_MIN}° to {ZOOM_LON_MAX}°)")
    fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

    # P2: Zoomed Helicity View
    axes[1].imshow(cmb_helicity_zoom, origin="lower", aspect="auto", extent=extent_zoom)
    axes[1].set_title("2. Helicity View (Logarithmic Structure Enhancement)")

    # P3: Zoomed Laplacian
    im2 = axes[2].imshow(
        cmb_laplacian_zoom, origin="lower", aspect="auto", extent=extent_zoom, cmap="bwr",
        vmin=np.nanpercentile(cmb_laplacian_zoom, 1), vmax=np.nanpercentile(cmb_laplacian_zoom, 99) # Local Contrast
    )
    axes[2].set_title("3. Laplacian ('Lyapunov' Texture Filter)")
    fig.colorbar(im2, ax=axes[2], fraction=0.046, pad=0.04, label="$\\nabla^2 T$")
    
    # Set common labels
    for ax in axes.flat:
        ax.set_xlabel("Longitude (deg)")
        ax.set_ylabel("Latitude (deg)")
        
    plt.suptitle(f"CMB Structure Enhancement: Upper Right Quadrant")
    plt.savefig("cmb_zoom_enhancement.png")
    plt.close(fig)
    print("[*] Plot saved as cmb_zoom_enhancement.png")


if __name__ == "__main__":
    main()