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
    """n-gram predictor with Laplace smoothing."""
    def __init__(self, n=4):
        self.n = n
        self.counts = defaultdict(Counter)
        self.context_totals = Counter()
        self.vocabulary = set()
        self.V = 0

    def train(self, training_sequence: str):
        """Trains the n-gram model on a given sequence."""
        char_list = list(training_sequence)
        if len(char_list) < self.n:
            return
        
        self.vocabulary = set(char_list)
        self.V = len(self.vocabulary)
        
        for i in range(len(char_list) - self.n + 1):
            ctx = tuple(char_list[i : i + self.n - 1])
            w   = char_list[i + self.n - 1]
            self.counts[ctx][w] += 1
            self.context_totals[ctx] += 1

    def get_token_probability(self, context: tuple, word: str) -> float:
        """Calculates the Laplace-smoothed probability of a word given a context."""
        if not self.vocabulary:
            return 0.0
        
        count_w = self.counts.get(context, {}).get(word, 0)
        count_ctx = self.context_totals.get(context, 0)
        
        # Laplace smoothing
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
                parts.append(line)
        if header:
            yield header, "".join(parts)

def analyze_protein_for_ki_rhythm(header, protein_sequence, gulp, ngram, do_plot):
    """Returns dict if we find Ki, else None."""
    try:
        # 1) Sanitize and check length
        sanitized_sequence = "".join([c for c in protein_sequence.upper() if c in ALLOWED_AMINO_ACIDS])
        
        # FIX 1: Loosen minimum length requirement for analysis.
        # We need the target sequence (half the total) to be long enough to generate a signal of at least 10 data points.
        # Required length for target_sequence = gulp + 10. Total length = 2 * (gulp + 10).
        if len(sanitized_sequence) < (gulp + 10) * 2:
            return None

        # 2) Split sequence into training and target sets
        split_point = len(sanitized_sequence) // 2
        training_sequence = sanitized_sequence[:split_point]
        target_sequence   = sanitized_sequence[split_point:]

        # 3) Train the prophet model on the first half of the sequence
        prophet = ProteinProphet(n=ngram)
        prophet.train(training_sequence)
        
        # If training produced no vocabulary (e.g., training sequence was too short), abort.
        if not prophet.vocabulary:
            return None

        # 4) FIX 2: Correctly generate the 'ta' signal from the second half
        # The original code had a confusing and error-prone nested loop structure.
        # This new logic is clearer: the signal at each point is the average
        # predictability of the amino acids within the sliding window.
        ta = []
        # First, pre-calculate probabilities for each n-gram in the target sequence
        probabilities = []
        for i in range(len(target_sequence) - ngram + 1):
            ctx = tuple(target_sequence[i : i + ngram - 1])
            w = target_sequence[i + ngram - 1]
            prob = prophet.get_token_probability(ctx, w)
            probabilities.append(prob)
        
        # Now, create the smoothed 'ta' signal using a sliding window ('gulp') over the probabilities
        if len(probabilities) < gulp:
             return None
        for i in range(len(probabilities) - gulp + 1):
            window_mean_prob = np.mean(probabilities[i : i + gulp])
            ta.append(window_mean_prob)

        ta = np.array(ta, dtype=float)
        if ta.size < 10 or np.var(ta) < 1e-9:
            return None

        # 5) FFT + peak-finding (This section remains unchanged)
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
            log.error(f"Peak-find error on {header[:10]}…: {e}")
            return None

        if peaks.size < 2:
            return None

        dfreqs = freqs[peaks]
        dpows  = power[peaks]
        idx    = int(np.argmax(dpows))
        f0     = float(dfreqs[idx])
        if f0 == 0.0:
            return None

        # 6) Look for Ki (This section remains unchanged)
        matches = {}
        for f in dfreqs:
            r = f / f0
            if abs(r - KI_REST)   < 0.1: matches['Ki_Rest']   = r
            if abs(r - KI_MOTION) < 0.1: matches['Ki_Motion'] = r
        if not matches:
            return None

        # 7) Optional plotting (This section remains unchanged)
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
        log.error(f"Full analysis error on {header[:15]}…: {e}")
        log.debug(traceback.format_exc())
        return None

def process_fasta_for_ki_rhythms(fasta, out_csv, chk, err, gulp, ngram, do_plot):
    log.info(f"Counting records in {fasta}…")
    total = sum(1 for L in open(fasta, 'r', errors='ignore') if L.startswith('>'))
    log.info(f"{total:,} total proteins")

    done = set()
    if os.path.exists(chk):
        with open(chk, 'r') as f_chk:
            done = set(f_chk.read().splitlines())
        log.info(f"Resuming: {len(done):,} already done")
    
    # This section for writing to CSV remains unchanged but is included for completeness
    fieldnames = ['header', 'length', 'mean_ta', 'f0', 'matches']
    file_exists = os.path.exists(out_csv) and os.path.getsize(out_csv) > 0

    with open(out_csv, 'a', newline='') as csvfile, open(chk, 'a') as f_chk, open(err, 'a') as f_err:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        
        with tqdm(total=total, desc="Analyzing") as bar:
            for hdr, seq in parse_fasta_generator(fasta):
                bar.update(1)
                if hdr in done or 'mol:protein' not in hdr:
                    continue

                res = analyze_protein_for_ki_rhythm(hdr, seq, gulp, ngram, do_plot)
                if res:
                    writer.writerow(res)
                else:
                    f_err.write(hdr + "\n")

                f_chk.write(hdr + "\n")

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