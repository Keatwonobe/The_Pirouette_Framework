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

# The "Spin Axis" (Pole of the Rolling Disc)
SPIN_L = -111.3
SPIN_B = 1.8

# The "Dipole Vector" (The Engine?)
# Standard Solar Dipole from Planck 2018
DIPOLE_L = 264.0
DIPOLE_B = 48.3

# ======================
# 1. GEOMETRY ENGINE
# ======================

def get_rotation_matrix(l_target, b_target):
    """ Matrix to rotate Z-axis to Target (Spin Axis) """
    l = np.deg2rad(l_target)
    b = np.deg2rad(b_target)
    sx = np.cos(b) * np.cos(l)
    sy = np.cos(b) * np.sin(l)
    sz = np.sin(b)
    s = np.array([sx, sy, sz])
    z = np.array([0, 0, 1])
    k = np.cross(z, s)
    k_len = np.linalg.norm(k)
    if k_len < 1e-6: return np.eye(3)
    k = k / k_len
    theta = np.arccos(sz)
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    R = np.eye(3) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)
    return R

def get_dipole_in_spin_frame():
    """ Transforms the Dipole Vector into the Spin Coordinate System """
    # 1. Dipole in Galactic Cartesian
    dl = np.deg2rad(DIPOLE_L); db = np.deg2rad(DIPOLE_B)
    dx = np.cos(db) * np.cos(dl)
    dy = np.cos(db) * np.sin(dl)
    dz = np.sin(db)
    v_dipole = np.array([dx, dy, dz])
    
    # 2. Rotation Matrix (Galactic -> Spin Frame)
    # The matrix R takes Z_cam -> Z_spin.
    # So v_spin = R.T @ v_galactic (Inverse rotation)
    R = get_rotation_matrix(SPIN_L, SPIN_B)
    v_prime = R.T @ v_dipole
    
    # 3. Convert back to Spherical (Spin Frame Lat/Lon)
    px, py, pz = v_prime
    lat_prime = np.rad2deg(np.arcsin(pz))
    lon_prime = np.rad2deg(np.arctan2(py, px))
    
    return lon_prime, lat_prime, v_prime, v_dipole

# ======================
# 2. HARMONIC ENGINE
# ======================

def get_alms(fits_path, lmax):
    print(f"[*] Loading CMB Data...")
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
    print("[*] Extracting Harmonics...")
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    return alms

def synthesize_arbitrary(alms, lmax, theta_flat, phi_flat):
    field = np.zeros_like(theta_flat, dtype=np.complex128)
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            Y_lm = sph_harm(m, l, phi_flat, theta_flat)
            field += alms[(l, m)] * Y_lm
    return field.real

def generate_rotated_grid(n_res, l_center, b_center):
    theta_cam = np.linspace(0, np.pi, n_res)
    phi_cam = np.linspace(-np.pi, np.pi, n_res)
    TH_C, PH_C = np.meshgrid(theta_cam, phi_cam, indexing='ij')
    
    vx_c = np.sin(TH_C) * np.cos(PH_C)
    vy_c = np.sin(TH_C) * np.sin(PH_C)
    vz_c = np.cos(TH_C)
    vectors_c = np.vstack((vx_c.flatten(), vy_c.flatten(), vz_c.flatten()))
    
    R = get_rotation_matrix(l_center, b_center)
    vectors_orig = R @ vectors_c
    
    vx_o, vy_o, vz_o = vectors_orig
    theta_o = np.arccos(np.clip(vz_o, -1, 1))
    phi_o = np.arctan2(vy_o, vx_o)
    
    return theta_o, phi_o, (n_res, n_res)

# ======================
# 3. MAIN
# ======================

def run_dipole_flywheel():
    # 1. Calculate Geometry
    d_lon, d_lat, v_prime, v_dip = get_dipole_in_spin_frame()
    
    # Angle between Spin Axis and Dipole Axis
    # Dot product of unit vectors
    # Spin Axis in Spin Frame is (0,0,1)
    # v_prime is Dipole in Spin Frame
    cos_angle = v_prime[2] # z-component
    angle = np.rad2deg(np.arccos(np.clip(cos_angle, -1, 1)))
    
    print(f"[*] GEOMETRIC ALIGNMENT:")
    print(f"    Spin Axis:   l={SPIN_L}, b={SPIN_B}")
    print(f"    Dipole Axis: l={DIPOLE_L}, b={DIPOLE_B}")
    print(f"    Separation Angle: {angle:.2f}°")
    print(f"    Dipole Latitude in Spin Frame: {d_lat:.2f}°")
    
    if abs(d_lat) < 15:
        status = "FLYWHEEL LOCKED (Equatorial)"
    elif abs(abs(d_lat) - 90) < 15:
        status = "AXLE LOCKED (Polar)"
    else:
        status = "OBLIQUE / PRECESSING"
    print(f"    CONCLUSION: {status}")

    # 2. Generate Map
    alms = get_alms(FITS_PATH, LMAX)
    th_sample, ph_sample, shape = generate_rotated_grid(N_RES, SPIN_L, SPIN_B)
    
    print(f"[*] Synthesizing Background Map...")
    field_flat = synthesize_arbitrary(alms, LMAX, th_sample, ph_sample)
    spin_map = field_flat.reshape(shape)
    
    # 3. Plot
    fig = plt.figure(figsize=(10, 8), facecolor='#050505')
    ax = plt.subplot(111)
    
    im = ax.imshow(spin_map, origin='upper', cmap='twilight', extent=[-180, 180, -90, 90])
    
    # Overlay Equator
    ax.axhline(0, color='white', linestyle='--', alpha=0.3)
    ax.text(-175, 2, "SPIN EQUATOR", color='white', fontsize=8)
    
    # Overlay Dipole
    ax.scatter(d_lon, d_lat, s=300, c='lime', marker='*', label='CMB Dipole Vector', zorder=10)
    ax.text(d_lon+5, d_lat, " DIPOLE", color='lime', fontweight='bold')
    
    # Overlay Anti-Dipole
    anti_lon = d_lon + 180 if d_lon < 0 else d_lon - 180
    anti_lat = -d_lat
    ax.scatter(anti_lon, anti_lat, s=300, c='red', marker='x', label='Anti-Dipole', zorder=10)
    
    ax.set_title(f"THE COSMIC ENGINE | Dipole vs Spin Axis ({status})", color='white', fontsize=14)
    ax.set_xlabel("Spin Longitude", color='gray')
    ax.set_ylabel("Spin Latitude", color='gray')
    ax.legend(loc='lower right')
    
    plt.tight_layout()
    plt.savefig("cmb_dipole_flywheel.png", dpi=100, facecolor='#050505')
    print("✅ Analysis Complete. Saved to cmb_dipole_flywheel.png")

if __name__ == "__main__":
    run_dipole_flywheel()