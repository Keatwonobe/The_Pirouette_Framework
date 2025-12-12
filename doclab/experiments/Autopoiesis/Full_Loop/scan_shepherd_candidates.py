#!/usr/bin/env python3
"""
scan_shepherd_candidates.py

Look at:
- a vocab folder (markdown terms)
- a canon/modules folder (authored *.md)

and propose shepherd phrases that exist in vocab but not in canon titles.

Usage:
  python scan_shepherd_candidates.py --vocab vocab_terms --canon canon --out shepherd_candidates.json
"""

from pathlib import Path
import argparse
import json
import re

def load_vocab_terms(vocab_dir: Path) -> set[str]:
    terms = set()
    for p in vocab_dir.glob("*.md"):
        terms.add(p.stem.upper())
    return terms

def load_canon_tokens(canon_dir: Path) -> set[str]:
    toks = set()
    for p in canon_dir.glob("*.md"):
        name = p.stem.upper()
        parts = re.split(r"[_\-\s]+", name)
        toks.update(parts)
    return toks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vocab", required=True, help="folder with vocab *.md")
    ap.add_argument("--canon", required=True, help="folder with canon / authored *.md")
    ap.add_argument("--out", default="shepherd_candidates.json")
    args = ap.parse_args()

    vocab_terms = load_vocab_terms(Path(args.vocab))
    canon_tokens = load_canon_tokens(Path(args.canon))

    missing = []
    for term in sorted(vocab_terms):
        # skip very short tokens
        if len(term) < 4:
            continue
        if term not in canon_tokens:
            missing.append(term)

    Path(args.out).write_text(json.dumps(missing, indent=2), encoding="utf-8")
    print(f"[shepherd-scan] wrote {len(missing)} candidates to {args.out}")

if __name__ == "__main__":
    main()
