import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks
import argparse
import os

class KiSignatureAnalyzer:
    """
    Implements Phase 2 & 3 of the Universal Ki-Signature Detection Protocol.
    This class ingests a triaxial time-series, analyzes its frequency
    spectrum, and scores its resonance with the theoretical Ki-harmonics.
    """

    def __init__(self, ki_rest=4.14159, ki_motion=4.18879):
        """
        Initializes the analyzer with the theoretical Ki constants.
        """
        self.KI_REST = ki_rest
        self.KI_MOTION = ki_motion
        self.HARMONIC_RATIOS = {
            "Ki_motion_div": 1 / self.KI_MOTION,
            "Ki_rest_div": 1 / self.KI_REST,
            "Ki_motion_mul": self.KI_MOTION,
            "Ki_rest_mul": self.KI_REST,
            "golden_ratio": 1.618,
            "pi_ratio": np.pi,
        }

    def _calculate_fft(self, time_series_data):
        """
        Performs a Fast Fourier Transform on a time-series.
        """
        n = len(time_series_data)
        if n < 2:
            return np.array([]), np.array([])
            
        yf = rfft(time_series_data)
        xf = rfftfreq(n, 1)
        
        return xf, np.abs(yf)

    def _find_dominant_frequencies(self, freqs, amps, num_peaks=10):
        """
        Finds the most prominent frequency peaks in a spectrum, ignoring DC.
        """
        if len(amps) < 2:
            return [], []
        
        peaks, properties = find_peaks(amps[1:], height=np.mean(amps[1:]))
        
        if len(peaks) == 0:
            return [], []
            
        sorted_peak_indices = sorted(peaks, key=lambda p: properties['peak_heights'][np.where(peaks == p)[0][0]], reverse=True)
        
        top_indices = sorted_peak_indices[:num_peaks]
        
        # --- FIX IS HERE ---
        # Ensure the indices are integers before using them to slice the arrays.
        correct_indices = np.array(top_indices, dtype=int) + 1
        
        dominant_freqs = freqs[correct_indices]
        dominant_amps = amps[correct_indices]
        
        return dominant_freqs, dominant_amps

    def _match_harmonics(self, dominant_freqs, dominant_amps):
        """
        Compares dominant frequencies to theoretical Ki-harmonics
        and calculates a resonance score.
        """
        if len(dominant_freqs) < 2:
            return 0.0, {}

        base_frequency = dominant_freqs[0]
        
        matches = {}
        total_match_strength = 0.0
        
        for i in range(1, len(dominant_freqs)):
            observed_ratio = dominant_freqs[i] / base_frequency
            
            for name, theo_ratio in self.HARMONIC_RATIOS.items():
                if abs(observed_ratio - theo_ratio) < 0.05 or abs(1/observed_ratio - theo_ratio) < 0.05:
                    match_strength = dominant_amps[i] / dominant_amps[0]
                    matches[f"{name}_at_{dominant_freqs[i]:.3f}Hz"] = f"ratio={observed_ratio:.3f}, strength={match_strength:.3f}"
                    total_match_strength += match_strength

        resonance_score = total_match_strength
        return resonance_score, matches

    def analyze_csv(self, input_path: str, visualize: bool = True):
        """
        Main analysis pipeline for a single CSV file.
        """
        print(f"\nAnalyzing file: {os.path.basename(input_path)}")
        try:
            df = pd.read_csv(input_path)
            if df.empty:
                print("  - CSV file is empty. Skipping.")
                return
        except (FileNotFoundError, pd.errors.EmptyDataError) as e:
            print(f"  - Error reading or parsing CSV: {e}")
            return
            
        proxies_to_analyze = ['Ta_proxy', 'Gamma_proxy', 'phi_dot_proxy']
        all_results = {}

        for proxy_name in proxies_to_analyze:
            print(f"  - Analyzing proxy: {proxy_name}")
            time_series = df[proxy_name].values
            
            freqs, amps = self._calculate_fft(time_series)
            dominant_freqs, dominant_amps = self._find_dominant_frequencies(freqs, amps)
            
            if len(dominant_freqs) > 0:
                score, matches = self._match_harmonics(dominant_freqs, dominant_amps)
                all_results[proxy_name] = {
                    'ki_resonance_score': score,
                    'fundamental_freq': dominant_freqs[0],
                    'harmonic_matches': matches
                }
                print(f"    - Ki-Resonance Score: {score:.4f}")
                print(f"    - Fundamental Frequency: {dominant_freqs[0]:.4f} cycles/gulp")
                for match, details in matches.items():
                    print(f"      - Found Match: {match} ({details})")
            else:
                 all_results[proxy_name] = {'ki_resonance_score': 0, 'fundamental_freq': None, 'harmonic_matches': {}}
                 print(f"    - No dominant frequencies found for this proxy.")

            if visualize:
                self._visualize_results(
                    time_series, freqs, amps, dominant_freqs, dominant_amps,
                    proxy_name, os.path.basename(input_path)
                )
        return all_results

    def _visualize_results(self, time_series, freqs, amps, dom_freqs, dom_amps, proxy_name, filename):
        """
        Creates a plot showing the time-series and its FFT spectrum.
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        ax1.plot(time_series, color='cornflowerblue', lw=1.5)
        ax1.set_title(f'Time-Series for {proxy_name}', fontsize=14)
        ax1.set_xlabel('Segment ID (Gulp)')
        ax1.set_ylabel('Proxy Value')
        ax1.grid(True, linestyle='--', alpha=0.6)
        
        if len(freqs) > 1:
            ax2.plot(freqs[1:], amps[1:], color='slateblue', lw=1)
            if len(dom_freqs) > 0:
                ax2.plot(dom_freqs, dom_amps, 'x', color='crimson', markersize=10, label='Dominant Frequencies')
            ax2.set_title(f'Frequency Spectrum for {proxy_name}', fontsize=14)
            ax2.set_xlabel('Frequency (cycles per gulp)')
            ax2.set_ylabel('Amplitude')
            ax2.grid(True, linestyle='--', alpha=0.6)
            ax2.legend()
        
        fig.suptitle(f'Ki-Signature Analysis for: {filename}', fontsize=16, weight='bold')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        output_filename = f"{os.path.splitext(filename)[0]}_{proxy_name}_analysis.png"
        plt.savefig(output_filename)
        print(f"    - Saved visualization to {output_filename}")
        plt.close(fig)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="TEN-KID-1.0 (Prototype): Analyzes triaxial time-series CSVs for Ki-resonant signatures."
    )
    # --- FIX IS HERE ---
    # Corrected typo from 'add_gument' to 'add_argument'
    parser.add_argument("input_files", nargs='+', help="Path(s) to the input CSV file(s) generated by the TriaxialSemanticSensor.")
    
    args = parser.parse_args()

    analyzer = KiSignatureAnalyzer()
    for file_path in args.input_files:
        analyzer.analyze_csv(file_path)