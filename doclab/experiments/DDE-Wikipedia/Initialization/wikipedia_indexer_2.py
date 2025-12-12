"""
DDE-Pirouette: Wikipedia Resonance Indexer v1.3 (Early Exit)
------------------------------------------------------------
- Fixed: "Endless Scan" bug (Stops immediately when all targets are found)
- Added: Completion Check on Startup
- Retains: Checkpointing & Memory Safety

Usage:  python wiki_indexer.py "wiki.xml" --checkpoint "dde_wiki_checkpoint_20000.json"
"""

import sys
import os
import argparse
import re
import xml.etree.ElementTree as ET
import json
import time
import gc
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
    meaningful_words = [w for w in words if len(w) > 4]
    counts = Counter(meaningful_words)
    # Rank by (Length * Frequency) -> "Heavy" words
    ranked = sorted(counts.items(), key=lambda x: (len(x[0]) * x[1]), reverse=True)
    return [w for w, count in ranked[:top_k]]

def local_tag(tag):
    if not tag: return ""
    return tag.split('}', 1)[-1] if '}' in tag else tag

def save_index_atomic(index_data, filepath):
    """Saves index safely without corruption risk."""
    temp = filepath + ".tmp"
    try:
        with open(temp, 'w') as f:
            json.dump(index_data, f)
        if os.path.exists(filepath):
            os.remove(filepath)
        os.rename(temp, filepath)
    except Exception as e:
        print(f"\n   ⚠️ Save failed (non-fatal): {e}")

def build_index(xml_path, checkpoint_path):
    print(f"🧠 RESONANCE INDEXER v1.3 ONLINE")
    
    # 1. Load Targets
    print(f"   📖 Loading manifest from {checkpoint_path}...")
    try:
        with open(checkpoint_path, 'r') as f:
            data = json.load(f)
            if "data" in data: 
                manifest = data["data"]["m"]
            else:
                manifest = data.get("manifest", {})
    except Exception as e:
        print(f"❌ Failed to load manifest: {e}")
        return

    target_ids = set(manifest.keys())
    target_count = len(target_ids)
    print(f"   🎯 Targeting {target_count} articles.")
    
    # 2. Load Existing Index
    index = {}
    if os.path.exists(OUTPUT_INDEX):
        print(f"   📂 Found existing index: {OUTPUT_INDEX}")
        try:
            with open(OUTPUT_INDEX, 'r') as f:
                existing_data = json.load(f)
                index = existing_data.get("index", {})
            print(f"   ⏩ Resuming with {len(index)} signatures already indexed.")
        except:
            print("   ⚠️ Index file corrupt or unreadable. Starting fresh.")

    # --- EARLY EXIT CHECK ---
    if len(index) >= target_count:
        print(f"\n✨ INDEX COMPLETE! ({len(index)}/{target_count} found)")
        print("   No need to scan XML. Exiting.")
        return
    # ------------------------

    # 3. Stream
    context = ET.iterparse(xml_path, events=('start', 'end'))
    context = iter(context)
    event, root = next(context)

    processed = 0
    indexed_count = len(index)
    skipped = 0
    start_time = time.time()

    print("   ⚡ Scanning XML...")

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
                        
                        # Is it a target?
                        if mid in target_ids:
                            # Do we already have it?
                            if mid in index:
                                skipped += 1
                                if skipped % 5000 == 0:
                                    sys.stdout.write(f"\r   ⏩ Skipped {skipped} existing...")
                            else:
                                # It's new! Process it.
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
                                    indexed_count += 1
                                    
                                    # Feedback
                                    if indexed_count % 100 == 0:
                                        sys.stdout.write(f"\r   📝 Indexed: {indexed_count}/{target_count} | {title[:20]:<20}")

                                    # Periodic Save
                                    if indexed_count % 1000 == 0:
                                        save_data = {
                                            "created": time.time(),
                                            "count": indexed_count,
                                            "index": index
                                        }
                                        save_index_atomic(save_data, OUTPUT_INDEX)
                                        gc.collect()

                                    # --- LOOP BREAK CONDITION ---
                                    # If we have found everything, STOP SCANNING.
                                    if indexed_count >= target_count:
                                        print(f"\n\n✨ ALL TARGETS FOUND ({indexed_count}). Stopping scan.")
                                        elem.clear()
                                        root.clear()
                                        break
                                    # ----------------------------

                except Exception as e:
                    pass
                finally:
                    elem.clear()
                    root.clear()
                    processed += 1
                    
                    if processed % 5000 == 0:
                        gc.collect()

    # Final Save
    print(f"\n   💾 Saving Final Resonance Index...")
    with open(OUTPUT_INDEX, 'w') as f:
        json.dump({
            "created": time.time(),
            "count": indexed_count,
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