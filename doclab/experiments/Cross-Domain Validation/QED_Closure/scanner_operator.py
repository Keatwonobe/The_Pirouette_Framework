
from __future__ import annotations
import json, math, argparse, pathlib, random
from dataclasses import dataclass
from typing import Dict, Any, List

# ------------------------------
# Determinism
# ------------------------------
SEED = 1337
random.seed(SEED)

# ------------------------------
# Dataclasses
# ------------------------------
@dataclass
class GaugeBlock:
    group: str    # "U1","SU2","SU3"
    kind: str     # "abelian" or "nonabelian"
    Nc: int
    g: float
    beta: float

@dataclass
class LatticeSpec:
    N: int = 16
    Nt: int = 32
    a: float = 1.0

@dataclass
class ModelSpec:
    lat: LatticeSpec
    groups: Dict[str, GaugeBlock]

@dataclass
class OptionCParams:
    dphi0: float = 1.0
    xi0: float = 1.0
    kappa3: float = 1.0
    g_c: float = 0.9
    alpha_beta: float = 0.5
    eps_floor: float = 1e-9

# ------------------------------
# Option-C Map
# ------------------------------
def effective_dphi_bound(g: float, beta: float, p: OptionCParams) -> float:
    act = 1.0 / (1.0 + math.exp(-(g - p.g_c) * (1.0 + p.alpha_beta*beta) * 8.0))
    shrink = 0.8 * act
    return max(p.dphi0 * (1.0 - shrink), p.eps_floor)

def xi_gamma_from_dphi(dphi_bound: float, p: OptionCParams) -> float:
    return max(p.xi0 * (dphi_bound / p.dphi0), p.eps_floor)

def binding_energy(g: float, beta: float, p: OptionCParams) -> float:
    x = max(g - p.g_c, 0.0)
    return x * (1.0 + p.alpha_beta * beta)

def sigma_string_tension(xi_g: float, E_bind: float, kappa3: float) -> float:
    return (kappa3 / (xi_g*xi_g)) * (E_bind * E_bind)

def predict_observables_grouped(model, group_key, base_params, w, gc, ab):
    p = OptionCParams(**{**base_params.__dict__, "g_c": gc[group_key], "alpha_beta": ab[group_key]})
    # as before:
    gblock = model.groups[group_key]
    dphi_b = effective_dphi_bound(gblock.g, gblock.beta, p)
    xi_g   = xi_gamma_from_dphi(dphi_b, p)
    Eb0    = binding_energy(gblock.g, gblock.beta, p)
    E_b    = w[group_key] * Eb0                    # ← group weight
    sigma  = sigma_string_tension(xi_g, E_b, p.kappa3)
    lat_penalty = 0.05 if (model.lat.N < 12 or model.lat.Nt < 24) else 0.0
    loss = 1.0*xi_g + 0.2*E_b + lat_penalty
    return {"dphi_bound": dphi_b, "xi_gamma": xi_g, "E_bind": E_b, "sigma": sigma, "closure_loss": loss}


# ------------------------------
# Scan generation (standalone grid)
# ------------------------------
def generate_scan_grid(group: str, gmin: float, gmax: float, gbins: int,
                       bmin: float, bmax: float, bbins: int,
                       N: int=16, Nt: int=32, a: float=1.0) -> List[ModelSpec]:
    if group not in ("U1","SU2","SU3"):
        raise ValueError("group must be one of U1, SU2, SU3")

    kind = "abelian" if group=="U1" else "nonabelian"
    Nc = {"U1":1,"SU2":2,"SU3":3}[group]

    models = []
    for i in range(gbins):
        g = gmin + (gmax - gmin) * (i/(gbins-1 if gbins>1 else 1))
        for j in range(bbins):
            beta = bmin + (bmax - bmin) * (j/(bbins-1 if bbins>1 else 1))

            blocks = {
                "U1":  GaugeBlock("U1",  "abelian",    1, g if group=="U1" else 0.9, beta if group=="U1" else 2.0),
                "SU2": GaugeBlock("SU2", "nonabelian", 2, g if group=="SU2" else 1.1, beta if group=="SU2" else 2.2),
                "SU3": GaugeBlock("SU3", "nonabelian", 3, g if group=="SU3" else 1.1, beta if group=="SU3" else 2.2),
            }
            # The active group uses the scan values; inactive groups use reasonable placeholders.
            models.append(ModelSpec(lat=LatticeSpec(N=N,Nt=Nt,a=a), groups=blocks))
    return models

# ------------------------------
# Run scan + closure for a group
# ------------------------------
def run_scan_and_close(models: List[ModelSpec], group_key: str, p: OptionCParams) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for m in models:
        obs = predict_observables_grouped(m, group_key, p, w, gc, ab)
        rows.append({
            "lat_N": m.lat.N, "lat_Nt": m.lat.Nt, "lat_a": m.lat.a,
            "group": group_key,
            "g": m.groups[group_key].g,
            "beta": m.groups[group_key].beta,
            "Nc": m.groups[group_key].Nc,
            **obs,
            "status": "OK"
        })
    best_idx = min(range(len(rows)), key=lambda i: rows[i]["closure_loss"])
    rows[best_idx]["status"] = "BEST"
    return rows

