#!/usr/bin/env python3
"""
scene_assembler.py

Forces ./initiative/ to match a scene blueprint by copying JSONs
from ./roster/ and renaming duplicates.

Workflow:
1. Put all master NPC/PC JSONs in ./roster
2. Edit SCENE_BLUEPRINT below
3. run:  python scene_assembler.py
4. then run your combat script (march_pressure_test, shadow_theater, etc.)
"""

import os
import json
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROSTER_DIR = os.path.join(BASE_DIR, "roster")
INIT_DIR   = os.path.join(BASE_DIR, "initiative")

# --------------------------------------------------------------------
# 1) Define the scene you want to assemble
# --------------------------------------------------------------------
SCENE_BLUEPRINT = {
    # these must exist in ./roster
    "players": [
        "player-stoneborn-001",
        "player-vinemage-001",
        "player-sparkblade-001",
        "player-necrotist-001"
    ],
    # these must exist in ./roster
    "enemies": [
        {"id": "desert-raider-001", "count": 5},
        {"id": "sand-wraith-001",   "count": 3}
    ]
}

# --------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------
def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def roster_lookup(roster_id):
    """
    Return absolute path to roster JSON with matching "id".
    We don't rely on filename; we read each file and check data["id"].
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

def clear_initiative():
    if not os.path.isdir(INIT_DIR):
        return
    for fn in os.listdir(INIT_DIR):
        full = os.path.join(INIT_DIR, fn)
        if os.path.isfile(full):
            os.remove(full)

def make_iterated_id(base_id: str, idx: int) -> str:
    """
    base_id = "desert-raider-001", idx = 2 → "desert-raider-002"
    we keep the prefix and just change the number at the end.
    If there's no number, we append one.
    """
    # try to split on last dash
    if "-" in base_id:
        prefix, last = base_id.rsplit("-", 1)
        if last.isdigit():
            return f"{prefix}-{idx:03d}"
    # fallback
    return f"{base_id}-{idx:03d}"

# --------------------------------------------------------------------
# main assembler
# --------------------------------------------------------------------
def assemble_scene(scene):
    ensure_dir(ROSTER_DIR)
    ensure_dir(INIT_DIR)

    print(f"[scene-assembler] clearing {INIT_DIR} …")
    clear_initiative()

    # 1) players — 1:1 copies
    for pid in scene.get("players", []):
        src_path, data = roster_lookup(pid)
        if not src_path:
            print(f"[WARN] player '{pid}' not found in ./roster")
            continue
        # write to initiative with same name
        out_path = os.path.join(INIT_DIR, f"{pid}.json")
        # force player flag on
        data["player"] = True
        save_json(out_path, data)
        print(f"[OK] added player {pid}")

    # 2) enemies — may need iteration
    for enemy in scene.get("enemies", []):
        base_id = enemy["id"]
        count   = enemy.get("count", 1)
        src_path, data = roster_lookup(base_id)
        if not src_path:
            print(f"[WARN] enemy '{base_id}' not found in ./roster")
            continue

        for i in range(1, count + 1):
            # first one keeps original id, later ones get incremented
            if i == 1:
                new_id = base_id
            else:
                new_id = make_iterated_id(base_id, i)
            new_data = json.loads(json.dumps(data))  # deep copy
            new_data["id"] = new_id
            # you can also offset positions here so they don't spawn on top of each other
            new_data.setdefault("position", {"x": 6, "y": 0})
            new_data["position"]["x"] = 6
            new_data["position"]["y"] = i - 1  # 0,1,2,...
            out_path = os.path.join(INIT_DIR, f"{new_id}.json")
            save_json(out_path, new_data)
            print(f"[OK] added enemy {new_id}")

    print("[scene-assembler] done.")

# --------------------------------------------------------------------
if __name__ == "__main__":
    assemble_scene(SCENE_BLUEPRINT)
