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
        # CORRECTED: Loop range fixed to prevent IndexError
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
        # CORRECTED: Loop range fixed
        for i in range(len(words) - self.n + 1):
            # CORRECTED: Use a different variable name 'current_context' to avoid bugs
            current_context = tuple(words[i:i + self.n - 1])
            word_to_predict = words[i + self.n - 1]

            context_count = self.context_totals.get(current_context, 0)
            word_count_in_context = self.counts.get(current_context, {}).get(word_to_predict, 0)

            # CORRECTED: This logic was the source of the main TypeError
            probability = (word_count_in_context + 1) / (context_count + len(self.vocabulary))
            probabilities.append(probability)

        return np.mean(probabilities) if probabilities else 0.0

def parse_fasta_generator(file_path):
    """Generator function to parse large FASTA files record by record."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
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

def analyze_fasta_predictability_streaming(fasta_path, output_csv):
    """
    Analyzes all protein sequences in a FASTA file using a streaming approach.
    """
    log.info(f"Starting streaming predictability analysis for {fasta_path}...")

    # --- Checkpointing Logic ---
    processed_headers = set()
    if os.path.exists(output_csv):
        try:
            df_existing = pd.read_csv(output_csv)
            if 'header' in df_existing.columns:
                processed_headers = set(df_existing['header'])
                log.info(f"Resuming. Found {len(processed_headers)} already processed sequences.")
        except (pd.errors.EmptyDataError, KeyError, UnicodeDecodeError):
            log.info("Output CSV is empty or malformed. Starting fresh.")
        except Exception as e:
            log.warning(f"Could not read existing CSV, starting fresh. Error: {e}")

    # Count total records for tqdm progress bar
    total_records = sum(1 for line in open(fasta_path, 'r', encoding='utf-8', errors='ignore') if line.startswith('>'))

    # Open the output file in append mode
    with open(output_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header if the file is new or was empty
        if not processed_headers:
            writer.writerow(['header', 'sequence_length', 'predictability_score_Ta'])

        fasta_generator = parse_fasta_generator(fasta_path)

        with tqdm(total=total_records, desc="Analyzing Sequences") as pbar:
            pbar.update(len(processed_headers))
            for header, sequence in fasta_generator:
                if header in processed_headers:
                    continue

                if 'mol:protein' not in header or len(sequence) < 10:
                    pbar.update(1)
                    continue

                prophet = ProteinProphet(n=4)
                prophet.train(sequence)
                predictability_score = prophet.calculate_predictability(sequence)

                writer.writerow([header, len(sequence), predictability_score])

                pbar.update(1)

    log.success(f"Streaming analysis complete. Results are in {output_csv}")

    # Final step: Sort the CSV and show the most/least predictable proteins
    log.info("Sorting final results...")
    final_df = pd.read_csv(output_csv)
    final_df = final_df.sort_values('predictability_score_Ta', ascending=True)
    final_df.to_csv(output_csv, index=False)

    print("\n--- Top 5 Most UNUSUAL (Least Predictable) Proteins ---")
    print(final_df.head(5))
    print("\n--- Top 5 Most REGULAR (Most Predictable) Proteins ---")
    print(final_df.tail(5))


if __name__ == '__main__':
    FASTA_FILE_PATH = 'pdb_seqres.txt'
    OUTPUT_CSV = 'protein_predictability_analysis_final.csv'

    if not os.path.exists(FASTA_FILE_PATH):
        print(f"Error: Input file '{FASTA_FILE_PATH}' not found. Please place it in the same directory as the script.")
    else:
        analyze_fasta_predictability_streaming(FASTA_FILE_PATH, OUTPUT_CSV)