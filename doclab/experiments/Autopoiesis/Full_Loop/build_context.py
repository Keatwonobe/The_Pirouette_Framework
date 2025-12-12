#!/usr/bin/env python3
"""
Context builder for Pirouette autopoiesis.

Given:
- pirouette_dict.dictpack   (JSON or pickle)
- essentialized_pirouette.md (big compiled file of ## Law / ## Philosophy / ## Art)
- a stub text (emitted by your DDE loop)

…build a context payload to send to the API author.
"""

import json
import pickle
import re
import gzip
from pathlib import Path
from typing import Dict, Any, List, Optional


FRONTMATTER_RE = re.compile(r"^---\s*(.*?)---\s*", re.DOTALL | re.MULTILINE)

def extract_term_payload(md_text: str) -> str:
    """
    Given one of your vocab markdowns, pull out the actual definition-y bit.
    Priority:
      1. pirouette_definition: ...
      2. operational_definition: ...
      3. first '## ' section body
    """
    # strip frontmatter if present
    m = FRONTMATTER_RE.match(md_text)
    if m:
        md_text = md_text[m.end():]

    # 1) pirouette_definition: |
    m = re.search(r"pirouette_definition:\s*\|([\s\S]+?)(\n[a-zA-Z_]+:|\Z)", md_text)
    if m:
        return m.group(1).strip()

    # 2) operational_definition:
    m = re.search(r"operational_definition:\s*\|([\s\S]+?)(\n[a-zA-Z_]+:|\Z)", md_text)
    if m:
        return m.group(1).strip()

    # 3) first markdown section
    m = re.search(r"^##\s+(.+)$([\s\S]+?)(^##\s+|\Z)", md_text, re.MULTILINE)
    if m:
        return m.group(2).strip()

    # fallback: whole thing, but trimmed
    return md_text.strip()

def extract_stub_tokens(stub_text: str) -> list[str]:
    """
    Pulls useful tokens out of a stub:
    - ID parts (XXP, CORE, KI, PULSARS)
    - domain
    - shepherd context
    Returns lowercased tokens.
    """
    tokens = set()

    # from id/title lines
    m = re.search(r"id:\s*([A-Za-z0-9_\-]+)", stub_text)
    if m:
        parts = re.split(r"[_\-]+", m.group(1))
        tokens.update(p.lower() for p in parts if p)

    m = re.search(r"title:\s*(.+)", stub_text)
    if m:
        parts = re.split(r"[\s_\-]+", m.group(1))
        tokens.update(p.lower() for p in parts if p)

    # domain
    m = re.search(r"domain:\s*([A-Za-z0-9_\-]+)", stub_text)
    if m:
        tokens.add(m.group(1).lower())

    # shepherd context
    m = re.search(r"shepherd_context:\s*([A-Za-z0-9_\-]+)", stub_text)
    if m:
        tokens.add(m.group(1).lower())

    return list(tokens)

