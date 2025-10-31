
# (File content abbreviated in this message — full content includes baseline,
# altruism (cooperation), and parasitism (imitation) modes, plus plotting.)
# See earlier cell for the complete header docs; this is the full runnable script.

import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import label, binary_dilation
from matplotlib.colors import LogNorm
from tqdm import tqdm

def update_grid(grid):
    padded_grid = np.pad(grid, 1, mode='wrap')
    neighbors = (padded_grid[1:-1, :-2] + padded_grid[1:-1, 2:] +
                 padded_grid[:-2, 1:-1] + padded_grid[2:, 1:-1] +
                 padded_grid[:-2, :-2] + padded_grid[:-2, 2:] +
                 padded_grid[2:, :-2] + padded_grid[2:, 2:])
    survivors = grid & ((neighbors == 2) | (neighbors == 3))
    births = ~grid & (neighbors == 3)
    return survivors | births

def analyze_actors(history_window, current_grid, min_mass=4):
    actor_metrics = []
    labeled_array, num_features = label(current_grid)
    if num_features == 0:
        return actor_metrics, labeled_array
    start_grid = history_window[0]
    for actor_id in range(1, num_features + 1):
        mask = (labeled_array == actor_id)
        mass_end = int(np.sum(mask))
        mass_start = int(np.sum(start_grid[mask]))
        if mass_start < min_mass: continue
        churn = 0
        for step in range(len(history_window) - 1):
            changes = np.abs(history_window[step+1] - history_window[step])
            churn += int(np.sum(changes[mask]))
        perf = (mass_end - mass_start) / (mass_start + 1e-9)
        kappa = churn / (len(history_window) * (mass_start + 1e-9))
        actor_metrics.append({
            "actor_id": actor_id, "mass": mass_end,
            "performance": float(np.clip(perf, -2, 2)),
            "kappa": float(np.clip(kappa, 0, 2))
        })
    return actor_metrics, labeled_array

def quadrant_of(kappa, perf, k_med=0.0):
    if perf > 0 and kappa < k_med: return "Weaver"
    if perf > 0 and kappa >= k_med: return "Gladiator"
    if perf <= 0 and kappa < k_med: return "Drifter"
    return "Vortex"

def altruism_bridge(grid, labeled_array, p=0.15, max_bridges=50, rng=None):
    if rng is None: rng = np.random.default_rng()
    if labeled_array.max() < 2: return grid
    new_grid = grid.copy()
    dil = binary_dilation(labeled_array>0, structure=np.ones((3,3)))
    touching = np.where(dil & (~(labeled_array>0)))
    coords = list(zip(touching[0], touching[1]))
    rng.shuffle(coords)
    placed = 0
    for r,c in coords:
        if placed >= max_bridges: break
        if rng.random() < p:
            new_grid[r, c] = 1
            placed += 1
    return new_grid

