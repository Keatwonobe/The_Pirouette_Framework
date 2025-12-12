# entity_gauntlet_generator_v6.py
# shape-first monster builder
# REVISED: Logic for limb consistency.

import os, json, random, uuid
from typing import Dict, Any, List

BODYPART_ROOT = "./items/bodyparts" # Using the directory walk per your setup

DEFAULT_AXES = [
    "ax_aeric","ax_hydric","ax_terric","ax_pyric",
    "ax_epistemic","ax_oneiric","ax_aetheric"
]

# torso families we know we have on disk
TORSO_FAMILIES = {
    "humanoid": ["bp_torso_humanoid"],
    "quadruped": ["bp_quadruped_torso", "bp_hybrid_torso_avian_quadruped", "bp_saurid_torso"],
    "serpentine": ["bp_serpentine_torso", "bp_segmented_core"],
    "colony": ["bp_colony_nucleus"],
    "construct": ["bp_construct_frame"],
    "elemental": ["bp_elemental_core"],
    "arcane": ["bp_arcane_cognition_core", "bp_arcane_manifest_core", "bp_energy_core"]
}

# limb pools by family (all real file names from your dirs)
LIMB_FAMILIES = {
    "humanoid": [
        "bp_limb_basic"
    ],
    "insectoid": [
        "bp_insectoid_leg",
        "bp_insectoid_wings",
    ],
    "avian": [
        "bp_avian_wing_pair",
        "bp_avian_talons"
    ],
    "aquatic": [
        "bp_aquatic_fin_pair",
        "bp_webbed_appendage"
    ],
    "saurid": [
        "bp_saurid_raptor_claw"
    ]
}

def load_all_bodyparts(root: str) -> Dict[str, Dict[str, Any]]:
    # This is the v4 os.walk loader you reverted to.
    parts = {}
    for dirpath, _, filenames in os.walk(root):
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
                print(f"[WARN] cannot load {full}: {e}")
    return parts

def build_buckets(parts: dict[str, dict]) -> dict[str, list[dict]]:
    """
    Using the v5 logic to bucket by 'slot' and separate true Torsos.
    """
    buckets = {
        "torso": [],
        "limb": [],
        "wing": [],
        "sense": [],  # slot: head
        "skin": [],
        "graft": [],  # slot: dorsal, appendage, head_modifier, etc.
        "internal": [], # slot: internal, or 'core' parts that AREN'T torsos
        "other": []
    }
    
    master_torso_list = [item for sublist in TORSO_FAMILIES.values() for item in sublist]

    for pid, pdata in parts.items():
        if pid in master_torso_list:
            buckets["torso"].append(pdata)
            continue
        slot = pdata.get("slot", "other")
        if slot == "limb":
            buckets["limb"].append(pdata)
        elif slot == "wing":
            buckets["wing"].append(pdata)
        elif slot == "head":
            buckets["sense"].append(pdata)
        elif slot == "skin":
            buckets["skin"].append(pdata)
        elif slot in ("internal", "link"):
            buckets["internal"].append(pdata)
        elif slot in ("dorsal", "appendage", "head_modifier", "limb_modifier", "skin_modifier", "tail"):
            buckets["graft"].append(pdata)
        elif slot == "core":
            buckets["internal"].append(pdata)
        else:
            buckets["other"].append(pdata)
            
    buckets["graft"].extend(buckets["other"])
    return buckets


# ---------------------------------------------------------------
# 1. size & torso config
# ---------------------------------------------------------------
def roll_size() -> str:
    return random.choices(["small","medium","large"], weights=[1,3,2], k=1)[0]


def pick_torso(torso_bucket: List[Dict[str, Any]], size: str) -> Dict[str, Any]:
    if not torso_bucket:
        return None
    humanoid_torsos = [p for p in torso_bucket if "humanoid" in p["item_id"]]
    quad_torsos = [p for p in torso_bucket if "quadruped" in p["item_id"] or "saurid" in p["item_id"]]
    other_torsos = [p for p in torso_bucket if p not in humanoid_torsos and p not in quad_torsos]
    if size == "small" and humanoid_torsos:
        candidates = humanoid_torsos + other_torsos
    elif size == "large" and quad_torsos:
        candidates = quad_torsos + other_torsos
    else:
        candidates = humanoid_torsos + quad_torsos + other_torsos
    if not candidates:
        return random.choice(torso_bucket)
    return random.choice(candidates)


