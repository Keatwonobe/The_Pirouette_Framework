#!/usr/bin/env python3
import os, json, random

# make path explicit so Windows/OneDrive shenanigans don't break it
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INIT_DIR = os.path.join(BASE_DIR, "initiative")

# ------------------------------------------------------------
# 1) show me what’s actually in ./initiative
# ------------------------------------------------------------
def discover_initiative():
    found = []
    if not os.path.isdir(INIT_DIR):
        print(f"[ERR] initiative folder not found at {INIT_DIR}")
        return found
    for fn in os.listdir(INIT_DIR):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(INIT_DIR, fn)
        try:
            with open(path, "r") as f:
                data = json.load(f)
            file_id = data.get("id", "<no id>")
            found.append({"file": fn, "id": file_id, "data": data})
        except Exception as e:
            print(f"[WARN] could not read {fn}: {e}")
    print("\n[INIT SCAN] I found these character IDs:")
    for item in found:
        print(f"  - file: {item['file']}   id: {item['id']}")
    print()
    return found

# ------------------------------------------------------------
# 2) util bits
# ------------------------------------------------------------
def distance(a, b):
    return abs(a["position"]["x"] - b["position"]["x"]) + abs(a["position"]["y"] - b["position"]["y"])

def move_unit(ch, x, y):
    ch["position"]["x"] = x
    ch["position"]["y"] = y

def get_range(ch):
    return ch.get("stats", {}).get("range", 1)

def get_mod_from_invested(ep):
    if ep is None:
        return 0
    if ep < 10:
        score = ep
    else:
        score = ep // 2
    return score // 4

def get_attr_mod(ch, attr):
    return get_mod_from_invested(ch.get("stats", {}).get(attr))

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

def player_d20_input(prompt="Enter d20 (1-20): "):
    while True:
        raw = input(prompt).strip()
        try:
            n = int(raw)
            if 1 <= n <= 20:
                return n
        except ValueError:
            pass
        print("Give me an integer 1–20.")

# ------------------------------------------------------------
# 3) attack + reactions
# ------------------------------------------------------------
def announce_attack(attacker, defender, ctx=None):
    msg = f"» {attacker['name']} attacks {defender['name']}"
    if ctx and ctx.get("mode") == "ranged":
        msg += " (ranged)"
    if ctx and ctx.get("ep_spent", 0):
        msg += f", spending {ctx['ep_spent']} entropy"
    print(msg + "!")

def offer_reaction(defender, incoming_damage):
    if not defender.get("player", False):
        return None
    print(f"{defender['name']} may react: block | dodge | defend N | speak | pass")
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
                print("use: defend N")
                continue
            try:
                amt = int(parts[1])
            except ValueError:
                print("N must be int")
                continue
            return {"type": "defend", "amount": amt}
        if op == "speak":
            line = input("Say: ")
            print(f"{defender['name']} says: {line}")
            return {"type": "speak"}
        if op == "pass":
            return {"type": "pass"}

