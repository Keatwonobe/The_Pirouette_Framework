#!/usr/bin/env python3
"""
check_system.py - NEW: Field visibility and DC-based information revelation
Implements the postmortem's "check" command system for skill-based information gathering
"""

import random
from character_state import ability_bonus


def get_field_visibility(character):
    """
    Get visibility thresholds for character fields.
    Returns dict of field_name -> DC.
    """
    # Check if character has custom visibility defined
    if "visibility" in character:
        return character["visibility"]
    
    # Default visibility thresholds
    default_visibility = {
        "mask_identity": 18,
        "spellbook": 12,
        "true_name": 20,
        "secret_orders": 16,
        "hidden_weapons": 14,
        "vulnerabilities": 16,
        "allegiances": 15,
        "inventory": 10,
        "stats": 12,
    }
    
    return default_visibility


def list_checkable_fields(character, dc_threshold=None):
    """
    List fields that can be checked on a character.
    If dc_threshold provided, only show fields with DC <= threshold.
    Returns list of (field_name, dc) tuples.
    """
    visibility = get_field_visibility(character)
    
    if dc_threshold is None:
        return [(k, v) for k, v in visibility.items()]
    
    return [(k, v) for k, v in visibility.items() if v <= dc_threshold]


def perform_check(checker, target, field_name, mode="auto", bonus_stat=None):
    """
    Perform a check to reveal information about a target.
    
    Args:
        checker: Character performing the check
        target: Character being checked
        field_name: Field to check (e.g., "mask_identity", "spellbook")
        mode: "auto" (script rolls) or "manual" (GM enters roll)
        bonus_stat: Which stat to use for bonus (default: WIS)
    
    Returns:
        dict with 'success', 'total', 'dc', 'revealed_info'
    """
    if bonus_stat is None:
        bonus_stat = "wis"
    
    visibility = get_field_visibility(target)
    
    # Get DC for this field
    if field_name not in visibility:
        # Field doesn't exist or isn't protected
        dc = 8  # Easy check for unprotected info
    else:
        dc = visibility[field_name]
    
    # Calculate modifier
    modifier = ability_bonus(checker, bonus_stat)
    
    print(f"\n[CHECK] {checker['name']} checks {target['name']}'s '{field_name}'")
    print(f"[CHECK] DC {dc} | Using {bonus_stat.upper()} modifier: +{modifier}")
    
    # Roll or get manual input
    if mode == "manual":
        print(f"[CHECK] Roll 1d20 + {modifier} and enter total (or 'q' to cancel):")
        while True:
            raw = input("  total> ").strip()
            if raw.lower().startswith("q"):
                print("[CHECK] Check cancelled.")
                return None
            try:
                total = int(raw)
                break
            except ValueError:
                print("  Please enter an integer or 'q'.")
    else:
        die = random.randint(1, 20)
        total = die + modifier
        print(f"[CHECK] Roll: 1d20({die}) + {modifier} = {total}")
    
    success = total >= dc
    
    # Get revealed information
    revealed_info = None
    if success:
        revealed_info = get_field_info(target, field_name)
        print(f"[CHECK] ✓ SUCCESS - Information revealed!")
    else:
        print(f"[CHECK] ✗ FAILURE - Information remains hidden.")
    
    return {
        "success": success,
        "total": total,
        "dc": dc,
        "field": field_name,
        "revealed_info": revealed_info
    }


def get_field_info(character, field_name):
    """
    Extract the actual information for a field from character JSON.
    Handles nested fields with dot notation (e.g., "stats.str").
    """
    if "." in field_name:
        # Handle nested fields
        parts = field_name.split(".")
        data = character
        for part in parts:
            if isinstance(data, dict) and part in data:
                data = data[part]
            else:
                return None
        return data
    
    # Direct field access
    if field_name in character:
        return character[field_name]
    
    # Special handling for common aliases
    if field_name == "spellbook" and "spells" in character:
        return character["spells"]
    if field_name == "hidden_weapons" and "inventory" in character:
        weapons = [item for item in character.get("inventory", []) 
                   if "weapon" in str(item).lower()]
        return weapons
    
    return None


def handle_check_command(parts, checker, all_chars):
    """
    Handle the 'check' command from CLI.
    
    Usage:
        check <target_idx>.<field> [DC or auto]
        check list <target_idx>
    
    Examples:
        check 3.mask_identity auto
        check 5.spellbook DC 18
        check list 3
    """
    if len(parts) < 2:
        print("Usage: check <target_idx>.<field> [DC or auto]")
        print("       check list <target_idx>")
        return
    
    # Handle 'check list' to show available fields
    if parts[1].lower() == "list":
        if len(parts) < 3:
            print("Usage: check list <target_idx>")
            return
        try:
            target_idx = int(parts[2]) - 1
        except ValueError:
            print("Invalid target index")
            return
        
        if target_idx < 0 or target_idx >= len(all_chars):
            print("Target index out of range")
            return
        
        target = all_chars[target_idx]
        fields = list_checkable_fields(target)
        
        print(f"\n[CHECK] Checkable fields for {target['name']}:")
        for field, dc in sorted(fields, key=lambda x: x[1]):
            print(f"  {field:<20} DC {dc}")
        return
    
    # Parse target.field notation
    if "." not in parts[1]:
        print("Format: <target_idx>.<field_name>")
        return
    
    target_str, field_name = parts[1].split(".", 1)
    
    try:
        target_idx = int(target_str) - 1
    except ValueError:
        print("Invalid target index")
        return
    
    if target_idx < 0 or target_idx >= len(all_chars):
        print("Target index out of range")
        return
    
    target = all_chars[target_idx]
    
    # Determine mode and custom DC
    mode = "auto"
    custom_dc = None
    
    if len(parts) > 2:
        if parts[2].lower() == "manual":
            mode = "manual"
        elif parts[2].upper() == "DC" and len(parts) > 3:
            try:
                custom_dc = int(parts[3])
                # Override the field's DC temporarily
                target.setdefault("visibility", {})
                target["visibility"][field_name] = custom_dc
            except ValueError:
                print("Invalid DC value")
                return
    
    # Perform the check
    result = perform_check(checker, target, field_name, mode=mode)
    
    if result and result["revealed_info"] is not None:
        print(f"\n[INFO] {field_name}: {result['revealed_info']}")
