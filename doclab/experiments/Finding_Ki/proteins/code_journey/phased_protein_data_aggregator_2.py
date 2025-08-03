#!/usr/bin/env python3
import os
import argparse
import csv
import numpy as np
from collections import defaultdict, Counter
from tqdm import tqdm
from loguru import logger as log
import re
import traceback
import pickle
import gc

from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

KI_REST   = 4.14159
KI_MOTION = 4.18879
ALLOWED_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWYBZXUO")

# The class definition MUST be present for pickle to load the model object correctly.
class ProteinProphet:
    """n-gram predictor with Laplace smoothing."""
    def __init__(self, n=3):
        self.n = n
        self.counts = defaultdict(Counter)
        self.context_totals = Counter()
        self.vocabulary = set()
        self.V = 0

    def get_token_probability(self, context: tuple, word: str) -> float:
        """Calculates the Laplace-smoothed probability of a word given a context."""
        if not self.V:
            return 0.0
        count_w = self.counts.get(context, {}).get(word, 0)
        count_ctx = self.context_totals.get(context, 0)
        return (count_w + 1) / (count_ctx + self.V)


def parse_fasta_generator(fp):
    """Stream FASTA as (header, seq)."""
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        header, parts = None, []
        for line in f:
            line = line.rstrip()
            if line.startswith('>'):
                if header:
                    yield header, "".join(parts)
                header, parts = line[1:], []
            else:
                parts.append(line.upper())
        if header:
            yield header, "".join(parts)


def analyze_protein_for_ki_rhythm(prophet, header, protein_sequence, gulp, do_plot):
    """Returns dict if we find Ki, else None. Uses a pre-trained prophet model."""
    try:
        sanitized_sequence = "".join([c for c in protein_sequence if c in ALLOWED_AMINO_ACIDS])
        ngram = prophet.n
        # Must be long enough for sliding window
        if len(sanitized_sequence) < gulp + ngram:
            return None

        # Compute token probabilities
        probabilities = []
        for i in range(len(sanitized_sequence) - ngram + 1):
            ctx = tuple(sanitized_sequence[i : i + ngram - 1])
            w = sanitized_sequence[i + ngram - 1]
            prob = prophet.get_token_probability(ctx, w)
            probabilities.append(prob)
        probabilities = np.array(probabilities, dtype=float)

        # Sliding-window mean (ta)
        if probabilities.size < gulp:
            return None
        ta = np.convolve(probabilities, np.ones(gulp)/gulp, mode='valid')
        if ta.size < 10 or np.var(ta) < 1e-9:
            return None

        # FFT + peak finding
        amps  = rfft(ta)
        freqs = rfftfreq(ta.size, d=1.0)
        power = np.abs(amps)**2
        peaks, _ = find_peaks(power, height=np.mean(power)*5)
        if peaks.size < 2:
            return None

        dfreqs = freqs[peaks]
        dpows  = power[peaks]
        idx    = int(np.argmax(dpows))
        f0     = float(dfreqs[idx])
        if f0 == 0.0:
            return None

        # Detect Ki matches
        matches = {}
        for f in dfreqs:
            r = f / f0
            if abs(r - KI_REST)   < 0.1: matches['Ki_Rest']   = r
            if abs(r - KI_MOTION) < 0.1: matches['Ki_Motion'] = r
        if not matches:
            return None

        # Optional plotting (intentionally omitted for memory)
        if do_plot:
            pass

        return {
            'header': header,
            'length': len(sanitized_sequence),
            'mean_ta': float(np.mean(ta)),
            'f0': f0,
            'matches': matches
        }

    except Exception as e:
        log.error(f"Error analyzing {header[:15]}: {e}")
        log.debug(traceback.format_exc())
        return None


def process_fasta_for_ki_rhythms(prophet, fasta, out_csv, chk, err, gulp, do_plot):
    log.info(f"Starting analysis of {fasta}...")

    # Determine resume index
    resume_idx = 0
    if os.path.exists(chk):
        try:
            with open(chk, 'r') as f_chk:
                resume_idx = int(f_chk.read().strip() or 0)
            log.info(f"Resuming at record {resume_idx:,}")
        except Exception:
            log.warning("Couldn't parse checkpoint; starting at 0")
            resume_idx = 0

    # Prepare CSV: write fresh header on new run, else append
    mode = 'w' if resume_idx == 0 else 'a'
    with open(out_csv, mode, newline='') as csvfile, open(err, 'a') as f_err:
        writer = csv.DictWriter(csvfile, fieldnames=['header','length','mean_ta','f0','matches'])
        if mode == 'w':
            log.info("Writing CSV header")
            writer.writeheader()
        else:
            log.info("Appending to existing CSV, skipping header")

        # Stream and process
        with tqdm(desc="Analyzing") as bar:
            for idx, (hdr, seq) in enumerate(parse_fasta_generator(fasta), start=1):
                bar.update(1)
                if idx <= resume_idx:
                    continue

                res = analyze_protein_for_ki_rhythm(prophet, hdr, seq, gulp, do_plot)
                if res:
                    writer.writerow(res)
                else:
                    f_err.write(hdr + "\n")

                # Update checkpoint
                with open(chk, 'w') as f_chk:
                    f_chk.write(str(idx))

                if idx % 1000 == 0:
                    gc.collect()

    log.success(f"Done! Results are in {out_csv}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Find Ki rhythms in proteins.")
    p.add_argument("fasta", help="Input FASTA file.")
    p.add_argument("model", help="Pickled ProteinProphet model.")
    p.add_argument("csv",   help="Output CSV path.")
    p.add_argument("--checkpoint", default="ki.chk")
    p.add_argument("--errors",     default="ki.err.log")
    p.add_argument("--gulp",       type=int, default=50)
    p.add_argument("--no-plot",    action="store_true")
    args = p.parse_args()

    log.info(f"Loading model from {args.model}...")
    try:
        with open(args.model, 'rb') as f:
            prophet_model = pickle.load(f)
        log.success("Model loaded.")
    except Exception as e:
        log.error(f"Can't load model: {e}")
        exit(1)

    process_fasta_for_ki_rhythms(
        prophet = prophet_model,
        fasta   = args.fasta,
        out_csv = args.csv,
        chk     = args.checkpoint,
        err     = args.errors,
        gulp    = args.gulp,
        do_plot = not args.no_plot
    )
