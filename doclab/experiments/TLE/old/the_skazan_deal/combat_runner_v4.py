#!/usr/bin/env python3
"""
combat_runner_v4.py

- scans ./initiative for actors
- installs a brain (existing -> keep, signature -> synthesize, else junk)
- runs combat with player d20 input and entropy-aware attacks
- persists "vessel" state back into ./initiative/<id>.json at the end
"""

import os, json, random, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INIT_DIR = os.path.join(BASE_DIR, "initiative")

# =========================================================
# LOADING / SAVING
# =========================================================

def load_initiative():
    characters = []
    if not os.path.isdir(INIT_DIR):
        return characters
    for fn in os.listdir(INIT_DIR):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(INIT_DIR, fn)
        with open(path, "r") as f:
            data = json.load(f)
        # remember filename so we can write back
        data["_filename"] = fn
        data.setdefault("pools", {})
        data["pools"].setdefault("HP", 10)
        data["pools"].setdefault("ENT", 0)
        data["pools"].setdefault("AEP", 0)
        data.setdefault("position", {"x": 0, "y": 0})
        characters.append(data)
    return characters

def save_back_vessels(characters):
    # write the updated JSONs back to ./initiative
    for ch in characters:
        fn = ch.get("_filename")
        if not fn:
            continue
        out_path = os.path.join(INIT_DIR, fn)
        # don't persist _filename itself
        tmp = dict(ch)
        tmp.pop("_filename", None)
        with open(out_path, "w") as f:
            json.dump(tmp, f, indent=2)

# =========================================================
# MATH / HELPERS
# =========================================================

def distance(a, b):
    return abs(a["position"]["x"] - b["position"]["x"]) + abs(a["position"]["y"] - b["position"]["y"])

def move_unit(ch, x, y):
    ch["position"]["x"] = x
    ch["position"]["y"] = y

def get_range(ch):
    return ch.get("stats", {}).get("range", 1)

def parse_entropy_from_cmd(parts):
    """
    parts like ['a','5','e=6'] or ['ra','3','ent=4']
    """
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            if k in ("e", "ent", "ep"):
                try:
                    return int(v)
                except ValueError:
                    return 0
    return 0

def player_d20():
    while True:
        raw = input("Attack d20: ").strip()
        try:
            n = int(raw)
            if 1 <= n <= 20:
                return n
        except ValueError:
            pass
        print("Give me 1–20.")

# =========================================================
# ENTROPY-AWARE ATTACK
# =========================================================

