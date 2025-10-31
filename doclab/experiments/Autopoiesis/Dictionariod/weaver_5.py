#!/usr/bin/env python3
"""
weaver_terms_md.py
Markdown-only term dictionary generator.
- Extracts core vocabulary as a bullet list (no JSON).
- Expands each term by asking the model to fill `term_template.md` and return Markdown.
- Writes one Markdown file per term.

Usage:
  python weaver_terms_md.py <modules_dir> \
    --out_terms ./dictionary \
    --template ./term_template.md \
    --per_module_cap 12 \
    --limit 0 \
    --no_frontmatter

Requires:
  - GOOGLE_API_KEY in env
  - google-generativeai (Gemini)

Notes:
  - Produces: <out_terms>/<CANONICAL_ID>.md
  - De-duplicates terms across modules.
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime

import google.generativeai as genai

# -------------------- Config --------------------

EXTRACT_TERMS_PROMPT = """You identify the *core vocabulary* of the following technical document.
Return a concise BULLET LIST (no JSON, no code fences) with one term per line, like:

- Temporal Pressure | symbol: Γ | aliases: Gladiator Force | brief: Field measuring temporal stress; governs momentum exchange across coherence gradients.
- Time Adherence | brief: Degree to which a system stays phase-locked with the substrate's local arrow of time.

Rules:
- 8–15 terms typical; include only central concepts.
- 'symbol' and 'aliases' are optional; 'brief' is one short sentence.
- No extra commentary before or after the list.

DOCUMENT: {module_name}
---
{module_excerpt}
---
Return ONLY the bullet list.
"""

EXPAND_TERM_PROMPT = """You are writing a dictionary entry for the Pirouette Framework.
Fill the provided Markdown template for the term below. Keep section headers and structure.
Write clearly, operationally, and densely (no filler). Include concrete tests/measurements.

Constraints:
- Output ONLY the completed Markdown (no code fences, no pre/post text).
- Where the template has placeholders like {{term}}, replace them with content.
- Today's date: {today}
- Use module_id in a Provenance line.

TERM SEED
Name: {term}
Symbol: {symbol}
Aliases: {aliases}
One-line brief: {brief}

MODULE_ID: {module_id}
MODULE_CONTENT (excerpt):
{module_excerpt}

