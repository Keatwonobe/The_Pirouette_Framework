#!/usr/bin/env python3
"""
scene_assembler_v3.py

Externalized encounters.

Usage:
    python scene_assembler_v3.py --encounter ./encounters/march.json
    python scene_assembler_v3.py --encounter ./encounters/heavy_march.json

If you don’t pass --encounter, it will fall back to built-in BLUEPRINTS like before.
"""

import os
import sys
import json
import argparse

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ROSTER_DIR = os.path.join(BASE_DIR, "roster")
INIT_DIR   = os.path.join(BASE_DIR, "initiative")

# ---------------------------------------------------------------------
# Optional built-in blueprints (fallback)
# ---------------------------------------------------------------------
BLUEPRINTS = {
    "march": {
        "players": [
            "player-stoneborn-001",
            "player-vinemage-001",
            "player-sparkblade-001",
            "player-necrotist-001"
        ],
        "enemies": [
            {"id": "desert-raider-001", "count": 3},
            {"id": "sand-wraith-001",   "count": 1}
        ]
    }
}

DEFAULT_SCENE_NAME = "march"

# ---------------------------------------------------------------------
# utils
# ---------------------------------------------------------------------
def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def clear_initiative():
    if not os.path.isdir(INIT_DIR):
        return
    for fn in os.listdir(INIT_DIR):
        full = os.path.join(INIT_DIR, fn)
        if os.path.isfile(full):
            os.remove(full)

def roster_lookup(roster_id):
    """
    Look through ./roster and return (path, data) whose data["id"] == roster_id.
    """
    for fn in os.listdir(ROSTER_DIR):
        if not fn.endswith(".json"):
            continue
        full = os.path.join(ROSTER_DIR, fn)
        try:
            data = load_json(full)
        except Exception:
            continue
        if data.get("id") == roster_id:
            return full, data
    return None, None

def make_iterated_id(base_id: str, idx: int) -> str:
    # "desert-raider-001" → "desert-raider-002"
    if "-" in base_id:
        prefix, last = base_id.rsplit("-", 1)
        if last.isdigit():
            return f"{prefix}-{idx:03d}"
    return f"{base_id}-{idx:03d}"

# ---------------------------------------------------------------------
# core assembler
# ---------------------------------------------------------------------
def assemble_from_dict(scene: dict):
    """
    scene dict must look like:
    {
      "players": [...],
      "enemies": [...]
    }
    optionally with "stage" or whatever else — we ignore that here.
    """
    ensure_dir(ROSTER_DIR)
    ensure_dir(INIT_DIR)

    print(f"[scene-assembler] clearing {INIT_DIR} …")
    clear_initiative()

    # players: x=0, y increments
    py = 0
    for p in scene.get("players", []):
        # p can be "player-stoneborn-001" or {"id": "player-stoneborn-001", "x":0,"y":0}
        if isinstance(p, str):
            pid = p
            px = 0
            py_override = None
        else:
            pid = p["id"]
            px = p.get("x", 0)
            py_override = p.get("y")

        src_path, data = roster_lookup(pid)
        if not src_path:
            print(f"[WARN] player '{pid}' not found in ./roster")
            continue

        data["player"] = True
        data.setdefault("position", {})
        data["position"]["x"] = px
        data["position"]["y"] = py if py_override is None else py_override
        out_path = os.path.join(INIT_DIR, f"{pid}.json")
        save_json(out_path, data)
        print(f"[OK] added player {pid} at ({data['position']['x']},{data['position']['y']})")
        # only auto-increment if y wasn’t explicitly set
        if py_override is None:
            py += 1

    # enemies: x=6, y increments, unless explicitly set
    for enemy in scene.get("enemies", []):
        base_id = enemy["id"]
        count   = enemy.get("count", 1)
        ex = enemy.get("x", 6)
        ey = enemy.get("y", 0)  # starting y if explicit
        src_path, data = roster_lookup(base_id)
        if not src_path:
            print(f"[WARN] enemy '{base_id}' not found in ./roster")
            continue

        for i in range(1, count + 1):
            if i == 1:
                new_id = base_id
                ny = enemy.get("y", 0)
            else:
                new_id = make_iterated_id(base_id, i)
                # if user specified y, stack down from there; else just i-1
                ny = enemy.get("y", 0) + (i - 1)

            new_data = json.loads(json.dumps(data))  # deep copy
            new_data["id"] = new_id
            new_data.setdefault("position", {})
            new_data["position"]["x"] = enemy.get("x", 6)
            new_data["position"]["y"] = ny
            out_path = os.path.join(INIT_DIR, f"{new_id}.json")
            save_json(out_path, new_data)
            print(f"[OK] added enemy {new_id} at ({new_data['position']['x']},{new_data['position']['y']})")

    print("[scene-assembler] done.")

# ---------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Assemble initiative from roster + encounter JSON.")
    parser.add_argument("--encounter", "-e", help="Path to encounter JSON", default=None)
    parser.add_argument("--blueprint", "-b", help="Name of built-in blueprint", default=None)
    args = parser.parse_args()

    if args.encounter:
        enc_path = os.path.abspath(args.encounter)
        if not os.path.isfile(enc_path):
            print(f"[ERR] encounter file '{enc_path}' not found.")
            sys.exit(1)
        data = load_json(enc_path)
        assemble_from_dict(data)
    else:
        # fallback to built-in blueprint
        name = args.blueprint or DEFAULT_SCENE_NAME
        if name not in BLUEPRINTS:
            print(f"[ERR] blueprint '{name}' not found. Available: {', '.join(BLUEPRINTS.keys())}")
            sys.exit(1)
        assemble_from_dict(BLUEPRINTS[name])

if __name__ == "__main__":
    main()
