#!/usr/bin/env python3
"""
INST-AUTH-MAP-001 prototype
Idea Manifold Surveyor
- load pirouette graph
- embed into (C,A,D)
- detect undersampled cells
- emit YAML module stubs
"""

import os
import math
import json
import uuid
import networkx as nx
from collections import defaultdict
from datetime import datetime

# ---------------------------------------------------------------------------
# 1. config
# ---------------------------------------------------------------------------
GRAPH_PATH = "graph.gexf"              # your uploaded graph
DICTPACK_PATH = "pirouette_dict.dictpack"  # not parsed yet, placeholder
OUT_PHASE_JSON = "phase_space.json"
OUT_GAPS_JSON = "gaps.json"
OUT_STUBS_DIR = "gap_stubs"

os.makedirs(OUT_STUBS_DIR, exist_ok=True)

# “small” nodes we use to measure accessibility
SIMPLE_DEGREE_THRESHOLD = 3

# grid resolution for gap detection
GRID_CELLS_C = 12
GRID_CELLS_A = 12

# how many neighbors in grid-space we consider “filled enough”
MIN_POINTS_PER_CELL = 1


# ---------------------------------------------------------------------------
# 2. helpers
# ---------------------------------------------------------------------------
def safe_mean(xs, default=None):
    xs = [x for x in xs if x is not None]
    if not xs:
        return default
    return sum(xs) / len(xs)


def norm01(vals, eps=1e-9):
    lo = min(vals)
    hi = max(vals)
    span = (hi - lo) if (hi - lo) > eps else 1.0
    return [(v - lo) / span for v in vals], lo, hi


# ---------------------------------------------------------------------------
# 3. load graph
# ---------------------------------------------------------------------------
if not os.path.exists(GRAPH_PATH):
    raise SystemExit(f"Graph file not found: {GRAPH_PATH}")

G = nx.read_gexf(GRAPH_PATH)

nodes = list(G.nodes)
print(f"[info] loaded graph with {len(nodes)} nodes and {G.number_of_edges()} edges.")


# ---------------------------------------------------------------------------
# 4. derive raw features per node
# ---------------------------------------------------------------------------
# C: complexity -> log(1+degree)
# A: accessibility -> inverse shortest-path to simple nodes
# D: domain -> from attribute, else 0

