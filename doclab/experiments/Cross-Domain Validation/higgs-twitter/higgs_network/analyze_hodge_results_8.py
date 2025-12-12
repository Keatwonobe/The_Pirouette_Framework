import argparse
import glob
import os
import collections
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt

def load_hodge_npz(fname):
    data = np.load(fname, allow_pickle=True)
    return data

def avalanche_from_edges(edges):
    G = ig.Graph.TupleList(edges, directed=False)
    comps = G.components(mode="strong").subgraphs()
    return [c.ecount() for c in comps if c.ecount() > 0]

def fit_power_law(sizes, counts):
    if len(sizes) < 2:
        return None, None
    log_s = np.log10(sizes)
    log_c = np.log10(counts)
    mask = np.isfinite(log_c)
    if mask.sum() < 2:
        return None, None
    m, c = np.polyfit(log_s[mask], log_c[mask], 1)
    return m, c

def plot_avalanche_distribution(sizes, counts, slope, outpath):
    plt.figure(figsize=(12, 6))

    # left
    plt.subplot(1, 2, 1)
    plt.bar(sizes, counts, width=0.8, align="center")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("Avalanche Size (number of edges)")
    plt.ylabel("Frequency (count)")
    plt.title("Avalanche Size Distribution")

    # right
    plt.subplot(1, 2, 2)
    plt.scatter(sizes, counts)
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("Avalanche Size (log scale)")
    plt.ylabel("Frequency (log scale)")
    plt.title("Log-Log Plot")

    if slope is not None:
        c = np.log10(counts[0]) - slope * np.log10(sizes[0])
        xs = np.linspace(min(sizes), max(sizes), 50)
        plt.plot(xs, 10 ** (slope * np.log10(xs) + c),
                 "r--", label=f"Power Law Fit (slope α={slope:.2f})")
        plt.legend()

    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def select_edges_legacy(data, k_gamma):
    """Script-5 style: curl^2 > k * grad^2"""
    edges = data["edges"]
    grad = data["grad"]
    curl = data["curl"]
    grad_e = grad ** 2
    curl_e = curl ** 2
    mask = curl_e > (k_gamma * grad_e)
    return edges[mask]

def select_edges_quantile(data, k_gamma):
    """
    New-style: if 'ratio' exists, interpret k_gamma in (0,1] as
    'keep top k_gamma fraction' of most turbulent edges.
    If k_gamma > 1, keep 1/k_gamma.
    """
    edges = data["edges"]
    ratio = data["ratio"]
    # map to fraction
    if 0 < k_gamma <= 1.0:
        frac = k_gamma
    else:
        frac = 1.0 / k_gamma
    frac = min(0.99, max(0.01, frac))
    thr = np.quantile(ratio, 1.0 - frac)
    mask = ratio >= thr
    return edges[mask]

def main():
    parser = argparse.ArgumentParser(
        description="Adaptive Hodge cascade analyzer (legacy + normalized)"
    )
    parser.add_argument("--input", "-i", default="higgs_hodge_out.npz")
    parser.add_argument("--kgammas", "-k", default="0.5,1.0,2.0",
                        help="For legacy: numeric kΓ. For normalized: fraction to keep.")
    parser.add_argument("--pattern", "-p", default=None,
                        help="Optional glob for multi-slice.")
    args = parser.parse_args()

    k_vals = [float(x) for x in args.kgammas.split(",")]

    if args.pattern is None:
        data = load_hodge_npz(args.input)
        has_ratio = "ratio" in data

        # 1) main run using first k
        k0 = k_vals[0]
        if has_ratio:
            sel_edges = select_edges_quantile(data, k0)
        else:
            sel_edges = select_edges_legacy(data, k0)

        if sel_edges.size == 0:
            print(f"No cascades found at k_Gamma = {k0}")
            return

        avalanches = avalanche_from_edges(sel_edges)
        counter = collections.Counter(avalanches)
        sizes = np.array(sorted(counter.keys()))
        counts = np.array([counter[s] for s in sizes])
        slope, _ = fit_power_law(sizes, counts)
        print(f"Single file: found {len(avalanches)} avalanches, slope={slope}")

        plot_avalanche_distribution(
            sizes, counts, slope,
            outpath="higgs_avalanche_distribution.png"
        )
        print("Wrote higgs_avalanche_distribution.png")

        # 2) sweep
        sweep_alphas = []
        for k in k_vals:
            if has_ratio:
                sel_edges = select_edges_quantile(data, k)
            else:
                sel_edges = select_edges_legacy(data, k)

            if sel_edges.size == 0:
                print(f"[k={k}] no cascades")
                sweep_alphas.append(np.nan)
                continue

            avalanches = avalanche_from_edges(sel_edges)
            ctr = collections.Counter(avalanches)
            s = np.array(sorted(ctr.keys()))
            c = np.array([ctr[si] for si in s])
            s_lp, _ = fit_power_law(s, c)
            print(f"[k={k}] avalanches={len(avalanches)}, slope={s_lp}")
            sweep_alphas.append(s_lp)

        # 3) plot sweep
        plt.figure(figsize=(6, 4))
        plt.plot(k_vals, sweep_alphas, marker="o")
        plt.xlabel("k_Γ (legacy) / fraction (normalized)")
        plt.ylabel("Power-law slope α")
        plt.title("Cascade Exponent vs threshold")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("alpha_vs_kgamma.png")
        plt.close()
        print("Wrote alpha_vs_kgamma.png")

    else:
        # multi-file mode: same logic, just loop
        files = sorted(glob.glob(args.pattern))
        data0 = load_hodge_npz(files[0])
        has_ratio = "ratio" in data0
        day_labels = []
        day_slopes = []
        plt.figure(figsize=(10, 4 * len(files)))
        for idx, f in enumerate(files):
            d = load_hodge_npz(f)
            if has_ratio:
                sel_edges = select_edges_quantile(d, k_vals[0])
            else:
                sel_edges = select_edges_legacy(d, k_vals[0])

            avalanches = avalanche_from_edges(sel_edges)
            ctr = collections.Counter(avalanches)
            s = np.array(sorted(ctr.keys()))
            c = np.array([ctr[si] for si in s])
            s_lp, _ = fit_power_law(s, c)
            day_labels.append(os.path.basename(f))
            day_slopes.append(s_lp)

            plt.subplot(len(files), 1, idx + 1)
            if len(s):
                plt.scatter(s, c)
                plt.xscale("log"); plt.yscale("log")
            plt.title(f"{os.path.basename(f)} (α={s_lp})")

        plt.tight_layout()
        plt.savefig("daily_avalanche_comparison.png")
        plt.close()
        with open("daily_avalanche_slopes.csv", "w") as fw:
            fw.write("file,alpha\n")
            for f, a in zip(day_labels, day_slopes):
                fw.write(f"{f},{a}\n")
        print("Wrote daily_avalanche_comparison.png and daily_avalanche_slopes.csv")


if __name__ == "__main__":
    main()
