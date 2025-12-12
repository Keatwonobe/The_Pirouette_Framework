#!/usr/bin/env python3
"""
sweep_constants_fit.py
Grid-sweeps κ0, interaction flag, ridge λ, and local (r,θ) anchor nudges,
then ranks models by leave-one-out (LOO) log-RMSE. Produces CSV+JSON reports.

Usage (defaults are sensible):
  python sweep_constants_fit.py --grid small
  python sweep_constants_fit.py --grid full --out /mnt/data

Requires:
  - constants_fit_modern.py  (run_fit, design_matrix, polar, theta_twisted, ...)
  - cosmic_compass_modern.py (kappa_field optional)
"""
import argparse, json, math, sys
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from pathlib import Path


import constants_fit_modern as C
# import cosmic_compass_modern as CC # This import is unused, can be removed

Ki = 4.0*math.pi/3.0

# ---------- Helpers ----------

def ridge_fit(X: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    I = np.eye(X.shape[1])
    # Add a small epsilon to the diagonal for stability, especially if lam is zero
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

# ----------------- NEW HELPER FUNCTION -----------------
def build_design_matrix(names: List[str], pos: Dict[str, Tuple[float, float]], kappa0: float, with_interact: bool) -> np.ndarray:
    """
    Correctly preprocesses positions into (r, theta') before calling the
    original design_matrix function.
    """
    geom = C.CompassGeom(kappa0=kappa0)
    rs, ths_twisted = [], []
    for name in names:
        if name not in pos: continue
        G, T = pos[name]
        r, th = geom.polar(G, T)
        # When kappa0=0, theta_twisted returns the original theta, which is correct
        th_twisted = geom.theta_twisted(th, r, use_kappa=True)
        rs.append(r)
        ths_twisted.append(th_twisted)
    
    return C.design_matrix(rs, ths_twisted, Ki, with_interact=with_interact)
# --------------------------------------------------------

def reanchor_positions(names: List[str], pos: Dict[str, Tuple[float,float]],
                       kappa0: float, r_nudge: float, theta_sweep_deg: int) -> Dict[str, Tuple[float,float]]:
    """
    For each constant, hold r within a scale factor (r * r_nudge) and sweep theta around
    its original, choosing the angle that minimizes the one-point residual against current
    global beta estimate. We do a single coarse pass using a provisional beta from all points.
    """
    # Provisional fit to get a beta for guidance
    obs_map = C.load_constants()
    obs = np.array([obs_map[n] for n in names], dtype=float)
    # --- FIXED CALL ---
    X0 = build_design_matrix(names, pos, kappa0=kappa0, with_interact=True)
    ylog = np.log(obs + 1e-30)
    beta0 = ridge_fit(X0, ylog, lam=1e-3)

    new_pos = {}
    geom = C.CompassGeom() # Used for polar conversion
    for nm in names:
        G, Ta = pos[nm]
        r, th = geom.polar(G, Ta)
        r2 = r * r_nudge
        best = None
        for th_deg in range(-theta_sweep_deg, theta_sweep_deg+1, max(1, theta_sweep_deg//36 or 1)):
            th_try = th + math.radians(th_deg)
            # Convert back to Gamma, Ta coordinates for consistency
            Gt = r2 * math.cos(th_try) * geom.gamma_scale
            Tat = r2 * math.sin(th_try) * geom.ta_scale
            
            pos_try = dict(pos); pos_try[nm] = (Gt, Tat)
            # --- FIXED CALL ---
            x = build_design_matrix([nm], pos_try, kappa0=kappa0, with_interact=True)[0]
            yhat = float(x @ beta0)
            resid = abs(ylog[names.index(nm)] - yhat)
            if (best is None) or (resid < best[0]):
                best = (resid, (Gt, Tat))
        new_pos[nm] = best[1]
    return new_pos

@dataclass
class TrialResult:
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
    

def run_sweep(grid: str = "small") -> Tuple[pd.DataFrame, Dict]:
    names = list(C.load_constants().keys())
    pos = C.load_positions()

    if grid == "small":
        kappa_grid = [0.0, 0.03, 0.06]
        interact_grid = [False, True]
        ridge_grid = [0.0, 1e-3, 1e-2]
        r_nudge_grid = [1.0]
        theta_deg_grid = [0, 12]
    else:
        kappa_grid = [0.0, 0.02, 0.04, 0.06, 0.08]
        interact_grid = [False, True]
        ridge_grid = [0.0, 1e-4, 1e-3, 1e-2, 1e-1]
        r_nudge_grid = [1.0, 1.05, 0.95]
        theta_deg_grid = [0, 8, 16, 24]

    obs_map = C.load_constants()
    obs = np.array([obs_map[n] for n in names], dtype=float)
    ylog = np.log(obs + 1e-30)

    trials: List[TrialResult] = []
    rows = []

    for k0 in kappa_grid:
        for inter in interact_grid:
            for lam in ridge_grid:
                for rn in r_nudge_grid:
                    for td in theta_deg_grid:
                        # optionally re-anchor
                        pos_try = pos if (rn == 1.0 and td == 0) else reanchor_positions(names, pos, kappa0=k0, r_nudge=rn, theta_sweep_deg=td)
                        
                        # --- FIXED CALL ---
                        # build design matrix
                        X = build_design_matrix(names, pos_try, kappa0=k0, with_interact=inter)

                        # CV metrics in log-space
                        rmse_log, mae_log = loo_log_metrics(X, ylog, lam)

                        # Also compute your two AICs with the built-in run_fit (using its default solver)
                        # NOTE: run_fit has its own internal geometry and positions, so its results
                        # won't reflect the nudged positions or swept kappa. This might be intended,
                        # but be aware of it.
                        fit_res = C.run_fit(use_interact=inter)
                        AIC_kOFF = float(fit_res["AIC_kOFF"])
                        AIC_kON  = float(fit_res["AIC_kON"])
                        dAIC = float(fit_res["delta_AIC"])

                        tr = TrialResult(kappa0=k0, interact=inter, ridge=lam,
                                         r_nudge=rn, theta_sweep_deg=td,
                                         rmse_log=rmse_log, mae_log=mae_log,
                                         AIC_kOFF=AIC_kOFF, AIC_kON=AIC_kON, delta_AIC=dAIC)
                        trials.append(tr)
                        rows.append(asdict(tr))

    df = pd.DataFrame(rows)
    # Rank by CV RMSE_log, tie-breaker by MAE_log
    df = df.sort_values(["rmse_log","mae_log","delta_AIC"], ascending=[True, True, True]).reset_index(drop=True)
    summary = {
        "best": df.iloc[0].to_dict(),
        "n_trials": int(len(df)),
        "grid": grid,
        "columns": list(df.columns),
    }
    return df, summary

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", choices=["small","full"], default="small")
    ap.add_argument("--out", default=".") # Default to current directory
    args = ap.parse_args()

    df, summary = run_sweep(grid=args.grid)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)


    csv_path = out_dir / f"sweep_results_{args.grid}.csv"
    json_path = out_dir / f"sweep_summary_{args.grid}.json"
    df.to_csv(csv_path, index=False)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()