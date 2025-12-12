#!/usr/bin/env python3
"""
character_state.py - Character loading, saving, and state management
"""

import os
import json
import datetime
import random
from copy import deepcopy


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INIT_DIR = os.path.join(BASE_DIR, "initiative")


def default_wound_channels():
    return {
        "cut": 0, "pierce": 0, "blunt": 0, "thermal": 0,
        "cold": 0, "lightning": 0, "acid": 0,
    }


def default_pools():
    return {
        "HP": 10, "max_HP": 10,
        "EP": 10, "max_EP": 10,
        "temp_block": 0
    }


def load_initiative():
    chars = []
    if not os.path.isdir(INIT_DIR):
        os.makedirs(INIT_DIR, exist_ok=True)
        return chars
    
    for fn in os.listdir(INIT_DIR):
        if not fn.endswith(".json"):
            continue
        full = os.path.join(INIT_DIR, fn)
        try:
            with open(full, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARN] could not load '{full}': {e}")
            continue
        
        data.setdefault("pools", default_pools())
        data.setdefault("wounds", default_wound_channels())
        data.setdefault("stats", {})
        data.setdefault("inventory", [])
        data.setdefault("equipped", {"weapon": None, "armor": None})
        data.setdefault("name", fn.replace(".json", ""))
        data.setdefault("id", fn.replace(".json", ""))
        data.setdefault("position", {"x": 0, "y": 0})
        
        chars.append(data)
    
    return chars


def load_new_characters(existing_chars):
    existing_ids = {c.get("id") for c in existing_chars}
    new_chars = []
    
    if not os.path.isdir(INIT_DIR):
        return new_chars
    
    for fn in os.listdir(INIT_DIR):
        if not fn.endswith(".json"):
            continue
        
        char_id = fn.replace(".json", "")
        if char_id in existing_ids:
            continue
        
        full = os.path.join(INIT_DIR, fn)
        try:
            with open(full, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARN] could not load new character '{full}': {e}")
            continue
        
        data.setdefault("pools", default_pools())
        data.setdefault("wounds", default_wound_channels())
        data.setdefault("stats", {})
        data.setdefault("inventory", [])
        data.setdefault("equipped", {"weapon": None, "armor": None})
        data.setdefault("name", char_id)
        data.setdefault("id", char_id)
        data.setdefault("position", {"x": 0, "y": 0})
        
        is_player = bool(data.get("player", False) or str(data.get("id", "")).startswith("player-"))
        if is_player:
            data["side"] = "players"
            data["player"] = True
        else:
            data.setdefault("side", "raiders")
        
        data.setdefault("stance", "combat")
        data.setdefault("hostility", "friendly" if is_player else "hostile")
        data.setdefault("ai_enabled", not is_player)
        data.setdefault("conversation", {
            "last_roll": None, "last_dc": None, "last_stat": None,
            "last_target": None, "outcome": None
        })
        
        new_chars.append(data)
    
    return new_chars


def save_back_vessels(chars):
    now = datetime.datetime.utcnow().isoformat()
    
    for ch in chars:
        char_id = ch.get("id", "unknown")
        fn = f"{char_id}.json"
        full = os.path.join(INIT_DIR, fn)
        
        vessel = ch.setdefault("vessel", {})
        history = vessel.setdefault("history", [])
        history.append({
            "stamp": now,
            "note": "participated in TLE combat session"
        })
        
        try:
            with open(full, "w") as f:
                json.dump(ch, f, indent=2)
        except Exception as e:
            print(f"[WARN] could not save '{full}': {e}")


def init_social_flags(chars):
    for ch in chars:
        is_player = bool(ch.get("player", False) or str(ch.get("id", "")).startswith("player-"))
        ch.setdefault("stance", "combat")
        ch.setdefault("hostility", "friendly" if is_player else "hostile")
        ch.setdefault("ai_enabled", not is_player)
        ch.setdefault("conversation", {
            "last_roll": None, "last_dc": None, "last_stat": None,
            "last_target": None, "outcome": None
        })


def ability_bonus(ch, stat_name: str):
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


def rebuild_initiative(characters):
    return sorted(
        characters,
        key=lambda c: (
            c.get("stats", {}).get("TEP", 10) +
            c.get("stats", {}).get("init_bonus", 0) +
            random.randint(0, 5)
        ),
        reverse=True
    )


def print_state(chars):
    """Print current battlefield state (Robust Version)"""
    print("\n--- BATTLEFIELD STATE ---")
    for i, ch in enumerate(chars, 1):
        # Use .get() to avoid KeyErrors if sanitization missed something
        pools = ch.get("pools", {})
        hp = pools.get("HP", 0)
        max_hp = pools.get("max_HP", 10)
        ep = pools.get("EP", 0)
        max_ep = pools.get("max_EP", 10)
        
        side = ch.get("side", "?")
        stance = ch.get("stance", "combat")
        hostility = ch.get("hostility", "neutral")
        ai = "AI" if ch.get("ai_enabled", False) else "MANUAL"
        
        print(f"[{i}] {ch['name']:<25} | {side:<12} | HP {hp}/{max_hp} | EP {ep}/{max_ep}")
        print(f"     stance={stance:<10} hostility={hostility:<10} {ai}")
    print("-------------------------\n")