import numpy as np
import matplotlib.pyplot as plt
import json
import os

# ==============================================================================
#  1. CONSTANTS & FRAMEWORK (from strangeness_meter.py)
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

def calculate_strangeness(observed_frequency_hz, scale_meters, 
                         observed_phase_rad=None, temporal_pressure=None):
    """
    Calculate Universal Strangeness Score (Σ).
    (Only key components for the CMB application are used/weighted)
    """
    
    # Expected values from universal clock (for the universe scale)
    expected_phase, expected_amplitude = universal_clock_phase(scale_meters)
    expected_freq = F_FUNDAMENTAL / expected_amplitude
    
    # Component 1: Frequency Deviation (ΔF)
    freq_deviation = abs(observed_frequency_hz - expected_freq) / expected_freq
    
    # Component 2: Phase Deviation (ΔΦ) - Not provided for the twist, set to 0
    phase_deviation = 0.0
    
    # Component 3: Coherence Violation (ΔC) - Derived from frequency alignment
    freq_alignment = np.exp(-freq_deviation)
    phase_alignment = 1.0 # Due to lack of phase observation
    T_a = freq_alignment * phase_alignment
    
    # Component 4: Pressure Anomaly (ΔΓ) - Not provided, set to 0
    pressure_deviation = 0.0
    
    # === STRANGENESS SCORE (Σ) ===
    # Using weights from strangeness_meter.py
    w_freq = 0.4
    w_phase = 0.3
    w_coherence = 0.2
    w_pressure = 0.1
    
    S_freq = freq_deviation
    S_coherence = 1 - T_a
    
    Sigma = (w_freq * S_freq + 
             w_phase * 0.0 + 
             w_coherence * S_coherence + 
             w_pressure * 0.0) # Phase and Pressure set to 0
    
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
    
    return {
        'strangeness_score': Sigma,
        'classification': classification,
        'color': color,
        'T_a': T_a,
        'components': {
            'frequency_deviation': S_freq,
            'coherence_violation': S_coherence,
        },
        'expected_freq': expected_freq
    }

# ==============================================================================
#  2. CMB STRANGENESS SCANNER LOGIC (Mocking CMB process)
# ==============================================================================

def cmb_strangeness_scanner():
    
    print("=" * 80)
    print("CMB TOPOLOGICAL STRANGENESS SCANNER")
    print("Integrating Pirouette T_a into CMB Twist Model")
    print("=" * 80)
    
    # --- Config from cmb_twister_math_good_edition.py ---
    GIF_FRAMES = 60
    # K_RANGE is the twist parameter
    K_RANGE = np.linspace(0.99999999, 1.00000001, GIF_FRAMES, endpoint=False) 
    
    # --- Strangeness Meter Setup ---
    SCALE = UNIVERSE_SCALE
    # Expected frequency for Universe scale (calculated to be 12.0 Hz)
    EXPECTED_FREQ = F_FUNDAMENTAL / (1 + np.cos(universal_clock_phase(SCALE)[0]))
    
    print(f"\nScanning CMB scale ({SCALE:.2e} m) against Universal Clock (Exp Freq: {EXPECTED_FREQ:.4f} Hz)")
    print(f"Twist parameter (k) range: {K_RANGE.min():.10f} to {K_RANGE.max():.10f}")

    # --- MOCK SIMULATION of CMB Interference Magnitude (D_k) ---
    # NOTE: The actual CMB FITS file is missing, so the interference map 
    # synthesis is bypassed and the deviation is SIMULATED.
    # Deviation is expected to be minimal at k=1.0 (untwisted).
    
    k_dev = K_RANGE - 1.0
    max_k_dev_sq = np.max(k_dev**2)
    
    # Simulated deviation (D_k) is a proxy for how much the map changes
    # D_k is proportional to |k-1|^2
    # We normalize this deviation and set a max deviation factor of 0.5%
    MAX_FREQ_DEVIATION_FACTOR = 0.005 # Max 0.5% deviation from expected freq
    
    # Map the squared deviation to the frequency deviation factor
    # This acts as the "Topological Anomaly" signal
    freq_dev_factor = MAX_FREQ_DEVIATION_FACTOR * (k_dev**2 / max_k_dev_sq)
    
    # Observed frequency is the expected frequency plus the deviation
    observed_frequencies = EXPECTED_FREQ * (1.0 + freq_dev_factor)
    
    print(f"\nSimulated Max Frequency Deviation: {EXPECTED_FREQ * freq_dev_factor.max():.4f} Hz")
    
    # --- Strangeness Calculation for each k ---
    
    strangeness_results = []
    
    print("\nCalculating Strangeness Score (Σ) for each twist parameter k...")
    for i, k in enumerate(K_RANGE):
        freq_obs = observed_frequencies[i]
        
        result = calculate_strangeness(
            observed_frequency_hz=freq_obs,
            scale_meters=SCALE,
            observed_phase_rad=None, # Phase/Pressure not applicable/available
            temporal_pressure=None
        )
        
        strangeness_results.append({
            'k': k,
            'frequency_hz': freq_obs,
            'strangeness_score': result['strangeness_score'],
            'classification': result['classification'],
            'color': result['color']
        })
        
    # --- Visualization ---
    
    scores = np.array([r['strangeness_score'] for r in strangeness_results])
    colors = [r['color'] for r in strangeness_results]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Scatter plot of Strangeness Score vs. Twist Parameter (k)
    scatter = ax.scatter(K_RANGE, scores, c=colors, s=150, 
                        edgecolors='black', linewidth=1.5, alpha=0.8)
    
    # Plot thresholds
    ax.axhline(0.1, color='green', linestyle='--', alpha=0.5, label='Normal ($\Sigma < 0.1$)')
    ax.axhline(0.3, color='yellow', linestyle='--', alpha=0.5, label='Mildly Strange ($\Sigma < 0.3$)')
    ax.axhline(0.6, color='orange', linestyle='--', alpha=0.5, label='Strange ($\Sigma < 0.6$)')
    
    # Add a curve fit to show the parabolic nature of the simulation
    p = np.polyfit(K_RANGE, scores, 2)
    k_smooth = np.linspace(K_RANGE.min(), K_RANGE.max(), 300)
    scores_smooth = np.polyval(p, k_smooth)
    ax.plot(k_smooth, scores_smooth, color='gray', linestyle='-', alpha=0.6, 
            label='Simulated Strangeness Trend')

    ax.set_title('Strangeness Meter Scan of CMB Twist Parameter (k)', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('CMB Twist Parameter ($k$)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Strangeness Score ($\Sigma$)', fontsize=12, fontweight='bold')
    ax.ticklabel_format(useOffset=False, style='plain') # Avoid scientific notation on x-axis
    ax.tick_params(axis='x', rotation=45)
    
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right')
    
    # Highlight the most strange point
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
    output_filename = 'cmb_strangeness_scanner_plot.png'
    plt.savefig(output_filename, dpi=150)
    print(f"\n✅ Visualization saved: {output_filename}")
    
    # --- Summary & Export (JSON) ---
    
    summary_output = {
        'framework': 'Pirouette T_a (Time-Adherence) Metric on CMB Twist',
        'scale_meters': SCALE,
        'expected_frequency_hz': EXPECTED_FREQ,
        'scan_results': strangeness_results
    }
    
    json_filename = 'cmb_strangeness_scan_results.json'
    with open(json_filename, 'w') as f:
        json.dump(summary_output, f, indent=2)
    print(f"✅ Results saved: {json_filename}")

cmb_strangeness_scanner()