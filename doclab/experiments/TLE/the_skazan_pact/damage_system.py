#!/usr/bin/env python3
"""
damage_system.py - Wound channels and damage resolution
"""

from copy import deepcopy


def route_damage_to_wounds(target, damage_amount, damage_type, log):
    """
    Route damage through wound channels.
    
    Args:
        target: Character receiving damage
        damage_amount: Total damage
        damage_type: Type of damage (cut, pierce, blunt, thermal, etc.)
        log: List to append log messages
    
    Returns:
        actual_damage: Damage after armor/block
    """
    wounds = target.setdefault("wounds", {})
    pools = target.get("pools", {})
    
    # Apply temp block first
    temp_block = pools.get("temp_block", 0)
    if temp_block > 0:
        blocked = min(temp_block, damage_amount)
        damage_amount -= blocked
        pools["temp_block"] -= blocked
        log.append(f"{target['name']} blocks {blocked} damage (temp_block)")
    
    # Route through wound channel
    if damage_type in wounds:
        wounds[damage_type] += damage_amount
        log.append(f"{target['name']} takes {damage_amount} {damage_type} damage")
    else:
        # Unknown damage type, default to generic
        wounds.setdefault("generic", 0)
        wounds["generic"] += damage_amount
        log.append(f"{target['name']} takes {damage_amount} generic damage")
    
    # Apply to HP
    pools["HP"] = max(0, pools["HP"] - damage_amount)
    
    if pools["HP"] <= 0:
        log.append(f"{target['name']} is DEFEATED!")
    
    return damage_amount


def apply_wound_effects(character):
    """
    Check wound thresholds and apply status effects.
    This can be expanded with more sophisticated wound tracking.
    
    Args:
        character: Character to check
    
    Returns:
        list of status effects applied
    """
    wounds = character.get("wounds", {})
    max_hp = character["pools"]["max_HP"]
    effects = []
    
    # Check for major wounds
    for wound_type, amount in wounds.items():
        if amount > max_hp * 0.3:
            effect = f"major_{wound_type}_wound"
            if effect not in character.get("status_effects", []):
                effects.append(effect)
                character.setdefault("status_effects", []).append(effect)
    
    return effects


def heal_wounds(character, heal_amount, wound_type=None):
    """
    Heal specific wound types or distribute healing.
    
    Args:
        character: Character to heal
        heal_amount: Amount of healing
        wound_type: Specific wound type to heal, or None for all
    
    Returns:
        dict with healing details
    """
    wounds = character.get("wounds", {})
    pools = character.get("pools", {})
    
    if wound_type and wound_type in wounds:
        # Heal specific wound type
        healed = min(heal_amount, wounds[wound_type])
        wounds[wound_type] -= healed
        pools["HP"] = min(pools["max_HP"], pools["HP"] + healed)
        
        return {
            "total_healed": healed,
            "wounds_healed": {wound_type: healed}
        }
    
    # Distribute healing across all wounds
    total_wounds = sum(wounds.values())
    if total_wounds == 0:
        # No wounds to heal, just restore HP
        healed = min(heal_amount, pools["max_HP"] - pools["HP"])
        pools["HP"] += healed
        return {
            "total_healed": healed,
            "wounds_healed": {}
        }
    
    # Proportional healing
    healed_by_type = {}
    remaining_heal = heal_amount
    
    for wtype, amount in wounds.items():
        if remaining_heal <= 0:
            break
        
        proportion = amount / total_wounds
        heal_this = min(int(heal_amount * proportion), amount, remaining_heal)
        
        wounds[wtype] -= heal_this
        healed_by_type[wtype] = heal_this
        remaining_heal -= heal_this
    
    total_healed = heal_amount - remaining_heal
    pools["HP"] = min(pools["max_HP"], pools["HP"] + total_healed)
    
    return {
        "total_healed": total_healed,
        "wounds_healed": healed_by_type
    }


def calculate_armor_absorption(attacker, target, damage_amount, libs):
    """
    Calculate damage absorption from armor.
    Armor has its own AEP (Armor Entropy Pool).
    
    Args:
        attacker: Attacking character
        target: Target with armor
        damage_amount: Incoming damage
        libs: Library dict
    
    Returns:
        dict with absorbed and penetrating damage
    """
    equipped = target.get("equipped", {})
    armor_id = equipped.get("armor")
    
    if not armor_id:
        return {
            "absorbed": 0,
            "penetrating": damage_amount,
            "armor_destroyed": False
        }
    
    # Get armor data
    armor = target.get("armor_data")
    if not armor:
        # Load from library if needed
        armor_lib = libs.get("items", {})
        armor_template = armor_lib.get(armor_id)
        if armor_template:
            armor = deepcopy(armor_template)
            target["armor_data"] = armor
    
    if not armor:
        return {
            "absorbed": 0,
            "penetrating": damage_amount,
            "armor_destroyed": False
        }
    
    # Get armor's entropy pool
    aep = armor.get("aep", 0)
    
    if aep <= 0:
        # Armor is broken
        return {
            "absorbed": 0,
            "penetrating": damage_amount,
            "armor_destroyed": True
        }
    
    # Armor absorbs damage
    absorbed = min(aep, damage_amount)
    armor["aep"] -= absorbed
    penetrating = damage_amount - absorbed
    
    armor_destroyed = armor["aep"] <= 0
    
    return {
        "absorbed": absorbed,
        "penetrating": penetrating,
        "armor_destroyed": armor_destroyed,
        "remaining_aep": armor["aep"]
    }