# ---------------------------------------------------------------
# 2. derive min appendages from torso
# ---------------------------------------------------------------
def derive_required_limbs(torso_id: str) -> dict:
    if "quadruped_torso" in torso_id or "hybrid_torso_avian_quadruped" in torso_id or "saurid_torso" in torso_id:
        return {"legs": 4, "arms": 0}
    if "torso_humanoid" in torso_id:
        return {"legs": 2, "arms": 2}
    if "construct_frame" in torso_id:
        return {"legs": 2, "arms": 2}
    if "serpentine" in torso_id or "segmented_core" in torso_id:
        return {"legs": 0, "arms": 0}
    if "colony_nucleus" in torso_id:
        return {"legs": 0, "arms": 0}
    if "elemental_core" in torso_id:
        return {"legs": 0, "arms": 0}
    if "arcane_cognition_core" in torso_id or "arcane_manifest_core" in torso_id or "energy_core" in torso_id:
        return {"legs": 0, "arms": 0}
    return {"legs": 0, "arms": 0}


# ---------------------------------------------------------------
# 3. choose limb families (primary + maybe secondary)
# ---------------------------------------------------------------
def choose_limb_families() -> List[str]:
    all_fams = list(LIMB_FAMILIES.keys())
    primary = random.choice(all_fams)
    fams = [primary]
    if random.random() < 0.20:
        secondary = random.choice([f for f in all_fams if f != primary])
        fams.append(secondary)
    return fams


def pick_from_families(fams: List[str], parts: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for fam in fams:
        for pid in LIMB_FAMILIES.get(fam, []):
            if pid in parts:
                out.append(parts[pid])
    return out


# ---------------------------------------------------------------
# 4. fill limbs
# ---------------------------------------------------------------

# REVISED: This function is now built for *consistency*.
# It picks ONE part for legs and ONE part for arms and copies them.
def fill_limbs(chosen: List[Dict[str, Any]],
               all_limbs_pool: List[Dict[str, Any]],
               themed_limbs_pool: List[Dict[str, Any]],
               needed: dict):
    
    legs_needed = needed.get("legs", 0)
    arms_needed = needed.get("arms", 0)

    if not all_limbs_pool: # Safety check
        return

    # Helper functions to find candidates
    def is_leg(p):
        pid = p["item_id"]
        return "leg" in pid or "fin" in pid or "raptor_claw" in pid
    
    def is_arm(p):
        pid = p["item_id"]
        return "arm" in pid or "talon" in pid or "limb_basic" in pid or "webbed_appendage" in pid

    # 1. Find all possible leg/arm candidates
    themed_leg_candidates = [p for p in themed_limbs_pool if is_leg(p)]
    themed_arm_candidates = [p for p in themed_limbs_pool if is_arm(p)]
    
    all_leg_candidates = [p for p in all_limbs_pool if is_leg(p)]
    all_arm_candidates = [p for p in all_limbs_pool if is_arm(p)]

    # 2. Fill LEGS
    if legs_needed > 0:
        leg_to_use = None
        # Prioritize themed legs first
        if themed_leg_candidates:
            leg_to_use = random.choice(themed_leg_candidates)
        # Fallback to any leg
        elif all_leg_candidates:
            leg_to_use = random.choice(all_leg_candidates)
        # CRITICAL FALLBACK: No parts defined as "legs" were found.
        # Grab *any* limb and use it as a "leg".
        else:
            leg_to_use = random.choice(all_limbs_pool)
            
        # Add the *same part* N times
        for _ in range(legs_needed):
            chosen.append(leg_to_use)

    # 3. Fill ARMS
    if arms_needed > 0:
        arm_to_use = None
        # Prioritize themed arms
        if themed_arm_candidates:
            arm_to_use = random.choice(themed_arm_candidates)
        # Fallback to any arm
        elif all_arm_candidates:
            arm_to_use = random.choice(all_arm_candidates)
        # CRITICAL FALLBACK: No "arms" found.
        # Grab *any* limb and use it as an "arm".
        else:
            arm_to_use = random.choice(all_limbs_pool)
        
        # Add the *same part* N times
        for _ in range(arms_needed):
            chosen.append(arm_to_use)


# ---------------------------------------------------------------
# 5. add senses / skin / grafts with cap
# ---------------------------------------------------------------
def add_from_bucket(chosen: List[Dict[str, Any]], bucket: List[Dict[str, Any]], max_to_add: int):
    if not bucket:
        return
    for _ in range(max_to_add):
        chosen.append(random.choice(bucket))


# ---------------------------------------------------------------
# assemble entity
# ---------------------------------------------------------------
def build_entity(parts: dict[str, dict]) -> dict[str, any]:
    buckets = build_buckets(parts)
    size = roll_size()
    torso = pick_torso(buckets["torso"], size)
    if not torso:
        return {"error": "no valid torso parts found in codex"}

    # REVISED: 'chosen' is now our final parts list.
    final_parts = [torso]
    torso_id = torso["item_id"]
    limb_need = derive_required_limbs(torso_id)

    limb_fams = choose_limb_families()
    themed_limb_pool = pick_from_families(limb_fams, parts)
    all_limb_pool = buckets["limb"]

    # fill_limbs now adds directly to the 'final_parts' list
    fill_limbs(final_parts, all_limb_pool, themed_limb_pool, limb_need)

    # Add other parts
    add_from_bucket(final_parts, buckets["sense"], max_to_add=1)
    add_from_bucket(final_parts, buckets["skin"], max_to_add=1)
    add_from_bucket(final_parts, buckets["graft"], max_to_add=2)
    add_from_bucket(final_parts, buckets["internal"], max_to_add=1)

    axes = []
    # (Axis logic removed as it wasn't working with codex parts)
    if not axes:
        axes = random.sample(DEFAULT_AXES, k=3)

    # REVISED: The de-duplication step is REMOVED.
    # We now count *all* parts in final_parts, including copies.

    size_factor = round(1.0 + 0.1*len(final_parts), 2)
    ent_scale = round(size_factor**2, 2)
    char_id = f"gen_auto_{uuid.uuid4().hex[:6]}"
    
    hp_base = 30
    if size == "small": hp_base = 20
    if size == "large": hp_base = 40
    ent_base = 10
    
    entity = {
        "character_id": char_id,
        "name": f"Generated {size.title()} Creature",
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
            # Stats are now based on the full list length, including duplicates
            "HP": int((hp_base + len(final_parts)*3) * (size_factor / 1.5)),
            "ENT": ent_base + len(final_parts)
        },
        # REVISED: body_parts list will now show multiples
        "body_parts": {f"part_{i}": p["item_id"] for i, p in enumerate(final_parts)},
        "inventory": [],
        "spellbook": [],
        "ai_profile": {"behavior": "auto", "weights": {}},
        "notes": [
            f"size:{size}",
            f"torso:{torso_id}",
            f"limb_families:{','.join(limb_fams)}",
            f"size_factor:{size_factor}",
            f"entropy_scale:{ent_scale}"
        ]
    }
    return entity


