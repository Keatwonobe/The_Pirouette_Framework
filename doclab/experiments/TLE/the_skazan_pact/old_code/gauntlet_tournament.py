# gauntlet_tournament.py
# Build AI-vs-AI encounters from ./generated_entities_v7 and prepare for combat_runner_v5.
# Modes: 'duel' (1v1 round-robin), 'teams' (NxN), 'royale' (all-in).
# Works with v7 entity schema emitted by your generator/bundle.

import os, json, uuid, itertools, random, subprocess, sys
from pathlib import Path
from datetime import datetime

# --- CONFIG ---
GEN_DIR          = Path("./generated_entities_v7")
BUNDLE_FALLBACK  = GEN_DIR / "_tle_entity_bundle_v7.json"
ENCOUNTER_OUTDIR = Path("./encounters/gauntlet")
ASSEMBLER_PATH   = Path("./scene_assembler_v3.py")   # optional, if present
COMBAT_RUNNER    = Path("./combat_runner_v5.py")     # you may run manually
MODE             = "duel"      # 'duel' | 'teams' | 'royale'
TEAM_SIZE        = 1           # used for 'teams'
N_MATCHES        = 24          # cap for large pools; set None for full round-robin
SEED             = 1337
POUND_FOR_POUND  = True        # normalize HP/ENT by size_factor to compare “skill”
SHUFFLE_ENTRIES  = True
ALLOW_DUPES_IN_TEAMS = False   # for small pools you might allow duplicates
# ---------------

random.seed(SEED)
ENCOUNTER_OUTDIR.mkdir(parents=True, exist_ok=True)

# --- helpers -----------------------------------------------------------------

def load_entities_from_folder(folder: Path):
    if not folder.exists():
        return {}
    ents = {}
    for f in folder.glob("*.json"):
        if f.name.startswith("_tle_entity_bundle"):  # skip bundle here
            continue
        try:
            with open(f, "r", encoding="utf-8") as fh:
                ent = json.load(fh)
            ents[f.stem] = ent
        except Exception as e:
            print(f"[WARN] cannot load {f}: {e}")
    return ents

