
import re, json
from pathlib import Path
from typing import Dict, List, Tuple

from glob import glob

SOURCE_FILES = [
    "pirouette_version_6.md",
    "I__*.md","II__*.md","III__*.md","IV__*.md","V__*.md","VI__*.md","SYN__*.md","APP__*.md",
    "paper_*.md","manifesto_*.md","grand_manifesto.md"
]

OUT_JSON = "./concept_graph.json"
OUT_TSV  = "./concept_edges.tsv"
OUT_DOT  = "./concept_graph.dot"

TERMS = [
    r"\bKi\b", r"\bK[iι]\b", r"\bΓ\b", r"\bGamma\b", r"\bT[_ ]?a\b", r"\bchronon\b", r"\bT[_ ]?c\b",
    r"\bcausal inertia\b", r"\bsubstrate\b", r"\btime[- ]substrate\b",
    r"\bsubstrate energy density\b", r"\bU[_ ]?s\b",
    r"\bAnisotropic Temporal Vector\b|\bT[ _]?α\b|\bTalpha\b",
    r"\bpressuron\b", r"\bg-2\b|\banomalous magnetic moment\b",
    r"\bEEG\b|\bMEG\b|\bphase[- ]locking\b|\bPLV\b",
    r"\bCasimir\b", r"\bdecoherence\b", r"\bringdown\b|\bquasi[- ]normal\b",
    r"\bCMB\b|\bcosmolog\w+ constant\b|\bΛ\b", r"\balpha\b (constant|variation)",
    r"\bInformational Inertia\b|\bK[_ ]?i\b", r"\bUniversal Rate\b|\bC = Γ / T[_ ]?a\b",
    r"\bDomain Inertia\b", r"\bLorentz\b|\bGR\b|\brelativity\b",
    r"\bethic\w+\b|\bgovernance\b|\bDark Residue\b",
]

def load_files() -> List[Tuple[str,str]]:
    files = []
    for pat in SOURCE_FILES:
        for p in glob(pat):
            try:
                files.append((p, Path(p).read_text(encoding="utf-8", errors="ignore")))
            except Exception:
                pass
    return files

def tokenize_paragraphs(text: str) -> List[str]:
    import re
    paras = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paras if p.strip()]

def extract_nodes(paragraphs: List[str]) -> Dict[str, Dict]:
    import re
    nodes = {}
    for p in paragraphs:
        found = []
        for pat in TERMS:
            if re.search(pat, p, flags=re.I):
                found.append(pat)
        for f in set(found):
            nodes.setdefault(f, {"id": f, "label": re.sub(r"\\b","",f), "count":0})
            nodes[f]["count"] += 1
    return nodes

def cooccurrence_edges(paragraphs: List[str], nodes: Dict[str,Dict]) -> Dict[Tuple[str,str], int]:
    import re
    edges = {}
    pats = list(nodes.keys())
    for p in paragraphs:
        present = [pat for pat in pats if re.search(pat, p, flags=re.I)]
        present = sorted(set(present))
        for i in range(len(present)):
            for j in range(i+1, len(present)):
                e = (present[i], present[j])
                edges[e] = edges.get(e,0)+1
    return edges

def main():
    files = load_files()
    all_paras = []
    for name, text in files:
        all_paras.extend(tokenize_paragraphs(text))

    nodes = extract_nodes(all_paras)
    edges = cooccurrence_edges(all_paras, nodes)

    j = {
        "nodes": [{"id": k, "label": nodes[k]["label"], "count": nodes[k]["count"]} for k in nodes],
        "edges": [{"source": a, "target": b, "weight": w} for (a,b), w in edges.items()]
    }
    Path(OUT_JSON).write_text(json.dumps(j, indent=2), encoding="utf-8")

    with open(OUT_TSV, "w", encoding="utf-8") as f:
        f.write("source\ttarget\tweight\n")
        for (a,b), w in sorted(edges.items(), key=lambda x: -x[1]):
            f.write(f"{nodes[a]['label']}\t{nodes[b]['label']}\t{w}\n")

    with open(OUT_DOT, "w", encoding="utf-8") as f:
        f.write("graph pirouette {\n  overlap=false;\n  splines=true;\n")
        for k, nd in nodes.items():
            f.write(f'  "{k}" [label="{nd["label"]}", shape=ellipse, fontsize=12];\n')
        for (a,b), w in edges.items():
            pen = 1 + min(5, w)
            f.write(f'  "{a}" -- "{b}" [penwidth={pen}];\n')
        f.write("}\n")

    print(f"✅ Wrote graph: {OUT_JSON}, {OUT_TSV}, {OUT_DOT}")

if __name__ == "__main__":
    main()
