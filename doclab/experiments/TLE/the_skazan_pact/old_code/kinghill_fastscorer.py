# kinghill_fastscorer.py
# King-of-the-Hill Duel Cage (fast heuristic scorer)
#
# Phase 1: cage pairs, fight until one per pair drops
# Phase 2: lift gates (no reposition), last combatant standing wins
#
# Inputs:
#   - ./generated_entities_v7/*.json  (or bundle fallback)
#
# Outputs:
#   - ./encounters/kinghill/_kinghill_manifest_*.json
#   - ./encounters/kinghill/_kinghill_leaderboard_*.md
#
# Notes:
#   - This is a fast, simplified combat model to rank builds quickly.
#   - Use the leaderboard to pick finalists, then run them in combat_runner_v5.py for full fidelity.

import os, json, math, random, uuid
from pathlib import Path
from datetime import datetime

# ---------- CONFIG ----------
GEN_DIR          = Path("./generated_entities_v7")
BUNDLE_FALLBACK  = GEN_DIR / "_tle_entity_bundle_v7.json"
OUTDIR           = Path("./encounters/kinghill")
PAIRS            = None   # None = auto pair from pool; or set like [("A","B"),("C","D"),...]
SEED             = 424242
MAX_ROUNDS       = 200
P4P_NORMALIZE    = True   # pound-for-pound normalize HP/ENT by size_factor
# Core dice knobs (simple, consistent, deterministic-ish)
DIE_SIDES        = 8      # base damage die
CRIT_RANGE       = 20     # d20 roll == 20 crit
CRIT_MULT        = 2.0
BLOCK_BASE       = 0      # simple flat block; tweak if you add armor parsing
HIT_DC_BASE      = 10     # target number to hit
AC_SCALE         = 0.25   # each point of DEX above/below 10 nudges AC a bit
MOVE_PER_TURN    = 5
ARENA_W          = 22
ARENA_H          = 12
CAGE_COL_GAP     = 4      # spacing between pair cages in phase 1
# ----------------------------

random.seed(SEED)
OUTDIR.mkdir(parents=True, exist_ok=True)

def load_entities_from_folder(folder: Path):
    ents = {}
    if folder.exists():
        for f in folder.glob("*.json"):
            if f.name.startswith("_tle_entity_bundle"):
                continue
            try:
                ents[f.stem] = json.load(open(f, "r", encoding="utf-8"))
            except Exception as e:
                print(f"[WARN] {f}: {e}")
    return ents

def load_bundle(path: Path):
    if not path.exists(): return {}
    try:
        bundle = json.load(open(path, "r", encoding="utf-8"))
        return bundle.get("directories", {}).get(".", {})
    except Exception as e:
        print(f"[WARN] bundle: {e}")
        return {}

def extract_sf(notes):
    sf = 1.0
    if not notes: return sf
    for n in notes:
        if n.startswith("size_factor:"):
            try: sf = float(n.split(":",1)[1])
            except: pass
    return max(0.1, sf)

def p4p(ent):
    if not P4P_NORMALIZE: return json.loads(json.dumps(ent))
    sf = extract_sf(ent.get("notes", []))
    e = json.loads(json.dumps(ent))
    pools = e.setdefault("pools", {})
    for k in ("HP","ENT"):
        if k in pools:
            pools[k] = max(1, int(round(pools[k] / sf)))
    return e

def ability_mod(x):
    # classic-ish modifier
    return math.floor((x - 10) / 2)

def roll_d(n=1, s=6):
    # deterministic-ish by seed; still random per call
    return sum(random.randint(1, s) for _ in range(n))

def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

