import argparse
import json
import os
import random
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Tuple


# ---------- Utility loaders ----------

def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_pool(path: Path) -> List[str]:
    """
    Loads a pool from a JSON file in a tolerant, schema-flexible way.

    Accepts:
    - A bare list:                ["Red", "Blue", ...]
    - Any dict containing a list: {"values":[...]}, {"colors":[...]}, {"names":[...]}
    - Nested dicts with only one list field
    - If multiple list fields appear, takes the first
    """

    data = load_json(path)

    # Case 1: bare list
    if isinstance(data, list):
        if all(isinstance(x, (str, int, float)) for x in data):
            return [str(x) for x in data]
        else:
            raise ValueError(f"Pool file {path} contains a list but entries aren't strings/numbers.")

    # Case 2: dictionary containing at least one list
    if isinstance(data, dict):
        # Search for the first list value
        for key, value in data.items():
            if isinstance(value, list):
                if all(isinstance(x, (str, int, float)) for x in value):
                    return [str(x) for x in value]
                else:
                    raise ValueError(f"Pool file {path} contains list under '{key}' but entries invalid.")
        # No list found
        raise ValueError(f"Pool file {path} does not contain any list fields.")

    # Case 3: unsupported
    raise ValueError(f"Pool file {path} is not a list or a dict containing a list.")



def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "pc"

# --- Stat allocation helpers -------------------------------------------------

STAT_KEYS = ["str", "dex", "con", "int", "will"]

STAT_BASE = 8
STAT_BONUSES = {
    "high": 6,
    "medium": 4,
    "low": 2
}


