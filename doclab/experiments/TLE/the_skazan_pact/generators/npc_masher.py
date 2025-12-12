import json
import random
import copy
from pathlib import Path


def load_json(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_pool(path):
    """Supports either {values:[...]} or a bare [...] file."""
    data = load_json(path)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "values" in data:
        return data["values"]
    raise ValueError(f"Pool file {path} is not in a recognized format.")


def build_name(config, pools):
    """
    config["name_slots"] = [{slot, source}, ...]
    pools = {slot: [values...]}
    """
    slot_values = {}
    for slot_cfg in config["name_slots"]:
        slot = slot_cfg["slot"]
        pool_values = pools[slot]
        slot_values[slot] = random.choice(pool_values)
    return config["name_format"].format(**slot_values)


def load_roster_templates(config):
    templates = []
    for path in config["roster_templates"]:
        tmpl = load_json(path)
        templates.append((path, tmpl))
    return templates


def generate_guest_block(base_tmpl, name, new_id):
    """
    base_tmpl: a stat template from roster_templates (e.g. guest_physique)
    Returns a new initiative block with overridden id + name.
    """
    npc = copy.deepcopy(base_tmpl)

    # There are many ways to do this; this keeps it minimal & generic.
    npc["character_id"] = new_id
    npc["name"] = name

    # Optional: mark as generated so you can filter/debug later
    meta = npc.get("meta", {})
    meta["generated_by"] = "npc_masher"
    npc["meta"] = meta

    return npc


def attach_to_encounter(encounter, npc_ids, side_key, starting_positions=None):
    """
    Adds the given npc_ids to encounter.sides[side_key] and starting positions.
    starting_positions: optional dict {npc_id: {"x": int, "y": int}}
    """
    sides = encounter.setdefault("sides", {})
    side_list = sides.setdefault(side_key, [])

    for nid in npc_ids:
        side_list.append(nid)

    if starting_positions:
        sp = encounter.setdefault("starting_positions", {})
        sp.update(starting_positions)

    return encounter


def generate_npcs_and_encounter(
    masher_config_path: str,
    count: int,
    out_encounter_path: str = None,
    out_initiative_dir: str = None,
):
    """
    Core entrypoint:
    - loads masher config
    - generates `count` NPCs with mashed names
    - returns (encounter_json, npc_blocks)
    If out_* paths are provided, saves them to disk.
    """
    config = load_json(masher_config_path)

    # 1) Load pools
    pools = {}
    for slot_cfg in config["name_slots"]:
        slot = slot_cfg["slot"]
        source_path = slot_cfg["source"]
        pools[slot] = load_pool(source_path)

    # 2) Load roster templates
    roster_templates = load_roster_templates(config)

    # 3) Load encounter template
    encounter = load_json(config["encounter_template"])

    generated_npcs = []
    npc_ids = []
    starting_positions = {}

    prefix = config.get("character_id_prefix", "npc_")
    id_mode = config.get("id_suffix_mode", "increment")

    for i in range(1, count + 1):
        # pick a random body template
        tmpl_path, tmpl = random.choice(roster_templates)

        # build name
        name = build_name(config, pools)

        # character id
        if id_mode == "increment":
            new_id = f"{prefix}{i:03d}"
        else:
            # id_mode could support other schemes later
            new_id = f"{prefix}{i}"

        npc_block = generate_guest_block(tmpl, name, new_id)
        generated_npcs.append(npc_block)
        npc_ids.append(new_id)

        # Optional: quick “ballroom grid” scatter
        # (you can delete this and let your map placer handle it)
        starting_positions[new_id] = {"x": (i % 8) + 1, "y": (i // 8) + 1}

    # 4) Attach guests to encounter
    encounter_side_key = config.get("encounter_side_key", "guests")
    encounter = attach_to_encounter(
        encounter, npc_ids, encounter_side_key, starting_positions
    )

    # 5) Optionally save
    if out_initiative_dir:
        out_dir = Path(out_initiative_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for npc in generated_npcs:
            cid = npc["character_id"]
            save_json(npc, out_dir / f"{cid}.json")

    if out_encounter_path:
        save_json(encounter, out_encounter_path)

    return encounter, generated_npcs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generic NPC Masher for TLE-style codexes."
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to npc_masher_* config JSON.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=24,
        help="How many NPCs to generate.",
    )
    parser.add_argument(
        "--out-encounter",
        default="encounters/masquerade_ball_generated.json",
        help="Where to save the generated encounter JSON.",
    )
    parser.add_argument(
        "--out-initiative-dir",
        default="roster/generated_guests",
        help="Directory to dump generated NPC initiative blocks.",
    )

    args = parser.parse_args()

    encounter, npcs = generate_npcs_and_encounter(
        masher_config_path=args.config,
        count=args.count,
        out_encounter_path=args.out_encounter,
        out_initiative_dir=args.out_initiative_dir,
    )

    print(
        f"Generated {len(npcs)} NPCs into {args.out_initiative_dir} "
        f"and encounter {args.out_encounter}."
    )
