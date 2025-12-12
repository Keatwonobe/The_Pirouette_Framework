import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
TARGET_K = 1.96994992  # The resonance frequency we found
LMAX = 60              # Keep resolution matched to previous run
N_RES = 400            # Plot resolution

# Known Anomalies (Galactic Coordinates l, b)
ANOMALIES = {
    "The Cold Spot": (209.0, -57.0),
    "Dipole Apex": (264.0, 48.0),
    "Axis of Evil (Head)": (240.0, 60.0)
}

# ======================
# 1. EXTRACT ALM (Re-used for consistency)
# ======================
def get_alm_from_fits(fits_path, lmax):
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {fits_path}")
        return None

    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)
    
    # Fill NaNs
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    print(f"[*] Decomposing CMB (lmax={lmax})...")
    
    # Generate Integration Grid
    n_theta = lmax * 4
    n_phi = lmax * 8
    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    
    # Sample Map
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]
    weights = np.sin(TH) * dtheta * dphi
    
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH, TH)
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    return alms

# ======================
# 2. HARMONIC SYNTHESIS
# ======================
def synthesize_twisted_universe(alms, k, lmax, res):
    # Standard synthesis grid
    theta = np.linspace(0, np.pi, res)
    phi = np.linspace(-np.pi, np.pi, res)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    
    # Apply Twist to Phase
    PH_twisted = PH * k 
    PH_twisted = (PH_twisted + np.pi) % (2*np.pi) - np.pi
    
    map_out = np.zeros_like(TH, dtype=np.complex128)
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            alm = alms[(l, m)]
            # Reconstruct with twisted phase
            Y_lm_twisted = sph_harm(m, l, PH_twisted, TH)
            map_out += alm * Y_lm_twisted
            
    return map_out.real

# ======================
# 3. OVERLAY EXECUTION
# ======================
def run_anomaly_check():
    alms = get_alm_from_fits(FITS_PATH, LMAX)
    if alms is None: return

    # 1. Regenerate the Pure Harmonic Maps
    print("[*] Regenerating Pure Harmonic Maps...")
    map_ref = synthesize_twisted_universe(alms, 1.0, LMAX, N_RES)
    map_twist = synthesize_twisted_universe(alms, TARGET_K, LMAX, N_RES)
    
    # 2. Compute Interference Magnitude
    interference = np.abs(map_ref - map_twist)
    mean_val = np.mean(interference)
    
    # 3. Plot Setup
    fig, ax = plt.subplots(figsize=(14, 9))
    extent = (-180, 180, -90, 90)
    
    # Plot the Interference Background
    im = ax.imshow(interference, extent=extent, cmap='inferno', origin='lower')
    cbar = plt.colorbar(im, fraction=0.03, pad=0.04)
    cbar.set_label("| Wave Interference | (Amplitude)", fontsize=10)
    
    print("\n[*] Anomaly Report:")
    
    # 4. Plot Anomalies
    markers = ['o', 'D', '^']
    colors = ['cyan', 'lime', 'magenta']
    
    for i, (name, (l, b)) in enumerate(ANOMALIES.items()):
        # Convert Galactic l (0..360) to Plot x (-180..180)
        # Note: FITS maps usually center on 0, wrapping -180 to 180.
        plot_x = l if l <= 180 else l - 360
        plot_y = b
        
        # Sample the map value at this spot
        # Convert physical coord to array index
        col = int((plot_x + 180) / 360 * N_RES)
        row = int((plot_y + 90) / 180 * N_RES)
        col = np.clip(col, 0, N_RES-1)
        row = np.clip(row, 0, N_RES-1)
        
        val = interference[row, col]
        ratio = val / mean_val
        
        status = "NULL (Dark)" if ratio < 0.5 else "PEAK (Bright)" if ratio > 1.5 else "AVG"
        print(f"    -> {name}: {ratio:.2f}x Mean Amplitude [{status}]")
        
        # Draw Marker
        ax.plot(plot_x, plot_y, marker=markers[i], color=colors[i], 
                markersize=12, markeredgecolor='black', markeredgewidth=2,
                label=f"{name} ({status})")
        
        # Draw Label with outline for readability
        txt = ax.text(plot_x + 5, plot_y + 2, name, color='white', 
                      fontsize=11, fontweight='bold')
        txt.set_path_effects([path_effects.withStroke(linewidth=3, foreground='black')])

    # Formatting
    ax.set_title(f"Topological Interference Map (k={TARGET_K})\nPure Harmonic Synthesis (No Grid Artifacts)", fontsize=16)
    ax.set_xlabel("Galactic Longitude (deg)")
    ax.set_ylabel("Galactic Latitude (deg)")
    ax.legend(loc='lower right', frameon=True, facecolor='black', labelcolor='white', framealpha=0.8)
    
    # Grid lines to help orientation
    ax.grid(color='white', linestyle='--', alpha=0.2)
    ax.axhline(0, color='white', alpha=0.3)
    ax.axvline(0, color='white', alpha=0.3)
    
    outfile = "cmb_anomaly_overlay.png"
    plt.savefig(outfile, dpi=150, bbox_inches='tight')
    print(f"[+] Saved overlay to {outfile}")

if __name__ == "__main__":
    run_anomaly_check()