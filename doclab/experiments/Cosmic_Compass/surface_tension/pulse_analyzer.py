import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
from scipy.stats import gaussian_kde
import pickle

# --- PULSE DETECTION AND ANALYSIS ---
class LyapunovPulseAnalyzer:
    """
    Analyzes the quantized pulse structure in Lyapunov exponent time series.
    
    Each pulse = one quantum transition = one decoherence event = one Pirouette.
    """
    
    def __init__(self, threshold_high=0.7, threshold_low=0.3):
        self.threshold_high = threshold_high
        self.threshold_low = threshold_low
        
    def detect_pulses(self, x, lyap):
        """
        Detects pulses in Lyapunov time series.
        
        A pulse is a region where λ exceeds threshold_high.
        Returns pulse locations, widths, and amplitudes.
        """
        
        # Find peaks (local maxima above threshold)
        peaks, properties = find_peaks(
            lyap, 
            height=self.threshold_high,
            distance=5,  # Pulses must be separated by at least 5 samples
            prominence=0.2
        )
        
        if len(peaks) == 0:
            return None
        
        # Get peak amplitudes
        amplitudes = lyap[peaks]
        
        # Get peak widths at half maximum
        widths, width_heights, left_ips, right_ips = peak_widths(
            lyap, peaks, rel_height=0.5
        )
        
        # Compute x-positions of pulses
        x_positions = x[peaks]
        
        # Compute inter-pulse spacing (recurrence times)
        if len(x_positions) > 1:
            spacings = np.diff(x_positions)
        else:
            spacings = np.array([])
        
        pulse_data = {
            'peaks': peaks,
            'x_positions': x_positions,
            'amplitudes': amplitudes,
            'widths': widths,
            'spacings': spacings,
            'left_edges': left_ips,
            'right_edges': right_ips
        }
        
        return pulse_data
    
    def compute_coherence_time(self, pulse_data, x):
        """
        Computes coherence time = average width of stable regions between pulses.
        """
        
        if pulse_data is None or len(pulse_data['peaks']) < 2:
            return None
        
        # Coherence = time spent in stable state (λ ≈ 0)
        # = spacing between pulses
        
        coherence_times = pulse_data['spacings']
        
        return {
            'mean': np.mean(coherence_times),
            'std': np.std(coherence_times),
            'median': np.median(coherence_times),
            'all': coherence_times
        }
    
    def compute_decoherence_time(self, pulse_data, x):
        """
        Computes decoherence time = average width of pulses (time spent chaotic).
        """
        
        if pulse_data is None:
            return None
        
        # Convert width from sample indices to x-coordinates
        # Approximate: width in samples * mean spacing between samples
        dx_mean = np.mean(np.diff(x))
        decoherence_times = pulse_data['widths'] * dx_mean
        
        return {
            'mean': np.mean(decoherence_times),
            'std': np.std(decoherence_times),
            'median': np.median(decoherence_times),
            'all': decoherence_times
        }
    
    def test_quantization(self, values, name="Observable"):
        """
        Tests if a set of values shows quantization (clustering into discrete levels).
        
        Uses kernel density estimation to find peaks in the distribution.
        """
        
        if len(values) < 3:
            return None
        
        # Remove outliers for cleaner peak detection
        q1, q3 = np.percentile(values, [25, 75])
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        filtered = values[(values >= lower) & (values <= upper)]
        
        if len(filtered) < 3:
            return None
        
        # Kernel density estimate
        kde = gaussian_kde(filtered)
        x_range = np.linspace(filtered.min(), filtered.max(), 200)
        density = kde(x_range)
        
        # Find peaks in density
        peaks, _ = find_peaks(density, prominence=0.1*density.max())
        
        quantization_result = {
            'values': filtered,
            'x_range': x_range,
            'density': density,
            'peak_positions': x_range[peaks],
            'n_levels': len(peaks),
            'is_quantized': len(peaks) >= 2 and len(peaks) <= 10
        }
        
        return quantization_result

