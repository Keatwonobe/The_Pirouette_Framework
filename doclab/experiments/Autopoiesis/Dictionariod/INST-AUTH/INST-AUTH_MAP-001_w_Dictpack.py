#!/usr/bin/env python3
"""
INST-AUTH-MAP-001 + dictpack pull
Idea Manifold Surveyor (language-weighted)
- load pirouette graph
- load dictpack (terms + rarity / weight)
- embed into (C,A,D) with lexical pressure
- detect undersampled cells
- emit YAML module stubs sensitive to rare/high-value vocab
"""

import os
import math
import json
import uuid
import ast
import networkx as nx
from collections import defaultdict, Counter
from datetime import datetime

import yaml  # needs pyyaml

# ---------------------------------------------------------------------------
# 1. config
# ---------------------------------------------------------------------------
GRAPH_PATH = "graph.gexf"
DICTPACK_PATH = "pirouette_dict.dictpack"
OUT_PHASE_JSON = "phase_space.json"
OUT_GAPS_JSON = "gaps.json"
OUT_STUBS_DIR = "gap_stubs"

os.makedirs(OUT_STUBS_DIR, exist_ok=True)

SIMPLE_DEGREE_THRESHOLD = 3
GRID_CELLS_C = 12
GRID_CELLS_A = 12
MIN_POINTS_PER_CELL = 1

# how strongly rare terms should *lower* accessibility and *raise* complexity
LEX_COMPLEXITY_GAIN = 0.35
LEX_ACCESSIBILITY_LOSS = 0.25

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

def cell_index(x, cells):
    ix = int(x * cells)
    if ix == cells:
        ix = cells - 1
    return ix

def domain_name_from_id(D):
    return {
        0: "MATH",
        1: "DYNA",
        2: "DOMA",
        3: "XXP",
        9: "MISC",
    }.get(D, f"DOM-{D}")

# ---------------------------------------------------------------------------
# 3. load dictpack (adaptive)
# ---------------------------------------------------------------------------
dictpack = {}
if os.path.exists(DICTPACK_PATH):
    # MODIFIED: Added errors="ignore" to handle potential encoding issues
    raw = open(DICTPACK_PATH, "r", encoding="utf-8", errors="ignore").read()
    loaded = None
    # try json
    try:
        loaded = json.loads(raw)
    except Exception:
        pass
    # try yaml
    if loaded is None:
        try:
            loaded = yaml.safe_load(raw)
        except Exception:
            pass
    # try python literal
    if loaded is None:
        try:
            loaded = ast.literal_eval(raw)
        except Exception:
            pass
    if isinstance(loaded, dict):
        dictpack = loaded
        print(f"[info] loaded dictpack with {len(dictpack)} entries.")
    else:
        print("[warn] could not interpret dictpack, continuing without lexical weighting.")
else:
    print("[warn] dictpack not found, continuing without lexical weighting.")

# Normalize dictpack into a uniform structure:
# wanted: {term: {"weight": float, "rarity": float, "tags": [...]} }
normalized_dictpack = {}
if dictpack:
    for k, v in dictpack.items():
        # if simple form: "term": 1.0
        if isinstance(v, (int, float)):
            normalized_dictpack[k.lower()] = {
                "weight": float(v),
                "rarity": 1.0 / (1.0 + float(v)),  # very crude
                "tags": []
            }
        elif isinstance(v, dict):
            w = float(v.get("weight", 1.0))
            r = float(v.get("rarity", 1.0 / (1.0 + w)))
            tags = v.get("tags", [])
            normalized_dictpack[k.lower()] = {
                "weight": w,
                "rarity": r,
                "tags": tags,
            }
        else:
            normalized_dictpack[k.lower()] = {
                "weight": 1.0,
                "rarity": 0.5,
                "tags": []
            }
else:
    normalized_dictpack = {}

# ---------------------------------------------------------------------------
# 4. load graph
# ---------------------------------------------------------------------------
if not os.path.exists(GRAPH_PATH):
    raise SystemExit(f"Graph file not found: {GRAPH_PATH}")

G = nx.read_gexf(GRAPH_PATH)
nodes = list(G.nodes)
print(f"[info] loaded graph with {len(nodes)} nodes and {G.number_of_edges()} edges.")

