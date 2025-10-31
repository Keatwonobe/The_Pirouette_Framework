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
    g_c: float = 0.9 # Default g_c, will be overridden by group-specific ones if provided
    alpha_beta: float = 0.5 # Default alpha_beta, will be overridden by group-specific ones if provided
    eps_floor: float = 1e-9

# ------------------------------
# Option-C Map
# ------------------------------
def effective_dphi_bound(g: float, beta: float, p: OptionCParams) -> float:
    # Note: p.g_c and p.alpha_beta here should be the group-specific values
    act = 1.0 / (1.0 + math.exp(-(g - p.g_c) * (1.0 + p.alpha_beta*beta) * 8.0))
    shrink = 0.8 * act
    return max(p.dphi0 * (1.0 - shrink), p.eps_floor)

def xi_gamma_from_dphi(dphi_bound: float, p: OptionCParams) -> float:
    return max(p.xi0 * (dphi_bound / p.dphi0), p.eps_floor)

def binding_energy(g: float, beta: float, p: OptionCParams) -> float:
    # Note: p.g_c and p.alpha_beta here should be the group-specific values
    x = max(g - p.g_c, 0.0)
    return x * (1.0 + p.alpha_beta * beta)

def sigma_string_tension(xi_g: float, E_bind: float, kappa3: float) -> float:
    # Check for non-positive xi_g to avoid division by zero or sqrt of negative
    if xi_g <= 0:
        return float('inf') # Or handle as an error
    return (kappa3 / (xi_g*xi_g)) * (E_bind * E_bind)

def predict_observables_grouped(model: ModelSpec, group_key: str, base_params: OptionCParams, w: Dict[str, float], gc: Dict[str, float], ab: Dict[str, float]):
    """
    Predicts observables for a specific group using group-specific gc and ab.
    """
    # Create OptionCParams instance with the CORRECT group-specific g_c and alpha_beta
    p = OptionCParams(
        **{**base_params.__dict__, "g_c": gc[group_key], "alpha_beta": ab[group_key]}
    )

    gblock = model.groups[group_key]
    dphi_b = effective_dphi_bound(gblock.g, gblock.beta, p)
    xi_g   = xi_gamma_from_dphi(dphi_b, p)
    Eb0    = binding_energy(gblock.g, gblock.beta, p)
    E_b    = w[group_key] * Eb0                    # ← group weight

    # Calculate sigma using the base kappa3 from base_params
    sigma  = sigma_string_tension(xi_g, E_b, base_params.kappa3)

    lat_penalty = 0.05 if (model.lat.N < 12 or model.lat.Nt < 24) else 0.0
    # Make sure loss components are finite
    loss = 1.0 * (xi_g if math.isfinite(xi_g) else 1e9) + \
           0.2 * (E_b if math.isfinite(E_b) else 1e9) + \
           lat_penalty
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
    # Ensure bins >= 1
    gbins = max(1, gbins)
    bbins = max(1, bbins)

    for i in range(gbins):
        g = gmin + (gmax - gmin) * (i/(gbins-1 if gbins>1 else 1)) if gbins > 1 else gmin
        for j in range(bbins):
            beta = bmin + (bmax - bmin) * (j/(bbins-1 if bbins>1 else 1)) if bbins > 1 else bmin

            # Use reasonable fixed placeholder values for inactive groups
            blocks = {
                "U1":  GaugeBlock("U1",  "abelian",    1, g if group=="U1" else 0.4, beta if group=="U1" else 1.2),
                "SU2": GaugeBlock("SU2", "nonabelian", 2, g if group=="SU2" else 0.8, beta if group=="SU2" else 1.8),
                "SU3": GaugeBlock("SU3", "nonabelian", 3, g if group=="SU3" else 1.0, beta if group=="SU3" else 2.2),
            }
            # The active group uses the scan values; inactive groups use the placeholders.
            models.append(ModelSpec(lat=LatticeSpec(N=N,Nt=Nt,a=a), groups=blocks))
    return models

