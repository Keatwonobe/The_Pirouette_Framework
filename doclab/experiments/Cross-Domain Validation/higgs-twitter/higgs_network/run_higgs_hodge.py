import gzip
import pandas as pd
import networkx as nx
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve, cg, LinearOperator

# 1) Load the temporal activity
# Format from SNAP: userA userB timestamp interaction
# interaction in {RT, MT, RE}
def load_activity(path, t_min=None, t_max=None):
    rows = []
    with gzip.open(path, 'rt') as f:
        for line in f:
            a, b, ts, itype = line.strip().split()
            ts = int(ts)
            if (t_min is not None and ts < t_min) or (t_max is not None and ts > t_max):
                continue
            rows.append((int(a), int(b), ts, itype))
    return pd.DataFrame(rows, columns=["src", "dst", "ts", "itype"])

# choose a tight window around the announcement to make it manageable
# announcement was 2012-07-04 08:00 GMT → in dataset seconds; we'll just narrow to that day
df = load_activity("higgs-activity_time.txt.gz",
                   t_min=1341360000,  # ~July 4, 2012 00:00
                   t_max=1341446400)  # ~July 5, 2012 00:00

# 2) Build a directed multigraph of actual info flow
# SNAP note says: if you care about info flow, reverse RT direction.
# So: info goes FROM "dst" TO "src"
G = nx.DiGraph()
for _, row in df.iterrows():
    u = row["dst"]  # original author
    v = row["src"]  # person who echoed it
    w = 1.0
    if G.has_edge(u, v):
        G[u][v]["weight"] += w
    else:
        G.add_edge(u, v, weight=w)

print("nodes:", G.number_of_nodes(), "edges:", G.number_of_edges())

# 3) Observed flow J_obs: just take edge weights as flux
edges = list(G.edges())
m = len(edges)
n = G.number_of_nodes()
node_index = {node: i for i, node in enumerate(G.nodes())}

# incidence matrix B (n x m): for each edge e = (i->j), B[i,e] = -1, B[j,e] = +1
rows_i = []
cols_j = []
data = []
for e_idx, (i, j) in enumerate(edges):
    rows_i.append(node_index[i]); cols_j.append(e_idx); data.append(-1.0)
    rows_i.append(node_index[j]); cols_j.append(e_idx); data.append(+1.0)
B = sparse.coo_matrix((data, (rows_i, cols_j)), shape=(n, m)).tocsr()

# observed edge flow as vector (m,)
J_obs = np.array([G[u][v]["weight"] for (u, v) in edges], dtype=float)

from scipy.sparse.linalg import cg, LinearOperator

# --- The Solution: Avoid forming L_edge explicitly ---

# 4) Compute "optimal" flow J_opt using an iterative solver.
# We need to solve (M_inv + B.T @ B) J = J_obs without building the huge
# B.T @ B matrix. We can do this by defining a function that calculates
# the matrix-vector product and passing it to an iterative solver.

# Define Gamma first, so it's available to the function below.
Gamma = np.ones(m)

def L_edge_matvec(v):
    """Calculates the matrix-vector product for L_edge @ v."""
    # First term: M_inv @ v. Since M_inv is diagonal, this is just element-wise multiplication.
    part1 = (1.0 / Gamma) * v
    # Second term: B.T @ (B @ v). This is done in two steps to stay efficient.
    part2 = B.T @ (B @ v)
    return part1 + part2

# Create a LinearOperator that represents L_edge without storing it.
# The shape is (m, m) where m is the number of edges.
L_edge_op = LinearOperator((m, m), matvec=L_edge_matvec)

# Now, solve the system using the Conjugate Gradient (cg) iterative solver.
# It returns the solution vector and an exit code (info).
print("Solving for J_opt using iterative solver (cg)...")
J_opt, info = cg(L_edge_op, J_obs) # Added a tolerance for faster convergence

if info != 0:
    print(f"Warning: Conjugate Gradient solver did not converge fully. Info code: {info}")
