
import os, json, re
from pathlib import Path
from typing import List, Dict

OUT_DIR = "./manifesto_modules"

def load_sections(curated_dir: str) -> Dict[str, List[Path]]:
    d = Path(curated_dir)
    buckets = {}
    for p in sorted(d.glob("*.md")):
        name = p.stem
        if "__" in name:
            sec = name.split("__",1)[0]
        else:
            head = p.read_text(encoding="utf-8").splitlines()[0].strip("# ").strip()
            sec = head.split(".",1)[0]
        buckets.setdefault(sec,[]).append(p)
    return buckets

def anti_redundancy(texts: List[str]) -> List[str]:
    seen=set(); out=[]
    for t in texts:
        key = re.sub(r"\s+"," ",t[:120]).lower()
        if key in seen: continue
        seen.add(key); out.append(t)
    return out

def weave_manifesto(curated_dir: str, vessel_map_path: str, title: str="Manifesto Module") -> str:
    vm = json.loads(Path(vessel_map_path).read_text(encoding="utf-8"))
    buckets = load_sections(curated_dir)
    parts = [f"# {title}\n"]
    for sec in vm["sections"]:
        sid = sec["id"]
        parts.append(f"\n## {sid}. {sec['name']}\n")
        items = buckets.get(sid, [])
        texts = [Path(p).read_text(encoding="utf-8") for p in items if p.name.endswith("__PASS.md")]
        texts = anti_redundancy(texts)
        if not texts:
            parts.append("_(No accepted sections; placeholder for synthesis.)_")
        else:
            for i, t in enumerate(texts):
                parts.append(t.strip())
                if i < len(texts)-1:
                    parts.append("\n> **Resonance Delta:** The following section challenges or deepens the prior claim.\n")
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    out = Path(OUT_DIR)/ (title.replace(" ","_").lower()+".md")
    out.write_text("\n\n".join(parts), encoding="utf-8")
    return str(out)

def main():
    import argparse
    p = argparse.ArgumentParser(description="Assemble a manifesto from curated PASS sections.")
    p.add_argument("curated_dir", help="sections_curated")
    p.add_argument("vessel_map", help="section_map.json")
    p.add_argument("--title", default="Manifesto Module: Resonant Unification")
    args = p.parse_args()
    path = weave_manifesto(args.curated_dir, args.vessel_map, args.title)
    print(f"✅ Wrote manifesto module: {path}")

if __name__=="__main__":
    main()
