# entity_gauntlet_generator_v7.py
# REVISED: Added world_profile hooks for probability control.

import os, json, random, uuid
from typing import Dict, Any, List

BODYPART_ROOT = "./items/bodyparts" # Using the directory walk per your setup

DEFAULT_AXES = [
    "ax_aeric","ax_hydric","ax_terric","ax_pyric",
    "ax_epistemic","ax_oneiric","ax_aetheric"
]

# Torso families now used for weighting
TORSO_FAMILIES = {
    "humanoid": ["bp_torso_humanoid"],
    "quadruped": ["bp_quadruped_torso", "bp_hybrid_torso_avian_quadruped", "bp_saurid_torso"],
    "serpentine": ["bp_serpentine_torso", "bp_segmented_core"],
    "colony": ["bp_colony_nucleus"],
    "construct": ["bp_construct_frame"],
    "elemental": ["bp_elemental_core"],
    "arcane": ["bp_arcane_cognition_core", "bp_arcane_manifest_core", "bp_energy_core"]
}

# Limb families now used for weighting
LIMB_FAMILIES = {
    "humanoid": ["bp_limb_basic"],
    "insectoid": ["bp_insectoid_leg", "bp_insectoid_wings"],
    "avian": ["bp_avian_wing_pair", "bp_avian_talons"],
    "aquatic": ["bp_aquatic_fin_pair", "bp_webbed_appendage"],
    "saurid": ["bp_saurid_raptor_claw"]
}

def load_all_bodyparts(root: str) -> Dict[str, Dict[str, Any]]:
    # This os.walk loader is correct and will pick up new files.
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

def build_buckets(parts: dict[str, dict], world_profile: Dict = None) -> dict[str, list[dict]]:
    """
    REVISED: Now checks world_profile for attribute filters, like 'allow_flight'.
    """
    if world_profile is None:
        world_profile = {}
        
    buckets = {
        "torso": [], "limb": [], "wing": [], "sense": [], "skin": [],
        "graft": [], "internal": [], "other": []
    }
    
    master_torso_list = [item for sublist in TORSO_FAMILIES.values() for item in sublist]
    
    # Get probability hooks from profile
    allow_flight_prob = world_profile.get('allow_flight', 1.0) # 1.0 = 100% allowed

    for pid, pdata in parts.items():
        if pid in master_torso_list:
            buckets["torso"].append(pdata)
            continue
        
        slot = pdata.get("slot", "other")
        
        if slot == "limb":
            buckets["limb"].append(pdata)
        elif slot == "wing":
            # NEW: Check probability before adding wings
            if random.random() <= allow_flight_prob:
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


def pick_torso(torso_bucket: List[Dict[str, Any]], size: str, world_profile: Dict = None) -> Dict[str, Any]:
    """
    REVISED: Now uses 'torso_family_weights' from the profile if it exists.
    Falls back to size-based bias.
    """
    if not torso_bucket:
        return None
    if world_profile is None:
        world_profile = {}

    torso_weights = world_profile.get('torso_family_weights')

    if torso_weights:
        # NEW: Use probability weights from the profile
        population = []
        weights = []
        
        # Build a mapping of family -> list of torsos
        family_map = {}
        for fam, pids in TORSO_FAMILIES.items():
            family_map[fam] = [p for p in torso_bucket if p["item_id"] in pids]

        # Create the weighted population list
        for fam, weight in torso_weights.items():
            if fam in family_map:
                for torso_part in family_map[fam]:
                    population.append(torso_part)
                    # Distribute the family's weight among its members
                    weights.append(weight / len(family_map[fam])) 
        
        if population:
            return random.choices(population, weights=weights, k=1)[0]
        else:
            # Fallback if weights were bad
            return random.choice(torso_bucket)

    else:
        # FALLBACK: Use the old v6 size-bias logic
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
    # This logic is sound and remains from v6
    if "quadruped_torso" in torso_id or "hybrid_torso_avian_quadruped" in torso_id or "saurid_torso" in torso_id:
        return {"legs": 4, "arms": 0}
    if "torso_humanoid" in torso_id:
        return {"legs": 2, "arms": 2}
    if "construct_frame" in torso_id:
        return {"legs": 2, "arms": 2}
    # All others are 0-limbed "cores" or serpentine
    return {"legs": 0, "arms": 0}


