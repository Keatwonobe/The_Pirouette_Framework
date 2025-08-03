#!/usr/bin/env python3
import os
import argparse
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
ALLOWED_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWYBZXUO")

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
        if len(words) < self.n:
            return
        for i in range(len(words) - self.n + 1):
            context = tuple(words[i : i + self.n - 1])
            next_word = words[i + self.n - 1]
            self.counts[context][next_word] += 1
            self.context_totals[context] += 1

    def calculate_predictability(self, sequence: str) -> float:
        words = list(sequence)
        if len(words) < self.n or not self.vocabulary:
            return 0.0
        
        probs = []
        V = len(self.vocabulary)
        for i in range(len(words) - self.n + 1):
            ctx = tuple(words[i : i + self.n - 1])
            w = words[i + self.n - 1]
            count_ctx = int(self.context_totals.get(ctx, 0))
            count_w = int(self.counts.get(ctx, {}).get(w, 0))
            # Laplace smoothing
            p = (count_w + 1) / (count_ctx + V)
            probs.append(p)
        return float(np.mean(probs)) if probs else 0.0

def parse_fasta_generator(fp):
    """Yields (header, seq) tuples, streaming FASTA records."""
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        header = None
        seq_parts = []
        for line in f:
            line = line.rstrip()
            if line.startswith('>'):
                if header:
                    yield header, "".join(seq_parts)
                header = line[1:]
                seq_parts = []
            else:
                seq_parts.append(line)
        if header:
            yield header, "".join(seq_parts)

def analyze_protein_for_ki_rhythm(header, sequence, gulp_size, n_gram, do_plot):
    # 1. Sanitization
    seq = "".join([c for c in sequence.upper() if c in ALLOWED_AMINO_ACIDS])
    if len(seq) < gulp_size * 2:
        return None

    # 2. Build Ta signal
    prophet = ProteinProphet(n=n_gram)
    prophet.train(seq)
    ta = []
    for i in range(len(seq) - gulp_size + 1):
        window = seq[i : i + gulp_size]
        ta.append(prophet.calculate_predictability(window))
    ta = np.array(ta, dtype=float)
    if ta.size < 10 or np.var(ta) < 1e-9:
        return None

    # 3. FFT and peak finding
    amps = rfft(ta)
    freqs = rfftfreq(ta.size, d=1.0)
    power = np.abs(amps)**2
    peaks, _ = find_peaks(power, height=np.mean(power) * 5)
    if peaks.size < 2:
        return None

    dfreqs = freqs[peaks]
    dpows = power[peaks]
    idx = np.argmax(dpows)
    f0 = float(dfreqs[idx])
    if f0 == 0.0:
        return None

    # 4. Look for Ki ratios
    matches = {}
    for f in dfreqs:
        r = f / f0
        if abs(r - KI_REST) < 0.1:
            matches['Ki_Rest_Ratio'] = r
        if abs(r - KI_MOTION) < 0.1:
            matches['Ki_Motion_Ratio'] = r
    if not matches:
        return None

    # 5. Optional plotting
    if do_plot:
        safe = re.sub(r'[^\w\-]', '_', header.split()[0])[:50]
        outdir = "ki_rhythm_plots"
        os.makedirs(outdir, exist_ok=True)

        fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))
        fig.suptitle(f"{header}", fontsize=14)

        ax1.plot(ta, label='Predictability')
        ax1.set_ylabel('Ta score')
        ax1.legend()

        ax2.semilogy(freqs, power, alpha=0.6, label='Power')
        ax2.plot(dfreqs, dpows, "x", label='Peaks')
        for lab, r in matches.items():
            kc = KI_REST if 'Rest' in lab else KI_MOTION
            ax2.axvline(f0*kc, linestyle='--', label=f"{lab}")
        ax2.set_xlabel('Frequency')
        ax2.legend()

        plt.tight_layout()
        plt.savefig(os.path.join(outdir, f"{safe}.png"))
        plt.close()

    return {
        'header': header,
        'sequence_length': len(seq),
        'mean_ta_score': float(np.mean(ta)),
        'ta_fundamental_freq': f0,
        'ki_harmonic_matches': matches
    }

def process_fasta_for_ki_rhythms(fasta_path, output_csv, checkpoint_file,
                                error_log_file, gulp_size, n_gram, do_plot):
    log.info(f"Counting total records in {fasta_path}…")
    total = 0
    with open(fasta_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith('>'):
                total += 1

    processed = set()
    if os.path.exists(checkpoint_file):
        processed = set(open(checkpoint_file).read().splitlines())
        log.info(f"Resuming: {len(processed)} headers already done")
    elif os.path.exists(error_log_file):
        os.remove(error_log_file)

    results = []
    with tqdm(total=total, desc="Analyzing Protein Rhythms") as pbar:
        for header, seq in parse_fasta_generator(fasta_path):
            pbar.update(1)
            if header in processed or 'mol:protein' not in header:
                continue

            try:
                res = analyze_protein_for_ki_rhythm(header, seq,
                                                    gulp_size, n_gram, do_plot)
                if res:
                    results.append(res)
            except Exception as e:
                log.error(f"[{header[:30]}...] processing failed: {e}")
                with open(error_log_file, 'a') as ferr:
                    ferr.write(f"{header}\t{repr(e)}\n")
            finally:
                # always checkpoint even if analysis or I/O failed
                with open(checkpoint_file, 'a') as fchk:
                    fchk.write(header + "\n")

    # write out CSV
    if results:
        pd.DataFrame(results).to_csv(output_csv, index=False)
        log.success(f"Done—found {len(results)} hits. Results in {output_csv}")
    else:
        log.warning("Done—no Ki‑rhythms detected.")

    # clean up checkpoint
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("fasta", help="Input FASTA file")
    p.add_argument("csv", help="Output results CSV")
    p.add_argument("--checkpoint", default="ki_rhythm.chk")
    p.add_argument("--errors",     default="ki_errors.log")
    p.add_argument("--gulp",       type=int, default=50)
    p.add_argument("--ngram",      type=int, default=3)
    p.add_argument("--no-plot",    action="store_true",
                   help="Disable all matplotlib plotting")
    args = p.parse_args()

    process_fasta_for_ki_rhythms(
        fasta_path       = args.fasta,
        output_csv       = args.csv,
        checkpoint_file  = args.checkpoint,
        error_log_file   = args.errors,
        gulp_size        = args.gulp,
        n_gram           = args.ngram,
        do_plot          = not args.no_plot
    )
