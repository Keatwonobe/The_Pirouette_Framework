#!/usr/bin/env python3
"""
social_system.py - Conversation, stance, and hostility mechanics
"""

import random
from character_state import ability_bonus


def conversation_check(speaker, listener, stat="wis", mode="auto"):
    """
    Resolve a conversation roll between two characters.
    
    Args:
        speaker: Character initiating conversation
        listener: Character being spoken to
        stat: Stat to use for check (default: wis)
        mode: "auto" (script rolls) or "manual" (GM enters)
    
    Returns:
        dict with outcome
    """
    stat = stat.lower()
    atk_bonus = ability_bonus(speaker, stat)
    def_bonus = ability_bonus(listener, stat)
    
    dc = 10 + def_bonus
    
    print(f"\n[CONV] {speaker['name']} engages {listener['name']}")
    print(f"[CONV] Using {stat.upper()} vs DC {dc}")
    
    if mode == "manual":
        print(f"[CONV] Roll 1d20 + {atk_bonus} and enter total (or 'q' to cancel):")
        while True:
            raw = input("  total> ").strip()
            if raw.lower().startswith("q"):
                print("[CONV] Conversation cancelled.")
                return None
            try:
                total = int(raw)
                break
            except ValueError:
                print("  Please enter an integer or 'q'.")
    else:
        die = random.randint(1, 20)
        total = die + atk_bonus
        print(f"[CONV] Roll: 1d20({die}) + {atk_bonus} = {total}")
    
    success = total >= dc
    outcome = "success" if success else "failure"
    
    print(f"[CONV] Result: {outcome.upper()}")
    
    # Store on speaker
    conv = speaker.setdefault("conversation", {})
    conv.update({
        "last_roll": total,
        "last_dc": dc,
        "last_stat": stat,
        "last_target": listener.get("name"),
        "outcome": outcome
    })
    
    # Apply hostility shifts
    apply_conversation_result(speaker, listener, success)
    
    return {
        "success": success,
        "total": total,
        "dc": dc,
        "stat": stat
    }


def apply_conversation_result(speaker, listener, success):
    """
    Apply hostility changes based on conversation success.
    
    Args:
        speaker: Character who spoke
        listener: Character who listened
        success: Whether check succeeded
    """
    current_hostility = listener.get("hostility", "neutral")
    
    if success:
        if current_hostility == "hostile":
            listener["hostility"] = "neutral"
            print(f"[CONV] {listener['name']} shifts: HOSTILE → NEUTRAL")
        elif current_hostility == "neutral":
            listener["hostility"] = "friendly"
            print(f"[CONV] {listener['name']} shifts: NEUTRAL → FRIENDLY")
        else:
            print(f"[CONV] {listener['name']} remains FRIENDLY")
    else:
        if current_hostility == "neutral":
            listener["hostility"] = "hostile"
            print(f"[CONV] {listener['name']} is offended: NEUTRAL → HOSTILE")
        elif current_hostility == "friendly":
            listener["hostility"] = "neutral"
            print(f"[CONV] {listener['name']} is disappointed: FRIENDLY → NEUTRAL")
        else:
            print(f"[CONV] {listener['name']} remains HOSTILE")


def set_stance(character, new_stance):
    """
    Change character's stance.
    
    Args:
        character: Character to modify
        new_stance: "combat", "conversation", or "neutral"
    """
    valid_stances = ["combat", "conversation", "neutral", "talk"]
    
    if new_stance not in valid_stances:
        return False
    
    # Normalize talk to conversation
    if new_stance == "talk":
        new_stance = "conversation"
    
    old_stance = character.get("stance", "combat")
    character["stance"] = new_stance
    
    print(f"{character['name']} stance: {old_stance} → {new_stance}")
    return True


def set_hostility(character, new_hostility):
    """
    Change character's hostility level.
    
    Args:
        character: Character to modify
        new_hostility: "hostile", "neutral", or "friendly"
    """
    valid_hostility = ["hostile", "neutral", "friendly"]
    
    if new_hostility not in valid_hostility:
        return False
    
    old_hostility = character.get("hostility", "neutral")
    character["hostility"] = new_hostility
    
    print(f"{character['name']} hostility: {old_hostility} → {new_hostility}")
    return True


def get_conversation_targets(character, all_chars):
    """
    Get valid conversation targets based on stance and hostility.
    
    Args:
        character: Character looking for targets
        all_chars: All characters in scene
    
    Returns:
        list of valid targets
    """
    targets = []
    
    for other in all_chars:
        if other is character:
            continue
        if other["pools"]["HP"] <= 0:
            continue
        
        # Can talk to anyone, but hostile targets are harder
        targets.append(other)
    
    return targets


def handle_conversation_turn(speaker, all_chars):
    """
    Handle a character's conversation turn.
    
    Args:
        speaker: Character taking conversation action
        all_chars: All characters in scene
    """
    print(f"\n--- {speaker['name']}'s CONVERSATION TURN ---")
    
    targets = get_conversation_targets(speaker, all_chars)
    
    if not targets:
        print("No valid conversation targets.")
        return
    
    print("Available targets:")
    for i, t in enumerate(targets, 1):
        hostility = t.get("hostility", "neutral")
        print(f"  [{i}] {t['name']} ({hostility})")
    
    print("\nCommand: talk <target_num> [stat]")
    print("         (stat = str/dex/con/int/wis, default wis)")
    
    while True:
        cmd = input("conv> ").strip()
        if not cmd:
            continue
        
        parts = cmd.split()
        op = parts[0].lower()
        
        if op in ("skip", "pass", "q"):
            print("Conversation turn skipped.")
            return
        
        if op == "talk":
            if len(parts) < 2:
                print("Usage: talk <target_num> [stat]")
                continue
            
            try:
                target_idx = int(parts[1]) - 1
            except ValueError:
                print("Invalid target number")
                continue
            
            if target_idx < 0 or target_idx >= len(targets):
                print("Target number out of range")
                continue
            
            target = targets[target_idx]
            stat = parts[2] if len(parts) > 2 else "wis"
            
            conversation_check(speaker, target, stat=stat, mode="auto")
            return


def get_social_modifier(character1, character2):
    """
    Calculate social interaction modifier based on hostility.
    
    Args:
        character1: First character
        character2: Second character
    
    Returns:
        modifier to apply to social checks
    """
    hostility = character2.get("hostility", "neutral")
    
    modifiers = {
        "friendly": -2,  # Easier to convince
        "neutral": 0,
        "hostile": +4   # Harder to convince
    }
    
    return modifiers.get(hostility, 0)
