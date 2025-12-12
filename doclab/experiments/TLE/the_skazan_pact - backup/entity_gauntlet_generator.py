# entity_gauntlet_generator.py
"""
Autogenerates TLE entities from modular body-part JSONs.

Usage:
    python entity_gauntlet_generator.py
"""
from future import __annotations__
import os, json, random, uuid
from typing import Dict, List, Any

# ---------------------------------------------------------
# CONFIG: where your part JSONs live
# ---------------------------------------------------------
PART_ROOTS = [
    "./items/bodyparts/humanoid",
    "./items/bodyparts/beast",
    "./items/bodyparts/avian",
    "./items/bodyparts/saurid",
    "./items/bodyparts/arcane",
    "./items/bodyparts/elemental",
    "./items/bodyparts/construct",
    "./items/bodyparts/colony"
]

# quick axis pool in case a part forgets
DEFAULT_AXES = [
    "ax_aeric","ax_hydric","ax_terric","ax_pyric",
    "ax_void","ax_entropic","ax_biotic","ax_morphic",
    "ax_epistemic","ax_oneiric","ax_aetheric"
]


# ---------------------------------------------------------
# LOADING
# ---------------------------------------------------------
def load_parts(roots: List[str]) -> Dict[str, Dict[str, Any]]:
    parts = {}
    for root in roots:
        if not os.path.isdir(root):
            continue
        for fn in os.listdir(root):
            if not fn.endswith(".json"):
                continue
            full = os.path.join(root, fn)
            try:
                with open(full, "r", encoding="utf-8") as f:
                    data = json.load(f)
                parts[data["item_id"]] = data
            except Exception as e:
                print(f"[WARN] cannot load {full}: {e}")
    return parts


# ---------------------------------------------------------
# ARCHETYPE RECIPES
# each recipe is a list of *slots we want to try to fill*
# we will pick compatible parts to fill them
# ---------------------------------------------------------
ARCHETYPES = {
    "humanoid": ["core", "head", "limb", "limb", "skin?"],
    "serpentine": ["core_serpentine", "head?", "skin?"],
    "dragon": ["core_saurid", "skin_heavy", "wing", "tail", "internal_breath"],
    "construct": ["core_construct", "internal_repair", "head_logic", "skin?"],
    "colony": ["core_colony", "skin_membrane", "link_synapse"],
    "elemental": ["core_elemental", "skin_elemental", "link_elemental?"],
    "dream_mountain": ["core_elemental_earth", "arcane_manifest", "link_consensus"]
}


# ---------------------------------------------------------
# MAPPERS: which slots map to which tags
# ---------------------------------------------------------
SLOT_TO_TAGS = {
    "core": ["core_torso", "humanoid", "core"],
    "core_serpentine": ["serpentine", "core"],
    "core_saurid": ["saurid", "core_torso", "core"],
    "core_construct": ["construct", "core"],
    "core_colony": ["colony", "core"],
    "core_elemental": ["elemental", "core"],
    "core_elemental_earth": ["elemental", "core", "earth"],
    "head": ["head", "sensor", "incorporeal"],
    "head_logic": ["intelligence", "construct"],
    "limb": ["limb", "locomotion", "utility"],
    "wing": ["wing", "mobility"],
    "tail": ["appendage", "tail", "appendage", "saurid"],
    "skin?": ["skin", "defensive_surface", "adaptive_surface"],
    "skin_heavy": ["defensive_surface", "saurid", "beast"],
    "skin_membrane": ["membrane", "ooze", "colony", "skin"],
    "internal_breath": ["dragon", "breath", "arcane", "internal"],
    "internal_repair": ["healing", "repair", "construct"],
    "link_synapse": ["collective_mind", "consensus", "link"],
    "arcane_manifest": ["arcane", "manifestation"]
}