# identify simple nodes for accessibility baseline
simple_nodes = [n for n in nodes if G.degree(n) <= SIMPLE_DEGREE_THRESHOLD]
if not simple_nodes:
    simple_nodes = sorted(nodes, key=lambda n: G.degree(n))[:max(3, len(nodes)//20)]

phase_records = []

# ---------------------------------------------------------------------------
# 5. per-node feature derivation (now lexical-aware)
# ---------------------------------------------------------------------------
for n in nodes:
    deg = G.degree(n)
    C_raw = math.log1p(deg)

    # accessibility by graph distance to simple nodes
    dists = []
    for s in simple_nodes:
        try:
            d = nx.shortest_path_length(G, n, s)
        except nx.NetworkXNoPath:
            d = None
        dists.append(d)
    mean_dist = safe_mean([d for d in dists if d is not None], default=10.0)
    A_raw = 1.0 / (1.0 + mean_dist)

    # domain from attribute or label
    dom = G.nodes[n].get("domain", None)
    label = str(G.nodes[n].get("label", n))
    if dom is None:
        UL = label.upper()
        if UL.startswith("MATH"):
            dom = 0
        elif UL.startswith("DYNA"):
            dom = 1
        elif UL.startswith("DOMA"):
            dom = 2
        elif UL.startswith("XXP"):
            dom = 3
        else:
            dom = 9

    # NEW: lexical pull
    # try to get any text associated with node
    node_text_fields = []
    for key in ("summary", "description", "text", "body"):
        if key in G.nodes[n]:
            node_text_fields.append(str(G.nodes[n][key]))
    # we also use the label
    node_text_fields.append(label)
    node_text = " ".join(node_text_fields).lower()

    lex_terms = node_text.split()
    # count overlap with dictpack
    overlap = [t for t in lex_terms if t in normalized_dictpack]
    if overlap:
        # score rare / high weight terms more
        rare_score = 0.0
        for t in overlap:
            info = normalized_dictpack[t]
            # rarity high -> term is special
            rare_score += info["rarity"] * info["weight"]
        # normalize by number of terms to avoid runaway
        if lex_terms:
            rare_score = rare_score / len(lex_terms)
        else:
            rare_score = 0.0


        # apply to complexity and accessibility
        C_raw = C_raw + LEX_COMPLEXITY_GAIN * rare_score
        A_raw = max(0.0, A_raw - LEX_ACCESSIBILITY_LOSS * rare_score)

    phase_records.append(
        {
            "id": n,
            "degree": deg,
            "C_raw": C_raw,
            "A_raw": A_raw,
            "D": dom,
            "label": label,
            "parents": list(G.predecessors(n)),
            "children": list(G.successors(n)),
            "lex_overlap": overlap,
        }
    )

# ---------------------------------------------------------------------------
# 6. normalize to [0,1] and grid
# ---------------------------------------------------------------------------
C_vals = [r["C_raw"] for r in phase_records]
A_vals = [r["A_raw"] for r in phase_records]
C_norm, C_lo, C_hi = norm01(C_vals)
A_norm, A_lo, A_hi = norm01(A_vals)

for r, c, a in zip(phase_records, C_norm, A_norm):
    r["C"] = c
    r["A"] = a

grid = defaultdict(list)
for r in phase_records:
    cix = cell_index(r["C"], GRID_CELLS_C)
    aix = cell_index(r["A"], GRID_CELLS_A)
    key = (r["D"], cix, aix)
    grid[key].append(r["id"])

# ---------------------------------------------------------------------------
# 7. gap detection (same as before)
# ---------------------------------------------------------------------------
gaps = []
domains_present = set(r["D"] for r in phase_records)

for D in domains_present:
    for cix in range(GRID_CELLS_C):
        for aix in range(GRID_CELLS_A):
            key = (D, cix, aix)
            if key in grid and len(grid[key]) >= MIN_POINTS_PER_CELL:
                continue
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
                gaps.append(
                    {
                        "domain": D,
                        "cix": cix,
                        "aix": aix,
                        "neighbors": neighbors_filled,
                    }
                )

print(f"[info] detected {len(gaps)} candidate gaps (lex-weighted).")

# ---------------------------------------------------------------------------
# 8. emit stubs (now with lexical suggestions)
# ---------------------------------------------------------------------------
stub_paths = []

for g in gaps:
    D = g["domain"]
    dn = domain_name_from_id(D)
    c_center = (g["cix"] + 0.5) / GRID_CELLS_C
    a_center = (g["aix"] + 0.5) / GRID_CELLS_A

    same_domain = [r for r in phase_records if r["D"] == D]

    def dist2(r):
        return (r["C"] - c_center) ** 2 + (r["A"] - a_center) ** 2
    
    # Handle case where same_domain might be empty
    if not same_domain:
        print(f"[warn] No nodes found in domain {dn} to find nearest neighbors for gap.")
        continue

    nearest = sorted(same_domain, key=dist2)[:3]
    stub_id = f"BRG-{dn}-{uuid.uuid4().hex[:6].upper()}"
    filename = os.path.join(OUT_STUBS_DIR, stub_id + ".yaml")

    parents = [n["id"] for n in nearest]

    # collect lexical hints from nearest nodes
    lex_counter = Counter()
    for n in nearest:
        for term in n.get("lex_overlap", []):
            lex_counter[term] += 1
    # pick top 5 to suggest continuity of language
    lex_suggestions = [t for t, _ in lex_counter.most_common(5)]

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
            "Auto-generated gap-filling module derived from lexically weighted manifold. "
            "Bridges nearby nodes in the same domain to restore continuity in (complexity, accessibility) space, "
            "preserving local Pirouette vocabulary."
        ),
        "referee_mode": "low-pirouette",
        "recommended_vocabulary": lex_suggestions,
        "notes": [
            "Use the recommended_vocabulary terms to maintain resonance with adjacent modules.",
            "State the shared geometric / temporal quantity without naming the Pirouette framework.",
            "Offer either a worked example OR a two-sided introduction (from A to B) depending on referee sensitivity."
        ],
    }

    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(stub, f, sort_keys=False, allow_unicode=True)

    stub_paths.append(filename)

print(f"[info] wrote {len(stub_paths)} lexically-aware stub modules to {OUT_STUBS_DIR}/")

# ---------------------------------------------------------------------------
# 9. write phase & gaps
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

print("[done] phase-space + gaps (lexical) emitted.")
