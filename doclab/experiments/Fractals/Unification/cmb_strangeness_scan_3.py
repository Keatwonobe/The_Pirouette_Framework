import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
import astropy.units as u
from astropy.coordinates import SkyCoord
import os
import json

# ==============================================================================
# 1. STRANGENESS METER FRAMEWORK (From strangeness_meter.py)
# ==============================================================================

# Universal constants
F_FUNDAMENTAL = 24.0        # Hz
PROTON_SCALE = 0.8414e-15   # m
UNIVERSE_SCALE = 4.4e26     # m

def universal_clock_phase(scale_meters):
    """Get expected cardioid phase for a scale."""
    log_scale = np.log10(scale_meters)
    log_proton = np.log10(PROTON_SCALE)
    log_universe = np.log10(UNIVERSE_SCALE)
    
    normalized = (log_scale - log_proton) / (log_universe - log_proton)
    phase = normalized * 2 * np.pi
    amplitude = 1 + np.cos(phase)
    
    return phase, amplitude

def calculate_strangeness(observed_frequency_hz, scale_meters):
    """Calculate Universal Strangeness Score (Σ) (Simplified for CMB)."""
    expected_phase, expected_amplitude = universal_clock_phase(scale_meters)
    expected_freq = F_FUNDAMENTAL / expected_amplitude
    
    freq_deviation = abs(observed_frequency_hz - expected_freq) / expected_freq
    freq_alignment = np.exp(-freq_deviation)
    T_a = freq_alignment
    
    # Weights (w_phase=0.3, w_pressure=0.1 are set to 0 contribution)
    w_freq = 0.4
    w_coherence = 0.2
    
    S_freq = freq_deviation
    S_coherence = 1 - T_a
    
    Sigma = (w_freq * S_freq + w_coherence * S_coherence)
    Sigma = min(Sigma, 1.0)
    
    if Sigma < 0.1:
        classification = "Normal"
        color = "green"
    elif Sigma < 0.3:
        classification = "Mildly Strange"
        color = "yellow"
    elif Sigma < 0.6:
        classification = "Strange"
        color = "orange"
    else:
        classification = "Highly Anomalous"
        color = "red"
        
    return Sigma, expected_freq, classification, color

# ==============================================================================
# 2. CMB TWISTER CORE LOGIC (From cmb_twister_math_good_edition.py)
# ==============================================================================

# CONFIGURATION
FITS_PATH = "COM_CompMap_CMB-smica_2048_R1.20.fits"
LMAX = 40          # Lower LMAX for faster synthesis
N_RES = 300        # Plot resolution
K_RANGE = np.linspace(0.99999999, 1.00000001, 60, endpoint=False) 

# SCALING FACTOR: How much the maximum CMB temperature deviation (T_ref - T_twist) 
# scales to frequency deviation. Higher value amplifies the resulting Sigma score.
# This factor is necessary because we don't have an established physical theory
# linking temperature deviation in K_CMB directly to the Pirouette frequency unit (Hz).
CMB_MAGNITUDE_TO_FREQ_FACTOR = 0.5 

YLM_CACHE = None
ALMS_CACHE = None
TH_GRID = None
PH_GRID = None

