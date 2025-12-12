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
LMAX = 60                   # Total Bandwidth
SKELETON_RANGE = (10, 40)   # The "Bass" Range
N_RES = 250                 # Resolution (250x250)
FRAMES = 60                 # Animation frames
K_RANGE = np.linspace(0.8, 1.2, FRAMES) # Twist Range
GIF_NAME = "cmb_super_scanner_six_fast.gif"

# ======================
# 1. DATA INGESTION & ALM EXTRACTION
# ======================
def get_alms_and_grid(fits_path, lmax, n_res):
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    # Handle FITS structure variability
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    # Infill NaNs
    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    # Healpix Setup
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # 1. Integration Grid (High Res for ALM extraction)
    n_theta_alm = lmax * 3
    n_phi_alm = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta_alm)
    p_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')

    # Sample the Map
    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]

    # Weights
    dtheta = t_alm[1] - t_alm[0]
    dphi = p_alm[1] - p_alm[0]
    weights = np.sin(TH_ALM) * dtheta * dphi

    print("[*] Computing Spherical Harmonics Decomposition...")
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    # 2. Synthesis Grid (Display Resolution)
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    return alms, TH_GRID, PH_GRID

# ======================
# 2. OPTIMIZATION: BUILD MODE MAPS
# ======================
def build_mode_maps(alms, lmax, l_range, TH, PH):
    """
    Collapses the L-summation into static 'Mode Maps' for each m.
    M_m(theta, phi) = sum_{l} a_lm * Y_lm(theta, phi)
    
    This removes the spherical harmonic calculation from the animation loop.
    """
    l_start, l_end = l_range
    mode_maps = {} # Key: m, Value: 2D Complex Array
    
    # We iterate m from -lmax to lmax. 
    # For a given m, we sum all valid l's.
    
    print(f"[*] Pre-computing Mode Maps for L range {l_range}...")
    
    # Pre-compute Y_lm only when needed to save RAM, but here we iterate efficiently
    for l in range(l_start, l_end + 1):
        if l > lmax: break
        
        for m in range(-l, l + 1):
            alm = alms.get((l, m), 0j)
            if alm == 0j: continue
            
            # Compute Y_lm on the visual grid
            Y_lm = sph_harm(m, l, PH, TH)
            
            # Accumulate into the mode map for this m
            if m not in mode_maps:
                mode_maps[m] = np.zeros_like(TH, dtype=np.complex128)
            
            mode_maps[m] += alm * Y_lm
            
    return mode_maps

# ======================
# 3. FAST SYNTHESIS
# ======================
def synthesize_from_modes(mode_maps, k, PH_GRID):
    """
    Reconstructs the map from mode maps.
    Map = sum_m M_m * exp(i * m * (k-1) * phi)
    """
    map_out = np.zeros_like(PH_GRID, dtype=np.complex128)
    twist_factor = k - 1.0
    
    for m, M_map in mode_maps.items():
        # The phase only depends on m and phi
        if twist_factor == 0:
            map_out += M_map
        else:
            phase = np.exp(1j * m * twist_factor * PH_GRID)
            map_out += M_map * phase
            
    return map_out.real

