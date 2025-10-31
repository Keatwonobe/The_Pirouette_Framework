#!/usr/bin/env python
"""
plasma_calibrate.py

Scan one or more *_kappa.csv files to derive per-band thresholds:
- kappa_lo, kappa_hi from quantiles (default q_lo=0.65, q_hi=0.85)
- deltaP_pos from quantile (default q_dp=0.60)

Writes a YAML file usable by the classifier/processing pipeline.
"""
import argparse, pandas as pd, yaml
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", nargs="+", required=True, help="One or more *_kappa.csv files")
    ap.add_argument("--out", required=True, help="Calibration YAML path")
    ap.add_argument("--q_lo", type=float, default=0.65)
    ap.add_argument("--q_hi", type=float, default=0.85)
    ap.add_argument("--q_dp", type=float, default=0.60)
    args = ap.parse_args()

    bands = {}
    for csv in args.csv:
        df = pd.read_csv(csv)
        for b, g in df.groupby("band"):
            if b not in bands: bands[b] = {"kappa_vals": [], "dp_vals": []}
            bands[b]["kappa_vals"].extend(g["kappa_abs"].dropna().tolist())
            bands[b]["dp_vals"].extend(g["delta_power"].dropna().tolist())

    out = {"bands": {}}
    for b, d in bands.items():
        s_k = pd.Series(d["kappa_vals"])
        s_p = pd.Series(d["dp_vals"])
        out["bands"][b] = {
            "kappa_lo": float(s_k.quantile(args.q_lo)),
            "kappa_hi": float(s_k.quantile(args.q_hi)),
            "deltaP_pos": float(s_p.quantile(args.q_dp)),
        }

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        yaml.safe_dump(out, f, sort_keys=True)
    print(f"Wrote calibration to {args.out}")
if __name__ == "__main__":
    main()