def get_alm_and_grid(fits_path, lmax, n_res):
    global YLM_CACHE, ALMS_CACHE, TH_GRID, PH_GRID
    if ALMS_CACHE is not None: return
        
    print(f"[*] Loading CMB from {fits_path}...")
    try:
        data = fits.getdata(fits_path)
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {fits_path}")
        print("[!] Please download the FITS file and place it in the same directory.")
        return

    if "I" in data.dtype.names:
        cmb = np.array(data["I"], dtype=np.float64)
    elif "INP_CMB" in data.dtype.names:
        cmb = np.array(data["INP_CMB"], dtype=np.float64)
    else:
        # Fallback to general data structure if specific names are missing
        # This is the most likely code path for R1.20 smica map:
        # It typically uses the 1st extension which is just an array of I values
        try:
             # Assuming the primary data extension contains the map
             cmb = data.field(0) if data.ndim == 1 else data
        except:
             cmb = data.astype(np.float64)

    mask = np.isnan(cmb)
    # Filling NaNs with mean is a simple masking technique for HEALPix borders
    cmb[mask] = np.nanmean(cmb) 
    
    # HEALPix setup
    nside = int(np.sqrt(cmb.size / 12))
    hpix = HEALPix(nside=nside, order="ring", frame="galactic")
    
    # Grid setup for spherical harmonic transform
    n_theta_alm = lmax * 4
    n_phi_alm = lmax * 8
    theta_alm = np.linspace(0, np.pi, n_theta_alm)
    phi_alm = np.linspace(-np.pi, np.pi, n_phi_alm, endpoint=False)
    TH_ALM, PH_ALM = np.meshgrid(theta_alm, phi_alm, indexing='ij')
    
    # Coordinate transformation
    lon_deg = np.rad2deg((PH_ALM + 2*np.pi) % (2*np.pi))
    lat_deg = np.rad2deg(0.5*np.pi - TH_ALM)
    coords = SkyCoord(l=lon_deg*u.deg, b=lat_deg*u.deg, frame="galactic")
    ipix = hpix.lonlat_to_healpix(coords.l, coords.b)
    T_sample = cmb[ipix]
    
    # a_lm computation (spherical transform)
    dtheta = theta_alm[1] - theta_alm[0]
    dphi = phi_alm[1] - phi_alm[0]
    weights = np.sin(TH_ALM) * dtheta * dphi
    
    print(f"[*] Computing a_lm (lmax={lmax})... This may take a moment.")
    alms = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            Y_lm = sph_harm(m, l, PH_ALM, TH_ALM) 
            alms[(l, m)] = np.sum(T_sample * np.conjugate(Y_lm) * weights)
    
    ALMS_CACHE = alms
    
    # Grid setup for map synthesis
    theta = np.linspace(0, np.pi, n_res)
    phi = np.linspace(-np.pi, np.pi, n_res)
    TH_GRID, PH_GRID = np.meshgrid(theta, phi, indexing='ij')

    print(f"[*] Caching UNTWISTED Y_lm on {n_res}x{n_res} grid...")
    YLM_CACHE = {}
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            YLM_CACHE[(l, m)] = sph_harm(m, l, PH_GRID, TH_GRID)
            
def synthesize_twisted_universe_fast(k, lmax):
    """Synthesizes the twisted temperature map T_twist."""
    map_out = np.zeros_like(TH_GRID, dtype=np.complex128)
    delta_phi_multiplier = (k - 1) * PH_GRID
    
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            alm = ALMS_CACHE[(l, m)]
            Y_lm_untwisted = YLM_CACHE[(l, m)]
            phase_corr = np.exp(1j * m * delta_phi_multiplier)
            map_out += alm * Y_lm_untwisted * phase_corr
            
    return map_out.real


# ==============================================================================
# 3. CMB STRANGENESS INTEGRATION (New Main Function)
# ==============================================================================

