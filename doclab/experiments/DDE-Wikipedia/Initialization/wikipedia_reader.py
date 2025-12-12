"""
DDE-Pirouette: Wikipedia Reader (The Astronomer)
------------------------------------------------
Completes the cycle. Takes a physical coordinate (from the Constellation)
and decodes the Semantic DNA (Title + Keywords) stored there.

Usage:
    python wiki_reader.py 41 13
"""

import sys
import json
import argparse
import os

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
INDEX_FILE = "wiki_resonance_index.json"
ATLAS_MAP = "wiki_atlas_map.json"

def load_data():
    if not os.path.exists(INDEX_FILE) or not os.path.exists(ATLAS_MAP):
        print("❌ Missing Index or Map.")
        sys.exit(1)
        
    print("   📖 Loading Codex...")
    with open(INDEX_FILE, 'r') as f:
        semantic_index = json.load(f)["index"]
    with open(ATLAS_MAP, 'r') as f:
        physical_map = json.load(f)["tiles"]
        
    return semantic_index, physical_map

def read_star(target_x, target_y):
    semantic_index, physical_map = load_data()
    
    print(f"\n🔭 TELESCOPE FOCUSED ON: ({target_x}, {target_y})")
    
    # 1. Reverse Search the Map (Coords -> ID)
    found_tile = None
    found_filename = None
    
    for filename, info in physical_map.items():
        if info['x'] == target_x and info['y'] == target_y:
            found_tile = info
            found_filename = filename
            break
            
    if not found_tile:
        print("   🌑 Void. No data exists at these coordinates.")
        return

    # 2. Extract Identity
    article_id = found_tile['id'] # "Title"
    mid = f"WIKI-{article_id}" # "WIKI-Title"
    
    print(f"   ✨ IDENTITY CONFIRMED: {article_id}")
    print(f"      File: {found_filename}")
    print(f"      Index: {found_tile['idx']}")

    # 3. Decode Semantic DNA (ID -> Signature)
    if mid in semantic_index:
        signature = semantic_index[mid]
        
        print("\n🧬 SEMANTIC DNA (The 'Why'):")
        print("   The DDE placed this here because it resonates with:")
        print("   ------------------------------------------------")
        
        # Format nicely
        sig_str = ", ".join(signature[:20])
        print(f"   {sig_str}...")
        
        print("\n   (This is the 'Prompt Context' you would feed an LLM)")
    else:
        print("\n   ⚠️ No semantic signature found in index (Sync error?)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("x", type=int, help="X Coordinate")
    parser.add_argument("y", type=int, help="Y Coordinate")
    args = parser.parse_args()
    
    read_star(args.x, args.y)