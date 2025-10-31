import numpy as np
import obspy
from scipy.signal import gausspulse
from datetime import datetime, timezone

# --- Constants from the Pirouette Prime Series ---
# As defined in PPS-033 and the ki_mseed_analyzer_advanced_4.py script.
# Ki represents the fundamental constant of motion-locked phase evolution.
KI_MOTION = 4.18879  # Approximately 4π/3

class SyntheticSeismogramGenerator:
    """
    Generates synthetic seismograms (.mseed files) containing predictable 
    'Ki-modulated interference fringes' based on the Pirouette Prime Series.

    This model is derived from:
    - PPS-036: The Spider's Web, A Unified Field Model
      The signal's energy and modulation are based on the core Lagrangian:
      L_interaction = g * Gamma * (dT_a/dt) * cos(Delta_phi_Ki)

    - PPS-037: Experimental Predictions & Testable Signatures
      The signal structure simulates the rhythmic "thumper" gravitational 
      wave bursts predicted from "Maw" objects.
    """

    def __init__(self, config):
        """
        Initializes the generator with a configuration dictionary.
        
        Args:
            config (dict): A dictionary containing all necessary parameters.
        """
        self.config = config
        self.validate_config()

    def validate_config(self):
        """Ensures the provided configuration is valid."""
        required_keys = [
            'duration_s', 'sampling_rate_hz', 'station_info',
            'thump_rhythm_hz', 'thump_carrier_hz', 'thump_bandwidth',
            'pattern', 'pirouette_params', 'output_filename'
        ]
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required configuration key: {key}")
        
        if self.config['thump_carrier_hz'] >= self.config['sampling_rate_hz'] / 2:
            raise ValueError(
                "Thump carrier frequency must be less than the Nyquist frequency "
                "(sampling_rate / 2)."
            )

    def generate_signal(self):
        """
        Generates the full time-series signal based on the configuration.
        This corrected version properly centers each thump wavelet and handles
        boundary conditions.
        
        Returns:
            np.ndarray: The generated signal as a NumPy array.
        """
        # Unpack configuration for easier access
        duration = self.config['duration_s']
        sr = self.config['sampling_rate_hz']
        thump_rhythm = self.config['thump_rhythm_hz']
        pattern_str = self.config['pattern']
        
        # Create the main signal array
        num_samples = int(duration * sr)
        signal = np.zeros(num_samples)
        
        # --- Pre-calculate the base wavelet shape for efficiency ---
        wavelet_duration = 2.0
        wavelet_len = int(wavelet_duration * sr)
        t_wavelet = np.linspace(-wavelet_duration/2, wavelet_duration/2, wavelet_len, endpoint=False)
        
        fc = self.config['thump_carrier_hz']
        bw = self.config['thump_bandwidth']
        f_ki = fc / KI_MOTION
        
        signal1 = np.cos(2 * np.pi * fc * t_wavelet)
        signal2 = np.cos(2 * np.pi * (fc + f_ki) * t_wavelet)
        interference_signal = signal1 + signal2
        envelope = np.exp(-(t_wavelet**2) / (2 * (1/(2*np.pi*fc*bw))**2))
        base_wavelet = envelope * interference_signal
        
        # --- Loop through and place each thump ---
        num_thumps = int(duration * thump_rhythm)
        thump_interval = 1.0 / thump_rhythm
        
        for i in range(num_thumps):
            thump_time = i * thump_interval
            
            # Determine amplitude for this specific thump based on the pattern
            pattern_char = pattern_str[i % len(pattern_str)]
            g = self.config['pirouette_params']['g_coupling']
            gamma = self.config['pirouette_params']['gamma_confinement']
            dTa_dt = self.config['pirouette_params']['dTa_dt_coherence_rate']
            
            amplitude_modifier = 1.0
            if pattern_char == 'B': amplitude_modifier = 1.5
            elif pattern_char == 'C': amplitude_modifier = 0.5
            amplitude = g * gamma * dTa_dt * amplitude_modifier
            
            thump_wavelet = amplitude * base_wavelet
            
            # --- Correctly calculate placement indices ---
            center_index = int(thump_time * sr)
            start_index = center_index - (wavelet_len // 2)
            end_index = start_index + wavelet_len
            
            # Determine the overlapping slice of the signal and the wavelet
            # This robustly handles cases where the wavelet is partially off either end.
            signal_start_slice = max(0, start_index)
            signal_end_slice = min(num_samples, end_index)
            
            wavelet_start_slice = max(0, -start_index)
            wavelet_end_slice = wavelet_len - max(0, end_index - num_samples)
            
            # Add the overlapping part of the wavelet to the signal
            if signal_start_slice < signal_end_slice:
                signal[signal_start_slice:signal_end_slice] += thump_wavelet[wavelet_start_slice:wavelet_end_slice]

        return signal

    def write_mseed(self, signal_data):
        stats = obspy.core.trace.Stats()
        # … same header setup …

        # 1) Choose a scale so your floats fit nicely into int32
        scale = 1e6
        int_data = np.int32(signal_data * scale)

        # 2) Tell ObsPy what that scale means
        stats.calib = 1.0 / scale

        # 3) Build the trace & write as INT32
        trace = obspy.Trace(data=int_data, header=stats)
        stream = obspy.Stream([trace])
        stream.write(
            self.config['output_filename'],
            format="MSEED",
            encoding="INT32"
        )
        print(f"Successfully generated synthetic seismogram: {self.config['output_filename']}")



if __name__ == '__main__':
    # --- Configuration ---
    # This section defines all parameters for the synthetic signal generation.
    # Users should modify this dictionary to customize the output.
    
    # NOTE on frequencies: PPS-037 predicts GHz frequencies for "thumpers".
    # Standard seismic equipment samples in the 1-1000 Hz range.
    # We must therefore downscale the carrier frequency to a representable
    # value (e.g., 80 Hz) to be stored in an MSEED file.
    # The physics (Ki-modulation) is preserved in the signal structure.
    
    config = {
        # General signal properties
        "duration_s": 20.0,          # Total length of the seismogram in seconds
        "sampling_rate_hz": 200,     # Samples per second. Must be > 2 * carrier_hz
        
        # MSEED file station information
        "station_info": {
            "network": "SY",
            "station": "MAW01",
            "location": "00",
            "channel": "BHZ"
        },
        
        # "Thumper" signal properties (from PPS-037)
        "thump_rhythm_hz": 80,       # Repetition rate of thumps (10-100 Hz predicted)
        "thump_carrier_hz": 40,      # Base frequency within each thump (downscaled from GHz)
        "thump_bandwidth": 0.2,      # Fractional bandwidth, controls duration of thump
        
        # Pattern for testing (from user request)
        # 'A' = normal thump, 'B' = strong thump, 'C' = weak thump
        # This pattern will repeat throughout the signal duration.
        "pattern": "AABBC",
        
        # Pirouette physics parameters (from PPS-036 Lagrangian)
        "pirouette_params": {
            "g_coupling": 1.0,               # Coupling constant
            "gamma_confinement": 0.8,        # Gladiator Force (boundary strength)
            "dTa_dt_coherence_rate": 1.0     # Rate of change of Time-Adherence
        },
        
        # Output file
        "output_filename": "synthetic_ki_thumper.mseed"
    }

    try:
        # Initialize and run the generator
        generator = SyntheticSeismogramGenerator(config)
        synthetic_signal = generator.generate_signal()
        print(f"  ▶ Signal length: {len(synthetic_signal)} samples")
        print(f"  ▶ Non-zero samples: {np.count_nonzero(synthetic_signal)}")
        print(f"  ▶ Amplitude range: {synthetic_signal.min():.3e} … {synthetic_signal.max():.3e}")
        generator.write_mseed(synthetic_signal)
        
        # Optional: Plot the generated signal for verification
        try:
            import matplotlib.pyplot as plt
            time_vector = np.linspace(0, config['duration_s'], len(synthetic_signal), endpoint=False)
            plt.figure(figsize=(15, 5))
            plt.plot(time_vector, synthetic_signal)
            plt.title("Generated Synthetic 'Thumper' Signal (Corrected)")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude (Strain)")
            plt.grid(True)
            plt.show()
        except ImportError:
            print("\nMatplotlib not found. Skipping plot.")
            print("To visualize the signal, please install it: pip install matplotlib")

    except Exception as e:
        print(f"An error occurred: {e}")