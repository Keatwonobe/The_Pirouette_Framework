"""
DDE-Pirouette Atlas Reader v2.0
"Rehydrates" a single module from a "glob" atlas .png
using its (potentially minified) .json manifest.
"""

import sys
import json
from PIL import Image
from pathlib import Path
# Import the new v7.3 class and its helper functions
from DDE_Pirouette import DDEPirouette, _rehydrate_keys_recursive

def rehydrate_module(glob_manifest_path: str, module_id: str):
    """
    Loads a single module from the DDE atlas and decodes it.
    """
    
    # 1. Load the Glob Manifest
    manifest_path = Path(glob_manifest_path)
    if not manifest_path.exists():
        print(f"❌ Error: Glob manifest not found: {glob_manifest_path}")
        return
        
    print(f"🗺️  Loading atlas map from: {manifest_path.name}")
    with open(manifest_path, 'r') as f:
        raw_data = json.load(f)

    # --- NEW: Smart Rehydration ---
    glob_data = {}
    if "meta_map" in raw_data and "data" in raw_data:
        print("🧬 Minified glob manifest detected. Rehydrating...")
        meta_map = raw_data['meta_map']
        reverse_key_map = {v: k for k, v in meta_map.items()}
        glob_data = _rehydrate_keys_recursive(raw_data['data'], reverse_key_map)
        print("   ✅ Rehydration complete.")
    else:
        print("🧬 Bloated glob manifest detected. Loading directly.")
        glob_data = raw_data
    # ------------------------------

    # 2. Find the module's location and metadata
    locations = glob_data.get('locations')
    tile_size = glob_data.get('tile_size')
    original_manifest_data = glob_data.get('original_manifest')
    
    if module_id not in locations:
        print(f"❌ Error: Module '{module_id}' not found in atlas locations.")
        return
    
    if module_id not in original_manifest_data['manifest']:
        print(f"❌ Error: Module '{module_id}' not found in original manifest data.")
        return

    # 3. Get the "Priming" data
    module_location = locations[module_id]
    module_info = original_manifest_data['manifest'][module_id]
    
    # 4. Load the Atlas Image
    atlas_image_path = Path(glob_data['atlas_file'])
    if not atlas_image_path.exists():
        print(f"❌ Error: Atlas image '{atlas_image_path}' not found.")
        return

    print(f"🧬 Loading data from: {atlas_image_path.name}")
    with Image.open(atlas_image_path) as atlas_image:
        
        # 5. Calculate crop coordinates
        x_tile = module_location['x']
        y_tile = module_location['y']
        
        x0 = x_tile * tile_size
        y0 = y_tile * tile_size
        x1 = x0 + tile_size
        y1 = y0 + tile_size
        
        print(f"   └─ Found '{module_id}' at tile ({x_tile}, {y_tile})")
        print(f"   └─ Cropping pixels from [{x0}:{x1}, {y0}:{y1}]")
        
        # 6. Crop the specific module's image
        tile_image = atlas_image.crop((x0, y0, x1, y1))
        
        # 7. "Prime" a new DDE instance
        dde = DDEPirouette()
        
        dde.manifest[module_id] = module_info
        dde.vocab = original_manifest_data['vocab']
        dde.reverse_vocab = {
            int(k): v for k, v in original_manifest_data['reverse_vocab'].items()
        }

        # 8. Decode the cropped tile
        print("\n" + "─" * 70)
        print(f"💧 REHYDRATING: {module_id}")
        print("─" * 70)
        
        reconstructed_df = dde.decode(tile_image, module_id)
        
        print("\n✅ Rehydration Complete. DataFrame:")
        print(reconstructed_df.to_string())


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("="*70)
        print("DDE Atlas Reader v2.0 (Minified-Aware)")
        print("="*70)
        print("Usage: python read_atlas_v2.py <path_to_glob_manifest.json> <MODULE_ID>")
        print("\nExample:")
        print('  python read_atlas_v2.py dde_glob_manifest_modules_outbox.json "CORE-001_THE_PIROUETTE_SEED"')
        print("="*70)
        sys.exit(1)
        
    manifest_file = sys.argv[1]
    module_to_find = sys.argv[2].upper()
    
    rehydrate_module(manifest_file, module_to_find)