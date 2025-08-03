import os
import pandas as pd
from collections import defaultdict, Counter
import numpy as np
from tqdm import tqdm
from loguru import logger as log
import re
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# --- Constants from your framework ---
KI_REST = 4.14159
KI_MOTION = 4.18879
ALLOWED_AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWYBZXUO"

class ProteinProphet:
    """A simple n-gram model to measure the predictability of a protein sequence."""
    def __init__(self, n=4):
        self.n = n
        self.counts = defaultdict(Counter)
        self.context_totals = Counter()
        self.vocabulary = set()

    def train(self, sequence: str):
        """Trains the n-gram model on a given sequence."""
        self.vocabulary = set(sequence)
        words = list(sequence)
        # Ensure there's enough data for at least one n-gram
        if len(words) < self.n:
            return
        for i in range(len(words) - self.n + 1):
            context = tuple(words[i : i + self.n - 1])
            next_word = words[i + self.n - 1]
            self.counts[context][next_word] += 1
            self.context_totals[context] += 1

    def calculate_predictability(self, sequence: str) -> float:
        """Calculates the mean predictability of a sequence using the trained model."""
        words = list(sequence)
        if len(words) < self.n or not self.vocabulary:
            return 0.0
        
        probabilities = []
        vocab_len = len(self.vocabulary)
        
        for i in range(len(words) - self.n + 1):
            current_context = tuple(words[i : i + self.n - 1])
            word_to_predict = words[i + self.n - 1]
            
            context_count = self.context_totals.get(current_context, 0)
            word_count_in_context = self.counts.get(current_context, {}).get(word_to_predict, 0)
            
            # Using Laplace smoothing to avoid zero probabilities
            probability = (word_count_in_context + 1) / (context_count + vocab_len)
            probabilities.append(probability)
            
        return np.mean(probabilities) if probabilities else 0.0

