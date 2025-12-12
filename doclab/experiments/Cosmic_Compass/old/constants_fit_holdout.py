#!/usr/bin/env python3
"""
constants_fit_holdout.py

Leave-one-out predictive validation for the Cosmic Compass.
See header of this file for details.
"""
import argparse, json, math, random
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
from pathlib import Path

import numpy as np
import pandas as pd

import constants_fit_modern as C

Ki = 4.0 * math.pi / 3.0

def ridge_fit(X: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    I = np.eye(X.shape[1])
    return np.linalg.lstsq(X.T @ X + lam * I, X.T @ y, rcond=None)[0]

def kfold_cv_log(X: np.ndarray, ylog: np.ndarray, lam: float, K: int = 5, seed: int = 123):
    n = len(ylog)
    idx = list(range(n))
    random.Random(seed).shuffle(idx)
    folds = [idx[i::K] for i in range(K)]
    preds = np.zeros(n)
    for k in range(K):
        test_idx = folds[k]
        train_idx = [i for i in idx if i not in test_idx]
        Xt, yt = X[train_idx], ylog[train_idx]
        beta = ridge_fit(Xt, yt, lam)
        preds[test_idx] = X[test_idx] @ beta
    resid = ylog - preds
    rmse = float(np.sqrt(np.mean(resid**2)))
    mae = float(np.mean(np.abs(resid)))
    return rmse, mae

def build_design_matrix(names, pos, k0, interact):
    geom = C.CompassGeom(kappa0=k0)
    rs, ths = [], []
    for nm in names:
        G, Ta = pos[nm]
        r, th = geom.polar(G, Ta)
        th_tw = geom.theta_twisted(th, r, use_kappa=True)
        rs.append(r); ths.append(th_tw)
    return C.design_matrix(rs, ths, Ki, with_interact=interact)

def build_design_matrix_linear(names, pos, k0, k1, interact):
    geom = C.CompassGeom(kappa0=0.0)
    rs, ths = [], []
    for nm in names:
        G, Ta = pos[nm]
        r, th = geom.polar(G, Ta)
        th_tw = th + (k0 + k1*r)
        rs.append(r); ths.append(th_tw)
    return C.design_matrix(rs, ths, Ki, with_interact=interact)

def reanchor_positions(names, pos, k0, r_nudge, theta_sweep_deg, interact=True):
    """Re-anchor TRAINING names only (no leakage)."""
    consts = C.load_constants()
    ylog = np.log(np.array([consts[n] for n in names], dtype=float) + 1e-30)
    X0 = build_design_matrix(names, pos, k0, interact=interact)
    beta0 = ridge_fit(X0, ylog, lam=1e-3)

    new_pos = dict(pos)
    geom = C.CompassGeom(kappa0=0.0)
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
            pos_try = dict(new_pos); pos_try[nm] = (Gt, Tat)
            x = build_design_matrix([nm], pos_try, k0, interact=interact)[0]
            yhat = float(x @ beta0)
            resid = abs(ylog[names.index(nm)] - yhat)
            if (best is None) or (resid < best[0]):
                best = (resid, (Gt, Tat))
        new_pos[nm] = best[1]
    return new_pos

@dataclass
class Spec:
    k0: float = 0.08
    k1: Optional[float] = None
    interact: bool = True
    ridge: float = 1e-4
    r_nudge: float = 0.95
    theta_sweep_deg: int = 16
    K: int = 5

def run_holdout(out_dir: str, spec: Spec):
    consts = C.load_constants()
    pos_all = C.load_positions()
    all_names = list(consts.keys())

    rows = []
    for ho in all_names:
        train = [n for n in all_names if n != ho]

        # Re-anchor training set only
        if spec.r_nudge==1.0 and spec.theta_sweep_deg==0:
            pos_train = dict(pos_all)
        else:
            pos_train = reanchor_positions(train, pos_all, spec.k0, spec.r_nudge, spec.theta_sweep_deg, interact=spec.interact)

        ylog_train = np.log(np.array([consts[n] for n in train], dtype=float) + 1e-30)

        if spec.k1 is None:
            X_train = build_design_matrix(train, pos_train, spec.k0, spec.interact)
            X_ho = build_design_matrix([ho], pos_all, spec.k0, spec.interact)
        else:
            X_train = build_design_matrix_linear(train, pos_train, spec.k0, spec.k1, spec.interact)
            X_ho = build_design_matrix_linear([ho], pos_all, spec.k0, spec.k1, spec.interact)

        beta = ridge_fit(X_train, ylog_train, lam=spec.ridge)
        rmse_cv, mae_cv = kfold_cv_log(X_train, ylog_train, lam=spec.ridge, K=spec.K, seed=321)

        y_pred_log = float(X_ho[0] @ beta)
        y_true_log = float(math.log(consts[ho] + 1e-30))
        eps = abs(y_pred_log - y_true_log)

        rows.append({
            "constant": ho,
            "log_true": y_true_log,
            "log_pred": y_pred_log,
            "abs_log_error": eps,
            "train_rmse_log": rmse_cv,
            "train_mae_log": mae_cv,
            "k0": spec.k0,
            "k1": spec.k1 if spec.k1 is not None else 0.0,
            "interact": spec.interact,
            "ridge": spec.ridge,
            "r_nudge": spec.r_nudge,
            "theta_sweep_deg": spec.theta_sweep_deg,
            "K": spec.K,
        })

    df = pd.DataFrame(rows).sort_values("abs_log_error")
    outp = Path(out_dir) / "holdout_predictions.csv"
    df.to_csv(outp, index=False)

    within = (df["abs_log_error"] <= df["train_rmse_log"]).mean()
    summary = {
        "n": int(len(df)),
        "abs_log_error_mean": float(df["abs_log_error"].mean()),
        "abs_log_error_median": float(df["abs_log_error"].median()),
        "within_train_rmse_frac": float(within),
        "best_5": df.head(5).to_dict(orient="records"),
        "worst_5": df.tail(5).to_dict(orient="records"),
        "spec": asdict(spec),
        "csv_path": str(outp),
    }
    with open(Path(out_dir)/"holdout_summary.json","w",encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/mnt/data")
    ap.add_argument("--k0", type=float, default=0.08)
    ap.add_argument("--k1", type=float, default=None)
    ap.add_argument("--interact", action="store_true")
    ap.add_argument("--ridge", type=float, default=1e-4)
    ap.add_argument("--r_nudge", type=float, default=0.95)
    ap.add_argument("--theta_sweep", type=int, default=16)
    ap.add_argument("--K", type=int, default=5)
    args = ap.parse_args()

    spec = Spec(
        k0=args.k0,
        k1=args.k1,
        interact=bool(args.interact),
        ridge=args.ridge,
        r_nudge=args.r_nudge,
        theta_sweep_deg=args.theta_sweep,
        K=args.K,
    )
    Path(args.out).mkdir(parents=True, exist_ok=True)
    run_holdout(args.out, spec)

if __name__ == "__main__":
    main()
