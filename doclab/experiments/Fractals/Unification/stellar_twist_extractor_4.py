import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.interpolate import RectBivariateSpline
from astropy.coordinates import SkyCoord
import astropy.units as u

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
FLOW_FIELD_PATH = "twist_flow_field.npz"
SEARCH_RES = 100 # Resolution of the template match (matches stellar map)

def load_cmb_gradient(fits_path):
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {fits_path}")
        return None, None

    # Handle different FITS structures
    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    # Replace NaNs
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)

    print("[*] Computing CMB Gradient Field...")
    # We project the HEALPix map onto a 2D grid to compute gradients easily
    # (Matches the geometry of your stellar flow map)
    grid_l = np.linspace(-180, 180, 360)
    grid_b = np.linspace(-90, 90, 180)
    L_GRID, B_GRID = np.meshgrid(grid_l, grid_b)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Interpolate CMB onto the grid
    coords = SkyCoord(l=L_GRID*u.deg, b=B_GRID*u.deg, frame='galactic')
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    cmb_2d = cmb[ipix]

    # Calculate Gradients (The "Flow" of Temperature)
    # Gradient Y = d/db (Latitude), Gradient X = d/dl (Longitude)
    grad_y, grad_x = np.gradient(cmb_2d)
    
    # Normalize
    mag = np.sqrt(grad_x**2 + grad_y**2)
    mag[mag == 0] = 1 # Avoid div/0
    grad_x /= mag
    grad_y /= mag

    return grad_x, grad_y, cmb_2d

def load_stellar_template(npz_path):
    print(f"[*] Loading Stellar Flow Template from {npz_path}...")
    data = np.load(npz_path)
    U = data['U'] # Flow X
    V = data['V'] # Flow Y
    
    # Normalize the stellar template too
    mag = np.sqrt(U**2 + V**2)
    mag[mag == 0] = 1
    U /= mag
    V /= mag
    
    return U, V

def scan_for_resonance(cmb_gx, cmb_gy, temp_u, temp_v):
    print("[*] Scanning CMB for Twist Resonance...")
    
    # We are looking for alignment.
    # Alignment Score = Dot Product of (CMB_Grad . Stellar_Flow)
    # Ideally, we slide the template over the map. 
    # For this proof of concept, we check if the GLOBAL stellar pattern 
    # aligns with the GLOBAL CMB pattern (checking for local/universal connection).
    
    # Resize match (The stellar map is 100x100, CMB grid was 360x180)
    # Let's resize CMB to 100x100 for direct correlation
    from skimage.transform import resize
    
    target_shape = temp_u.shape # (100, 100)
    cmb_gx_s = resize(cmb_gx, target_shape)
    cmb_gy_s = resize(cmb_gy, target_shape)
    
    # Compute Dot Product Map (Resonance)
    # R = (Grad_X * Flow_X) + (Grad_Y * Flow_Y)
    # Range: -1 (Anti-aligned) to +1 (Perfect Flow Match)
    resonance_map = (cmb_gx_s * temp_u) + (cmb_gy_s * temp_v)
    
    return resonance_map

def main():
    # 1. Load Data
    cmb_gx, cmb_gy, cmb_map = load_cmb_gradient(FITS_PATH)
    if cmb_gx is None: return
    
    st_u, st_v = load_stellar_template(FLOW_FIELD_PATH)
    
    # 2. Correlate
    resonance = scan_for_resonance(cmb_gx, cmb_gy, st_u, st_v)
    
    # 3. Visualize
    print("[*] Generating Resonance Map...")
    fig = plt.figure(figsize=(16, 12), facecolor='#050505')
    
    # Plot A: The Stellar Template (For Reference)
    ax1 = fig.add_subplot(221)
    ax1.set_title("1. The Search Pattern (Stellar Twist)", color='white')
    ax1.imshow(np.sqrt(st_u**2 + st_v**2), cmap='plasma', origin='lower')
    ax1.axis('off')
    
    # Plot B: The CMB Gradient Field
    ax2 = fig.add_subplot(222)
    ax2.set_title("2. The Territory (CMB Gradients)", color='white')
    ax2.imshow(np.sqrt(cmb_gx**2 + cmb_gy**2), cmap='gray', origin='lower') # Showing magnitude
    ax2.axis('off')
    
    # Plot C: The Resonance (Correlation)
    ax3 = fig.add_subplot(212)
    ax3.set_facecolor('#050505')
    
    # Smooth the resonance for better visibility
    from scipy.ndimage import gaussian_filter
    res_smooth = gaussian_filter(resonance, sigma=1)
    
    im = ax3.imshow(res_smooth, cmap='RdBu_r', origin='lower', extent=[-180,180,-90,90], vmin=-0.8, vmax=0.8)
    
    ax3.set_title("3. TWIST RESONANCE MAP: Where CMB flows like Stars", color='white', fontsize=16)
    ax3.set_xlabel("Galactic Longitude", color='gray')
    ax3.set_ylabel("Galactic Latitude", color='gray')
    ax3.grid(True, color='#333333', linestyle=':')
    
    cbar = plt.colorbar(im, ax=ax3, orientation='horizontal', pad=0.1)
    cbar.set_label("Resonance Score (Blue = Flow Matches | Red = Anti-Flow)", color='gray')
    cbar.ax.xaxis.set_tick_params(color='gray', labelcolor='gray')
    
    plt.savefig("cmb_twist_resonance.png")
    print("✅ Resonance Map Saved: cmb_twist_resonance.png")
    
    # Check for High Resonance Zones (Nodes)
    # We find the peak coordinates
    max_idx = np.unravel_index(np.argmax(res_smooth), res_smooth.shape)
    
    # Convert grid index back to Lat/Lon
    # Grid is 100x100 covering -180..180 (lon) and -90..90 (lat)
    res_lon = np.linspace(-180, 180, 100)
    res_lat = np.linspace(-90, 90, 100)
    
    best_lon = res_lon[max_idx[1]]
    best_lat = res_lat[max_idx[0]]
    
    print("\n" + "="*50)
    print(f"HIGHEST RESONANCE NODE FOUND:")
    print(f"Location: l={best_lon:.1f}°, b={best_lat:.1f}°")
    print(f"Score: {np.max(res_smooth):.4f}")
    print("="*50)

if __name__ == "__main__":
    main()