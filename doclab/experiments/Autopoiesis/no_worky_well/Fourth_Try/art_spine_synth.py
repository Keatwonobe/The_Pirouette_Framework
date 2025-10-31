
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
    p = argparse.ArgumentParser()
    p.add_argument("--law_dir", default="./spines/law")
    p.add_argument("--phil_dir", default="./spines/philosophy")
    p.add_argument("--out", default="./spines/art")
    p.add_argument("--provider", default="openai")
    p.add_argument("--model", default="gpt-5-thinking")
    p.add_argument("--max_tokens", type=int, default=1200)
    args = p.parse_args()

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    law_files = sorted(Path(args.law_dir).glob("law_mod_*.md"))
    for lf in law_files:
        idx = lf.stem.split("_")[-1]
        pf = Path(args.phil_dir)/f"phil_mod_{idx}.md"
        phil_text = pf.read_text(encoding="utf-8") if pf.exists() else ""
        law_text = lf.read_text(encoding="utf-8")
        prompt = PROMPT_TMPL.format(SYSTEM=SYSTEM, law_text=law_text[:10000], phil_text=phil_text[:8000])
        text = generate_text(args.provider, args.model, prompt, max_output_tokens=args.max_tokens, temperature=0.45)
        out = outdir / f"art_mod_{idx}.md"
        out.write_text(text, encoding="utf-8")
        print(f"✅ Wrote {out}")

if __name__ == "__main__":
    main()
