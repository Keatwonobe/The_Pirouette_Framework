import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
import cv2
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 512
K_BASE = 1.0
K_Twist = 1.01

# The Hypothesis: Motion Vector (From Bulk Velocity Analysis)
HEADING_L = 51.8
HEADING_B = -72.9

# ======================
# 1. ENGINE (Fixed for Astropy Units)
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
    
    # --- FIX: Explicit Units for Astropy 5.0+ ---
    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi)) * u.deg
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM) * u.deg
    ipix = hpix.lonlat_to_healpix(lon_deg, lat_deg)
    # --------------------------------------------

    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    alms = {}
    print("[*] Extracting Harmonics...")
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, theta, phi, TH_GRID, PH_GRID

def synthesize_field(alms, lmax, theta_vec, phi_vec, k):
    m_range = np.arange(-lmax, lmax + 1)
    n_theta = len(theta_vec)
    zeros_phi = np.zeros_like(theta_vec)
    
    profiles = np.zeros((len(m_range), n_theta), dtype=np.complex128)
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) not in alms: continue
            profiles[i, :] += alms[(l, m)] * sph_harm(m, l, zeros_phi, theta_vec)
            
    phase_matrix = np.exp(1j * m_range[:, None] * k * phi_vec[None, :])
    field = (profiles.T @ phase_matrix).real
    return field

# ======================
# 2. PHYSICS ENGINE (Angular Momentum)
# ======================

def spherical_to_cartesian(l_deg, b_deg):
    """ Converts Galactic (l, b) to unit vector (x, y, z) """
    l = np.deg2rad(l_deg)
    b = np.deg2rad(b_deg)
    # Standard Physics Convention (z=North) matches HEALPix Galactic
    x = np.cos(b) * np.cos(l)
    y = np.cos(b) * np.sin(l)
    z = np.sin(b)
    return np.array([x, y, z])

def cartesian_to_spherical(vec):
    """ Converts unit vector to (l, b) in degrees """
    x, y, z = vec / np.linalg.norm(vec)
    b = np.arcsin(z)
    l = np.arctan2(y, x)
    return np.rad2deg(l), np.rad2deg(b)

def calculate_spin_axis(vx, vy, theta_grid, phi_grid):
    """
    Computes the Total Angular Momentum Vector L = Sum( r x v )
    to find the global axis of rotation.
    """
    print("[*] Integrating Angular Momentum Tensor...")
    
    # 1. Grid Position Vectors (r)
    # theta: 0 (North) -> pi (South)
    # phi: -pi -> pi
    st = np.sin(theta_grid)
    ct = np.cos(theta_grid)
    sp = np.sin(phi_grid)
    cp = np.cos(phi_grid)
    
    rx = st * cp
    ry = st * sp
    rz = ct
    
    # 2. Flow Vectors in 3D (v)
    # vx is along phi (East), vy is along theta (South)
    # Basis Vectors:
    # e_theta (South) = (cos(t)cos(p), cos(t)sin(p), -sin(t))
    # e_phi (East)    = (-sin(p),      cos(p),         0)
    
    # Map 2D optical flow to physical 3D tangent vectors
    # Note: cv2 y-axis is "down" (increasing theta), so +vy is South. Correct.
    # Note: cv2 x-axis is "right" (increasing phi), so +vx is East. Correct.
    
    v_global_x = vx * (-sp) + vy * (ct * cp)
    v_global_y = vx * (cp)  + vy * (ct * sp)
    v_global_z = vx * (0)   + vy * (-st)
    
    # 3. Cross Product (r x v) = Angular Momentum Density
    Lx = ry * v_global_z - rz * v_global_y
    Ly = rz * v_global_x - rx * v_global_z
    Lz = rx * v_global_y - ry * v_global_x
    
    # 4. Integrate (Weighted by Area element sin(theta))
    weights = st
    L_total = np.array([
        np.sum(Lx * weights),
        np.sum(Ly * weights),
        np.sum(Lz * weights)
    ])
    
    # Normalize
    L_norm = L_total / np.linalg.norm(L_total)
    return L_norm

# ======================
# 3. MAIN
# ======================

