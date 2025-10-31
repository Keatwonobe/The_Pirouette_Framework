
import os
from pathlib import Path
from typing import List
import google.generativeai as genai  # type: ignore

MODEL = "gemini-2.5-pro"
API_KEY_ENV = "GOOGLE_API_KEY"

def read_papers(papers_dir: str) -> List[str]:
    files = sorted(Path(papers_dir).glob("paper_*.md"))
    return [Path(f).read_text(encoding="utf-8") for f in files]

def build_manifesto_prompt(papers: List[str], title_hint: str):
    joined = "\n\n--- PAPER SPLIT ---\n\n".join(papers)
    return f"""
You are assembling a 30–35 page **Manifesto** from multiple papers.
Follow this scaffold:

1. The Foundational Crisis
2. The Substrate Action
3. Physics Predictions
4. Cross-Domain Instantiation
5. Experimental Roadmap
6. Philosophical Implications

Rules:
- Use debate resonance (steelman objections, then fuse).
- Use minimal, load-bearing external citations only, with a References section.
- No internal file/module IDs.
- Conclude with a single blockquote capturing the ethos.

SOURCE (for understanding only):
{joined}

Now write the full manifesto titled: {title_hint}
"""

def construct_manifesto(papers_dir: str, out_dir: str, title_hint: str, index: int):
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"{API_KEY_ENV} not set")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL)

    papers = read_papers(papers_dir)
    prompt = build_manifesto_prompt(papers, title_hint)
    resp = model.generate_content(prompt)
    text = getattr(resp, "text", "")
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out = Path(out_dir) / f"manifesto_{index:02d}.md"
    out.write_text(text, encoding="utf-8")
    return str(out)

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("papers_dir")
    p.add_argument("--out", default="./generated_manifestos")
    p.add_argument("--title", default="Manifesto: Resonant Unification")
    p.add_argument("--index", type=int, default=0)
    args = p.parse_args()
    path = construct_manifesto(args.papers_dir, args.out, args.title, args.index)
    print(f"✅ Wrote {path}")

if __name__ == "__main__":
    main()
