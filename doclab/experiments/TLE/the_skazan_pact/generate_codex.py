#!/usr/bin/env python3
"""
generate_codex.py - Creates codex.json for web combat runner
Scans initiative/, spells/, items/, axes/, influences/ directories
and bundles them into a single codex.json file for web loading.
"""

import os
import json
from pathlib import Path


def load_json_from_dir(directory):
    """Load all JSON files from a directory into a dict keyed by filename."""
    result = {}
    
    if not os.path.isdir(directory):
        return result
    
    for filename in os.listdir(directory):
        if not filename.endswith('.json'):
            continue
        
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
                # Pre-calculate HP/EP for characters
                if directory.endswith('initiative'):
                    data = calculate_character_pools(data)
                
                result[filename] = data
        except Exception as e:
            print(f"[WARN] Could not load {filepath}: {e}")
    
    return result


def calculate_character_pools(char_data):
    """
    Calculate total HP/EP from per-level values and character level.
    This ensures web runner shows correct values.
    """
    if 'pools_profile' not in char_data or 'level' not in char_data:
        return char_data
    
    level = char_data['level']
    profile = char_data['pools_profile']
    
    # Calculate HP
    if 'HP_per_level' in profile:
        hp_per_level = profile['HP_per_level']
        if isinstance(hp_per_level, list):
            avg_hp = sum(hp_per_level) / len(hp_per_level)
        else:
            avg_hp = hp_per_level
        
        total_hp = int(avg_hp * level)
        
        # Set in pools
        if 'pools' not in char_data:
            char_data['pools'] = {}
        char_data['pools']['max_HP'] = total_hp
        char_data['pools']['HP'] = char_data['pools'].get('HP', total_hp)
    
    # Calculate EP
    if 'ENT_per_level' in profile:
        ep_per_level = profile['ENT_per_level']
        if isinstance(ep_per_level, list):
            avg_ep = sum(ep_per_level) / len(ep_per_level)
        else:
            avg_ep = ep_per_level
        
        total_ep = int(avg_ep * level)
        
        # Set in pools
        if 'pools' not in char_data:
            char_data['pools'] = {}
        char_data['pools']['max_EP'] = total_ep
        char_data['pools']['EP'] = char_data['pools'].get('EP', total_ep)
    
    # Also check NPC format (combat.hp and ep.max)
    if 'combat' in char_data and 'hp' in char_data['combat']:
        if 'pools' not in char_data:
            char_data['pools'] = {}
        char_data['pools']['max_HP'] = char_data['combat']['hp']
        char_data['pools']['HP'] = char_data['pools'].get('HP', char_data['combat']['hp'])
    
    if 'ep' in char_data and 'max' in char_data['ep']:
        if 'pools' not in char_data:
            char_data['pools'] = {}
        char_data['pools']['max_EP'] = char_data['ep']['max']
        char_data['pools']['EP'] = char_data['pools'].get('EP', char_data['ep']['max'])
    
    return char_data


def generate_codex(base_dir='.'):
    """Generate codex.json from directory structure."""
    
    print("═══════════════════════════════════════")
    print("  TLE CODEX GENERATOR")
    print("═══════════════════════════════════════\n")
    
    codex = {
        "version": "3.1",
        "generated_by": "generate_codex.py",
        "description": "TLE Combat Runner Codex Bundle",
        "directories": {}
    }
    
    # Define directories to scan
    dirs_to_scan = {
        'initiative': os.path.join(base_dir, 'initiative'),
        'spells': os.path.join(base_dir, 'spells'),
        'items': os.path.join(base_dir, 'items'),
        'axes': os.path.join(base_dir, 'axes'),
        'influences': os.path.join(base_dir, 'influences')
    }
    
    total_files = 0
    
    for dir_name, dir_path in dirs_to_scan.items():
        print(f"Scanning {dir_name}/...")
        data = load_json_from_dir(dir_path)
        
        if data:
            codex['directories'][dir_name] = data
            print(f"  ✓ Loaded {len(data)} files")
            total_files += len(data)
        else:
            print(f"  ⚠ Directory not found or empty")
    
    # Write codex
    output_path = os.path.join(base_dir, 'codex.json')
    
    try:
        with open(output_path, 'w') as f:
            json.dump(codex, f, indent=2)
        
        print(f"\n✓ Codex generated: {output_path}")
        print(f"  Total files: {total_files}")
        
        # Print summary by category
        print("\n═══ CODEX SUMMARY ═══")
        for dir_name, contents in codex['directories'].items():
            print(f"  {dir_name}: {len(contents)} entries")
        
        print("\n═══════════════════════════════════════")
        print("Place codex.json in the same directory")
        print("as tle_combat_runner.html to auto-load.")
        print("═══════════════════════════════════════\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error writing codex: {e}")
        return False


if __name__ == '__main__':
    import sys
    
    # Allow specifying base directory
    base_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"Base directory: {os.path.abspath(base_dir)}\n")
    
    success = generate_codex(base_dir)
    sys.exit(0 if success else 1)
