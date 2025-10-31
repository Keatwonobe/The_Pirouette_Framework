
from pathlib import Path
from model_router import generate_text

SYSTEM = """You are the PHILOSOPHY axis: ontology, epistemology, ethics, and governance.
Re-express LAW as rigorous philosophy; preserve symbols via a short glossary.
Include 'Objections & Resolution' and a 'Principles for Governance' list.
Minimal, load-bearing external citations only."""

PROMPT_TMPL = """{SYSTEM}

LAW INPUT (do not cite internally; retain symbol meanings):
{law_text}

TASK:
Produce a PHILOSOPHY section (~900–1400 words) legible standalone that interlocks with LAW.
End with 'Principles for Governance'.
Begin.
"""

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--in_dir", default="./spines/law")
    p.add_argument("--out", default="./spines/philosophy")
    p.add_argument("--provider", default="gemini")
    p.add_argument("--model", default="gemini-2.5-pro")
    p.add_argument("--max_tokens", type=int, default=1600)
    args = p.parse_args()

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    for path in sorted(Path(args.in_dir).glob("law_mod_*.md")):
        law_text = path.read_text(encoding="utf-8")
        prompt = PROMPT_TMPL.format(SYSTEM=SYSTEM, law_text=law_text[:16000])
        text = generate_text(args.provider, args.model, prompt, max_output_tokens=args.max_tokens, temperature=0.25)
        out = outdir / f"phil_{path.name.replace('law_', '')}"
        out.write_text(text, encoding="utf-8")
        print(f"✅ Wrote {out}")

if __name__ == "__main__":
    main()
