import os
import numpy as np
import pandas as pd
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from tqdm import tqdm
from loguru import logger as log

# --- Constants from your framework ---
KI_REST = 4.14159
KI_MOTION = 4.18879

# --- Amino Acid Physical Property Map ---
# Using molecular weight to translate biology into a numerical signal
AMINO_ACID_MW = {
    'A': 89.09,  'R': 174.20, 'N': 132.12, 'D': 133.10, 'C': 121.16,
    'Q': 146.15, 'E': 147.13, 'G': 75.07,  'H': 155.16, 'I': 131.17,
    'L': 131.17, 'K': 146.19, 'M': 149.21, 'F': 165.19, 'P': 115.13,
    'S': 105.09, 'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15,
    'X': 0, 'U': 168.06, 'B': 132.61, 'Z': 146.64, 'J': 131.17
}

def parse_fasta(file_path):
    """Parses a FASTA file and returns a dictionary of sequences."""
    sequences = {}
    with open(file_path, 'r') as f:
        header = None
        seq = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header:
                    sequences[header] = "".join(seq)
                header = line[1:]
                seq = []
            else:
                seq.append(line)
        if header:
            sequences[header] = "".join(seq)
    return sequences

def sequence_to_signal(sequence):
    """Translates an amino acid sequence to a numerical signal using molecular weight."""
    return np.array([AMINO_ACID_MW.get(aa.upper(), 0) for aa in sequence])

def analyze_signal_for_ki(signal, sequence_id):
    """
    Performs FFT analysis on a numerical signal to find Ki-harmonics.
    """
    if len(signal) < 10: # Need a minimum length for meaningful FFT
        return None

    # Perform FFT
    fft_amps = rfft(signal)
    fft_freqs = rfftfreq(len(signal), 1) # Frequency is in cycles per amino acid
    power_spectrum = np.abs(fft_amps)**2

    # Find dominant peaks
    peaks, _ = find_peaks(power_spectrum, height=np.mean(power_spectrum) * 5)
    if len(peaks) < 2:
        return None

    dominant_freqs = fft_freqs[peaks]
    dominant_powers = power_spectrum[peaks]

    sorted_indices = np.argsort(dominant_powers)[::-1]
    fundamental_freq = dominant_freqs[sorted_indices[0]]

    # Look for Ki-harmonic ratios
    matches = {}
    for freq in dominant_freqs:
        if fundamental_freq == 0: continue
        ratio = freq / fundamental_freq
        if abs(ratio - KI_REST) < 0.1 or abs(1/ratio - KI_REST) < 0.1:
            matches['Ki_Rest_Ratio'] = ratio
        if abs(ratio - KI_MOTION) < 0.1 or abs(1/ratio - KI_MOTION) < 0.1:
            matches['Ki_Motion_Ratio'] = ratio
            
    if not matches:
        return None

    # --- Visualization ---
    plt.figure(figsize=(12, 6))
    plt.semilogy(fft_freqs, power_spectrum)
    plt.plot(dominant_freqs, dominant_powers, "x", color='red', markersize=10)
    plt.title(f'Protein Resonance Spectrum for {sequence_id[:50]}...')
    plt.xlabel('Frequency (cycles per residue)')
    plt.ylabel('Power Spectral Density')
    plt.grid(True, which="both", ls="--")
    plt.savefig(f"{sequence_id[:20].replace('|','_').replace(':','_')}_resonance.png")
    plt.close()
    
    return {
        'sequence_id': sequence_id,
        'fundamental_freq': fundamental_freq,
        'harmonic_matches': matches
    }

def analyze_fasta_directory(directory_path, output_csv):
    """
    Analyzes all FASTA files in a directory for Ki-resonant signatures.
    """
    fasta_files = [f for f in os.listdir(directory_path) if f.endswith('.fasta')]
    all_results = []

    for filename in tqdm(fasta_files, desc="Analyzing FASTA Files"):
        file_path = os.path.join(directory_path, filename)
        sequences = parse_fasta(file_path)
        
        for header, seq in sequences.items():
            signal = sequence_to_signal(seq)
            result = analyze_signal_for_ki(signal, header)
            if result:
                all_results.append(result)
    
    if all_results:
        results_df = pd.DataFrame(all_results)
        results_df.to_csv(output_csv, index=False)
        log.success(f"Found {len(results_df)} protein sequences with potential Ki-signatures. Results saved to {output_csv}")
    else:
        log.warning("No significant Ki-signatures found in the dataset.")


if __name__ == '__main__':
    # Directory where you downloaded and unzipped the FASTA files
    FASTA_DIR = 'C:/Users/keatw/Downloads/pdb_seqres.txt'
    OUTPUT_CSV = 'protein_ki_resonance_findings.csv'

    if FASTA_DIR == 'path/to/your/fasta/files':
        print("Please update the 'FASTA_DIR' variable to the correct path.")
    else:
        analyze_fasta_directory(FASTA_DIR, OUTPUT_CSV)