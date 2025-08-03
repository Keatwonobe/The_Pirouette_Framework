import numpy as np
import obspy
from datetime import datetime, timezone

# --- Constants from the Pirouette Prime Series ---
KI_MOTION = 4.18879  # Approximately 4π/3

# --- Physics Models ---

class Maw:
    """
    A physics-based model for a "Maw" object as described in PPS-037.
    It simulates the buildup and catastrophic release of spacetime tension,
    which dictates the timing and amplitude of the "thumper" events.
    """
    def __init__(self, max_tension, buildup_rate):
        """
        Initializes the Maw model.
        Args:
            max_tension (float): The tension threshold at which a "snap" occurs.
            buildup_rate (float): The rate at which tension accumulates per second.
        """
        self.max_tension = max_tension
        self.buildup_rate = buildup_rate
        self.current_tension = 0.0

    def update(self, dt):
        """Evolves the Maw's internal state over a time step."""
        if self.current_tension < self.max_tension:
            self.current_tension += self.buildup_rate * dt

    def thump(self):
        """
        Checks if a thump should occur and returns its amplitude.
        If a thump occurs, tension is reset.
        """
        if self.current_tension >= self.max_tension:
            # The amplitude of the snap is proportional to the released tension.
            amplitude = self.current_tension
            # Reset tension after the catastrophic release.
            self.current_tension = 0.0
            return amplitude
        return 0.0 # No thump if tension is not critical.


def snap_envelope(t, attack_time, decay_time):
    """
    Generates a physically-motivated envelope with a sharp attack and exponential decay.
    This models the "snap-back" of a spacetime fold from PPS-037.
    
    Args:
        t (np.ndarray): Time vector for the envelope, centered at t=0.
        attack_time (float): The rise time of the envelope.
        decay_time (float): The characteristic decay time (tau) of the ringdown.
    
    Returns:
        np.ndarray: The envelope shape.
    """
    envelope = np.zeros_like(t)
    # Shift time vector to start attack at t=0
    t_shifted = t + attack_time
    
    # Attack phase (e.g., a sine-squared ramp for smoothness)
    attack_mask = (t_shifted > 0) & (t_shifted <= attack_time)
    envelope[attack_mask] = np.sin(np.pi * t_shifted[attack_mask] / (2 * attack_time))**2
    
    # Decay phase (exponential)
    decay_mask = t_shifted > attack_time
    envelope[decay_mask] = np.exp(-(t_shifted[decay_mask] - attack_time) / decay_time)
    
    return envelope