else:
    print("Solver converged successfully.")

# 5) Residual r
r = J_obs - J_opt

# 6) Hodge: grad component is B^T φ solving (B B^T) φ = B r
# The node Laplacian BBt is singular. We regularize it by adding a small
# value to the diagonal to make it invertible and find a stable solution.
BBt = B @ B.T
epsilon = 1e-9  # Small regularization parameter
BBt_reg = BBt + sparse.eye(n) * epsilon

# Solve the regularized system
phi = spsolve(BBt_reg.tocsr(), B @ r)
grad_part = B.T @ phi

# 7) curl part = r - grad_part
curl_part = r - grad_part

# We now have: r = grad_part + curl_part  (ignoring harmonic for now)
# Save to disk for later analysis
np.savez("higgs_hodge_out.npz",
         edges=np.array(edges, dtype=object),
         J_obs=J_obs,
         J_opt=J_opt,
         r=r,
         grad=grad_part,
         curl=curl_part)
print("done, wrote higgs_hodge_out.npz")

# --- Better root user selection (optional but recommended) ---
# Instead of the first tweeter, find a root user central to the giant component.
# We'll use the user with the highest total degree (in + out connections).

# First, get the largest connected component of the undirected version of G
G_undirected = G.to_undirected()
largest_cc_nodes = max(nx.connected_components(G_undirected), key=len)
G_main = G.subgraph(largest_cc_nodes)

# Find the node with the highest degree in this main component
degrees = dict(G_main.degree())
root_user = max(degrees, key=degrees.get)
print(f"Found new root user {root_user} with degree {degrees[root_user]}")

# Now compute graph distances FROM the new, more central root_user
# Note: This now uses the subgraph G_main
lengths = nx.single_source_shortest_path_length(G_main, root_user)
# make an array of radii per edge = max(dist(u), dist(v))
radii = np.zeros(m)
for e_idx, (u, v) in enumerate(edges):
    du = lengths.get(u, np.inf)
    dv = lengths.get(v, np.inf)
    radii[e_idx] = max(du, dv)

# magnitude of residual field
D_mag = np.abs(grad_part + curl_part)

# bin by radius
max_r = int(np.nanmax(radii[np.isfinite(radii)]))
theta_by_r = []
grad_by_r = []
A_by_r = []
for rbin in range(max_r + 1):
    mask = (radii == rbin)
    if not np.any(mask):
        theta_by_r.append(np.nan); grad_by_r.append(np.nan); A_by_r.append(np.nan)
        continue
    curl_loc = curl_part[mask]
    grad_loc = grad_part[mask]
    # in Pirouette terms: Θ = <|curl|^2>
    theta_by_r.append(np.mean(curl_loc**2))
    grad_by_r.append(np.mean(grad_loc**2))
    A_by_r.append(np.mean(np.abs(curl_loc)))  # proxy for |A|^2 denominator

theta_by_r = np.array(theta_by_r)
grad_by_r = np.array(grad_by_r)
A_by_r = np.array(A_by_r)

# find r_c where D decays fastest
D_by_r = []
for rbin in range(max_r + 1):
    mask = (radii == rbin)
    if np.any(mask):
        D_by_r.append(np.mean(D_mag[mask]))
    else:
        D_by_r.append(np.nan)
D_by_r = np.array(D_by_r)

# discrete derivative
dD = np.diff(D_by_r)
r_c = np.nanargmin(dD)  # steepest drop

# now compute Θ and Θ_c in ring around r_c
k_Gamma = 1.0  # <- THIS is the thing we will try to match across domains
num = grad_by_r[r_c] if not np.isnan(grad_by_r[r_c]) else 0.0
den = (A_by_r[r_c]**2) if not np.isnan(A_by_r[r_c]) else 1.0
Theta_c = k_Gamma * num / den
Theta = theta_by_r[r_c]

print("r_c =", r_c)
print("Theta =", Theta)
print("Theta_c =", Theta_c)
print("cascade?", Theta > Theta_c)
