
#!/usr/bin/env python3
"""
constants_make_synthetic.py

Generate synthetic (invented) constants per sector by sampling positions in Compass space
and assigning values predicted by the current fitted linear model in log-space.
Use ONLY for training augmentation & diagnostics. Do NOT mix with real-constant evaluation.

Outputs:
  synthetic_constants.json  (name -> value)
  synthetic_positions.json  (name -> [Gamma, Ta])
  synthetic_sectors.json    (name -> sector)

Example:
  python constants_make_synthetic.py --per_sector 5 --k0 0.06 --k1 0.05 --interact --ridge 1e-4 --out /mnt/data
"""
import argparse, json, math, random
from pathlib import Path

import numpy as np

import sys, importlib
sys.path.append("/mnt/data")
C = importlib.import_module("constants_fit_modern")

Ki = 4.0 * math.pi / 3.0

def ridge_fit(X, y, lam):
    I = np.eye(X.shape[1])
    return np.linalg.lstsq(X.T @ X + lam * I, X.T @ y, rcond=None)[0]

def build_design_matrix(names, pos, k0, k1, interact):
    # linear kappa if k1 is not None, else flat
    geom = C.CompassGeom(kappa0=0.0)
    rs, ths = [], []
    for nm in names:
        G, Ta = pos[nm]
        r, th = geom.polar(G, Ta)
        th_tw = th + (k0 + (k1 or 0.0)*r)
        rs.append(r); ths.append(th_tw)
    return C.design_matrix(rs, ths, Ki, with_interact=interact)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/mnt/data")
    ap.add_argument("--per_sector", type=int, default=5)
    ap.add_argument("--k0", type=float, default=0.06)
    ap.add_argument("--k1", type=float, default=None)
    ap.add_argument("--interact", action="store_true")
    ap.add_argument("--ridge", type=float, default=1e-4)
    ap.add_argument("--sectors_json", default="/mnt/data/sectors.json")
    ap.add_argument("--positions_json", default="/mnt/data/positions_extended.json")
    ap.add_argument("--constants_json", default="/mnt/data/constants_extended.json")
    args = ap.parse_args()

    consts = json.loads(Path(args.constants_json).read_text())
    pos = json.loads(Path(args.positions_json).read_text())
    sector_map = json.loads(Path(args.sectors_json).read_text())

    names = list(consts.keys())
    ylog = np.log(np.array([consts[n] for n in names], dtype=float) + 1e-30)

    # Fit current model
    X = build_design_matrix(names, pos, args.k0, args.k1, args.interact)
    beta = ridge_fit(X, ylog, lam=args.ridge)

    # Sector centers from existing items
    geom = C.CompassGeom(kappa0=0.0)
    per_sector = {}
    for nm, sec in sector_map.items():
        r, th = geom.polar(*pos[nm])
        per_sector.setdefault(sec, {"r": [], "th": []})
        per_sector[sec]["r"].append(r)
        per_sector[sec]["th"].append(th)

    def circ_mean(ths):
        import cmath
        return float(cmath.phase(sum(cmath.exp(1j*t) for t in ths)/len(ths)))

    centers = {sec: (float(np.median(v["r"])), circ_mean(v["th"])) for sec,v in per_sector.items()}

    # Sample synthetic points
    synth_consts = {}
    synth_pos = {}
    synth_sector = {}
    rnd = random.Random(42)

    for sec, (r0, th0) in centers.items():
        for i in range(args.per_sector):
            # jitter around center
            r = max(0.2, rnd.uniform(0.9*r0, 1.1*r0))
            th = th0 + rnd.uniform(-math.radians(10), math.radians(10))
            G = r * math.cos(th) * geom.gamma_scale
            T = r * math.sin(th) * geom.ta_scale
            nm = f"syn_{sec}_{i+1:02d}"
            # predict value
            Xi = build_design_matrix([nm], {nm:(G,T)}, args.k0, args.k1, args.interact)
            yhat_log = float(Xi[0] @ beta)
            val = float(math.exp(yhat_log))
            synth_consts[nm] = val
            synth_pos[nm] = [G, T]
            synth_sector[nm] = sec

    out_dir = Path(args.out)
    (out_dir/"synthetic_constants.json").write_text(json.dumps(synth_consts, indent=2))
    (out_dir/"synthetic_positions.json").write_text(json.dumps(synth_pos, indent=2))
    (out_dir/"synthetic_sectors.json").write_text(json.dumps(synth_sector, indent=2))
    print("Wrote synthetic datasets to", out_dir)

if __name__ == "__main__":
    main()
