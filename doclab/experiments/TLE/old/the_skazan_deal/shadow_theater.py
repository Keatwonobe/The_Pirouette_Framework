import json
import os
import random

INIT_DIR = "./initiative"
SCENE_DIR = "./scenes"
STAGE_DIR = "./stages"

# ------------------ LOADERS ------------------
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
            if ids is None or data["id"] in ids:
                chars.append(data)
    return chars

# ------------------ RENDERING ------------------
def render_battlefield(characters, stage=None):
    print("\n=== SHADOW STAGE ===")
    if stage:
      print(f"Stage: {stage.get('name','?')} – {stage.get('desc','')}")
    for ch in characters:
        hp = ch.get("pools", {}).get("HP", "?")
        pos = ch.get("position", {})
        print(f"- {ch['id']:20s} [{ch['side']}] HP={hp:>3} at ({pos['x']},{pos['y']})")
    print("=====================\n")

# ------------------ UTILS ------------------
def distance(a, b):
    return abs(a["position"]["x"] - b["position"]["x"]) + abs(a["position"]["y"] - b["position"]["y"])

def move_unit(ch, x, y):
    ch["position"]["x"] = x
    ch["position"]["y"] = y

def get_initiative_score(ch):
    stats = ch.get("stats", {})
    return stats.get("TEP", 10) + stats.get("init_bonus", 0) + random.randint(0,5)

def find_targets(ch, characters):
    return [o for o in characters if o["side"] != ch["side"] and o.get("pools", {}).get("HP", 0) > 0]

# ------------------ NARRATION ------------------
def announce_attack(attacker, defender, ctx=None):
    # you can later branch on ctx ("opportunity", "ranged", etc.)
    print(f"» {attacker['name']} declares an attack on {defender['name']}!")

def offer_reaction(defender, attacker):
    """
    Only for players (or maybe 'reactive' NPCs later).
    Lets defender try to block/dodge/speak.
    For now it’s narrative first, mechanical second.
    """
    print(f"{defender['name']} may react. (block | dodge | speak | pass)")
    while True:
        resp = input("(react)> ").strip().lower()
        if resp == "block":
            # simple: halve damage later
            return {"type": "block"}
        elif resp == "dodge":
            # simple: 50% chance to negate
            return {"type": "dodge"}
        elif resp == "speak":
            line = input("Say your piece: ")
            print(f"{defender['name']} says: {line}")
            # still counts as a reaction, no defense
            return {"type": "speak"}
        elif resp == "pass":
            return {"type": "pass"}
        else:
            print("Options: block | dodge | speak | pass")

def resolve_damage(attacker, defender, reaction=None):
    base_dmg = 4  # placeholder
    final_dmg = base_dmg

    if reaction:
        if reaction["type"] == "block":
            final_dmg = max(1, base_dmg // 2)
            print(f"{defender['name']} blocks! Damage reduced to {final_dmg}.")
        elif reaction["type"] == "dodge":
            # simple 50% dodge
            if random.random() < 0.5:
                print(f"{defender['name']} dodges completely!")
                final_dmg = 0

    if final_dmg > 0:
        defender["pools"]["HP"] = max(0, defender["pools"]["HP"] - final_dmg)
        print(f"{attacker['name']} hits {defender['name']} for {final_dmg} damage. (HP={defender['pools']['HP']})")
    else:
        print(f"{attacker['name']}'s strike fails to land.")

def attack_unit(attacker, defender):
    # 1) announce
    announce_attack(attacker, defender)
    # 2) if defender is player, offer reaction
    reaction = None
    if defender.get("player", False):
        reaction = offer_reaction(defender, attacker)
    # 3) apply damage
    resolve_damage(attacker, defender, reaction)
    # 4) add any on-hit effects later

# ------------------ PLAYER TURN (CONTINUOUS) ------------------
def handle_player_turn(player, characters, stage=None):
    """
    Player stays in here until they say 'pass'.
    This gives GM space to stage-talk and the player to do multiple micro-actions.
    """
    print(f"\n--- {player['name']}'s turn ---")
    render_battlefield(characters, stage)
    print("Commands: look | pass | m x y | a target_id | ma x y target_id | say ...")

    while True:
        cmd = input("> ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        op = parts[0].lower()

        if op == "pass":
            print(f"{player['name']} ends their turn.")
            break

        elif op == "look":
            render_battlefield(characters, stage)
            continue

        elif op == "say":
            # everything after 'say' is dialogue
            line = cmd[len("say"):].strip()
            print(f"{player['name']} says: {line}")
            continue

        elif op == "m" and len(parts) == 3:
            x, y = int(parts[1]), int(parts[2])
            move_unit(player, x, y)
            print(f"{player['name']} moves to ({x},{y}).")
            continue

        elif op == "a" and len(parts) == 2:
            target_id = parts[1]
            target = next((c for c in characters if c["id"] == target_id and c.get("pools", {}).get("HP", 0) > 0), None)
            if not target:
                print("No such target or target is down.")
                continue
            # simple melee range
            if distance(player, target) > 1:
                print("Target out of melee range.")
                continue
            attack_unit(player, target)
            continue

        elif op == "ma" and len(parts) == 4:
            x, y = int(parts[1]), int(parts[2])
            target_id = parts[3]
            target = next((c for c in characters if c["id"] == target_id and c.get("pools", {}).get("HP", 0) > 0), None)
            move_unit(player, x, y)
            print(f"{player['name']} moves to ({x},{y}).")
            if target and distance(player, target) <= 1:
                attack_unit(player, target)
            else:
                print("Moved, but target not in range.")
            continue

        else:
            print("Unrecognized command. Try: look | pass | m x y | a id | ma x y id | say ...")

# ------------------ AI TURN ------------------
def handle_ai_turn(ch, characters):
    targets = find_targets(ch, characters)
    if not targets:
        print(f"{ch['name']} has no targets.")
        return
    tgt = min(targets, key=lambda t: distance(ch, t))
    d = distance(ch, tgt)
    if d <= 1:
        attack_unit(ch, tgt)
    else:
        cx, cy = ch["position"]["x"], ch["position"]["y"]
        tx, ty = tgt["position"]["x"], tgt["position"]["y"]
        if tx > cx: cx += 1
        elif tx < cx: cx -= 1
        elif ty > cy: cy += 1
        elif ty < cy: cy -= 1
        move_unit(ch, cx, cy)
        print(f"{ch['name']} advances toward {tgt['name']} ({cx},{cy}).")

# ------------------ MAIN SCENE RUNNER ------------------
def run_scene(scene_file):
    scene = load_scene(scene_file)
    stage = load_stage(scene["stage"])
    characters = load_characters(scene["actors"])
    order = sorted(characters, key=lambda c: get_initiative_score(c), reverse=True)
    max_rounds = scene.get("max_rounds", 10)

    for round_no in range(1, max_rounds + 1):
        print(f"\n===== ROUND {round_no} =====")
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

        # clean dead
        characters = [c for c in characters if c.get("pools", {}).get("HP", 0) > 0]

    print("Shadow play complete.")

if __name__ == "__main__":
    run_scene("scene_meadow_raid.json")