def parse_fasta_generator(file_path):
    """Generator function to parse large FASTA files record by record, ignoring errors."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        header, seq = None, []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header:
                    yield header, "".join(seq)
                header, seq = line[1:], []
            else:
                seq.append(line)
        if header:
            yield header, "".join(seq)

def analyze_protein_for_ki_rhythm(header, sequence, gulp_size=50, n_gram=3):
    """
    Performs the two-stage analysis on a single protein sequence with robust error handling.
    """
    # 1. --- Sequence Sanitization and Validation ---
    sequence = "".join([char for char in sequence.upper() if char in ALLOWED_AMINO_ACIDS])
    if len(sequence) < gulp_size * 2:  # Need at least two full "gulps" to create a signal
        return None

    # 2. --- Create the Ta Predictability Signal ---
    prophet = ProteinProphet(n=n_gram)
    prophet.train(sequence)

    ta_signal = []
    for i in range(len(sequence) - gulp_size + 1):
        gulp = sequence[i : i + gulp_size]
        predictability = prophet.calculate_predictability(gulp)
        ta_signal.append(predictability)
    
    ta_signal = np.array(ta_signal)

    # --- Stability Check: Ensure the signal has variance ---
    if len(ta_signal) < 10 or np.var(ta_signal) < 1e-9:
        return None

    # 3. --- Analyze the Ta Signal for Ki-Harmonics using FFT ---
    fft_amps = rfft(ta_signal)
    fft_freqs = rfftfreq(len(ta_signal), 1)
    power_spectrum = np.abs(fft_amps)**2

    # --- Stability Check: Ensure there are enough peaks to find harmonics ---
    # Use a dynamic peak height based on the signal's power
    peaks, _ = find_peaks(power_spectrum, height=np.mean(power_spectrum) * 5)
    if len(peaks) < 2:  # Need at least two peaks to identify a fundamental frequency and a harmonic
        return None

    dominant_freqs = fft_freqs[peaks]
    dominant_powers = power_spectrum[peaks]
    
    # Identify the fundamental frequency as the one with the highest power
    sorted_indices = np.argsort(dominant_powers)[::-1]
    fundamental_freq = dominant_freqs[sorted_indices[0]]

    if fundamental_freq == 0: # Avoid division by zero
        return None

    # 4. --- Match Dominant Frequencies to Ki-Ratios ---
    matches = {}
    for freq in dominant_freqs:
        ratio = freq / fundamental_freq
        if abs(ratio - KI_REST) < 0.1:
            matches['Ki_Rest_Ratio'] = ratio
        if abs(ratio - KI_MOTION) < 0.1:
            matches['Ki_Motion_Ratio'] = ratio
            
    if not matches:
        return None
    
    # 5. --- Visualization (Optional but useful) ---
    # Sanitize header for a valid filename
    safe_header = re.sub(r'[|:<>"/\\?*]', '_', header.split()[0][:20])
    output_dir = "ki_rhythm_plots"
    os.makedirs(output_dir, exist_ok=True)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle(f"Ki-Rhythm Analysis for: {header}", fontsize=16)

    # Plot Ta Signal
    ax1.plot(ta_signal, label='Ta Signal (Predictability)', color='cornflowerblue')
    ax1.set_title(f'Local Predictability Along Sequence (Gulp Size: {gulp_size})')
    ax1.set_xlabel('Residue Position (Window Start)')
    ax1.set_ylabel('Predictability Score')
    ax1.grid(True, linestyle='--')
    ax1.legend()
    
    # Plot Power Spectrum
    ax2.semilogy(fft_freqs, power_spectrum, label='Power Spectrum', color='slateblue', alpha=0.7)
    ax2.plot(dominant_freqs, dominant_powers, "x", color='crimson', markersize=10, label='Dominant Frequencies')
    
    # Highlight matched harmonic frequencies
    for label, ratio_val in matches.items():
        ki_constant = KI_REST if 'Rest' in label else KI_MOTION
        matched_freq_val = fundamental_freq * ki_constant
        ax2.axvline(x=matched_freq_val, color='limegreen', linestyle='--', lw=2, label=f'{label} (Theoretical)')

    ax2.legend()
    ax2.set_title('Resonance Spectrum of Predictability Signal')
    ax2.set_xlabel('Frequency (cycles per residue shift)')
    ax2.set_ylabel('Power (log scale)')
    ax2.grid(True, which="both", ls="--")
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(output_dir, f"{safe_header}_ki_from_ta.png"))
    plt.close()

    return {
        'header': header,
        'sequence_length': len(sequence),
        'mean_ta_score': np.mean(ta_signal),
        'ta_fundamental_freq': fundamental_freq,
        'ki_harmonic_matches': matches
    }

def process_fasta_for_ki_rhythms(fasta_path, output_csv, checkpoint_file='ki_rhythm_2.checkpoint', error_log_file='problematic_records.txt'):
    """Main streaming function with robust checkpointing and error handling."""
    log.info(f"Starting Ki-rhythm analysis for {fasta_path}...")
    
    processed_headers = set()
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            processed_headers = set(f.read().splitlines())
        log.info(f"Resuming analysis, found {len(processed_headers)} previously processed records.")

    if not processed_headers and os.path.exists(error_log_file):
        os.remove(error_log_file)

    all_results = []
    
    fasta_generator = parse_fasta_generator(fasta_path)
    # Use a dictionary to handle multi-line FASTA entries for progress bar
    records = {header: seq for header, seq in fasta_generator}
    
    with tqdm(total=len(records), desc="Analyzing Protein Rhythms") as pbar:
        for header, sequence in records.items():
            if header in processed_headers:
                pbar.update(1)
                continue
                
            try:
                # Filter for proteins if your FASTA contains other molecule types
                if 'mol:protein' in header:
                    result = analyze_protein_for_ki_rhythm(header, sequence)
                    if result:
                        all_results.append(result)
            
            except Exception as e:
                log.error(f"An unexpected error occurred processing record: {header[:80]}...")
                log.error(f"--> Error Type: {type(e).__name__}, Message: {e}")
                with open(error_log_file, "a") as f_err:
                    f_err.write(f"Header: {header}\nError: {e}\n---\n")

            # Update checkpoint with the header of the processed record
            with open(checkpoint_file, 'a') as f:
                f.write(f"{header}\n")
            pbar.update(1)

    if all_results:
        df = pd.DataFrame(all_results)
        df.to_csv(output_csv, index=False)
        log.success(f"Analysis complete. Found {len(df)} proteins with potential Ki-rhythms. Results saved to {output_csv}")
    else:
        log.warning("Analysis complete. No significant Ki-rhythms were found in the dataset.")
        
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)
        log.info("Checkpoint file removed.")

if __name__ == '__main__':
    # Make sure to place your FASTA file in the same directory as the script,
    # or provide the full path to the file.
    FASTA_FILE_PATH = 'pdb_seqres.txt'
    OUTPUT_CSV = 'protein_ki_rhythm_analysis.csv'
    
    if not os.path.exists(FASTA_FILE_PATH):
        print(f"Error: Input FASTA file not found at '{FASTA_FILE_PATH}'")
        print("Please ensure the file exists and the path is correct.")
    else:
        process_fasta_for_ki_rhythms(FASTA_FILE_PATH, OUTPUT_CSV)