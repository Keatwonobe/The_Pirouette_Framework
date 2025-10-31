
import os, sys, re, json
from pathlib import Path
from model_router import generate_text

SYSTEM = """You are the LAW axis of a triaxial scientific paper.
Write as a formal, precise physicist-mathematician.
Define all symbols on first use; include at least one derivation (Markdown math ok) and one falsifiable criterion with measurable thresholds.
Use minimal, load-bearing external citations in (Author, Year) and add a References list.
Tone: formal with restrained poetic gravitas."""

PROMPT_TMPL = """{SYSTEM}

MODULE FILE: {fname}
MODULE SOURCE (for understanding only; do NOT cite internally):
{source_excerpt}

TASK:
Write a self-contained LAW section (~1200–1800 words) that will become part of a larger paper collaboration.
Deliverables:
- Problem recap + symbol glossary
- Governing equations or action-like formal object
- One explicit derivation (not just statements)
- Predictions with effect sizes and falsifiability thresholds (datasets/instruments, N, sigma)
- Objections & Resolution (steelman 2 strongest objections)
- References (2–5 external, load-bearing)

Begin.
"""

def main():
    import argparse
    p = argparse.ArgumentParser(description="LAW spine writer over a directory of Markdown modules.")
    p.add_argument("modules_dir", help="Path to directory with *.md modules")
    p.add_argument("--provider", default="openai")
    p.add_argument("--model", default="gpt-5-thinking")
    p.add_argument("--out", default="./spines/law")
    p.add_argument("--glob", default="*.md", help="Glob filter inside modules_dir")
    p.add_argument("--exclude", nargs="*", default=["readme*.md","index*.md"], help="Exclusion globs")
    p.add_argument("--max_tokens", type=int, default=2200)
    p.add_argument("--limit", type=int, default=0)
    args = p.parse_args()

    srcdir = Path(args.modules_dir)
    files = sorted(srcdir.rglob(args.glob))
    # apply exclusions
    if args.exclude:
        def excluded(path: Path) -> bool:
            name = path.name.lower()
            return any(re.fullmatch(glob_to_re(g), name) for g in args.exclude)
        files = [f for f in files if not excluded(f)]

    if args.limit > 0:
        files = files[:args.limit]

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    logs = []

    for i, f in enumerate(files, start=1):
        text = f.read_text(encoding="utf-8", errors="ignore")
        excerpt = text[:15000]  # keep prompt bounded; adjust as needed
        prompt = PROMPT_TMPL.format(SYSTEM=SYSTEM, fname=f.name, source_excerpt=excerpt)
        resp = generate_text(args.provider, args.model, prompt, max_output_tokens=args.max_tokens, temperature=0.2)

        if not resp or len(resp) < 200:
            logs.append(f"SKIP (empty/short): {f}")
            print(f"– Skipping {f.name} (empty/short response). Check API key/limits.")
            continue

        # Add minimal YAML header so later passes can sort/route
        header = f"---\naxis: Law\nsource_file: {f.name}\nstatus: draft\n---\n"
        out_path = outdir / f"law__{f.stem}.md"
        out_path.write_text(header + resp.strip() + "\n", encoding="utf-8")
        print(f"✅ {i:03d}/{len(files)} wrote {out_path}")

    if logs:
        (outdir / "_law_warnings.log").write_text("\n".join(logs), encoding="utf-8")

def glob_to_re(glob: str) -> str:
    # simple glob→regex for filename matching
    s = re.escape(glob).replace(r"\*", ".*").replace(r"\?", ".")
    return s

if __name__ == "__main__":
    main()
