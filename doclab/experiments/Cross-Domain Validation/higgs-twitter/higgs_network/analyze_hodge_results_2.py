import numpy as np
import igraph as ig

FNAME = "higgs_hodge_out.npz"
EPS = 1e-12

print(f"Loading data from {FNAME}...")
data = np.load(FNAME, allow_pickle=True)

# 1) pull arrays
edges_raw = data["edges"]
grad_part = data["grad"]
curl_part = data["curl"]

# 2) *** KEY: normalize edge endpoints to strings ***
#    this makes them match igraph's 'name' attribute
edges = [(str(u), str(v)) for (u, v) in edges_raw]

print("Rebuilding graph using igraph...")
G = ig.Graph.TupleList(edges, directed=True, vertex_name_attr="name")

print(f"Total vertices in full graph: {len(G.vs)}")
print(f"Total edges in full graph:    {len(G.es)}")

print("Finding largest connected component (weak)...")
giant = G.components(mode="weak").giant()
print(f"Giant component vertices: {len(giant.vs)}")
print(f"Giant component edges:    {len(giant.es)}")

# 3) pick hub in THIS component
degrees = giant.degree()
root_local_idx = int(np.argmax(degrees))
root_name = giant.vs[root_local_idx]["name"]
print(f"Found central root user {root_name} with degree {degrees[root_local_idx]}")

# 4) *** KEY: undirected distances for geometry ***
giant_undirected = giant.as_undirected(combine_edges="first")

print("Calculating shortest path lengths...")
dists_from_root = giant_undirected.distances(source=root_local_idx)[0]

# map name -> distance (all strings!)
name_to_dist = {v["name"]: d for v, d in zip(giant_undirected.vs, dists_from_root)}

max_dist_seen = int(np.max(dists_from_root))
print(f"Max distance from root inside giant (undirected): {max_dist_seen}")

print("Mapping distances and calculating radii...")
radii = np.zeros(len(edges), dtype=float)
for i, (u, v) in enumerate(edges):
    du = name_to_dist.get(u, np.inf)  # u, v are strings now
    dv = name_to_dist.get(v, np.inf)
    radii[i] = max(du, dv)

finite_mask = np.isfinite(radii)
finite_r = radii[finite_mask]
finite_grad = grad_part[finite_mask]
finite_curl = curl_part[finite_mask]

if finite_r.size == 0:
    raise RuntimeError("No edges mapped to finite radii – check ID normalization.")

max_r = int(np.max(finite_r))

theta_mean = []
grad_mean = []
ratio = []

print("Binning data by radius and calculating final metrics...")
for r in range(max_r + 1):
    mask = (finite_r == r)
    if not np.any(mask):
        theta_mean.append(np.nan)
        grad_mean.append(np.nan)
        ratio.append(0.0)
        continue

    curl_energy = (finite_curl[mask] ** 2)
    grad_energy = (finite_grad[mask] ** 2)

    th_m = float(np.mean(curl_energy))
    gr_m = float(np.mean(grad_energy))
    # dominance
    dom = float(np.sum(curl_energy) / (np.sum(grad_energy) + EPS))

    theta_mean.append(th_m)
    grad_mean.append(gr_m)
    ratio.append(dom)

theta_mean = np.array(theta_mean)
grad_mean = np.array(grad_mean)
ratio = np.array(ratio)

# *** skip r=0 to avoid trivial win ***
if max_r >= 1:
    r_candidates = np.arange(1, max_r + 1)
    # note: ratio[1:] aligns with r_candidates
    winner_pos = int(np.nanargmax(ratio[1:]))
    r_c = int(r_candidates[winner_pos])
else:
    r_c = 0

Theta = theta_mean[r_c]
Theta_c = grad_mean[r_c]
cascade = ratio[r_c] > 1.0  # adjust to taste

print("\n--- PER-RADIUS DIAGNOSTIC (r, mean_curl, mean_grad, ratio) ---")
for r in range(max_r + 1):
    print(f"{r:3d}: {theta_mean[r]:.6e}  {grad_mean[r]:.6e}  ratio={ratio[r]:.6e}")

print("\n--- FINAL RESULTS ---")
print(f"Critical Radius (r_c) = {r_c}")
print(f"Theta at r_c          = {Theta:.6f}")
print(f"Theta_c (critical)    = {Theta_c:.6f}")
print(f"Dominance ratio       = {ratio[r_c]:.6f}")
print(f"Cascade Condition Met?  {cascade}")
