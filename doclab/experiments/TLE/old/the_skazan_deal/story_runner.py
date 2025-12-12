#!/usr/bin/env python3
import json, random, datetime, argparse
from pathlib import Path

BASE = Path(__file__).parent
ROSTER = BASE/"roster"
INIT = BASE/"initiative"
LOGS = BASE/"logs"
WORLD = json.loads((BASE/"world.json").read_text())

def load_char(fp):
    j = json.loads(Path(fp).read_text())
    j["_alive"] = j["pools"]["HP"]>0
    j["_err"] = j["stats"]["ERR"]
    j["_spoken"] = False
    return j

def roll_d20(supplied=None):
    if supplied is not None:
        try:
            v = int(supplied); return max(1,min(20,v))
        except: pass
    return random.randint(1,20)

def tn_from_ep(ep): return WORLD["rules"]["tn_base"] + (ep//2)
def atk_total(j, die): return die + (j["stats"]["DEX"]//4) + (j["stats"]["INT"]//4)

def prompt_choice(prompt, options, default=None):
    opts = "/".join(options); dtext = f" [{default}]" if default else ""
    while True:
        val = input(f"{prompt} ({opts}){dtext}: ").strip().lower()
        if not val and default: return default
        if val in options: return val
        print("Choose:", options)

def prompt_int(prompt, mn=0, mx=None, default=None):
    dtext = f" [{default}]" if default is not None else ""
    while True:
        s = input(f"{prompt}{dtext}: ").strip()
        if not s and default is not None: return default
        try:
            v = int(s)
            if v < mn: print(f"Min {mn}"); continue
            if mx is not None and v > mx: print(f"Max {mx}"); continue
            return v
        except: print("Enter an integer.")

def npc_why(ch, verb, target=None, ep=0):
    arch = ch["persona"]["archetype"]
    why = []
    if verb=="talk": why.append("Seek advantage without bloodshed.")
    if verb=="defend": why.append("Preserve resources under threat.")
    if verb=="reposition": why.append("Improve position and reduce exposure.")
    if verb=="attack":
        why.append({
            "assassin":"Exploit weakness quickly.",
            "intrepid":"Burst early to shock morale.",
            "guardian":"Pressure hostiles; guard allies.",
            "parleyist":"Demonstrate resolve to reinforce negotiation."
        }.get(arch,"Probe defenses and learn."))
    tenets = ch.get("constitution",{}).get("tenets",[])
    if tenets: why.append(f"Tenet: {random.choice(tenets)}")
    why.append(f"EP rationale: spend {ep} (TN {tn_from_ep(ep)})")
    if target: why.append(f"Target: {target['name']} (HP {target['pools']['HP']}, AEP {target['pools']['AEP']})")
    return " | ".join(why)

def choose_target(ch, others):
    enemies=[o for o in others if o["side"]!=ch["side"] and o["_alive"]]
    if not enemies: return None
    enemies.sort(key=lambda o:(o["pools"]["HP"], o["pools"]["AEP"]))
    return enemies[0]

def run_story(auto=False):
    chars = [load_char(fp) for fp in INIT.glob("*.json")]
    if not chars:
        print("No characters in initiative/."); return
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log = [f"# Story Combat {stamp}", f"World: {WORLD['name']}"]
    order = sorted([ch for ch in chars if ch["_alive"]], key=lambda c: -(random.randint(1,20) + c["stats"]["init_bonus"] + (c["stats"]["DEX"]//4)))

    rnd = 1
    while True:
        for ch in order:
            if ch["_alive"]: ch["_err"] = ch["stats"]["ERR"]; ch["_spoken"]=False
        log.append(f"\\n## Round {rnd}")
        for ch in order:
            if not ch["_alive"]: continue
            others = [o for o in order if o["id"]!=ch["id"]]
            is_player = bool(ch.get("player")) and ch["side"]=="players" and not auto
            if is_player:
                print(f"\\n--- {ch['name']}'s turn ---")
                print(f"ERR {ch['_err']} | HP {ch['pools']['HP']} | AEP {ch['pools']['AEP']}")
                verb = prompt_choice("Action", ["talk","attack","defend","reposition"], default="attack")
                ep = 0; tgt = None
                if verb in ("attack","defend","reposition"):
                    ep = prompt_int("EP to spend", mn=1, mx=max(1,ch["_err"]), default=min(3, ch["_err"] or 1))
                if verb=="attack":
                    alive_enemies=[o for o in others if o["side"]!=ch["side"] and o["_alive"]]
                    for i,e in enumerate(alive_enemies, start=1):
                        print(f"  [{i}] {e['name']}  HP:{e['pools']['HP']} AEP:{e['pools']['AEP']}")
                    if alive_enemies:
                        idx = prompt_int("Target #", mn=1, mx=len(alive_enemies), default=1)
                        tgt = alive_enemies[idx-1]
                why = input("Why? ").strip() or "(kept own counsel)"
                d = roll_d20(supplied=input("d20 (or blank for auto): ").strip()) if verb=="attack" else None
            else:
                if ch["_err"]<=0:
                    log.append(f"- {ch['name']} pauses (no ERR)."); continue
                if ch["persona"]["archetype"]=="parleyist" and not ch["_spoken"] and random.random()<0.5:
                    verb, ep, tgt = "talk", 0, None
                else:
                    verb, tgt = "attack", choose_target(ch, others)
                    ep = max(1, min(ch["_err"], 3 if ch["persona"]["archetype"]!="intrepid" else ch["_err"]))
                why = npc_why(ch, verb, tgt, ep)
                d = roll_d20() if verb=="attack" else None
            # resolve
            if verb=="talk":
                ch["_spoken"]=True
                log.append(f"- **{ch['name']}** speaks: _“{why if is_player and why!='(kept own counsel)' else 'Lay down arms and live.'}”_")
                continue
            if verb=="defend":
                spend = min(ep, ch["_err"]); ch["_err"] -= spend
                log.append(f"- **{ch['name']}** prepares ({spend} EP). _Why:_ {why}")
                continue
            if verb=="reposition":
                spend = min(ep, ch["_err"]); ch["_err"] -= spend
                log.append(f"- **{ch['name']}** repositions {spend} squares. _Why:_ {why}")
                continue
            if verb=="attack":
                spend = min(ep, ch["_err"]); ch["_err"] -= spend
                tn = tn_from_ep(spend); total = d if d is not None else roll_d20()
                total = (total if isinstance(total,int) else 10)
                roll_total = total + (ch["stats"]["DEX"]//4) + (ch["stats"]["INT"]//4)
                line = f"- **{ch['name']}** attacks (EP {spend}, TN {tn}) — d20 {total} → total {roll_total}. _Why:_ {why}"
                if not tgt or not tgt["_alive"]:
                    log.append(line + " Target unavailable."); continue
                if roll_total < tn:
                    log.append(line + " **Miss.**"); continue
                defend = min(spend, max(0, tgt["_err"]//2)); tgt["_err"] -= defend
                dmg = max(0, spend - defend)
                soak = min(dmg, tgt["pools"]["AEP"]); tgt["pools"]["AEP"] -= soak; dmg -= soak
                tgt["pools"]["HP"] -= dmg
                if tgt["pools"]["HP"]<=0: tgt["_alive"]=False
                log.append(line + f" **Hit!** Def {defend}, Soak {soak}, HP -{dmg} → {tgt['pools']['HP']}" + ("" if tgt["_alive"] else f". **{tgt['name']} falls.**"))
        alive_sides = set([ch["side"] for ch in order if ch["_alive"]])
        if len(alive_sides)<=1: break
        rnd += 1
    sides = [ch["side"] for ch in order if ch["_alive"]]
    log.append(f"\\n**Outcome:** {sides[0]} stand(s) victorious." if sides else "\\n**Outcome:** Mutual ruin.")
    out = LOGS/f"story_{stamp}.md"
    Path(out).write_text("\\n".join(log))
    print(f"Wrote story log: {out}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--auto", action="store_true")
    args = ap.parse_args()
    run_story(auto=args.auto)
