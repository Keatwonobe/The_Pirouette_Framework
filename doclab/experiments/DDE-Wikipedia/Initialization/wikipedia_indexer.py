"""
DDE-Pirouette: Wikipedia Resonance Indexer v1.1
-----------------------------------------------
- Fixed: Removed lxml dependency (getprevious crash)
- Fixed: Standard Library Memory Safety (Root Clearing)
- Output: wiki_resonance_index.json

Usage:  python wiki_indexer.py "wiki.xml" --checkpoint "dde_wiki_checkpoint_20000.json"
"""

import sys
import os
import argparse
import re
import xml.etree.ElementTree as ET
import json
import time
from collections import Counter

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
OUTPUT_INDEX = "wiki_resonance_index.json"

def clean_wiki_text_fast(text):
    """Fast cleaner for semantic extraction."""
    if not text: return ""
    # Strip heavy markup
    text = re.sub(r'\[\[File:.*?\]\]', '', text)
    text = re.sub(r'<ref.*?>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'\{\{.*?\}\}', '', text, flags=re.DOTALL)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text) # Keep only letters
    return text.lower()

def generate_module_id(title):
    safe_title = "".join([c if c.isalnum() else "_" for c in title])
    return f"WIKI-{safe_title[:50]}"

def compute_signature(text, top_k=50):
    """Extracts the 'Signature' of an article."""
    words = text.split()
    # Filter stop words (rough heuristic by length)
    meaningful_words = [w for w in words if len(w) > 4]
    
    counts = Counter(meaningful_words)
    
    # Sort by (Length * Frequency) to find "Heavy" words
    ranked = sorted(counts.items(), key=lambda x: (len(x[0]) * x[1]), reverse=True)
    
    # Return top K words
    return [w for w, count in ranked[:top_k]]

def local_tag(tag):
    if not tag: return ""
    return tag.split('}', 1)[-1] if '}' in tag else tag

def build_index(xml_path, checkpoint_path):
    print(f"🧠 RESONANCE INDEXER ONLINE")
    print(f"   Loading manifest from {checkpoint_path}...")
    
    try:
        with open(checkpoint_path, 'r') as f:
            data = json.load(f)
            # Handle minified/full formats
            if "data" in data: 
                manifest = data["data"]["m"] # Minified 'manifest' key
            else:
                manifest = data.get("manifest", {})
    except Exception as e:
        print(f"❌ Failed to load checkpoint: {e}")
        return

    target_ids = set(manifest.keys())
    print(f"   Targeting {len(target_ids)} articles for indexing.")
    
    index = {}
    
    # Robust Stream Setup
    context = ET.iterparse(xml_path, events=('start', 'end'))
    context = iter(context)
    event, root = next(context)

    processed = 0
    indexed = 0
    start_time = time.time()

    print("   ⚡ Scanning XML for semantic signatures...")

    for event, elem in context:
        if event == "end":
            tag = local_tag(elem.tag)
            if tag == "page":
                try:
                    # Extract Title
                    title = "Unknown"
                    for child in elem:
                        if local_tag(child.tag) == "title":
                            title = child.text
                            break

                    if title:
                        mid = generate_module_id(title)
                        if mid in target_ids:
                            # Extract Text
                            raw_text = ""
                            try:
                                for child in elem:
                                    if local_tag(child.tag) == "revision":
                                        for rev in child:
                                            if local_tag(rev.tag) == "text": 
                                                raw_text = rev.text
                            except: pass
                            
                            if raw_text:
                                clean = clean_wiki_text_fast(raw_text)
                                sig = compute_signature(clean)
                                index[mid] = sig
                                indexed += 1
                                
                                if indexed % 1000 == 0:
                                    sys.stdout.write(f"\r   📝 Indexed: {indexed}/{len(target_ids)} | Last: {title[:20]}")
                except Exception as e:
                    pass
                finally:
                    # Standard Library Safe Clearing
                    elem.clear()
                    root.clear()
                    processed += 1

    print(f"\n   💾 Saving Resonance Index to {OUTPUT_INDEX}...")
    with open(OUTPUT_INDEX, 'w') as f:
        json.dump({
            "created": time.time(),
            "count": indexed,
            "index": index
        }, f)
    
    print(f"   ✅ Indexing Complete ({time.time() - start_time:.2f}s)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("xml_file", type=str)
    parser.add_argument("--checkpoint", type=str, required=True)
    args = parser.parse_args()
    
    if not os.path.exists(args.xml_file):
        print("❌ XML not found")
        sys.exit(1)
        
    build_index(args.xml_file, args.checkpoint)