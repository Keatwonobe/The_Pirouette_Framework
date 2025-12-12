#!/usr/bin/env python
import argparse
import json
import os
import glob
from collections import defaultdict

def safe_slope(xs, ys):
    """
    Simple least-squares slope: y = a + b*x
    Returns b, or None if ill-defined.
    """
    if len(xs) < 2:
        return None
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    if den == 0:
        return None
    return num / den

def main():
    ap = argparse.ArgumentParser(
        description="Summarize triadic TPCI results across loads/triads."
    )
    ap.add_argument(
        "--dir",
        default=".",
        help="Directory containing triad result JSON files (default: current directory).",
    )
    ap.add_argument(
        "--glob",
        default="triad-*.json",
        help="Glob pattern for result files (default: triad-*.json).",
    )
    ap.add_argument(
        "--task",
        help="Optional task filter (e.g. LG, NB, SART).",
    )
    ap.add_argument(
        "--subject",
        help="Optional subject filter (e.g. 1, 2...).",
    )
    args = ap.parse_args()

    pattern = os.path.join(args.dir, args.glob)
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No files found for pattern: {pattern}")
        return

    records = []
    for path in files:
        try:
            with open(path, "r") as f:
                rec = json.load(f)
        except Exception as e:
            print(f"! Failed to read {path}: {e}")
            continue

        # Basic sanity: require key fields
        for key in ["subject", "task", "triad", "load", "bandwidth_half", "gauss_fit", "p_bw_ge_null"]:
            if key not in rec:
                print(f"! Skipping {path} (missing key: {key})")
                break
        else:
            if args.subject and str(rec["subject"]) != str(args.subject):
                continue
            if args.task and str(rec["task"]) != str(args.task):
                continue

            gf = rec["gauss_fit"]
            A = gf["A"]
            B = gf["B"]
            rec["_filename"] = os.path.basename(path)
            rec["peak"] = A + B
            rec["baseline"] = B
            rec["peak_minus_baseline"] = A
            records.append(rec)

    if not records:
        print("No matching records after filters.")
        return

    groups = defaultdict(list)
    for r in records:
        key = (str(r["subject"]), str(r["task"]), tuple(float(x) for x in r["triad"]))
        groups[key].append(r)

    for (sub, task, triad), rows in sorted(groups.items()):
        triad_str = f"{triad[0]:.1f}-{triad[1]:.1f}-{triad[2]:.1f}"
        print("=" * 80)
        print(f"Subject {sub} | Task {task} | Triad {triad_str}")
        print("-" * 80)
        print(" load | peak  | bw_half | A(peak-baseline) | p_bw_ge_null | file")
        print("------+-------+---------+------------------+--------------+-----------------------------")

        rows_sorted = sorted(rows, key=lambda r: r["load"])
        loads = [int(r["load"]) for r in rows_sorted]
        peaks = [r["peak"] for r in rows_sorted]
        amps  = [r["peak_minus_baseline"] for r in rows_sorted]
        bws   = [r["bandwidth_half"] for r in rows_sorted]

        for r in rows_sorted:
            print(
                f" {int(r['load']):4d} | "
                f"{r['peak']:.3f} | "
                f"{r['bandwidth_half']:.3f} | "
                f"{r['peak_minus_baseline']:.3f}           | "
                f"{r['p_bw_ge_null']:.3f}       | "
                f"{r['_filename']}"
            )

        # Simple load trends
        slope_peak = safe_slope(loads, peaks)
        slope_amp  = safe_slope(loads, amps)
        slope_bw   = safe_slope(loads, bws)

        print("")
        print("  Trends vs load (per unit load):")
        if slope_peak is not None:
            print(f"    d(peak)/d(load) ≈ {slope_peak:.4f}")
        if slope_amp is not None:
            print(f"    d(A)/d(load)    ≈ {slope_amp:.4f}")
        if slope_bw is not None:
            print(f"    d(bw)/d(load)   ≈ {slope_bw:.4f}  (expect negative if higher load ⇒ sharper peak)")
        print("")

if __name__ == "__main__":
    main()
