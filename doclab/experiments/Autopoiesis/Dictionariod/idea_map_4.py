#!/usr/bin/env python3
"""
idea_map_4.py
Generate a graph from Pirouette dictionary .md entries for visualization.

- Parses markdown files for YAML frontmatter and body text.
- Cleans and validates data.
- Builds a graph with nodes representing terms.
- Creates edges based on:
  1. Structural links (parents/children).
  2. Textual similarity (TF-IDF + Cosine Similarity).
- Saves graph data as JSON files (nodes, edges) and a GEXF file for Gephi.
- Includes checkpointing to resume long-running calculations.

Usage:
  python idea_map_4.py --dict ./dictionary --out ./ideamap
"""
import argparse
import re
import textwrap
import keyword
import string
import json
from pathlib import Path
from datetime import datetime
import yaml
from typing import List, Dict, Any, Tuple
from collections import defaultdict
import logging

# Use scikit-learn for fast text analysis
# pip install scikit-learn numpy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.INFO, format='  %(levelname)-7s: %(message)s')
log = logging.getLogger()

# --- Configuration ---
TFIDF_TOPK = 25
TFIDF_THRESH = 0.01
TFIDF_MINDF = 2
TFIDF_MAXDF = 0.85

# --- Helpers ---
CID_OK = set(string.ascii_uppercase + string.digits + "_")

def read(fp: Path) -> str:
    return fp.read_text(encoding="utf-8")

def parse_frontmatter_and_body(raw: str, filepath: Path) -> Tuple[Dict[str, Any], str]:
    if not raw.startswith("---"):
        return {}, raw

    try:
        _, rest = raw.split("\n", 1)
        fm_raw, body = rest.split("---", 1)
        # Attempt to fix common YAML errors before parsing
        fixed_fm_raw = fm_raw
        if '"' in fm_raw and '\\' in fm_raw:
            # Simple fix: if a line has double quotes and backslashes, try single quotes
            lines = fm_raw.splitlines()
            fixed_lines = []
            for line in lines:
                if line.strip().startswith("symbol:") and '"' in line and '\\' in line:
                    parts = line.split(':', 1)
                    val = parts[1].strip().strip('"')
                    fixed_lines.append(f"{parts[0]}: '{val}'")
                else:
                    fixed_lines.append(line)
            fixed_fm_raw = "\n".join(fixed_lines)
        
        # Another common fix for lists with special characters
        fixed_fm_raw = re.sub(r'(\[\s*)([>])', r"\1'\2", fixed_fm_raw)

        fm = yaml.safe_load(fixed_fm_raw) or {}
        return fm, body.lstrip("\n")
    except yaml.YAMLError as e:
        log.info(f"YAML parse failed for {filepath.name}, attempting fix. Error: {e}")
        # More aggressive fix for complex cases
        try:
            lines = fm_raw.splitlines()
            fixed_lines = []
            for line in lines:
                if re.search(r':\s*".*\\.*"', line):
                    parts = line.split(':', 1)
                    val = parts[1].strip().strip('"')
                    fixed_lines.append(f"{parts[0]}: '{val}'")
                elif re.search(r'\[.*>.*\]', line):
                     parts = line.split(':', 1)
                     val = parts[1].strip().strip('[]').strip()
                     if val and not val.startswith("'") and not val.startswith('"'):
                         fixed_lines.append(f"{parts[0]}: ['{val}']")
                     else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            fixed_fm_raw = "\n".join(fixed_lines)
            fm = yaml.safe_load(fixed_fm_raw) or {}
            log.info(f"...fix successful for {filepath.name}.")
            return fm, body.lstrip("\n")
        except yaml.YAMLError as e2:
            log.warning(f"Could not parse YAML for {filepath.name} after attempting fix. Error: {e2}")
            return {}, raw # Return raw on failure to avoid crash

def is_valid_cid(cid: str) -> bool:
    if not cid or len(cid) < 3: return False
    return all(ch in CID_OK for ch in cid)

def sanitize_cid_from_term(term: str) -> str:
    cid = re.sub(r"[^A-Za-z0-9]+", "_", (term or "").strip()).upper()
    cid = re.sub(r"_+", "_", cid).strip("_")
    return cid or f"TERM_{abs(hash(term)) % 100000:05d}"

def calculate_text_overlap_fast(nodes: dict, topk: int, min_df: int, max_df: float, thresh: float) -> dict:
    """Calculates all-pairs text overlap using a fast, vectorized approach."""
    log.info(f"TF-IDF: vectorizing {len(nodes)} documents...")
    cids = list(nodes.keys())
    # FIX: Use a list comprehension `[]` to create a list of strings, not a generator.
    texts = [nodes[cid].get("body", "") for cid in cids]

    vec = TfidfVectorizer(stop_words='english', min_df=min_df, max_df=max_df, norm='l2')
    X = vec.fit_transform(texts)

    log.info("TF-IDF: computing cosine similarity matrix...")
    sim_matrix = cosine_similarity(X)
    np.fill_diagonal(sim_matrix, 0) # Zero out self-similarity

    log.info("TF-IDF: building sparse edge list...")
    edges = {}
    for i in range(len(cids)):
        # Get the indices of the top-k similarities for the current node
        # We use argpartition which is faster than a full sort
        if sim_matrix[i].size > topk:
            top_indices = np.argpartition(sim_matrix[i], -topk)[-topk:]
        else:
            top_indices = np.arange(sim_matrix[i].size)

        for j in top_indices:
            if i >= j: continue # Avoid duplicates and self-loops
            
            score = sim_matrix[i, j]
            if score >= thresh:
                cid1, cid2 = cids[i], cids[j]
                edges[(cid1, cid2)] = score

    log.info(f"TF-IDF: kept {len(edges)} edges (topk per node = {topk} , thresh = {thresh} )")
    return edges


