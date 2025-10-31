
import re
from pathlib import Path
from typing import List, Tuple

def extract_modules(md_path: str) -> List[Tuple[str,str]]:
    text = Path(md_path).read_text(encoding="utf-8")
    parts = re.split(r"(?:^##[^\n]*\n|^\-\-\-\s*$)", text, flags=re.M)
    chunks = []
    idx = 0
    for block in parts:
        b = block.strip()
        if not b: continue
        title_match = re.match(r"^#*\s*([A-Za-z0-9 \-\:\(\)\[\]_,]+)", b)
        title = title_match.group(1).strip() if title_match else f"Module {idx+1}"
        chunks.append((title, b))
        idx += 1
    return chunks

def main():
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument("modules_md", help="pirouette_version_6.md")
    p.add_argument("--out", default="./modules_out")
    args = p.parse_args()
    mods = extract_modules(args.modules_md)
    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    for i,(t,b) in enumerate(mods):
        path = outdir / f"mod_{i:02d}.md"
        path.write_text(b, encoding="utf-8")
        print(f"Saved {path} :: {t}")
    meta = [{"index":i,"title":t,"path":str((outdir / f'mod_{i:02d}.md').resolve())} for i,(t,_) in enumerate(mods)]
    (outdir / "modules_index.json").write_text(__import__("json").dumps(meta, indent=2), encoding="utf-8")
    print("✅ Wrote modules_index.json")

if __name__ == "__main__":
    main()
