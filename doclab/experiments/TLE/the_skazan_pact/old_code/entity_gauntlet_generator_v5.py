# entity_gauntlet_generator_v4_revised.py
# shape-first monster builder

import os, json, random, uuid
from typing import Dict, Any, List

# FIXED: We will load this from the codex bundle directly
BODYPART_ROOT = "./items/bodyparts"

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
    # FIXED: Added missing arcane "core" types
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

# FIXED: These lists are incomplete and string matching is brittle.
# We will use the 'slot' property from the JSON data instead in build_buckets.


def load_all_bodyparts(root: str) -> Dict[str, Dict[str, Any]]:
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
    FIXED: This function is rewritten to use the 'slot' property from the
    part data, which is much more reliable than string matching filenames.
    It also properly separates TRUE TORSOS from other "cores".
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
    
    # Create a master list of all valid torso IDs from the global dict
    master_torso_list = [item for sublist in TORSO_FAMILIES.values() for item in sublist]

    for pid, pdata in parts.items():
        # 1. Check if it's a TRUE TORSO first
        if pid in master_torso_list:
            buckets["torso"].append(pdata)
            continue

        slot = pdata.get("slot", "other")

        # 2. Assign to buckets based on explicit slot
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
        # 3. Handle 'core' parts that *weren't* in the master torso list
        elif slot == "core":
            buckets["internal"].append(pdata)
        else:
            buckets["other"].append(pdata)
            
    # Add 'other' parts to grafts as a fallback
    buckets["graft"].extend(buckets["other"])
            
    return buckets


# ---------------------------------------------------------------
# 1. size & torso config
# ---------------------------------------------------------------
def roll_size() -> str:
    # weight toward medium
    return random.choices(["small","medium","large"], weights=[1,3,2], k=1)[0]


def pick_torso(torso_bucket: List[Dict[str, Any]], size: str) -> Dict[str, Any]:
    """
    FIXED: Simplified to pick from the pre-filtered 'torso' bucket.
    The old logic was sound but complex. This is cleaner.
    """
    if not torso_bucket:
        return None # Signal failure
        
    # We can still bias by size if we want
    humanoid_torsos = [p for p in torso_bucket if "humanoid" in p["item_id"]]
    quad_torsos = [p for p in torso_bucket if "quadruped" in p["item_id"] or "saurid" in p["item_id"]]
    other_torsos = [p for p in torso_bucket if p not in humanoid_torsos and p not in quad_torsos]

    if size == "small" and humanoid_torsos:
        candidates = humanoid_torsos + other_torsos
    elif size == "large" and quad_torsos:
        candidates = quad_torsos + other_torsos
    else:
        # Medium or fallback
        candidates = humanoid_torsos + quad_torsos + other_torsos

    if not candidates:
        return random.choice(torso_bucket) # Should be impossible, but safe

    return random.choice(candidates)


# ---------------------------------------------------------------
# 2. derive min appendages from torso
# ---------------------------------------------------------------
def derive_required_limbs(torso_id: str) -> dict:
    """
    returns dict like {"legs":4, "arms":2}
    FIXED: Added missing arcane/energy cores
    """
    if "quadruped_torso" in torso_id or "hybrid_torso_avian_quadruped" in torso_id or "saurid_torso" in torso_id:
        return {"legs": 4, "arms": 0}
    if "torso_humanoid" in torso_id:
        return {"legs": 2, "arms": 2}
    if "construct_frame" in torso_id:
        # let constructs be biped by default
        return {"legs": 2, "arms": 2}
        
    # All other "torsos" are cores, serpentine, or colonies
    if "serpentine" in torso_id or "segmented_core" in torso_id:
        return {"legs": 0, "arms": 0}
    if "colony_nucleus" in torso_id:
        return {"legs": 0, "arms": 0}
    if "elemental_core" in torso_id:
        return {"legs": 0, "arms": 0}
    if "arcane_cognition_core" in torso_id or "arcane_manifest_core" in torso_id or "energy_core" in torso_id:
        return {"legs": 0, "arms": 0}
        
    # Default fallback
    return {"legs": 0, "arms": 0}


