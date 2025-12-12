"""
DDE-Pirouette: Wikipedia Oracle (The Recall Engine)
---------------------------------------------------
Performs Semantic Recall on the DDE Atlas.
1. Converts user query to keywords.
2. Scans 'wiki_resonance_index.json' for matches (Jaccard Similarity).
3. Retrieves physical coordinates from 'wiki_atlas_map.json'.

Usage:
    python wiki_oracle.py "Agricultural Science"
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
        print("❌ Missing Index or Map files. Run stitcher and indexer first.")
        sys.exit(1)
        
    print("   📖 Loading Resonance Index...")
    with open(INDEX_FILE, 'r') as f:
        semantic_index = json.load(f)["index"]
        
    print("   📖 Loading Atlas Map...")
    with open(ATLAS_MAP, 'r') as f:
        physical_map = json.load(f)["tiles"]
        
    return semantic_index, physical_map

def query_oracle(query, top_k=10):
    semantic_index, physical_map = load_data()
    
    # 1. Process Query
    query_words = set(query.lower().split())
    print(f"\n🔮 ORACLE QUERY: '{query}'")
    print(f"   Keywords: {query_words}")
    
    # 2. Score Articles (Jaccard Overlap)
    scores = []
    
    for mid, signature in semantic_index.items():
        sig_set = set(signature)
        # Intersection count
        overlap = len(query_words.intersection(sig_set))
        
        if overlap > 0:
            # Score = Overlap / (Total Unique Words) - Basic Jaccard
            score = overlap / len(query_words.union(sig_set))
            scores.append((mid, score, overlap))
    
    # 3. Sort & Rank
    scores.sort(key=lambda x: x[1], reverse=True)
    top_results = scores[:top_k]
    
    if not top_results:
        print("   🌑 No resonance found.")
        return

    print(f"\n✨ FOUND {len(top_results)} RESONANT ARTIFACTS:")
    print(f"   {'SCORE':<8} | {'COORDINATES':<12} | {'TITLE'}")
    print("   " + "-"*50)
    
    # 4. Resolve to Atlas Coordinates
    # We need to match IDs from index (WIKI-Title) to filenames in map (WIKI-Title.png)
    
    # Create lookup for map (ID -> Coords)
    id_to_coords = {v['id']: (v['x'], v['y']) for k, v in physical_map.items()}
    
    for mid, score, overlap in top_results:
        # mid is "WIKI-Title_..."
        # map ID is usually just the title part "Title_..."
        
        # Try direct match first
        clean_id = mid.replace("WIKI-", "")
        coords = id_to_coords.get(clean_id, ("?", "?"))
        
        print(f"   {score:.4f}   | {str(coords):<12} | {clean_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, help="Topic to recall")
    args = parser.parse_args()
    
    query_oracle(args.query)