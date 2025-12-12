#!/usr/bin/env python3
"""
combat_runner_v5.py

Extends combat_runner_v4 to:
- load axes/, influences/, items/, spells/ as JSON libraries
- let characters use inventory items with per-character overrides
- let characters cast spells that call influences
- route all damage/effects through wound_channels
- still support the simple CLI actions

Folders expected (missing ok):
  ./axes
  ./influences
  ./items
  ./spells
  ./initiative
"""

import os, json, random, datetime, re
from copy import deepcopy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INIT_DIR = os.path.join(BASE_DIR, "initiative")
AXES_DIR = os.path.join(BASE_DIR, "axes")
INFL_DIR = os.path.join(BASE_DIR, "influences")
ITEMS_DIR = os.path.join(BASE_DIR, "items")
SPELLS_DIR = os.path.join(BASE_DIR, "spells")

# =========================================================
# UTIL
# =========================================================

DICE_RE = re.compile(r"^(\d+)d(\d+)$")

def roll_amt(s: str):
    """
    '1d6' -> int, '2d4' -> int, '5' -> int
    """
    if isinstance(s, (int, float)):
        return int(s)
    s = str(s)
    m = DICE_RE.match(s)
    if not m:
        return int(float(s))
    n, d = int(m.group(1)), int(m.group(2))
    return sum(random.randint(1, d) for _ in range(n))

import json
import os

def load_dir_as_map(path):
    """
    Load all .json files in a directory into a dict, skipping malformed ones.
    Will tell you which file failed so you can fix it.
    """
    out = {}
    if not os.path.isdir(path):
        return out
    for fn in os.listdir(path):
        if not fn.endswith(".json"):
            continue
        full = os.path.join(path, fn)
        try:
            with open(full, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARN] could not load JSON '{full}': {e}")
            continue

        key = (
            data.get("influence_id")
            or data.get("axis_id")
            or data.get("item_id")
            or data.get("spell_id")
            or fn
        )
        out[key] = data
    return out


def deep_merge(base: dict, override: dict):
    """simple deep merge for item/spell overrides"""
    if not isinstance(override, dict):
        return override
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            base[k] = deep_merge(base[k], v)
        else:
            base[k] = v
    return base

# =========================================================
# LOADING CHARACTERS
# =========================================================

def default_wound_channels():
    return {
        "cut": 0,
        "pierce": 0,
        "blunt": 0,
        "thermal": 0,
        "cold": 0,
        "lightning": 0,
        "acid": 0,
        "entropy": 0,
        "psychic": 0,
        "oneiric": 0,
        "void": 0,
        "status": []
    }

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
        data["_filename"] = fn
        data.setdefault("pools", {})
        data["pools"].setdefault("HP", 10)
        data["pools"].setdefault("ENT", 0)
        data["pools"].setdefault("AEP", 0)
        data.setdefault("position", {"x": 0, "y": 0})
        data.setdefault("wound_channels", default_wound_channels())
        data.setdefault("inventory", [])
        data.setdefault("spellbook", [])
        characters.append(data)
    return characters

def save_back_vessels(characters):
    for ch in characters:
        fn = ch.get("_filename")
        if not fn:
            continue
        out_path = os.path.join(INIT_DIR, fn)
        tmp = dict(ch)
        tmp.pop("_filename", None)
        with open(out_path, "w") as f:
            json.dump(tmp, f, indent=2)

# =========================================================
# GEOMETRY
# =========================================================

def distance(a, b):
    return abs(a["position"]["x"] - b["position"]["x"]) + abs(a["position"]["y"] - b["position"]["y"])

def move_unit(ch, x, y):
    ch["position"]["x"] = x
    ch["position"]["y"] = y

# =========================================================
# INFLUENCE ENGINE
# =========================================================

