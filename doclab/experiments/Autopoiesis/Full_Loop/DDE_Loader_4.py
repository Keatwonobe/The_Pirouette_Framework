"""
DDE-Pirouette Folder Synchronizer v4.0
- Ingests all .md files from a folder
- Saves the corresponding .png image tiles
- Accepts a master vocabulary file to "prime" the DDE
- Adds a --minify flag to save a compact, AI-readable JSON
"""

import sys
import numpy as np
from pathlib import Path
# Import the new v7.3 class
from DDE_Pirouette import DDEPirouette, PirouetteMetadata, FAISS_AVAILABLE
import os
import argparse 

def sync_folder_to_dde(folder_path_str: str, master_vocab_path: str = None, save_minified: bool = False):
    """
    Ingests all .md files from a target folder into a new DDE instance.
    """
    
    folder_path = Path(folder_path_str)
    if not folder_path.is_dir():
        print(f"❌ Error: Path '{folder_path_str}' is not a valid directory.")
        return

    domain_name = folder_path.name.upper()
    db_label = folder_path.name
    
    img_folder_name = f"dde_img_{db_label}"
    img_folder_path = Path.cwd() / img_folder_name
    os.makedirs(img_folder_path, exist_ok=True)
    print(f"🖼️  Saving all generated images into: ./{img_folder_name}/")
    
    print("=" * 70)
    print(f"🌱 INITIALIZING NEW DDE INSTANCE for: {db_label}")
    print(f"   Domain: {domain_name}")
    print("=" * 70)
    
    dde = DDEPirouette(patch_size=8)
    
    if master_vocab_path:
        dde.prime_vocabulary_from_file(master_vocab_path)
    else:
        print("🧬 No master vocab provided. Building vocab dynamically.")
    
    md_files = list(folder_path.glob('*.md'))
    if not md_files:
        print(f"⚠️  No markdown files found in '{folder_path_str}'.")
        return

    print(f"Found {len(md_files)} modules to ingest...")
    
    all_vectors = []
    
    print("\n" + "─" * 70)
    print("STAGE 1: INGESTING MODULES")
    print("─" * 70)
    
    for md_path in md_files:
        try:
            module_id = md_path.stem.upper()
            
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            meta = PirouetteMetadata(
                module_id=module_id,
                domain=domain_name,
                gamma_profile="medium",
                parents=[],
                temporal_adherence=0.8
            )
            
            img = dde.ingest_pirouette_module(
                content,
                module_id=module_id,
                domain=domain_name,
                gamma_profile="medium",
                parents=[]
            )
            
            img_save_path = img_folder_path / f"{module_id}.png"
            img.save(img_save_path)
            
            residue = dde.dark_residue(module_id, energy_kwh=0.0001)
            dde.manifest[module_id]["dark_residue"] = residue
            
            if FAISS_AVAILABLE:
                vectors = dde.vectorize(img, module_id)
                all_vectors.append(vectors)
            
            print(f"  ✅ Ingested: {md_path.name} (Image: {img_save_path.name})")
        
        except Exception as e:
            print(f"  ❌ FAILED to ingest {md_path.name}: {e}")
            
    if FAISS_AVAILABLE and all_vectors:
        print("\n" + "─" * 70)
        print(f"STAGE 2: BUILDING COHERENCE ({len(all_vectors)} modules)")
        print("─" * 70)
        
        all_vectors_np = np.concatenate(all_vectors, axis=0)
        n_clusters = max(1, min(16, len(all_vectors) // 4)) 
        
        dde.build_index(use_gpu=False, n_clusters=n_clusters)
        dde.add_to_index(all_vectors_np)
        
        print("\n" + "─" * 70)
        print("STAGE 3: AUTOPOIETIC ANNEALING")
        print("─" * 70)
        
        dde.run_evolution(n_cycles=3, budget_per_cycle=0.01)

    print("\n" + "─" * 70)
    print("STAGE 4: SAVING DATABASE MANIFEST")
    print("─" * 70)
    
    output_filename = f"dde_db_{db_label}.json"
    
    # --- NEW: Save minified or full ---
    if save_minified:
        dde.save_manifest_minified(output_filename)
    else:
        dde.save_manifest(output_filename) # The full, bloated version
    # ----------------------------------
    
    print(f"\n🎉 SUCCESS! 🎉")
    print(f"   Manifest: {output_filename}")
    print(f"   Images:   ./{img_folder_name}/")
    print(f"   Vocab items: {len(dde.vocab)}")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DDE Folder Synchronizer v4.0 (Minified)"
    )
    parser.add_argument(
        "folder_path", 
        type=str, 
        help="Path to the folder of .md modules to ingest."
    )
    parser.add_argument(
        "--vocab", 
        type=str, 
        dest="vocab_file",
        help="Optional: Path to a .txt master vocabulary file (one word per line)."
    )
    # --- NEW FLAG ---
    parser.add_argument(
        "--minify",
        action="store_true",
        help="Save the output manifest in a minified, compact format."
    )
    
    args = parser.parse_args()
        
    sync_folder_to_dde(args.folder_path, args.vocab_file, args.minify)