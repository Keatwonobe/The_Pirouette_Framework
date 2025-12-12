import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import time

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
TARGET_K = 1.96994992  # The value where you saw the structure
LMAX = 60              # Resolution of the wave simulation (Higher = slower but more detail)
N_RES = 400            # Output image resolution (400x400)

# ======================
# 1. EXTRACT THE "SHEET MUSIC" (ALM)
# ======================
def get_alm_from_fits(fits_path, lmax):
    print(f"[*] Loading CMB from {fits_path}...")
    data = fits.getdata(fits_path)
    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        raise ValueError("Could not find CMB temperature data.")
    
    # Replace NaNs with mean to prevent spectral bleeding
    mask = np.isnan(cmb)
    cmb[mask] = np.nanmean(cmb)
    
    # Setup HEALPix to extract alm
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    print(f"[*] Decomposing CMB into Spherical Harmonics (lmax={lmax})...")
    # We do a rough discrete transform here. 
    # For perfect precision we'd use healpy.map2alm, but to keep dependencies low 
    # we will use a Monte Carlo integration approach on the sphere grid.
    
    # Generate a sampling grid on the sphere
    n_theta = lmax * 4
    n_phi = lmax * 8
    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    
    # Sample the map
    import astropy.units as u
    from astropy.coordinates import SkyCoord
    lon_deg = np.rad2deg((PH + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    # Integrate to get alm (approximate)
    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]
    weights = np.sin(TH) * dtheta * dphi
    
    alms = {}
    print("    -> Computing coefficients...")
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH, TH)
            # Integration: Sum( T * Y_lm_conj * weight )
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
            
    return alms

# ======================
# 2. THE HARMONIC SYNTHESIZER
# ======================
def synthesize_twisted_universe(alms, k, lmax, res):
    print(f"[*] Synthesizing Twisted Universe (k={k}) from pure waves...")
    print("    This effectively simulates T = Sum( a_lm * Y_lm(theta, k*phi) )")
    
    # Create the target viewing grid
    theta = np.linspace(0, np.pi, res)
    phi = np.linspace(-np.pi, np.pi, res) # Square aspect for clarity
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    
    # THE MAGIC: Apply the twist to the coordinate BEFORE generating the wave
    # This avoids pixel interpolation entirely.
    PH_twisted = PH * k 
    
    # We also need to wrap the phase to keep it valid for the math function
    # (Though technically sph_harm handles huge phi, wrapping keeps precision)
    PH_twisted = (PH_twisted + np.pi) % (2*np.pi) - np.pi
    
    map_out = np.zeros_like(TH, dtype=np.complex128)
    
    start_time = time.time()
    
    # Summation Loop
    # We sum the waves directly. No pixels are moved.
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            alm = alms[(l, m)]
            # Reconstruct using the TWISTED phase
            Y_lm_twisted = sph_harm(m, l, PH_twisted, TH)
            map_out += alm * Y_lm_twisted
            
    print(f"    -> Synthesis complete in {time.time() - start_time:.2f}s")
    return map_out.real, TH, PH

# ======================
# 3. PLOTTING
# ======================
def analyze_harmonic_twist():
    # 1. Get coefficients
    alms = get_alm_from_fits(FITS_PATH, LMAX)
    
    # 2. Synthesize Standard (k=1) for reference
    print("\n[*] Generating Reference Map (k=1)...")
    map_ref, _, _ = synthesize_twisted_universe(alms, 1.0, LMAX, N_RES)
    
    # 3. Synthesize Twisted (k=TARGET)
    print(f"\n[*] Generating Twisted Map (k={TARGET_K})...")
    map_twist, TH, PH = synthesize_twisted_universe(alms, TARGET_K, LMAX, N_RES)
    
    # 4. Compute Difference (The Interference Pattern)
    diff = map_ref - map_twist
    
    # 5. Visualization
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Plot 1: The Original (Reconstructed from waves)
    im1 = axes[0].imshow(map_ref, extent=(-180, 180, -90, 90), cmap='coolwarm', origin='lower')
    axes[0].set_title(f"1. Harmonic Reconstruction (k=1, L={LMAX})")
    plt.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)
    
    # Plot 2: The Twisted Wave Function
    im2 = axes[1].imshow(map_twist, extent=(-180, 180, -90, 90), cmap='coolwarm', origin='lower')
    axes[1].set_title(f"2. Twisted Wave Function (k={TARGET_K})")
    plt.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)
    
    # Plot 3: The Interference (The "Lines")
    im3 = axes[2].imshow(np.abs(diff), extent=(-180, 180, -90, 90), cmap='inferno', origin='lower')
    axes[2].set_title("3. Wave Interference (Pure Harmonic)")
    plt.colorbar(im3, ax=axes[2], fraction=0.046, pad=0.04)
    
    plt.suptitle(f"Pure Harmonic Synthesis: Investigating Latent Structure at k={TARGET_K}", fontsize=16)
    plt.savefig(f"harmonic_twist_k_{TARGET_K}.png")
    print(f"[+] Result saved to harmonic_twist_k_{TARGET_K}.png")

if __name__ == "__main__":
    analyze_harmonic_twist()