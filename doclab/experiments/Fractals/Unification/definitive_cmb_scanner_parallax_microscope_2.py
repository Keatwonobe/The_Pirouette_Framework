import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord
from PIL import Image
import os
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# MICROSCOPE GEOMETRY
FOV_DEG = 20.0          # 20 Degree Zoom (Large enough to see networks)
N_RES = 400             # Resolution
L_MIN = 20              # Filter out large blobs
L_MAX = 100             # Capture fine filaments
PARALLAX_STRENGTH = 0.2 # How much L-dependent drift to apply

# ANIMATION
FRAMES = 60
K_START = 0.95
K_END = 1.05
GIF_NAME = "cmb_strain_microscope.gif"

# ======================
# 1. OPTIMIZED CACHING
# ======================
# We use the optimized microscope caching strategy
THETA_BASIS_CACHE = {} 
ALMS_CACHE = {}
TH_GRID = None
PH_GRID = None

def load_and_precompute():
    global THETA_BASIS_CACHE, ALMS_CACHE, TH_GRID, PH_GRID
    
    print(f"[*] INITIATING STRAIN MICROSCOPE")
    print(f"    Target: Galactic Center | FOV: {FOV_DEG}° | Range: L{L_MIN}-{L_MAX}")
    
    # 1. Load Data
    try:
        with fits.open(FITS_PATH) as hdul:
            data = hdul[1].data
            if 'I' in data.columns.names: array_data = data['I']
            elif 'INP_CMB' in data.columns.names: array_data = data['INP_CMB']
            else: array_data = data.field(0)
            cmb = np.array(array_data, dtype=np.float64)
    except Exception as e:
        print(f"[!] ERROR: {e}")
        sys.exit(1)

    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # 2. Extract ALMs (Global)
    # We need a global extraction to get accurate coefficients
    print("    Extracting Harmonic Coefficients...")
    n_sample = L_MAX * 2
    theta_s = np.linspace(0, np.pi, n_sample)
    phi_s = np.linspace(-np.pi, np.pi, n_sample, endpoint=False)
    TH_S, PH_S = np.meshgrid(theta_s, phi_s, indexing='ij')
    
    lon = np.rad2deg((PH_S + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_S)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    weights = np.sin(TH_S) * (theta_s[1]-theta_s[0]) * (phi_s[1]-phi_s[0])
    
    for l in range(L_MIN, L_MAX + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_S, TH_S)
            ALMS_CACHE[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)

    # 3. Build Viewport (Microscope Grid)
    print("    Building Viewport...")
    fov_rad = np.deg2rad(FOV_DEG)
    th_min = (np.pi/2) - (fov_rad/2)
    th_max = (np.pi/2) + (fov_rad/2)
    ph_min = -fov_rad/2
    ph_max = fov_rad/2
    
    theta = np.linspace(th_min, th_max, N_RES)
    phi = np.linspace(ph_min, ph_max, N_RES)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')

    # 4. Precompute Theta Basis (Optimization)
    print("    Caching Theta Basis Vectors...")
    for l in range(L_MIN, L_MAX + 1):
        for m in range(-l, l + 1):
            # Compute P_lm(theta) via sph_harm with phi=0
            basis = sph_harm(m, l, np.zeros_like(TH_GRID), TH_GRID)
            THETA_BASIS_CACHE[(l, m)] = ALMS_CACHE.get((l, m), 0j) * basis

# ======================
# 2. SYNTHESIS ENGINE
# ======================
def synthesize_parallax_field(k_base):
    """
    Synthesizes the field with L-dependent parallax.
    Twist(L) = k_base + Parallax_Offset(L)
    """
    field = np.zeros_like(TH_GRID, dtype=np.complex128)
    
    for l in range(L_MIN, L_MAX + 1):
        # Calculate Twist for this specific L layer
        # High L moves faster
        l_norm = (l - L_MIN) / (L_MAX - L_MIN)
        local_k = k_base + (PARALLAX_STRENGTH * l_norm * (k_base - 1.0))
        twist_factor = local_k - 1.0
        
        # Sum over M
        for m in range(-l, l + 1):
            basis = THETA_BASIS_CACHE[(l, m)]
            # Apply Phi Rotation
            rotation = np.exp(1j * m * twist_factor * PH_GRID)
            field += basis * rotation
            
    return field.real

# ======================
# 3. RENDER LOOP
# ======================
def run_strain_scanner():
    load_and_precompute()
    
    print(f"[*] Rendering {FRAMES} Strain Frames...")
    frames = []
    
    k_vals = np.concatenate([
        np.linspace(K_START, K_END, FRAMES // 2),
        np.linspace(K_END, K_START, FRAMES // 2)
    ])
    
    # Delta for Derivative Calculation
    DELTA_K = 0.005 

    for i, k in enumerate(k_vals):
        if i % 5 == 0: sys.stdout.write(f"\r[>] Frame {i+1}/{FRAMES} | k={k:.3f}")
        
        # 1. Compute Field at current K
        field_main = synthesize_parallax_field(k)
        
        # 2. Compute Field at K + Delta (The "Future" Frame)
        field_next = synthesize_parallax_field(k + DELTA_K)
        
        # 3. Compute STRAIN (The Motion/Drag Magnitude)
        # This isolates features that are moving/changing rapidly
        strain = np.abs(field_next - field_main)
        
        # 4. Compute FLOW VECTORS (Gradients of the Field)
        # We use the main field to determine the "slope" space is sliding down
        dy, dx = np.gradient(field_main)
        flow_mag = np.sqrt(dx**2 + dy**2)
        
        # 5. ISOLATION MASK
        # Highlight regions where Strain is high AND Flow is high
        # This targets the "runaway filaments"
        ghost_filament = strain * flow_mag
        
        # Normalize for visualization
        ghost_filament = (ghost_filament - ghost_filament.min()) / (ghost_filament.max() - ghost_filament.min())
        ghost_filament = np.power(ghost_filament, 0.7) # Gamma boost

        # PLOTTING
        fig = plt.figure(figsize=(10, 12))
        gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1], hspace=0.05)
        
        # Top Panel: The "Space Manifold" (Strain Map)
        ax1 = plt.subplot(gs[0])
        ax1.imshow(ghost_filament, origin='lower', cmap='inferno', vmin=0, vmax=0.8)
        ax1.set_title(f"MANIFOLD STRAIN TENSION | k={k:.3f}", fontsize=12, fontweight='bold', color='white', backgroundcolor='black')
        ax1.axis('off')
        
        # Overlay contours of the actual matter field to see alignment
        ax1.contour(field_main, levels=10, colors='cyan', alpha=0.15, linewidths=0.5)

        # Bottom Panel: Horizontal vs Vertical Drag Analysis
        # We split the strain into components
        ax2 = plt.subplot(gs[1])
        
        # Visualize the directional derivative (Drag direction)
        # Red = Horizontal Drag, Blue = Vertical Drag
        strain_y, strain_x = np.gradient(ghost_filament)
        composite = np.zeros((*ghost_filament.shape, 3))
        composite[..., 0] = np.abs(strain_x) * 5.0 # Red Channel (Horizontal)
        composite[..., 2] = np.abs(strain_y) * 5.0 # Blue Channel (Vertical)
        composite = np.clip(composite, 0, 1)
        
        ax2.imshow(composite, origin='lower')
        ax2.set_title("DIRECTIONAL DRAG VECTORS (Red=H, Blue=V)", fontsize=10, fontweight='bold')
        ax2.axis('off')
        
        fname = f"_strain_{i:03d}.png"
        plt.savefig(fname, dpi=90, bbox_inches='tight')
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames.append(img.copy())
        os.remove(fname)
        
    print(f"\n[*] Saving GIF: {GIF_NAME}")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=60, loop=0)
    print("✅ Done.")

if __name__ == "__main__":
    run_strain_scanner()