def compute_accuracy_tn(ep_spent):
    return 8 + (ep_spent // 2)

def resolve_damage(attacker, defender, base_dmg, reaction=None):
    dmg = base_dmg
    if reaction:
        if reaction["type"] == "block":
            dmg = max(1, dmg // 2)
            print(f"{defender['name']} blocks → {dmg}")
        elif reaction["type"] == "dodge":
            if random.random() < 0.5:
                print(f"{defender['name']} dodges completely!")
                dmg = 0
            else:
                print(f"{defender['name']} fails to dodge.")
        elif reaction["type"] == "defend":
            spent = spend_entropy(defender, reaction["amount"])
            if spent >= dmg:
                print(f"{defender['name']} spends {spent} ENT to nullify.")
                dmg = 0
            else:
                dmg -= spent
                print(f"{defender['name']} spends {spent} ENT → dmg {dmg}")
    if dmg > 0:
        defender["pools"]["HP"] = max(0, defender["pools"]["HP"] - dmg)
        print(f"{attacker['name']} deals {dmg} to {defender['name']} (HP={defender['pools']['HP']})")
    else:
        print(f"{attacker['name']}'s attack leaves no wound.")

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
    print(f"[ACC] {d20} + {dex_mod} + {int_mod} = {acc} vs TN {tn}")
    if acc < tn:
        print("Miss.")
        return
    reaction = offer_reaction(defender, 4 + ep_spent)
    base_dmg = 4 + ep_spent
    resolve_damage(attacker, defender, base_dmg, reaction=reaction)

# ------------------------------------------------------------
# 4) player & AI turns
# ------------------------------------------------------------
def print_targets(characters):
    print("\n=== WASTED MARCH STATE ===")
    for i, ch in enumerate(characters, start=1):
        hp = ch.get("pools", {}).get("HP", 0)
        pos = ch.get("position", {})
        print(f"[{i:2d}] {ch['id'][:10]:10s} | {ch.get('name','?'):20s} | {ch['side']:8s} | HP={hp:3d} @ ({pos['x']},{pos['y']})")
    print("===========================\n")

def find_target(characters, token):
    # index?
    if token.isdigit():
        idx = int(token)
        if 1 <= idx <= len(characters):
            return characters[idx-1]
    # exact or prefix
    for ch in characters:
        if ch["id"] == token or ch["id"].startswith(token):
            return ch
    return None

def handle_player_turn(player, characters):
    print(f"\n--- {player['name']}'s turn ---")
    print_targets(characters)
    print("Commands: look | pass | m x y | a TARGET [e=N] | ra TARGET [e=N] | say ...")
    while True:
        cmd = input("> ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        op = parts[0].lower()

        if op == "pass":
            print(f"{player['name']} ends turn.")
            break
        if op == "look":
            print_targets(characters)
            ent = player.get("pools", {}).get("ENT", 0)
            print(f"ENT={ent}")
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
        if op in ("a","ra") and len(parts) >= 2:
            tgt = find_target(characters, parts[1])
            if not tgt or tgt.get("pools", {}).get("HP", 0) <= 0:
                print("No such target / target down.")
                continue
            max_r = get_range(player) if op == "ra" else 1
            if distance(player, tgt) > max_r:
                print(f"Target out of range (> {max_r}).")
                continue
            ent_decl = parse_entropy_spend(parts[2:])
            perform_attack(player, tgt, mode=("ranged" if op=="ra" else "melee"),
                           ep_declared=ent_decl, player_roll=True)
            continue
        print("Unknown command.")

def handle_ai_turn(ch, characters):
    targets = [c for c in characters if c["side"] != ch["side"] and c.get("pools", {}).get("HP", 0) > 0]
    if not targets:
        print(f"{ch['name']} has no targets.")
        return
    tgt = min(targets, key=lambda t: distance(ch, t))
    d = distance(ch, tgt)
    r = get_range(ch)
    if d <= 1:
        perform_attack(ch, tgt, mode="melee", ep_declared=0, player_roll=False)
    elif d <= r and r > 1:
        perform_attack(ch, tgt, mode="ranged", ep_declared=0, player_roll=False)
    else:
        cx, cy = ch["position"]["x"], ch["position"]["y"]
        tx, ty = tgt["position"]["x"], tgt["position"]["y"]
        if tx > cx: cx += 1
        elif tx < cx: cx -= 1
        elif ty > cy: cy += 1
        elif ty < cy: cy -= 1
        move_unit(ch, cx, cy)
        print(f"{ch['name']} advances toward {tgt['name']} ({cx},{cy}).")

# ------------------------------------------------------------
# 5) initiative
# ------------------------------------------------------------
def rebuild_initiative(characters):
    return sorted(
        characters,
        key=lambda c: c.get("stats", {}).get("TEP", 10) + c.get("stats", {}).get("init_bonus", 0) + random.randint(0,5),
        reverse=True
    )

# ------------------------------------------------------------
# 6) main test runner
# ------------------------------------------------------------
def run_wasted_march_test():
    # 1) scan what's actually in initiative
    found = discover_initiative()
    if not found:
        print("No JSONs in ./initiative — run the scene_assembler first.")
        return

    characters = []

    # 2) separate players vs enemies based on id / flag
    players = []
    enemies = []
    for item in found:
        data = item["data"]
        cid = item["id"]
        # normalize basics
        data.setdefault("position", {"x": 0, "y": 0})
        data.setdefault("pools", {})
        data["pools"].setdefault("HP", 10)
        data["pools"].setdefault("ENT", 0)
        data["pools"].setdefault("AEP", 0)

        if data.get("player", False) or cid.startswith("player-"):
            players.append(data)
        else:
            enemies.append(data)

    if not players:
        print("I didn't find any players (ids starting with 'player-'). Mark at least one as player.")
        return
    if not enemies:
        print("I didn't find any enemies (non-player ids). Add desert-raider-001.json etc.")
        return

    # 3) place them on the field
    # players on the left
    for i, ch in enumerate(players):
        ch["position"]["x"] = 0
        ch["position"]["y"] = i
        ch["side"] = "players"
        ch["player"] = True
        characters.append(ch)

    # enemies on the right
    for i, ch in enumerate(enemies):
        ch["position"]["x"] = 6
        ch["position"]["y"] = i
        # keep their side if they have one, else call them 'hostiles'
        ch["side"] = ch.get("side", "hostiles")
        characters.append(ch)

    max_rounds = 15

    for rnd in range(1, max_rounds + 1):
        print(f"\n===== ROUND {rnd} =====")

        # rebuild initiative fresh every round
        order = rebuild_initiative(characters)

        # check living sides
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

        # drop the dead before next round
        characters = [c for c in characters if c.get("pools", {}).get("HP", 0) > 0]

    print("Wasted March test complete.")


if __name__ == "__main__":
    run_wasted_march_test()
