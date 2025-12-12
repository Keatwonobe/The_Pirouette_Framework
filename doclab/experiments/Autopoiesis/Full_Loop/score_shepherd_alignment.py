#!/usr/bin/env python3
"""
score_shepherd_alignment.py

Given a shepherd phrase, scan authored/canon modules
and score them for how aligned they are.

Writes shepherd_alignment.json with {id, score, path}.
"""

from pathlib import Path
import argparse
import json

def score_text(text: str, shepherd: str) -> float:
    t = text.lower()
    s = shepherd.lower().replace("_", " ")
    score = 0.0
    if s in t:
        score += 1.0
    # partial matches
    for part in s.split():
        if part and part in t:
            score += 0.2
    return score

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shepherd", required=True, help="e.g. 'altruism' or 'qed-spine'")
    ap.add_argument("--modules", default="autopoiesis_runs/authored", help="folder with authored .md")
    ap.add_argument("--canon", default="canon", help="also scan canon folder if present")
    ap.add_argument("--out", default="shepherd_alignment.json")
    args = ap.parse_args()

    paths = []
    for folder in (args.modules, args.canon):
        p = Path(folder)
        if p.exists():
            paths.extend(list(p.glob("*.md")))

    results = []
    for p in paths:
        text = p.read_text(encoding="utf-8", errors="ignore")
        score = score_text(text, args.shepherd)
        if score > 0.0:
            results.append({
                "id": p.stem,
                "score": score,
                "path": str(p),
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    Path(args.out).write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"[shepherd-score] wrote {len(results)} aligned modules to {args.out}")

if __name__ == "__main__":
    main()
