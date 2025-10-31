#!/usr/bin/env python3
"""
idea_map.py
Build an "idea map" (concept graph) from Pirouette dictionary entries.

Inputs:
  ./dictionary/*.md  (frontmatter + body)

Outputs (in ./ideamap/):
  - nodes.csv                 # id,cid,term,symbol,aliases,residue,degree,cluster
  - edges.csv                 # source,target,weight,type
  - idea_map.gexf             # for Gephi/Cytoscape (if networkx present)
  - idea_map.json             # summary (nodes/edges stats + cluster sizes)
  - idea_map_d3.html          # standalone D3 force-graph (no server needed)
  - progress_checkpoint.json  # Resumable checkpoint for edges and progress

Weights:
  +1.00 parent/child (bidirectional)
  +0.60 "next inquiry" / downstream_effects / explicit Next sections
  +0.50 crosslinks [CID] in body
  +0.25 alias overlap (shared alias)
  +0.20 symbol overlap (same frontmatter symbol)
  +0.10 text overlap (ONLY if both bodies share ≥3 rare tokens; no sklearn needed)

Residue signal:
  Heuristic in-body detectors (“What doesn’t (yet) fit”, “Residue”, “Gaps”, etc.) raise node 'residue'.
  We DO NOT multiply edge weights by residue (keeps topology honest), but we export the score for styling.

Deps:
  - PyYAML  (required)
  - networkx (optional; enables GEXF + modularity clustering; otherwise fallback clustering)

Usage:
  python idea_map.py --dict ./dictionary --out ./ideamap
"""

import re, json, argparse, math, time, os
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

try:
    import yaml
except Exception as e:
    raise SystemExit("Please `pip install pyyaml`")

try:
    import networkx as nx
    HAS_NX = True
except Exception:
    HAS_NX = False

R_CROSSLINK = re.compile(r"\[([A-Z0-9_]{3,})\]")
R_RESIDUE_HEAD = re.compile(r"^(#+\s+)(?:(?:What\s+doesn'?t(?:\s+\(yet\))?)|Residue|Gaps|Open\s+Questions)\b", re.I | re.M)
R_NEXT_HEAD = re.compile(r"^(#+\s+)(?:The\s+residue\s+points\s+toward|Next\s+Inquiry|Next\s+Step|Where\s+to\s+next)\b", re.I|re.M)
TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_]{2,}")

def read(p: Path) -> str: return p.read_text(encoding="utf-8")

