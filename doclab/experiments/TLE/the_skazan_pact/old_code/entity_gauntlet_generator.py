# entity_gauntlet_generator_v2.py
"""
Autogenerates TLE entities from the current on-disk bodypart layout.

Works with:
  ./items/bodyparts/
      aquatic/
      arcane/
      avian/
      colony/
      construct/
      elemental/
      grafts/
      humanoid/
      hybrid/
      insectoid/
      old/
      saurid/
      generated_entities/

No need to move files; we recurse.
"""

import os, json, random, uuid
from typing import Dict, Any, List, Tuple

# root from your PS dump
BODYPART_ROOT = "./items/bodyparts"

# fallback axes
DEFAULT_AXES = [
    "ax_aeric","ax_hydric","ax_terric","ax_pyric",
    "ax_epistemic","ax_oneiric","ax_aetheric"
]

# add near other globals
FALLBACK_CORES = {
    "humanoid": ["bp_torso_humanoid"],
    "dragon": ["bp_saurid_torso", "bp_quadruped_torso", "bp_hybrid_torso_avian_quadruped"],
    "colony": ["bp_colony_nucleus"],
    "construct": ["bp_construct_frame"],
    "elemental": ["bp_elemental_core"],
    "serpentine": ["bp_serpentine_torso"],
    "dream_entity": ["bp_arcane_vessel", "bp_arcane_spirit_shell"]
}

MOBILITY_CANDIDATES = [
    "bp_limb_basic",
    "bp_insectoid_leg",
    "bp_aquatic_fin_pair",
    "bp_avian_wing_pair"
]

# how many of each limb a "sane" body wants
LIMB_QUOTAS = {
    "humanoid": {"arm": 2, "leg": 2},
    "dragon": {"leg": 4},            # wings handled separately
    "construct": {},                 # ok to be weird
    "colony": {},                    # ooze
    "elemental": {},                 # aura-only fine
    "serpentine": {},                # no legs by default
    "dream_entity": {}               # can be abstract
}

# what bodyparts count as which limb role
LIMB_ROLE_HINTS = {
    "arm": [
        "bp_arm_humanoid_left",
        "bp_arm_humanoid_right",
        "bp_limb_basic"          # fallback
    ],
    "leg": [
        "bp_leg_humanoid_left",
        "bp_leg_humanoid_right",
        "bp_insectoid_leg",
        "bp_aquatic_fin_pair",   # better than nothing
        "bp_limb_basic"
    ],
    "wing": [
        "bp_avian_wing_pair",
        "bp_insectoid_wings",
        "bp_hybrid_wing_support"
    ]
}

def find_parts_for_role(role: str, parts: dict[str, dict]) -> list[dict]:
    """Return all on-disk parts that match any of the IDs we consider valid for this role."""
    wanted_ids = set(LIMB_ROLE_HINTS.get(role, []))
    found = []
    for pid, pdata in parts.items():
        if pid in wanted_ids:
            found.append(pdata)
    return found


