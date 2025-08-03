import os
import re
import pandas as pd
from collections import defaultdict, Counter
import numpy as np
from tqdm import tqdm
from loguru import logger as log

class ProteinProphet:
    """A simple n-gram model to measure the predictability of a protein sequence."""
    def __init__(self, n=3):
        self.n = n
        self.counts = defaultdict(Counter)
        self.context_totals = Counter()
        self.vocabulary = set()

    def train(self, sequence: str):
        """Trains the model on a single protein sequence."""
        self.vocabulary = set(sequence)
        words = list(sequence) # Treat each amino acid as a "word"
        for i in range(len(words) - self.n):
            context = tuple(words[i:i + self.n - 1])
            next_word = words[i + self.n - 1]
            self.counts[context][next_word] += 1
            self.context_totals[context] += 1

    def calculate_predictability(self, sequence: str) -> float:
        """
        Calculates the average predictability (Ta proxy) for the entire sequence.
        """
        words = list(sequence)
        if len(words) < self.n:
            return 0.0

        probabilities = []
        for i in range(len(words) - self.n + 1):
            context = tuple(words[i:i + self.n - 1])
            word_to_predict = words[i + self.n - 1]
            
            context_count = self.context_totals.get(context, 0)
            word_count_in_context = self.counts.get(context, {}).get(word_to_predict, 0)
            
            # Laplace (add-1) smoothing for unseen contexts/words
            probability = (word_count_in_context + 1) / (context_count + len(self.vocabulary))
            probabilities.append(probability)
            
        return np.mean(probabilities) if probabilities else 0.0

def parse_fasta(file_path):
    """Generator function to parse large FASTA files record by record."""
    with open(file_path, 'r') as f:
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

def analyze_fasta_predictability(fasta_path, output_csv):
    """
    Analyzes all protein sequences in a FASTA file for their predictability.
    """
    log.info(f"Starting predictability analysis for {fasta_path}...")
    results = []

    # Use tqdm for a progress bar
    # We need to count the records first for tqdm to work properly
    record_count = sum(1 for line in open(fasta_path) if line.startswith('>'))
    
    with open(fasta_path, 'r') as f:
        fasta_generator = parse_fasta(fasta_path)
        for header, sequence in tqdm(fasta_generator, total=record_count, desc="Analyzing Sequences"):
            # Filter for proteins and ensure sequence is not too short
            if 'mol:protein' not in header or len(sequence) < 10:
                continue

            prophet = ProteinProphet(n=4) # Using a slightly larger context (tetrapeptide)
            prophet.train(sequence)
            predictability_score = prophet.calculate_predictability(sequence)

            results.append({
                'header': header,
                'sequence_length': len(sequence),
                'predictability_score_Ta': predictability_score
            })

    if results:
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('predictability_score_Ta', ascending=True)
        results_df.to_csv(output_csv, index=False)
        log.success(f"Analysis complete. Found {len(results_df)} proteins. Results saved to {output_csv}")
        print("\n--- Top 5 Most UNUSUAL (Least Predictable) Proteins ---")
        print(results_df.head(5))
        print("\n--- Top 5 Most REGULAR (Most Predictable) Proteins ---")
        print(results_df.tail(5))
    else:
        log.warning("No suitable protein sequences were found or analyzed.")


if __name__ == '__main__':
    # --- Configuration ---
    # Path to your large, single FASTA file
    FASTA_FILE_PATH = 'C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_5/doclab/experiments/Finding_Ki/proteins/pdb_seqres.txt'
    OUTPUT_CSV = 'protein_predictability_analysis.csv'
    
    if FASTA_FILE_PATH == 'path/to/your/fasta_file.fasta':
        print("Please update the 'FASTA_FILE_PATH' variable to the correct path to your FASTA data dump.")
    else:
        analyze_fasta_predictability(FASTA_FILE_PATH, OUTPUT_CSV)