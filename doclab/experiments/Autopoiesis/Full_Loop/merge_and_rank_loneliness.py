#!/usr/bin/env python3
"""
Merge old Pirouette corpus and new auto-v7 corpus,
then rank everything by "loneliness" so the framework
can pick what to grow next.

- de-dupes by title/id
- uses atlas to measure neighbor count
- uses v7 header to read dark_residue
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple

# ---------- helpers ----------

YAML_RE = re.compile(r"^---\s*(.*?)---\s*", re.DOTALL | re.MULTILINE)

def load_atlas(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    # handle minified version you used
    if "meta_map" in data and "data" in data:
        # if you kept the rehydrate helper, you could call that here
        data = data["data"]
    return data

def parse_yaml_header(text: str) -> Dict[str, Any]:
    m = YAML_RE.match(text)
    if not m:
        return {}
    raw = m.group(1)
    # very small YAML-ish parser: key: value, no nesting
    header = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            header[k.strip()] = v.strip()
    return header

def load_md_dir(path: str) -> Dict[str, Dict[str, Any]]:
    """
    returns {id_or_title: {"header":..., "text":...}}
    """
    out = {}
    for p in Path(path).glob("*.md"):
        text = p.read_text(encoding="utf-8")
        hdr = parse_yaml_header(text)
        module_id = hdr.get("id") or hdr.get("title") or p.stem
        out[module_id] = {"header": hdr, "text": text, "path": str(p)}
    return out

def get_atlas_neighbors(atlas: dict, module_id: str, radius: int = 1) -> int:
    locs = atlas.get("locations", {})
    if module_id not in locs:
        return 0
    x = locs[module_id]["x"]
    y = locs[module_id]["y"]
    # count occupied tiles in radius
    cnt = 0
    for mid, loc in locs.items():
        if mid == module_id:
            continue
        if abs(loc["x"] - x) <= radius and abs(loc["y"] - y) <= radius:
            cnt += 1
    return cnt

def loneliness_score(
    atlas: dict,
    module_id: str,
    header: Dict[str, Any],
    all_ids: set,
    max_neighbors: int = 8,
    w_neighbors: float = 0.6,
    w_residue: float = 0.3,
    w_parent: float = 0.4,
) -> float:
    # 1) neighbors
    neighbors = get_atlas_neighbors(atlas, module_id)
    neighbor_term = max(0, max_neighbors - neighbors)

    # 2) residue
    # v7: header has resonance.dark_residue, but we only parsed 1-level YAML
    # so fall back to 'dark_residue' or 0
    residue = 0.0
    for k in ("dark_residue", "resonance.dark_residue"):
        if k in header:
            try:
                residue = float(header[k])
                break
            except Exception:
                pass

    # 3) parent missing
    parent_term = 0.0
    parents = header.get("parents")
    if parents:
        # parents could be like "['CORE-006', '...']"
        if isinstance(parents, str):
            # try to pull ids out of brackets
            ps = re.findall(r"[A-Z0-9_\-\.]+", parents)
        else:
            ps = parents
        for p in ps:
            if p not in all_ids:
                parent_term = 1.0
                break

    return (
        w_neighbors * neighbor_term
        + w_residue * residue
        + w_parent * parent_term
    )


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=False, default="C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/output/modules_outbox")
    ap.add_argument("--new", required=False, default="C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/Autopoiesis/Full_Loop/autopoiesis_runs/authored")
    ap.add_argument("--atlas", required=False, default="dde_glob_manifest_modules_outbox.json")
    ap.add_argument("--out", default="lonely_rank.json")
    args = ap.parse_args()

    atlas = load_atlas(args.atlas)
    old_mods = load_md_dir(args.old)
    new_mods = load_md_dir(args.new)

    # merge without dupes (prefer new over old if same id)
    merged = {**old_mods, **new_mods}
    all_ids = set(merged.keys())

    scored: List[Tuple[str, float]] = []
    for mid, obj in merged.items():
        score = loneliness_score(atlas, mid, obj["header"], all_ids)
        scored.append((mid, score))

    scored.sort(key=lambda x: x[1], reverse=True)

    result = []
    for mid, score in scored:
        result.append(
            {
                "id": mid,
                "loneliness": score,
                "path": merged[mid]["path"],
            }
        )

    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"wrote {len(result)} ranked modules to {args.out}")


if __name__ == "__main__":
    main()
