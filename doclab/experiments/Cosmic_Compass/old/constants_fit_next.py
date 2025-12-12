import argparse, json, math, random
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
from pathlib import Path

import numpy as np
import pandas as pd

import constants_fit_modern as C

Ki = 4.0 * math.pi / 3.0

def load_constants_with_overrides(constants_override: Optional[str]) -> Dict[str, float]:
    base = C.load_constants()
    if constants_override:
        with open(constants_override, "r", encoding="utf-8") as f:
            extra = json.load(f)
        base.update({k: float(v) for k, v in extra.items()})
    return base

def load_positions_with_overrides(positions_override: Optional[str]) -> Dict[str, Tuple[float, float]]:
    base = C.load_positions()
    if positions_override:
        with open(positions_override, "r", encoding="utf-8") as f:
            extra = json.load(f)
        for k, v in extra.items():
            base[k] = (float(v[0]), float(v[1]))
    return base

def ridge_fit(X: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    I = np.eye(X.shape[1])
    beta = np.linalg.lstsq(X.T @ X + lam * I, X.T @ y, rcond=None)[0]
    return beta

def kfold_cv_log(X: np.ndarray, ylog: np.ndarray, lam: float, K: int = 5, seed: int = 123) -> tuple[float, float]:
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

def build_design_matrix(names: List[str], pos: Dict[str, Tuple[float, float]],
                        k0: float, interact: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    geom = C.CompassGeom(kappa0=k0)
    rs, ths = [], []
    for nm in names:
        G, Ta = pos[nm]
        r, th = geom.polar(G, Ta)
        th_tw = geom.theta_twisted(th, r, use_kappa=True)
        rs.append(r); ths.append(th_tw)
    X = C.design_matrix(rs, ths, Ki, with_interact=interact)
    return X, np.array(rs), np.array(ths)

def build_design_matrix_kappa_linear(names: List[str], pos: Dict[str, Tuple[float, float]],
                                     k0: float, k1: float, interact: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    geom = C.CompassGeom(kappa0=0.0)
    rs, ths = [], []
    for nm in names:
        G, Ta = pos[nm]
        r, th = geom.polar(G, Ta)
        th_tw = th + (k0 + k1 * r)
        rs.append(r); ths.append(th_tw)
    X = C.design_matrix(rs, ths, Ki, with_interact=interact)
    return X, np.array(rs), np.array(ths)

@dataclass
class FitSpec:
    k0: float = 0.08
    k1: Optional[float] = None
    interact: bool = True
    ridge: float = 1e-4
    r_nudge: float = 0.95
    theta_sweep_deg: int = 16

def reanchor_positions(names: List[str], pos: Dict[str, Tuple[float,float]],
                       obs_map: Dict[str, float], k0: float, r_nudge: float, theta_sweep_deg: int) -> Dict[str, Tuple[float,float]]:
    ylog = np.log(np.array([obs_map[n] for n in names], dtype=float) + 1e-30)
    X0, _, _ = build_design_matrix(names, pos, k0, interact=True)
    beta0 = ridge_fit(X0, ylog, lam=1e-3)

    new_pos = {}
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
            pos_try = dict(pos); pos_try[nm] = (Gt, Tat)
            x,_,_ = build_design_matrix([nm], pos_try, k0, interact=True)
            yhat = float(x[0] @ beta0)
            resid = abs(ylog[names.index(nm)] - yhat)
            if (best is None) or (resid < best[0]):
                best = (resid, (Gt, Tat))
        new_pos[nm] = best[1]
    return new_pos

def run_baseline(constants_override: Optional[str], positions_override: Optional[str],
                 spec: FitSpec, K: int, out_dir: str):
    consts = load_constants_with_overrides(constants_override)
    pos = load_positions_with_overrides(positions_override)
    names = list(consts.keys())
    ylog = np.log(np.array([abs(consts[n] for n in names)], dtype=float) + 1e-30)

    pos_use = pos if (spec.r_nudge==1.0 and spec.theta_sweep_deg==0) else reanchor_positions(names, pos, consts, spec.k0, spec.r_nudge, spec.theta_sweep_deg)

    if spec.k1 is None:
        X, _, _ = build_design_matrix(names, pos_use, spec.k0, spec.interact)
    else:
        X, _, _ = build_design_matrix_kappa_linear(names, pos_use, spec.k0, spec.k1, spec.interact)

    rmse, mae = kfold_cv_log(X, ylog, lam=spec.ridge, K=K, seed=123)
    out = {
        "names": names,
        "K": K,
        "rmse_log": rmse,
        "mae_log": mae,
        "spec": asdict(spec),
        "n_constants": len(names),
    }
    p = Path(out_dir) / "baseline_kfold_summary.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    return out

def run_kappa_profile(constants_override: Optional[str], positions_override: Optional[str],
                      k0_grid: List[float], k1_grid: List[float],
                      interact: bool, ridge: float, K: int, out_dir: str):
    consts = load_constants_with_overrides(constants_override)
    pos = load_positions_with_overrides(positions_override)
    names = list(consts.keys())
    ylog = np.log(np.array([abs(consts[n] for n in names)], dtype=float) + 1e-30)

    rows = []
    for k0 in k0_grid:
        for k1 in k1_grid:
            pos_use = reanchor_positions(names, pos, consts, k0, r_nudge=0.95, theta_sweep_deg=16)
            X, _, _ = build_design_matrix_kappa_linear(names, pos_use, k0, k1, interact)
            rmse, mae = kfold_cv_log(X, ylog, lam=ridge, K=K, seed=123)
            rows.append({"k0": k0, "k1": k1, "rmse_log": rmse, "mae_log": mae})
    df = pd.DataFrame(rows).sort_values(["rmse_log","mae_log"]).reset_index(drop=True)
    csvp = Path(out_dir) / "kappa_profile_grid.csv"
    df.to_csv(csvp, index=False)
    best = df.iloc[0].to_dict()
    with open(Path(out_dir)/"kappa_profile_best.json","w",encoding="utf-8") as f:
        json.dump(best, f, indent=2)
    return best, df

def per_constant_impact(constants_override: Optional[str], positions_override: Optional[str],
                        base_spec: FitSpec, out_dir: str):
    consts = load_constants_with_overrides(constants_override)
    pos = load_positions_with_overrides(positions_override)
    names = list(consts.keys())
    ylog = np.log(np.array([consts[n] for n in names], dtype=float) + 1e-30)

    pos_use = reanchor_positions(names, pos, consts, base_spec.k0, base_spec.r_nudge, base_spec.theta_sweep_deg)
    X_base,_,_ = build_design_matrix(names, pos_use, base_spec.k0, base_spec.interact)
    beta = ridge_fit(X_base, ylog, lam=base_spec.ridge)
    yhat = X_base @ beta
    resid_base = ylog - yhat

    audits = []
    X_koff,_,_ = build_design_matrix(names, pos_use, 0.0, base_spec.interact)
    yhat_koff = X_koff @ ridge_fit(X_koff, ylog, lam=base_spec.ridge)
    resid_koff = ylog - yhat_koff
    audits.append(("kappa_off", resid_koff))

    X_i0,_,_ = build_design_matrix(names, pos_use, base_spec.k0, False)
    yhat_i0 = X_i0 @ ridge_fit(X_i0, ylog, lam=base_spec.ridge)
    resid_i0 = ylog - yhat_i0
    audits.append(("interact_off", resid_i0))

    X_a0,_,_ = build_design_matrix(names, pos, base_spec.k0, base_spec.interact)
    yhat_a0 = X_a0 @ ridge_fit(X_a0, ylog, lam=base_spec.ridge)
    resid_a0 = ylog - yhat_a0
    audits.append(("anchor_off", resid_a0))

    rows = []
    for tag, resid_alt in audits:
        for nm, r_base, r_alt in zip(names, resid_base, resid_alt):
            rows.append({
                "constant": nm,
                "mode": tag,
                "delta_abs_resid": float(abs(r_alt) - abs(r_base)),
                "abs_resid_baseline": float(abs(r_base)),
                "abs_resid_mode": float(abs(r_alt)),
            })
    df = pd.DataFrame(rows)
    outp = Path(out_dir) / "per_constant_impact.csv"
    df.to_csv(outp, index=False)
    return df

def bootstrap_ci(constants_override: Optional[str], positions_override: Optional[str],
                 spec: FitSpec, K: int, B: int, out_dir: str):
    consts = load_constants_with_overrides(constants_override)
    pos = load_positions_with_overrides(positions_override)
    names_full = list(consts.keys())
    ylog_full = np.log(np.array([consts[n] for n in names_full], dtype=float) + 1e-30)

    rows = []
    rng = np.random.default_rng(1234)
    for b in range(B):
        idx = rng.integers(0, len(names_full), size=len(names_full))
        names = [names_full[i] for i in idx]
        names_unique = list(dict.fromkeys(names))

        pos_use = reanchor_positions(names_unique, pos, consts, spec.k0, spec.r_nudge, spec.theta_sweep_deg)
        ylog = np.log(np.array([consts[n] for n in names_unique], dtype=float) + 1e-30)

        if spec.k1 is None:
            X,_,_ = build_design_matrix(names_unique, pos_use, spec.k0, spec.interact)
        else:
            X,_,_ = build_design_matrix_kappa_linear(names_unique, pos_use, spec.k0, spec.k1, spec.interact)

        rmse, mae = kfold_cv_log(X, ylog, lam=spec.ridge, K=K, seed=123+b)
        rows.append({"b": b, "rmse_log": rmse, "mae_log": mae})

    df = pd.DataFrame(rows)
    df.to_csv(Path(out_dir)/"bootstrap_metrics.csv", index=False)
    q = df["rmse_log"].quantile
    summary = {
        "B": B, "K": K,
        "rmse_log_mean": float(df["rmse_log"].mean()),
        "rmse_log_ci_95": [float(q(0.025)), float(q(0.975))],
        "mae_log_mean": float(df["mae_log"].mean()),
        "mae_log_ci_95": [float(df["mae_log"].quantile(0.025)), float(df["mae_log"].quantile(0.975))],
        "spec": asdict(spec),
    }
    with open(Path(out_dir)/"bootstrap_summary.json","w",encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return summary

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="./")
    ap.add_argument("--constants_override", default=None)
    ap.add_argument("--positions_override", default=None)
    ap.add_argument("--mode", choices=["baseline","kappa_profile","impact","bootstrap"], default="baseline")

    ap.add_argument("--k0", type=float, default=0.08)
    ap.add_argument("--k1", type=float, default=None)
    ap.add_argument("--interact", action="store_true")
    ap.add_argument("--ridge", type=float, default=1e-4)
    ap.add_argument("--r_nudge", type=float, default=0.95)
    ap.add_argument("--theta_sweep", type=int, default=16)
    ap.add_argument("--K", type=int, default=5)
    ap.add_argument("--B", type=int, default=200)

    ap.add_argument("--k0_grid", type=str, default="0,0.02,0.04,0.06,0.08")
    ap.add_argument("--k1_grid", type=str, default="-0.05,-0.02,0,0.02,0.05")

    args = ap.parse_args()
    out_dir = args.out

    spec = FitSpec(
        k0=args.k0,
        k1=args.k1,
        interact=bool(args.interact),
        ridge=args.ridge,
        r_nudge=args.r_nudge,
        theta_sweep_deg=args.theta_sweep,
    )

    if args.mode == "baseline":
        res = run_baseline(args.constants_override, args.positions_override, spec, K=args.K, out_dir=out_dir)
        print(json.dumps(res, indent=2))
    elif args.mode == "kappa_profile":
        k0_grid = [float(x) for x in args.k0_grid.split(",") if x.strip()!=""]
        k1_grid = [float(x) for x in args.k1_grid.split(",") if x.strip()!=""]
        best, _ = run_kappa_profile(args.constants_override, args.positions_override,
                                    k0_grid, k1_grid, spec.interact, spec.ridge, args.K, out_dir)
        print(json.dumps({"best": best}, indent=2))
    elif args.mode == "impact":
        df = per_constant_impact(args.constants_override, args.positions_override, spec, out_dir)
        print(f"Wrote per-constant impact to {out_dir}/per_constant_impact.csv (rows={len(df)})")
    elif args.mode == "bootstrap":
        summ = bootstrap_ci(args.constants_override, args.positions_override, spec, K=args.K, B=args.B, out_dir=out_dir)
        print(json.dumps(summ, indent=2))

if __name__ == "__main__":
    main()
