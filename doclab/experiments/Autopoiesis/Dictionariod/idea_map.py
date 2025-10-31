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

import re, json, argparse, math
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

def parse_frontmatter_and_body(text: str):
    # tolerant loader for LaTeX backslashes etc.
    if not text.startswith("---"):
        return {}, text
    try:
        _, rest = text.split("\n", 1)
        fm_raw, body = rest.split("---", 1)
    except ValueError:
        return {}, text
    try:
        fm = yaml.safe_load(fm_raw) or {}
        return fm, body.lstrip("\n")
    except yaml.YAMLError:
        # fallback: naive key: value
        fm_min = {}
        for line in fm_raw.splitlines():
            line=line.strip()
            if not line or ":" not in line: continue
            k,v=line.split(":",1)
            k=k.strip(); v=v.strip().strip("'").strip('"')
            fm_min[k]=v
        return fm_min, body.lstrip("\n")

def harvest_pump(body: str, fm: dict, self_cid: str):
    # residue score
    residue_hits = len(R_RESIDUE_HEAD.findall(body))
    token_hits = len(re.findall(r"\b(residue|mismatch|gap|doesn'?t\s+fit)\b", body, flags=re.I))
    residue_score = min(1.0, 0.2*residue_hits + 0.02*token_hits)

    # next inquiry candidates
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

def rare_token_overlap(a: str, b: str, min_common=3):
    # cheap "semantic-ish" link: intersect tokens, penalize very common tokens
    ta = TOKEN.findall(a.lower()); tb = TOKEN.findall(b.lower())
    if not ta or not tb: return 0.0
    ca, cb = Counter(ta), Counter(tb)
    # pseudo-idf from local docfreq (2 docs here), so use length penalty only
    common = set(ca) & set(cb)
    # favor rarer tokens by inverse frequency across both docs
    score = 0.0  # <<< FIX IS HERE: Ensure score is initialized as a float.
    for t in common:
        freq = ca[t] + cb[t]
        score += 1.0 / (1.0 + freq)
    return score if len(common) >= min_common else 0.0

def build_graph(dict_dir: Path):
    nodes = {}   # cid -> {term,symbol,aliases,body,residue,next,parents,children}
    alias_map = defaultdict(set)
    symbol_map = defaultdict(set)

    files = sorted(dict_dir.glob("*.md"))
    for fp in files:
        fm, body = parse_frontmatter_and_body(read(fp))
        term = (fm.get("term") or fp.stem).strip()
        cid  = (fm.get("canonical_id") or canon_id(term))
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
            "body": body, "residue": residue, "nexts": nexts
        }
        if sym: symbol_map[sym].add(cid)
        for a in aliases: alias_map[a.lower()].add(cid)

    # edges
    edges = defaultdict(lambda: defaultdict(float))
    # parents/children (strong)
    for u, n in nodes.items():
        for v in n["parents"]:
            if v in nodes:
                edges[u][v] += 1.0; edges[v][u] += 1.0
        for v in n["children"]:
            if v in nodes:
                edges[u][v] += 1.0; edges[v][u] += 1.0
    # next inquiry (medium)
    for u, n in nodes.items():
        for v in n["nexts"]:
            if v in nodes:
                edges[u][v] += 0.6; edges[v][u] += 0.6
    # alias overlap (light)
    for _, cids in alias_map.items():
        cids = list(cids)
        for i in range(len(cids)):
            for j in range(i+1, len(cids)):
                a,b = cids[i], cids[j]
                edges[a][b] += 0.25; edges[b][a] += 0.25
    # symbol overlap (lighter)
    for _, cids in symbol_map.items():
        cids = list(cids)
        for i in range(len(cids)):
            for j in range(i+1, len(cids)):
                a,b = cids[i], cids[j]
                edges[a][b] += 0.2; edges[b][a] += 0.2
    # text overlap (very light)
    cids = list(nodes.keys())
    for i in range(len(cids)):
        for j in range(i+1, len(cids)):
            a,b = cids[i], cids[j]
            s = rare_token_overlap(nodes[a]["body"], nodes[b]["body"])
            if s > 0:
                w = min(0.10, 0.02 * s)   # cap; gentle nudge
                edges[a][b] += w; edges[b][a] += w

    return nodes, edges