# --- VISUALIZATION ---
def visualize_pulse_analysis(manifold_data, analyzer):
    """
    Comprehensive visualization of pulse structure.
    """
    
    # Pick one manifold for detailed analysis
    # Use an unstable manifold (they show cleaner structure)
    m = manifold_data['unstable'][0]
    
    x = m['x']
    y = m['y']
    lyap = m['lyap']
    
    print(f"Analyzing manifold from Saddle {m['saddle']+1}")
    print(f"Length: {len(x)} points")
    
    # Detect pulses
    pulse_data = analyzer.detect_pulses(x, lyap)
    
    if pulse_data is None:
        print("No pulses detected!")
        return
    
    print(f"\nDetected {len(pulse_data['peaks'])} pulses")
    
    # Compute statistics
    coherence = analyzer.compute_coherence_time(pulse_data, x)
    decoherence = analyzer.compute_decoherence_time(pulse_data, x)
    
    # Test for quantization
    spacing_quant = analyzer.test_quantization(pulse_data['spacings'], "Inter-pulse spacing")
    amplitude_quant = analyzer.test_quantization(pulse_data['amplitudes'], "Pulse amplitude")
    width_quant = analyzer.test_quantization(pulse_data['widths'], "Pulse width")
    
    # Create figure
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Plot 1: Lyapunov trace with detected pulses
    ax1 = fig.add_subplot(gs[0, :])
    
    ax1.plot(x, lyap, 'k-', linewidth=1, alpha=0.6, label='Lyapunov λ')
    ax1.plot(x[pulse_data['peaks']], lyap[pulse_data['peaks']], 
            'ro', markersize=10, label='Detected Pulses')
    
    # Mark pulse widths
    for i, peak_idx in enumerate(pulse_data['peaks']):
        left = int(pulse_data['left_edges'][i])
        right = int(pulse_data['right_edges'][i])
        ax1.axvspan(x[left], x[right], alpha=0.2, color='red')
    
    ax1.axhline(analyzer.threshold_high, color='red', linestyle='--', 
               linewidth=1, alpha=0.5, label='Detection Threshold')
    ax1.axhline(analyzer.threshold_low, color='blue', linestyle='--', 
               linewidth=1, alpha=0.5)
    
    ax1.set_xlabel('x position')
    ax1.set_ylabel('Lyapunov λ')
    ax1.set_title('Lyapunov Pulse Structure Along Manifold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Inter-pulse spacing histogram
    ax2 = fig.add_subplot(gs[1, 0])
    
    if spacing_quant is not None:
        ax2.hist(spacing_quant['values'], bins=20, density=True, 
                alpha=0.6, color='blue', edgecolor='black')
        ax2.plot(spacing_quant['x_range'], spacing_quant['density'], 
                'r-', linewidth=2, label='KDE')
        ax2.plot(spacing_quant['peak_positions'], 
                spacing_quant['density'][find_peaks(spacing_quant['density'], 
                                                    prominence=0.1*spacing_quant['density'].max())[0]],
                'ro', markersize=10, label='Quantized Levels')
        
        ax2.set_xlabel('Inter-pulse Spacing Δx')
        ax2.set_ylabel('Density')
        ax2.set_title(f'Recurrence Time Distribution\n{spacing_quant["n_levels"]} Levels Detected')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        if spacing_quant['is_quantized']:
            ax2.text(0.05, 0.95, 'QUANTIZED', transform=ax2.transAxes,
                    fontsize=14, fontweight='bold', color='red',
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    # Plot 3: Pulse amplitude distribution
    ax3 = fig.add_subplot(gs[1, 1])
    
    if amplitude_quant is not None:
        ax3.hist(amplitude_quant['values'], bins=20, density=True,
                alpha=0.6, color='green', edgecolor='black')
        ax3.plot(amplitude_quant['x_range'], amplitude_quant['density'],
                'r-', linewidth=2, label='KDE')
        
        ax3.set_xlabel('Pulse Amplitude (max λ)')
        ax3.set_ylabel('Density')
        ax3.set_title(f'Amplitude Distribution\n{amplitude_quant["n_levels"]} Levels')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        if amplitude_quant['is_quantized']:
            ax3.text(0.05, 0.95, 'QUANTIZED', transform=ax3.transAxes,
                    fontsize=14, fontweight='bold', color='red',
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    # Plot 4: Pulse width distribution
    ax4 = fig.add_subplot(gs[1, 2])
    
    if width_quant is not None:
        ax4.hist(width_quant['values'], bins=20, density=True,
                alpha=0.6, color='orange', edgecolor='black')
        ax4.plot(width_quant['x_range'], width_quant['density'],
                'r-', linewidth=2, label='KDE')
        
        ax4.set_xlabel('Pulse Width (samples)')
        ax4.set_ylabel('Density')
        ax4.set_title(f'Decoherence Time Distribution\n{width_quant["n_levels"]} Levels')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        if width_quant['is_quantized']:
            ax4.text(0.05, 0.95, 'QUANTIZED', transform=ax4.transAxes,
                    fontsize=14, fontweight='bold', color='red',
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    # Plot 5: Coherence vs Decoherence times
    ax5 = fig.add_subplot(gs[2, 0])
    
    if coherence is not None and decoherence is not None:
        ax5.bar(['Coherence\n(stable)', 'Decoherence\n(chaotic)'],
               [coherence['mean'], decoherence['mean']],
               yerr=[coherence['std'], decoherence['std']],
               color=['blue', 'red'], alpha=0.7, capsize=10)
        
        ax5.set_ylabel('Time (Δx units)')
        ax5.set_title('Coherence vs Decoherence Time')
        ax5.grid(True, alpha=0.3, axis='y')
        
        # Compute ratio
        ratio = coherence['mean'] / decoherence['mean']
        ax5.text(0.5, 0.95, f'Ratio: {ratio:.2f}:1', transform=ax5.transAxes,
                fontsize=12, ha='center', va='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Plot 6: Phase space trajectory
    ax6 = fig.add_subplot(gs[2, 1])
    
    # Color by Lyapunov
    scatter = ax6.scatter(x, y, c=lyap, cmap='RdYlBu_r', s=2, alpha=0.6)
    ax6.set_xlabel('x position')
    ax6.set_ylabel('y position')
    ax6.set_title('Phase Space Trajectory\n(Color = Lyapunov λ)')
    ax6.set_aspect('equal')
    plt.colorbar(scatter, ax=ax6, label='λ')
    ax6.grid(True, alpha=0.3)
    
    # Plot 7: Statistics summary
    ax7 = fig.add_subplot(gs[2, 2])
    ax7.axis('off')
    
    summary_text = f"""
QUANTUM STATISTICS
{'='*30}

Pulses Detected: {len(pulse_data['peaks'])}

Coherence Time:
  Mean:   {coherence['mean']:.4f}
  Median: {coherence['median']:.4f}
  Std:    {coherence['std']:.4f}

Decoherence Time:
  Mean:   {decoherence['mean']:.4f}
  Median: {decoherence['median']:.4f}
  Std:    {decoherence['std']:.4f}

Ratio τ_coh/τ_dec: {coherence['mean']/decoherence['mean']:.2f}

QUANTIZATION TEST:
  Spacing:   {"YES" if spacing_quant and spacing_quant['is_quantized'] else "NO"}
  Amplitude: {"YES" if amplitude_quant and amplitude_quant['is_quantized'] else "NO"}
  Width:     {"YES" if width_quant and width_quant['is_quantized'] else "NO"}
    """
    
    ax7.text(0.1, 0.9, summary_text, transform=ax7.transAxes,
            fontsize=10, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    plt.savefig('lyapunov_pulse_analysis.png', dpi=150, bbox_inches='tight')
    print("\nSaved: lyapunov_pulse_analysis.png")
    plt.show()
    
    return pulse_data, coherence, decoherence

# --- MULTI-MANIFOLD ANALYSIS ---
def analyze_all_manifolds(manifold_data, analyzer):
    """
    Analyzes pulse structure across all manifolds to find universal patterns.
    """
    
    print("\n" + "="*60)
    print("MULTI-MANIFOLD PULSE ANALYSIS")
    print("="*60)
    
    all_spacings = []
    all_amplitudes = []
    all_widths = []
    
    for manifold_type in ['stable', 'unstable']:
        print(f"\n{manifold_type.upper()} MANIFOLDS:")
        
        for m in manifold_data[manifold_type]:
            pulse_data = analyzer.detect_pulses(m['x'], m['lyap'])
            
            if pulse_data is None:
                continue
            
            n_pulses = len(pulse_data['peaks'])
            print(f"  Saddle {m['saddle']+1}, Angle {m['angle']:.2f}: "
                  f"{n_pulses} pulses")
            
            if len(pulse_data['spacings']) > 0:
                all_spacings.extend(pulse_data['spacings'])
            all_amplitudes.extend(pulse_data['amplitudes'])
            all_widths.extend(pulse_data['widths'])
    
    # Test for universal quantization
    print("\n" + "="*60)
    print("UNIVERSAL QUANTIZATION TEST")
    print("="*60)
    
    if len(all_spacings) > 10:
        spacing_quant = analyzer.test_quantization(np.array(all_spacings), "All spacings")
        print(f"\nInter-pulse spacing:")
        print(f"  Levels detected: {spacing_quant['n_levels']}")
        print(f"  Quantized: {spacing_quant['is_quantized']}")
        if spacing_quant['is_quantized']:
            print(f"  Level positions: {spacing_quant['peak_positions']}")
    
    if len(all_amplitudes) > 10:
        amp_quant = analyzer.test_quantization(np.array(all_amplitudes), "All amplitudes")
        print(f"\nPulse amplitudes:")
        print(f"  Levels detected: {amp_quant['n_levels']}")
        print(f"  Quantized: {amp_quant['is_quantized']}")

# --- EXECUTION ---
if __name__ == "__main__":
    print("="*60)
    print("LYAPUNOV PULSE ANALYZER")
    print("Extracting quantum structure from classical chaos")
    print("="*60)
    print()
    
    # Load manifold data
    try:
        with open('manifolds_data.pkl', 'rb') as f:
            manifolds = pickle.load(f)
        print("Loaded manifolds_data.pkl")
    except FileNotFoundError:
        print("ERROR: manifolds_data.pkl not found!")
        print("Run integrated_knot_analyzer.py first to generate this file.")
        exit(1)
    
    # Create analyzer
    analyzer = LyapunovPulseAnalyzer(threshold_high=0.7, threshold_low=0.3)
    
    # Detailed analysis of one manifold
    print("\n" + "="*60)
    print("SINGLE MANIFOLD ANALYSIS")
    print("="*60)
    pulse_data, coherence, decoherence = visualize_pulse_analysis(manifolds, analyzer)
    
    # Universal patterns across all manifolds
    analyze_all_manifolds(manifolds, analyzer)
    
    print("\n" + "="*60)
    print("COMPLETE")
    print("="*60)
    print("\nIf you see quantization, you've found the quantum structure.")