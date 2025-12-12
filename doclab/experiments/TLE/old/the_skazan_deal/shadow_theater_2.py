#!/usr/bin/env python3
"""
Shadow Theater v2
- Player-driven terminal turns
- Entropy-aware accuracy (TLE universal accuracy)   # see TLE-001 §3.1
- Ranged attacks
- Player-provided d20 rolls (no auto RNG for PCs)
- Target list with index + truncated id + name
"""

import os
import json
import random
import math

INIT_DIR = "./initiative"
SCENE_DIR = "./scenes"
STAGE_DIR = "./stages"

# ------------------------------------------------------------------------------
# LOADING
# ------------------------------------------------------------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load_scene(scene_name):
    return load_json(os.path.join(SCENE_DIR, scene_name))

def load_stage(stage_name):
    return load_json(os.path.join(STAGE_DIR, stage_name))

def load_characters(ids=None):
    chars = []
    for fn in os.listdir(INIT_DIR):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(INIT_DIR, fn), "r") as f:
            data = json.load(f)
            data.setdefault("position", {"x": 0, "y": 0})
            # pools defaults
            data.setdefault("pools", {})
            data["pools"].setdefault("HP", 10)
            data["pools"].setdefault("ENT", 0)   # entropy spendable in combat
            data["pools"].setdefault("AEP", 0)
            if ids is None or data["id"] in ids:
                chars.append(data)
    return chars

# ------------------------------------------------------------------------------
# RENDER / TARGET MENU
# ------------------------------------------------------------------------------

def truncate_id(full_id, length=6):
    return full_id[:length]

def build_target_menu(characters):
    """
    Returns a list of dicts:
    [
      { "idx": 1, "id": "polite-pyro-001", "short": "polite-", "name": "Kindlefoot", "side": "players", ...}
    ]
    """
    menu = []
    i = 1
    for ch in characters:
        hp = ch.get("pools", {}).get("HP", 0)
        pos = ch.get("position", {})
        menu.append({
            "idx": i,
            "id": ch["id"],
            "short": truncate_id(ch["id"]),
            "name": ch.get("name", ch["id"]),
            "side": ch.get("side", "?"),
            "hp": hp,
            "pos": (pos.get("x", 0), pos.get("y", 0)),
            "player": ch.get("player", False),
        })
        i += 1
    return menu

def print_target_menu(characters, stage=None):
    print("\n=== SHADOW STAGE ===")
    if stage:
        print(f"Stage: {stage.get('name','?')} – {stage.get('desc','')}")
    menu = build_target_menu(characters)
    for row in menu:
        print(f"[{row['idx']:2d}] {row['short']:8s} | {row['name']:20s} | {row['side']:8s} | HP={row['hp']:3d} @ {row['pos']}")
    print("=====================\n")

def find_character_by_idx(characters, idx):
    menu = build_target_menu(characters)
    for row in menu:
        if row["idx"] == idx:
            return next(c for c in characters if c["id"] == row["id"])
    return None

def find_character_by_id(characters, thing):
    # try exact first
    for c in characters:
        if c["id"] == thing:
            return c
    # try prefix
    matches = [c for c in characters if c["id"].startswith(thing)]
    if len(matches) == 1:
        return matches[0]
    return None

# ------------------------------------------------------------------------------
# UTILS
# ------------------------------------------------------------------------------

def distance(a, b):
    return abs(a["position"]["x"] - b["position"]["x"]) + abs(a["position"]["y"] - b["position"]["y"])

def move_unit(ch, x, y):
    ch["position"]["x"] = x
    ch["position"]["y"] = y

def get_range(ch):
    # default melee 1
    return ch.get("stats", {}).get("range", 1)

def get_mod_from_invested(ep_in_attr):
    """
    Rules say: Score = floor(EP / 2), Mod = floor(Score / 4)
    We'll accept either raw EP or score; if small number, it's probably score.
    """
    if ep_in_attr is None:
        return 0
    # if ep is small (<10), assume it's already a score
    if ep_in_attr < 10:
        score = ep_in_attr
    else:
        score = ep_in_attr // 2
    return score // 4

def get_attr_mod(ch, attr):
    # try stats[attr] as EP invested
    stats = ch.get("stats", {})
    val = stats.get(attr)
    if val is None:
        return 0
    return get_mod_from_invested(val)

def get_initiative_score(ch):
    stats = ch.get("stats", {})
    base = stats.get("TEP", 10)
    bonus = stats.get("init_bonus", 0)
    return base + bonus + random.randint(0, 5)

def parse_entropy_spend(parts):
    for p in parts:
        if "=" in p:
            key, val = p.split("=", 1)
            if key in ("e", "ent", "ep"):
                try:
                    return int(val)
                except ValueError:
                    return 0
    return 0

def spend_entropy(ch, amount):
    ent = ch.get("pools", {}).get("ENT", 0)
    if amount <= 0 or ent <= 0:
        return 0
    spent = min(ent, amount)
    ch["pools"]["ENT"] = ent - spent
    return spent

def player_d20_input(prompt="Enter d20 roll: "):
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if 1 <= val <= 20:
                return val
            else:
                print("d20 must be 1–20.")
        except ValueError:
            print("Enter an integer 1–20.")

