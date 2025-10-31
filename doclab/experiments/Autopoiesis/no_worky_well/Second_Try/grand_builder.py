
import os, json, re
from pathlib import Path
from typing import Dict, List, Tuple

OUT_DIR = "./grand_out"

def coverage_report(vessel_map: dict, manifestos: List[Path]) -> Dict[str, bool]:
    coverage = {s["id"]: False for s in vessel_map["sections"]}
    for m in manifestos:
        txt = Path(m).read_text(encoding="utf-8")
        for s in vessel_map["sections"]:
            if re.search(rf"^##\s*{re.escape(s['id'])}\.", txt, flags=re.M):
                block = re.split(rf"^##\s*{re.escape(s['id'])}\.", txt, flags=re.M)[-1]
                coverage[s["id"]] = coverage[s["id"]] or ("placeholder" not in block.lower())
    return coverage

def sort_sections(vessel_map: dict, pool_texts: List[str]) -> List[Tuple[str,str]]:
    ordered = []
    for s in vessel_map["sections"]:
        sid = s["id"]
        candidates = [t for t in pool_texts if t.strip().startswith(f"## {sid}.")]
        ordered.extend([(sid, t) for t in candidates])
    return ordered

def renormalize(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+(\n)", r"\1", text)
    return text

def build_grand(vessel_map_path: str, manifesto_dir: str, write_missing: bool = True) -> str:
    vm = json.loads(Path(vessel_map_path).read_text(encoding="utf-8"))
    mfiles = sorted(Path(manifesto_dir).glob("*.md"))
    cov = coverage_report(vm, mfiles)

    pool = []
    for mf in mfiles:
        pool.append(Path(mf).read_text(encoding="utf-8"))

    additions = []
    for s in vm["sections"]:
        if s.get("required", True) and not cov.get(s["id"], False) and write_missing:
            additions.append(f"## {s['id']}. {s['name']}\n_(Synthesis required: this section was not addressed sufficiently. Draft now.)_\n")

    ordered = sort_sections(vm, pool + additions)
    parts = [f"# {vm.get('title','Grand Manifesto')}\n"]
    parts.extend(t for _, t in ordered)
    text = renormalize("\n\n".join(parts))

    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    out = Path(OUT_DIR)/"grand_manifesto_assembled.md"
    Path(out).write_text(text, encoding="utf-8")
    return str(out)

def main():
    import argparse
    p = argparse.ArgumentParser(description="Grand builder: coverage check, sorting, renormalization.")
    p.add_argument("vessel_map", help="section_map.json")
    p.add_argument("manifesto_dir", help="manifesto_modules/")
    p.add_argument("--no_missing", action="store_true", help="Do not add TODO stubs for missing sections.")
    args = p.parse_args()
    path = build_grand(args.vessel_map, args.manifesto_dir, write_missing=not args.no_missing)
    print(f"✅ Grand assembled: {path}")

if __name__=="__main__":
    main()
