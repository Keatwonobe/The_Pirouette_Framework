import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 400

# The Axis of Rotation (Found in previous step)
SPIN_L = -111.3
SPIN_B = 1.8

# ======================
# 1. HARMONIC ENGINE
# ======================

def get_alms(fits_path, lmax):
    print(f"[*] Loading CMB Data and Extracting Harmonics...")
    try:
        data = fits.getdata(fits_path)
        if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
        elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
        else: cmb = data.astype(np.float64)
        cmb[np.isnan(cmb)] = np.nanmean(cmb)
    except FileNotFoundError:
        print("[!] File not found.")
        sys.exit(1)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    n_theta = lmax * 3; n_phi = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta)
    p_alm = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')
    
    # Fix for Astropy Units
    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi)) * u.deg
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM) * u.deg
    ipix = hpix.lonlat_to_healpix(lon_deg, lat_deg)
    
    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    return alms

def synthesize_arbitrary(alms, lmax, theta_flat, phi_flat):
    """ 
    Synthesizes field at arbitrary non-grid coordinates.
    Used for re-sampling the rotated map.
    """
    field = np.zeros_like(theta_flat, dtype=np.complex128)
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            Y_lm = sph_harm(m, l, phi_flat, theta_flat)
            field += alms[(l, m)] * Y_lm
    return field.real

# ======================
# 2. ROTATION ENGINE
# ======================

def get_rotation_matrix(l_target, b_target):
    """
    Returns matrix M that rotates the Z-axis (0,0,1) to the Target Axis.
    """
    # Target vector (The Spin Axis)
    l = np.deg2rad(l_target)
    b = np.deg2rad(b_target)
    
    sx = np.cos(b) * np.cos(l)
    sy = np.cos(b) * np.sin(l)
    sz = np.sin(b)
    s = np.array([sx, sy, sz])
    
    z = np.array([0, 0, 1])
    
    # Axis of rotation k = z x s
    k = np.cross(z, s)
    k_len = np.linalg.norm(k)
    
    if k_len < 1e-6:
        # Already aligned or anti-aligned
        return np.eye(3) if sz > 0 else -np.eye(3)
    
    k = k / k_len
    theta = np.arccos(sz) # Angle to rotate
    
    # Rodrigues' formula for rotation matrix
    K = np.array([
        [0, -k[2], k[1]],
        [k[2], 0, -k[0]],
        [-k[1], k[0], 0]
    ])
    
    R = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)
    return R

def generate_rotated_grid(n_res, l_center, b_center):
    print(f"[*] Constructing Spin Frame (North = {l_center}°, {b_center}°)...")
    
    # 1. Create the "Camera" Grid (The View we want to see)
    # Standard Lat/Lon Grid
    theta_cam = np.linspace(0, np.pi, n_res)
    phi_cam = np.linspace(-np.pi, np.pi, n_res)
    TH_C, PH_C = np.meshgrid(theta_cam, phi_cam, indexing='ij')
    
    # 2. Convert Camera Grid to Vectors
    vx_c = np.sin(TH_C) * np.cos(PH_C)
    vy_c = np.sin(TH_C) * np.sin(PH_C)
    vz_c = np.cos(TH_C)
    
    # Flatten for transformation
    vectors_c = np.vstack((vx_c.flatten(), vy_c.flatten(), vz_c.flatten()))
    
    # 3. Rotate Vectors to Original Frame
    # We want the Camera's North (Z) to point to Spin Axis.
    R = get_rotation_matrix(l_center, b_center)
    vectors_orig = R @ vectors_c
    
    # 4. Convert Original Vectors back to Theta/Phi for Sampling
    vx_o, vy_o, vz_o = vectors_orig
    
    theta_o = np.arccos(np.clip(vz_o, -1, 1))
    phi_o = np.arctan2(vy_o, vx_o)
    
    return theta_o, phi_o, (n_res, n_res)

# ======================
# 3. MAIN
# ======================

def run_spin_mapper():
    alms = get_alms(FITS_PATH, LMAX)
    
    # Generate Sampling Coordinates
    th_sample, ph_sample, shape = generate_rotated_grid(N_RES, SPIN_L, SPIN_B)
    
    print(f"[*] Synthesizing Spin-Aligned Map (This may take a minute)...")
    # Sample the field at the rotated coordinates
    field_flat = synthesize_arbitrary(alms, LMAX, th_sample, ph_sample)
    spin_map = field_flat.reshape(shape)
    
    # Calculate Zonal Profile (Latitude Average in Spin Frame)
    zonal_profile = np.mean(spin_map, axis=1) # Average over longitude
    latitudes = np.linspace(90, -90, N_RES)
    
    # --- PLOTTING ---
    fig = plt.figure(figsize=(10, 12), facecolor='#050505')
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    
    # 1. The Spin-Aligned Map
    ax_map = plt.subplot(gs[0])
    # Use 'twilight' or 'hsv' to show phase/structure, or 'magma' for density
    im = ax_map.imshow(spin_map, origin='upper', cmap='twilight', extent=[-180, 180, -90, 90])
    
    # Overlay Equator
    ax_map.axhline(0, color='white', linestyle='--', alpha=0.5, linewidth=1)
    ax_map.text(-170, 2, "SPIN EQUATOR", color='white', fontsize=8)
    
    ax_map.set_title(f"THE UNIVERSE IN SPIN-LOCK | Axis: (l={SPIN_L}, b={SPIN_B})", color='white', fontsize=14)
    ax_map.set_xlabel("Spin Longitude (Phase)", color='gray')
    ax_map.set_ylabel("Spin Latitude", color='gray')
    
    # 2. The Banding Profile
    ax_prof = plt.subplot(gs[1])
    ax_prof.set_facecolor('#111')
    
    ax_prof.plot(latitudes, zonal_profile, color='cyan', linewidth=1.5)
    
    # Highlight the Poles and Equator
    ax_prof.axvline(0, color='white', linestyle='--', alpha=0.3)
    ax_prof.text(2, max(zonal_profile)*0.8, "Equator", color='white', fontsize=8, rotation=90)
    
    ax_prof.set_xlim(90, -90) # North to South
    ax_prof.set_title("LATITUDINAL STRUCTURE DENSITY (Zonal Bands)", color='white', fontsize=10)
    ax_prof.set_xlabel("Latitude (Degrees from Spin North)", color='gray')
    ax_prof.tick_params(colors='gray')
    ax_prof.grid(color='#333', linestyle=':')
    
    plt.tight_layout()
    plt.savefig("cmb_spin_aligned_view.png", dpi=100, facecolor='#050505')
    print("✅ Spin Map Generated. Saved to cmb_spin_aligned_view.png")

if __name__ == "__main__":
    run_spin_mapper()