# ------------------------------------------------------------------------------
# ATTACK FLOW (TLE accuracy)  (TN = 8 + floor(EP_spent_on_damage / 2))
# ------------------------------------------------------------------------------

def announce_attack(attacker, defender, ctx=None):
    bits = []
    bits.append(f"» {attacker['name']} declares an attack on {defender['name']}")
    if ctx and ctx.get("mode") == "ranged":
        bits.append("(ranged)")
    if ctx and ctx.get("ep_spent", 0) > 0:
        bits.append(f"spending {ctx['ep_spent']} entropy")
    print(" ".join(bits) + "!")

def offer_reaction(defender, incoming_damage):
    """
    Defender can:
    - block (half)
    - dodge (50%)
    - defend N (spend entropy to nullify or reduce)  # from active defense idea
    - speak
    - pass
    """
    print(f"{defender['name']} may react. Options: block | dodge | defend N | speak | pass")
    while True:
        resp = input("(react)> ").strip()
        if not resp:
            continue
        parts = resp.split()
        op = parts[0].lower()
        if op == "block":
            return {"type": "block"}
        elif op == "dodge":
            return {"type": "dodge"}
        elif op == "defend":
            if len(parts) != 2:
                print("Use: defend N")
                continue
            try:
                amt = int(parts[1])
            except ValueError:
                print("N must be an integer.")
                continue
            # we'll interpret this as: spend N ENT to soak up to N damage
            return {"type": "defend", "amount": amt}
        elif op == "speak":
            line = input("Say: ")
            print(f"{defender['name']} says: {line}")
            # doesn't defend, but returns so we can still take damage
            return {"type": "speak"}
        elif op == "pass":
            return {"type": "pass"}
        else:
            print("Options: block | dodge | defend N | speak | pass")

