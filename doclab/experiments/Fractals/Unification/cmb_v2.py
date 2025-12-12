#!/usr/bin/env python3
"""
CMB Helical Scanner v2.1: Rigorous Math + Optimized I/O

Key improvements:
- v2.0 Rigorous Math (HelicalOperator, geometric corrections) preserved.
- Spherical Harmonics (my_sph_harm) and a_lm Extraction ported from cmb_helical_gif_3.py.
- Streamlined GIF generation for performance.
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord
from scipy.special import sph_harm
import astropy.units as u
from PIL import Image
import os
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60                   
N_RES_TH = 240              # Sky grid resolution (lat)
N_RES_PH = 480              # Sky grid resolution (lon)
FRAMES = 120                
K_RANGE = np.linspace(0.85, 1.15, FRAMES)
GIF_NAME = "cmb_helical_v2_optimized.gif"
FRAME_DUR = 60              # ms per frame

# Physical constants for interpretation
OMEGA_CMB = 2.0 * np.pi     # Natural frequency unit

# ======================================================
# SPHERICAL HARMONICS WRAPPER (from gif_3)
# ======================================================
try:
    # SciPy >= 1.15
    from scipy.special import sph_harm_y

    def my_sph_harm(m, l, phi_az, theta_pol):
        # match your convention: (m, l, phi, theta)
        return sph_harm_y(l, m, phi_az, theta_pol)

except ImportError:
    # fallback: older SciPy
    from scipy.special import sph_harm as _sph_harm

    def my_sph_harm(m, l, phi_az, theta_pol):
        # NOTE: sph_harm uses (m, l, phi, theta)
        return _sph_harm(m, l, phi_az, theta_pol)

# ======================
# HELICAL CALCULUS v2.0 (PRESERVED)
# ======================

class HelicalOperator:
    """
    Implements the κ-Hamiltonian operator algebra from MATH-028v2.
    """
    
    def __init__(self, omega, kappa):
        self.omega = omega
        self.kappa = kappa
        self.omega_eff = omega * np.sqrt(1 + kappa**2)
        
    def effective_frequency(self):
        return self.omega_eff
        
    def berry_phase(self, phi_initial, phi_final):
        """
        Compute Berry phase accumulated along helical trajectory.
        """
        return self.kappa * self.omega * (phi_final - phi_initial)


# ======================================================
# 1. EXTRACT a_lm ONCE (from gif_3, modified to use my_sph_harm)
# ======================================================
def extract_alms(fits_path, lmax):
    """
    Computes a_lm coefficients using a full-sky integration grid.
    """
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: {fits_path} not found.")
        sys.exit(1)

    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        cmb = data.astype(np.float64)

    cmb[np.isnan(cmb)] = np.nanmean(cmb)

    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")

    # integration grid (coarser than nside; only for alms)
    n_theta = lmax * 4
    n_phi   = lmax * 8
    theta_grid = np.linspace(0.0, np.pi, n_theta)
    phi_grid   = np.linspace(-np.pi, np.pi, n_phi, endpoint=False)
    TH, PH = np.meshgrid(theta_grid, phi_grid, indexing="ij")

    print("[*] Sampling CMB on integration grid...")
    lon_deg = np.rad2deg((PH + 2.0*np.pi) % (2.0*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH)
    coords  = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix    = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_s     = cmb[ipix]

    dtheta = theta_grid[1] - theta_grid[0]
    dphi   = phi_grid[1]   - phi_grid[0]
    weights = np.sin(TH) * dtheta * dphi

    print(f"[*] Extracting a_lm up to LMAX={lmax}...")
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            # Use the robust my_sph_harm wrapper
            Y_lm = my_sph_harm(m, l, PH, TH)
            val  = np.sum(T_s * np.conjugate(Y_lm) * weights)
            alms[(l, m)] = val

    # Synthesis grid for HelicalModeBank
    theta = np.linspace(0, np.pi, N_RES_TH)
    phi = np.linspace(-np.pi, np.pi, N_RES_PH)
    TH_SYN, PH_SYN = np.meshgrid(theta, phi, indexing='ij')

    return alms, TH_SYN, PH_SYN

# ======================
# HELICAL MODE DECOMPOSITION v2.0 (PRESERVED)
# ======================

class HelicalModeBank:
    """
    Pre-computed mode bank for fast helical filtering, using v2.0 math.
    """
    
    def __init__(self, alms, TH, PH, lmax):
        self.alms = alms
        self.TH = TH
        self.PH = PH
        self.lmax = lmax
        self.modes = {}
        
        print("[*] Building helical mode bank v2.0...")
        self._compute_modes()
    
    def _compute_modes(self):
        """
        Decompose CMB into helical eigenmodes (coefficients and structure).
        """
        for l in range(self.lmax + 1):
            if l % 10 == 0:
                print(f"   Processing l={l}...")
                
            for m in range(-l, l + 1):
                alm = self.alms.get((l, m), 0j)
                if alm == 0j: 
                    continue
                
                # Compute base mode (using my_sph_harm convention)
                Y_lm = my_sph_harm(m, l, self.PH, self.TH)
                
                # Estimate natural κ for this mode (preserved v2.0 logic)
                kappa_mode = np.abs(m) / (l + 1) if l > 0 else 0.0
                
                # Store mode with metadata
                self.modes[(l, m)] = {
                    'Y_lm': Y_lm,
                    'a_lm': alm,
                    'kappa': kappa_mode,
                    'omega': OMEGA_CMB * l  # Mode frequency scales with l
                }
    
    def synthesize_helical_v2(self, k_twist):
        """
        Synthesize CMB with helical twist parameter k (v2.0 math).
        
        For each mode (l,m), apply phase correction using:
        - Effective frequency ω_eff = ω√(1+κ²)
        - Geometric phase shift m * Δφ * √(1+κ²)
        """
        map_out = np.zeros_like(self.TH, dtype=np.complex128)
        berry_phase_map = np.zeros_like(self.TH, dtype=np.float64)
        
        # Twist-induced phase shift
        delta_phi = (k_twist - 1.0) * self.PH
        
        for (l, m), mode_data in self.modes.items():
            Y_lm = mode_data['Y_lm']
            alm = mode_data['a_lm']
            kappa = mode_data['kappa']
            omega = mode_data['omega']
            
            # Create helical operator for this mode
            h_op = HelicalOperator(omega, kappa)
            
            # v2.0: Phase correction with geometric factor
            geometric_factor = np.sqrt(1 + kappa**2)
            phase_correction = np.exp(1j * m * delta_phi * geometric_factor)
            
            # Accumulate Berry phase (for analysis)
            berry_phase = h_op.berry_phase(0, delta_phi)
            berry_phase_map += np.abs(alm)**2 * np.real(berry_phase)
            
            # Add helically-corrected mode
            map_out += alm * Y_lm * phase_correction
            
        return map_out.real, berry_phase_map

# ======================
# VISUALIZATION DRIVER (Streamlined for speed)
# ======================

def run_helical_scanner_v2_optimized():
    """
    Execute full helical CMB analysis and generate GIF.
    """
    
    # Load data (using optimized I/O from gif_3)
    alms, TH, PH = extract_alms(FITS_PATH, LMAX)
    
    # Build helical mode bank (preserving v2.0 math)
    mode_bank = HelicalModeBank(alms, TH, PH, LMAX)
    
    print(f"\n[*] Generating {FRAMES} frames...")
    
    # --- Color Scaling (from gif_3 for consistent contrast) ---
    print("[*] Determining color scale...")
    sample_ks = np.linspace(K_RANGE.min(), K_RANGE.max(), 10)
    vals = []
    for k in sample_ks:
        Tk, _ = mode_bank.synthesize_helical_v2(k_twist=k)
        vals.append(np.abs(Tk))
    vals = np.concatenate([v.ravel() for v in vals])
    # Use 1% and 99% percentiles for robust scaling
    vmin, vmax = np.percentile(vals, [1, 99])
    
    frames = []
    # ---------------------------------------------------------
    
    for i, k_val in enumerate(K_RANGE):
        sys.stdout.write(f"\r[>] Frame {i+1}/{FRAMES} | k={k_val:.4f}")
        sys.stdout.flush()
        
        # Synthesize map (using preserved v2.0 logic)
        Tk, _ = mode_bank.synthesize_helical_v2(k_twist=k_val)
        
        # Apply contrast stretch for visualization
        vis = np.abs(Tk) ** 0.45 

        # Create figure (streamlined plot)
        fig, ax = plt.subplots(figsize=(10, 6))
        im = ax.imshow(
            vis,
            # Extent for Galactic coordinates
            extent=(-180, 180, -90, 90),
            origin="lower",
            cmap="RdBu_r",
            vmin=vmin, vmax=vmax,
            aspect="auto",
        )
        ax.set_title(f"Helical CMB Map (v2.1 Rigorous) | k={k_val:.4f}", fontsize=14)
        ax.set_xlabel("Galactic Longitude (deg)")
        ax.set_ylabel("Galactic Latitude (deg)")
        plt.colorbar(im, ax=ax, label='Contrast-Stretched T (a.u.)', fraction=0.05)
        
        # Save frame
        fname = f"_temp_helical_v2_{i:03d}.png"
        plt.savefig(fname, dpi=100, bbox_inches="tight")
        plt.close(fig)
        
        # Load and append
        with Image.open(fname) as img:
            frames.append(img.copy())
        os.remove(fname)
    
    print(f"\n\n[*] Saving GIF: {GIF_NAME}")
    if frames:
        frames[0].save(
            GIF_NAME,
            save_all=True,
            append_images=frames[1:],
            duration=FRAME_DUR,
            loop=0
        )
        print("✅ Done.")
    else:
        print("[!] Error: No frames generated")
    
if __name__ == "__main__":
    run_helical_scanner_v2_optimized()