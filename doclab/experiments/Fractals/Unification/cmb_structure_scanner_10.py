import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from scipy.signal import find_peaks
import astropy.units as u
from astropy.coordinates import SkyCoord
import sys

# ======================
# CONFIGURATION
# ======================
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 60
N_RES = 200                 # Lower res for speed (we need many frames)
FRAMES = 120                # High temporal resolution
K_START = 0.5               # Wide scan to catch the full wave
K_END = 1.5

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
            
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    return alms, theta, phi

def precompute_profiles(alms, lmax, theta_vec):
    m_range = np.arange(-lmax, lmax + 1)
    n_m = len(m_range); n_theta = len(theta_vec)
    zeros_phi = np.zeros_like(theta_vec)
    profiles = np.zeros((n_m, n_theta), dtype=np.complex128)
    for i, m in enumerate(m_range):
        for l in range(max(1, abs(m)), lmax + 1): 
            if (l, m) not in alms: continue
            Y_lm_theta = sph_harm(m, l, zeros_phi, theta_vec)
            profiles[i, :] += alms[(l, m)] * Y_lm_theta
    return profiles, m_range

def synthesize_field(profiles, m_range, phi_vec, k):
    m_col = m_range[:, np.newaxis]
    phi_row = phi_vec[np.newaxis, :]
    phase_matrix = np.exp(1j * m_col * k * phi_row)
    field = (profiles.T @ phase_matrix).real
    return field

def calculate_metrics(field_k, field_next):
    # 1. Divergence (Breath)
    diff = field_next - field_k
    vy, vx = np.gradient(diff)
    dvx_dx = np.gradient(vx, axis=1)
    dvy_dy = np.gradient(vy, axis=0)
    divergence = dvx_dx + dvy_dy
    total_breath = np.sum(divergence)
    
    # 2. Structure Count (Entropy/Complexity)
    # Simple peak count as proxy for L10/L20 dots
    # We use a high threshold to find only "Universes"
    threshold = np.percentile(field_k, 95)
    peaks = np.sum(field_k > threshold)
    
    return total_breath, peaks

# ======================
# 2. SPECTROMETER LOOP
# ======================

def run_spectrometer():
    alms, theta_vec, phi_vec = get_alms_and_grid(FITS_PATH, LMAX, N_RES)
    profiles, m_range = precompute_profiles(alms, LMAX, theta_vec)
    
    k_vals = np.linspace(K_START, K_END, FRAMES)
    
    breath_signal = []
    structure_signal = []
    
    print(f"[*] Recording Cosmic Resonance (k={K_START}->{K_END})...")
    
    for i in range(FRAMES - 1):
        k_curr = k_vals[i]
        k_next = k_vals[i] + 0.001
        
        sys.stdout.write(f"\r[>] Sample {i+1}/{FRAMES} | k={k_curr:.3f}")
        sys.stdout.flush()
        
        field_curr = synthesize_field(profiles, m_range, phi_vec, k_curr)
        field_next = synthesize_field(profiles, m_range, phi_vec, k_next)
        
        breath, structure = calculate_metrics(field_curr, field_next)
        
        breath_signal.append(breath)
        structure_signal.append(structure)
        
    # --- ANALYSIS ---
    breath_signal = np.array(breath_signal)
    structure_signal = np.array(structure_signal)
    
    # Normalize for plotting overlay
    breath_norm = (breath_signal - np.mean(breath_signal)) / np.std(breath_signal)
    struct_norm = (structure_signal - np.mean(structure_signal)) / np.std(structure_signal)
    
    # Find Zero Crossings (Rest Points)
    zero_crossings = np.where(np.diff(np.sign(breath_signal)))[0]
    rest_k = k_vals[zero_crossings]
    
    # FFT Analysis
    freqs = np.fft.rfftfreq(len(breath_signal), d=(k_vals[1]-k_vals[0]))
    fft_spectrum = np.abs(np.fft.rfft(breath_norm))
    peak_idx = np.argmax(fft_spectrum[1:]) + 1 # Ignore DC
    dominant_freq = freqs[peak_idx]
    
    print(f"\n" + "="*40)
    print(f"      COSMIC RESONANCE REPORT      ")
    print(f"="*40)
    print(f"Dominant Frequency: {dominant_freq:.4f} Hz (Cycles per Unit Twist)")
    print(f"Rest Points (k):    {rest_k}")
    print(f"Phase Correlation:  {np.corrcoef(breath_norm, struct_norm)[0,1]:.4f}")
    print(f"="*40)
    
    # Plotting
    fig = plt.figure(figsize=(12, 8), facecolor='#111')
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    
    # 1. The Time Domain (The Wave)
    ax1 = plt.subplot(gs[0])
    ax1.set_facecolor('#050505')
    ax1.plot(k_vals[:-1], breath_norm, color='cyan', label='Cosmic Breath (Divergence)', linewidth=2)
    ax1.plot(k_vals[:-1], struct_norm, color='magenta', label='Structure Count (Universes)', linestyle='--', alpha=0.7)
    
    # Mark Reality
    ax1.axvline(1.0, color='yellow', linestyle=':', label='Reality (k=1.0)')
    
    # Mark Rest Points
    for rk in rest_k:
        ax1.axvline(rk, color='lime', alpha=0.3)
        if abs(rk - 1.0) < 0.1:
            ax1.text(rk, 2, "REST", color='lime', rotation=90, fontsize=8)
            
    ax1.set_title("THE HARMONIC UNIVERSE: Breath vs Structure", color='white', fontsize=14)
    ax1.set_ylabel("Normalized Amplitude", color='gray')
    ax1.legend(loc='upper right')
    ax1.grid(color='#333', linestyle='--')
    ax1.tick_params(colors='gray')
    
    # 2. The Frequency Domain (The Spectrum)
    ax2 = plt.subplot(gs[1])
    ax2.set_facecolor('#050505')
    ax2.plot(freqs, fft_spectrum, color='lime')
    ax2.fill_between(freqs, 0, fft_spectrum, color='lime', alpha=0.2)
    ax2.set_xlabel("Frequency (Cycles / k)", color='gray')
    ax2.set_title(f"RESONANCE SPECTRUM (Peak = {dominant_freq:.2f})", color='white', fontsize=10)
    ax2.grid(color='#333', linestyle='--')
    ax2.tick_params(colors='gray')
    
    plt.tight_layout()
    plt.savefig("cmb_resonance_spectrometer.png", dpi=100, facecolor='#111')
    print("✅ Analysis Complete. Saved to cmb_resonance_spectrometer.png")

if __name__ == "__main__":
    run_spectrometer()