def load_bundle(path: Path):
    if not path.exists(): 
        return {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            bundle = json.load(fh)
        return bundle.get("directories", {}).get(".", {})
    except Exception as e:
        print(f"[WARN] cannot read bundle {path}: {e}")
        return {}

def extract_size_factor_notes(notes):
    # notes like: ["size:medium","torso:bp_torso_humanoid","limb_families:avian","size_factor:2.1","entropy_scale:4.41"]
    sf = 1.0
    if not notes: 
        return sf
    for n in notes:
        if n.startswith("size_factor:"):
            try:
                sf = float(n.split(":",1)[1])
            except:
                pass
    return sf

def pound_for_pound_normalize(ent):
    """Scale down pools by size_factor for 'skill' comparison, preserving ints."""
    notes = ent.get("notes", [])
    sf = extract_size_factor_notes(notes)
    if sf <= 0: 
        return ent
    ent = json.loads(json.dumps(ent))  # deep copy
    pools = ent.setdefault("pools", {})
    for k in ("HP","ENT"):
        if k in pools:
            pools[k] = max(1, int(round(pools[k] / sf)))
    return ent

def clone_for_side(ent, side):
    """Make a side-tagged copy with unique ID; ensure AI 'auto'."""
    e = json.loads(json.dumps(ent))
    e["character_id"] = f"{ent['character_id']}_{side[:1]}{uuid.uuid4().hex[:3]}"
    e["side"] = "players" if side == "A" else "hostiles"
    ap = e.setdefault("ai_profile", {})
    ap["behavior"] = "auto"
    ap["weights"] = ap.get("weights", {})
    return e

def make_encounter(roster_A, roster_B, name="Auto Gauntlet"):
    # Minimal encounter doc that combat_runner_v5 has been using
    # Adjust to your exact schema if needed.
    encounter = {
        "encounter_id": f"gauntlet_{uuid.uuid4().hex[:6]}",
        "name": name,
        "map": {"width": 12, "height": 12},   # small arena
        "roster": roster_A + roster_B,
        "settings": {
            "auto_mode": True,
            "seed": SEED,
            "max_rounds": 30
        },
        "notes": ["generated_by:gauntlet_tournament"]
    }
    return encounter

def save_encounter(enc, outdir: Path):
    path = outdir / f"{enc['encounter_id']}.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(enc, fh, indent=2)
    return path

def maybe_run_assembler(enc_path: Path):
    if not ASSEMBLER_PATH.exists():
        return None
    try:
        # scene_assembler_v3.py supports directory or file inputs in your current setup.
        # If it takes a dir, pass the parent; if it takes a file, pass the file.
        cmd = [sys.executable, str(ASSEMBLER_PATH), "--in", str(enc_path)]
        print(f"[assembler] {' '.join(cmd)}")
        out = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if out.returncode == 0:
            print("[assembler] ok")
        else:
            print("[assembler] WARN nonzero exit:\n", out.stdout, out.stderr)
    except Exception as e:
        print("[assembler] WARN:", e)

def roster_from_entities(ents, ids):
    out = []
    for ent_id, side in ids:
        ent = ents[ent_id]
        e = pound_for_pound_normalize(ent) if POUND_FOR_POUND else ent
        out.append(clone_for_side(e, side))
    return out

# --- load pool ----------------------------------------------------------------
pool = load_entities_from_folder(GEN_DIR)
if not pool:
    print("[INFO] no loose jsons; trying bundle fallback")
    pool = load_bundle(BUNDLE_FALLBACK)

if not pool:
    print("[FATAL] no entities found in generated_entities_v7/")
    sys.exit(1)

all_ids = list(pool.keys())
if SHUFFLE_ENTRIES:
    random.shuffle(all_ids)

# cap pool for round-robin spam
if N_MATCHES and MODE == "duel":
    all_ids = all_ids[:max(2, min(len(all_ids), N_MATCHES))]

print(f"[INFO] loaded {len(all_ids)} contenders")

# --- schedule & emit ----------------------------------------------------------

scoreboard = {}

def record_result(a_id, b_id, enc_path):
    # We don’t parse combat logs here; we emit a manifest of matches to run.
    # You can later augment this to parse combat_runner logs and tally W/L.
    scoreboard.setdefault(a_id, []).append({"vs": b_id, "encounter": str(enc_path)})
    scoreboard.setdefault(b_id, []).append({"vs": a_id, "encounter": str(enc_path)})

created = []

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
series_tag = f"{MODE}_{'p4p' if POUND_FOR_POUND else 'raw'}_{ts}"

if MODE == "duel":
    pairs = list(itertools.combinations(all_ids, 2))
    if N_MATCHES:
        pairs = pairs[:N_MATCHES]
    for a, b in pairs:
        roster_A = roster_from_entities(pool, [(a, "A")])
        roster_B = roster_from_entities(pool, [(b, "B")])
        enc = make_encounter(roster_A, roster_B, name=f"Duel: {a} vs {b} ({series_tag})")
        path = save_encounter(enc, ENCOUNTER_OUTDIR)
        maybe_run_assembler(path)
        record_result(a, b, path)
        created.append(path)

elif MODE == "teams":
    # Build small teams of size TEAM_SIZE; sample without repl by default
    if len(all_ids) < TEAM_SIZE * 2:
        print("[FATAL] not enough entities for team mode")
        sys.exit(1)
    # simple drafting: split shuffled list into two teams repeatedly
    chunks = [all_ids[i:i+2*TEAM_SIZE] for i in range(0, len(all_ids), 2*TEAM_SIZE)]
    chunks = [c for c in chunks if len(c) == 2*TEAM_SIZE]
    if N_MATCHES:
        chunks = chunks[:N_MATCHES]
    for chunk in chunks:
        A_ids = [(eid, "A") for eid in chunk[:TEAM_SIZE]]
        B_ids = [(eid, "B") for eid in chunk[TEAM_SIZE:2*TEAM_SIZE]]
        roster_A = roster_from_entities(pool, A_ids)
        roster_B = roster_from_entities(pool, B_ids)
        label = f"Teams({TEAM_SIZE}v{TEAM_SIZE}): {'+'.join([x[0] for x in A_ids])} vs {'+'.join([x[0] for x in B_ids])} ({series_tag})"
        enc = make_encounter(roster_A, roster_B, name=label)
        path = save_encounter(enc, ENCOUNTER_OUTDIR)
        maybe_run_assembler(path)
        for a in [x[0] for x in A_ids]:
            for b in [x[0] for x in B_ids]:
                record_result(a, b, path)
        created.append(path)

elif MODE == "royale":
    # everyone vs everyone in one scrum
    roster_A = roster_from_entities(pool, [(eid, "A") for eid in all_ids[::2]])
    roster_B = roster_from_entities(pool, [(eid, "B") for eid in all_ids[1::2]])
    enc = make_encounter(roster_A, roster_B, name=f"Battle Royale ({len(roster_A)}v{len(roster_B)}): {series_tag}")
    path = save_encounter(enc, ENCOUNTER_OUTDIR)
    maybe_run_assembler(path)
    for a in [x["character_id"] for x in roster_A]:
        for b in [x["character_id"] for x in roster_B]:
            record_result(a, b, path)
    created.append(path)

# --- manifest of matches to run ----------------------------------------------
manifest = {
    "series": series_tag,
    "mode": MODE,
    "pound_for_pound": POUND_FOR_POUND,
    "encounters": [str(p) for p in created],
    "scoreboard_seed": scoreboard,
    "how_to_run": [
        f"python {COMBAT_RUNNER}  # then select encounter file when prompted",
        f"(or adapt combat_runner_v5 to accept --enc <path> --auto)"
    ]
}
mf_path = ENCOUNTER_OUTDIR / f"_gauntlet_manifest_{series_tag}.json"
with open(mf_path, "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, indent=2)

print("\n[GAUNTLET] wrote", len(created), "encounters →", ENCOUNTER_OUTDIR)
print("[GAUNTLET] manifest:", mf_path)
print("[NEXT] Run combat_runner_v5 against these encounters; parse logs later to rank W/L.")