def apply_influence(inf: dict, source: dict, target: dict, ctx: dict):
    """
    inf: influence JSON
    source/target: characters
    ctx: { "ep_spent": int, "axis": {...}, "log": [] }
    """
    ep_spent = ctx.get("ep_spent", 0)
    # writes to wound channels
    for w in inf.get("writes", []):
        chan = w["channel"]
        amt = w["amount"]
        base = roll_amt(amt)
        # scaling
        scaling = w.get("scaling")
        if scaling and ep_spent:
            per_ep = scaling.get("per_ep")
            if per_ep:
                base += int(ep_spent * float(per_ep))
            max_ep = scaling.get("max_ep")
            if max_ep and ep_spent > max_ep:
                # we just cap the scaling part
                pass
        target["wound_channels"][chan] = target["wound_channels"].get(chan, 0) + base
        ctx["log"].append(f"{source['name']} → {target['name']} {chan}+={base}")

    # statuses
    for st in inf.get("status_apply", []):
        status = deepcopy(st)
        target["wound_channels"]["status"].append(status)
        ctx["log"].append(f"{target['name']} gains status {status['status']}")

    # blocks / buffs etc. (minimal)
    if "block" in inf and inf["target"] == "self":
        blk = inf["block"]["amount"]
        source.setdefault("temp_block", 0)
        source["temp_block"] += blk
        ctx["log"].append(f"{source['name']} blocks {blk}")

    # dynamic: axis house
    dyn = inf.get("dynamic")
    if dyn and dyn.get("source") == "axis":
        axis = ctx.get("axis")
        if axis:
            # get house default contact
            house = axis.get("positive_house") or {}
            for sub_inf_id in house.get("contact_influences", []):
                ctx["log"].append(f"dynamic axis call → {sub_inf_id}")
                yield sub_inf_id  # tell caller to apply this too

    # dynamic: entropy → channel
    if dyn and dyn.get("source") == "spent_entropy":
        ratio = dyn.get("ratio", 1)
        chan = dyn.get("map_to", "entropy")
        amt = ep_spent * ratio
        target["wound_channels"][chan] = target["wound_channels"].get(chan, 0) + amt
        ctx["log"].append(f"{source['name']} converts {ep_spent} EP → {amt} {chan}")

    return

# =========================================================
# ITEM / SPELL RESOLVERS
# =========================================================

def resolve_item_for_character(ch, item_id, items_lib):
    base = items_lib.get(item_id)
    if not base:
        return None
    merged = deepcopy(base)
    # find an inventory entry with this item_id
    for inv in ch.get("inventory", []):
        if inv.get("item_id") == item_id:
            overrides = inv.get("overrides")
            if overrides:
                merged = deep_merge(merged, overrides)
            break
    return merged

def resolve_spell_for_character(ch, spell_id, spells_lib):
    base = spells_lib.get(spell_id)
    if not base:
        return None
    # (could also do per-character overrides like with inventory)
    return deepcopy(base)

# =========================================================
# ACTIONS
# =========================================================

def spend_entropy(ch, requested):
    have = ch["pools"].get("ENT", 0)
    spend = max(0, min(have, requested))
    ch["pools"]["ENT"] = have - spend
    return spend

def execute_item_attack(attacker, defender, item, influences_lib, axes_lib, ep_spent, log):
    # items list influences directly
    inf_ids = item.get("influences", [])
    ctx = {"ep_spent": ep_spent, "axis": None, "log": log}
    # if item hints at an axis, you can load it
    axis_hint = item.get("weapon_axis_hint")
    if axis_hint:
        # first axis only for now
        ax = axes_lib.get(axis_hint[0]) if isinstance(axis_hint, list) else axes_lib.get(axis_hint)
        if ax:
            ctx["axis"] = ax

    to_apply = list(inf_ids)
    while to_apply:
        inf_id = to_apply.pop(0)
        inf = influences_lib.get(inf_id)
        if not inf:
            log.append(f"missing influence {inf_id}")
            continue
        extra = list(apply_influence(inf, attacker, defender, ctx)) or []
        to_apply.extend(extra)

def execute_spell_cast(caster, defender, spell, influences_lib, axes_lib, ep_spent, log):
    ctx = {"ep_spent": ep_spent, "axis": None, "log": log}
    # bind axis if required
    req_axes = spell.get("axis_required", [])
    if req_axes:
        ax = axes_lib.get(req_axes[0])
        if ax:
            ctx["axis"] = ax
    to_apply = list(spell.get("influences", []))
    while to_apply:
        inf_id = to_apply.pop(0)
        inf = influences_lib.get(inf_id)
        if not inf:
            log.append(f"missing influence {inf_id}")
            continue
        extra = list(apply_influence(inf, caster, defender, ctx)) or []
        to_apply.extend(extra)

