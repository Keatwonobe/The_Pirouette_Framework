#!/usr/bin/env python3
"""
validate_codex.py - Validates codex.json structure and character data
Checks for common issues before loading into web runner.
"""

import json
import sys
from pathlib import Path


def validate_character(char_id, char_data, issues):
    """Validate a single character's data structure."""
    
    # Required fields
    required = ['name', 'side', 'stats']
    for field in required:
        if field not in char_data:
            issues.append(f"  ⚠ {char_id}: Missing '{field}' field")
    
    # Validate pools calculation
    if 'pools_profile' in char_data and 'level' in char_data:
        level = char_data['level']
        profile = char_data['pools_profile']
        
        # Check HP calculation
        if 'HP_per_level' in profile:
            hp_per_level = profile['HP_per_level']
            if isinstance(hp_per_level, list):
                avg_hp = sum(hp_per_level) / len(hp_per_level)
            else:
                avg_hp = hp_per_level
            
            expected_hp = int(avg_hp * level)
            
            if 'pools' in char_data and 'max_HP' in char_data['pools']:
                actual_hp = char_data['pools']['max_HP']
                if actual_hp != expected_hp:
                    issues.append(f"  ℹ {char_id}: HP mismatch - Expected {expected_hp} (lvl {level}), got {actual_hp}")
            else:
                issues.append(f"  ℹ {char_id}: No pools.max_HP - will calculate as {expected_hp}")
        
        # Check EP calculation
        if 'ENT_per_level' in profile:
            ep_per_level = profile['ENT_per_level']
            if isinstance(ep_per_level, list):
                avg_ep = sum(ep_per_level) / len(ep_per_level)
            else:
                avg_ep = ep_per_level
            
            expected_ep = int(avg_ep * level)
            
            if 'pools' in char_data and 'max_EP' in char_data['pools']:
                actual_ep = char_data['pools']['max_EP']
                if actual_ep != expected_ep:
                    issues.append(f"  ℹ {char_id}: EP mismatch - Expected {expected_ep} (lvl {level}), got {actual_ep}")
            else:
                issues.append(f"  ℹ {char_id}: No pools.max_EP - will calculate as {expected_ep}")
    
    # Validate pools exist
    if 'pools' not in char_data:
        issues.append(f"  ⚠ {char_id}: Missing 'pools' field")
    else:
        pools = char_data['pools']
        if 'HP' not in pools or 'max_HP' not in pools:
            issues.append(f"  ⚠ {char_id}: Missing HP or max_HP in pools")
        if 'EP' not in pools or 'max_EP' not in pools:
            issues.append(f"  ⚠ {char_id}: Missing EP or max_EP in pools")
        
        # Check HP/EP consistency
        if 'HP' in pools and 'max_HP' in pools:
            if pools['HP'] > pools['max_HP']:
                issues.append(f"  ℹ {char_id}: HP ({pools['HP']}) > max_HP ({pools['max_HP']}) - will auto-fix")
    
    # Validate stats
    if 'stats' in char_data:
        stats = char_data['stats']
        core_stats = ['str', 'dex', 'con', 'int', 'wis']
        missing_stats = [s for s in core_stats if s not in stats]
        if missing_stats:
            issues.append(f"  ⚠ {char_id}: Missing stats: {', '.join(missing_stats)}")
        
        if 'TEP' not in stats:
            issues.append(f"  ℹ {char_id}: Missing TEP (initiative stat) - will default to 10")
    
    # Check position
    if 'position' not in char_data:
        issues.append(f"  ℹ {char_id}: No position - will auto-assign based on side '{char_data.get('side', 'unknown')}'")
    
    # Check color
    if 'color' not in char_data:
        issues.append(f"  ℹ {char_id}: No color - will use side default")
    
    # Check side
    side = char_data.get('side', '')
    valid_sides = ['players', 'raiders', 'guards', 'neutral']
    if side not in valid_sides:
        issues.append(f"  ⚠ {char_id}: Unknown side '{side}' - valid: {', '.join(valid_sides)}")
    
    return issues


def validate_codex(codex_path):
    """Validate entire codex structure."""
    
    print("═══════════════════════════════════════")
    print("  TLE CODEX VALIDATOR")
    print("═══════════════════════════════════════\n")
    
    try:
        with open(codex_path, 'r') as f:
            codex = json.load(f)
    except FileNotFoundError:
        print(f"✗ Codex not found: {codex_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}")
        return False
    
    print(f"✓ Loaded: {codex_path}\n")
    
    # Check structure
    if 'directories' not in codex:
        print("✗ Missing 'directories' key in codex")
        return False
    
    directories = codex['directories']
    
    # Validate each directory
    all_issues = []
    stats = {}
    
    for dir_name, contents in directories.items():
        print(f"Checking {dir_name}/...")
        stats[dir_name] = len(contents)
        
        if dir_name == 'initiative':
            # Validate characters
            for char_id, char_data in contents.items():
                validate_character(char_id, char_data, all_issues)
        
        print(f"  ✓ {len(contents)} entries\n")
    
    # Print statistics
    print("═══ CODEX STATISTICS ═══")
    for dir_name, count in stats.items():
        print(f"  {dir_name}: {count} entries")
    
    # Count by side
    if 'initiative' in directories:
        by_side = {}
        for char_id, char_data in directories['initiative'].items():
            side = char_data.get('side', 'unknown')
            by_side[side] = by_side.get(side, 0) + 1
        
        print("\n═══ COMBATANTS BY SIDE ═══")
        for side, count in sorted(by_side.items()):
            print(f"  {side}: {count}")
    
    # Print issues
    if all_issues:
        print(f"\n═══ ISSUES FOUND ({len(all_issues)}) ═══")
        
        # Categorize
        warnings = [i for i in all_issues if '⚠' in i]
        infos = [i for i in all_issues if 'ℹ' in i]
        
        if warnings:
            print("\n⚠ WARNINGS (should fix):")
            for issue in warnings:
                print(issue)
        
        if infos:
            print("\nℹ INFO (auto-handled):")
            for issue in infos:
                print(issue)
        
        print(f"\n✓ Validation complete with {len(warnings)} warnings")
        return len(warnings) == 0
    else:
        print("\n✓ No issues found - codex is clean!")
        return True


def print_usage():
    print("Usage: python validate_codex.py [path/to/codex.json]")
    print("Default: ./codex.json")


if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        print_usage()
        sys.exit(0)
    
    codex_path = sys.argv[1] if len(sys.argv) > 1 else 'codex.json'
    
    valid = validate_codex(codex_path)
    
    if valid:
        print("\n═══════════════════════════════════════")
        print("Codex is ready for combat runner!")
        print("═══════════════════════════════════════\n")
        sys.exit(0)
    else:
        print("\n═══════════════════════════════════════")
        print("Please fix warnings before loading.")
        print("═══════════════════════════════════════\n")
        sys.exit(1)
