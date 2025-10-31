#!/usr/bin/env python3
"""
weaver_terms.py
Extract core vocabulary from Pirouette modules and write one markdown file per term
(using a template + schema validation). Designed as a companion to weaver_3.py.

Usage:
  python weaver_terms.py <modules_dir> \
    --out_terms ./terms \
    --template ./term_template.md \
    --schema ./term_entry.schema.json \
    --limit 0 \
    --per_module_cap 12

Requires:
  - GOOGLE_API_KEY in env
  - google-generativeai (Gemini)
  - jsonschema (optional but recommended for validation)

Notes:
  - Produces: <out_terms>/<CANONICAL_ID>.md and <out_terms>/json/<CANONICAL_ID>.json
  - De-duplicates terms across modules (merges context_windows & provenance)
"""

import os
import json
import argparse
from pathlib import Path
import re
from datetime import datetime
from typing import Dict, List, Any

# --- External deps
try:
    import jsonschema  # type: ignore
    HAS_JSONSCHEMA = True
except Exception:
    HAS_JSONSCHEMA = False

import google.generativeai as genai

# ---------- Config / Model ----------
def get_model(model_name="gemini-2.5-pro"):
    return genai.GenerativeModel(model_name)

# ---------- IO Helpers ----------
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def write_json(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# ---------- Template Rendering ----------
_BRACE_PATTERN = re.compile(r"{([a-zA-Z0-9_\.]+)}")

def flat_lookup(d: Dict[str, Any], dotted: str, default: str = "") -> str:
    """Lookup 'a.b.c' in nested dict d."""
    cur = d
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur if isinstance(cur, str) else json.dumps(cur, ensure_ascii=False)

def render_template(template_text: str, entry: Dict[str, Any]) -> str:
    """
    Naive {placeholder} replacement using dotted-path lookups into entry.
    Leaves unknown placeholders intact to make debugging obvious.
    """
    def repl(m):
        key = m.group(1)
        val = flat_lookup(entry, key, default=m.group(0))
        return val
    return _BRACE_PATTERN.sub(repl, template_text)

# ---------- Canonical ID Helpers ----------
def to_canonical_id(term: str) -> str:
    term = re.sub(r"[^A-Za-z0-9]+", "_", term.strip())
    term = re.sub(r"_+", "_", term).strip("_")
    return term.upper()

# ---------- Prompts ----------
EXTRACT_TERMS_SYS = """You extract the *core vocabulary* (key terms) from technical documents.
Return a compact JSON list of seed term objects with fields:
- term (string, human readable)
- symbol (string or array, optional)
- aliases (array of strings, optional)
- brief_definition (1-3 sentences)
Pick only terms that are central to the document's thesis (8–15 typical)."""

EXPAND_TERM_SYS = """You are writing a formal dictionary entry for the Pirouette Framework.
Given:
- a seed term
- one source module's content
- previously seen entry (optional)

Produce a JSON object that adheres to the 'Pirouette Dictionary Entry' schema.
Fill all required fields, be precise and operational. When unsure, be explicit about
confidence and keep placeholders minimal (never write 'TBD'—write crisp, falsifiable hooks).
Use house style consistent with examples.
"""

def extract_core_terms(model, module_name: str, module_text: str, max_terms: int) -> List[Dict[str, Any]]:
    prompt = f"""{EXTRACT_TERMS_SYS}

DOCUMENT: {module_name}
---
{module_text[:18000]}
---
TASK:
1) Identify the core vocabulary.
2) Return ONLY JSON (no prose), like:
[
  {{"term":"Temporal Pressure","symbol":"Γ","aliases":["Gladiator Force"],"brief_definition":"..."}}
]"""
    resp = model.generate_content(prompt)
    raw = "".join(getattr(p, "text", "") for p in getattr(resp, "parts", []))
    # heuristically find the JSON array
    m = re.search(r"\[.*\]", raw, flags=re.S)
    if not m:
        return []
    try:
        items = json.loads(m.group(0))
        if isinstance(items, list):
            if max_terms > 0:
                items = items[:max_terms]
            return items
    except Exception:
        pass
    return []

def expand_term_entry(model, seed: Dict[str, Any], module_id: str, module_text: str) -> Dict[str, Any]:
    term = seed.get("term", "").strip()
    symbol = seed.get("symbol", "")
    aliases = seed.get("aliases", [])
    brief = seed.get("brief_definition", "")

    prompt = f"""{EXPAND_TERM_SYS}

SEED:
{json.dumps(seed, ensure_ascii=False, indent=2)}

GUIDANCE:
- 'triad' must be vivid but precise.
- Provide at least one measurement procedure with expected signals & pitfalls.
- Provide 1–3 'formal_mappings.candidates' with confidence numbers.
- Add 'constraints_and_falsifiers.claims' with test ideas.
- Set 'status' to "draft" and 'version' to "0.1".
- 'last_updated' must be today's date (YYYY-MM-DD).
- Include a 'provenance.sources' entry pointing to this module_id.

MODULE_ID: {module_id}
MODULE_CONTENT:
{module_text[:18000]}

OUTPUT:
Return ONLY a single JSON object following the schema.
"""
    resp = model.generate_content(prompt)
    raw = "".join(getattr(p, "text", "") for p in getattr(resp, "parts", []))
    # heuristically grab outermost JSON object
    m = re.search(r"\{.*\}\s*$", raw, flags=re.S)
    if not m:
        raise ValueError("Model did not return a JSON object.")
    return json.loads(m.group(0))

# ---------- Merge Helpers ----------
def merge_entries(existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """Merge context_windows & provenance; prefer existing for term-level identity."""
    merged = dict(existing)
    # provenance.sources
    p_src = merged.setdefault("provenance", {}).setdefault("sources", [])
    for s in new.get("provenance", {}).get("sources", []):
        if s not in p_src:
            p_src.append(s)
    # context_windows
    cw = merged.setdefault("context_windows", [])
    for w in new.get("context_windows", []):
        if w not in cw:
            cw.append(w)
    # unions for arrays
    def u(key):
        if key in new and isinstance(new[key], list):
            old = set(merged.get(key, []))
            merged[key] = list(old.union(new[key]))
    for key in ["aliases", "parents", "children", "provenance"].copy():
        pass  # already handled where needed
    return merged

# ---------- Validation ----------
def validate_against_schema(entry: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    if not HAS_JSONSCHEMA:
        return []
    try:
        jsonschema.validate(instance=entry, schema=schema)
        return []
    except jsonschema.ValidationError as e:
        return [f"{e.message} at path {'/'.join(str(p) for p in e.path)}"]

# ---------- Markdown Serialization ----------
def entry_to_frontmatter(entry: Dict[str, Any]) -> str:
    # Minimal YAML from selected keys (stable & readable). Full fidelity kept in JSON sidecar.
    keys = ["term","canonical_id","symbol","aliases","parents","children",
            "status","version","last_updated","provenance","triad","pirouette_definition",
            "operational_definition","context_windows","poetic_connections",
            "formal_mappings","constraints_and_falsifiers","naming_notes","crosslinks","license"]
    serial = {k: entry.get(k) for k in keys if k in entry}
    # YAML without external deps
    def to_yaml(o, indent=0):
        sp = "  " * indent
        if isinstance(o, dict):
            lines = []
            for k,v in o.items():
                if v is None: continue
                if isinstance(v,(dict,list)):
                    lines.append(f"{sp}{k}:")
                    lines.append(to_yaml(v, indent+1))
                else:
                    v_str = json.dumps(v, ensure_ascii=False) if isinstance(v, (str,int,float)) and ("\n" in str(v)) else v
                    if isinstance(v, str) and ("\n" in v):
                        # block scalar
                        lines.append(f"{sp}{k}: |")
                        for ln in v.splitlines():
                            lines.append(f"{sp}  {ln}")
                    else:
                        lines.append(f"{sp}{k}: {json.dumps(v, ensure_ascii=False) if not isinstance(v, (int,float)) and not isinstance(v, str) else v}")
            return "\n".join(lines)
        elif isinstance(o, list):
            return "\n".join(f"{sp}- {to_yaml(i,0) if not isinstance(i,str) else i}" for i in o)
        else:
            return f"{sp}{o}"
    return f"---\n{to_yaml(serial)}\n---\n"

def render_markdown_entry(entry: Dict[str, Any], template_text: str) -> str:
    # 1) YAML frontmatter synthesized from entry
    fm = entry_to_frontmatter(entry)
    # 2) Body using your template placeholders (e.g., {term}, {pirouette_definition})
    body = render_template(template_text, entry)
    return fm + "\n" + body.strip() + "\n"

# ---------- Main ----------
def main():
    ap = argparse.ArgumentParser(description="Build Pirouette dictionary entries per term from modules.")
    ap.add_argument("modules_dir", help="Path to directory with *.md modules")
    ap.add_argument("--out_terms", default="./terms", help="Directory to write term files")
    ap.add_argument("--template", default="./term_template.md", help="Path to term template markdown")
    ap.add_argument("--schema", default="./term_entry.schema.json", help="Path to term JSON schema")
    ap.add_argument("--limit", type=int, default=0, help="Max modules to process (0 = all)")
    ap.add_argument("--per_module_cap", type=int, default=12, help="Max terms extracted per module (0 = no cap)")
    args = ap.parse_args()

    # API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = get_model()

    modules_dir = Path(args.modules_dir)
    module_files = sorted([p for p in modules_dir.glob("*.md") if not p.name.lower().startswith("readme")])
    if args.limit > 0:
        module_files = module_files[:args.limit]

    # Template & schema
    template_text = read_text(Path(args.template))
    schema = {}
    try:
        schema = json.loads(read_text(Path(args.schema)))
    except Exception:
        pass

    print(f"Found {len(module_files)} modules.")
    terms_out_dir = Path(args.out_terms)
    json_out_dir = terms_out_dir / "json"

    # Global term index to merge duplicates
    index: Dict[str, Dict[str, Any]] = {}
    today = datetime.today().strftime("%Y-%m-%d")

    for mod_path in module_files:
        module_text = read_text(mod_path)
        module_id = mod_path.stem
        print(f"[scan] {mod_path.name}")

        seeds = extract_core_terms(model, mod_path.name, module_text, args.per_module_cap)
        if not seeds:
            print("  -> no seeds returned")
            continue

        for seed in seeds:
            term = seed.get("term", "").strip()
            if not term:
                continue
            canonical_id = to_canonical_id(term)
            try:
                expanded = expand_term_entry(model, seed, module_id, module_text)
            except Exception as e:
                print(f"  -> skip '{term}': {e}")
                continue

            # Ensure canonical_id present/consistent
            expanded["term"] = expanded.get("term", term)
            expanded["canonical_id"] = expanded.get("canonical_id", canonical_id)
            # Ensure last_updated is today if absent
            expanded["last_updated"] = expanded.get("last_updated", today)

            # Merge with existing if seen before
            if canonical_id in index:
                merged = merge_entries(index[canonical_id], expanded)
                index[canonical_id] = merged
            else:
                index[canonical_id] = expanded

    # Write out entries
    wrote = 0
    for cid, entry in index.items():
        # Validate
        errs = validate_against_schema(entry, schema) if schema else []
        if errs:
            print(f"[warn] {cid} schema issues: " + " | ".join(errs))

        # Render
        md_text = render_markdown_entry(entry, template_text)
        md_path = terms_out_dir / f"{cid}.md"
        json_path = json_out_dir / f"{cid}.json"

        write_text(md_path, md_text)
        write_json(json_path, entry)
        wrote += 1

    print(f"Done. Wrote {wrote} term entries to {terms_out_dir.resolve()}")

if __name__ == "__main__":
    main()
