import os, sys, re, json
from pathlib import Path
from model_router import generate_text # Re-uses your existing model router

# This new system prompt is tailored for the "engram" creation task.
SYSTEM = """You are a master synthesist and philosopher of science. Your task is to distill a complex technical document into its essential, potent core.
You must structure your output using three and only three specific Markdown headings: ## Law, ## Philosophy, and ## Art.

- ## Law: Extract the absolute core mathematical and formal principles. Include key equations, derivations, vocabulary, engrams and falsifiable criteria. This section must be dense, precise, and unsparing in its formalism. All other layers unfold by the rules this lays out.
- ## Philosophy: Articulate the single most cogent and profound philosophical implication of the Law section. What does this formalism mean for our understanding of reality, consciousness, or systems?
- ## Art: Create a concise, powerful metaphor or poetic statement that bridges the abstract nature of the Law with the human implication of the Philosophy. This is the connective tissue.

The final output should be a compact, self-contained "engram" of the source material, no more than 500 tokens in total.
"""

PROMPT_TMPL = """{SYSTEM}

SOURCE DOCUMENT: {fname}
SOURCE CONTENT:
---
{source_content}
---

TASK: Distill the source content into its essential ## Law, ## Philosophy, and ## Art components. Begin your response directly with the `## Law` heading.
"""

def main():
    import argparse
    p = argparse.ArgumentParser(description="Distill Pirouette modules into potent engrams (Law, Philosophy, Art).")
    p.add_argument("modules_dir", help="Path to directory with *.md modules")
    # Defaults are set for the Gemini API as requested
    p.add_argument("--provider", default="google")
    p.add_argument("--model", default="gemini-2.5-pro")
    p.add_argument("--out", default="./engrams")
    p.add_argument("--glob", default="*.md", help="Glob filter inside modules_dir")
    p.add_argument("--exclude", nargs="*", default=["readme*.md","index*.md"], help="Exclusion globs")
    p.add_argument("--max_tokens", type=int, default=1024) # More than enough for a ~500 token engram
    p.add_argument("--limit", type=int, default=0)
    args = p.parse_args()

    srcdir = Path(args.modules_dir)
    files = sorted(srcdir.rglob(args.glob))
    # apply exclusions
    if args.exclude:
        def excluded(path: Path) -> bool:
            name = path.name.lower()
            # Simple glob-to-regex helper function
            def glob_to_re(g): return re.escape(g).replace(r"\*", ".*").replace(r"\?", ".")
            return any(re.fullmatch(glob_to_re(g), name) for g in args.exclude)
        files = [f for f in files if not excluded(f)]

    if args.limit > 0:
        files = files[:args.limit]

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    logs = []

    for i, f in enumerate(files, start=1):
        text = f.read_text(encoding="utf-8", errors="ignore")
        prompt = PROMPT_TMPL.format(SYSTEM=SYSTEM, fname=f.name, source_content=text)
        
        print(f" distilling {f.name}...")
        resp = generate_text(args.provider, args.model, prompt, max_output_tokens=args.max_tokens, temperature=0.1)

        if not resp or len(resp) < 50:
            logs.append(f"SKIP (empty/short): {f}")
            print(f"– Skipping {f.name} (empty/short response).")
            continue

        out_path = outdir / f"engram__{f.stem}.md"
        out_path.write_text(resp.strip() + "\n", encoding="utf-8")
        print(f"✅ {i:03d}/{len(files)} wrote {out_path}")

    if logs:
        (outdir / "_contract_warnings.log").write_text("\n".join(logs), encoding="utf-8")

if __name__ == "__main__":
    main()