class Fighter:
    def __init__(self, ent, slot, start_pos, pair_tag):
        self.source_id = ent["character_id"]
        self.name = ent.get("name", self.source_id)
        self.slot = slot       # unique in fight
        self.side = ent.get("side","players")
        self.axes = ent.get("axes", [])
        st = ent.get("stats", {})
        self.str = st.get("str", 10)
        self.dex = st.get("dex", 10)
        self.int = st.get("int", 10)
        self.will= st.get("will",10)
        self.init_bonus = st.get("init_bonus",0)
        pools = ent.get("pools", {})
        self.hp  = int(pools.get("HP", 12))
        self.ent = int(pools.get("ENT", 6))
        self.pos = start_pos
        self.pair = pair_tag   # used in Phase 1 targeting
        self.alive = True
        self.drop_round = None
        self.tags = set()      # future: prone, rooted, etc.

    def armor_class(self):
        # base 10 +/- DEX influence
        return int(HIT_DC_BASE + (self.dex - 10)*AC_SCALE)

    def attack_bonus(self):
        # simple STR-based melee bias
        return ability_mod(self.str)

    def pick_target(self, fighters, phase):
        # Phase 1: only target within your pair unless your pairmate is already dead
        candidates = [f for f in fighters if f.alive and f.slot != self.slot]
        if phase == 1:
            my_pairmates = [f for f in candidates if f.pair == self.pair]
            alive_pair = [f for f in my_pairmates]
            if alive_pair:
                candidates = alive_pair
        # nearest enemy heuristic
        candidates.sort(key=lambda t: distance(self.pos, t.pos))
        return candidates[0] if candidates else None

    def step_toward(self, target):
        if not target: return
        x, y = self.pos
        tx, ty = target.pos
        steps = MOVE_PER_TURN
        while steps > 0 and distance((x,y),(tx,ty)) > 1:
            if tx != x:
                x += 1 if tx > x else -1
            elif ty != y:
                y += 1 if ty > y else -1
            steps -= 1
        self.pos = (x, y)

    def try_attack(self, target, round_idx):
        if not target: return None
        if distance(self.pos, target.pos) > 1:
            return None
        # d20 to hit
        d20 = roll_d(1, 20)
        hit = (d20 + self.attack_bonus()) >= target.armor_class()
        crit = (d20 >= CRIT_RANGE)
        if not hit:
            return {"type":"miss","attacker":self.slot,"defender":target.slot,"d20":d20}
        dmg = roll_d(1, DIE_SIDES) + max(0, ability_mod(self.str))
        if crit:
            dmg = int(math.ceil(dmg * CRIT_MULT))
        dmg = max(1, dmg - BLOCK_BASE)
        target.hp -= dmg
        if target.hp <= 0 and target.alive:
            target.alive = False
            target.drop_round = round_idx
        return {"type":"hit","attacker":self.slot,"defender":target.slot,"d20":d20,"crit":crit,"dmg":dmg,"hp_after":max(0,target.hp)}

def roll_initiative(fighters):
    init = []
    for f in fighters:
        d20 = roll_d(1,20)
        total = d20 + f.init_bonus
        init.append((-(total), f.slot))  # negative to sort desc
    init.sort()
    order = [slot for _, slot in init]
    return order

def all_pairs_resolved(fighters):
    # pair is resolved if at least one in that pair is dead
    by_pair = {}
    for f in fighters:
        by_pair.setdefault(f.pair, []).append(f)
    for pair, lst in by_pair.items():
        alive = [f for f in lst if f.alive]
        if len(alive) > (len(lst)-1):  # i.e., both alive in a 2-size pair
            return False
    return True

def survivors(fighters):
    return [f for f in fighters if f.alive]

