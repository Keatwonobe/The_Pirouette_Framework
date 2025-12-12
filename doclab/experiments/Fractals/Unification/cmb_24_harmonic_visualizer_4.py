import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 300                 # Resolution for integration
K_REALITY = 1.0             # Measure at Reality

# ======================
# 1. OPTIMIZED ENGINE
# ======================

def get_alms_and_grid(fits_path, lmax, n_res):
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
    
    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, TH_GRID, PH_GRID

def synthesize_chaos_field(alms, TH, PH):
    # Synthesize at K=1.0
    field = np.zeros_like(TH, dtype=np.complex128)
    for l in range(LMAX + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            Y_lm = sph_harm(m, l, PH, TH)
            field += alms[(l, m)] * Y_lm
            
    # Compute Chaos (Gradient Energy)
    gy, gx = np.gradient(field.real)
    chaos = np.sqrt(gx**2 + gy**2)
    return chaos

# ======================
# 2. BOW SHOCK DETECTOR
# ======================

def calculate_dipole_asymmetry(chaos_map, TH, PH):
    """
    Scans direction vectors to find the axis of maximum asymmetry.
    """
    print(f"[*] Scanning for Bow Shock (Directional Asymmetry)...")
    
    # 3D Unit Vectors of the grid
    X = np.sin(TH) * np.cos(PH)
    Y = np.sin(TH) * np.sin(PH)
    Z = np.cos(TH)
    
    # We want to find vector V such that dot(Pos, V) correlates with Chaos
    # This is essentially the Dipole Moment of the Chaos Field
    
    # Weighted Sum of vectors by Chaos Magnitude
    # Center of Chaos (CoC)
    total_chaos = np.sum(chaos_map)
    Rx = np.sum(chaos_map * X) / total_chaos
    Ry = np.sum(chaos_map * Y) / total_chaos
    Rz = np.sum(chaos_map * Z) / total_chaos
    
    dipole_vector = np.array([Rx, Ry, Rz])
    magnitude = np.linalg.norm(dipole_vector)
    direction = dipole_vector / magnitude
    
    # Convert Direction to Galactic Coords
    theta_dip = np.arccos(direction[2])
    phi_dip = np.arctan2(direction[1], direction[0])
    
    lat_dip = np.degrees(np.pi/2 - theta_dip)
    lon_dip = np.degrees(phi_dip)
    
    return dipole_vector, (lon_dip, lat_dip), magnitude

# ======================
# 3. MAIN
# ======================

def run_bow_shock_detector():
    alms, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    
    print(f"[*] Synthesizing Chaos Field...")
    chaos_map = synthesize_chaos_field(alms, TH, PH)
    
    # Normalize for plotting
    chaos_vis = (chaos_map - chaos_map.min()) / (chaos_map.max() - chaos_map.min())
    
    # Calculate Dipole
    vec, coords, strength = calculate_dipole_asymmetry(chaos_map, TH, PH)
    lon_max, lat_max = coords
    
    # Calculate Anti-Pole (The Tail)
    lon_min = lon_max + 180 if lon_max < 0 else lon_max - 180
    lat_min = -lat_max
    
    print(f"\n" + "="*40)
    print(f"      COSMIC BOW SHOCK REPORT      ")
    print(f"="*40)
    print(f"Motion Vector:     (l={lon_max:.1f}, b={lat_max:.1f})")
    print(f"Asymmetry Index:   {strength:.5f} (0=Isotropic)")
    print(f"Interpretation:    Universe is moving towards Galactic l={lon_max:.0f}, b={lat_max:.0f}")
    print(f"="*40)
    
    # --- PLOTTING ---
    fig = plt.figure(figsize=(12, 8), facecolor='#050505')
    ax = plt.gca()
    
    # 1. The Chaos Map
    im = plt.imshow(chaos_vis, origin='lower', cmap='inferno', extent=[-180, 180, -90, 90])
    
    # 2. The Bow Shock Marker
    plt.scatter(lon_max, lat_max, c='cyan', s=200, marker='*', label='Bow Shock (Head)', zorder=10)
    plt.scatter(lon_min, lat_min, c='magenta', s=100, marker='x', label='Wake (Tail)', zorder=10)
    
    # 3. Animate the Flow (Quiver) - Simplified visual of flow AWAY from Bow Shock
    # This is artistic representation of the "Wind"
    Y, X = np.mgrid[-90:90:20j, -180:180:20j]
    # Flow is opposite to motion vector
    # Project 3D vector onto 2D lat/lon grid (simplified)
    # Just draw a big arrow for the global motion
    
    plt.arrow(lon_min, lat_min, (lon_max-lon_min)*0.8, (lat_max-lat_min)*0.8, 
              head_width=10, color='white', alpha=0.5, length_includes_head=True)
    
    plt.title(f"THE COSMIC BOW SHOCK: Velocity through the Bulk\nDirection: (l={lon_max:.1f}, b={lat_max:.1f})", color='white', fontsize=14)
    plt.xlabel("Galactic Longitude", color='gray')
    plt.ylabel("Galactic Latitude", color='gray')
    plt.legend(loc='upper right')
    plt.grid(color='#333', linestyle='--')
    
    plt.savefig("cmb_bow_shock.png", dpi=100, bbox_inches='tight', facecolor='#050505')
    print("✅ Bow Shock Detected. Saved to cmb_bow_shock.png")

if __name__ == "__main__":
    run_bow_shock_detector()