def run_gauntlet(n: int = 30):
    parts = load_all_bodyparts(BODYPART_ROOT)
    if not parts:
        print(f"[FATAL] No parts were loaded. Check file '{BODYPART_ROOT}'.")
        return
        
    print(f"[INFO] loaded {len(parts)} parts from {BODYPART_ROOT}")
    
    outdir = "./generated_entities_v6"
    os.makedirs(outdir, exist_ok=True)
    print(f"[INFO] Saving new entities to {outdir}")
    
    ok = 0
    all_entities = {}
    
    for _ in range(n):
        ent = build_entity(parts)
        if "error" in ent:
            print(f"[REJECT] {ent['error']}")
            continue
            
        ok += 1
        outpath = os.path.join(outdir, f"{ent['character_id']}.json")
        all_entities[f"{ent['character_id']}.json"] = ent
        
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(ent, f, indent=2)
            
        print(f"[OK] {ent['character_id']} :: {ent['name']} :: {ent['notes']}")

    # Save a bundle file
    bundle_path = os.path.join(outdir, "_tle_entity_bundle_v6.json")
    bundle_data = {
        "TLE_VERSION": "1.0-v6-gen",
        "compiled_at": "2025-11-12T05:00:00.000000Z", # Placeholder time
        "directories": {
            ".": all_entities
        }
    }
    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(bundle_data, f, indent=2)

    print(f"\n[SUMMARY] generated={n} valid={ok}")
    print(f"[INFO] Bundle file saved to: {bundle_path}")


if __name__ == "__main__":
    run_gauntlet(30)