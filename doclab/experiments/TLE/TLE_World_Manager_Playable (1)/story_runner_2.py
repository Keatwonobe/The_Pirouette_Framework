# Create story_runner_v2.py that adds prose narration, grid movement, and richer logging.
from pathlib import Path
import json, random, datetime, argparse, math

BASE = Path("/mnt/data")
LOGS = BASE / "logs"
INIT = BASE / "initiative"
ROSTER = BASE / "roster"
LOGS.mkdir(exist_ok=True)
INIT.mkdir(exist_ok=True)
ROSTER.mkdir(exist_ok=True)

WORLD_PATH = BASE / "world.json"
WORLD = json.loads(WORLD_PATH.read_text()) if WORLD_PATH.exists() else {
    "name": "Unnamed World",
    "grid_scale_ft": 5,
    "rules": {"tn_base": 8, "range_per_ep_ft": 5, "ante": {"enabled": True}, "environment": {"corruption_per_2_ep": True}},
}

# ---------- Utility ----------
def load_char(fp):
    j = json.loads(Path(fp).read_text())
    j["_alive"] = j["pools"]["HP"] > 0
    j["_err"] = j["stats"]["ERR"]
    j["_spoken"] = False
    # Ensure position exists
    j.setdefault("position", {"x": 0, "y": 0})
    return j

def roll_d20(supplied=None):
    if supplied is not None:
        try:
            v = int(supplied); return max(1, min(20, v))
        except: pass
    return random.randint(1, 20)