def finalize_damage_from_wounds(target, log):
    """
    for now: sum cut + pierce + blunt + thermal + cold + lightning + acid + entropy as HP loss
    shields / temp_block would be applied here
    """
    wc = target["wound_channels"]
    raw = (
        wc.get("cut", 0) +
        wc.get("pierce", 0) +
        wc.get("blunt", 0) +
        wc.get("thermal", 0) +
        wc.get("cold", 0) +
        wc.get("lightning", 0) +
        wc.get("acid", 0)
    )
    # entropy / psychic / oneiric could do other things later
    block = target.pop("temp_block", 0)
    dmg = max(0, raw - block)
    target["pools"]["HP"] = max(0, target["pools"]["HP"] - dmg)
    log.append(f"{target['name']} takes {dmg} HP (after block {block}), HP={target['pools']['HP']}")
    # reset channels for next turn
    target["wound_channels"] = default_wound_channels()

# =========================================================
# AI
# =========================================================

def nearest_enemy(ch, characters):
    enemies = [c for c in characters if c["side"] != ch["side"] and c["pools"]["HP"] > 0]
    if not enemies:
        return None
    return min(enemies, key=lambda t: distance(ch, t))

def ai_take_turn(ch, chars, libs):
    target = nearest_enemy(ch, chars)
    if not target:
        print(f"{ch['name']} has no targets.")
        return
    # basic AI: use first equipped item or fall back
    inv = ch.get("inventory", [])
    item = None
    for it in inv:
        if it.get("equipped"):
            item = resolve_item_for_character(ch, it["item_id"], libs["items"])
            break
    if not item:
        # fallback: fake slash
        log = []
        fake = {"influences": ["inf_slash"], "weapon_axis_hint": ["e_2"]}
        ep_spent = spend_entropy(ch, 0)
        execute_item_attack(ch, target, fake, libs["influences"], libs["axes"], ep_spent, log)
        finalize_damage_from_wounds(target, log)
        for line in log: print("  " + line)
        return

    ep_spent = spend_entropy(ch, 0)
    log = []
    execute_item_attack(ch, target, item, libs["influences"], libs["axes"], ep_spent, log)
    finalize_damage_from_wounds(target, log)
    for line in log: print("  " + line)

# =========================================================
# PLAYER
# =========================================================

def print_state(characters):
    print("\n=== STATE ===")
    for i, ch in enumerate(characters, start=1):
        pos = ch["position"]
        print(f"[{i}] {ch.get('name','?'):18s} | {ch['side']:8s} | HP={ch['pools']['HP']:3d} ENT={ch['pools']['ENT']:2d} @({pos['x']},{pos['y']})")
    print("Commands:")
    print("  pass")
    print("  m X Y               move")
    print("  a TARGET [ep=N] [item=item_id]")
    print("  cast TARGET spell_id [ep=N]")
    print("  look")
    print("==============\n")

