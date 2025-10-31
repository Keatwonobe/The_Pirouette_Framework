import os
import pandas as pd
from collections import defaultdict, Counter
import numpy as np
from tqdm import tqdm
from loguru import logger as log
import csv
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
        self.vocabulary = set(sequence)
        words = list(sequence)
        for i in range(len(words) - self.n + 1):
            context = tuple(words[i:i + self.n - 1])
            next_word = words[i + self.n - 1]
            self.counts[context][next_word] += 1
            self.context_totals[context] += 1

    def calculate_predictability(self, sequence: str) -> float:
        words = list(sequence)
        if len(words) < self.n: return 0.0
        probabilities = []
        for i in range(len(words) - self.n + 1):
            current_context = tuple(words[i:i + self.n - 1])
            word_to_predict = words[i + self.n - 1]
            context_count = self.context_totals.get(current_context, 0)
            word_count_in_context = self.counts.get(current_context, {}).get(word_to_predict, 0)
            if not self.vocabulary: return 0.0
            probability = (word_count_in_context + 1) / (context_count + len(self.vocabulary))
            probabilities.append(probability)
        return np.mean(probabilities) if probabilities else 0.0

def parse_fasta_generator(file_path):
    """Generator function to parse large FASTA files record by record."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        header, seq = None, []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header: yield header, "".join(seq)
                header, seq = line[1:], []
            else:
                seq.append(line)
        if header: yield header, "".join(seq)

def analyze_protein_for_ki_rhythm(header, sequence, gulp_size=50, n_gram=3):
    """
    Performs the two-stage analysis on a single protein sequence.
    """
    # --- FIX: Sanitize the sequence to remove any invalid characters ---
    sequence = "".join([char for char in sequence.upper() if char in ALLOWED_AMINO_ACIDS])

    # --- Stage 1: Create the Ta Predictability Signal ---
    if len(sequence) < gulp_size * 2: # Need enough gulps for a signal
        return None

    prophet = ProteinProphet(n=n_gram)
    prophet.train(sequence) # Train on the whole sequence first

    ta_signal = []
    for i in range(len(sequence) - gulp_size + 1):
        gulp = sequence[i:i + gulp_size]
        predictability = prophet.calculate_predictability(gulp)
        ta_signal.append(predictability)
    
    ta_signal = np.array(ta_signal)
    if len(ta_signal) < 10 or np.var(ta_signal) == 0:
        return None

    # --- Stage 2: Analyze the Ta Signal for Ki-Harmonics ---
    fft_amps = rfft(ta_signal)
    fft_freqs = rfftfreq(len(ta_signal), 1) # Freq in cycles per residue shift
    power_spectrum = np.abs(fft_amps)**2

    peaks, _ = find_peaks(power_spectrum, height=np.mean(power_spectrum) * 5)
    if len(peaks) < 2:
        return None

    dominant_freqs = fft_freqs[peaks]
    dominant_powers = power_spectrum[peaks]
    sorted_indices = np.argsort(dominant_powers)[::-1]
    fundamental_freq = dominant_freqs[sorted_indices[0]]

    matches = {}
    for freq in dominant_freqs:
        if fundamental_freq == 0: continue
        ratio = freq / fundamental_freq
        if abs(ratio - KI_REST) < 0.1: matches['Ki_Rest_Ratio'] = ratio
        if abs(ratio - KI_MOTION) < 0.1: matches['Ki_Motion_Ratio'] = ratio
            
    if not matches:
        return None
    
    # --- Visualization ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    ax1.plot(ta_signal, label=f'Ta Signal (Predictability)', color='cornflowerblue')
    ax1.set_title(f'Local Predictability (Ta) Along Sequence for {header[:40]}...')
    ax1.set_xlabel('Residue Position (Gulp Window Start)')
    ax1.set_ylabel('Predictability Score (Ta Proxy)')
    ax1.grid(True, linestyle='--')
    ax1.legend()
    
    ax2.semilogy(fft_freqs, power_spectrum, label='Power Spectrum of Ta Signal', color='slateblue')
    ax2.plot(dominant_freqs, dominant_powers, "x", color='crimson', markersize=8, label='Dominant Frequencies')
    if matches:
        # Corrected loop for plotting vertical lines for matches
        matched_freqs = {
            'Ki_Rest_Ratio': fundamental_freq * KI_REST,
            'Ki_Motion_Ratio': fundamental_freq * KI_MOTION
        }
        for label, freq_val in matches.items():
            # Use the actual dominant frequency that was matched
             matched_freq_instance = [f for f in dominant_freqs if abs((f / fundamental_freq) - (KI_REST if 'Rest' in label else KI_MOTION)) < 0.1][0]
             ax2.axvline(x=matched_freq_instance, color='limegreen', linestyle='--', lw=2, label=f'{label} Match')

    ax2.legend()
    ax2.set_title(f'Resonance Spectrum of Predictability')
    ax2.set_xlabel('Frequency (cycles per residue shift)')
    ax2.set_ylabel('Power')
    ax2.grid(True, which="both", ls="--")
    plt.tight_layout()
    # Sanitize header for filename
    safe_header = re.sub(r'[|:<>"/\\?*]', '_', header[:20])
    plt.savefig(f"{safe_header}_ki_from_ta.png")
    plt.close()

    return {
        'header': header,
        'sequence_length': len(sequence),
        'mean_ta_score': np.mean(ta_signal),
        'ta_fundamental_freq': fundamental_freq,
        'ki_harmonic_matches': matches
    }

def process_fasta_for_ki_rhythms(fasta_path, output_csv, checkpoint_file='ki_rhythm.checkpoint', error_log_file='problematic_records.txt'):
    """Main streaming function with robust checkpointing and error handling."""
    log.info(f"Starting Ki-rhythm analysis for {fasta_path}...")
    
    processed_count = 0
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            processed_count = int(f.read().strip())
        log.info(f"Resuming from record #{processed_count}")

    # Clear error log on new run (but not on resume)
    if processed_count == 0 and os.path.exists(error_log_file):
        os.remove(error_log_file)

    try:
        total_records = sum(1 for line in open(fasta_path, 'r', encoding='utf-8', errors='ignore') if line.startswith('>'))
    except Exception as e:
        log.error(f"Could not count records in FASTA file. Error: {e}")
        return

    fasta_generator = parse_fasta_generator(fasta_path)
    
    # Skip already processed records
    for _ in range(processed_count):
        next(fasta_generator, None)

    all_results = []
    with tqdm(total=total_records, initial=processed_count, desc="Analyzing Protein Rhythms") as pbar:
        for header, sequence in fasta_generator:
            try:
                if 'mol:protein' in header:
                    result = analyze_protein_for_ki_rhythm(header, sequence)
                    if result:
                        all_results.append(result)
            
            except Exception as e:
                # If any error occurs during analysis, log it and continue
                log.error(f"Skipping record due to error: {header[:80]}...")
                log.error(f"--> Error Type: {type(e).__name__}, Message: {e}")
                with open(error_log_file, "a") as f_err:
                    f_err.write(f"Header: {header}\nError: {e}\n---\n")

            processed_count += 1
            if processed_count % 100 == 0: # Update checkpoint every 100 records
                with open(checkpoint_file, 'w') as f:
                    f.write(str(processed_count))
            pbar.update(1)

    if all_results:
        df = pd.DataFrame(all_results)
        df.to_csv(output_csv, index=False)
        log.success(f"Found {len(df)} proteins with Ki-rhythms. Results saved to {output_csv}")
    else:
        log.warning("No significant Ki-rhythms were found.")
        
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)


if __name__ == '__main__':
    FASTA_FILE_PATH = 'pdb_seqres.txt'
    OUTPUT_CSV = 'protein_ki_rhythm_analysis.csv'
    
    if not os.path.exists(FASTA_FILE_PATH):
        print(f"Error: Input file '{FASTA_FILE_PATH}' not found.")
    else:
        process_fasta_for_ki_rhythms(FASTA_FILE_PATH, OUTPUT_CSV)