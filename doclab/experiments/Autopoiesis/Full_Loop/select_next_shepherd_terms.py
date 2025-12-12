#!/usr/bin/env python3
"""
select_next_shepherd_terms.py

Combine loneliness (fill the framework)
with shepherd alignment (serve the goal)
and produce the next N items to emit stubs for.

priority = wL * loneliness + wS * shepherd_alignment
"""

import argparse
import json
from pathlib import Path

def load_json_safe(path: str):
    p = Path(path)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lonely", default="lonely_rank.json")
    ap.add_argument("--shepherd-align", default="shepherd_alignment.json")
    ap.add_argument("--out", default="next_seeds.json")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--w-lonely", type=float, default=0.6)
    ap.add_argument("--w-shepherd", type=float, default=0.4)
    args = ap.parse_args()

    lonely = load_json_safe(args.lonely)
    aligned = load_json_safe(args.shepherd_align)

    align_map = {a["id"]: a["score"] for a in aligned}

    scored = []
    for item in lonely:
        mid = item["id"]
        lscore = float(item.get("loneliness", item.get("score", 0.0)))
        sscore = float(align_map.get(mid, 0.0))
        priority = args.w_lonely * lscore + args.w_shepherd * sscore
        scored.append({
            "id": mid,
            "priority": priority,
            "loneliness": lscore,
            "shepherd_alignment": sscore,
            "path": item.get("path", ""),
        })

    scored.sort(key=lambda x: x["priority"], reverse=True)
    Path(args.out).write_text(json.dumps(scored[: args.top], indent=2), encoding="utf-8")
    print(f"[shepherd-select] wrote {min(args.top, len(scored))} seeds to {args.out}")

if __name__ == "__main__":
    main()