# ---------------------------------------------------------------
# 3. choose limb families (primary + maybe secondary)
# ---------------------------------------------------------------
def choose_limb_families(world_profile: Dict = None) -> List[str]:
    """
    REVISED: Now uses 'limb_family_weights' from the profile if it exists.
    """
    if world_profile is None:
        world_profile = {}
        
    all_fams = list(LIMB_FAMILIES.keys())
    primary = None
    
    limb_weights = world_profile.get('limb_family_weights')
    
    if limb_weights:
        # NEW: Use weighted choice
        fam_population = list(limb_weights.keys())
        fam_weights = list(limb_weights.values())
        # Ensure we only pick from families we know
        valid_pop = [f for f in fam_population if f in all_fams]
        valid_weights = [fam_weights[i] for i, f in enumerate(fam_population) if f in all_fams]
        
        if valid_pop:
            primary = random.choices(valid_pop, weights=valid_weights, k=1)[0]
        else:
            primary = random.choice(all_fams) # Fallback
    else:
        # FALLBACK: Use old random logic
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
# 4. fill limbs (v6 Consistency Logic)
# ---------------------------------------------------------------
def fill_limbs(chosen: List[Dict[str, Any]],
               all_limbs_pool: List[Dict[str, Any]],
               themed_limbs_pool: List[Dict[str, Any]],
               needed: dict):
    
    # This consistency-based logic from v6 remains
    legs_needed = needed.get("legs", 0)
    arms_needed = needed.get("arms", 0)
    if not all_limbs_pool: return

    def is_leg(p): return "leg" in p["item_id"] or "fin" in p["item_id"] or "raptor_claw" in p["item_id"]
    def is_arm(p): return "arm" in p["item_id"] or "talon" in p["item_id"] or "limb_basic" in p["item_id"] or "webbed_appendage" in p["item_id"]

    themed_leg_candidates = [p for p in themed_limbs_pool if is_leg(p)]
    themed_arm_candidates = [p for p in themed_limbs_pool if is_arm(p)]
    all_leg_candidates = [p for p in all_limbs_pool if is_leg(p)]
    all_arm_candidates = [p for p in all_limbs_pool if is_arm(p)]

    if legs_needed > 0:
        leg_to_use = None
        if themed_leg_candidates: leg_to_use = random.choice(themed_leg_candidates)
        elif all_leg_candidates: leg_to_use = random.choice(all_leg_candidates)
        else: leg_to_use = random.choice(all_limbs_pool)
        for _ in range(legs_needed): chosen.append(leg_to_use)

    if arms_needed > 0:
        arm_to_use = None
        if themed_arm_candidates: arm_to_use = random.choice(themed_arm_candidates)
        elif all_arm_candidates: arm_to_use = random.choice(all_arm_candidates)
        else: arm_to_use = random.choice(all_limbs_pool)
        for _ in range(arms_needed): chosen.append(arm_to_use)


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
def build_entity(parts: dict[str, dict], world_profile: Dict = None) -> dict[str, any]:
    if world_profile is None:
        world_profile = {}
        
    # REVISED: Pass profile to buckets
    buckets = build_buckets(parts, world_profile)
    size = roll_size()
    
    # REVISED: Pass profile to torso picker
    torso = pick_torso(buckets["torso"], size, world_profile)
    if not torso:
        return {"error": "no valid torso parts found in codex"}

    final_parts = [torso]
    torso_id = torso["item_id"]
    limb_need = derive_required_limbs(torso_id)

    # REVISED: Pass profile to family chooser
    limb_fams = choose_limb_families(world_profile)
    themed_limb_pool = pick_from_families(limb_fams, parts)
    all_limb_pool = buckets["limb"]

    fill_limbs(final_parts, all_limb_pool, themed_limb_pool, limb_need)

    add_from_bucket(final_parts, buckets["sense"], max_to_add=1)
    add_from_bucket(final_parts, buckets["skin"], max_to_add=1)
    add_from_bucket(final_parts, buckets["graft"], max_to_add=2)
    add_from_bucket(final_parts, buckets["internal"], max_to_add=1)
    
    # Add wings if any made it through the filter
    add_from_bucket(final_parts, buckets["wing"], max_to_add=1)


    axes = random.sample(DEFAULT_AXES, k=3)
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
            "str": random.randint(6,16), "dex": random.randint(4,14),
            "int": random.randint(4,14), "will": random.randint(6,16),
            "init_bonus": random.randint(-1,4)
        },
        "pools": {
            "HP": int((hp_base + len(final_parts)*3) * (size_factor / 1.5)),
            "ENT": ent_base + len(final_parts)
        },
        "body_parts": {f"part_{i}": p["item_id"] for i, p in enumerate(final_parts)},
        "inventory": [], "spellbook": [],
        "ai_profile": {"behavior": "auto", "weights": {}},
        "notes": [
            f"size:{size}", f"torso:{torso_id}",
            f"limb_families:{','.join(limb_fams)}",
            f"size_factor:{size_factor}", f"entropy_scale:{ent_scale}"
        ]
    }
    return entity


