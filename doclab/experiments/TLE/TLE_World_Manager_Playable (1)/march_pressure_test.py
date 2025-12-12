#!/usr/bin/env python3
"""
march_pressure_test.py
Pressure-test for 'The Wasted March' encounter.

Party (players):
  - player-stoneborn-001
  - player-vinemage-001
  - player-sparkblade-001
  - player-necrotist-001

Enemies:
  - desert-raider-001 x3
  - sand-wraith-001 x1

Requires these JSONs in ./initiative/
"""

import os
import json
import random

INIT_DIR = "./initiative"

# ------------------ basic loaders ------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load_character_by_id(ch_id):
    # scan initiative folder for matching id
    for fn in os.listdir(INIT_DIR):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(INIT_DIR, fn)
        with open(path, "r") as f:
            data = json.load(f)
            if data["id"] == ch_id:
                # ensure defaults
                data.setdefault("position", {"x": 0, "y": 0})
                data.setdefault("pools", {})
                data["pools"].setdefault("HP", 10)
                data["pools"].setdefault("ENT", 0)
                data["pools"].setdefault("AEP", 0)
                return data
    raise RuntimeError(f"Character {ch_id} not found in {INIT_DIR}")

# ------------------ render & target menu ------------------

def truncate_id(full_id, length=6):
    return full_id[:length]

def build_target_menu(characters):
    menu = []
    for i, ch in enumerate(characters, start=1):
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
    return menu

def print_target_menu(characters, stage=None):
    print("\n=== THE WASTED MARCH ===")
    if stage:
        print(stage)
    for row in build_target_menu(characters):
        print(f"[{row['idx']:2d}] {row['short']:10s} | {row['name']:20s} | {row['side']:8s} | HP={row['hp']:3d} @ {row['pos']}")
    print("=========================\n")

# ------------------ math utils ------------------

def distance(a, b):
    return abs(a["position"]["x"] - b["position"]["x"]) + abs(a["position"]["y"] - b["position"]["y"])

def move_unit(ch, x, y):
    ch["position"]["x"] = x
    ch["position"]["y"] = y

def get_range(ch):
    return ch.get("stats", {}).get("range", 1)

def get_mod_from_invested(ep_in_attr):
    if ep_in_attr is None:
        return 0
    if ep_in_attr < 10:
        score = ep_in_attr
    else:
        score = ep_in_attr // 2
    return score // 4

def get_attr_mod(ch, attr):
    stats = ch.get("stats", {})
    return get_mod_from_invested(stats.get(attr))

def parse_entropy_spend(parts):
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            if k in ("e", "ent", "ep"):
                try:
                    return int(v)
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

def player_d20_input(prompt="Enter d20 roll (1-20): "):
    while True:
        val = input(prompt).strip()
        try:
            n = int(val)
            if 1 <= n <= 20:
                return n
        except ValueError:
            pass
        print("Please enter an integer from 1 to 20.")

# ------------------ attack / reaction ------------------

def announce_attack(attacker, defender, ctx=None):
    msg = f"» {attacker['name']} declares an attack on {defender['name']}"
    if ctx and ctx.get("mode") == "ranged":
        msg += " (ranged)"
    if ctx and ctx.get("ep_spent", 0) > 0:
        msg += f", spending {ctx['ep_spent']} entropy"
    print(msg + "!")