def run_strangeness_scanner_on_real_data():
    
    get_alm_and_grid(FITS_PATH, LMAX, N_RES)
    if ALMS_CACHE is None: return

    # Setup Strangeness Constants
    SCALE = UNIVERSE_SCALE
    # Expected frequency is 12.0 Hz
    EXPECTED_FREQ = F_FUNDAMENTAL / (1 + np.cos(universal_clock_phase(SCALE)[0]))

    print(f"\n[*] Calculating Reference Map (k=1.0)...")
    T_ref = synthesize_twisted_universe_fast(1.0, LMAX)
    
    all_deviations = []
    strangeness_results = []

    # 1. First Pass: Calculate and Collect Deviation Magnitudes
    print("[*] Pass 1: Calculating Maximum Topological Deviation for k-range...")
    for k_val in K_RANGE:
        T_twist = synthesize_twisted_universe_fast(k_val, LMAX)
        # Interference Magnitude (deviation from reference)
        interference_map = np.abs(T_ref - T_twist)
        # Maximum deviation is the signal for the Strangeness Meter
        max_deviation = np.max(interference_map)
        all_deviations.append(max_deviation)

    all_deviations = np.array(all_deviations)
    max_total_deviation = np.max(all_deviations)
    
    if max_total_deviation == 0:
        print("[!] ERROR: Maximum deviation is zero. Cannot proceed with strangeness scaling.")
        return

    # 2. Second Pass: Calculate Strangeness Scores
    print("[*] Pass 2: Calculating Strangeness Score (Σ) based on deviations...")
    for i, k_val in enumerate(K_RANGE):
        deviation = all_deviations[i]
        
        # Scaling the actual maximum temperature deviation to a frequency deviation factor
        deviation_factor = CMB_MAGNITUDE_TO_FREQ_FACTOR * (deviation / max_total_deviation)
        
        # Observed frequency = Expected frequency * (1 + deviation factor)
        freq_obs = EXPECTED_FREQ * (1.0 + deviation_factor)
        
        sigma, expected_freq, classification, color = calculate_strangeness(freq_obs, SCALE)
        
        strangeness_results.append({
            'k': k_val,
            'max_temp_deviation': deviation,
            'frequency_hz': freq_obs,
            'strangeness_score': sigma,
            'classification': classification,
            'color': color
        })
        
    # --- Visualization ---
    scores = np.array([r['strangeness_score'] for r in strangeness_results])
    colors = [r['color'] for r in strangeness_results]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.scatter(K_RANGE, scores, c=colors, s=150, edgecolors='black', 
               linewidth=1.5, alpha=0.8)
    
    # Plot thresholds
    ax.axhline(0.1, color='green', linestyle='--', alpha=0.5, label='Normal ($\Sigma < 0.1$)')
    ax.axhline(0.3, color='yellow', linestyle='--', alpha=0.5, label='Mildly Strange ($\Sigma < 0.3$)')
    ax.axhline(0.6, color='orange', linestyle='--', alpha=0.5, label='Strange ($\Sigma < 0.6$)')

    ax.set_title('Strangeness Scan of CMB Twist Parameter (k) - REAL DATA INTEGRATION', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('CMB Twist Parameter ($k$)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Strangeness Score ($\Sigma$)', fontsize=12, fontweight='bold')
    ax.ticklabel_format(useOffset=False, style='plain', axis='x')
    ax.tick_params(axis='x', rotation=45)
    
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right')
    
    max_idx = np.argmax(scores)
    k_max = K_RANGE[max_idx]
    sigma_max = scores[max_idx]
    ax.annotate(f'Max Strange ($\Sigma={sigma_max:.3f}$)', 
                (k_max, sigma_max), 
                xytext=(k_max, sigma_max + 0.02),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                horizontalalignment='center',
                fontsize=10)
    
    plt.tight_layout()
    output_filename = 'cmb_strangeness_real_data_plot.png'
    plt.savefig(output_filename, dpi=150)
    print(f"\n✅ Visualization saved: {output_filename}")
    
    # --- Summary & Export (JSON) ---
    summary_output = {
        'framework': 'Pirouette T_a Metric on CMB Twist (Real Data Integration)',
        'scale_meters': SCALE,
        'expected_frequency_hz': EXPECTED_FREQ,
        'scaling_factor_used': CMB_MAGNITUDE_TO_FREQ_FACTOR,
        'scan_results': strangeness_results
    }
    
    json_filename = 'cmb_strangeness_real_data_results.json'
    with open(json_filename, 'w') as f:
        json.dump(summary_output, f, indent=2)
    print(f"✅ Results saved: {json_filename}")

if __name__ == "__main__":
    run_strangeness_scanner_on_real_data()