#!/usr/bin/env python3
"""
player_interface.py - Handle player turns and CLI commands
"""

from utils import parse_index_tokens, distance_2d
from character_state import print_state
from social_system import conversation_check, set_stance, set_hostility
from check_system import handle_check_command
from dice_buy import handle_dice_buy_attack, parse_dice_buy_command, explain_dice_buy_options
from spellcasting import resolve_spell_cast, handle_split_cast, explain_spellcasting, calculate_spell_range_cost
from damage_system import route_damage_to_wounds
from influence_system import resolve_item_use


def handle_player_turn(character, all_chars, libs):
    """
    Handle a player character's turn with CLI interface.
    """
    print(f"\n{'='*60}")
    print(f"  {character['name']}'s TURN")
    print(f"  HP: {character['pools']['HP']}/{character['pools']['max_HP']} | "
          f"EP: {character['pools']['EP']}/{character['pools']['max_EP']}")
    print(f"{'='*60}")
    
    # Show nearby enemies
    print("\nTargets:")
    for i, ch in enumerate(all_chars, 1):
        if ch["pools"]["HP"] <= 0:
            continue
        if ch is character:
            continue
        
        hp = ch["pools"]["HP"]
        max_hp = ch["pools"]["max_HP"]
        side = ch.get("side", "?")
        
        print(f"  [{i}] {ch['name']:<20} | {side:<10} | HP {hp}/{max_hp}")
    
    print("\nCommands:")
    print("  attack <target> spend <ep>              - Standard Attack")
    print("  cast <spell> <target> [power <ep>]      - Cast Spell (Auto-range)")
    print("  check <target>.<field>                  - Skill Check")
    print("  move <x> <y>                            - Move")
    print("  pass                                    - End Turn")
    print()
    
    while True:
        try:
            cmd = input(f"{character['name']}> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSkipping turn.")
            return
        
        if not cmd:
            continue
        
        parts = cmd.split()
        op = parts[0].lower()
        
        # === HELP COMMANDS ===
        if op == "help":
            if len(parts) > 1:
                topic = parts[1].lower()
                if topic in ("dice", "buy"):
                    explain_dice_buy_options()
                elif topic in ("spell", "spells", "cast"):
                    explain_spellcasting()
            else:
                print("Available commands: attack, cast, check, use, move, pass, look")
            continue
        
        # === END TURN ===
        if op in ("pass", "skip", "done", "end"):
            print(f"{character['name']} ends turn.")
            return
        
        # === LOOK ===
        if op == "look":
            print_state(all_chars)
            continue
        
        # === ATTACK ===
        if op == "attack":
            parsed = parse_dice_buy_command(parts)
            if not parsed:
                print("Usage: attack <target> spend <base_ep> [buy <buy_ep>]")
                continue
            
            target_idx, base_ep, buy_ep = parsed
            
            if target_idx < 0 or target_idx >= len(all_chars):
                print("Invalid target index")
                continue
            
            target = all_chars[target_idx]
            
            if target["pools"]["HP"] <= 0:
                print("Target is already defeated")
                continue
            
            # Check EP
            total_ep = base_ep + buy_ep
            if character["pools"]["EP"] < total_ep:
                print(f"Insufficient EP! Need {total_ep}, have {character['pools']['EP']}")
                continue
            
            # Execute attack
            handle_dice_buy_attack(character, target, base_ep, buy_ep, libs)
            character["pools"]["EP"] -= total_ep
            return
        
        # === CHECK ===
        if op == "check":
            handle_check_command(parts, character, all_chars)
            continue
        
        # === CAST (SIMPLIFIED) ===
        if op == "cast":
            if len(parts) < 3:
                print("Usage: cast <spell> <target> [power <ep>]")
                continue
            
            spell_id = parts[1]
            spell_card = libs.get("spells", {}).get(spell_id, {})
            
            try:
                target_idx = int(parts[2]) - 1
            except ValueError:
                print("Invalid target index")
                continue
            
            if target_idx < 0 or target_idx >= len(all_chars):
                print("Invalid target index")
                continue
            
            target = all_chars[target_idx]
            
            # Auto-Calculate Range Cost
            dist = distance_2d(character.get("position", {}), target.get("position", {}))
            range_ep = calculate_spell_range_cost(dist)
            
            # Determine Damage/Power Cost
            damage_ep = spell_card.get("base_cost", 1) 
            
            if "power" in parts:
                try:
                    p_idx = parts.index("power")
                    damage_ep = int(parts[p_idx+1])
                except (ValueError, IndexError):
                    print("Invalid power value.")
                    continue
            elif "spend" in parts:
                 try:
                    s_idx = parts.index("spend")
                    damage_ep = int(parts[s_idx+1])
                 except: pass

            total_ep = damage_ep + range_ep
            
            print(f"  [CASTING] {spell_id} -> {target['name']}")
            print(f"  Range: {dist:.1f} ft ({range_ep} EP)")
            print(f"  Power: {damage_ep} EP")
            print(f"  Total Cost: {total_ep} EP")
            
            if character["pools"]["EP"] < total_ep:
                print(f"  [FAIL] Insufficient EP! Need {total_ep}, Have {character['pools']['EP']}")
                continue
            
            result = resolve_spell_cast(
                character, target, spell_id,
                damage_ep, range_ep, libs, mode="auto"
            )
            
            if result.get("success"):
                log = []
                route_damage_to_wounds(target, result["damage"], "arcane", log)
                for line in log:
                    print(f"  {line}")
                character["pools"]["EP"] -= total_ep
                return
            else:
                character["pools"]["EP"] -= total_ep
                return
        
        # === USE ITEM ===
        if op == "use":
            if len(parts) < 2:
                print("Usage: use <item> [on <target>]")
                continue
            
            item_id = parts[1]
            target = character
            if "on" in parts:
                on_idx = parts.index("on")
                if on_idx + 1 < len(parts):
                    try:
                        target_idx = int(parts[on_idx + 1]) - 1
                        if 0 <= target_idx < len(all_chars):
                            target = all_chars[target_idx]
                    except ValueError:
                        pass
            
            result = resolve_item_use(character, item_id, target, libs)
            if result["success"]:
                for line in result["log"]:
                    print(f"  {line}")
                return
            else:
                print(f"Cannot use item: {result['reason']}")
                continue
        
        # === TALK ===
        if op == "talk":
            if len(parts) < 2:
                print("Usage: talk <target> [stat]")
                continue
            try:
                target_idx = int(parts[1]) - 1
                target = all_chars[target_idx]
                stat = parts[2] if len(parts) > 2 else "wis"
                conversation_check(character, target, stat=stat, mode="auto")
                return
            except:
                print("Invalid target.")
                continue
        
        # === MOVE ===
        if op == "move":
            try:
                x = float(parts[1])
                y = float(parts[2])
                character["position"] = {"x": x, "y": y}
                print(f"{character['name']} moves to ({x}, {y})")
                return
            except:
                print("Usage: move <x> <y>")
                continue
        
        print("Unknown command. Type 'help' for available commands.")