def to_exports(nodes, edges, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    # degree & clusters
    degrees = {u: sum(edges[u].values()) for u in edges}
    cluster_of = {u: 0 for u in nodes}
    if HAS_NX:
        G = nx.Graph()
        for u in nodes: G.add_node(u)
        for u in edges:
            for v,w in edges[u].items():
                if u < v: G.add_edge(u,v,weight=float(w))
        try:
            # greedy modularity
            comms = list(nx.algorithms.community.greedy_modularity_communities(G, weight="weight"))
            for i, com in enumerate(comms, 1):
                for u in com: cluster_of[u] = i
        except Exception:
            pass
        # gexf
        for u in G.nodes:
            G.nodes[u]["term"] = nodes[u]["term"]
            G.nodes[u]["symbol"] = nodes[u]["symbol"]
            G.nodes[u]["aliases"] = ", ".join(nodes[u]["aliases"])
            G.nodes[u]["residue"] = float(nodes[u]["residue"])
            G.nodes[u]["degree"]  = float(degrees.get(u,0.0))
            G.nodes[u]["cluster"] = int(cluster_of.get(u,0))
        nx.write_gexf(G, out_dir / "idea_map.gexf")

    # csvs
    with (out_dir / "nodes.csv").open("w", encoding="utf-8") as f:
        f.write("id,cid,term,symbol,aliases,residue,degree,cluster\n")
        for u, n in nodes.items():
            ali = "; ".join(n["aliases"])
            f.write(f"{u},{u},{n['term'].replace(',',';')},{n['symbol'].replace(',',';')},{ali.replace(',',';')},{n['residue']:.3f},{degrees.get(u,0.0):.3f},{cluster_of.get(u,0)}\n")
    with (out_dir / "edges.csv").open("w", encoding="utf-8") as f:
        f.write("source,target,weight,type\n")
        seen = set()
        for u in edges:
            for v,w in edges[u].items():
                key = tuple(sorted((u,v)))
                if key in seen: continue
                seen.add(key)
                f.write(f"{key[0]},{key[1]},{float(w):.3f},undirected\n")

    # summary
    clusters = defaultdict(int)
    for u in nodes: clusters[cluster_of.get(u,0)] += 1
    summary = {
        "generated_at": datetime.utcnow().isoformat()+"Z",
        "nodes": len(nodes),
        "edges": len(seen),
        "clusters": {str(k): v for k,v in sorted(clusters.items())},
        "has_networkx": HAS_NX
    }
    (out_dir / "idea_map.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # tiny d3 HTML (force graph)
    make_d3(out_dir, nodes, edges, cluster_of, degrees)

def make_d3(out_dir: Path, nodes, edges, cluster_of, degrees):
    # pack minimal graph as a single JSON object embedded in HTML
    nid = {u:i for i,u in enumerate(nodes)}
    d3_nodes = [{
        "id": nid[u],
        "cid": u,
        "term": nodes[u]["term"],
        "symbol": nodes[u]["symbol"],
        "cluster": int(cluster_of.get(u,0)),
        "residue": float(nodes[u]["residue"]),
        "degree": float(degrees.get(u,0.0))
    } for u in nodes]
    links = []
    seen = set()
    for u in edges:
        for v,w in edges[u].items():
            key = tuple(sorted((u,v)))
            if key in seen: continue
            seen.add(key)
            links.append({"source": nid[key[0]], "target": nid[key[1]], "weight": float(w)})
    data = {"nodes": d3_nodes, "links": links}
    html = f"""<!DOCTYPE html>
<meta charset="utf-8">
<title>Pirouette Idea Map</title>
<style>
  body {{ margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; }}
  #legend {{ position: fixed; top:10px; left:10px; background:#fff7; padding:8px 10px; border-radius:8px; }}
  .node {{ stroke:#fff; stroke-width:0.6px; }}
  .link {{ stroke:#999; stroke-opacity:0.25; }}
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
  g.appendChild(halo); g.appendChild(dot); g.title = n.term + ' ['+n.cid+']';
  gNodes.appendChild(g);
  g.addEventListener('mousedown', dragstart);
  return g;
}});
function tick() {{
  linkEls.forEach((e,i)=>{{ const l=links[i]; const s=nodes[l.source], t=nodes[l.target];
    e.setAttribute('x1', s.x); e.setAttribute('y1', s.y);
    e.setAttribute('x2', t.x); e.setAttribute('y2', t.y); }});
  nodeEls.forEach((e,i)=>{{ const n=nodes[i]; e.setAttribute('transform','translate('+n.x+','+n.y+')'); }});
}}
function dragstart(ev) {{
  const n = nodeEls.indexOf(this);
  if (n<0) return;
  const node = nodes[n];
  const move = (e)=>{{ node.fx=e.clientX; node.fy=e.clientY; }};
  const up = ()=>{{ node.fx=null; node.fy=null; window.removeEventListener('mousemove',move); window.removeEventListener('mouseup',up); }};
  window.addEventListener('mousemove',move); window.addEventListener('mouseup',up);
}}
/* tiny force */
function sim() {{
  // init positions
  nodes.forEach((n,i)=>{{ n.x = (Math.random()*0.6+0.2)*width; n.y=(Math.random()*0.6+0.2)*height; }});
  for (let iter=0; iter<600; iter++) {{
    // repulsion
    for (let i=0;i<nodes.length;i++) for (let j=i+1;j<nodes.length;j++) {{
      const a=nodes[i], b=nodes[j]; let dx=a.x-b.x, dy=a.y-b.y; let d2=dx*dx+dy*dy+0.1;
      let k = 120.0/d2; a.x += dx*k; a.y += dy*k; b.x -= dx*k; b.y -= dy*k;
    }}
    // spring along links
    links.forEach(l=>{{
      const a=nodes[l.source], b=nodes[l.target]; let dx=b.x-a.x, dy=b.y-a.y;
      const dist = Math.hypot(dx,dy)+0.001; const want = 40 - Math.min(25, Math.sqrt(l.weight)*6);
      const k = 0.02*(dist - want);
      a.x += dx/dist*k; a.y += dy/dist*k; b.x -= dx/dist*k; b.y -= dy/dist*k;
    }});
    // confinement
    nodes.forEach(n=>{{ n.x = Math.max(20, Math.min(width-20, n.x)); n.y = Math.max(20, Math.min(height-20, n.y)); }});
    if (iter%6===0) tick();
  }}
  tick();
}}
sim();
</script>
"""
    (out_dir / "idea_map_d3.html").write_text(html, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser(description="Build an idea map (graph + clusters) from dictionary markdown.")
    ap.add_argument("--dict", default="./dictionary")
    ap.add_argument("--out", default="./ideamap")
    args = ap.parse_args()

    dict_dir = Path(args.dict)
    out_dir  = Path(args.out)
    nodes, edges = build_graph(dict_dir)
    if not nodes:
        print("No entries found in", dict_dir); return
    to_exports(nodes, edges, out_dir)
    print("Idea map written to:", out_dir.resolve())

if __name__ == "__main__":
    main()