def allocate_stats_from_profile(stat_profile: dict) -> dict:
    """
    Turn a TLE stat_profile into concrete stats for play.

    stat_profile = {
        "base_point_buy": 28,
        "bias": {
            "high": ["str", ...],
            "medium": ["dex", ...],
            "low": ["int", ...]
        }
    }

    Returns:
        {
          "str": 14,
          "dex": 12,
          "con": 10,
          "int": 10,
          "will": 10,
          "init_bonus": 1
        }
    """
    bias = stat_profile.get("bias", {})

    # Reverse index: stat -> rank ("high"/"medium"/"low")
    stat_rank = {}
    for rank in ("high", "medium", "low"):
        for key in bias.get(rank, []):
            stat_rank[key] = rank

    stats = {}

    for key in STAT_KEYS:
        rank = stat_rank.get(key, "low")  # anything unmentioned defaults to low
        bonus = STAT_BONUSES.get(rank, STAT_BONUSES["low"])
        stats[key] = STAT_BASE + bonus

    # Derive a simple initiative bonus from Dexterity
    dex = stats.get("dex", STAT_BASE)
    init_bonus = max(0, (dex - 10) // 2)
    stats["init_bonus"] = init_bonus

    return stats


# ---------- Axes handling ----------

def pick_axes(all_axis_ids, pool_size=3, active_size=2, rng=None):
    """
    all_axis_ids: list of axis ids like ['ax_thermal', 'ax_biotic', ...]
    pool_size: how many axes a character 'has in their orbit'
    active_size: how many are actually mechanically active
    """
    if rng is None:
        rng = random

    if not all_axis_ids:
        return [], []

    # Make sure pool_size doesn't exceed number of axes
    pool_size = min(pool_size, len(all_axis_ids))

    # First: choose the pool (the 3 that define their 'school')
    axes_pool = rng.sample(all_axis_ids, k=pool_size)

    # Then: choose which ones are active from that pool
    active_size = min(active_size, len(axes_pool))
    axes_active = rng.sample(axes_pool, k=active_size)

    return axes_pool, axes_active



def load_axes(axes_dir: Path, allowlist: List[str] = None) -> List[Dict[str, Any]]:
    """
    Load axes from a directory of JSON files.
    We expect each JSON to have at least:
      - axis_id
      - name
    We then optionally filter by allowlist of axis_ids.
    """
    axes = []
    for path in axes_dir.glob("*.json"):
        try:
            data = load_json(path)
        except Exception:
            continue

        # support both "axis_id" and "id" styles just in case
        axis_id = data.get("axis_id") or data.get("id")
        if not axis_id:
            continue

        if allowlist and axis_id not in allowlist:
            continue

        axes.append({
            "axis_id": axis_id,
            "name": data.get("name", axis_id),
            "raw": data
        })

    if not axes:
        raise ValueError(f"No axes loaded from {axes_dir} (check path / allowlist).")
    return axes


def pick_two_axes(axes: List[Dict[str, Any]]) -> Tuple[str, str]:
    """
    Pick exactly 2 distinct axes, returned as axis_id strings.
    """
    if len(axes) < 2:
        raise ValueError("Need at least 2 axes to generate PCs.")
    chosen = random.sample(axes, 2)
    return chosen[0]["axis_id"], chosen[1]["axis_id"]


# ---------- Flavor name generation ----------

def load_flavor_pools(config_dir: Path, flavor_sources: Dict[str, str]) -> Dict[str, List[str]]:
    """
    flavor_sources: { "color": "colors.json", "epithet": "epithets.json", ... }
    Returns: { "color": [...], "epithet": [...], ... }
    """
    pools = {}
    for key, relative_path in flavor_sources.items():
        path = (config_dir / relative_path).resolve()
        pools[key] = load_pool(path)
        if not pools[key]:
            raise ValueError(f"Flavor pool {key} at {path} is empty.")
    return pools


def generate_flavor_name(name_format: str, pools: Dict[str, List[str]]) -> str:
    """
    Fill a format string like "{color} {epithet} {animal}"
    with random picks from the pools.
    """
    # find all {placeholders} in the format
    keys = set(re.findall(r"{([^}]+)}", name_format))

    subs = {}
    for key in keys:
        if key not in pools:
            raise ValueError(f"Name format requested key '{key}' but no pool provided.")
        subs[key] = random.choice(pools[key])

    return name_format.format(**subs)


# ---------- Archetype templates ----------

def load_archetype_templates(config_dir: Path, template_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Load character templates that will be used as the base for PCs.
    They should be full character JSONs that we can deep-copy and then
    override name/id/axes/etc.
    """
    templates = []
    for rel in template_paths:
        path = (config_dir / rel).resolve()
        data = load_json(path)
        templates.append(data)
    if not templates:
        raise ValueError("No archetype templates loaded.")
    return templates


def pick_archetype(templates: List[Dict[str, Any]]) -> Dict[str, Any]:
    return deepcopy(random.choice(templates))


# ---------- Weapon / inventory helpers ----------

def maybe_pick_weapon(config_dir: Path, weapon_pool_path: str) -> str:
    """
    Load weapon pool and return one random weapon_id string.
    """
    if not weapon_pool_path:
        return None
    path = (config_dir / weapon_pool_path).resolve()
    pool = load_pool(path)
    if not pool:
        return None
    return random.choice(pool)


def attach_weapon_to_inventory(character: Dict[str, Any], weapon_id: str):
    """
    Attach a weapon as equipped to the character's inventory if not already set.
    Weapon here is represented just by item_id; the actual item stats live in the codex.
    """
    if not weapon_id:
        return

    inventory = character.setdefault("inventory", [])
    # Avoid duplicates
    for item in inventory:
        if item.get("item_id") == weapon_id:
            return

    inventory.append({
        "item_id": weapon_id,
        "equipped": True
    })


# ---------- PC generation ----------

def generate_pc(
    idx: int,
    config: Dict[str, Any],
    axes: List[Dict[str, Any]],
    flavor_pools: Dict[str, List[str]],
    templates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate a single PC JSON using:
    - random archetype template
    - random flavor name
    - 2 axes
    - optional weapon selection
    """
    archetype = pick_archetype(templates)

    name_format = config.get("name_format", "{color} {animal}")
    pc_name = generate_flavor_name(name_format, flavor_pools)
    id_prefix = config.get("id_prefix", "pc_")

    character_id = f"{id_prefix}{slugify(pc_name)}_{idx:02d}"

    # Basic fields
    archetype["character_id"] = character_id
    archetype["name"] = pc_name

    # Ensure player / side flags
    archetype["player"] = True
    archetype["side"] = config.get("side", "players")

    # Level (if you want to override)
    base_level = config.get("base_level")
    if base_level is not None:
        archetype["level"] = base_level

# Axes
    template_axes_pool_ids = archetype.get("axes_pool") # This is List[str]
    
    local_axes_pool = []
    if template_axes_pool_ids and isinstance(template_axes_pool_ids, list):
        # Filter the global 'axes' list (which is List[Dict])
        # to only include axes whose 'axis_id' is in our template's list.
        local_axes_pool = [ax for ax in axes if ax["axis_id"] in template_axes_pool_ids]

    if len(local_axes_pool) >= 2:
        # We have a valid, specific pool from the template. Use it.
        ax1, ax2 = pick_two_axes(local_axes_pool)
    else:
        # The template didn't define a pool, or it was invalid.
        # Fall back to the global pool as before.
        if template_axes_pool_ids:
            # Log a warning if a pool was defined but couldn't be used
            print(f"Warning: Archetype {archetype.get('character_id')} 'axes_pool' {template_axes_pool_ids} had < 2 valid axes found. Falling back to global pool.")
        ax1, ax2 = pick_two_axes(axes)
        
    archetype["axes"] = [ax1, ax2]

    # Position is not important for roster; let the encounter file place them
    archetype.setdefault("position", {"x": 0, "y": 0})

    # Optional weapon
    weapon_pool_path = config.get("weapon_pool")
    weapon_id = maybe_pick_weapon(Path(config["_config_dir"]), weapon_pool_path) if weapon_pool_path else None
    if weapon_id:
        attach_weapon_to_inventory(archetype, weapon_id)

    return archetype


def generate_pcs(config_path: Path) -> List[Dict[str, Any]]:
    # Load config
    config = load_json(config_path)
    config["_config_dir"] = str(config_path.parent)  # internal helper

    out_dir = Path(config.get("output_dir", "generated_pcs")).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    count = int(config.get("count", 6))

    # Axes
    axes_dir = Path(config.get("axes_dir", "./axes")).resolve()
    axes_allowlist = config.get("axes_allowlist") or None
    axes = load_axes(axes_dir, axes_allowlist)

    # Flavor pools
    flavor_sources = config.get("flavor_sources", {})
    flavor_pools = load_flavor_pools(config_path.parent, flavor_sources)

    # Archetype templates
    template_paths = config.get("archetype_templates", [])
    templates = load_archetype_templates(config_path.parent, template_paths)

    pcs = []
    for i in range(count):
        pc = generate_pc(
            idx=i + 1,
            config=config,
            axes=axes,
            flavor_pools=flavor_pools,
            templates=templates
        )
            # Auto-allocate concrete stats from the stat_profile
        stat_profile = pc.get("stat_profile")
        if stat_profile:
            pc["stats"] = allocate_stats_from_profile(stat_profile)
        pcs.append(pc)

    # Output
    output_mode = config.get("output_mode", "split_and_roster")
    roster_filename = config.get("roster_filename", "pc_roster.json")
    roster_path = out_dir / roster_filename

    if output_mode in ("roster_only", "split_and_roster"):
        with roster_path.open("w", encoding="utf-8") as f:
            json.dump(pcs, f, indent=2, ensure_ascii=False)

    if output_mode in ("split", "split_and_roster"):
        for pc in pcs:
            cid = pc.get("character_id", "pc")
            pc_path = out_dir / f"{cid}.json"
            with pc_path.open("w", encoding="utf-8") as f:
                json.dump(pc, f, indent=2, ensure_ascii=False)

    return pcs


# ---------- CLI ----------

def main():
    parser = argparse.ArgumentParser(description="TLE Player Character Generator (PC Masher)")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to pc_masher_config.json"
    )
    args = parser.parse_args()
    config_path = Path(args.config).resolve()

    pcs = generate_pcs(config_path)
    print(f"Generated {len(pcs)} PCs from {config_path}")


if __name__ == "__main__":
    main()
