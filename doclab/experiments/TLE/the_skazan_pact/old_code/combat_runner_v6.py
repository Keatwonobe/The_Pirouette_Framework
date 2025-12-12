#!/usr/bin/env python3
"""
combat_runner_v6.py

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

def parse_index_tokens(tokens, max_len):
    """
    Given a list of tokens like ['3', '5-8'], return a set of 0-based indices
    within [0, max_len). Invalid entries are ignored.
    """
    indices = set()
    for tok in tokens:
        if "-" in tok:
            start_str, end_str = tok.split("-", 1)
            try:
                start = int(start_str) - 1
                end = int(end_str) - 1
            except ValueError:
                continue
            if start > end:
                start, end = end, start
            for i in range(start, end + 1):
                if 0 <= i < max_len:
                    indices.add(i)
        else:
            try:
                idx = int(tok) - 1
            except ValueError:
                continue
            if 0 <= idx < max_len:
                indices.add(idx)
    return sorted(indices)

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
# STANCE / CONVERSATION HELPERS
# =========================================================

def ability_bonus(ch, stat_name: str):
    """
    Simple D&D-style modifier from a numeric stat.
    If the stat is missing, returns 0.
    """
    stat_name = stat_name.lower()
    stats = ch.get("stats", {})
    val = stats.get(stat_name)
    if val is None:
        return 0
    try:
        v = int(val)
    except Exception:
        v = 10
    return (v - 10) // 2


def init_social_flags(chars):
    """
    Initialize stance/hostility/AI flags and a conversation pocket
    for every character loaded.
    - stance: 'combat' or 'conversation'
    - hostility: 'hostile' / 'neutral' / 'friendly'
    - ai_enabled: bool
    """
    for ch in chars:
        is_player = bool(ch.get("player", False) or str(ch.get("id", "")).startswith("player-"))
        # stance: what kind of action they normally take
        ch.setdefault("stance", "combat")
        # players default to friendly, NPCs to hostile
        ch.setdefault("hostility", "friendly" if is_player else "hostile")
        # players use manual control, NPCs use AI unless GM toggles
        ch.setdefault("ai_enabled", not is_player)
        # pocket for last conversation roll
        ch.setdefault("conversation", {
            "last_roll": None,
            "last_dc": None,
            "last_stat": None,
            "last_target": None,
            "outcome": None
        })


def conversation_check(speaker, listener, stat: str = "will", mode: str = "auto"):
    """
    Resolve a single 'conversation roll' between two characters.

    stat: which stat to use (e.g. 'will', 'int', 'str')
    mode: 'auto' (script rolls) or 'manual' (GM rolls at table, enters total)
    """
    stat = stat.lower()
    atk_bonus = ability_bonus(speaker, stat)
    def_bonus = ability_bonus(listener, stat)

    dc = 10 + def_bonus
    print(f"[CONV] {speaker['name']} engages {listener['name']} "
          f"using {stat.upper()} vs DC {dc}.")

    if mode == "manual":
        print(f"[CONV] Roll 1d20 + {stat.upper()} modifier ({atk_bonus}) vs DC {dc}.")
        print("       Enter the TOTAL you rolled (or 'q' to cancel).")
        while True:
            raw = input("  total> ").strip()
            if raw.lower().startswith("q"):
                print("[CONV] Conversation cancelled.")
                return
            try:
                total = int(raw)
                break
            except ValueError:
                print("  Please enter an integer or 'q'.")
    else:
        die = random.randint(1, 20)
        total = die + atk_bonus
        print(f"[CONV] AUTO roll: 1d20 = {die} + {atk_bonus} => {total}")

    success = total >= dc
    outcome = "success" if success else "failure"
    print(f"[CONV] Result: {outcome.upper()}")

    # store summary on speaker
    conv = speaker.setdefault("conversation", {})
    conv.update({
        "last_roll": total,
        "last_dc": dc,
        "last_stat": stat,
        "last_target": listener.get("name"),
        "outcome": outcome
    })

    # simple hostility shifts
    if success:
        if listener.get("hostility") == "hostile":
            listener["hostility"] = "neutral"
            print(f"[CONV] {listener['name']} shifts from HOSTILE → NEUTRAL.")
        elif listener.get("hostility") == "neutral":
            listener["hostility"] = "friendly"
            print(f"[CONV] {listener['name']} shifts from NEUTRAL → FRIENDLY.")
    else:
        if listener.get("hostility") == "neutral":
            listener["hostility"] = "hostile"
            print(f"[CONV] {listener['name']} is offended and becomes HOSTILE.")

    # conversation itself consumes the turn; caller doesn't need return


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

def hydrate_character_from_dict(data, filename=None):
    """
    Apply default fields to a freshly loaded character dict.
    """
    if filename is not None:
        data["_filename"] = filename
    data.setdefault("pools", {})
    data["pools"].setdefault("HP", 10)
    data["pools"].setdefault("ENT", 0)
    data["pools"].setdefault("AEP", 0)
    data.setdefault("position", {"x": 0, "y": 0})
    data.setdefault("wound_channels", default_wound_channels())
    data.setdefault("inventory", [])
    data.setdefault("spellbook", [])

    # default behavioral flags
    # mode: "combat" or "talk" or "neutral"
    data.setdefault("mode", "combat")
    # ai_enabled: non-players default to True, players default to False
    if "ai_enabled" not in data:
        is_player = data.get("player", False) or str(data.get("id", "")).startswith("player-")
        data["ai_enabled"] = not is_player
    # hostilities can be extended later if needed
    data.setdefault("hostile", True)

    return data

def load_new_characters(existing_chars):
    """
    Scan INIT_DIR for .json files that are not yet loaded into existing_chars.
    Return a list of *new* hydrated character dicts.
    """
    existing_files = {c.get("_filename") for c in existing_chars if c.get("_filename")}
    new_chars = []
    if not os.path.isdir(INIT_DIR):
        return new_chars

    for fn in os.listdir(INIT_DIR):
        if not fn.endswith(".json"):
            continue
        if fn in existing_files:
            continue
        path = os.path.join(INIT_DIR, fn)
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARN] Could not load new initiative file '{fn}': {e}")
            continue
        hydrate_character_from_dict(data, filename=fn)
        new_chars.append(data)

    return new_chars

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
        hydrate_character_from_dict(data, filename=fn)
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
    enemies = [
        c for c in characters
        if c["side"] != ch["side"]
        and c["pools"]["HP"] > 0
        and c.get("mode", "combat") == "combat"
    ]
    if not enemies:
        return None
    return min(enemies, key=lambda t: distance(ch, t))


def ai_conversation_turn(ch, chars):
    """
    Very simple AI for 'conversation stance' NPCs:
    they pick a random opposite-side character and
    attempt a conversation check using WILL in auto mode.
    """
    targets = [
        c for c in chars
        if c["side"] != ch["side"] and c["pools"].get("HP", 0) > 0
    ]
    if not targets:
        print(f"{ch['name']} looks around but has nobody to talk to.")
        return
    target = random.choice(targets)
    print(f"\n[AI-CONV] {ch['name']} engages {target['name']} in conversation.")
    conversation_check(ch, target, stat="will", mode="auto")

def ai_take_turn(ch, chars, libs):
    # AI toggle
    if not ch.get("ai_enabled", True):
        print(f"{ch['name']} (AI disabled this round).")
        return

    # Conversation stance → do not attack, talk instead
    if ch.get("stance", "combat") == "conversation":
        ai_conversation_turn(ch, chars)
        return

    # No targets? do nothing
    target = nearest_enemy(ch, chars)
    if not target:
        print(f"{ch['name']} has no valid targets.")
        return

    # basic AI: use first equipped item or fall back
    inv = ch.get("inventory", [])
    item = None
    for it in inv:
        if it.get("equipped"):
            item = resolve_item_for_character(ch, it["item_id"], libs["items"])
            break

    log = []

    if not item:
        # fallback: fake slash
        fake = {"influences": ["inf_slash"], "weapon_axis_hint": ["e_2"]}
        ep_spent = spend_entropy(ch, 0)
        execute_item_attack(ch, target, fake, libs["influences"], libs["axes"], ep_spent, log)
        finalize_damage_from_wounds(target, log)
        for line in log:
            print("  " + line)
        return

    ep_spent = spend_entropy(ch, 0)
    execute_item_attack(ch, target, item, libs["influences"], libs["axes"], ep_spent, log)
    finalize_damage_from_wounds(target, log)
    for line in log:
        print("  " + line)


# =========================================================
# PLAYER
# =========================================================

def print_state(characters):
    print("\n=== STATE ===")
    for i, ch in enumerate(characters, start=1):
        pos = ch["position"]
        mode = ch.get("mode", "combat")
        ai_flag = "AI" if ch.get("ai_enabled", False) else "NO-AI"
        hp = ch["pools"]["HP"]
        ent = ch["pools"]["ENT"]
        print(f"[{i}] {ch.get('name','?'):18s} | {ch['side']:8s} | {mode:7s} | {ai_flag:5s} | HP={hp:3d} ENT={ent:2d} @({pos['x']},{pos['y']})")
    print("Commands:")
    print("  pass")
    print("  m X Y                 move")
    print("  a TARGET [ep=N] [item=item_id]")
    print("  cast TARGET spell_id [ep=N]")
    print("  talk TARGET [auto]    social check vs TARGET")
    print("  spells [IDX]          show spellbook (self or by index)")
    print("  show IDX FIELD        show raw field from character JSON")
    print("  ai on|off IDX[..]     toggle AI on/off (range ok)")
    print("  mode IDX[..] TYPE     TYPE = combat|talk|neutral")
    print("  look")
    print("==============\n")

def print_spellbook_for(ch, spells_lib):
    sb = ch.get("spellbook", [])
    if not sb:
        print(f"{ch.get('name','?')} has no spells.")
        return
    print(f"Spellbook for {ch.get('name','?')}:")
    for entry in sb:
        if isinstance(entry, str):
            sid = entry
        elif isinstance(entry, dict):
            sid = entry.get("spell_id") or entry.get("id") or "?"
        else:
            continue
        spell = spells_lib.get(sid, {})
        sname = spell.get("name", sid)
        summary = spell.get("summary", spell.get("tagline", ""))
        if summary:
            print(f"  - {sid}: {sname} :: {summary}")
        else:
            print(f"  - {sid}: {sname}")


def show_field_for(ch, field):
    val = ch.get(field)
    if val is None:
        print(f"{ch.get('name','?')} has no field '{field}'.")
    else:
        print(f"{ch.get('name','?')}.{field} =")
        print(json.dumps(val, indent=2))


def conversation_check(player, target, auto=False):
    """
    Simple social opposed roll: d20 + CHA (or 0 if missing).
    If auto=False, ask for totals so you can roll at the table.
    """
    p_stats = player.get("stats", {})
    t_stats = target.get("stats", {})
    p_cha = int(p_stats.get("CHA", 0))
    t_cha = int(t_stats.get("CHA", 0))

    if auto:
        p_roll = random.randint(1, 20)
        t_roll = random.randint(1, 20)
        p_total = p_roll + p_cha
        t_total = t_roll + t_cha
        print(f"{player['name']} rolls {p_roll} + CHA({p_cha}) = {p_total}")
        print(f"{target['name']} rolls {t_roll} + CHA({t_cha}) = {t_total}")
    else:
        print("Roll d20 + any social modifiers at the table.")
        p_total = int(input(f"Total for {player['name']}? "))
        t_total = int(input(f"Total for {target['name']}? "))

    if p_total > t_total:
        print(f"[SOCIAL] {player['name']} succeeds vs {target['name']} ({p_total} > {t_total}).")
        return "success"
    elif p_total < t_total:
        print(f"[SOCIAL] {player['name']} fails vs {target['name']} ({p_total} < {t_total}).")
        return "failure"
    else:
        print(f"[SOCIAL] {player['name']} and {target['name']} tie ({p_total} = {t_total}).")
        return "tie"

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

        # basic attack
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

        # spell casting
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

        # conversation check
        if op == "talk":
            if len(parts) < 2:
                print("usage: talk TARGET [auto]")
                continue
            try:
                tgt_idx = int(parts[1]) - 1
                target = characters[tgt_idx]
            except (ValueError, IndexError):
                print("bad target")
                continue
            auto = any(p.lower() == "auto" for p in parts[2:])
            result = conversation_check(player, target, auto=auto)
            # put the player into "talk" mode if desired
            player["mode"] = "talk"
            # you can hang tags on target based on result later
            continue

        # show spellbook
        if op == "spells":
            if len(parts) == 1:
                print_spellbook_for(player, libs["spells"])
            else:
                try:
                    idx = int(parts[1]) - 1
                    if 0 <= idx < len(characters):
                        print_spellbook_for(characters[idx], libs["spells"])
                    else:
                        print("bad index")
                except ValueError:
                    print("usage: spells [IDX]")
            continue

        # generic field introspection
        if op == "show":
            if len(parts) < 3:
                print("usage: show IDX FIELD")
                continue
            try:
                idx = int(parts[1]) - 1
                ch = characters[idx]
            except (ValueError, IndexError):
                print("bad index")
                continue
            field = parts[2]
            show_field_for(ch, field)
            continue

        # AI toggles: ai on|off idx or ranges
        if op == "ai":
            if len(parts) < 3:
                print("usage: ai on|off IDX [IDX or A-B...]")
                continue
            mode = parts[1].lower()
            if mode not in ("on", "off"):
                print("usage: ai on|off IDX [IDX or A-B...]")
                continue
            indices = parse_index_tokens(parts[2:], len(characters))
            if not indices:
                print("no valid indices")
                continue
            val = (mode == "on")
            for i in indices:
                ch = characters[i]
                ch["ai_enabled"] = val
                print(f"AI {'ON' if val else 'OFF'} for [{i+1}] {ch.get('name','?')}")
            continue

        # mode toggles: mode 3-5 talk / mode 2 combat
        if op == "mode":
            if len(parts) < 3:
                print("usage: mode IDX[..] TYPE  (TYPE = combat|talk|neutral)")
                continue
            # last token is mode, everything before are indices
            mode_str = parts[-1].lower()
            if mode_str in ("talk", "conv", "conversation"):
                new_mode = "talk"
            elif mode_str in ("combat", "fight"):
                new_mode = "combat"
            elif mode_str in ("neutral", "idle"):
                new_mode = "neutral"
            else:
                print("unknown mode type; use combat/talk/neutral")
                continue
            idx_tokens = parts[1:-1]
            indices = parse_index_tokens(idx_tokens, len(characters))
            if not indices:
                print("no valid indices")
                continue
            for i in indices:
                ch = characters[i]
                ch["mode"] = new_mode
                print(f"Mode for [{i+1}] {ch.get('name','?')} → {new_mode}")
            continue

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

def preflight_setup(chars):
    """
    Pre-combat staging step so GM can inspect the battlefield and
    toggle AI / mode / hostility before any rounds or victory checks run.
    Returns True to start combat, False to exit immediately.
    """
    while True:
        print("\n=== PRE-FLIGHT SETUP ===")
        print("Type 'start' to begin rounds, or 'quit' to exit without running combat.")
        print("You can use:")
        print("  ai on|off IDX[..]         toggle AI")
        print("  mode IDX[..] TYPE         TYPE = combat|talk|neutral")
        print("  hostility IDX[..] STATE   STATE = hostile|neutral|friendly")
        print("  side IDX[..] LABEL    change SIDE/team label")
        print("  look                      reprint state\n")

        print_state(chars)  # reuse existing state printer

        cmd = input("setup> ").strip()
        if not cmd:
            continue

        parts = cmd.split()
        op = parts[0].lower()

        # start / quit
        if op in ("start", "go", "run", "begin"):
            return True
        if op in ("q", "quit", "exit"):
            print("[setup] Exiting before combat; initiative left as-is.")
            return False

        if op == "look":
            # just re-loop and reprint
            continue

        # --- AI toggles (reuse logic from handle_player_turn) ---
        if op == "ai":
            if len(parts) < 3:
                print("usage: ai on|off IDX [IDX or A-B...]")
                continue
            mode = parts[1].lower()
            if mode not in ("on", "off"):
                print("usage: ai on|off IDX [IDX or A-B...]")
                continue
            indices = parse_index_tokens(parts[2:], len(chars))
            if not indices:
                print("no valid indices")
                continue
            val = (mode == "on")
            for i in indices:
                ch = chars[i]
                ch["ai_enabled"] = val
                print(f"AI {'ON' if val else 'OFF'} for [{i+1}] {ch.get('name','?')}")
            continue

        # --- mode toggles (combat / talk / neutral) ---
        if op == "mode":
            if len(parts) < 3:
                print("usage: mode IDX[..] TYPE  (TYPE = combat|talk|neutral)")
                continue
            mode_str = parts[-1].lower()
            if mode_str in ("talk", "conv", "conversation"):
                new_mode = "talk"
            elif mode_str in ("combat", "fight"):
                new_mode = "combat"
            elif mode_str in ("neutral", "idle"):
                new_mode = "neutral"
            else:
                print("unknown mode type; use combat/talk/neutral")
                continue
            idx_tokens = parts[1:-1]
            indices = parse_index_tokens(idx_tokens, len(chars))
            if not indices:
                print("no valid indices")
                continue
            for i in indices:
                ch = chars[i]
                ch["mode"] = new_mode
                print(f"Mode for [{i+1}] {ch.get('name','?')} → {new_mode}")
            continue

        # --- hostility toggles (for your guard/guest logic) ---
        if op == "hostility":
            if len(parts) < 3:
                print("usage: hostility IDX[..] STATE  (STATE = hostile|neutral|friendly)")
                continue
            state = parts[-1].lower()
            if state not in ("hostile", "neutral", "friendly"):
                print("unknown hostility state; use hostile/neutral/friendly")
                continue
            idx_tokens = parts[1:-1]
            indices = parse_index_tokens(idx_tokens, len(chars))
            if not indices:
                print("no valid indices")
                continue
            for i in indices:
                ch = chars[i]
                ch["hostility"] = state
                print(f"Hostility for [{i+1}] {ch.get('name','?')} → {state}")
            continue

                # side toggles: side 3-5 guards / side 2 calophage_minions
        if op == "side":
            if len(parts) < 3:
                print("usage: side IDX[..] LABEL")
                continue
            new_side = parts[-1]
            idx_tokens = parts[1:-1]
            indices = parse_index_tokens(idx_tokens, len(chars))
            if not indices:
                print("no valid indices")
                continue
            for i in indices:
                ch = chars[i]
                old_side = ch.get("side", "?")
                ch["side"] = new_side
                print(f"Side for [{i+1}] {ch.get('name','?')} : {old_side} → {new_side}")
            continue

        print("unknown setup command")

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

    # basic side + player detection
    for ch in chars:
        if ch.get("player", False) or str(ch.get("id", "")).startswith("player-"):
            ch["side"] = "players"
            ch["player"] = True
        else:
            ch.setdefault("side", "raiders")

    # initialize stance / hostility / AI flags now that side/player is known
    init_social_flags(chars)

    if not preflight_setup(chars):
        # optional: persist any tweaks you made (AI flags etc.) before exiting
        save_back_vessels(chars)
        print("Done. No combat rounds were run.")
        return

    max_rounds = 15
    for rnd in range(1, max_rounds + 1):
        print(f"\n===== ROUND {rnd} =====")

        # check for any new JSONs dropped into ./initiative
        new_chars = load_new_characters(chars)
        if new_chars:
            print(f"[JOIN] {len(new_chars)} new combatant(s) added from ./initiative:")
            for nc in new_chars:
                print(f"   - {nc.get('name','(unnamed)')} [{nc.get('side','?')}]")
            chars.extend(new_chars)

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
                if not ch.get("ai_enabled", True):
                    print(f"{ch['name']} (AI OFF) takes no action.")
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
