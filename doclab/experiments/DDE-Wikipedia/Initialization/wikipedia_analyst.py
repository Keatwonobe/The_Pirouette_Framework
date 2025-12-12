"""
DDE-Pirouette: Wikipedia Analyst (The Cartographer's Lens)
----------------------------------------------------------
Generates visual "Constellations" from the DDE Atlas.
1. Takes a query (e.g., "History").
2. Dimms the entire Atlas to near-black.
3. Lights up resonant pixels with high intensity.
4. Draws "connection lines" between the top matches to show the shape.

Usage:
    python wiki_analyst.py "Civil War"
"""

import sys
import json
import argparse
import os
import math
from PIL import Image, ImageDraw, ImageEnhance

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
INDEX_FILE = "wiki_resonance_index.json"
ATLAS_MAP = "wiki_atlas_map.json"
ATLAS_IMAGE = "wiki_atlas_25k.png"
OUTPUT_DIR = "wiki_constellations"

def load_data():
    if not os.path.exists(INDEX_FILE) or not os.path.exists(ATLAS_MAP) or not os.path.exists(ATLAS_IMAGE):
        print("❌ Missing Index, Map, or Atlas Image.")
        sys.exit(1)
        
    print("   📖 Loading Dataset...")
    with open(INDEX_FILE, 'r') as f:
        semantic_index = json.load(f)["index"]
    with open(ATLAS_MAP, 'r') as f:
        physical_map = json.load(f)["tiles"]
        
    return semantic_index, physical_map

def generate_constellation(query):
    semantic_index, physical_map = load_data()
    
    # 1. Prepare Canvas
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"   🎨 Loading Atlas Canvas...")
    original_atlas = Image.open(ATLAS_IMAGE).convert("RGBA")
    
    # Create a "Night Mode" version (dimmed by 90%)
    enhancer = ImageEnhance.Brightness(original_atlas)
    night_atlas = enhancer.enhance(0.1) 
    draw = ImageDraw.Draw(night_atlas)

    # 2. Process Query
    query_words = set(query.lower().split())
    q_len = len(query_words)
    print(f"\n🔮 Analyzing Semantic Geometry for: '{query}'")

    matches = []
    
    # 3. Find Matches
    for mid, signature in semantic_index.items():
        sig_set = set(signature)
        
        # Fast Intersection
        if len(sig_set) < q_len:
            overlap = len(sig_set.intersection(query_words))
        else:
            overlap = len(query_words.intersection(sig_set))
        
        if overlap > 0:
            union_len = len(sig_set) + q_len - overlap
            score = overlap / union_len
            matches.append((mid, score))
    
    matches.sort(key=lambda x: x[1], reverse=True)
    
    # Filter: Only show meaningful matches (Top 50 or Score > 0.05)
    top_matches = matches[:50]
    
    if not top_matches:
        print("   🌑 No constellations found.")
        return

    # 4. Map Coordinates
    # Build lookup for filename -> coords
    id_to_coords = {}
    for filename, info in physical_map.items():
        clean_key = filename.replace("WIKI-", "").replace(".png", "")
        id_to_coords[clean_key] = (info['x'], info['y'])

    print(f"   ✨ Plotting {len(top_matches)} stars...")

    coordinates = []
    
    for mid, score in top_matches:
        clean_id = mid.replace("WIKI-", "")
        if clean_id in id_to_coords:
            x, y = id_to_coords[clean_id]
            coordinates.append((x, y, score))
            
            # Restore original pixel brightness for this spot
            # We do this by pasting the original pixel back onto the darkened map
            pixel = original_atlas.getpixel((x, y))
            night_atlas.putpixel((x, y), pixel)
            
            # Add a "Glow" (Draw a faint circle around high resonance items)
            if score > 0.1: # High confidence
                draw.ellipse((x-1, y-1, x+1, y+1), outline=(255, 255, 255, 100))

    # 5. Draw Constellation Lines (Connect the top 5 points)
    # This visualizes the "Shape" of the concept
    top_k_coords = coordinates[:5]
    if len(top_k_coords) > 1:
        for i in range(len(top_k_coords) - 1):
            p1 = top_k_coords[i]
            p2 = top_k_coords[i+1]
            # Draw faint line
            draw.line([(p1[0], p1[1]), (p2[0], p2[1])], fill=(255, 255, 255, 50), width=1)

    # 6. Save
    safe_query = "".join([c if c.isalnum() else "_" for c in query])
    filename = f"{OUTPUT_DIR}/constellation_{safe_query}.png"
    night_atlas.save(filename)
    
    print(f"\n🌠 Constellation Captured: {filename}")
    print(f"   (Open this image to see where '{query}' lives in the DDE)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, help="Topic to visualize")
    args = parser.parse_args()
    
    generate_constellation(args.query)