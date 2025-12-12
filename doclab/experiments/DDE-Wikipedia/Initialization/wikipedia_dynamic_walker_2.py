"""
DDE-Pirouette: Dynamic Walker v2.0 (Personality Modes)
------------------------------------------------------
A Resonant Engine with distinct 'Personality Profiles'.

Modes:
1. THE DANCER (Sine Wave): Logic -> Dream -> Logic
2. THE EXPERIMENTALIST: Logic -> ONE DREAM LEAP -> Logic
3. THE PROPHET: Dream -> Latch on High Resonance -> Logic

Usage:
    python wiki_dynamic_walker.py "Philosophy" --mode prophet
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
    # Quick rarity heuristic (inverse of commonality)
    # We sample a subset to be fast
    sample_pool = random.sample(list(semantic_index.values()), min(50, len(semantic_index)))
    total_score = 0
    my_keywords = set(signature)
    for other_sig in sample_pool:
        overlap = len(my_keywords.intersection(set(other_sig)))
        total_score += overlap
    if total_score == 0: return 1.0
    rarity = 1.0 / (1.0 + (total_score * 0.2))
    return min(1.0, max(0.0, rarity))

def draw_static_field(candidates, chosen_idx, temp, mode_name):
    display_limit = min(5, len(candidates))
    print(f"\n   [STATIC FIELD | Temp: {temp:.2f} | {mode_name}]")
    
    for i in range(display_limit):
        mid, score = candidates[i]
        clean_id = mid.replace("WIKI-", "")
        bar = "█" * int(score * 20)
        marker = "  "
        if i == chosen_idx: marker = "->"
        print(f"   {marker} {clean_id:<20} | {score:.3f} {bar}")

# ---------------------------------------------------------------------------
# PERSONALITY LOGIC
# ---------------------------------------------------------------------------

def get_temp_dancer(step, total_steps):
    # Sine Wave: 0.1 -> 0.95 -> 0.1
    progress = step / total_steps
    wave = math.sin(progress * math.pi)
    return 0.1 + (wave * 0.85)

def get_temp_experimentalist(step, total_steps):
    # Flatline Logic (0.1) with ONE SPIKE at 50% mark
    midpoint = total_steps // 2
    if step == midpoint:
        return 0.95 # The Experiment
    return 0.1 # The Control

def get_temp_prophet(current_rarity, is_latched):
    # Chaos (0.9) until Rare Truth found, then Logic (0.1)
    if is_latched:
        return 0.1
    
    # Trigger Condition: If concept is very rare/profound (>0.8)
    if current_rarity > 0.85:
        return "LATCH" # Special signal
        
    return 0.9

def run_dynamic_walk(start_query, steps=12, mode="dancer"):
    semantic_index = load_data()
    
    print(f"🎭 DYNAMIC WALKER ONLINE")
    print(f"   Mode: {mode.upper()}")
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
    prophet_latched = False
    
    print("\n--- BEGIN WALK ---")
    
    for step in range(steps):
        clean_id = current_node.replace("WIKI-", "")
        signature = semantic_index.get(current_node, [])
        rarity = calculate_rarity(signature, semantic_index)
        
        # 1. Determine Temperature based on Personality
        if mode == "dancer":
            temp = get_temp_dancer(step, steps)
        elif mode == "experimentalist":
            temp = get_temp_experimentalist(step, steps)
        elif mode == "prophet":
            val = get_temp_prophet(rarity, prophet_latched)
            if val == "LATCH":
                print(f"\n   👁️  PROPHET HAS SEEN THE TRUTH! (Rarity: {rarity:.2f})")
                print("      Latching onto this concept...")
                prophet_latched = True
                temp = 0.1
            else:
                temp = val
        else:
            temp = 0.5 # Default flat
            
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
        
        # 3. The Selection
        if temp < 0.3:
            chosen_idx = 0
            action = "LOGIC"
        elif temp < 0.7:
            limit = max(1, int(len(candidates) * 0.2))
            chosen_idx = random.randint(0, limit)
            action = "BRIDGE"
        else:
            limit = max(1, int(len(candidates) * 0.6))
            chosen_idx = random.randint(int(limit*0.2), limit)
            action = "DREAM"
            
        draw_static_field(candidates, chosen_idx, temp, action)
        print(f"   >>> {action} >>>")
        
        current_node = candidates[chosen_idx][0]
        path.append(current_node)
        time.sleep(0.2)

    print("\n✨ WALK COMPLETE")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str)
    parser.add_argument("--steps", type=int, default=12)
    parser.add_argument("--mode", type=str, default="dancer", choices=["dancer", "experimentalist", "prophet"])
    args = parser.parse_args()
    
    run_dynamic_walk(args.query, args.steps, args.mode)