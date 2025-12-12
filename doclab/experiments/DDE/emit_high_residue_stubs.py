#!/usr/bin/env python3
"""
Emit Pirouette-style module stubs for the "neediest" spots in the atlas.
This assumes DDE_Pirouette.py defines:
    - DDEPirouette
    - IdeaManifoldSurveyor   (the thing you just integrated)
"""

import argparse
from pathlib import Path
from datetime import datetime

# import from your big file
from DDE_Pirouette import IdeaManifoldSurveyor


TEMPLATE = """---
id: {id}
title: {title}
version: {version}
domain: {domain}
status: draft
parents: {parents}
created_at: {created_at}
origin_tile: ({x},{y})
score: {score:.4f}
engram:
  - inst:auth-map-001
  - dde:auto-emitted
  - origin:({x},{y})
---
## Purpose
Automatic bridge module emitted by DDE-Pirouette's idea-manifold survey
to reduce local dark residue and increase neighbor coherence.

## Context
This tile scored high on dark residue or low neighbor density relative to the atlas.
Existing module here: {existing}

## Task
Describe the missing connective tissue between this module and its immediate neighbors.
Specify:
- Γ/Ki deltas to be resolved
- expected temporal adherence (Tₐ)
- closure style (core, dome, or lattice-bridging)
- validation path for this bridge

## Notes
This stub was generated for API content streams; safe to expand.
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--atlas", required=True,
                        help="path to dde_glob_manifest_modules_outbox.json")
    parser.add_argument("--out", default="stubs_out.txt",
                        help="where to write the emitted stubs")
    parser.add_argument("--top", type=int, default=5,
                        help="how many stubs to emit")
    parser.add_argument("--neighbor-radius", type=int, default=1,
                        help="radius for void detection in surveyor")
    args = parser.parse_args()

    surveyor = IdeaManifoldSurveyor(
        atlas_json_path=args.atlas,
        neighbor_radius=args.neighbor_radius,
    )

    print(f"DEBUG: Surveyor loaded {len(surveyor.locations)} module locations.")

    # run the surveyor you added inside the DDE file
    voids = surveyor.find_voids(min_neighbors=5)

    print(f"DEBUG: Surveyor find_voids() returned {len(voids)} potential voids.")

    # keep only the top N by score
    top_voids = voids[: args.top]

    lines = []
    for rank, (x, y, score) in enumerate(top_voids):
        # try to name the existing module at this tile
        existing_id = None
        for mid, loc in surveyor.locations.items():
            if loc["x"] == x and loc["y"] == y:
                existing_id = mid
                break

        if existing_id:
            stub_id = f"{existing_id}_AUTH-BRIDGE"
            parents = [existing_id]
        else:
            stub_id = f"AUTH-VOID-{x:02d}-{y:02d}"
            parents = []

        txt = TEMPLATE.format(
            id=stub_id,
            title=f"Idea Manifold Bridge near ({x},{y})",
            version="0.1-dde",
            domain="INST-AUTH-MAP",
            parents=parents,
            created_at=datetime.utcnow().isoformat(),
            x=x,
            y=y,
            score=score,
            existing=existing_id or "∅",
        )
        lines.append(txt.strip() + "\n")

    out_path = Path(args.out)
    out_path.write_text("\n\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(lines)} stubs to {out_path}")


if __name__ == "__main__":
    main()
