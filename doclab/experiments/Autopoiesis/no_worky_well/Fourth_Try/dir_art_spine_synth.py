
from pathlib import Path
from model_router import generate_text

SYSTEM = """You are the ART axis: disciplined imagery that illuminates formal structure.
Every metaphor must map to a named variable or observable.
Tone: lyrical-precise; include a 'Map of Metaphors → Variables' table."""

PROMPT_TMPL = """{SYSTEM}

LAW SECTION (alignment only):
{law_text}

PHILOSOPHY SECTION (alignment only):
{phil_text}

TASK:
Write an ART section (~600–1000 words) that braids reader intuition to LAW & PHILOSOPHY.
Conclude with a 3–5 line stanza encoding invariants.
Begin.
"""

def main():
    import argparse
    p = argparse.ArgumentParser(description="Compose ART spine sections from LAW + PHILOSOPHY.")
    p.add_argument("--law_dir", default="./spines/law")
    p.add_argument("--phil_dir", default="./spines/philosophy")
    p.add_argument("--out", default="./spines/art")
    p.add_argument("--provider", default="openai")
    p.add_argument("--model", default="gpt-5-thinking")
    p.add_argument("--max_tokens", type=int, default=1200)
    p.add_argument("--limit", type=int, default=0)
    args = p.parse_args()

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    law_files = sorted(Path(args.law_dir).glob("law__*.md"))
    if args.limit > 0:
        law_files = law_files[:args.limit]

    for i, lf in enumerate(law_files, start=1):
        idx = lf.stem.replace("law__", "")
        pf = Path(args.phil_dir)/f"phil__{idx}.md"
        law_text  = lf.read_text(encoding="utf-8", errors="ignore")[:10000]
        phil_text = pf.read_text(encoding="utf-8", errors="ignore")[:8000] if pf.exists() else ""
        resp = generate_text(args.provider, args.model, PROMPT_TMPL.format(SYSTEM=SYSTEM, law_text=law_text, phil_text=phil_text),
                             max_output_tokens=args.max_tokens, temperature=0.45)
        if not resp or len(resp) < 200:
            print(f"– Skipping {lf.name} (empty/short resp).")
            continue
        header = f"---\naxis: Art\nsource_law: {lf.name}\nsource_philosophy: {pf.name if pf.exists() else ''}\nstatus: draft\n---\n"
        out = outdir / f"art__{idx}.md"
        out.write_text(header + resp.strip() + "\n", encoding="utf-8")
        print(f"✅ {i:03d}/{len(law_files)} wrote {out}")

if __name__ == "__main__":
    main()
