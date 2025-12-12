"""
DDE-Pirouette: The Smart Neuron (Looping Seekers)
-------------------------------------------------
A 'Smart Neuron' that recursively fires, feeding its own output back
into its input to trace a 'Wound Channel' or coherent path through the corpus.

It seeks stability (repeating concepts) or a specific target state.

Usage:
    python wiki_loop_neuron.py "Chaos" --loops 10
"""

import sys
import json
import argparse
import os
import random
import time

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
INDEX_FILE = "wiki_resonance_index.json"

def load_data():
    if not os.path.exists(INDEX_FILE):
        print("❌ Missing Index.")
        sys.exit(1)
    with open(INDEX_FILE, 'r') as f:
        return json.load(f)["index"]

def get_resonance(signature_a, signature_b):
    set_a = set(signature_a)
    set_b = set(signature_b)
    if not set_a or not set_b: return 0
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    return intersection / union if union > 0 else 0

def run_smart_neuron(start_concept, loops=10):
    index = load_data()
    
    # 1. Initialize
    query_words = set(start_concept.lower().split())
    current_mid = None
    best_score = -1
    
    # Find entry point
    for mid, sig in index.items():
        score = len(set(sig).intersection(query_words))
        if score > best_score:
            best_score = score
            current_mid = mid
            
    if not current_mid:
        print("🌑 Input concept not found.")
        return

    print(f"🧠 SMART NEURON ONLINE: [{current_mid.replace('WIKI-', '')}]")
    print("   Tracing coherent path...")
    
    path_history = [current_mid]
    
    # 2. The Loop
    for i in range(loops):
        current_sig = index[current_mid]
        clean_current = current_mid.replace("WIKI-", "")
        
        print(f"\n🔄 CYCLE {i+1}: Processing '{clean_current}'...")
        
        # Scan for signals (Dendrites)
        # We scan a subset for speed, simulating 'attention'
        sample_pool = random.sample(list(index.items()), min(600, len(index)))
        
        candidates_logic = [] # High resonance
        candidates_assoc = [] # Medium resonance
        
        for mid, sig in sample_pool:
            if mid == current_mid: continue
            
            res = get_resonance(current_sig, sig)
            if res == 0: continue
            
            if res > 0.15:
                candidates_logic.append((mid, res))
            elif res > 0.05:
                candidates_assoc.append((mid, res))
        
        # Decision Logic (The 'Smart' part)
        # If we have strong logic options, prefer them (Stability)
        # If not, take an associative leap (exploration)
        
        next_mid = None
        decision_type = ""
        
        if candidates_logic:
            # Sort by resonance
            candidates_logic.sort(key=lambda x: x[1], reverse=True)
            # Pick top 1
            next_mid = candidates_logic[0][0]
            decision_type = "LOGIC (Coherence)"
        elif candidates_assoc:
            # Pick random from top 5
            candidates_assoc.sort(key=lambda x: x[1], reverse=True)
            top_assoc = candidates_assoc[:5]
            next_mid = random.choice(top_assoc)[0]
            decision_type = "ASSOC (Seeking)"
        else:
            print("   (Neuron stalled - no signals)")
            break
            
        # Loop Detection
        if next_mid in path_history:
            print(f"   ⚠️ Loop detected at '{next_mid.replace('WIKI-', '')}'. Breaking...")
            # Force a random jump to break loop? Or stop?
            # For a 'seeker', we might want to stop at stability.
            print(f"   ✨ STABILITY REACHED.")
            break
            
        print(f"   ⚡ ACTION: {decision_type}")
        print(f"   >>> MOVING TO: {next_mid.replace('WIKI-', '')}")
        
        current_mid = next_mid
        path_history.append(current_mid)
        time.sleep(0.1)

    print("\n📜 PATH TRACE:")
    for idx, node in enumerate(path_history):
        print(f"   {idx+1}. {node.replace('WIKI-', '')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("concept", type=str)
    parser.add_argument("--loops", type=int, default=10)
    args = parser.parse_args()
    
    run_smart_neuron(args.concept, args.loops)