def offer_reaction(defender, incoming_damage):
    if not defender.get("player", False):
        return None
    print(f"{defender['name']} may react. (block | dodge | defend N | speak | pass)")
    while True:
        cmd = input("(react)> ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        op = parts[0].lower()
        if op == "block":
            return {"type": "block"}
        if op == "dodge":
            return {"type": "dodge"}
        if op == "defend":
            if len(parts) != 2:
                print("Use: defend N")
                continue
            try:
                amt = int(parts[1])
            except ValueError:
                print("N must be integer.")
                continue
            return {"type": "defend", "amount": amt}
        if op == "speak":
            line = input("Say: ")
            print(f"{defender['name']} says: {line}")
            return {"type": "speak"}
        if op == "pass":
            return {"type": "pass"}
        print("Options: block | dodge | defend N | speak | pass")

def compute_accuracy_tn(ep_spent):
    # TN = 8 + floor(EP/2)
    return 8 + (ep_spent // 2)

def resolve_damage(attacker, defender, base_dmg, reaction=None):
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
            spent = spend_entropy(defender, to_spend)
            if spent >= dmg:
                print(f"{defender['name']} spends {spent} entropy to fully defend!")
                dmg = 0
            else:
                dmg = max(0, dmg - spent)
                print(f"{defender['name']} spends {spent} entropy, damage now {dmg}.")
        # speak/pass do nothing

    if dmg > 0:
        defender["pools"]["HP"] = max(0, defender["pools"]["HP"] - dmg)
        print(f"{attacker['name']} deals {dmg} damage to {defender['name']} (HP={defender['pools']['HP']}).")
    else:
        print(f"{attacker['name']}'s attack leaves no lasting wound.")

def perform_attack(attacker, defender, mode="melee", ep_declared=0, player_roll=False):
    announce_attack(attacker, defender, {"mode": mode, "ep_spent": ep_declared})
    ep_spent = spend_entropy(attacker, ep_declared)
    dex_mod = get_attr_mod(attacker, "DEX")
    int_mod = get_attr_mod(attacker, "INT")
    tn = compute_accuracy_tn(ep_spent)
    if player_roll:
        d20 = player_d20_input("Attack d20: ")
    else:
        d20 = random.randint(1, 20)
    acc = d20 + dex_mod + int_mod
    print(f"[ACC] d20({d20}) + DEX({dex_mod}) + INT({int_mod}) = {acc} vs TN {tn}")
    if acc < tn:
        print("Attack misses.")
        return
    # hit
    reaction = offer_reaction(defender, 4 + ep_spent)
    base_dmg = 4 + ep_spent
    resolve_damage(attacker, defender, base_dmg, reaction=reaction)

# ------------------ player turn ------------------

def find_character_by_idx(characters, idx):
    menu = build_target_menu(characters)
    for row in menu:
        if row["idx"] == idx:
            return next(c for c in characters if c["id"] == row["id"])
    return None

def find_character_by_id_or_prefix(characters, token):
    # exact
    for c in characters:
        if c["id"] == token:
            return c
    # prefix
    matches = [c for c in characters if c["id"].startswith(token)]
    if len(matches) == 1:
        return matches[0]
    return None

def handle_player_turn(player, characters):
    print(f"\n--- {player['name']}'s turn ---")
    print_target_menu(characters, "Violet dunes and cutting wind.")
    print("Commands: look | pass | m x y | a TARGET [e=N] | ra TARGET [e=N] | say ...")

    while True:
        cmd = input("> ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        op = parts[0].lower()

        if op == "pass":
            print(f"{player['name']} ends their turn.")
            break

        if op == "look":
            print_target_menu(characters)
            ent = player.get("pools", {}).get("ENT", 0)
            print(f"Your ENT={ent}")
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
            tgt_token = parts[1]
            target = None
            if tgt_token.isdigit():
                target = find_character_by_idx(characters, int(tgt_token))
            if target is None:
                target = find_character_by_id_or_prefix(characters, tgt_token)
            if target is None or target.get("pools", {}).get("HP", 0) <= 0:
                print("Target not found / is down.")
                continue

            # range check
            max_r = get_range(player) if op == "ra" else 1
            if distance(player, target) > max_r:
                print(f"Target out of range (> {max_r}).")
                continue

            ent_decl = parse_entropy_spend(parts[2:])
            perform_attack(player, target, mode=("ranged" if op == "ra" else "melee"), ep_declared=ent_decl, player_roll=True)
            continue

        print("Unknown command.")

# ------------------ AI turn ------------------

def handle_ai_turn(ch, characters):
    # find nearest enemy
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
        # step closer
        cx, cy = ch["position"]["x"], ch["position"]["y"]
        tx, ty = tgt["position"]["x"], tgt["position"]["y"]
        if tx > cx: cx += 1
        elif tx < cx: cx -= 1
        elif ty > cy: cy += 1
        elif ty < cy: cy -= 1
        move_unit(ch, cx, cy)
        print(f"{ch['name']} advances toward {tgt['name']} ({cx},{cy}).")

# ------------------ init combat ------------------

def run_wasted_march_test():
    # players 7-10 from our previous list
    party_ids = [
        "player-stoneborn-001",
        "player-vinemage-001",
        "player-sparkblade-001",
        "player-necrotist-001"
    ]
    enemy_ids = [
        "desert-raider-001",
        "desert-raider-001",
        "desert-raider-001",
        "sand-wraith-001"
    ]

    characters = []

    # load players
    for i, pid in enumerate(party_ids):
        ch = load_character_by_id(pid)
        # plant them in a line
        ch["position"]["x"] = 0
        ch["position"]["y"] = i  # 0..3
        characters.append(ch)

    # load enemies, spread out ahead
    for j, eid in enumerate(enemy_ids):
        ch = load_character_by_id(eid)
        ch["position"]["x"] = 6  # far side of dunes
        ch["position"]["y"] = j  # 0..3
        characters.append(ch)

    # initiative
    order = sorted(characters, key=lambda c: c.get("stats", {}).get("TEP", 10) + c.get("stats", {}).get("init_bonus", 0) + random.randint(0,5), reverse=True)

    max_rounds = 15
    for rnd in range(1, max_rounds + 1):
        print(f"\n===== ROUND {rnd} =====")
        # victory check
        sides_alive = {c["side"] for c in characters if c.get("pools", {}).get("HP", 0) > 0}
        if len(sides_alive) <= 1:
            print("Combat ends.")
            break

        for ch in order:
            if ch.get("pools", {}).get("HP", 0) <= 0:
                continue
            if ch.get("player", False):
                handle_player_turn(ch, characters)
            else:
                handle_ai_turn(ch, characters)

        # cull dead
        characters = [c for c in characters if c.get("pools", {}).get("HP", 0) > 0]

    print("Wasted March test complete.")

if __name__ == "__main__":
    run_wasted_march_test()
