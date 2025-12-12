"""
DDE-Pirouette: Dynamic Walker (The Data Dancer)
-----------------------------------------------
A Resonant Engine that oscillates its temperature over time.
It forces the narrative to move from Logic -> Dream -> Logic,
attempting to synthesize disparate concepts into a single train of thought.

Usage:
    python wiki_dynamic_walker.py "Philosophy" --steps 12
"""

import sys
import json
import argparse
import os
import random
import math
import time

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
    return semantic_index

def get_resonance(signature_a, signature_b):
    set_a = set(signature_a)
    set_b = set(signature_b)
    if not set_a or not set_b: return 0
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    if union == 0: return 0
    return intersection / union

def get_dynamic_temperature(step, total_steps):
    """
    Generates a Sine Wave temperature profile.
    Starts Low (Logic), Peaks High (Dream), Ends Low (Logic).
    """
    # Normalized progress (0.0 to 1.0)
    progress = step / total_steps
    
    # Sine wave from 0 to PI (0 -> 1 -> 0)
    # We scale it so base is 0.1 and peak is 0.95
    wave = math.sin(progress * math.pi)
    temp = 0.1 + (wave * 0.85)
    return temp

def draw_static_field(candidates, chosen_idx, temp):
    """Visualizes the field and the chosen jump."""
    display_limit = min(5, len(candidates))
    print(f"\n   [STATIC FIELD | Temp: {temp:.2f}]")
    
    for i in range(display_limit):
        mid, score = candidates[i]
        clean_id = mid.replace("WIKI-", "")
        bar = "█" * int(score * 20)
        
        marker = "  "
        if i == chosen_idx:
            marker = "->"
        print(f"   {marker} {clean_id:<20} | {score:.3f} {bar}")

def run_dynamic_walk(start_query, steps=12):
    semantic_index = load_data()
    
    print(f"💃 DYNAMIC WALKER ONLINE")
    print(f"   Seed: '{start_query}'")
    
    # Find Start
    query_words = set(start_query.lower().split())
    best_start = None
    best_score = -1
    for mid, sig in semantic_index.items():
        score = len(set(sig).intersection(query_words))
        if score > best_score:
            best_score = score
            best_start = mid
            
    if not best_start:
        print("   🌑 Seed not found.")
        return

    current_node = best_start
    path = [current_node]
    
    print("\n--- BEGIN DANCE ---")
    
    for step in range(steps):
        clean_id = current_node.replace("WIKI-", "")
        signature = semantic_index.get(current_node, [])
        
        # 1. Calculate Dynamic Temperature
        temperature = get_dynamic_temperature(step, steps)
        
        print(f"\n🔹 STEP {step+1}: {clean_id}")
        
        # 2. Scan Resonance
        candidates = []
        sample_keys = random.sample(list(semantic_index.keys()), min(800, len(semantic_index)))
        
        for cand_mid in sample_keys:
            if cand_mid == current_node or cand_mid in path: continue
            cand_sig = semantic_index[cand_mid]
            res = get_resonance(signature, cand_sig)
            if res > 0:
                candidates.append((cand_mid, res))
                
        if not candidates:
            print("   (Signal lost)")
            break
            
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # 3. The Selection (Temperature Modulated)
        if temperature < 0.3:
            # Logic Phase (Top 1)
            chosen_idx = 0
            mode = "LOGIC (Grounding)"
        elif temperature < 0.7:
            # Bridge Phase (Top 15%)
            limit = max(1, int(len(candidates) * 0.15))
            chosen_idx = random.randint(0, limit)
            mode = "BRIDGE (Expanding)"
        else:
            # Dream Phase (Deep Field)
            limit = max(1, int(len(candidates) * 0.6))
            # Bias slightly away from 0 to force a jump
            chosen_idx = random.randint(int(limit*0.2), limit)
            mode = "DREAM (Leaping)"
            
        draw_static_field(candidates, chosen_idx, temperature)
        print(f"   >>> {mode} >>>")
        
        current_node = candidates[chosen_idx][0]
        path.append(current_node)
        time.sleep(0.2)

    print("\n✨ DANCE COMPLETE")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str)
    parser.add_argument("--steps", type=int, default=12)
    args = parser.parse_args()
    
    run_dynamic_walk(args.query, args.steps)