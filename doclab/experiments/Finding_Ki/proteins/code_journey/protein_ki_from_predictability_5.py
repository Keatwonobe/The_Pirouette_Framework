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

from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

KI_REST   = 4.14159
KI_MOTION = 4.18879
ALLOWED_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWYBZXUO")

class ProteinProphet:
    """n‑gram predictor with Laplace smoothing."""
    def __init__(self, n=4):
        self.n = n
        self.counts = defaultdict(Counter)
        self.context_totals = Counter()
        self.vocabulary = set()

    def train(self, training_sequence: str):
        char_list = list(training_sequence)
        if len(char_list) < self.n:
            return
        self.vocabulary = set(char_list)
        for i in range(len(char_list) - self.n + 1):
            ctx = tuple(char_list[i : i + self.n - 1])
            w   = char_list[i + self.n - 1]
            self.counts[ctx][w] += 1
            self.context_totals[ctx] += 1

    def calculate_predictability(self, target_sequence: str) -> float:
        """Mean Laplace‑smoothed P(word|context)."""
        char_list = list(target_sequence)
        if len(char_list) < self.n or not self.vocabulary:
            return 0.0
        V = len(self.vocabulary)
        ps = []
        for i in range(len(char_list) - self.n + 1):
            ctx = tuple(char_list[i : i + self.n - 1])
            w   = char_list[i + self.n - 1]
            # get counts (may be missing)
            count_ctx = self.context_totals.get(ctx, 0)
            context_counts = self.counts.get(ctx)
            if context_counts:
                count_w = context_counts.get(w, 0)
            else:
                count_w = 0
            # guard types
            if not isinstance(count_ctx, (int, float)) or not isinstance(count_w, (int, float)):
                log.error(f"TypeError in predictability: ctx={ctx}, count_ctx={count_ctx}({type(count_ctx)}), "
                        f"count_w={count_w}({type(count_w)}), V={V}")
                return 0.0
            # Laplace smoothing
            try:
                p = (count_w + 1) / (count_ctx + V)
            except Exception:
                log.error(f"Division error in predictability: {count_w=} {count_ctx=} {V=}")
                return 0.0
            ps.append(p)
        return float(np.mean(ps)) if ps else 0.0

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
                parts.append(line)
        if header:
            yield header, "".join(parts)

def analyze_protein_for_ki_rhythm(header, protein_sequence, gulp, ngram, do_plot):
    """Returns dict if we find Ki, else None."""
    try:
        # 1) sanitize
        sanitized_sequence = "".join([c for c in protein_sequence.upper() if c in ALLOWED_AMINO_ACIDS])
        
        # --- FIX 1: Increase minimum length for robust analysis ---
        if len(sanitized_sequence) < gulp * 4: # Changed from gulp * 2
            return None

        # --- FIX 2: Split sequence into training and target sets ---
        split_point = len(sanitized_sequence) // 2
        training_sequence = sanitized_sequence[:split_point]
        target_sequence   = sanitized_sequence[split_point:]

        # 2) build Ta
        prophet = ProteinProphet(n=ngram)
        
        # --- FIX 3: Train on the first half of the sequence ---
        prophet.train(training_sequence)
        
        ta = []
        # --- FIX 4: Generate the signal from the second half ---
        for i in range(len(target_sequence) - gulp + 1):
            window = target_sequence[i : i + gulp]
            t = prophet.calculate_predictability(window)
            ta.append(t)
            
        ta = np.array(ta, dtype=float)
        # Check if ta has enough data points and variance
        if ta.size < 10 or np.var(ta) < 1e-9:
            return None

        # 3) FFT + peak‑finding (This section remains unchanged)
        try:
            amps  = rfft(ta)
            freqs = rfftfreq(ta.size, d=1.0)
            power = np.abs(amps)**2
        except Exception as e:
            log.error(f"FFT error on {header[:10]}…: {e}")
            return None

        try:
            peaks, props = find_peaks(power, height=np.mean(power)*5)
        except Exception as e:
            log.error(f"Peak‑find error on {header[:10]}…: {e}")
            return None

        if peaks.size < 2:
            return None

        dfreqs = freqs[peaks]
        dpows  = power[peaks]
        idx    = int(np.argmax(dpows))
        f0     = float(dfreqs[idx])
        if f0 == 0.0:
            return None

        # 4) look for Ki (This section remains unchanged)
        matches = {}
        for f in dfreqs:
            r = f / f0
            if abs(r - KI_REST)   < 0.1: matches['Ki_Rest']   = r
            if abs(r - KI_MOTION) < 0.1: matches['Ki_Motion'] = r
        if not matches:
            return None

        # 5) optional plotting (This section remains unchanged)
        if do_plot:
            safe = re.sub(r'[^\w\-]', '_', header.split()[0])[:50]
            out = "ki_rhythm_plots"
            os.makedirs(out, exist_ok=True)

            fig, (ax1, ax2) = plt.subplots(2,1,figsize=(12,8))
            fig.suptitle(header, fontsize=14)
            ax1.plot(ta);          ax1.set_ylabel('Ta score')
            ax2.semilogy(freqs,power,alpha=0.6); ax2.plot(dfreqs,dpows,"x")
            for k,v in matches.items():
                kc = KI_REST if 'Rest' in k else KI_MOTION
                ax2.axvline(f0*kc,linestyle='--',label=f"{k}:{v:.3f}")
            ax2.set_xlabel('Freq'); ax2.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(out, f"{safe}.png"))
            plt.close()

        return {
            'header': header,
            'length': len(sanitized_sequence),
            'mean_ta': float(np.mean(ta)),
            'f0': f0,
            'matches': matches
        }

    except Exception as e:
        # catch EVERYTHING so the loop never dies
        log.error(f"Full analysis error on {header[:15]}…: {e}")
        log.debug(traceback.format_exc())
        return None

