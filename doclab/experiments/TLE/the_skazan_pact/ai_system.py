#!/usr/bin/env python3
"""
ai_system.py - NPC decision-making, targeting, and Player Reactions
"""

import random
from utils import distance_2d, roll_dice


def player_reaction_prompt(attacker, target, incoming_damage, damage_type, info_str):
    """
    Interrupts combat to allow player to Block or Dodge.
    Returns the final damage to be applied.
    """
    if incoming_damage <= 0:
        return 0

    print(f"\n{'!'*60}")
    print(f"  REACTION MOMENT: {target['name']}")
    print(f"{'!'*60}")
    print(f"  Attacker: {attacker['name']}")
    print(f"  Incoming: {incoming_damage} {damage_type} damage")
    print(f"  Details:  {info_str}")
    print(f"  You:      HP {target['pools']['HP']}/{target['pools']['max_HP']} | EP {target['pools']['EP']}/{target['pools']['max_EP']}")
    
    while True:
        print("\n  [1] TAKE IT: Take full damage")
        print("  [2] BLOCK:   Spend EP to reduce damage (1 EP = -1 DMG)")
        print("  [3] DODGE:   Risk it! (Dex check vs DC 12)")
        
        choice = input(f"  {target['name']} Reaction > ").strip()
        
        if choice == "1":
            return incoming_damage
            
        elif choice == "2":
            max_block = target['pools']['EP']
            if max_block == 0:
                print("  You have 0 EP! You cannot block.")
                continue
                
            print(f"  How much EP to spend? (Max {max_block}, Need {incoming_damage})")
            try:
                spend = int(input("  EP amount > "))
                if spend < 0: spend = 0
                if spend > max_block: spend = max_block
                
                target['pools']['EP'] -= spend
                reduced_dmg = max(0, incoming_damage - spend)
                print(f"  >> BLOCK: Spent {spend} EP. Damage reduced to {reduced_dmg}.")
                return reduced_dmg
            except ValueError:
                print("  Invalid amount.")

        elif choice == "3":
            # Simple Dodge Mechanic: 1d20 + Dex Bonus vs DC 12
            # You can make this DC dynamic later based on attacker accuracy
            from character_state import ability_bonus
            dex_mod = ability_bonus(target, "dex")
            roll = random.randint(1, 20)
            total = roll + dex_mod
            
            print(f"  >> DODGE: Rolled {roll} + {dex_mod} (DEX) = {total} vs DC 12")
            
            if total >= 12:
                print("  >> SUCCESS! You evade the attack completely!")
                return 0
            else:
                print("  >> FAIL! You take full damage.")
                return incoming_damage
        else:
            print("  Invalid selection.")


def choose_target(character, all_chars):
    """
    AI chooses a target based on hostility and tactics.
    """
    hostility = character.get("hostility", "hostile")
    side = character.get("side", "")
    
    # Get valid targets
    enemies = []
    for other in all_chars:
        if other is character:
            continue
        if other["pools"]["HP"] <= 0:
            continue
        
        # Target based on hostility
        if hostility == "hostile":
            # Attack different sides
            if other.get("side") != side:
                enemies.append(other)
        elif hostility == "neutral":
            # Only defend self, don't initiate (unless provoked, handled elsewhere)
            pass
        else:  # friendly
            pass
    
    if not enemies:
        return None
    
    # Choose target based on tactics
    tactics = character.get("tactics", "random")
    
    if tactics == "weakest":
        return min(enemies, key=lambda c: c["pools"]["HP"])
    elif tactics == "strongest":
        return max(enemies, key=lambda c: c["pools"]["HP"])
    elif tactics == "closest":
        return min(enemies, key=lambda c: distance_2d(
            character.get("position", {}),
            c.get("position", {})
        ))
    else:  # random
        return random.choice(enemies)


def calculate_ai_action_budget(character):
    """
    Calculate how much EP an AI should spend this turn.
    """
    current_ep = character["pools"]["EP"]
    max_ep = character["pools"]["max_EP"]
    current_hp = character["pools"]["HP"]
    max_hp = character["pools"]["max_HP"]
    
    # Calculate HP percentage
    hp_percent = current_hp / max_hp if max_hp > 0 else 0
    
    # Base budget: use 50-70% of available EP
    base_percent = random.uniform(0.5, 0.7)
    
    # Adjust based on HP
    if hp_percent < 0.3:
        # Low HP: more conservative or desperate
        personality = character.get("personality", "balanced")
        if personality == "cautious":
            base_percent *= 0.7  # More conservative
        elif personality == "aggressive":
            base_percent *= 1.3  # Go all in
    
    budget = int(current_ep * base_percent)
    budget = max(2, min(budget, current_ep))  # At least 2, at most current
    
    # Split between damage and utility
    damage_ep = int(budget * 0.7)
    utility_ep = budget - damage_ep
    
    return {
        "total": budget,
        "damage": damage_ep,
        "utility": utility_ep
    }


