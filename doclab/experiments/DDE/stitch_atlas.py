"""
DDE-Pirouette Atlas Stitcher v1.0
"Stitches" all individual DDE module images into a single
"glob" atlas image and creates a new manifest to map it.
"""

import sys
import json
import math
from PIL import Image
from pathlib import Path

def stitch_to_atlas(manifest_path_str: str, image_folder_str: str):
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
    print(f"🗺️  STARTING ATLAS STITCHING")
    print(f"   Manifest: {manifest_path.name}")
    print(f"   Images:   ./{image_folder_path.name}/")
    print("=" * 70)

    # 1. Load the original database manifest
    with open(manifest_path, 'r') as f:
        db_data = json.load(f)
    
    manifest = db_data.get('manifest')
    if not manifest:
        print("❌ Error: No 'manifest' key found in JSON file.")
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
    # We use RGBA for consistency, (0,0,0,0) is transparent
    atlas_image = Image.new('RGBA', (atlas_dim_px, atlas_dim_px), (0, 0, 0, 0))

    # 5. Create the new glob manifest
    # We embed the original manifest inside this new one for full provenance
    db_name = manifest_path.stem.split('dde_db_')[-1]
    
    glob_manifest = {
        'version': '7.0-glob-v1',
        'atlas_file': f'dde_glob_atlas_{db_name}.png',
        'tile_size': max_size,
        'grid_dim': grid_side,
        'total_modules': n_modules,
        'locations': {}, # This will map module_id -> {x, y}
        'original_manifest': db_data
    }

    print(f"\nStitching {n_modules} images into atlas...")

    # 6. Iterate, load, and paste
    current_x_tile = 0
    current_y_tile = 0

    for module_id in module_ids:
        img_path = image_folder_path / f"{module_id}.png"
        
        if not img_path.exists():
            print(f"  ⚠️  Warning: Missing image for {module_id}, skipping.")
            continue

        try:
            with Image.open(img_path) as tile_img:
                # Calculate paste position in pixels
                # All tiles are pasted at the top-left of their "slot"
                paste_x_px = current_x_tile * max_size
                paste_y_px = current_y_tile * max_size
                
                # Paste (using tile_img as mask for transparency)
                atlas_image.paste(tile_img, (paste_x_px, paste_y_px), tile_img)
                
                # Record the location in the manifest
                glob_manifest['locations'][module_id] = {
                    'x': current_x_tile, 
                    'y': current_y_tile
                }

            # Increment tile coordinates
            current_x_tile += 1
            if current_x_tile >= grid_side:
                current_x_tile = 0
                current_y_tile += 1
                
        except Exception as e:
            print(f"  ❌ FAILED to paste {module_id}: {e}")

    # 7. Save the final files
    atlas_image_path = glob_manifest['atlas_file']
    atlas_manifest_path = f'dde_glob_manifest_{db_name}.json'

    atlas_image.save(atlas_image_path)
    print(f"\n✅ Atlas image saved: {atlas_image_path}")
    
    with open(atlas_manifest_path, 'w') as f:
        json.dump(glob_manifest, f, indent=2)
    print(f"✅ Atlas manifest saved: {atlas_manifest_path}")
    
    print("\n" + "=" * 70)
    print(f"🎉 GLOB DATABASE CREATED! 🎉")
    print("   You now have a single .png file and a single .json")
    print("   manifest that describes the 'packed' database.")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("="*70)
        print("DDE Atlas Stitcher v1.0")
        print("="*70)
        print("Usage: python stitch_atlas.py <path_to_db.json> <path_to_img_folder>")
        print("\nExample:")
        print("  python stitch_atlas.py ./dde_db_modules_outbox.json ./dde_img_modules_outbox")
        print("="*70)
        sys.exit(1)
        
    json_path = sys.argv[1]
    img_folder = sys.argv[2]
    stitch_to_atlas(json_path, img_folder)