def load_essentialized_dir(path: str | Path) -> dict[str, str]:
    """
    Load essentialized modules from a directory of *.md files.
    Key them by lowercased stem for fuzzy lookup.
    """
    path = Path(path)
    out = {}
    for p in path.glob("*.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        stem = p.stem.lower()
        out[stem] = text
    return out

def pick_relevant_essentialized_from_map(stub_text: str, ess_map: dict[str, str], limit: int = 3) -> list[str]:
    """
    Fuzzy-match essentialized modules to the stub tokens.
    """
    tokens = extract_stub_tokens(stub_text)
    picked = []
    for key, val in ess_map.items():
        if any(tok in key for tok in tokens):
            picked.append(val)
            if len(picked) >= limit:
                return picked
    # fallback: grab some core ones if nothing matched
    if not picked:
        for key, val in ess_map.items():
            if key.startswith("core-") or "pirouette" in key:
                picked.append(val)
                if len(picked) >= limit:
                    break
    return picked


def load_dictpack_markdown_dir(dirpath: str | Path) -> dict[str, str]:
    """
    If your 'dictpack' is actually 'a bunch of term .md files in a folder', use this.
    """
    dirpath = Path(dirpath)
    out = {}
    for p in dirpath.glob("*.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        term_id = p.stem.upper()
        payload = extract_term_payload(text)
        out[term_id] = payload
    return out


def load_essentialized(path: str | Path) -> Dict[str, str]:
    """
    Parse the big essentialized_pirouette.md into a {name: text} map.

    This assumes headings like:
    ## COG-RES-001_essentialized.md
    ## CORE-001_the_pirouette_seed_essentialized.md
    …which is what you showed. :contentReference[oaicite:2]{index=2}
    """
    path = Path(path)
    if not path.exists():
        print(f"[context] essentialized file missing at {path}")
        return {}
    text = path.read_text(encoding="utf-8")

    # split on '## ' headers
    blocks = re.split(r"^##\s+", text, flags=re.MULTILINE)
    essentialized: Dict[str, str] = {}
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # first line is name
        first_line, *rest = block.splitlines()
        name = first_line.strip()
        body = "\n".join(rest).strip()
        # normalize name (strip .md if present)
        name = name.replace(".md", "")
        essentialized[name] = body
    return essentialized


def pick_relevant_essentialized(
    stub_text: str,
    essentialized_map: Dict[str, str],
    limit: int = 3,
) -> List[str]:
    """
    Very cheap relevance: look for module IDs mentioned in stub,
    then fall back to CORE-*.
    """
    stub_low = stub_text.lower()
    hits: List[str] = []

    # exact ID mentions
    for name in essentialized_map.keys():
        # compare simplified names
        needle = name.lower()
        if needle in stub_low:
            hits.append(name)
        if len(hits) >= limit:
            break

    if len(hits) < limit:
        # pad with CORE-* because those are your axioms
        for name in essentialized_map.keys():
            if name.startswith("CORE-") and name not in hits:
                hits.append(name)
            if len(hits) >= limit:
                break

    return [essentialized_map[h] for h in hits if h in essentialized_map]


def pick_relevant_dict_entries(stub_text: str, dictpack: dict[str, str], limit: int = 5) -> dict[str, str]:
    """
    Fuzzy match: if any token from the stub appears inside a dict key,
    take that entry. Falls back to a couple of generic entries.
    """
    if not dictpack:
        return {}

    stub_tokens = extract_stub_tokens(stub_text)
    picked = {}

    # 1) token-based matches
    for key, val in dictpack.items():
        key_low = key.lower()
        if any(tok in key_low for tok in stub_tokens):
            picked[key] = val
            if len(picked) >= limit:
                return picked

    # 2) fallback: grab some high-value generic terms, if present
    for generic in ("pirouette", "lagrangian", "closure", "manifold"):
        for key, val in dictpack.items():
            if key.lower().startswith(generic) and key not in picked:
                picked[key] = val
                if len(picked) >= limit:
                    return picked

    return picked



def build_context_blob(
    stub_text: str,
    dict_entries: Dict[str, Any],
    essentialized_chunks: List[str],
) -> str:
    """
    Assemble a single markdown-ish blob to give to the model.
    """
    parts = []
    parts.append("# PIRouette Authoring Context")
    parts.append("## Current Stub")
    parts.append(stub_text.strip())
    if dict_entries:
        parts.append("## Dictionary")
        for k, v in dict_entries.items():
            parts.append(f"- **{k}**: {v}")
    if essentialized_chunks:
        parts.append("## Canonical Essentials")
        for ch in essentialized_chunks:
            parts.append(ch.strip())
            parts.append("\n")
    return "\n\n".join(parts)


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--stub", required=True, help="path to stub .md file emitted by the loop")
    # this can be EITHER a folder of .md terms OR a single .md with terms appended
    ap.add_argument("--dictpack", default="pirouette_dictionary_markdown.md")
    ap.add_argument("--essentialized", default="essentialized_pirouette.md")
    ap.add_argument("--out", default="context_out.txt")
    args = ap.parse_args()

    # 1) stub
    stub_text = Path(args.stub).read_text(encoding="utf-8")

    # 2) dictionary terms (markdown form)
    # if args.dictpack is a dir, we'll load every *.md in it
    dictpack = load_dictpack_markdown_dir(args.dictpack)

    # 3) essentialized corpus
    ess_path = Path(args.essentialized)
    if ess_path.is_dir():
        ess_map = load_essentialized_dir(ess_path)
        ess_chunks = pick_relevant_essentialized_from_map(stub_text, ess_map)
    else:
        ess_map = load_essentialized(ess_path)
        ess_chunks = pick_relevant_essentialized(stub_text, ess_map)     # 4) pick 2–3 essentialized modules


    # 5) now actually FILTER the dict by what’s in the stub
    dict_entries = pick_relevant_dict_entries(stub_text, dictpack)



    # 6) assemble context
    blob = build_context_blob(stub_text, dict_entries, ess_chunks)
    Path(args.out).write_text(blob, encoding="utf-8")
    print(f"[context] wrote {args.out}")


if __name__ == "__main__":
    main()