def handle_player_turn(player, characters, libs):
    while True:
        print_state(characters)
        cmd = input(f"{player['name']}> ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        op = parts[0].lower()

        if op == "pass":
            break

        if op == "look":
            continue

        if op == "m" and len(parts) == 3:
            x, y = int(parts[1]), int(parts[2])
            move_unit(player, x, y)
            print(f"{player['name']} moves to ({x},{y}).")
            continue

        if op == "a":
            if len(parts) < 2:
                print("usage: a TARGET [ep=N] [item=item_id]")
                continue
            try:
                tgt_idx = int(parts[1]) - 1
                target = characters[tgt_idx]
            except (ValueError, IndexError):
                print("bad target")
                continue

            # parse extras
            ep_req = 0
            item_id = None
            for p in parts[2:]:
                if p.startswith("ep=") or p.startswith("e="):
                    ep_req = int(p.split("=", 1)[1])
                elif p.startswith("item="):
                    item_id = p.split("=", 1)[1]

            # resolve item
            if item_id:
                item = resolve_item_for_character(player, item_id, libs["items"])
            else:
                # pick equipped or first
                item = None
                for it in player.get("inventory", []):
                    if it.get("equipped"):
                        item = resolve_item_for_character(player, it["item_id"], libs["items"])
                        break

            if not item:
                print("no usable item")
                continue

            ep_spent = spend_entropy(player, ep_req)
            log = []
            execute_item_attack(player, target, item, libs["influences"], libs["axes"], ep_spent, log)
            finalize_damage_from_wounds(target, log)
            for line in log: print("  " + line)
            break

        if op == "cast":
            if len(parts) < 3:
                print("usage: cast TARGET spell_id [ep=N]")
                continue
            try:
                tgt_idx = int(parts[1]) - 1
                target = characters[tgt_idx]
            except (ValueError, IndexError):
                print("bad target")
                continue
            spell_id = parts[2]
            ep_req = 0
            for p in parts[3:]:
                if "=" in p:
                    ep_req = int(p.split("=", 1)[1])
            spell = resolve_spell_for_character(player, spell_id, libs["spells"])
            if not spell:
                print("no such spell")
                continue
            ep_spent = spend_entropy(player, ep_req)
            log = []
            execute_spell_cast(player, target, spell, libs["influences"], libs["axes"], ep_spent, log)
            finalize_damage_from_wounds(target, log)
            for line in log: print("  " + line)
            break

        print("unknown command")

def start_of_round_reactions(characters, libs):
    """
    Give players a chance to defend even if they lose init.
    - If they have an equipped item with auto_react, use its influence(s)
    - else give them a flat temp_block
    """
    influences_lib = libs["influences"]
    axes_lib = libs["axes"]
    items_lib = libs["items"]

    for ch in characters:
        if ch.get("side") != "players":
            continue
        if ch["pools"].get("HP", 0) <= 0:
            continue

        # try to find an equipped item with auto_react
        equipped = None
        for it in ch.get("inventory", []):
            if it.get("equipped"):
                equipped = resolve_item_for_character(ch, it["item_id"], items_lib)
                break

        log = []
        reacted = False

        if equipped and equipped.get("auto_react"):
            # run its listed influences as if self-target
            ctx = {"ep_spent": 0, "axis": None, "log": log}
            to_apply = list(equipped.get("influences", []))
            while to_apply:
                inf_id = to_apply.pop(0)
                inf = influences_lib.get(inf_id)
                if not inf:
                    continue
                # self-target
                extra = list(apply_influence(inf, ch, ch, ctx)) or []
                to_apply.extend(extra)
            reacted = True

        if not reacted:
            # just give them some block for the opening salvo
            ch.setdefault("temp_block", 0)
            ch["temp_block"] += 4  # tweakable
            log.append(f"{ch['name']} braces for impact (+4 block)")

        for line in log:
            print("  " + line)


# =========================================================
# INIT ORDER + MAIN
# =========================================================

def rebuild_initiative(characters):
    return sorted(
        characters,
        key=lambda c: c.get("stats", {}).get("TEP", 10) + c.get("stats", {}).get("init_bonus", 0) + random.randint(0,5),
        reverse=True
    )

def main():
    # load libraries
    axes_lib = load_dir_as_map(AXES_DIR)
    infl_lib = load_dir_as_map(INFL_DIR)
    items_lib = load_dir_as_map(ITEMS_DIR)
    spells_lib = load_dir_as_map(SPELLS_DIR)

    libs = {
        "axes": axes_lib,
        "influences": infl_lib,
        "items": items_lib,
        "spells": spells_lib
    }

    chars = load_initiative()
    if not chars:
        print("no characters in ./initiative")
        return

    # sides
    for ch in chars:
        if ch.get("player", False) or str(ch.get("id", "")).startswith("player-"):
            ch["side"] = "players"
            ch["player"] = True
        else:
            ch.setdefault("side", "raiders")

    max_rounds = 15
    for rnd in range(1, max_rounds + 1):
        print(f"\n===== ROUND {rnd} =====")
        order = rebuild_initiative(chars)
        start_of_round_reactions(chars, libs)

        # victory check
        alive_sides = {c["side"] for c in chars if c["pools"]["HP"] > 0}
        if len(alive_sides) <= 1:
            print("Combat ends.")
            break

        for ch in order:
            if ch["pools"]["HP"] <= 0:
                continue
            if ch.get("player", False):
                handle_player_turn(ch, chars, libs)
            else:
                ai_take_turn(ch, chars, libs)

        # prune the dead
        chars = [c for c in chars if c["pools"]["HP"] > 0]

    # writeback
    now = datetime.datetime.utcnow().isoformat()
    for ch in chars:
        vessel = ch.setdefault("vessel", {})
        history = vessel.setdefault("history", [])
        history.append({
            "stamp": now,
            "note": "participated in combat_runner_v5 session"
        })
    save_back_vessels(chars)
    print("Done, vessels updated.")

if __name__ == "__main__":
    main()