def parasitic_imitation(grid, metrics, labeled_array, p=0.15, rng=None):
    if rng is None: rng = np.random.default_rng()
    new_grid = grid.copy()
    if not metrics: return new_grid
    order = np.argsort([-m["performance"] for m in metrics])
    top_ids = [metrics[i]["actor_id"] for i in order[:max(1, len(metrics)//4)]]
    bot_ids = [metrics[i]["actor_id"] for i in order[-max(1, len(metrics)//3):]]
    for b in bot_ids:
        d = np.random.choice(top_ids)
        dmask = (labeled_array == d)
        edge = dmask ^ binary_dilation(dmask, structure=np.ones((3,3)))
        coords = np.array(np.where(edge)).T
        if len(coords) == 0: 
            continue
        take = coords[np.random.choice(len(coords), size=max(3, len(coords)//20), replace=False)]
        for (r,c) in take:
            rr = (r + np.random.randint(-2,3)) % grid.shape[0]
            cc = (c + np.random.randint(-2,3)) % grid.shape[1]
            if np.random.rand() < p:
                new_grid[rr, cc] = 1
    return new_grid

def scatter_phase(metrics, title, fname):
    if not metrics: return
    kappas = [m["kappa"] for m in metrics]
    perfs = [m["performance"] for m in metrics]
    masses = [m["mass"] for m in metrics]
    k_med = float(np.nanmedian(kappas)) if kappas else 0.0
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 8))
    sc = ax.scatter(perfs, kappas, c=masses, s=(np.array(masses)*1.5 + 10),
                    cmap="viridis", norm=LogNorm(), alpha=0.8, edgecolors="none")
    ax.axhline(0, ls="--", c="grey", lw=1)
    ax.axvline(0, ls="--", c="grey", lw=1)
    ax.axhline(k_med, ls=":", c="grey", lw=1, alpha=0.6)
    ax.set_xlabel("Performance (net mass change)")
    ax.set_ylabel("Intrinsic κ (churn/mass)")
    ax.set_title(title)
    cbar = plt.colorbar(sc); cbar.set_label("Actor mass (cells)")
    fig.tight_layout(); fig.savefig(fname, dpi=160, bbox_inches="tight"); plt.close(fig)

def run(mode="baseline", grid_size=100, steps=300, density=0.35, window=50,
        selection=None, coop_p=0.15, imit_p=0.15, seed=7, out_prefix="/mnt/data/exp"):
    rng = np.random.default_rng(seed)
    grid = rng.random((grid_size, grid_size)) < density
    history = [grid.copy()]
    all_metrics = []
    for t in tqdm(range(steps), desc=f"Running {mode}"):
        grid = update_grid(grid)
        if t % window == 0 and t > 0:
            metrics, labeled = analyze_actors(history, grid)
            if metrics:
                all_metrics.extend(metrics)
                if selection is not None:
                    perfs = {m["actor_id"]: m["performance"] for m in metrics}
                    for aid in range(1, labeled.max()+1):
                        if perfs.get(aid, selection+1) < selection:
                            grid[labeled == aid] = 0
            if mode == "altruism":
                grid = altruism_bridge(grid, labeled, p=coop_p)
            elif mode == "parasitism":
                grid = parasitic_imitation(grid, metrics, labeled, p=imit_p)
            history = [grid.copy()]
        else:
            history.append(grid.copy())
            if len(history) > window:
                history.pop(0)
    metrics, labeled = analyze_actors(history, grid)
    all_metrics.extend(metrics)
    if not all_metrics:
        return None, None
    df = pd.DataFrame(all_metrics)
    k_med = df["kappa"].median()
    df["quadrant"] = ["Weaver" if (p>0 and k<k_med) else
                      "Gladiator" if (p>0 and k>=k_med) else
                      "Drifter" if (p<=0 and k<k_med) else
                      "Vortex" for k,p in zip(df["kappa"], df["performance"])]
    summary = df["quadrant"].value_counts().sort_index()
    title = f"{mode.title()} mode (selection={selection})"
    fig_path = f"{out_prefix}_{mode}_phase.png"
    csv_path = f"{out_prefix}_{mode}_metrics.csv"
    scatter_phase(all_metrics, title, fig_path)
    df.to_csv(csv_path, index=False)
    return summary, (fig_path, csv_path)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["baseline","altruism","parasitism"], default="baseline")
    ap.add_argument("--grid_size", type=int, default=100)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--density", type=float, default=0.35)
    ap.add_argument("--window", type=int, default=50)
    ap.add_argument("--selection", type=float, default=None)
    ap.add_argument("--coop_p", type=float, default=0.15)
    ap.add_argument("--imit_p", type=float, default=0.15)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out_prefix", type=str, default="")
    args = ap.parse_args()
    summary, paths = run(**vars(args))
    if summary is None:
        print("No metrics produced.")
    else:
        print("Archetype counts:\n", summary.to_string())
        print("Outputs:", paths)

if __name__ == "__main__":
    main()

