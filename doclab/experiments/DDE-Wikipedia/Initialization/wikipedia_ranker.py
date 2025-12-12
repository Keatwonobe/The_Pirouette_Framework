"""
DDE-Pirouette: Wikipedia Ranker (The Curator)
---------------------------------------------
Re-ranks the entire DDE Corpus based on distance to a specific set of Seed Concepts.
Used to create 'Curated Curricula' or 'Filtered Reality Tunnels'.

Usage:
    python wiki_ranker.py "Physics,Mathematics,Logic" --top 100
"""

import sys
import json
import argparse
import os
import math

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
INDEX_FILE = "wiki_resonance_index.json"

def load_index():
    if not os.path.exists(INDEX_FILE):
        print("❌ Missing Resonance Index.")
        sys.exit(1)
    with open(INDEX_FILE, 'r') as f:
        return json.load(f)["index"]

def get_resonance(signature_a, signature_b):
    set_a = set(signature_a)
    set_b = set(signature_b)
    if not set_a or not set_b: return 0
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    return intersection / union

def rank_corpus(seeds_string, top_k=100):
    index = load_index()
    
    seeds = [s.strip() for s in seeds_string.split(',')]
    print(f"⚖️  RANKER ONLINE")
    print(f"   Seeds: {seeds}")
    
    # 1. Find Seed Anchors
    seed_signatures = []
    for seed in seeds:
        seed_words = set(seed.lower().split())
        best_sig = None
        best_score = -1
        
        for mid, sig in index.items():
            score = len(set(sig).intersection(seed_words))
            if score > best_score:
                best_score = score
                best_sig = sig
        
        if best_sig:
            seed_signatures.append(best_sig)
        else:
            print(f"   ⚠️ Warning: Seed '{seed}' not found in corpus.")

    if not seed_signatures:
        print("   ❌ No valid seeds found. Aborting.")
        return

    print(f"   Anchored {len(seed_signatures)} seeds. Calculating gradients...")

    # 2. Calculate Global Resonance
    # Every article gets a score based on its average resonance with ALL seeds
    ranked_corpus = []
    
    total = len(index)
    processed = 0
    
    for mid, sig in index.items():
        # Sum of resonance with all seeds
        total_resonance = 0
        for seed_sig in seed_signatures:
            total_resonance += get_resonance(sig, seed_sig)
            
        # Average it
        avg_score = total_resonance / len(seed_signatures)
        
        if avg_score > 0:
            ranked_corpus.append((mid, avg_score))
            
        processed += 1
        if processed % 5000 == 0:
            sys.stdout.write(f"\r   Scanned {processed}/{total}...")

    # 3. Sort and Display
    ranked_corpus.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n\n🏆 TOP {top_k} RELEVANT ARTIFACTS:")
    print(f"   {'SCORE':<8} | {'TITLE'}")
    print("   " + "-"*50)
    
    for i, (mid, score) in enumerate(ranked_corpus[:top_k]):
        clean_id = mid.replace("WIKI-", "")
        print(f"   {score:.4f}   | {clean_id}")

    # 4. Save to CSV
    filename = f"ranked_corpus_{len(seeds)}seeds.csv"
    print(f"\n💾 Saving full ranking to {filename}...")
    with open(filename, 'w') as f:
        f.write("rank,score,article_id\n")
        for i, (mid, score) in enumerate(ranked_corpus):
            clean_id = mid.replace("WIKI-", "")
            f.write(f"{i+1},{score:.6f},{clean_id}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("seeds", type=str, help="Comma separated seeds")
    parser.add_argument("--top", type=int, default=100)
    args = parser.parse_args()
    
    rank_corpus(args.seeds, args.top)