def resolve_damage(attacker, defender, base_dmg, reaction=None):
    """
    base_dmg is after entropy spend.
    reaction can reduce it.
    """
    dmg = base_dmg
    if reaction:
        if reaction["type"] == "block":
            dmg = max(1, dmg // 2)
            print(f"{defender['name']} blocks! Damage now {dmg}.")
        elif reaction["type"] == "dodge":
            if random.random() < 0.5:
                dmg = 0
                print(f"{defender['name']} dodges completely!")
            else:
                print(f"{defender['name']} fails to dodge.")
        elif reaction["type"] == "defend":
            to_spend = reaction["amount"]
            actually_spent = spend_entropy(defender, to_spend)
            if actually_spent >= dmg:
                print(f"{defender['name']} spends {actually_spent} entropy to fully defend!")
                dmg = 0
            else:
                dmg = max(0, dmg - actually_spent)
                print(f"{defender['name']} spends {actually_spent} entropy to reduce damage to {dmg}.")
        # 'speak'/'pass' do nothing
    if dmg > 0:
        defender["pools"]["HP"] = max(0, defender["pools"]["HP"] - dmg)
        print(f"{attacker['name']} deals {dmg} damage to {defender['name']} (HP={defender['pools']['HP']}).")
    else:
        print(f"{attacker['name']}'s attack leaves no lasting wound.")

def compute_accuracy_tn(ep_spent_on_damage):
    # TN = 8 + floor(EP_spent / 2)  (from your rules)
    return 8 + (ep_spent_on_damage // 2)

def perform_attack(attacker, defender, mode="melee", ep_declared=0, player_roll=False):
    """
    Full TLE-style attack:
      - declare EP (we spend it from ENT)
      - roll accuracy: d20 + DEX_mod + INT_mod vs TN
      - on hit: target reacts
    """

    announce_attack(attacker, defender, {"mode": mode, "ep_spent": ep_declared})

    # spend EP from attacker now
    ep_spent = spend_entropy(attacker, ep_declared)

    # ACCURACY
    dex_mod = get_attr_mod(attacker, "DEX")
    int_mod = get_attr_mod(attacker, "INT")
    tn = compute_accuracy_tn(ep_spent)
    if player_roll:
        d20 = player_d20_input("Attack d20: ")
    else:
        d20 = random.randint(1, 20)
    acc_total = d20 + dex_mod + int_mod
    print(f"[ACC] d20({d20}) + DEX_mod({dex_mod}) + INT_mod({int_mod}) = {acc_total} vs TN {tn}")

    if acc_total < tn:
        print(f"{attacker['name']}'s attack fails to connect (miss).")
        return

    # HIT: defender may react
    reaction = None
    if defender.get("player", False):
        reaction = offer_reaction(defender, ep_spent if ep_spent > 0 else 4)

    # damage model: base 4 + ep_spent
    base_damage = 4 + ep_spent
    resolve_damage(attacker, defender, base_damage, reaction=reaction)

# ------------------------------------------------------------------------------
# PLAYER TURN (continuous)
# ------------------------------------------------------------------------------

def handle_player_turn(player, characters, stage=None):
    print(f"\n--- {player['name']}'s turn ---")
    print_target_menu(characters, stage)
    print("Commands:")
    print("  look                   -> reprint battlefield")
    print("  pass                   -> end turn")
    print("  say ...                -> speak")
    print("  m x y                  -> move")
    print("  a TARGET [e=N]         -> melee attack by id/prefix/index")
    print("  ra TARGET [e=N]        -> ranged attack by id/prefix/index")
    print("  targets                -> show numbered list")
    print("Budgets: ENT={}, AEP={}".format(
        player.get("pools", {}).get("ENT", 0),
        player.get("pools", {}).get("AEP", 0),
    ))

    while True:
        cmd = input("> ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        op = parts[0].lower()

        if op == "pass":
            print(f"{player['name']} ends their turn.")
            break

        elif op == "look" or op == "targets":
            print_target_menu(characters, stage)
            ent = player.get("pools", {}).get("ENT", 0)
            print(f"{player['name']} ENT={ent}")
            continue

        elif op == "say":
            line = cmd[len("say"):].strip()
            print(f"{player['name']} says: {line}")
            continue

        elif op == "m" and len(parts) == 3:
            x, y = int(parts[1]), int(parts[2])
            move_unit(player, x, y)
            print(f"{player['name']} moves to ({x},{y}).")
            continue

        # melee
        elif op == "a" and len(parts) >= 2:
            target_token = parts[1]
            target = None
            # try index
            if target_token.isdigit():
                target = find_character_by_idx(characters, int(target_token))
            if target is None:
                target = find_character_by_id(characters, target_token)
            if target is None or target.get("pools", {}).get("HP", 0) <= 0:
                print("Target not found or is down.")
                continue
            # melee range check
            if distance(player, target) > 1:
                print("Target out of melee range.")
                continue
            ep_declared = parse_entropy_spend(parts[2:])
            perform_attack(player, target, mode="melee", ep_declared=ep_declared, player_roll=True)
            continue

        # ranged
        elif op == "ra" and len(parts) >= 2:
            target_token = parts[1]
            target = None
            if target_token.isdigit():
                target = find_character_by_idx(characters, int(target_token))
            if target is None:
                target = find_character_by_id(characters, target_token)
            if target is None or target.get("pools", {}).get("HP", 0) <= 0:
                print("Target not found or is down.")
                continue
            max_r = get_range(player)
            if distance(player, target) > max_r:
                print(f"Target out of ranged distance (> {max_r}).")
                continue
            ep_declared = parse_entropy_spend(parts[2:])
            perform_attack(player, target, mode="ranged", ep_declared=ep_declared, player_roll=True)
            continue

        else:
            print("Unrecognized command.")

# ------------------------------------------------------------------------------
# AI TURN
# ------------------------------------------------------------------------------

def handle_ai_turn(ch, characters):
    # simple: nearest enemy
    targets = [o for o in characters if o["side"] != ch["side"] and o.get("pools", {}).get("HP", 0) > 0]
    if not targets:
        print(f"{ch['name']} has no targets.")
        return
    tgt = min(targets, key=lambda t: distance(ch, t))
    d = distance(ch, tgt)
    max_r = get_range(ch)
    if d <= 1:
        perform_attack(ch, tgt, mode="melee", ep_declared=0, player_roll=False)
    elif d <= max_r and max_r > 1:
        perform_attack(ch, tgt, mode="ranged", ep_declared=0, player_roll=False)
    else:
        # walk toward
        cx, cy = ch["position"]["x"], ch["position"]["y"]
        tx, ty = tgt["position"]["x"], tgt["position"]["y"]
        if tx > cx: cx += 1
        elif tx < cx: cx -= 1
        elif ty > cy: cy += 1
        elif ty < cy: cy -= 1
        move_unit(ch, cx, cy)
        print(f"{ch['name']} advances toward {tgt['name']} ({cx},{cy}).")

# ------------------------------------------------------------------------------
# MAIN SCENE RUNNER
# ------------------------------------------------------------------------------

def run_scene(scene_file):
    scene = load_scene(scene_file)
    stage = load_stage(scene["stage"])
    characters = load_characters(scene["actors"])
    # initial initiative
    order = sorted(characters, key=lambda c: get_initiative_score(c), reverse=True)
    max_rounds = scene.get("max_rounds", 10)

    for round_no in range(1, max_rounds + 1):
        print(f"\n===== ROUND {round_no} =====")
        # victory check
        alive_sides = {c["side"] for c in characters if c.get("pools", {}).get("HP", 0) > 0}
        if len(alive_sides) <= 1:
            print("Scene ends.")
            break

        for ch in order:
            if ch.get("pools", {}).get("HP", 0) <= 0:
                continue
            if ch.get("player", False):
                handle_player_turn(ch, characters, stage)
            else:
                handle_ai_turn(ch, characters)

        # cull dead
        characters = [c for c in characters if c.get("pools", {}).get("HP", 0) > 0]
        # (optional) re-sort each round if you want dynamic init
        # order = sorted(characters, key=lambda c: get_initiative_score(c), reverse=True)

    print("Shadow play complete.")

if __name__ == "__main__":
    # example:
    # python shadow_theater_v2.py
    run_scene("scene_meadow_raid.json")
