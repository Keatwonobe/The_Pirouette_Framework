"""
DDE-Pirouette: Wikipedia Bridge (The Interface)
-----------------------------------------------
The "Context Engine".
1. Accepts a natural language query.
2. Consults the DDE Atlas to find resonant facts.
3. Extracts the 'Semantic DNA' from those coordinates.
4. Constructs a 'Grounding Prompt' for an LLM.

Usage:
    python wiki_bridge.py "Who is Abraham Lincoln?"
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
        
    with open(INDEX_FILE, 'r') as f:
        semantic_index = json.load(f)["index"]
    with open(ATLAS_MAP, 'r') as f:
        physical_map = json.load(f)["tiles"]
    return semantic_index, physical_map

def generate_llm_prompt(query, top_k=3):
    semantic_index, physical_map = load_data()
    
    # 1. Analyze Query
    query_words = set(query.lower().split())
    q_len = len(query_words)
    
    # 2. Resonance Search
    scores = []
    for mid, signature in semantic_index.items():
        sig_set = set(signature)
        if len(sig_set) < q_len:
            overlap = len(sig_set.intersection(query_words))
        else:
            overlap = len(query_words.intersection(sig_set))
        
        if overlap > 0:
            union_len = len(sig_set) + q_len - overlap
            score = overlap / union_len
            scores.append((mid, score))
            
    scores.sort(key=lambda x: x[1], reverse=True)
    top_matches = scores[:top_k]
    
    if not top_matches:
        print("🌑 The DDE is silent on this topic.")
        return

    # 3. Construct Context Block
    context_block = []
    
    print(f"⚡ DDE BRIDGE ACTIVATED: '{query}'")
    print(f"   Found {len(top_matches)} grounding artifacts.")
    print("-" * 60)

    for i, (mid, score) in enumerate(top_matches):
        clean_id = mid.replace("WIKI-", "")
        signature = semantic_index[mid]
        
        # We construct a "Fact Block" for the LLM
        fact = f"SOURCE {i+1} ({clean_id}): Contains concepts like {', '.join(signature[:15])}..."
        context_block.append(fact)
        print(f"   + Attached Context: {clean_id} (Resonance: {score:.2f})")

    # 4. The Final Prompt
    # This is what you would send to GPT/Claude
    final_prompt = f"""
SYSTEM: You are a helpful assistant backed by a DDE Context Engine.
Use the provided SOURCES to answer the user's question. 
If the answer is not in the sources, admit you don't know.

USER QUESTION: {query}

--- DDE CONTEXT STREAM ---
{chr(10).join(context_block)}
--------------------------

ANSWER:
"""
    
    print("\n" + "="*60)
    print("GENERATED PROMPT (Copy/Paste this to your LLM):")
    print("="*60)
    print(final_prompt)
    print("="*60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, help="Question for the AI")
    args = parser.parse_args()
    
    generate_llm_prompt(args.query)