
import os
from pathlib import Path
from typing import List
import google.generativeai as genai  # type: ignore

MODEL = "gemini-2.5-pro"
API_KEY_ENV = "GOOGLE_API_KEY"

def load_modules(md_path: str) -> List[str]:
    text = Path(md_path).read_text(encoding="utf-8")
    # naive split on module delimiters; adjust if your md uses YAML blocks
    chunks = [c.strip() for c in text.split('\n---\n') if c.strip()]
    return chunks

def build_prompt(modules: List[str], theme: str):
    joined = "\n\n".join(modules[:12])  # ~10–12 per paper
    return f"""
You are the Steward of a scientific framework. Compose a formal academic paper
that triangulates **Art, Law, Philosophy** while deriving claims from first principles.

STRUCTURE (Markdown):
- Title
- Abstract (150–250 words)
- Introduction
- Theoretical Framework
- Methods / Formal Model
- Results / Predictions
- Discussion
- Conclusion
- References (external where necessary)
CITATION STYLE: minimal, load-bearing external sources only. Use (Author, Year) in-text and a References list.

Debate Resonance: surface strongest objections; resolve via derivation or falsifiability.
Include equations in plaintext Markdown; define symbols on first use.

SOURCE MATERIAL (for understanding; do NOT cite internally):
{joined}

Now write the full paper.
"""

def synthesize_paper(modules_path: str, out_dir: str, theme: str, index: int):
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"{API_KEY_ENV} not set")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL)

    mods = load_modules(modules_path)
    prompt = build_prompt(mods, theme)
    resp = model.generate_content(prompt)
    text = getattr(resp, "text", "")
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out = Path(out_dir) / f"paper_{index:02d}.md"
    out.write_text(text, encoding="utf-8")
    return str(out)

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("modules_md", help="Path to pirouette_version_6.md or compiled modules markdown")
    p.add_argument("--out", default="./generated_papers")
    p.add_argument("--theme", default="Resonant Unification")
    p.add_argument("--index", type=int, default=0)
    args = p.parse_args()
    path = synthesize_paper(args.modules_md, args.out, args.theme, args.index)
    print(f"✅ Wrote {path}")

if __name__ == "__main__":
    main()