def run_gauntlet(n: int = 30, world_profile: Dict = None):
    """
    Main runner.
    world_profile: A dict of weights and filters.
    
    Example:
    profile = {
        'torso_family_weights': {'humanoid': 0.4, 'quadruped': 0.4, 'construct': 0.1, 'arcane': 0.05, 'elemental': 0.05},
        'limb_family_weights': {'humanoid': 0.5, 'insectoid': 0.4, 'avian': 0.1},
        'allow_flight': 0.1 # 10% chance for wings to even be in the pool
    }
    """
    if world_profile:
        print(f"[INFO] Running gauntlet with profile: {world_profile}")
    else:
        print("[INFO] Running gauntlet with default (random) profile.")
        world_profile = {} # Use empty dict to pass down
        
    parts = load_all_bodyparts(BODYPART_ROOT)
    if not parts:
        print(f"[FATAL] No parts loaded from {BODYPART_ROOT}.")
        return
        
    print(f"[INFO] loaded {len(parts)} parts from {BODYPART_ROOT}")
    
    outdir = "./generated_entities_v7"
    os.makedirs(outdir, exist_ok=True)
    print(f"[INFO] Saving new entities to {outdir}")
    
    ok = 0
    all_entities = {}
    
    for _ in range(n):
        ent = build_entity(parts, world_profile)
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
    bundle_path = os.path.join(outdir, "_tle_entity_bundle_v7.json")
    bundle_data = {
        "TLE_VERSION": "1.0-v7-gen",
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
    
    # --- EXAMPLE USAGE ---
    
    # 1. To run normally (all random), just call:
    # run_gauntlet(10)

    # 2. To run with your "World Manager" hooks, define a profile.
    
    # This profile makes a region with lots of insects, few birds,
    # and NO flying creatures. It also makes "weird" torsos rare.
    insect_swamp_profile = {
        'torso_family_weights': {
            'humanoid': 0.3,
            'quadruped': 0.3,
            'serpentine': 0.1,
            'construct': 0.1,
            'colony': 0.05,
            'arcane': 0.05, 
            'elemental': 0.05
        },
        'limb_family_weights': {
            'humanoid': 0.1,
            'insectoid': 0.6,  # 60% chance of insect limbs
            'avian': 0.0,      # 0% chance of avian limbs
            'aquatic': 0.3,
            'saurid': 0.1
        },
        'allow_flight': 0.0 # 0% chance. No wings allowed.
    }
    
    print("--- RUNNING SWAMP PROFILE ---")
    run_gauntlet(15, world_profile=insect_swamp_profile)
    
    
    # This profile makes a "holy mountain" area with lots of birds,
    # elementals, and flying creatures, but no insects.
    holy_mountain_profile = {
        'torso_family_weights': {
            'humanoid': 0.1,
            'quadruped': 0.2,
            'serpentine': 0.05,
            'construct': 0.15,
            'colony': 0.0,
            'arcane': 0.2, 
            'elemental': 0.3  # High chance of elemental/arcane "freaks"
        },
        'limb_family_weights': {
            'humanoid': 0.2,
            'insectoid': 0.0,  # No insects
            'avian': 0.7,      # 70% chance of avian limbs
            'aquatic': 0.0,
            'saurid': 0.1
        },
        'allow_flight': 0.75 # 75% chance that wings are available
    }
    
    print("\n--- RUNNING MOUNTAIN PROFILE ---")
    run_gauntlet(15, world_profile=holy_mountain_profile)