def build_graph(dict_dir: Path, out_dir: Path) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    nodes = {}
    edges = []
    
    log.info(f"Parsing {len(list(dict_dir.glob('*.md')))} dictionary files...")
    all_files = sorted(list(dict_dir.glob("*.md")))
    
    for fp in all_files:
        fm, body = parse_frontmatter_and_body(read(fp), fp)
        term = (fm.get("term") or fp.stem).strip()
        cid = (fm.get("canonical_id") or "").strip()

        if not cid or not is_valid_cid(cid):
            cid = sanitize_cid_from_term(term)

        if not term or not cid or not is_valid_cid(cid):
            log.warning(f"Skipping file with missing term/cid: {fp.name}")
            continue

        nodes[cid] = {
            "id": cid,
            "label": term,
            "symbol": fm.get("symbol", ""),
            "aliases": fm.get("aliases", []),
            "parents": fm.get("parents", []),
            "children": fm.get("children", []),
            "body": body,
            "file": fp.name
        }

    # --- Edge Calculation ---
    structural_edges = {}
    log.info("Calculating edge weights (structural)...")
    for cid, data in nodes.items():
        for p in data.get("parents", []):
            if p in nodes:
                # Ensure canonical edge direction (alphabetical)
                u, v = sorted((cid, p))
                structural_edges[(u, v)] = structural_edges.get((u, v), 0) + 1.0
        for c in data.get("children", []):
            if c in nodes:
                u, v = sorted((cid, c))
                structural_edges[(u, v)] = structural_edges.get((u, v), 0) + 1.0

    log.info("Calculating edge weights (text overlap)... this may take a while.")
    tfidf_edges = calculate_text_overlap_fast(nodes, topk=TFIDF_TOPK, min_df=TFIDF_MINDF, max_df=TFIDF_MAXDF, thresh=TFIDF_THRESH)

    # --- Combine Edges ---
    log.info("Combining and normalizing edge weights...")
    combined_edges = defaultdict(lambda: {'struct': 0.0, 'text': 0.0})
    for (u, v), w in structural_edges.items():
        combined_edges[(u, v)]['struct'] = w
    for (u, v), w in tfidf_edges.items():
        combined_edges[(u, v)]['text'] = w

    final_edges = []
    for (u, v), weights in combined_edges.items():
        # Simple weighted combination
        total_weight = weights['struct'] * 2.0 + weights['text'] * 1.0
        if total_weight > 0:
            final_edges.append({
                "source": u,
                "target": v,
                "weight": total_weight,
                "type": "undirected",
                "kind": "struct_and_text" if weights['struct'] > 0 and weights['text'] > 0 else "struct_only" if weights['struct'] > 0 else "text_only"
            })
            
    # Remove 'body' from final node output to keep JSON small
    for cid in nodes:
        del nodes[cid]['body']
        
    return nodes, final_edges

def save_to_json(nodes: Dict[str, Any], edges: List[Dict[str, Any]], out_dir: Path):
    log.info("Saving nodes.json and edges.json...")
    (out_dir / "nodes.json").write_text(json.dumps(list(nodes.values()), indent=2), encoding="utf-8")
    (out_dir / "edges.json").write_text(json.dumps(edges, indent=2), encoding="utf-8")

def save_to_gexf(nodes: Dict[str, Any], edges: List[Dict[str, Any]], out_dir: Path):
    log.info("Saving graph.gexf for Gephi...")
    gexf_header = """<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
    <meta lastmodifieddate="{date}">
        <creator>Pirouette Idea Map Generator</creator>
    </meta>
    <graph mode="static" defaultedgetype="undirected">
        <nodes>
""".format(date=datetime.now().strftime("%Y-%m-%d"))

    gexf_footer = """
        </nodes>
        <edges>
{edges_str}
        </edges>
    </graph>
</gexf>
"""
    nodes_str = []
    for cid, data in nodes.items():
        label = data['label'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        nodes_str.append(f'            <node id="{cid}" label="{label}" />')

    edges_str = []
    for i, edge in enumerate(edges):
        edges_str.append(
            f'            <edge id="{i}" source="{edge["source"]}" target="{edge["target"]}" weight="{edge["weight"]:.4f}" />'
        )

    full_gexf = gexf_header + "\n".join(nodes_str) + gexf_footer.format(edges_str="\n".join(edges_str))
    (out_dir / "graph.gexf").write_text(full_gexf, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate an idea map from the Pirouette dictionary.")
    parser.add_argument("--dict", required=True, help="Path to the dictionary directory.")
    parser.add_argument("--out", required=True, help="Path to the output directory.")
    args = parser.parse_args()

    dict_dir = Path(args.dict)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    nodes, edges = build_graph(dict_dir, out_dir)
    save_to_json(nodes, edges, out_dir)
    save_to_gexf(nodes, edges, out_dir)

    log.info(f"Graph generation complete. Output saved to '{out_dir.resolve()}'")
    log.info(f"  - Nodes: {len(nodes)}")
    log.info(f"  - Edges: {len(edges)}")
    log.info("You can now open 'graph.gexf' in Gephi.")

if __name__ == "__main__":
    main()