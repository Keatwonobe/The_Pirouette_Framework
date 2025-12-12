"""
DDE-Pirouette Atlas Stitcher v2.0
- Stitches all module images into a single "glob" atlas.
- Reads both minified and full DDE DB manifests.
- Saves its own minified glob manifest.
"""

import sys
import json
import math
from PIL import Image
from pathlib import Path
import argparse
from datetime import datetime
# Import the new v7.3 class and its helper functions
from DDE_Pirouette import DDEPirouette, DDE_KEY_MAP, _minify_keys_recursive

def stitch_to_atlas(manifest_path_str: str, image_folder_str: str, save_minified: bool):
    """
    Combines all module images from a folder into a single atlas image.
    """
    
    manifest_path = Path(manifest_path_str)
    image_folder_path = Path(image_folder_str)

    if not manifest_path.exists():
        print(f"❌ Error: Manifest file not found: {manifest_path_str}")
        return
    if not image_folder_path.is_dir():
        print(f"❌ Error: Image directory not found: {image_folder_str}")
        return

    print("=" * 70)
    print(f"🗺️  STARTING ATLAS STITCHING (v2)")
    print(f"   Manifest: {manifest_path.name}")
    print(f"   Images:   ./{image_folder_path.name}/")
    print("=" * 70)

    # 1. Load the DB manifest (using the "smart" loader)
    dde = DDEPirouette()
    dde.load_manifest(manifest_path_str)
    
    manifest = dde.manifest
    if not manifest:
        print("❌ Error: No 'manifest' data found in loaded DDE instance.")
        return

    # 2. Find the max tile size and module count
    max_size = 0
    module_ids = list(manifest.keys())
    n_modules = len(module_ids)
    
    for module_id, data in manifest.items():
        max_size = max(max_size, data.get('image_size', 0))

    if max_size == 0:
        print("❌ Error: No images with a size > 0 found in manifest.")
        return
        
    print(f"   Found {n_modules} modules.")
    print(f"   Max tile size (padding): {max_size}x{max_size} pixels")

    # 3. Calculate grid dimensions
    grid_side = int(math.ceil(math.sqrt(n_modules)))
    atlas_dim_px = grid_side * max_size
    
    print(f"   Atlas grid: {grid_side} x {grid_side} tiles")
    print(f"   Final image size: {atlas_dim_px} x {atlas_dim_px} pixels")

    # 4. Create the new blank atlas image
    atlas_image = Image.new('RGBA', (atlas_dim_px, atlas_dim_px), (0, 0, 0, 0))

    # 5. Create the new glob manifest data (un-minified first)
    db_name = manifest_path.stem.split('dde_db_')[-1]
    
    glob_manifest_data = {
        'version': '7.3-glob-v2-minified',
        'atlas_file': f'dde_glob_atlas_{db_name}.png',
        'tile_size': max_size,
        'grid_dim': grid_side,
        'total_modules': n_modules,
        'locations': {},
        # Embed the *entire* original manifest data, including vocab
        'original_manifest': {
            'version': dde.manifest.get('version', '7.3-minified-rehydrated'),
            'created': dde.manifest.get('created', datetime.now().isoformat()),
            'manifest': dde.manifest,
            'coherence_history': dde.coherence_history,
            'vocab': dde.vocab,
            'reverse_vocab': dde.reverse_vocab
        }
    }

    print(f"\nStitching {n_modules} images into atlas...")

    # 6. Iterate, load, and paste
    current_x_tile, current_y_tile = 0, 0

    for module_id in module_ids:
        img_path = image_folder_path / f"{module_id}.png"
        
        if not img_path.exists():
            print(f"  ⚠️  Warning: Missing image for {module_id}, skipping.")
            continue

        try:
            with Image.open(img_path) as tile_img:
                paste_x_px = current_x_tile * max_size
                paste_y_px = current_y_tile * max_size
                
                atlas_image.paste(tile_img, (paste_x_px, paste_y_px), tile_img)
                
                glob_manifest_data['locations'][module_id] = {
                    'x': current_x_tile, 
                    'y': current_y_tile
                }

            current_x_tile += 1
            if current_x_tile >= grid_side:
                current_x_tile = 0
                current_y_tile += 1
                
        except Exception as e:
            print(f"  ❌ FAILED to paste {module_id}: {e}")

    # 7. Save the final files
    atlas_image_path = glob_manifest_data['atlas_file']
    atlas_manifest_path = f'dde_glob_manifest_{db_name}.json'

    atlas_image.save(atlas_image_path)
    print(f"\n✅ Atlas image saved: {atlas_image_path}")
    
    # --- NEW: Save minified or full ---
    if save_minified:
        print(f"🗜️  Saving MINIFIED glob manifest to {atlas_manifest_path}...")
        minified_data = _minify_keys_recursive(glob_manifest_data, DDE_KEY_MAP)
        output_json = {
            "meta_map": DDE_KEY_MAP,
            "data": minified_data
        }
        with open(atlas_manifest_path, 'w') as f:
            json.dump(output_json, f, separators=(',', ':'), default=str)
    else:
        print(f"💾 Saving FULL glob manifest to {atlas_manifest_path}...")
        with open(atlas_manifest_path, 'w') as f:
            json.dump(glob_manifest_data, f, indent=2, default=str)
    
    print(f"   ✅ Atlas manifest saved.")
    print("\n" + "=" * 70)
    print(f"🎉 GLOB DATABASE CREATED! 🎉")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DDE Atlas Stitcher v2.0 (Minified)"
    )
    parser.add_argument(
        "db_manifest", 
        type=str, 
        help="Path to the dde_db_[name].json manifest file."
    )
    parser.add_argument(
        "img_folder",
        type=str,
        help="Path to the dde_img_[name]/ folder."
    )
    parser.add_argument(
        "--minify",
        action="store_true",
        help="Save the output glob_manifest in a minified format."
    )
    
    args = parser.parse_args()
        
    stitch_to_atlas(args.db_manifest, args.img_folder, args.minify)