#!/usr/bin/env python3
"""
spellcasting.py - Spell resolution with TLE range mechanics
Implements distance-based EP costs and Spell Sniper's Gambit
"""

import random
from utils import distance_2d
from character_state import ability_bonus


def calculate_spell_range_cost(distance_ft):
    """
    Calculate EP cost for spell range.
    TLE-001 rule: 1 EP spent = 5 ft of range
    
    Args:
        distance_ft: Distance to target in feet
    
    Returns:
        EP cost for that distance
    """
    return (distance_ft + 4) // 5  # Round up


def calculate_spell_snipers_gambit(distance_ft, extra_range_ft):
    """
    Calculate cost for Spell Sniper's Gambit.
    1 additional EP = 5-10 ft extra range
    
    Args:
        distance_ft: Base distance to target
        extra_range_ft: Additional range needed
    
    Returns:
        EP cost for gambit
    """
    # Each EP gives 5-10 ft, so we need ceil(extra_range / 5) EP minimum
    return (extra_range_ft + 4) // 5


def check_spell_range(caster, target, ep_available, spell_info=None):
    """
    Check if caster has enough EP to reach target with spell.
    
    Args:
        caster: Caster character dict
        target: Target character dict
        ep_available: EP caster is willing to spend on range
        spell_info: Optional spell data with range modifiers
    
    Returns:
        dict with 'in_range', 'distance', 'ep_needed', 'ep_remaining'
    """
    # Calculate distance
    distance = distance_2d(caster.get("position", {}), target.get("position", {}))
    
    # EP needed for this distance
    ep_needed = calculate_spell_range_cost(distance)
    
    # Check spell modifiers
    range_multiplier = 1.0
    if spell_info:
        range_multiplier = spell_info.get("range_multiplier", 1.0)
    
    effective_ep_needed = int(ep_needed / range_multiplier)
    
    in_range = ep_available >= effective_ep_needed
    ep_remaining = ep_available - effective_ep_needed if in_range else 0
    
    return {
        "in_range": in_range,
        "distance": distance,
        "ep_needed": effective_ep_needed,
        "ep_remaining": ep_remaining,
        "range_multiplier": range_multiplier
    }


def resolve_spell_cast(caster, target, spell_id, ep_damage, ep_range, libs, mode="auto"):
    """
    Resolve a spell cast with range and damage.
    
    Args:
        caster: Caster character
        target: Target character
        spell_id: Spell identifier
        ep_damage: EP spent on damage
        ep_range: EP spent on range
        libs: Library dict
        mode: "auto" or "manual" for accuracy check
    
    Returns:
        dict with cast results
    """
    spell = libs.get("spells", {}).get(spell_id, {})
    spell_name = spell.get("name", spell_id)
    
    print(f"\n[SPELL] {caster['name']} casts {spell_name} at {target['name']}")
    
    # Check range
    range_check = check_spell_range(caster, target, ep_range, spell)
    
    if not range_check["in_range"]:
        print(f"[SPELL] ✗ OUT OF RANGE!")
        print(f"  Distance: {range_check['distance']:.1f} ft")
        print(f"  EP needed: {range_check['ep_needed']}")
        print(f"  EP available: {ep_range}")
        print(f"  Consider Spell Sniper's Gambit for +5-10 ft per extra EP")
        return {
            "success": False,
            "reason": "out_of_range",
            "range_check": range_check
        }
    
    print(f"  Distance: {range_check['distance']:.1f} ft (costs {range_check['ep_needed']} EP)")
    print(f"  Damage EP: {ep_damage}")
    
    # TLE-001 accuracy check: d20 + DEX + INT vs TN
    # TN = 8 + floor(EP_damage / 2)
    dex_mod = ability_bonus(caster, "dex")
    int_mod = ability_bonus(caster, "int")
    tn = 8 + (ep_damage // 2)
    
    print(f"  Accuracy: d20 + DEX({dex_mod:+d}) + INT({int_mod:+d}) vs TN {tn}")
    
    if mode == "manual":
        print(f"  Roll 1d20 + {dex_mod + int_mod} and enter total (or 'q' to cancel):")
        while True:
            raw = input("  total> ").strip()
            if raw.lower().startswith("q"):
                print("[SPELL] Cast cancelled.")
                return {"success": False, "reason": "cancelled"}
            try:
                total = int(raw)
                break
            except ValueError:
                print("  Please enter an integer or 'q'.")
    else:
        die = random.randint(1, 20)
        total = die + dex_mod + int_mod
        print(f"  Roll: 1d20({die}) + {dex_mod + int_mod} = {total}")
    
    hit = total >= tn
    
    if not hit:
        print(f"[SPELL] ✗ MISS")
        return {
            "success": False,
            "reason": "missed",
            "total": total,
            "tn": tn
        }
    
    print(f"[SPELL] ✓ HIT")
    
    # Calculate damage
    # Spells use axis-based damage from influences
    damage = ep_damage  # Base damage, modified by influences
    
    # Apply spell influences if any
    if "influences" in spell:
        for inf_id in spell["influences"]:
            inf = libs.get("influences", {}).get(inf_id)
            if inf:
                # Apply influence effects
                damage_mod = inf.get("damage_modifier", 1.0)
                damage = int(damage * damage_mod)
    
    print(f"  Damage: {damage}")
    
    return {
        "success": True,
        "damage": damage,
        "ep_spent": ep_damage + ep_range,
        "range_check": range_check,
        "total": total,
        "tn": tn
    }


def handle_split_cast(caster, targets, spell_id, ep_damage, ep_range, libs):
    """
    Handle split casting to multiple targets.
    TLE-001: +3 EP per additional target.
    
    Args:
        caster: Caster character
        targets: List of target characters
        spell_id: Spell identifier
        ep_damage: EP for damage (split among targets)
        ep_range: EP for range (must reach furthest target)
        libs: Library dict
    
    Returns:
        list of cast results
    """
    num_targets = len(targets)
    split_cost = 3 * (num_targets - 1)
    
    print(f"\n[SPLIT CAST] {caster['name']} targets {num_targets} creatures")
    print(f"  Split cost: +{split_cost} EP")
    
    # Check if caster has enough EP
    total_ep_needed = ep_damage + ep_range + split_cost
    if caster["pools"]["EP"] < total_ep_needed:
        print(f"[SPLIT CAST] ✗ Insufficient EP!")
        print(f"  Need: {total_ep_needed}, Have: {caster['pools']['EP']}")
        return []
    
    # Damage is split among targets
    damage_per_target = ep_damage // num_targets
    
    results = []
    for target in targets:
        result = resolve_spell_cast(
            caster, target, spell_id, 
            damage_per_target, ep_range, libs
        )
        results.append(result)
    
    return results


def explain_spellcasting():
    """Print explanation of spellcasting system"""
    print("\n=== SPELLCASTING SYSTEM ===")
    print("Range Cost: 1 EP = 5 feet of range")
    print("Spell Sniper's Gambit: +1 EP = 5-10 extra feet")
    print("Split Cast: +3 EP per additional target")
    print("\nAccuracy: d20 + DEX + INT vs TN")
    print("TN = 8 + floor(Damage EP / 2)")
    print("\nUsage: cast <spell_id> <target> spend <damage_ep> range <range_ep>")
    print("       cast <spell_id> <target1> <target2> ... spend <damage_ep> range <range_ep>\n")