TEMPLATE:
{template_text}
"""

# -------------------- Helpers --------------------

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")

def write_text(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")

def to_canonical_id(term: str) -> str:
    t = re.sub(r"[^A-Za-z0-9]+", "_", term.strip())
    t = re.sub(r"_+", "_", t).strip("_")
    return t.upper()

def parse_bullet_list(text: str):
    """
    Parse lines like:
      - Temporal Pressure | symbol: Γ | aliases: Gladiator Force | brief: ...
      - Time Adherence | brief: ...
    Return list of dicts with keys: term, symbol, aliases, brief
    """
    terms = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        body = line[2:].strip()
        # Split on pipes while keeping brief segments intact
        parts = [p.strip() for p in body.split("|")]
        # First chunk should be the term (may contain spaces)
        term = parts[0].strip()
        symbol, aliases, brief = "", [], ""
        for chunk in parts[1:]:
            m = re.match(r"(?i)symbol\s*:\s*(.+)$", chunk)
            if m:
                symbol = m.group(1).strip()
                continue
            m = re.match(r"(?i)aliases?\s*:\s*(.+)$", chunk)
            if m:
                aliases = [a.strip() for a in re.split(r"[;,/]", m.group(1)) if a.strip()]
                continue
            m = re.match(r"(?i)brief\s*:\s*(.+)$", chunk)
            if m:
                brief = m.group(1).strip()
                continue
        if term:
            terms.append({"term": term, "symbol": symbol, "aliases": aliases, "brief": brief})
    return terms

def fallback_extract_terms(module_text: str, cap: int):
    """
    Heuristic fallback if model returns something unexpected:
    - pick Title Case or SCREAMING_SNAKE candidates in headings,
    - cap length.
    """
    candidates = set()
    # Headings and bolded tokens
    for m in re.finditer(r"^(#+|\*\*)\s*([A-Z][A-Za-z0-9 _\-]{2,})", module_text, flags=re.M):
        tok = m.group(2).strip().strip("*#- ")
        if len(tok.split()) <= 4:
            candidates.add(tok)
    # ALLCAP snake-ish tokens
    for m in re.finditer(r"\b[A-Z][A-Z0-9_]{3,}\b", module_text):
        candidates.add(m.group(0))
    out = [{"term": t, "symbol": "", "aliases": [], "brief": ""} for t in sorted(candidates)]
    return out[:cap] if cap > 0 else out

# -------------------- Model --------------------

def get_model(name="gemini-2.5-pro"):
    return genai.GenerativeModel(name)

def generate_markdown(model, prompt: str) -> str:
    resp = model.generate_content(prompt)
    # Stitch parts; no JSON expected.
    text_parts = []
    for part in getattr(resp, "parts", []):
        if hasattr(part, "text"):
            text_parts.append(part.text)
    out = "".join(text_parts).strip()
    return out

# -------------------- Frontmatter (optional) --------------------

def frontmatter_for(term, symbol, aliases, module_id):
    today = datetime.today().strftime("%Y-%m-%d")
    ali = f"[{', '.join(aliases)}]" if aliases else "[]"
    fm = (
        "---\n"
        f'term: "{term}"\n'
        f'canonical_id: "{to_canonical_id(term)}"\n'
        f'symbol: "{symbol or ""}"\n'
        f"aliases: {ali}\n"
        f'status: "draft"\n'
        f'version: "0.1"\n'
        f'last_updated: "{today}"\n'
        f'provenance: ["{module_id}"]\n'
        "---\n\n"
    )
    return fm

# -------------------- Main --------------------

def main():
    ap = argparse.ArgumentParser(description="Generate Markdown dictionary entries per term (no JSON).")
    ap.add_argument("modules_dir")
    ap.add_argument("--out_terms", default="./terms")
    ap.add_argument("--template", default="./term_template.md")
    ap.add_argument("--limit", type=int, default=0, help="Max modules (0=all)")
    ap.add_argument("--per_module_cap", type=int, default=12, help="Max terms per module (0=no cap)")
    ap.add_argument("--model", default="gemini-2.5-pro")
    ap.add_argument("--no_frontmatter", action="store_true", help="Do not prepend YAML frontmatter")
    ap.add_argument("--dedupe", action="store_true", help="De-duplicate across modules")
    args = ap.parse_args()

    # API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not set")
        return
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = get_model(args.model)

    template_text = read_text(Path(args.template))

    modules = sorted([p for p in Path(args.modules_dir).glob("*.md") if not p.name.lower().startswith("readme")])
    if args.limit > 0:
        modules = modules[:args.limit]
    print(f"Found {len(modules)} modules.")

    out_dir = Path(args.out_terms)
    out_dir.mkdir(parents=True, exist_ok=True)

    seen_terms = set()

    for mpath in modules:
        module_id = mpath.stem
        mtext = read_text(mpath)
        excerpt = mtext[:16000]  # keep prompt small enough

        print(f"[scan] {mpath.name}")

        # 1) ask for bullet list
        prompt_list = EXTRACT_TERMS_PROMPT.format(
            module_name=mpath.name,
            module_excerpt=excerpt
        )
        raw_list = generate_markdown(model, prompt_list)

        # Bail if model drifted; try fallback
        if not raw_list or "- " not in raw_list:
            terms = fallback_extract_terms(mtext, args.per_module_cap)
        else:
            terms = parse_bullet_list(raw_list)
            if args.per_module_cap > 0:
                terms = terms[:args.per_module_cap]

        if not terms:
            print("  -> no terms returned")
            continue

        # 2) for each term, ask model to fill the template and return ONLY Markdown
        for seed in terms:
            term = seed.get("term", "").strip()
            if not term:
                continue
            cid = to_canonical_id(term)
            if args.dedupe and cid in seen_terms:
                continue

            symbol = seed.get("symbol", "")
            aliases = seed.get("aliases", [])
            brief = seed.get("brief", "")

            prompt_md = EXPAND_TERM_PROMPT.format(
                today=datetime.today().strftime("%Y-%m-%d"),
                term=term,
                symbol=symbol,
                aliases=", ".join(aliases) if aliases else "",
                brief=brief,
                module_id=module_id,
                module_excerpt=excerpt,
                template_text=template_text
            )

            try:
                md = generate_markdown(model, prompt_md)
                if not md or md.strip() == "":
                    print(f"  -> skip '{term}': empty Markdown")
                    continue
            except Exception as e:
                print(f"  -> skip '{term}': {e}")
                continue

            # Optional frontmatter
            final_md = md
            if not args.no_frontmatter:
                fm = frontmatter_for(term, symbol, aliases, module_id)
                final_md = fm + md.lstrip()

            out_path = out_dir / f"{cid}.md"
            write_text(out_path, final_md)
            if args.dedupe:
                seen_terms.add(cid)

    print(f"Done. Wrote files to {out_dir.resolve()}")

if __name__ == "__main__":
    main()