# ------------------------------
# Run scan + closure for a group
# ------------------------------
# <<< FIX: Added w, gc, ab arguments >>>
def run_scan_and_close(models: List[ModelSpec], group_key: str, p: OptionCParams, w: Dict[str, float], gc: Dict[str, float], ab: Dict[str, float]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for m in models:
        # <<< FIX: Pass w, gc, ab down >>>
        obs = predict_observables_grouped(m, group_key, p, w, gc, ab)
        # Store results
        rows.append({
            "lat_N": m.lat.N, "lat_Nt": m.lat.Nt, "lat_a": m.lat.a,
            "group": group_key,
            "g": m.groups[group_key].g,
            "beta": m.groups[group_key].beta,
            "Nc": m.groups[group_key].Nc,
            **obs,
            "status": "OK" # Default status
        })

    # Find the best result (minimum finite loss)
    finite_loss_rows = [r for r in rows if math.isfinite(r["closure_loss"])]
    if finite_loss_rows:
        best_row = min(finite_loss_rows, key=lambda row: row["closure_loss"])
        # Update status in the original rows list by finding the matching entry
        for i, row in enumerate(rows):
             # Compare relevant params to uniquely identify the row
             if row['g'] == best_row['g'] and row['beta'] == best_row['beta'] and row['group'] == best_row['group']:
                 rows[i]["status"] = "BEST"
                 break
    else:
        print(f"Warning: No valid results with finite loss found for group {group_key}.")

    return rows

def write_json(path: pathlib.Path, obj: Any):
    # Helper to convert potential non-serializable types like inf
    def default_serializer(o):
        if isinstance(o, float) and not math.isfinite(o):
            return str(o) # Convert inf/-inf/nan to string
        return o

    try:
        path.write_text(json.dumps(obj, indent=2, default=default_serializer))
    except TypeError as e:
        print(f"Error writing JSON to {path}: {e}")
        # Optionally, print the problematic object part
        # print("Problematic object snippet:", repr(obj)[:500])


# ------------------------------
# Seeds maintenance
# ------------------------------
def update_empirical_seeds(outdir: pathlib.Path, best_sigma_by_group: Dict[str, float]):
    seeds_path = outdir / "empirical_seeds.json"
    if seeds_path.exists():
        try:
            data = json.loads(seeds_path.read_text())
            if not isinstance(data.get("seeds"), list): # Basic validation
                 data = {"seeds": [], "source": "empirical (Option-C BEST per group)"}
        except json.JSONDecodeError:
            print(f"Warning: Could not decode existing seeds file {seeds_path}. Starting fresh.")
            data = {"seeds": [], "source": "empirical (Option-C BEST per group)"}
    else:
        data = {"seeds": [], "source": "empirical (Option-C BEST per group)"}

    # Convert to dict for easy update
    existing = {row["group"]: row for row in data.get("seeds", []) if "group" in row}

    for gkey, sigma in best_sigma_by_group.items():
        if sigma is None or not math.isfinite(sigma) or sigma <= 0: # Check for valid sigma
            print(f"Skipping update for group {gkey} due to invalid sigma: {sigma}")
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
    # --- OptionCParams Base ---
    # These set the defaults for OptionCParams, but can be overridden by group-specific gc/ab args below
    ap.add_argument("--kappa3", type=float, default=1.0)
    ap.add_argument("--dphi0", type=float, default=1.0)
    ap.add_argument("--xi0", type=float, default=1.0)
    ap.add_argument("--gc", type=float, default=0.9, help="Default binding threshold g_c if group-specific not set")
    ap.add_argument("--alpha_beta", type=float, default=0.5, help="Default beta sharpness if group-specific not set")
    # --- Group Weights ---
    ap.add_argument("--wU1", type=float, default=1.0)
    ap.add_argument("--wSU2", type=float, default=1.0)
    ap.add_argument("--wSU3", type=float, default=1.0)
    # --- Group Specific Overrides for g_c ---
    ap.add_argument("--gcU1", type=float, default=None, help="Override g_c for U1")
    ap.add_argument("--gcSU2", type=float, default=None, help="Override g_c for SU2")
    ap.add_argument("--gcSU3", type=float, default=None, help="Override g_c for SU3")
    # --- Group Specific Overrides for alpha_beta ---
    ap.add_argument("--abU1", type=float, default=None, help="Override alpha_beta for U1")
    ap.add_argument("--abSU2", type=float, default=None, help="Override alpha_beta for SU2")
    ap.add_argument("--abSU3", type=float, default=None, help="Override alpha_beta for SU3")
    args = ap.parse_args()

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Consolidate group-specific parameters
    w = {"U1": args.wU1, "SU2": args.wSU2, "SU3": args.wSU3}
    # Use specific override if provided, else use the default gc/alpha_beta
    gc = {"U1": args.gcU1 if args.gcU1 is not None else args.gc,
          "SU2": args.gcSU2 if args.gcSU2 is not None else args.gc,
          "SU3": args.gcSU3 if args.gcSU3 is not None else args.gc}
    ab = {"U1": args.abU1 if args.abU1 is not None else args.alpha_beta,
          "SU2": args.abSU2 if args.abSU2 is not None else args.alpha_beta,
          "SU3": args.abSU3 if args.abSU3 is not None else args.alpha_beta}

    # Generate grid
    print(f"Generating grid for {args.group}...")
    models = generate_scan_grid(args.group, args.gmin, args.gmax, args.gbins,
                                args.bmin, args.bmax, args.bbins,
                                N=args.N, Nt=args.Nt, a=args.a)
    print(f"Generated {len(models)} model configurations.")

    # Save raw scan params for provenance (Optional but good practice)
    # Consider saving less redundant info if needed
    # scan_rows = [...] # Code omitted for brevity, logic remains the same
    # scan_path = outdir / f"scan_{args.group}.json"
    # write_json(scan_path, scan_rows)
    # print(f"Saved raw scan parameter list to {scan_path}")

    # Create base OptionCParams (without group-specific gc/ab, those are handled in predict_observables_grouped)
    base_p = OptionCParams(
        kappa3=args.kappa3,
        dphi0=args.dphi0,
        xi0=args.xi0,
        g_c=args.gc, # Include defaults, though they'll be overridden per group
        alpha_beta=args.alpha_beta
    )

    # Run closure
    print(f"Running closure calculations for {args.group}...")
    # <<< FIX: Pass w, gc, ab to run_scan_and_close >>>
    closed = run_scan_and_close(models, group_key=args.group, p=base_p, w=w, gc=gc, ab=ab)
    closure_path = outdir / f"closure_{args.group}.json"
    write_json(closure_path, closed)
    print(f"Saved closure results to {closure_path}")


    # Announce BEST and update seeds
    best_rows = [row for row in closed if row["status"]=="BEST"]
    if best_rows:
        best = best_rows[0] # Get the first 'BEST' row found
        print(f"[{args.group}] BEST @ g={best['g']:.6g}, beta={best['beta']:.6g} "
              f"→ sigma={best['sigma']:.6g}, xi_gamma={best['xi_gamma']:.6g}, loss={best['closure_loss']:.6g}")
        seeds_path = update_empirical_seeds(outdir, {args.group: best["sigma"]})
        print(f"[seeds] updated: {seeds_path}")
    else:
        print(f"[{args.group}] No BEST result found (likely all results had non-finite loss).")


if __name__ == "__main__":
    main()
