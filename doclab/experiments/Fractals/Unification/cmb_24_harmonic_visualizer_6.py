import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.interpolate import interp1d
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 400
K_REALITY = 1.0

# The Heading (from previous step)
HEADING_L = 51.8
HEADING_B = -72.9

# ======================
# 1. ENGINE
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
    
    n_theta_alm = lmax * 3; n_phi_alm = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta_alm)
    p_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
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
            
    # Standard Grid
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    return alms, TH_GRID, PH_GRID

def synthesize_structure(alms, TH, PH):
    field = np.zeros_like(TH, dtype=np.complex128)
    for l in range(LMAX + 1):
        for m in range(-l, l + 1):
            if (l, m) not in alms: continue
            Y_lm = sph_harm(m, l, PH, TH)
            field += alms[(l, m)] * Y_lm
    
    # Gradient Energy (Structure)
    gy, gx = np.gradient(field.real)
    return np.sqrt(gx**2 + gy**2)

# ======================
# 2. THE SONAR ROTATOR
# ======================

def rotate_to_heading(structure_map, heading_l, heading_b):
    """
    Rotates the spherical map so the Heading is at the North Pole (top).
    This simplifies the analysis to a simple Zonal Mean (averaging rows).
    """
    print(f"[*] Rotating Universe to Heading (l={heading_l}, b={heading_b})...")
    
    # We need to rotate the coordinate system.
    # Instead of complex math, we'll re-sample the ALMs at rotated coordinates?
    # Actually, simpler to just use healpy/astropy rotation if available, 
    # but we only have the synthesized grid.
    # Let's use coordinate transform on the grid points.
    
    n_res = structure_map.shape[0]
    
    # Target Grid (The Rotated View)
    # North Pole of this grid is our Heading
    theta_t = np.linspace(0, np.pi, n_res)
    phi_t = np.linspace(-np.pi, np.pi, n_res)
    TH_T, PH_T = np.meshgrid(theta_t, phi_t, indexing='ij')
    
    # Convert Target Spherical -> Target Cartesian
    x_t = np.sin(TH_T) * np.cos(PH_T)
    y_t = np.sin(TH_T) * np.sin(PH_T)
    z_t = np.cos(TH_T)
    
    # Rotation Matrix to align Z-axis with Heading
    # Heading Spherical:
    # theta_h = 90 - b
    # phi_h = l
    th_h = np.deg2rad(90 - heading_b)
    ph_h = np.deg2rad(heading_l)
    
    # Rotation 1: Rotate around Z by -phi_h (Align with XZ plane)
    # Rotation 2: Rotate around Y by -theta_h (Align with Z axis)
    # Wait, simpler: We want to Map [0,0,1] to [Heading].
    # So we define the Rotation Matrix R that takes Z to Heading.
    
    # Vector of Heading
    hx = np.sin(th_h) * np.cos(ph_h)
    hy = np.sin(th_h) * np.sin(ph_h)
    hz = np.cos(th_h)
    
    # Construct Basis Vectors for the Rotated Frame
    # New Z is Heading
    z_new = np.array([hx, hy, hz])
    # New Y (arbitrary, say orthogonal to Z and Z_new, or just standard)
    # Let's pick X_new = cross(Y_global, Z_new) normalized
    x_new = np.cross(np.array([0,1,0]), z_new)
    if np.linalg.norm(x_new) < 0.01: x_new = np.array([1,0,0]) # Handle pole case
    x_new /= np.linalg.norm(x_new)
    y_new = np.cross(z_new, x_new)
    
    # Rotation Matrix from Target Frame to Original Frame
    R = np.column_stack((x_new, y_new, z_new))
    
    # Rotate all grid points
    # Points P_orig = R @ P_target
    # Shape (3, N)
    P_target = np.vstack((x_t.flatten(), y_t.flatten(), z_t.flatten()))
    P_orig = R @ P_target
    
    # Convert back to Spherical to sample the original map
    x_o, y_o, z_o = P_orig
    theta_o = np.arccos(np.clip(z_o, -1, 1))
    phi_o = np.arctan2(y_o, x_o)
    
    # Map (theta, phi) to indices
    # Theta 0..pi -> 0..N_RES
    # Phi -pi..pi -> 0..N_RES
    r_idx = (theta_o / np.pi) * (n_res - 1)
    c_idx = ((phi_o + np.pi) / (2*np.pi)) * (n_res - 1)
    
    # Bilinear Interpolation (Manual for speed/deps)
    # Let's just use nearest neighbor for the visualization scan
    r_idx = np.clip(np.round(r_idx), 0, n_res-1).astype(int)
    c_idx = np.clip(np.round(c_idx), 0, n_res-1).astype(int)
    
    rotated_map = structure_map[r_idx, c_idx].reshape(n_res, n_res)
    
    return rotated_map