def layout_pairs(entities):
    """
    Returns list[Fighter], with starting positions arranged in side-by-side cages.
    entities: list of (entity_dict, pair_tag)
    """
    fighters = []
    # Arrange cages left-to-right; each cage holds 2 fighters at x and x+1
    x = 1
    for idx, (ent, pair_tag) in enumerate(entities):
        # two slots per pair
        if idx % 2 == 0:
            posA = (x, 2 + (idx//2)% (ARENA_H-3))
            posB = (x+2, 2 + (idx//2)% (ARENA_H-3))
            fA = Fighter(ent, slot=f"{ent['character_id']}_A", start_pos=posA, pair_tag=pair_tag)
            fighters.append(fA)
        else:
            # pair second
            posB = (x+2, 2 + (idx//2)% (ARENA_H-3))
            fB = Fighter(ent, slot=f"{ent['character_id']}_B", start_pos=posB, pair_tag=pair_tag)
            fighters.append(fB)
            # advance cage column after placing the second
            x += CAGE_COL_GAP
    return fighters

def run_phase(fighters, phase, max_rounds):
    # Initiative once at the start (classic feel). Could refresh per round if you prefer.
    init_order = roll_initiative(fighters)
    slot2f = {f.slot: f for f in fighters}
    log = []
    for rnd in range(1, max_rounds+1):
        # end condition
        if phase == 1 and all_pairs_resolved(fighters):
            break
        if phase == 2 and len(survivors(fighters)) <= 1:
            break
        for slot in init_order:
            f = slot2f[slot]
            if not f.alive: continue
            t = f.pick_target(survivors(fighters), phase)
            if not t: continue
            if distance(f.pos, t.pos) > 1:
                f.step_toward(t)
                log.append({"round":rnd,"act":"move","who":f.slot,"to":f.pos})
            res = f.try_attack(t, rnd)
            if res:
                res["round"] = rnd
                log.append(res)
                if phase == 1 and all_pairs_resolved(fighters):
                    break
        # allow quick early stop if a single survivor remains in phase 2
        if phase == 2 and len(survivors(fighters)) <= 1:
            break
    return log

def rank_kinghill(all_fighters):
    # Winner is last alive; rank others by (phase dropped, round dropped, distance from winner at drop)
    alive = survivors(all_fighters)
    if alive:
        king = alive[0]
    else:
        # edge case: simultaneous KO — pick highest HP-before; here just pick any
        king = sorted(all_fighters, key=lambda f: (f.drop_round or 10**6))[-1]
    ranks = []
    for f in all_fighters:
        if f.slot == king.slot:
            ranks.append((0, 10**6, 0, f))  # top
        else:
            drop_round = f.drop_round or 0
            dist = distance(f.pos, king.pos)
            # heuristic: earlier drop_round -> worse; farther from king at drop -> slightly worse
            ranks.append((1, -drop_round, -dist, f))
    # Sort: king first, then by later drop better, then closer to king better
    ranks.sort()
    ordered = [r[-1] for r in ranks]
    return king, ordered

def main():
    # load pool
    pool = load_entities_from_folder(GEN_DIR)
    if not pool:
        pool = load_bundle(BUNDLE_FALLBACK)
    if not pool:
        print("[FATAL] no entities found")
        return

    ids = list(pool.keys())
    if len(ids) < 2:
        print("[FATAL] need at least two entities")
        return

    # Auto-pair if not provided
    if PAIRS is None:
        random.shuffle(ids)
        pairs = []
        for i in range(0, len(ids)-1, 2):
            pairs.append((ids[i], ids[i+1]))
        if len(ids) % 2 == 1:
            # last one gets a bye -> pair with the strongest (arbitrary choice)
            pairs.append((ids[-1], ids[0]))
    else:
        pairs = PAIRS

    # Build fighter list with P4P normalization and pair tags
    fighters = []
    entities = []
    for idx, (a,b) in enumerate(pairs):
        pa = p4p(pool[a])
        pb = p4p(pool[b])
        pa["character_id"] = f"{pa['character_id']}_{uuid.uuid4().hex[:3]}"
        pb["character_id"] = f"{pb['character_id']}_{uuid.uuid4().hex[:3]}"
        pair_tag = f"pair_{idx+1}"
        entities.append((pa, pair_tag))
        entities.append((pb, pair_tag))

    fighters = layout_pairs(entities)

    # Phase 1: duels inside cages
    log1 = run_phase(fighters, phase=1, max_rounds=MAX_ROUNDS)

    # Phase 2: gates lifted — no reposition, free-for-all
    log2 = run_phase(fighters, phase=2, max_rounds=MAX_ROUNDS)

    # Ranking
    king, ordered = rank_kinghill(fighters)

    # Output
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    series = f"kinghill_{'p4p' if P4P_NORMALIZE else 'raw'}_{ts}"

    manifest = {
        "series": series,
        "seed": SEED,
        "arena": {"w": ARENA_W, "h": ARENA_H},
        "pairs": pairs,
        "p4p": P4P_NORMALIZE,
        "fighters": [{
            "slot": f.slot,
            "name": f.name,
            "source_id": f.source_id,
            "final_hp": max(0, f.hp),
            "drop_round": f.drop_round,
            "pos": f.pos,
            "pair": f.pair
        } for f in fighters],
        "king": {"slot": king.slot, "name": king.name, "source_id": king.source_id},
        "log_len_phase1": len(log1),
        "log_len_phase2": len(log2),
    }
    mpath = OUTDIR / f"_kinghill_manifest_{series}.json"
    json.dump(manifest, open(mpath,"w",encoding="utf-8"), indent=2)

    # Leaderboard markdown
    lines = []
    lines.append(f"# King of the Hill — {series}\n")
    lines.append(f"**Winner:** `{king.name}` (`{king.source_id}`)\n")
    lines.append("## Ranking\n")
    rank_rows = []
    for i, f in enumerate(ordered, start=1):
        rank_rows.append(f"{i}. **{f.name}** (`{f.source_id}`) — drop_round={f.drop_round if f.drop_round else 'WIN'}, pos={f.pos}, pair={f.pair}")
    lines.extend("\n".join(rank_rows))
    mdpath = OUTDIR / f"_kinghill_leaderboard_{series}.md"
    with open(mdpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"[KINGHILL] winner: {king.name} ({king.source_id})")
    print(f"[KINGHILL] manifest: {mpath}")
    print(f"[KINGHILL] leaderboard: {mdpath}")
    print("[NEXT] Take top N and pit them via gauntlet_tournament.py or feed into combat_runner_v5 for full sim.")
    
if __name__ == "__main__":
    main()
