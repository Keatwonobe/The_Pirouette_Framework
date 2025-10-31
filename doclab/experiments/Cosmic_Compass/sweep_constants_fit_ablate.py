
#!/usr/bin/env python3
"""
sweep_constants_fit_ablate.py

Extends the working sweep to run automatic ablations:
  1) κ OFF:        force kappa0=0 across the grid
  2) interaction OFF
  3) no re-anchoring: r_nudge=1.0 and theta_sweep=0
It also runs the full (baseline) grid and writes:
  - one CSV/JSON per scenario
  - an overall "delta" table comparing each ablation's best vs baseline best

Usage examples:
  python sweep_constants_fit_ablate.py --grid small --out /mnt/data
  python sweep_constants_fit_ablate.py --grid full  --out /mnt/data
"""
import argparse, json, math
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
from pathlib import Path

import numpy as np
import pandas as pd

import constants_fit_modern as C

Ki = 4.0*math.pi/3.0

# ---------- Core helpers ----------

def ridge_fit(X: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    I = np.eye(X.shape[1])
    beta = np.linalg.lstsq(X.T @ X + lam * I, X.T @ y, rcond=None)[0]
    return beta

def loo_log_metrics(X: np.ndarray, ylog: np.ndarray, lam: float) -> Tuple[float, float]:
    """Leave-one-out CV on log targets; returns (RMSE_log, MAE_log)."""
    n = len(ylog)
    preds = np.zeros(n)
    for i in range(n):
        mask = np.ones(n, dtype=bool); mask[i] = False
        Xi, yi = X[mask], ylog[mask]
        beta = ridge_fit(Xi, yi, lam)
        preds[i] = X[i] @ beta
    resid = ylog - preds
    rmse = float(np.sqrt(np.mean(resid**2)))
    mae = float(np.mean(np.abs(resid)))
    return rmse, mae

# --- Geom / design wrapper (aligned with your working script) ---
def build_design_matrix(names: List[str], pos: Dict[str, Tuple[float, float]], kappa0: float, with_interact: bool) -> np.ndarray:
    geom = C.CompassGeom(kappa0=kappa0)
    rs, ths_twisted = [], []
    for name in names:
        if name not in pos: continue
        G, T = pos[name]
        r, th = geom.polar(G, T)
        th_twisted = geom.theta_twisted(th, r, use_kappa=True)  # includes kappa0 if nonzero
        rs.append(r)
        ths_twisted.append(th_twisted)
    return C.design_matrix(rs, ths_twisted, Ki, with_interact=with_interact)

def reanchor_positions(names: List[str], pos: Dict[str, Tuple[float,float]],
                       kappa0: float, r_nudge: float, theta_sweep_deg: int) -> Dict[str, Tuple[float,float]]:
    """Single-pass local re-anchoring guided by provisional beta."""
    obs_map = C.load_constants()
    obs = np.array([obs_map[n] for n in names], dtype=float)
    X0 = build_design_matrix(names, pos, kappa0=kappa0, with_interact=True)
    ylog = np.log(obs + 1e-30)
    beta0 = ridge_fit(X0, ylog, lam=1e-3)

    new_pos = {}
    geom = C.CompassGeom()
    step = max(1, theta_sweep_deg//36 or 1)
    for nm in names:
        G, Ta = pos[nm]
        r, th = geom.polar(G, Ta)
        r2 = r * r_nudge
        best = None
        for th_deg in range(-theta_sweep_deg, theta_sweep_deg+1, step):
            th_try = th + math.radians(th_deg)
            Gt = r2 * math.cos(th_try) * geom.gamma_scale
            Tat = r2 * math.sin(th_try) * geom.ta_scale
            pos_try = dict(pos); pos_try[nm] = (Gt, Tat)
            x = build_design_matrix([nm], pos_try, kappa0=kappa0, with_interact=True)[0]
            yhat = float(x @ beta0)
            resid = abs(ylog[names.index(nm)] - yhat)
            if (best is None) or (resid < best[0]):
                best = (resid, (Gt, Tat))
        new_pos[nm] = best[1]
    return new_pos

@dataclass
class TrialResult:
    scenario: str
    kappa0: float
    interact: bool
    ridge: float
    r_nudge: float
    theta_sweep_deg: int
    rmse_log: float
    mae_log: float
    AIC_kOFF: float
    AIC_kON: float
    delta_AIC: float

def grid_values(which: str):
    if which == "small":
        return {
            "kappa_grid":   [0.0, 0.03, 0.06],
            "inter_grid":   [False, True],
            "ridge_grid":   [0.0, 1e-3, 1e-2],
            "r_nudge_grid": [1.0],
            "theta_grid":   [0, 12],
        }
    else:
        return {
            "kappa_grid":   [0.0, 0.02, 0.04, 0.06, 0.08],
            "inter_grid":   [False, True],
            "ridge_grid":   [0.0, 1e-4, 1e-3, 1e-2, 1e-1],
            "r_nudge_grid": [1.0, 1.05, 0.95],
            "theta_grid":   [0, 8, 16, 24],
        }

def run_sweep_once(grid: str, scenario: str, force_kappa=None, force_inter=None, force_anchor=False):
    gv = grid_values(grid)
    kappa_grid   = [force_kappa] if force_kappa is not None else gv["kappa_grid"]
    inter_grid   = [force_inter] if force_inter is not None else gv["inter_grid"]
    ridge_grid   = gv["ridge_grid"]
    r_nudge_grid = [1.0] if force_anchor else gv["r_nudge_grid"]
    theta_grid   = [0]   if force_anchor else gv["theta_grid"]

    names = list(C.load_constants().keys())
    pos0  = C.load_positions()
    obs_map = C.load_constants()
    obs = np.array([obs_map[n] for n in names], dtype=float)
    ylog = np.log(obs + 1e-30)

    rows = []
    for k0 in kappa_grid:
        for inter in inter_grid:
            for lam in ridge_grid:
                for rn in r_nudge_grid:
                    for td in theta_grid:
                        pos_try = pos0 if (rn == 1.0 and td == 0) else reanchor_positions(names, pos0, kappa0=k0, r_nudge=rn, theta_sweep_deg=td)
                        X = build_design_matrix(names, pos_try, kappa0=k0, with_interact=inter)
                        rmse_log, mae_log = loo_log_metrics(X, ylog, lam)

                        fit_res = C.run_fit(use_interact=inter)
                        rows.append(asdict(TrialResult(
                            scenario=scenario, kappa0=k0, interact=inter, ridge=lam,
                            r_nudge=rn, theta_sweep_deg=td,
                            rmse_log=rmse_log, mae_log=mae_log,
                            AIC_kOFF=float(fit_res["AIC_kOFF"]),
                            AIC_kON=float(fit_res["AIC_kON"]),
                            delta_AIC=float(fit_res["delta_AIC"])
                        )))

    df = pd.DataFrame(rows).sort_values(["rmse_log","mae_log","delta_AIC"], ascending=[True,True,True]).reset_index(drop=True)
    best = df.iloc[0].to_dict()
    return df, best

def run_all(grid: str, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    scenarios = [
        ("baseline",        dict(force_kappa=None, force_inter=None, force_anchor=False)),
        ("ablate_kappa",    dict(force_kappa=0.0,  force_inter=None, force_anchor=False)),
        ("ablate_interact", dict(force_kappa=None, force_inter=False, force_anchor=False)),
        ("ablate_anchor",   dict(force_kappa=None, force_inter=None, force_anchor=True)),
    ]

    best_map = {}
    for scen, args in scenarios:
        df, best = run_sweep_once(grid, scen, **args)
        csv_path = out_dir / f"sweep_{scen}_{grid}.csv"
        json_path = out_dir / f"sweep_{scen}_{grid}.json"
        df.to_csv(csv_path, index=False)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({"best": best, "n_trials": int(len(df)), "scenario": scen, "grid": grid}, f, indent=2)
        best_map[scen] = best

    # Comparison table of bests
    base = best_map["baseline"]
    comp_rows = []
    for scen, b in best_map.items():
        comp = {
            "scenario": scen,
            "rmse_log": float(b["rmse_log"]),
            "mae_log": float(b["mae_log"]),
            "delta_AIC": float(b["delta_AIC"]),
            "kappa0": float(b["kappa0"]),
            "interact": bool(b["interact"]),
            "ridge": float(b["ridge"]),
            "r_nudge": float(b["r_nudge"]),
            "theta_sweep_deg": int(b["theta_sweep_deg"]),
        }
        comp["d_rmse_vs_base"] = float(b["rmse_log"]) - float(base["rmse_log"])
        comp["d_mae_vs_base"]  = float(b["mae_log"])  - float(base["mae_log"])
        comp["d_AIC_vs_base"]  = float(b["delta_AIC"]) - float(base["delta_AIC"])
        comp_rows.append(comp)

    comp_df = pd.DataFrame(comp_rows).sort_values("rmse_log").reset_index(drop=True)
    comp_csv = out_dir / f"sweep_ablation_compare_{grid}.csv"
    comp_df.to_csv(comp_csv, index=False)

    summary = {
        "grid": grid,
        "bests": best_map,
        "comparison_csv": str(comp_csv),
    }
    with open(out_dir / f"sweep_ablation_summary_{grid}.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Wrote ablation CSVs+JSONs to {out_dir}")
    return best_map, comp_df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", choices=["small","full"], default="small")
    ap.add_argument("--out", default="./")
    args = ap.parse_args()
    out_dir = Path(args.out)

    bests, comp_df = run_all(args.grid, out_dir)
    print("=== Best per scenario ===")
    for scen, b in bests.items():
        print(scen, "->", {k: b[k] for k in ["rmse_log","mae_log","delta_AIC","kappa0","interact","ridge","r_nudge","theta_sweep_deg"]})
    print("\nAblation comparison written to:", out_dir / f"sweep_ablation_compare_{args.grid}.csv")

if __name__ == "__main__":
    main()
