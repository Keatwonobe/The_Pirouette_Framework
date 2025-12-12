"""
DDE-Pirouette: Semantic Bridge Builder
--------------------------------------
Attempts to find a 'Semantic Path' between two disparate concepts.
Uses a Bi-Directional Search strategy (meet-in-the-middle).

Usage:
    python wiki_bridge_builder.py "Quantum mechanics" "General relativity"
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

def find_closest_node(query, index):
    query_words = set(query.lower().split())
    best_mid = None
    best_score = -1
    for mid, sig in index.items():
        score = len(set(sig).intersection(query_words))
        if score > best_score:
            best_score = score
            best_mid = mid
    return best_mid

def build_bridge(start_query, end_query, max_depth=10):
    index = load_data()
    
    print(f"🌉 BRIDGE BUILDER ONLINE")
    print(f"   From: '{start_query}'")
    print(f"   To:   '{end_query}'")
    
    start_node = find_closest_node(start_query, index)
    end_node = find_closest_node(end_query, index)
    
    if not start_node or not end_node:
        print("   🌑 Could not anchor bridge endpoints.")
        return

    print(f"   Anchors: {start_node.replace('WIKI-', '')} <---> {end_node.replace('WIKI-', '')}")
    
    # Frontiers
    front_a = {start_node}
    front_b = {end_node}
    
    visited_a = {start_node: [start_node]} # Node -> Path to get there
    visited_b = {end_node: [end_node]}
    
    print("\n--- CONSTRUCTION STARTED ---")
    
    for depth in range(max_depth):
        print(f"   Layer {depth+1}...")
        
        # Expand A (Forward)
        next_front_a = set()
        # Sample if too large to keep speed up
        current_nodes_a = list(front_a)
        if len(current_nodes_a) > 50: current_nodes_a = random.sample(current_nodes_a, 50)
        
        for node in current_nodes_a:
            # Find neighbors
            sig = index[node]
            # We only scan a subset for speed
            candidates = random.sample(list(index.keys()), 200)
            neighbors = []
            for cand in candidates:
                if get_resonance(sig, index[cand]) > 0.05: # Threshold
                    neighbors.append(cand)
            
            for neighbor in neighbors:
                if neighbor not in visited_a:
                    visited_a[neighbor] = visited_a[node] + [neighbor]
                    next_front_a.add(neighbor)
                    
                    # Check intersection
                    if neighbor in visited_b:
                        print(f"\n✨ BRIDGE COMPLETED AT: {neighbor.replace('WIKI-', '')}")
                        path_a = visited_a[neighbor]
                        path_b = visited_b[neighbor]
                        full_path = path_a[:-1] + path_b[::-1] # Join paths
                        
                        print("\n   [THE PATH]")
                        for i, step in enumerate(full_path):
                            clean = step.replace("WIKI-", "")
                            print(f"   {i+1}. {clean}")
                        return

        front_a = next_front_a
        
        # Expand B (Backward) - Symmetric Logic
        next_front_b = set()
        current_nodes_b = list(front_b)
        if len(current_nodes_b) > 50: current_nodes_b = random.sample(current_nodes_b, 50)
        
        for node in current_nodes_b:
            sig = index[node]
            candidates = random.sample(list(index.keys()), 200)
            neighbors = []
            for cand in candidates:
                if get_resonance(sig, index[cand]) > 0.05:
                    neighbors.append(cand)
            
            for neighbor in neighbors:
                if neighbor not in visited_b:
                    visited_b[neighbor] = visited_b[node] + [neighbor]
                    next_front_b.add(neighbor)
                    
                    if neighbor in visited_a:
                        print(f"\n✨ BRIDGE COMPLETED AT: {neighbor.replace('WIKI-', '')}")
                        path_a = visited_a[neighbor]
                        path_b = visited_b[neighbor]
                        full_path = path_a + path_b[::-1][1:]
                        
                        print("\n   [THE PATH]")
                        for i, step in enumerate(full_path):
                            clean = step.replace("WIKI-", "")
                            print(f"   {i+1}. {clean}")
                        return
        
        front_b = next_front_b
        
        print(f"      Frontiers: A={len(front_a)}, B={len(front_b)}")
        if not front_a and not front_b:
            print("   (Bridge collapsed - frontiers empty)")
            break

    print("\n❌ Bridge failed to close within depth limit.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("start", type=str)
    parser.add_argument("end", type=str)
    args = parser.parse_args()
    
    build_bridge(args.start, args.end)