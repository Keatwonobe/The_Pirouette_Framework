#!/usr/bin/env python3
"""
combat_runner_v3.py

Adds a 'minloader' behavior layer on top of the previous runner:
- supports old-style actors (no behavior at all)
- supports new triaxial actors with behavior_signature {Gamma, Coherence, K_t}
- still supports fully-authored behavior { "stratagems": [...] }

This assumes you already have:
- distance(...)
- perform_attack(...)
- move_unit(...)
from the earlier script.
"""

import os, json, random

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
INIT_DIR   = os.path.join(BASE_DIR, "initiative")

# ---------------------------------------------------------
# basic utilities (trimmed to essentials)
# ---------------------------------------------------------
def load_initiative():
    chars = []
    if not os.path.isdir(INIT_DIR):
        return chars
    for fn in os.listdir(INIT_DIR):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(INIT_DIR, fn)
        with open(path, "r") as f:
            data = json.load(f)
        # ensure pools
        data.setdefault("pools", {})
        data["pools"].setdefault("HP", 10)
        data["pools"].setdefault("ENT", 0)
        data["pools"].setdefault("AEP", 0)
        data.setdefault("position", {"x": 0, "y": 0})
        chars.append(data)
    return chars

def distance(a, b):
    return abs(a["position"]["x"] - b["position"]["x"]) + abs(a["position"]["y"] - b["position"]["y"])

def move_unit(ch, x, y):
    ch["position"]["x"] = x
    ch["position"]["y"] = y

def get_range(ch):
    return ch.get("stats", {}).get("range", 1)