# ------------------------------------------------------------------
# 1. LOADER: recurse down from BODYPART_ROOT
# ------------------------------------------------------------------
def load_all_bodyparts(root: str) -> Dict[str, Dict[str, Any]]:
    parts: Dict[str, Dict[str, Any]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            if not fn.endswith(".json"):
                continue
            full = os.path.join(dirpath, fn)
            try:
                with open(full, "r", encoding="utf-8") as f:
                    data = json.load(f)
                item_id = data.get("item_id") or os.path.splitext(fn)[0]
                parts[item_id] = data
            except Exception as e:
                print(f"[WARN] could not load {full}: {e}")
    return parts

# ------------------------------------------------------------------
# 2. ARCHETYPES — aligned to what you actually have on disk
# ------------------------------------------------------------------
ARCHETYPES = {
    # your humans
    "humanoid": ["core_humanoid", "head?", "limb", "limb", "skin?"],
    # you have serpentine + segmented in grafts
    "serpentine": ["core_serpentine", "skin?", "head?"],
    # dragons = saurid + avian + arcane breath
    "dragon": ["core_saurid", "skin_heavy", "wing", "tail", "internal_breath"],
    # constructs = construct + arcane vessel
    "construct": ["core_construct", "internal_repair", "head_logic", "skin?"],
    # oozes / colonies = in colony dir
    "colony": ["core_colony", "skin_membrane", "link_synapse"],
    # pure elementals
    "elemental": ["core_elemental", "skin_elemental", "link_elemental?"],
    # dream-mountain etc
    "dream_entity": ["core_arcane", "arcane_manifest", "link_consensus?"]
}

# ------------------------------------------------------------------
# 3. SLOT → MATCH RULES
#    we'll match by:
#      - tags (preferred)
#      - OR filename pattern (since we saw your actual names)
# ------------------------------------------------------------------
SLOT_TO_TAGS = {
    "core_humanoid": ["humanoid", "core", "torso"],
    "core_serpentine": ["serpentine", "core"],
    "core_saurid": ["saurid", "core"],
    "core_construct": ["construct", "core"],
    "core_colony": ["colony", "core"],
    "core_elemental": ["elemental", "core"],
    "core_arcane": ["arcane", "core"],

    "head": ["head", "sensor"],
    "head_logic": ["intelligence", "construct", "logic"],

    "limb": ["limb", "locomotion", "utility"],
    "wing": ["wing", "mobility"],
    "tail": ["tail", "appendage"],

    "skin?": ["skin", "defensive_surface", "adaptive_surface"],
    "skin_heavy": ["defensive_surface", "saurid", "beast"],
    "skin_membrane": ["membrane", "colony", "ooze"],
    "skin_elemental": ["elemental", "defensive_surface"],

    "internal_breath": ["dragon", "breath", "arcane"],
    "internal_repair": ["repair", "construct", "healing"],

    "link_synapse": ["collective_mind", "consensus", "link"],
    "link_elemental": ["elemental", "link"],
    "link_consensus": ["consensus", "arcane", "link"],
    "arcane_manifest": ["arcane", "manifestation"]
}

# patterns we saw in your actual files
FILENAME_HINTS = {
    "core_serpentine": ["serpentine_torso"],
    "core_colony": ["colony_nucleus"],
    "skin_membrane": ["colony_membrane"],
    "core_saurid": ["saurid_torso"],
    "internal_breath": ["arcane_breath_chamber"],
    "core_arcane": ["arcane_vessel", "arcane_binding_matrix", "arcane_spirit_shell"],
    "core_construct": ["construct_frame"],
    "head_logic": ["construct_logic_node"],
    "internal_repair": ["construct_repair_matrix"],
    "link_synapse": ["colony_synapse_field"],
    "link_consensus": ["resonance_anchor", "arcane_conduit"]
}

# ------------------------------------------------------------------
# 4. PICKER
# ------------------------------------------------------------------
def pick_part_for_slot(slot: str, parts: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    optional = slot.endswith("?")
    base_slot = slot.replace("?", "")
    desired_tags = SLOT_TO_TAGS.get(base_slot, [])
    candidates: List[Dict[str, Any]] = []

    # try by tags first
    for p in parts.values():
        ptags = p.get("tags", [])
        if any(tag in ptags for tag in desired_tags):
            candidates.append(p)

    # if nothing, try filename hints
    if not candidates and base_slot in FILENAME_HINTS:
        hints = FILENAME_HINTS[base_slot]
        for p_id, p in parts.items():
            for h in hints:
                if h in p_id:
                    candidates.append(p)
                    break

    # last resort: grab something with matching slot
    if not candidates:
        for p in parts.values():
            if p.get("slot") and base_slot.startswith(p.get("slot")):
                candidates.append(p)

    if not candidates:
        if optional:
            return {}
        return {}

    return random.choice(candidates)

def enforce_symmetry(archetype: str,
                     chosen: list[dict],
                     parts: dict[str, dict]) -> list[dict]:
    """
    Ensure we have the expected count of arms/legs for the archetype,
    but let 20% weirdos through untouched.
    """
    quotas = LIMB_QUOTAS.get(archetype, {})
    if not quotas:
        return chosen  # this archetype doesn't care

    # 20% chance to keep the freak
    if random.random() < 0.20:
        return chosen

    # count what we already have
    have_arm = 0
    have_leg = 0
    for p in chosen:
        pid = p.get("item_id", "")
        if pid.startswith("bp_arm_humanoid"):
            have_arm += 1
        elif (
            pid.startswith("bp_leg_humanoid")
            or pid.startswith("bp_insectoid_leg")
            or pid.startswith("bp_aquatic_fin_pair")
        ):
            have_leg += 1
        # bp_limb_basic we’ll use only if we still can’t find a “real” limb

    # ARMS
    need_arm = max(0, quotas.get("arm", 0) - have_arm)
    if need_arm > 0:
        arm_pool = find_parts_for_role("arm", parts)
        # if we have literal arms, pull from them
        for _ in range(need_arm):
            if arm_pool:
                chosen.append(random.choice(arm_pool))
            else:
                # fallback: basic limb if present
                if "bp_limb_basic" in parts:
                    chosen.append(parts["bp_limb_basic"])

    # LEGS
    need_leg = max(0, quotas.get("leg", 0) - have_leg)
    if need_leg > 0:
        leg_pool = find_parts_for_role("leg", parts)
        for _ in range(need_leg):
            if leg_pool:
                chosen.append(random.choice(leg_pool))
            else:
                if "bp_limb_basic" in parts:
                    chosen.append(parts["bp_limb_basic"])

    return chosen

def estimate_size_entropy(chosen: list[dict]) -> dict:
    """
    crude size estimator:
      base = 1.0
      +0.1 per body part
      +0.2 if has saurid_torso / quadruped_torso
      +0.2 if has elemental_mantle (big aura)
    """
    size = 1.0 + 0.1 * len(chosen)
    for p in chosen:
        pid = p.get("item_id", "")
        if "saurid_torso" in pid or "quadruped_torso" in pid:
            size += 0.2
        if "elemental_mantle" in pid:
            size += 0.2
    # square to exaggerate true behemoths
    return {
        "size_factor": round(size, 2),
        "entropy_scale": round(size ** 2, 2)
    }


# ------------------------------------------------------------------
# 5. ENTITY BUILDER
# ------------------------------------------------------------------
def build_entity(archetype: str, parts: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    slots = ARCHETYPES[archetype]
    chosen: List[Dict[str, Any]] = []
    for slot in slots:
        part = pick_part_for_slot(slot, parts)
        opt = slot.endswith("?")
        if not part and not opt:
            return {"error": f"missing required slot {slot}", "archetype": archetype}
        if part:
            chosen.append(part)

    # ensure core
    has_core = any(p.get("slot") in ("core","core_torso","torso") for p in chosen)
    if not has_core:
        for fb_id in FALLBACK_CORES.get(archetype, []):
            if fb_id in parts:
                chosen.append(parts[fb_id])
                has_core = True
                break
    if not has_core:
        return {"error": "could not resolve core", "archetype": archetype}

    # ensure mobility
    has_move = False
    for p in chosen:
        utils = p.get("utility", [])
        if any(u in ("move","slither","swim","flight","glide","pouncing") for u in utils):
            has_move = True
            break
    if not has_move:
        for m_id in MOBILITY_CANDIDATES:
            if m_id in parts:
                chosen.append(parts[m_id])
                has_move = True
                break

    # NEW: symmetry pass
    chosen = enforce_symmetry(archetype, chosen, parts)

    # collect axes
    axes = []
    for p in chosen:
        for ax in p.get("axes", []):
            if ax not in axes:
                axes.append(ax)
    if not axes:
        axes = random.sample(DEFAULT_AXES, k=3)

    # NEW: estimate size/entropy scaling
    size_info = estimate_size_entropy(chosen)

    char_id = f"gen_{archetype}_{uuid.uuid4().hex[:6]}"
    entity = {
        "character_id": char_id,
        "name": f"Generated {archetype.title()}",
        "type": "enemy",
        "side": "hostiles",
        "level": random.randint(1,5),
        "axes": axes,
        "stats": {
            "str": random.randint(6,16),
            "dex": random.randint(4,14),
            "int": random.randint(4,14),
            "will": random.randint(6,16),
            "init_bonus": random.randint(-1,4)
        },
        "pools": {
            # scale HP a little by size
            "HP": int((10 + len(chosen)*2) * size_info["size_factor"]),
            "ENT": 6 + len(chosen)
        },
        "body_parts": {f"part_{i}": p["item_id"] for i, p in enumerate(chosen)},
        "inventory": [],
        "spellbook": [],
        "ai_profile": {"behavior": "auto", "weights": {}},
        "notes": [
            f"generated_from:{archetype}",
            f"size_factor:{size_info['size_factor']}",
            f"entropy_scale:{size_info['entropy_scale']}"
        ]
    }
    return entity

# ------------------------------------------------------------------
# 6. VALIDATION
# ------------------------------------------------------------------
def validate_entity(entity: Dict[str, Any], parts: Dict[str, Dict[str, Any]]) -> Tuple[bool, str]:
    if "error" in entity:
        return False, entity["error"]

    bp_ids = list(entity.get("body_parts", {}).values())
    if not bp_ids:
        return False, "no body parts"

    has_core = False
    has_move = False

    for bp_id in bp_ids:
        p = parts.get(bp_id, {})
        slot = p.get("slot", "")
        if slot in ("core", "core_torso", "torso"):
            has_core = True
        utils = p.get("utility", [])
        if any(u in ("move", "slither", "swim", "flight", "glide", "pouncing") for u in utils):
            has_move = True

    if not has_core:
        return False, "no core"
    if not has_move:
        # not fatal, maybe it's a turret or floating spirit
        return True, "valid (static entity)"
    return True, "valid"

# ------------------------------------------------------------------
# 7. GAUNTLET
# ------------------------------------------------------------------
def run_gauntlet(parts: Dict[str, Dict[str, Any]], n: int = 25):
    os.makedirs(os.path.join(BODYPART_ROOT, "generated_entities"), exist_ok=True)
    archetypes = list(ARCHETYPES.keys())
    valid_count = 0
    for _ in range(n):
        arch = random.choice(archetypes)
        ent = build_entity(arch, parts)
        ok, reason = validate_entity(ent, parts)
        if ok:
            valid_count += 1
            outpath = os.path.join(BODYPART_ROOT, "generated_entities", f"{ent['character_id']}.json")
            with open(outpath, "w", encoding="utf-8") as f:
                json.dump(ent, f, indent=2)
            print(f"[OK] {ent['character_id']} <- {arch} :: {reason}")
        else:
            print(f"[REJECT] {arch} :: {reason}")
    print(f"\n[SUMMARY] generated={n} valid={valid_count}")

# ------------------------------------------------------------------
if __name__ == "__main__":
    parts = load_all_bodyparts(BODYPART_ROOT)
    print(f"[INFO] loaded {len(parts)} parts from {BODYPART_ROOT}")
    run_gauntlet(parts, n=30)
