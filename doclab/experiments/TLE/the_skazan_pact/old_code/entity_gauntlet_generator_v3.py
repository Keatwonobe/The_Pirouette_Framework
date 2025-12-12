# entity_gauntlet_generator_v3.py
# Keaton's Monster-Masher: budget → body plan → limbs → senses → grafts
import os, json, random, uuid
from typing import Dict, Any, List, Tuple

BODYPART_ROOT = "./items/bodyparts"

# axes fallback
DEFAULT_AXES = [
    "ax_aeric","ax_hydric","ax_terric","ax_pyric",
    "ax_epistemic","ax_oneiric","ax_aetheric"
]

# ------------------------------------------------------------------
# ARCHETYPES (high-level, not final body layout)
# ------------------------------------------------------------------
ARCHETYPES = {
    "humanoid": {"plan": "biped", "base_cost": 5},
    "dragon": {"plan": "quadruped_wings", "base_cost": 8},
    "construct": {"plan": "core_plus_limbs", "base_cost": 5},
    "colony": {"plan": "colony", "base_cost": 4},
    "elemental": {"plan": "aura", "base_cost": 4},
    "dream_entity": {"plan": "biped_soft", "base_cost": 4},
    "serpentine": {"plan": "serpentine", "base_cost": 4},
}

# ------------------------------------------------------------------
# ID hints from your folders
# ------------------------------------------------------------------
TORSO_HINTS = [
    "bp_torso_humanoid",
    "bp_saurid_torso",
    "bp_quadruped_torso",
    "bp_hybrid_torso_avian_quadruped",
    "bp_serpentine_torso",
    "bp_segmented_core",
    "bp_colony_nucleus",
    "bp_construct_frame",
    "bp_elemental_core",
    "bp_arcane_vessel"
]

LEG_HINTS = [
    "bp_leg_humanoid_left",
    "bp_leg_humanoid_right",
    "bp_insectoid_leg",
    "bp_aquatic_fin_pair"
]

ARM_HINTS = [
    "bp_arm_humanoid_left",
    "bp_arm_humanoid_right",
    "bp_limb_basic"
]

UTILITY_HINTS = [
    "bp_tail_weaponized",
    "bp_tail_balancer",
    "bp_tail_variants",
    "bp_clawed_appendage",
    "bp_synthesis_organ",
    "bp_graft_spines",
    "bp_graft_quills",
    "bp_graft_horns",
    "bp_graft_tusks",
    "bp_graft_antlers",
    "bp_graft_back_plates",
    "bp_mane_or_crest"
]

SENSE_HINTS = [
    "bp_sensory_array",
    "bp_eye_variant",
    "bp_eye_humanoid",
    "bp_insectoid_antennae",
    "bp_insectoid_compound_eye",
    "bp_avian_sight_peak",
    "bp_elemental_sense"
]

SKIN_HINTS = [
    "bp_coat_surface",
    "bp_aquatic_scales",
    "bp_elemental_mantle",
    "bp_insectoid_chitin",
    "bp_saurid_scale_plate",
    "bp_camouflage_membrane",
    "bp_bioluminescent_layer"
]

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

# simple finder
def find_any(parts: Dict[str, Dict[str, Any]], hints: List[str]) -> List[Dict[str, Any]]:
    out = []
    for h in hints:
        if h in parts:
            out.append(parts[h])
    return out

# ------------------------------------------------------------------
# BUDGETING
# ------------------------------------------------------------------
def make_budget(archetype: str) -> dict:
    base = ARCHETYPES[archetype]["base_cost"]
    # add a little randomness
    complexity = random.randint(0, 3)
    return {
        "total": base + complexity,
        "spent": 0
    }

def spend(budget: dict, cost: int) -> bool:
    if budget["spent"] + cost > budget["total"]:
        return False
    budget["spent"] += cost
    return True

# ------------------------------------------------------------------
# BODY PLAN BUILDERS
# ------------------------------------------------------------------
def add_torso(chosen: List[Dict], parts: Dict[str, Dict], budget: dict, archetype: str):
    torsos = find_any(parts, TORSO_HINTS)
    if torsos and spend(budget, 2):
        chosen.append(random.choice(torsos))
        return
    # fallback: any core-like
    for pid, pdata in parts.items():
        if pdata.get("slot") in ("core","torso","core_torso"):
            if spend(budget, 2):
                chosen.append(pdata)
                return

def add_leg_pair(chosen: List[Dict], parts: Dict[str, Dict], budget: dict):
    legs = find_any(parts, LEG_HINTS)
    if not legs:
        return
    # two legs cost 2
    if spend(budget, 2):
        chosen.append(random.choice(legs))
        # try to pick different one for variety
        chosen.append(random.choice(legs))

def add_arm_pair(chosen: List[Dict], parts: Dict[str, Dict], budget: dict):
    arms = find_any(parts, ARM_HINTS)
    if not arms:
        return
    if spend(budget, 2):
        chosen.append(random.choice(arms))
        chosen.append(random.choice(arms))