# you already had something like this; keeping it short here:
def perform_attack(attacker, defender, mode="melee", ep_declared=0, player_roll=False):
    # stub: you can paste your full version here
    ep_spent = min(attacker["pools"].get("ENT", 0), ep_declared)
    attacker["pools"]["ENT"] -= ep_spent
    d20 = random.randint(1, 20)
    tn = 8 + (ep_spent // 2)
    acc = d20
    print(f"» {attacker['name']} attacks {defender['name']} ({mode}), d20={d20} vs TN={tn}")
    if acc < tn:
        print("  miss.")
        return
    dmg = 4 + ep_spent
    defender["pools"]["HP"] = max(0, defender["pools"]["HP"] - dmg)
    print(f"  hits for {dmg}, {defender['name']} HP={defender['pools']['HP']}")

# ---------------------------------------------------------
# MINLOADER SECTION
# ---------------------------------------------------------

def synthesize_behavior_from_signature(sig):
    """
    Turn {Gamma, Coherence, K_t} into an ordered list of stratagems.
    This is the triaxial-to-strats step.
    """
    Γ  = sig.get("Gamma", 5)
    C  = sig.get("Coherence", 5)
    Kt = sig.get("K_t", 5)

    stratagems = []

    # Coherence-first agents want to be in formation
    if C >= 7:
        stratagems.append({"type": "hold_line"})

    # Gamma drives aggression
    if Γ >= 7:
        stratagems.append({"type": "close_strike", "entropy": max(1, Γ // 2)})
        stratagems.append({"type": "ranged_pressure", "entropy": max(0, Γ - 3)})
    elif Γ >= 4:
        stratagems.append({"type": "close_strike", "entropy": 1})
    else:
        stratagems.append({"type": "zone_mark"})

    # low tempo → prep/delay
    if Kt <= 3:
        stratagems.append({"type": "delay_then_strike"})

    # low coherence → allow flanking/orbit
    if C <= 3:
        stratagems.append({"type": "orbit_flank"})

    return stratagems

def install_junk_brain():
    """
    fallback brain if actor has nothing
    """
    return {
        "stratagems": [
            {"type": "close_strike", "entropy": 0},
            {"type": "ranged_pressure", "entropy": 0}
        ]
    }

def minload_actor_brain(actor):
    """
    if actor already has a behavior, keep it
    elif actor has behavior_signature, synthesize
    else give junk brain
    """
    if "behavior" in actor:
        return  # already has brain
    if "behavior_signature" in actor:
        actor["behavior"] = {
            "stratagems": synthesize_behavior_from_signature(actor["behavior_signature"])
        }
        return
    # no brain, no signature → junk brain
    actor["behavior"] = install_junk_brain()

def minload_all(characters):
    for ch in characters:
        minload_actor_brain(ch)

# ---------------------------------------------------------
# BEHAVIOR EXECUTION
# ---------------------------------------------------------

def nearest_enemy(ch, characters):
    enemies = [c for c in characters if c["side"] != ch["side"] and c["pools"]["HP"] > 0]
    if not enemies:
        return None
    return min(enemies, key=lambda t: distance(ch, t))

def ai_execute_stratagem(ch, strat, characters):
    t = strat["type"]
    target = nearest_enemy(ch, characters)

    if t == "hold_line":
        # move toward center of allies
        allies = [a for a in characters if a["side"] == ch["side"] and a["pools"]["HP"] > 0]
        if allies:
            avg_x = sum(a["position"]["x"] for a in allies) / len(allies)
            avg_y = sum(a["position"]["y"] for a in allies) / len(allies)
            # step 1 tile toward centroid
            cx, cy = ch["position"]["x"], ch["position"]["y"]
            if avg_x > cx: cx += 1
            elif avg_x < cx: cx -= 1
            if avg_y > cy: cy += 1
            elif avg_y < cy: cy -= 1
            move_unit(ch, cx, cy)
            print(f"{ch['name']} holds line toward ({cx},{cy}).")
        return

    if not target:
        print(f"{ch['name']} has no targets.")
        return

    if t == "close_strike":
        # move in if needed
        if distance(ch, target) > 1:
            cx, cy = ch["position"]["x"], ch["position"]["y"]
            tx, ty = target["position"]["x"], target["position"]["y"]
            if tx > cx: cx += 1
            elif tx < cx: cx -= 1
            elif ty > cy: cy += 1
            elif ty < cy: cy -= 1
            move_unit(ch, cx, cy)
            print(f"{ch['name']} advances to ({cx},{cy}).")
        if distance(ch, target) <= 1:
            ent = strat.get("entropy", 0)
            perform_attack(ch, target, mode="melee", ep_declared=ent, player_roll=False)
        return

    if t == "ranged_pressure":
        r = get_range(ch)
        if distance(ch, target) <= r:
            ent = strat.get("entropy", 0)
            perform_attack(ch, target, mode="ranged", ep_declared=ent, player_roll=False)
        else:
            # step closer if out of range
            cx, cy = ch["position"]["x"], ch["position"]["y"]
            tx, ty = target["position"]["x"], target["position"]["y"]
            if tx > cx: cx += 1
            elif tx < cx: cx -= 1
            elif ty > cy: cy += 1
            elif ty < cy: cy -= 1
            move_unit(ch, cx, cy)
            print(f"{ch['name']} repositions for ranged pressure to ({cx},{cy}).")
        return

    if t == "zone_mark":
        print(f"[SCENE] {ch['name']} exerts field pressure here (slow / hazard).")
        return

    if t == "orbit_flank":
        # very simple: sidestep horizontally if possible
        cx, cy = ch["position"]["x"], ch["position"]["y"]
        move_unit(ch, cx, cy + 1)
        print(f"{ch['name']} orbits to flank at ({cx},{cy+1}).")
        return

    if t == "delay_then_strike":
        # for now, just narrate
        print(f"{ch['name']} is coiling for a strike next turn.")
        return

def handle_ai_turn(ch, characters):
    beh = ch.get("behavior", {})
    strats = beh.get("stratagems", [])
    if strats:
        # use first that makes sense (for now we just execute in order)
        ai_execute_stratagem(ch, strats[0], characters)
        # optional: rotate stratagems for variety
        beh["stratagems"] = strats[1:] + strats[:1]
    else:
        # fall back to nearest attack
        target = nearest_enemy(ch, characters)
        if target:
            perform_attack(ch, target, mode="melee", ep_declared=0, player_roll=False)

# ---------------------------------------------------------
# PLAYER TURN (simplified)
# ---------------------------------------------------------
def print_targets(characters):
    print("\n=== STATE ===")
    for i, ch in enumerate(characters, start=1):
        pos = ch["position"]
        print(f"[{i}] {ch['id'][:12]:12s} | {ch.get('name','?'):20s} | {ch['side']:10s} | HP={ch['pools']['HP']:3d} @({pos['x']},{pos['y']})")
    print("Commands: look | pass | m x y | a TARGET [e=N] | ra TARGET [e=N] | say ...")
    print("=============\n")

def handle_player_turn(player, characters):
    print(f"\n--- {player['name']}'s turn ---")
    print_targets(characters)
    while True:
        cmd = input("> ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        op = parts[0].lower()
        if op == "pass":
            break
        if op == "m" and len(parts) == 3:
            x, y = int(parts[1]), int(parts[2])
            move_unit(player, x, y)
            print(f"{player['name']} moves to ({x},{y}).")
            continue
        if op in ("a","ra") and len(parts) >= 2:
            idx = int(parts[1])
            target = characters[idx-1]
            mode = "ranged" if op == "ra" else "melee"
            perform_attack(player, target, mode=mode, ep_declared=0, player_roll=True)
            continue
        if op == "look":
            print_targets(characters)
            continue
    

# ---------------------------------------------------------
# INITIATIVE + MAIN LOOP
# ---------------------------------------------------------
def rebuild_initiative(characters):
    return sorted(
        characters,
        key=lambda c: c.get("stats", {}).get("TEP", 10) + c.get("stats", {}).get("init_bonus", 0) + random.randint(0,5),
        reverse=True
    )

def main():
    characters = load_initiative()
    if not characters:
        print("No characters in ./initiative")
        return

    # split sides heuristically
    for ch in characters:
        if ch.get("player", False) or ch["id"].startswith("player-"):
            ch["side"] = "players"
            ch["player"] = True
        else:
            ch.setdefault("side", "hostiles")

    # *** HERE: install brains ***
    minload_all(characters)

    max_rounds = 12
    for rnd in range(1, max_rounds + 1):
        print(f"\n===== ROUND {rnd} =====")
        order = rebuild_initiative(characters)

        # victory check
        alive_sides = {c["side"] for c in characters if c["pools"]["HP"] > 0}
        if len(alive_sides) <= 1:
            print("Combat ends.")
            break

        for ch in order:
            if ch["pools"]["HP"] <= 0:
                continue
            if ch.get("player", False):
                handle_player_turn(ch, characters)
            else:
                handle_ai_turn(ch, characters)

        # purge dead
        characters = [c for c in characters if c["pools"]["HP"] > 0]

    print("Done.")

if __name__ == "__main__":
    main()
