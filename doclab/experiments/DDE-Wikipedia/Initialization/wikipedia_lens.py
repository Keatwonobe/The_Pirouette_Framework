"""
DDE-Pirouette: Wikipedia Lens (The Path Visualizer)
---------------------------------------------------
Visualizes a Semantic Bridge on the Atlas.
Takes a list of concepts (a path) and draws the trajectory on the map.

Usage:
    python wiki_lens.py "Aristotle,A_Fire_Upon_the_Deep,Arthur_Schopenhauer"
"""

import sys
import json
import argparse
import os
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
ATLAS_MAP = "wiki_atlas_map.json"
ATLAS_IMAGE = "wiki_atlas_25k.png"
OUTPUT_DIR = "wiki_lenses"

def visualize_path(path_string):
    if not os.path.exists(ATLAS_MAP) or not os.path.exists(ATLAS_IMAGE):
        print("❌ Missing Map or Image.")
        return

    # 1. Parse Path
    # Expecting comma-separated string: "ConceptA,ConceptB,ConceptC"
    concepts = [c.strip() for c in path_string.split(',')]
    print(f"🔭 LENS FOCUSED ON: {len(concepts)} nodes")

    # 2. Load Map
    with open(ATLAS_MAP, 'r') as f:
        physical_map = json.load(f)["tiles"]
    
    # Build lookup (Title -> Coords)
    id_to_coords = {}
    for filename, info in physical_map.items():
        clean_key = filename.replace("WIKI-", "").replace(".png", "")
        id_to_coords[clean_key] = (info['x'], info['y'])

    # 3. Prepare Canvas
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    atlas = Image.open(ATLAS_IMAGE).convert("RGBA")
    # Darken base map
    dark_layer = Image.new('RGBA', atlas.size, (0, 0, 0, 200))
    atlas = Image.alpha_composite(atlas, dark_layer)
    
    draw = ImageDraw.Draw(atlas)
    
    # 4. Plot Path
    points = []
    for concept in concepts:
        if concept in id_to_coords:
            points.append(id_to_coords[concept])
        else:
            print(f"   ⚠️ Concept not mapped: {concept}")

    if len(points) < 2:
        print("   🌑 Not enough valid points to draw a path.")
        return

    # Draw Lines
    draw.line(points, fill=(0, 255, 255, 255), width=1)
    
    # Draw Nodes
    for i, (x, y) in enumerate(points):
        # Start = Green, End = Red, Mid = White
        if i == 0:
            color = (0, 255, 0, 255)
            r = 2
        elif i == len(points) - 1:
            color = (255, 0, 0, 255)
            r = 2
        else:
            color = (255, 255, 255, 255)
            r = 1
            
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color)

    # 5. Save
    safe_name = f"{concepts[0]}_to_{concepts[-1]}".replace(" ", "_")[:50]
    filename = f"{OUTPUT_DIR}/path_{safe_name}.png"
    atlas.save(filename)
    print(f"✨ Path Visualized: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Comma separated list of concepts")
    args = parser.parse_args()
    
    visualize_path(args.path)