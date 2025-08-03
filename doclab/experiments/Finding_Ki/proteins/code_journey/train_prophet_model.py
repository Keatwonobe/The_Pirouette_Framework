#!/usr/bin/env python3
import argparse
import pickle
import os
import json
from collections import defaultdict, Counter
from loguru import logger as log
from tqdm import tqdm

ALLOWED_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWYBZXUO")

class ProteinProphet:
    """A container for n-gram counts. Can be merged."""
    def __init__(self, n=3):
        self.n = n
        self.counts = defaultdict(Counter)
        self.context_totals = Counter()
        self.vocabulary = set()

    def train(self, training_sequence: str):
        """Trains on a single sequence."""
        char_list = list(training_sequence)
        if len(char_list) < self.n:
            return
        self.vocabulary.update(char_list)
        # slide window
        for i in range(len(char_list) - self.n + 1):
            ctx = tuple(char_list[i : i + self.n - 1])
            w = char_list[i + self.n - 1]
            self.counts[ctx][w] += 1
            self.context_totals[ctx] += 1

    def merge(self, other: 'ProteinProphet'):
        """Merge another model into this one."""
        assert self.n == other.n, "N-gram sizes must match"
        for ctx, counter in other.counts.items():
            self.counts[ctx].update(counter)
            self.context_totals[ctx] += other.context_totals[ctx]
        self.vocabulary.update(other.vocabulary)


def parse_fasta_generator(fp_path):
    """Streams FASTA records from a file path."""
    with open(fp_path, 'r', encoding='utf-8', errors='ignore') as f:
        header = None
        parts = []
        for line in f:
            line = line.rstrip()
            if not line:
                continue
            if line.startswith('>'):
                if header is not None:
                    yield header, ''.join(parts)
                header = line[1:]
                parts = []
            else:
                parts.append(line.upper())
        if header is not None:
            yield header, ''.join(parts)


def save_checkpoint(model, temp_dir, processed):
    """Save a checkpoint named by record count to avoid overwrites."""
    filename = f"checkpoint_{processed}.pkl"
    out_path = os.path.join(temp_dir, filename)
    with open(out_path, 'wb') as f:
        pickle.dump(model, f)
    meta = {'last_model': filename, 'processed': processed}
    with open(os.path.join(temp_dir, 'checkpoint_meta.json'), 'w') as f:
        json.dump(meta, f)
    log.info(f"Checkpoint saved at record {processed} -> {out_path}")


def load_checkpoint(temp_dir):
    meta_fp = os.path.join(temp_dir, 'checkpoint_meta.json')
    if os.path.exists(meta_fp):
        try:
            with open(meta_fp, 'r') as mf:
                meta = json.load(mf)
            model_fp = os.path.join(temp_dir, meta['last_model'])
            if os.path.exists(model_fp):
                with open(model_fp, 'rb') as mf:
                    model = pickle.load(mf)
                return model, meta.get('processed', 0)
        except Exception as e:
            log.error(f"Failed to load checkpoint metadata: {e}")
    return None, 0


def main():
    parser = argparse.ArgumentParser(description="Streaming checkpointed ProteinProphet trainer.")
    parser.add_argument("fasta_corpus", help="Input FASTA file path.")
    parser.add_argument("temp_dir", help="Directory to store checkpoint files.")
    parser.add_argument("--chunk_size", type=int, default=1000,
                        help="Number of proteins between checkpoints.")
    parser.add_argument("--ngram", type=int, default=3, help="N-gram size.")
    args = parser.parse_args()

    os.makedirs(args.temp_dir, exist_ok=True)
    log.info(f"Checkpoint every {args.chunk_size} proteins.")

    prophet, start_idx = load_checkpoint(args.temp_dir)
    if prophet:
        log.info(f"Resuming from checkpoint at record {start_idx}.")
    else:
        prophet = ProteinProphet(n=args.ngram)
        start_idx = 0
        log.info("Starting fresh training.")

    # Count total records for progress
    total = sum(1 for L in open(args.fasta_corpus, 'r', errors='ignore') if L.startswith('>'))
    log.info(f"Total proteins: {total:,}")

    record_idx = 0
    iterator = parse_fasta_generator(args.fasta_corpus)
    # Use initial to reflect warmup on resume
    for header, seq in tqdm(iterator, total=total, initial=start_idx, desc="Training"):  # progress bar
        record_idx += 1
        # Warmup skip
        if record_idx <= start_idx:
            continue
        try:
            sanitized = ''.join(c for c in seq if c in ALLOWED_AMINO_ACIDS)
            if sanitized:
                prophet.train(sanitized)
        except Exception as e:
            log.error(f"Skipping record {record_idx} ({header}) due to error: {e}")
            continue

        # Checkpoint at intervals
        if (record_idx - start_idx) % args.chunk_size == 0:
            save_checkpoint(prophet, args.temp_dir, record_idx)

    # Final checkpoint
    save_checkpoint(prophet, args.temp_dir, record_idx)
    log.success("Training complete.")

if __name__ == "__main__":
    main()
