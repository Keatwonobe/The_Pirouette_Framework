import numpy as np
import igraph as ig

# --- SCRIPT CONFIGURATION ---
FNAME = "higgs_hodge_out.npz"

# 1. Load the pre-computed Hodge decomposition data
print(f"Loading data from {FNAME}...")
data = np.load(FNAME, allow_pickle=True)
edges = data['edges']
grad_part = data['grad']
curl_part = data['curl']
m = len(edges)

# 2. Rebuild the graph using the high-performance igraph library
print("Rebuilding graph using igraph...")
G = ig.Graph.TupleList(edges, directed=True)

# 3. Find the largest connected component
print("Finding largest connected component...")
giant_component = G.components(mode='weak').giant()

degrees = giant_component.degree()
root_vertex_index_local = np.argmax(degrees)
root_vertex_id = giant_component.vs[root_vertex_index_local]['name']
print(f"Found central root user {root_vertex_id} with degree {max(degrees)}")

# 4. Compute graph distances from the central root user
print("Calculating shortest path lengths...")
# FIX: Updated to use the recommended .distances() method
distances = giant_component.distances(source=root_vertex_id, mode='all')[0]

# 5. Calculate the radius for each edge
print("Mapping distances and calculating radii...")
node_id_to_distance = {v['name']: dist for v, dist in zip(giant_component.vs, distances)}

radii = np.zeros(m)
for e_idx, (u, v) in enumerate(edges):
    du = node_id_to_distance.get(u, np.inf)
    dv = node_id_to_distance.get(v, np.inf)
    radii[e_idx] = max(du, dv)

# 6. Bin data by radius and calculate metrics
print("Binning data by radius and calculating final metrics...")
max_r = int(np.nanmax(radii[np.isfinite(radii)]))
theta_by_r, grad_by_r = [], []

for rbin in range(max_r + 1):
    mask = (radii == rbin)
    if not np.any(mask):
        theta_by_r.append(np.nan)
        grad_by_r.append(np.nan)
        continue
    theta_by_r.append(np.mean(curl_part[mask]**2))
    grad_by_r.append(np.mean(grad_part[mask]**2))

theta_by_r = np.array(theta_by_r)
grad_by_r = np.array(grad_by_r)

# --- MODIFIED CRITICAL RADIUS LOGIC (FIX) ---
# 7. Find r_c where the curl energy (Theta) is at its maximum.
# This is a more robust way to find the most relevant "cascade" region.
r_c = np.nanargmax(theta_by_r)

# 8. Compute final Pirouette Framework metrics
k_Gamma = 1.0
Theta = theta_by_r[r_c]
Theta_c = k_Gamma * grad_by_r[r_c]

print("\n--- FINAL RESULTS ---")
print(f"Critical Radius (r_c) = {r_c} (Radius of max curl energy)")
print(f"Theta at r_c          = {Theta:.6f}")
print(f"Theta_c (critical)    = {Theta_c:.6f}")
print(f"Cascade Condition Met?  {Theta > Theta_c}")