def tn_from_ep(ep): 
    return WORLD["rules"]["tn_base"] + (ep // 2)

def atk_total(j, die): 
    return die + (j["stats"]["DEX"] // 4) + (j["stats"]["INT"] // 4)

def choose_target(ch, others):
    enemies = [o for o in others if o["side"] != ch["side"] and o["_alive"]]
    if not enemies:
        return None
    enemies.sort(key=lambda o: (o["pools"]["HP"], o["pools"]["AEP"]))
    return enemies[0]

def distance(a, b):
    dx = b["position"]["x"] - a["position"]["x"]
    dy = b["position"]["y"] - a["position"]["y"]
    return math.sqrt(dx*dx + dy*dy)

def step_toward(a, b, squares=1):
    if not b: return a["position"]
    ax, ay = a["position"]["x"], a["position"]["y"]
    bx, by = b["position"]["x"], b["position"]["y"]
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0: 
        return {"x": ax, "y": ay}
    mag = math.sqrt(dx*dx + dy*dy)
    ux, uy = dx / mag, dy / mag
    # grid step
    nx = ax + int(round(ux * squares))
    ny = ay + int(round(uy * squares))
    return {"x": nx, "y": ny}

def morale(ch):
    hp = ch["pools"]["HP"]
    max_hp = ch.get("_max_hp", hp)
    ratio = hp / max(1, max_hp)
    rz = ch.get("constitution", {}).get("resolve", 10)
    comp = ch.get("constitution", {}).get("composure", 10)
    if ratio >= 0.75: return "steady"
    if ratio >= 0.5: return "wary" if comp < 15 else "focused"
    if ratio >= 0.25: return "shaken" if rz < 15 else "grim"
    return "desperate"

class Narrator:
    def __init__(self, style="omniscient", tense="present"):
        self.style = style
        self.tense = tense

    def intro(self, world, order):
        sides = {}
        for ch in order:
            sides.setdefault(ch["side"], []).append(ch["name"])
        side_lines = [f"{side.capitalize()}: {', '.join(names)}" for side, names in sides.items()]
        return [
            f"# Encounter Log — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**World:** {world.get('name','—')} (grid {world.get('grid_scale_ft',5)} ft)",
            " | ".join(side_lines),
            ""
        ]

    def start_round(self, rnd, order):
        blips = []
        for ch in order:
            m = morale(ch)
            blips.append(f"{ch['name']} ({m}, HP {ch['pools']['HP']}, AEP {ch['pools']['AEP']}) @ ({ch['position']['x']},{ch['position']['y']})")
        return [f"## Round {rnd}", "*Status:* " + " • ".join(blips)]

    def narr_talk(self, ch, why_text):
        voice = why_text if why_text and why_text != "(kept own counsel)" else "Lay down arms and live."
        return f"- **{ch['name']}** calls out: _“{voice}”_"
    
    def narr_move(self, ch, old_pos, new_pos, why_text, squares):
        return f"- **{ch['name']}** shifts from {old_pos} to {new_pos} ({squares} sq). _Why:_ {why_text}"

    def narr_defend(self, ch, ep, why_text):
        return f"- **{ch['name']}** braces, investing {ep} EP. _Why:_ {why_text}"

    def narr_attack(self, ch, tgt, spend, tn, d20, total, defend, soak, dmg, fell, why_text):
        pre = f"- **{ch['name']}** strikes at **{tgt['name']}** (EP {spend}, TN {tn}) — d20 {d20} → total {total}. "
        if total < tn:
            return pre + f"**Miss.** _Why:_ {why_text}"
        line = pre + f"**Hit!** Def {defend}, Soak {soak}, HP -{dmg} → {tgt['pools']['HP']}. _Why:_ {why_text}"
        if fell:
            line += f" **{tgt['name']} falls.**"
        return line

def load_initiative():
    # Load everyone in initiative/, else try fallback: put sample files from root if present
    files = sorted(INIT.glob("*.json"))
    if not files:
        # if user hasn't staged initiative, copy the two sample actors when present
        for fname in ["pilgrim-001.json", "wolf-001.json"]:
            src = BASE / fname
            if src.exists():
                (INIT / fname).write_text(src.read_text())
        files = sorted(INIT.glob("*.json"))
    chars = [load_char(fp) for fp in files]
    # annotate max hp for morale
    for ch in chars:
        ch["_max_hp"] = ch["pools"]["HP"]
    return chars

def run_story_v2(auto=True, seed=None, max_rounds=20, prose=True):
    if seed is not None:
        random.seed(seed)

    narrator = Narrator()
    chars = load_initiative()
    if not chars:
        return None, None

    # Initiative order: roll + init + DEX//4
    order = sorted(
        [ch for ch in chars if ch["_alive"]],
        key=lambda c: -(random.randint(1, 20) + c["stats"].get("init_bonus", 0) + (c["stats"]["DEX"] // 4)),
    )

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    md_lines = narrator.intro(WORLD, order)

    rnd = 1
    while rnd <= max_rounds:
        # refresh ERR each round and clear 'spoken'
        for ch in order:
            if ch["_alive"]:
                ch["_err"] = ch["stats"]["ERR"]
                ch["_spoken"] = False

        md_lines += narrator.start_round(rnd, order)

        for ch in order:
            if not ch["_alive"]:
                continue
            others = [o for o in order if o["id"] != ch["id"]]
            # very lightweight AI
            if ch["_err"] <= 0:
                md_lines.append(f"- **{ch['name']}** pauses (no ERR).")
                continue

            # prefer talk_first once per round if archetype has it and hasn't spoken
            tactics = ch.get("persona", {}).get("tactics", [])
            arche = ch.get("persona", {}).get("archetype", "")
            will_talk = ("talk_first" in tactics or arche == "parleyist") and not ch["_spoken"] and random.random() < 0.5
            if will_talk:
                ch["_spoken"] = True
                tenets = ch.get("constitution", {}).get("tenets", [])
                line = random.choice(tenets) if tenets else "We can still choose mercy."
                md_lines.append(narrator.narr_talk(ch, line))
                continue

            # choose a target and decide EP spend
            tgt = choose_target(ch, others)
            aggressive = (arche == "intrepid")
            ep_spend = max(1, min(ch["_err"], ch["_err"] if aggressive else 3))

            # small chance to reposition instead of attack
            if random.random() < 0.25 and tgt:
                old = (ch["position"]["x"], ch["position"]["y"])
                squares = min(ep_spend, 4)
                newpos = step_toward(ch, tgt, squares=squares)
                ch["position"] = {"x": newpos["x"], "y": newpos["y"]}
                ch["_err"] -= squares
                why = f"Improve angle; close distance to {tgt['name']} (now {distance(ch,tgt):.1f} sq)."
                md_lines.append(narrator.narr_move(ch, old, (newpos['x'], newpos['y']), why, squares))
                continue

            # default to attack
            ch["_err"] -= ep_spend
            tn = tn_from_ep(ep_spend)
            d20 = roll_d20()
            total = atk_total(ch, d20)

            if not tgt or not tgt["_alive"]:
                md_lines.append(f"- **{ch['name']}** attacks but finds no viable target.")
                continue

            # defending/soak
            defend = min(ep_spend, max(0, tgt["_err"] // 2))
            tgt["_err"] -= defend
            dmg = max(0, ep_spend - defend)
            soak = min(dmg, tgt["pools"]["AEP"])
            tgt["pools"]["AEP"] -= soak
            dmg -= soak

            fell = False
            if total >= tn:
                tgt["pools"]["HP"] -= dmg
                if tgt["pools"]["HP"] <= 0:
                    tgt["_alive"] = False
                    fell = True

            why = f"Tenet: {(random.choice(ch.get('constitution',{}).get('tenets',[])) if ch.get('constitution',{}).get('tenets') else '—')} | EP {ep_spend} for pressure."
            md_lines.append(narrator.narr_attack(ch, tgt, ep_spend, tn, d20, total, defend, soak, dmg, fell, why))

        alive_sides = set([ch["side"] for ch in order if ch["_alive"]])
        if len(alive_sides) <= 1:
            break
        rnd += 1

    sides = [ch["side"] for ch in order if ch["_alive"]]
    outcome = f"**Outcome:** {sides[0]} stand(s) victorious." if sides else "**Outcome:** Mutual ruin."
    md_lines.append("")
    md_lines.append(outcome)

    out_md = LOGS / f"story_v2_{stamp}.md"
    out_json = LOGS / f"story_v2_{stamp}.json"
    out_state = {
        "world": WORLD,
        "order": order,
        "outcome": outcome,
        "timestamp": stamp,
    }
    out_md.write_text("\n".join(md_lines))
    out_json.write_text(json.dumps(out_state, indent=2))

    return str(out_md), str(out_json)


# Run once automatically to produce an example log if both character files are present
if (BASE / "pilgrim-001.json").exists() and (BASE / "wolf-001.json").exists():
    # Stage them into initiative/ for a sample encounter
    (INIT / "pilgrim-001.json").write_text((BASE / "pilgrim-001.json").read_text())
    (INIT / "wolf-001.json").write_text((BASE / "wolf-001.json").read_text())
    log_md, log_json = run_story_v2(auto=True, seed=42, max_rounds=10, prose=True)
    print("Sample run complete.")
    print("Markdown:", log_md)
    print("State JSON:", log_json)
else:
    print("Sample files not found. Create initiative/*.json and re-run.")
