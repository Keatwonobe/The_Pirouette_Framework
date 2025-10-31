
from pathlib import Path
from model_router import generate_text

SYSTEM = """You are the PHILOSOPHY axis: ontology, epistemology, ethics, governance.
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
    p = argparse.ArgumentParser(description="Translate LAW spine files into PHILOSOPHY with Gemini.")
    p.add_argument("--in_dir", default="./spines/law")
    p.add_argument("--out", default="./spines/philosophy")
    p.add_argument("--provider", default="gemini")
    p.add_argument("--model", default="gemini-2.5-pro")
    p.add_argument("--max_tokens", type=int, default=1600)
    p.add_argument("--limit", type=int, default=0)
    args = p.parse_args()

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    files = sorted(Path(args.in_dir).glob("law__*.md"))
    if args.limit > 0:
        files = files[:args.limit]

    for i, path in enumerate(files, start=1):
        law_text = path.read_text(encoding="utf-8", errors="ignore")[:16000]
        resp = generate_text(args.provider, args.model, PROMPT_TMPL.format(SYSTEM=SYSTEM, law_text=law_text),
                             max_output_tokens=args.max_tokens, temperature=0.25)
        if not resp or len(resp) < 200:
            print(f"– Skipping {path.name} (empty/short resp). Check GOOGLE_API_KEY/limits.")
            continue
        header = f"---\naxis: Philosophy\nsource_law: {path.name}\nstatus: draft\n---\n"
        out = outdir / path.name.replace("law__", "phil__")
        out.write_text(header + resp.strip() + "\n", encoding="utf-8")
        print(f"✅ {i:03d}/{len(files)} wrote {out}")

if __name__ == "__main__":
    main()