def write_json(path: pathlib.Path, obj: Any):
    path.write_text(json.dumps(obj, indent=2))

# ------------------------------
# Seeds maintenance
# ------------------------------
def update_empirical_seeds(outdir: pathlib.Path, best_sigma_by_group: Dict[str, float]):
    seeds_path = outdir / "empirical_seeds.json"
    if seeds_path.exists():
        data = json.loads(seeds_path.read_text())
    else:
        data = {"seeds": [], "source": "empirical (Option-C BEST per group)"}

    # Convert to dict for easy update
    existing = {row["group"]: row for row in data.get("seeds", [])}

    for gkey, sigma in best_sigma_by_group.items():
        if sigma is None: 
            continue
        K = math.sqrt(sigma)
        note = "BEST from Option-C closure"
        existing[gkey] = {"group": gkey, "sigma": sigma, "K": K, "note": note}

    # Rebuild ordered list U1, SU2, SU3
    new_list = [existing[k] for k in ("U1","SU2","SU3") if k in existing]
    data["seeds"] = new_list
    write_json(seeds_path, data)
    return seeds_path

# ------------------------------
# CLI
# ------------------------------
def main():
    ap = argparse.ArgumentParser(description="Standalone scanner operator for U1/SU2/SU3 Option-C closure")
    ap.add_argument("--group", required=True, choices=["U1","SU2","SU3"])
    ap.add_argument("--outdir", type=str, default="/mnt/data")
    ap.add_argument("--gmin", type=float, required=True)
    ap.add_argument("--gmax", type=float, required=True)
    ap.add_argument("--gbins", type=int, default=25)
    ap.add_argument("--bmin", type=float, required=True)
    ap.add_argument("--bmax", type=float, required=True)
    ap.add_argument("--bbins", type=int, default=25)
    ap.add_argument("--N", type=int, default=16)
    ap.add_argument("--Nt", type=int, default=32)
    ap.add_argument("--a", type=float, default=1.0)
    ap.add_argument("--gc", type=float, default=0.9, help="binding threshold g_c")
    ap.add_argument("--alpha_beta", type=float, default=0.5, help="beta sharpness")
    ap.add_argument("--wU1", type=float, default=1.0)
    ap.add_argument("--wSU2", type=float, default=1.0)
    ap.add_argument("--wSU3", type=float, default=1.0)
    ap.add_argument("--gcU1", type=float, default=None)
    ap.add_argument("--gcSU2", type=float, default=None)
    ap.add_argument("--gcSU3", type=float, default=None)
    ap.add_argument("--abU1", type=float, default=None)   # alpha_beta overrides
    ap.add_argument("--abSU2", type=float, default=None)
    ap.add_argument("--abSU3", type=float, default=None)
    args = ap.parse_args()

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    w = {"U1": args.wU1, "SU2": args.wSU2, "SU3": args.wSU3}
    gc = {"U1": args.gcU1 or args.gc, "SU2": args.gcSU2 or args.gc, "SU3": args.gcSU3 or args.gc}
    ab = {"U1": args.abU1 or args.alpha_beta, "SU2": args.abSU2 or args.alpha_beta, "SU3": args.abSU3 or args.alpha_beta}

    # Generate grid
    models = generate_scan_grid(args.group, args.gmin, args.gmax, args.gbins,
                                args.bmin, args.bmax, args.bbins,
                                N=args.N, Nt=args.Nt, a=args.a)
    # Save raw scan params for provenance
    scan_rows = []
    for m in models:
        scan_rows.append({
            "params": {
                "U1":  {"type": m.groups["U1"].kind,  "Nc": m.groups["U1"].Nc,  "g": m.groups["U1"].g,  "beta": m.groups["U1"].beta},
                "SU2": {"type": m.groups["SU2"].kind, "Nc": m.groups["SU2"].Nc, "g": m.groups["SU2"].g, "beta": m.groups["SU2"].beta},
                "SU3": {"type": m.groups["SU3"].kind, "Nc": m.groups["SU3"].Nc, "g": m.groups["SU3"].g, "beta": m.groups["SU3"].beta},
                "N": m.lat.N, "Nt": m.lat.Nt, "a": m.lat.a
            }
        })
    scan_path = outdir / f"scan_{args.group}.json"
    write_json(scan_path, scan_rows)

    # Run closure
    p = OptionCParams(g_c=args.gc, alpha_beta=args.alpha_beta)
    closed = run_scan_and_close(models, group_key=args.group, p=p)
    closure_path = outdir / f"closure_{args.group}.json"
    write_json(closure_path, closed)

    # Announce BEST and update seeds
    best = next(row for row in closed if row["status"]=="BEST")
    print(f"[{args.group}] BEST @ g={best['g']:.6g}, beta={best['beta']:.6g} "
          f"→ sigma={best['sigma']:.6g}, xi_gamma={best['xi_gamma']:.6g}")

    seeds_path = update_empirical_seeds(outdir, {args.group: best["sigma"]})
    print(f"[seeds] updated: {seeds_path}")

if __name__ == "__main__":
    main()
