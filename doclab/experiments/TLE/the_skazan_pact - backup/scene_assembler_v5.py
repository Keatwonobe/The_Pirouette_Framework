#!/usr/bin/env python3
"""
scene_assembler_v5.py

Modernized to match newer TLE/Pirouette JSONs.

- supports old format:
    {
      "players": [...],
      "enemies": [...]
    }

- supports new format:
    {
      "sides": {
        "players": [...],
        "hostiles": [...],
        "npcs": [...]
      }
    }

- roster lookup now checks: id -> character_id -> name
- can assemble from a single encounter file OR every encounter in a directory
"""

import os
import sys
import json
import argparse

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ROSTER_DIR = os.path.join(BASE_DIR, "roster")
INIT_DIR   = os.path.join(BASE_DIR, "initiative")

def ensure_dir(p):
    if not os.path.isdir(p):
        os.makedirs(p, exist_ok=True)

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

def load_roster_files():
    """index roster by several possible keys"""
    idx = {
        "by_id": {},
        "by_character_id": {},
        "by_name": {}
    }
    if not os.path.isdir(ROSTER_DIR):
        return idx
    for fn in os.listdir(ROSTER_DIR):
        if not fn.endswith(".json"):
            continue
        full = os.path.join(ROSTER_DIR, fn)
        try:
            data = load_json(full)
        except Exception:
            continue
        # index
        rid  = data.get("id")
        cid  = data.get("character_id")
        name = data.get("name")
        if rid:
            idx["by_id"][rid] = (full, data)
        if cid:
            idx["by_character_id"][cid] = (full, data)
        if name:
            idx["by_name"][name] = (full, data)
    return idx

def roster_lookup(idx, key):
    """try id → character_id → name"""
    if key in idx["by_id"]:
        return idx["by_id"][key]
    if key in idx["by_character_id"]:
        return idx["by_character_id"][key]
    if key in idx["by_name"]:
        return idx["by_name"][key]
    return None, None

def make_iterated_id(base_id: str, idx: int) -> str:
    if "-" in base_id:
        prefix, last = base_id.rsplit("-", 1)
        if last.isdigit():
            return f"{prefix}-{idx:03d}"
    return f"{base_id}-{idx:03d}"

def _write_init_entry(char_data, out_id, x, y):
    char_data = json.loads(json.dumps(char_data))  # deep copy
    # normalize field name to what your runner expects
    char_data["character_id"] = out_id
    char_data.setdefault("position", {})
    char_data["position"]["x"] = x
    char_data["position"]["y"] = y
    out_path = os.path.join(INIT_DIR, f"{out_id}.json")
    save_json(out_path, char_data)
    print(f"[OK] initiative <- {out_id} at ({x},{y})")

def assemble_from_encounter_dict(scene: dict, roster_index: dict):
    """
    Handles both old and new formats
    """
    ensure_dir(ROSTER_DIR)
    ensure_dir(INIT_DIR)
    clear_initiative()

    # --- players / hostiles extraction
    players = []
    enemies = []

    if "sides" in scene:
        sides = scene["sides"]
        players = sides.get("players", [])
        enemies = sides.get("hostiles", []) + sides.get("enemies", [])
        # npcs we can add later if you want
    else:
        players = scene.get("players", [])
        enemies = scene.get("enemies", [])

    # positions (optional)
    start_pos = scene.get("starting_positions", {})

    # players: default x=0, y increments
    py = 0
    for entry in players:
        if isinstance(entry, str):
            pid = entry
            x, y = 0, py
        else:
            pid = entry.get("id") or entry.get("character_id") or entry.get("name")
            x = entry.get("x", 0)
            y = entry.get("y", py)

        src_path, data = roster_lookup(roster_index, pid)
        if not src_path:
            print(f"[WARN] player '{pid}' not found in ./roster")
            continue

        data["player"] = True
        # override with encounter starting_positions if present
        if pid in start_pos:
            x = start_pos[pid]["x"]
            y = start_pos[pid]["y"]
        _write_init_entry(data, pid, x, y)
        py += 1

    # enemies: default x=6, y increments
    ey_default = 0
    for entry in enemies:
        # new-style might already be a plain string ("en_wheat_wolf#1")
        if isinstance(entry, str):
            base_id = entry
            count = 1
            x = 6
            y = ey_default
        else:
            base_id = entry.get("id") or entry.get("character_id") or entry.get("name")
            count = entry.get("count", 1)
            x = entry.get("x", 6)
            y = entry.get("y", ey_default)

        # strip instance tag if someone wrote en_wheat_wolf#3 in encounter
        base_id_clean = base_id.split("#")[0]

        src_path, data = roster_lookup(roster_index, base_id_clean)
        if not src_path:
            print(f"[WARN] enemy '{base_id_clean}' not found in ./roster")
            continue

        for i in range(1, count + 1):
            if i == 1:
                out_id = base_id
                out_y = y
            else:
                out_id = make_iterated_id(base_id_clean, i)
                out_y = y + (i - 1)
            # override with encounter starting_positions if present
            if out_id in start_pos:
                x = start_pos[out_id]["x"]
                out_y = start_pos[out_id]["y"]
            _write_init_entry(data, out_id, x, out_y)
        ey_default = max(ey_default, y + count)

    print("[scene-assembler] done.")

def main():
    parser = argparse.ArgumentParser(description="Assemble initiative from roster + encounter JSON(s).")
    parser.add_argument("--encounter", "-e", help="Path to encounter JSON", default=None)
    parser.add_argument("--encounter-dir", "-E", help="Directory of encounter JSONs", default=None)
    args = parser.parse_args()

    roster_index = load_roster_files()

    if args.encounter_dir:
        enc_dir = os.path.abspath(args.encounter_dir)
        if not os.path.isdir(enc_dir):
            print(f"[ERR] encounter-dir '{enc_dir}' not found.")
            sys.exit(1)
        # assemble last one only? let's assemble the first for now, or all of them
        for fn in os.listdir(enc_dir):
            if not fn.endswith(".json"):
                continue
            path = os.path.join(enc_dir, fn)
            print(f"[scene-assembler] assembling from {path}")
            data = load_json(path)
            assemble_from_encounter_dict(data, roster_index)
        sys.exit(0)

    if args.encounter:
        enc_path = os.path.abspath(args.encounter)
        if not os.path.isfile(enc_path):
            print(f"[ERR] encounter file '{enc_path}' not found.")
            sys.exit(1)
        data = load_json(enc_path)
        assemble_from_encounter_dict(data, roster_index)
    else:
        print("Provide --encounter path or --encounter-dir to assemble.")
        sys.exit(1)

if __name__ == "__main__":
    main()
