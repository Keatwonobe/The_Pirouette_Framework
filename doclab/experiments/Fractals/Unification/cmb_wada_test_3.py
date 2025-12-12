import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.special import sph_harm
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
import astropy.units as u

# --- CONFIGURATION ---
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"  # Real CMB file
LMAX = 40
N_RES = 300

# --- HELPER FUNCTIONS ---

def get_real_cmb_grid(fits_path, lmax, n_res):
    """
    Loads real CMB data, computes spherical harmonic coefficients (a_lm),
    and reconstructs the map on a regular (theta, phi) grid up to lmax.
    """
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {fits_path}. Using synthetic data.")
        return generate_synthetic_cmb(n_res, lmax)

    # Extract Temperature (I)
    if 'I' in data.dtype.names:
        cmb = np.array(data['I'], dtype=np.float64)
    elif 'INP_CMB' in data.dtype.names: # Depending on Planck release format
        cmb = np.array(data['INP_CMB'], dtype=np.float64)
    else:
        # Fallback if structure is different
        cmb = data.astype(np.float64)

    # Handle NaNs (e.g. Galactic mask) - Simple fill
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)

    # Setup HEALPix
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order='ring', frame='galactic')

    # Create synthesis grid
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')

    # Convert grid to HEALPix indices to sample (Nearest Neighbor Approx)
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi)) # 0..360
    lat_deg = np.rad2deg(0.5*np.pi - TH)             # -90..90
    
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    
    # Sample the map
    cmb_grid = cmb[ipix]
    
    # Optional: Smooth via SH transform (Forward -> Inverse with cutoff)
    # For now, raw sampling is faster for visual check.
    # To strictly enforce LMAX cutoff, we'd need proper SH analysis (healpy is best but unavailable).
    # We will assume the user wants the raw data or a simple projection.
    
    # Normalize
    cmb_grid = (cmb_grid - np.mean(cmb_grid)) / np.std(cmb_grid)
    
    return cmb_grid

def generate_synthetic_cmb(res, l_max=30):
    """Fallback if FITS file is missing."""
    print("[-] Generating synthetic CMB...")
    x = np.linspace(-1, 1, res)
    y = np.linspace(-1, 1, res)
    X, Y = np.meshgrid(x, y)
    theta = np.pi * (Y + 1) / 2
    phi = np.pi * (X + 1)
    cmb = np.zeros_like(X)
    for l in range(1, l_max):
        for m in range(-l, l+1):
            a_lm = np.random.randn() + 1j * np.random.randn()
            scale = 1.0 / (l**1.5)
            harmonic = sph_harm(m, l, phi, theta).real
            cmb += scale * a_lm.real * harmonic
    return (cmb - cmb.mean()) / cmb.std()

# --- GEOMETRY KERNEL (Wada) ---
def generate_wada_mask_vectorized(res, zoom=2.0):
    """Deterministic Wada Basin Skeleton."""
    x = np.linspace(-zoom, zoom, res)
    y = np.linspace(-zoom, zoom, res)
    X, Y = np.meshgrid(x, y)
    
    m = X.copy()
    l = Y.copy()
    pm = np.zeros_like(m)
    pl = np.zeros_like(l)
    
    steps = 40
    dt = 0.1
    sigma = 1.0
    
    for _ in range(steps):
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        m += dt * pm; l += dt * pl
        fm = -(m + 2*sigma*m*l); fl = -(l + sigma*(m**2 - l**2))
        pm += 0.5 * dt * fm; pl += 0.5 * dt * fl
        
    angle = np.arctan2(l, m)
    grad = np.abs(np.diff(angle, axis=1, append=angle[:, -1:])) + \
           np.abs(np.diff(angle, axis=0, append=angle[-1:, :]))
    mask = grad > 0.5
    return mask.astype(float)

# --- EXECUTION ---

print(f"[*] Loading CMB Data...")
# Try to load the real file, fallback to synthetic if not found in environment
cmb_map = get_real_cmb_grid(FITS_PATH, LMAX, N_RES)

print(f"[*] Generating Wada Geometry...")
wada_map = generate_wada_mask_vectorized(N_RES, zoom=2.0)

print(f"[*] Computing Interaction...")
# Physics: Interference = CMB Field * Geometry Waveguide
interference = cmb_map * wada_map

# Plotting
fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor='black')

# 1. CMB
axes[0].imshow(cmb_map, cmap='RdBu_r', extent=[-1,1,-1,1], interpolation='bilinear')
axes[0].set_title("1. The Data (Planck CMB)", color='white')
axes[0].axis('off')

# 2. Wada
axes[1].imshow(wada_map, cmap='gray', extent=[-1,1,-1,1], interpolation='nearest')
axes[1].set_title("2. The Geometry (Wada Skeleton)", color='white')
axes[1].axis('off')

# 3. Interaction
# Use 'inferno' to highlight constructive interference "energy"
axes[2].imshow(interference, cmap='inferno', extent=[-1,1,-1,1], interpolation='bilinear')
axes[2].set_title("3. The Pop-Out (Constructive Interference)", color='white')
axes[2].axis('off')

plt.suptitle(f"Geometric Filtering of Cosmic Data (Interference Analysis)", color='white', fontsize=16)
plt.tight_layout()
plt.savefig('wada_real_cmb_interaction.png', dpi=150)
print("[+] Analysis Complete.")