"""
DDE-Pirouette: Wikipedia Stitcher v1.1 (Atomic)
-----------------------------------------------
Scans the 'wiki_vault' and builds the High-Density Atlas.
- Fixed: Atomic JSON saving (Prevents 'Expecting , delimiter' corruption).
- Optimized: Buffered image pasting for speed.

Usage:
    python wiki_stitcher.py
"""

import os
import glob
import math
import json
import time
from PIL import Image
from datetime import datetime

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
VAULT_DIR = "wiki_vault"
OUTPUT_IMAGE = "wiki_atlas_20k.png"
OUTPUT_MAP = "wiki_atlas_map.json"

def save_json_atomic(data, filepath):
    """Saves JSON safely to prevent corruption on crash."""
    temp = filepath + ".tmp"
    try:
        with open(temp, 'w') as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno()) # Force write to disk
        if os.path.exists(filepath):
            os.remove(filepath)
        os.rename(temp, filepath)
        print(f"   💾 Map saved atomically to {filepath}")
    except Exception as e:
        print(f"   ❌ Map Save Failed: {e}")

def stitch_atlas():
    print(f"🗺️  DDE ATLAS STITCHER v1.1 ONLINE")
    print(f"   Scanning {VAULT_DIR}...")
    
    # 1. Gather Artifacts
    files = sorted(glob.glob(os.path.join(VAULT_DIR, "*.png")))
    total_count = len(files)
    
    if total_count == 0:
        print("❌ No artifacts found in vault. Run the Factory first.")
        return

    print(f"   Found {total_count} spirit pixels.")

    # 2. Calculate Grid
    grid_side = math.ceil(math.sqrt(total_count))
    print(f"   📐 Grid Geometry: {grid_side} x {grid_side} ({grid_side**2} slots)")

    # 3. Create Canvas
    atlas = Image.new('RGBA', (grid_side, grid_side), (0, 0, 0, 0))
    
    # 4. The Stitching Loop
    atlas_map = {}
    print("   🪡 Stitching pixels...")
    
    start_time = time.time()
    
    for idx, filepath in enumerate(files):
        try:
            with Image.open(filepath) as tile:
                x = idx % grid_side
                y = idx // grid_side
                
                atlas.paste(tile, (x, y))
                
                filename = os.path.basename(filepath)
                article_name = filename.replace("WIKI-", "").replace(".png", "")
                
                atlas_map[filename] = {
                    "id": article_name,
                    "x": x,
                    "y": y,
                    "idx": idx
                }
                
                if idx % 5000 == 0 and idx > 0:
                    print(f"      Stitched {idx}/{total_count}...")
                    
        except Exception as e:
            print(f"⚠️  Corrupt pixel {filepath}: {e}")

    # 5. Save Image
    print(f"   💾 Saving Atlas Image...")
    atlas.save(OUTPUT_IMAGE)
    
    # 6. Save Map (Atomic)
    map_data = {
        "created": datetime.utcnow().isoformat(),
        "count": total_count,
        "geometry": [grid_side, grid_side],
        "tiles": atlas_map
    }
    save_json_atomic(map_data, OUTPUT_MAP)

    print("\n✨ ATLAS COMPLETE")
    print(f"   Time:  {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    if not os.path.exists(VAULT_DIR):
        print(f"❌ Vault directory '{VAULT_DIR}' not found.")
    else:
        stitch_atlas()