def canon_id(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", s.strip())
    return re.sub(r"_+","_", s).strip("_").upper()

def parse_frontmatter_and_body(text: str, filepath: Path):
    if not text.startswith("---"):
        return {}, text
    try:
        _, rest = text.split("\n", 1)
        fm_raw, body = rest.split("---", 1)
    except ValueError:
        print(f"  WARNING: Malformed frontmatter delimiter in file: {filepath.name}")
        return {}, text
    try:
        fm = yaml.safe_load(fm_raw) or {}
        return fm, body.lstrip("\n")
    except (yaml.YAMLError, ValueError) as e:
        print(f"  WARNING: Could not parse YAML frontmatter in file: {filepath.name}. Error: {e}")
        # Fallback to naive key:value parsing on error
        fm_min = {}
        for line in fm_raw.splitlines():
            line=line.strip()
            if not line or ":" not in line: continue
            try:
                k,v=line.split(":",1)
                k=k.strip(); v=v.strip().strip("'").strip('"')
                fm_min[k]=v
            except Exception:
                continue # Skip malformed lines
        return fm_min, body.lstrip("\n")


def harvest_pump(body: str, fm: dict, self_cid: str):
    residue_hits = len(R_RESIDUE_HEAD.findall(body))
    token_hits = len(re.findall(r"\b(residue|mismatch|gap|doesn'?t\s+fit)\b", body, flags=re.I))
    residue_score = min(1.0, 0.2*residue_hits + 0.02*token_hits)
    next_cands = set()
    x = fm.get("crosslinks") or {}
    for lst in ("downstream_effects","prerequisites","near_synonyms"):
        for t in (x.get(lst) or []):
            next_cands.add(str(t).upper())
    for m in R_NEXT_HEAD.finditer(body):
        start = m.end()
        nxt = re.search(r"^#+\s+", body[start:], flags=re.M)
        end = start + (nxt.start() if nxt else len(body[start:]))
        sec = body[start:end]
        for cid2 in R_CROSSLINK.findall(sec):
            next_cands.add(cid2.upper())
    for cid2 in R_CROSSLINK.findall(body):
        next_cands.add(cid2.upper())
    next_cands.discard(self_cid)
    return residue_score, next_cands

def rare_token_overlap(a_tokens: Counter, b_tokens: Counter, min_common=3):
    if not a_tokens or not b_tokens: return 0.0
    common = set(a_tokens) & set(b_tokens)
    if len(common) < min_common: return 0.0
    score = 0.0
    for t in common:
        freq = a_tokens.get(t, 0) + b_tokens.get(t, 0)
        if freq <= 0: continue
        score += 1.0 / (1.0 + freq)
    return score

def build_graph(dict_dir: Path, out_dir: Path):
    nodes = {}
    alias_map = defaultdict(set)
    symbol_map = defaultdict(set)
    checkpoint_file = out_dir / "progress_checkpoint.json"

    files = sorted(dict_dir.glob("*.md"))
    print(f"Parsing {len(files)} dictionary files...")
    for fp in files:
        fm, body = parse_frontmatter_and_body(read(fp), fp)
        term = (fm.get("term") or fp.stem).strip()
        cid  = (fm.get("canonical_id") or canon_id(term))
        if not term or not cid:
            print(f"  WARNING: Skipping file with missing term/cid: {fp.name}")
            continue
        sym  = (fm.get("symbol") or "").strip()
        aliases = fm.get("aliases") or []
        if isinstance(aliases, str):
            aliases = [a.strip() for a in aliases.split(",") if a.strip()]
        parents  = [str(x).strip().upper() for x in (fm.get("parents")  or [])]
        children = [str(x).strip().upper() for x in (fm.get("children") or [])]
        residue, nexts = harvest_pump(body, fm, cid)
        nodes[cid] = {
            "term": term, "symbol": sym, "aliases": aliases,
            "parents": parents, "children": children,
            "body": body, "residue": residue, "nexts": nexts,
            "tokens": Counter(TOKEN.findall(body.lower()))
        }
        if sym: symbol_map[sym].add(cid)
        for a in aliases: alias_map[a.lower()].add(cid)

    edges = defaultdict(lambda: defaultdict(float))
    start_index = 0

    if checkpoint_file.exists():
        print(f"Loading progress from checkpoint: {checkpoint_file}")
        try:
            with checkpoint_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                start_index = data.get("progress_index", 0)
                edge_data = data.get("edges", {})
                for k, v_weight in edge_data.items():
                    u, v_node = k.split(',')
                    edges[u][v_node] = float(v_weight)
                print(f"  ...Resuming from pair index {start_index}.")
        except json.JSONDecodeError:
            print(f"  WARNING: Checkpoint file is corrupted. Deleting and starting fresh.")
            checkpoint_file.unlink()

    print("Calculating edge weights (structural)...")
    for u, n in nodes.items():
        for v in n["parents"]:
            if v in nodes:
                edges[u][v] = max(edges.get(u,{}).get(v, 0.0), 1.0); edges[v][u] = max(edges.get(v,{}).get(u, 0.0), 1.0)
        for v in n["children"]:
            if v in nodes:
                edges[u][v] = max(edges.get(u,{}).get(v, 0.0), 1.0); edges[v][u] = max(edges.get(v,{}).get(u, 0.0), 1.0)
    for u, n in nodes.items():
        for v in n["nexts"]:
            if v in nodes:
                edges[u][v] = max(edges.get(u,{}).get(v, 0.0), 0.6); edges[v][u] = max(edges.get(v,{}).get(u, 0.0), 0.6)
    for _, cids in alias_map.items():
        cids = list(cids)
        for i in range(len(cids)):
            for j in range(i+1, len(cids)):
                a,b = cids[i], cids[j]
                edges[a][b] = max(edges.get(a,{}).get(b, 0.0), 0.25); edges[b][a] = max(edges.get(b,{}).get(a, 0.0), 0.25)
    for _, cids in symbol_map.items():
        cids = list(cids)
        for i in range(len(cids)):
            for j in range(i+1, len(cids)):
                a,b = cids[i], cids[j]
                edges[a][b] = max(edges.get(a,{}).get(b, 0.0), 0.2); edges[b][a] = max(edges.get(b,{}).get(a, 0.0), 0.2)

    print("Calculating edge weights (text overlap)... this may take a while.")
    doc_freq = Counter()
    for node in nodes.values(): doc_freq.update(node["tokens"].keys())
    
    rare_tokens = {t for t, count in doc_freq.items() if 1 < count < len(nodes) * 0.1}
    inverted_index = defaultdict(list)
    for cid, node in nodes.items():
        for token in node["tokens"]:
            if token in rare_tokens: inverted_index[token].append(cid)

    pairs_to_compare = set()
    for doc_list in inverted_index.values():
        for i in range(len(doc_list)):
            for j in range(i + 1, len(doc_list)):
                pairs_to_compare.add(tuple(sorted((doc_list[i], doc_list[j]))))

    pairs_list = sorted(list(pairs_to_compare))
    total_pairs = len(pairs_list)
    print(f"Found {total_pairs} candidate pairs for text overlap analysis.")
    
    checkpoint_temp_file = out_dir / "progress_checkpoint.json.tmp"
    last_checkpoint_time = time.time()

    for i in range(start_index, total_pairs):
        a, b = pairs_list[i]
        s = rare_token_overlap(nodes[a]["tokens"], nodes[b]["tokens"])
        if s > 0:
            w = min(0.10, 0.02 * s)
            edges[a][b] = max(edges.get(a,{}).get(b, 0.0), w); edges[b][a] = max(edges.get(b,{}).get(a, 0.0), w)

        current_time = time.time()
        if current_time - last_checkpoint_time > 5 or i % 1000 == 999:
            print(f"  ...processed {i + 1}/{total_pairs} pairs. Checkpointing...")
            serializable_edges = {f"{u},{v}": w for u, inner in edges.items() for v, w in inner.items()}
            checkpoint_data = {"progress_index": i + 1, "edges": serializable_edges}
            try:
                with checkpoint_temp_file.open("w", encoding="utf-8") as f:
                    json.dump(checkpoint_data, f)
                os.replace(checkpoint_temp_file, checkpoint_file)
            except Exception as e:
                print(f"  WARNING: Could not write checkpoint: {e}")
            last_checkpoint_time = current_time

    print("Finished calculating all edge weights.")
    serializable_edges = {f"{u},{v}": w for u, inner in edges.items() for v, w in inner.items()}
    final_data = {"progress_index": total_pairs, "edges": serializable_edges}
    try:
        with checkpoint_temp_file.open("w", encoding="utf-8") as f:
            json.dump(final_data, f)
        os.replace(checkpoint_temp_file, checkpoint_file)
    except Exception as e:
        print(f"  WARNING: Could not write final checkpoint: {e}")

    return nodes, edges

def to_exports(nodes, edges, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    degrees = {u: sum(edges.get(u, {}).values()) for u in nodes}
    cluster_of = {u: 0 for u in nodes}
    
    edge_list_for_nx = []
    for u, inner in edges.items():
        for v, w in inner.items():
            if u < v:
                edge_list_for_nx.append((u, v, float(w)))

    if HAS_NX:
        print("Clustering with networkx...")
        G = nx.Graph()
        for u in nodes: G.add_node(u)
        G.add_weighted_edges_from(edge_list_for_nx)
        try:
            comms = list(nx.algorithms.community.greedy_modularity_communities(G, weight="weight"))
            for i, com in enumerate(comms, 1):
                for u in com: cluster_of[u] = i
        except Exception as e:
            print(f"Clustering failed: {e}")
        print("Writing GEXF file...")
        for u in G.nodes:
            G.nodes[u]["label"] = nodes[u]["term"]
            G.nodes[u]["term"] = nodes[u]["term"]
            G.nodes[u]["symbol"] = nodes[u]["symbol"]
            G.nodes[u]["aliases"] = ", ".join(nodes[u]["aliases"])
            G.nodes[u]["residue"] = float(nodes[u]["residue"])
            G.nodes[u]["degree"]  = float(degrees.get(u,0.0))
            G.nodes[u]["cluster"] = int(cluster_of.get(u,0))
        nx.write_gexf(G, out_dir / "idea_map.gexf")
    else:
        print("networkx not found, skipping GEXF and clustering.")

    print("Writing CSV files...")
    with (out_dir / "nodes.csv").open("w", encoding="utf-8") as f:
        f.write("id,cid,term,symbol,aliases,residue,degree,cluster\n")
        for u, n in nodes.items():
            ali = "; ".join(n["aliases"])
            f.write(f"{u},{u},{n['term'].replace(',',';')},{n['symbol'].replace(',',';')},{ali.replace(',',';')},{n['residue']:.3f},{degrees.get(u,0.0):.3f},{cluster_of.get(u,0)}\n")
    
    with (out_dir / "edges.csv").open("w", encoding="utf-8") as f:
        f.write("source,target,weight,type\n")
        for u,v,w in edge_list_for_nx:
            f.write(f"{u},{v},{w:.3f},undirected\n")

    print("Writing summary JSON...")
    clusters = defaultdict(int)
    for u in nodes: clusters[cluster_of.get(u,0)] += 1
    summary = {
        "generated_at": datetime.utcnow().isoformat()+"Z",
        "nodes": len(nodes),
        "edges": len(edge_list_for_nx),
        "clusters": {str(k): v for k,v in sorted(clusters.items())},
        "has_networkx": HAS_NX
    }
    (out_dir / "idea_map.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Writing interactive D3 graph...")
    make_d3(out_dir, nodes, edge_list_for_nx, cluster_of, degrees)

def make_d3(out_dir: Path, nodes, edge_list, cluster_of, degrees):
    nid = {u:i for i,u in enumerate(nodes)}
    d3_nodes = [{
        "id": nid[u], "cid": u, "term": nodes[u]["term"],
        "symbol": nodes[u]["symbol"], "cluster": int(cluster_of.get(u,0)),
        "residue": float(nodes[u]["residue"]), "degree": float(degrees.get(u,0.0))
    } for u in nodes]
    links = [{"source": nid[u], "target": nid[v], "weight": w} for u,v,w in edge_list]
    data = {"nodes": d3_nodes, "links": links}
    html = f"""<!DOCTYPE html>
<meta charset="utf-8">
<title>Pirouette Idea Map</title>
<style>
  body {{ margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; background:#111; color:#fff; }}
  #legend {{ position: fixed; top:10px; left:10px; background:rgba(0,0,0,0.7); padding:8px 10px; border-radius:8px; font-size: 12px; }}
  .node {{ stroke:#fff; stroke-width:0.6px; }}
  .link {{ stroke:#999; stroke-opacity:0.25; }}
  g.nodes g:hover {{ cursor: pointer; }}
</style>
<div id="legend">Drag to explore • color=cluster • size~degree • halo~residue</div>
<svg id="svg" width="100%" height="100vh"></svg>
<script>
const data = {json.dumps(data)};
const svg = document.getElementById('svg');
const width = svg.clientWidth, height = svg.clientHeight;
const NS='http://www.w3.org/2000/svg';
const gLinks = document.createElementNS(NS,'g'); gLinks.setAttribute('class','links'); svg.appendChild(gLinks);
const gNodes = document.createElementNS(NS,'g'); gNodes.setAttribute('class','nodes'); svg.appendChild(gNodes);
function color(c) {{ const palette = ['#6e40aa','#4178ae','#2ca25f','#e6550d','#9467bd','#d62728','#8c6d31','#17becf','#7f7f7f','#1f77b4']; return palette[c % palette.length]; }}
const nodes = data.nodes.map(d => Object.assign({{}}, d));
const links = data.links.map(d=>Object.assign({{}}, d));
function circle(r, fill, cls) {{
  const c = document.createElementNS(NS,'circle');
  c.setAttribute('r', r); c.setAttribute('fill', fill);
  if (cls) c.setAttribute('class', cls);
  return c;
}}
const linkEls = links.map(l => {{
  const e = document.createElementNS(NS,'line');
  e.setAttribute('class','link');
  e.setAttribute('stroke-width', Math.max(0.5, Math.sqrt(l.weight)));
  gLinks.appendChild(e);
  return e;
}});
const nodeEls = nodes.map(n => {{
  const g = document.createElementNS(NS,'g');
  const size = 2 + Math.log(2 + n.degree);
  const halo = circle(size+2, 'rgba(255,165,0,'+(0.1 + 0.5*n.residue)+')');
  const dot  = circle(size, color(n.cluster), 'node');
  const text = document.createElementNS(NS, 'text');
  text.textContent = n.term;
  text.setAttribute('fill', '#fff'); text.setAttribute('font-size', '10px');
  text.setAttribute('dx', size + 2); text.setAttribute('dy', '0.3em');
  text.style.display = 'none';
  g.appendChild(halo); g.appendChild(dot); g.appendChild(text);
  const title = document.createElementNS(NS, 'title');
  title.textContent = n.term + ' ['+n.cid+']';
  g.appendChild(title);
  gNodes.appendChild(g);
  g.addEventListener('mousedown', dragstart);
  g.addEventListener('mouseover', () => text.style.display = 'block');
  g.addEventListener('mouseout', () => text.style.display = 'none');
  return g;
}});
function tick() {{
  linkEls.forEach((e,i)=>{{ const l=links[i]; const s=nodes[l.source], t=nodes[l.target];
    e.setAttribute('x1', s.x); e.setAttribute('y1', s.y);
    e.setAttribute('x2', t.x); e.setAttribute('y2', t.y); }});
  nodeEls.forEach((e,i)=>{{ const n=nodes[i]; e.setAttribute('transform','translate('+n.x+','+n.y+')'); }});
}}
function dragstart(ev) {{
  const n = Array.from(gNodes.children).indexOf(this);
  if (n<0) return;
  const node = nodes[n];
  const move = (e)=>{{ node.fx=e.clientX; node.fy=e.clientY; tick(); }};
  const up = ()=>{{ node.fx=null; node.fy=null; window.removeEventListener('mousemove',move); window.removeEventListener('mouseup',up); }};
  window.addEventListener('mousemove',move); window.addEventListener('mouseup',up);
}}
function sim() {{
  nodes.forEach((n,i)=>{{ n.x = (Math.random()*0.6+0.2)*width; n.y=(Math.random()*0.6+0.2)*height; }});
  let frame;
  function run() {{
    links.forEach(l=>{{
      const a=nodes[l.source], b=nodes[l.target]; let dx=b.x-a.x, dy=b.y-a.y;
      const dist = Math.hypot(dx,dy)+1e-6; const want = 40 - Math.min(25, Math.sqrt(l.weight)*6);
      const k = 0.01 * (dist-want)/dist; a.x += dx*k; a.y += dy*k; b.x -= dx*k; b.y -= dy*k;
    }});
    for (let i=0;i<nodes.length;i++) {{
        for (let j=i+1;j<nodes.length;j++) {{
            const a=nodes[i], b=nodes[j]; let dx=a.x-b.x, dy=a.y-b.y; let d2=dx*dx+dy*dy+1;
            const k = -80/d2; a.x += dx*k; a.y += dy*k; b.x -= dx*k; b.y -= dy*k;
        }}
    }}
    nodes.forEach(n=>{{
        if (n.fx === null) n.x = Math.max(20, Math.min(width-20, n.x));
        if (n.fy === null) n.y = Math.max(20, Math.min(height-20, n.y));
    }});
    tick();
    frame = requestAnimationFrame(run);
  }}
  run();
}}
sim();
</script>
"""
    (out_dir / "idea_map_d3.html").write_text(html, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser(description="Build an idea map (graph + clusters) from dictionary markdown.")
    ap.add_argument("--dict", default="./dictionary", help="Directory with dictionary markdown files")
    ap.add_argument("--out", default="./ideamap", help="Output directory for the idea map")
    args = ap.parse_args()

    dict_dir = Path(args.dict)
    out_dir  = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    nodes, edges = build_graph(dict_dir, out_dir)
    if not nodes:
        print("No entries found in", dict_dir); return
    to_exports(nodes, edges, out_dir)
    print("Idea map written to:", out_dir.resolve())
    
    checkpoint_file = out_dir / "progress_checkpoint.json"
    if checkpoint_file.exists():
        checkpoint_file.unlink()
        print(f"Successfully completed. Removed checkpoint file.")

if __name__ == "__main__":
    main()