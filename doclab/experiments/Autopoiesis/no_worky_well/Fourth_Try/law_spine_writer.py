
import json
from pathlib import Path
from model_router import generate_text

SYSTEM = """You are the LAW axis of a triaxial manifesto.
Write as a formal, precise physicist-mathematician.
Define all symbols on first use; include at least one derivation and one falsifiable criterion with measurable thresholds.
Use minimal, load-bearing external citations in (Author, Year) and add a References list.
Tone: formal with restrained poetic gravitas."""

PROMPT_TMPL = """{SYSTEM}

MODULE TITLE: {title}
MODULE SOURCE (for understanding only; do NOT cite internally): 
{source_excerpt}

TASK:
Write a self-contained LAW-section (~1200–1800 words) that will become part of a larger manifesto.
Deliverables:
- Problem recap + symbol glossary
- Governing equations or action-like formal object
- One explicit derivation
- Predictions with effect sizes and falsifiability thresholds (datasets/instruments, N, sigma)
- Objections & Resolution (steelman 2 objections)
- References (2–5 external)

Begin.
"""

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("modules_index")
    p.add_argument("--provider", default="openai")
    p.add_argument("--model", default="gpt-5-thinking")
    p.add_argument("--max_tokens", type=int, default=2200)
    p.add_argument("--out", default="./spines/law")
    p.add_argument("--limit", type=int, default=0)
    args = p.parse_args()

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    mods = json.loads(Path(args.modules_index).read_text(encoding="utf-8"))
    if args.limit > 0:
        mods = mods[:args.limit]

    for m in mods:
        title = m["title"]
        src = Path(m["path"]).read_text(encoding="utf-8")
        excerpt = src[:12000]
        prompt = PROMPT_TMPL.format(SYSTEM=SYSTEM, title=title, source_excerpt=excerpt)
        text = generate_text(args.provider, args.model, prompt, max_output_tokens=args.max_tokens, temperature=0.2)
        fname = outdir / f"law_mod_{m['index']:02d}.md"
        fname.write_text(text, encoding="utf-8")
        print(f"✅ Wrote {fname}")

if __name__ == "__main__":
    main()