def add_utility(chosen: List[Dict], parts: Dict[str, Dict], budget: dict, max_util: int = 2):
    utils = find_any(parts, UTILITY_HINTS)
    count = 0
    while utils and count < max_util and spend(budget, 1):
        chosen.append(random.choice(utils))
        count += 1

def add_sense(chosen: List[Dict], parts: Dict[str, Dict], budget: dict):
    senses = find_any(parts, SENSE_HINTS)
    if senses and spend(budget, 1):
        chosen.append(random.choice(senses))

def add_skin(chosen: List[Dict], parts: Dict[str, Dict], budget: dict):
    skins = find_any(parts, SKIN_HINTS)
    if skins and spend(budget, 1):
        chosen.append(random.choice(skins))

# ------------------------------------------------------------------
# MAIN BUILDER
# ------------------------------------------------------------------
def build_entity(archetype: str, parts: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    plan = ARCHETYPES[archetype]["plan"]
    budget = make_budget(archetype)
    chosen: List[Dict[str, Any]] = []

    # 1) torso/core is always first
    add_torso(chosen, parts, budget, archetype)

    # 2) locomotion depending on plan
    if plan == "biped":
        add_leg_pair(chosen, parts, budget)
        # 95% chance to have arms if there are legs
        if random.random() < 0.95:
            add_arm_pair(chosen, parts, budget)
    elif plan == "biped_soft":
        add_leg_pair(chosen, parts, budget)
        if random.random() < 0.95:
            add_arm_pair(chosen, parts, budget)
    elif plan == "quadruped_wings":
        # two leg pairs = 4 legs
        add_leg_pair(chosen, parts, budget)
        add_leg_pair(chosen, parts, budget)
        # wings if available
        wings = find_any(parts, ["bp_avian_wing_pair","bp_hybrid_wing_support","bp_insectoid_wings"])
        if wings and spend(budget, 2):
            chosen.append(random.choice(wings))
    elif plan == "serpentine":
        # serpentine torso already added, we can add utility instead of legs
        pass
    elif plan == "colony":
        # colony: membrane + synapse
        mem = parts.get("bp_colony_membrane")
        syn = parts.get("bp_colony_synapse_field")
        if mem and spend(budget, 1):
            chosen.append(mem)
        if syn and spend(budget, 1):
            chosen.append(syn)
    elif plan == "aura":
        # elementals: mantle + conduit
        mant = parts.get("bp_elemental_mantle")
        cond = parts.get("bp_elemental_conduit")
        if mant and spend(budget, 1):
            chosen.append(mant)
        if cond and spend(budget, 1):
            chosen.append(cond)

    # 3) sense & skin
    add_sense(chosen, parts, budget)
    add_skin(chosen, parts, budget)

    # 4) use remaining budget on utility/grafts (but capped so we don't get “horns x 12”)
    add_utility(chosen, parts, budget, max_util=2)

    # 5) if *still* only one limb-like thing and it's awkward, force a utility limb
    limb_like = [p for p in chosen if "limb" in p.get("item_id","") or "leg" in p.get("item_id","") or "arm" in p.get("item_id","")]
    if len(limb_like) == 1:
        # add a tail/pedipalp/whatever to balance it
        add_utility(chosen, parts, budget, max_util=1)

    # collect axes
    axes = []
    for p in chosen:
        for ax in p.get("axes", []):
            if ax not in axes:
                axes.append(ax)
    if not axes:
        axes = random.sample(DEFAULT_AXES, k=3)

    # crude size factor = 1 + 0.1 per part
    size_factor = round(1.0 + 0.1*len(chosen), 2)
    entropy_scale = round(size_factor**2, 2)

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
            "HP": int((10 + len(chosen)*2) * size_factor),
            "ENT": 6 + len(chosen)
        },
        "body_parts": {f"part_{i}": p["item_id"] for i, p in enumerate(chosen)},
        "inventory": [],
        "spellbook": [],
        "ai_profile": {"behavior": "auto", "weights": {}},
        "notes": [
            f"generated_from:{archetype}",
            f"size_factor:{size_factor}",
            f"entropy_scale:{entropy_scale}"
        ]
    }
    return entity

# ------------------------------------------------------------------
def run_gauntlet(parts: Dict[str, Dict[str, Any]], n: int = 30):
    outdir = os.path.join(BODYPART_ROOT, "generated_entities")
    os.makedirs(outdir, exist_ok=True)
    archetypes = list(ARCHETYPES.keys())
    ok = 0
    for _ in range(n):
        arch = random.choice(archetypes)
        ent = build_entity(arch, parts)
        # minimal validate
        if not ent.get("body_parts"):
            print(f"[REJECT] {arch} :: no parts")
            continue
        ok += 1
        outpath = os.path.join(outdir, f"{ent['character_id']}.json")
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(ent, f, indent=2)
        print(f"[OK] {ent['character_id']} <- {arch}")
    print(f"[SUMMARY] generated={n} valid={ok}")

if __name__ == "__main__":
    parts = load_all_bodyparts(BODYPART_ROOT)
    print(f"[INFO] loaded {len(parts)} parts from {BODYPART_ROOT}")
    run_gauntlet(parts, n=30)