class SyntheticSeismogramGenerator:
    """
    Generates synthetic seismograms (.mseed files) containing predictable 
    'Ki-modulated interference fringes' based on the Pirouette Prime Series.
    """

    def __init__(self, config):
        self.config = config
        self.validate_config()

    def validate_config(self):
        """Ensures the provided configuration is valid."""
        # ... (validation logic remains the same, but would check for new keys)
        pass

    def _create_wavelet(self):
        """
        Pre-calculates the base Ki-modulated wavelet shape.
        """
        sr = self.config['sampling_rate_hz']
        fc = self.config['thump_carrier_hz']
        bw = self.config['thump_bandwidth'] # Note: bw is less critical for snap_envelope
        
        wavelet_duration = 2.0
        wavelet_len = int(wavelet_duration * sr)
        t_wavelet = np.linspace(-wavelet_duration/2, wavelet_duration/2, wavelet_len, endpoint=False)
        
        # Ki-modulated interference signal
        f_ki = fc / KI_MOTION
        signal1 = np.cos(2 * np.pi * fc * t_wavelet)
        signal2 = np.cos(2 * np.pi * (fc + f_ki) * t_wavelet)
        interference_signal = signal1 + signal2
        
        # Choose envelope based on signal type
        if self.config['signal_type'] == 'maw':
            attack = self.config['envelope_params']['attack_time_s']
            decay = self.config['envelope_params']['decay_time_s']
            envelope = snap_envelope(t_wavelet, attack, decay)
        else: # Default to Gaussian for pattern-based signal
             envelope = np.exp(-(t_wavelet**2) / (2 * (1/(2*np.pi*fc*bw))**2))

        return envelope * interference_signal

    def generate_signal(self):
        """
        Routes to the correct signal generation method based on config.
        """
        if self.config['signal_type'] == 'maw':
            return self._generate_maw_signal()
        else:
            return self._generate_pattern_signal()

    def _generate_maw_signal(self):
        """
        Generates a signal based on the Maw physics model.
        """
        print("Generating signal using 'Maw' physics model...")
        duration = self.config['duration_s']
        sr = self.config['sampling_rate_hz']
        num_samples = int(duration * sr)
        signal = np.zeros(num_samples)
        
        maw = Maw(
            max_tension=self.config['maw_params']['max_tension'],
            buildup_rate=self.config['maw_params']['buildup_rate']
        )
        
        base_wavelet = self._create_wavelet()
        wavelet_len = len(base_wavelet)
        
        # Evolve the system sample by sample
        for i in range(num_samples):
            # Update Maw tension
            maw.update(1.0 / sr)
            
            # Check for a thump
            amplitude = maw.thump()
            
            if amplitude > 0:
                # A thump occurred, add its wavelet to the signal
                g = self.config['pirouette_params']['g_coupling']
                gamma = self.config['pirouette_params']['gamma_confinement']
                dTa_dt = self.config['pirouette_params']['dTa_dt_coherence_rate']
                
                # Final amplitude combines Maw physics with Lagrangian params
                final_amplitude = amplitude * g * gamma * dTa_dt
                thump_wavelet = final_amplitude * base_wavelet
                
                # Place the wavelet (centered at current sample i)
                start_index = i - (wavelet_len // 2)
                end_index = start_index + wavelet_len
                
                sig_start = max(0, start_index)
                sig_end = min(num_samples, end_index)
                wav_start = max(0, -start_index)
                wav_end = wavelet_len - max(0, end_index - num_samples)
                
                if sig_start < sig_end:
                    signal[sig_start:sig_end] += thump_wavelet[wav_start:wav_end]

        # Add final noise pass
        noise_amp = self.config['noise_level']
        if noise_amp > 0:
            noise = np.random.normal(0, noise_amp * np.max(np.abs(signal)))
            signal += noise
            
        return signal

    def _generate_pattern_signal(self):
        """
        Generates a signal based on the simple repeating pattern.
        (This is the logic from the previous version).
        """
        print("Generating signal using simple 'pattern' model...")
        duration = self.config['duration_s']
        sr = self.config['sampling_rate_hz']
        thump_rhythm = self.config['thump_rhythm_hz']
        pattern_str = self.config['pattern']
        num_samples = int(duration * sr)
        signal = np.zeros(num_samples)

        base_wavelet = self._create_wavelet()
        wavelet_len = len(base_wavelet)

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
        scaling and a robust INT32 encoding.
        """
        max_abs_val = np.max(np.abs(signal_data))
        target_int_amp = self.config['target_int_amplitude']
        
        if max_abs_val == 0:
            scale_factor = 1.0
        else:
            scale_factor = target_int_amp / max_abs_val
            
        int_data = np.int32(signal_data * scale_factor)

        trace = obspy.Trace(data=int_data)

        trace.stats.network = self.config['station_info']['network']
        trace.stats.station = self.config['station_info']['station']
        trace.stats.location = self.config['station_info']['location']
        trace.stats.channel = self.config['station_info']['channel']
        trace.stats.starttime = obspy.UTCDateTime(datetime.now(timezone.utc))
        trace.stats.sampling_rate = self.config['sampling_rate_hz']
        trace.stats.calib = 1.0 / scale_factor

        print("\n--- Preparing to Write MSEED ---")
        print(f"Trace Stats (after creation):\n{trace.stats}")
        print("--------------------------------\n")
        
        stream = obspy.Stream([trace])
        output_file = self.config['output_filename']
        
        stream.write(output_file, format="MSEED", encoding="INT32")
        print(f"Successfully generated synthetic seismogram: {output_file}")


if __name__ == '__main__':
    config = {
        "duration_s": 2000.0,
        "sampling_rate_hz": 400, # Increased for better resolution of sharp attacks
        
        "station_info": {
            "network": "SY", "station": "MAW01",
            "location": "00", "channel": "BHZ"
        },
        
        # --- Signal Model Selection ---
        "signal_type": "maw", # "pattern" or "maw"
        
        # --- Maw Physics Parameters (for "maw" type) ---
        "maw_params": {
            "max_tension": 1.0,     # Tension threshold for a thump
            "buildup_rate": 0.0,    # Tension units per second
        },
        
        # --- Envelope Shape (for "maw" type) ---
        "envelope_params": {
            "attack_time_s": 0.005, # Very sharp attack
            "decay_time_s": 0.08,   # Exponential ringdown
        },
        
        # --- Thumper & Pattern (for "pattern" type) ---
        "thump_rhythm_hz": 5,
        "thump_carrier_hz": 80,
        "thump_bandwidth": 0.2,
        "pattern": "AABBC",
        
        # --- Universal Pirouette Parameters ---
        "pirouette_params": {
            "g_coupling": 1.0,
            "gamma_confinement": 0.5,
            "dTa_dt_coherence_rate": 1.0
        },
        
        # --- MSEED Conversion Parameters ---
        "noise_level": 0.01, # Relative to peak signal amplitude
        "target_int_amplitude": 10**8,
        "taper_duration_s": 0.05, # Only used for Gaussian envelope in pattern mode
        
        "output_filename": "control_null_hypothesis.mseed"
    }

    try:
        generator = SyntheticSeismogramGenerator(config)
        synthetic_signal = generator.generate_signal()

        print("\n--- Signal Generation Complete ---")
        print(f"Signal length: {len(synthetic_signal)} samples")
        print(f"Non-zero count: {np.count_nonzero(synthetic_signal)}")
        if np.count_nonzero(synthetic_signal) > 0:
             print(f"Min/Max: {np.min(synthetic_signal):.3e} / {np.max(synthetic_signal):.3e}")
        else:
            print("Signal is all zeros.")
        print("--------------------------------\n")

        generator.write_mseed(synthetic_signal)
        
        try:
            import matplotlib.pyplot as plt
            time_vector = np.linspace(0, config['duration_s'], len(synthetic_signal), endpoint=False)
            plt.figure(figsize=(15, 5))
            plt.plot(time_vector, synthetic_signal)
            plt.title("Generated Synthetic 'Maw Thumper' Signal")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude (Strain)")
            plt.grid(True)
            plt.show()
        except ImportError:
            print("\nMatplotlib not found. Skipping plot.")
            print("To visualize the signal, please install it: pip install matplotlib")

    except Exception as e:
        print(f"An error occurred: {e}")