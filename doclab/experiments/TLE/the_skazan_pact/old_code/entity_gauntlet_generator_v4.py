# entity_gauntlet_generator_v4.py
# shape-first monster builder

import os, json, random, uuid
from typing import Dict, Any, List

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
}

# limb pools by family (all real file names from your dirs)
LIMB_FAMILIES = {
    "humanoid": [
        "bp_limb_basic"
    ],
    "insectoid": [
        "bp_insectoid_leg",
        "bp_insectoid_wings",
        "bp_insectoid_antennae",
        "bp_insectoid_mandibles"
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

SENSE_PARTS = [
    "bp_sensory_array",
    "bp_eye_variant",
    "bp_insectoid_compound_eye",
    "bp_avian_sight_peak",
    "bp_elemental_sense"
]

SKIN_PARTS = [
    "bp_coat_surface",
    "bp_aquatic_scales",
    "bp_insectoid_chitin",
    "bp_elemental_mantle",
    "bp_camouflage_membrane",
    "bp_saurid_scale_plate"
]

GRAFT_PARTS = [
    "bp_tail_weaponized",
    "bp_tail_variants",
    "bp_tail_balancer",
    "bp_graft_horns",
    "bp_graft_tusks",
    "bp_graft_antlers",
    "bp_graft_back_plates",
    "bp_graft_quills",
    "bp_clawed_appendage",
    "bp_synthesis_organ"
]


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
    buckets = {
        "torso": [],
        "limb": [],
        "wing": [],
        "sense": [],
        "skin": [],
        "graft": [],
        "other": []
    }
    for pid, pdata in parts.items():
        name = pid.lower()
        if ("torso" in name or "core" in name or "frame" in name or "nucleus" in name):
            buckets["torso"].append(pdata)
        elif ("wing" in name):
            buckets["wing"].append(pdata)
        elif ("leg" in name or "arm" in name or "limb" in name or "fin_pair" in name or "raptor_claw" in name or "talons" in name):
            buckets["limb"].append(pdata)
        elif ("sensory" in name or "eye" in name or "sight" in name or "antennae" in name):
            buckets["sense"].append(pdata)
        elif ("scale" in name or "chitin" in name or "coat" in name or "mantle" in name or "camouflage" in name):
            buckets["skin"].append(pdata)
        elif (name.startswith("bp_graft_") or name.startswith("bp_tail_") or "synthesis_organ" in name or "mane_or_crest" in name or "spines" in name or "quills" in name):
            buckets["graft"].append(pdata)
        else:
            buckets["other"].append(pdata)
    return buckets


# ---------------------------------------------------------------
# 1. size & torso config
# ---------------------------------------------------------------
def roll_size() -> str:
    # weight toward medium
    return random.choices(["small","medium","large"], weights=[1,3,2], k=1)[0]


def pick_torso(parts: Dict[str, Dict[str, Any]], size: str) -> Dict[str, Any]:
    # medium/large more likely to be beast/quad, small more likely humanoid/colony
    if size == "small":
        order = ["humanoid","colony","serpentine","construct"]
    elif size == "large":
        order = ["quadruped","elemental","construct","humanoid"]
    else:
        order = ["humanoid","quadruped","serpentine","colony","construct"]

    for fam in order:
        for cand in TORSO_FAMILIES.get(fam, []):
            if cand in parts:
                return parts[cand]
    # absolute fallback: first torso-like
    for p in parts.values():
        if p.get("slot") in ("core","torso","core_torso"):
            return p
    return {}


# ---------------------------------------------------------------
# 2. derive min appendages from torso
# ---------------------------------------------------------------
def derive_required_limbs(torso_id: str) -> dict:
    """
    returns dict like {"legs":4, "arms":2}
    """
    if "quadruped_torso" in torso_id or "hybrid_torso_avian_quadruped" in torso_id or "saurid_torso" in torso_id:
        return {"legs": 4, "arms": 0}
    if "torso_humanoid" in torso_id:
        return {"legs": 2, "arms": 2}
    if "serpentine" in torso_id or "segmented_core" in torso_id:
        return {"legs": 0, "arms": 0}
    if "colony_nucleus" in torso_id:
        return {"legs": 0, "arms": 0}
    if "elemental_core" in torso_id:
        return {"legs": 0, "arms": 0}
    if "construct_frame" in torso_id:
        # let constructs be biped by default
        return {"legs": 2, "arms": 2}
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
               limb_pool: List[Dict[str, Any]],
               needed: dict):
    # legs first
    legs_have = 0
    arms_have = 0
    for p in chosen:
        pid = p.get("item_id","")
        if "leg" in pid or "fin_pair" in pid or "insectoid_leg" in pid:
            legs_have += 1
        if "arm" in pid or "limb_basic" in pid:
            arms_have += 1

    # fill legs
    while legs_have < needed.get("legs", 0) and limb_pool:
        # choose something leg-ish
        leg_opts = [p for p in limb_pool if ("leg" in p["item_id"] or "fin_pair" in p["item_id"] or "raptor_claw" in p["item_id"])]
        if not leg_opts:
            break
        pick = random.choice(leg_opts)
        chosen.append(pick)
        legs_have += 1

    # fill arms
    while arms_have < needed.get("arms", 0) and limb_pool:
        arm_opts = [p for p in limb_pool if ("arm" in p["item_id"] or "limb_basic" in p["item_id"] or "talons" in p["item_id"])]
        if not arm_opts:
            break
        pick = random.choice(arm_opts)
        chosen.append(pick)
        arms_have += 1

    # if we still have an odd number overall, add one utility-ish limb to make it interpretable
    total_limbish = legs_have + arms_have
    if total_limbish == 1:
        # single-limbers become “specialty appendage”
        # (we'll handle in grafts phase if needed)
        pass


# ---------------------------------------------------------------
# 5. add senses / skin / grafts with cap
# ---------------------------------------------------------------
def maybe_add(parts: Dict[str, Dict[str, Any]], chosen: List[Dict[str, Any]], pool: List[str], cap: int = 1):
    added = 0
    for _ in range(cap):
        avail = [parts[p] for p in pool if p in parts]
        if not avail:
            return
        chosen.append(random.choice(avail))
        added += 1


# ---------------------------------------------------------------
# assemble entity
# ---------------------------------------------------------------
def build_entity(parts: dict[str, dict]) -> dict[str, any]:
    buckets = build_buckets(parts)

    size = roll_size()
    # torso: prefer real torsos, but fall back to the old logic
    torso = None
    if buckets["torso"]:
        # size can bias, but for now just pick
        torso = random.choice(buckets["torso"])
    else:
        torso = pick_torso(parts, size)

    if not torso:
        return {"error": "no torso found"}

    chosen = [torso]
    torso_id = torso["item_id"]
    limb_need = derive_required_limbs(torso_id)

    # we still do the “one or two limb families” trick, but we now have a big limb bucket to draw from
    limb_fams = choose_limb_families()
    # old pool from families
    fam_pool = pick_from_families(limb_fams, parts)
    # add the generic limb bucket to increase odds of good matches
    limb_pool = fam_pool + buckets["limb"]

    fill_limbs(chosen, limb_pool, limb_need)

    # senses
    if buckets["sense"]:
        chosen.append(random.choice(buckets["sense"]))
    # skin
    if buckets["skin"]:
        chosen.append(random.choice(buckets["skin"]))
    # grafts, max 2
    for _ in range(2):
        if buckets["graft"]:
            chosen.append(random.choice(buckets["graft"]))
    # axes from parts
    axes = []
    for p in chosen:
        for ax in p.get("axes", []):
            if ax not in axes:
                axes.append(ax)
    if not axes:
        axes = random.sample(DEFAULT_AXES, k=3)

    size_factor = round(1.0 + 0.1*len(chosen), 2)
    ent_scale = round(size_factor**2, 2)

    char_id = f"gen_auto_{uuid.uuid4().hex[:6]}"
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
            "HP": int((10 + len(chosen)*2) * size_factor),
            "ENT": 6 + len(chosen)
        },
        "body_parts": {f"part_{i}": p["item_id"] for i, p in enumerate(chosen)},
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
    print(f"[INFO] loaded {len(parts)} parts from {BODYPART_ROOT}")
    outdir = os.path.join(BODYPART_ROOT, "generated_entities")
    os.makedirs(outdir, exist_ok=True)
    ok = 0
    for _ in range(n):
        ent = build_entity(parts)
        if "error" in ent:
            print(f"[REJECT] {ent['error']}")
            continue
        ok += 1
        outpath = os.path.join(outdir, f"{ent['character_id']}.json")
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(ent, f, indent=2)
        print(f"[OK] {ent['character_id']} :: {ent['notes']}")
    print(f"[SUMMARY] generated={n} valid={ok}")


if __name__ == "__main__":
    run_gauntlet(30)