# ======================
# 3. MAIN
# ======================

def run_bulk_sonar():
    alms, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    
    print(f"[*] Synthesizing Structure...")
    structure = synthesize_structure(alms, TH, PH)
    
    # Normalize
    structure = (structure - structure.min()) / (structure.max() - structure.min())
    
    # Rotate
    sonar_view = rotate_to_heading(structure, HEADING_L, HEADING_B)
    
    # Stack the Signal (Zonal Mean)
    # X-axis: Distance from Bow Shock (Degrees)
    # Y-axis: Average Structure Intensity
    signal_stack = np.mean(sonar_view, axis=1) # Average over longitude
    distance_deg = np.linspace(0, 180, N_RES) # 0 = Nose, 180 = Tail
    
    # FFT for periodicity in the signal
    # We look for "Ringing" in the forward sector (0-60 degrees)
    forward_signal = signal_stack[:N_RES//3]
    forward_signal -= np.mean(forward_signal) # Remove DC
    
    spectrum = np.abs(np.fft.rfft(forward_signal))
    freqs = np.fft.rfftfreq(len(forward_signal), d=(180/N_RES))
    
    # --- PLOTTING ---
    fig = plt.figure(figsize=(10, 12), facecolor='#050505')
    gs = gridspec.GridSpec(3, 1, height_ratios=[2, 1, 1])
    
    # 1. The Sonar View (Rotated Map)
    ax_map = plt.subplot(gs[0])
    im = ax_map.imshow(sonar_view, origin='upper', cmap='inferno', extent=[-180, 180, 180, 0])
    
    # Overlay rings
    for deg in [30, 60, 90]:
        y_pos = deg
        ax_map.axhline(y_pos, color='cyan', linestyle='--', alpha=0.3)
        ax_map.text(-170, y_pos-2, f"{deg}°", color='cyan', fontsize=8)
        
    ax_map.set_title(f"BULK SONAR VIEW | Nose at Top (l={HEADING_L}, b={HEADING_B})", color='white', fontsize=14)
    ax_map.set_ylabel("Angular Distance from Heading", color='gray')
    ax_map.set_xticks([])
    
    # 2. The Ping Return (Stacked Signal)
    ax_sig = plt.subplot(gs[1])
    ax_sig.set_facecolor('#111')
    ax_sig.plot(distance_deg, signal_stack, color='cyan', linewidth=1.5)
    
    # Highlight the Bow Shock Region
    ax_sig.axvspan(0, 30, color='yellow', alpha=0.1, label='Bow Shock Zone')
    ax_sig.set_xlim(0, 180)
    ax_sig.set_title("STRUCTURE DENSITY PROFILE (The Echo)", color='white', fontsize=10)
    ax_sig.set_xlabel("Degrees from Heading", color='gray')
    ax_sig.legend(loc='upper right')
    ax_sig.tick_params(colors='gray')
    ax_sig.grid(color='#333', linestyle=':')
    
    # 3. Frequency Analysis (Is it Crystalline?)
    ax_fft = plt.subplot(gs[2])
    ax_fft.set_facecolor('#111')
    ax_fft.plot(freqs[1:], spectrum[1:], color='lime') # Skip DC
    ax_fft.set_title("FORWARD SECTOR SPECTRUM (Lattice Periodicity Check)", color='white', fontsize=10)
    ax_fft.set_xlabel("Spatial Frequency (Cycles/Degree)", color='gray')
    ax_fft.tick_params(colors='gray')
    ax_fft.grid(color='#333', linestyle=':')
    
    plt.tight_layout()
    plt.savefig("cmb_bulk_sonar.png", dpi=100, facecolor='#050505')
    print("✅ Sonar Ping Complete. Saved to cmb_bulk_sonar.png")

if __name__ == "__main__":
    run_bulk_sonar()