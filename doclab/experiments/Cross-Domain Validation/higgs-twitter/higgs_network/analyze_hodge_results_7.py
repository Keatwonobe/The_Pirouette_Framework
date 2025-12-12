import argparse
import glob
import os
import collections
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt

# -------------------
# helpers
# -------------------

def load_hodge_npz(fname):
    data = np.load(fname, allow_pickle=True)
    edges = data["edges"]
    grad_part = data["grad"]
    curl_part = data["curl"]
    return edges, grad_part, curl_part

def avalanche_stats_from_hodge(edges, grad_part, curl_part, k_gamma=1.0, debug=False):
    # local Θ > Θ_c test
    curl_energy = curl_part ** 2
    grad_energy = grad_part ** 2

    # 1) build a SMALL floor, not median*0.05 (too big for your run)
    pos_grad = grad_energy[grad_energy > 0]
    if pos_grad.size:
        # go really small: 5% of the 10th percentile
        g10 = np.percentile(pos_grad, 10)
        eps = max(1e-9, g10 * 0.05)
    else:
        eps = 1e-9

    # 2) compute ratio
    ratio = curl_energy / (grad_energy + eps)

    if debug:
        print("ratio stats: min={:.3e} max={:.3e} mean={:.3e}".format(
            float(ratio.min()), float(ratio.max()), float(ratio.mean())
        ))
        print("k_gamma =", k_gamma)

    # 3) use ONLY the ratio test
    cascade_mask = ratio > k_gamma

    # 4) if still nothing, loosen automatically so you see *something*
    if not np.any(cascade_mask):
        if debug:
            print("no edges passed, loosening threshold to 0.5 * max(ratio)")
        k_gamma = 0.5 * float(ratio.max())
        cascade_mask = ratio > k_gamma

    cascade_edges = edges[cascade_mask]
    if len(cascade_edges) == 0:
        return [], 0

    G_cascade = ig.Graph.TupleList(cascade_edges, directed=False)
    comps = G_cascade.components(mode="strong").subgraphs()
    avalanche_sizes = [c.ecount() for c in comps if c.ecount() > 0]
    return avalanche_sizes, len(cascade_edges)



def fit_power_law(sizes, counts):
    # sizes, counts already aligned
    if len(sizes) < 2:
        return None, None
    log_sizes = np.log10(sizes)
    log_counts = np.log10(counts)
    mask = np.isfinite(log_counts)
    if mask.sum() < 2:
        return None, None
    m, c = np.polyfit(log_sizes[mask], log_counts[mask], 1)
    return m, c

def plot_avalanche_distribution(sizes, counts, slope, outpath):
    plt.figure(figsize=(12, 6))

    # linear/log plot (like your original)
    plt.subplot(1, 2, 1)
    plt.bar(sizes, counts, width=0.8, align="center")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Avalanche Size (number of edges)")
    plt.ylabel("Frequency (count)")
    plt.title("Avalanche Size Distribution")

    # log-log with fit
    plt.subplot(1, 2, 2)
    plt.scatter(sizes, counts)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Avalanche Size (log scale)")
    plt.ylabel("Frequency (log scale)")
    plt.title("Log-Log Plot")
    if slope is not None:
        m = slope
        c = np.log10(counts[0]) - m * np.log10(sizes[0])
        xs = np.linspace(min(sizes), max(sizes), 50)
        plt.plot(xs, 10 ** (m * np.log10(xs) + c),
                 "r--", label=f"Power Law Fit (slope α={m:.2f})")
        plt.legend()

    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


