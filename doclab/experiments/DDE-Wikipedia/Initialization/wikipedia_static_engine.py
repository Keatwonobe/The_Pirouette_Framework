"""
DDE-Pirouette: The Static Engine (Resonant Navigator)
-----------------------------------------------------
A prototype 'Resonant LLM' that navigates the DDE Atlas.
It uses Zipfian probability to modulate its 'Static Field',
dynamically shifting between high-probability (Logic) and 
low-probability (Creative) jumps based on the rarity of its current thought.

Usage:
    python wiki_static_engine.py "Philosophy" --steps 15
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

def calculate_rarity(signature, semantic_index):
    """
    Estimates the 'Rarity' of a concept based on how often 
    its keywords appear in the global index.
    (A simple heuristic for Zipfian position).
    """
    # We just sample 100 random nodes to estimate global frequency
    sample_pool = random.sample(list(semantic_index.values()), min(100, len(semantic_index)))
    
    total_score = 0
    my_keywords = set(signature)
    
    for other_sig in sample_pool:
        overlap = len(my_keywords.intersection(set(other_sig)))
        total_score += overlap
        
    # Invert score: High overlap = Common (Low Rarity), Low overlap = Rare (High Rarity)
    # Normalized 0.0 to 1.0
    if total_score == 0: return 1.0
    rarity = 1.0 / (1.0 + (total_score * 0.1))
    return min(1.0, max(0.0, rarity))

def draw_static_field(candidates, chosen_idx):
    """Visualizes the probability field (The Static)."""
    # Limit to top 10 for display
    display_limit = min(10, len(candidates))
    print("\n   [STATIC FIELD MONITOR]")
    print("   ----------------------")
    
    for i in range(display_limit):
        mid, score = candidates[i]
        clean_id = mid.replace("WIKI-", "")
        
        # Visual bar
        bar_len = int(score * 20)
        bar = "█" * bar_len
        
        marker = "  "
        if i == chosen_idx:
            marker = "->"
            
        print(f"   {marker} {clean_id:<20} | {score:.3f} {bar}")
        
    if len(candidates) > display_limit:
        print(f"      ...and {len(candidates)-display_limit} faint signals...")

def run_static_engine(start_query, steps=10):
    semantic_index = load_data()
    
    # 1. Boot Sequence
    print(f"🔮 STATIC ENGINE ONLINE")
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
    
    # 2. The Loop
    for step in range(steps):
        clean_id = current_node.replace("WIKI-", "")
        signature = semantic_index.get(current_node, [])
        
        # A. Calculate Rarity (Zipf Position)
        rarity = calculate_rarity(signature, semantic_index)
        
        # B. Determine Static Pressure (Dynamic Temperature)
        # If concept is RARE -> Seek GROUNDING (Low Temp)
        # If concept is COMMON -> Seek NOVELTY (High Temp)
        temperature = 1.0 - rarity 
        
        print(f"\n🔹 STEP {step+1}: {clean_id}")
        print(f"   Rarity: {rarity:.2f} | Static Temp: {temperature:.2f}")
        
        # C. Scan for Resonance
        candidates = []
        sample_keys = random.sample(list(semantic_index.keys()), min(500, len(semantic_index)))
        
        for cand_mid in sample_keys:
            if cand_mid == current_node or cand_mid in path: continue
            cand_sig = semantic_index[cand_mid]
            res = get_resonance(signature, cand_sig)
            if res > 0:
                candidates.append((cand_mid, res))
                
        if not candidates:
            print("   (Signal lost)")
            break
            
        # Sort by resonance
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # D. The Selection (Sampling the Static)
        # We use the calculated temperature to pick an index
        if temperature < 0.3:
            # Logical/Grounded Choice (Top 1)
            chosen_idx = 0
            mode = "LOGIC"
        elif temperature < 0.7:
            # Associative Choice (Top 20%)
            limit = max(1, int(len(candidates) * 0.2))
            chosen_idx = random.randint(0, limit)
            mode = "ASSOC"
        else:
            # Creative/Dream Choice (Top 50%)
            limit = max(1, int(len(candidates) * 0.5))
            chosen_idx = random.randint(0, limit)
            mode = "DREAM"
            
        # Visualize BEFORE moving
        draw_static_field(candidates, chosen_idx)
        
        print(f"   >>> {mode} JUMP (idx {chosen_idx}) >>>")
        
        current_node = candidates[chosen_idx][0]
        path.append(current_node)
        
        # Simulate "processing time"
        time.sleep(0.5)

    print("\n✨ SEQUENCE COMPLETE")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str)
    parser.add_argument("--steps", type=int, default=10)
    args = parser.parse_args()
    
    run_static_engine(args.query, args.steps)