def run_spin_detector():
    alms, theta_vec, phi_vec, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    
    # Synthesize & Flow
    print(f"[*] Generating Flow Field...")
    f0 = synthesize_field(alms, LMAX, theta_vec, phi_vec, K_BASE)
    f1 = synthesize_field(alms, LMAX, theta_vec, phi_vec, K_Twist)
    
    i1 = cv2.normalize(f0, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    i2 = cv2.normalize(f1, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    flow = cv2.calcOpticalFlowFarneback(i1, i2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    vx, vy = flow[..., 0], flow[..., 1]
    
    # Calculate Axes
    L_vec = calculate_spin_axis(vx, vy, TH, PH)
    M_vec = spherical_to_cartesian(HEADING_L, HEADING_B)
    
    spin_l, spin_b = cartesian_to_spherical(L_vec)
    
    # Calculate Alignment Angle
    dot_prod = np.dot(L_vec, M_vec)
    angle_rad = np.arccos(np.clip(dot_prod, -1.0, 1.0))
    angle_deg = np.degrees(angle_rad)
    
    # Interpret
    # If angle > 90, the spin is opposite to motion (Backspin).
    # We care about the axis line, so min(angle, 180-angle) for "Alignment"
    alignment_error = min(angle_deg, 180 - angle_deg)
    
    print(f"\n[*] GEOMETRIC SOLUTION:")
    print(f"    Motion Vector (Heading): l={HEADING_L:.1f}°, b={HEADING_B:.1f}°")
    print(f"    Spin Vector (Axis):      l={spin_l:.1f}°, b={spin_b:.1f}°")
    print(f"    ---------------------------------------------------")
    print(f"    SPIRAL ANGLE (Theta):    {angle_deg:.2f}°")
    
    if alignment_error < 20:
        shape = "RIFLED BULLET (Spin-Stabilized)"
    elif 70 < alignment_error < 110:
        shape = "ROLLING WHEEL / FRISBEE (Gyroscopic)"
    else:
        shape = "CORKSCREW VORTEX (Oblique Spiral)"
        
    print(f"    CONCLUSION: The Universe is a {shape}.")

    # --- PLOTTING ---
    fig = plt.figure(figsize=(12, 8), facecolor='#050505')
    gs = gridspec.GridSpec(1, 1)
    
    ax = plt.subplot(gs[0], projection="mollweide")
    ax.set_facecolor('#111')
    
    # Plot Background Flow Magnitude
    mag = np.sqrt(vx**2 + vy**2)
    # Map rectangular grid to Mollweide needs re-projection, but for visualization
    # we can just plot the vectors at specific points converted to RA/Dec
    
    # Simplified Visualization: Plot Vectors on Sphere surface
    # We plot the locations of the two poles
    
    # Convert L/B to Radians for Mollweide (RA, Dec)
    # Mollweide expects (-pi, pi) for x, (-pi/2, pi/2) for y
    # Galactic l is 0..360. We need to shift to -180..180
    
    def gal_to_moll(l_deg, b_deg):
        l_rad = np.deg2rad(l_deg)
        b_rad = np.deg2rad(b_deg)
        l_rad = (l_rad + np.pi) % (2*np.pi) - np.pi # Wrap to -pi..pi
        return l_rad, b_rad

    # 1. Motion Vector (Green)
    mx, my = gal_to_moll(HEADING_L, HEADING_B)
    ax.scatter(mx, my, s=500, c='lime', marker='*', label='Velocity Vector (Heading)', zorder=10)
    ax.text(mx+0.1, my, " V", color='lime', fontsize=12, fontweight='bold')
    
    # 2. Spin Vector (Cyan)
    sx, sy = gal_to_moll(spin_l, spin_b)
    ax.scatter(sx, sy, s=500, c='cyan', marker='P', label='Spin Axis', zorder=10)
    ax.text(sx+0.1, sy, " S", color='cyan', fontsize=12, fontweight='bold')
    
    # 3. Connect them with the Spiral Arc
    ax.plot([mx, sx], [my, sy], color='white', linestyle='--', alpha=0.5)
    ax.text((mx+sx)/2, (my+sy)/2, f"{angle_deg:.1f}°", color='white', ha='center', fontsize=10, backgroundcolor='#000')

    ax.grid(color='gray', linestyle=':', alpha=0.5)
    ax.set_title(f"COSMIC KINEMATICS | {shape}", color='white', fontsize=14, pad=20)
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig("cmb_spin_alignment.png", dpi=100, facecolor='#050505')
    print("✅ Geometric Solution Plotted. Saved to cmb_spin_alignment.png")

if __name__ == "__main__":
    run_spin_detector()