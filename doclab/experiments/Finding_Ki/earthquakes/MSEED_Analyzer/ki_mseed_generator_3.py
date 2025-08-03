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
            'pattern', 'pirouette_params', 'output_filename',
            'noise_level', 'target_int_amplitude', 'taper_duration_s'
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
        This version applies a taper to each wavelet to ensure compatibility
        with Steim compression algorithms.
        
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
        
        # --- Apply a taper to the envelope to smooth the edges ---
        taper_duration = self.config['taper_duration_s']
        taper_samples = int(taper_duration * sr)
        
        taper_samples = min(taper_samples, wavelet_len // 2)
        
        if taper_samples > 0:
            taper_window = np.hanning(taper_samples * 2)
            envelope[:taper_samples] *= taper_window[:taper_samples]
            envelope[-taper_samples:] *= taper_window[taper_samples:]

        base_wavelet = envelope * interference_signal
        
        # --- Loop through and place each thump ---
        num_thumps = int(duration * thump_rhythm)
        thump_interval = 1.0 / thump_rhythm
        
        for i in range(num_thumps):
            thump_time = i * thump_interval
            
            pattern_char = pattern_str[i % len(pattern_str)]
            g = self.config['pirouette_params']['g_coupling']
            gamma = self.config['pirouette_params']['gamma_confinement']
            dTa_dt = self.config['pirouette_params']['dTa_dt_coherence_rate']
            
            amplitude_modifier = 1.0
            if pattern_char == 'B': amplitude_modifier = 1.5
            elif pattern_char == 'C': amplitude_modifier = 0.5
            amplitude = g * gamma * dTa_dt * amplitude_modifier
            
            thump_wavelet = amplitude * base_wavelet
            
            center_index = int(thump_time * sr)
            start_index = center_index - (wavelet_len // 2)
            end_index = start_index + wavelet_len
            
            signal_start_slice = max(0, start_index)
            signal_end_slice = min(num_samples, end_index)
            
            wavelet_start_slice = max(0, -start_index)
            wavelet_end_slice = wavelet_len - max(0, end_index - num_samples)
            
            if signal_start_slice < signal_end_slice:
                signal[signal_start_slice:signal_end_slice] += thump_wavelet[wavelet_start_slice:wavelet_end_slice]
        
        noise_amp = self.config['noise_level']
        if noise_amp > 0:
            noise = np.random.normal(0, noise_amp, num_samples)
            signal += noise

        return signal

    def write_mseed(self, signal_data):
        """
        Writes the generated signal data to an MSEED file using intelligent
        scaling and a robust INT32 encoding. This version uses a more robust
        method for creating the obspy.Trace object.

        Args:
            signal_data (np.ndarray): The signal to write.
        """
        # --- Scaling and Integer Conversion ---
        max_abs_val = np.max(np.abs(signal_data))
        target_int_amp = self.config['target_int_amplitude']
        
        if max_abs_val == 0:
            scale_factor = 1.0
        else:
            scale_factor = target_int_amp / max_abs_val
            
        int_data = np.int32(signal_data * scale_factor)

        # --- Robust Trace Creation ---
        # 1. Create the Trace object from the integer data first.
        #    This allows ObsPy to correctly set npts and other data-dependent stats.
        trace = obspy.Trace(data=int_data)

        # 2. Now, populate the rest of the header information into the trace's stats.
        trace.stats.network = self.config['station_info']['network']
        trace.stats.station = self.config['station_info']['station']
        trace.stats.location = self.config['station_info']['location']
        trace.stats.channel = self.config['station_info']['channel']
        trace.stats.starttime = obspy.UTCDateTime(datetime.now(timezone.utc))
        trace.stats.sampling_rate = self.config['sampling_rate_hz']
        
        # 3. Set the calibration factor to allow conversion back to physical units.
        trace.stats.calib = 1.0 / scale_factor

        # --- DIAGNOSTIC (Post-Creation) ---
        print("\n--- Preparing to Write MSEED ---")
        print(f"Trace Stats (after creation):\n{trace.stats}")
        print("--------------------------------\n")
        
        # 4. Create the Stream and write the file.
        stream = obspy.Stream([trace])
        output_file = self.config['output_filename']
        
        # Explicitly use INT32 encoding. This is a lossless, non-difference
        # based encoding that is robust for synthetic data with sharp onsets.
        stream.write(output_file, format="MSEED", encoding="INT32")
        print(f"Successfully generated synthetic seismogram: {output_file}")


if __name__ == '__main__':
    # --- Configuration ---
    # This section defines all parameters for the synthetic signal generation.
    # Users should modify this dictionary to customize the output.
    
    config = {
        # General signal properties
        "duration_s": 20.0,
        "sampling_rate_hz": 200,
        
        # MSEED file station information
        "station_info": {
            "network": "SY",
            "station": "MAW01",
            "location": "00",
            "channel": "BHZ"
        },
        
        # "Thumper" signal properties (from PPS-037)
        "thump_rhythm_hz": 5,
        "thump_carrier_hz": 40,
        "thump_bandwidth": 0.2,
        
        # Pattern for testing
        "pattern": "AABBC",
        
        # Pirouette physics parameters (from PPS-036 Lagrangian)
        "pirouette_params": {
            "g_coupling": 1.0,
            "gamma_confinement": 0.8,
            "dTa_dt_coherence_rate": 1.0
        },
        
        # Parameters for robust MSEED conversion
        "noise_level": 1e-9,
        "target_int_amplitude": 10**8,
        "taper_duration_s": 0.05,
        
        # Output file
        "output_filename": "synthetic_ki_thumper.mseed"
    }

    try:
        # Initialize and run the generator
        generator = SyntheticSeismogramGenerator(config)
        synthetic_signal = generator.generate_signal()

        # --- DIAGNOSTIC ---
        print("\n--- Signal Generation Complete ---")
        print(f"Float signal length: {len(synthetic_signal)} samples")
        print(f"Float signal non-zero count: {np.count_nonzero(synthetic_signal)}")
        if np.count_nonzero(synthetic_signal) > 0:
             print(f"Float signal min/max: {np.min(synthetic_signal):.3e} / {np.max(synthetic_signal):.3e}")
        else:
            print("Float signal is all zeros.")
        print("--------------------------------\n")

        generator.write_mseed(synthetic_signal)
        
        # Optional: Plot the generated signal for verification
        try:
            import matplotlib.pyplot as plt
            time_vector = np.linspace(0, config['duration_s'], len(synthetic_signal), endpoint=False)
            plt.figure(figsize=(15, 5))
            plt.plot(time_vector, synthetic_signal)
            plt.title("Generated Synthetic 'Thumper' Signal (INT32 Encoding)")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude (Strain)")
            plt.grid(True)
            plt.show()
        except ImportError:
            print("\nMatplotlib not found. Skipping plot.")
            print("To visualize the signal, please install it: pip install matplotlib")

    except Exception as e:
        print(f"An error occurred: {e}")