def preflight_setup(chars):
    """
    Pre-combat setup phase for GM to configure battlefield.
    """
    while True:
        print("\n" + "="*60)
        print("  PRE-FLIGHT SETUP")
        print("="*60)
        print("  start / go              - Begin combat")
        print("  look                    - View battlefield")
        print("  ai on|off <idx>         - Toggle AI")
        print("  mode <idx> <type>       - Set stance (combat/talk/neutral)")
        print("  side <idx> <team>       - Set team (players/raiders)")
        print("  hostility <idx> <val>   - Set hostility (hostile/friendly/neutral)")
        
        cmd = input("setup> ").strip()
        if not cmd: continue
        
        parts = cmd.split()
        op = parts[0].lower()
        
        if op in ("start", "go", "run"): return True
        if op in ("q", "quit", "exit"): return False
        
        if op == "look":
            print_state(chars)
            continue
            
        if op == "ai":
             try:
                mode = parts[1]
                indices = parse_index_tokens(parts[2:], len(chars))
                for i in indices:
                    chars[i]["ai_enabled"] = (mode == "on")
                    print(f"AI {mode} for {chars[i]['name']}")
             except: print("Usage: ai on <idx>")
             continue

        if op == "mode":
             try:
                indices = parse_index_tokens(parts[1:-1], len(chars))
                mode = parts[-1]
                for i in indices:
                    set_stance(chars[i], mode)
             except: print("Usage: mode <idx> <combat/neutral>")
             continue
             
        # === SIDE COMMAND (FIXED) ===
        if op == "side":
            try:
                # Format: side 25-31 players
                team = parts[-1]
                indices = parse_index_tokens(parts[1:-1], len(chars))
                
                if not indices:
                    print("No valid indices found.")
                    continue
                    
                for i in indices:
                    chars[i]["side"] = team
                    # Optional: Auto-set friendly if players, hostile if raiders
                    if team == "players":
                        chars[i]["hostility"] = "friendly"
                        chars[i]["ai_enabled"] = False # Assume manual unless AI toggled back on
                    elif team == "raiders":
                        chars[i]["hostility"] = "hostile"
                        chars[i]["ai_enabled"] = True
                    print(f"Set {chars[i]['name']} to side '{team}'")
            except Exception as e:
                print(f"Error setting side: {e}")
                print("Usage: side <idx> <team_name>")
            continue

        if op == "hostility":
             try:
                indices = parse_index_tokens(parts[1:-1], len(chars))
                val = parts[-1]
                for i in indices:
                    set_hostility(chars[i], val)
             except: print("Usage: hostility <idx> <hostile/friendly>")
             continue