# ---------------------------------------------------------
# PICK PARTS THAT MATCH TAGS
# ---------------------------------------------------------
def pick_part_for_slot(slot: str, parts: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    desired_tags = SLOT_TO_TAGS.get(slot, [])
    candidates = []
    for p in parts.values():
        ptags = p.get("tags", [])
        if any(tag in ptags for tag in desired_tags):
            candidates.append(p)
    if not candidates:
        # fall back: any core for core, any skin for skin, etc.
        for p in parts.values():
            if slot.startswith("core") and p.get("slot") in ("core","torso"):
                candidates.append(p)
            elif "skin" in slot and p.get("slot") == "skin":
                candidates.append(p)
    if not candidates:
        return {}
    return random.choice(candidates)


# ---------------------------------------------------------
# BUILD ENTITY
# ---------------------------------------------------------
def build_entity(archetype: str, parts: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    plan = ARCHETYPES[archetype]
    chosen_parts = []
    for slot in plan:
        optional = slot.endswith("?")
        base_slot = slot.replace("?", "")
        part = pick_part_for_slot(base_slot, parts)
        if not part and not optional:
            return {"error": f"missing required slot {base_slot}", "archetype": archetype}
        if part:
            chosen_parts.append(part)

    # compose character
    char_id = f"gen_{archetype}_{uuid.uuid4().hex[:6]}"
    # collect axes from parts
    axes = []
    for p in chosen_parts:
        p_axes = p.get("axes", [])
        for a in p_axes:
            if a not in axes:
                axes.append(a)
    if not axes:
        axes = random.sample(DEFAULT_AXES, k=3)

    character = {
        "character_id": char_id,
        "name": f"Generated {archetype.title()}",
        "type": "enemy",
        "side": "hostiles",
        "level": random.randint(1, 6),
        "axes": axes,
        "stats": {
            "str": random.randint(6,16),
            "dex": random.randint(4,14),
            "int": random.randint(4,14),
            "will": random.randint(6,16),
            "init_bonus": random.randint(-1,4)
        },
        "pools": {
            "HP": 10 + len(chosen_parts)*2,
            "ENT": 6 + len(chosen_parts)
        },
        "body_parts": {f"part_{i}": p["item_id"] for i, p in enumerate(chosen_parts)},
        "inventory": [],
        "spellbook": [],
        "ai_profile": {"behavior": "auto", "weights": {}},
        "notes": [f"generated_from_archetype:{archetype}"]
    }
    return character


# ---------------------------------------------------------
# VALIDATION
# very simple: must have a core, must have at least 1 mobility or attack path,
# and must not contain an error
# ---------------------------------------------------------
def validate_entity(entity: Dict[str, Any], parts: Dict[str, Dict[str, Any]]) -> (bool, str):
    if "error" in entity:
        return False, entity["error"]

    bp_ids = list(entity.get("body_parts", {}).values())
    if not bp_ids:
        return False, "no body parts"

    # must have a core
    has_core = False
    mobility = 0
    senses = 0
    for bp_id in bp_ids:
        p = parts.get(bp_id, {})
        slot = p.get("slot", "")
        if slot in ("core","core_torso","torso"):
            has_core = True
        utils = p.get("utility", [])
        if "move" in utils or "slither" in utils or "flight" in utils or "swim" in utils:
            mobility += 1
        if "perception" in utils or "sense_aether" in utils or "detect_magic" in utils:
            senses += 1

    if not has_core:
        return False, "no core slot"
    if mobility == 0:
        return False, "no mobility utility"
    if senses == 0:
        # not fatal, but log
        return True, "valid (no senses)"
    return True, "valid"


# ---------------------------------------------------------
# GAUNTLET
# ---------------------------------------------------------
def run_gauntlet(parts: Dict[str, Dict[str, Any]], n: int = 20):
    archetypes = list(ARCHETYPES.keys())
    valids = []
    rejects = []
    for _ in range(n):
        arch = random.choice(archetypes)
        ent = build_entity(arch, parts)
        ok, reason = validate_entity(ent, parts)
        if ok:
            valids.append(ent)
            print(f"[OK] {ent['character_id']} ({ent['name']}) <- {reason}")
        else:
            rejects.append((ent, reason))
            print(f"[REJECT] {arch}: {reason}")

    # dump valids to file
    os.makedirs("./generated_entities", exist_ok=True)
    for ent in valids:
        outpath = os.path.join("./generated_entities", f"{ent['character_id']}.json")
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(ent, f, indent=2)
    print(f"\n[SUMMARY] generated={n} valid={len(valids)} rejected={len(rejects)}")
    return valids, rejects


if __name__ == "__main__":
    parts = load_parts(PART_ROOTS)
    print(f"[INFO] loaded {len(parts)} parts")
    run_gauntlet(parts, n=30)
