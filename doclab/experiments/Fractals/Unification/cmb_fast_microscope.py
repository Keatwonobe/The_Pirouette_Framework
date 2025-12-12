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
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"

# MICROSCOPE SETTINGS
LMAX = 350          # Pushed higher since we optimized the math
FOV_DEG = 8.0       # 8 Degree Zoom on Galactic Center
N_RES = 512         # Higher resolution grid (512x512)

# ANIMATION SETTINGS
GIF_FRAMES = 60
GIF_DURATION = 80

# The Singularity "Breath"
# Oscillating slightly around k=1 to see the fabric stretch
K_RANGE = np.concatenate([
    np.linspace(1.0, 1.0005, GIF_FRAMES // 2),
    np.linspace(1.0005, 1.0, GIF_FRAMES // 2)
])

# ======================
# OPTIMIZED CACHE
# ======================
# We only cache the Theta-dependent part of the harmonics
# Structure: Dict[(l, m)] -> 2D Array of Theta-Weights
THETA_BASIS_CACHE = {} 
ALMS_CACHE = {}
TH_GRID = None
PH_GRID = None

def load_data_and_precompute(fits_path, lmax, n_res, fov_deg):
    global THETA_BASIS_CACHE, ALMS_CACHE, TH_GRID, PH_GRID
    
    print(f"\n[*] INITIATING SPARSE MICROSCOPE")
    print(f"    Target: Galactic Center | FOV: {fov_deg}° | LMAX: {lmax}")
    
    # 1. Load FITS
    try:
        print("    Loading CMB Data...")
        with fits.open(fits_path) as hdul:
            data = hdul[1].data
            # Handle different field names in Planck data
            if 'I' in data.columns.names: array_data = data['I']
            elif 'INP_CMB' in data.columns.names: array_data = data['INP_CMB']
            else: array_data = data.field(0)
            
            cmb = np.array(array_data, dtype=np.float64)
    except Exception as e:
        print(f"[!] ERROR: {e}")
        return False

    # 2. Healpix Decomposition
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # 3. Compute Global ALMs (The "DNA" of the universe)
    print("    Extracting Harmonic Coefficients (a_lm)...")
    # Sampling grid for integration (Global sphere)
    n_sample = lmax * 2
    theta_alm = np.linspace(0, np.pi, n_sample)
    phi_alm = np.linspace(-np.pi, np.pi, n_sample, endpoint=False)
    TH_S, PH_S = np.meshgrid(theta_alm, phi_alm, indexing='ij')
    
    # Project sphere to find weights
    lon_deg = np.rad2deg((PH_S + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_S)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    weights = np.sin(TH_S) * (theta_alm[1]-theta_alm[0]) * (phi_alm[1]-phi_alm[0])
    
    # Compute ALMs
    # We do this the hard way once to ensure accuracy
    count = 0
    total_coeffs = (lmax*(lmax+1))//2 + lmax
    print(f"    Computing {total_coeffs} coefficients...")
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_S, TH_S)
            ALMS_CACHE[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    # 4. Generate ZOOM Grid (The Viewport)
    print("    Constructing Viewport Geometry...")
    fov_rad = np.deg2rad(fov_deg)
    th_min = (np.pi/2) - (fov_rad/2)
    th_max = (np.pi/2) + (fov_rad/2)
    ph_min = -fov_rad/2
    ph_max = fov_rad/2
    
    theta = np.linspace(th_min, th_max, n_res)
    phi = np.linspace(ph_min, ph_max, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    # 5. PRE-COMPUTE THETA BASIS (The "Sparse" Optimization)
    # We calculate Y_lm(theta, phi=0). This isolates the vertical oscillation.
    # During animation, we only need to apply the phi rotation.
    print("    Pre-computing Vertical Basis Vectors...")
    for l in range(lmax + 1):
        if l % 50 == 0: print(f"      Layer L={l} cached.")
        for m in range(-l, l + 1):
            # We compute sph_harm with phi=0
            # This captures the Legendre Polynomial part and Normalization
            basis = sph_harm(m, l, np.zeros_like(TH_GRID), TH_GRID)
            
            # Premultiply by a_lm to save time later
            # We store the "Weighted Basis"
            THETA_BASIS_CACHE[(l, m)] = ALMS_CACHE[(l, m)] * basis

    return True

def synthesize_fast_frame(k, lmax):
    """
    Reconstructs the map using the cached Theta basis and applying 
    the twist to Phi dynamically.
    Math: Sum [ (a_lm * P_lm(theta)) * exp(i * m * k * phi) ]
    """
    map_out = np.zeros_like(TH_GRID, dtype=np.complex128)
    
    # The twist scales the azimuthal frequency m
    # Normal physics: exp(i * m * phi)
    # Twisted physics: exp(i * m * k * phi)
    
    # This loop is now very fast because it's just matrix addition
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            # Retrieve pre-weighted theta basis
            weighted_basis = THETA_BASIS_CACHE[(l, m)]
            
            # Apply Twisted Rotation
            # This is the only expensive trig operation per frame
            rotation = np.exp(1j * m * k * PH_GRID)
            
            map_out += weighted_basis * rotation
            
    return map_out.real

def run_fast_microscope():
    if not load_data_and_precompute(FITS_PATH, LMAX, N_RES, FOV_DEG):
        return

    print(f"\n[*] Starting High-Speed Rendering Loop...")
    frames_buffer = []
    
    # 1. Generate Reference (k=1.0)
    print("    Generating Reference Topology...")
    T_ref = synthesize_fast_frame(1.0, LMAX)
    T_ref_std = np.std(T_ref)
    
    # Normalize
    T_ref_norm = T_ref / T_ref_std

    # 2. Render Loop
    for i, k_val in enumerate(K_RANGE):
        print(f"    Rendering Frame {i+1}/{GIF_FRAMES} (k={k_val:.5f})...", end='\r')
        
        # Fast Synthesis
        T_twist = synthesize_fast_frame(k_val, LMAX)
        T_twist_norm = T_twist / T_ref_std
        
        # --- TOPOLOGICAL INTERFERENCE FILTER ---
        # Logic: Enhance the "knots" where the twist breaks symmetry
        
        # 1. The Bulk Interference
        diff = np.abs(T_ref_norm - T_twist_norm)
        
        # 2. Edge Detection (Gradient Enhancement)
        # This brings out the "fractal" lines
        grad_x, grad_y = np.gradient(diff)
        grad_mag = np.sqrt(grad_x**2 + grad_y**2)
        
        # Composite: Dark background, bright interference, glowing edges
        vis_data = (diff * 0.7) + (grad_mag * 2.0)
        
        # Gamma correction to remove "grey" wash
        vis_data = np.power(vis_data, 0.6)
        
        # Plot
        fig, ax = plt.subplots(figsize=(8, 8))
        extent = (-FOV_DEG/2, FOV_DEG/2, -FOV_DEG/2, FOV_DEG/2)
        
        # Use 'twilight_shifted' - excellent for cyclic/topological interference
        im = ax.imshow(vis_data, extent=extent, cmap='magma', 
                       norm=colors.Normalize(vmin=0, vmax=np.percentile(vis_data, 99)),
                       origin='lower')
        
        ax.axis('off')
        
        # Annotation
        timestamp = f"k={k_val:.6f}"
        ax.text(0.02, 0.02, timestamp, transform=ax.transAxes, 
                color='white', fontsize=10, fontfamily='monospace', alpha=0.7)

        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        
        fname = f"temp_fast_{i:03d}.png"
        plt.savefig(fname, bbox_inches='tight', dpi=100, facecolor='black')
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames_buffer.append(img.copy())
        os.remove(fname)

    # Save
    out_name = f"cmb_microscope_L{LMAX}_FOV{int(FOV_DEG)}.gif"
    if frames_buffer:
        frames_buffer[0].save(out_name, save_all=True, append_images=frames_buffer[1:], 
                              duration=GIF_DURATION, loop=0)
        print(f"\n\n✅ DONE. Output saved to: {out_name}")

if __name__ == "__main__":
    run_fast_microscope()