def process_fasta_for_ki_rhythms(fasta, out_csv, chk, err, gulp, ngram, do_plot):
    log.info(f"Counting records in {fasta}…")
    total = sum(1 for L in open(fasta, 'r', errors='ignore') if L.startswith('>'))
    log.info(f"{total:,} total proteins")

    done = set()
    if os.path.exists(chk):
        done = set(open(chk).read().splitlines())
        log.info(f"Resuming: {len(done):,} already done")
    if os.path.exists(err):
        pass # Keep existing error log for inspection

    # Prepare for incremental CSV writing
    fieldnames = ['header', 'length', 'mean_ta', 'f0', 'matches'] # Define your CSV columns
    file_exists = os.path.exists(out_csv)

    # Open CSV file in append mode. 'newline=' is crucial for csv module.
    # We will write the header only if the file is new.
    with open(out_csv, 'a' if file_exists else 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists: # Write header only if the file is new
            writer.writeheader()
        
        # We no longer need the 'results' list that accumulated everything
        # results = [] # Remove this line

        with tqdm(total=total, desc="Analyzing") as bar:
            for hdr, seq in parse_fasta_generator(fasta):
                bar.update(1)
                if hdr in done or 'mol:protein' not in hdr:
                    continue

                res = analyze_protein_for_ki_rhythm(hdr, seq, gulp, ngram, do_plot)
                if res:
                    # Write result directly to CSV
                    writer.writerow(res)
                else:
                    # If analyze_protein_for_ki_rhythm returns None (indicating an error or skip)
                    with open(err, 'a') as f_err:
                        f_err.write(hdr + "\n")

                # always checkpoint
                with open(chk, 'a') as f:
                    f.write(hdr + "\n")

    log.success(f"Analysis complete. Results written to {out_csv}")
    if os.path.exists(chk):
        os.remove(chk) # Cleanup checkpoint file

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("fasta")
    p.add_argument("csv")
    p.add_argument("--checkpoint", default="ki.chk")
    p.add_argument("--errors",     default="ki.err.log")
    p.add_argument("--gulp",       type=int, default=50)
    p.add_argument("--ngram",      type=int, default=3)
    p.add_argument("--no-plot",    action="store_true")
    args = p.parse_args()

    process_fasta_for_ki_rhythms(
        fasta     = args.fasta,
        out_csv   = args.csv,
        chk       = args.checkpoint,
        err       = args.errors,
        gulp      = args.gulp,
        ngram     = args.ngram,
        do_plot   = not args.no_plot
    )
