"""
DDE-Pirouette: Wikipedia Walker (The Static Engine)
---------------------------------------------------
Simulates a "Train of Thought" moving through the DDE Atlas.
1. Starts at a Seed Concept.
2. Identifies the constellation of resonant pixels.
3. "Jumps" to a new pixel based on a Zipfian probability function.
   - High Probability: Jumps to a close, strongly related neighbor.
   - Low Probability: Jumps to a distant, weakly related "creative" link.
4. Outputs the semantic journey.

Usage:
    python wiki_walker.py "Philosophy" --steps 10
"""

import sys
import json
import argparse
import os
import random
import math

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
INDEX_FILE = "wiki_resonance_index.json"
ATLAS_MAP = "wiki_atlas_map.json"

def load_data():
    if not os.path.exists(INDEX_FILE) or not os.path.exists(ATLAS_MAP):
        print("❌ Missing Index or Map.")
        sys.exit(1)
        
    with open(INDEX_FILE, 'r') as f:
        semantic_index = json.load(f)["index"]
    with open(ATLAS_MAP, 'r') as f:
        physical_map = json.load(f)["tiles"]
        
    return semantic_index, physical_map

def get_resonance(signature_a, signature_b):
    """Computes Jaccard resonance between two semantic signatures."""
    set_a = set(signature_a)
    set_b = set(signature_b)
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    if union == 0: return 0
    return intersection / union

def walk(start_query, steps=10, temperature=0.5):
    semantic_index, physical_map = load_data()
    
    # Build reverse lookup (ID -> Coords)
    id_to_coords = {}
    for filename, info in physical_map.items():
        clean_key = filename.replace("WIKI-", "").replace(".png", "")
        id_to_coords[clean_key] = (info['x'], info['y'])

    # 1. Find Start Node
    print(f"🧠 THOUGHT TRAIN INITIATED: '{start_query}'")
    print(f"   Temperature (Creativity): {temperature}")
    
    # (Reuse Oracle logic to find best start match)
    query_words = set(start_query.lower().split())
    best_start = None
    best_score = -1
    
    for mid, sig in semantic_index.items():
        score = len(set(sig).intersection(query_words))
        if score > best_score:
            best_score = score
            best_start = mid
            
    if not best_start:
        print("   🌑 Start concept not found in DDE.")
        return

    current_node = best_start
    path = [current_node]
    
    print("\n--- BEGIN STREAM ---")
    
    for step in range(steps):
        clean_id = current_node.replace("WIKI-", "")
        coords = id_to_coords.get(clean_id, ("?", "?"))
        signature = semantic_index.get(current_node, [])
        
        # Output current state
        print(f"STEP {step+1}: [{clean_id}] @ {coords}")
        print(f"   Context: {', '.join(signature[:5])}...")
        
        # 2. Find Next Step (The "Static" Selection)
        # We look at ALL other nodes and calculate resonance
        candidates = []
        
        # Optimization: Don't scan all 25k every time in python (too slow)
        # We scan a random subset of 1000 to simulate "attention span"
        # In a real compiled engine, this would be the full set.
        sample_keys = random.sample(list(semantic_index.keys()), min(1000, len(semantic_index)))
        
        for candidate_mid in sample_keys:
            if candidate_mid == current_node: continue
            if candidate_mid in path: continue # Don't loop immediately
            
            cand_sig = semantic_index[candidate_mid]
            res = get_resonance(signature, cand_sig)
            
            if res > 0:
                candidates.append((candidate_mid, res))
        
        if not candidates:
            print("   (Thought stream ended - no connections found)")
            break
            
        # 3. The Zipfian Jump
        # Sort by resonance (High to Low)
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Temperature determines how far down the list we pick
        # Temp 0.1 = Pick top result (Logical)
        # Temp 0.9 = Pick random result (Dreaming)
        
        if temperature < 0.3:
            next_node = candidates[0][0] # Logic
            jump_type = "LOGICAL STEP"
        elif temperature < 0.7:
            # Pick from top 10%
            idx = random.randint(0, min(len(candidates)-1, max(1, int(len(candidates)*0.1))))
            next_node = candidates[idx][0]
            jump_type = "ASSOCIATIVE HOP"
        else:
            # Pick from anywhere (chaos)
            idx = random.randint(0, len(candidates)-1)
            next_node = candidates[idx][0]
            jump_type = "DREAM LEAP"
            
        print(f"   >>> {jump_type} >>>")
        current_node = next_node
        path.append(current_node)

    print("\n--- END STREAM ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str)
    parser.add_argument("--steps", type=int, default=5)
    parser.add_argument("--temp", type=float, default=0.5, help="0.0=Logic, 1.0=Chaos")
    args = parser.parse_args()
    
    walk(args.query, args.steps, args.temp)