def ai_decide_action(character, all_chars):
    """
    AI decides what action to take.
    """
    stance = character.get("stance", "combat")
    
    if stance == "conversation":
        # Try to talk
        targets = [c for c in all_chars 
                  if c is not character and c["pools"]["HP"] > 0]
        if targets:
            return {
                "type": "conversation",
                "target": random.choice(targets)
            }
    
    # Combat action
    target = choose_target(character, all_chars)
    
    if not target:
        return {
            "type": "pass"
        }
    
    budget = calculate_ai_action_budget(character)
    
    # Decide attack type
    has_spells = len(character.get("spells", [])) > 0
    # has_weapon = character.get("equipped", {}).get("weapon") is not None
    
    action_type = "attack"
    if has_spells and random.random() > 0.5:
        action_type = "spell"
    
    return {
        "type": action_type,
        "target": target,
        "budget": budget
    }


def ai_take_turn(character, all_chars, libs):
    """
    Execute AI turn for an NPC.
    """
    print(f"\n--- {character['name']}'s TURN (AI) ---")
    
    # Check if stunned or incapacitated
    if "stunned" in character.get("status_effects", []):
        print(f"{character['name']} is stunned and cannot act.")
        return
    
    # Decide action
    decision = ai_decide_action(character, all_chars)
    
    if decision["type"] == "pass":
        print(f"{character['name']} has no valid targets.")
        return
    
    if decision["type"] == "conversation":
        from social_system import conversation_check
        target = decision["target"]
        print(f"{character['name']} attempts to speak with {target['name']}")
        conversation_check(character, target, stat="wis", mode="auto")
        return
    
    # Combat action
    target = decision["target"]
    budget = decision["budget"]
    
    # Check if target is player to enable reactions
    is_player_target = target.get("player", False)
    
    if decision["type"] == "spell":
        # Cast spell
        spells = character.get("spells", [])
        if spells:
            spell_id = random.choice(spells)
            from spellcasting import resolve_spell_cast
            from damage_system import route_damage_to_wounds
            
            damage_ep = budget["damage"]
            range_ep = budget["utility"]
            
            # Resolve the cast mechanics first
            result = resolve_spell_cast(
                character, target, spell_id,
                damage_ep, range_ep, libs, mode="auto"
            )
            
            if result.get("success"):
                final_damage = result["damage"]
                
                # --- INTERRUPT FOR PLAYER REACTION ---
                if is_player_target and final_damage > 0:
                    final_damage = player_reaction_prompt(
                        character, target, final_damage, "arcane", f"Spell: {spell_id}"
                    )
                # -------------------------------------
                
                log = []
                route_damage_to_wounds(target, final_damage, "arcane", log)
                for line in log:
                    print(f"  {line}")
                    
            # Deduct EP even if missed/blocked, as spell was cast
            character["pools"]["EP"] -= result.get("ep_spent", 0)
    
    else:
        # Basic attack
        from dice_buy import calculate_attack_with_dice_buy
        from damage_system import route_damage_to_wounds
        
        # Decide how much to gamble on dice
        base_ep = int(budget["damage"] * 0.7)
        buy_ep = budget["damage"] - base_ep
        
        result = calculate_attack_with_dice_buy(base_ep, buy_ep)
        
        print(f"{character['name']} attacks {target['name']}")
        if result["dice_result"]:
            print(f"  Base: {result['base_damage']}")
            print(f"  Dice: {result['dice_result']['roll_detail']}")
        print(f"  Raw Damage: {result['total_damage']}")
        
        final_damage = result["total_damage"]
        
        # --- INTERRUPT FOR PLAYER REACTION ---
        if is_player_target and final_damage > 0:
             final_damage = player_reaction_prompt(
                 character, target, final_damage, "physical", "Standard Attack"
             )
        # -------------------------------------
        
        log = []
        route_damage_to_wounds(target, final_damage, "physical", log)
        for line in log:
            print(f"  {line}")

        # Deduct EP
        character["pools"]["EP"] -= budget["total"]


def set_ai_personality(character, personality):
    """
    Set AI personality/tactics.
    """
    valid = ["cautious", "aggressive", "balanced", "protective"]
    if personality not in valid:
        return False
    
    character["personality"] = personality
    
    # Set associated tactics
    tactics_map = {
        "cautious": "weakest",
        "aggressive": "strongest",
        "balanced": "random",
        "protective": "closest"
    }
    character["tactics"] = tactics_map.get(personality, "random")
    
    print(f"{character['name']} personality set to: {personality}")
    return True


def set_ai_tactics(character, tactics):
    """
    Set AI targeting tactics.
    """
    valid = ["random", "weakest", "strongest", "closest"]
    if tactics not in valid:
        return False
    
    character["tactics"] = tactics
    print(f"{character['name']} tactics set to: {tactics}")
    return True