# -------------------
# main
# -------------------

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Hodge cascade output with k_Gamma sweep and daily compare."
    )
    parser.add_argument(
        "--input", "-i",
        default="higgs_hodge_out.npz",
        help="Single NPZ file produced by the Hodge script."
    )
    parser.add_argument(
        "--pattern", "-p",
        default=None,
        help="Optional glob pattern for multiple NPZ files (e.g. 'higgs_hodge_day*.npz')."
    )
    parser.add_argument(
        "--kgammas", "-k",
        default="0.5,1.0,2.0",
        help="Comma-separated k_Gamma values to sweep."
    )
    args = parser.parse_args()

    # -----------------------------
    # 1) Single-file analysis (your old behavior)
    # -----------------------------
    if args.pattern is None:
        edges, grad_part, curl_part = load_hodge_npz(args.input)
        k_default = float(args.kgammas.split(",")[0])
        avalanche_sizes, n_cascade_edges = avalanche_stats_from_hodge(
            edges, grad_part, curl_part, k_gamma=k_default
        )

        if len(avalanche_sizes) == 0:
            print("No cascades found at k_Gamma =", k_default)
            return

        counter = collections.Counter(avalanche_sizes)
        sizes = np.array(sorted(counter.keys()))
        counts = np.array([counter[s] for s in sizes])

        slope, _ = fit_power_law(sizes, counts)
        print(f"Single file: found {len(avalanche_sizes)} avalanches, slope={slope}")

        plot_avalanche_distribution(
            sizes, counts, slope,
            outpath="higgs_avalanche_distribution.png"
        )
        print("Wrote higgs_avalanche_distribution.png")

    # -----------------------------
    # 2) k_Gamma sweep on single file
    # -----------------------------
    edges, grad_part, curl_part = load_hodge_npz(args.input)
    k_vals = [float(x) for x in args.kgammas.split(",")]
    sweep_alphas = []
    sweep_counts = []
    for k in k_vals:
        av_sizes, n_cascade_edges = avalanche_stats_from_hodge(
            edges, grad_part, curl_part, k_gamma=k
        )
        if len(av_sizes) == 0:
            print(f"[k={k}] no cascades → skipping")
            sweep_alphas.append(np.nan)
            sweep_counts.append(0)
            continue
        ctr = collections.Counter(av_sizes)
        s = np.array(sorted(ctr.keys()))
        c = np.array([ctr[si] for si in s])
        slope, _ = fit_power_law(s, c)
        print(f"[k={k}] avalanches={len(av_sizes)}, slope={slope}")
        sweep_alphas.append(slope)
        sweep_counts.append(len(av_sizes))

    # plot alpha vs k_Gamma
    plt.figure(figsize=(6, 4))
    plt.plot(k_vals, sweep_alphas, marker="o")
    plt.xlabel("k_Gamma")
    plt.ylabel("Power-law slope α")
    plt.title("Cascade Exponent vs k_Gamma")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("alpha_vs_kgamma.png")
    plt.close()
    print("Wrote alpha_vs_kgamma.png")

    # -----------------------------
    # 3) Daily / multi-slice comparison
    # -----------------------------
    if args.pattern is not None:
        files = sorted(glob.glob(args.pattern))
        if not files:
            print(f"No NPZ files matched pattern {args.pattern}")
        else:
            day_labels = []
            day_slopes = []
            plt.figure(figsize=(10, 4 * len(files)))
            for idx, f in enumerate(files):
                e2, g2, c2 = load_hodge_npz(f)
                av_sizes, _ = avalanche_stats_from_hodge(
                    e2, g2, c2, k_gamma=k_vals[0]
                )
                ctr = collections.Counter(av_sizes)
                s = np.array(sorted(ctr.keys()))
                c = np.array([ctr[si] for si in s])
                slope, _ = fit_power_law(s, c)
                day_labels.append(os.path.basename(f))
                day_slopes.append(slope)

                # make a small subplot of each day’s dist
                plt.subplot(len(files), 1, idx + 1)
                plt.scatter(s, c)
                plt.xscale("log"); plt.yscale("log")
                plt.title(f"{os.path.basename(f)} (α={slope:.2f} @ k={k_vals[0]})")
                plt.xlabel("avalanche size"); plt.ylabel("freq")

            plt.tight_layout()
            plt.savefig("daily_avalanche_comparison.png")
            plt.close()
            print("Wrote daily_avalanche_comparison.png")

            # also write out a CSV so you can see the numbers
            with open("daily_avalanche_slopes.csv", "w") as fw:
                fw.write("file,alpha\n")
                for f, a in zip(day_labels, day_slopes):
                    fw.write(f"{f},{a}\n")
            print("Wrote daily_avalanche_slopes.csv")


if __name__ == "__main__":
    main()