# ---------------------------------------------------------------
# 3. choose limb families (primary + maybe secondary)
# ---------------------------------------------------------------
def choose_limb_families() -> List[str]:
    all_fams = list(LIMB_FAMILIES.keys())
    primary = random.choice(all_fams)
    fams = [primary]
    # 20% chance to allow ONE cross breed
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
def fill_limbs(chosen: List[Dict[str, Any]],
               all_limbs_pool: List[Dict[str, Any]],
               themed_limbs_pool: List[Dict[str, Any]],
               needed: dict):
    
    # We prioritize themed limbs, but use all limbs as a fallback
    # This prevents duplicates and ensures we get *a* limb
    
    # Use sets for efficient removal
    themed_pool = list(themed_limbs_pool) # copy
    generic_pool = [p for p in all_limbs_pool if p not in themed_pool]
    
    random.shuffle(themed_pool)
    random.shuffle(generic_pool)

    legs_needed = needed.get("legs", 0)
    arms_needed = needed.get("arms", 0)
    legs_have = 0
    arms_have = 0

    # FIXED: Broader definition of what counts as a "leg" or "arm"
    def is_leg(p):
        pid = p["item_id"]
        return "leg" in pid or "fin" in pid or "raptor_claw" in pid
    
    def is_arm(p):
        pid = p["item_id"]
        return "arm" in pid or "talon" in pid or "limb_basic" in pid or "webbed_appendage" in pid

    # 1. Fill legs from themed pool
    for p in themed_pool:
        if legs_have < legs_needed and is_leg(p):
            chosen.append(p)
            legs_have += 1
            themed_pool.remove(p)

    # 2. Fill arms from themed pool
    for p in themed_pool:
        if arms_have < arms_needed and is_arm(p):
            chosen.append(p)
            arms_have += 1
            themed_pool.remove(p)

    # 3. Fill any remaining legs from generic pool
    for p in generic_pool:
        if legs_have < legs_needed and is_leg(p):
            chosen.append(p)
            legs_have += 1
            generic_pool.remove(p)
            
    # 4. Fill any remaining arms from generic pool
    for p in generic_pool:
        if arms_have < arms_needed and is_arm(p):
            chosen.append(p)
            arms_have += 1
            generic_pool.remove(p)

    # 5. FIXED: CRITICAL FALLBACK
    # If we *still* don't have enough (e.g., needed 4 legs, only 1 was found),
    # just grab *anything* from the remaining limb pools until the count is met.
    # This ensures a quadruped gets 4 appendages, even if they are weird.
    remaining_pool = themed_pool + generic_pool
    random.shuffle(remaining_pool)
    
    while (legs_have < legs_needed) and remaining_pool:
        chosen.append(remaining_pool.pop())
        legs_have += 1
        
    while (arms_have < arms_needed) and remaining_pool:
        chosen.append(remaining_pool.pop())
        arms_have += 1


# ---------------------------------------------------------------
# 5. add senses / skin / grafts with cap
# ---------------------------------------------------------------
def add_from_bucket(chosen: List[Dict[str, Any]], bucket: List[Dict[str, Any]], max_to_add: int):
    """
    Safely adds a number of random parts from a given bucket.
    """
    if not bucket:
        return # Bucket is empty
        
    for _ in range(max_to_add):
        # Pick a random part from the bucket
        # We allow replacement; a creature can have two 'graft_spines'
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

    chosen = [torso]
    torso_id = torso["item_id"]
    limb_need = derive_required_limbs(torso_id)

    # Get themed limbs
    limb_fams = choose_limb_families()
    themed_limb_pool = pick_from_families(limb_fams, parts)
    
    # Get all limbs
    all_limb_pool = buckets["limb"]

    fill_limbs(chosen, all_limb_pool, themed_limb_pool, limb_need)

    # Add other parts
    add_from_bucket(chosen, buckets["sense"], max_to_add=1)
    add_from_bucket(chosen, buckets["skin"], max_to_add=1)
    add_from_bucket(chosen, buckets["graft"], max_to_add=2) # Add up to 2 grafts
    add_from_bucket(chosen, buckets["internal"], max_to_add=1) # Add 1 internal part, like a 'core'

    # axes from parts
    axes = []
    for p in chosen:
        # FIXED: Parts in codex don't have 'axes', they have 'influences'
        # We'll just grab from the default list for now
        pass
        
    if not axes:
        axes = random.sample(DEFAULT_AXES, k=3)

    # De-duplicate chosen parts
    final_parts = []
    seen_ids = set()
    for p in chosen:
        if p["item_id"] not in seen_ids:
            final_parts.append(p)
            seen_ids.add(p["item_id"])

    # Calculate stats based on new 'final_parts' list
    size_factor = round(1.0 + 0.1*len(final_parts), 2)
    ent_scale = round(size_factor**2, 2)

    char_id = f"gen_auto_{uuid.uuid4().hex[:6]}"
    
    # HP: 30 base for medium, +5 per part. Scale by size.
    hp_base = 30
    if size == "small": hp_base = 20
    if size == "large": hp_base = 40
    
    # ENT: 10 base, +1 per part
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
            "HP": int((hp_base + len(final_parts)*3) * (size_factor / 1.5)), # Normalize factor a bit
            "ENT": ent_base + len(final_parts)
        },
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
    
    # Create a new directory for the revised output
    outdir = "./generated_entities_v5"
    os.makedirs(outdir, exist_ok=True)
    print(f"[INFO] Saving new entities to {outdir}")
    
    ok = 0
    all_entities = {} # To create a bundle
    
    for _ in range(n):
        ent = build_entity(parts)
        if "error" in ent:
            print(f"[REJECT] {ent['error']}")
            continue
            
        ok += 1
        outpath = os.path.join(outdir, f"{ent['character_id']}.json")
        all_entities[f"{ent['character_id']}.json"] = ent
        
        # Save individual file
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(ent, f, indent=2)
            
        print(f"[OK] {ent['character_id']} :: {ent['name']} :: {ent['notes']}")

    # Save a bundle file
    bundle_path = os.path.join(outdir, "_tle_entity_bundle_v5.json")
    bundle_data = {
        "TLE_VERSION": "1.0-v5-gen",
        "compiled_at": "2025-11-12T04:00:00.000000Z", # Placeholder time
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