def perform_attack(attacker, defender, mode="melee", ep_declared=0, player_roll=False):
    """
    - spend up to ep_declared from attacker.pools.ENT
    - TN = 8 + floor(ep_spent / 2)
    - damage = 4 + ep_spent
    - players roll their own d20
    """
    pools = attacker.get("pools", {})
    available_ent = pools.get("ENT", 0)
    ep_spent = min(available_ent, max(0, ep_declared))
    pools["ENT"] = available_ent - ep_spent

    # announce
    print(f"» {attacker['name']} attacks {defender['name']} ({mode}), spending {ep_spent} ENT (has {pools['ENT']} left).")

    if player_roll:
        d20 = player_d20()
    else:
        d20 = random.randint(1, 20)

    # you can add INT/DEX mods back here if you want
    tn = 8 + (ep_spent // 2)
    acc = d20
    print(f"  ACC: d20={d20} vs TN={tn}")
    if acc < tn:
        print("  miss.")
        return

    dmg = 4 + ep_spent
    defender["pools"]["HP"] = max(0, defender["pools"]["HP"] - dmg)
    print(f"  hits for {dmg}, {defender['name']} HP={defender['pools']['HP']}")

# =========================================================
# MINLOADER (brains)
# =========================================================

def synthesize_behavior_from_signature(sig):
    Γ  = sig.get("Gamma", 5)
    C  = sig.get("Coherence", 5)
    Kt = sig.get("K_t", 5)
    stratagems = []
    if C >= 7:
        stratagems.append({"type": "hold_line"})
    if Γ >= 7:
        stratagems.append({"type": "close_strike", "entropy": max(1, Γ // 2)})
        stratagems.append({"type": "ranged_pressure", "entropy": max(0, Γ - 3)})
    elif Γ >= 4:
        stratagems.append({"type": "close_strike", "entropy": 1})
    else:
        stratagems.append({"type": "zone_mark"})
    if Kt <= 3:
        stratagems.append({"type": "delay_then_strike"})
    if C <= 3:
        stratagems.append({"type": "orbit_flank"})
    return stratagems

def install_junk_brain():
    return {
        "stratagems": [
            {"type": "close_strike", "entropy": 0},
            {"type": "ranged_pressure", "entropy": 0}
        ]
    }

def minload_actor_brain(actor):
    if "behavior" in actor:
        return
    if "behavior_signature" in actor:
        actor["behavior"] = {"stratagems": synthesize_behavior_from_signature(actor["behavior_signature"])}
        return
    actor["behavior"] = install_junk_brain()

def minload_all(characters):
    for ch in characters:
        minload_actor_brain(ch)

# =========================================================
# AI EXECUTION
# =========================================================

def nearest_enemy(ch, characters):
    enemies = [c for c in characters if c["side"] != ch["side"] and c["pools"]["HP"] > 0]
    if not enemies:
        return None
    return min(enemies, key=lambda t: distance(ch, t))

def ai_execute_stratagem(ch, strat, characters):
    t = strat["type"]
    target = nearest_enemy(ch, characters)

    if t == "hold_line":
        allies = [a for a in characters if a["side"] == ch["side"] and a["pools"]["HP"] > 0]
        if allies:
            avg_x = sum(a["position"]["x"] for a in allies) / len(allies)
            avg_y = sum(a["position"]["y"] for a in allies) / len(allies)
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
            # step closer
            cx, cy = ch["position"]["x"], ch["position"]["y"]
            tx, ty = target["position"]["x"], target["position"]["y"]
            if tx > cx: cx += 1
            elif tx < cx: cx -= 1
            elif ty > cy: cy += 1
            elif ty < cy: cy -= 1
            move_unit(ch, cx, cy)
            print(f"{ch['name']} repositions to ({cx},{cy}).")
        return

    if t == "zone_mark":
        print(f"[SCENE] {ch['name']} exerts a field here.")
        return

    if t == "orbit_flank":
        cx, cy = ch["position"]["x"], ch["position"]["y"]
        move_unit(ch, cx, cy + 1)
        print(f"{ch['name']} orbits to flank at ({cx},{cy+1}).")
        return

    if t == "delay_then_strike":
        print(f"{ch['name']} is coiling for a strike.")
        return

def handle_ai_turn(ch, characters):
    beh = ch.get("behavior", {})
    strats = beh.get("stratagems", [])
    if strats:
        ai_execute_stratagem(ch, strats[0], characters)
        beh["stratagems"] = strats[1:] + strats[:1]
    else:
        target = nearest_enemy(ch, characters)
        if target:
            perform_attack(ch, target, mode="melee", ep_declared=0, player_roll=False)

# =========================================================
# PLAYER TURN
# =========================================================

def print_targets(characters):
    print("\n=== STATE ===")
    for i, ch in enumerate(characters, start=1):
        pos = ch["position"]
        print(f"[{i}] {ch['id'][:12]:12s} | {ch.get('name','?'):22s} | {ch['side']:10s} | HP={ch['pools']['HP']:3d} @({pos['x']},{pos['y']})")
    print("Commands: look | pass | m x y | a TARGET [e=N] | ra TARGET [e=N] | say ...")
    print("=============\n")

def handle_player_turn(player, characters):
    print(f"\n--- {player['name']}'s turn ---")
    while True:
        print_targets(characters)
        cmd = input("> ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        op = parts[0].lower()

        if op == "pass":
            break

        if op == "look":
            continue

        if op == "say":
            line = cmd[len("say"):].strip()
            print(f"{player['name']} says: {line}")
            continue

        if op == "m" and len(parts) == 3:
            x, y = int(parts[1]), int(parts[2])
            move_unit(player, x, y)
            print(f"{player['name']} moves to ({x},{y}).")
            continue

        if op in ("a", "ra") and len(parts) >= 2:
            # target can be index
            try:
                idx = int(parts[1])
                target = characters[idx-1]
            except (ValueError, IndexError):
                print("Bad target.")
                continue

            ent_decl = parse_entropy_from_cmd(parts[2:])
            mode = "ranged" if op == "ra" else "melee"

            # range check for ranged
            max_r = get_range(player) if mode == "ranged" else 1
            if distance(player, target) > max_r:
                print(f"Target out of range (> {max_r}).")
                continue

            perform_attack(player, target, mode=mode, ep_declared=ent_decl, player_roll=True)
            continue

        print("Unknown command.")

# =========================================================
# INITIATIVE + MAIN
# =========================================================

def rebuild_initiative(characters):
    return sorted(
        characters,
        key=lambda c: c.get("stats", {}).get("TEP", 10) + c.get("stats", {}).get("init_bonus", 0) + random.randint(0,5),
        reverse=True
    )

def main():
    chars = load_initiative()
    if not chars:
        print("No characters in ./initiative")
        return

    # sides
    for ch in chars:
        if ch.get("player", False) or ch["id"].startswith("player-"):
            ch["side"] = "players"
            ch["player"] = True
        else:
            ch.setdefault("side", "raiders")

    # install brains
    minload_all(chars)

    max_rounds = 15
    for rnd in range(1, max_rounds + 1):
        print(f"\n===== ROUND {rnd} =====")
        order = rebuild_initiative(chars)

        # victory check
        alive_sides = {c["side"] for c in chars if c["pools"]["HP"] > 0}
        if len(alive_sides) <= 1:
            print("Combat ends.")
            break

        for ch in order:
            if ch["pools"]["HP"] <= 0:
                continue
            if ch.get("player", False):
                handle_player_turn(ch, chars)
            else:
                handle_ai_turn(ch, chars)

        # prune
        chars = [c for c in chars if c["pools"]["HP"] > 0]

    # VESSEL WRITEBACK
    now = datetime.datetime.utcnow().isoformat()
    for ch in chars:
        vessel = ch.setdefault("vessel", {})
        history = vessel.setdefault("history", [])
        history.append({
            "stamp": now,
            "note": "participated in combat_runner_v4 session"
        })

    save_back_vessels(chars)
    print("Done, vessels updated.")

if __name__ == "__main__":
    main()