# ======================
# 4. MAIN RUNNER
# ======================
def run_super_scanner():
    
    # 1. Get raw DNA
    alms, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    
    # 2. Build Optimized Structures
    # Skeleton: L 10-40
    print("--- Skeleton Build ---")
    skel_modes = build_mode_maps(alms, LMAX, SKELETON_RANGE, TH, PH)
    
    # Substrate: L 0-9 AND L 41-60
    # We build two sets and merge them, or just logic the range.
    # Let's do it by exclusion.
    print("--- Substrate Build ---")
    # A bit of a hack: pass full range but filter inside? 
    # Actually, let's just use the function twice and merge the dicts carefully or sum the maps.
    # Better: Write a custom builder for the substrate "gap".
    
    sub_modes = {}
    
    # Low pass part (0-9)
    low_modes = build_mode_maps(alms, LMAX, (0, SKELETON_RANGE[0]-1), TH, PH)
    for m, data in low_modes.items():
        if m not in sub_modes: sub_modes[m] = np.zeros_like(TH, dtype=np.complex128)
        sub_modes[m] += data
        
    # High pass part (41-60)
    high_modes = build_mode_maps(alms, LMAX, (SKELETON_RANGE[1]+1, LMAX), TH, PH)
    for m, data in high_modes.items():
        if m not in sub_modes: sub_modes[m] = np.zeros_like(TH, dtype=np.complex128)
        sub_modes[m] += data

    # 3. Pre-calculate Static Baseline (k=1) for Distortion View
    print("[*] Calculating Static Baselines...")
    map_skel_static = synthesize_from_modes(skel_modes, 1.0, PH)
    map_sub_static = synthesize_from_modes(sub_modes, 1.0, PH)
    MAP_FULL_STATIC = map_skel_static + map_sub_static

    # 4. Animation Loop
    print(f"[*] Rendering {FRAMES} frames (High Speed Mode)...")
    frames = []
    
    # Helper for Plotting
    def plot_panel(ax, data, title, cmap, vlim=None):
        if vlim:
            im = ax.imshow(data, origin='lower', extent=[-180,180,-90,90], cmap=cmap, vmin=vlim[0], vmax=vlim[1])
        else:
            im = ax.imshow(data, origin='lower', extent=[-180,180,-90,90], cmap=cmap)
        ax.set_title(title, fontsize=9, fontweight='bold')
        ax.axis('off')
        return im

    for i, k in enumerate(K_RANGE):
        if i % 10 == 0: sys.stdout.write(f"\r[>] Frame {i+1}/{FRAMES} (k={k:.3f})")
        
        # --- FAST SYNTHESIS ---
        map_skel = synthesize_from_modes(skel_modes, k, PH)
        map_sub = synthesize_from_modes(sub_modes, k, PH)
        map_full = map_skel + map_sub
        
        # --- DERIVED MAPS ---
        # 1. Manifold Distortion: Absolute difference from the static universe
        # "How much has the space stretched?"
        map_distort = np.abs(map_full - MAP_FULL_STATIC)
        
        # 2. Interference: Contrast between Structure and Sea
        map_interf = map_skel - map_sub
        
        # 3. Bones: Nodal lines of the skeleton
        # Using a soft sign or binary
        map_bones = np.tanh(map_skel * 5) 

        # --- PLOTTING ---
        fig = plt.figure(figsize=(18, 10))
        gs = gridspec.GridSpec(2, 3, wspace=0.1, hspace=0.2)
        
        # Row 1
        plot_panel(plt.subplot(gs[0]), map_skel, f"1. SKELETON (L{SKELETON_RANGE[0]}-{SKELETON_RANGE[1]})", 'RdBu_r')
        plot_panel(plt.subplot(gs[1]), map_sub, "2. SUBSTRATE (L<10, L>40)", 'inferno')
        plot_panel(plt.subplot(gs[2]), map_full, f"3. COMPOSITE REALITY", 'viridis')
        
        # Row 2
        # Gamma correct distortion to see subtle waves
        plot_panel(plt.subplot(gs[3]), map_distort**0.6, "4. MANIFOLD DISTORTION (|Twist - Static|)", 'magma')
        plot_panel(plt.subplot(gs[4]), map_interf, "5. INTERFERENCE (Skel - Sub)", 'PiYG')
        plot_panel(plt.subplot(gs[5]), map_bones, "6. TOPOLOGICAL BONES (Nodal Structure)", 'gray')
        
        fig.suptitle(f"SUPER SCANNER SIX | Twist Parameter k = {k:.4f}", fontsize=16, y=0.95)
        
        fname = f"_frame_{i:03d}.png"
        plt.savefig(fname, dpi=70, bbox_inches='tight')
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames.append(img.copy())
        os.remove(fname)

    print(f"\n\n[*] Compiling High-Speed GIF...")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=80, loop=0)
    print(f"✅ DONE: {GIF_NAME}")

if __name__ == "__main__":
    run_super_scanner()