
import json
from pathlib import Path

OUT_DIR = "./manifesto_from_concepts"

def bucket(axfile: Path) -> str:
    name = axfile.name.lower()
    if "i__" in name or "foundational" in name: return "I"
    if "ii__" in name or "substrate" in name: return "II"
    if "iii__" in name or "prediction" in name or "g-2" in name: return "III"
    if "iv__" in name or "cross" in name or "instantiation" in name: return "IV"
    if "v__" in name or "experiment" in name or "roadmap" in name: return "V"
    if "vi__" in name or "philosophy" in name or "governance" in name or "dark" in name: return "VI"
    if "syn__" in name or "synth" in name or "outlook" in name: return "SYN"
    return "IV"

def weave(vessel_map: str, concept_dir: str, title: str) -> str:
    vm = json.loads(Path(vessel_map).read_text(encoding="utf-8"))
    parts = [f"# {title}\\n\\n_This document is assembled from micro-sections along three axes: Art, Law, Philosophy._\\n"]
    files = sorted(Path(concept_dir).glob("*.md"))
    bins = {s["id"]: [] for s in vm["sections"]}
    for f in files:
        sid = bucket(f)
        bins[sid].append(f.read_text(encoding="utf-8").strip())

    for s in vm["sections"]:
        parts.append(f"\\n## {s['id']}. {s['name']}\\n")
        if not bins[s["id"]]:
            parts.append("_(No content yet.)_")
            continue
        parts.append(f"_This section braids Art, Law, and Philosophy contributions for concepts mapped here._\\n")
        arts  = [t for t in bins[s["id"]] if t.lower().startswith("### art")  ]
        laws  = [t for t in bins[s["id"]] if t.lower().startswith("### law")  ]
        philos= [t for t in bins[s["id"]] if t.lower().startswith("### philosophy")]
        m = max(len(arts), len(laws), len(philos))
        for i in range(m):
            if i < len(arts): parts.append(arts[i])
            if i < len(laws): parts.append(laws[i])
            if i < len(philos): parts.append(philos[i])
            if i < m-1: parts.append("> **Resonance Delta:** Each axis sharpens the others.\\n")
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    out = Path(OUT_DIR)/ (title.replace(" ","_").lower()+".md")
    Path(out).write_text("\\n\\n".join(parts), encoding="utf-8")
    return str(out)

def main():
    import argparse
    p = argparse.ArgumentParser(description="Stitch concept-axis micro-sections into a manifesto.")
    p.add_argument("vessel_map")
    p.add_argument("concept_dir")
    p.add_argument("--title", default="Manifesto (Triaxial Concept Weave)")
    args = p.parse_args()
    path = weave(args.vessel_map, args.concept_dir, args.title)
    print(f"✅ Wrote manifesto: {path}")

if __name__=="__main__":
    main()