# identify simple nodes
simple_nodes = [n for n in nodes if G.degree(n) <= SIMPLE_DEGREE_THRESHOLD]
if not simple_nodes:
    # fallback: pick smallest 5-degree nodes
    simple_nodes = sorted(nodes, key=lambda n: G.degree(n))[:max(3, len(nodes)//20)]

phase_records = []

for n in nodes:
    deg = G.degree(n)
    C_raw = math.log1p(deg)

    # accessibility: mean shortest path to simple nodes
    dists = []
    for s in simple_nodes:
        try:
            d = nx.shortest_path_length(G, n, s)
        except nx.NetworkXNoPath:
            d = None
        dists.append(d)
    mean_dist = safe_mean([d for d in dists if d is not None], default=10.0)
    A_raw = 1.0 / (1.0 + mean_dist)

    # domain: try to read from node; fall back to 0
    dom = G.nodes[n].get("domain", None)
    if dom is None:
        # try inference from label
        label = str(G.nodes[n].get("label", n)).upper()
        if label.startswith("MATH"):
            dom = 0
        elif label.startswith("DYNA"):
            dom = 1
        elif label.startswith("DOMA"):
            dom = 2
        elif label.startswith("XXP"):
            dom = 3
        else:
            dom = 9  # unknown / misc

    phase_records.append(
        {
            "id": n,
            "degree": deg,
            "C_raw": C_raw,
            "A_raw": A_raw,
            "D": dom,
            "label": G.nodes[n].get("label", str(n)),
            "parents": list(G.predecessors(n)),
            "children": list(G.successors(n)),
        }
    )

# normalize C and A to [0,1] for grid binning
C_vals = [r["C_raw"] for r in phase_records]
A_vals = [r["A_raw"] for r in phase_records]
C_norm, C_lo, C_hi = norm01(C_vals)
A_norm, A_lo, A_hi = norm01(A_vals)

for r, c, a in zip(phase_records, C_norm, A_norm):
    r["C"] = c
    r["A"] = a

# ---------------------------------------------------------------------------
# 5. bucket into grid per domain
# ---------------------------------------------------------------------------
# grid key: (D, c_idx, a_idx)
grid = defaultdict(list)

def cell_index(x, cells):
    # x in [0,1]
    ix = int(x * cells)
    if ix == cells:
        ix = cells - 1
    return ix

for r in phase_records:
    cix = cell_index(r["C"], GRID_CELLS_C)
    aix = cell_index(r["A"], GRID_CELLS_A)
    key = (r["D"], cix, aix)
    grid[key].append(r["id"])

# ---------------------------------------------------------------------------
# 6. detect gaps
# a gap = a cell with 0 nodes, but at least one Moore-neighbor cell nonempty
# ---------------------------------------------------------------------------
gaps = []
domains_present = set(r["D"] for r in phase_records)

for D in domains_present:
    for cix in range(GRID_CELLS_C):
        for aix in range(GRID_CELLS_A):
            key = (D, cix, aix)
            if key in grid and len(grid[key]) >= MIN_POINTS_PER_CELL:
                continue  # filled
            # check neighbors
            neighbors_filled = 0
            for dc in (-1, 0, 1):
                for da in (-1, 0, 1):
                    if dc == 0 and da == 0:
                        continue
                    nc = cix + dc
                    na = aix + da
                    if 0 <= nc < GRID_CELLS_C and 0 <= na < GRID_CELLS_A:
                        if (D, nc, na) in grid and len(grid[(D, nc, na)]) > 0:
                            neighbors_filled += 1
            if neighbors_filled > 0:
                # we found a hole near populated areas
                gaps.append(
                    {
                        "domain": D,
                        "cix": cix,
                        "aix": aix,
                        "neighbors": neighbors_filled,
                    }
                )

print(f"[info] detected {len(gaps)} candidate gaps.")

# ---------------------------------------------------------------------------
# 7. emit YAML stubs for each gap
# ---------------------------------------------------------------------------
def domain_name_from_id(D):
    return {
        0: "MATH",
        1: "DYNA",
        2: "DOMA",
        3: "XXP",
        9: "MISC",
    }.get(D, f"DOM-{D}")

stub_paths = []

for g in gaps:
    D = g["domain"]
    dn = domain_name_from_id(D)
    # coarse center of the cell in normalized space
    c_center = (g["cix"] + 0.5) / GRID_CELLS_C
    a_center = (g["aix"] + 0.5) / GRID_CELLS_A

    # pick nearest existing nodes in same domain to use as parents
    # (very simple metric: euclidean in (C,A))
    same_domain = [r for r in phase_records if r["D"] == D]
    def dist2(r):
        return (r["C"] - c_center) ** 2 + (r["A"] - a_center) ** 2
    nearest = sorted(same_domain, key=dist2)[:3]

    stub_id = f"BRG-{dn}-{uuid.uuid4().hex[:6].upper()}"
    filename = os.path.join(OUT_STUBS_DIR, stub_id + ".yaml")

    parents = [n["id"] for n in nearest]

    stub = {
        "id": stub_id,
        "title": f"Interpolant for {dn} at ({c_center:.2f},{a_center:.2f})",
        "version": "0.1",
        "status": "draft",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "domain": dn,
        "parents": parents,
        "children": [],
        "summary": (
            "Auto-generated gap-filling module. Sits between nearby nodes in the same domain to restore "
            "manifold continuity in (complexity, accessibility) space."
        ),
        "referee_mode": "low-pirouette",
        "notes": [
            "Introduce concept using vocabulary from parents.",
            "State the shared geometric / temporal quantity without naming the Pirouette framework.",
            "Offer a worked example or parameterization to justify the bridge."
        ],
    }

    import yaml  # pyyaml

    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(stub, f, sort_keys=False, allow_unicode=True)

    stub_paths.append(filename)

print(f"[info] wrote {len(stub_paths)} stub modules to {OUT_STUBS_DIR}/")

# ---------------------------------------------------------------------------
# 8. write phase space
# ---------------------------------------------------------------------------
with open(OUT_PHASE_JSON, "w", encoding="utf-8") as f:
    json.dump(
        {
            "C_range": [C_lo, C_hi],
            "A_range": [A_lo, A_hi],
            "nodes": phase_records,
        },
        f,
        indent=2,
    )

with open(OUT_GAPS_JSON, "w", encoding="utf-8") as f:
    json.dump(gaps, f, indent=2)

print("[done] phase-space + gaps emitted.")
