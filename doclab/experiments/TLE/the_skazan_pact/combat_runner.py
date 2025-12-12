#!/usr/bin/env python3
"""
combat_runner.py - Main orchestrator for TLE combat system
"""

import os
from character_state import (
    load_initiative, load_new_characters, save_back_vessels,
    init_social_flags, rebuild_initiative
)
from utils import load_dir_as_map
from player_interface import handle_player_turn, preflight_setup
from ai_system import ai_take_turn
from influence_system import start_of_round_reactions


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AXES_DIR = os.path.join(BASE_DIR, "axes")
INFL_DIR = os.path.join(BASE_DIR, "influences")
ITEMS_DIR = os.path.join(BASE_DIR, "items")
SPELLS_DIR = os.path.join(BASE_DIR, "spells")

def calculate_average(num_list):
    if not num_list: return 0
    return sum(num_list) / len(num_list)

def ensure_stats_exist(chars):
    """
    Sanitizes character data.
    - Calculates Player HP/EP based on Level.
    - Pulls NPC HP/EP from 'combat' and 'ep' dicts.
    - FIX: If Current HP > Max HP, auto-correct Max HP.
    """
    print("\n--- SANITIZING STATS ---")
    for ch in chars:
        name = ch.get("name", "Unknown")
        
        # Ensure pools dict exists
        if "pools" not in ch:
            ch["pools"] = {}
        
        pools = ch["pools"]
        current_max_hp = pools.get("max_HP", 10)
        
        # --- CASE A: NPC (Explicit 'combat' and 'ep' stats) ---
        if "combat" in ch and "hp" in ch["combat"]:
            real_hp = ch["combat"]["hp"]
            real_ep = ch.get("ep", {}).get("max", 0) 
            
            pools["max_HP"] = real_hp
            pools["max_EP"] = real_ep
            
            # Heal to full if they were at default 10
            if pools.get("HP") == 10 and current_max_hp == 10:
                pools["HP"] = real_hp
            if pools.get("EP") == 10:
                pools["EP"] = real_ep

        # --- CASE B: PLAYER (Level-based calculation) ---
        elif "pools_profile" in ch and "level" in ch:
            level = ch["level"]
            profiles = ch["pools_profile"]
            
            hp_range = profiles.get("HP_per_level", [10])
            avg_hp = calculate_average(hp_range)
            calc_hp = int(avg_hp * level)
            
            ep_range = profiles.get("ENT_per_level", [10])
            avg_ep = calculate_average(ep_range)
            calc_ep = int(avg_ep * level)
            
            pools["max_HP"] = calc_hp
            pools["max_EP"] = calc_ep
            
            if pools.get("HP", 0) <= 10: pools["HP"] = calc_hp
            if pools.get("EP", 0) <= 10: pools["EP"] = calc_ep

        # --- FINAL SAFETY PASS ---
        if "max_HP" not in pools: pools["max_HP"] = 10
        if "max_EP" not in pools: pools["max_EP"] = 10
        if "HP" not in pools: pools["HP"] = pools["max_HP"]
        if "EP" not in pools: pools["EP"] = pools["max_EP"]

        # FIX: The "Beast" Patch
        # If the JSON loaded with HP 16 but Max HP 10, fix the Max.
        if pools["HP"] > pools["max_HP"]:
            # print(f"  [FIX] {name}: Adjusted Max HP ({pools['max_HP']} -> {pools['HP']})")
            pools["max_HP"] = pools["HP"]

        # Ensure Side exists
        if "side" not in ch:
            if ch.get("player", False) or str(ch.get("id", "")).startswith("player-"):
                ch["side"] = "players"
                ch["player"] = True
            else:
                ch["side"] = "raiders"

def main():
    """Main combat runner loop"""
    print("="*60)
    print("  TLE Combat Runner - Modular Edition (Smart Cast)")
    print("="*60)
    
    # Load libraries
    print("\nLoading libraries...")
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
    
    # Load characters
    chars = load_initiative()
    if not chars:
        print("\nNo characters found in ./initiative directory")
        return
    
    ensure_stats_exist(chars)
    print(f"\nLoaded {len(chars)} characters")
    
    init_social_flags(chars)
    
    print("\nEntering pre-flight setup...")
    if not preflight_setup(chars):
        print("Combat cancelled.")
        return
    
    had_players = any(c.get("side") == "players" for c in chars)
    max_rounds = 20
    
    for rnd in range(1, max_rounds + 1):
        print("\n" + "="*60)
        print(f"  ROUND {rnd}")
        print("="*60)
        
        # Check for new combatants
        new_chars = load_new_characters(chars)
        if new_chars:
            print(f"\n[JOIN] {len(new_chars)} new combatant(s) enter the fray!")
            ensure_stats_exist(new_chars)
            chars.extend(new_chars)
        
        order = rebuild_initiative(chars)
        ensure_stats_exist(chars)
        
        start_of_round_reactions(chars, libs)
        
        alive_sides = {c["side"] for c in chars if c["pools"]["HP"] > 0}
        
        if len(alive_sides) <= 1 and had_players:
            print("\n" + "="*60)
            if "players" in alive_sides:
                print("  VICTORY! Players win!")
            else:
                print("  DEFEAT! All players have fallen!")
            print("="*60)
            break
            
        if len(alive_sides) == 0:
            print("  DRAW! Everyone died.")
            break
        
        # Process turns
        for ch in order:
            if ch["pools"]["HP"] <= 0:
                continue
            
            if ch.get("player", False):
                handle_player_turn(ch, chars, libs)
            else:
                if not ch.get("ai_enabled", True):
                    print(f"\n{ch['name']} (AI disabled) takes no action.")
                else:
                    ai_take_turn(ch, chars, libs)
        
        chars = [c for c in chars if c["pools"]["HP"] > 0]
        save_back_vessels(chars)

    print("\nSession complete!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCombat interrupted by user.")
    except Exception as e:
        print(f"\n\nError during combat: {e}")
        import traceback
        traceback.print_exc()