import os
import pandas as pd
from collections import defaultdict, Counter
import numpy as np
from tqdm import tqdm
from loguru import logger as log
import csv

class ProteinProphet:
    """A simple n-gram model to measure the predictability of a protein sequence."""
    def __init__(self, n=4):
        self.n = n
        self.counts = defaultdict(Counter)
        self.context_totals = Counter()
        self.vocabulary = set()

    def train(self, sequence: str):
        """Trains the model on a single protein sequence."""
        self.vocabulary = set(sequence)
        words = list(sequence)
        # Loop range fixed to prevent IndexError
        for i in range(len(words) - self.n + 1):
            context = tuple(words[i:i + self.n - 1])
            next_word = words[i + self.n - 1]
            self.counts[context][next_word] += 1
            self.context_totals[context] += 1

    def calculate_predictability(self, sequence: str) -> float:
        """Calculates the average predictability (Ta proxy) for the entire sequence."""
        words = list(sequence)
        if len(words) < self.n:
            return 0.0

        probabilities = []
        # Loop range fixed
        for i in range(len(words) - self.n + 1):
            current_context = tuple(words[i:i + self.n - 1])
            word_to_predict = words[i + self.n - 1]

            context_count = self.context_totals.get(current_context, 0)
            word_count_in_context = self.counts.get(current_context, {}).get(word_to_predict, 0)
            
            # Laplace smoothing
            if not self.vocabulary: return 0.0 # Avoid division by zero if vocab is empty
            probability = (word_count_in_context + 1) / (context_count + len(self.vocabulary))
            probabilities.append(probability)

        return np.mean(probabilities) if probabilities else 0.0

def parse_fasta_generator(file_path, start_line=0):
    """Generator function that can skip to a specific line number."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for _ in range(start_line):
            next(f) # Skip lines efficiently

        header = None
        seq = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header:
                    yield header, "".join(seq)
                header = line[1:]
                seq = []
            else:
                seq.append(line)
        if header:
            yield header, "".join(seq)

def analyze_fasta_predictability_resilient(fasta_path, output_csv, checkpoint_file='analysis.checkpoint'):
    """
    Analyzes all protein sequences in a FASTA file using a robust,
    line-number-based streaming and checkpointing approach.
    """
    log.info(f"Starting resilient predictability analysis for {fasta_path}...")

    # --- New Checkpointing Logic ---
    start_line = 0
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as f:
                start_line = int(f.read().strip())
            log.info(f"Resuming from line {start_line}.")
        except (ValueError, FileNotFoundError):
            log.warning("Checkpoint file is invalid. Starting fresh.")
    
    total_lines = sum(1 for line in open(fasta_path, 'r', encoding='utf-8', errors='ignore'))

    with open(output_csv, 'a', newline='', encoding='utf-8') as f_out, \
         open(fasta_path, 'r', encoding='utf-8', errors='ignore') as f_in:
        
        writer = csv.writer(f_out)
        if start_line == 0 and os.path.getsize(output_csv) == 0:
            writer.writerow(['header', 'sequence_length', 'predictability_score_Ta'])

        # Fast-forward the input file to the start_line
        for _ in range(start_line):
            f_in.readline()
        
        current_line = start_line
        
        with tqdm(total=total_lines, initial=start_line, desc="Analyzing FASTA") as pbar:
            header = None
            sequence_lines = []
            for line in f_in:
                current_line += 1
                pbar.update(1)
                line = line.strip()
                if line.startswith('>'):
                    if header and sequence_lines:
                        sequence = "".join(sequence_lines)
                        if 'mol:protein' in header and len(sequence) >= 10:
                            prophet = ProteinProphet(n=4)
                            prophet.train(sequence)
                            score = prophet.calculate_predictability(sequence)
                            writer.writerow([header, len(sequence), score])
                            # Update checkpoint after a successful write
                            with open(checkpoint_file, 'w') as cf:
                                cf.write(str(current_line - 1)) # Write the line number of the header

                    header = line[1:]
                    sequence_lines = []
                else:
                    sequence_lines.append(line)
            
            # Process the very last record in the file
            if header and sequence_lines:
                sequence = "".join(sequence_lines)
                if 'mol:protein' in header and len(sequence) >= 10:
                    prophet = ProteinProphet(n=4)
                    prophet.train(sequence)
                    score = prophet.calculate_predictability(sequence)
                    writer.writerow([header, len(sequence), score])


    os.remove(checkpoint_file) # Clean up checkpoint file on success
    log.success(f"Streaming analysis complete. Results are in {output_csv}")
    
    log.info("Sorting final results...")
    final_df = pd.read_csv(output_csv)
    final_df.sort_values('predictability_score_Ta', ascending=True, inplace=True)
    final_df.to_csv(output_csv, index=False)
    
    print("\n--- Top 5 Most UNUSUAL (Least Predictable) Proteins ---")
    print(final_df.head(5))
    print("\n--- Top 5 Most REGULAR (Most Predictable) Proteins ---")
    print(final_df.tail(5))

if __name__ == '__main__':
    FASTA_FILE_PATH = 'pdb_seqres.txt'
    OUTPUT_CSV = 'protein_predictability_analysis_final.csv'

    if not os.path.exists(FASTA_FILE_PATH):
        print(f"Error: Input file '{FASTA_FILE_PATH}' not found.")
    else:
        analyze_fasta_predictability_resilient(FASTA_FILE_PATH, OUTPUT_CSV)