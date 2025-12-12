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
LMAX = 60                   # Bandwidth
N_RES = 300                 # Higher resolution for gradient calculation
FRAMES = 80                 # Smooth animation
K_START = 0.9
K_END = 1.1
GIF_NAME = "cmb_chaos_convection.gif"

# ======================
# 1. CORE LOGIC
# ======================

def get_alms_and_grid(fits_path, lmax, n_res):
    print(f"[*] Loading CMB Data...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    # Handle standard Planck FITS formats
    if "I" in data.dtype.names: cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names: cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else: cmb = data.astype(np.float64)

    cmb[np.isnan(cmb)] = np.nanmean(cmb)
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # High Res Grid for ALM Extraction
    n_theta_alm = lmax * 3
    n_phi_alm = lmax * 4
    t_alm = np.linspace(0, np.pi, n_theta_alm)
    p_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(t_alm, p_alm, indexing='ij')

    lon = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon*u.deg, b=lat*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    weights = np.sin(TH_ALM) * (t_alm[1] - t_alm[0]) * (p_alm[1] - p_alm[0])

    print("[*] Extracting Spherical Harmonics (ALMs)...")
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    # Synthesis Grid (Lat/Lon)
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')
    
    return alms, TH_GRID, PH_GRID

def build_twisted_field(alms, k, TH, PH, lmax):
    """ Synthesize the field with Twist K applied """
    out = np.zeros_like(TH, dtype=np.complex128)
    twist_factor = k - 1.0
    
    # We only care about the "Substrate" (Filaments), so skip low L (optional, but cleaner)
    # Let's keep all L to see the full convection
    for l in range(1, lmax + 1):
        for m in range(-l, l + 1):
            alm = alms.get((l, m), 0j)
            if alm == 0j: continue
            
            # Apply Twist: e^(i * m * (k-1) * phi)
            phase_shift = np.exp(1j * m * twist_factor * PH)
            Y_lm = sph_harm(m, l, PH, TH)
            
            out += alm * Y_lm * phase_shift
            
    return out.real

def calculate_chaos_metric(field, theta_step, phi_step):
    """ 
    Calculates the 'Chaos' (Local Gradient Magnitude).
    Analogous to 'Frustration' in the Spin Reactor.
    Gradient = sqrt( (dT/dTheta)^2 + (1/sinTheta * dT/dPhi)^2 )
    """
    grad_theta, grad_phi = np.gradient(field, theta_step, phi_step)
    
    # Create a sine mask to handle the spherical coordinate distortion (1/sinTheta)
    # We clip to avoid division by zero at poles
    sin_theta_map = np.sin(np.linspace(0, np.pi, field.shape[0]))
    sin_theta_map = np.clip(sin_theta_map, 0.01, 1.0)
    sin_theta_grid = sin_theta_map[:, np.newaxis]
    
    # Physical Gradient Magnitude
    chaos = np.sqrt(grad_theta**2 + (grad_phi / sin_theta_grid)**2)
    
    return chaos

# ======================
# 2. SCANNER LOOP
# ======================

def run_chaos_scanner():
    alms, TH, PH = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    
    theta_step = np.pi / N_RES
    phi_step = (2*np.pi) / N_RES
    
    K_RANGE = np.linspace(K_START, K_END, FRAMES)
    
    # Store history for the "Convection Plot" (Hovmöller Diagram)
    # Shape: (Frames, Latitude_Bins)
    convection_history = np.zeros((FRAMES, N_RES))
    
    # Store history for "Total Frustration"
    frustration_history = []
    
    frames = []
    
    print(f"[-] Igniting Chaos Scanner (Twist {K_START} -> {K_END})...")
    
    for i, k in enumerate(K_RANGE):
        sys.stdout.write(f"\r[>] Scanning Frame {i+1}/{FRAMES} | k={k:.4f}")
        sys.stdout.flush()
        
        # 1. Synthesize Twisted CMB
        field = build_twisted_field(alms, k, TH, PH, LMAX)
        
        # 2. Calculate Chaos (Gradient Energy)
        chaos_map = calculate_chaos_metric(field, theta_step, phi_step)
        
        # 3. Analyze Convection (Zonal Mean of Chaos)
        # Average chaos across all longitudes (axis 1) for each latitude
        zonal_chaos = np.mean(chaos_map, axis=1)
        convection_history[i, :] = zonal_chaos
        
        # 4. Total System Frustration
        total_frustration = np.sum(chaos_map)
        frustration_history.append(total_frustration)
        
        # --- PLOTTING ---
        fig = plt.figure(figsize=(12, 12), facecolor='#050505')
        gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1.5, 1])
        
        # PANEL 1: The Chaos Map (The Filament Structure)
        ax_map = plt.subplot(gs[0])
        ax_map.set_facecolor('black')
        im = ax_map.imshow(chaos_map, origin='lower', extent=[-180, 180, -90, 90], cmap='inferno', vmin=0, vmax=np.percentile(chaos_map, 99))
        ax_map.set_title(f"CHAOS FIELD TOMOGRAPHY (Gradient Energy) | k={k:.4f}", color='white', fontsize=12)
        ax_map.axis('off')
        
        # PANEL 2: The Convection Current (Hovmöller Diagram)
        # We plot the history UP TO this frame to show the "flow" accumulating
        ax_conv = plt.subplot(gs[1])
        ax_conv.set_facecolor('#111')
        
        # We display the full history buffer, but masked for future frames? 
        # Actually, let's just show the history built so far.
        extent_conv = [K_START, K_END, -90, 90]
        
        # Fill visually with zeros for future
        display_conv = np.zeros_like(convection_history)
        display_conv[:i+1] = convection_history[:i+1]
        
        # Transpose so Time(k) is X, Latitude is Y
        ax_conv.imshow(display_conv.T, origin='lower', extent=extent_conv, cmap='magma', aspect='auto')
        ax_conv.axvline(x=k, color='cyan', linestyle='--', linewidth=1, alpha=0.8) # Current Time Marker
        
        ax_conv.set_ylabel("Latitude", color='gray')
        ax_conv.set_xlabel("Twist Parameter (k)", color='gray')
        ax_conv.set_title("CHAOS CONVECTION FLOW (Zonal Average)", color='orange', fontsize=10)
        ax_conv.tick_params(colors='gray')
        
        # PANEL 3: System Heartbeat (Total Frustration)
        ax_graph = plt.subplot(gs[2])
        ax_graph.set_facecolor('#111')
        ax_graph.plot(K_RANGE[:i+1], frustration_history, color='cyan', linewidth=2)
        ax_graph.set_xlim(K_START, K_END)
        # Dynamic Y lim
        if len(frustration_history) > 1:
            ax_graph.set_ylim(min(frustration_history)*0.99, max(frustration_history)*1.01)
            
        ax_graph.set_title("TOTAL SYSTEM FRUSTRATION", color='cyan', fontsize=10)
        ax_graph.tick_params(colors='gray')
        ax_graph.grid(color='#333', linestyle='--')
        
        plt.tight_layout()
        
        # Save Frame
        fname = f"_chaos_{i:03d}.png"
        plt.savefig(fname, dpi=70, bbox_inches='tight', facecolor='#050505')
        plt.close(fig)
        
        with Image.open(fname) as img:
            frames.append(img.copy())
        os.remove(fname)

    print(f"\n[*] Compiling GIF: {GIF_NAME}")
    frames[0].save(GIF_NAME, save_all=True, append_images=frames[1:], duration=60, loop=0)
    print("✅ Chaos Convection Scan Complete.")

if __name__ == "__main__":
    run_chaos_scanner()