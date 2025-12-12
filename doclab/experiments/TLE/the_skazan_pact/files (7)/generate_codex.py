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
                result[filename] = data
        except Exception as e:
            print(f"[WARN] Could not load {filepath}: {e}")
    
    return result


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
