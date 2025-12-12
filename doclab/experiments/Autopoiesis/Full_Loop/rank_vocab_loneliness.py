#!/usr/bin/env python3
"""
Rank vocab terms (markdown files) by "loneliness" so we can
ask DDE / the authoring loop to generate connecting modules
or more definitions.

Assumes files like ACTION.md, ACCELERATION.md, ... in one folder,
with sections like:
- term:
- canonical_id:
- parents: [...]
- children: [...]
- prerequisites: [...]
- downstream_effects: [...]
- association_matrix: [ ["LAGRANGIAN_DENSITY", 0.9], ... ]

This is based on the example files the user showed. :contentReference[oaicite:3]{index=3} :contentReference[oaicite:4]{index=4} :contentReference[oaicite:5]{index=5}
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple


# very forgiving YAML-ish field capture
FIELD_RE = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")


def parse_vocab_file(path: Path) -> Dict[str, Any]:
    """
    Very forgiving parser for your term markdowns.

    Handles:
    term: ACTION
    parents:
      - DOMA-025
      - DOMA-169
    association_matrix:
      - ["LAGRANGIAN_DENSITY", 0.9]
    """
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    data: Dict[str, Any] = {
        "_file": str(path),
        "_raw": text,
    }

    current_key = None
    for line in lines:
        s = line.rstrip()

        # key: value on one line
        m = FIELD_RE.match(s)
        if m:
            key = m.group(1)
            val = m.group(2)
            current_key = key

            # list on one line: key: [a, b, c]
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                if inner:
                    data[key] = [x.strip() for x in inner.split(",")]
                else:
                    data[key] = []
            elif val == "" or val is None:
                # key:    (expecting list or multiline later)
                data[key] = []
            else:
                data[key] = val.strip()
            continue

        # list continuation: "- item"
        if current_key and s.strip().startswith("- "):
            # make sure current field is a list
            if not isinstance(data.get(current_key), list):
                data[current_key] = [] if data.get(current_key) in ("", None) else [data[current_key]]
            data[current_key].append(s.strip()[2:].strip())

    return data


def extract_assoc_targets(data: Dict[str, Any]) -> List[str]:
    """pulls target IDs from association_matrix if present"""
    text = data.get("_raw", "")
    # looks like: - [ "LAGRANGIAN_DENSITY", 0.9 ]
    matches = re.findall(r'\[\s*"([^"]+)"\s*,\s*([0-9.]+)\s*\]', text)
    return [m[0] for m in matches]


def loneliness_for_term(
    term_id: str,
    data: Dict[str, Any],
    all_ids: set,
    w_struct: float = 0.6,
    w_assoc: float = 0.25,
    w_draft: float = 0.1,
    w_no_alias: float = 0.05,
) -> float:
    # structural links
    struct_fields = ["parents", "children", "prerequisites", "downstream_effects"]
    missing_struct = 0
    total_struct = 0
    for f in struct_fields:
        vals = data.get(f, [])
        if isinstance(vals, str):
            vals = [vals]
        for v in vals:
            total_struct += 1
            if v not in all_ids:
                missing_struct += 1

    struct_term = (missing_struct / total_struct) if total_struct else 1.0

    # association links
    assoc_targets = extract_assoc_targets(data)
    missing_assoc = sum(1 for t in assoc_targets if t not in all_ids)
    assoc_term = (missing_assoc / len(assoc_targets)) if assoc_targets else 0.0

    # draft bonus
    draft_term = 1.0 if str(data.get("status", "")).lower() == "draft" else 0.0

    # alias bonus
    aliases = data.get("aliases", [])
    if isinstance(aliases, str) and aliases:
        aliases = [aliases]
    no_alias_term = 1.0 if not aliases else 0.0

    score = (
        w_struct * struct_term
        + w_assoc * assoc_term
        + w_draft * draft_term
        + w_no_alias * no_alias_term
    )
    return score


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--vocab-dir", required=False, default="C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/modules/dictionary")
    ap.add_argument("--out", default="vocab_lonely.json")
    args = ap.parse_args()

    vocab_dir = Path(args.vocab_dir)
    terms: Dict[str, Dict[str, Any]] = {}

    for p in vocab_dir.glob("*.md"):
        data = parse_vocab_file(p)
        # prefer canonical_id, fall back to term, fall back to filename
        term_id = data.get("canonical_id") or data.get("term") or p.stem
        terms[term_id] = data

    all_ids = set(terms.keys())

    ranked: List[Tuple[str, float]] = []
    for tid, data in terms.items():
        score = loneliness_for_term(tid, data, all_ids)
        ranked.append((tid, score))

    ranked.sort(key=lambda x: x[1], reverse=True)

    out_list = []
    for tid, score in ranked:
        out_list.append(
            {
                "id": tid,
                "score": score,
                "path": terms[tid]["_file"],
            }
        )

    Path(args.out).write_text(json.dumps(out_list, indent=2), encoding="utf-8")
    print(f"wrote {len(out_list)} vocab terms to {args.out}")


if __name__ == "__main__":
    main()
