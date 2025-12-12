#!/usr/bin/env python3
"""
influence_system.py - Apply influences and effects to characters
"""

from copy import deepcopy


def apply_influence(influence, source, target, context):
    """
    Apply an influence effect from source to target.
    
    Args:
        influence: Influence definition dict
        source: Character applying influence
        target: Character receiving influence
        context: Context dict with ep_spent, axis, log, etc.
    
    Yields:
        additional influence IDs to apply (chain reactions)
    """
    log = context.get("log", [])
    inf_type = influence.get("type", "damage")
    
    if inf_type == "damage":
        # Apply damage
        damage = influence.get("base_damage", 0)
        damage_type = influence.get("damage_type", "generic")
        
        # Scale by EP if configured
        if influence.get("scales_with_ep", False):
            ep_spent = context.get("ep_spent", 0)
            scale = influence.get("ep_scale", 1.0)
            damage += int(ep_spent * scale)
        
        from damage_system import route_damage_to_wounds
        route_damage_to_wounds(target, damage, damage_type, log)
    
    elif inf_type == "heal":
        # Apply healing
        heal = influence.get("base_heal", 0)
        
        if influence.get("scales_with_ep", False):
            ep_spent = context.get("ep_spent", 0)
            scale = influence.get("ep_scale", 1.0)
            heal += int(ep_spent * scale)
        
        from damage_system import heal_wounds
        result = heal_wounds(target, heal)
        log.append(f"{target['name']} heals {result['total_healed']} HP")
    
    elif inf_type == "buff":
        # Apply stat buff
        stat = influence.get("stat")
        bonus = influence.get("bonus", 1)
        duration = influence.get("duration", 1)
        
        target.setdefault("buffs", []).append({
            "stat": stat,
            "bonus": bonus,
            "duration": duration,
            "source": source.get("name")
        })
        log.append(f"{target['name']} gains +{bonus} {stat} for {duration} rounds")
    
    elif inf_type == "debuff":
        # Apply stat debuff
        stat = influence.get("stat")
        penalty = influence.get("penalty", 1)
        duration = influence.get("duration", 1)
        
        target.setdefault("debuffs", []).append({
            "stat": stat,
            "penalty": penalty,
            "duration": duration,
            "source": source.get("name")
        })
        log.append(f"{target['name']} suffers -{penalty} {stat} for {duration} rounds")
    
    elif inf_type == "status":
        # Apply status effect
        status = influence.get("status_effect")
        duration = influence.get("duration", 1)
        
        target.setdefault("status_effects", []).append(status)
        log.append(f"{target['name']} is {status}!")
    
    elif inf_type == "summon":
        # Summon creature (requires special handling)
        log.append(f"{source['name']} summons something!")
    
    # Check for chained influences
    chains = influence.get("chains", [])
    for chain_id in chains:
        yield chain_id


def resolve_item_use(character, item_id, target, libs):
    """
    Resolve using an item from inventory.
    
    Args:
        character: Character using item
        item_id: Item identifier
        target: Target character (can be self)
        libs: Library dict
    
    Returns:
        dict with use results
    """
    inventory = character.get("inventory", [])
    
    # Check if character has item
    item_entry = None
    for i, entry in enumerate(inventory):
        if isinstance(entry, dict):
            if entry.get("item_id") == item_id:
                item_entry = entry
                break
        elif entry == item_id:
            item_entry = {"item_id": item_id, "quantity": 1}
            inventory[i] = item_entry
            break
    
    if not item_entry:
        return {
            "success": False,
            "reason": "item_not_in_inventory"
        }
    
    # Get item template
    item = libs.get("items", {}).get(item_id)
    if not item:
        return {
            "success": False,
            "reason": "item_not_found"
        }
    
    # Check if consumable
    if item.get("consumable", False):
        quantity = item_entry.get("quantity", 1)
        if quantity <= 0:
            return {
                "success": False,
                "reason": "no_charges"
            }
        item_entry["quantity"] = quantity - 1
    
    # Apply item influences
    log = []
    ctx = {"ep_spent": 0, "axis": None, "log": log}
    
    influences = item.get("influences", [])
    for inf_id in influences:
        inf = libs.get("influences", {}).get(inf_id)
        if inf:
            list(apply_influence(inf, character, target, ctx))
    
    return {
        "success": True,
        "log": log
    }


def start_of_round_reactions(chars, libs):
    """
    Process start-of-round effects and reactions.
    
    Args:
        chars: All characters
        libs: Library dict
    """
    print("\n=== START OF ROUND REACTIONS ===")
    
    for ch in chars:
        if ch["pools"]["HP"] <= 0:
            continue
        
        log = []
        
        # Process buffs/debuffs duration
        process_effect_durations(ch, log)
        
        # Check equipped items for start-of-round effects
        equipped = ch.get("equipped", {})
        for slot, item_id in equipped.items():
            if not item_id:
                continue
            
            item = libs.get("items", {}).get(item_id)
            if not item:
                continue
            
            # Check for start_of_round influences
            if item.get("triggers_on") == "start_of_round":
                ctx = {"ep_spent": 0, "axis": None, "log": log}
                influences = item.get("influences", [])
                
                for inf_id in influences:
                    inf = libs.get("influences", {}).get(inf_id)
                    if inf:
                        list(apply_influence(inf, ch, ch, ctx))
        
        if log:
            print(f"{ch['name']}:")
            for line in log:
                print(f"  {line}")


def process_effect_durations(character, log):
    """
    Decrement effect durations and remove expired effects.
    
    Args:
        character: Character to process
        log: Log list to append messages
    """
    # Process buffs
    buffs = character.get("buffs", [])
    remaining_buffs = []
    
    for buff in buffs:
        buff["duration"] -= 1
        if buff["duration"] > 0:
            remaining_buffs.append(buff)
        else:
            log.append(f"Buff expired: +{buff['bonus']} {buff['stat']}")
    
    character["buffs"] = remaining_buffs
    
    # Process debuffs
    debuffs = character.get("debuffs", [])
    remaining_debuffs = []
    
    for debuff in debuffs:
        debuff["duration"] -= 1
        if debuff["duration"] > 0:
            remaining_debuffs.append(debuff)
        else:
            log.append(f"Debuff expired: -{debuff['penalty']} {debuff['stat']}")
    
    character["debuffs"] = remaining_debuffs
    
    # Process status effects (if they have duration)
    # This would need more sophisticated tracking
