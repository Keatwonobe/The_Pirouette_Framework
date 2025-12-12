#!/usr/bin/env python3
"""
scene_assembler_v2.py

Usage:
    python scene_assembler_v2.py            # uses DEFAULT_SCENE
    python scene_assembler_v2.py march      # uses "march" blueprint
    python scene_assembler_v2.py embassy    # uses "embassy" blueprint

- Reads from ./roster (master library)
- Writes to ./initiative (live cast)
- Clears initiative first
- Duplicates enemies (desert-raider-001 → ...002, ...003)
- Forces players to have player=true

Drop this next to your other scripts.
"""

import os
import sys
import json

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ROSTER_DIR = os.path.join(BASE_DIR, "roster")
INIT_DIR   = os.path.join(BASE_DIR, "initiative")

# ------------------------------------------------------------
# 1) DECLARE YOUR BLUEPRINTS HERE
# ------------------------------------------------------------
BLUEPRINTS = {
    # the one you just ran successfully
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
    },

    # heavier version you said you wanted to try
    "heavy-march": {
        "players": [
            "player-stoneborn-001",
            "player-vinemage-001",
            "player-sparkblade-001",
            "player-necrotist-001"
        ],
        "enemies": [
            {"id": "desert-raider-001", "count": 5},
            {"id": "sand-wraith-001",   "count": 3}
        ]
    },

    # city/social scene if you ever want a soft board
    "embassy": {
        "players": [
            "player-stoneborn-001",
            "player-vinemage-001",
            "player-sparkblade-001",
            "player-necrotist-001"
        ],
        "enemies": [
            {"id": "skazan-envoy-001",  "count": 1},
            {"id": "skazan-guard-001",  "count": 4}
        ]
    }
}

DEFAULT_SCENE_NAME = "march"

# ------------------------------------------------------------
# helpers
# ------------------------------------------------------------
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
    Find a JSON in ./roster whose internal data["id"] == roster_id.
    We don't rely on filenames.
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
    # base: "desert-raider-001" → "desert-raider-002"
    if "-" in base_id:
        prefix, last = base_id.rsplit("-", 1)
        if last.isdigit():
            return f"{prefix}-{idx:03d}"
    return f"{base_id}-{idx:03d}"

# ------------------------------------------------------------
# main
# ------------------------------------------------------------
def assemble_scene(scene: dict):
    ensure_dir(ROSTER_DIR)
    ensure_dir(INIT_DIR)

    print(f"[scene-assembler] clearing {INIT_DIR} …")
    clear_initiative()

    # players go on the left, we'll give them y = 0..N
    py = 0
    for pid in scene.get("players", []):
        src_path, data = roster_lookup(pid)
        if not src_path:
            print(f"[WARN] player '{pid}' not found in ./roster")
            continue
        data["player"] = True
        data.setdefault("position", {})
        data["position"]["x"] = 0
        data["position"]["y"] = py
        py += 1
        out_path = os.path.join(INIT_DIR, f"{pid}.json")
        save_json(out_path, data)
        print(f"[OK] added player {pid}")

    # enemies go on the right, x=6, y=0..N
    for enemy in scene.get("enemies", []):
        base_id = enemy["id"]
        count   = enemy.get("count", 1)
        src_path, data = roster_lookup(base_id)
        if not src_path:
            print(f"[WARN] enemy '{base_id}' not found in ./roster")
            continue

        for i in range(1, count + 1):
            if i == 1:
                new_id = base_id
            else:
                new_id = make_iterated_id(base_id, i)
            new_data = json.loads(json.dumps(data))  # deep copy
            new_data["id"] = new_id
            new_data.setdefault("position", {})
            new_data["position"]["x"] = 6
            new_data["position"]["y"] = i - 1
            out_path = os.path.join(INIT_DIR, f"{new_id}.json")
            save_json(out_path, new_data)
            print(f"[OK] added enemy {new_id}")

    print("[scene-assembler] done.")

# ------------------------------------------------------------
if __name__ == "__main__":
    # read scene name from CLI, else use default
    if len(sys.argv) > 1:
        scene_name = sys.argv[1]
    else:
        scene_name = DEFAULT_SCENE_NAME

    if scene_name not in BLUEPRINTS:
        print(f"[ERR] scene '{scene_name}' not found. Available: {', '.join(BLUEPRINTS.keys())}")
        sys.exit(1)

    assemble_scene(BLUEPRINTS[scene_name])
