"""
DDE-Pirouette: The Static Neuron (The Fundamental Unit)
-------------------------------------------------------
A single 'Cognitive Unit' that processes a concept through 4 distinct
'Dendrites' (Strategies) and stochastically selects an output based on resonance.

Dendrites:
1. NORTH (Logic): Finds the most resonant, grounded neighbor.
2. EAST (Dream): Finds a distant, creative association.
3. SOUTH (Memory): Finds a historically antecedent concept (heuristic: lower ID/older).
4. WEST (Critic): Finds a contrasting or distinct concept (low intersection but high rarity).

Usage:
    python wiki_static_neuron.py "Revolution"
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

def activate_neuron(input_concept):
    index = load_data()
    
    # 1. Resolve Input
    query_words = set(input_concept.lower().split())
    best_mid = None
    best_score = -1
    for mid, sig in index.items():
        score = len(set(sig).intersection(query_words))
        if score > best_score:
            best_score = score
            best_mid = mid
            
    if not best_mid:
        print("🌑 Neuron failed to fire: Input not recognized.")
        return

    current_sig = index[best_mid]
    clean_input = best_mid.replace("WIKI-", "")
    
    print(f"🧠 NEURON ACTIVATED: [{clean_input}]")
    print("   Processing Dendrites...")

    # 2. Calculate Dendrite Signals
    # We scan a subset of the brain for candidates
    sample_pool = random.sample(list(index.items()), min(500, len(index)))
    
    candidates_north = [] # Logic
    candidates_east = []  # Dream
    candidates_south = [] # Memory (Older IDs often have shorter/simpler names or lower indices in some systems, here we simulate by length/simplicity)
    candidates_west = []  # Critic
    
    for mid, sig in sample_pool:
        if mid == best_mid: continue
        
        res = get_resonance(current_sig, sig)
        if res == 0: continue
        
        # North: High Resonance
        candidates_north.append((mid, res))
        
        # East: Low but non-zero resonance (Creative)
        if res < 0.1:
            candidates_east.append((mid, res))
            
        # South: "Older" (Heuristic: Shorter titles often fundamental concepts)
        if len(mid) < len(best_mid):
            candidates_south.append((mid, res))
            
        # West: "Critic" (High Rarity words in common?)
        # Simulating contrast is hard, so we look for medium resonance but distinct domains
        if 0.1 < res < 0.3:
            candidates_west.append((mid, res))

    # 3. Weigh Signals
    # Strength of each dendrite = Average resonance of its top candidates
    def get_strength(cands):
        if not cands: return 0
        cands.sort(key=lambda x: x[1], reverse=True)
        top_3 = cands[:3]
        return sum(c[1] for c in top_3) / len(top_3)

    str_n = get_strength(candidates_north)
    str_e = get_strength(candidates_east)
    str_s = get_strength(candidates_south)
    str_w = get_strength(candidates_west)
    
    total_strength = str_n + str_e + str_s + str_w
    if total_strength == 0:
        print("   (Neuron Fizzled - No signal)")
        return

    # Normalize probabilities
    prob_n = str_n / total_strength
    prob_e = str_e / total_strength
    prob_s = str_s / total_strength
    prob_w = str_w / total_strength
    
    print(f"   [NORTH - Logic]  Signal: {prob_n:.3f}")
    print(f"   [EAST  - Dream]  Signal: {prob_e:.3f}")
    print(f"   [SOUTH - Memory] Signal: {prob_s:.3f}")
    print(f"   [WEST  - Critic] Signal: {prob_w:.3f}")
    
    # 4. Stochastic Fire (The Move)
    # This is the "Static" choice
    roll = random.random()
    
    if roll < prob_n:
        winner = "NORTH (Logic)"
        pool = candidates_north
    elif roll < prob_n + prob_e:
        winner = "EAST (Dream)"
        pool = candidates_east
    elif roll < prob_n + prob_e + prob_s:
        winner = "SOUTH (Memory)"
        pool = candidates_south
    else:
        winner = "WEST (Critic)"
        pool = candidates_west
        
    # Select specific concept from winning pool
    pool.sort(key=lambda x: x[1], reverse=True)
    # Top pick
    output_mid = pool[0][0]
    output_clean = output_mid.replace("WIKI-", "")
    
    print(f"\n⚡ FIRING: {winner}")
    print(f"   >>> OUTPUT: {output_clean}")
    
    # 5. Feedback Loop (Simulated)
    # If logic won, we reinforce logic slightly for next time (conceptually)
    print(f"   (Feedback: Reinforcing {winner} pathway...)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("concept", type=str)
    args = parser.parse_args()
    
    activate_neuron(args.concept)